---
title: "phase-08-validation"
document_type: "migration-runbook"
phase: "08"
title_text: "Phase 08: Validation"
depends_on:
  - "03"
  - "04"
  - "05"
  - "06"
  - "07"
status: "planned"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Phase 08: Validation

This runbook describes a FUTURE execution phase for the reorganization of the
novel repository "The Unnecessary". It is planning only. No migration work is
performed by authoring or reading this file.

The authoritative master spec is `migration/REPOSITORY-REORGANIZATION-SPEC.md`.
That spec OVERRIDES this runbook wherever the two conflict. If a validator finds
a discrepancy between an instruction here and the master spec, the master spec
wins, and the discrepancy itself should be logged as a finding in the validation
report. The operational source of truth for this phase lives in the master spec
sections "Validation Requirements", "Phase 10: Add Validation Tools", and
"Desired End State".

## 1. Purpose

Phase 08 is the INDEPENDENT review gate for the migration. By the time this phase
runs, phases 03 through 07 have produced the migrated tree under `docs/`, the
`context-manifests/`, the `scripts/`, the `.context/` plumbing, and the
per-chapter context manifests. Phase 08 does not move, split, or rewrite any of
that work. It PROVES, against the original source monoliths, that the migration
preserved every canonical fact, that the new structure is internally consistent
and linkable, and that Chapter 1 can be planned from the new structure without
loading the whole repository.

The single concrete outcome of this phase is `migration/validation-report.md`: a
machine-skimmable document with one pass or fail line per checklist item and an
explicit list of any gaps. The report is what unlocks Phase 09 (archival of the
source monoliths). The master spec is deliberate on ordering: a source monolith
is archived only after all of its meaningful sections have confirmed
destinations. Phase 08 is the evidence that produces that confirmation. Until
this phase passes, the source monoliths at repo root remain the live fallback
and must not be touched.

This phase exists because the migration phases were performed by agents who had
an interest in their own output passing. Validation must be performed by a
different set of eyes wherever possible, primarily read-only, so that errors of
omission committed during migration are caught rather than rubber-stamped.

## 2. Dependencies

The following earlier phases MUST be complete and committed before Phase 08
begins:

- Phase 03: metadata and front matter applied to active docs.
- Phase 04: source monoliths split by semantic responsibility into the `docs/`
  tree.
- Phase 05: index files created for directories with more than three meaningful
  files.
- Phase 06: task-specific context manifests under `context-manifests/`.
- Phase 07: per-chapter context manifests, including the Chapter 1 manifest under
  `docs/40-blueprints/book-1/chapter-01-no-signal/context-manifest.yaml`.

Each of those phases ends with its own git commit checkpoint. Phase 08 must start
from a clean working tree at the Phase 07 checkpoint commit. If the tree is dirty
or any dependency phase is incomplete, do not start; resolve the gap first.

This phase is a hard prerequisite for Phase 09 (archival). Phase 09 must not begin
until `migration/validation-report.md` shows an all-pass result, or until the
human reviewer has explicitly accepted the documented gaps.

## 3. Inputs

All inputs are read-only for this phase.

- The migrated tree: everything under `docs/` (00-governance, 10-vision,
  20-canon, 30-plot, 40-blueprints, 50-manuscript, 60-continuity, 70-research).
- The manifests: everything under `context-manifests/` and every per-chapter
  `context-manifest.yaml` under `docs/40-blueprints/book-1/`.
- The validation scripts produced earlier: `scripts/validate-links.py`,
  `scripts/validate-metadata.py`, `scripts/check-duplicate-headings.py`, and the
  pack builder `scripts/build-context-pack.py`.
- The original source monoliths at repo root, used ONLY for read-only comparison:
  `Narrative Brief.md`, `Story Bible.md`, `Character Bible.md`,
  `Technology Rules.md`, `Master Timeline.md`,
  `Plot Outline and Chapter Map.md`, `Style Guide.md`,
  `Creative Decision Log.md`, `Development and Canon Guide.md`, and
  `chapter-blueprints/Chapter Blueprint Template.md`.
- The migration trail: `migration/repository-audit.md`, `migration/migration-map.md`,
  `migration/conflicts-found.md`, if present.
