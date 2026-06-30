---
title: "The Respiratory-Support Controller"
document_type: "entity"
entity_type: "object"
status: "active-canon"
authority: "world-canon"
parent: patient-room-3
summary: "The respiratory-support controller that breathes for Mr. Adeyemi. The machine at the center of the clinic crisis: it runs on borrowed uptime after midnight on October 3 and fails in the pre-dawn outage of October 4, when the man on it dies, off the page."
tags:
  - world
  - object
  - clinic
  - machine
  - adeyemi
related:
  - "../patient-room-3.md"
  - "../../../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md"
  - "docs/50-manuscript/book-1/chapter-02-the-last-supported-day/chapter-02-the-last-supported-day.md"
  - "docs/20-canon/timeline/book-1/act-1-timeline.md"
---

# The Respiratory-Support Controller

The one of the three machines that "frightens" Lena. It runs continuous, breathing for Mr. Adeyemi through a night his own lungs cannot make, "a small even push and release."

## Appearance

A casing warm to the hand with "the particular living warmth of a thing doing work," cycling under the palm. Over the place where a status light used to burn, Lena has taped an index card in her own hand: "Cycle good. Last clean read, and a time. Pressures." The card tells her what the dead light no longer can.

## Significance

This is the machine the whole crisis narrows to: "the man first. Everything else second." Eli can forge the permission it has lost but not "what the permission was standing in front of," the calibration and dosing and safety record. Run on a hand-made yes, it would keep the man alive "slowly, correctly, while reporting that everything is fine," or fail outright. Its failure is the ignition of the book.

## Condition

Runs continuous and phones home on a cycle to confirm authorization. It loses remote authentication at midnight on October 3, runs on borrowed uptime, and in the pre-dawn outage of October 4 it restarts and does not come back.

```yaml
home: patient-room-3
edges:
  owner: okafor-lena
facts:
  capability: continuous-respiratory-support   # keeps a patient breathing; gated behind a cyclic remote authorization
  patient: adeyemi-bayo                          # clinical use; the death is recorded below and on the character state for adeyemi-bayo
timeline:
  - when: 2053-10-03T23:59
    set: { remote_auth: lost }
    note: "Manufacturer authentication discontinued end of day; behavior after the cutoff is unknown (Ch1, Ch2)."
  - when: 2053-10-04T00:00
    set: { condition: borrowed-uptime }
    note: "Keeps running until restarted; one outage where the generators lag and it stops for good (act-1-timeline.md)."
  - when: 2053-10-04T06:00
    set: { condition: failed }
    note: "Pre-dawn outage; the generators lag; the controller restarts and does not come back. Mr. Adeyemi dies, off the page. This is the ignition of everything that follows (act-1-timeline.md). Cross-reference the adeyemi-bayo character state."
locks:
  edges.owner:      { state: locked, by: b1-ch2 }          # clinic equipment; the clinic is Lena's
  facts.capability: { state: locked, by: b1-ch1 }          # "a controller that kept a set of lungs breathing" (Ch1 call), "a small even push and release" (Ch2)
  facts.patient:    { state: locked, by: b1-ch2 }          # Mr. Adeyemi on the controller
  timeline.0:       { state: locked, by: b1-ch1 }          # 23:59 auth loss
  timeline.1:       { state: locked, by: master-timeline } # borrowed uptime = act-1-timeline.md
  timeline.2:       { state: locked, by: master-timeline } # restart-failure + death = act-1-timeline.md (the exact 06:00 clock is approximate: "roughly 6 a.m.")
```
