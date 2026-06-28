#!/usr/bin/env python3
"""Catch Chatterbox "garble" artifacts in a rendered chapter by transcribing each
per-chunk WAV with the voice server's Whisper endpoint and diffing the transcript
against the words that chunk was SUPPOSED to say -- then deciding, per chunk, whether
the audio needs an automatic re-render (RETRY), a human ear (REVIEW), or nothing (OK).

Chatterbox occasionally emits non-speech "garble" (musical mumble, breaths, dropped
or invented words) on a chunk -- usually at high temperature. The render itself can't
tell; the audio is plausible until you listen. This script closes that loop: it
re-derives the exact chunk list the renderer produced, asks Whisper what each chunk
WAV actually says, and scores the transcript against the expected text.

CRUCIAL LESSON ENCODED HERE: Whisper is an UNRELIABLE oracle on long chunks. On a 40-58s
chunk faster-whisper routinely DROPS the MIDDLE of its OWN transcript, so a low
text-similarity is very often a Whisper artifact, NOT a real audio fault. Acting on
similarity alone produces false positives (a recent pass flagged 9 chunks whose RAW
audio was actually complete) and wastes re-renders on good audio. Therefore the verdict
must lean on signals that DO NOT depend on Whisper getting the whole transcript right:

  * foreign_words -- transcript tokens the script never contained. When Whisper merely
    DROPS the middle of a transcript, every word it DOES emit is correct (foreign ~= 0);
    a high foreign count instead means the audio genuinely says the wrong thing. This is
    a garble signal INDEPENDENT of similarity.
  * a Whisper-INDEPENDENT duration check -- estimate the seconds a chunk's text SHOULD
    take from its character count (chars / chars_per_sec) and compare to the ACTUAL wav
    length from ffprobe. If the audio is far shorter than its text demands, a real drop
    happened regardless of what Whisper transcribed.

Pipeline:
  1. Re-derive the chunk list EXACTLY as narrate-chapter-voiceserver.py does, by
     importing that module and reusing its functions:
        text   = extract_performance(raw_markdown)
        items  = build_segments(text)
        chunks = build_chunks(items, max_chars, min_chars)
     then normalize_ellipses(ch["text"], ellipsis) on each chunk -- the renderer
     applies that AFTER chunking, so we mirror it to get the text that was SPOKEN. Each
     chunk also carries its declared gap_after (register/beat/hold/scene). Chunk i here
     == chunk i rendered to <chunk-dir>/NN.wav (1-based, zero-padded 2).
  2. For each chunk, locate <chunk-dir>/%02d.wav (the RAW per-chunk render, pre-cap /
     pre-master -- the artifact as the model produced it). Missing files are reported.
  3. Get a transcript: either POST the bytes to {api}/api/transcribe (multipart, same
     HTTP Basic auth + proxy-bypassing opener the renderer uses, sequential, retrying on
     5xx), OR -- with --from-json -- reuse transcripts captured by an earlier run, so we
     can re-score WITHOUT touching the (often busy) server.
  4. Score + verdict (see compute_verdict): RETRY on reliable garble/drop signals
     (foreign_words > 2, a non-speech marker, or audio too short for its text); REVIEW on
     an ambiguous low similarity that is most likely a Whisper drop; OK otherwise.
  5. Report: per-chunk lines and a summary to stderr (with the explicit RETRY list of
     indices to re-render); optionally a --json results dump; optionally a --report
     human-readable markdown QC file (aligned per-chunk table + EXPECTED vs WHISPER for
     every non-OK chunk, so a human can eyeball the ambiguous ones). Exit 0 if every
     chunk is OK, 1 if anything needs attention.

Standard library only (urllib, json, difflib, argparse, os, re, sys, subprocess,
datetime, importlib). The renderer module is loaded via importlib.util because its
filename has hyphens. ffprobe (FFmpeg) is shelled out to for the duration check. Output
goes to stderr like the renderer.

Usage:
  # Live (transcribes via the server):
  python3 scripts/verify-narration.py \
      docs/50-manuscript/book-1/chapter-01-no-signal.narrative-script.md \
      [--api http://10.0.0.213:8080] [--chunk-dir audio/book-1/chunks/<stem>-voiceserver] \
      [--retry-threshold 0.80] [--chars-per-sec 16.0] [--short-ratio 0.6] \
      [--language en] [--json verify-ch01.json] [--report verify-ch01.md]

  # Re-score already-captured transcripts WITHOUT calling the server:
  python3 scripts/verify-narration.py <script.md> \
      --from-json verify-ch01.json --report verify-ch01.md
"""

import argparse
import collections
import csv
import datetime
import difflib
import importlib.util
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request


# Load the renderer module so we reuse its EXACT chunking pipeline + proxy-bypass
# opener + auth helpers. The filename has hyphens (not a valid module name), so it
# can't be `import`ed normally -- spec_from_file_location loads it from its path. The
# `if __name__ == "__main__"` guard in the renderer keeps its main() from running here.
_HERE = os.path.dirname(os.path.abspath(__file__))
_RENDERER_PATH = os.path.join(_HERE, "narrate-chapter-voiceserver.py")
_spec = importlib.util.spec_from_file_location("narrate_chapter_voiceserver", _RENDERER_PATH)
renderer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(renderer)

DEFAULT_API = "http://10.0.0.213:8080"

# Whisper emits non-speech events as parenthesized / bracketed tokens when the audio
# is musical mumble or breath rather than words -- e.g. "(music)", "(whispers)",
# "(breaths)", "[Music]". Their presence in a NARRATION transcript is a strong garble
# signal (real prose has no parentheticals here). Match any short bracketed run.
NONSPEECH_RE = re.compile(r'[\(\[][^\)\]]{0,40}[\)\]]')

# Word tokenizer for scoring: lowercase, then everything that isn't a letter/digit
# becomes a separator. Applied identically to BOTH expected and transcript so that
# punctuation, apostrophes, and casing never count as differences.
_WORD_SPLIT_RE = re.compile(r'[^a-z0-9]+')

# Length tripwire constants. The drop-signal compares ACTUAL SPEECH content (raw minus
# all detected silence) to the seconds the text demands -- using SPEECH length, not raw
# duration, so a Chatterbox drop that leaves a long wav padded with trailing silence is
# still caught. silencedetect params + the over-trim ratio match the renderer's masters.
SILENCE_NOISE_DB = "-38dB"   # silencedetect noise floor: below this is "silence"
SILENCE_MIN_D = "0.3"        # silencedetect min silent run (seconds) to count
OVERTRIM_RATIO = 0.85        # NN.trimmed.wav shorter than this * raw => OVER-TRIMMED
_SILENCE_DUR_RE = re.compile(r'silence_duration:\s*([0-9.]+)')

# ElevenLabs Scribe -- the SECOND transcriber, used ONLY as a tiebreaker on REVIEW
# chunks (cost-smart: it is metered). A direct, proxy-bypassing opener mirrors the
# voice server's _OPENER. el_whisper_sim >= this means BOTH transcribers heard the same
# thing, so a low el_sim is a real fault, not a Whisper artifact.
EL_STT_URL = "https://api.elevenlabs.io/v1/speech-to-text"
EL_AGREE_THRESHOLD = 0.7
# STRONG transcriber agreement. When BOTH transcribers heard nearly the same thing
# (el_whisper_sim >= this) at FULL audio length with no foreign tokens, a remaining
# diff against the SCRIPT is a number / normalization / spelling artifact (e.g. the
# audio says "Chapter One" and both write "Chapter 1"), NOT a Chatterbox garble -- so
# it must never escalate to a stitch-blocking RETRY. See apply_elevenlabs().
EL_GUARD_AGREE_THRESHOLD = 0.9
_EL_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


