---
title: "Decision 059: Entities Get Rich, Deduced Dossiers Protected by a Per-Field Lock Model (Reversing Stub-Minimalism)"
document_type: "decision"
status: "active"
authority: "governance"
summary: "Reverses the entity system's minimalism principle. The old spec held that most nouns stay prose and a near-empty file would be 'empty noise that lies to the graph,' so the three doors gated whether a file exists at all. The new model: every introduced entity earns its own file with a full, deduced dossier (complete description plus, where it has a life, a timeline), creativity filling the gaps the story has not reached without ever contradicting canon, so the world is production-ready for multiple books and an eventual film adaptation. The safety mechanism is a per-field LOCK lifecycle (entity-spec.md new section 14): every fact, edge, and timeline entry is locked (approved prose or hard bible canon, immutable, records by:), proposed (draft prose, hardens to locked on approval, discarded if cut), or open (deduced fill, mutable, must never contradict a locked item or a bible). Encoding adds a parallel locks: map keyed by dotted path so clean values stay legible and the existing parser still reads them. Approved prose promotes open/proposed items to locked (overwriting an open guess is a resolution, not a conflict); new prose disagreeing with an already-locked item is a true canon conflict flagged to the author, never auto-resolved. The three doors are repurposed from gating file existence to governing depth priority and what must be locked. The blueprint FOCUS system is preserved and explicitly orthogonal: focus governs how vividly the prose renders an entity, dossier depth and lock state are independent. Spec sections 3, 6, 10a, and 11 reconciled; new section 14 added. Reversible via git history."
tags: ["decision", "workflow", "entity-system", "canon-structure", "lock-model", "dossier", "reversible"]
related:
  - "../../entity-spec.md"
  - "./040-the-project-uses-separate-specialized-documents.md"
  - "./047-change-propagation-and-pack-freshness.md"
  - "../index.md"
source_documents:
  - "docs/00-governance/entity-spec.md"
---

## Decision 059: Entities Get Rich, Deduced Dossiers Protected by a Per-Field Lock Model

**Date:** 2026-06-29
**Status:** Locked for Current Workflow
**Category:** Canon structure and workflow

### Decision

The entity system moves from **minimal stubs** to **rich, fully deduced dossiers**, made safe by a **per-field lock lifecycle**. Two things are now true.

**1. Every introduced entity earns a full deduced dossier.** Any entity the world introduces -- named in a bible, brought into a blueprint, or rendered on the page -- gets its own file carrying a complete description and, where it has a life, a timeline. Creativity fills the gaps the story has not yet reached, so the world is **production-ready**: canon airtight enough to survive multiple books and, eventually, a film adaptation. Deduction is disciplined: it may never contradict an established fact or a bible. The three doors (canon importance, blueprint focus, on-page attributes) no longer decide *whether* a file exists; they now govern **depth priority** -- which entities get their rich dossier first and how deep -- and **what must be locked** the moment the file is born.

**2. A per-field lock lifecycle protects canon.** Every structured fact, edge, and timeline entry in an entity's fenced `yaml` block carries one of three states:

- **`locked`** -- established by approved manuscript prose or hard bible canon (Story, Character, or Technology Bible, or the Master Timeline). Immutable; records `by:` its source.
- **`proposed`** -- asserted only by draft (not-yet-approved) prose. Hardens to `locked` when that chapter is approved; discarded if the draft is cut.
- **`open`** -- deduced or creative fill, or never established on the page. Mutable; must never contradict a `locked` item or a bible.

