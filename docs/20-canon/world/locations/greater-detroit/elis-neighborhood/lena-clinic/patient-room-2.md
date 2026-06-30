---
title: "Clinic Patient Room 2"
document_type: "entity"
entity_type: "room"
status: "active-canon"
authority: "world-canon"
parent: lena-clinic
summary: "The second patient room, holding the two unsupported machines of the second kind: the diagnostic scanner and the medication-management unit. Both lose remote authentication at midnight on October 3."
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

# Clinic Patient Room 2

"In the second room" Lena stops at the diagnostic scanner and, in the same room, the medication-management unit. Two of the three machines under the midnight deadline stand here.

## Contents and Furnishings

The diagnostic scanner stands against the wall, and the medication-management unit, "a gray cabinet the size of a small refrigerator," stands in its corner. Both have promoted to their own object files under `patient-room-2/`. Both share "the same heart as the scanner and the controller, the same need to phone a company to be allowed to do its work."

## Light and Atmosphere

Dim, the lights kept down to spare the batteries, the cold risen into the floor. Lena reads the two machines' "perfect numbers at no one."

## Condition

Both machines work tonight and lose remote authentication at midnight; after that the scanner will not boot and the cabinet may lock its drawers or refuse new orders. No one knows which.

```yaml
edges: {}
facts:
  holds: [diagnostic-scanner, medication-unit]   # both derived by walking patient-room-2/
timeline: []
locks:
  facts.holds: { state: locked, by: b1-ch2 }   # "In the second room" Lena stops at the scanner and, "in the same room," the cabinet
```
