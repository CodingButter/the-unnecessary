#!/usr/bin/env python3
"""HANDS-OFF chapter narration orchestrator: narration script in, verified mp3 + qc.json
out, zero manual steps.

This ties the two single-purpose tools together so a human never has to babysit a
render. It drives:

  * scripts/narrate-chapter-voiceserver.py  (the RENDERER)  -- builds the chunk plan,
    renders each chunk via the self-hosted Chatterbox voice server, proactively splitting
    long chunks, and stitches/masters the final file.
  * scripts/verify-narration.py             (the VERIFIER)  -- transcribes each chunk WAV,
    scores it against the text it was meant to say, and returns a per-chunk verdict
    (OK / REVIEW / RETRY) plus a Whisper-INDEPENDENT speech-length tripwire, writing
    qc.json / qc.csv.

Both filenames are hyphenated (not importable as normal modules), so they are loaded via
importlib.util.spec_from_file_location -- exactly how the verifier already loads the
renderer. We reuse the modules' PUBLIC functions; nothing is reimplemented, so the chunk
list, auth, and scoring stay byte-identical to running the two tools by hand.

FLOW (strictly sequential -- the voice server is single-instance; the whole thing is
resumable and HONEST about what it could not fix):

  1. Build the chunk list and derive chunk_dir EXACTLY as the renderer's main() does
     (extract_performance -> build_segments -> build_chunks -> normalize_ellipses, then
     out/chunk_dir derivation). Resolve HTTP Basic auth; health-check the server.
  2. RENDER: for EVERY chunk, call renderer.render_chunk (the proactive sentence-split
     renderer), overwriting any existing chunk_dir/NN.wav -- a full fresh re-render by
     default, so a revised narration script is always re-voiced and never reuses stale
     audio. (--resume skips chunks already on disk to resume an interrupted render.) A
     render error is logged and left as-is -- QC will mark it RETRY and the auto-fix loop
     will re-render it.
  3. QC: run the verifier over ALL chunks (transcribe -> evaluate -> optional ElevenLabs
     tiebreaker on REVIEW chunks) for a per-chunk verdict + speech_len, and write
     qc.json / qc.csv. Collect the RETRY set.
  4. AUTO-FIX LOOP (--max-attempts, default 3, per chunk): for each RETRY chunk, delete
     NN.wav + NN.trimmed.wav and re-render with a LOWER split_threshold each attempt
     (attempt 1 = --split-threshold, 2 = 200, 3 = 120 -> split more aggressively for
     stubborn chunks). Re-QC ONLY the re-rendered chunks. A chunk reaching OK/REVIEW
     leaves the RETRY set; per-chunk attempt counts are tracked.
  5. Repeat (4) until the RETRY set is empty OR every remaining RETRY chunk has hit
     --max-attempts.
  6. If (and only if) zero RETRY remain, renderer.stitch_chapter -> the final mastered
     mp3/wav. The final qc.json / qc.csv is always written (the honest record).
  7. EXIT HONESTLY: exit 0 iff zero RETRY remain; otherwise exit NON-ZERO and clearly
     list the chunk(s) it could not fix after --max-attempts -- it NEVER silently stitches
     broken audio as if it were OK. REVIEW chunks (human ear) are listed separately and
     are NON-BLOCKING (they do not change the exit code). One-line summary at the end:
     "rendered N, auto-fixed M, gave-up K, review L".

Standard library only, plus the two sibling modules (which themselves need ffmpeg/ffprobe
on PATH). All progress goes to stderr; only the final file path is printed to stdout.

Usage:
  python3 scripts/render-chapter.py \
      docs/50-manuscript/book-1/chapter-01-no-signal.narrative-script.md \
      [--api http://10.0.0.213:8080] [--out audio/book-1/chapter-01-no-signal.voiceserver.mp3] \
      [--max-attempts 3] [--split-threshold 300] [--no-elevenlabs]
"""

import argparse
import importlib.util
import json
import os
import sys

# --- load the two hyphenated sibling scripts as modules -------------------------------
# Their filenames ("narrate-chapter-voiceserver.py", "verify-narration.py") are not valid
# module names, so a plain `import` is impossible; spec_from_file_location loads them from
# their paths. Each file's `if __name__ == "__main__"` guard keeps its main() from running
# at import. (The verifier itself loads its OWN copy of the renderer the same way; that is
# harmless -- the renderer module is stateless constants + pure functions.)
_HERE = os.path.dirname(os.path.abspath(__file__))


