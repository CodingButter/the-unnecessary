---
title: "target-architecture"
document_type: "migration-report"
phase: "02"
title_text: "Phase 02: Target Architecture"
status: "complete"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Phase 02: Target Architecture

> Authority note: the master spec at `migration/REPOSITORY-REORGANIZATION-SPEC.md` is authoritative and overrides this document. If anything here ever conflicts with the master spec, the spec wins and this document must be corrected to match it. This phase decides SHAPE only. It writes no canon, relocates nothing, and archives nothing (archival is reserved for Phase 09).

This document is the single stable architecture contract every later phase builds against. It records seven elements: the directory structure, the filename convention, the metadata schema, the index schema, the context-manifest schema, the authority and status vocabulary, and the canon-ownership rules. Each element is grounded in specific master-spec lines and reconciled against the Phase 01 audit (`migration/repository-audit.md`) and draft map (`migration/migration-map.md`). The orchestrator is the sole writer of this file; the five schema sections were drafted by read-only inspector agents (Tasks A through E) and verified by the orchestrator against the cited spec lines before assembly.

## 1. Directory structure and filename conventions

The target tree below is the master spec Phase 2 structure (spec lines 92 to 285) confirmed against the Phase 01 audit. Every top-level node from the spec is preserved. The few additions are justified item by item under "Deviations from the spec tree", each anchored to a Phase 01 audit finding; nothing in the spec tree was removed or renamed.

This phase decides shape only. Per spec line 287, no empty file is created merely to satisfy the tree; folders and files are created only where existing content or an immediate workflow need justifies them. Two domains (`docs/50-manuscript/` and `docs/70-research/`) are therefore created but intentionally left empty, as noted below.

### Final proposed directory tree

