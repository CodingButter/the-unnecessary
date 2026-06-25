---
title: "phase-07-continuity-bootstrap"
document_type: "migration-runbook"
phase: "07"
title_text: "Phase 07: Continuity Bootstrap"
depends_on:
  - "04"
status: "planned"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Phase 07: Continuity Bootstrap

> Authority note: the master spec at `migration/REPOSITORY-REORGANIZATION-SPEC.md` is authoritative. If anything in this runbook conflicts with that spec, the spec wins and this runbook must be corrected to match it. This runbook expands the operational detail of master spec Phase 13 (Create the Initial Continuity Structure); it does not replace or override it.

## 1. Purpose

Stand up the lightweight pre-draft continuity layer under `docs/60-continuity/` for The Unnecessary. The aim is to establish a single, authoritative place that records the starting conditions of the story world before any chapter is drafted, so that when manuscript chapters are later written and approved, continuity can be tracked forward from a known baseline rather than reconstructed.

This phase is deliberately small. It does not invent story, it does not promote plot plans into established fact, and it does not draft chapters. It records what is true at time zero, derived strictly from approved canon produced by Phase 04, and it makes the pre-draft nature of every file unmistakable.

Per master spec Phase 13, because no manuscript chapters are approved yet, every continuity file created here must carry the pre-draft banner:

> No manuscript chapters have been approved. These files contain pre-draft starting conditions only.

The one exception the spec allows: if approved manuscript chapters already exist when this phase runs, continuity must reflect their approved state through the last approved chapter rather than the pre-draft baseline. The orchestrator confirms this state before delegation (see Execution Steps step 1).

Master spec Phase 13 names seven minimum continuity dimensions, all of which this phase must produce: global starting conditions, character starting states, character knowledge states, relationship starting states, technology starting states, unresolved threads, and setups and payoffs.

## 2. Dependencies

- Phase 04 (Split Documents by Semantic Responsibility) MUST be complete. Continuity in this phase is built only from the split canon files under `docs/20-canon/**`. Without those files there is no authoritative source to derive starting states from.
- This phase MAY run in parallel with Phase 06, because the two phases touch disjoint file sets. Phase 06 writes context manifests under `context-manifests/`; this phase writes only under `docs/60-continuity/`. Neither edits the other's files.
- This phase MUST NOT begin before Phase 04's git checkpoint commit exists, so that the canon baseline it reads from is committed and stable.

## 3. Inputs

Read-only inputs. None of these may be modified by this phase.

- `docs/20-canon/characters/profiles/*.md` for character starting states (basic information, location, condition, goals, fears, secrets, false beliefs).
- `docs/20-canon/characters/relationship-map.md` for relationship starting states.
- `docs/20-canon/characters/viewpoint-rules.md` for who can carry knowledge in viewpoint terms.
- `docs/20-canon/technology/**` (foundational rules, ai/, infrastructure/, failure-rules.md, hard-plot-restrictions.md) for technology starting states.
- `docs/20-canon/timeline/book-1/pre-book-2053.md` and `docs/20-canon/timeline/book-1/character-knowledge-timeline.md` and `docs/20-canon/timeline/book-1/secret-timeline.md` for what each character knows and does not know at story start.
- `docs/20-canon/world/**` for global starting conditions (social structure, infrastructure decline, enclaves, locations).
- `docs/30-plot/book-1/reveal-management.md` and `docs/30-plot/book-1/major-beats.md` for identifying setups and payoffs and unresolved threads, used only to name planted elements, never to record their resolutions as already true.
- `migration/REPOSITORY-REORGANIZATION-SPEC.md` Phase 13 for the required file set and the pre-draft banner text.

Canon file and character names are whatever Phase 04 actually produced under `docs/20-canon/**`. The orchestrator resolves the real filenames before delegation; this runbook does not assume them.

## 4. Allowed Changes

This phase may create and edit ONLY the following paths, all new:

