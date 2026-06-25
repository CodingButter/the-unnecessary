---
title: "phase-02-target-architecture"
document_type: "migration-runbook"
phase: "02"
title_text: "Phase 02: Target Architecture"
depends_on:
  - "01"
status: "planned"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Phase 02: Target Architecture

> Authority note: the master spec at `migration/REPOSITORY-REORGANIZATION-SPEC.md` is authoritative. If anything in this runbook ever conflicts with that spec, the spec wins and this runbook must be corrected to match. This runbook is planning only. It describes work to be performed in a FUTURE execution pass. Running this runbook does not move, split, archive, or rewrite any canonical source document.

## 1. Purpose

Define and document the target repository architecture for "The Unnecessary" so that every later phase has one stable contract to build against. This phase converts the prose of master spec Phase 2, Phase 3, and Phase 12 into a single concrete architecture document plus optional empty scaffolding.

Concretely, this phase produces `migration/target-architecture.md`, which records:

- the final proposed directory tree under `docs/`, `context-manifests/`, `scripts/`, `.context/`, `migration/`, and `archive/`
- the filename convention (lowercase kebab-case)
- the YAML metadata schema for active documents
- the schema every `index.md` must satisfy
- the context-manifest YAML schema
- the authority and status vocabulary (controlled values)
- the canon-ownership rules that prevent duplicate sources of truth

This phase decides shape only. It does NOT relocate, split, or write any canon content. Later phases (04 vision, 05 canon, 06 plot, 07 blueprints, 08 manuscript and continuity, and so on) read this document and fill the structure. Phase 09 is the only phase permitted to archive the original monoliths.

## 2. Dependencies

- Phase 01 must complete first. Phase 01 produces the repository audit (`migration/repository-audit.md` per master spec Phase 1) which enumerates every existing document, its apparent version, canon status, subject, recommended destination, and any conflicts.
- This phase consumes that audit so the target tree can be confirmed or adapted against documents that actually exist, rather than against assumptions.
- Do not begin Phase 02 until the Phase 01 checkpoint commit exists in git history.

## 3. Inputs

- `migration/REPOSITORY-REORGANIZATION-SPEC.md`, primarily:
  - Phase 2, Target Structure (the canonical directory tree)
  - Phase 3, Add Standard Metadata (the YAML front matter shape and required fields)
  - Phase 5, Create Index Files (what every `index.md` must contain)
  - Phase 6, Create Task-Specific Context Manifests (the manifest fields)
  - Phase 12, Avoid Canon Duplication (domain ownership rules)
- `migration/repository-audit.md` from Phase 01 (the inventory of real documents and recommended destinations).
- No canon read is required for this phase. The architecture is derived from the spec and the audit, not from the content of the monoliths.

For reference only, the source monoliths that later phases will reorganize live at repo root and at `chapter-blueprints/Chapter Blueprint Template.md`. This phase must not open them for content; it only reasons about where their future split files will land.

## 4. Allowed Changes

The execution of this phase may create the following and nothing else:

- Create or overwrite `migration/target-architecture.md` (the primary deliverable).
- Optionally create EMPTY directory scaffolding that matches the confirmed tree, for example:
  - `docs/00-governance/`, `docs/10-vision/`, `docs/20-canon/`, `docs/30-plot/`, `docs/40-blueprints/`, `docs/50-manuscript/`, `docs/60-continuity/`, `docs/70-research/`
  - `context-manifests/`, `scripts/`, `.context/`, `archive/source-monoliths/`, `archive/superseded/`, `archive/rejected/`, `archive/retired-drafts/`
  - Because git does not track empty directories, an optional `.gitkeep` placeholder may be added inside each scaffolded directory so the tree survives the Phase 02 checkpoint commit.
- Optionally create structural TEMPLATE STUBS that contain NO canon content, for example:
  - `docs/_templates/active-document-template.md` (front matter schema with placeholder fields only)
  - `docs/_templates/context-manifest-template.yaml` (the manifest schema with placeholder keys only)

  This phase does NOT create an index-template stub. The single reusable index template lives at `docs/00-governance/_templates/index-template.md` and is owned by Phase 03. Phase 02 only DOCUMENTS the index schema in prose within `migration/target-architecture.md` (see Task C), so there is no competing template file.

  Note: the master spec Phase 2 tree shows blueprint templates under `docs/40-blueprints/_templates/`. This runbook's `docs/_templates/` stubs are migration scaffolding, not the canonical blueprint template; the blueprint template itself is handled in the blueprint phase. State this distinction explicitly in `migration/target-architecture.md` so there is no ambiguity about which template is which.

