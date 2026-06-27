---
title: "Lakeward"
document_type: "entity"
entity_type: "district"
status: "active-canon"
authority: "world-canon"
parent: greater-detroit
summary: "Canonical world facts for Lakeward, a protected wealthy enclave north of Detroit where Jonah Mercer and his family live. Promoted to a district entity (spec section 7); its interiors are not yet on the page and remain prose mentions."
tags:
  - world
  - location
  - enclave
  - lakeward
  - mercer
  - district
related:
  - "../greater-detroit.md"
  - "./elis-neighborhood.md"
  - "../../../world/protected-enclaves.md"
  - "../../../world/index.md"
  - "../../../../00-governance/entity-spec.md"
source_documents:
  - "archive/source-monoliths/story-bible.md"
  - "docs/20-canon/world/protected-enclaves.md"
---

## Lakeward

Lakeward is one of many protected enclaves.

It occupies a wealthy district north of Detroit and includes gated residential areas, private schools, medical facilities, artificial parks, autonomous security, and local energy generation.

Its streets resemble the best-maintained communities of the 2020s.

Residents do not experience the daily deterioration visible outside.

Jonah Mercer and his family live there.

Lakeward is not controlled by a single government.

Its services are maintained through corporate contracts and resident ownership agreements.

The people living there believe their protection is permanent.

It is not.

## See also

Lakeward is one instance of the broader pattern described in [protected enclaves](../../../world/protected-enclaves.md), and it sits within the [Greater Detroit](../greater-detroit.md) setting.

```yaml
# District entity, the wealthy counter-pole to Eli's neighborhood. No scene is set here yet,
# so its interiors (the Mercer house, private schools, medical facilities, artificial parks)
# stay prose mentions until a blueprint reaches them (spec section 6, section 8).
facts:
  protected: true
  withdrawal_factor: 0.05      # ESTIMATE: best-maintained, reliably serviced (spec section 5); contrast with Eli's neighborhood ~0.65
  services_via: [corporate-contracts, resident-ownership]
edges: {}                      # north of Detroit, ~35-60 min from Eli's neighborhood per the timeline index; travel time is derived route data, not stored here
timeline: []                   # no dated withdrawal yet; "their protection is permanent. It is not." is foreshadowed, not yet a dated event
```
