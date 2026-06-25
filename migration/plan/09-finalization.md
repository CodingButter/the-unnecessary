---
title: "Phase 09: Finalization"
document_type: "migration-runbook"
phase: "09"
title_text: "Finalization"
depends_on:
  - "08"
status: "planned"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Phase 09: Finalization

> Authority note: The master spec at `migration/REPOSITORY-REORGANIZATION-SPEC.md` is authoritative. If anything in this runbook ever conflicts with that spec, the spec wins. This runbook operationalizes spec Phase 11 (Preserve Source Monoliths), Phase 14 (Create Project Status), Phase 15 (Create the Final Migration Report), and the "Desired End State" section. This document is a PLAN. It describes work to be performed in a future execution pass. Nothing here is to be executed during the planning task that produced this file.

## 1. Purpose

This is the closing phase of the reorganization. After Phase 08 has produced and validated the full target tree under `docs/`, this phase does three things and nothing more:

1. Archives the original source monoliths into `archive/source-monoliths/` with archive headers, so the originals are preserved as historical reference and removed from active canon, exactly as spec Phase 11 requires.
2. Writes the final migration report at `migration/final-report.md` covering every item in spec Phase 15, including the final project tree, the old-to-new file map, validation results, and the recommended next command and next task.
3. UPDATES the existing `project-status.md` (created by Phase 03) per spec Phase 14 so the project is positioned to begin the Chapter 1 blueprint, with `next_task` set to "Create the Chapter 1 blueprint". This is an update in place that preserves the active-document-versions and other content accumulated by intervening phases; it does not clobber or recreate the file.

The phase exists to make the project handoff-ready: a different capable LLM should be able to open `CLAUDE.md`, read `project-status.md`, pick the right context manifest, and start Chapter 1 without loading the whole repository and without ever touching an archived monolith as if it were canon. This matches the spec "Desired End State" workflow.

The central safety contract of this phase: source monoliths MUST NOT be archived until Phase 08 has confirmed complete coverage. Per spec Phase 11, "Do not archive a source document until all of its meaningful sections have confirmed destinations." Archival is a one-way action in spirit, so it is the last thing this phase does, and only after validation passes.

## 2. Dependencies

- Phase 08 MUST be complete and committed before this phase begins. Phase 08 is the validation phase that confirms every active source section has a destination, no canonical section was lost, source-monolith headings match split-file headings, links resolve, manifests reference existing files, and Chapter 1 can be planned without loading the entire repository (see spec "Validation Requirements").
- The git baseline commit and the Phase 08 checkpoint commit MUST both exist. This phase begins from a clean working tree at the Phase 08 checkpoint.
- The following must already be in place from prior phases and are treated as read-only inputs here: the full `docs/` tree, `context-manifests/`, `scripts/`, `CLAUDE.md`, the earlier migration artifacts (`migration/repository-audit.md`, `migration/migration-map.md`, `migration/conflicts-found.md`), and the validation scripts (`scripts/validate-links.py`, `scripts/validate-metadata.py`).

If Phase 08 is not confirmed complete, STOP. Do not archive anything. Coverage confirmation is the gate for this entire phase.

## 3. Inputs

Read-only inputs (consumed, not modified, by this phase):

- The validated target tree from Phase 08: everything under `docs/` (00-governance through 70-research), `context-manifests/`, `scripts/`, and `CLAUDE.md`.
- The original source monoliths at repo root, exact filenames:
  - `Narrative Brief.md`
  - `Story Bible.md`
  - `Character Bible.md`
  - `Technology Rules.md`
  - `Master Timeline.md`
  - `Plot Outline and Chapter Map.md`
  - `Style Guide.md`
  - `Creative Decision Log.md`
  - `Development and Canon Guide.md`
  - `chapter-blueprints/Chapter Blueprint Template.md`
- Prior migration artifacts: `migration/repository-audit.md`, `migration/migration-map.md`, `migration/conflicts-found.md`.
- Validation tooling: `scripts/validate-links.py`, `scripts/validate-metadata.py`, plus any duplicate-authority and archive-safety checks built in Phase 10 ordering of the spec.
- The spec sections that govern this phase: spec Phase 11, Phase 14, Phase 15, "Validation Requirements", and "Desired End State".

