---
title: "Governance Index"
document_type: "index"
status: "active-support"
authority: "governance"
summary: "Indexes the governance directory: the process and navigation layer that tells a reader where authority lives, what to load for a task, and how to resolve conflicts. It summarizes and links; it never owns a story fact."
tags:
  - index
  - governance
related:
  - "../20-canon/index.md"
  - "../10-vision/index.md"
source_documents:
  - "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Governance Index

This directory is the governance layer for the novel **The Unnecessary**. It holds
the process and navigation files that sit above canon: the ranked authority order,
the per-task reading guide, the operating manual, the memory conventions, and the
decision log. Nothing here establishes a story fact. These files describe how to
work, where authority lives, and how to handle contradictions. For any load-bearing
story fact, defer to the owning canon file under `docs/20-canon/`
(pending: created in a later phase).

Read first: [canon-hierarchy.md](canon-hierarchy.md). It defines which file controls
which kind of fact, in what order authority is applied, and what to do when two files
disagree. Once you understand the authority order, use
[context-loading-guide.md](context-loading-guide.md) to decide what to load for your
specific task.

## Files

This table is a navigation aid. Each row summarizes a file and points at it as the
authority for detail. When a summary here and the linked file disagree, the linked
file wins and this index is corrected. Targets a later phase has not created yet are
marked pending.

| File | Summary | Authority or status | Load when |
| ---- | ------- | ------------------- | --------- |
| [canon-hierarchy.md](canon-hierarchy.md) | Defines the ranked authority order, the per-domain ownership of facts, and the flag-and-preserve conflict rule. Governance scaffolding; establishes no story fact. | active (governance) | Resolving which file owns a fact, ranking two sources that disagree, or handling any contradiction. Read this first in the directory. |
| [context-loading-guide.md](context-loading-guide.md) | A short reading guide: what to read per task, the authority hierarchy in brief, how to handle contradictions, and how to tell established canon from planned material. Derived from the development guide; does not replace it. | active (governance) | Starting any task and deciding what to load without reading the whole repository. |
| [index.md](index.md) | This file. Indexes the governance directory and links to related domain indexes. A pointer, not a canon record. | active-support (governance) | Orienting in the governance directory or finding the right governance file to open next. |
| novel-development-guide.md (pending: created in a later phase) | The full operating manual: document responsibilities, the complete canon hierarchy, the canon versus planning distinction, per-task reading guidance, drafting discipline, and contradiction handling. Relocated from `Development and Canon Guide.md` (root monolith) in a later phase. | active (governance), pending | Needing the complete operating manual rather than the short guide, or any process detail the context-loading guide summarizes but does not fully carry. |
| memory-conventions.md (pending: created in a later phase) | The persistent-memory spec: what to store while drafting, the metadata schema, and the recall-then-draft discipline. Relocated from `Memory Conventions.md` (root monolith) in a later phase; orchestrator-decided destination is `docs/00-governance/memory-conventions.md`. | active-support (governance), pending | Storing or recalling project memory while drafting, or checking the memory metadata schema. |
| decision-log/ (pending: created in a later phase) | The log of explicitly approved creative revisions and the reasons behind them. A change recorded here is enacted by editing the owning canon file and affected prose, not by the governance layer asserting a fact. The subtree carries its own `decision-log/index.md`. | active (governance), pending | Recording a major approved revision, or tracing why a canon decision was made. |

## Related indexes

- [canon index](../20-canon/index.md) (pending: created in a later phase) - the split
  canon (world, characters, technology, timeline), authoritative by subject. Governance
  ranks below canon on every story fact.
- [vision index](../10-vision/index.md) (pending: created in a later phase) - the
  narrative brief and the style files, owning creative identity and prose execution.
