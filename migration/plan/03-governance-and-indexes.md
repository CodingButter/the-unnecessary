---
title: "phase-03-governance-and-indexes"
document_type: "migration-runbook"
phase: "03"
title_text: "Phase 03: Governance and Indexes"
depends_on:
  - "02"
status: "planned"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Phase 03: Governance and Indexes

> This runbook is subordinate to the master specification at `migration/REPOSITORY-REORGANIZATION-SPEC.md`. The master spec is authoritative. If anything in this runbook conflicts with the master spec, the master spec wins and this runbook must be corrected to match it.

## 1. Purpose

This phase establishes the governance layer and the index scaffolding that lets a future LLM navigate the reorganized repository selectively rather than loading everything. It is the connective tissue that sits above canon and tells a reader where to start, what authority a file carries, and how to resolve contradictions.

Concretely, when this phase is later executed it produces the per-session entry point (root `CLAUDE.md`), the task-routing logic, the canon authority hierarchy, the lean reading guide derived from the full development guide, the reusable index shape, the live project-status record, and the migration tracking files that remain current as later phases run.

This phase does NOT split canon, archive monoliths, or move story content. Phase 02 already created the empty target directory tree under `docs/` and the supporting top-level folders. Phase 03 fills the governance corner of that tree and seeds the index template that every later content phase will reuse. The actual splitting of the source monoliths into canon happens in later phases (Phase 04 onward in the execution plan), and archival of the source monoliths happens only in Phase 09.

## 2. Dependencies

- Phase 02 must be complete before this phase begins. Phase 02 establishes the target directory structure described in the master spec Phase 2 tree, including `docs/00-governance/`, `context-manifests/`, `scripts/`, `.context/`, `migration/`, and `archive/`.
- A git baseline commit and the Phase 02 checkpoint commit must both already exist. This phase ends with its own checkpoint commit before any later phase begins.
- No canon split is required as a precondition. The governance documents here describe the target architecture and reference paths that later phases will populate. Where this runbook references a canon path that does not yet exist (for example `docs/20-canon/characters/index.md`), the governance document should describe it as the intended authority and the path must be confirmed valid by the link validator only after later phases create it. Until then, the canon-hierarchy and context-loading-guide describe destinations by directory rather than asserting that leaf files already exist.

## 3. Inputs

Read-only inputs for this phase:

- `migration/REPOSITORY-REORGANIZATION-SPEC.md` sections:
  - Phase 8 (lines covering CLAUDE.md content and the task-routing table) for the root `CLAUDE.md`.
  - Phase 5 (Index Files requirements) for the index template shape and the seven required index elements.
  - Phase 4 "Novel Development Guide" subsection for deriving `context-loading-guide.md` from the full guide.
  - Phase 14 for the `project-status.md` shape and required fields.
  - Phase 2 for the exact target tree, used to confirm governance and migration paths.
  - Important Operating Rules (canon hierarchy, conflict handling, archive rules) feeding `canon-hierarchy.md`.
- `Development and Canon Guide.md` at the repo root. This is the source the shorter `context-loading-guide.md` is derived from. It defines the document responsibilities, the canon hierarchy, the canon versus planning distinction, the per-task reading guidance, and the contradiction-handling rules. Read it but do NOT modify, move, or archive it in this phase.
- The Phase 02 directory tree, to confirm that governance target folders exist before writing into them.

This phase writes ONLY to `docs/00-governance/`, the root `CLAUDE.md`, the root `README.md`, the root `project-status.md`, and `migration/` tracking files. It writes one index template under the governance tree. Phase 03 SEEDS the initial `project-status.md`; Phase 09 will later UPDATE (not overwrite) it. It reads other source monoliths only to confirm naming for cross-reference, never to copy canon content into governance files.

## 4. Allowed Changes

This phase MAY create or edit only the following concrete paths:

- `CLAUDE.md` (repo root) - create or update.
- `README.md` (repo root) - create. A concise project introduction that points to `CLAUDE.md` and `docs/00-governance/`.
- `docs/00-governance/context-loading-guide.md` - create.
- `docs/00-governance/canon-hierarchy.md` - create.
- `docs/00-governance/index.md` - create.
- `docs/00-governance/_templates/index-template.md` - create (the reusable per-directory index shape, lowercase kebab-case).
- `project-status.md` (repo root) - create or update.
- `migration/migration-map.md` - APPEND to or keep current only. Phase 01 is the sole author of the substantive source-to-destination map; Phase 03 must NOT create or re-seed it, only append governance entries to the map Phase 01 authored.
- `migration/conflicts-found.md` - APPEND to (never re-create) the ledger Phase 00 seeded.