## 4. Allowed Changes

This phase may create or edit only the following concrete paths. Nothing else.

- Create: `archive/source-monoliths/narrative-brief.md`
- Create: `archive/source-monoliths/story-bible.md`
- Create: `archive/source-monoliths/character-bible.md`
- Create: `archive/source-monoliths/technology-rules.md`
- Create: `archive/source-monoliths/master-timeline.md`
- Create: `archive/source-monoliths/plot-outline-and-chapter-map.md`
- Create: `archive/source-monoliths/style-guide.md`
- Create: `archive/source-monoliths/creative-decision-log.md`
- Create: `archive/source-monoliths/development-and-canon-guide.md`
- Create: `archive/source-monoliths/chapter-blueprint-template.md`
- Create: `migration/final-report.md`
- Edit (update in place): `project-status.md`. Phase 03 created this file; Phase 09 updates it, preserving the active-document-versions and other content accumulated by intervening phases rather than recreating it.
- Edit (only if archival changes a documented source path): the `source_documents` front-matter values in active `docs/**` files, and any archive-safety note in `context-manifests/**`, strictly to point at the new `archive/source-monoliths/<kebab>.md` locations. This is a narrow, mechanical link-correction allowance, not a content edit.

Archived filenames use lowercase kebab-case, per spec operating rules. The move from repo-root `Original Name.md` to `archive/source-monoliths/original-name.md` is a relocate-and-rename, performed as a tracked git move so history is preserved.

## 5. Prohibited Changes

- Do NOT alter the prose, headings, tables, code blocks, or Mermaid diagrams inside any source monolith. The archived copy must be byte-faithful to the original except for the prepended archive header block. Per spec, do not paraphrase or shorten canonical prose.
- Do NOT archive any source monolith whose coverage Phase 08 did not confirm. If even one source has an unmapped section, archival of that source is forbidden until the gap is resolved (escalate to the orchestrator).
- Do NOT split, merge, rename, rewrite, or re-edit any active `docs/**` canon content. Splitting belongs to earlier phases. This phase only finalizes.
- Do NOT modify `context-manifests/**` content beyond the narrow archive-path correction in Allowed Changes. Manifests MUST continue to exclude archived files from normal task context (spec Phase 11 item 3).
- Do NOT touch `scripts/**`, `CLAUDE.md`, `.context/**`, `.git/**`, `.gitignore`, `.env`, `.mcp.json`, or the prior migration artifacts (`repository-audit.md`, `migration-map.md`, `conflicts-found.md`) except to read them.
- Do NOT delete the original source documents outright in a way that loses content. Archival is move-with-preservation, not deletion (spec operating rules: "Do not delete original source documents").
- Do NOT add archived monoliths to any index or context manifest as active canon. Archived material may appear only as explicitly marked historical reference (spec Phase 11 item 3, archive-safety check).
- Reminder for the planning pass that authored this file: the planning task itself moves nothing. The only file the planning task may write is this runbook.

## 6. Agent Delegation Plan

Agents run in parallel where work is independent. No two parallel agents may edit the same index, manifest, or shared file. The archival agent and the report agent and the status agent each own a disjoint output set. Shared-index and shared-manifest edits, archival approval, and acceptance of all agent work are reserved to the orchestrator (see Orchestrator Responsibilities).

### Agent A: Coverage-verification reader (must run first, read-only)

- Exact scope: Re-confirm, from Phase 08 artifacts, that every meaningful section of each source monolith has a confirmed destination in `docs/**`. Produce a per-source coverage matrix: source file, each top-level heading, its destination path, confirmed yes or no.
- Inputs: the ten source monoliths, `migration/migration-map.md`, `migration/repository-audit.md`, the active `docs/**` tree.
- Expected output: a coverage matrix returned in the agent report (not written to disk), plus an explicit pass or fail verdict per source and a single overall verdict.
- Read-only or may-edit: read-only.
- Files it may touch: none (reports back only).
- Files it must not touch: everything.
- How the orchestrator verifies: spot-check several source headings against the claimed destination files by reading those destinations; confirm the overall verdict matches the Phase 08 checkpoint. If any source is "fail", archival of that source is blocked.

