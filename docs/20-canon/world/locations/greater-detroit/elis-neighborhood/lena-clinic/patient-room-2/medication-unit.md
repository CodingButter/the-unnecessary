---
title: "The Medication-Management Unit"
document_type: "entity"
entity_type: "object"
status: "active-canon"
authority: "world-canon"
parent: patient-room-2
summary: "The clinic's medication-management unit: a gray locked-drawer cabinet that decides doses and may lock or refuse new orders once its authentication is withdrawn at midnight on October 3. Whether it locks is the night's central uncertainty."
tags:
  - world
  - object
  - clinic
  - machine
related:
  - "../patient-room-2.md"
  - "../../../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-02-the-last-supported-day/chapter-02-the-last-supported-day.md"
  - "docs/20-canon/timeline/book-1/act-1-timeline.md"
---

# The Medication-Management Unit

One of the three unsupported machines. "A gray cabinet the size of a small refrigerator with a screen and a row of locked drawers. It held the doses, decided how much and how often, would not let her hand more morphine than a body should have."

## Appearance

A gray cabinet the height of a small refrigerator, a screen and a row of locked drawers, standing gray and locked-faced in its corner.

## Significance

Lena "loved it for that on her good days and resented it on the rest." It embodies her career-long argument that a visible human deciding is safer than a machine deciding, now inverted: tonight she must lean on, or work around, the machine that holds the doses.

## Condition

Works tonight and reports ready, which Lena no longer believes. After midnight "it might keep the schedules already loaded and refuse to take a new one. It might lock the drawers and keep the keys." No one knows which: "the not knowing was the whole of it." Lena writes the doses she may need on a card by hand in case the cabinet decides at midnight that it no longer will.

```yaml
home: patient-room-2
edges:
  owner: okafor-lena
facts:
  capability: dose-control             # holds and dispenses controlled medication; gated behind remote license
timeline:
  - when: 2053-10-03T23:59
    set: { remote_auth: lost }
    note: "Manufacturer authentication discontinued end of day (Ch1, Ch2)."
  - when: 2053-10-04T00:00
    set: { condition: borrowed-uptime }
    note: "Behavior after a restart is unknown: may keep loaded schedules and refuse new orders, or lock the drawers."
  - when: 2053-10-04T06:00
    set: { condition: unknown-after-restart }
    note: "Pre-dawn outage restarts the equipment; canon does not resolve the cabinet's exact post-restart state (act-1-timeline.md)."
locks:
  edges.owner:      { state: locked, by: b1-ch2 }          # clinic equipment; the clinic is Lena's
  facts.capability: { state: locked, by: b1-ch2 }          # "held the doses, decided how much and how often"
  timeline.0:       { state: locked, by: b1-ch1 }          # 23:59 auth loss
  timeline.1:       { state: locked, by: master-timeline } # borrowed uptime = act-1-timeline.md
  timeline.2:       { state: open }                        # the cabinet's post-restart condition is canonically UNRESOLVED ("no one knew which"); OPEN so a later chapter that restarts it promotes cleanly (unlike the scanner's "will-not-boot" and the controller's "failed", which canon DOES resolve -> those stay locked). The 06:00 restart event itself is act-1-timeline.md.
```
