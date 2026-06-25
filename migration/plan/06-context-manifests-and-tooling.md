---
title: "phase-06-context-manifests-and-tooling"
document_type: "migration-runbook"
phase: "06"
title_text: "Phase 06: Context Manifests and Tooling"
depends_on:
  - "03"
  - "04"
  - "05"
status: "planned"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Phase 06: Context Manifests and Tooling

> Authority note: the master spec at `migration/REPOSITORY-REORGANIZATION-SPEC.md` is the single source of truth for this reorganization. If anything in this runbook conflicts with that spec, the spec wins. This runbook is an execution plan for a FUTURE migration. It is not an instruction to migrate now.

## 1. Purpose

This phase builds the retrieval and safety layer that sits on top of the reorganized documentation tree. By the time this phase runs, the active canon (migrated in Phase 04 under `docs/20-canon/`), the plot and style structure (migrated in Phase 05 under `docs/30-plot/` and `docs/10-vision/style/`), the governance layer and the one reusable index template (Phase 03), and the per-directory indexes (canon indexes built within Phase 04, plot and style indexes built within Phase 05) are already in place under `docs/`. The split files exist but nothing yet tells a future LLM which subset of them to load for a given job, and nothing yet enforces that those subsets stay correct over time.

This phase produces three concrete things:

1. Task-level context manifests under `context-manifests/` that name the exact files to load for each common workflow (blueprint, draft, revise, continuity-check, canon-revision, technology-research).
2. The Chapter 1 per-chapter context manifest under `docs/40-blueprints/book-1/chapter-01-no-signal/context-manifest.yaml`, scoped to Chapter 1 only.
3. The tooling that consumes and guards those manifests: a context-pack builder (`scripts/build-context-pack.py`), a link validator (`scripts/validate-links.py`), a metadata validator (`scripts/validate-metadata.py`), and a duplicate-authority check (`scripts/check-duplicate-headings.py`).

The phase exists so that the desired end state from the spec becomes mechanically reachable: read `CLAUDE.md`, identify the task, open a manifest, build a pack from only the listed files, and work on one chapter without loading the whole repository. The operational detail for everything in this phase lives in the master spec Phase 6 (Task-Specific Context Manifests), Phase 7 (Per-Chapter Context Manifests, including the Chapter 1 manifest), Phase 9 (Context Pack Builder), and Phase 10 (Validation Tools). Read those four spec sections before executing.

This phase also owns all three validation tools named in spec Phase 10, not just two of them. Spec Phase 10 lists a Link Validator, a Metadata Validator, a Duplicate Authority Check, and an Archive Safety Check. The Link Validator and Metadata Validator are authored here as standalone scripts. The Duplicate Authority Check is authored here as `scripts/check-duplicate-headings.py`, matching the script slot reserved for it in the spec Phase 2 target tree. The Archive Safety Check is not authored as a separate script in this phase; it is enforced by the builder's refuse-archive behavior plus the link validator's path resolution, and is asserted in the Validation section below. This ownership is deliberate: the downstream validation runbook (`migration/plan/08-validation.md`) names `scripts/check-duplicate-headings.py` among the scripts produced earlier and runs it in its Task E, so this phase must produce that file or Phase 08 will reference a file that does not exist.

## 2. Dependencies

This phase runs only after the following earlier phases have completed and been committed to git:

- Phase 03: the governance layer and the one reusable index template in place. The governance documents (`docs/00-governance/context-loading-guide.md`, `docs/00-governance/canon-hierarchy.md`) and `docs/00-governance/_templates/index-template.md` must exist, since several manifests list the governance documents as required reads and later index work reuses the template.
- Phase 04: active canon migrated and stable under `docs/20-canon/` (world, characters, technology, timeline), with the per-directory canon indexes built within Phase 04. Manifests reference these canon paths directly, so the paths must be final before manifests are authored.
- Phase 05: plot and style migrated and stable under `docs/30-plot/` and `docs/10-vision/style/`, including per-chapter plot-map files, with the plot and style indexes built within Phase 05. The chapter blueprint template at `docs/40-blueprints/_templates/chapter-blueprint-template.md` is also in place.

