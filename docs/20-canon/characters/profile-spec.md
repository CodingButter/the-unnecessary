---
title: "Character Profile Enrichment Specification"
document_type: "specification"
status: "draft"
authority: "character-canon"
summary: "Draft contract for enriching every human character profile of The Unnecessary to super-rich detail, and the at-scale method for generating them. Defines the house section schema, zero-blank rule, reveal-visibility tagging, invention policy, the five-phase relational generation method, reconciliation rules, and the draft-to-canon process. For author review; not yet active."
tags:
  - character
  - profiles
  - specification
  - schema
  - generation
  - reveal-control
related:
  - "./principles.md"
  - "./profiles/index.md"
  - "./relationship-map.md"
  - "./viewpoint-rules.md"
  - "../timeline/character-birth-dates.md"
  - "../world/social-structure.md"
  - "../technology/infrastructure/identity-and-money.md"
source_documents:
  - "docs/20-canon/characters/profiles/rook-eli.md"
  - "docs/20-canon/characters/principles.md"
  - "docs/20-canon/characters/relationship-map.md"
  - "docs/20-canon/timeline/character-birth-dates.md"
  - "docs/20-canon/world/social-structure.md"
---

# Character Profile Enrichment Specification

> Status: DRAFT for author review. Nothing here is canon yet. This file is a
> contract that defines what an enriched character profile must contain and how
> profiles are generated at scale. It does not itself establish character facts.
> On approval it becomes `active-support`, the existing profiles migrate to the
> schema below, and one Creative Decision Log entry records the change.

## 1. Purpose and authority

This specification governs the form and generation of every human character
profile under `docs/20-canon/characters/profiles/`. It exists so any drafting
agent can produce a complete, world-consistent, super-rich profile from this
file alone, without further instruction, and so the resulting cast coheres by
construction rather than by later cleanup.

This file orients and standardizes. It never overrides canon. Where this
specification and an existing canon file disagree, the canon file wins and the
conflict is flagged, never silently reconciled. The bibles outrank this spec.

`principles.md` remains the authority for the character principles themselves
(the goal, need, fear, contradiction, moral boundary, and the Final Character
Standard). This spec maps those required elements into named fields; it does not
replace them. See Section 11 for the reconciliation points the author must
settle before approval.

## 2. Scope

In scope: every named or specifically referenced human person across active
canon and approved manuscript. This is approximately 34 individuals. It includes
the eleven who already hold profiles, the four additional canon-named family
members in the birth-date table, and every named or specifically referenced
walk-on in approved chapters. The working roster is in Appendix A.

Out of scope: Morrow and Crown. They are nonhuman intelligences. They keep their
existing behavioral, non-physical template under `profiles/morrow.md` and
`profiles/crown.md`. Do not apply the physical or daily-life sections to them.

Zero blanks. Every field in the schema is filled for every in-scope character.
Where canon and approved prose are silent, the field is filled by
world-consistent invention under the policy in Section 6. A profile with an
empty field, a "TBD", or an "unknown" does not satisfy this contract. Minor
walk-ons are filled to the same schema; their invented depth is shallower, but
no field is left blank.

## 3. House form

Generated profiles obey the existing house style, confirmed against
`profiles/rook-eli.md` and `profiles/kade-adrian.md`:

- YAML front matter carrying all eight required fields, in this order:
  `title`, `document_type`, `status`, `authority`, `summary`, `tags`,
  `related`, `source_documents`. This is enforced by
  `scripts/validate-metadata.py`. Generated profiles use
  `document_type: "character-profile"`, `authority: "character-canon"`, and
  `status: "draft"` until approved (Section 9).
- One `#` H1 with the character's display name.
- `##` headers for each of the thirteen sections in Section 4, in order.
- Inline `**Label:**` bold field labels for discrete facts, as in the existing
  Basic Information blocks.
- Short, declarative sentences. One idea per sentence. No em dashes.
- `related` links use repo-relative paths to other profiles and to the spine
  files this profile draws on.

## 4. Section schema

Thirteen sections, in this fixed order. Every profile carries all thirteen.
Each section below states what it owns and the sub-blocks it must contain.

### 1) Basic Information

`**Full name:**`, `**Common name:**`, `**Age at the start of Book One:**`,
`**Birth date:**`, `**Birthplace:**`, `**Current residence:**`,
`**Household:**` (who they live with), `**Occupation:**`, `**Faction or class:**`
(Gatekeeper, Protected Wealthy, or Everyone Else, per
`../world/social-structure.md`), `**Primary viewpoint:**`, `**Story role:**`.
Ages and birth dates must agree with `../timeline/character-birth-dates.md` for
characters listed there.

