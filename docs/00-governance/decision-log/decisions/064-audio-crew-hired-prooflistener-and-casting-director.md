---
title: "Decision 064: The Audio Crew Gains a Prooflistener and a Casting Director, With Ensemble Casting Carved Out of the Live-Narration-Director"
document_type: "decision"
status: "active"
authority: "governance"
summary: "Hires the two HIGH-priority audio roles the audio-roles audit flagged as GAPS, and carves ensemble casting cleanly out of live-narration-director the same way sound-engineer was split off. (1) prooflistener: the crew's audio QC ears -- it runs AFTER render and verifies the produced WAVs against the script and the canon pronunciation lexicon, emitting a timestamped re-roll list. It is the ONE gate no text-vs-text check covers: the audiobook-director's tag-strip-and-diff proves the SCRIPT matches the manuscript and the Gemini gate critiques the cue SHEET against the prose, but neither listens to the rendered AUDIO, so the native TTS failure mode (a clean, confident, WRONG read -- a dropped/doubled/missing word or line, a wrong-but-plausible word, a homograph said wrong, a number misread, a name pronounced one way in chapter two and another in chapter nine) went uncaught. It diagnoses and routes; it never re-renders or edits. Built on scripts/verify-narration.py and structurally a SECOND set of ears that did not perform the take. (2) casting-director: owns the ensemble as a SET -- which character gets which voice, the deliberate contrast map so no two co-present speakers collide on the ear, and cross-chapter voice consistency -- authored into the cast sheet at docs/10-vision/audio/cast-sheet.md and signed off before live scenes render. It briefs voice-designer (which voices to design, to what contrast target) and routes the design/render work; it has no Bash by design. The CARVE-OUT: ensemble casting is lifted OUT of live-narration-director, which now CONSUMES the cast sheet (ensures each assigned voice is on the server, performs and directs the scene) and routes any unassigned speaker or undesigned voice back to the casting-director -- the same clean seam by which sound-engineer was earlier split from this agent. Grounded in docs/70-research/audio-roles-audit.md sections 1.1, 1.2, and 2.1 and prioritized recommendations 1 and 2. FOLLOW-UP, explicit: both are HIRED but NOT yet wired into the pipeline -- the consolidated wiring pass that slots every book and audio agent at its right cadence is the next deliberate step. Changes no canon or prose; reversible via git."
tags: ["decision", "workflow", "crew", "agents", "audio", "prooflistener", "casting-director", "live-narration-director", "audio-qc", "roles-audit", "governance", "reversible"]
related:
  - "../../../../.claude/agents/prooflistener.md"
  - "../../../../.claude/agents/casting-director.md"
  - "../../../../.claude/agents/live-narration-director.md"
  - "../../../../.claude/agents/voice-designer.md"
  - "../../../10-vision/audio/cast-sheet.md"
  - "../../../70-research/audio-roles-audit.md"
  - "./060-autonomous-resolution-crew-resolves-logs-and-proceeds-never-blocks-on-the-author.md"
  - "./062-self-improving-crew-via-per-agent-field-notes.md"
  - "./063-editorial-crew-hired-developmental-copy-sensitivity-cold-read.md"
  - "../index.md"
source_documents:
  - ".claude/agents/"
  - "docs/70-research/audio-roles-audit.md"
  - "docs/10-vision/audio/cast-sheet.md"
---

## Decision 064: The Audio Crew Gains a Prooflistener and a Casting Director, With Ensemble Casting Carved Out of the Live-Narration-Director

**Date:** 2026-06-30
**Status:** Active but Revisable
**Category:** Workflow

### Decision

The crew gains **two audio agents**, hired against the two HIGH-priority GAPS the audio-roles audit identified (`docs/70-research/audio-roles-audit.md`, sections 1.1 and 1.2 and prioritized recommendations 1 and 2), and one existing agent is **carved down** by the same audit (section 2.1). Both new agents follow the house pattern: each carries the shared crew directives via the crew handbook and a field-notes file (Decision 062), and routes its findings/briefs to the owning agent or to the adjudicator (Decision 060) rather than reaching past its lane.

The two roles, and the one thing each catches or owns:

