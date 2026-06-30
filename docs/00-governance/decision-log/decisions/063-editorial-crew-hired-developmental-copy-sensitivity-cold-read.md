---
title: "Decision 063: The Editorial Crew Expands by Four (Developmental, Copy, Sensitivity, Cold-Read) as Read-Only Diagnosers"
document_type: "decision"
status: "active"
authority: "governance"
summary: "Hires the four editorial roles the crew-roles audit flagged as GAPS, each a distinct error class no existing agent owned, all built as read-only DIAGNOSERS that route findings to the adjudicator (Decision 060) and never edit prose themselves. (1) developmental-editor: reads the ASSEMBLED book (or the blueprint SET) for big-picture architecture -- arc, sagging middles, structure and chapter order, character-arc motivation, theme drift, setup/payoff -- as a prioritized revision letter, the most expensive errors to fix late. (2) copy-editor: owns prose MECHANICS (grammar, spelling, punctuation, usage, homophones, hyphenation/capitalization consistency, missing/doubled words) and keeps the project STYLE SHEET; mechanics is a deliberate industry split from prose-critic craft and continuity-auditor fact. (3) sensitivity-reader: an advisory lived-standpoint TRIAGE for the Detroit/class/race/disability material, two lenses (authenticity = might misrepresent, sensitivity = might offend/harm); load-bearing caveat baked in -- a synthetic agent only APPROXIMATES, so it surfaces candidates early and points load-bearing cases at a HUMAN reader, triage not sign-off. (4) cold-reader: a terminal fresh-eyes errors-ONLY proofread of the FINALIZED prose and narration scripts by the one agent deliberately denied all earlier-stage context, defeating familiarity blindness and catching errors later edits INTRODUCED. Grounded in docs/70-research/crew-roles-audit.md sections 1.1-1.4. FOLLOW-UP, explicit: these four are HIRED but NOT yet wired into the gauntlet/workflows -- wiring is a separate deliberate step (copy-editor and cold-reader fit the per-chapter gauntlet; developmental-editor runs at SECTION/book cadence, not per chapter; sensitivity-reader is conditional on identity-depicting chapters). Changes no canon or prose; reversible via git."
tags: ["decision", "workflow", "crew", "agents", "editorial", "developmental-editor", "copy-editor", "sensitivity-reader", "cold-reader", "roles-audit", "governance", "reversible"]
related:
  - "../../../../.claude/agents/developmental-editor.md"
  - "../../../../.claude/agents/copy-editor.md"
  - "../../../../.claude/agents/sensitivity-reader.md"
  - "../../../../.claude/agents/cold-reader.md"
  - "../../../70-research/crew-roles-audit.md"
  - "./060-autonomous-resolution-crew-resolves-logs-and-proceeds-never-blocks-on-the-author.md"
  - "./062-self-improving-crew-via-per-agent-field-notes.md"
  - "../index.md"
source_documents:
  - ".claude/agents/"
  - "docs/70-research/crew-roles-audit.md"
---

## Decision 063: The Editorial Crew Expands by Four (Developmental, Copy, Sensitivity, Cold-Read) as Read-Only Diagnosers

**Date:** 2026-06-30
**Status:** Active but Revisable
**Category:** Workflow

### Decision

The crew gains **four editorial agents**, hired against the prioritized GAPS the crew-roles audit identified (`docs/70-research/crew-roles-audit.md`, sections 1.1 through 1.4 and the prioritized recommendation). Each fills a **distinct error class that no existing agent owned**, and each is built in the house pattern: a **read-only DIAGNOSER** that reads, flags, and routes its findings to the **adjudicator** (Decision 060), and **never edits prose itself**. The one read-write exception is narrow and named below.

The four roles, and the one thing each catches:

