#!/usr/bin/env python3
"""Narrate a chapter narration-script to one file via the self-hosted voice server (Chatterbox).

This is the Chatterbox counterpart to narrate-chapter.py (which targets ElevenLabs
v3). Chatterbox has NO inline [audio tags], so instead of passing the tags through
verbatim, this script REUSES the same v3-style "## Performance Script" markup and
maps each bracketed tag to a voice-server performance profile (emotion + tuning
knobs). The tags are then STRIPPED from the spoken text and replaced with per-chunk
synthesis settings.

Pipeline:
  1. Extract the "## Performance Script" section, preserving [tags] and the `---`
     scene-break lines (front matter and any later ## section are dropped).
  2. Walk the text into (profile, text) segments: a run of bracket tags sets the
     active profile (TAG_PRESETS merged in order, later keys win, None-mapped tags
     ignored); that profile holds for the following prose until the next tag run.
  3. Smart-chunk: coalesce consecutive same-profile segments into one chunk, capped
     at --max-chars by splitting too-long runs at sentence boundaries. A `---` line
     forces a chunk boundary (and a larger inter-chunk silence). Chunk boundaries
     therefore fall at real register changes or the size cap.
  4. Strip all [tags] from each chunk's text, collapse whitespace, skip if empty.
  5. Render each chunk via POST {API}/api/generate (format wav, normalize true),
     sequentially (the server 502s on parallel requests), resumable (skip existing
     chunk files), retrying on 5xx up to 3 times, 600s timeout per request.
  6. Stitch chunk WAVs with ffmpeg's concat demuxer, inserting a silence WAV between
     chunks (~0.35s default, ~1.2s at scene breaks). Convert to --format for --out.

  --dry-run prints the chunk PLAN and makes no API calls.

Standard library only (plus ffmpeg on PATH for silence + concat + convert). The API
has no auth.

Usage:
  python3 scripts/narrate-chapter-voiceserver.py \
      docs/50-manuscript/book-1/chapter-01-no-signal.narrative-script.md \
      [--voice Will_Wheaton] [--out audio/book-1/chapter-01-no-signal.voiceserver.mp3] \
      [--format mp3] [--max-chars 2000] [--api http://tts.codingbutter.com] [--dry-run]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error

DEFAULT_API = "http://tts.codingbutter.com"
SAMPLE_RATE = 24000

# Silence to keep at each chunk edge after trimming the leading/trailing dead air
# Chatterbox bakes into every WAV (~0.25-0.34s). Trimming both edges to this small pad
# is what makes the renderer's DECLARED inter-chunk gaps (register/beat/hold/scene)
# actually exact: an actual boundary pause becomes ~EDGE_PAD + gap + EDGE_PAD instead
# of trailing(~0.3s) + gap + leading(~0.3s).
EDGE_PAD = 0.05

# Four REGISTERS anchored on the server's "audiobook" preset. No "emotion" key: the
# emotion presets (plus repetition_penalty 1.4) manufactured non-speech garble. These
# are knobs only, every value inside the stable range (exaggeration <= 0.6,
# temperature <= 0.75). Each register is a coarse mode the chunker coalesces on; tags
# map onto these four, and unknown tags fall back to BASE via resolve_profile.
BASE  = {"register": "base",  "exaggeration": 0.4, "cfg_weight": 0.6,  "temperature": 0.7}   # audiobook preset; the weary, controlled default narration voice
FLAT  = {"register": "flat",  "exaggeration": 0.3, "cfg_weight": 0.65, "temperature": 0.6}   # automated corporate notices, machine-cold (the calm is the threat)
TENSE = {"register": "tense", "exaggeration": 0.6, "cfg_weight": 0.55, "temperature": 0.75}  # strained dialogue, the breaking link
GRAVE = {"register": "grave", "exaggeration": 0.4, "cfg_weight": 0.65, "temperature": 0.55}  # deliberate heavy landings, the final line (slow weight, not volume)

# Map each v3-style narration tag onto one of the four registers (or None for pure
# pacing). Same tag KEYS as before so existing narration scripts still parse. Use
# dict(...) copies so a tag run never mutates the shared register dicts at runtime.
TAG_PRESETS = {
    # FLAT: automated corporate / machine register.
    "flat":            dict(FLAT),
    "monotone":        dict(FLAT),
    "cold":            dict(FLAT),
    # TENSE: strained dialogue, a failing link, clipped insistence.
    "tense":           dict(TENSE),
    "strained":        dict(TENSE),
    "breaking up":     dict(TENSE),
    "glitching":       dict(TENSE),
    "clipped":         dict(TENSE),
    "insistent":       dict(TENSE),
    "emphatic":        dict(TENSE),
    "probing":         dict(TENSE),
    # GRAVE: deliberate heavy landings, the final line.
    "slowly":          dict(GRAVE),
    "drawn out":       dict(GRAVE),
    "heavy":           dict(GRAVE),
    "hollow":          dict(GRAVE),
    "sad":             dict(GRAVE),
    "grim":            dict(GRAVE),
    "faint":           dict(GRAVE),
    # BASE: the weary, controlled default narration voice.
    "measured":        dict(BASE),
    "steady":          dict(BASE),
    "observant":       dict(BASE),
    "observing":       dict(BASE),
    "matter-of-fact":  dict(BASE),
    "weary":           dict(BASE),
    "tired":           dict(BASE),
    "quiet":           dict(BASE),
    "soft":            dict(BASE),
    "softly":          dict(BASE),
    "clear":           dict(BASE),
    "appreciative":    dict(BASE),
    "dry":             dict(BASE),
    "dryly":           dict(BASE),
    "careful":         dict(BASE),
    "troubled":        dict(BASE),
    "unsettled":       dict(BASE),
    "guarded":         dict(BASE),
    "wryly":           dict(BASE),
    # Pure-pacing tags: no profile change.
    "a beat":          None,
    "beat":            None,
    "pause":           None,
}

# Fallback for any tag not in TAG_PRESETS: the audiobook base register.
DEFAULT_PROFILE = dict(BASE)

# PACING ENGINE -- deliberate pauses become CHUNK BOUNDARIES whose silence length is
# DECLARED by the script. Each boundary has a "gap kind"; the stitch step inserts
# exactly this much silence between the chunks it separates. Tunable named constants.
GAP_SECONDS = {
    "register": 0.15,   # a plain register/size boundary -- near-seamless
    "beat":     0.4,    # a short breath, marked [beat] (aliases: [a beat], [pause])
    "hold":     1.0,    # a deliberate weighted pause, marked [hold]
    "scene":    1.8,    # a --- scene break
}

# Pause tags (tag name -> gap kind). These mark a deliberate boundary and a declared
# silence; they do NOT change register. In a single tag run "hold" outranks "beat".
PAUSE_TAGS = {"beat": "beat", "a beat": "beat", "pause": "beat", "hold": "hold"}

# Matches a single bracketed tag, e.g. [weary] or [breaking up].
TAG_RE = re.compile(r'\[([^\[\]]+)\]')


def _strip_markdown(s):
    """Drop markdown emphasis/code markers but KEEP [tags] and ellipses."""
    return s.replace("**", "").replace("*", "").replace("`", "")


def extract_performance(md_text):
    """Return the spoken text from a narration script: drop front matter, keep ONLY
    what is under the '## Performance Script' heading (up to the next ## section),
    and preserve [tags] and the `---` scene-break lines verbatim."""
    text = md_text
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            text = text[end + 4:]
    marker = re.search(r'^##\s+Performance Script\s*$', text, re.M)
    if marker:
        text = text[marker.end():]
        nxt = re.search(r'^##\s+\S', text, re.M)   # stop before any later section (e.g. an adjudication log)
        if nxt:
            text = text[:nxt.start()]
    out_lines = []
    for line in text.split("\n"):
        s = line.strip()
        if s == "---":                 # scene break: keep as its own marker line
            out_lines.append("---")
            continue
        if re.match(r'^#{1,6}\s', s):   # stray sub-heading -> not spoken
            continue
        out_lines.append(_strip_markdown(s))   # keeps [tags] and ellipses
    text = "\n".join(out_lines)
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def resolve_profile(tags):
    """Merge a run of tag names into one resolved profile dict. Tags are applied in
    order (later keys win); tags mapped to None are ignored. Returns None if every
    tag in the run is pure-pacing (None) -> caller keeps the active profile."""
    merged = {}
    saw_real = False
    for name in tags:
        preset = TAG_PRESETS.get(name.strip().lower(), DEFAULT_PROFILE)
        if preset is None:
            continue
        saw_real = True
        merged.update(preset)
    return merged if saw_real else None


def _pause_kind(tags):
    """Return the heaviest pause gap kind present in a tag run, or None. A run may mix
    pause tags with registers; only the pause tags are considered, and 'hold' (the
    weighted pause) outranks 'beat' (the short breath)."""
    kinds = [PAUSE_TAGS[t.strip().lower()] for t in tags
             if t.strip().lower() in PAUSE_TAGS]
    if not kinds:
        return None
    return "hold" if "hold" in kinds else "beat"


def build_segments(text):
    """Walk the performance text into a list of items. Each item is either:
      ("break",)                 -- a scene break (`---` on its own line),
      ("pause", kind)            -- a deliberate pause ([beat]/[a beat]/[pause]/[hold]),
      ("seg", profile, prose)    -- prose with its resolved profile dict.

    A run of one or more bracket tags at a point may BOTH declare a pause and set the
    active register: pause tags emit a ("pause", kind) item at that position, while the
    non-pause tags update the active profile (which persists for the following prose
    until the next tag run). resolve_profile already ignores pause tags (mapped to
    None), so "[hold] [tense] He said" yields ("pause","hold") then a tense seg. The
    very first prose before any tag uses DEFAULT_PROFILE.
    """
    items = []
    active = dict(DEFAULT_PROFILE)

    def apply_tags(tags):
        """Emit any pause item for this tag run, then fold its registers into `active`."""
        nonlocal active
        if not tags:
            return
        kind = _pause_kind(tags)
        if kind is not None:
            items.append(("pause", kind))
        prof = resolve_profile(tags)   # pause tags map to None and are ignored here
        if prof is not None:
            active = prof

    # Process line by line so `---` boundaries are preserved.
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if line == "":
            continue
        if line == "---":
            items.append(("break",))
            continue
        # Within a line, alternate between [tag runs] and prose spans.
        pos = 0
        pending_tags = []
        for m in TAG_RE.finditer(line):
            # Prose before this tag (belongs to the currently active profile).
            pre = line[pos:m.start()].strip()
            if pre:
                # Any tags collected immediately before this prose apply now.
                apply_tags(pending_tags)
                pending_tags = []
                items.append(("seg", dict(active), pre))
            pending_tags.append(m.group(1))
            pos = m.end()
        # Trailing prose after the last tag on the line.
        tail = line[pos:].strip()
        apply_tags(pending_tags)
        pending_tags = []
        if tail:
            items.append(("seg", dict(active), tail))
    return items


def _strip_tags(s):
    """Remove all [tags] from prose, keep ellipses/punctuation, collapse whitespace."""
    s = TAG_RE.sub(" ", s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def normalize_ellipses(s, mode="comma"):
    """Chatterbox renders '...' as runaway multi-second pauses (chunk 2 produced a
    6.3s and a 27.6s gap). Convert ellipses to standard punctuation it paces on
    naturally. Modes:
      comma  - ellipsis becomes a comma-length pause (default; smoothest flow)
      period - ellipsis becomes a sentence-length pause
      drop   - remove ellipses entirely
      dotdot - collapse to '..' (experimental; for A/B comparison only)
      keep   - leave '...' untouched
    """
    s = s.replace("…", "...")                 # unicode ellipsis -> three dots
    if mode == "keep":
        return s
    if mode == "dotdot":
        return re.sub(r'\.{3,}', '..', s)
    # Absorb an ellipsis that follows existing punctuation into that punctuation.
    s = re.sub(r',\s*\.{2,}', ',', s)              # ",..." -> ","
    s = re.sub(r'([.!?;:])\s+\.{2,}', r'\1', s)    # ". ..." -> "." (need a space, else a bare "..." self-matches)
    if mode == "drop":
        s = re.sub(r'\s*\.{2,}\s*', ' ', s)
    elif mode == "period":
        s = re.sub(r'\s*\.{2,}', '.', s)           # "word..." -> "word."
    else:  # comma
        s = re.sub(r'\s*\.{2,}', ',', s)           # "word..." -> "word,"
    # Tidy any doubled/leading punctuation the substitutions may have produced.
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s+([,.!?;:])', r'\1', s)         # no space before punctuation
    s = re.sub(r',(\s*[,.!?;:])', r'\1', s)        # ",." / ",," -> drop the comma
    s = re.sub(r'^[\s,]+', '', s)                  # no leading comma/space
    return s.strip()


def _split_sentences(s, limit):
    """Split prose at sentence boundaries ([.!?]) into pieces no longer than limit."""
    sentences = re.split(r'(?<=[.!?])\s+', s)
    pieces = []
    buf = ""
    for sent in sentences:
        if len(buf) + len(sent) + 1 > limit and buf:
            pieces.append(buf.strip())
            buf = ""
        buf = (buf + " " + sent).strip()
    if buf:
        pieces.append(buf.strip())
    return pieces


def _register_of(profile):
    return (profile or {}).get("register", "base")


def _dominant_profile(segs):
    """Pick the profile (from a chunk's segments) covering the most characters."""
    by = {}
    for prof, prose in segs:
        key = json.dumps(prof, sort_keys=True)
        slot = by.setdefault(key, [prof, 0])
        slot[1] += len(prose)
    best, best_len = DEFAULT_PROFILE, -1
    for prof, ln in by.values():
        if ln > best_len:
            best, best_len = prof, ln
    return best


def build_chunks(items, max_chars, min_chars):
    """Coalesce segments into a small number of register-blocks for the voice server.

    Pass 1: split on scene breaks; within a block, coalesce consecutive segments that
    share a REGISTER (the coarse mode) up to --max-chars; a single oversized
    segment is split at sentence boundaries.
    Pass 2: absorb any chunk shorter than --min-chars into its previous neighbour
    (never across a scene break), so single-word tag flickers do not each become an
    API call. Each final chunk's tuning is the profile covering the most characters.

    A ("break",) forces a boundary with gap_after="scene"; a ("pause", kind) forces a
    boundary with gap_after=kind ("beat"/"hold"); a normal flush (register change or
    max-chars) leaves gap_after="register".

    Returns list of {profile, text, gap_after}.
    """
    raw = []            # each: {"segs": [(profile, prose)], "gap_after": str}
    cur, cur_reg, cur_len = [], None, 0

    def flush(gap="register"):
        nonlocal cur, cur_reg, cur_len
        if cur:
            raw.append({"segs": cur, "gap_after": gap})
        cur, cur_reg, cur_len = [], None, 0

    for item in items:
        if item[0] == "break":
            if cur:
                flush(gap="scene")
            elif raw:
                raw[-1]["gap_after"] = "scene"
            continue
        if item[0] == "pause":
            kind = item[1]
            if cur:
                flush(gap=kind)
            elif raw:
                raw[-1]["gap_after"] = kind
            continue
        _, prof, prose = item
        prose = _strip_tags(prose)
        if not prose:
            continue
        if len(prose) > max_chars:          # oversized single segment -> sentence split
            if cur:
                flush()
            for piece in _split_sentences(prose, max_chars):
                raw.append({"segs": [(prof, piece)], "gap_after": "register"})
            continue
        reg = _register_of(prof)
        if cur and (reg != cur_reg or cur_len + len(prose) + 1 > max_chars):
            flush()
        cur.append((prof, prose))
        cur_reg = reg
        cur_len += len(prose) + 1
    flush()

    # Pass 2: absorb sub-min chunks into the previous chunk (only when the boundary
    # between them is an ordinary "register" gap -- never erase a declared pause/break).
    merged = []
    for ch in raw:
        ch_len = sum(len(p) for _, p in ch["segs"])
        prev_len = sum(len(p) for _, p in merged[-1]["segs"]) if merged else 0
        if (merged and ch_len < min_chars and merged[-1]["gap_after"] == "register"
                and prev_len + ch_len <= max_chars):
            merged[-1]["segs"].extend(ch["segs"])
            merged[-1]["gap_after"] = ch["gap_after"]
        else:
            merged.append(ch)

    out = []
    for ch in merged:
        text = re.sub(r'\s+', ' ', " ".join(p for _, p in ch["segs"])).strip()
        if text:
            out.append({"profile": _dominant_profile(ch["segs"]),
                        "text": text, "gap_after": ch["gap_after"]})
    return out


def healthz(api):
    """Return (ok, detail). Hits GET {api}/healthz."""
    url = api.rstrip("/") + "/healthz"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            body = resp.read().decode("utf-8", "replace")
        try:
            data = json.loads(body)
            return (data.get("status") == "ok", body.strip())
        except ValueError:
            return (False, body.strip()[:200])
    except Exception as err:  # noqa: BLE001
        return (False, str(err)[:200])


def generate(api, voice, profile, text, out_path, rep_penalty=None,
             base_temp=0.6, max_temp=0.8):
    """POST one chunk to /api/generate -> WAV on disk. Returns (None, duration_secs)
    on success or (error_string, None). Retries on 5xx up to 3 times."""
    url = api.rstrip("/") + "/api/generate"
    payload = {"voice": voice, "text": text, "format": "wav", "normalize": True}
    if rep_penalty is not None:
        payload["repetition_penalty"] = rep_penalty
    payload.update(profile or {})
    # The /api/generate endpoint only accepts voice/text/format/normalize/exaggeration/
    # cfg_weight/temperature/repetition_penalty; "register" is our internal coalescing
    # key (and "emotion" is the retired model). Strip both before sending.
    payload.pop("register", None)
    payload.pop("emotion", None)
    # Temperature drives Chatterbox's randomness, and high temperature is where the
    # non-speech "garble" artifacts come from. Give EVERY chunk an explicit, steady
    # temperature: the profile's own value if it set one, else base_temp, then clamp
    # to max_temp so nothing reaches the unstable >=0.85 zone the API docs warn about.
    temp = profile.get("temperature") if profile else None
    if temp is None:
        temp = base_temp
    payload["temperature"] = min(float(temp), max_temp)
    body = json.dumps(payload).encode("utf-8")

    last_err = None
    for attempt in range(1, 4):
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json", "Accept": "audio/wav"})
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                audio = resp.read()
                dur = resp.headers.get("X-Duration-Seconds")
            if not audio:
                last_err = "empty audio response"
            else:
                with open(out_path, "wb") as handle:
                    handle.write(audio)
                try:
                    dur_f = float(dur) if dur else None
                except (TypeError, ValueError):
                    dur_f = None
                return (None, dur_f)
        except urllib.error.HTTPError as err:
            detail = err.read().decode("utf-8", "replace")
            last_err = "HTTP " + str(err.code) + ": " + detail[:300]
            if 500 <= err.code < 600 and attempt < 3:
                time.sleep(2 * attempt)
                continue
            return (last_err, None)
        except Exception as err:  # noqa: BLE001
            last_err = str(err)[:300]
            if attempt < 3:
                time.sleep(2 * attempt)
                continue
            return (last_err, None)
    return (last_err or "unknown error", None)


def make_silence(path, seconds):
    """Generate a mono 24kHz WAV of `seconds` silence via ffmpeg anullsrc."""
    if os.path.exists(path):
        return True
    res = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi",
         "-i", "anullsrc=channel_layout=mono:sample_rate=%d" % SAMPLE_RATE,
         "-t", "%.3f" % seconds, "-ar", str(SAMPLE_RATE), "-ac", "1", path],
        capture_output=True, text=True)
    return res.returncode == 0


