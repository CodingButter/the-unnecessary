#!/usr/bin/env python3
"""Narrate a manuscript chapter to a single MP3 using ElevenLabs.

ElevenLabs caps the text per request, and a chapter is far longer than that, so
this chunks the prose at paragraph boundaries, generates one MP3 per chunk, and
stitches them into a single file with ffmpeg (stream copy, no re-encode). The
result is a downloaded file, not a stream, stored in an organized location.

Standard library only (plus ffmpeg on PATH for the final concat).

Usage:
  python3 scripts/narrate-chapter.py docs/50-manuscript/book-1/chapter-01-no-signal.md \
      [--voice JBFqnCBsd6RMkjVDRZzb] [--out audio/book-1/chapter-01-no-signal.mp3] \
      [--model eleven_multilingual_v2] [--chunk-chars 2500]

The ElevenLabs API key is read from ELEVENLABS_API_KEY in the environment,
falling back to the repo-root .env. The key is never printed. Default voice is
"George, Warm Captivating Storyteller".
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error

API = "https://api.elevenlabs.io/v1/text-to-speech/"


def load_key():
    val = os.environ.get("ELEVENLABS_API_KEY")
    if val:
        return val.strip()
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(repo_root, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line.startswith("ELEVENLABS_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def extract_prose(md_text):
    """Return clean narratable prose: drop front matter, the adjudication log,
    markdown markers, and scene-break rules; keep the chapter title and body."""
    text = md_text
    # Drop YAML front matter.
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            text = text[end + 4:]
    # Drop everything from the Adjudication Log onward (it is meta, not prose).
    cut = re.search(r'^##\s+Adjudication Log', text, re.M)
    if cut:
        text = text[:cut.start()]
    # Drop "See also" or other trailing meta sections if present.
    out_lines = []
    for line in text.split("\n"):
        s = line.strip()
        if s == "---":          # scene-break rule -> becomes a paragraph gap (pause)
            out_lines.append("")
            continue
        if re.match(r'^#{1,6}\s', s):   # heading -> read its text, no hashes
            s = re.sub(r'^#{1,6}\s+', '', s)
            out_lines.append(s)
            continue
        # strip bold/italic markers and stray backticks
        s = s.replace("**", "").replace("*", "").replace("`", "")
        out_lines.append(s)
    text = "\n".join(out_lines)
    # Collapse 3+ newlines to a paragraph break.
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text


def chunk_paragraphs(text, limit):
    """Group paragraphs into chunks no larger than limit chars, never splitting
    a paragraph across chunks unless a single paragraph exceeds the limit."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    cur = ""
    for p in paras:
        if len(p) > limit:
            # Flush, then hard-split the oversized paragraph at sentence ends.
            if cur:
                chunks.append(cur)
                cur = ""
            sentences = re.split(r'(?<=[.!?])\s+', p)
            buf = ""
            for sent in sentences:
                if len(buf) + len(sent) + 1 > limit and buf:
                    chunks.append(buf.strip())
                    buf = ""
                buf = (buf + " " + sent).strip()
            if buf:
                cur = buf
            continue
        if cur and len(cur) + len(p) + 2 > limit:
            chunks.append(cur)
            cur = p
        else:
            cur = (cur + "\n\n" + p).strip() if cur else p
    if cur:
        chunks.append(cur)
    return chunks


def tts(text, voice, model, key, out_path):
    url = API + voice
    body = json.dumps({
        "text": text,
        "model_id": model,
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.8,
                           "style": 0.1, "use_speaker_boost": True},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={
        "xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            audio = resp.read()
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        return "HTTP " + str(err.code) + ": " + detail[:300]
    except Exception as err:  # noqa: BLE001
        return str(err)[:300]
    if not audio:
        return "empty audio response"
    with open(out_path, "wb") as handle:
        handle.write(audio)
    return None


def main():
    ap = argparse.ArgumentParser(description="Narrate a chapter to one MP3 via ElevenLabs.")
    ap.add_argument("chapter")
    ap.add_argument("--voice", default="JBFqnCBsd6RMkjVDRZzb")  # George, storyteller
    ap.add_argument("--out", default=None)
    ap.add_argument("--model", default="eleven_multilingual_v2")
    ap.add_argument("--chunk-chars", type=int, default=2500)
    args = ap.parse_args()

    key = load_key()
    if not key:
        print("ERROR: no ELEVENLABS_API_KEY in env or .env", file=sys.stderr)
        return 2
    if not os.path.exists(args.chapter):
        print("ERROR: chapter not found: " + args.chapter, file=sys.stderr)
        return 2

    stem = os.path.splitext(os.path.basename(args.chapter))[0]
    out = args.out or os.path.join("audio", "book-1", stem + ".mp3")
    out_dir = os.path.dirname(out) or "."
    chunk_dir = os.path.join(out_dir, "chunks", stem)
    os.makedirs(chunk_dir, exist_ok=True)

    prose = extract_prose(open(args.chapter, "r", encoding="utf-8").read())
    chunks = chunk_paragraphs(prose, args.chunk_chars)
    print("Narrating " + stem + ": " + str(len(prose)) + " chars in "
          + str(len(chunks)) + " chunk(s), voice " + args.voice, file=sys.stderr)

    chunk_files = []
    for i, ch in enumerate(chunks, 1):
        cf = os.path.join(chunk_dir, "%02d.mp3" % i)
        print("  chunk %02d/%d (%d chars)..." % (i, len(chunks), len(ch)), file=sys.stderr)
        err = tts(ch, args.voice, args.model, key, cf)
        if err:
            print("ERROR on chunk %d: %s" % (i, err), file=sys.stderr)
            return 1
        chunk_files.append(cf)

    # Stitch with ffmpeg concat (stream copy, all chunks share the mp3 codec).
    listfile = os.path.join(chunk_dir, "concat.txt")
    with open(listfile, "w", encoding="utf-8") as handle:
        for cf in chunk_files:
            handle.write("file '" + os.path.abspath(cf) + "'\n")
    res = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                          "-i", listfile, "-c", "copy", out],
                         capture_output=True, text=True)
    if res.returncode != 0:
        print("ffmpeg concat failed: " + res.stderr[-400:], file=sys.stderr)
        return 1
    print(out)  # stdout: the final file path
    return 0


if __name__ == "__main__":
    sys.exit(main())