def _load_module(mod_name, filename):
    path = os.path.join(_HERE, filename)
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


renderer = _load_module("narrate_chapter_voiceserver", "narrate-chapter-voiceserver.py")
verifier = _load_module("verify_narration", "verify-narration.py")

# Default to the verifier's API (the LAN host), not the renderer's public hostname, so the
# orchestrator's transcribe + render calls share one base URL. Overridable with --api.
DEFAULT_API = "http://10.0.0.213:8080"

# Auto-fix split-threshold schedule: each successive re-render of a stubborn chunk splits
# MORE aggressively (smaller pieces drop trailing text less often). Attempt 1 reuses the
# CLI --split-threshold; later attempts step down through these. split_for_attempt() clamps
# so the value is always non-increasing and never exceeds the CLI threshold.
_SPLIT_STEPS = [200, 120]


def log(msg):
    """Single stderr logging channel (stdout is reserved for the final file path)."""
    print(msg, file=sys.stderr)


def split_for_attempt(attempt, cli_threshold):
    """split_threshold for a 1-based auto-fix attempt number.

    Attempt 1 uses the CLI --split-threshold (default 300). Attempts 2 and 3 step down
    through 200 then 120 (more aggressive splitting for chunks that keep dropping text).
    Beyond attempt 3 it keeps shrinking (floor 60). The result is clamped to <= cli_threshold
    and is monotonically non-increasing, so a small --split-threshold is never overridden
    upward by the schedule.
    """
    if attempt <= 1:
        val = cli_threshold
    elif attempt - 2 < len(_SPLIT_STEPS):
        val = _SPLIT_STEPS[attempt - 2]
    else:
        val = max(60, _SPLIT_STEPS[-1] - 30 * (attempt - 1 - len(_SPLIT_STEPS)))
    return min(val, cli_threshold)


def derive_paths(script_path, out, fmt):
    """Return (base_stem, out, chunk_dir), derived EXACTLY as the renderer's main() does:
    base_stem strips '.narrative-script'; out defaults to audio/book-1/<stem>.voiceserver.<fmt>;
    chunk_dir = <dirname(out)>/chunks/<stem>-voiceserver. Using the renderer's own derivation
    guarantees the orchestrator reads/writes the same NN.wav files the renderer would."""
    in_stem = os.path.splitext(os.path.basename(script_path))[0]
    base_stem = in_stem.replace(".narrative-script", "")
    out = out or os.path.join("audio", "book-1", base_stem, base_stem + "." + fmt)
    out_dir = os.path.dirname(out) or "."
    chunk_dir = os.path.join(out_dir, "chunks")
    return base_stem, out, chunk_dir


def build_chunk_list(script_path, max_chars, min_chars, ellipsis):
    """Build the chunk list EXACTLY as the renderer's main() does (and therefore exactly as
    the verifier re-derives it): extract_performance -> build_segments -> build_chunks ->
    normalize_ellipses applied per chunk. Returns (chunks, performance_text); each chunk is
    {profile, text, gap_after}. Built ONCE here and used for BOTH render and QC, so the two
    can never drift out of alignment regardless of flag values."""
    raw = open(script_path, "r", encoding="utf-8").read()
    text = renderer.extract_performance(raw)
    items = renderer.build_segments(text)
    chunks = renderer.build_chunks(items, max_chars, min_chars)
    for ch in chunks:
        ch["text"] = renderer.normalize_ellipses(ch["text"], ellipsis)
    return chunks, text


def render_chunks(chunks, chunk_dir, api, voice, auth, rep_penalty, base_temp, max_temp,
                  edge_pad, split_threshold, resume=False, lexicon=None):
    """Render every chunk to chunk_dir/NN.wav via renderer.render_chunk (proactive sentence
    split). DEFAULT is a full fresh re-render that OVERWRITES any existing NN.wav, so a revised
    narration script is always re-voiced and never reuses the prior render's stale audio; pass
    resume=True to skip chunks already on disk (to resume an interrupted render). Returns the
    count freshly rendered. A render error is logged and the wav is left as-is -- the QC pass
    will mark that chunk RETRY and the auto-fix loop owns the recovery, so one failed chunk
    never aborts the run."""
    os.makedirs(chunk_dir, exist_ok=True)
    rendered = 0
    n = len(chunks)
    for i, ch in enumerate(chunks, 1):
        cf = os.path.join(chunk_dir, "%02d.wav" % i)
        prof = ch["profile"]
        if resume and os.path.exists(cf):
            log("  chunk %02d/%d  [%s]  skip (--resume; exists)"
                % (i, n, renderer.profile_str(prof)))
            continue
        log("  chunk %02d/%d  [%s]  %d chars ..."
            % (i, n, renderer.profile_str(prof), len(ch["text"])))
        err, dur = renderer.render_chunk(api, voice, prof, ch["text"], cf, auth,
                                         rep_penalty, base_temp, max_temp,
                                         edge_pad=edge_pad, split_threshold=split_threshold,
                                         lexicon=lexicon)
        if err:
            log("  ERROR rendering chunk %02d: %s (left missing -> will be a RETRY)"
                % (i, err))
            continue
        rendered += 1
        dur_s = ("%.1fs audio" % dur) if dur is not None else "duration unknown"
        log("      -> %s (%s)" % (os.path.basename(cf), dur_s))
    return rendered


