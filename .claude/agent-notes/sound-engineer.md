# sound-engineer — field notes

Durable, sourced lessons for the live-audio mix craft. One dated entry per lesson.

## 2026-06-30 — Ch1 audio overhaul (research + design)

- **Pipeline loudness is already correct; do not blanket-cut music.** Measured via
  `ffmpeg ebur128`: voice normalizes to ~−18 LUFS, music beds to ~−22, SFX to ~−20
  (`normalize-stems.py:24-26`). After `gain × MUSIC_GAIN_SCALE` (0.72), beds rest ~9–12 LU
  under voice — a solid, slightly conservative delta. The chapter master lands −18 LUFS /
  −1.5 dBTP (`stitch-chapter.py:46`), inside the spoken-word band (−19…−16). The recurring
  mix complaint is almost never "too loud"; it is "static / not tied to scene."

- **The mixer ALREADY has the mechanism for content-aware ducking — extend it, don't invent.**
  `muffle_suffix()` (`mix-live-scene.py:70-83`) builds a per-frame `volume@fb=...:eval=frame`
  duck from window edges using `clip()` trapezoids + `_nested_max()`. Content-aware ducking is
  the same construction keyed to the voice-cue timeline (which the loop already tracks as
  `cstart`/`t`, lines 145-150). An analytic volume envelope beats `sidechaincompress` here:
  deterministic, composes by multiplication with the flashback duck + `MUSIC_GAIN_SCALE`, and
  allows anticipatory pre-roll (we know voice onset in advance). Must suppress the content duck
  inside flashback windows or you over-attenuate (×0.35 × ×0.5 ≈ ×0.18).

- **Mode (a) single-bed cue sheets silently discard duck keys.** The mode-a branch
  (`mix-live-scene.py:197-205`) reads only `asset`+`gain`. `scene-04-midnight/cues.json` still
  declares `duck_under_voice`/`duck_amount` (+ stale `output`/`asset_dirs`/`build-live-scene.py`
  refs) that do nothing. Mode (b) timed-bed lists (scenes 1-3) are the live standard; any scene
  still on mode (a) is a rebuild candidate.

- **"Odd pauses / weird timings" root cause: untrimmed SFX advance the timeline by full length.**
  `normalize-stems.py` silence-trims VOICE only (line 20); SFX get loudnorm only (line 25). The
  mixer does `t += d` on each non-`room-ambiance` SFX (lines 163-164). Ch1 offenders (via
  `silencedetect=n=-50dB:d=0.3`): `key-lock-door` ~2.1 s internal silence (3.5 s for a ~1.4 s
  event), `shop-door` ~1.0 s tail, `doorbell-ring` ~0.56 s tail; plus `kettle-boil` 5 s /
  `gas-ring` 4 s insert their whole length as VO rests. Fix = trim SFX in normalize, or stop the
  mixer advancing `t` by trailing silence. `room-ambiance` is the one SFX treated as overlay
  (line 163) — that's the pattern for any ambient/non-advancing cue.

- **Notice-motif: under `role:"notice"` machine-voice lines, pull the score to near-silence.**
  The horror of the automated provider/manufacturer notices is that they are *unscored* — flat
  and clinical. Make "notice arrives → score recedes" a chapter-wide audio motif (scenes 1, 3,
  and Lena's reading in 4).

- **Ducking is a CONTROL, not a fixed number — cite this.** Preferred dialogue-to-background
  loudness difference varies widely listener-to-listener (preferred-loudness-difference IQR
  ~5.7 LU; Torcoli et al., arXiv:2305.19100, abstract). VO practice: 3–6 dB subtle duck, pumps
  beyond ~6–8 dB (Sonarworks, Unison); film score sits ~6–12 dB under dialogue. Default chosen:
  −9 dB under solo narration, −6 dB under dialogue, near-mute under notices; attack ~0.3 s
  pre-rolled, release ~0.55 s, hold ~0.6 s.

- **Crossfade craft:** the mode-(b) bed crossfades use two independent linear `afade` (`tri`)
  curves, which can dip ~3–6 dB in the middle for uncorrelated beds. ffmpeg `qsin` (quarter-sine)
  ≈ equal-power and avoids the dip (FFmpeg afade docs) — worth exposing as a bed-fade option.

- **Frontmatter contract for docs/ files:** `scripts/validate-metadata.py` requires exactly 8
  top-level fields: title, document_type, status, authority, summary, tags, related,
  source_documents. (A research doc using `source:` instead of `source_documents:` will fail.)
  Run `python3 scripts/validate-metadata.py` to confirm PASS.
