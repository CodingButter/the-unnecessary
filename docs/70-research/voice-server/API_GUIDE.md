# Voice API — Client Developer Guide

This document describes how a client application (web, mobile, server) integrates
with the voice system. The system has two cooperating pieces:

1. **Supabase Edge Functions** — business logic, auth, credit deduction, voice design.
2. **FastAPI chatterbox server** — TTS synthesis. Runs on CPU on a host under your control.

Callers almost always talk to **edge functions** first, and the edge function
tells them where to find the FastAPI server (URL + token). The one exception is
the realtime WebSocket, which clients connect to directly for minimum latency.

---

## Contents

- [Architecture at a glance](#architecture-at-a-glance)
- [Authentication](#authentication)
- [Voice design & saving](#voice-design--saving)
- [Listing / deleting voices](#listing--deleting-voices)
- [One-shot TTS (HTTP)](#one-shot-tts-http)
- [Realtime TTS (WebSocket)](#realtime-tts-websocket)
- [Programmatic API keys (optional)](#programmatic-api-keys-optional)
- [Error envelope](#error-envelope)
- [Environment / configuration](#environment--configuration)

---

## Architecture at a glance

```
Browser / client
   │
   │  Supabase JWT (from supabase-js)
   ▼
Supabase Edge Functions           Supabase DB + Storage
 ├─ design-voice                      saved_voices
 ├─ voices                            voice_api_keys
 ├─ tts-stream  (HTTP TTS fallback)   voice-previews/  (bucket)
 └─ tts-token   (WS handshake)
        │
        │  WS URL + token
        ▼
FastAPI chatterbox server (CPU)
 ├─ GET  /healthz
 ├─ POST /tts/synthesize
 └─ WS   /tts/stream
```

- Voice design uses ElevenLabs server-side; the generated preview MP3 is
  stored in Supabase and later used as a reference clip for chatterbox
  voice cloning during synthesis.
- The FastAPI server never talks to ElevenLabs. It only does TTS.
- Credits are deducted by edge functions (`deduct_credits` RPC), not by
  the FastAPI server.

---

## Authentication

All caller requests use the **Supabase user JWT** as a Bearer token. You get
this from `supabase.auth.getSession()` in the browser, or by signing in from
a server.

```ts
const { data: { session } } = await supabase.auth.getSession()
const token = session.access_token
```

- **Edge functions** verify the JWT by calling `supabase.auth.getUser(token)`.
- **FastAPI server** verifies the JWT via the project's JWKS endpoint
  (`/auth/v1/.well-known/jwks.json`), ES256 signing. No shared secret required.

There are no separately-issued session tokens in the normal flow — a Supabase
JWT works everywhere. See
[Programmatic API keys](#programmatic-api-keys-optional) for the rare case
where a non-Supabase caller needs access.

---

## Voice design & saving

**Endpoint:** `POST /functions/v1/design-voice`

The flow is two-step:

1. Generate 3 preview clips from a text description.
2. Save the chosen preview — that preview's MP3 becomes the reference audio
   used by chatterbox for all future synthesis with this voice.

### Step 1 — generate previews

```ts
const res = await fetch(`${SUPABASE_URL}/functions/v1/design-voice`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    action: "generate_previews",
    voice_description: "A warm, raspy, older man with a slow Southern drawl.",
  }),
})
const { previews } = await res.json()
// previews: [{ generated_voice_id, audio_base64, media_type, duration_secs }, ...]
```

**Cost:** 100 credits per call (regardless of how many previews the user listens to).
**Validation:** `voice_description` must be 20–1000 characters.

### Step 2 — save the chosen preview

```ts
const chosen = previews[1] // e.g. the user picked the second preview
const save = await fetch(`${SUPABASE_URL}/functions/v1/design-voice`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    action: "save_voice",
    voice_name: "Gus",
    voice_description: "The voice above.",        // optional
    generated_voice_id: chosen.generated_voice_id,
    audio_base64: chosen.audio_base64,
    media_type: chosen.media_type,                // optional, default "audio/mpeg"
    is_default: false,                            // optional
  }),
})
const saved = await save.json()
// { id: "<uuid>", voice_id: "<generated_voice_id>", voice_name: "Gus", provider: "elevenlabs+chatterbox" }
```

Returns the `saved_voices.id` UUID. **Pass this `id` (not `voice_id`) to all
subsequent TTS calls.**

**Cost:** 50 credits per save.

---

## Listing / deleting voices

**Endpoint:** `/functions/v1/voices`

```ts
// List
const { voices } = await (await fetch(`${SUPABASE_URL}/functions/v1/voices`, {
  headers: { Authorization: `Bearer ${token}` },
})).json()
// voices: [{ id, voice_name, voice_id, preview_path, preview_format, is_default, created_at, ... }]

// Get one + signed preview URL
const one = await (await fetch(`${SUPABASE_URL}/functions/v1/voices/${id}`, {
  headers: { Authorization: `Bearer ${token}` },
})).json()
// { id, voice_name, ..., preview_url: "<1-hour signed URL>" }

// Set default
await fetch(`${SUPABASE_URL}/functions/v1/voices/${id}/default`, {
  method: "POST",
  headers: { Authorization: `Bearer ${token}` },
})

// Delete (row + storage object)
await fetch(`${SUPABASE_URL}/functions/v1/voices/${id}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${token}` },
})
```

---

## One-shot TTS (HTTP)

For short clips, simple use cases, or non-browser callers. Returns a single
WAV blob. Latency = full synthesis time (a few seconds on CPU for short text).

**Endpoint:** `POST /functions/v1/tts-stream`

```ts
const res = await fetch(`${SUPABASE_URL}/functions/v1/tts-stream`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    voice_id: saved.id,    // saved_voices.id UUID
    text: "Hello, world.",
  }),
})
const audioBlob = await res.blob()               // audio/wav
const audioUrl = URL.createObjectURL(audioBlob)
new Audio(audioUrl).play()

// Response headers include:
//   X-Credits-Used: 1
//   X-Characters-Processed: 13
//   X-Sample-Rate: 24000
```

**Limits:** text ≤ 4000 chars.
**Cost:** `ceil(chars * credits_per_1000 / 1000)` — rate card entry for
`provider='chatterbox', operation='tts_characters'` (default: 100 per 1000).

Credits are charged **before** synthesis; on upstream failure the edge
function posts a negative `deduct_credits` entry to refund.

---

## Realtime TTS (WebSocket)

For chat-style interactive use where the client wants audio to start playing
as soon as the first frame is ready and wants to barge-in / cancel mid-synth.

### Step 1 — get a connection handle

```ts
const handle = await (await fetch(`${SUPABASE_URL}/functions/v1/tts-token`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ voice_id: saved.id }),
})).json()
//
// {
//   websocket_url: "wss://voice-api.example.com/tts/stream?token=<jwt>&voice_id=<id>",
//   base_url:      "wss://voice-api.example.com/tts/stream",
//   voice_row_id:  "<uuid>",
//   voice_name:    "Gus",
//   token:         "<the jwt passed through>",
//   expires_at:    1776468000,
//   protocol:      { init: {...}, hint: "..." }
// }
```

### Step 2 — connect and stream

```ts
const ws = new WebSocket(handle.websocket_url)

ws.addEventListener("open", () => {
  ws.send(JSON.stringify({ type: "init", voice_id: handle.voice_row_id }))
})

const chunks: Int16Array[] = []
let sampleRate = 24000

ws.addEventListener("message", (ev) => {
  const msg = JSON.parse(ev.data)
  switch (msg.type) {
    case "ready":
      ws.send(JSON.stringify({
        type: "synthesize",
        text: "Good mornin', darlin'.",
        request_id: "utt-1",
      }))
      break
    case "audio": {
      const bytes = Uint8Array.from(atob(msg.pcm16), c => c.charCodeAt(0))
      chunks.push(new Int16Array(bytes.buffer, bytes.byteOffset, bytes.byteLength / 2))
      break
    }
    case "end":
      sampleRate = msg.sample_rate ?? sampleRate
      console.log("done", msg.char_count, "chars in", msg.duration_ms, "ms")
      // You can send more `synthesize` messages on the same connection.
      break
    case "error":
      console.error("ws error", msg)
      break
  }
})

// Barge-in: stop current synth
ws.send(JSON.stringify({ type: "cancel", request_id: "utt-1" }))
```

### Protocol reference

```jsonc
// client -> server
{"type":"init",        "voice_id":"<saved_voices.id>"}                 // FIRST message only
{"type":"synthesize",  "text":"...", "request_id":"utt-1"}             // N times on same conn
{"type":"cancel",      "request_id":"utt-1"}                           // best effort

// server -> client
{"type":"ready",  "frame_ms":40}                                       // after init
{"type":"audio",  "request_id":"utt-1", "seq":0, "pcm16":"<b64 pcm16>"}
{"type":"audio",  "request_id":"utt-1", "seq":1, "pcm16":"<b64 pcm16>"}
{"type":"end",    "request_id":"utt-1", "sample_rate":24000, "char_count":18, "duration_ms":812, "frames":20}
{"type":"error",  "request_id":"utt-1"?, "code":"...", "message":"..."}
```

- PCM is **mono, 16-bit signed little-endian**. Sample rate arrives on `end`
  (Chatterbox-Turbo is typically 24 kHz).
- The same connection handles many sequential `synthesize` requests — keep it
  open for the whole user session to avoid reconnect cost.
- `cancel` will interrupt in-flight synthesis and abort emission of further
  frames for that `request_id`. An `end` with `cancelled: true` follows.

### Credit tracking

The FastAPI server does not charge credits. The client should aggregate
`char_count` from each `end` message and, at session end, report usage to the
existing `end-session` edge function (if you're inside a provider session)
**or** use `tts-stream` instead of the WS path if you want per-call
auto-deduction.

---

## Programmatic API keys (optional)

If a non-browser caller (backend service, cron job, CLI) needs access and
doesn't have a Supabase user session, they can use an API key:

```bash
# 1. User (with a valid Supabase JWT) creates a key via FastAPI:
curl -X POST https://voice-api.example.com/api-keys \
  -H "Authorization: Bearer $SUPABASE_JWT" \
  -H "Content-Type: application/json" \
  -d '{"name":"scheduled-report"}'

# Response: { id, name, key_prefix, api_key: "vsk_live_<prefix>_<secret>", ... }
# Store api_key somewhere safe — it will never be shown again.

# 2. Later, exchange the API key for a short-lived Supabase JWT:
curl -X POST https://voice-api.example.com/sessions \
  -H "X-API-Key: vsk_live_<prefix>_<secret>"

# Response: { session_token, expires_at, expires_in }

# 3. Use session_token as a Supabase JWT for any edge function or FastAPI route.
```

Notes:
- API keys are stored hashed (SHA-256 of the full key).
- Key lookup + validation happens inside Postgres via the SECURITY DEFINER
  RPC `verify_voice_api_key` — no service role needed server-side.
- Session tokens are minted with `SUPABASE_JWT_SECRET` and default to a 5-min
  TTL. This feature requires that secret to be set on the FastAPI server.
  If you don't need programmatic access, you can skip setting it and users
  will still use their normal Supabase JWT everywhere.

---

## Error envelope

Edge functions return JSON errors with HTTP status codes:

```json
{ "error": "short message", "details": "optional extra" }
```

FastAPI errors follow the same shape (`detail` field, per FastAPI's default).

Common statuses:
- `400` bad input
- `401` missing/invalid token
- `402` insufficient credits
- `403` voice belongs to another user
- `404` voice / API key not found
- `409` voice has no preview audio
- `502` upstream TTS or ElevenLabs failure
- `503` configuration missing (no VOICE_API_URL, no ELEVENLABS_API_KEY)

---

## Environment / configuration

### FastAPI server (chatterbox)

Required env (from `.env` at project root):

```env
ELEVENLABS_API_KEY=                # only if you want to proxy voice design through FastAPI directly
SUPABASE_URL=https://<proj>.supabase.co
SUPABASE_ANON_KEY=eyJ...
# SUPABASE_JWT_SECRET=             # optional, only needed for /sessions minting
# SUPABASE_SERVICE_ROLE_KEY=       # optional, no route currently uses it

VOICE_PREVIEWS_BUCKET=voice-previews
VOICE_SESSION_TTL_SECONDS=300

CHATTERBOX_DEVICE=cpu              # "cuda" when you add a GPU
TTS_MAX_CONCURRENCY=1              # Serialize synth; CPU can't parallelize usefully

HOST=0.0.0.0
PORT=8080
```

### Supabase vault secrets

Already configured (via MCP), read by edge functions via the `get_secret` RPC:

- `ELEVENLABS_API_KEY` — used by `design-voice`
- `VOICE_API_URL` — **must be updated to the real FastAPI host** before prod.
  Currently set to `https://voice.example.com` as a placeholder.
  To update:
  ```sql
  select vault.update_secret(
    (select id from vault.secrets where name='VOICE_API_URL'),
    'https://your-actual-voice-api.example.com'
  );
  ```

### Running locally

```bash
cd voice/
uv venv -p python3.12 --seed                # or: python3 -m venv .venv
source .venv/bin/activate
pip install -e .                             # installs torch + chatterbox (slow)
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Docker

```bash
docker compose up -d --build
# first build is slow (pulls torch + chatterbox model weights on first request)
```

---

## Deployment checklist

- [ ] Deploy FastAPI server (Docker) on a host with ≥4 CPU cores, ≥8 GB RAM, persistent volume for model cache
- [ ] Update `VOICE_API_URL` in Supabase vault to the deployed URL
- [ ] Verify: `curl $VOICE_API_URL/healthz` returns `{"status":"ok","device":"cpu"}`
- [ ] Verify: call `design-voice` / `generate_previews` from an authenticated client
- [ ] Verify: call `design-voice` / `save_voice` and confirm a row appears in `saved_voices` with `preview_path` set
- [ ] Verify: call `tts-stream` with a saved voice and play the returned WAV
- [ ] Verify: `tts-token` returns a `websocket_url` pointing at the real host
- [ ] Verify: WebSocket opens, `init` → `ready`, `synthesize` → `audio`* → `end`
- [ ] Adjust `rate_cards` row `(provider='chatterbox', operation='tts_characters')` if you want different pricing.
