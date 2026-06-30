---
title: "Lena's Clinic"
document_type: "entity"
entity_type: "building"
status: "active-canon"
authority: "world-canon"
parent: elis-neighborhood
summary: "Dr. Lena Okafor's independent community clinic, the most richly rendered structure in canon (Chapter 2). A former dentist office in a former insurance office, carrying three patient rooms, a six-bed ward, an exam room, a front room, a back hall, a supply closet, and a back-room server room."
tags:
  - world
  - building
  - clinic
  - lena
  - medical
related:
  - "../elis-neighborhood.md"
  - "../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-02-the-last-supported-day/chapter-02-the-last-supported-day.md"
  - "docs/40-blueprints/book-1/chapter-02-the-last-supported-day/blueprint.md"
  - "docs/20-canon/timeline/book-1/act-1-timeline.md"
---

# Lena's Clinic

An independent community clinic run by Dr. Lena Okafor, "near Eli's neighborhood." Chapter 2 spends a whole evening inside it, the last supported day before three of its machines lose their remote authorization at midnight.

> District-membership note (flagged, not silently resolved): Chapter 2 places the clinic
> "near Eli's neighborhood," while Chapter 1 shows Lena reachable on the neighborhood mesh.
> It is parented under `elis-neighborhood` here because it shares that community and its
> mesh; if the author intends it as a separate adjacent community in the network, the
> `parent` edge should move. See the geography flags.

## Exterior and Approach

A modest converted storefront with a front door that lets in a thread of cold each time it opens, and a back door beside the food-trade board.

## Layout and Scale

The clinic is "three patient rooms, a ward of six beds, an exam room, the front room with its bench and its counter, and a back hall that ran past a supply closet to a door she had not opened in a year." Each of those spaces that the chapter renders has promoted to its own file under `lena-clinic/`. By the back door hangs the food-trade board, a cork panel where Dembele pins his columns of who has what and who needs it; the economy it tracks is owned by `../../../../technology/infrastructure/community-infrastructure.md`, linked here, not duplicated.

## Systems and Condition

The building runs dim to spare its batteries, the cold settled into the floor and rising through the soles of shoes since warmth became a thing rationed. Power is cut to the neighborhood's low tier after October 3, with no emergency restoration. An old, underpowered server in the back room keeps the records and nothing harder. Three pieces of equipment depend on remote authentication from manufacturers who have withdrawn: a diagnostic scanner and a medication-management unit (in the second patient room) and a respiratory-support controller (in the end room, on Mr. Adeyemi).

## Occupancy and History

Lena took the clinic over "from a dentist who had taken it over from an insurance office, and the bones of all three were still in it if you looked, the reception window, the little frosted partitions, the carpet glue under the new flooring." On the night of Chapter 2 the staff is Lena and the nurse Tomas Herrera, with Priya watching the ward; the ward holds the Reyes man, Mrs. Diallo, old Dembele in a spare bed, and others, four of six beds filled.

## Significance

The clinic is where the withdrawal stops being an inconvenience and acquires a body underneath it. The midnight authentication deadline and the borrowed-uptime reprieve play out here; the death that ignites the book happens here before dawn on October 4.

```yaml
# Building HOME is this district folder; it carries no addressed-to edge because canon gives
# the clinic no street position (only "near Eli's neighborhood"). Rooms are derived by walking
# lena-clinic/ (spec section 3). The clinic-wide withdrawal events live in the timeline below;
# the death itself is recorded on the respiratory-controller object (spec section 9).
edges:
  owner: okafor-lena
facts:
  former_use: [dentist-office, insurance-office]
  power_tier: low                     # cut to the neighborhood's lower tier Oct 3; no emergency restore
  unsupported_systems: [diagnostic-scanner, medication-unit, respiratory-controller]
timeline:
  - when: 2053-03
    set: { support_warning: true }
    note: "Lena learns several clinic systems will lose support before year end (pre-book-2053.md)."
  - when: 2053-10-03T23:59
    set: { remote_auth: lost }
    note: "Three systems (diagnostic scanner, medication-management unit, respiratory controller) lose remote authentication at end of day (Ch1, Ch2, act-1-timeline.md)."
  - when: 2053-10-04T00:00
    set: { equipment_state: borrowed-uptime }
    note: "After midnight the equipment still works, but only until restarted: one outage where the generators lag and the machines stop for good (act-1-timeline.md)."
  - when: 2053-10-04T06:00
    set: { equipment_state: dead }
    note: "A pre-dawn outage; the generators lag; the borrowed-uptime equipment restarts and does not come back. The man on the respiratory controller dies, off the page (act-1-timeline.md). Recorded in full on the respiratory-controller object."
locks:
  edges.owner:               { state: locked, by: b1-ch2 }          # "an independent community clinic run by Dr. Lena Okafor"
  facts.former_use:          { state: locked, by: b1-ch2 }          # "a dentist who had taken it over from an insurance office"
  facts.power_tier:          { state: locked, by: b1-ch2 }          # "you're on the low tier, no emergency restore"
  facts.unsupported_systems: { state: locked, by: b1-ch1 }          # the three systems named in Ch1's clinic call
  timeline.0:                { state: locked, by: master-timeline } # Mar-2053 support warning = pre-book-2053.md
  timeline.1:                { state: locked, by: b1-ch1 }          # 23:59 auth loss
  timeline.2:                { state: locked, by: master-timeline } # borrowed uptime = act-1-timeline.md (also draft Ch3)
  timeline.3:                { state: locked, by: master-timeline } # ~6am death/failure = act-1-timeline.md (the exact 06:00 clock is approximate: "roughly 6 a.m.")
```