```text
the-unnecessary/
├── README.md                         # added: root readme (Phase 03)
├── CLAUDE.md                         # stays at root, updated in place later (audit doc 11)
├── project-status.md                 # added: root status artifact (later phase)
│
├── docs/
│   ├── _templates/                   # added: migration scaffolding (Phase 02); see distinction note
│   │   ├── active-document-template.md
│   │   └── context-manifest-template.yaml
│   │
│   ├── 00-governance/
│   │   ├── index.md
│   │   ├── canon-hierarchy.md
│   │   ├── novel-development-guide.md
│   │   ├── context-loading-guide.md
│   │   ├── memory-conventions.md      # added (RECOMMENDED, pending confirmation), audit doc 12 / section 10
│   │   ├── _templates/                # added: Phase 03-owned
│   │   │   └── index-template.md
│   │   └── decision-log/
│   │       ├── index.md
│   │       └── decisions/
│   │
│   ├── 10-vision/
│   │   ├── index.md
│   │   ├── narrative-brief.md
│   │   └── style/
│   │       ├── index.md
│   │       ├── core-prose.md
│   │       ├── viewpoint.md
│   │       ├── dialogue.md
│   │       ├── character-voices.md
│   │       ├── ai-dialogue.md
│   │       ├── technology-in-prose.md
│   │       ├── pacing-and-structure.md
│   │       ├── formatting.md
│   │       └── prohibited-patterns.md
│   │
│   ├── 20-canon/
│   │   ├── index.md
│   │   │
│   │   ├── world/
│   │   │   ├── index.md
│   │   │   ├── core-premise.md
│   │   │   ├── social-structure.md
│   │   │   ├── infrastructure-decline.md
│   │   │   ├── protected-enclaves.md
│   │   │   ├── mars-and-aurelia.md
│   │   │   ├── government-and-corporations.md
│   │   │   ├── themes-and-questions.md
│   │   │   └── locations/
│   │   │       ├── index.md
│   │   │       ├── greater-detroit.md
│   │   │       ├── elis-neighborhood.md
│   │   │       ├── lakeward.md
│   │   │       ├── northglass.md
│   │   │       └── mars-sites.md
│   │   │
│   │   ├── characters/
│   │   │   ├── index.md
│   │   │   ├── relationship-map.md
│   │   │   ├── viewpoint-rules.md
│   │   │   └── profiles/
│   │   │       ├── eli-rook.md
│   │   │       ├── jonah-mercer.md
│   │   │       ├── adrian-kade.md
│   │   │       ├── lena-okafor.md
│   │   │       ├── june-park.md
│   │   │       ├── mara-voss.md
│   │   │       ├── talia-reed.md
│   │   │       ├── nolan-avery.md
│   │   │       ├── sera-vale.md
│   │   │       ├── celeste-mercer.md
│   │   │       ├── nora-bell.md
│   │   │       ├── morrow.md
│   │   │       └── crown.md
│   │   │
│   │   ├── technology/
│   │   │   ├── index.md
│   │   │   ├── foundational-rules.md
│   │   │   ├── ai/
│   │   │   │   ├── index.md
│   │   │   │   ├── intelligence-levels.md
│   │   │   │   ├── crown.md
│   │   │   │   ├── morrow.md
│   │   │   │   ├── crown-vs-morrow.md
│   │   │   │   └── consciousness-and-personhood.md
│   │   │   ├── infrastructure/
│   │   │   │   ├── energy.md
│   │   │   │   ├── communications.md
│   │   │   │   ├── cloud-dependency.md
│   │   │   │   ├── identity-and-money.md
│   │   │   │   └── community-infrastructure.md
│   │   │   ├── robotics-and-manufacturing.md
│   │   │   ├── medicine.md
│   │   │   ├── transportation.md
│   │   │   ├── security-and-conflict.md
│   │   │   ├── mars-technology.md
│   │   │   ├── hard-plot-restrictions.md
│   │   │   └── failure-rules.md
│   │   │
│   │   └── timeline/
│   │       ├── index.md
│   │       ├── character-birth-dates.md
│   │       ├── historical/
│   │       │   ├── 2026-2034-assistance-and-compression.md
│   │       │   ├── 2035-2041-autonomy-and-labor-break.md
│   │       │   ├── 2042-2047-infrastructure-and-support-collapse.md
│   │       │   └── 2048-2052-preservation-years.md
│   │       └── book-1/
│   │           ├── index.md
│   │           ├── pre-book-2053.md
│   │           ├── act-1-timeline.md
│   │           ├── act-2-timeline.md
│   │           ├── act-3-timeline.md
│   │           ├── act-4-timeline.md
│   │           ├── character-knowledge-timeline.md
│   │           └── secret-timeline.md
│   │
│   ├── 30-plot/
│   │   └── book-1/
│   │       ├── index.md
│   │       ├── story-spine.md
│   │       ├── major-beats.md
│   │       ├── subplot-map.md
│   │       ├── reveal-management.md
│   │       ├── act-1.md
│   │       ├── act-2.md
│   │       ├── act-3.md
│   │       ├── act-4.md
│   │       └── chapters/
│   │           ├── index.md
│   │           ├── chapter-01.md
│   │           ├── chapter-02.md
│   │           └── ...                # through chapter-36.md
│   │
│   ├── 40-blueprints/
│   │   ├── _templates/                # canonical blueprint template (distinct from docs/_templates/)
│   │   │   └── chapter-blueprint-template.md
│   │   └── book-1/
│   │       ├── index.md
│   │       └── chapter-01-no-signal/
│   │           ├── blueprint.md
│   │           ├── context-manifest.yaml
│   │           ├── notes.md
│   │           └── revision-log.md
│   │
│   ├── 50-manuscript/                 # created empty; no approved chapter exists yet (audit / migration-map sec 3)
│   │   └── book-1/
│   │       ├── index.md
│   │       └── chapter-01-no-signal.md
│   │
│   ├── 60-continuity/
│   │   ├── index.md
│   │   ├── global-continuity.md
│   │   ├── character-states/
│   │   ├── relationships/
│   │   ├── locations/
│   │   ├── technology-state/
│   │   ├── knowledge-state/
│   │   ├── resources-and-injuries.md
│   │   ├── setups-and-payoffs.md
│   │   └── unresolved-threads.md
│   │
│   └── 70-research/                   # created empty; no research material exists yet (audit / migration-map sec 3)
│       ├── index.md
│       ├── plausibility-ledger.md
│       ├── sources.md
│       └── topics/
│
├── context-manifests/
│   ├── index.md
│   ├── create-chapter-blueprint.yaml
│   ├── draft-chapter.yaml
│   ├── revise-chapter.yaml
│   ├── continuity-check.yaml
│   ├── character-development.yaml
│   ├── technology-research.yaml
│   └── canon-revision.yaml
│
├── scripts/
│   ├── build-context-pack.py
│   ├── validate-links.py
│   ├── validate-metadata.py
│   └── check-duplicate-headings.py
│
├── .context/
│   └── generated context packs        # gitignored; created on demand, not scaffolded into git
│
├── migration/
│   ├── repository-audit.md
│   ├── migration-map.md
│   ├── conflicts-found.md
│   ├── target-architecture.md         # this document
│   ├── validation-report.md           # added: Phase 08 added artifact
│   └── final-report.md
│
└── archive/
    ├── source-monoliths/
    ├── superseded/
    ├── rejected/
    └── retired-drafts/
```