# --- number-word <-> digit normalization (scoring only) --------------------------------
# Whisper / Scribe transcribe SPOKEN numbers as DIGITS ("Chapter 1", "61", "October 3rd")
# while the script SPELLS them ("Chapter One", "sixty-one", "October the third"). On a
# short phrase that single word-vs-digit divergence tanks word-similarity and used to
# drive a FALSE RETRY that blocked the stitch. Before scoring, runs of number-words are
# collapsed to their integer value -- on BOTH the script and every transcript -- so
# word-form and digit-form compare EQUAL. Pure-stdlib local mapping (no new dependency,
# deterministic): cardinals, teens, tens, "twenty-three" compounds, hundred/thousand/
# million/billion scales, and common ordinals folded to cardinals ("third" -> 3, and the
# digit form "3rd" -> 3). Anything it cannot fold is left as-is and caught instead by the
# transcriber-agreement guard in apply_elevenlabs().
_NUM_UNITS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19,
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6,
    "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12,
    "thirteenth": 13, "fourteenth": 14, "fifteenth": 15, "sixteenth": 16,
    "seventeenth": 17, "eighteenth": 18, "nineteenth": 19,
}
_NUM_TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90,
    "twentieth": 20, "thirtieth": 30, "fortieth": 40, "fiftieth": 50, "sixtieth": 60,
    "seventieth": 70, "eightieth": 80, "ninetieth": 90,
}
_NUM_SCALES = {
    "hundred": 100, "hundredth": 100, "thousand": 1000, "thousandth": 1000,
    "million": 1000000, "millionth": 1000000, "billion": 1000000000,
    "billionth": 1000000000,
}
_NUM_WORDSET = set(_NUM_UNITS) | set(_NUM_TENS) | set(_NUM_SCALES)
_ORD_DIGIT_RE = re.compile(r'^(\d+)(?:st|nd|rd|th)$')  # "3rd" -> "3", "21st" -> "21"


def _run_to_int(run):
    """Collapse a contiguous run of number-words (all in _NUM_WORDSET) to one integer:
    'sixty', 'one' -> 61; 'two', 'thousand' -> 2000; 'hundred' alone -> 100."""
    total = current = 0
    for w in run:
        if w in _NUM_UNITS:
            current += _NUM_UNITS[w]
        elif w in _NUM_TENS:
            current += _NUM_TENS[w]
        elif w in ("hundred", "hundredth"):
            current = (current or 1) * 100
        else:  # thousand / million / billion (+ ordinal -th forms)
            current = (current or 1) * _NUM_SCALES[w]
            total += current
            current = 0
    return total + current


def _collapse_numbers(tokens):
    """Replace every maximal run of number-words in a token list with its digit string,
    and strip ordinal suffixes off digit tokens ('3rd' -> '3'). Non-number tokens pass
    through untouched. ['chapter', 'one'] -> ['chapter', '1']."""
    out = []
    run = []
    for tok in tokens:
        if tok in _NUM_WORDSET:
            run.append(tok)
            continue
        if run:
            out.append(str(_run_to_int(run)))
            run = []
        m = _ORD_DIGIT_RE.match(tok)
        out.append(m.group(1) if m else tok)
    if run:
        out.append(str(_run_to_int(run)))
    return out


def words_of(text):
    """Normalize prose to a comparable word list: lowercase, drop punctuation, split on
    any non-alphanumeric run, THEN fold number-words to their digit form so word-form and
    digit-form score equal. '"Don\'t," he said.' -> ['don', 't', 'he', 'said'];
    'Chapter One.' -> ['chapter', '1']. Applied identically to script AND transcript."""
    raw = [w for w in _WORD_SPLIT_RE.split((text or "").lower()) if w]
    return _collapse_numbers(raw)


def oneline(text):
    """Collapse all whitespace to single spaces -- full text, untruncated, for the
    side-by-side EXPECTED vs WHISPER blocks a human reads in the report."""
    return re.sub(r'\s+', ' ', (text or "")).strip()


def word_similarity(a_text, b_text):
    """Word-list SequenceMatcher ratio between two prose strings -- the SAME scoring the
    per-chunk Whisper sim uses (words_of + difflib), reused for the ElevenLabs el_sim /
    el_whisper_sim so the second opinion is measured on the identical scale. Empty-vs-
    empty is 1.0; empty-vs-nonempty is 0.0."""
    aw = words_of(a_text)
    bw = words_of(b_text)
    if not aw and not bw:
        return 1.0
    if not aw or not bw:
        return 0.0
    return difflib.SequenceMatcher(None, aw, bw).ratio()


def build_chunks_meta(script_path, max_chars, min_chars, ellipsis):
    """Re-derive every chunk in render order, mirroring the renderer's main() exactly
    (extract -> segment -> chunk -> normalize_ellipses). Returns a list of
    {"text": spoken_text, "gap_after": kind}; element i-1 describes chunk NN.wav.
    The renderer normalizes ellipses AFTER chunking, so we mirror it: EXPECTED == SPOKEN."""
    raw = open(script_path, "r", encoding="utf-8").read()
    text = renderer.extract_performance(raw)
    items = renderer.build_segments(text)
    chunks = renderer.build_chunks(items, max_chars, min_chars)
    return [{"text": renderer.normalize_ellipses(ch["text"], ellipsis),
             "gap_after": ch.get("gap_after", "register")} for ch in chunks]


def encode_multipart(audio_bytes, filename, language):
    """Build a multipart/form-data body in pure stdlib for POST /api/transcribe.

    Two parts: the audio `file` (Content-Type audio/wav) and a `language` field. Each
    part is delimited by --<boundary>; the body ends with --<boundary>--. Returns
    (content_type_header_value, body_bytes). The boundary is randomized per call so it
    can't collide with anything inside the audio payload.
    """
    boundary = "----verifynarration" + os.urandom(16).hex()
    bb = boundary.encode("ascii")
    crlf = b"\r\n"
    parts = []
    # file part
    parts.append(b"--" + bb + crlf)
    parts.append(
        ('Content-Disposition: form-data; name="file"; filename="%s"' % filename).encode("utf-8")
        + crlf)
    parts.append(b"Content-Type: audio/wav" + crlf)
    parts.append(crlf)
    parts.append(audio_bytes)
    parts.append(crlf)
    # language part
    parts.append(b"--" + bb + crlf)
    parts.append(b'Content-Disposition: form-data; name="language"' + crlf)
    parts.append(crlf)
    parts.append((language or "").encode("utf-8"))
    parts.append(crlf)
    # closing boundary
    parts.append(b"--" + bb + b"--" + crlf)
    body = b"".join(parts)
    return "multipart/form-data; boundary=" + boundary, body


def transcribe(api, wav_path, language, auth):
    """Transcribe one WAV via POST {api}/api/transcribe (multipart). Returns
    (text, None) on success or (None, error_string). Uses the renderer's proxy-
    bypassing opener and HTTP Basic auth; retries up to twice on a 5xx (server is
    single-instance and 502s under load, so a transient 5xx is worth one or two waits).
    """
    url = api.rstrip("/") + "/api/transcribe"
    with open(wav_path, "rb") as fh:
        audio = fh.read()
    filename = os.path.basename(wav_path)

    last_err = None
    for attempt in range(1, 4):  # initial try + up to 2 retries
        content_type, body = encode_multipart(audio, filename, language)
        headers = {"Content-Type": content_type, "Accept": "application/json"}
        if auth:
            headers.update(auth)
        req = urllib.request.Request(url, data=body, headers=headers)
        try:
            with renderer._OPENER.open(req, timeout=600) as resp:
                raw = resp.read().decode("utf-8", "replace")
            try:
                data = json.loads(raw)
            except ValueError:
                return (None, "non-JSON response: " + raw[:200])
            return (data.get("text", "") or "", None)
        except urllib.error.HTTPError as err:
            detail = err.read().decode("utf-8", "replace")
            last_err = "HTTP " + str(err.code) + ": " + detail[:300]
            if 500 <= err.code < 600 and attempt < 3:
                continue
            return (None, last_err)
        except Exception as err:  # noqa: BLE001  (network / socket errors)
            last_err = str(err)[:300]
            if attempt < 3:
                continue
            return (None, last_err)
    return (None, last_err or "unknown error")


