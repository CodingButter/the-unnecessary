---
title: "The Library Hub"
document_type: "entity"
entity_type: "building"
status: "active-canon"
authority: "world-canon"
parent: elis-neighborhood
summary: "A former public library that now hosts the neighborhood's local server and communications hub: the mesh, the local board, and an old satellite terminal. It posts to residents simply as 'The library.'"
tags:
  - world
  - building
  - library
  - hub
  - communications
related:
  - "../elis-neighborhood.md"
  - "../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md"
  - "docs/20-canon/world/locations/greater-detroit/elis-neighborhood.md"
  - "docs/20-canon/technology/infrastructure/community-infrastructure.md"
---

# The Library Hub

A former public library that now hosts the neighborhood's local server and communications hub. When it posts to the board it signs simply as "The library."

## Systems and Condition

The hub runs the neighborhood mesh, the local message board, and an old satellite terminal kept for the chance of a route out past the neighborhood's edge. As long as the hub has power, the mesh is up, which means the neighborhood can talk to itself even when it cannot talk to anyone past its own edge. On the morning of October 3 the queued cellular-withdrawal notice arrives forwarded "from the hub, passed hand to hand the way mail did now," and Eli's thin call to Lena is carried through "the hub's relay." The hub is the single node the whole community's communications now hang on.

## Significance

This is the spine of the neighborhood network's communications. The local mesh and the old satellite terminal run off it; the board where Dorsey and "The library" post is hosted here. The deeper technology of the mesh and the community's coordination is owned by `../../../../technology/infrastructure/community-infrastructure.md`; this entity is the place, not the network rules.

```yaml
# Community-run: no single owner edge (the hub belongs to the neighborhood, not a person).
edges: {}
facts:
  hosts: [neighborhood-mesh, local-board, old-satellite-terminal]
  posts_as: "The library"
  power_dependency: true              # while the hub has power the mesh is up; the community's comms live and die with it
timeline: []
locks:
  facts.hosts:            { state: locked, by: b1-ch1 }   # mesh, local board, old satellite terminal all named in Ch1
  facts.posts_as:         { state: locked, by: b1-ch1 }   # board message signed "The library"
  facts.power_dependency: { state: locked, by: b1-ch1 }   # "the mesh was up, which meant the library hub still had power"
```