### Agent B: Archive-header preparer (read-only, runs after Agent A passes)

- Exact scope: For each source that Agent A marked pass, draft the archive header block (original title, original path, archive date, replacement index, canon status) per spec Phase 11 item 2. Determine each source's correct replacement-index path in `docs/**` (for example the index that now owns that material).
- Inputs: the source monoliths (for original titles and paths), the `docs/**` index files, `migration/migration-map.md`.
- Expected output: ten header blocks (one per source) returned in the report, each with the exact target archive path in kebab-case and the resolved replacement-index relative path.
- Read-only or may-edit: read-only (drafts headers, does not write them).
- Files it may touch: none.
- Files it must not touch: everything; in particular it must not perform the move.
- How the orchestrator verifies: confirm each replacement-index path actually exists in `docs/**` by reading it; confirm header fields are complete and dates are correct.

### Agent C: Final-report author (may-edit, single owned file)

- Exact scope: Write `migration/final-report.md` covering all fifteen spec Phase 15 items, including the final project tree, old-to-new file map, files split, files archived, files left intact, indexes created, manifests created, scripts created, conflicts found, duplicate content found, broken links fixed, validation results, human-review items, the recommended Chapter 1 context-pack command, and the recommended next task.
- Inputs: outputs of Agents A, B, D, E; `migration/migration-map.md`; `migration/conflicts-found.md`; validation run logs from Agent D; the live `docs/**` tree for the final tree section.
- Expected output: `migration/final-report.md`, complete and internally consistent with the other artifacts.
- Read-only or may-edit: may-edit, but only `migration/final-report.md`.
- Files it may touch: `migration/final-report.md` only.
- Files it must not touch: any `docs/**`, `context-manifests/**`, `scripts/**`, `project-status.md`, source monoliths, prior migration artifacts.
- How the orchestrator verifies: read the report end to end; confirm every Phase 15 item is present and non-empty; cross-check the old-to-new map against `migration/migration-map.md`; confirm the recommended command and next task match `project-status.md`.

### Agent D: Validation runner (read-only execution, runs before archival)

- Exact scope: Run `scripts/validate-links.py` and `scripts/validate-metadata.py` and the archive-safety check across the active tree; collect pass or fail output. Run the link validator a second time AFTER archival (orchestrator re-dispatches) to confirm no link broke.
- Inputs: `scripts/**`, the active `docs/**`, `context-manifests/**`, `CLAUDE.md`.
- Expected output: captured validator output and a pass or fail summary, returned in the report.
- Read-only or may-edit: read-only (executes scripts that do not mutate canon).
- Files it may touch: none beyond reading; may write transient logs only under the scratchpad, never under the repo.
- Files it must not touch: any repo file as a write target.
- How the orchestrator verifies: read the raw validator output, not just the agent's summary; confirm zero broken links and zero missing required metadata fields.

### Agent E: Project-status author (may-edit, single owned file)

- Exact scope: UPDATE the existing `project-status.md` (created by Phase 03) to the spec Phase 14 shape, with `next_task: "Create the Chapter 1 blueprint"`, active document versions, known unresolved conflicts (sourced from `migration/conflicts-found.md`), the recommended context manifest for the next task, and the date of last reorganization. Update in place: preserve the active-document-versions and other content accumulated by intervening phases; do not clobber or recreate the file.
- Inputs: spec Phase 14, the existing `project-status.md` from Phase 03 (and its accumulated content), `migration/conflicts-found.md`, the active document versions visible in `docs/**` front matter, the date.
- Expected output: `project-status.md` updated to the Phase 14 fields exactly, with accumulated content preserved.
- Read-only or may-edit: may-edit, but only `project-status.md`.
- Files it may touch: `project-status.md` only.
- Files it must not touch: any `docs/**`, `context-manifests/**`, `migration/**`, source monoliths.
- How the orchestrator verifies: read `project-status.md`; confirm every Phase 14 key is present, `next_task` is exactly the Chapter 1 blueprint string, and the conflicts list matches `migration/conflicts-found.md`.

