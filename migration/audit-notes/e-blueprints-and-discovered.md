# Audit note: Task E

Blueprints, manuscript, continuity, research, and discovered-file scan for Phase 01 (Repository Audit) of "The Unnecessary".

Authority: `migration/REPOSITORY-REORGANIZATION-SPEC.md` (wins all conflicts); runbook `migration/plan/01-repository-audit.md`. This note is READ-ONLY against all project documents. The only file written by this task is this note. No source document was moved, renamed, split, edited, archived, or deleted. Destinations are labelled "recommended"; the orchestrator decides final paths.

Avoidance of em dashes is observed in all prose authored here. Quotations of source headings reproduce the source verbatim and may contain em dashes; those are quoted text, not my prose.

---

## Scope summary (what this task covers)

1. Everything under `chapter-blueprints/` (the template, plus any other blueprints).
2. A whole-repository search for manuscript chapters, continuity documents, research files, and any filled chapter blueprints other than the template. Presence or confirmed absence recorded with the commands that proved it.
3. Two discovered governance/process documents not covered by Tasks B/C/D: `CLAUDE.md` and `Memory Conventions.md`. These are operational/process governance, NOT story canon.

---

## chapter-blueprints/Chapter Blueprint Template.md

- Title (as stated in the doc): `Chapter Blueprint Template`
- Current path: `/home/codingbutter/Novel/chapter-blueprints/Chapter Blueprint Template.md`
- Document type: planning scaffold / reusable template (a blank chapter-blueprint form to be copied per chapter)
- Apparent version: not stated (no version label, no frontmatter, no revision number anywhere in the file)
- Canon status: not stated as a version label. By role it is NOT story canon; it is a blueprint authoring template. It is the single document the master spec validation requires to "remain intact" (master spec "Validation Requirements", line 874: "Confirm the Chapter Blueprint Template remains intact.").
- Subject: A comprehensive per-chapter blueprint form. It instructs the author to copy the file for each chapter and replace bracketed placeholders (suggested filename `chapter-##-short-title.md`). It captures chapter metadata, summary, narrative purpose, viewpoint, reader information, opening, a repeatable per-scene breakdown block, chapter-level escalation and conflict layers, character development, relationships, theme, worldbuilding, technology, setup/payoff, foreshadowing, imagery, pacing, prose guidance, opening/closing contrast, ending hook, continuity-ledger updates, canon checks, drafting checklist, open questions, revision notes, and a completion standard.

### Mermaid blocks

- Mermaid block count: 1. Located under the `## Chapter Escalation` heading (a `flowchart LR` Opening-condition to Chapter-ending diagram). Confirmed by `grep -c '```mermaid'` returning 1.

### FULL heading outline (every H1, H2, H3; H1 marked, otherwise level shown)

- H1 `# Chapter Blueprint Template`
- H1 `# Chapter [Number]: [Working Title]`
  - H2 `## Chapter Metadata` (contains a YAML block; note `chapter_status: "blueprint"`)
  - H2 `## Chapter Summary`
  - H2 `## Narrative Purpose`
    - H3 `### Primary Purpose`
    - H3 `### Secondary Purposes`
    - H3 `### Why This Chapter Cannot Be Removed`
  - H2 `## Chapter Promise`
  - H2 `## Viewpoint Character`
    - H3 `### External Goal`
    - H3 `### Internal Pressure`
    - H3 `### Starting Emotional State`
    - H3 `### Ending Emotional State`
    - H3 `### False Assumption`
    - H3 `### Decision`
  - H2 `## Reader Information`
    - H3 `### What the Viewpoint Character Knows`
    - H3 `### What the Viewpoint Character Does Not Know`
    - H3 `### What the Reader Already Knows`
    - H3 `### New Information Revealed`
    - H3 `### Information Deliberately Withheld`
  - H2 `## Opening`
    - H3 `### Opening Image`
    - H3 `### Opening Situation`
    - H3 `### Immediate Question`
- H1 `# Scene Breakdown` (instruction: "Duplicate the following section for every scene.")
  - H2 `## Scene [Number]: [Scene Title]`
    - H3 `### Scene Metadata` (contains a YAML block)
    - H3 `### Scene Purpose`
    - H3 `### Viewpoint Goal`
    - H3 `### Opposition`
    - H3 `### Stakes`
    - H3 `### Entry Condition`
    - H3 `### Major Beats`
    - H3 `### Scene Turn`
    - H3 `### Exit Condition`
    - H3 `### Emotional Movement`
    - H3 `### Relationship Movement`
    - H3 `### Information Revealed`
    - H3 `### Technology and Worldbuilding`
    - H3 `### Sensory Anchor`
    - H3 `### Dialogue Objective` (contains a Markdown table)
    - H3 `### Subtext`
    - H3 `### Continuity Changes`
    - H3 `### Scene Ending`
