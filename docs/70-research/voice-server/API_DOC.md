# Voice API

Self-hosted **text-to-speech** (Chatterbox, with voice cloning + emotion presets +
full tuning) **and speech-to-text** (Whisper `large-v3`).

Text → speech:

- **`POST /api/generate`** → a complete **WAV/MP3 file** (one-shot, best quality). Use this for audiobooks / offline rendering.
- **`POST /api/synthesize`** → a **real-time PCM16 stream**. Use this for live playback.

Both TTS paths share the exact same control surface (voice + emotion + tuning knobs).

Speech → text:

- **`POST /api/transcribe`** → upload an audio file, get the **transcript** back (with optional language auto-detect, segment timestamps, and translate-to-English).

---

## Base URL & access

The service listens on port **8080**.

| From | URL |
|------|-----|
| **Public (anywhere)** | **`http://voice.codingbutter.com`** |
| Same machine | `http://localhost:8080` |
| Another machine on the LAN | `http://10.0.0.213:8080` |

The public URL is served over a tunnel — use it as-is (no `:8080` port needed). All
examples below use `localhost`; swap in `http://voice.codingbutter.com` from anywhere else.

Quick health check (public, no auth):

```bash
curl http://localhost:8080/healthz
# {"status":"ok","device":"cuda"}
```

Interactive OpenAPI docs (auto-generated): **`http://localhost:8080/docs`**

---

## Authentication

The `/api/*` data routes (voices, synthesize, generate, transcribe, voice-preview)
require a login. Accounts live in **`users.json`** at the project root:

```json
[
  { "username": "admin", "password": "change-me" }
]
```

There are **two ways to authenticate**, both backed by that file:

**1. Browser — session cookie.** The web UI shows a login page; on success the
server sets a signed, HttpOnly cookie and you use the app normally (with a Log out
button). Scripts can do the same:

```bash
# Log in, save the cookie, then call protected routes with it
curl -c cookies.txt -X POST http://localhost:8080/api/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"change-me"}'
curl -b cookies.txt http://localhost:8080/api/voices
```

**2. Scripts / CLI — HTTP Basic auth.** Simplest for `curl` and the MCP shim — just
send the same username/password:

```bash
curl -u admin:change-me http://localhost:8080/api/voices
```

> Public (no auth): `/` (login page), `/healthz`, `/docs`. The `/mcp` endpoint has
> its own API-key gate. Unauthenticated `/api/*` calls return **401**.
>
> **All `curl` examples below need auth** — add `-u <user>:<password>` (or a login
> cookie). They're omitted from each example for brevity.

Auth endpoints: `POST /api/login` `{username,password}` → sets cookie; `POST
/api/logout` → clears it; `GET /api/me` → 200 + `{username}` when authenticated,
else 401.

---

## Voices

Voices are reference clips on disk (server-side). List them at runtime:

```bash
curl http://localhost:8080/api/voices
```

```jsonc
{
  "voices": [
    {"id": "Will_Wheaton", "name": "Will Wheaton", "format": "mp3"},
    {"id": "Aragon_Voice", "name": "Aragon",       "format": "mp3"}
    // ...
  ],
  "emotions": ["angry","calm","cheerful","dramatic","excited","fearful",
               "happy","narrator","neutral","sad","serious","soft"],
  "setting_ranges": {
    "exaggeration":        [0.25, 2.0],
    "cfg_weight":          [0.0, 1.0],
    "temperature":         [0.05, 1.5],
    "repetition_penalty":  [1.0, 2.0],
    "top_p":               [0.05, 1.0]
  },
  "sample_rate": 24000,
  "max_chars": 4000
}
```

Use the **`id`** (e.g. `Will_Wheaton`) as the `voice` field in requests.

Currently installed: `Aragon_Voice`, `Bay_Area_Buggs`, `Ezra_Pike_Voice`,
`Harry_Kroto`, `Mario_Vance_Voice`, `Simon_Singh`, `Werner_Herzog`, `Will_Wheaton`.