### 2) Physical and Identifiers

The super-rich physical layer. Eight sub-blocks, each a `###` sub-header:

- **Frame.** Height, weight or build descriptor, build, posture.
- **Coloring.** Complexion, hair (color, texture, length, upkeep), eyes. This
  sub-block also carries a `**Heritage:**` field, present on every human profile,
  naming the character's specific ethnic and national ancestry (for example
  "White American: Polish, German, and English European, with Anishinaabe/Ojibwe
  ancestry", or "African-American, light-skinned end of the Black spectrum"). The
  complexion wording must be consistent with the stated heritage; where prose and
  heritage appear to disagree, the heritage field resolves it rather than the
  complexion being silently rewritten. The portrait renderer reads this field so
  the rendered heritage is the stated one, not an inference from complexion and
  surname.
- **Face.** Shape, notable features, expression at rest.
- **Hands and handedness.** Dominant hand, condition of the hands, what the
  hands reveal about the work the person does.
- **Distinguishing marks.** Scars with origin, birthmarks, moles or freckles,
  tattoos with meaning, piercings, dental notes. Each mark states where it came
  from, not only that it exists.
- **Identity and body status (2053).** Biometric and verified-identity
  registration status per `../technology/infrastructure/identity-and-money.md`
  (registered, lapsed, deliberately unregistered, and the consequences for
  institutional access). Implants or augmentations, or the deliberate absence of
  them and why. Prosthetics. Chronic conditions and how they are managed under a
  withdrawn healthcare system.
- **Movement and voice.** Gait, physical timbre of the voice, accent. This is
  the body of the voice; the spoken style lives in Section 8.
- **Grooming and default dress.** Upkeep, default clothing, footwear,
  accessories, scent. Dress should read the character's faction and economy.

### 3) Personality

Public and private personality, temperament, humor, and the
`principles.md`-mandated interior apparatus carried as named fields:
`**Articulated goal:**`, `**Deeper need:**`, `**Governing fear:**`,
`**Core contradiction:**`, `**Moral boundary:**`,
`**What could make them cross it:**`, `**Private reading of the collapse:**`
(their private interpretation of what happened to civilization),
`**Personal definition of human value:**`, and `**What they are preserving:**`
(their entry in the Final Character Standard). For walk-ons these are brief but
present.

### 4) Daily Life and Habits

A day and a week in this person's 2053, grounded in the canonized everyday
economy: barter and labor exchange as the norm outside protected systems,
community ledgers and food-trade boards, care without a bill, aging devices, and
uneven service, per `../world/social-structure.md` and
`../technology/infrastructure/identity-and-money.md`. State what they do for
money or goods, what they trade, how they eat, sleep, commute, and pay.

### 5) Hobbies and Interests

What they do that is not survival or work. At least three concrete interests,
consistent with their economy and access.

### 6) Likes and Dislikes

Concrete preferences: food, sound, weather, kinds of people, textures, machines.
Specific, not abstract. These are the small handles a drafter uses on the page.

### 7) Relationships

One sub-entry per significant relationship, each linking the other person's
profile by repo-relative path. State the bond, the tension, and what each wants
from the other. Pairwise dynamics that already live in `relationship-map.md` are
referenced, not silently rewritten.

Beneath the prose, each profile carries a machine-readable edge list that the
tooling parses. One edge per bullet, in the form `- relation: target`, where
`target` is a Markdown link to the other profile (`[Display](./<slug>.md)`) and the
`relation` is a term from the controlled vocabulary defined immediately below.
An edge may carry a trailing reveal tag or a `(proposed)` note. Off-vocabulary
labels, and stored derived inverses, are rejected by
`scripts/validate-characters.py`.

#### The relationship model

Every edge is one of exactly two classes. There is no third kind.

**Directional edges** are stored exactly once, on the **dependent** end,
pointing at the **authority**. The inverse is **derived by traversal and never
stored**. A child stores `father` and `mother`; the parent never stores `son`
or `daughter`, and a grandparent never stores `grandson`, because all of those
are computed from the chain. Storing an inverse is a defect, not a courtesy.

