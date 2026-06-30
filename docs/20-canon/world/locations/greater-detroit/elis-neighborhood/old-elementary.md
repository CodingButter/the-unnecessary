---
title: "The Old Elementary"
document_type: "entity"
entity_type: "building"
status: "draft"
authority: "world-canon"
parent: elis-neighborhood
summary: "The former elementary school that now hosts the neighborhood-run school program, after the district stopped paying for buses and teachers. Mentioned in Chapter 1, not entered; stub."
tags:
  - world
  - building
  - school
  - stub
related:
  - "../elis-neighborhood.md"
  - "../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md"
---

# The Old Elementary

Stub. The former elementary school now hosts the program the neighborhood runs for its children, "now that the district had stopped paying for buses and teachers both" (Chapter 1). Mentioned in passing, not yet entered; promote when a scene reaches it.

```yaml
edges: {}
facts:
  use: neighborhood-run-school-program   # the district defunded buses and teachers; the community runs the program here
timeline: []
locks:
  facts.use: { state: locked, by: b1-ch1 }   # "the program the neighborhood ran out of the old elementary now that the district had stopped paying for buses and teachers"
```
