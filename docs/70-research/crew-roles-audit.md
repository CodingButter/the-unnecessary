---
title: "Crew vs Industry Roles Audit (Book Production)"
document_type: "research"
status: "reference"
authority: "research-grounding"
summary: "Maps the 21-agent production crew of The Unnecessary against the standard professional roles of the literary-novel craft/editorial chain, surfacing prioritized GAPS (roles we lack), OVERLOADED agents (one agent wearing 2+ distinct roles), and apparent OVER-FRAGMENTATION (several agents on one role), plus where our structure is deliberately better than the industry default. A recommendation for the author to review; changes no agent files."
tags:
  - research
  - crew
  - roles-audit
  - editorial
  - pipeline
  - process
source: "Industry research (cited inline; EFA, Jane Friedman, Penguin Random House, SFWA, et al.) cross-referenced against the live crew inventory under .claude/agents/. Synthesis only; no agent files changed."
related:
  - "../../CLAUDE.md"
  - "../../docs/00-governance/novel-development-guide.md"
  - "../../.claude/agents/adjudicator.md"
  - "../../.claude/agents/continuity-auditor.md"
  - "../../.claude/agents/prose-critic.md"
  - "../../.claude/agents/clarity-auditor.md"
  - "../../.claude/agents/logic-auditor.md"
source_documents:
  - "CLAUDE.md"
  - "docs/00-governance/novel-development-guide.md"
  - ".claude/agents/"
---

# Crew vs Industry Roles Audit (Book Production)

> Scope note. The cited industry research delivered for this audit covers ONE
> domain: the literary-novel craft/editorial chain (author, developmental, line,
> copy, proof, continuity, fact-check, the reader tiers, sensitivity, evaluation,
> and editorial project management). It does NOT cover audiobook narration or
> audio-drama production. Our audio agents (audiobook-director, live-narration-director,
> sound-engineer, voice-designer, portrait-renderer) are therefore mapped only
> provisionally and flagged as out-of-cited-scope; a follow-up pass with
> audiobook/audio-drama research is needed to audit them properly. This document
> recommends; it changes no agent file.

## Crew-to-industry crosswalk (the 21 agents)

| Agent | Closest industry role(s) | Coverage |
|---|---|---|
| chapter-drafter | Author / Writer | Covered |
| blueprint-author | Author's structural planning (pre-draft); developmental-adjacent | Covered (pre-prose only) |
| prose-critic | Line editor (diagnosis side) | Covered |
| adjudicator | Managing/production editor (query reconciliation) + the executor that APPLIES line/copy/continuity fixes | Covered, overloaded (see 2) |
| continuity-auditor | Story / continuity editor + internal fabrication fact-check | Covered |
| canon-scout | Story/continuity editor (ground-truth read) | Covered |
| entity-author | Story/continuity editor (builds the bible) | Covered |
| entity-extractor | Story/continuity editor (maintains/backfills the bible) | Covered |
| logic-auditor | Researcher/fact-checker (plausibility) + developmental (plot logic) | Covered, mild overload (see 2) |
| research-consultant | Researcher / fact-checker (real-world method) | Covered |
| lay-reader | Beta reader (raw reaction) | Covered |
| clarity-auditor | Beta reader (analysis of the reaction) | Covered |
| focus-reviewer | Bespoke (Focus methodology); developmental/reveal-timing-adjacent | Project-specific |
| echo-auditor | Bespoke (cross-chapter freshness); line/developmental-adjacent | Project-specific |
| recap-generator | Continuity-support scaffolding | Project-specific |
| audiobook-director | Audiobook narration direction | Out of cited scope |
| live-narration-director | Audio-drama adaptation + voice/casting direction | Out of cited scope |
| sound-engineer | Audio-drama sound design + mix | Out of cited scope |
| voice-designer | Casting / voice design | Out of cited scope |
| portrait-renderer | Visual asset production | Out of cited scope |
| systems-engineer | Tooling/dev (not editorial) | Infrastructure |

Two structural facts shape everything below. (1) Our reviewers DIAGNOSE only; they
never rewrite. A single executor, the adjudicator, APPLIES every accepted fix to the
one prose file. (2) Continuity is not a single editor's side-job here; it is a formal
canon system (the bibles) served by four agents split by verb. Both are deliberate and
both turn out to be strengths, not accidents.

---

## 1. GAPS: proven industry roles with NO agent (candidate HIRES)