- The master spec: `migration/REPOSITORY-REORGANIZATION-SPEC.md`, in particular
  "Validation Requirements", "Phase 10: Add Validation Tools", and
  "Desired End State".

## 4. Allowed Changes

The ONLY file this phase may create or modify is:

- `migration/validation-report.md`

Validators may additionally write scratch artifacts OUTSIDE the repository (for
example under a temporary scratch directory) to hold intermediate diffs, heading
extracts, and coverage tables. These scratch artifacts are not part of the repo
and must not be committed.

Running the existing validation scripts is allowed, because they only read the
tree and write generated packs under `.context/` (which is git-ignored per the
master spec). Generated `.context/` packs are byproducts of running checks, not
deliverables of this phase, and must not be committed.

No other path under the repository may be created, edited, renamed, moved, or
deleted by this phase.

## 5. Prohibited Changes

This phase is a review. It fixes nothing. Specifically prohibited:

- Do NOT move, split, rename, archive, edit, or rewrite any original source
  monolith. The source monoliths listed in Inputs are touched only by Phase 09,
  and only after this phase passes. Reading them is allowed; altering or
  archiving them is forbidden here.
- Do NOT edit anything under `docs/`, `context-manifests/`, `scripts/`,
  `.context/`, or `archive/`. If a validator finds a broken link, a missing
  character profile, a lost canonical section, or a metadata gap, the validator
  RECORDS it as a finding. The validator does not patch it. Remediation belongs
  to a re-run of the responsible earlier phase, decided by the orchestrator and
  the human reviewer.
- Do NOT create any markdown file other than `migration/validation-report.md`.
- Do NOT commit generated `.context/` packs or any out-of-repo scratch files.
- Do NOT resolve canon conflicts. A validator who discovers two files asserting
  contradictory facts records both statements and flags the conflict; resolution
  is reserved to the orchestrator and human reviewer.
- Do NOT delete or silently deduplicate anything, including duplicate
  authoritative headings. Duplicates are reported, never removed.

## 6. Agent Delegation Plan

Validators are INDEPENDENT and PRIMARILY READ-ONLY. Where staffing allows, a
validator for a given domain must NOT be the same agent that performed the
corresponding migration in phases 03 through 07. Each task below produces a
findings fragment that the orchestrator alone merges into the single shared
`migration/validation-report.md`. No agent writes to that report directly, so no
two agents contend for the shared file. All tasks below are independent of one
another and are dispatched in parallel.

### Task A: Source-heading coverage

- Exact scope: Extract every heading from each source monolith. For each source
  heading, confirm a destination heading or destination file exists in the
  migrated tree. Verify against `migration/migration-map.md` where present.
- Inputs: all source monoliths; the `docs/` tree; `migration/migration-map.md`.
- Expected output: a coverage table (source heading, destination path, present
  or missing) plus a count of unmapped headings, returned as a findings fragment.
- Read-only or may-edit: read-only.
- Files it may touch: none in-repo; scratch heading extracts out-of-repo only.
- Files it must not touch: everything; especially the source monoliths and `docs/`.
- Orchestrator verification: spot-check a random sample of "present" rows by
  reading the named destination file, and confirm every "missing" row against the
  migration map.

### Task B: Source-to-destination content verification

- Exact scope: For each source monolith, confirm no canonical section was lost or
  silently paraphrased away. Compare section bodies, tables, code blocks, and
  Mermaid diagrams between source and destination. Confirm Mermaid blocks remain
  valid fenced markdown blocks.
- Inputs: source monoliths; destination files in `docs/`.
- Expected output: per-source verdict (content preserved or section X missing or
  altered), with file:line references on both sides for every gap.
- Read-only or may-edit: read-only.
- Files it may touch: none in-repo; out-of-repo scratch diffs only.
- Files it must not touch: everything in-repo.
- Orchestrator verification: re-read both sides for any reported loss before
  accepting it as a real gap.

### Task C: Link and manifest-reference validation

- Exact scope: Run `scripts/validate-links.py` over the tree and confirm relative
  markdown links, index links, metadata `related` paths, and source-document
  paths resolve. Confirm every path referenced by every context manifest (task
  manifests and per-chapter manifests) points at an existing file.
