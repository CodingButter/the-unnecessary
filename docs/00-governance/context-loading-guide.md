---
title: "Context Loading Guide"
document_type: "governance-guide"
status: "active"
authority: "governance"
summary: "A short reading guide for the novel. It tells a contributor what to read for each task, the order of authority, how to handle contradictions, and how to tell established canon from planned material. Derived from the full development guide; it does not replace it."
tags: ["governance", "context-loading", "canon", "reading-guide", "workflow"]
related:
  - "canon-hierarchy.md"
  - "index.md"
source_documents:
  - "Development and Canon Guide.md"
---

# Context Loading Guide

This is the short reading guide for the novel **The Unnecessary**. It exists so a
contributor or AI loads the right material for a task rather than loading the whole
repository. It is derived from the full operating manual and does not replace it. For the
complete operating manual, read `Development and Canon Guide.md` (root monolith; later
phases split it into the governance tree). For the full authority ranking and per-domain
ownership, read `canon-hierarchy.md` (sibling in this directory).

Two rules sit above everything below. First, do not load every file blindly when the task
is narrow; load enough to avoid obvious contradictions and no more. Second, the operational
entry point for any task is its context manifest, not this guide. The manifests name the
exact files a task needs.

## 1. What to read for each task

Start from the context manifest for your task. Each manifest in `context-manifests/`
(pending: created in a later phase) lists the exact files to load and in what priority.
Open the manifest first, then load what it names. The table below is the quick routing map;
the manifest is the authority on the precise file set.

| Task | Start with the manifest | Then load, in brief |
| --- | --- | --- |
| Create a chapter blueprint | `context-manifests/create-chapter-blueprint.yaml` (pending: created in a later phase) | narrative brief, story bible, character bible, technology rules, master timeline, plot outline, blueprint template, continuity ledger, previous blueprint, previous approved chapter |
| Draft a chapter | `context-manifests/draft-chapter.yaml` (pending: created in a later phase) | approved blueprint, style guide, relevant character profiles, relevant technology rules, previous approved chapter, current continuity ledger, relevant brief and bible sections |
| Revise a chapter | `context-manifests/revise-chapter.yaml` (pending: created in a later phase) | current manuscript chapter, approved blueprint, style guide, the revision goal, continuity ledger, feedback already accepted |
| Check continuity | `context-manifests/continuity-check.yaml` (pending: created in a later phase) | the approved chapters involved, continuity ledger, master timeline, character bible, relevant blueprints |
| Develop a character | `context-manifests/character-development.yaml` (pending: created in a later phase) | narrative brief, story bible, character bible, master timeline, plot outline, relevant continuity entries; technology rules only if the role depends on technical access |
| Research a technical question | `context-manifests/technology-research.yaml` (pending: created in a later phase) | relevant technology rules section, research and plausibility ledger, the exact story need, the year and location, and whether the goal is realism, plausibility, or speculation |
| Revise canon | `context-manifests/canon-revision.yaml` (pending: created in a later phase) | the canon files affected, the decision log, every document the change propagates to |

When a manifest does not yet exist, fall back to the per-task reading lists in
`Development and Canon Guide.md` under its task-specific context packages. The manifests
are the intended destinations; until they are written, the full guide is the operating
source.

## 2. Authority hierarchy

Authority is not one universal ladder. It depends on the kind of fact in question. In broad
terms: an approved manuscript chapter is the highest authority for what happened, an
explicitly approved revision overrides older canon, and the continuity ledger is the quick
operational reference that the manuscript still outranks. By subject, the narrative brief
owns creative identity, the story bible owns world canon, the character bible owns people,
the technology rules own capability, the master timeline owns dates and event order, the
plot outline owns book structure, the individual blueprint owns scene order inside its
chapter, and the style guide owns prose execution.

This is the short form. For the full ranked order and the complete per-domain ownership
table, read `canon-hierarchy.md` (sibling in this directory). When a conflict touches
authority, defer to that file.

## 3. How to handle contradictions

When two documents disagree, do not silently choose one and do not average them together.
Flag the contradiction and preserve both sides. State which documents conflict, what the
conflict is, which authority normally controls that kind of fact, whether approved
manuscript prose is affected, and a recommended resolution. Then stop.

Resolution is not yours to perform inside the canon files. Only the orchestrator or the
author decides how a conflict resolves, and the resolution propagates to every affected
document and, when it touches major canon, into the decision log. A flagged conflict is
logged, not fixed. Note also that some apparent contradictions are intentional, such as
character misinformation, corporate propaganda, unreliable memory, or deliberate deception;
preserve those rather than collapsing them, and let the source of each statement stay clear.

## 4. How to distinguish canon from planning

Established fact and planned intention do not carry equal weight. Sort every file you load
into one of these three buckets before you trust it.

- **Established canon.** Approved manuscript chapters and active canon files (the brief, the
  bibles, the technology rules, the timeline, and the continuity ledger that summarizes
  approved prose). These are established fact, authoritative by subject. Treat them as what
  is already true.
- **Approved plans, not yet events.** The plot outline, the chapter map, and the individual
  chapter blueprints. These are authoritative for current drafting but describe intended
  future events that have not yet appeared in approved prose. They are easier to revise than
  established canon, and a continuity check must never use a planned future event as proof
  of what has already happened.
- **Never canon.** Anything under the archive. Archived drafts, replaced canon, and
  abandoned concepts are retained for history only and must never be treated as active
  canon.

In short: approved manuscript and active canon are established fact by subject; plot files
and blueprints are approved plans, not established events; archived files are never canon.
