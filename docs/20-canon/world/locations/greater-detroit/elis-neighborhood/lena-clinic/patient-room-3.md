---
title: "Clinic Patient Room (End Room)"
document_type: "entity"
entity_type: "room"
status: "active-canon"
authority: "world-canon"
parent: lena-clinic
summary: "The end room, 'in with the man': where Mr. Adeyemi lies on the respiratory-support controller through the night of October 3. The room of the death that ignites the book."
tags:
  - world
  - room
  - clinic
  - adeyemi
related:
  - "../lena-clinic.md"
  - "../../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-02-the-last-supported-day/chapter-02-the-last-supported-day.md"
  - "docs/20-canon/timeline/book-1/act-1-timeline.md"
---

# Clinic Patient Room (End Room)

"The controller's down the end, in with the man." The last room on Lena's nightly round, where Mr. Adeyemi sleeps on the respiratory-support controller because his own lungs will not make the night.

## Layout and Dimensions

A patient room at the far end of the hall, with a bed and a chair beside it that Lena does not usually sit in, and does this night.

## Contents and Furnishings

The respiratory-support controller stands by the bed, an index card taped over its dead status light; it has promoted to its own object file under `patient-room-3/`. Mr. Adeyemi (`../../../../../characters/profiles/adeyemi-bayo.md`), sixty-one, lies "narrow under the blanket, his chest rising on the machine's count and not his own."

## Light and Atmosphere

Dark and cold by night, the controller's even cycle pushing under the man's words, the daughter in a protected zone gone quiet in him along with everything else.

## Use and History

In the day Adeyemi comes off the machine for hours; at night he cannot hold without it. Lena chooses to keep him here rather than send him across the dark to a clinic two towns over. The pre-dawn outage on October 4 is where the controller fails and the man dies, off the page.

```yaml
edges: {}
facts:
  holds: [respiratory-controller]      # derived by walking patient-room-3/
  occupant: adeyemi-bayo               # string reference; people are not spatially contained (spec section 12), this is the room's clinical use
timeline: []                           # the room is fixed; the controller object carries the borrowed-uptime and death events
```