- Inputs: `scripts/validate-links.py`; `docs/`; `context-manifests/`; per-chapter
  manifests.
- Expected output: the validator output captured as a list of broken links and
  broken manifest references, or a clean result.
- Read-only or may-edit: read-only (the script may emit to `.context/`, which is
  not committed).
- Files it may touch: none requiring edits.
- Files it must not touch: any doc, manifest, or source monolith.
- Orchestrator verification: re-run the same script and confirm identical output.

### Task D: Metadata validation

- Exact scope: Run `scripts/validate-metadata.py` and confirm every active
  document carries the required front-matter fields named in the master spec
  ("Phase 3: Add Standard Metadata"): title, document_type, status, authority,
  summary, tags, related, source_documents.
- Inputs: `scripts/validate-metadata.py`; `docs/`.
- Expected output: list of documents missing required fields, by field, or a
  clean result.
- Read-only or may-edit: read-only.
- Files it may touch: none requiring edits.
- Files it must not touch: any doc or source monolith.
- Orchestrator verification: re-run the script; spot-check two flagged files.

### Task E: Duplicate authority and archive exclusion

- Exact scope: Run `scripts/check-duplicate-headings.py` to surface repeated
  authoritative headings or duplicated long passages across active canon. Confirm
  no active index or context manifest pulls in archived material unless it is
  explicitly marked as historical reference. Confirm the pack builder
  `scripts/build-context-pack.py` refuses `archive/` paths unless explicitly
  included.
- Inputs: `scripts/check-duplicate-headings.py`; `scripts/build-context-pack.py`;
  `docs/`; `context-manifests/`; `archive/` listing.
- Expected output: duplicate-authority report (reported, not removed) plus a
  pass or fail on archive exclusion, with the offending references if any.
- Read-only or may-edit: read-only.
- Files it may touch: none requiring edits.
- Files it must not touch: any doc, manifest, script, or archived file.
- Orchestrator verification: read each flagged duplicate to judge whether it is a
  true canon duplication or an allowed index summary that links to its authority.

### Task F: Character, technology, and timeline coverage

- Exact scope: Confirm every established character in `Character Bible.md` has a
  profile under `docs/20-canon/characters/profiles/`. Confirm every technology
  rule from `Technology Rules.md` is represented, with explicit attention to any
  rule whose wording LIMITS plot convenience (hard restrictions and failure
  rules). Confirm the timeline is fully represented across historical periods and
  Book One acts, including character birth dates and knowledge or secret
  timelines.
- Inputs: `Character Bible.md`; `Technology Rules.md`; `Master Timeline.md`;
  `docs/20-canon/characters/`; `docs/20-canon/technology/`;
  `docs/20-canon/timeline/`.
- Expected output: three coverage lists (every established character to its
  profile; every technology rule, plot-limiting ones called out by name, to its
  destination; every timeline period and date set to its destination), with any
  missing item named.
- Read-only or may-edit: read-only.
- Files it may touch: none in-repo; out-of-repo scratch tables only.
- Files it must not touch: everything in-repo.
- Orchestrator verification: re-derive the established-character list from the
  source and diff it against the profiles directory listing.

### Task G: Chapter-map, decision-log, and style-guide coverage

- Exact scope: Confirm all 36 chapter plot-map entries from
  `Plot Outline and Chapter Map.md` are represented under
  `docs/30-plot/book-1/chapters/`. Confirm the Creative Decision Log is fully
  represented (every decision has a destination file and an index row, rejected
  concepts remain locatable). Confirm the Style Guide is fully represented across
  its split files. Confirm the Chapter Blueprint Template and the Development and
  Canon Guide remain available in the new tree.
- Inputs: `Plot Outline and Chapter Map.md`; `Creative Decision Log.md`;
  `Style Guide.md`; `Development and Canon Guide.md`;
  `chapter-blueprints/Chapter Blueprint Template.md`; the corresponding `docs/`
  destinations.
- Expected output: chapter-map count (must equal 36) with any missing entry
  named; decision-log coverage list; style-guide coverage list; template and
  guide presence checks.
