---
title: "Chapter 1 Live-Audio Sound-Design Overhaul: Research + Design"
document_type: "research"
status: "reference"
authority: "research-grounding"
summary: "RESEARCH + DESIGN brief (no implementation) for the sound-design overhaul of the dramatized Chapter 1 (chapter-01-no-signal) live audiobook. Part A is a backward-compatible MIXER UPGRADE SPEC for content-aware ducking in scripts/mix-live-scene.py + cue-sheet schema, built as an analytic per-voice-span volume envelope (the proven flashback-duck mechanism extended), with cited target dB / attack / release and how it composes with mode-(b) timed beds, the flashback duck, and MUSIC_GAIN_SCALE. Part B is a per-scene sound-design plan for all four scenes: critique of the current beds plus the prescribed redesign (music moods, bed timing, SFX placement, ducking intent). Diagnoses the author's complaints (random-feeling music, odd pauses, weird timings) to two grounded root causes: scene-04 still runs one static looped tension-bed with phantom duck keys the mixer discards, and SFX are loudness-normalized but never silence-trimmed while the mixer advances the timeline by their full length."
tags:
  - research
  - audio
  - sound-design
  - live-audiobook
  - book-1
  - chapter-01
  - ducking
  - mixer
  - cue-sheet
source_documents:
  - "scripts/mix-live-scene.py"
  - "scripts/normalize-stems.py"
  - "scripts/stitch-chapter.py"
  - "docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md"
  - "audio/live-audio-book/book-1/chapter-01-no-signal/scene-04-midnight/cues.json"
related:
  - "./audio-roles-audit.md"
  - "../../.claude/agents/sound-engineer.md"
  - "../../.claude/agents/live-narration-director.md"
  - "../../.claude/agents/systems-engineer.md"
---

# Chapter 1 Live-Audio Sound-Design Overhaul: Research + Design

> Scope: RESEARCH + DESIGN only. This brief does NOT edit `mix-live-scene.py` and does NOT
> author the final cue sheets. Part A is the implementation spec for **systems-engineer**;
> Part B is the rebuild brief the **live-narration-director** follows when the cue sheets are
> re-authored. The voice **performance** stays the director's; everything under and around it
> (music, SFX, levels, fades, master) is designed here.

## 0. Diagnosis — what is actually wrong with the current Ch1 audio

Measured and read against the four scripts, the cue sheets, the prose, and the assets. Two
root causes carry most of the author's complaint; a third is a craft ceiling.