- `docs/60-continuity/index.md`
- `docs/60-continuity/global-continuity.md`
- `docs/60-continuity/character-states/` (directory) and one file per established character, lowercase kebab-case, for example `docs/60-continuity/character-states/eli-rook.md`, plus `docs/60-continuity/character-states/index.md`
- `docs/60-continuity/knowledge-state/` (directory) and its contents, for example `docs/60-continuity/knowledge-state/index.md` and per-character knowledge files using the same kebab-case names
- `docs/60-continuity/relationships/` (directory) and its contents, for example `docs/60-continuity/relationships/index.md` and pairwise or per-character relationship-state files
- `docs/60-continuity/technology-state/` (directory) and its contents, for example `docs/60-continuity/technology-state/index.md`, `docs/60-continuity/technology-state/crown.md`, `docs/60-continuity/technology-state/morrow.md`, `docs/60-continuity/technology-state/infrastructure.md`
- `docs/60-continuity/unresolved-threads.md`
- `docs/60-continuity/setups-and-payoffs.md`

All new prose must avoid em dashes. All new filenames must be lowercase kebab-case. All active continuity files must carry YAML front matter consistent with master spec Phase 3 (`title`, `document_type`, `status`, `authority`, `summary`, `tags`, `related`, `source_documents`), with `document_type` such as `continuity-baseline` and `status` such as `active` for a pre-draft baseline.

## 5. Prohibited Changes

- MUST NOT create, edit, move, rename, split, archive, or delete any file outside `docs/60-continuity/`.
- MUST NOT modify any file under `docs/20-canon/**`, `docs/30-plot/**`, `docs/10-vision/**`, `docs/00-governance/**`, `docs/40-blueprints/**`, `docs/50-manuscript/**`, or `docs/70-research/**`.
- MUST NOT touch `context-manifests/**` (owned by Phase 06).
- MUST NOT touch, alter, archive, or move the original source monoliths at repo root: `Narrative Brief.md`, `Story Bible.md`, `Character Bible.md`, `Technology Rules.md`, `Master Timeline.md`, `Plot Outline and Chapter Map.md`, `Style Guide.md`, `Creative Decision Log.md`, `Development and Canon Guide.md`, and `chapter-blueprints/Chapter Blueprint Template.md`. Archival of source monoliths is reserved exclusively to Phase 09 (per master spec Phase 11, archive only after destinations are confirmed). This phase never archives anything.
- MUST NOT change canon. If a continuity fact would require resolving a canon ambiguity or conflict, the agent stops and escalates to the orchestrator rather than deciding.
- MUST NOT record any planned, future, or yet-to-be-drafted event as established continuity. Setups may be named; their payoffs MUST NOT be marked as occurred. Per master spec Phase 13, do not treat planned future events as already-established continuity.
- MUST NOT remove or weaken the pre-draft banner on any file (unless approved manuscript chapters already exist, in which case the orchestrator directs the alternate phrasing).
- MUST NOT use em dashes in any new prose.

## 6. Agent Delegation Plan

Tasks below are designed to run in parallel. They write to disjoint files. The two shared files that multiple tasks would otherwise contend on, `docs/60-continuity/index.md` and each subdirectory `index.md`, are reserved to the orchestrator (Task G), so no two agents edit the same index or shared file.

### Task A: Global starting conditions
- Exact scope: write `docs/60-continuity/global-continuity.md` describing the state of the world at story start (year, social structure, infrastructure decline level, enclave status, location baselines, what is functional and what has failed).
- Inputs: `docs/20-canon/world/**`, `docs/20-canon/timeline/book-1/pre-book-2053.md`.
- Expected output: one file, front matter present, pre-draft banner at top, prose only, em-dash free.
- Read-only or may-edit: may-edit (creates one new file only).
- Files it may touch: `docs/60-continuity/global-continuity.md` only.
- Files it must not touch: all canon, all other continuity files, all root monoliths, all manifests.
- Verification: orchestrator confirms file exists, banner present verbatim, every claim traceable to a cited world or timeline source file, no future events recorded.