- H1 `# End of Scene Breakdown`
  - H2 `## Chapter Escalation` (contains the single Mermaid `flowchart LR` block)
  - H2 `## Conflict Layers`
    - H3 `### External Conflict`
    - H3 `### Interpersonal Conflict`
    - H3 `### Internal Conflict`
    - H3 `### Thematic Conflict`
  - H2 `## Character Development`
    - H3 `### Viewpoint Character`
    - H3 `### Supporting Characters` (contains a Markdown table)
    - H3 `### Character Contradictions`
  - H2 `## Relationships` (contains a Markdown table)
  - H2 `## Theme`
    - H3 `### Primary Theme`
    - H3 `### Thematic Question`
    - H3 `### Competing Answers`
  - H2 `## Worldbuilding Introduced`
  - H2 `## Technology Used` (contains a Markdown table)
  - H2 `## Setup and Payoff`
    - H3 `### Setups Introduced` (contains a Markdown table)
    - H3 `### Earlier Setups Paid Off` (contains a Markdown table)
    - H3 `### Red Herrings`
  - H2 `## Foreshadowing`
  - H2 `## Symbolic or Repeated Imagery`
  - H2 `## Pacing Plan`
    - H3 `### Opening Pace`
    - H3 `### Middle Pace`
    - H3 `### Ending Pace`
    - H3 `### Intended Balance`
  - H2 `## Prose Guidance`
    - H3 `### Tone`
    - H3 `### Narrative Distance`
    - H3 `### Description Priorities`
    - H3 `### Dialogue Style`
    - H3 `### Technical Explanation Limit`
    - H3 `### Language to Avoid`
  - H2 `## Opening and Closing Contrast`
    - H3 `### Opening Condition`
    - H3 `### Closing Condition`
    - H3 `### Irreversible Change`
  - H2 `## Ending Hook`
    - H3 `### Hook Type`
    - H3 `### Intended Hook`
    - H3 `### Reader Question`
  - H2 `## Continuity Ledger Updates`
    - H3 `### Character State` (contains a Markdown table)
    - H3 `### Knowledge Changes` (contains a Markdown table)
    - H3 `### Relationship Changes`
    - H3 `### Resources`
    - H3 `### Injuries and Physical Consequences`
    - H3 `### Promises, Threats, and Obligations`
    - H3 `### Secrets`
    - H3 `### Technology State`
    - H3 `### Location Changes`
  - H2 `## Canon Checks` (checklist that names: Narrative Brief, Story Bible, Character Bible, World and Technology Rules, Master Timeline, Plot Outline and Chapter Map, Previous chapter blueprints, Existing Continuity Ledger)
  - H2 `## Drafting Checklist`
  - H2 `## Open Questions`
  - H2 `## Revision Notes`
    - H3 `### What Worked`
    - H3 `### What Needs Revision`
    - H3 `### Continuity Problems`
    - H3 `### Pacing Problems`
    - H3 `### Character Problems`
    - H3 `### Changes Made to Canon`
  - H2 `## Chapter Completion Standard`

Heading totals (verified by grep on `^#{1,3} `): H1 = 4; H2 = 30; H3 = 64. The four H1 headings are `# Chapter Blueprint Template`, `# Chapter [Number]: [Working Title]`, `# Scene Breakdown`, and `# End of Scene Breakdown`.

- Recommended destination(s): `docs/40-blueprints/_templates/chapter-blueprint-template.md` (matches master spec target tree lines 222 to 223 exactly).
- Split decision: relocate-intact. Do NOT split. The master spec validation requires the template to remain intact (line 874). The whole file maps unchanged to the single destination above; no heading boundary mapping applies because there is no split.
- Internal relative Markdown links found: none. The file contains backtick code spans such as `chapter-##-short-title.md` (a suggested filename, not a link) and `chapter-XX-title` style references, but no `[text](path)` Markdown links. Confirmed by grep for `]\([^)]+\)` returning nothing.
- Active-or-archive: active. It is the live authoring scaffold for all future chapter blueprints and is a named validation target. It relocates intact; it is not archived.
- Conflicts/ambiguities observed: none specific to the template. Minor note for the orchestrator: the template's `## Canon Checks` references an "Existing Continuity Ledger" and the `## Continuity Ledger Updates` section instructs transfer of facts into a Continuity Ledger, yet no Continuity Ledger document exists in the repository today (see absence findings below). This is expected: master spec Phase 13 creates lightweight continuity files only after chapters are approved. Recorded, not resolved.

