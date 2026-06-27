---
title: "Greater Detroit"
document_type: "entity"
entity_type: "city"
status: "active-canon"
authority: "world-canon"
summary: "Canonical world facts for the novel's primary setting, Greater Detroit, and the informal neighborhood network of cooperating communities within it. Promoted to the city root of the geography entity tree (spec section 7)."
tags:
  - world
  - location
  - setting
  - detroit
  - neighborhood-network
  - city
related:
  - "./greater-detroit/elis-neighborhood.md"
  - "./greater-detroit/lakeward.md"
  - "./greater-detroit/northglass.md"
  - "./mars-sites.md"
  - "../../world/index.md"
  - "../../../00-governance/entity-spec.md"
source_documents:
  - "archive/source-monoliths/story-bible.md"
  - "docs/00-governance/entity-spec.md"
---

## Primary Setting

The story takes place primarily in Greater Detroit.

During the automation boom, the region experienced major investment in robotics, manufacturing, energy storage, data centers, autonomous vehicles, and advanced logistics.

Old automotive infrastructure made the region ideal for the new industrial economy.

For several years, the area appeared to be experiencing a second golden age.

Then most human workers became unnecessary.

Factories remained productive while surrounding communities lost income.

Companies consolidated.

Facilities closed or became fully autonomous.

Public infrastructure deteriorated.

The region now contains ordinary neighborhoods, partially functioning municipalities, abandoned technology campuses, autonomous industrial facilities, and protected wealthy enclaves within driving distance of one another.

The Great Lakes also make the region strategically important because of water, agriculture, transportation, and energy potential.

## The Neighborhood Network

Several nearby communities have created informal agreements to share electricity, technical knowledge, medicine, food, communications, and labor.

The network has no formal government.

Each neighborhood retains its own leadership and priorities.

The alliance is fragile.

Some communities cooperate.

Others hoard resources.

Morrow initially exists to help this network coordinate systems that were never designed to work together.

## See also

The individual locations within this region have their own files: [Eli's neighborhood](./greater-detroit/elis-neighborhood.md), the protected enclave of [Lakeward](./greater-detroit/lakeward.md), the abandoned [Northglass](./greater-detroit/northglass.md) campus, and the [Mars sites](./mars-sites.md) that appear by contrast.

```yaml
# Greater Detroit is the CITY ROOT of the geography tree (spec section 7): it has no
# parent. Its districts are DERIVED by walking the greater-detroit/ folder, never listed
# here (spec section 3). The canonical district-to-district travel TIMES live once in
# docs/20-canon/timeline/book-1/index.md and are route data, not hand-stored per place
# (spec section 5: distance is physics, time is politics).
facts:
  region: great-lakes
  strategic_value: [water, agriculture, transportation, energy]
  holds: neighborhood-network        # informal, no formal government; membership is fluid
edges: {}                            # the city root owns no outward edge; containment is derived downward
timeline: []                         # region-wide change is recorded per-district as a withdrawal_factor shift, not here
```
