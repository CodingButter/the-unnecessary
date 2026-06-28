---
title: "The Clinic's Records Server"
document_type: "entity"
entity_type: "object"
status: "active-canon"
authority: "world-canon"
parent: server-room
summary: "The clinic's own old machine, kept alive for the records and nothing harder: a squat, single-amber-lit box on the back-room rack, a decade older than the scanner and underpowered. The closet Eli crouches at on the night of October 3 to make stand in for a withdrawn company."
tags:
  - world
  - object
  - clinic
  - server
  - machine
related:
  - "../server-room.md"
  - "../../../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-02-the-last-supported-day/chapter-02-the-last-supported-day.md"
  - "docs/20-canon/timeline/book-1/act-1-timeline.md"
---

# The Clinic's Records Server

The clinic's own machine, the kind "every place like this has," something the last tenant left in a back room "the world had stopped coming into." It is the seat of the night's decisive work: the local thing Eli means to stand up so the orphaned devices stop asking the sky and start asking the closet.

## Overview

The squat box on the steel rack in the back-room server room. By itself it does one small job, holding the clinic's records, but on the night of October 3 it is the only local hardware near power, and so it becomes the machine Eli works to convert into a stand-in for the manufacturer servers going quiet at midnight.

## Appearance

"A squat machine with a single amber light, older than the scanner by a decade, underpowered." It sits on a steel rack under a window painted shut, in stale cold air "of a year unopened, dust and old electronics and something faintly sweet, mouse maybe." A work light on a hook throws Eli's bent shadow long across the painted-shut window while he crouches at it.

## Provenance and History

It came with the building, inherited down the chain of tenants Lena took the clinic from, "a dentist who had taken it over from an insurance office." It has sat behind a door swelled in its frame that Lena "had not opened in a year," kept running quietly at the one task left to it. Eli expects it before he sees it: "Every place like this has one, a closet, a room, something the last tenant left."

## Significance

This is the closet Lena hands the night to, three feet from the chair where she can do nothing. When the manufacturer servers go silent, "you put up something local that answers in its place," and this underpowered records box is the local thing Eli reaches for. From it he means to forge the lost authentication, "the permission," though not "what the permission was standing in front of," so a rescued machine will run and report itself fine on a yes that now comes from "me, and a closet." It is the seat of the borrowed-uptime fix and of the vigil that follows.

## Condition

Working, on its single amber light, at the records task and nothing harder. It is on the neighborhood's low tier: "Your power's already cut, you're on the low tier, no emergency restore." Eli judges it underpowered for what he needs, warning "this'll hold a light and a board and not much," so he must be careful what he draws. If the grid sags and the batteries take it, whatever he has running is lost and "the room goes dark with the rest" of the clinic.

```yaml
# A MOVABLE-class object by type, but fixed clinic equipment in practice: the timeline carries
# its repurposing over time, not its location (spec section 9). The parent room's server-room.md
# carries a `facts.holds: clinic-records-server`; this is the proper child file it pointed at, so
# the parent/child containment cross-check (folder home == `parent:`) now resolves.
home: server-room
edges:
  owner: okafor-lena                              # the clinic's own machine; Lena owns the clinic
facts:
  role: records-only                              # "kept alive for the records and nothing harder"
  capacity: "a light and a board, not much"       # underpowered, on the low tier; Eli must be careful what he draws
  age: "a decade older than the diagnostic-scanner"
timeline:
  - when: 2053-10-03
    set: { repurpose: begun-toward-local-emulation }
    note: "(proposed) On the night of October 3 Eli crouches at the rack, opens the bag, runs out cable, and begins repurposing the records-only machine into a local emulation / stand-in server, so the orphaned devices resolve and authenticate against this closet instead of the withdrawn manufacturer. The BEGINNING is on the page in Ch2; Chapter 3 ATTEMPTS the conversion but does NOT complete it -- Eli does not finish, and the machines are left on borrowed uptime (incomplete). Marked (proposed) until that prose is approved."
```