The encoding keeps the clean scalar values as they are and adds a parallel `locks:` map keyed by dotted path (`edges.owner`, `facts.casing_color`, `timeline.0`), so existing values stay legible and the current parser still reads them. The heuristic: an exact ISO datetime from prose or bible locks, an approximate `{ circa | before | after: ... }` date stays open; an on-page value locks, an invented fleshing-out value stays open; when in doubt, prefer open. **Promotion:** approved prose renders an `open` or `proposed` item, locking it `by: bN-chN`; if the prose value differs from the open guess, prose overwrites and then locks -- a resolution, not a conflict, because an open item is a mutable placeholder. **Conflict:** new prose disagreeing with an already-`locked` item is a true canon conflict, flagged to the author and never auto-resolved, per the project's canon-conflict rule.

**The blueprint FOCUS system is preserved and explicitly orthogonal.** Focus governs how vividly the *prose* renders an entity; dossier depth and lock state are independent. A `blur`-focus room can still carry a full `open` dossier; a `crisp`-focus object locks only the properties the prose actually paints.

### Previous or Alternative Direction

The entity spec (`docs/00-governance/entity-spec.md`) previously enforced minimalism. Section 3's "three doors" held that "a reference is not a file," that "most nouns a chapter names stay as prose inside their container," and that with none of the three doors crossed "a file would be empty noise that lies to the graph about what matters." Section 6 made the stub the default ("Most entities, most of the time. A neighbor's house nobody has entered yet"). Backfilled facts (section 10a) were tagged loosely with `from:` and a parenthetical `(proposed)`, with no formal immutability for established canon. The alternative considered and rejected was to keep stub-minimalism and lean harder on just-in-time growth; it was rejected because it leaves the world thin, defers worldbuilding indefinitely, and gives canon no machine-checkable notion of which facts are settled versus provisional.

### Reason

A production-ready world -- one that can carry a multi-book series and survive a film adaptation without continuity gaps -- needs every introduced thing to be deducible in full, not a placeholder awaiting the scene that may never come. Minimalism optimized for a near-empty graph; the project now optimizes for a complete, airtight one. The risk of richer files is that invented detail hardens into accidental false canon; the lock model removes that risk by labeling every fact with its provenance and immutability. Deduction becomes safe precisely because it is always marked `open` and can be overwritten by prose without ceremony, while genuine canon is `locked` and protected by the existing canon-conflict rule. This also makes section 10a's backward direction (prose as a source of canon) rigorous: approved prose locks, draft prose proposes, deduction stays open, and the diff-judge can tell which is which.

### Consequences

- `docs/00-governance/entity-spec.md`: section 3's "three doors" subsection rewritten so every introduced entity earns a dossier and the doors govern depth priority and locking rather than file existence; section 6 reframed from stub-default to deduced-dossier-default; principle 3 clarified to separate containment depth from dossier richness; section 10a's backfill bullets rewritten to use lock states; section 11 gains a lock-state-integrity validation bullet; new **section 14** added defining the three states, the `locks:` encoding with a worked example, the locked-vs-open heuristic, the promotion rule, the conflict rule, and the model's universality across characters, timelines, places, and objects.
- Entity authoring now produces rich, deduced dossiers with an explicit `locks:` map, not stubs. (No existing entity files are edited by this decision; backfilling lock state into already-authored entities is follow-up work.)
- The validator must enforce lock-state integrity (every `locks:` path resolves, every locked/proposed item records `by:`, no open item contradicts a locked item or a bible).
- Workflows that bind prose to canon (draft, revise, continuity, entity-extraction) gain a clear rule: approved prose locks `by: bN-chN`, draft prose proposes, deductions stay open, and an open-vs-locked disagreement is the line between an automatic resolution and an author-flagged conflict.

### Affected Documents

- `docs/00-governance/entity-spec.md`
- `scripts/` (the entity parser and validator gain lock-state handling; follow-up)
- `docs/20-canon/**` entity files (gain `locks:` maps as they are authored or revisited; no edit required by this decision)

### Reconsider Only If

The author decides the world should stay minimal and stub-first (retracting the rich-dossier reversal), or rules that the per-field lock model is more bookkeeping than it is worth and a coarser provenance scheme suffices. Both are reversible via git history.