- **prooflistener** (`.claude/agents/prooflistener.md`) is the crew's **audio quality-control ears**, and it owns the one error class **no text-vs-text gate can touch**. It runs AFTER render: given a chapter's narration audio (single-narrator edition) or a live scene's stems, it verifies the **produced WAVs** against the script that made them and the project's canon **pronunciation lexicon**, and emits a precise, **timestamped re-roll list**. The native TTS failure mode is a **clean, confident, WRONG read**, plausible until you listen against the text: a dropped, doubled, or missing word, clause, or whole line; a garbled or wrong-but-plausible word the model invented; a homograph said the wrong way; a number or year misread; and above all **pronunciation INCONSISTENCY across chapters** (*Asterion*, *Aurelia*, *Mosaic*, *Morrow*, *Kade* said one way in chapter two and another in chapter nine). Every existing check stops at text and is blind to all of it: the audiobook-director's tag-strip-and-diff proves the *script* matches the manuscript, and the Gemini fidelity gate critiques the live *cue sheet* against the prose; **neither listens to the produced audio.** The prooflistener is the gate that closes that loop. It is built on `scripts/verify-narration.py` (already wired into the render pipeline as the verifier), and it is structurally a **second set of ears that did NOT perform the take** -- it can never QC its own render, the same familiarity-blindness defense the cold-reader gives the text side. It diagnoses and routes a re-roll handle (chunk index for the single-narrator edition, cue index + role for a live scene); it never re-renders, re-tunes, or edits a word.
- **casting-director** (`.claude/agents/casting-director.md`) owns the **ensemble as a SET**, the function that until now had no owner. Where **voice-designer** designs ONE voice in isolation from ONE canon profile, blind to the rest of the cast, the casting-director stands back and owns the whole roster at once: **which character gets which voice**, a deliberate **contrast map** spread across the acoustic axes (gender, age band, accent/heritage cadence, persona/timbre) so no two characters who are ever **co-present in a scene** collide on the ear, and **cross-chapter voice consistency** so a character is the same instrument in chapter nine as in chapter one. It authors this into the **cast sheet** (`docs/10-vision/audio/cast-sheet.md`) and **signs off the ensemble before live scenes render**. It **briefs voice-designer** (which slugs to design, to what contrast target) and routes the actual design/render work; it runs no endpoint and has **no Bash by design**. It reads canon to cast and never changes it; the cast sheet derives FROM canon and is never a canon authority of its own.

### The carve-out: ensemble casting lifted out of live-narration-director (the same clean split as sound-engineer)

The audit's only real split on the audio side (section 2.1) is that **live-narration-director** was wearing four roles at once: adapter/dramatist, director, **ensemble casting**, and line producer. The adapter and director functions share one "make this scene play as heard drama" mind and one toolchain, so the audit explicitly says **keep them combined**; the producer function is just running mechanical scripts, harmless to keep. The genuinely different altitude is **CASTING**: deciding and auditing the cast as a SET (whole-ensemble distinctiveness, the contrast map, cross-chapter consistency) is a different job from directing THIS scene's performance, and it was precisely the unowned seam in section 1.2 (voice-designer designs each voice blind to the others; live-narration-director consumed whatever existed; nobody owned the set).