- **developmental-editor** (`.claude/agents/developmental-editor.md`) catches **big-picture architecture failures of the assembled book**: a sagging middle, an unmotivated character turn, a structural hole, an unearned ending, a pacing collapse, theme drift, a chapter in the wrong order, a setup with no payoff or a payoff with no setup. It reads a whole act/section (or the blueprint SET before a section is drafted) and returns a prioritized **developmental revision letter** saying what to cut, expand, or reorder. It never line-edits.
- **copy-editor** (`.claude/agents/copy-editor.md`) catches the **mechanical error class that erodes credibility on every page**: grammar, spelling, punctuation, usage, homophones (being/begin, sipped/shipped), inconsistent hyphenation and capitalization, missing or doubled words, number and recurring-term treatment. It also **owns and maintains the project's house style sheet** (the Copy-Edit Consistency Ledger kept within `docs/10-vision/style/formatting.md`, the project's single style sheet, not a separate document) that pins the book's house spellings and treatment decisions. It is read-only on the manuscript and read-write only on that one style sheet.
- **sensitivity-reader** (`.claude/agents/sensitivity-reader.md`) catches **misrepresentation and harm invisible to everyone outside the depicted group** in the book's class, race, disability, and abandoned-community material, read through two separated lenses: **authenticity** (portrayals that might MISREPRESENT) and **sensitivity** (portrayals that might OFFEND or do harm: stereotypes, harmful tropes, unintentional bias). It is advisory only and never signs off (see the caveat below).
- **cold-reader** (`.claude/agents/cold-reader.md`) catches the **granular slips everyone upstream has gone blind to** plus the **errors later editing stages INTRODUCED**: a homophone, a dropped/doubled/transposed word, a mis-keyed character or place name, a self-contradicting micro-detail, a dangling clause an edit left behind, a narration line that lost a word. It runs a **terminal, fresh-eyes, errors-only** proofread of the FINALIZED prose and the narration/cue scripts, by the one agent **deliberately denied all earlier-stage context** so familiarity blindness cannot hide the slip.

### Why these four — each a distinct error class no existing agent owned

The audit's grounding (sections 1.1 through 1.4) is that the entire post-draft gauntlet already operates at or below the scene/sentence layer, and four proven editorial functions had no owner:

- **Arc / structure (developmental-editor, HIGH).** Nobody read the *assembled* book for architecture. prose-critic is craft, continuity-auditor is fact-vs-canon, lay-reader plus clarity-auditor is comprehension, focus-reviewer is per-entity emphasis, echo-auditor is cross-chapter repetition, logic-auditor is local plot-logic and explicitly **not** arc, pacing, structure, or theme. blueprint-author plans architecture *pre*-prose; it does not critique the realized architecture. The expensive errors are the late, structural ones, and they had no lens.
- **Mechanics + style sheet (copy-editor, MED-HIGH).** The project enforces some mechanics structurally (the no-em-dash rule, the validators), but no agent owned grammar/spelling/punctuation/usage or a running style sheet. Style versus mechanics is a deliberate industry split: prose-critic is craft (voice, rhythm, cliche), and the research is explicit that mechanics is a distinct error class needing its own pass, not a rider on the prose or judgment roles.
- **Sensitivity triage (sensitivity-reader, MED).** The book is grounded cyberpunk in Greater Detroit centered on class, race, disability, and abandoned/unprofitable communities, exactly this role's material, and the crew held no lived-standpoint lens anywhere. The craft and continuity agents lack the standpoint by definition.
- **Terminal cold-read (cold-reader, MED).** No agent did an errors-only cold read of the FINAL prose, and crucially the adjudicator **cannot** be that reader because it authored the edits, so familiarity blindness is built into it. The role's whole value is being the one agent that did not see the chapter before.

### The sensitivity-reader caveat (load-bearing — recorded deliberately)

A synthetic agent can only **APPROXIMATE** a sensitivity read. It has no lived standpoint; it pattern-matches against what it has read about one. Therefore its value is **triage, never sign-off**: it surfaces candidates early and cheaply so a human can decide where to spend a real reader's time. For anything **load-bearing** (a portrayal central to the book, a depiction that could plausibly do real-world harm, any case where being wrong carries high stakes), the agent does not adjudicate; it **points at a human sensitivity/authenticity reader from the depicted community** and says so in its report. This caveat is written into the charter and must appear in every report the agent produces. Being the early-warning system is the job; pretending to be the final word is the one way this role does damage.

### Follow-up: hired, NOT yet wired (a separate deliberate step)