| Term | Stored on | Points at | Derived inverse (never stored) | Cardinality |
|---|---|---|---|---|
| `father` | the child | the father | child | at most one per character |
| `mother` | the child | the mother | child | at most one per character |
| `guardian` | the ward | the guardian | ward | — |
| `employer` | the employee | the employer | employee | — |
| `reports-to` | the subordinate | the superior | direct-report | — |
| `mentor` | the mentee | the mentor | mentee | — |
| `landlord` | the tenant | the landlord | tenant | — |
| `owner` | the owned | the owner | owns | — |
| `patient-of` | the patient | the clinician | patient | — |
| `creator-of` | the creator | the creation | created-by | — |

`creator-of` is the single deliberate exception to "stored on the dependent
end". It is authored on the **creator** (the authority) pointing at the
creation, because there is one creator of record and the fact reads naturally
from the creator's side. It is still stored exactly once; its inverse,
`created-by`, is derived. The derivations the tooling computes are: the direct
inverse of every directional edge, plus two-hop `grandparent` / `grandchild`
over the `father` / `mother` backbone, plus in-law relations over
`spouse` + parent edges.

**Symmetric edges** mean the same thing from both ends. They are stored on
**both** profiles and reciprocity-checked: if A stores `friend: B`, B must store
`friend: A`, with the same term. This is the only place double-entry applies.

`spouse`, `former-spouse`, `sibling`, `friend`, `rival`, `adversary`,
`colleague`, `neighbor`, `partner`, `acquaintance`.

#### Rules

1. A directional edge is stored once, on the dependent end (on the creator end
   for `creator-of`), pointing at the authority. Its inverse is derived, never
   written. Authoring an inverse (`son`, `daughter`, `grandfather`,
   `mother-of`, `mentor-of`, `owner-of`, `employees`) is a rejected defect.
2. `father` and `mother` are capped at one each per character. The directional
   ancestry edges (`father`, `mother`, `guardian`) must form a DAG: no
   character is their own ancestor.
3. A symmetric edge is stored on both ends and must reciprocate with the same
   term. Reciprocity is checked for symmetric edges only.
4. Tense and circumstance live in vocabulary or prose, not in new terms.
   Divorce uses `former-spouse`. A widowed or separated marriage uses `spouse`
   with the life-status noted in prose (so a widow is never mislabeled
   divorced). "Former" mentorship or employment stays `mentor` / `employer`
   with the lapse noted in prose.
5. Every edge label is in the controlled vocabulary. Anything else is rejected.
6. Facts that are not relationships are re-homed out of the edge list into prose
   or a dedicated non-edge field: naming choices, reserved seats, one-sided
   beliefs and assumptions, thematic rhymes, leak beneficiaries, and the barter
   economy's supply, routing, debt, fee, repair, and customer logistics. The
   relationship model carries kinship, authority, and durable social bonds; it
   is not a supply-chain ledger.

#### Old label to action mapping

Every label that existed before this model is resolved to exactly one action:
**map** it to a controlled term, **DROP** it as a derived inverse that the
tooling now computes, or **RE-HOME** it to prose because it is not a
relationship. Migration applies this table; the validator rejects every label
still in the left column until it is migrated.

Directional, kept or re-pointed to the dependent end:

| Old label | Action | Result |
|---|---|---|
| `father`, `mother` | keep | `father` / `mother` |
| `absent-father` | map | `father` (absence noted in prose) |
| `absent-mother`, `mother-past-the-mesh-edge` | map | `mother` (circumstance in prose) |
| `attending-physician`, `clinic-physician`, `night-nurse`, `watched-by` | map | `patient-of` (stored on the patient) |
| `supervisor` | map | `reports-to` |
| `former-student-of` | map | `mentor` ("former" noted in prose) |
| `mentor` | keep | `mentor` |
| `reports-to` | keep | `reports-to` |
| `patient-of` | keep | `patient-of` |
| `creator-of` | keep | `creator-of` (creator → creation) |
| `co-builder-and-bond` | map | `creator-of` (the bond noted in prose) |

Symmetric:

