You are reorganizing an existing novel-development repository for **The Unnecessary**.

Your job is to refactor the project’s Markdown documentation into a structure that is easier for an LLM to navigate selectively while creating chapter blueprints, drafting manuscript chapters, checking continuity, researching technical questions, and revising canon.

You have permission to create folders, split files, rename files, move files, create indexes, write support scripts, and update internal links.

Do not rewrite the story, change canon, improve plot decisions, or invent missing content during this task.

The goal is **context efficiency, discoverability, and canon safety**.

# Primary Objectives

1. Break large documents into smaller, semantically focused files.
2. Make it possible to load only the files relevant to the current task.
3. Preserve a clear hierarchy between canon, planning, manuscript, continuity, and research.
4. Prevent duplicate or conflicting sources of truth.
5. Create indexes that help an LLM identify which files it needs.
6. Create task-specific context manifests for common workflows.
7. Preserve all existing content and Mermaid diagrams.
8. Make the repository understandable without access to the conversation that created it.
9. Create safeguards so future LLMs do not silently alter canon.
10. Leave the project ready to begin the Chapter 1 blueprint.

# Important Operating Rules

- Inspect the entire repository before moving or editing anything.
- Do not assume filenames or folder locations before inspecting them.
- Do not stop after proposing a plan. Perform the reorganization.
- Preserve all meaningful existing content.
- Do not paraphrase canonical prose merely to shorten it.
- Do not silently merge conflicting facts.
- If two files conflict, preserve both statements, flag the conflict, and record it in a migration report.
- Do not delete original source documents.
- Move original monolithic documents into an archive after their content has been safely split and verified.
- Use lowercase kebab-case filenames.
- Avoid em dashes in any new prose you write.
- Preserve existing document titles, version information, status labels, tables, code blocks, and Mermaid diagrams.
- Update all relative Markdown links after moving files.
- Do not place generated context bundles in active canon folders.
- Do not treat archived documents as active canon.
- Use Git history if available, but do not rely on Git as the only backup.
- Do not create unnecessary duplication between files.
- An index may summarize another file, but the index must clearly identify the linked file as the authority for details.

# Phase 1: Audit the Existing Repository

Before changing files:

1. Recursively inspect all Markdown files and relevant folders.
2. Identify the current versions of:
   - Narrative Brief
   - Story Bible
   - Character Bible
   - World and Technology Rules
   - Master Timeline
   - Plot Outline and Chapter Map
   - Chapter Blueprint Template
   - Novel Development and Canon Guide
   - Creative Decision Log
   - Style Guide
   - Any existing blueprints
   - Any manuscript chapters
   - Any continuity documents
   - Any research files

3. Identify duplicate, obsolete, partial, or superseded versions.
4. Identify broken links.
5. Identify information repeated across several documents.
6. Identify sections that can be split safely without losing meaning.
7. Record the audit in:

```text
migration/repository-audit.md
```

The audit should contain:

- Existing file tree
- Document title
- Current path
- Apparent version
- Canon status
- Approximate subject
- Recommended destination
- Whether the file should be split
- Any conflicts or ambiguities discovered

# Phase 2: Create the Target Structure

Use the following structure as the preferred target. Adapt it only when the existing repository clearly requires a better variation.

```text
the-unnecessary/
├── README.md
├── CLAUDE.md
├── project-status.md
│
├── docs/
│   ├── 00-governance/
│   │   ├── index.md
│   │   ├── canon-hierarchy.md
│   │   ├── novel-development-guide.md
│   │   ├── context-loading-guide.md
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
│   │           └── ...
│   │
│   ├── 40-blueprints/
│   │   ├── _templates/
│   │   │   └── chapter-blueprint-template.md
│   │   └── book-1/
│   │       ├── index.md
│   │       └── chapter-01-no-signal/
│   │           ├── blueprint.md
│   │           ├── context-manifest.yaml
│   │           ├── notes.md
│   │           └── revision-log.md
│   │
│   ├── 50-manuscript/
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
│   └── 70-research/
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
│   └── generated context packs
│
├── migration/
│   ├── repository-audit.md
│   ├── migration-map.md
│   ├── conflicts-found.md
│   └── final-report.md
│
└── archive/
    ├── source-monoliths/
    ├── superseded/
    ├── rejected/
    └── retired-drafts/
```

Do not create empty files merely to satisfy the tree. Create folders and files that are justified by existing content or immediate workflow needs.

# Phase 3: Add Standard Metadata

Add concise YAML front matter to active documents.

Use this shape where appropriate:

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

Metadata requirements:

- `title`
- `document_type`
- `status`
- `authority`
- `summary`
- `tags`
- `related`
- `source_documents`

