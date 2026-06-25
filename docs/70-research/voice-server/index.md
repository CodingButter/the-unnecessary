---
title: "Voice Server (Chatterbox TTS) — API Reference"
document_type: "reference"
status: "active"
authority: "reference"
summary: "Self-hosted Chatterbox TTS API reference for the project's own voice server (FastAPI, port 8080; reachable at tts.codingbutter.com). Documents the /api/generate file endpoint, the /api/synthesize PCM16 stream, and the shared voice + emotion + tuning-knob control surface. Basis for the planned voice-server narration script."
tags: ["reference", "voice-server", "chatterbox", "tts", "narration", "tooling", "api"]
related:
  - "./API_DOC.md"
  - "./API_GUIDE.md"
  - "../../00-governance/decision-log/decisions/048-narration-script-phase.md"
source_documents:
  - "docs/70-research/voice-server/API_DOC.md"
  - "docs/70-research/voice-server/API_GUIDE.md"
---

# Voice Server (Chatterbox TTS) — API Reference

Reference for the project's **self-hosted Chatterbox TTS** voice server, fetched from the
dev machine (`codingbutter@10.0.0.213:~/voice/`) on 2026-06-25. This is the engine behind
the `Will_Wheaton` voice. It will back a future `narrate-chapter-voiceserver.py` (the
Chatterbox counterpart to the ElevenLabs `narrate-chapter.py`).

The author is still updating the server and its docs; treat this as a working snapshot and
re-fetch when handed a newer version.

## Files

- **[API_DOC.md](API_DOC.md)** — the HTTP API itself: endpoints, the control surface (knobs),
  emotion presets, output formats.
- **[API_GUIDE.md](API_GUIDE.md)** — client developer guide: the Supabase edge-function layer
  (auth, credits, voice design) in front of the FastAPI synthesis server.

## What matters for narration (quick reference)

- **`POST /api/generate`** → a complete, level-normalized **WAV/MP3 file** (one-shot, best
  quality). This is the right call for offline audiobook rendering — no streaming, no
  underrun/stutter. (`/api/synthesize` is the real-time PCM16 stream we use for live replies.)
- Server: FastAPI on **port 8080**; `GET /api/voices` lists voices (e.g. `Will_Wheaton`);
  output **sample_rate 24000**, mono.
- **Direction comes from knobs, not bracket tags** (Chatterbox has no inline `[tag]` syntax):
  `voice` (required), `text` (required), `emotion` (12 presets: angry, calm, cheerful,
  dramatic, excited, fearful, ...), `exaggeration` (0.25–2.0, def 0.5), `cfg_weight` (0.0–1.0,
  def 0.5), `temperature` (0.05–1.5, def 0.8), `repetition_penalty` (1.0–2.0, def 1.2),
  `top_p` (0.05–1.0, def 0.95). Resolution order: defaults → emotion bundle → individual knobs.
- **Pauses/pacing** come from punctuation (ellipses) and inserted silence between segments;
  pronunciation fixes come from phonetic spelling. See the Chatterbox narration plan.
- **Auth:** the direct `/api/*` routes have no built-in auth (the edge-function layer handles
  auth/credits for app clients); a host/LAN-side batch renderer can call the FastAPI server
  directly, exactly as the ElevenLabs `narrate-chapter.py` calls its API directly.
