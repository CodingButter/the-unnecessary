---
title: "Phase 05: Planning and Style Migration"
document_type: "migration-runbook"
phase: "05"
title_text: "Planning and Style Migration"
depends_on:
  - "04"
status: "planned"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Phase 05: Planning and Style Migration

> Authority note. The authoritative master spec is `migration/REPOSITORY-REORGANIZATION-SPEC.md`. If anything in this runbook conflicts with that spec, the spec wins. This runbook is an execution plan only. It describes work to be performed LATER. Running this phase does not happen now, and nothing in this document authorizes moving, splitting, renaming, archiving, or rewriting any existing project document during the planning task that produced it.

## 1. Purpose

This phase splits the project's planning, style, and governance-of-craft monoliths into the target documentation tree so that an LLM can load only the planning or style files relevant to a single chapter task instead of four large documents.

When executed later, this phase produces:

- The Book One plot layer under `docs/30-plot/book-1/`: story spine, major structural beats, one file per act, one concise high-level entry per chapter, a subplot map, and a reveal-management file, derived from `Plot Outline and Chapter Map.md`.
- The independently loadable style layer under `docs/10-vision/style/`, derived from `Style Guide.md`.
- The governance decision log under `docs/00-governance/decision-log/` as one file per decision plus an index table, derived from `Creative Decision Log.md`.
- The relocated chapter blueprint template at `docs/40-blueprints/_templates/chapter-blueprint-template.md`, derived from `chapter-blueprints/Chapter Blueprint Template.md`.
- The active governance guide at `docs/00-governance/novel-development-guide.md`, derived from `Development and Canon Guide.md`.
- As a pending item, the vision-level narrative brief at `docs/10-vision/narrative-brief.md`, derived from `Narrative Brief.md`, kept mostly intact. See Human Review Points; this assignment awaits orchestrator confirmation.

This phase covers master spec Phase 4 for these four named documents (Plot Outline and Chapter Map, Style Guide, Decision Log, Novel Development Guide) plus the template relocation. The Phase 5 index rules in the master spec apply to every directory this phase creates that holds more than three meaningful files.

A hard distinction this phase must preserve: high-level chapter-map entries under `docs/30-plot/book-1/chapters/` are NOT chapter blueprints. They are short structural plot-map entries. Detailed Chapter Blueprints live under `docs/40-blueprints/book-1/` and are produced by other phases. This phase only relocates the blueprint TEMPLATE, not any blueprint.

## 2. Dependencies

- Requires Phase 04 to be complete and committed before this phase starts. Phase 04 is the immediate predecessor in the phased plan.
- Requires the target skeleton directories from master spec Phase 2 to exist: `docs/00-governance/`, `docs/10-vision/`, `docs/30-plot/`, `docs/40-blueprints/`. If a predecessor phase has not created these parent folders, the orchestrator creates them before delegating, since this phase owns the leaf paths listed in Allowed Changes.
- Requires the git baseline commit and the Phase 04 checkpoint commit to exist, so this phase can be reverted cleanly if validation fails.
- Reads, but does not depend on the completion of, the canon phases. Cross-domain references this phase emits (for example a chapter entry pointing at a character profile) are written as relative links to their eventual target paths even if a sibling phase has not populated them yet. Link validation for cross-phase targets is deferred to the master spec Phase 10 link validator.

## 3. Inputs

Existing source documents read by this phase (read-only, never modified here):

- `Plot Outline and Chapter Map.md` (repo root). Contains story spine, major structural beats, four act sections, 36 chapter sections, a subplot map, and a reveal-management section.
- `Style Guide.md` (repo root). Contains core prose identity, viewpoint and narrative distance, dialogue, per-character voice sections, Morrow and Crown dialogue, technology and exposition, emotional writing, pacing, formatting, prohibited patterns, cliches, and a multi-pass style review process plus a chapter style checklist.
- `Creative Decision Log.md` (repo root). Contains 43 numbered decisions across the categories Foundational Story, Setting and Social Structure, Mars, Artificial Intelligence, Character, Plot and Structure, Style and Tone, and Workflow, plus Explicitly Rejected Concepts and Open Decisions sections.
- `Development and Canon Guide.md` (repo root). The full novel development and canon operating guide.
- `chapter-blueprints/Chapter Blueprint Template.md` (repo root subfolder). The blueprint template.
- `Narrative Brief.md` (repo root). Pending assignment to this phase; see Human Review Points.

Governing input:

- `migration/REPOSITORY-REORGANIZATION-SPEC.md`, master spec Phase 4 (split rules for these four documents and the narrative brief) and Phase 5 (index requirements), Phase 3 (metadata shape), and Phase 12 (anti-duplication rules).

