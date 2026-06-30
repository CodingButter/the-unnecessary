---
title: "Eli's Neighborhood"
document_type: "entity"
entity_type: "district"
status: "active-canon"
authority: "world-canon"
parent: greater-detroit
summary: "Canonical world facts for the ordinary, canonically unnamed residential neighborhood where Eli Rook lives in Greater Detroit. Promoted to a district entity (spec section 7); carries the withdrawal-status timeline that the early chapters render."
tags:
  - world
  - location
  - neighborhood
  - eli
  - district
related:
  - "../greater-detroit.md"
  - "./lakeward.md"
  - "./northglass.md"
  - "../../../world/index.md"
  - "../../../../00-governance/entity-spec.md"
source_documents:
  - "archive/source-monoliths/story-bible.md"
  - "docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md"
  - "docs/20-canon/timeline/book-1/act-1-timeline.md"
  - "docs/20-canon/timeline/book-1/pre-book-2053.md"
---

## Eli's Neighborhood

Eli lives in an ordinary residential neighborhood in the Detroit metropolitan area.

The neighborhood does not possess a special dystopian name.

Residents use the same name it had before the collapse.

The houses, apartments, schools, stores, garages, churches, clinics, and streets remain recognizable.

The changes are subtle but constant.

Several streetlights no longer work.

Cellular coverage disappears during power shortages.

The local internet provider operates only a few days each week.

A closed pharmacy still contains empty automated dispensing systems.

Electric vehicles are used as neighborhood battery storage.

A former public library now hosts a local server and communications hub.

People still attempt to live normal lives.

Normality requires increasing amounts of technical skill and collective labor.

## See also

This neighborhood sits inside the wider [Greater Detroit](../greater-detroit.md) setting, which also documents the informal neighborhood network of cooperating communities.

```yaml
# District entity. Its buildings are DERIVED by walking the elis-neighborhood/ folder
# (spec section 3); the street network lives in elis-neighborhood/streets/ as a browse-only
# bucket (graph-only entities, spec section 7). The neighborhood is canonically UNNAMED.
facts:
  named: false                 # residents keep its pre-collapse name (Ch1); no in-world name exists in canon -- do not invent one
  withdrawal_factor: 0.65      # ESTIMATE for the time-is-politics travel model (spec section 5), not a stated-canon number; rises with each event below
edges: {}                      # no adjacency edge: canon names no bordering district. Inter-district TRAVEL TIMES live once in
                               # docs/20-canon/timeline/book-1/index.md and are derived route data (Lakeward ~35-60 min N; Northglass ~20-35 min), never stored here.
timeline:
  - when: 2053-01
    set: { withdrawal_factor: 0.5 }
    note: "Regional power provider introduces automated priority tiers; the neighborhood is classified BELOW protected, industrial, and government zones (pre-book-2053.md)."
  - when: 2053-10-03
    set: { cellular: withdrawn }
    note: "Regional cellular formally withdrawn, 'no longer supported under current service-continuity thresholds' (Ch1). The local mesh still runs off the library hub."
  - when: 2053-10-03
    set: { withdrawal_factor: 0.65, emergency_power_restore: false }
    note: "Midday reclassification to a lower power distribution tier; outages here are no longer processed as emergency restoration events (Ch1; act-1-timeline.md)."
locks:
  facts.named:             { state: open }                          # "no name" is asserted only by the ARCHIVED story-monolith (non-canon); approved prose never names it
  facts.withdrawal_factor: { state: open }                          # self-described model ESTIMATE, not a stated-canon number
  timeline.0:              { state: locked, by: master-timeline }   # Jan-2053 tier intro + below-protected = pre-book-2053.md (the 0.5 scalar is an estimate rider)
  timeline.1:              { state: locked, by: b1-ch1 }            # cellular formally withdrawn Oct 3
  timeline.2:              { state: locked, by: b1-ch1 }            # midday reclassification, no emergency restore (the 0.65 scalar is an estimate rider)
```