Hard precondition: every active path that a manifest will name must already resolve on disk. This phase does not create canon, plot, or index targets. If a needed target is missing, that is a phase 03 to 05 gap and must be escalated to the orchestrator rather than worked around by inventing a file here.

## 3. Inputs

Read-only inputs consumed while authoring this phase:

- `migration/REPOSITORY-REORGANIZATION-SPEC.md`, sections Phase 6, Phase 7, Phase 9, Phase 10 (authoritative operational detail).
- The stable target paths produced by phases 03 to 05, specifically:
  - `docs/00-governance/context-loading-guide.md`, `docs/00-governance/canon-hierarchy.md`, `docs/00-governance/decision-log/` and its decision files.
  - `docs/10-vision/narrative-brief.md` and `docs/10-vision/style/*.md`.
  - `docs/20-canon/world/*`, `docs/20-canon/characters/*`, `docs/20-canon/technology/*`, `docs/20-canon/timeline/*`.
  - `docs/30-plot/book-1/*` including `docs/30-plot/book-1/chapters/chapter-01.md` and the act files.
  - `docs/40-blueprints/_templates/chapter-blueprint-template.md` and `docs/40-blueprints/book-1/`.
  - `docs/60-continuity/*` starting-condition files.
- The root `CLAUDE.md` produced or updated in phase 08 is NOT a hard input here. Manifests may list `CLAUDE.md` as a required read per the spec, but its presence is verified by tooling at run time, not authored here.

These are reads only. This phase writes nothing into any of the directories above.

## 4. Allowed Changes

The only files this phase may create or edit are:

- `context-manifests/index.md`
- `context-manifests/create-chapter-blueprint.yaml`
- `context-manifests/draft-chapter.yaml`
- `context-manifests/revise-chapter.yaml`
- `context-manifests/continuity-check.yaml`
- `context-manifests/canon-revision.yaml`
- `context-manifests/technology-research.yaml`
- `docs/40-blueprints/book-1/chapter-01-no-signal/context-manifest.yaml`
- `scripts/build-context-pack.py`
- `scripts/validate-links.py`
- `scripts/validate-metadata.py`
- `scripts/check-duplicate-headings.py`
- `.gitignore` (Phase 06 owns the single `.gitignore` edit to add the `.context/` entry, per spec Phase 9; Phase 05 does not touch `.gitignore`)
- `migration/plan/06-context-manifests-and-tooling.md` (this runbook itself, during planning)

All new filenames use lowercase kebab-case. The `.context/` directory is created at runtime by the builder script and holds generated packs only; no manifest or canon content is authored there.

## 5. Prohibited Changes

This phase must NOT:

- Move, split, rename, archive, or rewrite any existing project document. In particular it must not touch the original source monoliths at repo root (`Narrative Brief.md`, `Story Bible.md`, `Character Bible.md`, `Technology Rules.md`, `Master Timeline.md`, `Plot Outline and Chapter Map.md`, `Style Guide.md`, `Creative Decision Log.md`, `Development and Canon Guide.md`, `chapter-blueprints/Chapter Blueprint Template.md`). Only Phase 09 (Preserve Source Monoliths) archives those, and only after their content has confirmed destinations. Nothing in this phase may move them to `archive/source-monoliths/` or anywhere else.
- Edit any file under `docs/` other than the single Chapter 1 manifest listed in Allowed Changes. No edits to canon (`docs/20-canon/**`), plot (`docs/30-plot/**`), style (`docs/10-vision/**`), governance (`docs/00-governance/**`), continuity (`docs/60-continuity/**`), research (`docs/70-research/**`), or any `index.md` produced by phase 05.
- Alter canon facts, plot decisions, character profiles, technology rules, dates, or prose. Manifests only point at files; they never restate or change content.
- Write content into `.context/`. That directory holds generated, disposable packs and is git-ignored.
- Include any path under `archive/` in any task manifest, the Chapter 1 manifest, or any active index. Archived material is historical reference only and must never appear in normal task context.
- Add third-party Python dependencies. All four scripts (`build-context-pack.py`, `validate-links.py`, `validate-metadata.py`, `check-duplicate-headings.py`) are standard-library-only per spec Phase 9 and Phase 10.
- Delete, deduplicate, merge, or rewrite any document when running the duplicate-authority check. Per spec Phase 10 ("Do not automatically delete duplicates. Report them."), `check-duplicate-headings.py` only reports. It never edits, removes, or rewrites canon.

