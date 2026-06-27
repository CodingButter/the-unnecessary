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
  2. RENDER: for every chunk missing its chunk_dir/NN.wav, call renderer.render_chunk
     (the proactive sentence-split renderer). Existing NN.wav are skipped (resume-safe);
     a render error is logged and left as a missing wav -- QC will mark it RETRY and the
     auto-fix loop will re-render it.
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


def render_missing(chunks, chunk_dir, api, voice, auth, rep_penalty, base_temp, max_temp,
                   edge_pad, split_threshold):
    """Render every chunk that has no chunk_dir/NN.wav yet (resume-safe), via
    renderer.render_chunk (proactive sentence split). Returns the count freshly rendered.
    A render error is logged and the wav is left missing -- the QC pass will mark that chunk
    RETRY and the auto-fix loop owns the recovery, so one failed chunk never aborts the run."""
    os.makedirs(chunk_dir, exist_ok=True)
    rendered = 0
    n = len(chunks)
    for i, ch in enumerate(chunks, 1):
        cf = os.path.join(chunk_dir, "%02d.wav" % i)
        prof = ch["profile"]
        if os.path.exists(cf):
            log("  chunk %02d/%d  [%s]  skip (exists)"
                % (i, n, renderer.profile_str(prof)))
            continue
        log("  chunk %02d/%d  [%s]  %d chars ..."
            % (i, n, renderer.profile_str(prof), len(ch["text"])))
        err, dur = renderer.render_chunk(api, voice, prof, ch["text"], cf, auth,
                                         rep_penalty, base_temp, max_temp,
                                         edge_pad=edge_pad, split_threshold=split_threshold)
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

    # --- 2. RENDER any missing chunks ---------------------------------------------------
    log("--- RENDER: %d chunk(s) (skipping any already on disk) ---" % n)
    rendered = render_missing(chunks, chunk_dir, args.api, args.voice, auth,
                              args.repetition_penalty, args.temperature, args.max_temp,
                              args.edge_pad, args.split_threshold)
    log("RENDER done: %d freshly rendered, %d already existed." % (rendered, n - rendered))

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
                edge_pad=args.edge_pad, split_threshold=thr)
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
