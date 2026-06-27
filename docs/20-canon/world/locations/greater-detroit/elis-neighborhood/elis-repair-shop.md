---
title: "Eli's Repair Shop"
document_type: "entity"
entity_type: "building"
status: "active-canon"
authority: "world-canon"
parent: elis-neighborhood
summary: "Eli Rook's former computer repair shop, where he talks stranded machines down off the ledge of their own obedience. Rendered lightly in Chapter 1; the business itself is canonically unnamed."
tags:
  - world
  - building
  - eli
  - repair-shop
related:
  - "../elis-neighborhood.md"
  - "./elis-home.md"
  - "./grocery.md"
  - "../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md"
  - "docs/20-canon/characters/profiles/rook-eli.md"
---

# Eli's Repair Shop

A former computer repair shop attached to a deteriorating commercial building, where Eli repairs the systems that manufacturers and infrastructure companies no longer support. The business has no canon name.

## Layout and Scale

A working front room organized around a single workbench under a lamp. A cracked screen rides an arm over the bench, propped into a cradle that feeds the library hub's relay so Eli can hold a thin call out of the neighborhood. A stool sits by the window. The shop is attached to Eli's living quarters; the two are one address.

## Systems and Condition

The bench has light and a hub relay for the mesh; a backup fan turns over behind the wall. The window gives a flat, cold light. Power is the neighborhood's degrading supply, on the low tier after October 3. Far off, a transformer he cannot see holds a single low note, the sound of power still being delivered to someone.

## Interior Feel

Quiet, the quiet that comes over him at the bench. There is always another stranded machine waiting on a server nobody answers for anymore, and the work leaves no room in him for anything else.

## Occupancy and History

Eli works the shop alone and lives in the attached quarters. A block from the shop sits the grocery (`../grocery.md`). He accepts payment in money, parts, food, labor, medicine, and favors, and often refuses payment from people who cannot afford it.

```yaml
# No addressed-to edge: canon gives the shop no street position, only that the grocery is
# "a block from the shop" (Ch1), a relative distance kept in prose, not a fabricated address.
edges:
  owner: rook-eli
  neighbor: elis-home                 # symmetric: the attached living quarters (reciprocated there)
facts:
  function: stranded-device-repair    # cloud-dependency removal, local emulation, firmware reflashing
  power_tier: low                     # neighborhood reclassified Oct 3; no emergency restore
timeline: []
```
