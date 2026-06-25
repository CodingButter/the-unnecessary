---
title: "Decision 047: Change Propagation and Pack-Freshness Discipline"
document_type: "decision"
status: "active"
authority: "governance"
summary: "When a fact changes, update its owner first, then every Affected Document the governing decision lists, then rebuild any context packs. Context packs are regenerated artifacts and are never trusted stale; tooling enforces this so propagation does not depend on memory."
tags: ["decision", "workflow", "tooling", "consistency", "context-pack"]
related:
  - "../../novel-development-guide.md"
  - "../index.md"
source_documents:
  - "docs/00-governance/decision-log/decisions/046-chapter-authorship-pipeline.md"
---

## Decision 047: Change Propagation and Pack-Freshness Discipline

**Status:** Locked for Current Workflow
**Category:** Workflow and tooling

### Decision

When any canonical or planning fact changes, it is propagated in this order, and the tooling enforces the parts that can be enforced:

1. Change the OWNER of the fact first (the single owner named in `docs/00-governance/canon-hierarchy.md`; for a chapter's structure that is the plot-map, for dates the timeline, and so on).
2. Update every document listed in the governing decision's "Affected Documents" section. Decisions MUST list their affected documents so propagation targets are written down, not remembered.
3. Rebuild any context pack that includes a changed source. A context pack under `.context/` is a frozen concatenation of sources; it goes stale the instant any source changes. A stale pack is never consumed.
4. Re-run the validators (`validate-links`, `validate-metadata`) and, for a chapter, a fresh Gemini critique on a rebuilt pack.

### Reason

The Chapter 1 Gemini critique flagged a high-severity contradiction between the plot-map and the blueprint. The plot-map had in fact already been reconciled (Decision 045); the critique ran against a pack snapshot built before that fix, so it read out-of-date canon. The real failure was a stale frozen copy, plus reliance on a person remembering every place a fact lived. Both are removed by making freshness a property of the tooling rather than a discipline.

### Consequences

Adds `scripts/check-pack-fresh.py`, which compares a pack's modification time against every source its manifest lists and reports STALE (nonzero exit) if any source is newer. `scripts/gemini-critique.py` gains a `--manifest` flag that rebuilds the pack before critiquing, so a critique can never run against a stale snapshot. The reusable `write-chapter` workflow rebuilds the pack in its Prep stage and critiques with `--manifest`, so the in-pipeline path is fresh by construction. Context packs remain git-ignored and regenerable; they are never a source of truth.

### Affected Documents

- `scripts/check-pack-fresh.py`
- `scripts/gemini-critique.py`
- `.claude/workflows/write-chapter.js`
- `docs/00-governance/decision-log/decisions/046-chapter-authorship-pipeline.md`

### Reconsider Only If

Context packs become content-addressed (hash-stamped) such that staleness is detected by content rather than modification time, in which case the mtime check is replaced rather than removed.