def resolve_elevenlabs_key():
    """ElevenLabs API key from ELEVENLABS_API_KEY env, else the `elevenlabs` server's env
    in ./.mcp.json. The .mcp.json value is often a ${ELEVENLABS_API_KEY} placeholder, so a
    bare ${VAR} is expanded from the environment. Returns None when nothing is found (the
    caller then leaves REVIEW chunks unresolved rather than crashing)."""
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key
    try:
        with open(".mcp.json", "r", encoding="utf-8") as fh:
            env = json.load(fh)["mcpServers"]["elevenlabs"]["env"]
        key = env.get("ELEVENLABS_API_KEY")
    except Exception:  # noqa: BLE001  (.mcp.json missing or shaped differently)
        key = None
    if key and key.startswith("${") and key.endswith("}"):
        key = os.environ.get(key[2:-1])
    return key or None


def encode_multipart_el(audio_bytes, filename):
    """multipart/form-data body for ElevenLabs Scribe: a `model_id=scribe_v1` field and
    the `file` part (Content-Type audio/wav). Pure stdlib, randomized boundary -- same
    shape as encode_multipart but with the fields the Scribe endpoint wants."""
    boundary = "----verifynarration-el" + os.urandom(16).hex()
    bb = boundary.encode("ascii")
    crlf = b"\r\n"
    parts = []
    # model_id part
    parts.append(b"--" + bb + crlf)
    parts.append(b'Content-Disposition: form-data; name="model_id"' + crlf)
    parts.append(crlf)
    parts.append(b"scribe_v1")
    parts.append(crlf)
    # file part
    parts.append(b"--" + bb + crlf)
    parts.append(
        ('Content-Disposition: form-data; name="file"; filename="%s"' % filename).encode("utf-8")
        + crlf)
    parts.append(b"Content-Type: audio/wav" + crlf)
    parts.append(crlf)
    parts.append(audio_bytes)
    parts.append(crlf)
    # closing boundary
    parts.append(b"--" + bb + b"--" + crlf)
    return "multipart/form-data; boundary=" + boundary, b"".join(parts)


def transcribe_elevenlabs(wav_path, api_key):
    """Transcribe one WAV with ElevenLabs Scribe (POST {EL_STT_URL}, xi-api-key header,
    multipart model_id=scribe_v1 + file). Returns (text, None) or (None, error_string).
    Uses a direct, proxy-bypassing opener. No retry loop -- this is a metered, on-demand
    second opinion fired only on already-doubtful chunks, so we make exactly one call."""
    try:
        with open(wav_path, "rb") as fh:
            audio = fh.read()
    except OSError as err:
        return (None, str(err)[:300])
    content_type, body = encode_multipart_el(audio, os.path.basename(wav_path))
    headers = {"xi-api-key": api_key, "Content-Type": content_type,
               "Accept": "application/json"}
    req = urllib.request.Request(EL_STT_URL, data=body, headers=headers)
    try:
        with _EL_OPENER.open(req, timeout=300) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        return (None, "HTTP " + str(err.code) + ": " + detail[:300])
    except Exception as err:  # noqa: BLE001  (network / socket errors)
        return (None, str(err)[:300])
    try:
        data = json.loads(raw)
    except ValueError:
        return (None, "non-JSON response: " + raw[:200])
    return (data.get("text", "") or "", None)


def apply_elevenlabs(res, api_key, retry_threshold):
    """Resolve ONE REVIEW chunk with the ElevenLabs second opinion, mutating res in place.
    Fills el_text and (on success) el_sim / el_whisper_sim, then RE-decides the verdict:

      * REPEAT/INFLATION OVERRIDE: if the EL transcript itself is looped/inflated vs the
        script -> RETRY immediately, ahead of every OK guard below (a loop must never be
        whitewashed by either transcriber reading the repeated-but-"correct" words).
      * el_sim >= retry_threshold -> OK (ElevenLabs reads it fine -> a Whisper artifact).
      * NORMALIZATION/ARTIFACT GUARD: el_whisper_sim >= EL_GUARD_AGREE_THRESHOLD AND
        len_status == "OK" AND no non-speech marker AND foreign == 0 AND NOT a detected
        repeat -> OK. When BOTH
        transcribers strongly agree at full audio length and every divergence from the
        script is in a benign class (digits / single-char splits, so foreign_words counts
        none), the script-vs-transcript diff is a number/normalization/spelling artifact
        (e.g. audio "Chapter One" transcribed "Chapter 1"), NOT a garble. Never a stitch
        blocker. Real word-substitution garbles leave foreign tokens (foreign > 0) and so
        skip this guard; mid-transcript drops on bad audio shorten it (len_status != OK).
      * el_sim < retry_threshold AND el_whisper_sim >= EL_AGREE_THRESHOLD -> RETRY
        (both transcribers agree the audio differs from the script -- a real fault).
      * otherwise -> stays REVIEW (genuinely ambiguous; a human listens).

    Returns (outcome, error). On a transcription error the chunk stays REVIEW and el_text
    is left None so the failure is visible in qc.json."""
    text, err = transcribe_elevenlabs(res.get("wav"), api_key)
    if err is not None:
        res["el_text"] = None
        return ("error", err)
    res["el_text"] = text
    el_sim = word_similarity(text, res.get("expected", ""))
    el_whisper_sim = word_similarity(text, res.get("got", ""))
    res["el_sim"] = round(el_sim, 4)
    res["el_whisper_sim"] = round(el_whisper_sim, 4)
    # A loop the Whisper pass missed (Whisper sometimes drops the repeat -> the chunk only
    # reaches REVIEW) can still surface in the ElevenLabs transcript. Re-run the repeat/
    # inflation detector against the SCRIPT on the EL transcript; a clear loop -> RETRY,
    # overriding BOTH the el_sim->OK and the strong-agreement->OK guards below.
    el_rep, el_rep_reason, el_rep_metrics = repeat_inflation(
        words_of(res.get("expected", "")), words_of(text))
    if el_rep:
        res["repeat"] = True
        res["inflation"] = el_rep_metrics.get("inflation")
        res["dup_ratio"] = el_rep_metrics.get("dup_ratio")
        res["loop_phrase"] = el_rep_metrics.get("loop_phrase")
        res["verdict"] = "RETRY"
        res["flagged"] = True
        res["reason"] = "repeat/inflation in elevenlabs transcript -> RETRY: " + el_rep_reason
        return ("RETRY", None)
    if el_sim >= retry_threshold:
        res["verdict"] = "OK"
        res["flagged"] = False
        res["reason"] = "whisper artifact, confirmed by elevenlabs"
        return ("OK", None)
    if (el_whisper_sim >= EL_GUARD_AGREE_THRESHOLD
            and res.get("len_status") == "OK"
            and not res.get("nonspeech")
            and not res.get("foreign")
            and not res.get("repeat")):
        res["verdict"] = "OK"
        res["flagged"] = False
        res["reason"] = ("both transcribers agree (el/whisper=%.2f) at full length with no "
                         "foreign tokens -- script diff is a number/normalization artifact, "
                         "not a garble" % el_whisper_sim)
        return ("OK", None)
    if el_whisper_sim >= EL_AGREE_THRESHOLD:
        res["verdict"] = "RETRY"
        res["flagged"] = True
        res["reason"] = "both transcribers disagree with script"
        return ("RETRY", None)
    return ("REVIEW", None)