## 6. Agent Delegation Plan

The work splits into independent streams. Parallel agents must never edit the same file. The manifests and the four scripts touch disjoint paths, so they can run concurrently. The `context-manifests/index.md` is a shared file: only one agent owns it, and it runs after the manifest-authoring agents so it can describe what they produced. No two parallel agents touch `.gitignore`; that one-line edit is reserved to the orchestrator.

### Task A: task-level manifests (group 1, world and chapter workflows)

- Exact scope: author `create-chapter-blueprint.yaml`, `draft-chapter.yaml`, `revise-chapter.yaml`. Each manifest lists task name, purpose, required files, optional files, files to exclude, loading order, expected output, canon rules, and relevant validation checks, following spec Phase 6.
- Inputs: spec Phase 6 (blueprint and drafting subsections), and the stable phase 03 to 05 paths for canon, plot, style, continuity.
- Expected output: three valid manifest files using only paths that resolve on disk; blueprint manifest must follow the 13-item required list in spec Phase 6 and must NOT auto-load every character profile, technology file, or chapter.
- Read-only or may-edit: may-edit (creates its three files).
- Files it may touch: `context-manifests/create-chapter-blueprint.yaml`, `context-manifests/draft-chapter.yaml`, `context-manifests/revise-chapter.yaml`.
- Files it must not touch: `context-manifests/index.md`, the continuity and canon-revision and technology manifests, any `docs/**` file, any script, `.gitignore`, any archive path.
- How the orchestrator verifies: confirm all three files parse; confirm every required and optional path exists on disk; confirm no `archive/` path appears; confirm the blueprint manifest does not glob whole directories of profiles or technology files.

### Task B: task-level manifests (group 2, continuity, canon, research)

- Exact scope: author `continuity-check.yaml`, `canon-revision.yaml`, `technology-research.yaml` per spec Phase 6 (continuity, canon-revision subsections) and the technology-research workflow.
- Inputs: spec Phase 6, plus stable paths for `docs/60-continuity/**`, `docs/20-canon/**`, `docs/00-governance/canon-hierarchy.md`, `docs/00-governance/decision-log/`, and `docs/70-research/**` (referenced only as OPTIONAL paths).
- Expected output: three valid manifests. The continuity manifest prioritizes approved manuscript, timeline, knowledge states, character states, technology states, relationships, setups and payoffs. The canon-revision manifest requires narrative brief, canon hierarchy, relevant canon files, decision-log index, relevant decisions, affected plot and manuscript and continuity files. Any `docs/70-research/**` paths that the canon-revision and technology-research manifests reference are listed as OPTIONAL files (never required), so the link validator and `build-context-pack.py` do not fail when no research file exists. Note: `docs/70-research/` content is intentionally deferred (no research exists yet; per the master spec, do not create empty files merely to satisfy the tree).
- Read-only or may-edit: may-edit (creates its three files).
- Files it may touch: `context-manifests/continuity-check.yaml`, `context-manifests/canon-revision.yaml`, `context-manifests/technology-research.yaml`.
- Files it must not touch: `context-manifests/index.md`, the three manifests owned by Task A, any `docs/**` file, any script, `.gitignore`, any archive path.
- How the orchestrator verifies: confirm all three parse; confirm every listed path resolves; confirm no archive path; confirm continuity manifest references existing continuity starting-condition files rather than assuming approved manuscript chapters exist yet.