### 1.1 Developmental / structural editor of the assembled draft  [PRIORITY: HIGH]
- Industry role: **Developmental editor (content/substantive/structural)** [EFA; Jericho Writers; KA Writing; Rachel Rowlands].
- What it would catch/add: big-picture failures of the FINISHED draft, the most expensive
  errors to fix late: a sagging middle, an unmotivated character turn, structural holes,
  an unearned ending, a pacing collapse, theme drift, chapter-order problems, "what to cut,
  expand, or reorder." Delivered as a revision letter, not line edits.
- Why it is a real gap: our entire post-draft gauntlet operates at or below the scene/
  sentence layer, prose craft (prose-critic), facts vs canon (continuity-auditor),
  reader comprehension (lay-reader plus clarity-auditor), focus landing (focus-reviewer),
  cross-chapter repetition (echo-auditor), and local plausibility (logic-auditor).
  logic-auditor touches plot logic ("effect without cause") but explicitly NOT arc,
  pacing, structure, or theme. Nobody reads the assembled book for architecture.
- How it fits our pipeline: a read-only **structure-auditor** running at two moments, on
  the blueprint set before a section is drafted, and on the assembled chapters of a
  completed act/section. Output is a revision letter routed like any other finding into
  the adjudicator, with scene-level rework routed back to chapter-drafter.
- Could an existing agent absorb it? Not cleanly. blueprint-author works PRE-prose (it
  plans architecture, it does not critique the realized architecture, different timing and
  different lens). focus-reviewer audits per-entity emphasis, not whole-arc shape. This
  warrants its own role.

### 1.2 Copy editor (prose mechanics and style sheet)  [PRIORITY: MED-HIGH]
- Industry role: **Copy editor** [EFA; Jane Friedman].
- What it would catch/add: the mechanical error class that erodes credibility on every
  page, grammar, spelling, punctuation, usage, homophones (being/begin), inconsistent
  hyphenation and capitalization, missing words, and the maintenance of a STYLE SHEET that
  pins house spellings and number/hyphenation rules. The research stresses developmental
  and line editors read straight past these while focused on story and style.
- Why it is a real gap: we enforce some mechanics structurally (the no-em-dash rule, the
  metadata/link validators) but no agent owns prose mechanics or a running style sheet.
  prose-critic is craft (style vs mechanics is a deliberate industry split), and
  continuity-auditor tracks FACT consistency, not punctuation/usage.
- How it fits our pipeline: a **copy-editor** reviewer in the gauntlet that flags mechanics
  and consistency findings for the adjudicator, plus ownership of a project style sheet
  (which doubles as input the audiobook agents already implicitly need).
- Could an existing agent absorb it? Partially. The adjudicator already APPLIES line-level
  fixes, so it could carry mechanics enforcement, but the research is explicit that
  mechanics is a distinct error class needing its own pass, not a rider on a judgment role.

### 1.3 Sensitivity / authenticity reader  [PRIORITY: MED (content-dependent)]
- Industry role: **Sensitivity / authenticity reader** [SFWA; EFA].
- What it would catch/add: misrepresentation and harm invisible to everyone outside the
  depicted group, stereotypes, cultural inaccuracy, harmful tropes, unintentional bias.
  The EFA splits the two lenses: AUTHENTICITY targets portrayals that "might misrepresent"
  (accuracy), SENSITIVITY targets portrayals that "might offend" (harm).
- Why it is a real gap, and why it is rated MED not LOW: the book is grounded cyberpunk in
  Greater Detroit centered on class, race, disability, and abandoned/unprofitable
  communities, exactly the material this role exists to vet. We have no lived-standpoint
  lens anywhere in the crew.
- How it fits our pipeline: an advisory reader pass on drafted chapters that depict a
  specific identity or lived experience; advisory only (the author decides), routed as
  flags, never as silent edits.
- Could an existing agent absorb it? No. The craft and continuity agents lack the lived
  standpoint by definition. Caveat to log for the author: a synthetic agent can only
  APPROXIMATE a sensitivity read; for anything load-bearing this points at a human reader,
  not an agent. The agent's value is triage (surface candidates early), not sign-off.

### 1.4 Proofreader / cold read (fresh-eyes, errors-only final pass)  [PRIORITY: MED]
- Industry role: **Proofreader / cold read** [Jane Friedman; EFA].
- What it would catch/add: the last net, the granular slips everyone upstream has gone
  blind to (sipped/shipped, dropped or transposed words, a misspelled name) plus errors
  INTRODUCED by later stages. The research is emphatic that it must be FRESH EYES, an agent
  uninvolved in earlier passes.
