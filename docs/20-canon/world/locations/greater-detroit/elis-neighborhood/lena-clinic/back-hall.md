---
title: "The Clinic Back Hall"
document_type: "entity"
entity_type: "room"
status: "active-canon"
authority: "world-canon"
parent: lena-clinic
summary: "The rear hall that runs past the supply closet to the back-room server room, with the food-trade board pinned by the back door. The corridor Lena stands in, on the wrong side of the door she has handed to one man."
tags:
  - world
  - room
  - clinic
  - hallway
related:
  - "../lena-clinic.md"
  - "../../../../../../00-governance/entity-spec.md"
source_documents:
  - "docs/50-manuscript/book-1/chapter-02-the-last-supported-day/chapter-02-the-last-supported-day.md"
  - "docs/20-canon/technology/infrastructure/community-infrastructure.md"
---

# The Clinic Back Hall

"A back hall that ran past a supply closet to a door she had not opened in a year." The corridor between the people Lena tends and the back room she cannot help in.

## Layout and Dimensions

A hall running from the ward end of the clinic past the supply closet (`./supply-closet.md`) to the back-room server room (`./server-room.md`). The server-room door stands a hand's width open, "a slice of work light falling out across the floor of the corridor and up the opposite wall."

## Contents and Furnishings

By the back door hangs the food-trade board, "the cork panel by the back door where Dembele pinned his columns, what the Vesely place had and what the Reyes place needed and who would carry which to whom." The board belongs to the community economy, whose authority is `../../../../technology/infrastructure/community-infrastructure.md`; it is mentioned here as a fixture, not owned here.

## Light and Atmosphere

Dim and cold, with the strip of work light from the cracked-open back room the brightest thing in it. Where Lena stands and does not push the door.

```yaml
edges: {}
facts:
  fixtures: [food-trade-board]         # cork panel by the back door; the economy it tracks is owned by community-infrastructure.md, linked not duplicated
  leads_to: [supply-closet, server-room]
timeline: []
locks:
  facts.fixtures: { state: locked, by: b1-ch2 }   # the food-trade board pinned by the back door
  facts.leads_to: { state: locked, by: b1-ch2 }   # "a back hall that ran past a supply closet to a door [the server room]"
```
