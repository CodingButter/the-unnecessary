---
title: "phase-01-repository-audit"
document_type: "migration-runbook"
phase: "01"
title_text: "Phase 01: Repository Audit"
depends_on:
  - "00"
status: "planned"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Phase 01: Repository Audit

> Authority note: the master spec at `migration/REPOSITORY-REORGANIZATION-SPEC.md` is authoritative. If anything in this runbook conflicts with the master spec, the master spec wins. This runbook operationalizes Phase 1 of that spec ("Audit the Existing Repository"); it does not override it.

> Planning note: this is a PLANNING document. Nothing in it is executed now. It describes what a future execution of Phase 01 must do. The audit phase itself is strictly READ-ONLY for all project documents.

## 1. Purpose

Produce a complete, evidence-backed picture of the existing repository before any file is moved, split, renamed, or archived in later phases. Phase 01 is the foundation every other phase reads from. It answers, for every Markdown document in the repository, the following questions:

- What is it (title, type, apparent version, canon status, subject)?
- Where does it live now, and where should it go under the target tree in master spec Phase 2?
- Should it be split, and if so along which heading boundaries (so no source heading is lost when a later phase splits it)?
- Does it duplicate, conflict with, or break links to any other document?
- Is it active material or material that should later be archived?

The phase exists so that later phases (target-structure creation, splitting, metadata, indexing, manifests, archival) can be driven by a written map instead of ad hoc inspection. The deliverables are the source-to-destination contract the rest of the migration depends on. No content is altered during this phase; the output is a set of reports under `migration/` only.

This phase covers master spec Phase 1 in full. It does not perform Phase 2 or later work.

## 2. Dependencies

- Phase 00 must be complete before Phase 01 begins. Phase 00 establishes the baseline git commit and the `migration/` working area. Phase 01 reads from that baseline and writes only audit reports.
- Required precondition: a clean git working tree at the Phase 00 baseline commit, so that the audit reflects a known, reproducible state and so that any accidental write can be detected as a diff.
- No later phase may begin until Phase 01 deliverables exist and the Phase 01 checkpoint commit is made.

## 3. Inputs

Read-only inputs. Every path below is read, never written, during this phase.

- `migration/REPOSITORY-REORGANIZATION-SPEC.md` (authoritative; sections of interest: Phase 1 "Audit the Existing Repository", Phase 2 target tree for destination mapping, the per-document split guidance in Phases 4 through 13 to inform split decisions and heading coverage, and the "Validation Requirements" list).
- Root monolith documents (exact filenames):
  - `Narrative Brief.md`
  - `Story Bible.md`
  - `Character Bible.md`
  - `Technology Rules.md`
  - `Master Timeline.md`
  - `Plot Outline and Chapter Map.md`
  - `Style Guide.md`
  - `Creative Decision Log.md`
  - `Development and Canon Guide.md`
- Blueprint material:
  - `chapter-blueprints/Chapter Blueprint Template.md`
  - any other files under `chapter-blueprints/`
- Any manuscript chapters, continuity documents, or research files discovered during the recursive scan (the scan must not assume these are absent; it must look).
- Git history and `git ls-files` output, used as a cross-check on the file inventory and to detect version or supersession signals.

## 4. Allowed Changes

The only writes permitted during execution of this phase are new or updated report files under `migration/`. Concretely:

- Create or update `migration/repository-audit.md`.
- Create or update `migration/migration-map.md`.
- APPEND to (never re-create) `migration/conflicts-found.md`, the ledger Phase 00 seeded (only if conflicts or ambiguities are found; if none are found, the audit must state that explicitly and the seeded ledger is left as its empty-but-headed Phase 00 state).
- Create or update transient working notes under `migration/` only if needed (for example `migration/audit-notes/*.md`). These are working artifacts, not canon.

Allowed write glob: `migration/**` and only the files listed above within it. Nothing else.

## 5. Prohibited Changes

- Do not move, split, rename, copy, archive, delete, or rewrite any existing project document. This includes every root `.md` monolith and everything under `chapter-blueprints/`.
- Do not alter or archive the original source monoliths. Archival of monoliths is reserved for Phase 09 only. Phase 01 must not touch `archive/` at all.
- Do not create the target `docs/` tree, `context-manifests/`, `scripts/`, `.context/`, or any folder from master spec Phase 2. Those are later phases.
- Do not edit `migration/REPOSITORY-REORGANIZATION-SPEC.md`. It is read-only authority.
- Do not edit any file outside `migration/`. Prohibited write globs include but are not limited to: every root `*.md`, `chapter-blueprints/**`, `archive/**`, `docs/**`, `context-manifests/**`, `scripts/**`, `.context/**`, `CLAUDE.md`, `README.md`, `project-status.md`, `.gitignore`.
- Do not "fix" broken links, duplicates, or conflicts in this phase. Record them only. Resolution happens in later phases under orchestrator control.
- Do not invent version history, canon status, or content that the source documents do not state. Record "unknown" or "not stated" rather than guessing.