All new filenames use lowercase kebab-case. All active governance documents created here carry YAML front matter per master spec Phase 3. The index template is a template, so it documents the front matter shape rather than asserting active-canon status for itself.

## 5. Prohibited Changes

This phase MUST NOT:

- Touch, move, rename, split, rewrite, or archive any source monolith. The originals stay exactly where they are at the repo root: `Narrative Brief.md`, `Story Bible.md`, `Character Bible.md`, `Technology Rules.md`, `Master Timeline.md`, `Plot Outline and Chapter Map.md`, `Style Guide.md`, `Creative Decision Log.md`, `Development and Canon Guide.md`, and `chapter-blueprints/Chapter Blueprint Template.md`. Archival of these is reserved for Phase 09 only.
- Create, edit, or populate any canon content under `docs/10-vision/`, `docs/20-canon/`, `docs/30-plot/`, `docs/40-blueprints/`, `docs/50-manuscript/`, `docs/60-continuity/`, or `docs/70-research/`. Those directories are filled by later phases. This phase may reference their intended paths from governance documents but must not write files into them.
- Create or edit `context-manifests/*.yaml` content. Manifests are a later phase. Governance documents may name the manifests as future entry points, and `CLAUDE.md` may include the task-routing table that points at them, but the manifest files themselves are not authored here.
- Create or edit `scripts/*` validation or build tooling. That is a later phase.
- Write anything into `archive/` or `.context/`.
- Resolve any canon conflict by editing canon. Conflicts are logged, not fixed, and only the orchestrator decides resolution.
- Add em dashes to any prose written in this phase.

If a needed change falls outside the Allowed Changes list, stop and escalate to the orchestrator rather than expanding scope.

## 6. Agent Delegation Plan

All tasks below are read-only against source material and write only to disjoint governance or migration files, so they can run in parallel. No two agents write to the same file. Shared-index reconciliation and final acceptance are reserved to the orchestrator (see section 7).

### Task A: Draft root CLAUDE.md

- Exact scope: Author the root `CLAUDE.md` per master spec Phase 8, including every required statement and the task-routing table.
- Inputs: master spec Phase 8.
- Expected output: `CLAUDE.md` at repo root with YAML front matter, the concise per-session guidance bullets (novel not software, read the context-loading guide first, never load the whole repo, start from a context manifest, treat approved manuscript as canon, treat plot and blueprints as plans not events, never use archived files as canon, flag conflicts rather than resolve them, do not change canon unless asked, avoid em dashes, preserve viewpoint and reveal timing, update continuity after approved changes, record major revisions in the decision log, do not expose future reveals, do not grant Morrow or Crown unestablished capabilities), and the six-row task-routing table mapping each task to its context manifest path.
- Read-only or may-edit: may-edit.
- Files it may touch: `CLAUDE.md` only.
- Files it must not touch: anything else.
- How the orchestrator verifies: read the diff; confirm every Phase 8 required statement is present, the routing table has all six rows with correct manifest paths, front matter is valid YAML, and there are no em dashes.

### Task A2: Author root README.md

- Exact scope: Author a concise root `README.md` that introduces the project and points readers to `CLAUDE.md` (the per-session entry point) and to `docs/00-governance/` (governance and navigation). Keep it brief: a short project intro and the two pointers, no canon content.
- Inputs: master spec for project framing; `CLAUDE.md` and `docs/00-governance/` paths as the targets to point at.
- Expected output: `README.md` at repo root, brief, pointing to `CLAUDE.md` and `docs/00-governance/`.
- Read-only or may-edit: may-edit.
- Files it may touch: `README.md` only.
- Files it must not touch: anything else.
- How the orchestrator verifies: read the diff; confirm the README is concise, names `CLAUDE.md` and `docs/00-governance/`, restates no canon, and has no em dashes.

### Task B: Derive context-loading-guide.md

- Exact scope: Produce `docs/00-governance/context-loading-guide.md` by deriving a short reading guide from `Development and Canon Guide.md` per master spec Phase 4, focused only on what to read per task, the authority hierarchy, how to handle contradictions, and how to distinguish canon from planning.
- Inputs: `Development and Canon Guide.md` (read-only), master spec Phase 4 subsection.
- Expected output: `docs/00-governance/context-loading-guide.md` with front matter, four sections matching the four required focuses. It links to the context manifests as the operational entry points and to `canon-hierarchy.md` as the authority reference. It summarizes and links; it does not copy the full guide.
- Read-only or may-edit: read-only against sources; may-edit only its own output file.
- Files it may touch: `docs/00-governance/context-loading-guide.md` only.
- Files it must not touch: `Development and Canon Guide.md`, any other source monolith, any canon directory.
- How the orchestrator verifies: read the diff; confirm the four required focuses are present and specific, that it derives rather than duplicates the full guide, that links resolve or are flagged as later-phase pending, and there are no em dashes.

