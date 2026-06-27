---
title: "Eli's Home"
document_type: "entity"
entity_type: "building"
status: "active-canon"
authority: "world-canon"
parent: elis-neighborhood
summary: "Eli Rook's living quarters, attached to his repair shop. Bedroom, kitchen, and front steps are rendered in Chapter 1; the rest stays a stub until a scene reaches it."
tags:
  - world
  - building
  - eli
  - home
related:
  - "../elis-neighborhood.md"
  - "./elis-repair-shop.md"
  - "../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md"
  - "docs/20-canon/characters/profiles/rook-eli.md"
---

# Eli's Home

The quarters where Eli lives alone, attached to his repair shop. Chapter 1 opens here, the morning the external signal does not come back.

## Layout and Scale

A small set of rooms running on stored power. Chapter 1 renders the bedroom and the kitchen, and the front steps where Eli comes down into the street. The bedroom and kitchen have promoted to their own files under `elis-home/`; the front steps remain a mention, the threshold from which "the street gave nothing away."

## Systems and Condition

The home runs on stored power, with the small outside noises of a place still talking to the world all gone. Warmth is a gas ring on the kitchen counter. Network reaches it only through the neighborhood mesh off the library hub; on the morning of October 3 the mesh icon stands lit and steady while the external bars show nothing.

## Interior Feel

Spare and quiet, the silence particular to a place running on a battery. The floor is cold underfoot in the morning. It is the home of a man who listens to a building's systems before he listens to anyone.

## Occupancy and History

Eli lives here alone, divorced six years, no children (`../../../../characters/profiles/rook-eli.md`). The quarters are attached to the repair shop next door, the two structures effectively one working address.

```yaml
# A building lives in its district FOLDER (containment); it would be POSITIONED on the
# street network by an addressed-to edge, but canon places no building on a named street,
# so that edge is OMITTED rather than fabricated (spec section 7). Rooms are derived by
# walking elis-home/ (spec section 3).
edges:
  owner: rook-eli
  neighbor: elis-repair-shop          # symmetric: the attached shop next door (reciprocated there)
facts:
  power: stored-battery               # runs on stored power; mesh-only network via the library hub
timeline: []
```