Every stub must be clearly labeled as a placeholder and must contain zero canonical prose.

## 5. Prohibited Changes

The execution of this phase must NOT:

- Move, copy, rename, split, merge, archive, or delete any existing source monolith, including: `Narrative Brief.md`, `Story Bible.md`, `Character Bible.md`, `Technology Rules.md`, `Master Timeline.md`, `Plot Outline and Chapter Map.md`, `Style Guide.md`, `Creative Decision Log.md`, `Development and Canon Guide.md`, and `chapter-blueprints/Chapter Blueprint Template.md`.
- Archive anything. Archival of the monoliths is reserved for Phase 09 only. Do not create archive headers or move files into `archive/` (creating the empty `archive/` directories is allowed; placing any real document inside them is not).
- Write any canon content into `docs/`. The scaffolding is empty. The template stubs hold placeholders only.
- Edit any file outside the allowed set in Section 4. In particular, do not edit `migration/REPOSITORY-REORGANIZATION-SPEC.md`, do not edit `migration/repository-audit.md`, and do not edit any other runbook under `migration/plan/`.
- Update internal links, populate indexes with real summaries, or write real manifests. Those are later-phase deliverables; here they are schemas only.
- Touch root `README.md`, `CLAUDE.md`, `project-status.md`, or `.gitignore`. Those are owned by later phases.

## 6. Agent Delegation Plan

All agent tasks below are read-only against the spec and the audit, and write only to the single deliverable plus optional stubs. To prevent write contention, exactly one task owns each writable file. The architecture document is assembled by the orchestrator from agent-returned section text, so no two agents write `migration/target-architecture.md` at the same time.

Tasks A through E can run in parallel. Each returns markdown text for its section; none of them writes the deliverable directly.

### Task A: Directory tree and filename convention
- Exact scope: Confirm or adapt the master spec Phase 2 tree against the Phase 01 audit. Produce the final tree as a fenced text block plus a short rationale for any deviation. Restate the kebab-case filename rule with examples.
- Inputs: spec Phase 2; `migration/repository-audit.md`.
- Expected output: markdown text for the "directory structure" and "filename conventions" sections, returned in the report (not written to disk).
- Read-only or may-edit: read-only.
- Files it may touch: none (returns text only).
- Files it must not touch: everything; especially the source monoliths and the deliverable file.
- Verification by orchestrator: diff the proposed tree against spec Phase 2 lines 92-285; confirm every top-level node is present; confirm any adaptation is justified by an audit finding and approve or reject it.

### Task B: Metadata schema
- Exact scope: Transcribe and tabulate the YAML front matter schema from spec Phase 3, listing each field, whether required, allowed value type, and an example. Mark which fields draw from the controlled status and authority vocabularies (Task D owns those vocabularies; Task B references them by name only).
- Inputs: spec Phase 3 lines 289-331.
- Expected output: markdown text for the "metadata schema" section.
- Read-only or may-edit: read-only.
- Files it may touch: none.
- Files it must not touch: all source documents and the deliverable.
- Verification by orchestrator: confirm all eight required fields from spec Phase 3 appear (title, document_type, status, authority, summary, tags, related, source_documents) and that the example matches the spec example.

### Task C: Index schema and context-manifest schema
- Exact scope: Produce two sub-schemas, both as prose and labeled skeletons within the architecture document. First, the seven-point index contract from spec Phase 5, documented in prose only (Phase 02 does NOT emit an index-template stub file; the reusable index template at `docs/00-governance/_templates/index-template.md` is owned by Phase 03). Second, the context-manifest field list from spec Phase 6, with a labeled skeleton.
- Inputs: spec Phase 5 lines 494-521; spec Phase 6 lines 523-597.
- Expected output: markdown text for the "index schema" and "context-manifest schema" sections.
- Read-only or may-edit: read-only.
- Files it may touch: none.
- Files it must not touch: all source documents and the deliverable.
- Verification by orchestrator: confirm the index schema lists all seven required elements and the manifest schema lists task name, purpose, required files, optional files, files to exclude, loading order, expected output, canon rules, and validation checks.

