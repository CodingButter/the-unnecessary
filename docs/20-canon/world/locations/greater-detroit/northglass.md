---
title: "Northglass"
document_type: "entity"
entity_type: "place"
status: "active-canon"
authority: "world-canon"
parent: greater-detroit
summary: "Canonical world location entity for Northglass, Asterion's abandoned Great Lakes research campus. Promoted to a place entity (spec section 7) that LINKS to the technology-domain authority for the facility interior rather than duplicating it; not yet rendered on the page (entered October 5)."
tags:
  - world
  - location
  - northglass
  - asterion
  - morrow
  - campus
related:
  - "../greater-detroit.md"
  - "./elis-neighborhood.md"
  - "../../../technology/northglass.md"
  - "../../../technology/ai/morrow.md"
  - "../../../world/index.md"
  - "../../../../00-governance/entity-spec.md"
source_documents:
  - "archive/source-monoliths/story-bible.md"
  - "docs/20-canon/technology/northglass.md"
  - "docs/20-canon/timeline/book-1/act-1-timeline.md"
---

## Northglass

Northglass is Asterion's abandoned Great Lakes research campus.

## Facility history and remaining technology

The campus still holds Asterion server facilities, robotics laboratories, prototype hardware, and other equipment that mostly cannot function because it depends on discontinued authentication services. The technology-domain authority for the facility history, why it was abandoned, and the remaining technology is [technology/northglass.md](../../../technology/northglass.md).

## Morrow's origin at Northglass

Northglass is where Eli hid Morrow. Years ago he secretly created Morrow on his own, and rather than destroy it he buried the drive holding it inside an old machine on this abandoned campus. He does not build Morrow here during the story; he returns to Northglass to retrieve that hidden drive and resume the intelligence already on it. The single authority for the Morrow-origin-at-Northglass material is [technology/ai/morrow.md](../../../technology/ai/morrow.md).

## See also

Northglass sits inside the [Greater Detroit](../greater-detroit.md) setting and is the campus Eli draws on from his nearby [neighborhood](./elis-neighborhood.md).

```yaml
# Place entity (an abandoned campus). Its sub-areas -- data centers, robotics labs, cooling
# plants, underground service tunnels, storage warehouses, the laboratory holding the buried
# Morrow drive -- are owned by the technology authority and stay prose mentions here; they
# earn their own child files only when a scene reaches them (Oct 5+, spec section 6, section 8).
# This entity LINKS to that authority, it does not absorb it.
facts:
  former_operator: asterion          # string fact, not an edge: no faction entity exists yet to point at
  state: abandoned                   # dormant security, flooded service corridors, unstable power; equipment still reports to Asterion
  rendered: false                    # not yet on the page in Book 1; entered October 5 (act-1-timeline.md)
  entry: old-utility-connection
edges: {}                            # ~20-35 min from Eli's neighborhood per the timeline index; travel time is derived route data, not stored here
timeline: []                         # abandonment predates Book 1 with no canonical date; the Oct 5 retrieval is a plot event, recorded in act-1-timeline.md
```
