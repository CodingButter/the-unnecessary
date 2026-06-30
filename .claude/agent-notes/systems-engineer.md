# Field Notes -- systems-engineer

> Durable, verified lessons this agent has learned in its field. One lesson per entry, dated (ISO), with its source/citation. The charter (.claude/agents/systems-engineer.md) is the stable role; this file is the growing, citable knowledge. The author may prune.

## 2026-06-30 -- Voice server /api/transcribe: free SEGMENT timestamps, no word-level

Probed the local Whisper endpoint (voice.codingbutter.com, faster-whisper, device cuda).
Verified facts (each tested with a real POST):
- Default response keys: `text`, `language`, `language_probability`, `duration` (no timing).
- POST a multipart field `timestamps=true` -> response gains a `segments` array of
  `{start, end, text}` (SEGMENT-level timing) at NO extra cost (same call, local/free).
  Segments break at sentence boundaries, so the inter-segment gap = a real detected pause.
- `word_timestamps=true` / `timestamp_granularities=word` / `response_format=verbose_json`
  are NOT honored -- the server build never returns a word-level array. Recommend exposing
  faster-whisper's `word_timestamps` server-side if word-level local timing is ever needed.
- ElevenLabs Scribe DOES return word-level `words[]` = `{text,start,end,type,logprob}`
  (`type` is "word" or "spacing") -- metered. Use only on already-flagged chunks.
Source: scripts/verify-narration.py pacing pass (transcribe_timed / encode_multipart
`timestamps` field); probe runs 2026-06-30.

## 2026-06-30 -- Live per-line stems QC bridge = stems.manifest.json

The live pipeline's `render-voice-stems.py` writes `stems.manifest.json` next to the
cue sheet, one entry per cue. Voice entries carry `{i, type:"voice", role, voice, file,
filter, gap_before, text, dur, err}`; the wav lives at `<scene>/voice/<file>`. sfx/music
entries carry `{i, type, asset, gain, gap_before}` and have no spoken script. This manifest
is the correct input to QC the live/dramatized audiobook per line (verify-narration.py
`--live-scene <scene-dir>` builds units from it). Source: scripts/render-voice-stems.py:168-204;
scripts/verify-narration.py build_live_units().

## 2026-06-30 -- mix-live-scene.py: deterministic encode, untracked renders

- The encode is DETERMINISTIC: two runs of the same cue sheet produce a byte-identical
  `scene-live.mp3` (libmp3lame `-q:a 2`, no timestamps), so byte-identical back-compat is
  testable by md5. Verified: scene-04 ran twice -> identical md5 each time.
- The live-audio renders (`audio/live-audio-book/**/scene-live.mp3`, chapter `.live.mp3`)
  are UNTRACKED generated artifacts, NOT git canon. Running the mixer regenerates them
  harmlessly; no need to restore. Only the `scripts/` change is the deliverable.
  Source: `git ls-files --error-unmatch` returned untracked for scene-04/scene-live.mp3.

## 2026-06-30 -- SFX silence-trim must clear the loudnorm floor; edge-only

- `normalize-stems.py` loudnorms SFX to -20 LUFS, which RAISES the "silent" floor of the
  normalized stems (`sfx_norm/`, what the mixer actually reads) to roughly -50..-52 dB. So
  `silenceremove` at -55 dB barely trims them (key-lock-door 0.024s); at -50 dB it removes
  the real edge dead air (doorbell-ring 0.89s, phone-dock 0.26s, monitor-drag 0.10s).
  Calibrate SFX trim thresholds to the POST-loudnorm floor (-50 dB), not the raw asset.
- Edge-only trim (areverse `silenceremove` sandwich) does NOT remove INTERNAL dead air.
  key-lock-door's measured ~2.1s is an internal gap + a trailing blip, so edge-trim leaves
  it (correctly) -- that is an asset re-cut routed to live-narration-director, not a mixer
  job. Internal rhythm (doorbell ring spacing, drag mid-pause) is preserved by design.
  Source: measured `silenceremove` deltas at -55/-50/-48 dB; design doc
  `docs/70-research/ch1-audio-overhaul-design.md` sec.0 + Part B.

## 2026-06-30 -- Content-aware ducking = muffle_suffix() twin, opt-in

- Built exactly like `muffle_suffix()`: a per-frame `volume@duck=...:eval=frame` envelope
  keyed to voice spans, chained AFTER `volume@fb`, composing by multiplication with the
  flashback duck and `bed_gain x MUSIC_GAIN_SCALE`. Opt-in via a scene-level `ducking`
  block; absent => `DUCK=""` => every music/SFX suffix reduces to `MUFFLE` => filtergraph
  byte-identical to pre-ducking (proven: stripping the one `volume@duck` node from the duck
  filtergraph == the no-duck filtergraph).
- ffmpeg expr parses parenthesized negative literals `clip((t-(-0.300))/0.3,...)` fine --
  needed for pre-roll when a span starts before `attack`. Depth->linear is `10**(dB/20)`
  (-9 dB=0.3548, -6 dB=0.5012). The `hold` merge (0.6 s) intentionally collapses a dense
  conversation into a few regions so the bed only lifts in genuine breaths (gaps > hold),
  not between words -- that is the design intent, not a bug. Source: this session; design
  doc Part A.

## 2026-06-30 -- Voice server /api/embed is LIVE: resemblyzer-ge2e, dim 256, L2-normalized

- Built `scripts/cast-audit.py` (casting-director acoustic ensemble audit). The
  speaker-embedding endpoint is already live and answers: `POST /api/embed` multipart
  `file` -> `{"embedding":[256 floats], "dim":256, "model":"resemblyzer-ge2e"}`, L2-normalized
  (cosine == dot). Same HTTP-Basic creds + proxy-bypass opener + browser-UA as the renderer.
- Cue `role` -> cast slug resolves cleanly by token-matching a hyphen-part of the roster slug
  (eli->rook-eli, dorsey->dorsey-ray, lena->okafor-lena, eli_thought->rook-eli); only the
  narrator family needs an alias (narration/notice->narrator). `elder` is a render-only
  non-canon generic with no roster slug -> reported unmapped, never guessed. Source: roster
  slugs in `docs/10-vision/audio/cast-sheet.md`; roles surveyed across
  `audio/live-audio-book/**/cues.json`.
- Pick-of-3 minimax is solved EXACTLY for the whole 12-node ensemble in ~1.4s by PRECOMPUTING
  the candidate-vs-candidate cosine per co-present pair (each selection score = O(pairs)
  lookups, not O(dim) vector math); naive per-selection vector math would force the greedy
  fallback. Lesson: precompute the pair tables before any 3^k sweep.
- Finding (current samples): the binding co-present collision is `dorsey-ray + rook-eli`
  (minimax cosine 0.754 > 0.75) -- both flat-Michigan/Detroit males by design; no sample
  choice separates them below threshold, so it is a genuine voice-REGENERATION candidate, not
  a selection problem. Report: `docs/10-vision/audio/_generated/cast-audit/cast-audit.md`.