---

## CLAUDE.md (discovered governance/process document)

- Title (as stated in the doc): `The Unnecessary — Project Instructions`
- Current path: `/home/codingbutter/Novel/CLAUDE.md`
- Document type: operational entry / project-instructions file (root harness file auto-loaded into every session). NOT story canon. It is an orientation and operating layer plus the mem0 operating protocol.
- Apparent version: not stated (no version label or frontmatter)
- Canon status: explicitly NON-canon by its own declaration. The file states it is "the entry / operational layer, not a canon document" and "does not define story canon and must never silently do the job of a canon or planning document." It defers all canon authority to the bibles and the Development and Canon Guide.
- Subject: Two parts. Part one orients the project (what "The Unnecessary" is, a brief premise, and a "Where authority lives" table that defers to the Development and Canon Guide, the Memory Conventions spec, and the eight named canon documents). Part two is the mandatory mem0 operating protocol (architecture table, the golden rules including the infer=false rule, graph-subordinate-to-canon stance, metadata schema, write/recall protocols, an agent directive block, a tool cheat sheet, and constraints/gotchas).

### FULL heading outline (every H1, H2, H3)

- H1 `# The Unnecessary — Project Instructions`
  - H2 `## What this project is`
  - H2 `## Where authority lives (defer; do not duplicate)`
- H1 `# mem0 — Operating Protocol (MANDATORY)`
  - H2 `## What it is (architecture)`
  - H2 `## THE GOLDEN RULES`
  - H2 `## The graph is ON — with canon subordinate`
  - H2 ``## Metadata schema (use this; do NOT add a `category` field)``
  - H2 `## Write protocol (persist)`
  - H2 `## Recall protocol (read)`
  - H2 `## Agents & workflows — propagate the protocol (novel work)`
    - H3 `### Directive block (paste verbatim into agent/workflow prompts)`
  - H2 `## Tool cheat sheet`
  - H2 `## Constraints & gotchas`

Heading totals (verified by grep): H1 = 2; H2 = 11; H3 = 1.

- Recommended destination(s): Root `CLAUDE.md` (stays at root, updated in place). The master spec target tree lists `CLAUDE.md` at the repository root (line 95) and Phase 8 (lines 634 to 636) creates or updates a root-level `CLAUDE.md`. Per the Task E brief and the runbook, CLAUDE.md stays at root and is updated in place in a later phase; Phase 01 does not move or edit it.
- Split decision: keep-intact (and relocate-intact in the sense that it stays at root). No splitting. A later phase (master spec Phase 8) rewrites/updates it in place at the root; that is not Phase 01 work. No heading boundary mapping applies.
- Internal relative Markdown links found: none. The file references other documents only as backtick code spans (for example `Development and Canon Guide.md`, `Memory Conventions.md`, `Character Bible.md`, `Story Bible.md`, `Master Timeline.md`, `Narrative Brief.md`, `Plot Outline and Chapter Map.md`, `Style Guide.md`, `Technology Rules.md`, `Creative Decision Log.md`, and `.mcp.json`), not as `[text](path)` links. Confirmed by grep for `]\([^)]+\)` returning nothing. These backtick references resolve as filenames present at the repo root today, but they are not Markdown links, so the broken-link check does not apply. Recorded for Task F awareness only.
- Active-or-archive: active. It is the live session-entry file and a named end-state requirement (master spec "Desired End State" line 884: "Read CLAUDE.md."). It is updated in place in Phase 8, not archived.
- Conflicts/ambiguities observed: none on its own content. Note for orchestrator: CLAUDE.md is process/operational governance, not story canon, so it is exempt from canon-conflict adjudication. Its embedded "Where authority lives" table and premise paragraph restate facts owned by the bibles; that is by design (it explicitly defers), not a conflict. Recorded, not resolved.

---

## Memory Conventions.md (discovered governance/process document)