## 4. Allowed Changes

This phase may create or edit ONLY the following paths and globs. All new filenames are lowercase kebab-case.

Plot layer:

- `docs/30-plot/book-1/index.md`
- `docs/30-plot/book-1/story-spine.md`
- `docs/30-plot/book-1/major-beats.md`
- `docs/30-plot/book-1/subplot-map.md`
- `docs/30-plot/book-1/reveal-management.md`
- `docs/30-plot/book-1/act-1.md`
- `docs/30-plot/book-1/act-2.md`
- `docs/30-plot/book-1/act-3.md`
- `docs/30-plot/book-1/act-4.md`
- `docs/30-plot/book-1/chapters/index.md`
- `docs/30-plot/book-1/chapters/chapter-01.md` through `docs/30-plot/book-1/chapters/chapter-36.md` (36 files)

Style layer:

- `docs/10-vision/style/index.md`
- `docs/10-vision/style/core-prose.md`
- `docs/10-vision/style/viewpoint.md`
- `docs/10-vision/style/dialogue.md`
- `docs/10-vision/style/character-voices.md`
- `docs/10-vision/style/ai-dialogue.md`
- `docs/10-vision/style/technology-in-prose.md`
- `docs/10-vision/style/emotion-and-moral-content.md`
- `docs/10-vision/style/pacing-and-structure.md`
- `docs/10-vision/style/formatting.md`
- `docs/10-vision/style/prohibited-patterns.md`
- `docs/10-vision/style/revision-checklist.md`

Decision log layer:

- `docs/00-governance/decision-log/index.md`
- `docs/00-governance/decision-log/decisions/001-*.md` through `docs/00-governance/decision-log/decisions/043-*.md` (one file per decision, zero-padded three-digit prefix plus kebab-case slug; the rejected-concepts and open-decisions material is preserved as its own files or a clearly labeled section so rejected concepts stay easy to locate)

Template and guide:

- `docs/40-blueprints/_templates/chapter-blueprint-template.md`
- `docs/00-governance/novel-development-guide.md`

Pending, awaiting orchestrator confirmation (see Human Review Points):

- `docs/10-vision/narrative-brief.md`

No other path may be created or edited by this phase.

## 5. Prohibited Changes

- Do NOT move, split, rename, archive, delete, or rewrite any original source monolith. Specifically, `Plot Outline and Chapter Map.md`, `Style Guide.md`, `Creative Decision Log.md`, `Development and Canon Guide.md`, `chapter-blueprints/Chapter Blueprint Template.md`, and `Narrative Brief.md` remain exactly as they are at the start of this phase. They are read-only inputs. Only the master spec Phase 11 archival step, scheduled as Phase 09 in this plan, may relocate or archive monoliths, and only after their content has confirmed destinations.
- Do NOT touch any path outside the Allowed Changes list. This includes all of `docs/20-canon/`, `docs/50-manuscript/`, `docs/60-continuity/`, `docs/70-research/`, `docs/40-blueprints/book-1/`, `context-manifests/`, `scripts/`, `.context/`, `archive/`, and the remaining `migration/` files. Those belong to other phases.
- Do NOT edit shared root files: `README.md`, `CLAUDE.md`, `project-status.md`, `.gitignore`. They are owned by later phases.
- Do NOT create chapter BLUEPRINTS under `docs/40-blueprints/book-1/`. This phase relocates only the template into `docs/40-blueprints/_templates/`.
- Do NOT paraphrase, condense, or "improve" canonical or planning prose to shorten it. Preserve titles, version labels, status labels, tables, code blocks, and Mermaid diagrams exactly. Index summaries are the only new prose, and they must point to the authority file for detail.
- Do NOT duplicate authority across domains. Chapter entries must not restate full character profiles, technology capabilities, or detailed dates. They link to the canon authority instead, per master spec Phase 12.
- Do NOT silently resolve any conflict discovered between source statements. Preserve both statements and escalate to the orchestrator, which records them per master spec Phase 1 and Phase 15 reporting.
- Do NOT have two parallel agents edit the same index or shared file. Index ownership is assigned to exactly one agent each, listed below.

## 6. Agent Delegation Plan

Five agent task streams. Streams A, B, C, D, and E touch disjoint directory subtrees and disjoint index files, so they run in parallel. No two agents write the same index, manifest, or shared file. Each agent is told its Files it must not touch list explicitly.

### Stream A: Plot spine, beats, acts, subplots, reveals

