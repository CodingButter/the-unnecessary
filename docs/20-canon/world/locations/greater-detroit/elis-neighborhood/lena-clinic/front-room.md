---
title: "The Clinic Front Room"
document_type: "entity"
entity_type: "room"
status: "active-canon"
authority: "world-canon"
parent: lena-clinic
summary: "The clinic's front room: a bench, a counter, and the dark payment terminal where a dozen brown eggs now sit in for an entire vanished billing apparatus."
tags:
  - world
  - room
  - clinic
related:
  - "../lena-clinic.md"
  - "../../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-02-the-last-supported-day/chapter-02-the-last-supported-day.md"
---

# The Clinic Front Room

"The front room with its bench and its counter," where Tomas keeps the late watch and where the clinic's economy now begins and ends on a countertop.

## Layout and Dimensions

A bench and a counter near the front door, which lets in a thread of cold each time it opens.

## Contents and Furnishings

On the counter stands the old payment terminal, "a screen at the counter that took a card and sent a number to an office," now dark, the office gone, the company folded. Where the screen used to be sit a dozen brown eggs from the Vesely place, the Okonkwos' fee for a visit: "the entire economy now, start to finish." Late in the chapter Tomas sits here with the lights low, "watching the door no one would come through."

## Light and Atmosphere

Lit low against the batteries; the warm/cold border of the building, the front door breathing cold into it.

## Use and History

Inherited through a dentist's office from an insurance office; the bones of the old reception are still here under the new flooring. The billing machine survives as dead furniture while barter runs across the same counter.

```yaml
edges: {}
facts:
  holds: [dark-payment-terminal, front-bench, counter]   # the terminal is dead furniture; barter runs on the counter (community-infrastructure.md owns the economy)
timeline: []
locks:
  facts.holds: { state: locked, by: b1-ch2 }   # bench, counter, and the dark card terminal all rendered in Ch2
```
