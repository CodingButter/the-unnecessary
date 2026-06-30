---
title: "The Diagnostic Scanner"
document_type: "entity"
entity_type: "object"
status: "active-canon"
authority: "world-canon"
parent: patient-room-2
summary: "The clinic's diagnostic scanner: 'the best doctor in the building,' which checks a license at startup and will not boot once its manufacturer's authentication is withdrawn at midnight on October 3."
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

# The Diagnostic Scanner

One of the three unsupported machines under the midnight deadline. "It stood against the wall, white and unmarked and perfect, a clean curved shell with a bed that slid into it, and it was the best doctor in the building."

## Appearance

A clean curved white shell with a bed that slides into it; an unmarked, perfect surface. It wakes a mild panel that asks the user to wait while it confirms its license.

## Significance

It once found a thing in a woman's pancreas that Lena's "own hands and eyes and forty-six years would have missed for another two months." It is better than her at finding, and useless tonight at the only thing that matters, which is running. The figure of the machine that "knows everything and is permitted to say none of it."

## Condition

Works tonight; "the wheel stopped. The machine said it was ready." It checks a license at startup against a server two thousand miles away. After midnight the server stops answering, so on its next restart "the wheel would turn and turn and never stop," and it will not boot.

```yaml
# A MOVABLE-class object by type, but fixed clinic equipment in practice: the timeline carries
# its authorization and condition over time, not its location (spec section 9).
home: patient-room-2
edges:
  owner: okafor-lena
facts:
  capability: imaging-diagnosis        # better than the doctor at finding; gated behind remote license
timeline:
  - when: 2053-10-03T23:59
    set: { remote_auth: lost }
    note: "Manufacturer authentication discontinued end of day (Ch1, Ch2)."
  - when: 2053-10-04T00:00
    set: { condition: borrowed-uptime }
    note: "Still ready while it keeps running, but it will not boot if restarted."
  - when: 2053-10-04T06:00
    set: { condition: "will-not-boot" }
    note: "Pre-dawn outage restarts the equipment; the scanner checks its license, the server is silent, it does not come on (act-1-timeline.md)."
locks:
  edges.owner:      { state: locked, by: b1-ch2 }          # clinic equipment; the clinic is Lena's
  facts.capability: { state: locked, by: b1-ch2 }          # found the pancreatic tumor; "the best doctor in the building"
  timeline.0:       { state: locked, by: b1-ch1 }          # 23:59 auth loss
  timeline.1:       { state: locked, by: master-timeline } # borrowed uptime = act-1-timeline.md
  timeline.2:       { state: locked, by: b1-ch2 }          # "the wheel would turn and turn... it will not boot" (restart per act-1-timeline.md; exact 06:00 approximate)
```