### Deviations from the spec tree (each justified by a Phase 01 audit finding)

The spec tree is the baseline. The following are additions only; no spec node was dropped or renamed. Items marked RECOMMENDED need human confirmation (see section 6).

| Added node | Justification (Phase 01 audit anchor) | Status |
|---|---|---|
| `docs/00-governance/memory-conventions.md` | The audit discovered `Memory Conventions.md` at root (audit section 2; doc 12 in the per-document table). The master spec tree enumerates no slot for it (audit section 10). Orchestrator recommendation is the governance folder; the alternative is keeping it at root next to `CLAUDE.md`. | RECOMMENDED, pending confirmation |
| `docs/00-governance/_templates/index-template.md` | The reusable index template is owned by Phase 03 (per the runbook); Phase 02 documents the index schema in prose only and does not create this file. Shown for tree completeness. | Added, Phase 03-owned |
| `README.md` (root) | New artifact created in Phase 03; already listed in the spec tree at line 94. | Added, later phase |
| `project-status.md` (root) | New artifact created in a later phase (spec Phase 14); already listed in the spec tree at line 96. | Added, later phase |
| `docs/_templates/active-document-template.md`, `docs/_templates/context-manifest-template.yaml` | Phase 02 migration scaffolding, placeholder-only stubs. Distinct from any canon template (see distinction note). Justified by Phase 02 runbook Allowed Changes. | Added, Phase 02 scaffolding |
| `migration/validation-report.md` | Added artifact produced by Phase 08; recorded so the `migration/` node is complete. | Added, Phase 08 |
| `docs/50-manuscript/` and `docs/70-research/` created empty | The audit confirmed both manuscript chapters and research files are absent (audit section 1); migration-map section 3 defers both. Per spec line 287, no placeholder canon is created; these domains are scaffolded as empty directories only. | Created empty, deferred fill |

### Distinction: blueprint template versus migration scaffolding templates versus index template

Three unrelated `_templates/` locations exist and must not be confused.

- `docs/40-blueprints/_templates/chapter-blueprint-template.md` is the CANONICAL chapter blueprint template, a live reusable per-chapter scaffold present in the spec tree (lines 222 to 223) and confirmed by the audit (doc 10, relocate-intact from `chapter-blueprints/Chapter Blueprint Template.md`; spec validation requires it remain intact). Owned by the blueprint phase, not Phase 02.
- `docs/_templates/` holds Phase 02 MIGRATION SCAFFOLDING only: `active-document-template.md` (the front-matter schema with placeholder fields) and `context-manifest-template.yaml` (the manifest schema with placeholder keys). Placeholder-only stubs with zero canon content.
- `docs/00-governance/_templates/index-template.md` is the reusable INDEX template, owned by Phase 03. Phase 02 documents the index schema in prose only and emits no index-template stub.

Three separate `_templates/` directories, three separate owners.

### Filename convention: lowercase kebab-case

All filenames and directory names use lowercase kebab-case: words lowercased, separated by single hyphens, no spaces, no underscores (except the reserved `_templates/` infrastructure name and dotfiles like `.context/`), no capitals, and no special characters. This is the convention the spec tree applies uniformly across every leaf (spec lines 92 to 285).

Concrete examples drawn directly from the target tree:

- `eli-rook.md`, a character profile under `docs/20-canon/characters/profiles/` (spec line 148).
- `crown-vs-morrow.md`, a comparison file under `docs/20-canon/technology/ai/` (spec line 170).
- `2042-2047-infrastructure-and-support-collapse.md`, a historical-era timeline file under `docs/20-canon/timeline/historical/` (spec line 192).
- `001-central-threat-is-economic-irrelevance.md`, a per-decision file pattern `NNN-slug.md` under `docs/00-governance/decision-log/decisions/` (the 44-decision split, migration-map section 2.7; the zero-padded three-digit ordinal preserves decision order).