def wav_duration(path):
    """Actual playback length of a WAV in seconds via ffprobe -- the Whisper-INDEPENDENT
    truth about the render. Returns a float, or None if the file is missing or ffprobe
    can't read it. This is the signal we trust when Whisper's transcript can't be."""
    if not path or not os.path.exists(path):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    try:
        return float((out.stdout or "").strip())
    except ValueError:
        return None


def total_silence(path, noise_db=SILENCE_NOISE_DB, min_d=SILENCE_MIN_D):
    """Total seconds of detected silence in a WAV via ffmpeg silencedetect -- the second
    half of the SPEECH-length tripwire (speech_len = raw_len - total_silence). Sums every
    `silence_duration` ffmpeg prints (on stderr) for noise=<noise_db> d=<min_d>. Returns
    a float (0.0 when the file is all speech), or None if the file is missing / unreadable.

    Catching a Chatterbox drop hinges on THIS: a dropped chunk often renders as a few
    seconds of speech followed by a long silent tail, so the raw duration looks fine while
    the speech content is tiny. Subtracting the silence exposes the real speech length."""
    if not path or not os.path.exists(path):
        return None
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", path,
             "-af", "silencedetect=noise=%s:d=%s" % (noise_db, min_d),
             "-f", "null", "-"],
            capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.SubprocessError):
        return None
    total = 0.0
    for m in _SILENCE_DUR_RE.finditer(out.stderr or ""):
        try:
            total += float(m.group(1))
        except ValueError:
            pass
    return total


def foreign_words(exp_words, got_words):
    """Transcript tokens the script never contained -- the fingerprint of REAL garble
    (Chatterbox invents words; Whisper writes them down). This is a garble signal
    INDEPENDENT of similarity: when Whisper merely DROPS the middle of a long-chunk
    transcript, similarity falls but every word it DOES emit is still correct, so
    foreign stays ~0. A high foreign count therefore means audio that genuinely says
    the wrong thing, not a Whisper artifact.

    Two benign Whisper behaviours are excluded so they never masquerade as garble:
      * pure-digit tokens -- number<->word normalization ("eleven"->"11",
        "seventeen"->"17", "23:59"->"2359"): the script speaks numbers, Whisper writes
        numerals, and that divergence is not garble.
      * single-character tokens -- possessive / contraction / plural splits, e.g.
        "towers" transcribed as "tower" + "s", or "Eli's" -> "eli" + "s".
    Everything else absent from the expected words is counted. Returns the token list."""
    exp_set = set(exp_words)
    return [w for w in got_words
            if w not in exp_set and len(w) > 1 and not w.isdigit()]


# --- repeat / inflation detector (looping audio that HIGH similarity misses) ----------
# A Chatterbox chunk that LOOPS or repeats a phrase keeps a HIGH word-similarity score:
# the looped words are all still "correct" against the script, so foreign~=0 and the
# SequenceMatcher ratio barely moves (extra MATCHED words add to both M and T in 2M/T).
# The audio is also LONGER, never SHORTER, so the speech-length tripwire -- which only
# catches drops -- never fires. Net result: a looping chunk passes QC and gets stitched.
# This detector closes that gap by comparing the TRANSCRIPT to the SCRIPT for the three
# fingerprints of looping. It is deliberately CONSERVATIVE and ALWAYS measured against the
# script, so prose that legitimately repeats a phrase (present in BOTH) never trips it.
REPEAT_INFLATION_RATIO = 1.25   # transcript_words / script_words above this == inflated
REPEAT_MIN_EXCESS = 4           # ...and at least this many EXTRA words (short-chunk guard)
REPEAT_NGRAM_MIN = 3            # shortest back-to-back phrase length treated as a loop
REPEAT_NGRAM_MAX = 6            # longest  back-to-back phrase length treated as a loop
REPEAT_DUP_RATIO = 0.25         # excess-duplicate tokens / script words above this == loop


def _consecutive_repeat(words, n):
    """The first n-gram that appears IMMEDIATELY repeated back-to-back in `words`
    (words[i:i+n] == words[i+n:i+2n]), returned as a tuple, else None. For n=2,
    ['a','b','a','b'] -> ('a','b')."""
    for i in range(len(words) - 2 * n + 1):
        if words[i:i + n] == words[i + n:i + 2 * n]:
            return tuple(words[i:i + n])
    return None


def _script_has_repeat(exp_words, phrase):
    """True when `phrase` (a tuple) ALSO appears back-to-back in the SCRIPT -- i.e. the
    repetition is legitimate prose the model was asked to say, not a loop artifact."""
    n = len(phrase)
    for i in range(len(exp_words) - 2 * n + 1):
        if (tuple(exp_words[i:i + n]) == phrase
                and tuple(exp_words[i + n:i + 2 * n]) == phrase):
            return True
    return False


def repeat_inflation(exp_words, got_words):
    """Detect TTS looping / length-inflation that HIGH word-similarity misses, comparing the
    transcript to the SCRIPT so legitimate repetition (present in both) never fires. Returns
    (flagged, reason, metrics) with metrics = {inflation, dup_ratio, loop_phrase}. Fires on
    any of three CONSERVATIVE signals (each needs a clear margin):
      (a) LENGTH INFLATION -- transcript has > REPEAT_INFLATION_RATIO x the script's words
          AND at least REPEAT_MIN_EXCESS extra words (the signature of repeated audio; a
          Whisper mid-drop SHORTENS the transcript, so it can never trip this).
      (b) LOOPED N-GRAM -- a 3..6-word phrase repeated immediately back-to-back in the
          transcript that does NOT also repeat back-to-back in the script.
      (c) DUPLICATE-TOKEN RATIO -- transcript tokens beyond their script multiplicity exceed
          REPEAT_DUP_RATIO of the script length (heavy duplication even without net inflation).
    With no script baseline (empty exp_words) nothing fires -- a loop can't be judged without
    the text it was meant to say."""
    metrics = {"inflation": None, "dup_ratio": None, "loop_phrase": None}
    exp_len = len(exp_words)
    got_len = len(got_words)
    if not exp_len:
        return (False, "", metrics)
    inflation = round(got_len / exp_len, 3)
    exp_counts = collections.Counter(exp_words)
    got_counts = collections.Counter(got_words)
    excess = sum(max(0, c - exp_counts.get(w, 0)) for w, c in got_counts.items())
    dup_ratio = round(excess / exp_len, 3)
    metrics["inflation"] = inflation
    metrics["dup_ratio"] = dup_ratio

    reasons = []
    if inflation > REPEAT_INFLATION_RATIO and (got_len - exp_len) >= REPEAT_MIN_EXCESS:
        reasons.append("length inflation %.2fx (transcript %d words vs script %d)"
                       % (inflation, got_len, exp_len))
    loop_phrase = None
    for n in range(REPEAT_NGRAM_MAX, REPEAT_NGRAM_MIN - 1, -1):
        if got_len < 2 * n:
            continue
        cand = _consecutive_repeat(got_words, n)
        if cand and not _script_has_repeat(exp_words, cand):
            loop_phrase = cand
            metrics["loop_phrase"] = " ".join(cand)
            reasons.append('looped phrase "%s" repeated back-to-back, not in script'
                           % " ".join(cand))
            break
    if dup_ratio > REPEAT_DUP_RATIO and excess >= REPEAT_MIN_EXCESS:
        reasons.append("duplicate-token ratio %.2f over script (%d excess tokens)"
                       % (dup_ratio, excess))
    return (bool(reasons), "; ".join(reasons), metrics)