These four agents are **hired** (their charters and field-notes files exist) but are **NOT yet wired into the gauntlet or the workflow skills**. Wiring is the explicit next step and is deliberate per role, because they do not all share one cadence:

- **copy-editor** and **cold-reader** fit the **per-chapter gauntlet** (copy-editor as a mechanics reviewer alongside prose-critic and continuity-auditor; cold-reader as a terminal pass after the adjudicator finalizes the chapter, on the locked prose and the narration scripts).
- **developmental-editor** runs at **SECTION / book cadence, not per chapter**: on the blueprint SET before a section is drafted, and on the assembled chapters of a completed act/section. Wiring it as a per-chapter reviewer would misuse it.
- **sensitivity-reader** is **conditional**: it runs only on chapters that depict a specific identity or lived experience, as an advisory pass, not on every chapter.

Until that wiring lands, the four are available to invoke by hand but are not part of any automated pipeline.

### Previous or Alternative Direction

Before this, the crew's post-draft gauntlet had no architecture lens on the finished book, no owner for prose mechanics or a style sheet, no lived-standpoint lens for the book's identity material, and no terminal fresh-eyes proofread. The rejected alternatives, per the audit, were to **fold these into existing agents** (the audit found none could absorb them cleanly: developmental is distinct from blueprint-author's pre-prose planning and focus-reviewer's emphasis lens; mechanics is a distinct error class from prose-critic's craft and a poor rider on the adjudicator's judgment role; sensitivity needs a standpoint the craft/continuity agents lack by definition; and the cold read is broken the moment the reader has earlier-stage context, so the adjudicator cannot be it) or to **leave the gaps open** (which leaves the most expensive late errors uncaught). The audit also explicitly warned **against** over-consolidation, so the four-agent continuity system and the two-agent beta-reading split were left intact.

### Reason

The audit named these four as the highest-value moves precisely because each is a proven editorial function covering an error class the gauntlet could not otherwise see, and the late/structural and final-proofing classes are the most expensive to fix when missed. Building them as read-only diagnosers that route to the adjudicator preserves the project's load-bearing **diagnose-then-apply** separation (all reviewers flag, one executor applies), so adding four lenses does not create four hands editing one file into mush. The sensitivity caveat keeps the role honest about what a synthetic pass can and cannot do. Hiring now but wiring later keeps the change reversible and lets each role be slotted at its correct cadence rather than forced into a uniform per-chapter slot.

### Consequences

- Four new agent charters exist under `.claude/agents/`: `developmental-editor.md`, `copy-editor.md`, `sensitivity-reader.md`, `cold-reader.md`, each a read-only diagnoser (cold-reader read-only by construction; copy-editor read-write only on the style sheet) routing findings to the adjudicator.
- Each new agent carries the shared crew directives via the crew handbook and a field-notes file (Decision 062) under `.claude/agent-notes/`.
- The copy-editor owns and extends the project's single house **style sheet** (the Copy-Edit Consistency Ledger within `docs/10-vision/style/formatting.md`, not a separate document); that style sheet also feeds the audio agents.
- The gauntlet and workflow skills are **unchanged** for now; none of the four is invoked automatically yet. Wiring is the tracked follow-up described above.
- No canon, prose, or existing agent behavior changed. The new Decision doc is well-formed and passes the metadata and link validators.

### Affected Documents

- `.claude/agents/developmental-editor.md`, `.claude/agents/copy-editor.md`, `.claude/agents/sensitivity-reader.md`, `.claude/agents/cold-reader.md` (new charters)
- `.claude/agent-notes/developmental-editor.md`, `.claude/agent-notes/copy-editor.md`, `.claude/agent-notes/sensitivity-reader.md`, `.claude/agent-notes/cold-reader.md` (new field-notes files)
- `docs/00-governance/decision-log/index.md` (index row added; count incremented)

### Reconsider Only If

The author decides any of the four is not worth maintaining (revert that hire via git history), or the wiring step reassigns a role's cadence, or the sensitivity-reader is judged to add no triage value over a direct human read (in which case retire the agent and rely on a human reader, never demote the human caveat). All are reversible via git history.