---

## Control surface (all endpoints)

Every synthesis request accepts these fields. All are optional except `voice` and `text`.

| Field | Type | Range | Default | What it does |
|-------|------|-------|---------|--------------|
| `voice` | string | — | *required* | Voice `id` from `/api/voices`. |
| `text` | string | 1–4000 (stream) / 1–12000 (file) | *required* | Text to speak. |
| `emotion` | string | one of 12 | none | **Sentiment preset** — sets exaggeration/cfg_weight/temperature for you. |
| `exaggeration` | float | 0.25–2.0 | 0.5 | Emotional energy. Higher = livelier & faster; ≥0.85 can get unstable. |
| `cfg_weight` | float | 0.0–1.0 | 0.5 | Adherence to the reference voice + pacing. Lower = looser/more varied. |
| `temperature` | float | 0.05–1.5 | 0.8 | Randomness. Lower = steadier; higher = more varied (risk of artifacts). |
| `repetition_penalty` | float | 1.0–2.0 | 1.2 | Discourages repeats. ~1.2 = natural; 2.0 flattens prosody. |
| `top_p` | float | 0.05–1.0 | 0.95 | Nucleus sampling width. ~0.95 = natural. |

**Resolution order:** built-in defaults → `emotion` bundle → any individual knob you pass.
So `{"emotion":"excited","temperature":0.7}` uses the *excited* bundle but with your
own temperature.

### Emotions

`neutral`, `calm`, `serious`, `sad`, `happy`, `cheerful`, `excited`, `angry`,
`fearful`, `dramatic`, `narrator`, `soft`.

> **Note:** Chatterbox has no native "emotion" input — these are curated presets that
> set the real knobs. For fine control, pass the individual knobs instead of (or on
> top of) an emotion. For pronunciation, spell tricky words/acronyms phonetically in
> the `text` (e.g. write `"S Q L"` or `"twenty twenty-six"`); there is no SSML/phoneme support.

---

## `POST /api/generate` — download a complete audio file

Best quality. Renders text **one sentence/paragraph at a time** (no streaming
boundary artifacts), soft-limits to prevent clipping, and **loudness-normalizes** so
every voice comes out at a consistent level. Returns the file as an attachment.

### Extra fields (file-only)

| Field | Type | Default | What it does |
|-------|------|---------|--------------|
| `format` | `"wav"` \| `"mp3"` | `"wav"` | Output container. |
| `normalize` | bool | `true` | Peak-normalize the whole render to a consistent level. |
| `gap_seconds` | float | `0.3` | Silence inserted between paragraphs. |

### Response

Binary audio. Headers: `Content-Disposition: attachment; filename="<Voice>.wav"`,
`X-Sample-Rate: 24000`, `X-Duration-Seconds`.

### Examples

```bash
# WAV
curl -X POST http://localhost:8080/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"voice":"Will_Wheaton","text":"Chapter one. It was a dark and stormy night.","emotion":"narrator"}' \
  -o chapter1.wav

# MP3 with explicit tuning
curl -X POST http://localhost:8080/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"voice":"Werner_Herzog","text":"The jungle is obscene.","format":"mp3","exaggeration":0.45,"cfg_weight":0.6,"temperature":0.7,"repetition_penalty":1.2,"top_p":0.95}' \
  -o line.mp3
```

> `text` accepts up to 12000 chars and is auto-split into sentences internally. For a
> whole book, loop per chapter/section in your script (below) so you get progress,
> resumability, and one file per piece.

---

## `POST /api/synthesize` — real-time stream

Streams raw **PCM16, mono, 24 kHz, little-endian** (`audio/L16`) as it's generated,
sentence by sentence (so it stays ahead of real-time even on long passages). Use this
for live playback, not for saving files.