- Exact scope: Split the non-chapter sections of the plot outline into `story-spine.md`, `major-beats.md`, `subplot-map.md`, `reveal-management.md`, and `act-1.md` through `act-4.md`. Preserve any Mermaid or table content verbatim.
- Inputs: `Plot Outline and Chapter Map.md` (read-only), master spec Phase 4 "Plot Outline and Chapter Map" and Phase 3 metadata shape.
- Expected output: 8 files under `docs/30-plot/book-1/` with YAML front matter, content copied at natural section boundaries, cross-domain references rendered as relative links.
- Read-only or may-edit: may-edit (creates new files only).
- Files it may touch: `docs/30-plot/book-1/story-spine.md`, `major-beats.md`, `subplot-map.md`, `reveal-management.md`, `act-1.md`, `act-2.md`, `act-3.md`, `act-4.md`.
- Files it must not touch: the source monolith; `docs/30-plot/book-1/index.md`; `docs/30-plot/book-1/chapters/**`; any other phase's paths.
- How the orchestrator verifies: diff each new file against the matching source section; confirm act files map to the four act sections; confirm the spine, beats, subplot map, and reveal-management content all have a destination and nothing from those sections is dropped.

### Stream B: Chapter-map entries and chapters index

- Exact scope: Create one concise high-level plot-map entry per chapter, `chapter-01.md` through `chapter-36.md`, each carrying that chapter's high-level outline content only (purpose, movement, character movement, information revealed, ending hook, as present in the source). Then build the chapters index after all 36 entry files exist.
- Inputs: `Plot Outline and Chapter Map.md` (read-only), the 36 chapter sections; master spec Phase 4 and Phase 5.
- Expected output: 36 chapter entry files plus `docs/30-plot/book-1/chapters/index.md`. Each entry states near the top that it is a high-level plot-map entry and that the detailed plan lives in the chapter blueprint, preserving the map-versus-blueprint distinction.
- Read-only or may-edit: may-edit (creates new files only).
- Files it may touch: `docs/30-plot/book-1/chapters/chapter-01.md` through `chapter-36.md` and `docs/30-plot/book-1/chapters/index.md`.
- Files it must not touch: the source monolith; `docs/30-plot/book-1/index.md`; the act, spine, beats, subplot, and reveal files owned by Stream A; any blueprint paths.
- How the orchestrator verifies: count equals 36; each chapter title matches the source; spot-check three entries for fidelity; confirm no entry contains full blueprint-level scene breakdowns; confirm the index lists all 36 with one-line summaries and links.

### Stream C: Style guide split

- Exact scope: Split the style guide into independently loadable files: core prose identity, viewpoint and narrative distance, dialogue, character voices, Morrow and Crown dialogue, technology and exposition, emotion and moral content, pacing and structure, formatting, prohibited patterns and cliches, and the revision checklist. Build the style index after the split files exist.
- Inputs: `Style Guide.md` (read-only), master spec Phase 4 "Style Guide" and Phase 5.
- Expected output: 11 split files plus `docs/10-vision/style/index.md`, all with YAML front matter, content preserved verbatim at section boundaries.
- Read-only or may-edit: may-edit (creates new files only).
- Files it may touch: the 11 style files listed in Allowed Changes plus `docs/10-vision/style/index.md`.
- Files it must not touch: the source monolith; `docs/10-vision/narrative-brief.md`; `docs/10-vision/index.md`; any other phase's paths.
- How the orchestrator verifies: confirm every source style section maps to exactly one destination file; confirm the per-character voice content and the prohibited-patterns and cliche content survive intact; confirm the revision checklist and multi-pass review process are present; confirm the index lists all files with load-when guidance.

### Stream D: Decision log split and index

- Exact scope: Split the decision log into one file per decision, prefixed with the zero-padded decision number and a kebab-case title slug, preserving each decision's full entry including Reason, Consequences, Affected Documents, and Reconsider Only If. Preserve the Explicitly Rejected Concepts and Open Decisions material so rejected concepts stay easy to locate. Build the index table.
- Inputs: `Creative Decision Log.md` (read-only), master spec Phase 4 "Decision Log" and Phase 5.
- Expected output: 43 decision files under `docs/00-governance/decision-log/decisions/`, the rejected and open material preserved, and `docs/00-governance/decision-log/index.md` with a table of decision number, title, status, category, short summary, and file link.
- Read-only or may-edit: may-edit (creates new files only).
- Files it may touch: `docs/00-governance/decision-log/decisions/**` and `docs/00-governance/decision-log/index.md`.
- Files it must not touch: the source monolith; `docs/00-governance/index.md`; `docs/00-governance/novel-development-guide.md`; any other phase's paths.
- How the orchestrator verifies: count equals 43 decision files; the index table row count matches; spot-check three decisions including one rejected concept for fidelity; confirm statuses and categories are carried over, not invented.

