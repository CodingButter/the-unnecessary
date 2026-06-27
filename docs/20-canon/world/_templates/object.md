---
title: "[Display Name]"
document_type: "entity"
entity_type: "object"
status: "stub"
authority: "world-canon"
parent: [room-id]
summary: "[one line: what this object is]"
tags:
  - world
  - object
related:
  - "../../../00-governance/entity-spec.md"
source_documents:
  - "docs/00-governance/entity-spec.md"
---

# [Display Name]

> Copy this file to `<id>.md` inside the room's (or building's) `<parent-id>/` folder,
> rename the heading, and replace the placeholders. An object is a MOVABLE thing: the
> folder is only its home shelf — its location, owner, condition, and existence over time
> live in the `timeline` below, keyed to in-world date, and the file NEVER moves when the
> object does (spec §9). CEILING, not floor: a stub is the frontmatter plus the one-line
> Overview. Raise `status` to `active-canon` when approved.

## Overview

[One sentence: what it is.]

## Appearance

[The sensory detail — how it looks, feels, weighs, sounds. Single source of these values
(a blueprint may *name* which to reveal, but the values live only here).]

## Provenance and History

[Where it came from and who has held it. The maker is stored on the person as `creator-of`
and derived here, not duplicated; ownership changes go in the timeline.]

## Significance

[What it means, what it foreshadows, why it matters — if anything yet.]

## Condition

[Its present state of wear or damage. Datable changes go in the timeline.]

```yaml
# A MOVABLE thing: the folder is its home shelf; the TIMELINE is the truth (spec §9). State at any date = home/initial values replayed forward.
home: [parent-id]                          # stable shelf — where the file lives, not a live location claim
edges:
  owner: [person-id]                       # directional; the initial holder. Changes of hands go in the timeline below.
facts: {}
# Timeline — in-world dates, never chapter numbers, so a flashback resolves to the earlier state (spec §9). Approximate ok: { circa: 2050 }.
timeline:
  - when: [YYYY-MM-DD]
    set: { located-in: [room-id], owner: [person-id], condition: "[state]" }
    note: "[what moved, changed hands, or broke on this date]"
  - when: [YYYY-MM-DD]
    set: { existence: [intact | lost | destroyed] }
    note: "[…]"
```
