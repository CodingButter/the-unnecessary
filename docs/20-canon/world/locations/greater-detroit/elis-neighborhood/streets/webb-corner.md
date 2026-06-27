---
title: "The Corner of Webb"
document_type: "entity"
entity_type: "intersection"
status: "active-canon"
authority: "world-canon"
parent: greater-detroit
summary: "The corner of Webb, the only named intersection in canon, marked by a streetlight dead since spring with its glass gone milky. The cross street is canonically unnamed."
tags:
  - world
  - intersection
  - network
related:
  - "../../../greater-detroit.md"
  - "./webb.md"
  - "../../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md"
---

# The Corner of Webb

The only named corner in the canon. Eli passes it on his morning walk: "The streetlight on the corner of Webb was dead, had been dead since spring, the glass gone milky."

## The Corner

A residential street corner with a streetlight overhead, dead since spring, its glass gone milky. It is the first marker in Eli's running tally of how far the neighborhood's maintenance has pulled back.

## Crossing and Control

The streetlight here is dead; the next one along works, the two after that are dead. The corner reads as one point in a boundary "drawn in cold glass" over the street.

## History

Dead since the spring of 2053; the cross street that meets Webb here is not named in canon.

```yaml
# A NETWORK NODE (spec section 7). connects names the streets that meet here; only Webb is named in
# canon, so the second street is deliberately omitted rather than invented. Incident segments are
# derived, and canon supplies none. Filed under elis-neighborhood/streets/ for browsing only.
edges:
  connects: [webb]                     # the cross street is canonically UNNAMED -- do not fabricate a second street id
facts:
  cross_street: unnamed                # stated absence: Ch1 names a corner of Webb but no intersecting street
timeline:
  - when: { circa: 2053-04 }
    set: { streetlight: dead }
    note: "Dead since spring ('dead since spring, the glass gone milky'); still dead through October 3 (Ch1). Spring date is approximate."
```