Use valid relative paths in `related`.

Do not invent version history that did not exist. Preserve known version information where available.

# Phase 4: Split Documents by Semantic Responsibility

Split large files at natural conceptual boundaries.

## Narrative Brief

Keep the Narrative Brief mostly intact because it is meant to be short and read first.

If it is already manageable, do not split it unnecessarily.

## Story Bible

Split into:

- Core premise and narrative promise
- Central questions and themes
- Social structure
- Infrastructure decline
- Protected enclaves
- Mars and Aurelia
- Primary setting and locations
- Book One broad arc
- Series direction
- Consistency rules

Do not duplicate complete character profiles or technical rules here. Link to those authorities.

## Character Bible

Create one file per major or recurring character.

Each profile should retain:

- Basic information
- Appearance
- History
- Personality
- external goal
- internal need
- fear
- contradiction
- moral boundary
- secret
- false belief
- truth or needed growth
- Book One arc
- long-term arc
- speech pattern
- writing rules
- relationships

Move the relationship map and dialogue differentiation into their own shared files.

## World and Technology Rules

Split by system:

- AI foundations
- Crown
- Morrow
- Crown versus Morrow
- computing
- energy
- communications
- cloud dependency
- identity and access
- robotics
- transportation
- medicine
- manufacturing
- security
- conflict
- government technology
- protected enclaves
- community infrastructure
- Northglass
- Mars
- hard restrictions
- failure rules

Preserve any rule whose wording limits plot convenience.

## Master Timeline

Split by historical period and Book One act.

Keep:

- A timeline index
- A compact high-level chronology
- Links to detailed periods
- Character birth dates
- Knowledge and secret timelines
- Mermaid visualizations where useful

Do not duplicate detailed chapter summaries from the plot files.

## Plot Outline and Chapter Map

Create:

- Story spine
- Major structural beats
- One file per act
- One concise file per chapter containing the high-level plot-map entry
- Subplot map
- Reveal-management file
- Viewpoint distribution if not stored elsewhere

Chapter plot-map files must remain different from full chapter blueprints.

## Style Guide

Split into practical files that can be loaded independently:

- Core prose identity
- Point of view and narrative distance
- Dialogue
- Character voices
- Morrow and Crown dialogue
- Technology and exposition
- Emotion and moral content
- Pacing, openings, and endings
- Formatting
- Prohibited patterns and clichés
- Revision checklist

## Decision Log

Split each major decision into a separate file.

Use filenames such as:

```text
001-central-threat-is-economic-irrelevance.md
002-decline-through-withdrawal.md
003-recognizable-ordinary-world.md
```

Create an index table containing:

- Decision number
- Title
- Status
- Category
- Short summary
- File link

Keep rejected concepts easy to locate.

## Novel Development Guide

Keep the complete operating guide as an active governance document.

Create a shorter `context-loading-guide.md` derived from it that focuses only on:

- What to read for each task
- Authority hierarchy
- How to handle contradictions
- How to distinguish canon from planning

# Phase 5: Create Index Files

Every directory containing more than three meaningful files should have an `index.md`.

Each index must contain:

1. The purpose of the directory
2. Which file should be read first
3. A table of files
4. A one or two sentence summary of each file
5. Authority or status
6. Common tasks that require each file
7. Links to related indexes

Example:

```markdown
# Character Canon Index

Read this index before loading individual character profiles.

| Character   | Role            | Viewpoint | Load when                                            | File                               |
| ----------- | --------------- | --------: | ---------------------------------------------------- | ---------------------------------- |
| Eli Rook    | Protagonist     |       Yes | Any Eli chapter, Morrow creation, Asterion history   | [Profile](profiles/eli-rook.md)    |
| Lena Okafor | Clinic director |       Yes | Medical ethics, clinic scenes, Morrow accountability | [Profile](profiles/lena-okafor.md) |
```

Indexes should help an LLM select files. They should not become replacement canon documents.

# Phase 6: Create Task-Specific Context Manifests

Create YAML manifests in `context-manifests/`.

Each manifest should identify:

- Task name
- Purpose
- Required files
- Optional files
- Files to exclude
- Loading order
- Expected output
- Canon rules
- Relevant validation checks

## Blueprint Manifest

`create-chapter-blueprint.yaml` should require:

1. `CLAUDE.md`
2. Context-loading guide
3. Narrative Brief
4. Relevant plot chapter file
5. Relevant act file
6. Chapter Blueprint Template
7. Relevant character profiles
8. Relevant technology files
9. Relevant timeline files
10. Current continuity files
11. Previous chapter blueprint
12. Previous approved manuscript chapter, when one exists
13. Relevant decisions