def compute_verdict(sim, foreign_count, has_nonspeech, audio_short, retry_threshold,
                    repeat_flagged=False):
    """Verdict. Two AUDIO/CONTENT-based checks hard-RETRY -- neither can be fooled by a
    transcriber's word choices. Everything else transcript-based (low similarity, a non-speech
    marker, or 'foreign' tokens) routes to REVIEW, where the ElevenLabs tiebreaker confirms
    before any re-render. A few foreign tokens at HIGH similarity are just Whisper's spelling
    (streetlight->street light, Webb->web, tier->tear), not garble -- so they must never force
    a re-render on good audio.

      RETRY  : the audio is too short for its text (speech_len drop), OR the repeat/inflation
               detector fired (looping / length-inflated audio). Both are trustworthy and
               INDEPENDENT of similarity, so a loop RETRYs even at sim >= 0.9 (the looped words
               are all "correct", which is exactly why similarity alone misses it).
      REVIEW : similarity < retry_threshold OR a non-speech marker. The ElevenLabs second
               opinion decides (both transcribers disagree with the script -> real fault;
               ElevenLabs reads it fine -> a Whisper artifact). Never a blind re-render.
      OK     : high similarity and clean. Foreign tokens at high similarity are quirks.
    sim may be None (no transcript); then only RETRY (if short / repeat) or OK."""
    if audio_short:
        return "RETRY"
    if repeat_flagged:
        return "RETRY"
    if has_nonspeech or (sim is not None and sim < retry_threshold):
        return "REVIEW"
    return "OK"


def verdict_reasons(foreign_count, nonspeech_marker, audio_short, sim, retry_threshold):
    """Human-readable explanation for a chunk's verdict (the RETRY trigger(s), or the
    ambiguous low-similarity note for REVIEW). Empty list means OK."""
    rs = []
    if audio_short:
        rs.append("speech too short for its text (real drop)")
    if nonspeech_marker and not audio_short:
        rs.append("non-speech marker %s (ElevenLabs to confirm)" % nonspeech_marker)
    if not audio_short and not nonspeech_marker and sim is not None and sim < retry_threshold:
        rs.append("low similarity %.2f < %.2f (likely a Whisper transcript drop; "
                  "ElevenLabs to confirm)" % (sim, retry_threshold))
    if foreign_count > 2 and (sim is None or sim >= retry_threshold):
        rs.append("note: %d foreign tokens at high similarity = transcription artifacts, "
                  "not a fault" % foreign_count)
    return rs


def evaluate(res, gap_after, chars_per_sec, short_ratio, retry_threshold):
    """Enrich one raw result ({index, wav, expected, got, [error]}) with every derived
    metric and a verdict, in place. Adds: gap_after, chars, sim, present, foreign,
    expected_len, raw_len, trimmed_len, speech_len, len_status, raw_dur/est_dur/rate
    (legacy aliases), short, nonspeech, el_text/el_sim/el_whisper_sim (None until the
    tiebreaker runs), verdict, flagged, reason.

    The length tripwire is Whisper-INDEPENDENT and runs even when transcription failed.
    It compares the chunk's ACTUAL SPEECH content -- raw_len minus all detected silence
    (silencedetect noise=-38dB d=0.3) -- to the seconds its text demands
    (expected_len = chars / chars_per_sec). Using SPEECH length, not raw duration, is the
    whole point: a Chatterbox drop can leave a 40s wav that is ~6s of speech and ~34s of
    trailing silence; the old raw-duration check missed that, the speech-length check
    catches it (len_status=SHORT -> RETRY). len_status is OVER-TRIMMED instead when our
    own NN.trimmed.wav fell below OVERTRIM_RATIO * raw_len (post-processing cut too much --
    not a Chatterbox fault, so it does NOT force a re-render)."""
    expected = res.get("expected", "") or ""
    got = res.get("got", "") or ""
    error = res.get("error")
    chars = len(expected)
    wav = res.get("wav")
    # Repeat/inflation defaults (overridden below when there is a usable transcript).
    rep_flagged = False
    rep_metrics = {"inflation": None, "dup_ratio": None, "loop_phrase": None}

    # --- length tripwire (SPEECH length, Whisper-INDEPENDENT) --------------------------
    expected_len = (chars / chars_per_sec) if chars_per_sec > 0 else None
    raw_len = wav_duration(wav)
    trimmed_path = (os.path.splitext(wav)[0] + ".trimmed.wav") if wav else None
    if trimmed_path and os.path.exists(trimmed_path):
        trimmed_len = wav_duration(trimmed_path)
    else:
        trimmed_len = raw_len
    silence = total_silence(wav)
    speech_len = (raw_len - silence) if (raw_len is not None and silence is not None) else raw_len
    is_short = (speech_len is not None and expected_len is not None and expected_len > 0
                and speech_len < short_ratio * expected_len)
    is_overtrim = (trimmed_len is not None and raw_len is not None and raw_len > 0
                   and trimmed_len < OVERTRIM_RATIO * raw_len)
    len_status = "SHORT" if is_short else ("OVER-TRIMMED" if is_overtrim else "OK")
    audio_short = is_short  # the RETRY drop-signal uses SPEECH length, never raw duration
    rate = (chars / raw_len) if (raw_len and raw_len > 0) else None

    if error:
        # No usable transcript -- fall back to the Whisper-INDEPENDENT length tripwire.
        sim = present = None
        foreign = 0
        nonspeech = ""
        if "missing" in error.lower():
            verdict = "RETRY"            # nothing rendered -- it must be rendered
        elif audio_short:
            verdict = "RETRY"            # speech too short regardless of Whisper
        else:
            verdict = "REVIEW"           # couldn't assess via Whisper; length plausible
        reasons = [error] + (["speech too short for its text"] if audio_short else [])
    else:
        exp_words = words_of(expected)
        got_words = words_of(got)
        if exp_words:
            sim = difflib.SequenceMatcher(None, exp_words, got_words).ratio()
            got_set = set(got_words)
            present = sum(1 for w in exp_words if w in got_set) / len(exp_words)
        else:
            sim = present = 1.0
        foreign = len(foreign_words(exp_words, got_words))
        marker = NONSPEECH_RE.search(got)
        nonspeech = marker.group(0) if marker else ""
        # Repeat/inflation detector: looping audio keeps a HIGH sim (looped words are all
        # "correct") so it must be able to force RETRY independently of similarity.
        rep_flagged, rep_reason, rep_metrics = repeat_inflation(exp_words, got_words)
        verdict = compute_verdict(sim, foreign, bool(nonspeech), audio_short,
                                  retry_threshold, repeat_flagged=rep_flagged)
        reasons = verdict_reasons(foreign, nonspeech, audio_short, sim, retry_threshold)
        if rep_flagged:
            reasons.insert(0, "repeat/inflation -> RETRY (overrides high-sim): " + rep_reason)

    res.update({
        "gap_after": gap_after,
        "chars": chars,
        "sim": round(sim, 4) if sim is not None else None,
        "present": round(present, 4) if present is not None else None,
        "foreign": foreign,
        "expected_len": round(expected_len, 2) if expected_len is not None else None,
        "raw_len": round(raw_len, 2) if raw_len is not None else None,
        "trimmed_len": round(trimmed_len, 2) if trimmed_len is not None else None,
        "speech_len": round(speech_len, 2) if speech_len is not None else None,
        "len_status": len_status,
        # legacy aliases kept so the markdown report + --json dump stay stable
        "raw_dur": round(raw_len, 2) if raw_len is not None else None,
        "est_dur": round(expected_len, 2) if expected_len is not None else None,
        "rate": round(rate, 2) if rate is not None else None,
        "short": bool(audio_short),
        "nonspeech": nonspeech,
        # repeat/inflation detector (looping audio that high similarity misses)
        "repeat": bool(rep_flagged),
        "inflation": rep_metrics.get("inflation"),
        "dup_ratio": rep_metrics.get("dup_ratio"),
        "loop_phrase": rep_metrics.get("loop_phrase"),
        # ElevenLabs tiebreaker fields -- populated later, only on REVIEW chunks
        "el_text": res.get("el_text"),
        "el_sim": res.get("el_sim"),
        "el_whisper_sim": res.get("el_whisper_sim"),
        "verdict": verdict,
        "flagged": verdict != "OK",
        "reason": "; ".join(reasons),
    })
    return res


