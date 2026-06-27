---
title: "Character Relationship Diagrams"
document_type: "generated-diagram"
status: "generated"
authority: "character-canon"
summary: "Generated index and banner for the compiled relationship diagrams."
tags:
  - character
  - relationships
  - generated
related:
  - "../profile-spec.md"
source_documents: []
---

# Character Relationship Diagrams

> DO NOT EDIT - generated from profiles by scripts/build-relationship-graph.py

These diagrams are a compiled artifact. They are never hand-edited.
The single source of truth is the `## Relationships` section of each
profile under `../profiles/`. Edit a relationship there, then re-run
`scripts/build-relationship-graph.py`.

The generator renders only the controlled relationship vocabulary
(see `../profile-spec.md`). Directional edges are stored once on the
dependent end; their inverses are derived by traversal and shown in
the derived graph below.

## Views

- [Family Tree](./family-tree.md)
- [Faction and Allegiance Map](./faction-map.md)
- [Social Web](./social-web.md)
- [Derived Inverse Graph](./derived-graph.md)

## Source status

- Profiles read: 35
- Profiles with structured edges (migrated): 32
- Profiles still legacy (no structured edges): 3
- In-vocabulary edges drawn: 79
- Derived inverse edges: 37
- Off-vocabulary labels still to migrate (0): none

As the remaining profiles migrate to the controlled vocabulary,
re-running the generator fills these diagrams in automatically.