### Task C: Draft canon-hierarchy.md

- Exact scope: Produce `docs/00-governance/canon-hierarchy.md` capturing the authority hierarchy and conflict-handling rules from the master spec Operating Rules and Phase 4, stating which document type is authoritative for which subject.
- Inputs: master spec Important Operating Rules and Phase 12 (canon duplication ownership rules), `Development and Canon Guide.md` (read-only) for hierarchy language.
- Expected output: `docs/00-governance/canon-hierarchy.md` with front matter, an explicit ranked hierarchy (approved manuscript as established canon, active canon files authoritative by subject, plot files and blueprints as approved plans not events, archived files never canon), per-domain ownership table (character facts to profiles, technology to technology files, dates to timeline, chapter order to plot, scene facts to blueprints and continuity, prose rules to style, decision rationale to decision files), and the rule that conflicts are flagged and preserved, never silently merged.
- Read-only or may-edit: read-only against sources; may-edit only its own output file.
- Files it may touch: `docs/00-governance/canon-hierarchy.md` only.
- Files it must not touch: any source monolith, any canon directory.
- How the orchestrator verifies: read the diff; confirm hierarchy ordering matches the master spec, the ownership table covers all domains in Phase 12, and conflict rule is present.

### Task D: Draft the index template

- Exact scope: Produce the reusable per-directory index shape at `docs/00-governance/_templates/index-template.md` per master spec Phase 5, capturing all seven required index elements as a fill-in template.
- Inputs: master spec Phase 5 (the seven required elements and the example table).
- Expected output: `docs/00-governance/_templates/index-template.md` containing placeholders for: directory purpose, which file to read first, a files table, a one or two sentence summary per file, authority or status, common tasks per file, and links to related indexes. It includes the example table layout from Phase 5 as a model. It is explicitly labeled a template and notes that an index summarizes but never replaces authority files.
- Read-only or may-edit: read-only against sources; may-edit only its own output file.
- Files it may touch: `docs/00-governance/_templates/index-template.md` only.
- Files it must not touch: any other index, any canon directory, any source monolith.
- How the orchestrator verifies: read the diff; confirm all seven Phase 5 elements appear as template fields and the no-replacement-canon caveat is present.

### Task E: Draft project-status.md

- Exact scope: SEED the initial `project-status.md` at repo root per master spec Phase 14. Phase 03 creates the initial record; Phase 09 will later UPDATE (not overwrite) it, preserving the active-document-versions and other content accumulated by intervening phases.
- Inputs: master spec Phase 14 (the YAML block and the additional required items).
- Expected output: `project-status.md` containing the Phase 14 YAML block verbatim in shape (current_phase chapter blueprinting, current_book 1, current_chapter 1, current_chapter_title No Signal, blueprint and manuscript statuses not started, last_approved_chapter 0, continuity_updated_through 0, next_task create the Chapter 1 blueprint) plus active document versions, known unresolved conflicts (cross-referencing `migration/conflicts-found.md`), the recommended context manifest for the next task, and the date of last project reorganization.
- Read-only or may-edit: may-edit.
- Files it may touch: `project-status.md` only.
- Files it must not touch: anything else.
- How the orchestrator verifies: read the diff; confirm all Phase 14 YAML fields and the four additional items are present and the values match the current project state.

### Task F: Append to migration tracking files

- Exact scope: APPEND to or keep current `migration/migration-map.md` and APPEND to (never re-create) `migration/conflicts-found.md`. Phase 01 is the sole author of the substantive source-to-destination map; Phase 03 must NOT create or re-seed it, only append the governance files now created to the map Phase 01 authored. Phase 00 seeded the conflicts ledger; Phase 03 only appends conflicts it discovers, never re-creating the ledger.
- Inputs: master spec Phase 2 tree, Phase 15 final-report fields (for the map columns), Important Operating Rules (conflict logging requirement), the existing `migration/migration-map.md` authored by Phase 01.
- Expected output: `migration/migration-map.md` updated in place with the governance files Phase 03 created appended to the map Phase 01 authored, leaving Phase 01's existing entries intact. `migration/conflicts-found.md` left as its Phase 00 empty-but-headed state unless Phase 03 discovers a conflict, in which case both sides are appended without re-creating the ledger.
- Read-only or may-edit: may-edit only these two files.
- Files it may touch: `migration/migration-map.md`, `migration/conflicts-found.md`.
- Files it must not touch: `migration/REPOSITORY-REORGANIZATION-SPEC.md`, `migration/repository-audit.md`, `migration/final-report.md`, any runbook other than as read-only reference, any source monolith.
- How the orchestrator verifies: read the diff; confirm Phase 01's existing map entries are preserved, Phase 03 only appended governance entries, and that the conflicts ledger was appended to rather than re-created (its Phase 00 header is intact).