```bash
# Pipe straight into a player (note the raw-PCM flags):
curl -sN -X POST http://localhost:8080/api/synthesize \
  -H 'Content-Type: application/json' \
  -d '{"voice":"Aragon_Voice","text":"Hello from the streaming endpoint.","emotion":"happy"}' \
| ffplay -autoexit -nodisp -loglevel quiet -f s16le -ar 24000 -ac 1 -
```

To save a stream to a WAV, prefer `/api/generate`. If you must convert a stream:

```bash
curl -sN -X POST http://localhost:8080/api/synthesize -H 'Content-Type: application/json' \
  -d '{"voice":"Aragon_Voice","text":"..."}' \
| ffmpeg -f s16le -ar 24000 -ac 1 -i - out.wav
```

---

## `POST /api/transcribe` — speech to text

Upload an audio file and get the transcript back. Powered by Whisper
(`large-v3` via faster-whisper). The model decodes the container itself, so you
can send **WAV, MP3, M4A, OGG, FLAC, or WebM** directly — no client-side
conversion. This is a **`multipart/form-data`** request (not JSON).

### Fields

| Field | Type | Default | What it does |
|-------|------|---------|--------------|
| `file` | file | *required* | The audio to transcribe (any common container, up to 100 MB). |
| `language` | string | auto | Force the source language (ISO code, e.g. `en`, `es`). Omit to auto-detect. |
| `task` | `transcribe` \| `translate` | `transcribe` | `transcribe` keeps the spoken language; `translate` outputs **English** text. |
| `timestamps` | bool | `false` | Also return per-segment start/end times. |

### Response

JSON:

```jsonc
{
  "text": "The full transcript as one string.",
  "language": "en",              // detected (or forced) language
  "language_probability": 0.99,  // detector confidence
  "duration": 12.34,             // seconds of audio
  "segments": [                  // only present when timestamps=true
    {"start": 0.0, "end": 3.2, "text": "The full transcript"},
    {"start": 3.2, "end": 6.1, "text": "as one string."}
  ]
}
```

### Examples

```bash
# Basic transcription
curl -X POST http://localhost:8080/api/transcribe \
  -F file=@meeting.m4a

# Force language + segment timestamps (for subtitles)
curl -X POST http://localhost:8080/api/transcribe \
  -F file=@clip.mp3 -F language=en -F timestamps=true

# Translate foreign-language speech to English text
curl -X POST http://localhost:8080/api/transcribe \
  -F file=@spanish.wav -F task=translate
```

