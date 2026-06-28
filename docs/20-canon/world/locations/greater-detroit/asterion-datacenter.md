---
title: "The Asterion Datacenter"
document_type: "entity"
entity_type: "place"
status: "active-canon"
authority: "world-canon"
parent: greater-detroit
summary: "The Asterion machine floor where Eli worked at the company's height, recalled only as his intercut flashback memory in Chapter 3. Sketch depth: the ordered, abundant, cool-lit floor and the adored ease of being the one who could always fix it, the bright bench against which the cold clinic closet is measured. Shallow corporate seed only; what ran on the floor and the deep Asterion history are deliberately out of scope."
tags:
  - world
  - location
  - asterion
  - datacenter
  - flashback
related:
  - "../greater-detroit.md"
  - "../../../characters/profiles/rook-eli.md"
  - "../../../timeline/historical/2035-2041-autonomy-and-labor-break.md"
  - "../../../technology/infrastructure/computing-hardware.md"
  - "../../../../40-blueprints/book-1/chapter-03-borrowed-time/blueprint.md"
  - "../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/40-blueprints/book-1/chapter-03-borrowed-time/blueprint.md"
  - "docs/20-canon/characters/profiles/rook-eli.md"
  - "docs/20-canon/timeline/historical/2035-2041-autonomy-and-labor-break.md"
  - "docs/20-canon/technology/infrastructure/computing-hardware.md"
  - "docs/20-canon/world/locations/greater-detroit.md"
---

# The Asterion Datacenter

The machine floor where Eli worked when Asterion was at its height, present in Book One only as memory. It is the place his hands were once worshipped, set years later against a cold clinic closet, the bright and easy half of the inversion the clinic night turns on. It has no part in the present story except as the thing Eli remembers.

## The Machine Floor

Rows of racks under a cool, even light, ordered and clean and seemingly without end, the steady hum of cooling carried up through the floor. Power came here without question, conditioned and abundant, a building raised so the machines never wanted for anything. Nothing in the room was scavenged or rationed, and every cable ran where it was meant to run. A low-tier neighborhood on stored battery is its negative in every sensory register, and so is a back room three feet from a corridor where a doctor can do nothing.

## Atmosphere

The floor ran on calm and on plenty. Work that should have been hard came easy here, and the ease was adored. A manager would stand at Eli's shoulder, sweating over money and the confidence of investors, while Eli stayed unhurried and the fix landed clean and the man went from terror to gratitude. To be the one who could always make the fear go away, with the light cool and the power sure, was a warmth, and Eli took it. The room asked nothing of him that his hands could not give.

## Significance

This is the bright bench against which the dark one is measured. Here Eli saved a corporation money without breaking a sweat, and was paid and praised for it; the inversion the clinic night discovers is that the same hands, alone, against a real clock, cannot keep one life. The datacenter is felt as a wound and a contrast and is never explained. What ran on this floor, and the deeper history of Eli's years inside Asterion, stay outside this file by design; the canon here is only the floor, the cool light, the ease, and the adoration.

```yaml
# CONTAINMENT / REVEAL-SAFETY (spec section 3, 7): this is a sketch-depth PLACE born as a
# sibling of Northglass under the city root, NOT a child of it. The Ch3 flashbacks are the
# shallow corporate SEED; the deep Asterion/buried-project layer is reserved for the
# Northglass return, so this file is deliberately NOT nested under northglass and asserts no
# edge to it. greater-detroit is the only canon-resolvable parent (the region of major
# datacenter investment where Eli's Asterion work, assigned to Northglass, sat); the
# blueprint's flat pointer docs/20-canon/world/locations/asterion-datacenter.md reconciles to
# this folder home. Sub-areas (specific racks, rooms) earn child files only if a later scene
# reaches them (spec section 6).
facts:
  former_operator: asterion          # string fact, not an edge: no faction entity exists to point at (mirrors northglass.md)
  era: company-height                # the remembered past, Asterion at its height; no canonical ISO date to pin, so none invented
  power: abundant                    # cool light, steady cooling, conditioned power without question (computing-hardware.md)
  rendered: ch3-flashback-memory     # appears only as Eli's intercut memory; never present-day on the page
edges: {}                            # no fabricated edges: the only person it relates to is Eli, and no on-vocabulary place->person edge applies
timeline: []                         # a fixed remembered place; canon pins no dated change to it, so the timeline stays empty (spec section 9)
```