It should not automatically load every character profile, every technology file, or every chapter.

## Drafting Manifest

`draft-chapter.yaml` should require:

1. Approved blueprint
2. Core prose guide
3. Viewpoint guide
4. Dialogue guide
5. Relevant character voices
6. Relevant character profiles
7. Relevant technology files
8. Current continuity
9. Previous approved manuscript chapter
10. Relevant plot-map entry

## Continuity Manifest

`continuity-check.yaml` should prioritize:

- Approved manuscript chapters
- Master timeline
- Knowledge states
- Character states
- Technology states
- Relationships
- Setups and payoffs

## Canon Revision Manifest

`canon-revision.yaml` should require:

- Narrative Brief
- Canon hierarchy
- Relevant canon files
- Decision Log index
- Relevant decisions
- Affected plot files
- Affected manuscript and continuity files

# Phase 7: Create Per-Chapter Context Manifests

For every active or soon-to-be-created chapter blueprint, create:

```text
docs/40-blueprints/book-1/chapter-XX-title/context-manifest.yaml
```

For Chapter 1, include only files relevant to Chapter 1.

The Chapter 1 context manifest should likely include:

- Narrative Brief
- Core Story Bible premise
- Infrastructure decline
- Greater Detroit
- Eli’s neighborhood
- Eli profile
- Lena profile
- Nolan profile
- Talia profile
- Relevant supporting relationship information
- Energy rules
- Communications rules
- Cloud dependency
- Medical technology rules
- Book One pre-story timeline
- Act One timeline
- Act One plot file
- Chapter 1 plot-map file
- Style files relevant to Eli, exposition, viewpoint, and openings
- Relevant decisions concerning setting, service withdrawal, Eli, tone, and style
- Chapter Blueprint Template

Do not include Mars technical details, Mara’s full profile, later-act timelines, or unrelated chapter files unless Chapter 1 directly needs them.

# Phase 8: Create CLAUDE.md

Create or update a root-level `CLAUDE.md`.

It should be concise enough to remain useful in every Claude Code session.

It should state:

- This is a novel project, not a software product.
- Read `docs/00-governance/context-loading-guide.md` before story work.
- Never load the whole repository by default.
- Start from the appropriate context manifest.
- Treat approved manuscript as established canon.
- Treat active canon files as authoritative by subject.
- Treat plot files and blueprints as approved plans, not already-established events.
- Never use archived files as active canon.
- Flag conflicts instead of silently resolving them.
- Do not change canon unless explicitly asked.
- Avoid em dashes in drafted prose.
- Preserve viewpoint and reveal timing.
- Update continuity after approved manuscript changes.
- Record major revisions in the Decision Log.
- Do not expose future reveals in earlier chapter work.
- Do not give Morrow or Crown unestablished capabilities.

Include a short task-routing table:

| Task                     | Start with                                        |
| ------------------------ | ------------------------------------------------- |
| Create chapter blueprint | `context-manifests/create-chapter-blueprint.yaml` |
| Draft chapter            | `context-manifests/draft-chapter.yaml`            |
| Revise chapter           | `context-manifests/revise-chapter.yaml`           |
| Check continuity         | `context-manifests/continuity-check.yaml`         |
| Revise canon             | `context-manifests/canon-revision.yaml`           |
| Research technology      | `context-manifests/technology-research.yaml`      |

# Phase 9: Create a Context Pack Builder

Create a simple script:

```text
scripts/build-context-pack.py
```

Use the Python standard library only unless the repository already has an established scripting environment.

The script should:

1. Accept a manifest path.
2. Read its ordered file list.
3. Verify that every required path exists.
4. Concatenate selected Markdown files into one generated Markdown context pack.
5. Insert a clear source heading before each file.
6. Preserve original content exactly.
7. Write generated packs under `.context/`.
8. Include generation time and manifest path.
9. Warn about missing optional files.
10. Fail on missing required files.
11. Refuse to load files from `archive/` unless explicitly included.
12. Support glob-free explicit paths by default.
13. Optionally support placeholders such as:
    - `{chapter_number}`
    - `{chapter_slug}`
    - `{previous_chapter_number}`

14. Print token or character estimates if practical without third-party dependencies.

Example command:

```bash
python scripts/build-context-pack.py \
  docs/40-blueprints/book-1/chapter-01-no-signal/context-manifest.yaml
```

If parsing YAML without dependencies is impractical, use JSON manifests instead, or implement a deliberately limited YAML parser supporting only this project’s schema.

Prefer reliability over cleverness.

Add `.context/` to `.gitignore` unless generated context packs should be committed.