**Root cause 1 — Scene 4 is the worst-mixed scene in the chapter, and it is the climax.**
`scene-04-midnight/cues.json` still uses the legacy **mode (a)** single bed: one
`tension-bed` (asset is 316 s) at `gain 0.75`, laid unbroken across the entire 313.7 s
climactic Lena call. Worse, the cue sheet declares `"duck_under_voice": true` and
`"duck_amount": 0.45` — but the **current mixer reads neither key** (the mode-a branch,
`mix-live-scene.py:197-205`, consumes only `asset` and `gain`). So the author explicitly
asked for ducking on the climax, the cue sheet says ducking is on, and the mixer silently
throws it away. The scene also carries stale top-level keys (`output`, `asset_dirs`,
"Consumed by scripts/build-live-scene.py") that prove it was never rebuilt to the mode-(b)
standard scenes 1-3 received. Result: a five-minute, multi-turn emotional escalation
("Stay down here with me" / the unforgeable-correctness wall / the link dropping / "This was
the one he could not fix") is scored with one undifferentiated drone at one static level.
This is the single biggest reason the music "feels random and not tied to scene feel."

**Root cause 2 — SFX inject dead air; this is the "odd pauses / weird timings."**
`normalize-stems.py` silence-trims **voice** stems (the `silenceremove` chain, line 20) but
applies only `loudnorm` to **SFX** (line 25). The mixer then advances the timeline by each
SFX's *full* probed duration (`t += d`, `mix-live-scene.py:163-164`). Several Ch1 SFX carry
seconds of head/tail silence that thereby become dead gaps in the narration flow (measured
with `silencedetect=n=-50dB:d=0.3`):

| SFX asset | Dur | Silence detected | Dead air injected |
|---|---|---|---|
| `key-lock-door` (scene 2 close) | 3.5 s | ~0.07–1.12 s lead + 2.43–3.48 s tail | **~2.1 s** of silence around a ~1.4 s event |
| `shop-door` (scene 3, old man exits) | 3.0 s | 2.01–3.0 s tail | **~1.0 s** dead tail before next line |
| `doorbell-ring` (scene 3) | 2.6 s | 2.0–2.56 s tail | ~0.56 s tail |
| `kettle-boil` (scene 1) | 5.0 s | none > 0.3 s | full **5.0 s** rest inserted mid-VO |
| `gas-ring` (scene 1) | 4.0 s | none > 0.3 s | full **4.0 s** rest inserted mid-VO |

These land on top of each cue's `gap_before` (0.3–1.0 s), compounding. A listener hears the
narrator stop, a door/key effect with a second of silence hanging off it, then the narrator
resume — exactly "odd pauses; strange timings."

**Root cause 3 (the ceiling) — every bed level is static.** Even in the well-sectioned
scenes 1-3, music never moves relative to the voice. Measured levels: voice normalizes to
**−18 LUFS** (stems probed at −17.8 to −18.2), music beds to **−22 LUFS** (probed −22.1 to
−22.4), SFX to **−20 LUFS** (probed −20.4). After `gain × MUSIC_GAIN_SCALE` (e.g.
`withdrawal` at 0.72 → 0.72×0.72 = 0.518 linear ≈ −5.7 dB), the bed rests roughly **9–12 LU
under the narration** — a solid, even slightly conservative resting delta. The defect is not
the level; it is that the level is **frozen**. The bed sits at the same delta whether the
narrator is mid-clause or there is a two-second silence, so it never "breathes" in the gaps
and never steps back under a bare, load-bearing line. That flatness reads as music that is
"just there," disconnected from the words. The fix is content-aware ducking (Part A).

"Weird artifacts": the degraded-`link` processing on Lena (tremolo + `acrusher` bits=8) and
the heavily band-limited `notice` voice are *intentional* character and can read as artifacts
to an untrained ear; they are defensible and should stay. A genuine candidate is limiter
pumping when a hot SFX coincides with bed + voice and the summed bus hits
`alimiter=limit=0.95` (`mix-live-scene.py:221`); I could not verify pumping cheaply, so it is
marked UNVERIFIED below and routed to the director to listen for after the SFX-trim fix
removes the loudest coincidences.

---

## Part A — MIXER UPGRADE SPEC: content-aware ducking

### A.1 Approach: analytic per-voice-span volume envelope (NOT sidechaincompress)

Implement ducking as a **deterministic volume automation envelope** keyed to the voice-cue
timeline the mixer already computes — *not* as `sidechaincompress` keyed to a summed voice
bus. Reasons, in priority order:

1. **The mechanism is already proven in this exact file.** `muffle_suffix()`
   (`mix-live-scene.py:70-83`) already builds a per-frame `volume@fb=...:eval=frame` duck
   from window edges, using `clip()` trapezoids folded with `_nested_max()`. The new duck is
   the same construction keyed to voice spans instead of flashback spans. We extend a working
   pattern; we do not introduce a new class of risk.
2. **It composes by multiplication, for free.** Chaining a second `volume@duck=...:eval=frame`
   after the existing `volume@fb` on the music chain multiplies the two envelopes sample-for-
   sample. Flashback duck × content duck × `bed_gain × MUSIC_GAIN_SCALE` all stack natively.
3. **It is deterministic and reviewable** — no transient detection, no pumping artifacts, no
   dependence on routing every delayed voice input into a sidechain key (which would force an
   intrusive amix-the-voice-bus-first rework and threaten back-compat).
4. **Anticipatory ducking.** Because the mixer knows each voice onset *in advance*, the bed
   can begin dipping a beat *before* the word lands (pre-roll the attack ramp), which sounds
   more intentional than a reactive compressor that ducks only after detecting the transient.

`sidechaincompress` is the right tool in a live console where you do not know the future;
here we know the entire timeline, so an analytic envelope is strictly better.

### A.2 Cue-sheet schema (opt-in, fully back-compatible)

Add one **optional scene-level** object, `ducking`. **Absent ⇒ behaves exactly as today**
(no envelope appended; byte-identical output). Proposed shape and defaults:

```json
"ducking": {
  "enabled": true,
  "depth_db": -6,            // default duck under any voice (dialogue/character)
  "narration_depth_db": -9,  // deeper duck under solo narrator (role == "narration"/"notice")
  "attack": 0.30,            // ramp-down seconds, pre-rolled before voice onset
  "release": 0.55,           // ramp-up seconds after voice end
  "hold": 0.60,              // merge voice spans closer than this into one ducked region
  "bus": "voice",            // "voice" (default) or "voice+sfx"
  "floor_under_notice_db": -15  // optional: near-mute the score under role:"notice" lines
}
```

Plus an **optional per-bed** and **per-cue** override:
- per-bed `"duck": false` on any timed bed exempts that bed (e.g. a deliberate stinger that
  should punch through the voice). Default true when `ducking.enabled`.
- per-voice-cue `"duck_depth_db": <n>` overrides the region depth for spans containing that
  cue (e.g. force a near-mute under a single bare line).

Scene 4's legacy `duck_under_voice` / `duck_amount` keys: the cleanest path is to **rebuild
scene 4 to mode (b) + the new `ducking` block** and delete the dead keys (Part B.4).
Optionally, systems-engineer may alias `duck_under_voice:true` → `ducking.enabled:true` and
`duck_amount:x` → `depth_db = 20*log10(1-x)` for the mode-a path as a one-line courtesy so the
existing file is not silently a no-op; either way the rebuild supersedes it.

### A.3 Concrete levels (cited) and how they map to this pipeline

The bed already **rests** ~9–12 LU under voice (§0). The duck adds movement *on top of* that
rest level:

- **Default duck depth: −6 dB under dialogue, −9 dB under solo narration.** Voiceover ducking
  practice puts a *subtle* duck at 3–6 dB and warns that beyond ~6–8 dB the gain reduction
  starts to "pump" audibly (Sonarworks; Unison). Film practice puts score roughly 6–12 dB
  under dialogue (Quora/WeVideo synthesis). Net effect here: under dense narration the bed
  drops from ~10 LU-under to ~**16–18 LU-under** (the words go bare and clinical); under
  character dialogue it drops less, ~**13–14 LU-under**, so the score still supports the
  performance and **lifts back toward the rest level in the breaths between lines** — the
  "breathe in the gaps" behavior the static mix lacks. This *is* the charter's "ducks under
  narration, lifts under dialogue," expressed as a depth that is keyed to **what** is
  speaking (`role`), not merely **that** something speaks.
- **Attack ~0.30 s (pre-rolled), release ~0.55 s.** VO-ducking guidance: attack 2–5 ms for
  reactive sidechain, release 50–200 ms (Sonarworks; Unison). We deliberately run **slower
  and pre-rolled** because (a) we know the onset, so a 0.3 s anticipatory glide reads as
  intentional scoring rather than a gate snapping; (b) a longer release prevents the bed from
  jumping up inside short inter-line gaps. The `hold` (0.6 s) further merges spans so the bed
  only re-opens in genuine breaths, not between words.
- **`floor_under_notice_db: -15` (motif).** Under the automated `role:"notice"` lines (the
  machine-composed provider notices in scenes 1 and 3, and Lena reading the manufacturer
  wording in scene 4) the score should recede to near-silence. The horror of those lines is
  that they are *unscored* — flat, clinical, no music telling you how to feel. Make "the
  notice arrives, the score gets out of the way" a chapter-wide audio motif.
- **Why a control, never a blanket rule.** Preferred dialogue-to-background loudness
  difference varies substantially listener-to-listener (preferred-loudness-difference IQR
  ~5.7 LU; Torcoli et al., arXiv 2305.19100). There is no single correct duck depth, so the
  depth is exposed per scene and tuned by ear — the design offers ducking as *available,
  justified control*, not a global default forced over every scene.

### A.4 Implementation sketch for systems-engineer

Mirror `muffle_suffix`. Concretely:

1. During the existing cue loop, collect voice spans as `(cstart, t, depth_linear)` where
   `depth_linear = 10**(depth_db/20)` chosen by role (`narration`/`notice` → `narration_depth`
   or `floor_under_notice`; else `depth_db`), honoring any per-cue `duck_depth_db`. The loop
   already tracks `cstart` and post-cue `t` (lines 145-150) — just append to a list.
2. **Skip spans that fall inside the flashback windows `fbw`** (known at line 170 before the
   music chains are built). The flashback machinery already owns the music level there; double-
   ducking would over-attenuate (×0.35 × ×0.5 ≈ ×0.18). Inside `fbw`, the content duck = 1.0.
3. **Merge** spans whose inter-span gap `< hold` into single regions; region depth = the
   *deepest* (smallest linear) depth among merged spans (so a dense narration run ducks deep;
   a dialogue exchange with breaths ducks shallow and lifts between lines).
4. Build `duck_suffix(regions) -> ",volume@duck=volume='<expr>':eval=frame"` where, with
   pre-roll, each region `[s,e]` at linear depth `g` contributes
   `(1-g)*clip((t-(s-attack))/attack,0,1)*clip(((e+release)-t)/release,0,1)` and
   `duck = 1 - max(all contributions)` via the existing `_nested_max()`. Append this suffix to
   **every music-bed chain** (both mode-a line 201 and mode-b line 191-193), after the existing
   `MUFFLE`. If `bus == "voice+sfx"`, also append to SFX chains; default music-only.
5. Empty regions / no `ducking` key ⇒ empty suffix ⇒ no-op (back-compat, exactly like
   `muffle_suffix("")`).

Caveat: many regions → a long `eval=frame` expression. For Ch1 (a few dozen voice cues/scene,
collapsing to ~10-20 merged regions) this is well within ffmpeg expr limits and matches the
flashback precedent. If a future scene ever explodes the expression, fall back to
`asendcmd`-driven `volume` keyframes (the same time-toggle pattern `muffle_suffix` uses for
`lowpass@fb`). Flag, not a blocker.

### A.5 Composition summary

| Layer | Source | Multiplies into music gain |
|---|---|---|
| Base normalization | `normalize-stems.py` → bed −22 LUFS | (fixed) |
| Authored bed level | per-bed `gain` | × gain |
| Global music trim | `MUSIC_GAIN_SCALE = 0.72` | × 0.72 |
| **NEW content duck** | `ducking` envelope (A.4) | × duck_env(t) ∈ [g, 1] |
| Flashback duck | `muffle_suffix` `volume@fb` | × fb_env(t) (and content duck suppressed inside `fbw`) |
| Final master | `amix normalize=0` → `alimiter=limit=0.95`; chapter `loudnorm I=-18` | (bus) |

All four scene mixes still land at chapter target **−18 LUFS / −1.5 dBTP** via
`stitch-chapter.py:46`, which sits correctly inside the spoken-word band (−19 to −16 LUFS
integrated; Auphonic, podnews, NarrationBox). No master-chain change needed; the overhaul is
purely the duck envelope plus the SFX-trim fix (§0 root cause 2 — route to systems-engineer:
add a gentle `silenceremove` to the SFX branch of `normalize-stems.py`, or have the mixer not
advance `t` by detected trailing silence).

---

## Part B — Per-scene Ch1 sound-design plan

Common conventions for the rebuild: keep the **mode-(b) timed-bed** structure (scenes 1-3
already have clean, non-looping, well-abutted beds — verified: every bed's `dur` ≤ its asset
length, and adjacent beds overlap 5-6 s so nothing loops). Adjacent-bed crossfades currently
use two independent linear `afade` curves (ffmpeg `tri`), which for *uncorrelated* beds can
dip ~3-6 dB in the crossfade middle; recommend the systems-engineer expose a `qsin`
(quarter-sine ≈ equal-power) curve option on the bed fades for cleaner mood-to-mood
transitions (FFmpeg afade docs). Enable `ducking` on every scene with the depths in A.3.

### B.1 Scene 1 — "No Signal" (waking, the notice, route-around) — 237.7 s

**Current beds:** `still-morning` (0-75) → `mesh-stir` (70-106) → `the-notice` (100-200) →
`route-around` (194-242). **Critique:** this is the *best* of the four — the sectioning
honestly tracks the beat map (still waking → communal stir → the notice → coping resolve),
timings are clean, nothing loops. It is not random. Its only failures are the static-level
ceiling and one missed motif.

**Redesign (light):**
- Keep all four beds and their timing.
- **Notice motif:** under the two `role:"notice"` cues (the "Notice of Service Continuity
  Adjustment" title and body, lines 167-184) pull `the-notice` bed to the
  `floor_under_notice_db` near-mute, so the flat machine voice lands cold and unscored, then
  let the bed return for "He read it twice." This is the chapter's first statement of the
  notice-motif that recurs in scenes 3 and 4.
- **Breathe at the realization:** the "you could not solder a decision… meant, now, to leave
  him here" paragraph is the emotional gut. With ducking on, the bed lifts in the beat of
  silence after it (the natural `gap_before`), which it currently cannot do.
- **SFX:** `gas-ring` (4 s) and `kettle-boil` (5 s) currently insert their *full* length as
  rests in the VO. Re-cut both to ~1.5-2 s of characteristic sound (the ignite *whump* / the
  rising boil), OR mark them as non-advancing overlays under the resuming narration. The
  `mesh-chime` before the notice is a good, motivated cue — keep it; it earns the
  notice-arrival beat. Net: the scene loses ~6-7 s of dead air.

### B.2 Scene 2 — "The Almost-Normal Street" — 208.9 s

**Current beds:** `still-morning` (0-72, reused from chapter scope for Friday-morning
continuity) → `cold-street-tally` (67-105) → `grocery-intimate` (100-178) → `permission-close`
(173-219). **Critique:** genuinely well-mapped to the prose's emotional sections (deceptive
ordinariness + kids → the dead-streetlight withdrawal boundary → the warm grocery / dark
dairy case / Marisol → the "nobody left to give it" close). The `still-morning` reuse is a
deliberate, correct continuity choice (same continuous Friday morning). Timings clean. No
redesign of the bed map needed.

**Redesign (light):**
- Enable `ducking` (dialogue depth −6 dB): Marisol's lines and Eli's "I'll take it" get the
  shallower dialogue duck so `grocery-intimate` supports the exchange and lifts in the beats
  between her lines, instead of sitting flat under everything.
- **Eli's interior echo** ("Controller wants to call home and nobody's home", `thought`
  filter, line 186) is the scene's quiet hinge — pull the bed a touch deeper under it
  (per-cue `duck_depth_db: -10`) so the filtered thought sits in its own small pocket.