def qc_one(index, chunk, chunk_dir, api, language, auth, chars_per_sec, short_ratio,
           retry_threshold, no_elevenlabs, el_key):
    """Transcribe + evaluate ONE chunk and return its result dict with a FINAL verdict.

    Mirrors the verifier's main() per-chunk path: locate chunk_dir/NN.wav, transcribe (or
    record a missing/transcribe error), verifier.evaluate (score + Whisper-INDEPENDENT
    speech-length tripwire), then -- only on a provisional REVIEW and only when ElevenLabs
    is enabled and keyed -- verifier.apply_elevenlabs to resolve REVIEW into OK or RETRY.
    """
    wav = os.path.join(chunk_dir, "%02d.wav" % index)
    expected = chunk["text"]
    gap = chunk.get("gap_after", "register")
    if not os.path.exists(wav):
        res = {"index": index, "wav": wav, "expected": expected, "got": "",
               "error": "missing wav"}
    else:
        text, err = verifier.transcribe(api, wav, language, auth)
        if err is not None:
            res = {"index": index, "wav": wav, "expected": expected, "got": "",
                   "error": "transcribe failed: " + err}
        else:
            res = {"index": index, "wav": wav, "expected": expected, "got": text}
    verifier.evaluate(res, gap, chars_per_sec, short_ratio, retry_threshold)
    if res["verdict"] == "REVIEW" and not no_elevenlabs and el_key:
        _outcome, el_err = verifier.apply_elevenlabs(res, el_key, retry_threshold)
        if el_err is not None:
            log("  chunk %02d  ELEVENLABS ERROR: %s (stays REVIEW)" % (index, el_err))
    return res


def write_qc(chunk_dir, results_by_index):
    """Write qc.json (full text, every field) and qc.csv (truncated text) for ALL chunks
    via the verifier's own writers, so the schema is identical to a standalone verify run."""
    records = [verifier.qc_record(results_by_index[i]) for i in sorted(results_by_index)]
    os.makedirs(chunk_dir, exist_ok=True)
    qc_json = os.path.join(chunk_dir, "qc.json")
    qc_csv = os.path.join(chunk_dir, "qc.csv")
    verifier.write_qc_json(qc_json, records)
    verifier.write_qc_csv(qc_csv, records)
    return qc_json, qc_csv


def _verdict_line(r):
    """Compact per-chunk verdict line for stderr (mirrors the verifier's own format)."""
    def cell(v, fmt):
        return (fmt % v) if v is not None else "-"
    reason = ("  [%s]" % r["reason"]) if r.get("reason") else ""
    return ("  chunk %02d  %-6s sim=%s speech=%ss exp=%ss len=%-12s%s"
            % (r["index"], r["verdict"], cell(r.get("sim"), "%.2f"),
               cell(r.get("speech_len"), "%.1f"), cell(r.get("expected_len"), "%.1f"),
               r.get("len_status", "-"), reason))


def load_prior_qc(chunk_dir):
    """Read chunk_dir/qc.json for a targeted re-render. Returns (records_by_index, texts)
    or (None, None) if qc.json is missing/unreadable/empty (caller refuses and tells the
    user to run a full render). records_by_index maps a 1-based int to the prior qc RECORD
    dict (reused verbatim for the chunks we do NOT re-render, so the report stays complete);
    texts is the index-ordered list of each chunk's prior script_text -- the boundary-safety
    baseline compared against the freshly re-chunked text."""
    qc_json = os.path.join(chunk_dir, "qc.json")
    if not os.path.exists(qc_json):
        return None, None
    try:
        with open(qc_json, "r", encoding="utf-8") as fh:
            records = json.load(fh)
    except (ValueError, OSError):
        return None, None
    if not isinstance(records, list) or not records:
        return None, None
    by_index = {}
    for rec in records:
        if not isinstance(rec, dict):
            return None, None
        try:
            by_index[int(rec.get("chunk"))] = rec
        except (TypeError, ValueError):
            return None, None
    order = sorted(by_index)
    # A qc.json must describe a contiguous 1..N chunk set to be a safe baseline.
    if order != list(range(1, len(order) + 1)):
        return None, None
    texts = [by_index[i].get("script_text", "") for i in order]
    return by_index, texts


