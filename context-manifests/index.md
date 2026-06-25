---
title: "Context Manifests Index"
document_type: "index"
status: "active-support"
authority: "governance"
summary: "Navigation index for the task-level context manifests of The Unnecessary. Describes the six workflow manifests under context-manifests/, states which manifest to open for which job, and links to each. It summarizes and links only; it restates no canon and lists no archive paths."
tags:
  - index
  - context-manifests
  - tooling
  - navigation
related:
  - "./create-chapter-blueprint.yaml"
  - "./draft-chapter.yaml"
  - "./revise-chapter.yaml"
  - "./continuity-check.yaml"
  - "./canon-revision.yaml"
  - "./technology-research.yaml"
source_documents:
  - "/home/codingbutter/Novel/migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Context Manifests Index

A context manifest names the exact subset of documents to load for one common
workflow, so a session can build a context pack from only the listed files and work
on a single job without loading the whole repository. This index describes the six
task-level manifests that live beside it under `context-manifests/`, tells you which
one to open for which job, and links to each.

These manifests are an operating-support layer, not canon. They point at files; they
never restate or change canon. The bibles outrank memory and the graph on every
conflict, and no manifest silently resolves a conflict between two authority files.
No manifest references any archived material; archived monoliths are historical
reference only and never appear in normal task context.

## How to use a manifest

1. Read `CLAUDE.md` and identify the task you are about to perform.
2. Open the matching manifest below and read its `purpose`.
3. Build a context pack from the manifest's `required_files`, plus the
   `optional_files` that apply to the specific chapter or question. The
   `exclude_files` list states what to keep out, and `loading_order` gives the
   recommended read sequence.
4. Honor the manifest's `canon_rules` while you work, and run the
   `relevant_validation_checks` it names when you finish.

Each manifest follows the same schema: `task_name`, `purpose`, `required_files`,
`optional_files`, `exclude_files`, `loading_order`, `expected_output`,
`canon_rules`, and `relevant_validation_checks`.

## Which manifest for which task

| Task | Manifest file | Purpose |
|---|---|---|
| Plan a single chapter blueprint | [create-chapter-blueprint.yaml](./create-chapter-blueprint.yaml) | Assemble the entry layer, the relevant plot and act context, the blueprint template, and a representative slice of canon plus current continuity to plan one chapter, without auto-loading every profile, technology file, or chapter. |
| Draft chapter prose from a blueprint | [draft-chapter.yaml](./draft-chapter.yaml) | Load the prose-craft style files, the relevant character voices and profiles, the relevant technology files, current continuity, and the chapter plot-map entry so one chapter can be drafted faithfully to its approved blueprint. |
| Revise an existing chapter draft | [revise-chapter.yaml](./revise-chapter.yaml) | Pair the style revision checklist with the chapter's blueprint, the drafted chapter, the relevant continuity, and the canon the revision must stay faithful to, so a revision pass resolves flagged items without introducing new plot. |
| Check a chapter against continuity | [continuity-check.yaml](./continuity-check.yaml) | Cross-check character states, knowledge states, relationship status, technology state, and the setups-and-payoffs ledger against the canonical timeline, surfacing any contradiction with its controlling authority. |
| Make a recorded change to canon | [canon-revision.yaml](./canon-revision.yaml) | Load the narrative brief and the canon hierarchy first, then the specific canon files affected, the decision-log index and the decisions touched, and the plot, manuscript, and continuity files the change ripples into, to produce one sourced revision plus its decision record. |
| Answer a technology question | [technology-research.yaml](./technology-research.yaml) | Load the technology canon index and the specific technology files a question touches, plus the canon hierarchy, to return a plausibility finding within established rules rather than a silent change to a technology rule. |

## Notes on shared behavior

- The manifests for chapter work name only representative relevant files for the
  chapter under work. The per-chapter manifest at
  `docs/40-blueprints/book-1/chapter-XX-title/context-manifest.yaml` narrows those
  to the exact set a given chapter needs and is the authority on the final
  per-chapter selection.
- No manuscript chapter is approved yet, so the blueprint and manuscript paths in
  several manifests are listed under `optional_files` as placeholders the context
  pack builder resolves and warns on when absent. They become the de facto required
  inputs once they exist on disk.
- Research notes under `docs/70-research/` are intentionally deferred and rank below
  the bibles. Where the canon-revision and technology-research manifests reference
  research, they do so under `optional_files` only, so the builder warns rather than
  fails when no research file exists.