def _wav_duration(path):
    """Return the duration (seconds) of `path` via ffprobe, or None if it can't be read."""
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True)
    try:
        return float(res.stdout.strip())
    except (TypeError, ValueError):
        return None


def cap_internal_pauses(in_wav, out_wav, cap=0.7):
    """Tidy one chunk WAV in a SINGLE ffmpeg pass: (1) trim the LEADING and TRAILING
    dead air Chatterbox bakes into every clip (~0.25-0.34s) down to EDGE_PAD, and
    (2) shorten every WITHIN-CHUNK silence longer than `cap` seconds back to `cap`.
    All other audio is left sample-for-sample equivalent. Returns True on success.

    Trimming the edges is what makes the renderer's DECLARED inter-chunk gaps exact:
    an actual boundary pause becomes ~EDGE_PAD + gap + EDGE_PAD rather than
    trailing(~0.3s) + gap + leading(~0.3s) ~= gap + 0.6s.

    Method: silencedetect (noise=-38dB, small d so the ~0.3s edges register too) reports
    silence_start/silence_end pairs. We build removal windows:
      * internal: for any silence with dur > cap, remove (dur - cap) from its MIDDLE;
      * leading:  the silence beginning at ~0.0 (silence_start <= ~0.02) -- its
                  silence_end is the first-sound onset; remove [0, onset - EDGE_PAD];
      * trailing: the silence ending at ~duration (silence_end >= duration - ~0.05) --
                  its silence_start is the last-sound offset; remove
                  [offset + EDGE_PAD, duration].
    All windows are unioned, clamped to [0, duration], and degenerate (<=0 length)
    windows dropped. One aselect drops them all at once; asetpts re-stamps the PTS so
    kept samples play gaplessly. With no edges and no over-long pause, in_wav is copied.
    """
    # Small detection threshold so the short (~0.3s) edge silences also register; the
    # internal-cap logic below still only acts on silences longer than `cap`.
    det = min(EDGE_PAD, 0.04)
    res = subprocess.run(
        ["ffmpeg", "-i", in_wav, "-af",
         "silencedetect=noise=-38dB:d=%.3f" % det, "-f", "null", "-"],
        capture_output=True, text=True)
    log = res.stderr
    starts = [float(x) for x in re.findall(r'silence_start:\s*(-?[0-9.]+)', log)]
    ends = [float(x) for x in re.findall(r'silence_end:\s*(-?[0-9.]+)', log)]
    pairs = list(zip(starts, ends))

    duration = _wav_duration(in_wav)

    windows = []

    # Internal: shave the excess from the middle of any over-long silence.
    for a, b in pairs:
        dur = b - a
        if dur > cap:
            excess = dur - cap
            mid = (a + b) / 2.0
            windows.append((mid - excess / 2.0, mid + excess / 2.0))

    # Leading edge: a silence that begins at the very start of the file.
    for a, b in pairs:
        if a <= 0.02:
            onset = b
            if onset > EDGE_PAD:               # else nothing to trim
                windows.append((0.0, onset - EDGE_PAD))
            break

    # Trailing edge: a silence that runs to (within ~0.05s of) the end of the file.
    if duration is not None:
        for a, b in pairs:
            if b >= duration - 0.05:
                offset = a
                if offset < duration - EDGE_PAD:   # else nothing to trim
                    windows.append((offset + EDGE_PAD, duration))
                break

    # Clamp to [0, duration] and drop degenerate / negative-length windows.
    cleaned = []
    for w0, w1 in windows:
        if duration is not None:
            w0 = max(0.0, min(w0, duration))
            w1 = max(0.0, min(w1, duration))
        else:
            w0 = max(0.0, w0)
            w1 = max(0.0, w1)
        if w1 - w0 > 1e-6:
            cleaned.append((w0, w1))

    if not cleaned:
        shutil.copyfile(in_wav, out_wav)
        return True

    cleaned.sort()
    betweens = "+".join("between(t,%.6f,%.6f)" % (w0, w1) for w0, w1 in cleaned)
    af = "aselect='not(%s)',asetpts=N/SR/TB" % betweens
    res = subprocess.run(
        ["ffmpeg", "-y", "-i", in_wav, "-af", af,
         "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le", out_wav],
        capture_output=True, text=True)
    return res.returncode == 0