- Why it is a real gap: we do not typeset, but the analog holds, a final cold read on the
  approved prose AND on the narration scripts. The audiobook-director's tag-strip-and-diff
  catches dropped words in the SCRIPT, but no agent does an errors-only cold read of the
  final PROSE, and crucially the adjudicator cannot be that reader because it authored the
  edits (familiarity blindness is the whole point of the role).
- How it fits our pipeline: a terminal **cold-read** pass by an agent deliberately given no
  earlier-stage context, run after the adjudicator finalizes a chapter.
- Could an existing agent absorb it? No, by construction: the role's value is being the one
  agent that did NOT see the chapter before.

### 1.5 Manuscript evaluation / whole-book readiness triage  [PRIORITY: LOW-MED]
- Industry role: **Manuscript evaluation / editorial assessment** [EFA; Jericho Writers].
- What it would add: a single high-level "is this even ready, and where to spend effort"
  diagnostic before committing to expensive passes. Largely subsumed by the developmental
  gap (1.1) and our blueprint gate; list it as a lighter-touch mode of that same hire,
  not a separate body.

### 1.6 Alpha reader / critique partner  [PRIORITY: LOW]
- Industry roles: **Alpha reader; critique partner** [EFA; Rachel Rowlands].
- Largely substituted in our pipeline by the blueprint gate (earliest big-picture check,
  before prose investment) and prose-critic (mid-draft craft diagnosis in a writer's
  vocabulary). No dedicated hire recommended; note the substitution as adequate at our scale.

---

## 2. OVERLOADED: agents wearing 2+ distinct industry roles (candidate SPLITS)

### 2.1 adjudicator  [SPLIT: mostly NO, keep, with one watch-item]
- Distinct roles it wears: (a) **Managing/production editor**, reconciling competing and
  conflicting reviewer queries by authority order and resolving canon conflicts
  loudly/logged; (b) the **executor** that APPLIES accepted fixes, which spans the
  line-editor's revising hand AND the copy-editor's mechanical hand AND continuity
  resolution, all in one agent.
- Risk of one generalist: it renders a single accept/reject judgment across craft, focus,
  continuity, and logic findings, each a different expertise, so a subtle line-craft call
  and a hard continuity fact get the same one-line treatment and the craft nuance can be
  ruled shallowly.
- Recommendation: KEEP the APPLICATION centralized. Concentrating all edits in one surgical
  hand is precisely the managing-editor function and it structurally prevents the
  multi-hands inconsistency the research warns about. The watch-item is the DECISION load:
  lean harder on each originating specialist's recommended resolution so the adjudicator
  ratifies rather than re-adjudicates expertise it does not hold. Low urgency.

### 2.2 logic-auditor  [SPLIT: NO]
- Distinct roles it wears: (a) **Researcher/fact-checker** (real-world plausibility,
  impossible clocks/travel/counts, a device defying its own mechanism) and (b) a sliver of
  **developmental editor** (plot logic, effect without cause).
- Risk: low. Both run on one "does this add up" engine, and the developmental sliver it
  carries is exactly why 1.1 is scoped to arc/pacing/structure/theme (the parts logic-auditor
  does NOT cover) rather than plot-logic (which it does).
- Recommendation: keep combined; just do not mistake it for the missing developmental editor.

### 2.3 continuity-auditor  [SPLIT: NO]
- It runs an external pass (chapter vs canon) and an internal pass (chapter vs itself,
  object/presence/possession/character/sequence ledger), plus FABRICATION detection. These
  read like several jobs but are one industry role, the **story/continuity editor**, applied
  on two axes, sharing one adversarial-verification mindset. The real-world fact-check lives
  elsewhere (research-consultant, logic-auditor), so there is no true double-hat. Keep.

### 2.4 live-narration-director  [SPLIT: already done, healthy precedent]
- It historically bundled adaptation, per-line voice/casting direction, AND sound design/
  mix. The new **sound-engineer** has already carved out sound design and mix, a clean
  split that left the director with two still-distinct audio-drama jobs (dramatist/adapter
  vs voice/casting director). Fine at our scale. Flagged as out of cited research scope;
  a proper audio-drama-roles audit should confirm the seam.

Top split-candidate to name: the **adjudicator** (decide-plus-apply across multiple error
classes). The recommendation is nuanced, not "split it", see 2.1.

---

## 3. OVER-FRAGMENTED: several agents on ONE industry role (candidate MERGES)

The honest finding: the crew LOOKS fragmented in three places, but each split is by VERB on
a shared substrate and is deliberate. None should be merged.