- **SFX — the headline fix here:** `key-lock-door` (3.5 s, ~2.1 s of internal silence) is the
  worst dead-air offender in the chapter and it lands on the scene's final beat ("put the key
  in the lock… He went in"). Re-cut to a tight ~1.2 s key-turn + latch, or trim the silence in
  `normalize-stems`. `kids-passing` (4 s, 0.3 s lead) is fine as a distant wash — keep it as a
  low overlay so it does not advance the timeline against the narrator's sentence.

### B.3 Scene 3 — "The Same Failure at Every Door" — 521.3 s

**Current beds:** `morning-bench` (0-166) → `the-rhyme` (160-334) → `withdrawal` (328-486) →
`personal-note` (480-562). **Critique:** the most ambitious and mostly right — four long,
scene-scope beds generated specifically so nothing loops (the cue-sheet `_doc` notes the prior
version audibly looped the 75 s `still-morning`, since fixed). The arc — steady repair →
dawning recognition + the buried-past probe → the cold institutional gut-punch (the power
notice) → the turn to Lena — is real scoring. The flashback handling (the `mentor` cue "There
it is. That's it, Eli." under `filter:"flashback"` + the `flashback:true` narration cue) is
already correct and will be *protected* from the new duck (A.4 step 2).

**Redesign (light):**
- Enable `ducking` (narration depth −9 dB, since the narrator carries almost the whole scene).
- **Notice motif again:** under the `role:"notice"` power-tier cues (lines 370-389) pull
  `withdrawal` to the near-mute floor — the second statement of the cold-machine-voice motif,
  now landing harder because it is the neighborhood-wide downgrade. Let the bed swell back on
  "And there it was. What the morning had been circling."
- **The recognition collage** ("They were one shape… a slow opening of a hand… finger by
  finger") is the chapter's thesis landing — `withdrawal` should be at its fullest authored
  level here (it already peaks at gain 0.72) with the duck lifting in the micro-pauses between
  the colliding images.
- **SFX:** `doorbell-ring` (trim 0.56 s tail) lands the "Someone is here. Let me know." beat —
  keep, it is the bare freed-bell and it is earned. `broadcast-pulse` (double-pulse) vs the
  single `mesh-chime` at the end is a deliberate, correct personal/everyone contrast — keep
  both. `shop-door` (trim ~1 s tail) on the old man's exit — trim the dead tail so "Eli was
  still standing there" does not float in silence. `phone-dock` at the recognition pivot — fine.

### B.4 Scene 4 — "Midnight" (the Lena call) — 313.7 s — **THE PRIORITY REBUILD**

**Current bed:** ONE `tension-bed` (mode a), gain 0.75, unbroken across the whole scene, with
`duck_under_voice`/`duck_amount` keys the mixer discards (§0 root cause 1). **Critique:** this
is the chapter's emotional summit and it is scored like a holding pattern. One drone cannot
serve a scene that moves through at least four distinct emotional rooms. This is the single
biggest fix in the overhaul.

**Redesign (full rebuild to mode (b) + `ducking`):** re-score as four crossfading scene-scope
beds tracking the call's structure (timings approximate; the director tunes to the rendered
voice lengths, as in scenes 1-3):

| Bed (new asset) | Window | Beat it scores | Intent |
|---|---|---|---|
| `midnight-dread` | 0 – ~70 s | the short message, monitor-drag, dock, call-connect, "Can you hear me" | thin, low, held — quiet dread; sparse so the degraded-link voice cuts through |
| `the-wording` | ~65 – ~150 s | Lena reads the manufacturer notice; the three machines; "Who's on it" / the silence that is not the link | **notice motif** — near-mute under the `link`-filtered reading, then a single low swell into the gut-silence after "Who's on it." |
| `the-wall` | ~145 – ~250 s | "Stay down here with me"; "It's the same thing, Lena"; Eli's `thought` realization (the unforgeable correctness) | the emotional peak — let it rise under the argument, then hold under the `thought` cue (deep per-cue duck so the filtered interior is bare), the score carrying the dread the words keep flat |
| `single-low-note` | ~245 – ~315 s | link drops; "The shop was very quiet after"; room-ambiance; "This was the one he could not fix." | collapse to one sustained low tone — the prose hands us this literally ("a transformer he could not see held its single low note"); near-silence into the final line |

- **Ducking:** enable, narration depth −9 / dialogue depth −6, plus the notice-floor under
  Lena's `link`-filtered notice reading. The `thought` cue (Eli's unforgeable-correctness
  interior, line 264) gets a deep per-cue duck so it sits alone.