- Title (as stated in the doc): `Memory Conventions (mem0)`
- Current path: `/home/codingbutter/Novel/Memory Conventions.md`
- Document type: process/governance spec for using mem0 (semantic memory) while drafting. NOT story canon. CLAUDE.md names it the "Memory spec" authority for memory practice.
- Apparent version: not stated (no version label or frontmatter)
- Canon status: explicitly NON-canon. The document states mem0 "is NOT the source of truth for canon" and "If a memory and a bible disagree, the bible is right." It governs memory practice, not story facts.
- Subject: How agents write and recall semantic memories while drafting. Covers what memory is and is not, the configured scope (Qdrant collection `novel_memory`, `user_id` `novel`, Neo4j graph via Gemini), the golden rule of writing with infer=false, when to write versus not write, how to phrase a good memory with the metadata schema, the recall-first discipline, maintenance, and an operational restart note.

### FULL heading outline (every H1, H2, H3)

- H1 `# Memory Conventions (mem0)`
  - H2 `## What memory is — and isn't`
  - H2 `## Scope (already configured)`
  - H2 ``## The golden rule of writing: `infer=false` ``
  - H2 `## When to WRITE a memory`
  - H2 `## When NOT to write`
  - H2 `## How to write a good memory`
  - H2 `## How to RECALL (do this first)`
  - H2 `## Maintenance`
  - H2 `## Operational note`

Heading totals (verified by grep): H1 = 1; H2 = 9; H3 = 0.

- Recommended destination(s): `docs/00-governance/memory-conventions.md` (recommended). CAVEAT: the master spec target tree under `docs/00-governance/` enumerates only `index.md`, `canon-hierarchy.md`, `novel-development-guide.md`, `context-loading-guide.md`, and the `decision-log/` subtree (spec lines 99 to 103). It does NOT list a `memory-conventions.md` slot. So this file is an ADDED artifact relative to the spec's explicit enumeration. Two defensible orchestrator options, both recorded for the orchestrator to decide: (a) relocate intact to `docs/00-governance/memory-conventions.md` as an added governance artifact; or (b) leave it at the repository root alongside CLAUDE.md as operational governance, since the spec did not assign it a docs/ slot. I recommend option (a) but flag it as not explicitly provisioned by the spec.
- Split decision: relocate-intact (single coherent process spec; no internal boundaries warrant splitting). If the orchestrator instead chooses to keep it at root, that becomes keep-intact. Either way: no split. No heading boundary mapping applies.
- Internal relative Markdown links found: none. The document references the bibles only as backtick code spans (for example `Character Bible.md`, `Story Bible.md`, `Master Timeline.md`, `Plot Outline and Chapter Map.md`, `Technology Rules.md`, `Style Guide.md`, `Narrative Brief.md`, `Creative Decision Log.md`), not as `[text](path)` links. Confirmed by grep for `]\([^)]+\)` returning nothing.
- Active-or-archive: active. It is the live memory-practice authority that CLAUDE.md defers to. Not archived.
- Conflicts/ambiguities observed: one destination ambiguity, recorded above: the spec does not enumerate a `docs/00-governance/memory-conventions.md` destination, so the orchestrator must decide whether to add the slot or keep the file at root. Not a canon conflict (this is process governance, not story canon). No content conflict observed. Recorded, not resolved.

---

## Whole-repository scan: presence vs. confirmed absence

The repository's novel-relevant Markdown (excluding the `.claude/` BMAD tooling tree and `migration/` working files) is exactly: the nine root monoliths (audited by Tasks B/C/D), plus `CLAUDE.md` and `Memory Conventions.md` (audited here), plus the single blueprint template under `chapter-blueprints/` (audited here). Verified with `git ls-files '*.md' | grep -v '^\.claude/'` and an independent `find` over the working tree.

### Manuscript chapters: CONFIRMED ABSENT