### Task G: Draft governance index

- Exact scope: Produce `docs/00-governance/index.md` using the index template shape, indexing the governance directory contents.
- Inputs: the index template (Task D output) and the governance files created by Tasks B, C; master spec Phase 5.
- Expected output: `docs/00-governance/index.md` with directory purpose, first file to read, a files table covering `canon-hierarchy.md`, `context-loading-guide.md`, the decision-log subtree (referenced as later-phase), the development guide destination, authority and status, common tasks per file, and links to related indexes.
- Read-only or may-edit: may-edit only its own output file.
- Files it may touch: `docs/00-governance/index.md` only.
- Files it must not touch: any other index, the index template, any source monolith, any canon directory.
- How the orchestrator verifies: read the diff; confirm it follows the template, lists the governance files, and does not assert content for files not yet created (those are marked pending).

Coordination rule for parallel agents: no two of the tasks above write to the same file. Tasks B and C and G all read `Development and Canon Guide.md` but only read it. Task G depends on Tasks B, C, and D for accurate references, so run Task G after B, C, D land, or run it last and have the orchestrator reconcile. The orchestrator performs all shared-file reconciliation and is the only writer permitted to touch a file another agent also needs.

## 7. Orchestrator Responsibilities

Reserved to the main instance and not delegated:

- Final path choices: the orchestrator confirms the exact destination paths and filenames before agents write, resolving any ambiguity against the master spec Phase 2 tree.
- Canon-conflict resolution: any conflict surfaced while reading the development guide or other sources is appended by an agent to the `migration/conflicts-found.md` ledger Phase 00 seeded (never re-creating it) but resolved only by the orchestrator. Agents never edit canon to resolve a conflict.
- Shared-index edits: if two index files must reference each other, or if the governance index must reconcile against the index template, the orchestrator makes those cross-file edits. Parallel agents do not co-edit shared indexes or manifests.
- Archival approval: this phase archives nothing. The orchestrator confirms that no agent touched the source monoliths and that archival remains deferred to Phase 09.
- Acceptance of agent work: the orchestrator reads every diff, runs the Validation checks in section 10, and explicitly accepts or rejects each agent output before the phase is considered done.
- Sequencing the dependent index task (Task G) after its inputs land.

## 8. Execution Steps

1. Confirm Phase 02 is complete and its checkpoint commit exists. Confirm the governance target folders from the master spec Phase 2 tree are present.
2. Orchestrator finalizes the exact governance paths and filenames against the master spec Phase 2 tree.
3. Dispatch Tasks A, A2, B, C, D, E, and F in parallel (all write to disjoint files).
4. Collect agent reports. Orchestrator reads each diff and runs preliminary validation.
5. After Tasks B, C, and D are accepted, dispatch Task G (governance index), which depends on them.
6. Orchestrator reconciles any cross-file references between the governance index, the index template, the context-loading guide, and the canon hierarchy.
7. Orchestrator appends any conflicts discovered during reading to the `migration/conflicts-found.md` ledger Phase 00 seeded (never re-creating it) and appends to `migration/migration-map.md` to reflect governance files now created, leaving the source-to-destination map Phase 01 authored intact.
8. Run the full Validation suite in section 10.
9. Address human review points in section 11.
10. When all Completion Criteria are met, perform the Checkpoint in section 13.

## 9. Deliverables

When this phase is later executed it produces, all with valid YAML front matter where they are active documents:

- `CLAUDE.md` (root) with the required per-session guidance and the six-row task-routing table.
- `README.md` (root): a concise project introduction pointing to `CLAUDE.md` and `docs/00-governance/`.
- `docs/00-governance/context-loading-guide.md` derived from the development guide.
- `docs/00-governance/canon-hierarchy.md`.
- `docs/00-governance/index.md`.
- `docs/00-governance/_templates/index-template.md` (the one reusable index shape, owned by Phase 03).
- `project-status.md` (root) seeded per Phase 14; Phase 09 later updates it.
- `migration/migration-map.md` appended to (Phase 01 remains its sole author), kept current.
- `migration/conflicts-found.md` appended to (never re-created); Phase 00 seeded it.

