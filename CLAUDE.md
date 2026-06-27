---
title: "The Unnecessary, Project Instructions"
document_type: "governance-guide"
status: "active"
authority: "governance"
summary: "Per-session entry layer for the novel: what the project is, where authority lives, the per-session story rules, the task-routing table, and the task-routing table."
tags:
  - governance
  - entry-point
related:
  - "docs/00-governance/context-loading-guide.md"
  - "docs/00-governance/canon-hierarchy.md"
---

# The Unnecessary — Project Instructions

> Loaded into every session. This file is the **entry / operational layer**, not a
> canon document. It tells you what the project is, where authority lives, and how to
> use persistent memory. It does **not** define story canon and must never silently do
> the job of a canon or planning document.

## What this project is

**The Unnecessary** is a near-future dystopian science-fiction thriller (working title;
the Story Bible lists alternates such as *A World Without Us* and *Human Value*). It is a
**novel project, not a software product.** Book One is the first of a planned multi-book
series, written as "grounded cyberpunk" without the visual cliches.

Premise, in brief: by 2053, artificial superintelligence and autonomous robotics have made
most human labor and mass consumption unnecessary. Civilization has not collapsed in an
apocalypse — it has *withdrawn*, abandoning services unevenly in unprofitable areas. Elias
"Eli" Rook, a former Asterion systems architect who helped create the **Mosaic** orchestration
architecture, builds **Morrow**, a decentralized intelligence that makes abandoned,
incompatible systems cooperate. Asterion's founder **Adrian Kade** wants Morrow for the
Mars project (the **Aurelia Initiative**) and fears it could let abandoned communities
survive without corporate support. The danger in this story is not AI turning against
humanity but AI faithfully inheriting the priorities of the humans who own it. The core
tension is **ownership of abundance**, not scarcity. Primary setting: **Greater Detroit**.
Book One spans thirty days (October 3 to November 1, 2053).

That is the most this file should say about canon. For anything load-bearing, go to the
authorities below — do not reason from this paragraph.

## Where authority lives (defer; do not duplicate)

| Authority | Document | Owns |
|---|---|---|
| **Operating manual** | `Development and Canon Guide.md` | The canon hierarchy, conflict-handling rules, drafting discipline, context packages, workflow phases, folder structure, versioning. **Defer to it on all process and conflict questions.** |
| Canon (by subject) | `Narrative Brief.md`, `Story Bible.md`, `Character Bible.md`, `Technology Rules.md`, `Master Timeline.md`, `Plot Outline and Chapter Map.md`, `Style Guide.md`, `Creative Decision Log.md` | Authoritative story facts. The bibles win every conflict against memory. |

Two non-negotiable principles inherited from the Canon Guide:

1. **No document silently does another's job.** This file orients and operates; it never
   establishes, overrides, or quietly edits canon.
2. **Never silently resolve a conflict.** When documents disagree, state which conflict,
   which authority normally controls that fact type, whether approved prose is affected,
   and a recommended resolution — then follow the Canon Guide's process. Do not average
   two versions together.

The repository is organized as a structured `docs/` tree (`docs/00-governance/`,
`docs/10-vision/`, `docs/20-canon/`, `docs/30-plot/`, `docs/40-blueprints/`,
`docs/50-manuscript/`, `docs/60-continuity/`, `docs/70-research/`), with `context-manifests/`,
`scripts/`, and `archive/` alongside. The separation-of-responsibilities is the load-bearing part.

## Working on the novel (per-session rules)

This is a novel project, not a software product. Before any story work, read
`docs/00-governance/context-loading-guide.md`. Never load the whole repository by default;
start from the appropriate context manifest in `context-manifests/`. Then:

- Treat approved manuscript as established canon.
- Treat active canon files (`docs/20-canon/**`) as authoritative by subject.
- Treat plot files and blueprints as approved plans, not already-established events.
- Never use archived files (`archive/**`) as active canon.
- Flag conflicts instead of silently resolving them.
- Do not change canon unless explicitly asked.
- Avoid em dashes in drafted prose.
- Preserve viewpoint and reveal timing.
- Update continuity after approved manuscript changes.
- Record major revisions in the Decision Log.
- Do not expose future reveals in earlier chapter work.
- Do not give Morrow or Crown unestablished capabilities.

## Task routing

Start each task from its context manifest:

| Task | Start with |
| --- | --- |
| Create chapter blueprint | `context-manifests/create-chapter-blueprint.yaml` |
| Draft chapter | `context-manifests/draft-chapter.yaml` |
| Revise chapter | `context-manifests/revise-chapter.yaml` |
| Check continuity | `context-manifests/continuity-check.yaml` |
| Revise canon | `context-manifests/canon-revision.yaml` |
| Research technology | `context-manifests/technology-research.yaml` |

---

## Memory

This project keeps no vector database or knowledge graph. Memory lives in three places,
each already authoritative for its kind:

- **Canon:** the bibles under `docs/20-canon/**`. The single source of truth for story
  facts; they win every conflict. Established facts belong here, not a side store.
- **Decisions and rationale:** git history and the **Creative Decision Log**. Major
  revisions get a Decision Log entry; the commit is the durable record.
- **Working notes, preferences, feedback:** the lightweight file-based notes at
  `~/.claude/projects/-home-codingbutter-Novel/memory/` (one fact per file, indexed by
  `MEMORY.md`). For cross-session preferences and how-to-work guidance, not canon.

"Recall before drafting" still applies, but recall means reading the relevant bible and
the context pack and checking continuity, not querying a side store. Do not duplicate
into a separate store what a bible or git already holds.