> First-time setup: the Whisper weights must be cached on disk before the first
> request (the service runs HuggingFace in offline mode so cold boots can't hang).
> Run `python scripts/preload_whisper.py` once after install. The model size is
> set by `WHISPER_MODEL` (default `large-v3`); `WHISPER_DEVICE` / `WHISPER_COMPUTE_TYPE`
> control placement (`cuda` + `float16` on GPU).

---

## Other endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `GET` | `/` | public | Browser UI (login gate + TTS + speech-to-text). |
| `POST` | `/api/login` | public | Log in `{username,password}` → sets session cookie. |
| `POST` | `/api/logout` | public | Clear the session cookie. |
| `GET` | `/api/me` | yes | `{username}` when authenticated, else 401. |
| `GET` | `/api/voices` | yes | List voices, emotions, ranges. |
| `GET` | `/api/voice-preview/{id}` | yes | Download the raw reference clip for a voice. |
| `POST` | `/api/transcribe` | yes | Speech to text (Whisper). |
| `GET` | `/healthz` | public | Liveness + device. |
| `GET` | `/docs` | public | Interactive OpenAPI docs. |

---

## Python: audiobook generation script

Renders a book to one audio file per chapter using `/api/generate`. Splits on a
`# Chapter` heading; everything is normalized and consistent across chapters.

```python
#!/usr/bin/env python3
"""Generate an audiobook from a plain-text file, one MP3 per chapter."""
import re
import sys
import time
from pathlib import Path

import requests  # pip install requests

API   = "http://voice.codingbutter.com"   # public URL (or http://10.0.0.213:8080 on the LAN)
AUTH  = ("admin", "change-me")     # (username, password) from users.json
VOICE = "Will_Wheaton"
EMOTION = "narrator"               # or None, or per-chapter
FORMAT = "mp3"                     # "mp3" or "wav"
OUTDIR = Path("audiobook")
# Optional fine-tuning (None = use the emotion/default):
TUNING = {
    "exaggeration": None,
    "cfg_weight": None,
    "temperature": 0.7,
    "repetition_penalty": 1.2,
    "top_p": 0.95,
}

def split_chapters(text: str):
    """Yield (title, body). Splits on lines like '# Chapter 1' or 'CHAPTER ONE'."""
    parts = re.split(r"(?im)^\s*#?\s*(chapter\b.*)$", text)
    if len(parts) == 1:
        yield ("chapter", text.strip()); return
    # parts = [pre, title1, body1, title2, body2, ...]
    pre = parts[0].strip()
    if pre:
        yield ("intro", pre)
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if body:
            yield (title, body)

def generate(text: str, out: Path):
    payload = {"voice": VOICE, "text": text, "emotion": EMOTION,
               "format": FORMAT, "normalize": True,
               **{k: v for k, v in TUNING.items() if v is not None}}
    r = requests.post(f"{API}/api/generate", json=payload, auth=AUTH, timeout=900)
    r.raise_for_status()
    out.write_bytes(r.content)
    secs = float(r.headers.get("X-Duration-Seconds", 0))
    print(f"  -> {out.name}  ({len(r.content)//1024} KB, {secs:.1f}s audio)")

def slug(s: str) -> str:
    return re.sub(r"[^\w]+", "_", s).strip("_").lower()[:60] or "chapter"

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: audiobook.py book.txt")
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    OUTDIR.mkdir(exist_ok=True)
    for n, (title, body) in enumerate(split_chapters(text), 1):
        out = OUTDIR / f"{n:02d}_{slug(title)}.{FORMAT}"
        if out.exists():
            print(f"[{n:02d}] skip (exists) {title!r}"); continue
        print(f"[{n:02d}] {title!r}  ({len(body)} chars)")
        t = time.time()
        generate(body, out)
        print(f"     done in {time.time()-t:.0f}s")
    print("All chapters rendered to", OUTDIR.resolve())

if __name__ == "__main__":
    main()
```

Run it:

```bash
pip install requests
python audiobook.py mybook.txt
# -> audiobook/01_chapter_one.mp3, 02_chapter_two.mp3, ...
```

### Tips for audiobook quality

- **Use `/api/generate`** (file), not the stream — no chunk-boundary artifacts.
- Keep `normalize: true` so chapters match in loudness.
- For narration, `emotion="narrator"` (or `neutral`) with `temperature` ~0.65–0.75 is
  stable; switch emotion per character for dialogue.
- If a word is mispronounced, respell it phonetically in the text — there is no SSML.
- One file per chapter (the script skips already-rendered files, so it's resumable).
- Long renders take a while (roughly real-time on GPU); the script prints progress.

---

## Error responses

JSON `{"detail": "..."}` with status:

| Status | Meaning |
|--------|---------|
| `404` | Unknown `voice`. |
| `400` | Unknown `emotion`, bad `format`, or invalid `task`. |
| `413` | Uploaded audio too large (transcribe; max 100 MB). |
| `422` | Empty text/upload, or no audio produced. |
| `500` | Synthesis or transcription failed. |

Out-of-range tuning values are **clamped**, not rejected.

---

## MCP server (optional, for AI agents)

The same engine is exposed as an MCP server at `POST /mcp` (Streamable HTTP) with
tools `synthesize`, `transcribe`, `list_voices`, `upload_voice`. `synthesize`
supports `X-Play-Local: true` to play on the server's own speakers; `transcribe`
takes audio as `audio_base64` or a `source_url` and returns the text. This is for
MCP clients (e.g. Claude Code) and is gated by `X-API-Key`; the REST endpoints
above are the path for your own scripts.
