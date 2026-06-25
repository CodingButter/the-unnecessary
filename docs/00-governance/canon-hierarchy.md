---
title: "Canon Hierarchy"
document_type: "governance-guide"
status: "active"
authority: "governance"
summary: "Defines the ranked authority order for canon, the per-domain ownership of facts, and the rule that conflicts are flagged and preserved rather than silently merged. This is governance scaffolding; it governs process and never establishes story facts."
tags:
  - governance
  - canon
  - authority
  - conflict-handling
related:
  - "context-loading-guide.md"
  - "index.md"
source_documents:
  - "Development and Canon Guide.md"
---

# Canon Hierarchy

This document tells a reader or a future LLM which file controls which kind of
fact, in what order authority is applied, and what to do when two files
disagree. It is governance scaffolding. It does not contain story canon and it
must never silently do the job of a canon file. For any load-bearing story
fact, defer to the owning canon file named below.

There is no single universal ordering that resolves every contradiction.
Authority depends on the kind of fact involved. The ranked order below applies
when documents of different kinds disagree; the per-domain ownership table
applies when the question is simply which file owns a given subject.

## 1. Ranked Authority Order

When two sources disagree, apply this order from highest to lowest.

1. **Approved manuscript is established canon.** An event clearly shown in
   approved prose is hard canon. The manuscript is the final story the reader
   experiences. If a plan or a profile contradicts an approved chapter, the
   plan is usually the thing that must change. The manuscript is changed only
   when the contradiction reveals a genuine story problem. Approved chapters
   live under `docs/50-manuscript/` (pending: created in a later phase).

2. **Active canon files are authoritative by subject.** The split canon under
   `docs/20-canon/` is the working authority for world facts, characters,
   technology, and dates, each owned by its own subject file (see the ownership
   table below). These files are authoritative for current drafting. They rank
   below approved manuscript prose, because prose that has been approved
   outranks the plans and profiles that fed it. Canon directories:
   `docs/20-canon/world/`, `docs/20-canon/characters/`,
   `docs/20-canon/technology/`, and `docs/20-canon/timeline/` (all pending:
   created in a later phase).

3. **Plot files and blueprints are approved plans, not established events.**
   The plot files under `docs/30-plot/` and the chapter blueprints under
   `docs/40-blueprints/` describe what is intended to happen. They are
   authoritative for drafting direction and they are easier to revise than
   established canon, but a planned event is not an established event until it
   appears in an approved chapter. Do not cite a plot beat or a blueprint as a
   fact the reader already knows. These directories are pending: created in a
   later phase.

4. **Process and governance documents govern process, not story facts.** The
   files under `docs/00-governance/`, including this one, the
   `context-loading-guide.md`, and the indexes, describe how to work, where
   authority lives, and how to resolve conflicts. They never establish,
   override, or quietly edit a story fact. An explicitly approved creative
   revision recorded in the decision log under
   `docs/00-governance/decision-log/` (pending: created in a later phase)
   changes canon, but the change is enacted by editing the owning canon file
   and the affected prose, not by the governance layer asserting the fact
   itself.

5. **Archived files are never active canon.** Anything under `archive/` is
   superseded source material kept for provenance only. It must never be loaded
   as active canon or used to resolve a contradiction, even when it once held
   the same content now split into the active canon files.

## 2. Per-Domain Ownership

When the question is which file owns a fact, use this table. Each fact type has
one primary home. Other files may reference that fact, but they link to the
owner rather than restating it.

| Fact type | Primary owner | Path (pending unless noted) |
|---|---|---|
| Character facts (history, personality, motivation, relationships, arc) | Character profiles | `docs/20-canon/characters/profiles/` (pending: created in a later phase) |
| Technology capabilities and limits | Technology files | `docs/20-canon/technology/` (pending: created in a later phase) |
| Dates and chronology | Timeline files | `docs/20-canon/timeline/` (pending: created in a later phase) |
| Chapter order and sequence | Plot files | `docs/30-plot/book-1/` (pending: created in a later phase) |
| Scene-level facts | Blueprints and continuity | `docs/40-blueprints/` and `docs/60-continuity/` (pending: created in a later phase) |
| Prose rules | Style files | `docs/10-vision/style/` (pending: created in a later phase) |
| Reasons behind decisions | Decision files | `docs/00-governance/decision-log/decisions/` (pending: created in a later phase) |

### The Index Rule

Indexes summarize and link. An index file never owns a fact. It may carry a one
or two sentence summary of a file, but it must clearly point at the linked file
as the authority for details. If an index summary and the file it points to
disagree, the file controls and the index is corrected.

### The Cross-Domain Rule: Link, Do Not Duplicate

When a concept crosses domains, link to each owner rather than copying full
sections into one place. Duplication is how two files drift apart and produce a
silent contradiction.

The canonical example is Morrow. A single overview should summarize Morrow's
role briefly and then link out:

- **Behavioral identity** lives in the character profile
  `docs/20-canon/characters/profiles/morrow.md` (pending: created in a later
  phase).
- **Architecture and capabilities** live in the technology file
  `docs/20-canon/technology/ai/morrow.md` (pending: created in a later phase).
- **Book One progression** lives in the plot files under
  `docs/30-plot/book-1/` (pending: created in a later phase).

The overview owns none of these. It summarizes and points. The owners hold the
detail.

## 3. Conflict Rule: Flag and Preserve, Never Silently Merge

When two files disagree, the conflict is recorded, not quietly fixed. Both
statements are preserved. The conflict is logged in
`migration/conflicts-found.md` with, at minimum:

- which documents conflict,
- what the conflict is,
- which authority normally controls that type of fact,
- whether any approved manuscript prose is affected,
- a recommended resolution.

Do not average the two versions together and do not pick a winner inside a
canon file on your own. Both sides stay on the record until the conflict is
resolved deliberately. Only the orchestrator resolves a conflict; an agent
flags it and stops. Resolution, when it comes, is enacted by editing the owning
canon file and recording the decision in the decision log, never by the
governance layer asserting a fact it does not own.
