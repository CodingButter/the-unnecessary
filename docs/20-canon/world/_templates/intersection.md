---
title: "[Display Name]"
document_type: "entity"
entity_type: "intersection"
status: "stub"
authority: "world-canon"
parent: [city-id]
summary: "[one line: which streets meet here]"
tags:
  - world
  - intersection
  - network
related:
  - "../../../00-governance/entity-spec.md"
source_documents:
  - "docs/00-governance/entity-spec.md"
---

# [Display Name]

> Copy this file to `<id>.md` in the city's network area, rename the heading, and
> replace the placeholders. An intersection is a NETWORK NODE: `parent` is a browsing
> home only; its place in the world is the `connects` edge below. The segments that meet
> here are DERIVED by walking segments whose `from`/`to` is this node (spec §7) — never
> listed. A corner is describable, so it can be painted as deep as a scene needs.
> CEILING, not floor. Raise `status` to `active-canon` when approved.

## Overview

[One sentence: the corner of A and B.]

## The Corner

[What physically stands here — the curb, the post, the cracked paint, the thing a
character would actually see and touch.]

## Crossing and Control

[The light or stop (working or dead), sightlines, how foot and vehicle traffic move
through, what the withdrawal has done to the signal.]

## Atmosphere

[The feel of standing here: exposure, noise, who lingers.]

## History

[What this corner has been. Datable changes go in the timeline.]

```yaml
# A node where streets meet. Incident segments are DERIVED (walk segments whose from/to is this node). Spec §4, §7, §11.
edges:
  connects: [street-id, street-id]   # the streets that meet here — SYMMETRIC, reciprocity-checked (spec §11)
facts: {}
timeline: []   # a corner can change (signal dies, curb cracked) — add a dated entry when it does
```