### Task C: Chapter 1 per-chapter manifest

- Exact scope: author `docs/40-blueprints/book-1/chapter-01-no-signal/context-manifest.yaml` scoped to Chapter 1 only, following the spec Phase 7 Chapter 1 inclusion list.
- Inputs: spec Phase 7, plus the resolved Chapter 1 relevant paths: narrative brief, core premise, infrastructure decline, greater-detroit, elis-neighborhood, eli profile, lena profile, nolan profile, talia profile, relevant relationship info, energy, communications, cloud-dependency, medicine, pre-book timeline, act-1 timeline, act-1 plot file, chapter-01 plot-map, style files for eli voice plus exposition plus viewpoint plus openings, relevant decisions, chapter blueprint template.
- Expected output: one valid manifest. It must EXCLUDE Mars technical detail, Mara's full profile, later-act timelines, and unrelated chapter files, per spec Phase 7.
- Read-only or may-edit: may-edit (creates one file inside the chapter-01 blueprint directory).
- Files it may touch: `docs/40-blueprints/book-1/chapter-01-no-signal/context-manifest.yaml` only.
- Files it must not touch: any other file under `docs/40-blueprints/`, any other `docs/**` file, any `context-manifests/**` file, any script, any archive path.
- How the orchestrator verifies: confirm the file parses; confirm every listed Chapter 1 path resolves; confirm the prohibited Chapter 1 exclusions are genuinely absent; confirm no archive path appears.

### Task D: context-pack builder script

- Exact scope: author `scripts/build-context-pack.py`, standard-library-only, implementing the 14 behaviors in spec Phase 9.
- Inputs: spec Phase 9 in full, plus the manifest schema agreed with Tasks A to C (same key names).
- Expected output: a runnable script that accepts a manifest path, reads its ordered file list, verifies required paths exist, concatenates selected Markdown with a source heading before each file, preserves content exactly, writes packs under `.context/`, records generation time and manifest path, warns on missing optional files, fails on missing required files, refuses `archive/` files unless explicitly included, defaults to glob-free explicit paths, supports the `{chapter_number}` and `{chapter_slug}` and `{previous_chapter_number}` placeholders, and prints a character or token estimate without third-party deps. If dependency-free YAML parsing is impractical, fall back to JSON manifests or a deliberately limited YAML parser for this project's schema only.
- Read-only or may-edit: may-edit (creates one script).
- Files it must not touch: any manifest, any `docs/**` file, the other three scripts, `.gitignore`, any archive path. The script may CREATE `.context/` at run time but the agent does not author content there.
- How the orchestrator verifies: read the diff; run the script against the Chapter 1 manifest once it exists and confirm it builds a pack, fails on an injected missing required path, warns on a missing optional path, and refuses an archive path unless explicitly flagged.

### Task E: validation scripts (link validator, metadata validator, duplicate-authority check)

