# Voice TTS API

Self-hosted text-to-speech (Chatterbox) with voice cloning, emotion presets, and
full tuning control. Two ways to get audio:

- **`POST /api/generate`** → a complete **WAV/MP3 file** (one-shot, best quality). Use this for audiobooks / offline rendering.
- **`POST /api/synthesize`** → a **real-time PCM16 stream**. Use this for live playback.

Both share the exact same control surface (voice + emotion + tuning knobs).

---

## Base URL & access

The service listens on port **8080**.

| From | URL |
|------|-----|
| **Public (anywhere)** | **`http://tts.codingbutter.com`** |
| Same machine | `http://localhost:8080` |
| Another machine on the LAN | `http://10.0.0.213:8080` |

The public URL is served over a tunnel — use it as-is (no `:8080` port needed). All
examples below use `localhost`; swap in `http://tts.codingbutter.com` from anywhere else.

> **⚠️ Security:** the `/api/*` routes have **no built-in authentication**. Since
> `tts.codingbutter.com` is public, anyone who knows the hostname can use your GPU to
> generate speech. Put access control at the tunnel/edge (e.g. Cloudflare Access, a
> reverse-proxy auth, or an IP allowlist) if that matters. (The separate `/mcp`
> endpoint is API-key gated and is for MCP clients, not these REST calls.)

Quick health check:

```bash
curl http://localhost:8080/healthz
# {"status":"ok","device":"cuda"}
```

Interactive OpenAPI docs (auto-generated): **`http://localhost:8080/docs`**

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

## Other endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/` | Browser UI (pick a voice, type, hear it). |
| `GET` | `/api/voices` | List voices, emotions, ranges. |
| `GET` | `/api/voice-preview/{id}` | Download the raw reference clip for a voice. |
| `GET` | `/healthz` | Liveness + device. |
| `GET` | `/docs` | Interactive OpenAPI docs. |

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

API   = "http://tts.codingbutter.com"   # public URL (or http://10.0.0.213:8080 on the LAN)
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
    r = requests.post(f"{API}/api/generate", json=payload, timeout=900)
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
| `400` | Unknown `emotion`, or bad `format`. |
| `422` | Empty text / no audio produced. |
| `500` | Synthesis failed. |

Out-of-range tuning values are **clamped**, not rejected.

---

## MCP server (optional, for AI agents)

The same engine is exposed as an MCP server at `POST /mcp` (Streamable HTTP) with
tools `synthesize`, `list_voices`, `upload_voice`. It supports `X-Play-Local: true`
to play on the server's own speakers. This is for MCP clients (e.g. Claude Code) and
is gated by `X-API-Key`; the REST endpoints above are the path for your own scripts.