## 6. Agent Delegation Plan

All audit agents are READ-ONLY against project documents. Agents write only into their own assigned, non-overlapping note file under `migration/audit-notes/`. No agent edits `migration/repository-audit.md`, `migration/migration-map.md`, or `migration/conflicts-found.md` directly; the orchestrator assembles those shared deliverables from agent notes. This guarantees parallel agents never edit the same index, manifest, or shared file.

Tasks A through E may run in parallel (independent input sets, independent output files). Task F is cross-cutting and runs after A through E so it can read their notes; it is the only task that reasons across documents and it still only writes its own note file.

### Task A: Inventory and structure scan
- Exact scope: recursively enumerate every Markdown file and relevant folder in the repository; record path, byte size, last-modified, and top-level heading count for each; cross-check against `git ls-files`.
- Inputs: the whole repository tree (read), `git ls-files` output.
- Expected output: `migration/audit-notes/a-inventory.md` containing the file tree and a per-file inventory row.
- Read-only or may-edit: read-only on all project documents; may write only its own note file.
- Files it may touch: `migration/audit-notes/a-inventory.md`.
- Files it must not touch: every project document, every other agent note, the three shared deliverables, the spec.
- How the orchestrator verifies: re-run a directory listing and `git ls-files`, confirm counts match the note; confirm git status shows no changes outside `migration/audit-notes/a-inventory.md`.

### Task B: Vision, plot, and style documents
- Exact scope: audit `Narrative Brief.md`, `Plot Outline and Chapter Map.md`, `Style Guide.md`. For each: title, apparent version, canon status, subject, full heading outline, recommended destination per master spec Phase 2, split decision with proposed boundaries, and any internal links.
- Inputs: those three files (read), master spec Phase 2 and Phases 4 split guidance (read).
- Expected output: `migration/audit-notes/b-vision-plot-style.md`.
- Read-only or may-edit: read-only on project documents; writes only its own note file.
- Files it may touch: `migration/audit-notes/b-vision-plot-style.md`.
- Files it must not touch: all other documents and notes, the three shared deliverables, the spec (read-only is fine, no writes).
- How the orchestrator verifies: spot-read the three sources, confirm every level-2 heading in each source appears in the agent's heading outline; confirm git status shows no source diffs.

### Task C: Canon documents (story, character, technology, timeline)
- Exact scope: audit `Story Bible.md`, `Character Bible.md`, `Technology Rules.md`, `Master Timeline.md`. Same per-document fields as Task B. For Character Bible, list every character profile detected. For Master Timeline, note Mermaid diagram blocks and date entries. For Technology Rules, flag any rule whose wording limits plot convenience (hard restrictions, failure rules).
- Inputs: those four files (read), master spec Phase 2 and the relevant split guidance (read).
- Expected output: `migration/audit-notes/c-canon.md`.
- Read-only or may-edit: read-only on project documents; writes only its own note file.
- Files it may touch: `migration/audit-notes/c-canon.md`.
- Files it must not touch: all other documents and notes, the three shared deliverables.
- How the orchestrator verifies: spot-read the four sources, confirm the character list and heading outlines are complete; confirm Mermaid blocks are counted; confirm no source diffs.

### Task D: Governance and decision documents
- Exact scope: audit `Development and Canon Guide.md` and `Creative Decision Log.md`. Same per-document fields. For the Decision Log, enumerate each decision entry with its number, title, status, and category so a later phase can split one file per decision without loss.
- Inputs: those two files (read), master spec Phase 2 and the decision-log and guide split guidance (read).
- Expected output: `migration/audit-notes/d-governance.md`.
- Read-only or may-edit: read-only on project documents; writes only its own note file.
- Files it may touch: `migration/audit-notes/d-governance.md`.
- Files it must not touch: all other documents and notes, the three shared deliverables.
- How the orchestrator verifies: spot-read both sources, confirm the decision enumeration count matches the source; confirm no source diffs.