def _purge_chunk_derivatives(chunk_dir, i):
    """Remove chunk i's wav and its stitch-time derivatives (NN.wav, NN.trimmed.wav,
    NN.capped.wav) so a re-render leaves no stale audio for the re-stitch to pick up."""
    cf = os.path.join(chunk_dir, "%02d.wav" % i)
    base = cf[:-len(".wav")]
    for p in (cf, base + ".trimmed.wav", base + ".capped.wav"):
        try:
            os.remove(p)
        except OSError:
            pass


def write_qc_merged(chunk_dir, fresh_results, prior_records, n):
    """Write qc.json/qc.csv for ALL n chunks after a targeted re-render: the freshly
    re-QC'd selected chunks (via verifier.qc_record) take precedence; every other chunk
    keeps its prior qc RECORD verbatim, so the record stays complete and HONEST about which
    chunks were reused. Records are index-ordered. Returns (qc_json, qc_csv)."""
    records = [verifier.qc_record(fresh_results[i]) if i in fresh_results
               else prior_records[i] for i in range(1, n + 1)]
    qc_json = os.path.join(chunk_dir, "qc.json")
    qc_csv = os.path.join(chunk_dir, "qc.csv")
    verifier.write_qc_json(qc_json, records)
    verifier.write_qc_csv(qc_csv, records)
    return qc_json, qc_csv


def _render_and_qc_chunk(args, chunks, i, chunk_dir, auth, el_key, lexicon, split_threshold):
    """Re-render chunk i (purging its stale wav/derivatives first, applying the current
    lexicon+clock rule through render_chunk -> to_spoken), then re-QC just that chunk.
    Returns its result dict (with a final verdict)."""
    _purge_chunk_derivatives(chunk_dir, i)
    ch = chunks[i - 1]
    cf = os.path.join(chunk_dir, "%02d.wav" % i)
    err, dur = renderer.render_chunk(
        args.api, args.voice, ch["profile"], ch["text"], cf, auth,
        args.repetition_penalty, args.temperature, args.max_temp,
        edge_pad=args.edge_pad, split_threshold=split_threshold, lexicon=lexicon)
    if err:
        log("    ERROR rendering chunk %02d: %s (will be a RETRY)" % (i, err))
    elif dur is not None:
        log("    -> %.1fs audio" % dur)
    return qc_one(i, ch, chunk_dir, args.api, args.language, auth, args.chars_per_sec,
                  args.short_ratio, args.retry_threshold, args.no_elevenlabs, el_key)