- Exact scope: author `scripts/validate-links.py`, `scripts/validate-metadata.py`, and `scripts/check-duplicate-headings.py`, all standard-library-only, per spec Phase 10.
- Inputs: spec Phase 10 (Link Validator, Metadata Validator, and Duplicate Authority Check subsections), the active doc tree from phases 03 to 05, and the required metadata field list from spec Phase 3 (`title`, `document_type`, `status`, `authority`, `summary`, `tags`, `related`, `source_documents`).
- Expected output:
  - `validate-links.py` checks relative Markdown links, referenced files, index links, metadata `related` paths, and source-document paths, reporting broken targets. Exits non-zero on failure so it can gate the phase.
  - `validate-metadata.py` checks active documents for the required metadata fields and reports missing ones. Exits non-zero on failure so it can gate the phase.
  - `check-duplicate-headings.py` scans active canon under `docs/` and REPORTS repeated authoritative headings and duplicated long passages across active canon files, per spec Phase 10 "Duplicate Authority Check". It must NEVER delete, merge, deduplicate, or rewrite anything; it only reports, matching the spec line "Do not automatically delete duplicates. Report them." Its report distinguishes a true canon duplication from an allowed short index summary that links to its authority. It must exclude `archive/` from its scan so historical monoliths are not flagged as duplicates of their split successors. It must also EXCLUDE any `_templates/` directories (for example `docs/00-governance/_templates/` and `docs/40-blueprints/_templates/`) so template stubs are never reported as duplicate authority. Exit code is informational (the report is the deliverable); the orchestrator and human reviewer judge each reported duplicate.
- Read-only or may-edit: may-edit (creates three scripts). All three scripts are read-only toward the repo at run time; they report, they do not fix.
- Files it may touch: `scripts/validate-links.py`, `scripts/validate-metadata.py`, `scripts/check-duplicate-headings.py`.
- Files it must not touch: any manifest, any `docs/**` file, `scripts/build-context-pack.py`, `.gitignore`, any archive path.
- How the orchestrator verifies: read all three diffs; run each against the active tree; confirm link validator flags a deliberately broken link and passes on the real tree; confirm metadata validator flags a document with a removed required field; confirm the duplicate-authority check reports a deliberately duplicated heading or passage, leaves both copies untouched on disk, does not flag archived monoliths against their split successors, and does not flag template stubs under any `_templates/` directory.

### Task F: manifests index (runs after Tasks A, B, C)

- Exact scope: author `context-manifests/index.md` describing each task manifest: purpose, which manifest to use for which task, and links. This is the shared index file, so it has a single owner and runs only after the manifest-authoring agents finish.
- Inputs: the manifests produced by Tasks A and B, and the Chapter 1 manifest from Task C.
- Expected output: an index that lets a future LLM pick the right manifest. Short summaries, links to authority, no restated canon, no archive references.
- Read-only or may-edit: may-edit (creates one file).
- Files it may touch: `context-manifests/index.md` only.
- Files it must not touch: any `.yaml` manifest, any script, any `docs/**` file, `.gitignore`, any archive path.
- How the orchestrator verifies: confirm every manifest listed in the index exists on disk; confirm the index adds no archive links and restates no canon.

## 7. Orchestrator Responsibilities

The main instance retains and does not delegate the following:

- Final path choices: the orchestrator approves the exact canonical paths each manifest names, resolving any ambiguity left by phases 03 to 05 before agents hardcode paths.
- Canon-conflict resolution: if authoring a manifest surfaces two competing authority files for the same fact, the orchestrator decides which is authoritative or flags the conflict for human review. Agents never silently pick.
- Shared-index edits: the orchestrator owns sequencing so that `context-manifests/index.md` (Task F) runs only after the manifest authors finish, and confirms no two agents wrote the same file.
- Archival approval: the orchestrator confirms that nothing in this phase archives or moves a source monolith. Archival is Phase 09 and is explicitly out of scope here.
- Archive-safety enforcement decision: the spec Phase 10 Archive Safety Check is enforced in this phase WITHOUT a dedicated script. The orchestrator owns confirming that no task manifest, the Chapter 1 manifest, or `context-manifests/index.md` references any `archive/` path (the link validator and the manifest path-resolution checks surface this), and that the builder refuses `archive/` files unless explicitly included. The orchestrator records this so the downstream validation runbook (`migration/plan/08-validation.md`) does not assume a separate archive-safety tool exists; Phase 08 Task E reuses the builder's refuse-archive behavior plus the link validator rather than a missing script.
- The single `.gitignore` edit to add `.context/` is owned by Phase 06 and performed by the orchestrator, not by a parallel agent. Phase 05 does not touch `.gitignore`.
- Acceptance of agent work: the orchestrator reads every diff, runs the validators and the builder, and accepts or rejects each agent's output. No agent self-certifies.