- **SFX:** `monitor-drag` (2 s, clean), `phone-dock`, `call-connect`, `link-drop` are all
  motivated and well-placed — keep. `room-ambiance` is correctly an overlay (the one SFX the
  mixer does not advance the timeline on, line 163) — keep. Verify `link-drop` into the 1.0 s
  `gap_before` before "The shop was very quiet after" is a *deliberate* silence (it is — the
  collapse of the call window), not the accidental dead air the trimming fix targets.
- **Drop the stale keys:** delete `output`, `asset_dirs`, `duck_under_voice`, `duck_amount`,
  and the `build-live-scene.py` doc reference on rebuild.

---

## Citations

Tagged `confirmed` (measured locally or stated in a primary/standards source), `inferred`
(synthesized from multiple practitioner sources), or `best-effort` (single secondary source).
Anything not cheaply verifiable is marked UNVERIFIED.

- **[confirmed, measured] Pipeline loudness:** voice −18 LUFS (stems probed −17.8/−18.2),
  music −22 LUFS (probed −22.1/−22.4), SFX −20 LUFS (probed −20.4), via `ffmpeg ebur128`;
  targets set in `normalize-stems.py:24-26`. Chapter master −18 LUFS / −1.5 dBTP via
  `stitch-chapter.py:46`.
