---
title: "validation-report"
document_type: "migration-report"
phase: "08"
title_text: "Phase 08: Validation Report"
status: "complete"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
overall_result: "ALL PASS"
---

# Phase 08: Validation Report

> Independent review gate for the migration of "The Unnecessary". One pass or fail line per master-spec "Validation Requirements" item, with evidence. Gaps found during validation were remediated in place (this is an autonomous single-operator run) and are listed in section 3 with their fix commits. Master spec `migration/REPOSITORY-REORGANIZATION-SPEC.md` is authoritative.

## Overall result: ALL PASS

Every master-spec Validation Requirement passes. Four independent read-only validator agents (content fidelity and coverage), three deterministic stdlib validators (`validate-links.py`, `validate-metadata.py`, `check-duplicate-headings.py`), and the context-pack builder were run against the migrated tree and the original source monoliths. The migration preserved every canonical fact, the new structure is internally linkable, and Chapter 1 can be planned from a bounded context (~45,000 tokens) without loading the whole repository.

## 1. Validation Requirements (one line per master-spec item)

| # | Requirement | Result | Evidence |
|---|---|---|---|
| 1 | Every active source section has a destination | PASS | Heading-coverage sweep over all 10 monoliths; cross-domain overviews summarize-and-link per Phase 12; framing sections routed (section 3). |
| 2 | No canonical section was lost | PASS | Independent canon-fidelity validator: hard restrictions, failure rules, and sampled profiles byte-identical to source (only section-boundary `---` dropped). Planning-fidelity validator: chapters, style, decisions verbatim. |
| 3 | Source-monolith headings reconcile with split-file headings | PASS | Every meaningful heading maps to a destination or is an intentional summarize-and-link; version labels preserved in the archived monoliths (Phase 09). |
| 4 | Mermaid diagrams remain valid fenced blocks | PASS | All 4 Master Timeline Mermaid blocks present and byte-faithful: `timeline` and `flowchart TD` in `timeline/index.md`, `gantt` in `book-1/index.md`, `flowchart LR` in `book-1/character-knowledge-timeline.md`; fence balance verified. |
| 5 | Relative links work | PASS | `scripts/validate-links.py` exit 0: no broken Markdown link, `related` path, or `source_documents` path across `docs/` and `context-manifests/`. |
| 6 | Context manifests reference existing files | PASS | All 6 task manifests + the Chapter 1 manifest parse and every required/optional path resolves on disk; no `archive/` path in any required/optional list. |
| 7 | Archived files excluded from normal context | PASS | `build-context-pack.py` refuses `archive/` paths unless explicitly listed with `--allow-archive` (verified: exit 1, refusal message). No manifest or active index references archived material as canon. |
| 8 | Active documents carry status metadata | PASS | `scripts/validate-metadata.py` exit 0: every active document declares all 8 required fields (title, document_type, status, authority, summary, tags, related, source_documents). Two intentional template stubs are skipped. |
| 9 | Character Bible material for every established character | PASS | Independent coverage validator re-derived 13 established characters (11 human + 2 nonhuman) from the Character Bible and confirmed a non-stub profile for each under `characters/profiles/`. |
| 10 | All 36 chapter plot-map entries represented | PASS | 36 source `## Chapter N` entries map to 36 files `chapters/chapter-01.md` through `chapter-36.md`, each a high-level plot-map entry (no scene breakdowns), distinct from blueprints. |
| 11 | Chapter Blueprint Template intact | PASS | `docs/40-blueprints/_templates/chapter-blueprint-template.md` heading count 111 equals the source 111; Mermaid block preserved. |
| 12 | Creative Decision Log fully represented | PASS | 44 decision files (001 to 044, no gaps) plus an index table, `rejected-concepts.md`, `open-decisions.md`, and `about.md` (how-to-use, entry template, update procedure, final principle, affected-docs). Statuses preserved verbatim, including the five "Locked for Current Workflow". |
| 13 | Style Guide fully represented | PASS | All source style sections map across the 11 `docs/10-vision/style/` files plus index; per-character voices and prohibited-patterns/cliches verbatim. |
| 14 | Novel Development and Canon Guide available | PASS | Full guide relocated intact to `docs/00-governance/novel-development-guide.md`; the derived `context-loading-guide.md` and `canon-hierarchy.md` also present. |
| 15 | Chapter 1 plannable without loading the whole repository | PASS | `build-context-pack.py` builds the Chapter 1 pack at ~44,778 tokens from 37 scoped files; excludes Mars detail (`mars-and-aurelia.md`, `mars-technology.md`), Mara's profile, and act-2/3/4 timelines. |