### Task D: Authority and status vocabulary
- Exact scope: Define the controlled vocabularies. Status values (for example active-canon, planning, archived, draft, superseded). Authority levels (for example character-canon, technology-canon, timeline-canon, plot-plan, style-rule, governance, continuity, research). Document_type values implied by the spec tree. Provide each as a closed enum with a one-line meaning.
- Inputs: spec Phase 3 (status and authority examples), spec Phase 2 (implied document_type values), spec global rules on canon vs planning vs archived (lines 39-43, 645-651).
- Expected output: markdown text for the "authority and status vocabulary" section.
- Read-only or may-edit: read-only.
- Files it may touch: none.
- Files it must not touch: all source documents and the deliverable.
- Verification by orchestrator: confirm status enum distinguishes active canon, planning, and archived as the spec requires; confirm authority levels map to the docs domains; resolve any naming choice yourself before acceptance.

### Task E: Canon-ownership and anti-duplication rules
- Exact scope: Convert spec Phase 12 into a domain-ownership table that names, for each fact type, the single owning domain and how other domains reference it via links rather than copies.
- Inputs: spec Phase 12 lines 768-789.
- Expected output: markdown text for the "rules for avoiding duplicate canon" section.
- Read-only or may-edit: read-only.
- Files it may touch: none.
- Files it must not touch: all source documents and the deliverable.
- Verification by orchestrator: confirm each of the seven ownership rules from spec Phase 12 is present and that the cross-domain rule is "link, do not duplicate".

### Task F: Optional template stubs
- Exact scope: After the orchestrator accepts Tasks B, C, and D, generate the two placeholder stubs (active-document, context-manifest) with placeholder fields only and a header marking each as a non-canon template. Do NOT generate an index-template stub; the reusable index template is Phase 03's, and Phase 02 documents the index schema in prose only (Task C).
- Inputs: accepted schema text from Tasks B, C, D.
- Expected output: the stub files themselves.
- Read-only or may-edit: may-edit, write only.
- Files it may touch: `docs/_templates/active-document-template.md`, `docs/_templates/context-manifest-template.yaml` (this task is the sole owner of these two paths).
- Files it must not touch: all source documents, `migration/target-architecture.md`, the spec, other runbooks, `docs/_templates/index-template.md` or any index-template stub, and anything under `docs/` other than `docs/_templates/`.
- Verification by orchestrator: open each stub; confirm zero canon content; confirm placeholders match the accepted schemas; confirm the non-canon header is present.

Coordination rule: parallel agents (A through E) write nothing, so they cannot collide. Task F runs after acceptance and owns its three files exclusively. The orchestrator alone writes `migration/target-architecture.md`. No shared index or manifest is edited by more than one agent in this phase.

## 7. Orchestrator Responsibilities

Reserved to the main instance and not delegated:

- Final path choices: the orchestrator decides whether to confirm the spec tree verbatim or adopt any adaptation proposed by Task A, and owns every final directory and filename decision.
- Canon-conflict resolution: if the Phase 01 audit surfaced conflicting facts that affect where a future split file should live, the orchestrator resolves the destination question. Agents must flag, never silently decide.
- Shared-index and shared-file edits: only the orchestrator writes `migration/target-architecture.md`. Any future shared index touched in later phases is likewise an orchestrator decision recorded here.
- Archival approval: the orchestrator confirms that this phase performs zero archival and that archival remains reserved to Phase 09.
- Acceptance of agent work: the orchestrator reads each agent's returned section, verifies it against the cited spec lines, and either accepts it into the deliverable or returns it for rework. Agent summaries are not trusted without checking the underlying spec text.
- Final git checkpoint: the orchestrator performs the Phase 02 commit (Section 13).

## 8. Execution Steps

1. Confirm the Phase 01 checkpoint commit exists and read `migration/repository-audit.md`.
2. Re-read spec Phase 2, Phase 3, Phase 5, Phase 6, and Phase 12 to ground the schemas in authoritative text.
3. Dispatch Tasks A through E in parallel as read-only agents; each returns its section as markdown text.
4. Verify each returned section against the exact spec lines cited in Section 6; resolve any flagged conflict; reject and re-dispatch anything that does not match.
5. Assemble the accepted sections into `migration/target-architecture.md`, with the orchestrator as sole writer. Include the authority note that the spec overrides this document.
6. Decide whether to create the optional empty scaffolding and `.gitkeep` placeholders. If yes, create only the directories listed in Section 4.
7. If template stubs are wanted, dispatch Task F to write the three placeholder stubs under `docs/_templates/`; verify they contain no canon.
8. Run the validation checks in Section 10.
9. Confirm completion criteria in Section 12.
10. Create the Phase 02 git checkpoint commit (Section 13) before any Phase 03 work begins.

