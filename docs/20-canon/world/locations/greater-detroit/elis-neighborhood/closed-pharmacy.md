---
title: "The Closed Pharmacy"
document_type: "entity"
entity_type: "building"
status: "draft"
authority: "world-canon"
parent: elis-neighborhood
summary: "A closed pharmacy that still contains empty automated dispensing systems. Named in the neighborhood canon, unplaced and not entered; stub."
tags:
  - world
  - building
  - pharmacy
  - stub
related:
  - "../elis-neighborhood.md"
  - "../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/20-canon/world/locations/greater-detroit/elis-neighborhood.md"
---

# The Closed Pharmacy

Stub. A closed pharmacy that "still contains empty automated dispensing systems" (neighborhood canon). Unplaced on the street network and not yet entered in any scene; promote when a scene reaches it.

```yaml
edges: {}
facts:
  contains: empty-automated-dispensing-systems
  state: closed
timeline: []
locks:
  facts.contains: { state: open }   # the closed pharmacy is in the ARCHIVED story-monolith only; absent from approved prose & active bibles
  facts.state:    { state: open }   # same; no approved-prose / active-bible basis
```