| Old label | Action | Result |
|---|---|---|
| `spouse`, `spouse-of` | map | `spouse` |
| `spouse-separated` | map | `spouse` (separated, noted in prose) |
| `late-husband`, `late-wife`, `late-spouse` | map | `spouse` (deceased/widowed, noted in prose) |
| `former-spouse`, `former-spouse-of` | map | `former-spouse` |
| `brother`, `sister`, `younger-sister` | map | `sibling` (birth order in prose) |
| `friend` | keep | `friend` |
| `family-friend`, `childhood-friend-of` | map | `friend` |
| `colleague-of`, `coworker` | map | `colleague` |
| `colleague-and-friend` | map | `colleague` + `friend` (both, on both ends) |
| `grew-to-trust` | map | `colleague` (the arc noted in prose) |
| `infrastructure-counterpart`, `neighbor-grid-elder` | map | `colleague` |
| `food-board-ally`, `grocery-node-ally`, `coordinates-board-with` | map | `colleague` |
| `neighbor-on-mesh-board`, `neighbor-grocer` | map | `neighbor` |
| `neighborhood-tech-who-serves-the-household` | map | `neighbor` (service noted in prose) |
| `community-counterpart`, `political-counterpart-of` | map | `rival` (productive conflict) |
| `adversary` | keep | `adversary` |
| `program-peer`, `clinic-guest-of` | map | `acquaintance` |

DROP, a derived inverse the tooling now computes:

| Old label | Derived from |
|---|---|
| `son`, `daughter`, `adult-daughter` | inverse of `father` / `mother` |
| `father-of`, `mother-of` | inverse of `father` / `mother` |
| `grandfather`, `grandmother`, `grandson`, `granddaughter` | two-hop over `father` / `mother` |
| `father-in-law`, `mother-in-law`, `daughter-in-law` | `spouse` + parent edges |
| `mentor-of`, `former-protege` | inverse of `mentor` |
| `employs-as-security-director` | inverse of `employer` / `reports-to` |
| `owner-of` | inverse of `owner` (the `owner` edge lives on the owned entity) |
| `patient`, `patient-charge`, `clinic-patient-family` | inverse of `patient-of` |

RE-HOME, not a relationship; move to prose or a dedicated non-edge field:

| Old label | Re-homed because |
|---|---|
| `named-son-after-self` | a naming fact (the father/son edge already carries the kinship) |
| `reserved-mars-place-for`, `reserved-mars-place-by` | a logistics commitment, not a bond |
| `assumes-admission-via`, `assumed-aurelia-partner` | a one-sided belief, explicitly not a real relationship |
| `archetype-rhyme` | a thematic device, "not a personal acquaintance" |
| `unknowing-beneficiary-of-leak` | a one-sided plot fact |
| `researcher-of` | an occupational role with respect to a system |
| `absent-mother-of-his-son` | the parent edge lives on the son; this is a co-parent prose note |
| `supported-relatives`, `grandchildren-in-household`, `enclave-peer-circle` | household / social-circle notes about unassigned, out-of-scope people |
| `board-keeper-for`, `routes-eggs-to`, `routed-by`, `board-node-routed-by`, `supplies-board`, `supplies-eggs-to`, `egg-source-for`, `needs-eggs-from`, `settling-debt-with`, `paid-clinic-fee-to`, `trades-with`, `repairs-for`, `called-in-for-repair`, `brought-doorbell-to`, `regular-customer` | barter-economy supply, routing, debt, fee, repair, and customer logistics |

The compiled views under `relationships/` render this model: `family-tree.md`
from the derived parent/child backbone, `social-web.md` from the stored
in-vocabulary edges, `faction-map.md` from the symmetric and authority edges,
and `derived-graph.md` from the inverses computed by traversal.

### 8) Voice and Speech

How they sound on the page: register, sentence shape, vocabulary, verbal tics,
what they say under stress. Must agree with `viewpoint-rules.md` for the
characters named there.

### 9) History and Background

Chronological life history: origin, family, formative public events, education,
work, how they arrived at their Book One situation. This is the page-usable
history. Hidden causes live in Section 10.

### 10) Private History and Behavioral Roots

The unrevealed causes of present behavior. Every entry is written as
cause then visible effect, in the form `cause -> visible effect`. Example
shape: "fell off a horse at seven -> goes still and quiet near large animals."
Most entries here carry the `behavior-only` tag (Section 5): never explained on
the page, always supplied to drafting agents because they govern consistent
behavior. Some carry `reveal: Book N` when the cause is a planned reveal.

### 11) Secrets

What the character hides, from whom, and what exposure would cost. Every secret
carries a reveal tag (Section 5). Secrets already recorded in existing profiles
are preserved and tagged, not rewritten.

### 12) Role and Series Potential

Story function, Book One arc, and long-term series potential. For major
characters this carries the existing arc fields (Book One arc, long-term arc,
false belief, truth they must learn, writing rules). For walk-ons it is a line
or two on what they could become if promoted.

### 13) Continuity Anchors

