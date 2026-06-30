---
title: "The Microgrid Node"
document_type: "entity"
entity_type: "place"
status: "draft"
authority: "world-canon"
parent: elis-neighborhood
summary: "The neighborhood's improvised power-coordination site, where the local sources that keep the block alive are tied together by hand: a generator pad, a commercial battery bank, the line of electric vehicles kept as neighborhood storage, and a residential solar array. Pre-draft stub for Chapter 4, Scene 2; the Master Timeline already establishes the Saturday-October-4 hand-braiding, so those facts are locked while the rest stays open."
tags:
  - world
  - place
  - energy
  - microgrid
  - power
related:
  - "../elis-neighborhood.md"
  - "./lena-clinic.md"
  - "../../../../technology/infrastructure/energy.md"
  - "../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/20-canon/technology/infrastructure/energy.md"
  - "docs/20-canon/timeline/book-1/act-1-timeline.md"
  - "docs/20-canon/world/locations/greater-detroit/elis-neighborhood.md"
  - "docs/40-blueprints/book-1/chapter-04-priority-tier/blueprint.md"
---

# The Microgrid Node

The neighborhood's improvised power-coordination site, where the local sources that keep the block alive are tied together: a generator pad, a commercial battery bank, the line of electric vehicles kept as neighborhood storage, and a residential solar array, run back toward Lena's clinic. It has no orchestration layer and no single keeper. Pre-draft stub: Chapter 4, Scene 2 renders the hand-braiding here on Saturday, October 4; promote it to a full dossier when that chapter is drafted.

## What It Is

A microgrid in the ordinary sense the world now lives by: local generation, batteries, vehicles, and controlled demand stitched into one supply (`../../../../technology/infrastructure/energy.md`). The neighborhood already leans on electric vehicles as battery storage (`../elis-neighborhood.md`). The pieces were built by different manufacturers and were never designed to cooperate, so each source speaks its own dialect of charge, discharge, and priority, and balancing them is translation under load with no margin.

## Systems and Condition

On Saturday, October 4, under a surging low tier with no emergency restoration, the sources are braided into a single microgrid by hand, source by source, to hold the clinic up while the backup batteries drain faster than anyone budgeted (`../../../../timeline/book-1/act-1-timeline.md`). It holds only while it is tended; no automated coordination exists yet to keep it balanced, and the most skilled hands available cannot be at every failing seam at once. Canon establishes the coordination points themselves, not a roofed structure or a street position, so this is the distributed site of the work, not a single building.

## Significance

This is where the book's hand-labor model meets its ceiling. The microgrid stands only because people stand over it, and the neighborhood's most experienced grid hand says aloud that manual balancing cannot be sustained: hand labor cannot keep enough machines alive at scale. The node is the practical floor under everything that follows from the day.

```yaml
# Community-tended, like the library hub: no single owner edge (the sources belong to the
# block, not a person), so the edges map is empty. The place HOME is this district folder;
# it carries no addressed-to edge because canon gives the coordination site no street
# position and no roofed structure -- only the pad, bank, EV line, and array (energy.md;
# act-1-timeline.md). Nothing symmetric is asserted (e.g. neighbor: lena-clinic) because the
# reciprocal end cannot be authored here, and an un-reciprocated symmetric edge would fail
# the rails -- the clinic relationship lives in prose instead.
edges: {}
facts:
  sources: [residential-solar, ev-storage, commercial-batteries, generators, clinic-backup]
  incompatible_protocols: true     # equipment from different manufacturers was never designed to cooperate
  coordination: by-hand            # no orchestration layer; tended source by source
timeline:
  - when: 2053-10-04
    set: { state: hand-coordinated }
    note: "Under the surging low tier, Eli and Nolan braid the neighborhood's incompatible sources -- residential solar, electric vehicles, commercial batteries, two generators, and the clinic backup -- into one microgrid by hand; Nolan warns that manual balancing cannot be sustained (act-1-timeline.md, Saturday Oct 4)."
locks:
  facts.sources:                { state: locked, by: master-timeline }  # the five source kinds named for Oct 4 (act-1-timeline.md); EVs-as-storage also b1-ch1 (elis-neighborhood.md)
  facts.incompatible_protocols: { state: locked, by: energy }           # energy.md: microgrids are hard because cross-manufacturer equipment was never designed to cooperate
  facts.coordination:           { state: locked, by: master-timeline }  # act-1-timeline.md: "Eli and Nolan attempt to coordinate by hand"
  timeline.0:                   { state: locked, by: master-timeline }  # the Oct 4 hand-coordination + Nolan's no-scaling warning are Master Timeline canon (the date is a day-span, not an exact clock)
```