Parallelization note: Agents C and E own disjoint files and may run in parallel after Agents A, B, D have reported. Agent D's post-archival re-run is sequenced by the orchestrator after the archival move, since it must observe the moved files.

## 7. Orchestrator Responsibilities

Reserved to the main instance and never delegated:

- Final path choices: the exact archive destination filenames and any replacement-index path decisions are confirmed by the orchestrator before any move.
- Canon-conflict resolution: if Agent A surfaces an uncovered section or a late conflict, the orchestrator decides how to resolve it. Agents never silently resolve canon conflicts; per spec they flag, they do not merge.
- Shared-index and shared-manifest edits: any correction to `context-manifests/**` or to `source_documents` paths across multiple `docs/**` files is performed or serialized by the orchestrator, never by parallel agents racing the same file.
- Archival approval: the orchestrator is the single gate that authorizes the actual move of each source monolith into `archive/source-monoliths/`. No agent moves a monolith on its own initiative. Approval is granted per source only after Agent A passes that source and Agent D's pre-archival validation passes.
- Acceptance of agent work: the orchestrator reads each agent's diff and underlying output, verifies it against the checks listed per agent, and accepts or rejects. Verification is the orchestrator's job, not an agent's.
- Performing the git move and the final checkpoint commit.

## 8. Execution Steps

1. Confirm the working tree is clean and sits at the Phase 08 checkpoint commit. If not clean, stop and reconcile.
2. Dispatch Agent A (coverage verification). Read its matrix and verdicts. If any source is "fail", resolve the gap (orchestrator decision) before that source can be archived. Sources that fail remain at repo root, unarchived.
3. Dispatch Agent D (pre-archival validation) and Agent B (archive-header preparation) in parallel. Both are read-only.
4. Review Agent D output directly. Require zero broken links and zero missing required metadata fields on the active tree before proceeding. Review Agent B headers and confirm each replacement-index path exists.
5. For each source that passed Agents A and B, the orchestrator approves archival, then performs the tracked git move: relocate the repo-root monolith (and the template under `chapter-blueprints/`) to `archive/source-monoliths/<kebab-case>.md`, and prepend the Agent B archive header to the moved file. Headers are the only added content.
6. Apply, serially and by the orchestrator, any narrow `source_documents` path corrections in active `docs/**` and any archive-path note in `context-manifests/**`, so references point at the new archive locations.
7. Dispatch Agent D again (post-archival link re-validation). Confirm nothing broke from the move and confirm the archive-safety check still reports no archived file appearing as active canon in any index or manifest.
8. Dispatch Agent C (final report) and Agent E (project status) in parallel. They own disjoint files.
9. Accept Agent C and Agent E output after reading both files and cross-checking them against each other and against the migration artifacts.
10. Run the Validation section below. All checks must pass.
11. Perform the Checkpoint commit.

## 9. Deliverables

- `archive/source-monoliths/narrative-brief.md`
- `archive/source-monoliths/story-bible.md`
- `archive/source-monoliths/character-bible.md`
- `archive/source-monoliths/technology-rules.md`
- `archive/source-monoliths/master-timeline.md`
- `archive/source-monoliths/plot-outline-and-chapter-map.md`
- `archive/source-monoliths/style-guide.md`
- `archive/source-monoliths/creative-decision-log.md`
- `archive/source-monoliths/development-and-canon-guide.md`
- `archive/source-monoliths/chapter-blueprint-template.md`

  Each archived file carries an archive header with: original title, original path, archive date, replacement index, and canon status (spec Phase 11 item 2).

- `migration/final-report.md` covering all fifteen spec Phase 15 items, including the final project tree, the old-to-new file map, validation results, the recommended Chapter 1 context-pack command, the recommended next task, and the known human-review items.
- `project-status.md` updated in place (the file Phase 03 created) to the spec Phase 14 shape, with `next_task: "Create the Chapter 1 blueprint"`, active document versions, known unresolved conflicts, the recommended context manifest for the next task, and the date of last reorganization. The update preserves the active-document-versions and other content accumulated by intervening phases rather than recreating the file.

## 10. Validation

All of the following must pass before the phase is considered complete:

- Coverage gate: every archived source had a confirmed-complete destination set (Agent A pass). No source was archived with an unmapped section.
- Header completeness: each file in `archive/source-monoliths/` begins with an archive header containing all five required fields, and each header's replacement-index path resolves to an existing file in `docs/**`.
- Faithfulness: each archived file's body (everything after the header) is unchanged from its original; Mermaid blocks, tables, and code blocks are intact.
- Link integrity: `scripts/validate-links.py` reports zero broken links after the archival move, including `source_documents` paths now pointing at `archive/source-monoliths/`.
- Metadata: `scripts/validate-metadata.py` reports zero active documents missing required metadata fields.
- Archive safety: no active index or context manifest references an archived file as active canon. Any archive reference is explicitly marked historical (spec Phase 11 item 3, archive-safety check). Confirms that active manifests exclude archived files.
- Report completeness: `migration/final-report.md` contains all fifteen Phase 15 items, each non-empty, and its old-to-new map agrees with `migration/migration-map.md`.
- Status correctness: `project-status.md` matches the Phase 14 field set, with `next_task` exactly "Create the Chapter 1 blueprint", and its conflict list matches `migration/conflicts-found.md`. The file was updated in place from the Phase 03 original, preserving the active-document-versions and other content accumulated by intervening phases.
- Handoff check: following the spec "Desired End State" workflow, a reader can open `CLAUDE.md`, read `project-status.md`, open the create-chapter-blueprint manifest, and reach the Chapter 1 inputs without loading the whole repository and without referencing any archived monolith as canon.

## 11. Human Review Points

Surface these for human sign-off and record them in the final report under "Anything requiring human review":

- Archival approval: a human confirms it is acceptable to move the source monoliths out of the repo root now that Phase 08 coverage is confirmed. Archival is the irreversible-in-spirit action of this phase.
- Any late canon conflict surfaced by Agent A or Agent D that the orchestrator could not resolve mechanically. These are flagged, never silently merged.
- Any source that failed the coverage gate and therefore was NOT archived; its remaining gap is a human decision item.
- Replacement-index choices where more than one `docs/**` index could plausibly be the authority for an archived source.
- The recommended Chapter 1 context-pack command and recommended next task, confirmed correct for the project's intended next move.
- Carry-forward known-issue items inherited from earlier phases (conflicts in `migration/conflicts-found.md`) that remain open at project handoff.

## 12. Completion Criteria

- [ ] Phase 08 confirmed complete and committed; working tree clean at the Phase 08 checkpoint before any change.
- [ ] Coverage gate passed for every source that was archived (no unmapped sections).
- [ ] All ten source monoliths archived under `archive/source-monoliths/` with complete five-field archive headers, via tracked git moves, bodies unchanged.
- [ ] `migration/final-report.md` written and complete across all fifteen Phase 15 items, including final project tree, old-to-new map, validation results, recommended Chapter 1 context-pack command, recommended next task, and known human-review items.
- [ ] `project-status.md` updated in place (from the Phase 03 original) to Phase 14 shape with `next_task: "Create the Chapter 1 blueprint"`, active versions, known conflicts, recommended manifest, and reorg date, preserving content accumulated by intervening phases.
- [ ] Link validator and metadata validator both pass after archival; archive-safety check confirms active manifests and indexes exclude archived files as canon.
- [ ] Human review points reviewed and recorded.
- [ ] Checkpoint commit created with the suggested message before any subsequent work.

## 13. Checkpoint

This phase ends with a git commit checkpoint before any further work begins, per the project's per-phase checkpoint rule. The orchestrator stages the archival moves, the new `archive/source-monoliths/**` files, `migration/final-report.md`, `project-status.md`, and any narrow link corrections, then commits.

Suggested commit message:

```text
chore(migration): phase 09 finalization - archive source monoliths, final report, status

Archive the ten source monoliths to archive/source-monoliths/ with archive
headers, write migration/final-report.md, and update project-status.md with
next_task set to create the Chapter 1 blueprint. Validation passing; active
manifests and indexes exclude archived files. Authority: REPOSITORY-REORGANIZATION-SPEC.md
phases 11, 14, 15.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

Do not begin any post-migration work (for example creating the Chapter 1 blueprint) until this checkpoint commit exists.