def profile_str(profile):
    """Compact human-readable rendering of a profile dict for plan/progress output."""
    if not profile:
        return "(none)"
    parts = []
    if "register" in profile:
        parts.append(profile["register"])
    for k in ("exaggeration", "cfg_weight", "temperature"):
        if k in profile:
            parts.append("%s=%s" % (k[:3], profile[k]))
    return " ".join(parts) if parts else "(none)"


def print_plan(chunks):
    """Print the dry-run chunk plan: count, profile distribution, per-chunk preview."""
    print("CHUNK PLAN: %d chunk(s)" % len(chunks), file=sys.stderr)
    dist = {}
    for ch in chunks:
        key = profile_str(ch["profile"])
        dist[key] = dist.get(key, 0) + 1
    print("Profile distribution:", file=sys.stderr)
    for key in sorted(dist, key=lambda k: (-dist[k], k)):
        print("  %3dx  %s" % (dist[key], key), file=sys.stderr)
    print("", file=sys.stderr)
    for i, ch in enumerate(chunks, 1):
        words = ch["text"].split()
        preview = " ".join(words[:8])
        if len(words) > 8:
            preview += " ..."
        flag = "" if ch["gap_after"] == "register" else "  <%s>" % ch["gap_after"]
        print("  %02d  [%-22s] %5d chars  %s%s"
              % (i, profile_str(ch["profile"]), len(ch["text"]), preview, flag),
              file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(
        description="Narrate a narration-script to one file via the self-hosted voice server (Chatterbox).")
    ap.add_argument("script", help="A chapter-XX.narrative-script.md (v3-tagged performance script)")
    ap.add_argument("--voice", default="Will_Wheaton")
    ap.add_argument("--out", default=None)
    ap.add_argument("--format", default="mp3", choices=["mp3", "wav"])
    ap.add_argument("--max-chars", type=int, default=2000,
                    help="Cap per chunk (~2 minutes of audio). Default 2000.")
    ap.add_argument("--min-chars", type=int, default=280,
                    help="Absorb chunks smaller than this into the previous block. Default 280.")
    ap.add_argument("--ellipsis", default="comma",
                    choices=["comma", "period", "drop", "dotdot", "keep"],
                    help="How to render '...' (Chatterbox mishandles it as runaway pauses). "
                         "Default comma.")
    ap.add_argument("--repetition-penalty", type=float, default=1.2,
                    help="Chatterbox repetition_penalty (1.0-2.0). Higher suppresses repeated "
                         "phrases; too high flattens prosody and manufactured garble artifacts "
                         "at 1.4. Default 1.2 (the natural value, matching the server default).")
    ap.add_argument("--temperature", type=float, default=0.7,
                    help="Base sampling temperature for chunks whose tag profile sets none. "
                         "Lower = steadier, fewer garble artifacts (~0.65-0.75 is the stable "
                         "narration zone). Default 0.7 (the audiobook base).")
    ap.add_argument("--max-temp", type=float, default=0.8,
                    help="Hard ceiling on every chunk's temperature (>=0.85 gets unstable per "
                         "the API docs); clamps any higher profile temperature down. Default 0.8.")
    ap.add_argument("--pause-cap", type=float, default=0.7,
                    help="Cap (seconds) on WITHIN-chunk silences: any internal pause "
                         "Chatterbox renders longer than this is trimmed back to it from "
                         "its middle (declared inter-chunk pauses are unaffected). "
                         "0 disables capping. Default 0.7.")
    ap.add_argument("--api", default=DEFAULT_API)
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the chunk plan and exit without calling the API.")
    args = ap.parse_args()

    if not os.path.exists(args.script):
        print("ERROR: script not found: " + args.script, file=sys.stderr)
        return 2

    raw = open(args.script, "r", encoding="utf-8").read()
    text = extract_performance(raw)
    items = build_segments(text)
    chunks = build_chunks(items, args.max_chars, args.min_chars)
    for ch in chunks:                       # Chatterbox can't read '...' (runaway pauses)
        ch["text"] = normalize_ellipses(ch["text"], args.ellipsis)

    in_stem = os.path.splitext(os.path.basename(args.script))[0]
    base_stem = in_stem.replace(".narrative-script", "")
    out = args.out or os.path.join("audio", "book-1", base_stem + ".voiceserver." + args.format)
    out_dir = os.path.dirname(out) or "."
    chunk_dir = os.path.join(out_dir, "chunks", base_stem + "-voiceserver")

    print("Narrating %s via voice server: %d chars -> %d chunk(s), voice %s, format %s"
          % (base_stem, len(text), len(chunks), args.voice, args.format), file=sys.stderr)

    if args.dry_run:
        print_plan(chunks)
        print("(dry run: no API calls made)", file=sys.stderr)
        return 0

    if not chunks:
        print("ERROR: no narratable chunks found in performance script", file=sys.stderr)
        return 1

    ok, detail = healthz(args.api)
    if not ok:
        print("WARNING: health check failed (%s): %s" % (args.api, detail), file=sys.stderr)
    else:
        print("Health: %s" % detail, file=sys.stderr)

    os.makedirs(chunk_dir, exist_ok=True)

    chunk_files = []
    for i, ch in enumerate(chunks, 1):
        cf = os.path.join(chunk_dir, "%02d.wav" % i)
        prof = ch["profile"]
        if os.path.exists(cf):
            print("  chunk %02d/%d  [%s]  skip (exists)"
                  % (i, len(chunks), profile_str(prof)), file=sys.stderr)
            chunk_files.append((cf, ch["gap_after"]))
            continue
        print("  chunk %02d/%d  [%s]  %d chars ..."
              % (i, len(chunks), profile_str(prof), len(ch["text"])), file=sys.stderr)
        err, dur = generate(args.api, args.voice, prof, ch["text"], cf, args.repetition_penalty,
                            args.temperature, args.max_temp)
        if err:
            print("ERROR on chunk %d: %s" % (i, err), file=sys.stderr)
            return 1
        dur_s = ("%.1fs audio" % dur) if dur is not None else "duration unknown"
        print("      -> %s (%s)" % (os.path.basename(cf), dur_s), file=sys.stderr)
        chunk_files.append((cf, ch["gap_after"]))

    # Pause-cap pass: tame runaway WITHIN-chunk silences. The raw NN.wav stays
    # untouched (so resume still works); NN.capped.wav is regenerated each run and is
    # what gets stitched. --pause-cap 0 disables capping and stitches the raw files.
    concat_files = []
    for cf, gap in chunk_files:
        if args.pause_cap and args.pause_cap > 0:
            capped = cf[:-len(".wav")] + ".capped.wav"
            if not cap_internal_pauses(cf, capped, args.pause_cap):
                print("ERROR: pause-cap failed for %s" % os.path.basename(cf), file=sys.stderr)
                return 1
            concat_files.append((capped, gap))
        else:
            concat_files.append((cf, gap))

    # Build one silence WAV per distinct gap kind actually used (last chunk has no
    # silence after it, so its gap is irrelevant), then the concat list.
    used_kinds = set(gap for _, gap in concat_files[:-1])
    sil_paths = {}
    for kind in sorted(used_kinds):
        sp = os.path.join(chunk_dir, "_sil_%s.wav" % kind)
        if not make_silence(sp, GAP_SECONDS[kind]):
            print("ERROR: failed to generate %s silence WAV" % kind, file=sys.stderr)
            return 1
        sil_paths[kind] = sp

    listfile = os.path.join(chunk_dir, "concat.txt")
    with open(listfile, "w", encoding="utf-8") as handle:
        for idx, (cf, gap) in enumerate(concat_files):
            handle.write("file '" + os.path.abspath(cf) + "'\n")
            if idx < len(concat_files) - 1:   # silence between, not after the last
                handle.write("file '" + os.path.abspath(sil_paths[gap]) + "'\n")

    # Concat into the final output, MASTERED with loudnorm: a consistent loudness
    # and a true-peak ceiling so peaks do not overshoot 0 dBFS and clip ("crunch")
    # when the lossy encoder reconstructs a near-full-scale signal.
    master_af = "loudnorm=I=-18:TP=-2.0:LRA=11"
    if args.format == "wav":
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
               "-af", master_af, "-ar", str(SAMPLE_RATE), "-ac", "1",
               "-c:a", "pcm_s16le", out]
    else:
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
               "-af", master_af, "-ar", str(SAMPLE_RATE), "-ac", "1",
               "-codec:a", "libmp3lame", "-q:a", "2", out]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("ffmpeg concat failed: " + res.stderr[-400:], file=sys.stderr)
        return 1
    print(out)  # stdout: the final file path
    return 0


if __name__ == "__main__":
    sys.exit(main())