- **[confirmed, measured] SFX dead air:** `silencedetect=n=-50dB:d=0.3` on the Ch1 SFX;
  `key-lock-door` ~2.1 s internal silence, `shop-door` ~1.0 s tail, `doorbell-ring` ~0.56 s
  tail. SFX get no silence-trim (`normalize-stems.py:25`) and the mixer advances `t` by full
  SFX duration (`mix-live-scene.py:163-164`).
- **[confirmed, code] Scene-4 ducking keys are dead:** mode-a branch reads only `asset`+`gain`
  (`mix-live-scene.py:197-205`); `duck_under_voice`/`duck_amount` are never referenced.
- **[confirmed] Spoken-word loudness band −19 to −16 LUFS integrated; podcast −16 LUFS
  (Apple ±1), Spotify −14, broadcast EBU R128 −23; true-peak ceiling −1 dBTP (−2 on upload).**
  Sources: Auphonic singletrack docs; podnews LUFS/LKFS FAQ; NarrationBox ACX guide (ACX RMS
  −23…−18, peak < −3 dB, noise floor < −60 dB). Our −18 LUFS chapter master sits in-band.
- **[confirmed/inferred] VO ducking depth 3–6 dB subtle, pumping beyond ~6–8 dB; attack
  2–5 ms reactive; release 50–200 ms; ratio 2:1–4:1.** Sources: Sonarworks sidechain blog;
  Unison side-chain guide; MixingMonster. (We intentionally run slower/pre-rolled — A.3.)