The static, immutable facts a drafter must never contradict: fixed physical
identifiers, fixed dates and ages, fixed relational facts, and any prose-locked
detail from approved chapters. This section is the baseline only. It does not
hold live per-chapter state. The live continuity ledger (current location,
condition, what they know, what they are hiding now) is owned by
`docs/60-continuity/` and must not be duplicated here. See Section 11, point 3.

## 5. Reveal and visibility tagging

This is the load-bearing control that lets a single rich profile serve every
chapter without leaking. Every hidden or timing-sensitive fact carries a
handling tag. The tag is appended to the fact inline, in square brackets.

| Tag | Meaning | Context-pack behavior |
|---|---|---|
| `[open]` | Page-usable now. Safe for any chapter. | Always included. |
| `[reveal: Book N]` or `[reveal: B1 Ch12]` | Gated until that point in the story. | Included only when the chapter being drafted is at or after that point. Filtered out before. |
| `[behavior-only]` | Never explained on the page, ever. Governs consistent behavior. | ALWAYS included, at every chapter, regardless of timeline. Passed as a behavioral constraint, never as droppable exposition. Must NOT be filtered out. |

Rules:

- Sections 10 and 11 require an explicit tag on every fact. Any fact elsewhere
  that is timing-sensitive also carries a tag. Untagged facts are treated as
  `[open]`.
- `behavior-only` and `reveal` are different. A reveal eventually reaches the
  page. A behavior-only fact never does. A fact may be a planned reveal of a
  behavior, in which case it carries both the visible behavior as
  `behavior-only` and the explanation as `reveal: Book N`.
- The context-pack builder filters by these tags using the chapter's timeline
  position. The builder lives in the chapter context-pack tooling under
  `context-manifests/` and `scripts/`, not in this file. This spec defines the
  required filtering behavior; wiring it into the builder is a separate,
  tracked tooling change and is called out in Section 11, point 4.

## 6. Invention policy

Invent freely to eliminate blanks and make each person whole. Constraints:

- Established prose and existing canon always win. Never invent over them.
- Tag every invented load-bearing fact `(proposed)` so the author can veto it.
  Load-bearing means it constrains other characters or future drafting:
  surnames, ages, birth dates, birthplaces, family structure, household
  composition, faction, and any first-of-record physical identifier.
- The `(proposed)` marker is independent of the reveal tag and may combine with
  it, for example `... [behavior-only] (proposed)`.
- Invention stays inside the world rules: the social structure, the everyday
  economy, the technology rules, and the timeline. Invented detail that
  contradicts a world rule is a defect, not a choice.

## 7. Generation method

Profiles are generated in five phases. Families and factions are generated
together, never in isolation, so shared facts cohere by construction.

### Phase 1: Ground

Build one shared relational-facts sheet for the whole cast before writing any
profile. Draw from `Story Bible` world canon, `relationship-map.md`,
`character-birth-dates.md`, and the existing profiles. Capture family trees,
surnames, ages and birth dates, households, and faction membership. This sheet
is the spine every profile is checked against.

### Phase 2: Derive implications

Read meaning out of the relational math and write it into the relevant profiles.
The age and household ladders carry implications that become formative facts.

Worked example: a sixteen-year gap between a parent and child implies teen
parenthood. That single derived fact then appears, consistently, in multiple
places. It is a formative event in the parent's History (Section 9). It shapes
the parent's Personality and governing fear (Section 3). It changes the parent's
economics and Daily Life (Section 4). It defines the parent-child relationship
from both sides (Section 7, reciprocal). And it shapes the child's upbringing
and History. The implication is derived once and propagated everywhere it
touches, rather than invented separately in each file.

### Phase 3: Cluster-generate

Write each family and each faction as a unit. Surnames, shared history,
household arrangements, and age ladders are decided once for the cluster and
written into every member at the same time. The Mercer family is generated
together. Asterion figures are generated together. This prevents two siblings
acquiring different surnames or an event being remembered two incompatible ways.

### Phase 4: Reconcile

Cross-check the whole cast against the spine and against each other:

- Surnames agree within families.
- Age and birth-date ladders validate against `character-birth-dates.md`.
- Relationships are reciprocal and non-contradictory from both sides.
- Shared events read consistently from every participant's profile.
- Households agree across the people who share them.
- Faction membership and cultural or ethnic naming are internally consistent.

Conflicts are flagged for the author with the conflicting files named and the
controlling authority identified. They are never silently averaged or resolved.

### Phase 5: Validate

Run `scripts/validate-metadata.py` so every generated profile passes the eight
required front-matter fields. Check that every `related` link resolves. Confirm
zero blank fields. Then route to the author. No profile flips to canon without
author approval.

