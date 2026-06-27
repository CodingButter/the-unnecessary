---
title: "[Display Name]"
document_type: "entity"
entity_type: "segment"
status: "stub"
authority: "world-canon"
parent: [city-id]
summary: "[one line: the stretch of <street> between <A> and <B>]"
tags:
  - world
  - segment
  - network
related:
  - "../../../00-governance/entity-spec.md"
source_documents:
  - "docs/00-governance/entity-spec.md"
---

# [Display Name]

> Copy this file to `<id>.md` in the city's network area, rename the heading, and
> replace the placeholders. A segment is the EDGE of the street graph: it owns its
> `street`, `from`, `to`, and `length_m` ONCE, and every address and distance derives
> from it (spec §5, §7). `parent` is a browsing home only. A stretch is describable.
> CEILING, not floor: a stub is the frontmatter plus the one-line Overview and the
> four facts below. Raise `status` to `active-canon` when approved.

## Overview

[One sentence: this run of the street between its two intersections.]

## The Stretch

[What this length looks and feels like to move along — narrow or open, what it passes.]

## Surface and Condition

[Paving, lighting, repair, blockages, how passable it is.]

## Frontage

[The character of what faces this stretch. The exact address list is derived from the
`addressed-to` edges that resolve onto it, so describe feel, not a roster.]

## History

[What this stretch has been. Datable changes go in the timeline.]

```yaml
# This segment IS the edge between two intersections (spec §7): street / from / to / length_m are single-source here and nowhere else.
facts:
  street: [street-id]          # which street this is a stretch of (directional)
  from: [intersection-id]      # one endpoint  ┐ from + to are the segment's symmetric `connects`:
  to: [intersection-id]        # other endpoint ┘ both intersections must list this segment back (spec §11 reciprocity)
  length_m: [meters]           # single source of this stretch's length; addresses derive distance from it
edges: {}                      # endpoints live in `facts` above — no separate connects line, from/to are it
timeline: []                   # add a dated entry if the segment is re-paved, blocked, or its length changes
```