- **[inferred] Score sits ~6–12 dB under dialogue in film.** Synthesis: Quora dialogue/music/
  FX levels thread; WeVideo film-levels guide.
- **[confirmed] Preferred dialogue-to-background loudness difference varies substantially;
  preferred-loudness-difference IQR ~5.7 LU.** Torcoli, Fischer et al., "Predicting Preferred
  Dialogue-to-Background Loudness Difference in Dialogue-Separated Audio," arXiv:2305.19100
  (abstract). Grounds "offer ducking as control, not one fixed number." (The absolute "+10 to
  +15 LU preferred" figure often quoted is **best-effort**; the abstract gives spread, not a
  median absolute value.)
- **[confirmed] FFmpeg `afade`/`acrossfade` curves: `tri` linear, `qsin` quarter-sine ≈ equal-
  power.** FFmpeg filters documentation. Grounds the equal-power crossfade recommendation.
- **[UNVERIFIED] Limiter pumping** when a hot SFX coincides with bed+voice at
  `alimiter=limit=0.95` — plausible from the filtergraph but not measured; routed to the
  director to confirm by ear after the SFX-trim fix.

Sources (URLs):
- https://www.sonarworks.com/blog/learn/sidechain-techniques-for-blending-ai-vocals-with-live-instruments
- https://unison.audio/side-chain-compression/
- https://mixingmonster.com/sidechaining-in-music-production/
- https://auphonic.com/help/algorithms/singletrack.html
- https://podnews.net/article/lufs-lkfs-for-podcasters
- https://narrationbox.com/blog/audiobook-mastering-rms-lufs-noise-floor-acx-guide
- https://www.quora.com/What-dB-level-should-I-mix-dialogue-music-and-effects-to-for-a-film
- https://www.wevideo.com/blog/how-to-set-audio-levels
- https://arxiv.org/abs/2305.19100
- https://ffmpeg.org/ffmpeg-filters.html