### Task B: Character starting states
- Exact scope: write `docs/60-continuity/character-states/<character>.md` for each established character profile present in canon, capturing location, physical and resource condition, immediate situation, active goals, and stated secrets as of story start.
- Inputs: `docs/20-canon/characters/profiles/*.md`, `docs/20-canon/timeline/book-1/pre-book-2053.md`.
- Expected output: one file per established character, each with front matter, pre-draft banner, and a `source_documents` entry pointing at the originating profile.
- Read-only or may-edit: may-edit (creates new files under `character-states/`).
- Files it may touch: `docs/60-continuity/character-states/<character>.md` files only. Does NOT write `character-states/index.md`.
- Files it must not touch: any canon profile, knowledge-state, relationships, technology-state, root monoliths, manifests, any index file.
- Verification: orchestrator confirms one continuity file exists per established canon character, no arc outcomes or planned beats recorded as fact, banner present.

### Task C: Character knowledge states
- Exact scope: write `docs/60-continuity/knowledge-state/<character>.md` recording, per character, what each one knows, believes falsely, and does not yet know at story start.
- Inputs: `docs/20-canon/timeline/book-1/character-knowledge-timeline.md`, `docs/20-canon/timeline/book-1/secret-timeline.md`, `docs/20-canon/characters/profiles/*.md` (false-belief fields).
- Expected output: per-character knowledge files with front matter and pre-draft banner; explicitly separates known, falsely believed, and not-yet-known.
- Read-only or may-edit: may-edit (creates new files under `knowledge-state/`).
- Files it may touch: `docs/60-continuity/knowledge-state/<character>.md` files only. Does NOT write `knowledge-state/index.md`.
- Files it must not touch: canon, character-states, relationships, technology-state, root monoliths, manifests, any index file.
- Verification: orchestrator confirms not-yet-known facts are not leaked into known state, no reveal is recorded as having happened, banner present.

### Task D: Relationship starting states
- Exact scope: write relationship-state files under `docs/60-continuity/relationships/` recording the status of each significant relationship at story start (alliance, tension, debt, trust level, last known interaction baseline).
- Inputs: `docs/20-canon/characters/relationship-map.md`, `docs/20-canon/characters/profiles/*.md` (relationships sections).
- Expected output: relationship-state files (per-pair or per-character), front matter, pre-draft banner.
- Read-only or may-edit: may-edit (creates new files under `relationships/`).
- Files it may touch: `docs/60-continuity/relationships/<name>.md` files only. Does NOT write `relationships/index.md`.
- Files it must not touch: canon, character-states, knowledge-state, technology-state, root monoliths, manifests, any index file.
- Verification: orchestrator confirms each recorded relationship traces to the canon relationship map, no future relationship turns recorded, banner present.

### Task E: Technology starting states
- Exact scope: write technology-state files under `docs/60-continuity/technology-state/` recording the operational state of key systems at story start (Crown, Morrow, energy, communications, cloud dependency, identity and access), including what is up, degraded, or failed.
- Inputs: `docs/20-canon/technology/**`, especially `foundational-rules.md`, `ai/`, `infrastructure/`, `failure-rules.md`, `hard-plot-restrictions.md`.
- Expected output: technology-state files with front matter and pre-draft banner; records capability state, not plot-driven future changes.
- Read-only or may-edit: may-edit (creates new files under `technology-state/`).
- Files it may touch: `docs/60-continuity/technology-state/<system>.md` files only. Does NOT write `technology-state/index.md`.
- Files it must not touch: canon technology files, other continuity dimensions, root monoliths, manifests, any index file.
- Verification: orchestrator confirms states respect canon failure rules and hard-plot restrictions, no planned outage or upgrade recorded as already occurred, banner present.