## 8. Worked field template

An agent generating a profile copies this skeleton, fills every field, tags
every hidden or invented fact, and leaves nothing blank.

```
## Basic Information
**Full name:** ...
**Common name:** ...
**Age at the start of Book One:** ...
**Birth date:** ...            (validate vs character-birth-dates.md)
**Birthplace:** ...
**Current residence:** ...
**Household:** ...
**Occupation:** ...
**Faction or class:** ...
**Primary viewpoint:** ...
**Story role:** ...

## Physical and Identifiers
### Frame ...
### Coloring ...
**Heritage:** ...            (specific ethnic/national ancestry; portrait reads this)
### Face ...
### Hands and handedness ...
### Distinguishing marks ...          (each mark: origin stated)
### Identity and body status (2053) ...
### Movement and voice ...
### Grooming and default dress ...

## Personality
... public, private, humor ...
**Articulated goal:** ...
**Deeper need:** ...
**Governing fear:** ...
**Core contradiction:** ...
**Moral boundary:** ...
**What could make them cross it:** ...
**Private reading of the collapse:** ...
**Personal definition of human value:** ...
**What they are preserving:** ...

## Daily Life and Habits ...
## Hobbies and Interests ...
## Likes and Dislikes ...
## Relationships ...                   (reciprocal; link each profile)
## Voice and Speech ...
## History and Background ...
## Private History and Behavioral Roots
- cause -> visible effect [behavior-only]
- cause -> visible effect [reveal: Book 2]
## Secrets
- secret, from whom, cost [reveal: Book 1 Ch ...]
## Role and Series Potential ...
## Continuity Anchors ...              (static only; no live state)
```

## 9. Process and lifecycle

- Generated profiles carry `status: "draft"` in front matter until approved.
- The author reviews, vetoes any `(proposed)` fact they reject, and resolves any
  flagged conflict.
- On approval the profile's `status` flips to `active-canon` and one Creative
  Decision Log entry records the enrichment pass and the schema migration.
- The eleven existing human profiles migrate to this thirteen-section schema.
  Their established content is preserved and re-homed into the new sections; no
  approved fact is dropped in migration. The named interior fields from
  `principles.md` (goal, need, fear, contradiction, moral boundary, arc, false
  belief, writing rules) survive as the named fields in Sections 3 and 12.

## 10. Definition of done

A profile satisfies this contract when: all thirteen sections are present and
ordered; no field is blank; every hidden or timing-sensitive fact carries a
reveal tag; every invented load-bearing fact carries `(proposed)`; ages and
surnames reconcile with the spine; relationships are reciprocal; the file passes
`validate-metadata.py`; and all `related` links resolve.

## 11. Reconciliation points for the author

These are the places this draft touches `principles.md` and adjacent canon and
needs an author decision before it can be approved. They are surfaced, not
resolved.

1. **Scope versus "important characters."** `principles.md` reserves the deep
   interior apparatus (goal, need, fear, contradiction, moral boundary, private
   reading of the collapse, definition of human value) for *important*
   characters. This spec extends a full profile to *every* named person,
   including walk-ons. Decision needed: confirm a single full schema for all, or
   approve a two-tier model where walk-ons fill a reduced interior block. This
   draft assumes one schema with shallower invention for walk-ons.

2. **Section consolidation.** The existing profiles use many bespoke headers
   (Early Life, Education, Career, Complicity, Public and Private Personality,
   Sense of Humor, External Goal, Internal Need, Greatest Fear, Core
   Contradiction, Moral Boundary, Secret, False Belief, Book One Arc, Speech
   Pattern, Writing Rules). This spec maps them into thirteen sections. Decision
   needed: approve the mapping so migration does not appear to drop any of those
   named blocks. None are deleted; several become named fields.

3. **Continuity Anchors versus the continuity ledger.** `principles.md` lists
   Character Continuity Fields, but states the live baseline lives under
   `docs/60-continuity/`. Section 13 here holds static anchors only and defers
   live state to `60-continuity/`. Decision needed: confirm Continuity Anchors
   does not duplicate or compete with the continuity ledger, so no document
   silently does another's job.

4. **Reveal tagging is new and needs a builder change.** Existing profiles
   embed secrets unfiltered in active canon. The `open` / `reveal` /
   `behavior-only` tags and per-timeline filtering do not exist in the current
   context-pack tooling. Decision needed: approve the tagging convention and
   authorize the separate tooling change to make the context-pack builder filter
   by tag and chapter position. Until that change ships, `behavior-only` and
   gated facts could still reach a drafter.