## 9. Deliverables

- `migration/target-architecture.md` containing all seven required architecture elements: directory structure, filename conventions, metadata schema, index schema, context-manifest schema, authority and status vocabulary, and canon-ownership rules. This file also states that the master spec is authoritative over it.
- Optional: empty directory scaffolding matching the confirmed tree, with `.gitkeep` placeholders so the tree survives the checkpoint commit.
- Optional: template stubs at `docs/_templates/active-document-template.md` and `docs/_templates/context-manifest-template.yaml`, both placeholder-only and non-canon. No index-template stub is produced here; the index schema is documented in prose within `migration/target-architecture.md`, and the reusable index template at `docs/00-governance/_templates/index-template.md` is owned by Phase 03.

No canon content and no archived files are produced by this phase.

## 10. Validation

All checks must pass before the phase is considered complete:

- `migration/target-architecture.md` exists and contains a section for each of the seven required elements.
- The documented directory tree matches spec Phase 2, or every deviation is explicitly justified against a Phase 01 audit finding.
- The metadata schema lists all eight required fields from spec Phase 3 (title, document_type, status, authority, summary, tags, related, source_documents).
- The index schema lists all seven elements required by spec Phase 5.
- The context-manifest schema lists all nine fields required by spec Phase 6 (task name, purpose, required files, optional files, files to exclude, loading order, expected output, canon rules, validation checks).
- The status vocabulary distinguishes active canon, planning, and archived; the authority vocabulary maps to the docs domains.
- The canon-ownership section reproduces all rules from spec Phase 12 and states the link-do-not-duplicate principle.
- No source monolith was modified: `git status` shows none of the root monoliths or `chapter-blueprints/Chapter Blueprint Template.md` as changed.
- Nothing was placed under `archive/`; any archive directories present are empty (or contain only `.gitkeep`).
- Any template stubs contain zero canon content and are clearly marked as placeholders.
- The deliverable explicitly states that the master spec overrides it on conflict.

## 11. Human Review Points

- Tree adaptations: if Task A proposes any deviation from the spec tree, a human approves or rejects each deviation before it is written.
- Vocabulary naming: the proposed status, authority, and document_type enums should get a human sign-off, since later phases bind to these exact strings.
- Canon-ownership edge cases: any fact type that plausibly belongs to two domains (for example Morrow, which spans character and technology) needs a human ruling on the primary owner before the table is finalized.
- Scope confirmation: a human confirms that no monolith was touched and that no archival occurred.

## 12. Completion Criteria

- [ ] Phase 01 checkpoint commit confirmed present and audit read.
- [ ] `migration/target-architecture.md` created with all seven required architecture elements.
- [ ] Directory tree confirmed or adapted with justification, matching spec Phase 2 intent.
- [ ] Filename convention (lowercase kebab-case) documented with examples.
- [ ] Metadata schema documents all eight required front matter fields.
- [ ] Index schema documents all seven required index elements.
- [ ] Context-manifest schema documents all nine required manifest fields.
- [ ] Authority and status vocabularies defined as closed enums distinguishing active canon, planning, and archived.
- [ ] Canon-ownership and anti-duplication rules captured from spec Phase 12.
- [ ] Deliverable states the master spec is authoritative over this document.
- [ ] Optional scaffolding and stubs (if created) contain no canon and are marked as placeholders.
- [ ] No source monolith moved, split, renamed, archived, or rewritten; verified via `git status`.
- [ ] All Section 10 validation checks pass.
- [ ] Phase 02 git checkpoint commit created (Section 13).

## 13. Checkpoint

This phase ends with a git-commit checkpoint before any Phase 03 work begins. Stage only the files this phase is allowed to produce: `migration/target-architecture.md`, any optional empty scaffolding with `.gitkeep` files, and any optional template stubs under `docs/_templates/` (active-document and context-manifest only; no index-template stub). Do not stage or commit any change to a source monolith.

Suggested commit message:

```text
docs(migration): phase 02 target architecture spec and scaffolding

Add migration/target-architecture.md documenting the target tree,
filename convention, metadata schema, index schema, context-manifest
schema, authority and status vocabulary, and canon-ownership rules.
Optionally add empty docs scaffolding and non-canon template stubs.
No source monolith moved, split, or archived (archival is phase 09).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

Do not proceed to Phase 03 until this checkpoint commit exists.