### Task F: Unresolved threads and setups and payoffs
- Exact scope: write `docs/60-continuity/unresolved-threads.md` (open questions and dangling threads at story start) and `docs/60-continuity/setups-and-payoffs.md` (planted setups with their intended payoffs marked as PLANNED, NOT as occurred).
- Inputs: `docs/30-plot/book-1/reveal-management.md`, `docs/30-plot/book-1/major-beats.md`, `docs/20-canon/timeline/book-1/secret-timeline.md`.
- Expected output: two files, each with front matter and pre-draft banner; every payoff explicitly labeled as not yet delivered.
- Read-only or may-edit: may-edit (creates two new files).
- Files it may touch: `docs/60-continuity/unresolved-threads.md` and `docs/60-continuity/setups-and-payoffs.md` only.
- Files it must not touch: plot canon, other continuity dimensions, root monoliths, manifests, any index file.
- Verification: orchestrator confirms no payoff is marked delivered, threads are framed as open, banner present.

### Task G: Index assembly (orchestrator-owned, runs after A through F)
- Exact scope: write `docs/60-continuity/index.md` plus each subdirectory `index.md` (`character-states/index.md`, `knowledge-state/index.md`, `relationships/index.md`, `technology-state/index.md`), linking to and briefly summarizing the files the other tasks produced.
- Inputs: the file set produced by Tasks A through F.
- Expected output: index files with front matter and pre-draft banner; short summaries that name each linked authority file.
- Read-only or may-edit: may-edit (orchestrator only).
- Files it may touch: the index files listed above only.
- Files it must not touch: the content files written by A through F (the orchestrator reviews them but content edits go back to the owning agent).
- Verification: orchestrator confirms every produced continuity file is linked from an index and no index links to a missing file.

## 7. Orchestrator Responsibilities

Reserved to the main instance, never delegated:

- Confirming at phase start whether any approved manuscript chapters exist, which determines whether files carry the pre-draft banner or reflect approved-chapter state.
- Final path and filename choices for all new continuity files (the agents propose kebab-case names; the orchestrator ratifies them).
- Canon-conflict and canon-ambiguity resolution. Any agent that hits a conflict escalates; only the orchestrator decides, and if a real canon conflict surfaces it is recorded for the migration conflict report rather than silently resolved.
- All shared-index edits: `docs/60-continuity/index.md` and every subdirectory `index.md` (Task G).
- Archival approval: not exercised in this phase. This phase archives nothing; the orchestrator explicitly withholds any archival action, which belongs to Phase 09.
- Acceptance of agent work: reviewing each produced file against its verification criteria before marking the task accepted and before the phase checkpoint.

## 8. Execution Steps

1. Confirm Phase 04 is complete and its checkpoint commit exists. Confirm whether any approved manuscript chapters exist under `docs/50-manuscript/**`; record the answer, which sets the banner mode for all files.
2. Resolve the real canon filenames and the established-character list from `docs/20-canon/characters/profiles/*.md`. Produce the concrete kebab-case target filename list for character-states, knowledge-state, relationships, and technology-state.
3. Create the directory skeleton: `docs/60-continuity/character-states/`, `docs/60-continuity/knowledge-state/`, `docs/60-continuity/relationships/`, `docs/60-continuity/technology-state/`. Do not create empty placeholder files merely to fill the tree.
4. Dispatch Tasks A, B, C, D, E, F in parallel (background agents), each with its scoped read-only inputs, its may-edit file list, and the explicit prohibition list from section 5.
5. As each agent reports, the orchestrator reviews the produced files against that task's verification criteria. Reject and re-dispatch any file that records future events as fact, omits the banner, uses em dashes, or strays outside its allowed paths.
6. After Tasks A through F are accepted, run Task G (orchestrator) to write the top-level index and all subdirectory indexes.
7. Run Validation (section 10). Fix any failure by returning the specific file to its owning task; do not patch content silently in an index.
8. When all validation passes, perform the Checkpoint (section 13).

## 9. Deliverables

