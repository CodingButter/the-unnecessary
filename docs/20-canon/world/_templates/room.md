---
title: "[Display Name]"
document_type: "entity"
entity_type: "room"
status: "stub"
authority: "world-canon"
parent: [building-id]
summary: "[one line: what this room is]"
tags:
  - world
  - room
related:
  - "../../../00-governance/entity-spec.md"
source_documents:
  - "docs/00-governance/entity-spec.md"
---

# [Display Name]

> Copy this file to `<id>.md` inside the building's `<building-id>/` folder, rename the
> heading, and replace the placeholders. A room is FIXED inside its building, so its home
> and live location coincide and the timeline usually stays empty (spec §9). Objects in it
> stay prose mentions until one earns its own `object` file under `<room-id>/` (spec §3).
> CEILING, not floor: a stub is the frontmatter plus the one-line Overview. Raise `status`
> to `active-canon` when approved.

## Overview

[One sentence: what this room is and does.]

## Layout and Dimensions

[Shape, size, doors and windows, where you enter and what you face.]

## Contents and Furnishings

[What is in here. Each item stays a prose mention until it earns its own file; when it
does, it promotes to `<room-id>/<object-id>.md` and this line need not change (spec §3).]

## Light and Atmosphere

[How it is lit, how it sounds and smells, what it feels like to be in.]

## Condition

[Repair, wear, what works and what does not.]

## Use and History

[Who uses it, for what, and what it has been.]

```yaml
# A room is FIXED inside its building: home and live location coincide, so the timeline stays empty (spec §9).
edges:
  # adjoins: [room-id]   # symmetric (neighbor), optional — the room through that door
facts: {}
timeline: []             # fixed thing — leave empty; add a dated entry only if the room itself changes (wall removed, flooded)
```