## 2. Metadata schema (YAML front matter)

Active documents carry a concise block of YAML front matter at the top of the file, fenced by `---` delimiters (spec lines 289 to 296, 315). Phase 3 names exactly eight required fields and shows several optional fields in its worked example. The spec instructs that front matter be added "where appropriate" and warns against fabricating history (spec lines 291, 331), so optional fields are recorded only when their values are already known.

### Field table

The eight required fields are listed verbatim at spec lines 318 to 327. Optional fields below appear in the spec's example block (spec lines 295 to 316) but are absent from the required-field list.

| Field | Required | Value type | Example |
|---|---|---|---|
| `title` | yes | quoted string | `"Elias Rook"` |
| `document_type` | yes | quoted string (kebab-case) | `"character-profile"` |
| `status` | yes | quoted string from the controlled status vocabulary (section 4) | `"active-canon"` |
| `authority` | yes | quoted string from the controlled authority vocabulary (section 4) | `"character-canon"` |
| `summary` | yes | quoted string, one sentence | `"Canonical profile, motives, history, voice, secrets, and arc for Eli Rook."` |
| `tags` | yes | list of bare strings | `character`, `protagonist`, `viewpoint`, `asterion` |
| `related` | yes | list of quoted relative paths | `"../relationship-map.md"`, `"../../technology/ai/morrow.md"` |
| `source_documents` | yes | list of quoted paths into the archived monolith(s) | `"archive/source-monoliths/character-bible.md"` |
| `version` | no | quoted string (semantic) | `"1.0"` |
| `scope` | no | quoted string | `"book-1"` |
| `last_reviewed` | no | quoted ISO date string | `"YYYY-MM-DD"` |

### Path-shaped and vocabulary-controlled fields

- `status` and `authority` draw their permitted values from the controlled vocabularies in section 4 (literal example values `active-canon` at spec line 299 and `character-canon` at spec line 302).
- `related` must use valid relative paths, resolved relative to the document's own location, not the repository root (spec line 329; examples at lines 310 to 311).
- `source_documents` is a list pointing at the archived monolith path(s) the active document was derived from (example `archive/source-monoliths/character-bible.md`, spec line 313). A single split file may draw from more than one source monolith.

### Worked example (character profile)

This block reproduces the spec's example shape (spec lines 295 to 316):

```yaml
---
title: "Elias Rook"
document_type: "character-profile"
status: "active-canon"
version: "1.0"
scope: "book-1"
authority: "character-canon"
summary: "Canonical profile, motives, history, voice, secrets, and arc for Eli Rook."
tags:
  - character
  - protagonist
  - viewpoint
  - asterion
related:
  - "../relationship-map.md"
  - "../../technology/ai/morrow.md"
source_documents:
  - "archive/source-monoliths/character-bible.md"
last_reviewed: "YYYY-MM-DD"
---
```

### Versioning and review-date discipline

The optional `version` and `last_reviewed` fields are preserved where their values are already known and are never invented (spec line 331: "Do not invent version history that did not exist. Preserve known version information where available."). The placeholder `"YYYY-MM-DD"` is a template, not a value to guess; a real `last_reviewed` date is written only when a genuine review date is on record.

## 3. Index schema and context-manifest schema

This section fixes the shape of two recurring artifact types: the `index.md` that fronts a directory, and the YAML context manifest that scopes a task's file load. Both are derived from master spec Phase 5 (lines 494 to 521) and Phase 6 (lines 523 to 597). Phase 02 writes no real index and no real manifest; populating them is later-phase work.

### Index schema

The spec requires an `index.md` in every directory containing more than three meaningful files (spec line 496). An index is a navigation aid: it summarizes and links to the authority files in its directory and must never become a replacement canon document (spec line 521). Phase 02 documents this schema in prose only and emits NO index-template stub; the single reusable index template lives at `docs/00-governance/_templates/index-template.md` and is owned by Phase 03.

Every `index.md` must contain all seven required elements (spec lines 498 to 506):

1. The purpose of the directory.
2. Which file should be read first.
3. A table of files.
4. A one or two sentence summary of each file.
5. Authority or status.
6. The common tasks that require each file.
7. Links to related indexes.

Governing rule: an index summarizes and links to the authority file; it is a pointer, never the source. When a fact and its index summary disagree, the linked authority file wins (the prose form of spec line 43 and 521).