---

## The seam / routing

- **Owned here (sound-engineer):** the ducking design + cue-sheet schema (Part A), the per-
  scene music/SFX/level plan (Part B), all cited levels.
- **Routed to systems-engineer (implementation):** the `ducking` envelope in
  `mix-live-scene.py` (A.4), the optional `qsin` bed-fade curve, and the SFX silence-trim in
  `normalize-stems.py` (or non-advancing-on-trailing-silence in the mixer). Back-compat is a
  hard requirement: no `ducking` key ⇒ identical output.
- **Routed to live-narration-director (performance + execution):** re-authoring the four cue
  sheets to this brief, re-cutting/trimming the dead-air SFX assets, generating the four new
  scene-4 beds, and the by-ear review. The voice **performance** and any re-tuning stay the
  director's call; this brief touches only what is under and around the voice.
- **Reveal-safety held:** no new score swell, stinger, or SFX telegraphs any withheld fact;
  the scene-3 deflected-past memory stays the existing restrained flashback treatment; nothing
  in this design implies Asterion/Mosaic/Morrow/Crown ahead of the prose.

## Decisions Made (author may override)

| Question | Decision | Grounding | Confidence |
|---|---|---|---|
| Sidechaincompress vs analytic envelope for ducking? | **Analytic per-voice-span volume envelope.** | Extends the proven `muffle_suffix` mechanism (`mix-live-scene.py:70-83`); composes by multiplication with flashback duck + `MUSIC_GAIN_SCALE`; deterministic; allows anticipatory pre-roll. Sidechain would force an intrusive voice-bus rework and risk back-compat. | high |
| One global duck depth, or content-aware? | **Content-aware: −9 dB under solo narration, −6 dB under dialogue, near-mute under `notice`.** Exposed per-scene, tuned by ear. | VO 3–6 dB subtle / pump > 6–8 dB (Sonarworks, Unison); film score 6–12 dB under dialogue; preference spread IQR 5.7 LU ⇒ must be control not rule (arXiv:2305.19100). | high |
| Is the music actually too loud (author: "random")? | **No — the rest level (~10 LU under voice) is fine; the defect is that it is static + scene-4 is one drone.** Fix with movement (duck) + scene-4 sectioning, not a global level cut. | Measured voice/music/SFX LUFS; `mix-live-scene.py:197-205` scene-4 mode-a single bed. | high |
| Source of "odd pauses / weird timings"? | **Untrimmed SFX head/tail silence advancing the timeline by full duration.** Trim SFX in normalize, or stop advancing `t` by trailing silence. | `silencedetect` measurements; `normalize-stems.py:25`; `mix-live-scene.py:163-164`. | high |
| Keep scenes 1-3 bed maps? | **Yes — they track the prose beats and do not loop; add ducking + the notice-mute motif + SFX trims only.** Full rebuild reserved for scene 4. | Verified every bed `dur` ≤ asset length and 5-6 s abutting crossfades; cue-sheet `_doc` rationales align with the prose sections. | high |
| Master-chain change needed? | **No.** −18 LUFS chapter master is already in the spoken-word band; the overhaul is the duck envelope + SFX trim only. | `stitch-chapter.py:46`; Auphonic/podnews/NarrationBox bands. | high |