- How confirmed: (1) `find` for directories/files named `manuscript*`, `draft*`, `prose*`, `chapter-*`, `ch[0-9]*` (excluding `.git` and `.claude`) returned nothing. (2) Content grep `grep -rIl -E 'chapter_status:\s*"?(draft|approved|manuscript)"?'` returned nothing (no chapter file carries a draft/approved status; the only `chapter_status` occurrence in the repo is the placeholder `chapter_status: "blueprint"` inside the template's example YAML). (3) No `manuscript/` or `50-manuscript/` directory exists.
- Consistency with spec: master spec Phase 13 (line 793) and `project-status.md` guidance (line 821, `current_manuscript_status: "not started"`) both assume no manuscript chapters are approved yet. Absence is expected, not a defect.

### Continuity documents: CONFIRMED ABSENT

- How confirmed: (1) `find` for directories named `continuity*` and files named `continuity*` or `*ledger*` (excluding `.git` and `.claude`) returned nothing. (2) The phrase "Continuity Ledger" appears only inside canon/governance/planning prose (Creative Decision Log, Development and Canon Guide, Style Guide, Plot Outline and Chapter Map, Narrative Brief, Character Bible) and inside the blueprint template's instructional sections. None of those is a populated continuity document; they are references to a future ledger.
- Consistency with spec: master spec Phase 13 (lines 791 to 807) explicitly creates lightweight continuity files from scratch because no manuscript chapters are approved. The `docs/60-continuity/` tree is mostly-new per the target reference. Absence is expected.

### Research files: CONFIRMED ABSENT

- How confirmed: (1) `find` for directories named `research*` and files named `research*` (excluding `.git` and `.claude`) returned nothing. (2) Content grep for an H1 `# Research` returned only `Development and Canon Guide.md`, where "research" appears as an internal section heading within the guide (owned by Task D), not as a standalone research file.
- Consistency with spec: master spec lists `docs/70-research/` as a target slot (line 249) with no current content. Absence is expected.

### Chapter blueprints other than the template: CONFIRMED ABSENT

- How confirmed: `find chapter-blueprints -type f -name '*.md' ! -name 'Chapter Blueprint Template.md'` returned nothing. The `chapter-blueprints/` directory contains exactly one file, the template. No filled per-chapter blueprint exists.
- Consistency with spec: master spec audit step (line 61) asks to identify "Any existing blueprints"; there are none beyond the template. `docs/40-blueprints/book-1/` will be populated in later phases. Absence is expected.

### Target reorganization directories not yet present (informational)

- `find` for directories named `docs`, `archive`, `planning`, or `canon` (excluding `.git` and `.claude`) returned nothing. None of the master spec Phase 2 target directories exists yet, consistent with Phase 01 being read-only and pre-structure. Recorded for completeness; not in Task E's primary scope.

---

## Read-only compliance

No project document was created, moved, renamed, split, edited, archived, or deleted by this task. The only write performed is this note file at `/home/codingbutter/Novel/migration/audit-notes/e-blueprints-and-discovered.md`. The orchestrator can verify with `git status` showing changes confined to that single path.

---

## Memory candidates

- (fact) Confirmed absent in the repository as of Phase 01 audit: any manuscript chapters, any continuity documents, any research files, and any filled chapter blueprints beyond the template. Proven by find and content grep. Metadata: {type: fact, chapter: null, characters: [], tags: ["migration", "audit", "phase-01", "absence"]}.
- (fact) The only file under chapter-blueprints/ is "Chapter Blueprint Template.md"; it contains exactly one Mermaid block (a flowchart LR under "Chapter Escalation") and the master spec requires the template to remain intact, so it is a relocate-intact to docs/40-blueprints/_templates/chapter-blueprint-template.md. Metadata: {type: decision, chapter: null, characters: [], tags: ["migration", "blueprint-template", "mermaid", "relocate-intact"]}.
- (decision) CLAUDE.md and Memory Conventions.md are operational/process governance, not story canon, and are therefore exempt from canon-conflict adjudication; CLAUDE.md stays at root (updated in place in Phase 8) and Memory Conventions.md is recommended for docs/00-governance/memory-conventions.md. Metadata: {type: decision, chapter: null, characters: [], tags: ["migration", "governance", "claude-md", "memory-conventions"]}.
- (hazard) The master spec target tree under docs/00-governance/ does not enumerate a memory-conventions.md slot, so Memory Conventions.md is an added artifact relative to the spec; the orchestrator must decide whether to add the slot or keep it at root. Recorded, not resolved. Metadata: {type: hazard, chapter: null, characters: [], tags: ["migration", "memory-conventions", "destination-ambiguity"]}.
- (continuity) The blueprint template references an "Existing Continuity Ledger" and instructs transfer of facts into a Continuity Ledger, but no such ledger exists yet; master spec Phase 13 creates lightweight continuity files only after chapters are approved. Metadata: {type: continuity, chapter: null, characters: [], tags: ["migration", "continuity-ledger", "phase-13"]}.
