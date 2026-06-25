---
title: "About the Decision Log"
document_type: "governance-guide"
status: "active"
authority: "governance"
summary: "Governance guide for the creative decision log. Carries the meta sections that orient use of the log: how to use the document, the decision entry template for new decisions, the future update procedure, the final principle, and the list of existing documents the log affects."
tags:
  - governance
  - decision-log
  - guide
related:
  - "./index.md"
  - "./rejected-concepts.md"
  - "./open-decisions.md"
  - "../novel-development-guide.md"
source_documents:
  - "archive/source-monoliths/creative-decision-log.md"
---

# How to Use This Document

Consult this document when:

- A proposed idea resembles something previously rejected
- A writer or AI wants to revise major canon
- Two active documents appear to conflict
- A new direction changes the identity of the story
- A character, location, technology, or plot element feels inconsistent
- An older idea appears in archived material
- Another AI is taking over development without access to the original conversation

This document should be provided to another AI when it is asked to:

- Revise the Story Bible
- Create or revise major characters
- Change the timeline
- Restructure the plot
- Introduce a new faction or technology
- Reconsider Mars
- Develop later books
- Resolve a major contradiction

It does not need to be included in every prose-drafting prompt unless a relevant decision affects the chapter.

---

# Decision Entry Template

Use the following format for future entries:

```markdown
## Decision [Number]: [Title]

**Date:** YYYY-MM-DD  
**Status:** Locked for Current Draft  
**Category:** Worldbuilding / Character / Plot / Technology / Style / Workflow

### Decision

[State the current decision clearly.]

### Previous or Alternative Direction

[Explain the earlier idea or rejected alternatives.]

### Reason

[Explain why the current direction better serves the novel.]

### Consequences

[Explain what this changes or requires.]

### Affected Documents

- [Document]
- [Document]

### Reconsider Only If

[Describe the circumstances that would justify revisiting this decision.]
```

---

# Existing Documents Affected by This Log

Note: the old paths listed below predate the docs/ tree and are preserved verbatim from the source log.

This Decision Log reflects and supports the current versions of:

- `canon/narrative-brief.md`
- `canon/story-bible.md`
- `canon/character-bible.md`
- `canon/world-and-technology-rules.md`
- `canon/master-timeline.md`
- `planning/plot-outline-and-chapter-map.md`
- `chapter-blueprints/_chapter-blueprint-template.md`
- `novel-development-and-canon-guide.md`

If one of these documents contains a direct conflict with a decision marked **Locked for Current Draft**, the conflict should be reviewed and corrected.

---

# Future Update Procedure

Whenever a major decision is made:

1. Add a new numbered entry.
2. State the previous direction.
3. Explain the reason for the change.
4. Identify affected documents.
5. Update those documents.
6. Move replaced files into the archive if necessary.
7. Update project status.
8. Check whether any approved manuscript chapter is affected.

Do not delete old decisions.

If a decision is replaced, mark it **Superseded** and reference the new decision number.

---

# Final Principle

The Decision Log exists to prevent accidental regression.

It does not mean rejected ideas can never return.

It means they should return only through a deliberate decision made with awareness of why they were rejected before.

A future writer or AI should be free to improve the story.

It should not unknowingly rebuild an earlier version of it.
