---
title: "The Grocery (Marisol's)"
document_type: "entity"
entity_type: "building"
status: "active-canon"
authority: "world-canon"
parent: elis-neighborhood
summary: "The neighborhood grocery run by Marisol, on Eli's morning route. Rendered in Chapter 1 by its failing dairy case; the business is canonically unnamed."
tags:
  - world
  - building
  - grocery
  - marisol
related:
  - "../elis-neighborhood.md"
  - "./elis-repair-shop.md"
  - "../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md"
  - "docs/20-canon/characters/profiles/vega-marisol.md"
---

# The Grocery (Marisol's)

The neighborhood grocery, run by Marisol, on Eli's morning walk through the neighborhood. It has no canon business name; people go in because going in is a way of saying the place is still worth coming into.

## Exterior and Approach

From the street it shows "the good warm yellow of a place that wanted you to come in," one of the few warm lights left on the block.

## Layout and Scale

A counter where Marisol works, often in her coat against the cold, and a dairy case running the length of the back wall.

## Systems and Condition

The compressor on the long dairy case failed, and the case is down to two lit doors holding milk and the cultured stuff that keeps, with the rest pulled empty and clean, "gray as the inside of a switched-off screen." The fault is not the compressor itself but a controller that "wants to call home and nobody's home." Power follows the neighborhood's low tier after October 3.

## Occupancy and History

Marisol runs the counter (`../../../../characters/profiles/vega-marisol.md`). Payment still moves hand to hand in soft worn bills for small things like coffee.

```yaml
edges:
  owner: vega-marisol
facts:
  warm_front: true                    # one of the block's few lit, welcoming storefronts
  route_note: "on Eli's morning route through the neighborhood"   # Ch1 gives no grocery-to-shop distance (the parked EV-cable car sits at the shop's own curb, not near the grocery)
timeline:
  - when: 2053-09-30
    set: { dairy_case: "two lit doors only" }
    note: "The long dairy case 'quit Tuesday' (the Tuesday before Friday Oct 3); the fault is not the compressor but the controller, which cannot reach its withdrawn cloud service ('wants to call home and nobody's home'). Marisol expects to lose the two remaining doors soon (Ch1)."
locks:
  edges.owner:      { state: locked, by: b1-ch1 }   # Marisol runs the grocery on-page
  facts.warm_front: { state: locked, by: b1-ch1 }   # "the good warm yellow of a place that wanted you to come in"
  facts.route_note: { state: locked, by: b1-ch1 }   # he goes in on his morning walk
  timeline.0:       { state: locked, by: b1-ch1 }   # "Long case quit Tuesday" + "down to two doors" (the 09-30 date is derived from the Fri-Oct-3 weekday anchor)
```