### Stream E: Template relocation and development guide

- Exact scope: Copy the blueprint template content into `docs/40-blueprints/_templates/chapter-blueprint-template.md` intact, and copy the full development and canon guide into `docs/00-governance/novel-development-guide.md` as an active governance document. Add YAML front matter to both. This stream does NOT create the shorter context-loading guide; that derivative is a separate governance phase per master spec Phase 4 "Novel Development Guide".
- Inputs: `chapter-blueprints/Chapter Blueprint Template.md` and `Development and Canon Guide.md` (both read-only), master spec Phase 4 and Phase 3.
- Expected output: 2 files with front matter and content preserved exactly.
- Read-only or may-edit: may-edit (creates new files only).
- Files it may touch: `docs/40-blueprints/_templates/chapter-blueprint-template.md` and `docs/00-governance/novel-development-guide.md`.
- Files it must not touch: the source files; `docs/40-blueprints/book-1/**`; `docs/00-governance/decision-log/**`; `docs/00-governance/index.md`; any other phase's paths.
- How the orchestrator verifies: diff template body against source heading-for-heading to confirm the template remains intact; diff the guide body against source to confirm it remains fully represented as active governance.

### Optional Stream F (pending): Narrative brief relocation

- Conditional on orchestrator confirmation per Human Review Points. If confirmed, copy `Narrative Brief.md` into `docs/10-vision/narrative-brief.md` mostly intact with front matter, no unnecessary splitting. Files it may touch: `docs/10-vision/narrative-brief.md` only. Files it must not touch: the source; `docs/10-vision/style/**`; `docs/10-vision/index.md`. Verified by full diff against source. If not confirmed, this stream is not dispatched and the narrative brief is left for the orchestrator to assign.

## 7. Orchestrator Responsibilities

Reserved to the main instance and never delegated:

- Final path choices, including the exact kebab-case slugs for the 43 decision files and the 36 chapter files, and any deviation from the master spec target tree.
- Canon-conflict resolution. If any agent reports two source statements that disagree, the orchestrator decides how to record the conflict and never lets an agent silently pick one.
- All edits to shared index files where ownership is ambiguous, and final acceptance of every index produced by streams.
- Creating parent skeleton folders if a predecessor phase did not.
- Archival approval. The orchestrator confirms that this phase does not archive any monolith and that archival waits for Phase 09.
- Acceptance of agent work. The orchestrator reads each diff and runs the validation checks before marking the phase complete. The orchestrator, not an agent, runs the git checkpoint commit.
- The narrative-brief assignment decision in Human Review Points.

## 8. Execution Steps

1. Confirm Phase 04 is complete and its checkpoint commit exists. Confirm a clean working tree.
2. Confirm the parent folders `docs/00-governance/`, `docs/10-vision/style/`, `docs/30-plot/book-1/chapters/`, `docs/40-blueprints/_templates/`, and `docs/00-governance/decision-log/decisions/` exist; create any missing ones.
3. Resolve the narrative-brief question in Human Review Points before dispatching Stream F. Record the decision.
4. Dispatch Streams A, B, C, D, and E in parallel, each with its scope, inputs, allowed files, forbidden files, and verification contract. Dispatch Stream F only if confirmed.
5. Within Stream B and Stream D, the agent creates all leaf files first, then builds its single owned index last so the index reflects the finished set.
6. Collect agent reports. For each stream, read the diffs and run the per-stream verification.
7. Resolve any reported conflicts at the orchestrator level. Do not let agents resolve them.
8. Run the phase-level Validation checks in section 10.
9. If validation passes, perform the Checkpoint commit in section 13. If it fails, revert the new files, fix, and rerun.

## 9. Deliverables

- `docs/30-plot/book-1/`: index, story-spine, major-beats, subplot-map, reveal-management, act-1 through act-4, and `chapters/` containing index and chapter-01 through chapter-36 (high-level entries, distinct from blueprints).
- `docs/10-vision/style/`: index plus core-prose, viewpoint, dialogue, character-voices, ai-dialogue, technology-in-prose, emotion-and-moral-content, pacing-and-structure, formatting, prohibited-patterns, and revision-checklist.
- `docs/00-governance/decision-log/`: index plus `decisions/` with one file per decision (43) and the rejected and open material preserved.
- `docs/40-blueprints/_templates/chapter-blueprint-template.md` (relocated, intact).
- `docs/00-governance/novel-development-guide.md` (active governance).
- `docs/10-vision/narrative-brief.md` (pending orchestrator confirmation).
- No source monolith moved or archived by this phase.