### Task E: Blueprints, manuscript, continuity, research scan
- Exact scope: audit everything under `chapter-blueprints/` (including `Chapter Blueprint Template.md`), and search the repository for any manuscript chapters, continuity documents, and research files. Record presence or confirmed absence of each category.
- Inputs: `chapter-blueprints/**` (read), full-tree search results (read), master spec Phase 2 (read).
- Expected output: `migration/audit-notes/e-blueprints-and-discovered.md`.
- Read-only or may-edit: read-only on project documents; writes only its own note file.
- Files it may touch: `migration/audit-notes/e-blueprints-and-discovered.md`.
- Files it must not touch: all other documents and notes, the three shared deliverables.
- How the orchestrator verifies: confirm the template heading outline is captured intact; confirm the "absent" claims by an independent search; confirm no source diffs.

### Task F: Cross-document duplicate, conflict, and broken-link sweep
- Exact scope: across all source documents, detect repeated authoritative passages and headings (duplicate detection), contradictory canonical statements (conflict detection), and relative Markdown links whose targets do not resolve (broken-link detection). Read the notes from Tasks A through E to avoid re-scanning and to align on what each document claims.
- Inputs: all source documents (read), notes from Tasks A through E (read).
- Expected output: `migration/audit-notes/f-conflicts-duplicates-links.md` listing each finding with both source locations (file plus heading or line) and a short description. It must not attempt resolution; it records both sides of every conflict.
- Read-only or may-edit: read-only on project documents and on other agents' notes; writes only its own note file.
- Files it may touch: `migration/audit-notes/f-conflicts-duplicates-links.md`.
- Files it must not touch: all source documents, the notes of Tasks A through E (read-only), the three shared deliverables.
- How the orchestrator verifies: for a sample of reported conflicts and broken links, the orchestrator opens both cited locations and confirms the finding is real; the orchestrator decides which findings rise to recorded conflicts.

Parallelism rule restated: Tasks A through E run concurrently because their input and output sets are disjoint. Task F runs after them. No two agents ever write the same file. The three shared deliverables are written by the orchestrator alone.

## 7. Orchestrator Responsibilities

Reserved to the main instance only; never delegated:

- Final destination path choices. Agents propose a recommended destination per document; the orchestrator makes the final call and records it in `migration/migration-map.md`.
- Canon-conflict resolution and adjudication. Agents only report conflicts with both sides preserved. The orchestrator decides which are true conflicts and how they are framed in `migration/conflicts-found.md`. No conflict is silently resolved here; resolution proper happens in later phases.
- All edits to shared deliverables: `migration/repository-audit.md`, `migration/migration-map.md`, `migration/conflicts-found.md`. The orchestrator assembles these from agent notes so no two writers collide.
- Archival approval. The orchestrator confirms that Phase 01 touches no monolith and that archival is deferred to Phase 09; no agent or this phase archives anything.
- Acceptance of agent work. The orchestrator reads each agent note, spot-verifies against the sources, runs `git status` to confirm read-only compliance, and accepts or rejects each note before assembling deliverables.
- Verification that the working tree shows zero diffs outside `migration/` at the end of the phase.

## 8. Execution Steps

1. Confirm Phase 00 is complete: clean working tree at the Phase 00 baseline commit, `migration/` present. Abort if the tree is dirty outside `migration/`.
2. Create the working notes directory `migration/audit-notes/` (the only structural change this phase makes, and it lives under `migration/`).
3. Dispatch Tasks A, B, C, D, and E in parallel. Each writes only its own note file.
4. Collect and accept the five notes: orchestrator reads each, spot-verifies against sources, and runs `git status` to confirm no source diffs.
5. Dispatch Task F. It reads the five notes plus the sources and writes `migration/audit-notes/f-conflicts-duplicates-links.md`.
6. Accept Task F's note after spot-verifying a sample of its conflict, duplicate, and broken-link findings.
7. Orchestrator assembles `migration/repository-audit.md` from notes A through F: file tree, then one row per document with title, current path, apparent version, canon status, subject, recommended destination, split decision, and conflicts or ambiguities. Include the heading coverage plan (every source heading mapped to a planned destination so none is lost when split later) and the active-versus-archive determination per document.
8. Orchestrator assembles `migration/migration-map.md`: a draft source-to-destination mapping table aligned to the master spec Phase 2 tree, including for split documents the per-section destinations.
9. If Task F found any conflicts, duplicates, or broken links worth recording, orchestrator APPENDS to (never re-creates) the `migration/conflicts-found.md` ledger Phase 00 seeded, preserving both sides of each conflict. If none, state "no conflicts found" inside `migration/repository-audit.md` and leave the seeded ledger in its empty-but-headed state.
10. Run the Validation checks in section 10. Fix any gaps by re-dispatching the relevant agent (notes only) and reassembling.
11. Make the checkpoint commit described in section 13.