Labeled skeleton (reference only, not a stub to be written):

```markdown
# [Directory Name] Index

[element 1: one short paragraph stating the purpose of this directory]

[element 2: read-first pointer, for example "Read first: <file>"]

| File | Summary | Authority or status | Load when |
| ---- | ------- | ------------------- | --------- |
| [link to file] | [element 4: one or two sentence summary] | [element 5: authority or status] | [element 6: common tasks that require this file] |

[element 7: links to related indexes]
```

Element 3 is satisfied by the table itself; elements 4, 5, 6 by its per-row columns; elements 1, 2, 7 by the surrounding lines. Column layout may vary (the spec example at lines 510 to 519 uses extra role and viewpoint columns); the required minimum is the seven elements above.

### Context-manifest schema

YAML manifests live in `context-manifests/` (spec line 525). Each manifest scopes one task by naming exactly which files to load, in what order, and with which constraints, so an agent loads a bounded relevant set rather than the whole repository. Every manifest must identify all nine required fields (spec lines 529 to 537):

1. Task name.
2. Purpose.
3. Required files.
4. Optional files.
5. Files to exclude.
6. Loading order.
7. Expected output.
8. Canon rules.
9. Relevant validation checks.

Reference-existing-files rule: a manifest references only files that exist when it is written. Any optional or possibly-absent path (for example anything under `docs/70-research/**`, spec lines 249 to 253) goes under `optional_files`, never `required_files`, so validators do not fail on a legitimately absent path. `required_files` is the hard contract (a missing entry blocks the task); `optional_files` is best-effort; `exclude_files` names paths the agent must not load even when relevant (the spec's anti-over-load discipline at lines 557 and 584). The `relevant_validation_checks` field references the existing scripts (`scripts/validate-links.py`, `scripts/validate-metadata.py`, `scripts/check-duplicate-headings.py`) by name.

Labeled YAML skeleton (placeholder keys only; not a real manifest):

```yaml
# Context manifest schema (placeholder keys only; not a real manifest)
task_name:            # field 1: short identifier, for example create-chapter-blueprint
purpose:              # field 2: one or two sentences on what this task does and why
required_files:       # field 3: files that MUST exist and load; a missing entry blocks the task
  - <existing-path>
optional_files:       # field 4: load if present; absent is acceptable and must not fail validation
  - <existing-or-absent-path>   # docs/70-research/** entries belong here
exclude_files:        # field 5: paths the agent must NOT load even when they look relevant
  - <path-to-suppress>
loading_order:        # field 6: the order in which the above files should be loaded
  - <path-in-load-order>
expected_output:      # field 7: what the task should produce, for example a blueprint or a draft chapter
canon_rules:          # field 8: the canon and authority constraints the task must respect
relevant_validation_checks:   # field 9: checks the result should satisfy; reference existing scripts by name
  - <validation-check-name>
```

The root task manifests (`context-manifests/*.yaml`) and the per-chapter manifests (`docs/40-blueprints/book-1/chapter-XX/context-manifest.yaml`, spec line 228 and Phase 7) share this same nine-field schema. Both scopes exist by design (see section 6).

## 4. Authority and status vocabulary (controlled enums)

Three closed enums for the YAML front matter (`status`, `authority`, `document_type`). Each value is grounded in the spec tree (lines 95 to 285) or the Phase 3 example (lines 297 to 303). The enums are closed: each active document carries exactly one value from each, and `validate-metadata.py` (spec line 268) should reject any off-list value. The exact spellings are flagged for human confirmation in section 6, because the validator binds to them. This phase fixes vocabulary only; binding specific files to specific values is later-phase work.

The load-bearing distinction is the three-way life state the spec draws repeatedly: active canon (authoritative established fact, by subject), approved plans (plot and blueprints, not yet established events; spec lines 207 to 230, 648), and archived material (never treated as canon; spec lines 40, 282 to 284, 649).

### Enum 1: `status`

| Value | Meaning |
| --- | --- |
| `active-canon` | Authoritative established story fact, by subject; outranks plans and memory. Applies to `docs/20-canon/**` and approved manuscript (spec lines 646 to 647; literal example line 299). |
| `active-plan` | Approved plan that is not yet an established event: plot files and blueprints. Authoritative as intent, not as fact (spec lines 648, 204 to 230). |
| `active-support` | Operational or supporting active document that is neither story canon nor a plan: indexes, continuity files, research, context manifests (spec lines 237 to 263). |
| `active` | Process and operational governance docs that are live but not story canon: `CLAUDE.md`, the development guide, context-loading and canon-hierarchy guides, memory-conventions (spec lines 95, 102 to 103, 643). Deliberately NOT `active-canon`. |
| `draft` | Work in progress not yet approved as canon or as an approved plan (implied by the active-versus-approved distinction, spec lines 646 to 648). |
| `superseded` | Replaced by a newer authoritative version; retained for history in `archive/superseded/`, never treated as active canon (spec lines 282, 40). |
| `archived` | Retired source material kept only for provenance: source monoliths, rejected drafts, retired drafts. Never active canon (spec lines 280 to 284, 40, 649). |

### Enum 2: `authority` (maps one-to-one to a docs/ domain)

| Value | Meaning | docs/ domain |
| --- | --- | --- |
| `world-canon` | Authoritative world, setting, social structure, and locations facts. | `docs/20-canon/world/` |
| `character-canon` | Authoritative character profiles, relationships, viewpoint rules (literal example, line 302). | `docs/20-canon/characters/` |
| `technology-canon` | Authoritative technology and AI rules and restrictions. | `docs/20-canon/technology/` |
| `timeline-canon` | Authoritative chronology: historical eras and book-1 act timelines. | `docs/20-canon/timeline/` |
| `plot-plan` | Approved plot structure (spine, beats, acts, chapter map). Plan authority, not established fact. | `docs/30-plot/` |
| `blueprint` | Approved per-chapter blueprints and their template. Plan authority. | `docs/40-blueprints/` |
| `manuscript` | Approved drafted prose, treated as established canon once approved. | `docs/50-manuscript/` |
| `style-rule` | Authoritative prose, voice, dialogue, and formatting rules. | `docs/10-vision/style/` |
| `vision` | The narrative brief: short, read-first framing of the project. | `docs/10-vision/narrative-brief.md` |
| `continuity` | Tracked running state across chapters. | `docs/60-continuity/` |
| `research` | Plausibility ledger, sources, research topics; supports canon but is not canon. | `docs/70-research/` |
| `governance` | Process and operational rules: canon hierarchy, development guide, context-loading guide, decision log, memory-conventions, root `CLAUDE.md`. NOT story canon. | `docs/00-governance/` and root `CLAUDE.md` |

### Enum 3: `document_type` (structural kind, independent of subject)

| Value | Meaning |
| --- | --- |
| `narrative-brief` | The single read-first vision document. |
| `story-bible-section` | A world or premise canon section split from the Story Bible. |
| `character-profile` | A single character's canonical profile (literal example, line 298). |
| `relationship-map` | The cross-character relationship map. |
| `viewpoint-rules` | Viewpoint and POV rules document. |
| `technology-rule` | A technology, AI, or infrastructure rules document. |
| `timeline-period` | A historical era or act-level timeline document. |
| `plot-act` | An act-level plot document. |
| `plot-chapter` | A per-chapter plot or chapter-map entry. |
| `plot-structure` | Story spine, major beats, subplot map, or reveal management. |
| `blueprint` | A per-chapter blueprint document. |
| `blueprint-template` | The reusable chapter-blueprint template. |
| `manuscript-chapter` | A drafted prose chapter. |
| `style-guide` | A prose, voice, dialogue, or formatting style document. |
| `continuity-file` | A continuity-tracking document. |
| `research-note` | A research, plausibility, or sources document. |
| `governance-guide` | A process or canon-hierarchy governance document. |
| `decision` | A single decision-log entry. |
| `index` | An index file that points to authoritative siblings (line 43). |
| `context-manifest` | A YAML context manifest. |
| `project-status` | The root project-status document. |

The three enums are orthogonal and combine: a character profile is `document_type: character-profile`, `authority: character-canon`, `status: active-canon`, matching the literal example at spec lines 298 to 302.

## 5. Canon-ownership and anti-duplication rules

Each canon fact has exactly one owning domain. Every other file that needs that fact links to the owner rather than copying it. This is the load-bearing rule that keeps the split tree from drifting back into the monolith problem: one place to update, one authority to cite. Reproduced from master-spec Phase 12 (lines 768 to 789), reinforced by the global anti-duplication and index-authority principles at lines 42 to 43.

### Domain-ownership table

| Fact type | Single owning domain | How other domains reference it |
|---|---|---|
| Character facts (identity, motives, history, voice, secrets, arc) | character profiles (`docs/20-canon/characters/`) | link to the character profile; do not restate |
| Technology capabilities (architecture, what a system can do) | technology files (`docs/20-canon/technology/`) | link to the technology file; do not restate |
| Dates (when events occur) | timeline files (`docs/20-canon/timeline/`) | link to the timeline file; do not restate |
| Chapter order (sequence of chapters) | plot files (`docs/30-plot/`) | link to the plot file; do not restate |
| Scene-level facts (what is true inside a given scene) | blueprints (planned) and continuity (established after approval) | link to the blueprint or continuity file; do not restate |
| Prose rules (voice, mechanics, style conventions) | style files (`docs/10-vision/style/`) | link to the style file; do not restate |
| Reasons behind decisions (rationale, trade-offs) | decision files (`docs/00-governance/decision-log/`) | link to the decision file; do not restate |

### Index rule and cross-domain rule

An index summarizes; it does not own. Index summaries stay short and link to the authority file for details (spec line 779), clearly identifying the linked file as the authority (spec line 43). When a concept crosses domains, use links rather than duplicating full sections (spec line 781); the mechanism is the file's `related` reference list (spec lines 309 to 311).

### Worked example: Morrow (and the rule for cross-domain entities)

The Story Bible's Morrow overview summarizes Morrow's role and links to its owners rather than reproducing them (spec lines 783 to 789): the character profile for behavioral identity, the technology file for architecture and capabilities, and the plot files for Book One progression.

A cross-domain entity such as Morrow or Crown is governed by all the ownership rules at once, with one primary owner per fact type. There are not two copies of Morrow. The spec tree intentionally places `morrow.md` and `crown.md` in BOTH `docs/20-canon/characters/profiles/` (spec lines 159 to 160) and `docs/20-canon/technology/ai/` (spec lines 168 to 169): the character file owns behavioral identity, the technology file owns architecture and capabilities, the plot files own progression, and the Story Bible overview links to all three. Split the entity by fact type, give each fact type to its rightful owner, and link the pieces; never duplicate.

## 6. Orchestrator decisions and items for human confirmation

The agents flagged decisions that the orchestrator reserves. The orchestrator has ruled on the ones below that do not change exact tooling-bound strings, and has held the rest for human confirmation because later phases bind to those strings.

### Ruled by the orchestrator (binding unless a human overrides)

- Morrow and Crown dual placement is spec-sanctioned and correct: one statement per fact type (behavior in the character profile, architecture in the technology file, progression in plot), Story Bible overview links to all three, zero duplicate copies. (Section 5.)
- Decision filenames use the zero-padded three-digit ordinal pattern `NNN-slug.md` (`001` not `1`) for stable sort order.
- Manifest scopes: the root `context-manifests/*.yaml` task manifests and the per-chapter `docs/40-blueprints/book-1/chapter-XX/context-manifest.yaml` manifests share the one nine-field schema; both exist by design.
- YAML quoting follows the spec example exactly: `tags` are bare strings, string values and paths are quoted.
- `version`, `scope`, and `last_reviewed` are optional, preserved where known, and never invented.
- Process and operational governance docs (`CLAUDE.md`, the development guide, `memory-conventions`, context-loading and canon-hierarchy guides) carry `authority: governance` and `status: active`, never `active-canon`, since they govern process rather than story facts.

### Decided by the orchestrator (user delegated these calls; binding for the migration)

- Memory Conventions.md relocates to `docs/00-governance/memory-conventions.md` (it is process governance, grouped with the development guide and canon hierarchy). The move happens in a later phase; the destination is fixed.
- The `status`, `authority`, and `document_type` enums in section 4 are adopted as written. Later phases bind front matter and `validate-metadata.py` to these exact strings.
- The four-way active-status split (`active-canon` / `active-plan` / `active-support` / `active`) is adopted.

These were originally held for human confirmation; the user delegated all remaining migration decisions to the orchestrator, so they are now settled. The path convention is also fixed: `related` paths are document-relative (resolved from the file's own location), while `source_documents` paths are repository-root-relative (matching the spec's `archive/source-monoliths/...` example). The validators bind to that convention.
