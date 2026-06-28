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
     sequentially (the server 502s on parallel requests). By DEFAULT every chunk is
     re-rendered fresh (overwriting any existing NN.wav) so a revised script is always
     re-voiced; pass --resume to skip chunks already on disk (interrupted-render resume).
     Retries on 5xx up to 3 times, 600s timeout per request.
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
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error

# Dedicated opener with an empty ProxyHandler so requests always go DIRECT, never through
# an injected http_proxy. The voice API is a direct LAN/host call; a proxy is never wanted
# here. (Harmless when no proxy is set, which is the norm.) Use _OPENER.open(...).
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
# Cloudflare WAF on the public API (voice.codingbutter.com) 403s the default python-urllib
# User-Agent; present a browser UA so generation + Whisper transcription work off-LAN too.
_OPENER.addheaders = [("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")]

DEFAULT_API = "http://voice.codingbutter.com"
SAMPLE_RATE = 24000

# PROACTIVE SPLIT: chunks longer than this (chars) intermittently DROP trailing text
# during Chatterbox generation -- the model speaks part of the chunk, then emits seconds
# of silence in place of the rest. Short pieces don't drop. render_chunk splits any
# chunk over this threshold into sentence-groups (each <= threshold), renders each
# separately, and concatenates them, so every chunk renders in full.
SPLIT_THRESHOLD = 300

# Silence (seconds) inserted BETWEEN sentence-pieces when render_chunk splits a long
# chunk. Small -- these are intra-chunk seams within one register block, not declared
# pauses (which live in GAP_SECONDS and are inserted by the chapter-level stitch).
INTRA_CHUNK_SILENCE = 0.12

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


# ------------------------------------------------------------------------------------
# PRONUNCIATION LAYER -- corrects only the text SENT to /api/generate, never the script.
#
# Two corrections, applied (in this order) by to_spoken() at render time, AFTER tags are
# stripped: (1) a GENERAL 24-hour clock-time rule that spells "HH:MM" as words so the
# server's number normalizer can't read "23:59" as "twenty-three THOUSAND fifty-nine";
# (2) a whole-word, case-sensitive LEXICON of surface->spoken respellings (e.g. proper
# nouns the model mispronounces) loaded from a JSON file. The narration .md and its
# word-for-word fidelity check are untouched -- only the rendered audio's input string is.
# ------------------------------------------------------------------------------------

# Default lexicon location (constant path string only -- no disk access at import).
DEFAULT_LEXICON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "data", "pronunciation-lexicon.json")

_ONES_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
               "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
               "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS_WORDS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty"}

# A 24-hour clock time written HH:MM. The hour is 0-23 (single- or double-digit), the
# minute exactly two digits 00-59. Negative look-around on [\d:] keeps it from matching
# inside a longer number or an H:M:S timestamp, and a two-digit minute means ratios and
# aspect ratios ("3:2", "16:9") are never touched. Only strict clock times are rewritten.
CLOCK_RE = re.compile(r'(?<![\d:])([01]?\d|2[0-3]):([0-5]\d)(?![\d:])')


def _two_digit_words(n):
    """Spell an integer 0-59 in words: 7 -> 'seven', 23 -> 'twenty-three', 40 -> 'forty'."""
    if n < 20:
        return _ONES_WORDS[n]
    tens, ones = divmod(n, 10)
    return _TENS_WORDS[tens] + ("-" + _ONES_WORDS[ones] if ones else "")


def _clock_to_words(hh, mm):
    """Spoken form of a 24-hour clock time. 23:59 -> 'twenty-three fifty-nine',
    09:05 -> 'nine oh five', 23:00 -> 'twenty-three hundred', 00:30 -> 'zero thirty'."""
    hour = _two_digit_words(hh)
    if mm == 0:
        minute = "hundred"
    elif mm < 10:
        minute = "oh " + _ONES_WORDS[mm]
    else:
        minute = _two_digit_words(mm)
    return hour + " " + minute


def normalize_clock_times(text):
    """Rewrite every 24-hour HH:MM clock time in `text` as spoken words. Returns
    (new_text, fired) where fired is a list of 'orig->spoken' strings (one per rewrite),
    for per-chunk logging. Touches nothing but strict clock times (see CLOCK_RE)."""
    fired = []

    def repl(m):
        words = _clock_to_words(int(m.group(1)), int(m.group(2)))
        fired.append("%s->%s" % (m.group(0), words))
        return words

    return CLOCK_RE.sub(repl, text), fired


def compile_lexicon(entries):
    """Compile a {surface: spoken} mapping into the ordered (regex, spoken, surface) list
    apply_lexicon consumes. Keys beginning '_' or '//' are treated as comments and skipped;
    non-string keys/values are ignored; entries are sorted longest-surface-first so a
    multi-word phrase wins over a shorter one it contains; each surface compiles to a
    WHOLE-WORD, CASE-SENSITIVE matcher so substrings are never corrupted. Factored out of
    load_lexicon so a lexicon can also be built in memory (e.g. the self-test)."""
    pairs = [(k, v) for k, v in entries.items()
             if isinstance(k, str) and isinstance(v, str)
             and not k.startswith("_") and not k.startswith("//")]
    pairs.sort(key=lambda kv: len(kv[0]), reverse=True)
    return [(re.compile(r'(?<!\w)' + re.escape(k) + r'(?!\w)'), v, k) for k, v in pairs]