def run_targeted(args, chunks, out, chunk_dir, auth, el_key, lexicon):
    """TARGETED re-render: re-render ONLY the selected chunks, reuse every other chunk's
    existing wav, then re-stitch the WHOLE chapter (the normal trim + interior-cap + master
    path). Returns a process exit code. See the --rerender-* flags.

    Sequence: (1) resolve the union selection; (2) boundary-safety -- the freshly re-chunked
    script must have the SAME count as qc.json and every NON-selected chunk's text must be
    unchanged, else REFUSE (run a full render); (3) re-render+re-QC each selected chunk with
    the same progressive auto-fix loop the full render uses, restricted to the selected set;
    (4) merge the fresh QC over the prior records and, only if every selected chunk is clean,
    stitch the full chapter -- never stitching broken audio."""
    n = len(chunks)
    if args.resume:
        log("ERROR: --resume cannot be combined with --rerender-* (a targeted re-render "
            "always overwrites exactly the selected chunks and reuses the rest). Pick one.")
        return 2

    # --- 1. selection: explicit indices UNION text-match -------------------------------
    try:
        idx = renderer.parse_chunk_indices(args.rerender_chunks, n)
    except ValueError as err:
        log("ERROR: --rerender-chunks: %s" % err)
        return 2
    selected = renderer.select_rerender_chunks(chunks, idx, args.rerender_matching)
    if not selected:
        log("ERROR: no chunks selected (--rerender-chunks %r / --rerender-matching %r "
            "matched none of the %d chunk(s))."
            % (args.rerender_chunks, args.rerender_matching, n))
        return 2

    # --- 2. boundary-safety: the re-chunk must line up with the existing render ---------
    prior_records, prior_texts = load_prior_qc(chunk_dir)
    if prior_texts is None:
        log("ERROR: targeted re-render needs a readable %s (a contiguous 1..N chunk set) to "
            "verify alignment; none found. Run a FULL render first."
            % os.path.join(chunk_dir, "qc.json"))
        return 2
    ok, detail = renderer.check_rerender_alignment(chunks, prior_texts, selected)
    if not ok:
        log("REFUSING targeted re-render: " + detail)
        return 2
    log("Alignment OK: " + detail)

    sel_set = set(selected)
    missing = [i for i in range(1, n + 1) if i not in sel_set
               and not os.path.exists(os.path.join(chunk_dir, "%02d.wav" % i))]
    if missing:
        log("REFUSING targeted re-render: reused (non-selected) chunk wav(s) missing on "
            "disk: %s. Run a FULL render." % ", ".join("%02d" % i for i in missing))
        return 2

    log("--- TARGETED RE-RENDER: chunk(s) %s of %d (reusing the other %d) ---"
        % (", ".join("%02d" % i for i in selected), n, n - len(selected)))

    # --- 3. re-render + re-QC the selected set, with the same progressive auto-fix ------
    results = {}
    attempts = {}
    retry_set = set()
    for i in selected:
        log("  re-render chunk %02d [%s] %d chars ..."
            % (i, renderer.profile_str(chunks[i - 1]["profile"]), len(chunks[i - 1]["text"])))
        res = _render_and_qc_chunk(args, chunks, i, chunk_dir, auth, el_key, lexicon,
                                   args.split_threshold)
        results[i] = res
        log(_verdict_line(res))
        if res["verdict"] == "RETRY":
            retry_set.add(i)

    while retry_set:
        to_fix = sorted(i for i in retry_set if attempts.get(i, 0) < args.max_attempts)
        if not to_fix:
            break                       # everyone remaining has exhausted --max-attempts
        log("--- AUTO-FIX pass: chunk(s) %s ---" % ", ".join("%02d" % i for i in to_fix))
        for i in to_fix:
            attempts[i] = attempts.get(i, 0) + 1
            thr = split_for_attempt(attempts[i], args.split_threshold)
            log("  re-render chunk %02d (attempt %d/%d, split_threshold=%d) ..."
                % (i, attempts[i], args.max_attempts, thr))
            res = _render_and_qc_chunk(args, chunks, i, chunk_dir, auth, el_key, lexicon, thr)
            results[i] = res
            log("  re-QC " + _verdict_line(res).lstrip())
            if res["verdict"] != "RETRY":
                retry_set.discard(i)

    # --- 4. merge fresh QC over the prior records; stitch only when clean ----------------
    qc_json, qc_csv = write_qc_merged(chunk_dir, results, prior_records, n)
    gave_up = sorted(retry_set)
    review = sorted(i for i in selected if results[i]["verdict"] == "REVIEW")

    if gave_up:
        log("--- STITCH SKIPPED: selected chunk(s) %s still RETRY after %d attempt(s); "
            "refusing to stitch broken audio ---"
            % (", ".join("%02d" % i for i in gave_up), args.max_attempts))
        log("qc.json: %s" % qc_json)
        for i in gave_up:
            log("   chunk %02d: %s" % (i, results[i].get("reason") or "(no reason)"))
        return 1

    log("--- STITCH: re-rendered chunk(s) clean -> mastering the full chapter from existing "
        "+ freshly-rendered chunks ---")
    if not renderer.stitch_chapter(chunks, chunk_dir, out, args.format,
                                   args.edge_pad, args.no_edge_trim):
        log("ERROR: stitch_chapter failed (see above).")
        return 1

    log("")
    log("=== SUMMARY (targeted re-render) ===")
    log("qc.json: %s" % qc_json)
    log("qc.csv : %s" % qc_csv)
    if review:
        log("REVIEW (human ear, NON-blocking): %s" % ", ".join("%02d" % i for i in review))
    log("re-rendered %d, reused %d, review %d"
        % (len(selected), n - len(selected), len(review)))
    print(out)                          # stdout: the final mastered file path
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="HANDS-OFF chapter narration orchestrator: render the narration script "
                    "via the voice server, QC every chunk, auto-fix RETRY chunks with "
                    "progressively more aggressive splitting, then stitch -- and exit "
                    "non-zero (never silently) if any chunk could not be fixed.")
    ap.add_argument("script", help="A chapter-XX.narrative-script.md (the renderer's input)")
    ap.add_argument("--api", default=DEFAULT_API,
                    help="Voice server base URL (render + transcribe). Default %s." % DEFAULT_API)
    ap.add_argument("--out", default=None,
                    help="Final mastered file path. Default audio/book-1/<stem>.voiceserver.<fmt>.")
    ap.add_argument("--max-attempts", type=int, default=3, dest="max_attempts",
                    help="Auto-fix re-render attempts per RETRY chunk before giving up. Default 3.")
    ap.add_argument("--split-threshold", type=int, default=renderer.SPLIT_THRESHOLD,
                    dest="split_threshold",
                    help="Initial render split threshold (chars); auto-fix attempts step DOWN "
                         "from it (200, 120, ...). Default %d." % renderer.SPLIT_THRESHOLD)
    ap.add_argument("--no-elevenlabs", action="store_true", dest="no_elevenlabs",
                    help="Skip the ElevenLabs Scribe tiebreaker on REVIEW chunks (Whisper-only); "
                         "passed through to the verifier.")
    ap.add_argument("--resume", action="store_true",
                    help="Skip any chunk whose NN.wav already exists on disk, to manually resume "
                         "an interrupted render. DEFAULT (no flag) is a full fresh re-render that "
                         "overwrites every chunk -- so a revised script is always re-voiced and "
                         "never reuses stale audio.")
    # --- TARGETED re-render (explicit opt-in; either flag triggers the mode) -------------
    ap.add_argument("--rerender-chunks", default=None, dest="rerender_chunks",
                    help="TARGETED re-render: comma-separated 1-based chunk indices to re-render "
                         "(e.g. 3,7). ONLY these are re-rendered+re-QC'd; every other chunk's "
                         "existing wav is reused, then the WHOLE chapter is re-stitched. Refuses "
                         "if the script no longer aligns with the rendered chunks (run a full "
                         "render). Unioned with --rerender-matching. Full render stays the default.")
    ap.add_argument("--rerender-matching", default=None, dest="rerender_matching",
                    help="TARGETED re-render: also re-render every chunk whose SCRIPT text contains "
                         "this exact (case-sensitive) substring, e.g. '23:59' to re-voice every "
                         "chunk touched by a clock-time/lexicon fix. Unioned with --rerender-chunks.")
    # --- shared render+QC knobs (defaults mirror the two modules so chunks stay aligned) ---
    ap.add_argument("--voice", default="Will_Wheaton")
    ap.add_argument("--format", default="mp3", choices=["mp3", "wav"])
    ap.add_argument("--max-chars", type=int, default=2000, dest="max_chars",
                    help="Per-chunk cap; used for BOTH render and QC chunking. Default 2000.")
    ap.add_argument("--min-chars", type=int, default=280, dest="min_chars",
                    help="Sub-min absorb threshold; used for BOTH render and QC. Default 280.")
    ap.add_argument("--ellipsis", default="comma",
                    choices=["comma", "period", "drop", "dotdot", "keep"],
                    help="Ellipsis handling; used for BOTH render and QC. Default comma.")
    ap.add_argument("--repetition-penalty", type=float, default=1.2, dest="repetition_penalty")
    ap.add_argument("--temperature", type=float, default=0.7,
                    help="Base temperature for chunks whose tag profile sets none. Default 0.7.")
    ap.add_argument("--max-temp", type=float, default=0.8, dest="max_temp",
                    help="Hard ceiling on every chunk's temperature. Default 0.8.")
    ap.add_argument("--edge-pad", type=float, default=0.05, dest="edge_pad")
    ap.add_argument("--no-edge-trim", action="store_true", dest="no_edge_trim")
    ap.add_argument("--lexicon", default=renderer.DEFAULT_LEXICON,
                    help="Pronunciation lexicon JSON (surface->spoken), passed through to the "
                         "renderer and applied only to the text sent to the voice server. Default "
                         "the seeded file at %s. The 24-hour clock-time rule always applies."
                         % renderer.DEFAULT_LEXICON)
    ap.add_argument("--no-lexicon", action="store_true",
                    help="Disable the pronunciation lexicon (clock-time rule still applies).")
    ap.add_argument("--language", default="en", help="Transcription language (ISO). Default en.")
    ap.add_argument("--retry-threshold", type=float, default=0.80, dest="retry_threshold",
                    help="Similarity below which a chunk is REVIEW. Default 0.80.")
    ap.add_argument("--chars-per-sec", type=float, default=16.0, dest="chars_per_sec",
                    help="Clean-narration rate for the speech-length tripwire. Default 16.0.")
    ap.add_argument("--short-ratio", type=float, default=0.6, dest="short_ratio",
                    help="Chunk is SHORT (a drop -> RETRY) when speech_len < ratio*expected_len. "
                         "Default 0.6.")
    ap.add_argument("--user", default=None,
                    help="API username for HTTP Basic auth (else VOICE_API_USER env, else .mcp.json).")
    ap.add_argument("--password", default=None,
                    help="API password for HTTP Basic auth (else VOICE_API_PASSWORD env, else .mcp.json).")
    args = ap.parse_args()

    if not os.path.exists(args.script):
        log("ERROR: script not found: " + args.script)
        return 2

    # --- 1. chunk list + paths + auth + health -----------------------------------------
    chunks, perf_text = build_chunk_list(args.script, args.max_chars, args.min_chars,
                                         args.ellipsis)
    base_stem, out, chunk_dir = derive_paths(args.script, args.out, args.format)
    n = len(chunks)
    if not chunks:
        log("ERROR: no narratable chunks derived from %s" % args.script)
        return 1

    log("Orchestrating %s: %d chars -> %d chunk(s); voice %s; api %s; out %s"
        % (base_stem, len(perf_text), n, args.voice, args.api, out))
    log("chunk_dir: %s" % chunk_dir)

    user, pw = renderer.resolve_credentials(args.user, args.password)
    auth = renderer.auth_header(user, pw)
    if not auth:
        log("WARNING: no API credentials found (--user/--password, VOICE_API_USER/"
            "VOICE_API_PASSWORD env, or .mcp.json); protected /api/* calls will 401.")
    else:
        log("Auth: HTTP Basic as %s" % user)

    ok, detail = renderer.healthz(args.api)
    log(("Health: %s" % detail) if ok
        else ("WARNING: health check failed (%s): %s" % (args.api, detail)))

    el_key = None
    if not args.no_elevenlabs:
        el_key = verifier.resolve_elevenlabs_key()
        if not el_key:
            log("WARNING: no ELEVENLABS_API_KEY (env or .mcp.json); REVIEW chunks will not "
                "be resolved by the tiebreaker (pass --no-elevenlabs to silence).")

    # Pronunciation lexicon (surface->spoken), resolved exactly as the renderer's main()
    # does via the shared renderer.resolve_lexicon so messaging/behaviour are identical.
    # Passed into every render_chunk call; the renderer applies it (plus the general
    # clock-time rule) only to the text sent to /api/generate.
    lexicon = renderer.resolve_lexicon(args.lexicon, args.no_lexicon, log)

    # --- TARGETED RE-RENDER (explicit opt-in) -------------------------------------------
    # If either --rerender-* flag is set, re-render ONLY the selected chunks, reuse the rest,
    # and re-stitch the whole chapter. The full-render default and --resume are unchanged.
    if args.rerender_chunks or args.rerender_matching:
        return run_targeted(args, chunks, out, chunk_dir, auth, el_key, lexicon)

    # --- 2. RENDER chunks ---------------------------------------------------------------
    mode = "resume (skip chunks already on disk)" if args.resume \
        else "full fresh re-render (overwrite every chunk)"
    log("--- RENDER: %d chunk(s) -- %s ---" % (n, mode))
    rendered = render_chunks(chunks, chunk_dir, args.api, args.voice, auth,
                             args.repetition_penalty, args.temperature, args.max_temp,
                             args.edge_pad, args.split_threshold, resume=args.resume,
                             lexicon=lexicon)
    log("RENDER done: %d freshly rendered, %d skipped/failed." % (rendered, n - rendered))

    # --- 3. QC every chunk --------------------------------------------------------------
    log("--- QC: transcribe + score %d chunk(s) ---" % n)
    results = {}
    for i, ch in enumerate(chunks, 1):
        res = qc_one(i, ch, chunk_dir, args.api, args.language, auth, args.chars_per_sec,
                     args.short_ratio, args.retry_threshold, args.no_elevenlabs, el_key)
        results[i] = res
        log(_verdict_line(res))
    write_qc(chunk_dir, results)

    initial_retry = set(i for i, r in results.items() if r["verdict"] == "RETRY")
    retry_set = set(initial_retry)
    log("QC done: RETRY = %s"
        % (", ".join("%02d" % i for i in sorted(retry_set)) if retry_set else "none"))

    # --- 4-5. AUTO-FIX LOOP -------------------------------------------------------------
    attempts = {}                       # chunk index -> re-render attempts made so far
    while retry_set:
        to_fix = sorted(i for i in retry_set if attempts.get(i, 0) < args.max_attempts)
        if not to_fix:
            break                       # everyone remaining has exhausted --max-attempts
        log("--- AUTO-FIX pass: chunk(s) %s ---"
            % ", ".join("%02d" % i for i in to_fix))
        progressed = []
        for i in to_fix:
            attempts[i] = attempts.get(i, 0) + 1
            thr = split_for_attempt(attempts[i], args.split_threshold)
            cf = os.path.join(chunk_dir, "%02d.wav" % i)
            trimmed = cf[:-len(".wav")] + ".trimmed.wav"
            for stale in (cf, trimmed):
                try:
                    os.remove(stale)
                except OSError:
                    pass
            ch = chunks[i - 1]
            log("  re-render chunk %02d (attempt %d/%d, split_threshold=%d, %d chars) ..."
                % (i, attempts[i], args.max_attempts, thr, len(ch["text"])))
            err, dur = renderer.render_chunk(
                args.api, args.voice, ch["profile"], ch["text"], cf, auth,
                args.repetition_penalty, args.temperature, args.max_temp,
                edge_pad=args.edge_pad, split_threshold=thr, lexicon=lexicon)
            if err:
                log("    ERROR re-rendering chunk %02d: %s (stays a RETRY)" % (i, err))
            elif dur is not None:
                log("    -> %.1fs audio" % dur)
            progressed.append(i)
        # Re-QC ONLY the chunks just re-rendered; a chunk reaching OK/REVIEW leaves RETRY.
        for i in progressed:
            res = qc_one(i, chunks[i - 1], chunk_dir, args.api, args.language, auth,
                         args.chars_per_sec, args.short_ratio, args.retry_threshold,
                         args.no_elevenlabs, el_key)
            results[i] = res
            log("  re-QC " + _verdict_line(res).lstrip())
            if res["verdict"] != "RETRY":
                retry_set.discard(i)
        write_qc(chunk_dir, results)    # keep qc.json current each pass (honest + resumable)

    gave_up = sorted(retry_set)         # still RETRY after exhausting --max-attempts
    review = sorted(i for i, r in results.items() if r["verdict"] == "REVIEW")
    auto_fixed = sorted(initial_retry - retry_set)

    # --- 6. stitch ONLY when clean ------------------------------------------------------
    qc_json, qc_csv = write_qc(chunk_dir, results)     # final, authoritative record
    stitched = False
    if not gave_up:
        log("--- STITCH: all chunks OK/REVIEW -> mastering final file ---")
        if renderer.stitch_chapter(chunks, chunk_dir, out, args.format,
                                   args.edge_pad, args.no_edge_trim):
            stitched = True
        else:
            log("ERROR: stitch_chapter failed (see above).")
    else:
        log("--- STITCH SKIPPED: %d chunk(s) still RETRY after %d attempts; refusing to "
            "stitch broken audio as if it were OK ---" % (len(gave_up), args.max_attempts))

    # --- 7. honest summary + exit -------------------------------------------------------
    log("")
    log("=== SUMMARY ===")
    log("qc.json: %s" % qc_json)
    log("qc.csv : %s" % qc_csv)
    if review:
        log("REVIEW (human ear, NON-blocking): %s"
            % ", ".join("%02d" % i for i in review))
    if gave_up:
        log("COULD NOT FIX after %d attempt(s) (BLOCKING): %s"
            % (args.max_attempts, ", ".join("%02d" % i for i in gave_up)))
        for i in gave_up:
            log("   chunk %02d: %s" % (i, results[i].get("reason") or "(no reason)"))
    log("rendered %d, auto-fixed %d, gave-up %d, review %d"
        % (rendered, len(auto_fixed), len(gave_up), len(review)))

    if gave_up:
        return 1                        # NON-ZERO: broken chunks remain, not stitched
    if not stitched:
        return 1                        # clean QC but stitch failed -> still a failure
    print(out)                          # stdout: the final mastered file path
    return 0


if __name__ == "__main__":
    sys.exit(main())