So ensemble casting is **lifted OUT of live-narration-director** into the new casting-director, and the live-narration-director charter is edited to match: its provisioning step now **consumes the cast sheet** (read the casting-director's assignment, ensure each assigned voice is on the server, then perform and direct it) and explicitly **does NOT decide** who gets which voice, the contrast map, or cross-chapter consistency. When the director hits a speaker with no cast-sheet assignment or an undesigned voice, it **routes that back to the casting-director** (who briefs voice-designer); it never assigns, invents, or re-casts a voice itself. This is the **same kind of clean carve-out** that already worked when sound-engineer was split off this agent: a coherent separable chair lifted out, with the residual agent consuming the new owner's deliverable rather than owning it.

### Why these two — grounded in the audio-roles audit

The audit's grounding is that the audio chain is **lean and, if anything, UNDER-staffed**: it has strong AUTHORING (adaptation, direction, voice design, mix design) but almost no **VERIFICATION** and no **cast-as-a-whole ownership**. The two hires close exactly those two gaps, and each is the audit's named top-value move:

- **Audio QC of the rendered output (prooflistener, HIGH).** The local-model narrator inverts the cost of error: a miscast or misreading human narrator forcing a full re-record is the industry's single most expensive, least-reversible failure, but for us a re-render is routine and near-free. That inversion is *why* a precise QC pickup list is so high-leverage: the fix is nearly free **once the defect is named**. And TTS substitutes its own failure class (the confident misread) for the dirty-capture class that does not exist for us, moving the risk from capture quality to output **verification** -- the one place the crew had no ears. The audiobook-director cannot be those ears (its diff is script-vs-manuscript, not audio QC), and by construction no agent can QC a take it performed.
- **Casting director, the ensemble as a SET (casting-director, HIGH).** Full-cast audio lives or dies on **voice distinctiveness across the whole ensemble**, and that was nobody's job. voice-designer's remit is deliberately one-voice and reveal-safe; piling the whole-set decision onto it would break that. The audit's recommendation was explicit: **lift ensemble casting out of live-narration-director rather than pile it onto voice-designer**, which is exactly what was done.

### Follow-up: hired, NOT yet wired (the consolidated wiring pass is next)

Both agents are **hired** (their charters and field-notes files exist, the cast sheet is seeded, and the live-narration-director charter is redirected) but are **NOT yet wired into the pipeline**. No workflow skill invokes the prooflistener after render, and no skill calls the casting-director's sign-off before a live scene renders, yet. Wiring is the explicit next step, and it is **deliberate per role and per cadence**: the prooflistener runs as a **terminal post-render pass** (after the audio exists, routing re-rolls to whoever owns the line); the casting-director runs **before live scenes render** (a one-time-then-on-change ensemble pass, signing off the cast sheet that live-narration-director then consumes). This is the same deferral discipline used for the editorial hires in Decision 063: the right move is a **single consolidated wiring pass** that slots every recently hired book and audio agent at its correct cadence at once, rather than bolting each new agent into the pipeline ad hoc. Until that pass lands, both audio agents are available to invoke by hand but are not part of any automated pipeline.

### Previous or Alternative Direction

Before this, the audio crew had **strong authoring and no verification**: every gate stopped at text (script-vs-manuscript, cue-sheet-vs-prose), so the rendered audio was never checked against its source and the native TTS misread class was uncaught. And the **cast had no owner**: voice-designer designed each voice blind to the others, live-narration-director consumed whatever existed and de-facto assigned voices, and no role decided or audited the ensemble as a whole. The rejected alternatives, per the audit, were to **fold audio QC into an existing agent** (impossible by construction -- a proofer's value is being ears that did not perform the take, so neither director can QC its own render) and to **pile ensemble casting onto voice-designer** (which would break its deliberately one-voice, reveal-safe remit). The audit also explicitly warned **against over-splitting**: keep adapter+director together in live-narration-director and keep sound-design+mix together in sound-engineer, because the audio risk is gaps, not fragmentation. Those were left intact; only ensemble casting was carved out.

### Reason

The audit named these two as the highest-value audio moves precisely because each closes a gap the existing chain could not otherwise see: the rendered-audio verification loop and the cast-as-a-whole ownership. Building the prooflistener as a diagnose-and-route role (it names defects and routes the cheap re-roll, never performing it) and the casting-director as an author-and-route role (it owns the cast sheet and briefs voice-designer, never running the endpoint itself) preserves the project's load-bearing **diagnose-then-apply / author-then-route** separation, so adding two lenses does not create two new hands editing the deliverables. Carving ensemble casting out of live-narration-director rather than splitting adapter from director keeps the single creative act whole while giving the genuinely different altitude its own owner -- the same successful pattern as the sound-engineer carve-out. Hiring now but wiring in a single later pass keeps the change reversible and lets each role be slotted at its correct cadence rather than forced into the pipeline prematurely.

### Consequences

- Two new agent charters exist under `.claude/agents/`: `prooflistener.md` (read-only audio QC; routes a timestamped re-roll list to the owning director, never re-renders) and `casting-director.md` (authors the cast sheet and briefs voice-designer; no Bash by design).
- Each new agent carries the shared crew directives via the crew handbook and a field-notes file (Decision 062) under `.claude/agent-notes/`.
- A new production-reference document exists: `docs/10-vision/audio/cast-sheet.md`, the casting-director's single source of truth for the live edition's cast (the assignment, the contrast map, the cross-chapter consistency ledger, the sign-off gate). It derives from canon and is not a canon authority.
- `live-narration-director.md` is edited so its provisioning step **consumes** the cast sheet and routes unassigned speakers / undesigned voices back to the casting-director; it no longer owns the cast-as-a-SET decision.
- The pipeline and workflow skills are **unchanged** for now; neither new audio agent is invoked automatically yet. The consolidated wiring pass is the tracked follow-up.
- No canon, prose, or existing voice asset changed. The new Decision doc and the new cast-sheet doc are well-formed and pass the metadata and link validators.

### Affected Documents

- `.claude/agents/prooflistener.md`, `.claude/agents/casting-director.md` (new charters)
- `.claude/agent-notes/prooflistener.md`, `.claude/agent-notes/casting-director.md` (new field-notes files)
- `.claude/agents/live-narration-director.md` (edited: provisioning step now consumes the cast sheet; ensemble-casting remit removed)
- `docs/10-vision/audio/cast-sheet.md` (new production-reference, owned by casting-director)
- `docs/00-governance/decision-log/index.md` (index row added; count incremented)

### Reconsider Only If

The author decides either hire is not worth maintaining (revert that hire via git history), or the consolidated wiring pass reassigns a role's cadence or owner, or a single project-wide pronunciation **lexicon** is established (audit recommendation 4), which would sharpen the prooflistener's consistency check and may change where that lexicon is owned. All are reversible via git history.