def _cell(value, fmt):
    """Format a possibly-None numeric cell for the report table ('-' when unknown)."""
    return (fmt % value) if value is not None else "-"


def write_report(path, base_stem, results, args, counts, retry_list, review_list, source):
    """Write the human-readable markdown QC report: a header summarizing the thresholds
    used and the OK/REVIEW/RETRY counts, an aligned per-chunk table, then EXPECTED vs
    WHISPER (full text) for every non-OK chunk so a human can eyeball the ambiguous
    REVIEW chunks and confirm the RETRY ones."""
    L = []
    A = L.append
    A("# Narration QC report -- %s" % base_stem)
    A("")
    A("- generated: %s" % datetime.datetime.now().isoformat(timespec="seconds"))
    A("- source: %s" % source)
    A("- total chunks: %d" % len(results))
    A("")
    A("## Thresholds")
    A("")
    A("- retry-threshold (similarity below which a chunk is REVIEW): **%.2f**" % args.retry_threshold)
    A("- chars-per-sec (clean-narration rate used for est_dur): **%.1f**" % args.chars_per_sec)
    A("- short-ratio (audio is \"short\" when raw_dur < ratio * est_dur): **%.2f**" % args.short_ratio)
    A("- foreign_words RETRY trigger: **> 2**   |   non-speech marker RETRY trigger: any `(music)` / `[breaths]`")
    A("")
    A("## Verdict rules")
    A("")
    A("- **RETRY** (auto re-render): the audio is too short for its text (Whisper-"
      "INDEPENDENT speech-length check), OR the repeat/inflation detector fired -- "
      "transcript length-inflated > %.2fx the script, a 3..6-word phrase looped back-to-"
      "back (not in the script), or duplicate-token ratio > %.2f. The repeat check "
      "OVERRIDES high similarity: a looping chunk keeps sim >= 0.9 (the looped words are "
      "all \"correct\") yet still RETRYs. These are reliable garble / loop / drop signals."
      % (REPEAT_INFLATION_RATIO, REPEAT_DUP_RATIO))
    A("- **REVIEW** (human ear -- do NOT auto-retry): similarity < retry-threshold but "
      "`foreign_words <= 2` and audio not short. Most likely Whisper dropped the MIDDLE "
      "of its OWN transcript on a long chunk, not a real audio fault. Auto-retrying "
      "these wastes renders on good audio.")
    A("- **OK**: none of the above.")
    A("")
    A("## Counts")
    A("")
    A("**OK = %d | REVIEW = %d | RETRY = %d** (total %d)"
      % (counts["OK"], counts["REVIEW"], counts["RETRY"], len(results)))
    A("")
    A("- RETRY chunks to re-render: %s"
      % (", ".join("%02d" % i for i in retry_list) if retry_list else "none"))
    A("- REVIEW chunks to eyeball: %s"
      % (", ".join("%02d" % i for i in review_list) if review_list else "none"))
    A("")
    A("## Per-chunk table")
    A("")
    A("| idx | gap_after | chars | sim | pres% | foreign | raw_dur | est_dur | rate | VERDICT |")
    A("| --: | :-------- | ----: | --: | ----: | ------: | ------: | ------: | ---: | :------ |")
    for r in results:
        A("| %d | %s | %d | %s | %s | %d | %s | %s | %s | %s |" % (
            r["index"], r["gap_after"], r["chars"],
            _cell(r["sim"], "%.2f"),
            _cell(round(r["present"] * 100) if r["present"] is not None else None, "%d"),
            r["foreign"],
            _cell(r["raw_dur"], "%.1f"),
            _cell(r["est_dur"], "%.1f"),
            _cell(r["rate"], "%.1f"),
            r["verdict"]))
    A("")
    A("## Chunks needing attention (EXPECTED vs WHISPER)")
    A("")
    attn = [r for r in results if r["verdict"] != "OK"]
    if not attn:
        A("_None -- every chunk is OK._")
    for r in attn:
        A("### chunk %02d -- %s" % (r["index"], r["verdict"]))
        A("")
        A("- reason: %s" % (r["reason"] or "-"))
        A("- gap_after=%s chars=%d sim=%s present=%s foreign=%d raw_dur=%ss est_dur=%ss "
          "rate=%s short=%s" % (
              r["gap_after"], r["chars"], _cell(r["sim"], "%.2f"),
              _cell(round(r["present"] * 100) if r["present"] is not None else None, "%d%%"),
              r["foreign"], _cell(r["raw_dur"], "%.1f"), _cell(r["est_dur"], "%.1f"),
              _cell(r["rate"], "%.1f"), r["short"]))
        A("")
        A("EXPECTED:")
        A("")
        A("> " + (oneline(r["expected"]) or "_(empty)_"))
        A("")
        A("WHISPER:")
        A("")
        A("> " + (oneline(r["got"]) or "_(empty transcript)_"))
        A("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


# The FINAL externally-specified QC schema (exact field names, exact order). qc.json
# carries the full untruncated text; qc.csv carries the same rows with text truncated.
QC_FIELDS = ["chunk", "path", "gap_after", "script_text", "whisper_text", "whisper_sim",
             "el_text", "el_sim", "el_whisper_sim", "chars", "expected_len", "raw_len",
             "trimmed_len", "speech_len", "len_status", "repeat", "inflation", "dup_ratio",
             "status", "reason"]


def qc_record(r):
    """Project an internal result onto QC_FIELDS. status == the final verdict;
    len_status == the speech-length tripwire result; el_* are non-null only on chunks the
    ElevenLabs tiebreaker actually transcribed."""
    return {
        "chunk": "%02d" % r["index"],
        "path": r.get("wav"),
        "gap_after": r.get("gap_after"),
        "script_text": r.get("expected", "") or "",
        "whisper_text": r.get("got", "") or "",
        "whisper_sim": r.get("sim"),
        "el_text": r.get("el_text"),
        "el_sim": r.get("el_sim"),
        "el_whisper_sim": r.get("el_whisper_sim"),
        "chars": r.get("chars"),
        "expected_len": r.get("expected_len"),
        "raw_len": r.get("raw_len"),
        "trimmed_len": r.get("trimmed_len"),
        "speech_len": r.get("speech_len"),
        "len_status": r.get("len_status"),
        "repeat": bool(r.get("repeat")),
        "inflation": r.get("inflation"),
        "dup_ratio": r.get("dup_ratio"),
        "status": r.get("verdict"),
        "reason": r.get("reason", "") or "",
    }


def write_qc_json(path, records):
    """qc.json -- a JSON array, one object per chunk, EVERY field with full (untruncated)
    text. The machine-readable record of the pass that a retry loop reads back."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2)


def _csv_trunc(text, limit=80):
    """Whitespace-collapsed, length-capped cell for the spreadsheet (full text lives in
    qc.json). The csv module still quotes/escapes whatever survives the cap."""
    s = oneline(text)
    return s if len(s) <= limit else s[:limit - 1] + "…"


def write_qc_csv(path, records):
    """qc.csv -- the same rows as qc.json, numeric/status columns plus TRUNCATED text,
    written through the csv module so embedded commas, quotes, and newlines are quoted
    correctly and the file opens cleanly in any spreadsheet."""
    text_cols = {"script_text", "whisper_text", "el_text"}
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        w.writerow(QC_FIELDS)
        for rec in records:
            row = []
            for k in QC_FIELDS:
                v = rec.get(k)
                if v is None:
                    row.append("")
                elif k in text_cols:
                    row.append(_csv_trunc(v))
                else:
                    row.append(v)
            w.writerow(row)


def run_selftest():
    """Tiny, offline self-test for the repeat/inflation detector (no network, no files).
    Exercises a clean transcript, a Whisper mid-drop (shorter -- must NOT flag), a fully
    looped transcript, an ISOLATED back-to-back phrase loop (length not inflated, so only
    the n-gram signal fires), and prose that LEGITIMATELY repeats a phrase present in BOTH
    sides (must NOT flag). Returns 0 if every case behaves, else 1."""
    fails = []

    def expect(name, cond):
        print("  %-38s %s" % (name, "ok" if cond else "FAIL"), file=sys.stderr)
        if not cond:
            fails.append(name)

    script = ("the rain came down on the empty street and eli watched the water gather "
              "at the curb while the city stayed dark")
    exp = words_of(script)
    expect("clean transcript -> no flag", not repeat_inflation(exp, words_of(script))[0])
    expect("mid-drop (shorter) -> no flag",
           not repeat_inflation(exp, words_of("the rain came down on the empty street"))[0])
    f, _, m = repeat_inflation(exp, words_of(script + " " + script))
    expect("full loop -> flag (inflation ~2x)", f and m["inflation"] >= 1.9)
    looped = ("the rain came the rain came down on the empty street and eli watched the "
              "water gather at the curb while the city stayed dark")
    fr, rr, _ = repeat_inflation(exp, words_of(looped))
    expect("isolated back-to-back loop -> flag", fr and "looped phrase" in rr)
    legit = "i can't i can't i can't believe the door is standing wide open"
    le = words_of(legit)
    expect("legit repeated prose (both sides) -> no flag", not repeat_inflation(le, le)[0])

    print("selftest: %s" % ("PASS" if not fails else "FAIL (%s)" % ", ".join(fails)),
          file=sys.stderr)
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser(
        description="Verify a rendered chapter for Chatterbox garble: transcribe each "
                    "chunk WAV (or reuse --from-json), score against the expected text, "
                    "add a Whisper-INDEPENDENT SPEECH-length tripwire (raw minus silence, "
                    "so a long-but-mostly-silent dropped chunk is caught), and -- on "
                    "doubtful chunks only -- a metered ElevenLabs Scribe second opinion to "
                    "resolve REVIEW into OK or RETRY. Emits a per-chunk RETRY / REVIEW / OK "
                    "verdict and, BY DEFAULT, writes qc.json (full text, every field) and "
                    "qc.csv (truncated text, spreadsheet-openable) into the chunk dir.")
    ap.add_argument("script", nargs="?",
                    help="A chapter-XX.narrative-script.md (same input as the renderer)")
    ap.add_argument("--selftest", action="store_true",
                    help="Run the offline repeat/inflation detector self-test and exit "
                         "(no script, no network, no files).")
    ap.add_argument("--api", default=DEFAULT_API,
                    help="Voice server base URL. Default %s." % DEFAULT_API)
    ap.add_argument("--chunk-dir", default=None,
                    help="Dir holding the per-chunk NN.wav renders. Default: derived "
                         "exactly like the renderer -> audio/book-1/chunks/<stem>-voiceserver.")
    ap.add_argument("--from-json", default=None, dest="from_json",
                    help="Re-score transcripts captured by an earlier --json run instead "
                         "of calling the server (no API calls; still ffprobes the wavs).")
    ap.add_argument("--max-chars", type=int, default=2000,
                    help="Per-chunk cap; MUST match the render so chunks line up. Default 2000.")
    ap.add_argument("--min-chars", type=int, default=280,
                    help="Sub-min absorb threshold; MUST match the render. Default 280.")
    ap.add_argument("--ellipsis", default="comma",
                    choices=["comma", "period", "drop", "dotdot", "keep"],
                    help="Ellipsis handling; MUST match the render so EXPECTED == SPOKEN. "
                         "Default comma.")
    ap.add_argument("--threshold", type=float, default=0.80,
                    help="Legacy similarity flag (kept for compatibility). The verdict "
                         "uses --retry-threshold. Default 0.80.")
    ap.add_argument("--retry-threshold", type=float, default=0.80, dest="retry_threshold",
                    help="Similarity below which a chunk is REVIEW (when no reliable "
                         "RETRY signal fires). Default 0.80.")
    ap.add_argument("--chars-per-sec", type=float, default=16.0, dest="chars_per_sec",
                    help="Clean-narration rate used to estimate expected audio seconds "
                         "from a chunk's character count (est_dur = chars / rate). "
                         "Default 16.0.")
    ap.add_argument("--short-ratio", type=float, default=0.6, dest="short_ratio",
                    help="Chunk is len_status=SHORT (a real drop -> RETRY) when its SPEECH "
                         "length (raw minus detected silence) < short_ratio * expected_len. "
                         "Default 0.6.")
    ap.add_argument("--no-elevenlabs", action="store_true", dest="no_elevenlabs",
                    help="Skip the ElevenLabs Scribe second opinion entirely (Whisper-only). "
                         "By default any chunk that would be REVIEW is re-transcribed with "
                         "ElevenLabs to resolve it to OK or RETRY; this flag leaves it REVIEW.")
    ap.add_argument("--language", default="en",
                    help="Force the transcription language (ISO code). Default en.")
    ap.add_argument("--user", default=None,
                    help="API username for HTTP Basic auth (else VOICE_API_USER env, else .mcp.json).")
    ap.add_argument("--password", default=None,
                    help="API password for HTTP Basic auth (else VOICE_API_PASSWORD env, else .mcp.json).")
    ap.add_argument("--json", default=None, dest="json_path",
                    help="Dump full per-chunk results (index, wav, gap_after, chars, sim, "
                         "present, foreign, raw_dur, est_dur, rate, short, nonspeech, "
                         "verdict, expected, got, reason) to this path.")
    ap.add_argument("--report", default=None, dest="report_path",
                    help="Write a human-readable markdown QC report (aligned per-chunk "
                         "table + EXPECTED vs WHISPER for every non-OK chunk).")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()
    if not args.script:
        ap.error("the script argument is required (omit it only with --selftest)")

    if not os.path.exists(args.script):
        print("ERROR: script not found: " + args.script, file=sys.stderr)
        return 2

    # Re-derive chunk texts + gaps and the chunk dir EXACTLY as the renderer would.
    chunks_meta = build_chunks_meta(args.script, args.max_chars, args.min_chars, args.ellipsis)
    in_stem = os.path.splitext(os.path.basename(args.script))[0]
    base_stem = in_stem.replace(".narrative-script", "")
    chunk_dir = args.chunk_dir or os.path.join("audio", "book-1", base_stem, "chunks")

    if not chunks_meta:
        print("ERROR: no narratable chunks derived from performance script", file=sys.stderr)
        return 1

    if args.from_json:
        source = "re-score --from-json %s" % args.from_json
    else:
        source = "live transcribe %s" % args.api
    print("Verifying %s: %d chunk(s) against %s  [%s]"
          % (base_stem, len(chunks_meta), chunk_dir, source), file=sys.stderr)

    # --- gather raw results (transcript per chunk) -------------------------------------
    results = []
    if args.from_json:
        with open(args.from_json, "r", encoding="utf-8") as fh:
            prior = json.load(fh)
        by_index = {int(r["index"]): r for r in prior}
        for i, meta in enumerate(chunks_meta, 1):
            wav = os.path.join(chunk_dir, "%02d.wav" % i)
            src = by_index.get(i)
            if src is None:
                results.append({"index": i, "wav": wav, "expected": meta["text"],
                                "got": "", "error": "no transcript in --from-json"})
            else:
                results.append({"index": i, "wav": src.get("wav") or wav,
                                "expected": src.get("expected", meta["text"]),
                                "got": src.get("got", "")})
    else:
        user, pw = renderer.resolve_credentials(args.user, args.password)
        auth = renderer.auth_header(user, pw)
        if not auth:
            print("WARNING: no API credentials found (--user/--password, VOICE_API_USER/"
                  "VOICE_API_PASSWORD env, or .mcp.json); /api/transcribe will 401.",
                  file=sys.stderr)
        else:
            print("Auth: HTTP Basic as %s" % user, file=sys.stderr)
        for i, meta in enumerate(chunks_meta, 1):
            wav = os.path.join(chunk_dir, "%02d.wav" % i)
            if not os.path.exists(wav):
                print("  chunk %02d  MISSING wav (%s) -- not rendered" % (i, wav),
                      file=sys.stderr)
                results.append({"index": i, "wav": wav, "expected": meta["text"],
                                "got": "", "error": "missing wav"})
                continue
            text, err = transcribe(args.api, wav, args.language, auth)
            if err is not None:
                print("  chunk %02d  TRANSCRIBE ERROR: %s" % (i, err), file=sys.stderr)
                results.append({"index": i, "wav": wav, "expected": meta["text"],
                                "got": "", "error": "transcribe failed: " + err})
                continue
            results.append({"index": i, "wav": wav, "expected": meta["text"], "got": text})

    # --- evaluate (score + SPEECH-length tripwire + provisional verdict) ---------------
    for r in results:
        idx = r["index"]
        gap = chunks_meta[idx - 1]["gap_after"] if 1 <= idx <= len(chunks_meta) else "?"
        evaluate(r, gap, args.chars_per_sec, args.short_ratio, args.retry_threshold)

    # --- ElevenLabs tiebreaker (second transcriber, REVIEW chunks ONLY) ----------------
    # Cost-smart: only the doubtful chunks (provisional verdict REVIEW -- low whisper_sim,
    # foreign<=2, not short) get a second, metered opinion. OK and already-RETRY chunks are
    # never sent. apply_elevenlabs resolves each REVIEW: both transcribers disagreeing with
    # the script -> RETRY; ElevenLabs reading it fine -> OK (a confirmed Whisper artifact).
    if not args.no_elevenlabs:
        review_now = [r for r in results if r["verdict"] == "REVIEW"]
        if review_now:
            el_key = resolve_elevenlabs_key()
            if not el_key:
                print("WARNING: no ELEVENLABS_API_KEY found (env or .mcp.json); leaving "
                      "%d REVIEW chunk(s) unresolved (pass --no-elevenlabs to silence)."
                      % len(review_now), file=sys.stderr)
            else:
                print("ElevenLabs Scribe tiebreaker on %d REVIEW chunk(s): %s"
                      % (len(review_now),
                         ", ".join("%02d" % r["index"] for r in review_now)),
                      file=sys.stderr)
                for r in review_now:
                    _outcome, el_err = apply_elevenlabs(r, el_key, args.retry_threshold)
                    if el_err is not None:
                        print("  chunk %02d  ELEVENLABS ERROR: %s (stays REVIEW)"
                              % (r["index"], el_err), file=sys.stderr)

    # --- per-chunk lines (printed AFTER the tiebreaker so verdicts are final) ----------
    for r in results:
        el_part = ""
        if r.get("el_sim") is not None:
            el_part = "  el=%s el/whisper=%s" % (
                _cell(r["el_sim"], "%.2f"), _cell(r["el_whisper_sim"], "%.2f"))
        print("  chunk %02d  %-6s sim=%s pres=%s foreign=%d raw=%ss speech=%ss exp=%ss "
              "len=%-12s%s%s"
              % (r["index"], r["verdict"],
                 _cell(r["sim"], "%.2f"), _cell(r["present"], "%.2f"), r["foreign"],
                 _cell(r["raw_len"], "%.1f"), _cell(r["speech_len"], "%.1f"),
                 _cell(r["expected_len"], "%.1f"), r["len_status"], el_part,
                 ("  [%s]" % r["reason"]) if r["reason"] else ""),
              file=sys.stderr)

    # --- summary -----------------------------------------------------------------------
    counts = {"OK": 0, "REVIEW": 0, "RETRY": 0}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    retry_list = [r["index"] for r in results if r["verdict"] == "RETRY"]
    review_list = [r["index"] for r in results if r["verdict"] == "REVIEW"]

    print("", file=sys.stderr)
    print("--- summary ---", file=sys.stderr)
    print("thresholds: retry-threshold=%.2f  chars-per-sec=%.1f  short-ratio=%.2f"
          % (args.retry_threshold, args.chars_per_sec, args.short_ratio), file=sys.stderr)
    print("total: %d   OK: %d   REVIEW: %d   RETRY: %d"
          % (len(results), counts["OK"], counts["REVIEW"], counts["RETRY"]), file=sys.stderr)
    print("RETRY (re-render these): %s"
          % (", ".join("%02d" % i for i in retry_list) if retry_list else "none"),
          file=sys.stderr)
    print("REVIEW (human ear, do NOT auto-retry): %s"
          % (", ".join("%02d" % i for i in review_list) if review_list else "none"),
          file=sys.stderr)
    for r in results:
        if r["verdict"] == "OK":
            continue
        print("", file=sys.stderr)
        print("  chunk %02d  %s  [%s]" % (r["index"], r["verdict"], r["reason"]),
              file=sys.stderr)
        print("    expected: %s" % (oneline(r["expected"])[:140]), file=sys.stderr)
        print("    got:      %s" % (oneline(r["got"])[:140]), file=sys.stderr)

    if args.json_path:
        with open(args.json_path, "w", encoding="utf-8") as fh:
            json.dump(results, fh, ensure_ascii=False, indent=2)
        print("", file=sys.stderr)
        print("results written to %s" % args.json_path, file=sys.stderr)

    if args.report_path:
        write_report(args.report_path, base_stem, results, args, counts,
                     retry_list, review_list, source)
        print("report written to %s" % args.report_path, file=sys.stderr)

    # --- DEFAULT structured outputs: qc.json + qc.csv into the chunk dir ----------------
    records = [qc_record(r) for r in results]
    qc_json_path = os.path.join(chunk_dir, "qc.json")
    qc_csv_path = os.path.join(chunk_dir, "qc.csv")
    try:
        os.makedirs(chunk_dir, exist_ok=True)
        write_qc_json(qc_json_path, records)
        write_qc_csv(qc_csv_path, records)
        print("", file=sys.stderr)
        print("qc.json written to %s" % qc_json_path, file=sys.stderr)
        print("qc.csv  written to %s" % qc_csv_path, file=sys.stderr)
    except OSError as err:
        print("WARNING: could not write qc.json/qc.csv to %s: %s" % (chunk_dir, err),
              file=sys.stderr)

    return 1 if (counts["RETRY"] or counts["REVIEW"]) else 0


if __name__ == "__main__":
    sys.exit(main())
