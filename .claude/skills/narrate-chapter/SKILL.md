---
name: narrate-chapter
description: Produce the PLAIN single-narrator audiobook for an APPROVED chapter of "The Unnecessary". The audiobook-director writes (or refreshes) the v3-tagged narration performance script from the frozen prose, a Gemini narration-critique gate enforces prose-fidelity + v3 tag discipline (ellipses-for-pauses, only tags the renderer honors) and re-rolls the script on FAIL, then the existing local voice-server script renders and self-normalizes one chapter mp3. HARD RULE -- no audio renders until the critique PASSES. This is the single-narrator counterpart to /live-audiobook (the dramatized full-cast path). args {book, chapter, slug, title?, voice?}.
---

# Narrate Chapter (single-narrator audiobook)

The first-class entry point for the project's **plain single-narrator** audiobook -- the
straight read of a chapter in one steady narrator voice, the counterpart to the dramatized
full-cast `/live-audiobook` path. It wraps the existing local-voice-server narration scripts
in the same skill + workflow shape `/live-audiobook` uses, with the project's non-negotiable
narration-critique gate baked in **before** any audio is rendered.

The narration itself is the audiobook-director's `[beat]`/`[hold]`/register-tag **performance
script** read by the self-hosted voice server's AUDIOBOOK preset (steady, weary, controlled --
a Herzog register that trusts silence). The prose words are frozen canon; only bracketed
direction, pause markers, and `---` scene breaks are added.

## The hard gate

This project never renders or ships narration audio without a **PASSED Gemini
narration-critique** (Decision: v3 tag discipline -- ellipses only for a genuine held beat,
pauses carried by `[beat]`/`[hold]`, only tags the voice server actually honors). The skill
enforces that as a real barrier: the critique runs, a gate agent rules PASS/FAIL on the
**blocking classes** -- prose-fidelity drift versus the manuscript, and v3 tag-discipline
violations (ellipsis misuse / runaway-pause risk, an unhonored tag) -- and on FAIL the
audiobook-director revises the script and it is re-critiqued. If it never passes within the
roll cap, the run **aborts unrendered**. Density and register taste are advisory and never
block.

## How to run

Invoke the workflow `.claude/workflows/narrate-chapter.js`, passing the target chapter
through `args`:

- `book` -- the book folder (default `book-1`).
- `chapter` -- the chapter NUMBER (e.g. `2`); zero-padded internally to `chapter-02-...`.
- `slug` -- the chapter slug WITHOUT the `chapter-NN-` prefix (e.g. `the-last-supported-day`).
- `title` -- optional; the spoken chapter title (default `Chapter <n>`).
- `voice` -- optional; the voice-server voice name (default `Will_Wheaton`).
- `voiceUser` / `voicePassword` -- optional; voice-server credentials. When omitted the render
  script resolves them itself from `VOICE_API_USER`/`VOICE_API_PASSWORD` or `.mcp.json`.
- `api` -- optional; override the voice-server base URL.
- `maxGate` -- optional; critique<->revise rolls before aborting unrendered (default 3).

The chapter must be an **approved** manuscript at
`docs/50-manuscript/<book>/chapter-<NN>-<slug>/chapter-<NN>-<slug>.md`; if it is missing the run
stops (this skill narrates an approved chapter, it does not draft one). Audio lands at
`audio/<book>/chapter-<NN>-<slug>/chapter-<NN>-<slug>.narrator.mp3`.

Example args:

```json
{ "book": "book-1", "chapter": 1, "slug": "no-signal", "title": "No Signal" }
```

## Phases

1. **Narration Script** -- the **audiobook-director** writes (or refreshes + re-verifies) the
   chapter `*.narrative-script.md` from the approved prose: register tags, `[beat]`/`[hold]`
   pause markers, and `---` scene breaks only, with every prose word frozen and a token-for-token
   fidelity diff.
2. **Critique gate** -- `scripts/gemini-critique.py --mode narration --reference <manuscript>`
   judges fidelity + density + register + pacing + v3 tag craft; a gate agent rules **PASS/FAIL**
   on the blocking classes; on FAIL the audiobook-director revises and it is re-critiqued. The
   render is gated on a PASS.
3. **Render** -- a Bash agent runs `scripts/narrate-chapter-voiceserver.py` on the passed script:
   a **full fresh** local-model re-render (never `--resume`) to one chapter mp3. The render's
   stitch self-masters with `loudnorm`.
4. **Normalize** -- measures the output's integrated loudness + true peak to confirm the built-in
   `loudnorm` master (I=-18 LUFS, TP=-2.0 dBTP) landed. No re-encode: unlike the live path's
   per-line stems, the single-narrator render normalizes itself, so there is no separate normalize
   script to run here.
5. **Output** -- reports the final mp3 path + duration + measured loudness, the narration-script,
   and the critique companion.

## Scripts it drives (reused, not reimplemented)

- `scripts/narrate-chapter-voiceserver.py` -- the local Chatterbox voice-server render (maps v3
  tags to performance profiles, renders + stitches + self-normalizes). The render engine.
- `scripts/gemini-critique.py --mode narration` -- the narration-critique gate (text-vs-text, on
  the Gemini quota, zero Claude budget).

(`scripts/narrate-chapter.py` is the ElevenLabs counterpart and is **not** used here -- this skill
targets the local voice model per the project's "always full re-render, local voice" rule.)

## Cost note

The render runs on the local voice model -- power, not tokens -- and is always a full fresh
re-render so a revised script is never voiced against stale audio. The expensive part is the
critique<->revise rolls; the gate caps them (`maxGate`, default 3) so a stubborn script aborts
rather than looping. To re-narrate after an edit, just edit the narration script and re-run this
skill: the gate re-passes and the chapter full-re-renders.