- Read-only or may-edit: read-only.
- Files it may touch: none in-repo; out-of-repo scratch tables only.
- Files it must not touch: everything in-repo.
- Orchestrator verification: independently count the chapter files and the source
  chapter entries; confirm the count is exactly 36 on both sides.

### Task H: Chapter 1 context completeness

- Exact scope: Confirm Chapter 1 can be planned without loading the whole repo.
  Validate the Chapter 1 context manifest against the master spec "Phase 7" list,
  confirm every file it names exists, build the Chapter 1 context pack with
  `scripts/build-context-pack.py`, and confirm the pack is self-sufficient for
  blueprinting (narrative brief, premise, infrastructure decline, Greater Detroit,
  Eli's neighborhood, the relevant character profiles, the relevant technology and
  timeline files, Act One plot and Chapter 1 plot-map, relevant style files,
  relevant decisions, and the blueprint template) and that it EXCLUDES out-of-scope
  material such as Mars detail, Mara's full profile, and later-act timelines.
- Inputs: the Chapter 1 `context-manifest.yaml`; `scripts/build-context-pack.py`;
  the files the manifest names.
- Expected output: pass or fail on manifest resolution, pass or fail on
  self-sufficiency, and a list of any required-but-missing or wrongly-included
  files. The generated pack stays under `.context/` and is not committed.
- Read-only or may-edit: read-only with respect to tracked files.
- Files it may touch: may generate a pack under `.context/` (not committed).
- Files it must not touch: any tracked doc, manifest, script, or source monolith.
- Orchestrator verification: read the manifest and the generated pack heading list
  and confirm scope inclusions and exclusions by eye.

## 7. Orchestrator Responsibilities

The main instance retains and does not delegate:

- Final path choices: deciding, when a validator reports an ambiguous mapping,
  which destination path is authoritative.
- Canon-conflict resolution: any contradiction between two files surfaced by a
  validator is resolved by the orchestrator, never by an agent. Both statements
  are preserved and the resolution is recorded.
- Shared-index edits: this phase edits no indexes, but if validation reveals an
  index defect, the orchestrator alone decides the remediation route. Agents
  never edit shared indexes or manifests.
- The single shared report: only the orchestrator writes
  `migration/validation-report.md`. Agents return findings fragments; the
  orchestrator merges them. This guarantees no two agents write the same file.
- Archival approval: the orchestrator alone judges whether the report's result is
  strong enough to authorize Phase 09. Archival is never authorized by an agent.
- Acceptance of agent work: the orchestrator verifies each agent's findings (per
  the verification line in each task) before merging them, re-reading source and
  destination for any claimed loss rather than trusting the summary.
- The git checkpoint commit at the end of this phase.

## 8. Execution Steps

1. Confirm the working tree is clean and sitting at the Phase 07 checkpoint
   commit. If not, stop and resolve.
2. Confirm dependency phases 03 through 07 are complete by checking that the
   migrated tree, manifests, scripts, and Chapter 1 manifest exist.
3. Read the master spec sections "Validation Requirements", "Phase 10: Add
   Validation Tools", and "Desired End State" to align this run with the
   authority.
4. Dispatch Tasks A through H in parallel as independent read-only validators,
   honoring the rule that a validator should not be the agent who built the thing
   it validates.
5. As each validator returns, verify its findings using the per-task verification
   method, re-reading source and destination for any claimed gap before accepting.
6. Resolve, at the orchestrator level only, any canon conflicts or ambiguous path
   mappings the validators surfaced. Preserve both sides of every conflict.
7. Merge all verified findings into `migration/validation-report.md`, writing one
   pass or fail line per checklist item drawn from the master spec "Validation
   Requirements", plus a dedicated gaps section listing every failure with a
   file:line reference and a recommended remediation phase.
8. Run the Validation checks in section 10 against the report itself and against
   the tree.
9. If any item is fail, route remediation back to the responsible earlier phase
   (do not patch here), then re-run the affected validator and update the report.
10. When the report is all-pass, or the human reviewer has accepted the documented
    gaps, complete the phase per section 12 and commit per section 13.

## 9. Deliverables