## 8. Execution Steps

1. Confirm preconditions: verify phases 03, 04, 05 are committed and that the active target paths the manifests will name resolve on disk. If any are missing, stop and escalate.
2. Read spec Phase 6, Phase 7, Phase 9, Phase 10 in full and fix the manifest schema (key names, placeholder names) so all agents agree.
3. Dispatch Tasks A, B, C, D, E in parallel (manifests group 1, manifests group 2, Chapter 1 manifest, builder, the three validation scripts). These touch disjoint files.
4. As each agent reports, read its diff and run the relevant check. Reject and re-dispatch on any failure.
5. After Tasks A, B, C are accepted, dispatch Task F to author `context-manifests/index.md`.
6. Run `scripts/validate-links.py` and `scripts/validate-metadata.py` against the active tree. Resolve reported failures (failures in canon or index files are escalated to the owning earlier phase, not patched here).
7. Run `scripts/check-duplicate-headings.py` against the active canon tree. Read the report. Confirm it leaves all files unchanged on disk. Escalate any true canon duplication it finds to the owning earlier phase rather than patching it here; an allowed index summary that links to its authority is not a failure.
8. Run `scripts/build-context-pack.py` against the Chapter 1 manifest and confirm a pack is produced under `.context/` with correct source headings and no archive content.
9. Perform the Archive Safety Check (no dedicated script): confirm via the link validator output and a path scan that no task manifest, the Chapter 1 manifest, or `context-manifests/index.md` names any `archive/` path, and that the builder refused an injected `archive/` path. Record that this check is satisfied by builder behavior plus the link validator, for Phase 08 to reuse.
10. Orchestrator adds the `.context/` entry to `.gitignore` if absent.
11. Run the full Validation section below. All checks must pass.
12. Create the git-commit checkpoint described in section 13 before any later phase begins.

## 9. Deliverables

- `context-manifests/index.md`
- `context-manifests/create-chapter-blueprint.yaml`
- `context-manifests/draft-chapter.yaml`
- `context-manifests/revise-chapter.yaml`
- `context-manifests/continuity-check.yaml`
- `context-manifests/canon-revision.yaml`
- `context-manifests/technology-research.yaml`
- `docs/40-blueprints/book-1/chapter-01-no-signal/context-manifest.yaml`
- `scripts/build-context-pack.py`
- `scripts/validate-links.py`
- `scripts/validate-metadata.py`
- `scripts/check-duplicate-headings.py`
- `.context/` present and git-ignored (directory created by the builder; entry in `.gitignore`)

## 10. Validation

Every check below must pass before the phase is complete:

- Every task manifest and the Chapter 1 manifest parse without error under the chosen format (YAML or the JSON fallback).
- Every required and optional path listed in every manifest resolves to a file that exists on disk.
- No manifest, the Chapter 1 manifest, or `context-manifests/index.md` references any path under `archive/`.
- The blueprint manifest does not auto-load every character profile, every technology file, or every chapter; it names only relevant files.
- The Chapter 1 manifest excludes Mars technical detail, Mara's full profile, later-act timelines, and unrelated chapter files.
- `scripts/build-context-pack.py` runs against the Chapter 1 manifest and produces a pack under `.context/` with a source heading before each file and content preserved exactly.
- The builder fails on a missing required file, warns on a missing optional file, and refuses an `archive/` file unless that file is explicitly included.
- `scripts/validate-links.py` reports zero broken relative links, index links, `related` paths, and source-document paths across the active tree.
- `scripts/validate-metadata.py` reports zero active documents missing required metadata fields.
- `scripts/check-duplicate-headings.py` runs against the active canon tree, produces a duplicate-authority report, and leaves every file unchanged on disk. Any true canon duplication it finds is escalated to the owning earlier phase, not patched here; an allowed index summary that links to its authority is not treated as a failure. The check excludes `archive/` so historical monoliths are not flagged against their split successors, and excludes any `_templates/` directory so template stubs are never reported as duplicate authority.
- Archive Safety Check: no task manifest, the Chapter 1 manifest, or `context-manifests/index.md` names any `archive/` path, and the builder refuses an injected `archive/` path. This check is satisfied by builder refuse-archive behavior plus the link validator, not by a separate script, and is recorded as such for Phase 08 to reuse.
- All four scripts (`build-context-pack.py`, `validate-links.py`, `validate-metadata.py`, `check-duplicate-headings.py`) run on the standard library alone, with no third-party imports.
- No source monolith at repo root has been moved, renamed, or archived by this phase.

