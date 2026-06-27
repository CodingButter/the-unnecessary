---
title: "[Display Name]"
document_type: "entity"
entity_type: "district"
status: "stub"
authority: "world-canon"
parent: [city-id]
summary: "[one line: what this district is]"
tags:
  - world
  - district
related:
  - "../../../00-governance/entity-spec.md"
source_documents:
  - "docs/00-governance/entity-spec.md"
---

# [Display Name]

> Copy this file to `<id>.md` inside the city's folder, rename the heading, and
> replace the bracketed placeholders. This template is a CEILING, not a floor: a
> valid stub is just the frontmatter, this heading, and the one-line **Overview**.
> Add a section only when the story reaches it, and never leave a section you
> declared blank (spec §6). Raise `status` to `active-canon` once an author approves
> the facts. Tag gated detail `[open]` / `[reveal: Book N]` / `[behavior-only]`.

## Overview

[One sentence. This line plus the frontmatter is a complete stub.]

## Feel and Atmosphere

[The mood of being here: light, sound, the texture of daily life.]

## Withdrawal and Services

[What the world still runs here and what it has let lapse. This is the coarse map
layer and the source of the `withdrawal_factor` below: distance is physics, time is
politics (spec §5).]

## Boundaries and Geography

[Where the district begins and ends; its terrain, edges, and major arteries.]

## Social Texture

[Who lives here, how they organize, what class or faction holds it.]

## History

[How the district came to be what it is now. Datable shifts also go in the timeline.]

## Sensory Signature

[The two or three concrete details that mark this district and no other.]

```yaml
# Structured facts + edges (machine-read; agents read the prose too). Spec §2, §4, §9.
facts:
  withdrawal_factor: [0.0 fully-serviced … 1.0 fully-abandoned]   # multiplies graph distance to yield travel TIME (spec §5)
edges:
  neighbor: [adjacent-district-id]        # symmetric; one line per neighbor (validator checks both ends agree)
  # owner: [faction-id]                   # directional, optional — who controls or operates the district
# Optional timeline — in-world dates, never chapter numbers (spec §9). Districts mostly change by withdrawal.
timeline:
  - when: [YYYY-MM-DD]
    set: { withdrawal_factor: [new value] }
    note: "[what the world withdrew or restored here on this date]"
```