# Phase 10: Add Validation Tools

Create lightweight validation scripts.

## Link Validator

`scripts/validate-links.py`

Check:

- Relative Markdown links
- Referenced files
- Index links
- Metadata `related` paths
- Source-document paths

## Metadata Validator

`scripts/validate-metadata.py`

Check active documents for required metadata fields.

## Duplicate Authority Check

Create a report that looks for repeated authoritative headings or duplicated long passages across active canon files.

Do not automatically delete duplicates. Report them.

## Archive Safety Check

Confirm no active index or context manifest includes archived material unless explicitly marked as historical reference.

# Phase 11: Preserve Source Monoliths

After splitting and validating a source file:

1. Copy or move the original complete document to:

```text
archive/source-monoliths/
```

2. Add an archive header containing:
   - Original title
   - Original path
   - Archive date
   - Replacement index
   - Canon status

3. Do not allow archived monoliths to appear in normal task context manifests.
4. Keep the active split files as the current authority.

Do not archive a source document until all of its meaningful sections have confirmed destinations.

# Phase 12: Avoid Canon Duplication

Use these rules:

- Character facts belong primarily in character profiles.
- Technology capabilities belong primarily in technology files.
- Dates belong primarily in timeline files.
- Chapter order belongs primarily in plot files.
- Scene-level facts belong in blueprints and continuity.
- Prose rules belong in style files.
- Reasons behind decisions belong in decision files.
- Index summaries should remain short and link to authority files.

When a concept crosses domains, use links rather than duplicating full sections.

Example:

The Story Bible’s Morrow overview should summarize Morrow’s role and link to:

- Character profile for Morrow’s behavioral identity
- Technology file for architecture and capabilities
- Plot files for Book One progression

# Phase 13: Create the Initial Continuity Structure

If no manuscript chapters are approved yet, create lightweight continuity files that clearly state:

> No manuscript chapters have been approved. These files contain pre-draft starting conditions only.

Create at minimum:

- Global starting conditions
- Character starting states
- Character knowledge states
- Relationship starting states
- Technology starting states
- Unresolved threads
- Setups and payoffs

Do not treat planned future events as already-established continuity.

# Phase 14: Create Project Status

Create or update `project-status.md`.

It should include:

```yaml
current_phase: "chapter blueprinting"
current_book: 1
current_chapter: 1
current_chapter_title: "No Signal"
current_blueprint_status: "not started"
current_manuscript_status: "not started"
last_approved_chapter: 0
continuity_updated_through: 0
next_task: "Create the Chapter 1 blueprint"
```

Also include:

- Active document versions
- Known unresolved conflicts
- Recommended context manifest for the next task
- Date of last project reorganization

# Phase 15: Create the Final Migration Report

Write:

```text
migration/final-report.md
```

Include:

1. Summary of changes
2. Old-to-new file map
3. Files split
4. Files archived
5. Files intentionally left intact
6. Indexes created
7. Context manifests created
8. Scripts created
9. Conflicts found
10. Duplicate content found
11. Broken links fixed
12. Validation results
13. Anything requiring human review
14. Recommended next command for generating the Chapter 1 context pack
15. Recommended next task

# Validation Requirements

Before considering the task complete:

- Confirm every active source section has a destination.
- Confirm no canonical section was lost.
- Compare source-monolith headings against split-file headings.
- Confirm Mermaid diagrams remain valid Markdown blocks.
- Confirm relative links work.
- Confirm context manifests reference existing files.
- Confirm archived files are excluded from normal context.
- Confirm active documents have status metadata.
- Confirm Character Bible material exists for every established character.
- Confirm all 36 chapter plot-map entries remain represented.
- Confirm the Chapter Blueprint Template remains intact.
- Confirm the Creative Decision Log remains fully represented.
- Confirm the Style Guide remains fully represented.
- Confirm the Novel Development and Canon Guide remains available.
- Confirm Chapter 1 can be planned without loading the entire repository.

# Desired End State

After this refactor, an LLM should be able to perform the following workflow:

1. Read `CLAUDE.md`.
2. Identify the current task from `project-status.md`.
3. Open the relevant context manifest.
4. Load only the selected indexes and source files.
5. Create or revise one chapter without loading unrelated canon.
6. Check conflicts against the correct authority.
7. Update continuity when prose is approved.
8. Record major changes in the Decision Log.
9. Continue the novel without access to the original development conversation.

# Final Constraint

Do not optimize only for a one-million-token context window.

Optimize for selective retrieval, stable authority, low duplication, and the ability to hand the project to a different capable LLM in the future.

A large context window is a safety margin, not a substitute for good information architecture.