5. **Sera Vale viewpoint discrepancy (pre-existing).** `profiles/index.md` marks
   Sera as a supporting viewpoint "Yes" while `characters/index.md` and
   `viewpoint-rules.md` mark her viewpoint "No". This predates this spec. The
   Reconcile phase will catch it. Flagging it here so Basic Information for Sera
   does not silently pick a side.

## Appendix A: Working roster

Canon-named humans (carry full profiles). The eleven with existing files plus
the four family members named only in the birth-date table.

| Name | Status today | Cluster |
|---|---|---|
| Elias "Eli" Rook | Profile exists | Rook |
| Jonah Mercer | Profile exists | Mercer |
| Celeste Mercer | Profile exists | Mercer |
| Adrian Kade | Profile exists | Asterion / Kade |
| Dr. Lena Okafor | Profile exists | Clinic |
| June Park | Profile exists | Community / Park |
| Mara Voss | Profile exists | Protected wealth / Voss |
| Talia Reed | Profile exists | Community |
| Nolan Avery | Profile exists | Grid |
| Sera Vale | Profile exists | Asterion security |
| Nora Bell | Profile exists | Asterion / Aurelia |
| Alexandra Kade | Named in birth table; no profile | Kade |
| Evan Voss | Named in birth table; no profile | Voss |
| Julian Mercer | Named in birth table; no profile | Mercer |
| Amelia Mercer | Named in birth table; no profile | Mercer |

Manuscript walk-ons (named or specifically referenced in approved chapters;
enumerated by the Phase 1 census and brought to full profiles): listed below.
The Ground phase finalizes this list against every approved chapter as the
manuscript grows.

Named in approved Chapters 1 and 2 (Phase 1 census):

| Name | First appears | Cluster | Notes |
|---|---|---|---|
| Mr. Adeyemi | Ch1 (unnamed), Ch2 | Clinic patients | Patient on the respiratory controller; has a daughter in a protected zone |
| Tomas | Ch2 | Clinic staff | Night nurse |
| Priya | Ch2 | Clinic staff | Staffer watching the Caldwell girl |
| Dembele | Ch2 | Food board | Former logistics chief; runs the neighborhood food board |
| Marisol | Ch1 | Neighborhood | Grocery counter clerk |
| Dorsey | Ch1 | Neighborhood | Neighbor on the mesh board |
| Vance | Ch1 | Vance family | Father of the 17-year-old who brings the doorbell |
| Mrs. Diallo | Ch2 | Diallo family | Delayed care over a nonexistent bill; husband quoted |
| the Caldwell girl | Ch2 | Caldwell family | Child patient |
| the Okonkwos | Ch2 | Okonkwo family | Brought eggs as payment |
| the Veselys | Ch2 | Vesely family | Egg producers in the barter chain (offscreen) |
| the Reyes family | Ch2 | Reyes family | Ward patient with a healing leg wound |

Note: the Chapter 1 "Nolan" who looked at the dead compressor is read as Nolan Avery (existing profile), not a new walk-on, pending Reconcile confirmation. Surname-only entries (Caldwell, Okonkwo, Vesely, Reyes) each stand for at least one person and are cluster-generated when promoted. Several specifically referenced but unnamed individuals also fall in scope and acquire names at generation: Vance's 17-year-old son, the woman with the bank-locked thermostat, the older man with the bank-locked tablet, the woman who cooks the salve. The Ground phase assigns or confirms each as the manuscript grows.

Target total is approximately 34 individuals. The exact count is fixed by the
Phase 1 census at generation time and grows with the manuscript.

## Structure, Naming & Validation

This section is contract-grade. It fixes how profile files are named, where
generated relational artifacts live, which copy of a relational fact is
authoritative, and what is checked by a script versus by an agent. It binds the
generation method in Section 7 and the definition of done in Section 10. Where
it touches existing canon files, the canon file still wins and the conflict is
flagged, never silently reconciled.

### Filename convention

Character profiles are named `lastname-firstname.md`, lowercase, hyphenated.
Examples: `mercer-jonah.md`, `rook-eli.md`, `kade-adrian.md`. Sorting on the
surname makes a family land adjacently in the directory listing, so a cluster
reads as a cluster on disk.

- The existing profiles are named `firstname-lastname.md`. All of them migrate.
  This is a one-time rename of the roughly thirteen current files to the
  surname-first form.
