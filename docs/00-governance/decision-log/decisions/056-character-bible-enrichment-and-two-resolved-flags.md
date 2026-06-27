---
title: "Decision 056: Character-Bible Enrichment Accepted, Daniel Rook Confirmed Deceased, Alexandra Kade Parallel Kept as a Book-2 Seed"
document_type: "decision"
status: "active"
authority: "governance"
summary: "Records the final resolution pass over the enriched character profiles. The author delegated two standing flags, now resolved: (1) Daniel Rook is confirmed DECEASED as character canon, an administrative death circa 2050 (a heart condition whose chain of care was severed by the service withdrawal; he died at home in Flint), with the dependent fact that Ruth Rook is a widow; the exact in-story timing of the death's reveal is left open as a plot decision. (2) Alexandra Kade's thematic parallel, that her restoration work lets abandoned communities survive without the corporation, the biological mirror of Morrow, is kept as canon characterization but marked a Book-2 seed and proposed direction, not a locked plot pillar, retaining its reveal: Book 2 tag. The remaining proposed FLAVOR facts across all profiles (surnames, ages, middle names, physical identifiers, hobbies) are accepted as canon and their proposed tags cleared; reveal-tagged and behavior-only items are left intact. All profiles remain status draft pending author activation, and the entire pass is reversible."
tags: ["decision", "character-canon", "character-bible", "enrichment", "rook", "kade", "reversible"]
related:
  - "../../../20-canon/characters/profiles/rook-daniel.md"
  - "../../../20-canon/characters/profiles/rook-ruth.md"
  - "../../../20-canon/characters/profiles/rook-eli.md"
  - "../../../20-canon/characters/profiles/kade-alexandra.md"
  - "../../../20-canon/characters/profile-spec.md"
  - "./054-chapter-2-approved-and-2053-everyday-economy-canonized.md"
  - "./055-chapter-1-approved-as-canon.md"
  - "../index.md"
source_documents:
  - "docs/20-canon/characters/profiles/rook-daniel.md"
  - "docs/20-canon/characters/profiles/rook-ruth.md"
  - "docs/20-canon/characters/profiles/kade-alexandra.md"
  - "docs/20-canon/characters/profile-spec.md"
---

## Decision 056: Character-Bible Enrichment Accepted, Daniel Rook Confirmed Deceased, Alexandra Kade Parallel Kept as a Book-2 Seed

**Status:** Locked for Current Draft
**Category:** Character canon and bible enrichment

### Decision

Following the profile-enrichment pass (the thirteen-section schema, the relational spine, and the reveal-safe tagging that produced the current `docs/20-canon/characters/profiles/**`), the author delegated the two standing author-decisions that the generators had surfaced and refused to settle. Both are now resolved, and the broad mass of low-risk flavor invention is accepted.

**1. Daniel Rook is DECEASED as character canon.** He died circa spring 2050, at about 67, three years before Book One, at home in the Rook family house in Flint. The cause is an "administrative death": a heart condition, manageable for decades in the old world with monitoring and routine medication, whose chain of care was severed one withdrawal at a time as the local cardiology service folded and the medication supply thinned, the same administrative death the manuscript gives the clinic's patients. The deceased facts in `rook-daniel.md` are flipped from proposed to canon, and the dependent fact in `rook-ruth.md` is flipped with them: Ruth is a widow of about three years, living and 67 in Book One. The "living father" alternative reading is dropped. The **exact in-story timing of the death's reveal** (when and how the reader learns of it) is deliberately left open as a plot decision and is not pinned in the profiles; the relevant items carry a reveal tag noting the timing is open.

**2. Alexandra Kade's Morrow parallel is kept, but as a Book-2 seed.** The thematic parallel, that her ecological restoration work increasingly lets abandoned communities feed, water, and sustain themselves without corporate support, the biological mirror of what Asterion fears Morrow could enable technically, is kept as **canon characterization**. The plot convergence between her work and Morrow, however, is explicitly a **Book-2 seed and proposed direction, not a locked plot pillar**. Its reveal stays tagged `[reveal: Book 2]`. Her mother remains an open canonical slot (not invented), and her ultimate Mars decision remains reserved for later books; neither is touched here.