def load_lexicon(path):
    """Load a pronunciation lexicon from a JSON file into the compiled list returned by
    compile_lexicon. The JSON is either a flat {surface: spoken} object or a
    {"entries": {...}} wrapper. Raises FileNotFoundError if the path is missing and
    ValueError if the JSON is malformed -- callers decide severity."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("lexicon root must be a JSON object")
    entries = data.get("entries", data)
    if not isinstance(entries, dict):
        raise ValueError("lexicon 'entries' must be a JSON object")
    return compile_lexicon(entries)


def apply_lexicon(text, lexicon):
    """Apply a compiled lexicon (from load_lexicon) to `text`. Returns (new_text, fired)
    where fired lists each surface that actually matched as 'surface->spoken' (with a
    '(xN)' suffix when it fired more than once). Matching is whole-word/case-sensitive."""
    fired = []
    for rx, spoken, surface in lexicon or []:
        new_text, n = rx.subn(lambda m, s=spoken: s, text)
        if n:
            fired.append("%s->%s%s" % (surface, spoken, (" (x%d)" % n) if n > 1 else ""))
            text = new_text
    return text, fired


def to_spoken(text, lexicon=None):
    """Transform one chunk's stripped text into the exact string SENT to /api/generate:
    first the general 24-hour clock-time rule, then the (optional) pronunciation lexicon.
    Returns (spoken, fired) -- fired is the ordered list of substitutions for per-chunk
    logging. `text` is never mutated. The clock rule always runs (it is a general server
    safety fix); `lexicon` may be None/empty to skip only the respelling step."""
    text, t_fired = normalize_clock_times(text)
    text, l_fired = apply_lexicon(text, lexicon) if lexicon else (text, [])
    return text, t_fired + l_fired


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


# ------------------------------------------------------------------------------------
# TARGETED RE-RENDER SELECTION + BOUNDARY-SAFETY (pure helpers).
#
# These support re-rendering only a FEW chunks of an already-rendered chapter and reusing
# the rest, to fix a localized issue without re-rolling the whole chapter (the TTS is
# stochastic, so re-rendering a good chunk risks regressing it). The orchestrator
# (render-chapter.py) drives the actual re-render/QC/re-stitch; these stay here, with the
# rest of the chunk logic, and are pure (no disk, no API) so they are trivially testable.
# ------------------------------------------------------------------------------------

def parse_chunk_indices(spec, n):
    """Parse a '1,3,5' chunk-index spec into a SORTED SET of 1-based ints, each validated
    in 1..n. Raises ValueError on a non-integer token or an out-of-range index. A None or
    empty spec yields an empty set."""
    out = set()
    if not spec:
        return out
    for tok in spec.split(","):
        tok = tok.strip()
        if not tok:
            continue
        try:
            i = int(tok)
        except ValueError:
            raise ValueError("not an integer chunk index: %r" % tok)
        if not (1 <= i <= n):
            raise ValueError("chunk index %d out of range 1..%d" % (i, n))
        out.add(i)
    return out


def select_rerender_chunks(chunks, indices=None, matching=None):
    """Union selection of 1-based chunk indices to re-render: the explicit `indices`
    (a set of validated ints) PLUS every chunk whose SCRIPT text (chunk['text'], i.e. the
    post-normalize_ellipses text -- the same string stored as qc.json script_text and the
    same string fed to to_spoken at render time) CONTAINS the substring `matching`
    (case-sensitive; None/'' selects nothing by text). Returns a sorted list of indices."""
    selected = set(indices or set())
    if matching:
        for i, ch in enumerate(chunks, 1):
            if matching in ch["text"]:
                selected.add(i)
    return sorted(selected)


def check_rerender_alignment(chunks, prior_texts, selected):
    """Boundary-safety gate for a targeted re-render. Confirm the freshly re-chunked
    `chunks` still line up with the already-rendered chunk set described by `prior_texts`
    (the index-ordered per-chunk script_text from qc.json), so reusing the NON-selected
    wavs is safe. Returns (ok, message).

    REFUSES (ok=False) when either:
      * the chunk COUNT differs (a broad edit added/removed chunks), or
      * any NON-selected chunk's CURRENT text != its prior text (an edit shifted a
        boundary into a chunk we were about to reuse untouched).
    `selected` is the set/list of 1-based indices being re-rendered; THEIR text is allowed
    to differ (that is the point). The refusal message names the first offending chunk and
    tells the caller to run a FULL render -- we never silently re-render a misaligned chunk.
    """
    sel = set(selected)
    n_now, n_prev = len(chunks), len(prior_texts)
    if n_now != n_prev:
        return (False,
                "chunk COUNT changed: the current script yields %d chunk(s) but the "
                "rendered chunks dir / qc.json has %d. A broad edit moved boundaries; "
                "run a FULL render." % (n_now, n_prev))
    for i in range(1, n_now + 1):
        if i in sel:
            continue
        if chunks[i - 1]["text"] != prior_texts[i - 1]:
            return (False,
                    "NON-selected chunk %02d text changed since the last render (an edit "
                    "shifted a boundary). Re-rendering only the selected chunks would "
                    "reuse a now-stale neighbour; run a FULL render." % i)
    return (True, "%d chunk(s) aligned; %d selected for re-render, %d reused"
            % (n_now, len(sel), n_now - len(sel)))


def resolve_credentials(cli_user, cli_password):
    """(user, password) for HTTP Basic auth, resolved from CLI flags, then the
    VOICE_API_USER/VOICE_API_PASSWORD env vars, then the voice block in ./.mcp.json
    (unstaged, holds the same creds). Returns (None, None) if nothing is found."""
    user = cli_user or os.environ.get("VOICE_API_USER")
    pw = cli_password or os.environ.get("VOICE_API_PASSWORD")
    if user and pw:
        return user, pw
    try:
        with open(".mcp.json", "r", encoding="utf-8") as fh:
            env = json.load(fh)["mcpServers"]["voice"]["env"]
        user = user or env.get("VOICE_API_USER")
        pw = pw or env.get("VOICE_API_PASSWORD")
    except Exception:  # noqa: BLE001  (.mcp.json missing or shaped differently)
        pass
    return user, pw


def auth_header(user, password):
    """{'Authorization': 'Basic ...'} for the given creds, or {} when either is missing."""
    if not (user and password):
        return {}
    token = base64.b64encode(("%s:%s" % (user, password)).encode("utf-8")).decode("ascii")
    return {"Authorization": "Basic " + token}


def healthz(api):
    """Return (ok, detail). Hits GET {api}/healthz."""
    url = api.rstrip("/") + "/healthz"
    try:
        with _OPENER.open(url, timeout=15) as resp:
            body = resp.read().decode("utf-8", "replace")
        try:
            data = json.loads(body)
            return (data.get("status") == "ok", body.strip())
        except ValueError:
            return (False, body.strip()[:200])
    except Exception as err:  # noqa: BLE001
        return (False, str(err)[:200])


def generate(api, voice, profile, text, out_path, rep_penalty=None,
             base_temp=0.6, max_temp=0.8, auth=None):
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
        headers = {"Content-Type": "application/json", "Accept": "audio/wav"}
        if auth:
            headers.update(auth)
        req = urllib.request.Request(url, data=body, headers=headers)
        try:
            with _OPENER.open(req, timeout=600) as resp:
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


def trim_chunk_edges(in_wav, out_wav, pad=0.05):
    """Keep ONLY the single contiguous span [onset-pad, offset+pad] of one chunk WAV,
    shaving the leading/trailing dead air Chatterbox bakes into every clip (~0.25-0.34s)
    down to `pad`. Returns True on success.

    Uses ffmpeg ATRIM, which keeps exactly ONE contiguous range -- it is STRUCTURALLY
    INCAPABLE of removing audio between the first and last word. (This replaces the old
    aselect approach, which could excise arbitrary windows from the MIDDLE of a clip and
    once ate 27-40s of speech from real chunks.)

    Trimming the edges is what makes the renderer's DECLARED inter-chunk gaps exact: an
    actual boundary pause becomes ~pad + gap + pad rather than trailing(~0.3s) + gap +
    leading(~0.3s) ~= gap + 0.6s.

    Detection: silencedetect (noise=-38dB, d=0.08) reports silence_start/silence_end
    pairs.
      * onset  = the silence_end of a LEADING silence (silence_start <= 0.03), the
                 first-sound onset; if there is no leading silence, onset = 0.0.
      * offset = the silence_start of a TRAILING silence (silence_end >= duration-0.05),
                 the last-sound offset; if there is none, offset = duration.
    Then A = max(0.0, onset - pad) and B = min(duration, offset + pad).

    GUARD (belt-and-suspenders): if B <= A, OR the kept span (B - A) is under HALF the
    chunk -- which genuine edge silence can never cause, so it signals a detection error
    -- ABORT: copy in_wav to out_wav unchanged and warn on stderr. We never remove more
    than real edge silence.

    Output is mono, 24000 Hz, pcm_s16le.
    """
    duration = _wav_duration(in_wav)
    if duration is None:
        shutil.copyfile(in_wav, out_wav)
        print("WARNING: edge-trim could not read duration of %s; copied unchanged"
              % os.path.basename(in_wav), file=sys.stderr)
        return True

    res = subprocess.run(
        ["ffmpeg", "-i", in_wav, "-af",
         "silencedetect=noise=-38dB:d=0.08", "-f", "null", "-"],
        capture_output=True, text=True)
    log = res.stderr
    starts = [float(x) for x in re.findall(r'silence_start:\s*(-?[0-9.]+)', log)]
    ends = [float(x) for x in re.findall(r'silence_end:\s*(-?[0-9.]+)', log)]
    pairs = list(zip(starts, ends))

    # Leading silence -> first-sound onset (else keep from 0.0).
    onset = 0.0
    for a, b in pairs:
        if a <= 0.03:
            onset = b
            break

    # Trailing silence -> last-sound offset (else keep to the end). Only the silence that
    # runs to EOF has silence_end at ~duration; interior silences end earlier.
    offset = duration
    for a, b in pairs:
        if b >= duration - 0.05:
            offset = a
            break

    A = max(0.0, onset - pad)
    B = min(duration, offset + pad)

    # GUARD: real edge silence can never shrink the kept span below half the chunk; if it
    # would, detection mis-fired -- pass the chunk through untouched rather than cut speech.
    if B <= A or (B - A) < 0.5 * duration:
        shutil.copyfile(in_wav, out_wav)
        print("WARNING: edge-trim aborted for %s (would keep %.2fs of %.2fs); copied unchanged"
              % (os.path.basename(in_wav), max(0.0, B - A), duration), file=sys.stderr)
        return True

    af = "atrim=start=%.6f:end=%.6f,asetpts=N/SR/TB" % (A, B)
    res = subprocess.run(
        ["ffmpeg", "-y", "-i", in_wav, "-af", af,
         "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le", out_wav],
        capture_output=True, text=True)
    return res.returncode == 0


# A single contiguous interior silence at or beyond this many seconds is an unmistakable
# TTS-hang artifact, never legitimate pacing (a within-chunk sentence/paragraph pause is
# < ~2s). cap_interior_silences ALWAYS caps such a gap, even if that removes a large
# fraction of the clip -- so a ~30s dead span is never left in the master. Well beyond the
# 0.8s detect threshold, so a normal pause can never reach it.
INTERIOR_ARTIFACT_GAP = 3.0


def _interior_cap_plan(pairs, duration, cap=0.5, artifact_gap=INTERIOR_ARTIFACT_GAP):
    """Pure (no-ffmpeg) decision for cap_interior_silences. Given detected silence
    (start, end) pairs and the clip duration, return (longs, action):

      * action 'none'  -- no silence run exceeds the cap; nothing to do.
      * action 'cap'   -- cap every long gap to `cap` seconds.
      * action 'abort' -- the removal is dominated by MANY shorter, borderline gaps with NO
                          single clear artifact gap, AND it would remove >= half the clip:
                          that pattern is the fingerprint of a silencedetect mis-fire eating
                          quiet speech, so pass the chunk through unchanged.

    A single contiguous gap >= `artifact_gap` is a trustworthy TTS-hang artifact (real speech
    is never one continuous sub-noise-floor run for that long), so its presence ALWAYS yields
    'cap' regardless of the fraction removed -- the old fraction-only guard left those ~30s
    dead gaps in the master. The anti-gutting guard now weighs ONLY the borderline removal."""
    longs = [(s, e) for s, e in pairs if e - s > cap + 0.02]
    if not longs:
        return [], "none"
    has_artifact = any((e - s) >= artifact_gap for s, e in longs)
    borderline_removed = sum((e - s) - cap for s, e in longs if (e - s) < artifact_gap)
    if not has_artifact and borderline_removed >= 0.5 * duration:
        return longs, "abort"
    return longs, "cap"


def cap_interior_silences(in_wav, out_wav, cap=0.5, detect=0.8, noise="-38dB"):
    """Compress any silence >= `detect` seconds INSIDE a chunk down to `cap` seconds.

    trim_chunk_edges only shaves the leading/trailing edges, and the pacing engine only sets
    the DECLARED inter-chunk gaps. Neither touches a pause Chatterbox sometimes invents in the
    MIDDLE of a chunk (e.g. a 3.5s dead span after a sentence) -- nor the ~30s dead span a
    hung TTS generation bakes in. This finds those gaps with silencedetect and rebuilds the
    clip with every silence kept to at most `cap` seconds.

    Like trim_chunk_edges it removes ONLY detected-silence excess via ATRIM keep-ranges, so it
    can never cut into speech; silences shorter than `detect` are left untouched (natural
    sentence pauses). Runs AFTER edge-trim on the trimmed clip, so the edges are already small.
    GUARD (see _interior_cap_plan): a single contiguous artifact gap (>= INTERIOR_ARTIFACT_GAP)
    is ALWAYS capped even if it removes a large fraction; only a removal made of many shorter
    borderline gaps that would gut half the clip aborts -- so a long TTS-hang silence is never
    left in. Output is mono, 24000 Hz, pcm_s16le. Returns True on success.
    """
    duration = _wav_duration(in_wav)
    if duration is None:
        shutil.copyfile(in_wav, out_wav)
        return True

    res = subprocess.run(
        ["ffmpeg", "-i", in_wav, "-af",
         "silencedetect=noise=%s:d=%.3f" % (noise, detect), "-f", "null", "-"],
        capture_output=True, text=True)
    log = res.stderr
    starts = [float(x) for x in re.findall(r'silence_start:\s*(-?[0-9.]+)', log)]
    ends = [float(x) for x in re.findall(r'silence_end:\s*(-?[0-9.]+)', log)]
    pairs = list(zip(starts, ends))

    # Only gaps longer than the cap need shortening; each loses its excess [s+cap, e].
    longs, action = _interior_cap_plan(pairs, duration, cap)
    if action == "none":
        shutil.copyfile(in_wav, out_wav)
        return True
    if action == "abort":
        removed = sum((e - s) - cap for s, e in longs)
        shutil.copyfile(in_wav, out_wav)
        print("WARNING: interior-cap aborted for %s (would remove %.2fs of %.2fs from many "
              "short gaps with no clear artifact gap; copied unchanged)"
              % (os.path.basename(in_wav), removed, duration), file=sys.stderr)
        return True

    # Keep-ranges = the whole clip minus each long gap's excess.
    keeps, prev = [], 0.0
    for s, e in longs:
        keeps.append((prev, s + cap))
        prev = e
    keeps.append((prev, duration))

    parts, labels = [], []
    for idx, (a, b) in enumerate(keeps):
        if b - a <= 0.001:
            continue
        parts.append("[0:a]atrim=start=%.6f:end=%.6f,asetpts=N/SR/TB[s%d]" % (a, b, idx))
        labels.append("[s%d]" % idx)
    filt = ";".join(parts) + ";" + "".join(labels) + ("concat=n=%d:v=0:a=1[out]" % len(labels))

    res = subprocess.run(
        ["ffmpeg", "-y", "-i", in_wav, "-filter_complex", filt, "-map", "[out]",
         "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le", out_wav],
        capture_output=True, text=True)
    if res.returncode != 0:
        shutil.copyfile(in_wav, out_wav)
        print("WARNING: interior-cap ffmpeg failed for %s; copied unchanged: %s"
              % (os.path.basename(in_wav), res.stderr[-200:]), file=sys.stderr)
        return True
    return True


def render_chunk(api, voice, profile, text, out_wav, auth, rep_penalty,
                 base_temp, max_temp, edge_pad=0.05, split_threshold=SPLIT_THRESHOLD,
                 lexicon=None):
    """Render ONE chunk to out_wav, PROACTIVELY splitting long text so nothing drops.

    PRONUNCIATION: before anything else, the chunk text is run through to_spoken() -- the
    general 24-hour clock-time rule plus the (optional) `lexicon` of surface->spoken
    respellings. This is the SINGLE point where the text sent to /api/generate diverges
    from the narration script; every substitution that fires is logged on stderr for this
    chunk. Splitting and length checks below operate on the transformed (sent) text. The
    clock rule always runs; pass lexicon=None to skip only the respelling step.

    Chatterbox intermittently DROPS trailing text on long chunks (>~300 chars): it
    speaks the start, then emits silence in place of the rest. Short pieces don't drop.
    So:
      * len(text) <= split_threshold -> a single generate() to out_wav (the unchanged,
        proven path; identical bytes to before).
      * len(text)  > split_threshold -> split into sentence-GROUPS each <= threshold
        (via _split_sentences: split on (?<=[.!?])\\s+, then greedily pack whole
        sentences up to the threshold; a lone sentence longer than the threshold is
        NEVER chopped -- it stays whole), generate() each group to a temp wav,
        trim_chunk_edges each, then ffmpeg-concat the trimmed pieces with a small
        INTRA_CHUNK_SILENCE seam into out_wav, and delete the temps.

    The split path's out_wav is mono / 24000 Hz / pcm_s16le -- format-identical to
    generate(), so the caller cannot tell a split chunk from a single one. Returns
    (None, duration_secs) on success or (error_string, None); the first failing piece's
    error is returned verbatim.
    """
    text, pron_fired = to_spoken(text, lexicon)
    if pron_fired:
        print("      pron: " + " | ".join(pron_fired), file=sys.stderr)
    if len(text) <= split_threshold:
        return generate(api, voice, profile, text, out_wav, rep_penalty,
                        base_temp, max_temp, auth=auth)

    groups = _split_sentences(text, split_threshold)
    tmp_dir = os.path.dirname(out_wav) or "."
    stem = os.path.splitext(os.path.basename(out_wav))[0]
    temps = []                  # every temp file to remove afterwards
    trimmed_pieces = []
    try:
        for j, grp in enumerate(groups, 1):
            raw_p = os.path.join(tmp_dir, "%s._p%02d.wav" % (stem, j))
            temps.append(raw_p)
            err, _ = generate(api, voice, profile, grp, raw_p, rep_penalty,
                              base_temp, max_temp, auth=auth)
            if err:
                return (err, None)
            trimmed_p = os.path.join(tmp_dir, "%s._p%02d.trimmed.wav" % (stem, j))
            temps.append(trimmed_p)
            if not trim_chunk_edges(raw_p, trimmed_p, edge_pad):
                return ("edge-trim failed for piece %d of %s"
                        % (j, os.path.basename(out_wav)), None)
            trimmed_pieces.append(trimmed_p)

        sil = os.path.join(tmp_dir, "%s._psil.wav" % stem)
        temps.append(sil)
        if not make_silence(sil, INTRA_CHUNK_SILENCE):
            return ("failed to make intra-chunk silence for %s"
                    % os.path.basename(out_wav), None)

        listfile = os.path.join(tmp_dir, "%s._pconcat.txt" % stem)
        temps.append(listfile)
        with open(listfile, "w", encoding="utf-8") as handle:
            for idx, tp in enumerate(trimmed_pieces):
                handle.write("file '" + os.path.abspath(tp) + "'\n")
                if idx < len(trimmed_pieces) - 1:   # silence between pieces, not after the last
                    handle.write("file '" + os.path.abspath(sil) + "'\n")

        res = subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
             "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le", out_wav],
            capture_output=True, text=True)
        if res.returncode != 0:
            return ("ffmpeg concat failed for %s: %s"
                    % (os.path.basename(out_wav), res.stderr[-300:]), None)
        return (None, _wav_duration(out_wav))
    finally:
        for p in temps:
            try:
                os.remove(p)
            except OSError:
                pass


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


def stitch_chapter(chunks, chunk_dir, out, fmt, edge_pad, no_edge_trim):
    """Stitch the already-rendered per-chunk WAVs into the final mastered file.

    Expects the rendered chunks at chunk_dir/NN.wav (01..len(chunks)); each chunk dict
    carries its 'gap_after' kind. This is exactly what main() used to do inline after
    rendering, lifted out so an orchestrator can drive render + stitch separately:

      1. Edge-trim each NN.wav -> NN.trimmed.wav (unless no_edge_trim), so the declared
         inter-chunk gaps stay exact. The raw NN.wav is left untouched (resume-safe);
         --no-edge-trim stitches the raw files directly.
      2. Build one silence WAV per distinct gap kind actually used between chunks.
      3. Write concat.txt interleaving chunk/silence, then ffmpeg-concat + loudnorm
         master (consistent loudness, true-peak ceiling so peaks never clip) to `out`.

    Returns True on success, False on failure (printing the cause to stderr, matching
    main()'s previous messages and exit behaviour).
    """
    chunk_files = [(os.path.join(chunk_dir, "%02d.wav" % i), ch["gap_after"])
                   for i, ch in enumerate(chunks, 1)]

    # Edge-trim pass: keep only the single contiguous [onset-pad, offset+pad] span of each
    # chunk, shaving the leading/trailing dead air so the declared inter-chunk gaps stay
    # exact. ATRIM keeps ONE range, so it cannot remove interior speech. The raw NN.wav
    # stays untouched (so resume still works); NN.trimmed.wav is regenerated each run and
    # is what gets stitched. --no-edge-trim stitches the raw files directly.
    concat_files = []
    for cf, gap in chunk_files:
        if no_edge_trim:
            concat_files.append((cf, gap))
        else:
            trimmed = cf[:-len(".wav")] + ".trimmed.wav"
            if not trim_chunk_edges(cf, trimmed, edge_pad):
                print("ERROR: edge-trim failed for %s" % os.path.basename(cf), file=sys.stderr)
                return False
            capped = cf[:-len(".wav")] + ".capped.wav"
            cap_interior_silences(trimmed, capped)        # shave model-invented mid-chunk pauses
            concat_files.append((capped, gap))

    # Build one silence WAV per distinct gap kind actually used (last chunk has no
    # silence after it, so its gap is irrelevant), then the concat list.
    used_kinds = set(gap for _, gap in concat_files[:-1])
    sil_paths = {}
    for kind in sorted(used_kinds):
        sp = os.path.join(chunk_dir, "_sil_%s.wav" % kind)
        if not make_silence(sp, GAP_SECONDS[kind]):
            print("ERROR: failed to generate %s silence WAV" % kind, file=sys.stderr)
            return False
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
    if fmt == "wav":
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
        return False
    return True


def _stderr_log(msg):
    """Default one-line stderr logger for resolve_lexicon."""
    print(msg, file=sys.stderr)


def resolve_lexicon(path, no_lexicon, log=_stderr_log):
    """Resolve the --lexicon / --no-lexicon flags into a compiled lexicon list (possibly
    empty). Shared by this renderer's main() and the render-chapter.py orchestrator so the
    loading + messaging behaviour is identical:
      * --no-lexicon          -> [] (the clock-time rule still applies).
      * default path missing  -> [] + WARNING (a fresh checkout may lack the file; graceful).
      * EXPLICIT path missing  -> fatal (sys.exit(2)).
      * malformed JSON         -> fatal (sys.exit(2)).
    """
    if no_lexicon:
        log("Lexicon: disabled (--no-lexicon); clock-time rule still applies.")
        return []
    try:
        lex = load_lexicon(path)
    except FileNotFoundError:
        if os.path.abspath(path) != os.path.abspath(DEFAULT_LEXICON):
            log("ERROR: --lexicon file not found: %s" % path)
            sys.exit(2)
        log("WARNING: default lexicon not found (%s); pronunciation lexicon empty "
            "(clock-time rule still applies)." % path)
        return []
    except (ValueError, KeyError) as err:
        log("ERROR: could not parse lexicon %s: %s" % (path, err))
        sys.exit(2)
    log("Lexicon: %d entr%s from %s"
        % (len(lex), "y" if len(lex) == 1 else "ies", path))
    return lex


def _run_selftest():
    """Print the transformed SPOKEN text for two canonical inputs, proving the clock-time
    rule fires and the lexicon mechanism is wired. The two required strings use the real
    SEEDED lexicon (which ships EMPTY by design); a final in-memory example lexicon then
    shows a whole-word respelling firing WITHOUT seeding any real override. Returns 0."""
    try:
        seeded = load_lexicon(DEFAULT_LEXICON)
    except Exception as err:  # noqa: BLE001
        print("selftest: could not load default lexicon (%s); using empty" % err)
        seeded = []
    print("seeded lexicon entries: %d" % len(seeded))
    for s in ["the time was 23:59.", "Marisol said"]:
        spoken, fired = to_spoken(s, seeded)
        print("IN : %r" % s)
        print("OUT: %r" % spoken)
        print("FIRED: %s" % ("; ".join(fired) if fired else "(none)"))
    example = compile_lexicon({"Marisol": "Mah-ree-sole"})   # mechanism demo, NOT seeded
    spoken, fired = to_spoken("Marisol said", example)
    print("MECH IN : %r" % "Marisol said")
    print("MECH OUT: %r  (example lexicon, not shipped)" % spoken)
    print("MECH FIRED: %s" % ("; ".join(fired) if fired else "(none)"))

    # interior-cap decision (_interior_cap_plan, the stitch's silence guard) -- offline,
    # no ffmpeg/files. The Ch3 artifact: a ~31s dead gap in a ~48s clip must be CAPPED,
    # not aborted (the old fraction-only guard left it in the master). A legitimately-paced
    # clip with many small natural pauses (no single long gap) must NOT trip; and a swarm of
    # borderline gaps that would gut half the clip with no artifact gap still aborts.
    cap_fails = []

    def _cap_expect(name, cond):
        print("  cap %-44s %s" % (name, "ok" if cond else "FAIL"))
        if not cond:
            cap_fails.append(name)

    # ~31s single gap (15.0..46.1) inside a 47.81s clip -> artifact -> cap, never abort.
    _, act = _interior_cap_plan([(15.0, 46.1)], 47.81)
    _cap_expect("long interior gap (31s of 48s) -> cap not abort", act == "cap")
    # normal pacing: a few <=0.6s pauses, none over the 0.5s cap+slack -> nothing to cap.
    _, act = _interior_cap_plan([(5.0, 5.45), (12.0, 12.5), (20.0, 20.4)], 30.0)
    _cap_expect("normal pacing (small pauses) -> none", act == "none")
    # many borderline (sub-artifact) gaps, no single clear artifact gap, whose combined
    # excess removal would gut >= half the clip -> abort (likely a silencedetect mis-fire).
    swarm = [(0.5, 3.3), (3.8, 6.6), (7.0, 9.8)]   # 3 gaps x 2.8s (< 3.0), in a 10s clip
    _, act = _interior_cap_plan(swarm, 10.0)        # removes 3*(2.8-0.5)=6.9s >= 5.0s
    _cap_expect("borderline-gap swarm gutting half -> abort", act == "abort")

    print("cap selftest: %s"
          % ("PASS" if not cap_fails else "FAIL (%s)" % ", ".join(cap_fails)))
    return 0 if not cap_fails else 1


def main():
    ap = argparse.ArgumentParser(
        description="Narrate a narration-script to one file via the self-hosted voice server (Chatterbox).")
    ap.add_argument("script", nargs="?", default=None,
                    help="A chapter-XX.narrative-script.md (v3-tagged performance script)")
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
    ap.add_argument("--edge-pad", type=float, default=0.05,
                    help="Silence (seconds) to keep at each chunk edge when trimming the "
                         "leading/trailing dead air Chatterbox bakes in. The kept audio is "
                         "the single contiguous span [onset-pad, offset+pad] via ffmpeg "
                         "atrim, so interior speech is never touched. Default 0.05.")
    ap.add_argument("--no-edge-trim", action="store_true",
                    help="Skip edge-trimming and stitch the raw NN.wav chunks directly.")
    ap.add_argument("--split-threshold", type=int, default=SPLIT_THRESHOLD,
                    help="Proactively split any chunk longer than this many characters into "
                         "sentence-pieces at render time, render each separately, and concat "
                         "them into one chunk WAV. Long chunks (>~300c) intermittently drop "
                         "trailing text during Chatterbox generation; short pieces don't. "
                         "Default %d." % SPLIT_THRESHOLD)
    ap.add_argument("--lexicon", default=DEFAULT_LEXICON,
                    help="Pronunciation lexicon JSON (surface->spoken, applied only to the text "
                         "sent to the server, after tag-stripping). Default the seeded file at %s. "
                         "The 24-hour clock-time rule is general and always applies regardless."
                         % DEFAULT_LEXICON)
    ap.add_argument("--no-lexicon", action="store_true",
                    help="Disable the pronunciation lexicon (the general clock-time rule still "
                         "applies). Use when you want zero respelling overrides.")
    ap.add_argument("--selftest", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--api", default=DEFAULT_API)
    ap.add_argument("--user", default=None,
                    help="API username for HTTP Basic auth (else VOICE_API_USER env, else .mcp.json).")
    ap.add_argument("--password", default=None,
                    help="API password for HTTP Basic auth (else VOICE_API_PASSWORD env, else .mcp.json).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the chunk plan and exit without calling the API.")
    ap.add_argument("--resume", action="store_true",
                    help="Skip any chunk whose NN.wav already exists on disk (filename only), "
                         "to manually resume an interrupted render. DEFAULT (no flag) is a full "
                         "fresh re-render that overwrites every chunk -- so a revised script is "
                         "always re-voiced and never reuses stale audio.")
    args = ap.parse_args()

    if args.selftest:                       # prove the time rule + lexicon mechanism fire
        return _run_selftest()

    if not args.script:
        ap.error("the 'script' argument is required (or pass --selftest)")
    if not os.path.exists(args.script):
        print("ERROR: script not found: " + args.script, file=sys.stderr)
        return 2

    lexicon = resolve_lexicon(args.lexicon, args.no_lexicon)

    raw = open(args.script, "r", encoding="utf-8").read()
    text = extract_performance(raw)
    items = build_segments(text)
    chunks = build_chunks(items, args.max_chars, args.min_chars)
    for ch in chunks:                       # Chatterbox can't read '...' (runaway pauses)
        ch["text"] = normalize_ellipses(ch["text"], args.ellipsis)

    in_stem = os.path.splitext(os.path.basename(args.script))[0]
    base_stem = in_stem.replace(".narrative-script", "")
    out = args.out or os.path.join("audio", "book-1", base_stem, base_stem + "." + args.format)
    out_dir = os.path.dirname(out) or "."
    chunk_dir = os.path.join(out_dir, "chunks")

    print("Narrating %s via voice server: %d chars -> %d chunk(s), voice %s, format %s"
          % (base_stem, len(text), len(chunks), args.voice, args.format), file=sys.stderr)

    if args.dry_run:
        print_plan(chunks)
        print("(dry run: no API calls made)", file=sys.stderr)
        return 0

    if not chunks:
        print("ERROR: no narratable chunks found in performance script", file=sys.stderr)
        return 1

    user, pw = resolve_credentials(args.user, args.password)
    auth = auth_header(user, pw)
    if not auth:
        print("WARNING: no API credentials found (--user/--password, VOICE_API_USER/"
              "VOICE_API_PASSWORD env, or .mcp.json); protected /api/* calls will 401.",
              file=sys.stderr)
    else:
        print("Auth: HTTP Basic as %s" % user, file=sys.stderr)

    ok, detail = healthz(args.api)
    if not ok:
        print("WARNING: health check failed (%s): %s" % (args.api, detail), file=sys.stderr)
    else:
        print("Health: %s" % detail, file=sys.stderr)

    os.makedirs(chunk_dir, exist_ok=True)

    # Render each chunk to chunk_dir/NN.wav. DEFAULT is a full fresh re-render that
    # overwrites any existing NN.wav (so a revised script is always re-voiced, never
    # reusing stale audio); --resume skips chunks already on disk to resume an
    # interrupted render. render_chunk proactively splits long chunks so nothing drops.
    for i, ch in enumerate(chunks, 1):
        cf = os.path.join(chunk_dir, "%02d.wav" % i)
        prof = ch["profile"]
        if args.resume and os.path.exists(cf):
            print("  chunk %02d/%d  [%s]  skip (--resume; exists)"
                  % (i, len(chunks), profile_str(prof)), file=sys.stderr)
            continue
        print("  chunk %02d/%d  [%s]  %d chars ..."
              % (i, len(chunks), profile_str(prof), len(ch["text"])), file=sys.stderr)
        err, dur = render_chunk(args.api, args.voice, prof, ch["text"], cf, auth,
                                args.repetition_penalty, args.temperature, args.max_temp,
                                edge_pad=args.edge_pad, split_threshold=args.split_threshold,
                                lexicon=lexicon)
        if err:
            print("ERROR on chunk %d: %s" % (i, err), file=sys.stderr)
            return 1
        dur_s = ("%.1fs audio" % dur) if dur is not None else "duration unknown"
        print("      -> %s (%s)" % (os.path.basename(cf), dur_s), file=sys.stderr)

    # Stitch the rendered chunks into the final mastered file (edge-trim -> per-gap
    # silences -> concat + loudnorm). Lifted into stitch_chapter so an orchestrator can
    # drive render + stitch independently; main() just calls it (behavior-preserving).
    if not stitch_chapter(chunks, chunk_dir, out, args.format, args.edge_pad, args.no_edge_trim):
        return 1
    print(out)  # stdout: the final file path
    return 0


if __name__ == "__main__":
    sys.exit(main())