- Renaming a file breaks every reference to it. Each rename updates every
  pointer: the `related` and `source_documents` front-matter lists in every
  profile and in this spec, the entries in `profiles/index.md` and
  `relationship-map.md`, and every inline repo-relative link in prose. After the
  rename pass, `scripts/validate-links.py` must pass clean. A broken link is a
  defect, not a deferred cleanup.
- Everyone has a surname to sort by. The zero-blanks rule (Section 2) extends to
  the filename: a character with no canon surname receives a world-consistent
  invented one under the Section 6 invention policy, tagged `(proposed)` in the
  profile so the author can veto it. No file is named from a blank.

### Relationships folder (generated artifact)

A `docs/20-canon/characters/relationships/` folder holds the relational views as
Mermaid diagrams: the family trees, the faction map, and the alliance and
betrayal web. These files are a compiled artifact. They are never hand-edited.

- A generator step builds them. It reads each profile's Relationships section
  (Section 7) and emits the corresponding Mermaid. The diagrams are an output of
  the profiles, the way a binary is an output of source.
- Because they are generated, they cannot drift from the profiles. An edit to a
  relationship is made in the owning profile and the folder is rebuilt. A diagram
  edited by hand is overwritten on the next build and is treated as a defect.
- The folder carries a banner marking it generated and a note naming the
  generator, so no one mistakes it for a place to author facts.

### Single source of truth

Each relational fact has exactly one authoritative home. There is no triplicate.

- **Profiles own their relationships.** The bond, the tension, and what each
  side wants are authored once, in the relevant profile's Relationships section.
  That is the source.
- **The relationship-map and the Mermaid diagrams are generated from the
  profiles.** They are redundant by construction, never retyped. Redundancy that
  is generated cannot disagree with its source; redundancy that is hand-kept can,
  and is forbidden.
- The ledger rule follows the relationship model in Section 7, and differs by
  edge class. A **directional** edge is single-entry: it is authored once, on
  the dependent end, and the inverse is derived by traversal, never written. If
  A names B as `father`, B does not store `child`; the child direction is
  computed. A **symmetric** edge is double-entry: both ends author it with the
  same term, and the two halves must reconcile (if A stores `friend: B`, B
  stores `friend: A`). The reciprocity requirement in Section 7 is the ledger
  rule for symmetric edges; directional edges are kept honest by acyclicity and
  cardinality instead. The generated views read the stored edges, derive the
  inverses, and render each agreed edge once.

### Validation: rules to a script, judgment to an agent

Validation splits by what is being checked. Anything a rule can decide goes to a
deterministic script that runs free on every change. Anything that needs reading
comprehension goes to an agent, once, at generation time.

- **Deterministic script: `scripts/validate-characters.py`.** Standard library
  only, no network, fast enough to run every time the way `validate-links.py`
  does. It checks the mechanical contract:
  - **Controlled vocabulary.** Every edge label is in the Section 7 vocabulary.
    Off-vocabulary labels and stored derived inverses (`son`, `grandfather`,
    `mentor-of`, `owner-of`) are rejected.
  - **Reciprocity (symmetric only).** Every symmetric edge is present from both
    sides with the same term. If A lists `friend: B`, B lists `friend: A`.
    Directional edges are exempt: their inverse is derived, not stored.
  - **Cardinality and acyclicity.** At most one `father` and one `mother` per
    character, and no character is their own ancestor over the directional
    ancestry edges.
  - **Age ladders.** Birth dates parsed from
    `../timeline/character-birth-dates.md` put parents ahead of children by a
    plausible generational gap, with no impossible orderings.
  - **Surname agreement.** Members of one family carry the same surname, and the
    filename surname matches the profile.
  - **Zero-blanks completeness.** Every field in the Section 4 schema is present
    and non-empty for every in-scope character.
  - **Link and tag integrity.** Every `related` and inline link resolves, and
    every reveal or visibility tag is well formed per Section 5.
- **Agent review: the Reconcile phase only.** An agent runs at generation time,
  in Section 7 Phase 4, to make the judgment a script cannot. It reads whether a
  personality squares with the backstory, whether a shared event reads
  consistently from both participants beyond mere reciprocity, and whether a
  derived implication (the teen-parenthood example in Phase 2) is actually woven
  through every place it touches. Semantic coherence is the agent's job.
- The principle is the dividing line: rules to a script, judgment to an agent.
  The script gates every change for free. The agent is paid attention spent once,
  where a machine cannot stand in for a reader.