## 10. Validation

Concrete checks that must pass before completion:

- File counts: exactly 36 chapter entry files; exactly 4 act files; exactly 43 decision files. Each count matches the source (36 chapters and 43 decisions confirmed in the source documents).
- Coverage: every section of each of the four covered monoliths plus the template maps to a confirmed destination, and no section is dropped. The story spine, major beats, subplot map, and reveal-management content all have destinations.
- Fidelity: diff-based spot checks confirm titles, version labels, status labels, tables, code blocks, and Mermaid diagrams are preserved verbatim. No canonical or planning prose was paraphrased to shorten it.
- Distinction: no `docs/30-plot/book-1/chapters/*.md` entry contains blueprint-level scene breakdowns; each states it is a high-level plot-map entry. The blueprint template exists only under `docs/40-blueprints/_templates/`.
- Indexes: each directory with more than three meaningful files has an `index.md` that names the file to read first, lists files with one or two sentence summaries, gives authority or status, and lists common tasks, per master spec Phase 5.
- Metadata: every new active document carries the required YAML front matter fields from master spec Phase 3 (title, document_type, status, authority, summary, tags, related, source_documents).
- Anti-duplication: chapter entries link to canon authorities rather than restating profiles, capabilities, or detailed dates.
- Relative links inside this phase's files resolve; cross-phase targets are noted as deferred to the master spec Phase 10 link validator.
- Source monoliths are byte-for-byte unchanged from the start of the phase.
- No conflicts were silently resolved; any found are recorded for the migration report.

## 11. Human Review Points

- NARRATIVE BRIEF ASSIGNMENT (must resolve before Stream F). The task spec does not explicitly assign `Narrative Brief.md` to any phase. It is folded into THIS phase as a pending item, target `docs/10-vision/narrative-brief.md`, kept mostly intact, PENDING orchestrator confirmation. The orchestrator must confirm that the narrative brief belongs to Phase 05 before any narrative-brief file is created. If the orchestrator declines, the brief is left unassigned and untouched.
- Decision and chapter slug naming. The orchestrator approves the final kebab-case slugs for the 43 decision files and 36 chapter files before they are treated as stable link targets.
- Any source conflict surfaced by an agent. The orchestrator decides how to record it; nothing is resolved silently.
- Confirmation that the shorter `context-loading-guide.md` is intentionally out of scope here and owned by a governance phase, so no duplicate governance authority is created.
- Confirmation that no monolith is archived in this phase; archival is reserved for Phase 09.

## 12. Completion Criteria

- [ ] Phase 04 verified complete and committed; working tree clean at start.
- [ ] Narrative-brief assignment question resolved and recorded; Stream F dispatched only if confirmed.
- [ ] Plot deliverables created: index, spine, beats, subplot map, reveal-management, 4 act files, chapters index, and 36 chapter entries.
- [ ] Style deliverables created: index plus 11 independently loadable style files.
- [ ] Decision log deliverables created: index plus 43 decision files, with rejected and open material preserved.
- [ ] Template relocated intact to `docs/40-blueprints/_templates/chapter-blueprint-template.md`.
- [ ] Development and canon guide created as active governance at `docs/00-governance/novel-development-guide.md`.
- [ ] All new active documents carry required YAML front matter.
- [ ] Every covered source section has a confirmed destination; nothing dropped or paraphrased to shorten.
- [ ] Chapter-map versus chapter-blueprint distinction preserved.
- [ ] No source monolith moved, renamed, archived, or rewritten.
- [ ] No out-of-scope path touched; no two agents edited the same index.
- [ ] All Validation checks in section 10 pass.
- [ ] Checkpoint commit created before the next phase begins.

## 13. Checkpoint

Before any later phase begins, the orchestrator commits this phase's work as a single checkpoint. A clean git status after commit is required so the next phase starts from a known state.

Suggested commit message:

```
phase-05: split planning and style monoliths into target tree

Add docs/30-plot/book-1 (spine, beats, subplots, reveals, 4 acts,
chapters index, 36 high-level chapter-map entries), docs/10-vision/style
(11 loadable style files plus index), docs/00-governance/decision-log
(43 decision files plus index), relocated chapter-blueprint-template, and
novel-development-guide. Narrative brief relocation pending orchestrator
confirmation. Source monoliths left intact; archival deferred to phase-09.

Spec: migration/REPOSITORY-REORGANIZATION-SPEC.md
Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
