---
title: "[Display Name]"
document_type: "entity"
entity_type: "building"
status: "stub"
authority: "world-canon"
parent: [district-id]
summary: "[one line: what this building is]"
tags:
  - world
  - building
related:
  - "../../../00-governance/entity-spec.md"
source_documents:
  - "docs/00-governance/entity-spec.md"
---

# [Display Name]

> Copy this file to `<id>.md` inside the district's folder, rename the heading, and
> replace the placeholders. A building lives in the district FOLDER (containment) but is
> POSITIONED on the street network by its `addressed-to` edge below — two facts, one home
> each, never colliding (spec §7). It grows rooms by adding a same-named `<id>/` folder
> of `room` files beside it; it never lists them (spec §3). CEILING, not floor: a stub is
> the frontmatter, the Overview line, and `addressed-to`. Raise `status` when approved.

## Overview

[One sentence. With the frontmatter and an address, this is a complete stub.]

## Exterior and Approach

[How it presents from the street: facade, scale, the way you come up to it.]

## Layout and Scale

[Storeys, footprint, the shape of the inside at a glance. Rooms that earn detail
promote to their own files under `<id>/`.]

## Systems and Condition

[Power, water, heat, network — what still works and what the withdrawal has cut.
Datable changes (boarded, power-cut, restored) also go in the timeline.]

## Interior Feel

[The atmosphere of being inside: light, temperature, smell, what the space does to you.]

## Occupancy and History

[Who lives or works here, who has, and how it came to its present state.]

## Significance

[What this place means in the story, if anything yet.]

```yaml
# A building's HOME is the district folder; its POSITION is the linear address below (spec §7). A move/sale/demolition is a dated timeline fact (spec §9).
edges:
  addressed-to:                            # a linear reference, not a coordinate — exact and human-legible
    street: [street-id]
    between: [intersection-a, intersection-b]   # the two intersections bounding the segment it sits on
    along: [0.0 … 1.0]                     # fraction from between[0] toward between[1]
    side: [north | south | east | west]
  owner: [person-or-faction-id]            # directional; the inverse (owns) is derived, never written back
  # landlord: [person-or-faction-id]       # directional, optional — if tenanted rather than owner-occupied
  # neighbor: [building-id]                # symmetric, optional — the building next door
facts: {}
# Optional timeline — existence, ownership, and condition are dated facts (spec §9).
timeline:
  - when: [YYYY-MM-DD]
    set: { condition: "[state, e.g. boarded, power-cut, restored]" }
    note: "[what happened to the building in the world on this date]"
```