- `docs/60-continuity/index.md`
- `docs/60-continuity/global-continuity.md`
- `docs/60-continuity/character-states/` with `index.md` and one file per established character
- `docs/60-continuity/knowledge-state/` with `index.md` and per-character knowledge files
- `docs/60-continuity/relationships/` with `index.md` and relationship-state files
- `docs/60-continuity/technology-state/` with `index.md`, `crown.md`, `morrow.md`, `infrastructure.md` (and other system files as canon warrants)
- `docs/60-continuity/unresolved-threads.md`
- `docs/60-continuity/setups-and-payoffs.md`

Every file carries YAML front matter and the pre-draft banner (or, only if approved chapters exist, the orchestrator-directed approved-state phrasing).

## 10. Validation

All of the following must pass before the phase is complete:

- All seven master spec Phase 13 dimensions are represented: global starting conditions, character starting states, character knowledge states, relationship starting states, technology starting states, unresolved threads, setups and payoffs.
- Every continuity file contains the exact pre-draft banner text: "No manuscript chapters have been approved. These files contain pre-draft starting conditions only." (unless approved manuscript chapters exist and the orchestrator has directed the alternate phrasing).
- There is one character-states file and one knowledge-state file for every established character profile under `docs/20-canon/characters/profiles/`.
- `setups-and-payoffs.md` marks every payoff as PLANNED or not-yet-delivered; no payoff is recorded as occurred. `unresolved-threads.md` frames every thread as open.
- No file records a planned future plot event as established continuity.
- Every file has valid YAML front matter with the required keys, and `related` and `source_documents` use valid relative paths to existing files.
- No new file uses an em dash. All new filenames are lowercase kebab-case.
- No file outside `docs/60-continuity/` was created, edited, moved, renamed, or deleted. The root source monoliths are byte-for-byte unchanged. `git status` shows changes only under `docs/60-continuity/`.
- Every produced file is linked from an index, and no index links to a missing file.

## 11. Human Review Points

- Human confirms the banner mode (pre-draft versus approved-chapter) is correct for the current project state.
- Human spot-checks two character knowledge-state files to confirm no reveal has leaked into the "known" column.
- Human reviews `setups-and-payoffs.md` to confirm no payoff is presented as already delivered.
- Human approves any canon conflict the orchestrator surfaced before it is recorded in the migration conflict report.
- Human gives final sign-off before the Checkpoint commit.

## 12. Completion Criteria

- [ ] Phase 04 confirmed complete and its checkpoint commit verified before this phase started.
- [ ] Banner mode (pre-draft versus approved-chapter) determined and recorded.
- [ ] `docs/60-continuity/global-continuity.md` created and accepted.
- [ ] `docs/60-continuity/character-states/` populated with one file per established character, plus index.
- [ ] `docs/60-continuity/knowledge-state/` populated per character, plus index.
- [ ] `docs/60-continuity/relationships/` populated, plus index.
- [ ] `docs/60-continuity/technology-state/` populated for key systems, plus index.
- [ ] `docs/60-continuity/unresolved-threads.md` created and accepted.
- [ ] `docs/60-continuity/setups-and-payoffs.md` created with all payoffs marked not-yet-delivered.
- [ ] `docs/60-continuity/index.md` links every produced file.
- [ ] Pre-draft banner present on every file (or orchestrator-approved alternate).
- [ ] All Validation checks (section 10) pass.
- [ ] No file outside `docs/60-continuity/` changed; root monoliths untouched; nothing archived.
- [ ] Human review points (section 11) cleared.

## 13. Checkpoint

This phase ends with a git commit before any later phase begins. Stage only `docs/60-continuity/` and commit.

Suggested commit message:

```text
phase-07: bootstrap pre-draft continuity under docs/60-continuity

Add lightweight pre-draft continuity baseline derived from phase-04 canon:
global-continuity, character-states, knowledge-state, relationships,
technology-state, unresolved-threads, setups-and-payoffs, plus indexes.
All files carry the pre-draft banner. No manuscript chapters approved.
No source monoliths touched; archival deferred to phase-09.
```

Do not proceed to dependent phases until this checkpoint commit exists.