### 3.1 Story/continuity editor split across FOUR agents  [MERGE: NO]
- Agents: canon-scout (read ground truth), entity-author (write the bible),
  entity-extractor (maintain/backfill the bible), continuity-auditor (verify against it).
- Single industry role: **story/continuity editor** [Penguin Random House; EFA].
- Verdict: KEEP, and it is BETTER than the industry default. Read/write/maintain/verify are
  separated so no agent grades its own output and canon-scout stays read-only so it can
  never invent. For a multi-book series with a formal canon hierarchy, this is the
  continuity-bible function done right, not redundancy.

### 3.2 Beta reading split across TWO agents  [MERGE: NO]
- Agents: lay-reader (blind raw retelling, no craft/continuity judgment) and clarity-auditor
  (analyzes the retellings against intended takeaway).
- Single industry role: **beta reader** [EFA].
- Verdict: KEEP, and it is BETTER than industry. Separating the naive REACTION from the
  ANALYSIS keeps the reader genuinely blind; a single agent told to "analyze" would
  contaminate the naive read it depends on.

### 3.3 Line/craft editing split across diagnosis and application  [MERGE: NO]
- Agents: prose-critic (and the other reviewers) DIAGNOSE; adjudicator APPLIES.
- Single industry role: **line editor** (often bundled with copyedit) [Jane Friedman].
- Verdict: KEEP. Diagnose-then-apply through one executor is the managing-editor
  reconciliation pattern, it prevents five agents editing one file into mush. Deliberate.

The only faint merge candidate is recap-generator, a small continuity-support scaffold that
could in principle fold into canon-scout, but it is cheap, single-purpose, and harmless.
Not worth merging. LOW.

---

## Prioritized recommendation (highest-value moves)

1. **HIRE a developmental / structural editor** (whole-draft arc, pacing, structure, theme).
   Biggest hole: the gauntlet has no architecture lens on the assembled book. [HIGH]
2. **HIRE a copy editor** (prose mechanics plus a maintained style sheet). Distinct error
   class no agent owns; the style sheet also feeds the audio agents. [MED-HIGH]
3. **HIRE a sensitivity / authenticity reader** for the Detroit/class/disability material,
   as triage, with the explicit caveat that a synthetic pass approximates and load-bearing
   cases point at a human reader. [MED]
4. **ADD a terminal cold-read / proofreader** by an agent deliberately denied earlier-stage
   context, on the finalized prose and the narration scripts. [MED]
5. **Resist consolidation.** Do NOT merge the four-agent continuity system or the
   two-agent beta-reading split; both are deliberately superior to the industry default.

## Where our structure is BETTER than the industry default (do not "fix")

- **Continuity editing is elevated to a canon SYSTEM**, four agents over the bibles, with
  read/write/maintain/verify separated so nothing grades itself. Industry folds this into
  one copyeditor's side-notes; ours is built for a series. [vs Penguin Random House model]
- **Beta reading is split into a blind reader plus an analyst**, preserving a truly naive
  first read that a single "analyze this" agent would destroy. [vs EFA beta model]
- **The managing/production-editor function is externalized into process**, the workflow
  skills, the CLAUDE.md canon hierarchy, and the adjudicator's query reconciliation, rather
  than resting in one fallible coordinator. Process-as-code. [vs EFA project-management role]
- **Diagnosis and application are split by construction**: all reviewers flag, one executor
  applies, which prevents the multi-hands inconsistency the managing editor exists to fix.
- **We correctly have NO indexer** (nonfiction-only; the one editorial role a novel does not
  need), and no spurious roles padding the crew. [EFA]

## Sources

- EFA, Editorial Services Definitions - https://www.the-efa.org/editorial-services-definitions/
- Jane Friedman, line vs copy vs proofreading - https://janefriedman.com/the-differences-between-line-editing-copy-editing-and-proofreading/
- KA Writing, types of book editing - https://www.ka-writing.com/the-different-types-of-book-editing/
- Jericho Writers, types of editing - https://jerichowriters.com/types-of-editing-how-to-choose/
- Rachel Rowlands, types of fiction editing - https://racheljrowlands.com/2021/10/14/types-of-fiction-editing-which-one-is-for-you/
- Penguin Random House, maintaining continuity (copy editor) - https://authornews.penguinrandomhouse.com/maintaining-continuity-tales-from-the-copy-editor/
- Taddle Creek, fact-checking fiction - https://www.taddlecreekmag.com/the-taddle-creek-guide-to-fact-checking-fiction
- SFWA, what is sensitivity reading - https://sfwa.org/2024/04/02/what-is-sensitivity-reading/