## 2. Independent validator verdicts

Four independent read-only validators (not the agents that built the tree) each returned PASS:

- Canon content fidelity: hard plot restrictions and failure rules verbatim (all 10 restrictions named, including "AI Cannot Solve Moral Conflict Mathematically"); sampled profiles (Eli, Kade, Morrow) verbatim; Morrow profile links to technology rather than duplicating capability lists; 4 Mermaid blocks byte-faithful.
- Planning and style fidelity: 36 chapter plot-map entries (no scene breakdowns); 11 style files cover every source section verbatim; 44 decisions with statuses preserved.
- Character, technology, timeline coverage: 13 characters covered; every plot-limiting technology rule present and named (the Foundational 13-item "cannot" list, the 10 hard plot restrictions, the 5 failure-rule categories); timeline complete across historical periods 2026 to 2052, Book One acts 1 to 4 and all 30 days, birth dates, knowledge timeline, secret timeline.
- Chapter-map, decision-log, style, template, guide coverage: 36 = 36 chapters, 44 = 44 decisions with index and rejected concepts locatable, all style sections represented, template intact, dev guide available.

## 3. Gaps found and remediated

This run remediated each gap in place rather than deferring, then re-validated to green. Fix commits:

- Vision domain index `docs/10-vision/index.md` was missing (referenced by the canon and governance indexes). Created. (commit 4e2641c)
- 16 continuity files lacked the `title` front-matter field. Added. (commit 4e2641c)
- 9 decision files had `related` paths pointing at non-existent canon paths (`characters/<name>.md` instead of `characters/profiles/<slug>.md`, and a non-existent `master-timeline.md`). Corrected to resolving paths. (commit 4e2641c)
- Character Bible framing sections (Core Character Principles, Primary Cast, Nonhuman Characters, Character Continuity Fields, Final Character Standard) and Decision Log meta sections (How to Use, Decision Entry Template, Future Update Procedure, Final Principle, Existing Documents Affected) had no active destination. Routed verbatim to `characters/principles.md` and `decision-log/about.md`. The Story Bible "Core Mystery / Moral Problem / Original Purpose" headings were classified as Morrow-overview subsections already linked (no gap). (commit 58f446e)
- Chapter-map titles were inconsistent (chapters 09 to 36 used H2 while 01 to 08 used H1). Normalized all 36 to H1. (commit 10ba366)

After remediation, `validate-links.py` and `validate-metadata.py` both exit 0.

## 4. Duplicate-authority report

`scripts/check-duplicate-headings.py` (report only, edits nothing) found NO cross-domain duplicated long passages. The only repeated headings are short structural skeletons by design (for example "Related indexes", "Common Tasks") and index navigation, which are not duplicate authority. The cross-domain entities Morrow and Crown are split by fact type (behavior in the character profile, architecture in the technology file) and linked, not duplicated.

## 5. Conflicts

The six conflicts found in the Phase 01 audit (C1 through C6) were resolved before the canon split (commit ea61dc2) and are recorded in `migration/conflicts-found.md`. No new canon conflict was surfaced during validation. There are no open conflicts at handoff.

## 6. Chapter 1 self-sufficiency verdict

PASS. The Chapter 1 context pack builds from `docs/40-blueprints/book-1/chapter-01-no-signal/context-manifest.yaml` at approximately 44,778 tokens, drawing on the narrative brief, world premise and infrastructure decline, Greater Detroit and Eli's neighborhood, the Chapter 1 character profiles (Eli, Lena, Nolan, Talia) and relationship map, the relevant infrastructure and medicine technology, the pre-book and Act One timelines, the Act One plot file and Chapter 1 plot-map entry, the relevant style files, ten relevant decisions, the blueprint template, and the Chapter 1 continuity baselines. It excludes Mars detail, Mara's full profile, and later-act timelines. Chapter 1 can be planned without loading the whole repository.

## 7. Tooling results

| Tool | Result |
|---|---|
| `scripts/validate-links.py` | PASS (exit 0) |
| `scripts/validate-metadata.py` | PASS (exit 0) |
| `scripts/check-duplicate-headings.py` | report only; no true duplicate authority |
| `scripts/build-context-pack.py` | builds Chapter 1 pack (~45k tokens); refuses archive paths unless explicit |

All four scripts run on the Python standard library alone (no third-party imports).

## 8. Gate

This report shows an all-pass result and authorizes Phase 09 (archival of the source monoliths). Phase 09 must re-run the link validator after the archival move and update `source_documents` paths to the new `archive/source-monoliths/` locations.
