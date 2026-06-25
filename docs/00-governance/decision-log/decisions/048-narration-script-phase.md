---
title: "Decision 048: Narration Script Phase (Eleven v3 Performance Markup)"
document_type: "decision"
status: "active"
authority: "governance"
summary: "After a chapter is adjudicated, Opus produces a separate narration script that marks the final prose with Eleven v3 audio tags and pacing for expressive read-aloud. The prose words are never changed; the manuscript stays canon. Audio generation is a separate, author-triggered step."
tags: ["decision", "workflow", "narration", "audio", "eleven-v3"]
related:
  - "../../novel-development-guide.md"
  - "../index.md"
source_documents:
  - "docs/00-governance/decision-log/decisions/046-chapter-authorship-pipeline.md"
---

## Decision 048: Narration Script Phase (Eleven v3 Performance Markup)

**Status:** Locked for Current Workflow
**Category:** Workflow and tooling

### Decision

Every chapter gets a fifth authorship phase, after adjudication: a **narration script** at `docs/50-manuscript/book-1/<chapter>.narrative-script.md`. It reproduces the chapter's final prose WORD FOR WORD and adds only (a) ElevenLabs Eleven v3 **audio tags** in brackets (for example `[quietly]`, `[weary]`, `[flat]`, `[tense]`, `[slowly]`) and (b) ellipses for pacing. It changes no prose words.

The script is produced by a **3-part pass that mirrors the chapter pipeline**: Opus directs it like an audiobook director in detailed, line-by-line markup (pacing, pauses, emotion, and distinct registers for Eli, the flat administrative notices, and a clipped tense Lena); Gemini critiques the performance (as an audiobook director, judging fidelity, direction density, register distinction, pacing, tag craft, and tone fit); Opus then revises, applying the notes it agrees with and logging each in a `## Narration Adjudication Log`. The standard is rich, purposeful direction that clearly differs from a flat read, while still serving the book's grounded register. Sparse, under-directed markup is a defect.

The script has three parts: YAML front matter (`document_type: "narration-script"`), a `## Voice Direction` section of overall direction to the narrator (not spoken), and a `## Performance Script` section (the tagged prose, the only part read aloud).

`scripts/narrate-chapter.py` auto-detects a narration script and narrates it with `eleven_v3` (which interprets the audio tags); plain chapter prose still narrates with `eleven_multilingual_v2`. **Audio generation is a separate, author-triggered step:** the narration script is generated and reviewed first, and audio is only (re)generated on the author's go.

### Reason

Eleven v3 reads bracketed audio tags as stage directions for the voice, giving real dynamic range (restraint, weariness, held pauses) that flat text-to-speech cannot. Keeping the performance markup in a derived file protects the manuscript: the prose stays canon and untouched, exactly as the critique and adjudication artifacts are kept separate. Decoupling the script from audio lets the author read and adjust the direction before any costly audio run. Eleven v3 was verified reachable via the API on the project key and honored `[whispers]` and `[pause]` tags.

### Consequences

Adds the `<chapter>.narrative-script.md` artifact and a 3-part `Narration Script` phase (Opus directs, Gemini critiques, Opus revises) to the `write-chapter` workflow. `scripts/gemini-critique.py` gains a `--mode narration` with `--reference <manuscript>` that runs an audiobook-director rubric against the script. `scripts/narrate-chapter.py` gains script auto-detection, an `eleven_v3` default for scripts, a `--stability` flag (Natural/Creative ranges respond to tags better than Robust), and reads only the `## Performance Script` section so an appended adjudication log is never spoken. Markup must stay restrained to match the book's grounded register; over-tagging is a defect. Note: `eleven_v3` does not support request stitching, so prosody may vary slightly between chunks; chunks break at scene and paragraph boundaries to minimize it.

### Affected Documents

- `scripts/narrate-chapter.py`
- `.claude/workflows/write-chapter.js`
- `docs/50-manuscript/book-1/<chapter>.narrative-script.md`
- `docs/00-governance/decision-log/decisions/046-chapter-authorship-pipeline.md`

### Reconsider Only If

ElevenLabs adds request stitching to v3 (chunk-boundary prosody handling can then simplify), or the markup is moved inline into the manuscript (rejected here to keep prose canon clean).