## 11. Human Review Points

Pause for human review when:

- Authoring a manifest surfaces two files claiming authority over the same canon fact (the orchestrator flags it; a human confirms which is authoritative before the manifest hardcodes a choice).
- A required target path from phases 03 to 05 is missing or ambiguous, since that indicates an upstream gap rather than something to invent here.
- The YAML-versus-JSON manifest format decision is made, because it affects every downstream tool and the human should confirm the tradeoff per spec Phase 9.
- A validator reports failures rooted in canon or index files produced by earlier phases, since fixing those is out of this phase's scope and needs an owner assignment.
- Before the checkpoint commit, a human confirms that no source monolith was touched and that `.context/` is correctly git-ignored.

## 12. Completion Criteria

- [ ] Spec Phase 6, 7, 9, 10 read and the manifest schema fixed across all agents.
- [ ] All six task manifests authored in `context-manifests/` and parsing cleanly.
- [ ] `context-manifests/index.md` authored and listing only existing manifests.
- [ ] Chapter 1 manifest authored at `docs/40-blueprints/book-1/chapter-01-no-signal/context-manifest.yaml`, scoped to Chapter 1 with required exclusions absent.
- [ ] `scripts/build-context-pack.py` authored, standard-library-only, implementing all spec Phase 9 behaviors.
- [ ] `scripts/validate-links.py`, `scripts/validate-metadata.py`, and `scripts/check-duplicate-headings.py` authored, standard-library-only, per spec Phase 10.
- [ ] Every manifest path resolves on disk and no manifest references `archive/`.
- [ ] Builder produces a Chapter 1 pack under `.context/`; required-file failure, optional-file warning, and archive refusal all confirmed.
- [ ] Link validator and metadata validator both pass on the active tree.
- [ ] `scripts/check-duplicate-headings.py` runs, produces a report-only duplicate-authority result, and changes no file on disk.
- [ ] Archive Safety Check satisfied (no manifest or index names an `archive/` path; builder refused an injected archive path), enforced via builder behavior plus the link validator and recorded for Phase 08 to reuse.
- [ ] `.context/` git-ignored; no source monolith moved or archived.
- [ ] Orchestrator has read every diff and accepted all agent work.
- [ ] Checkpoint git commit created before the next phase.

## 13. Checkpoint

This phase ends with a git-commit checkpoint before any later phase begins, per the spec's phased checkpoint rule. Stage only the files in the Deliverables list plus the `.gitignore` edit. Do not stage any generated pack under `.context/` (it is git-ignored). Confirm `git status` shows no source monolith moved or deleted.

Suggested commit message:

```text
phase-06: add context manifests and tooling

- add task manifests in context-manifests/ (blueprint, draft, revise,
  continuity-check, canon-revision, technology-research) plus index
- add chapter-01 context-manifest.yaml scoped to chapter 1 only
- add stdlib-only scripts: build-context-pack, validate-links, validate-metadata,
  check-duplicate-headings (duplicate-authority check, report only)
- gitignore .context/ generated packs
- no canon, plot, or source monolith altered

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