- `migration/validation-report.md`, containing, at minimum:
  - One pass or fail line for every item in the master spec "Validation
    Requirements" list.
  - A gaps section enumerating each fail with file:line references on the source
    and destination side and a recommended remediation phase.
  - A duplicate-authority listing (reported, never auto-removed).
  - A conflicts listing preserving both statements of any contradiction, with the
    orchestrator's resolution noted.
  - The Chapter 1 self-sufficiency verdict.
  - An overall result line (all-pass, or pass-with-accepted-gaps, or fail) that
    gates Phase 09.
- No other repository file is created or changed by this phase.

## 10. Validation

These checks must pass before the phase is considered complete:

- `migration/validation-report.md` exists and contains exactly one pass or fail
  line for each item in the master spec "Validation Requirements" list, with no
  item omitted.
- `scripts/validate-links.py` reports no broken links across `docs/`,
  `context-manifests/`, and metadata `related` paths.
- `scripts/validate-metadata.py` reports every active document carrying the
  required front-matter fields.
- The chapter-map count is exactly 36 on both the source side and the
  `docs/30-plot/book-1/chapters/` side.
- Every established character in `Character Bible.md` maps to a profile file.
- Every plot-limiting technology rule (hard restrictions, failure rules) is
  confirmed present and is explicitly named in the report.
- No active index or manifest references archived material except where marked as
  historical reference, and the pack builder refuses `archive/` paths unless
  explicitly included.
- The Chapter 1 context pack builds successfully and is judged self-sufficient,
  with confirmed exclusion of Mars detail, Mara's full profile, and later-act
  timelines.
- The working tree contains no modifications outside `migration/validation-report.md`
  (verify with a git status check before committing).

## 11. Human Review Points

- The human reviewer reads the overall result line and the gaps section of
  `migration/validation-report.md`.
- The human reviewer must explicitly sign off before Phase 09 archival runs.
  Archival is irreversible in spirit, since it removes the source monoliths from
  the live root, so it proceeds only on an all-pass result or on human acceptance
  of each documented gap.
- Any canon conflict surfaced during validation is escalated to the human for a
  decision; the orchestrator preserves both statements pending that decision.
- Any proposal to treat a documented gap as acceptable rather than remediating it
  requires explicit human approval recorded in the report.

## 12. Completion Criteria

- [ ] `migration/validation-report.md` exists with one pass or fail line per
      master-spec "Validation Requirements" item.
- [ ] Source-heading coverage confirmed: every source heading has a destination.
- [ ] Source-to-destination content verified: no canonical section lost or
      silently altered; Mermaid blocks remain valid.
- [ ] Link validation clean across docs, indexes, manifests, and metadata paths.
- [ ] Metadata validation clean: required fields present on active documents.
- [ ] Duplicate-authority review complete and reported (nothing auto-removed).
- [ ] Archive exclusion confirmed: archived files excluded from normal context;
      pack builder refuses `archive/` unless explicitly included.
- [ ] Character coverage confirmed: every established character has a profile.
- [ ] Technology-rule coverage confirmed, with plot-limiting rules named.
- [ ] Timeline coverage confirmed across periods, acts, dates, and knowledge or
      secret timelines.
- [ ] All 36 chapter-map entries represented.
- [ ] Decision Log coverage confirmed (rejected concepts remain locatable).
- [ ] Style Guide coverage confirmed; blueprint template and development guide
      remain available.
- [ ] Chapter 1 context completeness confirmed: Chapter 1 can be planned without
      loading the whole repository.
- [ ] No file changed outside `migration/validation-report.md`.
- [ ] Human reviewer has signed off on the overall result or accepted the gaps.

## 13. Checkpoint

This phase ends with a git commit before Phase 09 begins. Only
`migration/validation-report.md` should be staged; confirm with a git status
check that nothing else changed, and do not stage generated `.context/` packs or
out-of-repo scratch files.

Suggested commit message:

```text
phase-08: add migration validation report

Independent read-only validation of the migrated tree against the source
monoliths. One pass or fail line per validation-requirements item, with a
gaps section. Gates phase-09 archival.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

Do not proceed to Phase 09 (archival of source monoliths) until this commit
exists and the report shows an all-pass result or human-accepted gaps.