## 9. Deliverables

- `migration/repository-audit.md` (required). Contains: existing file tree; and per document: title, current path, apparent version, canon status, approximate subject, recommended destination, split decision (split or keep intact, with proposed heading boundaries when split), and any conflicts or ambiguities. Includes the heading coverage plan and the active-versus-archived determination.
- `migration/migration-map.md` (required). Draft source-to-destination mapping aligned to master spec Phase 2, including per-section destinations for documents marked for splitting.
- `migration/conflicts-found.md` (conditional append). Phase 01 APPENDS to (never re-creates) the ledger Phase 00 seeded, if and only if conflicts, duplicates, or broken links are found; each conflict preserves both statements with their source locations. If none are found, `migration/repository-audit.md` states this explicitly and the seeded ledger is left untouched.
- Working notes under `migration/audit-notes/` (supporting, not authoritative).

## 10. Validation

All checks must pass before the phase is considered complete:

- Inventory completeness: every Markdown file returned by a fresh recursive scan and by `git ls-files` appears in the audit file tree. Counts match exactly.
- Per-document coverage: each of the nine root monoliths plus the blueprint template plus every other discovered Markdown file has a complete audit row (no field left silently blank; "unknown" or "not stated" is allowed and explicit).
- Heading coverage: for every document marked for splitting, every level-2 (and deeper where the spec splits deeper) source heading is mapped to a planned destination in the heading coverage plan. No heading is unmapped.
- Destination coverage: every document and every split section has a recommended destination consistent with the master spec Phase 2 tree.
- Conflict and duplicate handling: every reported conflict in `migration/conflicts-found.md` preserves both source statements with locations; none is resolved or merged in this phase.
- Broken links: every relative Markdown link in every source has been checked and either resolves or is recorded as broken.
- Read-only proof: `git status` and `git diff` show zero changes to any path outside `migration/`. No monolith, no blueprint, no `archive/`, no `docs/` was created or touched.
- Spec alignment: the audit satisfies the master spec Phase 1 "audit should contain" list and supports the relevant items in the master spec "Validation Requirements".

## 11. Human Review Points

- Confirm the recommended destinations in `migration/migration-map.md` before later phases act on them; destination choices drive every subsequent move and split.
- Confirm the conflict list in `migration/conflicts-found.md`. A human should agree on what counts as a true canon conflict before any later resolution phase touches it.
- Confirm the active-versus-archive determinations. Nothing is archived in this phase, but the determination informs Phase 09, so it should be reviewed early.
- Confirm any "unknown version" or "ambiguous canon status" entries are acceptable to carry forward, or supply the missing information.

## 12. Completion Criteria

- [ ] Phase 00 confirmed complete and working tree clean before start.
- [ ] `migration/audit-notes/` created and all six agent notes (A through F) accepted by the orchestrator.
- [ ] `migration/repository-audit.md` written with the full file tree and a complete audit row per document.
- [ ] Heading coverage plan present so no source heading will be lost when documents are split in a later phase.
- [ ] Active-versus-archived determination recorded for every document.
- [ ] `migration/migration-map.md` written with a draft source-to-destination mapping aligned to master spec Phase 2.
- [ ] `migration/conflicts-found.md` appended to (never re-created) if any conflicts, duplicates, or broken links exist; otherwise an explicit "no conflicts found" statement appears in the audit and the seeded ledger is left untouched.
- [ ] Duplicate detection, conflict detection, and broken-link detection all performed and recorded.
- [ ] All Validation checks in section 10 pass, including the read-only proof that nothing outside `migration/` changed.
- [ ] Checkpoint commit made (section 13).

## 13. Checkpoint

A git commit is required at the end of Phase 01, before Phase 02 begins. The commit must include only the Phase 01 deliverables and notes under `migration/`, and nothing else. Before committing, run `git status` to confirm no source document changed.

Suggested commit message:

```text
phase-01: repository audit (read-only)

Add migration/repository-audit.md and migration/migration-map.md, and
append to migration/conflicts-found.md (if conflicts found; ledger seeded
in phase 00). No source documents were moved, split, renamed, archived,
or rewritten. Audit only.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

After this commit, Phase 02 may begin.