## 10. Validation

All checks must pass before the phase is complete:

- Every file in the Deliverables list exists at its exact path and nowhere else.
- No source monolith at the repo root was modified, moved, renamed, or archived. Confirm by checking that the ten original files are byte-identical to the Phase 02 baseline (git status shows them untouched).
- No file was written under `docs/10-vision/`, `docs/20-canon/`, `docs/30-plot/`, `docs/40-blueprints/`, `docs/50-manuscript/`, `docs/60-continuity/`, `docs/70-research/`, `context-manifests/`, `scripts/`, `.context/`, or `archive/`.
- `CLAUDE.md` contains every required Phase 8 statement and a six-row routing table with the correct manifest paths.
- `README.md` exists at repo root, is concise, points to `CLAUDE.md` and `docs/00-governance/`, and restates no canon.
- `context-loading-guide.md` contains the four required focuses (per-task reading, authority hierarchy, contradiction handling, canon versus planning) and derives rather than copies the full guide.
- `canon-hierarchy.md` states the ranked authority order and the per-domain ownership mapping and the flag-and-preserve conflict rule.
- `index-template.md` contains all seven required Phase 5 index elements as fillable fields and the no-replacement-canon caveat.
- `project-status.md` contains the full Phase 14 YAML block plus active document versions, unresolved conflicts, recommended next manifest, and last reorganization date.
- All active governance documents carry the required front matter fields (title, document_type, status, authority, summary, tags, related, source_documents).
- No new prose written in this phase contains an em dash.
- All new filenames are lowercase kebab-case.
- Any relative link in a governance document either resolves to an existing file or is explicitly marked as a later-phase pending destination.
- `migration/migration-map.md` still lists all ten source monoliths with intended destinations as authored by Phase 01, with Phase 03 governance entries appended and Phase 01's entries intact; `migration/conflicts-found.md` retains its Phase 00 header (appended to, never re-created) and states the flag-and-preserve rule.

## 11. Human Review Points

- Confirm the `CLAUDE.md` task-routing table matches the manifests the team intends to create in the later manifest phase.
- Confirm the `canon-hierarchy.md` ranked order and per-domain ownership match the author's intent, since this governs all future conflict resolution.
- Confirm the `context-loading-guide.md` faithfully represents the development guide without dropping any task-specific reading guidance the author relies on.
- Confirm `project-status.md` values (current chapter, statuses, next task) reflect the true project state at execution time.
- Approve that no source monolith was touched and that archival remains deferred to Phase 09.

## 12. Completion Criteria

- [ ] `CLAUDE.md` created or updated with all required statements and the six-row routing table.
- [ ] `README.md` created at repo root, concise, pointing to `CLAUDE.md` and `docs/00-governance/`.
- [ ] `docs/00-governance/context-loading-guide.md` created and derived from the development guide.
- [ ] `docs/00-governance/canon-hierarchy.md` created with ranked authority and per-domain ownership.
- [ ] `docs/00-governance/index.md` created using the index template shape.
- [ ] `docs/00-governance/_templates/index-template.md` created with all seven Phase 5 elements.
- [ ] `project-status.md` seeded per Phase 14 (Phase 09 later updates it, not Phase 03).
- [ ] `migration/migration-map.md` appended to (Phase 01 remains sole author) and `migration/conflicts-found.md` appended to (never re-created; seeded in Phase 00).
- [ ] No source monolith modified, moved, renamed, or archived.
- [ ] No canon, manifest, script, archive, or .context file created in this phase.
- [ ] All active governance documents carry required front matter.
- [ ] No em dashes in any prose written this phase; all new filenames are lowercase kebab-case.
- [ ] Full Validation suite in section 10 passed and accepted by the orchestrator.
- [ ] Human review points in section 11 addressed.

## 13. Checkpoint

This phase ends with a git-commit checkpoint before Phase 04 begins. The orchestrator commits only after every Completion Criterion is checked and Validation has passed.

Suggested commit message:

```text
phase-03: governance and indexes

Add root CLAUDE.md, root README.md, governance docs (context-loading-guide,
canon-hierarchy, governance index, the one reusable index template), seed
project-status, and append to migration tracking (migration-map appended,
conflicts-found appended). Phase 01 remains sole author of the migration map;
the conflicts ledger was seeded in phase 00. No canon split, no archival;
source monoliths untouched.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

Do not begin Phase 04 until this checkpoint commit exists.