**3. The remaining proposed FLAVOR facts are accepted as canon.** Across every profile, the proposed tags on surnames, ages, middle names, physical identifiers, hobbies, and comparable surface enrichment are cleared, promoting those facts to character canon. Reveal-tagged facts (`[reveal: ...]`) and behavior-only author-facing constraints (`[behavior-only]`) are left intact, including their proposed status, because they are hidden or future-facing rather than surface flavor. Structured relationship edges are untouched.

All profiles remain `status: draft`. This pass enriches and resolves; it does not activate. The author retains a final go to flip the profiles to active.

### Previous or Alternative Direction

Before this pass, `rook-daniel.md` and `rook-ruth.md` carried an unresolved, explicitly flagged author decision: Daniel might be deceased (the "deceased-reading," with Ruth a widow) or living (the "living-reading," with Daniel a 70-year-old mortality clock and Ruth half of an intact couple). The two readings were never averaged; the generator surfaced the fork and declined to choose. Alexandra Kade's Morrow parallel was tagged proposed with no ruling on whether it was a locked plot pillar or a discardable seed. The flavor inventions across the cast were each tagged proposed, pending a blanket accept-or-veto.

### Reason

The enrichment spec deliberately invents low-risk connective tissue and marks it proposed so the author can accept or veto in bulk rather than litigate every detail. The flavor facts are consistent with established canon and carry no reveal risk, so they are accepted. The Daniel fork is load-bearing for the Rook backstory and for Eli's interiority (the inherited radio, the "administrative death" that rhymes with the clinic), and leaving it open blocks any later chapter that references Daniel by name; the deceased reading is the stronger one and is confirmed, while the precise reveal timing is correctly a plot, not a profile, decision. The Alexandra parallel is thematically valuable and premise-consistent but must not harden into a committed plot before Book 2 is planned, so it is kept as characterization and seeded, not locked.

### Consequences

- `rook-daniel.md`: Daniel is deceased canon; living-reading text removed; deceased facts promoted; behavior-only and reveal items retained; flavor promoted; Continuity Anchors updated; status stays draft.
- `rook-ruth.md`: widowhood is canon; widow-versus-intact-couple conditionals removed; flavor promoted; non-death reveal and behavior-only items left intact; status stays draft.
- `rook-eli.md`: the note that Daniel's living-or-dead status was an open flag is replaced with the deceased fact and a pointer that the reveal timing is a later plot decision.
- `kade-alexandra.md`: the Morrow parallel secret is reworded to mark it a Book-2 seed and proposed direction, not a locked pillar, keeping `[reveal: Book 2]`; the open mother slot and the reserved Mars decision are unchanged.
- All other profiles: proposed flavor tags cleared; reveal-tagged and behavior-only items unchanged; structured edges unchanged.
- The relationship graph under `docs/20-canon/characters/relationships/**` is regenerated; metadata and link validators are unaffected by these edits.

### Affected Documents

- `docs/20-canon/characters/profiles/rook-daniel.md`
- `docs/20-canon/characters/profiles/rook-ruth.md`
- `docs/20-canon/characters/profiles/rook-eli.md`
- `docs/20-canon/characters/profiles/kade-alexandra.md`
- The remaining enriched profiles under `docs/20-canon/characters/profiles/**`
- `docs/20-canon/characters/relationships/**` (regenerated)

### Reconsider Only If

The author vetoes a specific promoted flavor fact, rules Daniel living after all (which would restore the mortality-clock reading and dissolve Ruth's widowhood), or promotes the Alexandra-Morrow parallel from a Book-2 seed to a committed plot pillar. Because the profiles remain drafts and this entry records the pass, every part of it is reversible.


## Activation (author-approved)

The author approved ("make them canon"). All 26 remaining draft profiles were flipped to `status: active-canon`; the full cast (37 profiles: 35 human + Morrow + Crown) is now active canon, validated clean (metadata, links, relationship-integrity all PASS). This supersedes the "all profiles remain draft" provision above. Reversibility is now via git history rather than draft status; the two resolved flags and all promoted flavor remain reversible by reverting.
