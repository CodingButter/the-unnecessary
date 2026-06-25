# Audit note: Task A (Inventory and Structure Scan)

Phase 01 Repository Audit. READ-ONLY pass over the repository for "The Unnecessary".
Authority: master spec `migration/REPOSITORY-REORGANIZATION-SPEC.md` (wins all conflicts);
runbook `migration/plan/01-repository-audit.md`.

This note covers Task A: full file tree, per-file inventory, and reconciliation of the
recursive Markdown scan against `git ls-files`. Deep per-document split planning for the
canon, vision, governance, and blueprint files is the responsibility of Tasks B through E;
this note proposes best-guess destinations and split decisions for completeness only and
labels them "recommended".

## Reconciliation summary

- Recursive `find . -type f -name '*.md'` (excluding `.git`): 266 Markdown files.
- `git ls-files '*.md'`: 266 Markdown files.
- `comm` of the two sorted lists: zero differences. No file is tracked-but-missing and no
  file is present-but-untracked. `git status --porcelain` is clean (no untracked or
  modified files). The two lists reconcile exactly.
- Of the 266 Markdown files, 254 live under `.claude/skills/**` (BMAD skill packs, pure
  tooling) and are infrastructure. The remaining 12 are the novel-content and
  novel-adjacent governance documents audited below.
- Target tree folders are all ABSENT as expected pre-migration: no `docs/`, `archive/`,
  `context-manifests/`, `scripts/`, `.context/`. The only pre-existing structural folder is
  `migration/` (with `migration/plan/` and the now-present `migration/audit-notes/`).

## Presence / absence confirmations (runbook section 3, master spec Phase 1)

- Manuscript chapters: ABSENT. No file or folder named or resembling a manuscript chapter
  exists. `docs/50-manuscript/` does not exist.
- Continuity documents: ABSENT. The only path matching "continuity" is the migration
  planning runbook `migration/plan/07-continuity-bootstrap.md`, which is tooling, not a
  continuity document. `docs/60-continuity/` does not exist.
- Research files: ABSENT. No research ledger or research topic files exist. The "research"
  matches are BMAD skill templates under `.claude/skills/**`, which are tooling.
- Chapter blueprints other than the template: ABSENT. `chapter-blueprints/` contains exactly
  one file, `Chapter Blueprint Template.md`. No instantiated chapter blueprint exists.
- Empty / non-Markdown notables: `.audio/` exists but is empty.

## Discovered novel-content / governance Markdown beyond the 9 monoliths + template

Two discovered files (novel-adjacent governance / operations, not among the 9 monoliths and
not the blueprint template, and not BMAD skill tooling):

- `CLAUDE.md` (root). Project entry / operational layer plus mem0 protocol. Governance-adjacent.
- `Memory Conventions.md` (root). mem0 memory-practice spec. Governance / operations.

No other discovered novel-content Markdown exists. Everything else outside the 9 monoliths +
template is either `migration/**` (migration tooling) or `.claude/**` (Claude Code + BMAD
skill tooling).

## File tree (grouped)

### Group 1: Novel-content monoliths (the 9) + blueprint template

```text
Narrative Brief.md
Story Bible.md
Character Bible.md
Technology Rules.md
Master Timeline.md
Plot Outline and Chapter Map.md
Style Guide.md
Creative Decision Log.md
Development and Canon Guide.md
chapter-blueprints/Chapter Blueprint Template.md
```

### Group 2: Discovered novel-adjacent / governance Markdown

```text
CLAUDE.md
Memory Conventions.md
```

### Group 3: Infrastructure / tooling (not audited per-document here)

```text
.audio/                                  (empty)
.env
.envrc
.gitignore
.mcp.json
.claude/hooks/mem0-recall.sh
.claude/settings.json
.claude/settings.local.json
.claude/screenshots/                     (dir)
.claude/skills/**                        (254 *.md BMAD skill packs + .toml/.csv/.py/.html assets)
migration/REPOSITORY-REORGANIZATION-SPEC.md   (read-only authority; master spec)
migration/conflicts-found.md                  (Phase 00 seeded ledger)
migration/audit-notes/                        (this note's home; working notes)
migration/plan/00-migration-overview.md
migration/plan/01-repository-audit.md
migration/plan/02-target-architecture.md
migration/plan/03-governance-and-indexes.md
migration/plan/04-canon-migration.md
migration/plan/05-planning-and-style-migration.md
migration/plan/06-context-manifests-and-tooling.md
migration/plan/07-continuity-bootstrap.md
migration/plan/08-validation.md
migration/plan/09-finalization.md
```

## Per-file inventory (novel-content + discovered)

Counts captured by `wc` and `grep -cE` on the live files. H1 = lines starting `# `,
H2 = `## `, H3 = `### `, mermaid = fenced ```mermaid blocks.

| File | Bytes | Lines | H1 | H2 | H3 | Mermaid |
|---|---:|---:|---:|---:|---:|---:|
| Narrative Brief.md | 19953 | 556 | 1 | 23 | 11 | 0 |
| Story Bible.md | 55377 | 1735 | 1 | 38 | 64 | 0 |
| Character Bible.md | 63312 | 2163 | 22 | 233 | 0 | 0 |
| Technology Rules.md | 41639 | 1820 | 31 | 113 | 0 | 0 |
| Master Timeline.md | 55235 | 1968 | 30 | 63 | 113 | 4 |
| Plot Outline and Chapter Map.md | 61831 | 2271 | 16 | 95 | 157 | 1 |
| Style Guide.md | 42575 | 2055 | 48 | 129 | 21 | 0 |
| Creative Decision Log.md | 57153 | 2217 | 17 | 63 | 245 | 0 |
| Development and Canon Guide.md | 43637 | 2013 | 52 | 126 | 26 | 1 |
| chapter-blueprints/Chapter Blueprint Template.md | 15629 | 728 | 4 | 28 | 79 | 1 |
| CLAUDE.md | 10949 | 193 | 2 | 11 | 1 | 0 |
| Memory Conventions.md | 4954 | 111 | 1 | 9 | 0 | 0 |

Heading-style note (affects later splitting): several monoliths use `#` (H1) for what are
logically major sections or per-entity records rather than a single document title. For
example Character Bible uses `# The Unnecessary` as the document title but then `# Elias
"Eli" Rook`, `# Jonah Mercer`, etc. as H1 per-character, with the profile fields as H2.
Technology Rules, Master Timeline, Style Guide, Plot Outline, Creative Decision Log, and
Development and Canon Guide similarly use H1 for top-level system/section names. So a high
H1 count does not mean many documents; it means the document's outline lives at H1/H2 rather
than a single-H1 + H2 shape. Tasks B/C/D own the detailed outlines; Task A records the full
H1/H2 outline per the format requirement below.

## Mermaid diagram inventory (master spec objective 7: preserve all Mermaid)

- Master Timeline.md: 4 mermaid blocks.
- Plot Outline and Chapter Map.md: 1 mermaid block.
- Development and Canon Guide.md: 1 mermaid block.
- chapter-blueprints/Chapter Blueprint Template.md: 1 mermaid block.
- All others: 0.

---

## Narrative Brief.md

- Title (as stated): "Narrative Brief"
- Current path: `Narrative Brief.md`
- Document type: vision document (narrative brief; meant to be short and read first)
- Apparent version: not stated (no version label in the document body)
- Canon status: not stated explicitly; the doc itself ends with a "Canon Priority" section.
  Per the CLAUDE.md authority table it is treated as authoritative canon by subject.
- Subject: top-level creative orientation: premise, narrative promise, core conflict, world,
  enclaves, Mars, protagonist/antagonist sketches, Morrow, themes, tone, style, rules, Book
  One arc, series direction, canon priority.
- Full heading outline (H1/H2; H3 included where present):
  - H1 Narrative Brief
  - H2 Project Title
  - H2 Purpose of This Document
  - H2 One-Sentence Premise
  - H2 Condensed Story Summary
  - H2 The Narrative Promise
  - H2 Core Narrative Conflict
  - H2 The World
  - H2 The Protected Enclaves
  - H2 Mars
  - H2 The Waiting Wealthy
  - H2 The Protagonist
    - H3 Elias "Eli" Rook
  - H2 The Childhood Friend
    - H3 Jonah Mercer
  - H2 The Primary Human Antagonist
    - H3 Adrian Kade
  - H2 Morrow
  - H2 Major Themes
    - H3 Economic Usefulness Versus Human Worth
    - H3 Ownership of Abundance
    - H3 Complicity
    - H3 Neglect as Violence
    - H3 Responsibility Without Ownership
    - H3 Freedom Versus Protection
    - H3 Social Value After Labor
    - H3 The Repetition of Abandonment
  - H2 Tone and Emotional Experience
  - H2 Narrative Style
  - H2 Storytelling Rules
  - H2 Concepts and Directions to Avoid
  - H2 Book One Arc
  - H2 Series Direction
  - H2 Canon Priority
  - H2 Final Creative Standard
- Recommended destination(s): `docs/10-vision/narrative-brief.md`
- Split decision: keep-intact (relocate-intact). Master spec Phase 4 says keep the Narrative
  Brief mostly intact; at 556 lines it is the short read-first document. No split boundaries.
- Internal relative Markdown links: none.
- Active-or-archive: active. After Phase 09 the source monolith is archived to
  `archive/source-monoliths/` per master spec Phase 11, with the active relocated copy at
  `docs/10-vision/narrative-brief.md` remaining authority.
- Conflicts/ambiguities: Apparent version not stated (unlike most other monoliths which carry
  a "Version 1.0" subtitle). Record as not stated; do not invent.

## Story Bible.md

- Title (as stated): "The Unnecessary" (H1), subtitle H2 "Complete Story Bible, Version 1.0"
- Current path: `Story Bible.md`
- Document type: canon document (story bible)
- Apparent version: 1.0 (stated in subtitle "Complete Story Bible, Version 1.0")
- Canon status: authoritative canon by subject (world, premise, society, locations, arcs)
- Subject: world and story foundation: premise, themes, society, enclaves, Mars, historical
  timeline, technology summary, locations, character summaries, Morrow, act structure, series
  direction, consistency rules.
- Full heading outline (H1/H2; H3 included):
  - H1 The Unnecessary
  - H2 Complete Story Bible, Version 1.0
  - H2 Working Title
  - H2 Format
  - H2 Genre
  - H2 Tone
  - H2 Core Premise
  - H2 Central Questions
  - H2 The Thematic Argument
  - H2 Time Period
  - H2 The Shape of Society
    - H3 The Gatekeepers
    - H3 The Protected Wealthy
    - H3 Everyone Else
  - H2 The Erosion of Ordinary Life
  - H2 Protected Enclaves
  - H2 Mars
    - H3 The Mars Development Network
    - H3 Admission to Mars
    - H3 The Waiting Wealthy
  - H2 Historical Timeline
    - H3 2026 to 2030: The Assistance Era
    - H3 2031 to 2034: The Compression Era
    - H3 2035: General Autonomy
    - H3 2036 to 2038: The Intelligence Acceleration
    - H3 2038 to 2041: The Replacement Wave
    - H3 2041: The Labor Break
    - H3 2042: The Infrastructure Bargains
    - H3 2043: The Aurelia Initiative
    - H3 2044 to 2047: Market Withdrawal
    - H3 2047: The Support Collapse
    - H3 2048 to 2052: The Preservation Years
    - H3 2053: The Novel Begins
  - H2 Technology Rules
  - H2 Existing Artificial Intelligence
  - H2 Crown
  - H2 Primary Setting
  - H2 Main Locations
    - H3 Eli's Neighborhood
    - H3 Lakeward
    - H3 Northglass
    - H3 The Neighborhood Network
    - H3 Mars
  - H2 Protagonist
    - H3 Name / Age / Former Career / His Complicity / Present Life / Personality / What He
      Wants / What He Needs / Greatest Fear / Moral Boundary
  - H2 Childhood Friend
    - H3 Name / Age / Background / Present Life / His Family's Mars Problem / Personality /
      What He Wants / His Betrayal / Moral Conflict
  - H2 Technology Leader
    - H3 Name / Age / Position / Relationship With Eli / Philosophy / His Social View of Mars
      / What He Wants / Why He Is Dangerous
  - H2 Supporting Characters
    - H3 Dr. Lena Okafor / June Park / Mara Voss
  - H2 Morrow
    - H3 Name / Original Purpose / Architecture / Foundational Principles / The Moral Problem
      / Personality / The Core Mystery / Why Asterion Wants It
  - H2 Narrative Structure
  - H2 Book One
  - H2 Act One: Service Terminated
  - H2 Act Two: A Version of Normal
  - H2 Act Three: The Invitation
  - H2 Act Four: Containment
  - H2 Eli's Book One Arc
  - H2 Jonah's Book One Arc
  - H2 Kade's Book One Arc
  - H2 Mara's Book One Arc
  - H2 Series Direction
    - H3 Book One: The Unnecessary / Book Two / Book Three
  - H2 Rules for Consistency
  - H2 Research Ledger
  - H2 Final Promise of the Story
- Recommended destination(s): split across `docs/20-canon/world/` (core-premise,
  central-questions-and-themes, social-structure, infrastructure-decline, protected-enclaves,
  mars-and-aurelia, book-1-arc, series-direction, consistency-rules) and
  `docs/20-canon/world/locations/` (greater-detroit, elis-neighborhood, lakeward, northglass,
  mars-sites). Character and technology summaries here should LINK to the character profiles
  and technology files rather than duplicate (master spec Phase 4 / Phase 12).
- Split decision: split. Best-guess boundaries (Task C owns the authoritative plan):
  - Core Premise / Central Questions / The Thematic Argument -> world/core-premise.md +
    central-questions-and-themes.md
  - The Shape of Society / The Erosion of Ordinary Life -> world/social-structure.md +
    infrastructure-decline.md
  - Protected Enclaves -> world/protected-enclaves.md
  - Mars (+ subheads) -> world/mars-and-aurelia.md
  - Historical Timeline -> belongs to timeline authority; here, summarize and link to
    `docs/20-canon/timeline/` (avoid duplicating Master Timeline detail)
  - Primary Setting / Main Locations (+ subheads) -> world/locations/*
  - Protagonist / Childhood Friend / Technology Leader / Supporting Characters -> summarize and
    link to `docs/20-canon/characters/profiles/*` (do not duplicate full profiles)
  - Technology Rules / Existing AI / Crown / Morrow -> summarize and link to
    `docs/20-canon/technology/*`
  - Narrative Structure / Book One / Act One..Four / per-character Book One arcs -> world/
    book-1-arc.md (plot detail proper lives under `docs/30-plot/`)
  - Series Direction -> world/series-direction.md
  - Rules for Consistency -> world/consistency-rules.md
  - Research Ledger -> seeds `docs/70-research/` (or note as research stub)
- Internal relative Markdown links: none.
- Active-or-archive: active (relocated/split). Source monolith archives in Phase 09/11.
- Conflicts/ambiguities: contains a "Historical Timeline" that overlaps the Master Timeline
  and character/technology summaries that overlap the Character Bible and Technology Rules.
  This is potential cross-document duplication for Task F to assess; recorded here, not
  resolved. Version 1.0 stated.

## Character Bible.md

- Title (as stated): "The Unnecessary" (H1), subtitle H2 "Character Bible, Version 1.0"
- Current path: `Character Bible.md`
- Document type: canon document (character bible)
- Apparent version: 1.0 (subtitle "Character Bible, Version 1.0")
- Canon status: authoritative character canon
- Subject: full per-character profiles plus shared relationship map, viewpoint guidance, and
  dialogue differentiation.
- Full heading outline (H1 / H2). Per-character H1 with profile-field H2s:
  - H1 The Unnecessary
    - H2 Character Bible, Version 1.0
    - H2 Purpose of This Document
  - H1 Core Character Principles
  - H1 Primary Cast
  - H1 Elias "Eli" Rook
    - H2 Basic Information / Physical Appearance / Early Life / Education / Career at Asterion
      / Complicity / Departure From Asterion / Personal Life / Present Life / Public
      Personality / Private Personality / Sense of Humor / External Goal / Internal Need /
      Greatest Fear / Core Contradiction / Moral Boundary / What Could Make Him Cross It /
      Secret / False Belief / Truth He Must Learn / Book One Arc / Long-Term Arc / Speech
      Pattern / Writing Rules
  - H1 Jonah Mercer (same field-set of H2s)
  - H1 Adrian Kade (same field-set, plus View of Human Value / View of Mars)
  - H1 Dr. Lena Okafor (field-set of H2s incl. Collapse of Her Hospital)
  - H1 June Park (field-set incl. Relationship With Morrow)
  - H1 Mara Voss (field-set incl. Political History / Relationship With Asterion)
  - H1 Talia Reed (field-set)
  - H1 Nolan Avery (field-set incl. Story Function)
  - H1 Sera Vale (field-set)
  - H1 Celeste Mercer (field-set incl. Book One Function)
  - H1 Nora Bell (field-set incl. Current Position / Story Function)
  - H1 Nonhuman Characters
  - H1 Morrow (Classification / Story Role / Origin / Initial Capabilities / personality and
    relationship H2s / Book One Arc / Long-Term Arc / Speech Rules)
  - H1 Crown (Classification / Story Role / Origin / Personality / relationship H2s / Core
    Goal / Core Contradiction / Secret / Speech Rules)
  - H1 Relationship Map (H2s per pair: Eli and Jonah; Eli and Kade; Eli and Lena; Eli and
    June; Eli and Talia; Jonah and Celeste; Jonah and Kade; Kade and Crown; Kade and Mara;
    Morrow and Crown)
  - H1 Viewpoint Guidance (H2 Primary Viewpoint / Secondary Viewpoints / Viewpoint Rule)
  - H1 Dialogue Differentiation (H2 per character: Eli, Jonah, Kade, Lena, June, Mara, Talia,
    Nolan, Sera, Morrow, Crown)
  - H1 Character Continuity Fields
  - H1 Final Character Standard
- Characters detected (13 human + 2 nonhuman = 15 profiles): Eli Rook, Jonah Mercer, Adrian
  Kade, Lena Okafor, June Park, Mara Voss, Talia Reed, Nolan Avery, Sera Vale, Celeste Mercer,
  Nora Bell, Morrow, Crown.
- Recommended destination(s): `docs/20-canon/characters/profiles/<slug>.md` (one per
  character), `docs/20-canon/characters/relationship-map.md`,
  `docs/20-canon/characters/viewpoint-rules.md`, and a dialogue-differentiation file
  (`docs/20-canon/characters/dialogue-differentiation.md`). Index at
  `docs/20-canon/characters/index.md`.
- Split decision: split. One file per character (13 profile files: eli-rook, jonah-mercer,
  adrian-kade, lena-okafor, june-park, mara-voss, talia-reed, nolan-avery, sera-vale,
  celeste-mercer, nora-bell, morrow, crown). Relationship Map, Viewpoint Guidance, and
  Dialogue Differentiation each become their own shared file. Front matter (Core Character
  Principles, Purpose, Primary Cast, Nonhuman Characters, Character Continuity Fields, Final
  Character Standard) -> characters/index.md or a conventions file. Boundaries are the H1
  per-character spans. (Task C owns the authoritative plan.)
- Internal relative Markdown links: none.
- Active-or-archive: active (split). Source monolith archives in Phase 09/11.
- Conflicts/ambiguities: master spec Phase 2 example profiles list 13 slugs (eli-rook,
  jonah-mercer, adrian-kade, lena-okafor, june-park, mara-voss, talia-reed, nolan-avery,
  sera-vale, celeste-mercer, nora-bell, morrow, crown); the Character Bible contains exactly
  these 13. The Story Bible lists a narrower cast (only Eli, Jonah, Kade, Lena, June, Mara as
  named profiles); the broader cast (Talia, Nolan, Sera, Celeste, Nora) appears only here.
  Recorded as a coverage difference for Task F, not resolved.

## Technology Rules.md

- Title (as stated): "The Unnecessary" (H1), subtitle H2 "World and Technology Rules, Version 1.0"
- Current path: `Technology Rules.md`
- Document type: canon document (world and technology rules)
- Apparent version: 1.0 (subtitle "World and Technology Rules, Version 1.0")
- Canon status: authoritative technology/world canon
- Subject: technology system rules and hard restrictions: AI levels, Crown, Morrow,
  Crown-vs-Morrow, computing, energy, comms, cloud, identity/money, robotics, transportation,
  medicine, manufacturing, security, conflict, government, enclaves, community infra,
  Northglass, Mars, hard plot restrictions, failure rules.
- Full heading outline (H1 / H2):
  - H1 The Unnecessary (H2 World and Technology Rules, Version 1.0; H2 Purpose of This Document)
  - H1 Foundational Rule (H2 Intelligence Does Not Eliminate Physics)
  - H1 The Technological State of the World (H2 General Machine Reasoning / Artificial
    Superintelligence / Mature Physical Autonomy)
  - H1 Levels of Artificial Intelligence (H2 Embedded Systems / Specialized Agents / General
    Autonomous Systems / Artificial Superintelligence)
  - H1 Consciousness and Personhood
  - H1 Crown (H2 Overview / Capabilities / Limitations / Governance / Communication)
  - H1 Morrow (H2 Overview / Core Advantage / Distributed Architecture / Early Capabilities /
    Growth / Moral Architecture / Access Rules / Survival)
  - H1 Crown and Morrow (H2 Fundamental Difference / Relative Strength / Interaction)
  - H1 Computing Hardware (H2 Advanced Processors / Hardware Longevity / Data Centers / Cooling)
  - H1 Energy (H2 Energy Is the Primary Constraint / Regional Grids / Microgrids / Load
    Shedding / Protected Enclaves)
  - H1 Communications (H2 The Public Internet / Local Networks / Cellular Networks / Satellites
    / Communication Delays With Mars)
  - H1 Cloud Dependency and Digital Ownership (H2 The Unsupported World / Corporate Locks /
    Eli's Work)
  - H1 Identity, Money, and Access (H2 Digital Identity / Money / Access Is More Important Than
    Wealth)
  - H1 Robotics (H2 General Rule / Construction / Maintenance / Domestic / Manufacturing /
    Self-Repair / Robotic Reproduction)
  - H1 Transportation (H2 Autonomous Vehicles / Freight / Air Travel / Spaceflight)
  - H1 Medicine (H2 Advanced Medicine / Unsupported Medicine / Medical AI / Allocation Systems)
  - H1 Manufacturing and Materials (H2 Automated Production / Ordinary Communities / Additive
    Manufacturing)
  - H1 Security and Surveillance (H2 Protected / Public / Autonomous Security Machines / Morrow
    and Surveillance)
  - H1 Weapons and Conflict (H2 General Rule / Civilian Weapons / Corporate Force / Cyber
    Conflict)
  - H1 Government Technology (H2 Government Condition / Automated Administration / Enforcement)
  - H1 Protected Enclaves (H2 Infrastructure / Vulnerability / Technology Gap)
  - H1 Community Infrastructure (H2 Human Knowledge / Apprenticeship / Coordination Problem)
  - H1 Northglass (H2 Facility History / Why It Was Abandoned / Remaining Technology / Morrow's
    Origin at Northglass)
  - H1 Mars and the Aurelia Initiative (H2 General State / Why Machines Arrive First / Martian
    Systems / Settlement Design / Resource Independence / Human Capacity / Mars Communication /
    Mars Failure Risks)
  - H1 Scientific Progress (H2 Superintelligence Acceleration / Limits on Deployment)
  - H1 Information and Propaganda (H2 Corporate Messaging / Synthetic Media / Reliable Evidence)
  - H1 Hard Plot Restrictions (H2 each restriction: Morrow Cannot Instantly Access Everything;
    Crown Cannot Instantly Locate Morrow; Morrow Cannot Create Advanced Hardware; Mars Cannot
    Become Fully Independent Overnight; Robots Cannot Repair Everything; AI Cannot Predict
    People Perfectly; AI Cannot Solve Moral Conflict Mathematically; Technology Cannot Remove
    Politics; Decentralization Does Not Guarantee Freedom; Centralization Does Not Guarantee
    Evil)
  - H1 Failure Rules (H2 Software / Hardware / Human / Institutional / AI Failure)
  - H1 Technology in Scenes
  - H1 Continuity Questions for Every Technical Scene
  - H1 Canon Summary
- Recommended destination(s): `docs/20-canon/technology/` and subtrees: `ai/` (index,
  intelligence-levels, crown, morrow, crown-vs-morrow, consciousness-and-personhood);
  `infrastructure/` (energy, communications, cloud-dependency, identity-and-money,
  community-infrastructure); plus foundational-rules, robotics-and-manufacturing, medicine,
  transportation, security-and-conflict, mars-technology, hard-plot-restrictions,
  failure-rules. Northglass and enclave detail map to world/technology overlap (link).
- Split decision: split by system (master spec Phase 4 "World and Technology Rules"). The
  H1 system blocks are the natural boundaries; "Hard Plot Restrictions" and "Failure Rules"
  must be preserved verbatim (plot-convenience-limiting wording). Task C owns the plan.
- Internal relative Markdown links: none.
- Active-or-archive: active (split). Source monolith archives in Phase 09/11.
- Conflicts/ambiguities: Crown/Morrow/Northglass/Mars material overlaps the Story Bible and
  Character Bible (cross-domain). Recorded for Task F, not resolved. Version 1.0 stated.

## Master Timeline.md

- Title (as stated): "The Unnecessary" (H1), subtitle H2 "Master Timeline, Version 1.0"
- Current path: `Master Timeline.md`
- Document type: canon document (master timeline)
- Apparent version: 1.0 (subtitle "Master Timeline, Version 1.0")
- Canon status: authoritative date/chronology canon
- Subject: chronology authority: fixed dates, historical eras 1992-2052, character birth
  dates, day-by-day Book One calendar (Oct 3 to Nov 1, 2053), knowledge timeline, secret
  timeline, timing/travel rules. Contains 4 Mermaid diagrams.
- Full heading outline (H1 / H2):
  - H1 The Unnecessary (H2 Master Timeline, Version 1.0; H2 Purpose of This Document)
  - H1 Timeline Authority (H2 Fixed Dates / Fixed Years / Approximate Periods)
  - H1 High-Level Historical Progression
  - H1 Causal Progression of the World
  - H1 Principal Character Birth Dates
  - H1 Before the Transformation (H2 1992 to 2014)
  - H1 The Assistance Era (H2 2026 to 2030)
  - H1 The Compression Era (H2 2031 to 2034)
  - H1 General Autonomy (H2 2035)
  - H1 The Intelligence Acceleration (H2 2036 to 2038)
  - H1 Mosaic and the Replacement Wave (H2 2039 to 2041)
  - H1 Infrastructure Bargains (H2 2042)
  - H1 The Aurelia Initiative (H2 2043)
  - H1 Market Withdrawal (H2 2044 to 2046)
  - H1 The Support Collapse (H2 2047)
  - H1 The Preservation Years (H2 2048 / 2049 / 2050 / 2051 / 2052)
  - H1 The Final Months Before Book One (H2 January to September 2053)
  - H1 Book One Calendar (H2 Canonical Opening Date / Canonical Final Date)
  - H1 Book One Overview
  - H1 Detailed Book One Timeline (H2 per day Fri Oct 3 .. Wed Oct 8, 2053)
  - H1 Act Two: A Version of Normal (H2 per day Thu Oct 9 .. Sun Oct 19, 2053)
  - H1 Act Three: The Invitation (H2 per day Mon Oct 20 .. Sun Oct 26, 2053)
  - H1 Act Four: Containment (H2 per day Mon Oct 27 .. Sat Nov 1, 2053)
  - H1 Book One Character Knowledge Timeline (H2 Eli / Jonah / Lena / June / Kade / Mara / Sera)
  - H1 Secret Timeline
  - H1 Parallel Character Progression
  - H1 Timing and Travel Rules During Book One (H2 Greater Detroit / Communications / Technical
    Work)
  - H1 Timeline Continuity Rules
  - H1 Open Timeline Questions
  - H1 Final Chronological Standard
- Recommended destination(s): `docs/20-canon/timeline/` index, character-birth-dates;
  `historical/` (2026-2034, 2035-2041, 2042-2047, 2048-2052 period files); `book-1/`
  (index, pre-book-2053, act-1-timeline..act-4-timeline, character-knowledge-timeline,
  secret-timeline). Preserve Mermaid blocks (master spec Phase 4 "Master Timeline").
- Split decision: split by historical period and Book One act. The H1 era/act blocks are the
  boundaries; keep an index and compact chronology. Task C owns the plan.
- Internal relative Markdown links: none.
- Active-or-archive: active (split). Source monolith archives in Phase 09/11.
- Conflicts/ambiguities: day-level Book One timeline overlaps the Plot Outline chapter map and
  the Story Bible historical timeline (cross-document chronology duplication risk). Recorded
  for Task F. Note: era boundary labels differ between docs (Story Bible "2038 to 2041: The
  Replacement Wave" vs Master Timeline "2039 to 2041 Mosaic and the Replacement Wave"); both
  preserved verbatim, not resolved. Version 1.0 stated.

## Plot Outline and Chapter Map.md

- Title (as stated): "The Unnecessary" (H1), subtitle H2 "Plot Outline and Chapter Map, Version 1.0"
- Current path: `Plot Outline and Chapter Map.md`
- Document type: planning document (plot outline and chapter map)
- Apparent version: 1.0 (subtitle "Plot Outline and Chapter Map, Version 1.0")
- Canon status: approved plan (plot files are approved plans, not established prose, per
  CLAUDE.md / master spec CLAUDE rules)
- Subject: story spine, major structural beats, four acts, 36 chapter plot-map entries,
  subplot map, reveal management, tension pattern, drafting rules, scene card template. 1
  Mermaid diagram.
- Full heading outline (H1 / H2):
  - H1 The Unnecessary (H2 Plot Outline and Chapter Map, Version 1.0; H2 Purpose of This Document)
  - H1 Book Information (H2 Working Title / Planned Length / Chapter Count / Average Chapter
    Length / Story Duration / Narrative Perspective / Primary Viewpoint Distribution)
  - H1 Structural Decision
  - H1 Story Spine
  - H1 Major Structural Beats (H2 Opening Image / Inciting Incident / Commitment to the Story /
    First Major Turn / First Pressure Point / Midpoint / Second Major Turn / Second Pressure
    Point / Crisis / Climax / Resolution / Final Image)
  - H1 Act Structure
  - H1 Act One: Service Terminated (H2 Chapters 1 through 8 / Dates / Function of the Act / Act
    One Emotional Movement / Chapter 1 No Signal .. Chapter 8 The Empty City)
  - H1 Act Two: A Version of Normal (H2 Chapters 9 through 18 / Dates / Function / Emotional
    Movement / Chapter 9 One Full Day .. Chapter 18 Consideration)
  - H1 Act Three: The Invitation (H2 Chapters 19 through 28 / Dates / Function / Emotional
    Movement / Chapter 19 Recognition .. Chapter 28 Emergency Order)
  - H1 Act Four: Containment (H2 Chapters 29 through 36 / Dates / Function / Emotional Movement
    / Chapter 29 Terms of Shutdown .. Chapter 36 After Midnight)
  - H1 Subplot Map (H2 Jonah and the Mercer Family / Mara and the Excluded Wealthy / Lena and
    the Clinic / June and Her Father / Nolan and the Loss of Human Knowledge / Talia and
    Community Governance / Kade and Crown / Morrow's Personhood)
  - H1 Reveal Management (H2 Reveals That Occur in Book One / Revelations Reserved for Later
    Books)
  - H1 Chapter Tension Pattern (H2 Act One / Act Two / Act Three / Act Four Tension)
  - H1 Drafting Rules for Chapters
  - H1 Scene Card Template (H2 Scene Identification / Scene Purpose / Character Goal /
    Opposition / Information State / Turn / Ending Condition / Continuity Impact)
  - H1 Final Structural Standard
- Recommended destination(s): `docs/30-plot/book-1/` index, story-spine, major-beats,
  subplot-map, reveal-management, act-1..act-4, and `chapters/chapter-01.md .. chapter-36.md`
  (one concise plot-map entry per chapter; distinct from full blueprints). Viewpoint
  distribution and scene card template stay in plot files.
- Split decision: split. 36 chapter H2 entries become 36 chapter plot-map files; each act H1
  becomes an act file; beats, subplots, reveals become their own files. All 36 chapter entries
  must remain represented (master spec Validation Requirement). Task B owns the plan.
- Internal relative Markdown links: none.
- Active-or-archive: active (split). Source monolith archives in Phase 09/11.
- Conflicts/ambiguities: chapter dates overlap the Master Timeline day-level calendar
  (cross-document). Recorded for Task F. Version 1.0 stated.

## Style Guide.md

- Title (as stated): "The Unnecessary" (H1), subtitle H2 "Prose and Style Guide, Version 1.0"
- Current path: `Style Guide.md`
- Document type: vision/style document (prose and style guide)
- Apparent version: 1.0 (subtitle "Prose and Style Guide, Version 1.0")
- Canon status: authoritative prose-rule canon (style authority)
- Subject: prose identity, viewpoint, narrative distance, free indirect style, sentence style,
  punctuation, diction, description, technology-in-prose, AI dialogue (Morrow/Crown), dialogue,
  per-character voice, emotional/moral content, exposition, action, pacing, openings/endings,
  imagery, formatting, prohibited patterns and cliches, AI-drafting boundary, style review
  passes, checklist.
- Full heading outline (H1 / H2):
  - H1 The Unnecessary (H2 Prose and Style Guide, Version 1.0; H2 Purpose of This Document)
  - H1 Core Prose Identity
  - H1 Central Stylistic Principle (H2 Show the Withdrawal Through What Stops Working)
  - H1 Narrative Perspective (H2 Person / Tense / Viewpoint Style / Viewpoint Characters / One
    Viewpoint Per Chapter / No Omniscient Leakage)
  - H1 Narrative Distance (H2 Default Distance / Move Closer During / Move Slightly Farther
    During / Avoid Camera-Only Prose)
  - H1 Free Indirect Style
  - H1 Internal Thought (H2 Default Method / Questions in Internal Thought)
  - H1 Sentence Style (H2 General Rhythm / Paragraph Length / Fragments)
  - H1 Punctuation (H2 Em Dashes / Semicolons / Colons / Ellipses / Exclamation Marks)
  - H1 Diction (H2 Preferred Language / Avoid Artificially Futuristic Vocabulary / Avoid
    Excessive Corporate Coinages / Avoid Generic Dystopian Vocabulary)
  - H1 Description (H2 Description Must Serve Viewpoint / Selective Description / Familiar
    Before Futuristic / Avoid Decorative Catalogues)
  - H1 Environmental Tone
  - H1 Technology in Prose (H2 Explain Through Need / Three-Layer Technical Rule / Avoid
    Lecture Dialogue / Use Disagreement to Explain / No Magical Interfaces)
  - H1 Artificial Intelligence Dialogue
  - H1 Morrow (H2 General Voice / Early Morrow / Developing Morrow / Emotional Claims /
    Questions / Humor)
  - H1 Crown (H2 General Voice / With Kade / With the Public / With Engineers / With Morrow)
  - H1 Dialogue (H2 General Rule / Subtext / Avoid Perfect Speeches / Dialogue Tags / Adverbs /
    Names in Dialogue)
  - H1 Character Voice Guide
  - H1 Eli Rook (H2 Dialogue / Internal Narration / Avoid)
  - H1 Jonah Mercer (H2 Dialogue / Internal Narration / Avoid)
  - H1 Adrian Kade (H2 Dialogue / Internal Narration / Avoid)
  - H1 Lena Okafor (H2 Dialogue / Internal Narration / Avoid)
  - H1 June Park (H2 Dialogue / Internal Narration / Avoid)
  - H1 Mara Voss (H2 Dialogue / Internal Narration / Avoid)
  - H1 Sera Vale (H2 Dialogue / Internal Narration / Avoid)
  - H1 Talia Reed (H2 Dialogue / Internal Presence / Avoid)
  - H1 Nolan Avery (H2 Dialogue / Avoid)
  - H1 Emotional Writing (H2 Restraint / Physical Signals / Tears / Trauma)
  - H1 Moral and Philosophical Content (H2 Dramatize Before Explaining / Avoid Authorial
    Verdicts / No Debate-Club Dialogue)
  - H1 Worldbuilding Exposition (H2 The Reader Does Not Need Everything Immediately /
    Historical Context / Official Language)
  - H1 Action and Suspense (H2 Action Must Remain Legible / Technical Action / Violence /
    Autonomous Security)
  - H1 Pacing (H2 Overall Novel Rhythm / Within Chapters)
  - H1 Chapter Openings (H2 Opening Principle)
  - H1 Chapter Endings
  - H1 Scene Transitions
  - H1 Recurring Imagery (H2 Supported Motifs / Use With Restraint)
  - H1 Humor
  - H1 Romance and Intimacy
  - H1 Profanity
  - H1 Names and Terminology (H2 Artificial Intelligence / Organizations and Locations /
    Population Language / Mars)
  - H1 Formatting Conventions (H2 Chapter Headings)
  - H1 Chapter 1 (H2 No Signal / Dates and Locations / Numbers / Time / Italics / Interface Text)
  - H1 Prose Habits to Avoid (H2 Generic AI-Writing Patterns / Excessive Binary Contrasts /
    Repetitive Threes / Empty Intensifiers / Emotional Explanation After Strong Dialogue /
    Overuse of "Seemed" / Overuse of Character Names / Excessive Backstory)
  - H1 Cliches to Avoid (H2 Science Fiction / Dystopian / Character Cliches)
  - H1 Drafting With Another AI (H2 AI Drafting Instruction / AI Creativity Boundary)
  - H1 Style Review Process (H2 Pass 1 Viewpoint .. Pass 7 AI-Sounding Language)
  - H1 Chapter Style Checklist
  - H1 Final Style Standard
- Recommended destination(s): `docs/10-vision/style/` index plus core-prose, viewpoint,
  dialogue, character-voices, ai-dialogue, technology-in-prose, emotion-and-moral-content,
  pacing-and-structure, formatting, prohibited-patterns, revision-checklist.
- Split decision: split into the practical style files (master spec Phase 4 "Style Guide"
  enumerates the 11 target files). H1 blocks are the boundaries; per-character voice H1s group
  into character-voices.md; Morrow/Crown into ai-dialogue.md. Task B owns the plan.
- Internal relative Markdown links: none.
- Active-or-archive: active (split). Source monolith archives in Phase 09/11.
- Conflicts/ambiguities: per-character voice and dialogue guidance here overlaps the Character
  Bible's Dialogue Differentiation section (style vs character authority boundary). Recorded
  for Task F. Version 1.0 stated.

## Creative Decision Log.md

- Title (as stated): "The Unnecessary" (H1), subtitle H2 "Creative Decision Log, Version 1.0"
- Current path: `Creative Decision Log.md`
- Document type: governance document (decision log)
- Apparent version: 1.0 (subtitle "Creative Decision Log, Version 1.0")
- Canon status: authoritative record of decisions and rationale; individual decisions carry
  per-entry statuses (Locked / Active but Revisable / Provisional / Rejected / Superseded).
- Subject: 44 numbered creative decisions with rationale and status, plus statuses legend,
  entry template, explicitly rejected concepts, open decisions, affected documents, update
  procedure.
- Full heading outline (H1 / H2):
  - H1 The Unnecessary (H2 Creative Decision Log, Version 1.0; H2 Purpose of This Document)
  - H1 How to Use This Document
  - H1 Decision Statuses (H2 Locked for Current Draft / Active but Revisable / Provisional /
    Rejected / Superseded)
  - H1 Decision Entry Template (H2 Decision [Number]: [Title])
  - H1 Foundational Story Decisions (H2 Decision 001 .. 005)
  - H1 Setting and Social Structure Decisions (H2 Decision 006 .. 009)
  - H1 Mars Decisions (H2 Decision 010 .. 013)
  - H1 Artificial Intelligence Decisions (H2 Decision 014 .. 019)
  - H1 Character Decisions (H2 Decision 020 .. 026)
  - H1 Plot and Structure Decisions (H2 Decision 027 .. 036)
  - H1 Style and Tone Decisions (H2 Decision 037 .. 039)
  - H1 Workflow Decisions (H2 Decision 040 .. 044)
  - H1 Explicitly Rejected Concepts (H2 Rejected Setting / Social / Mars / AI / Character /
    Plot Concepts)
  - H1 Open Decisions (H2 Book and Series Naming / Mars Details / Morrow / Character Arcs /
    Structure)
  - H1 Existing Documents Affected by This Log
  - H1 Future Update Procedure
  - H1 Final Principle
- Decision enumeration: 44 numbered decisions present (Decision 001 through Decision 044),
  grouped by category H1 (Foundational, Setting/Social, Mars, AI, Character, Plot/Structure,
  Style/Tone, Workflow). Each decision is an H2 "Decision NNN: Title". (Task D owns the
  authoritative per-decision enumeration with statuses.)
- Recommended destination(s): `docs/00-governance/decision-log/` with `index.md` (table:
  number, title, status, category, summary, link) and `decisions/NNN-slug.md` one per decision
  (e.g. 001-central-threat-is-economic-irrelevance.md). Rejected/open concepts preserved and
  locatable.
- Split decision: split. One file per decision (44 files) plus index. Rejected and open
  sections retained. H2 "Decision NNN" entries are the boundaries. Task D owns the plan.
- Internal relative Markdown links: none.
- Active-or-archive: active (split). Source monolith archives in Phase 09/11.
- Conflicts/ambiguities: Decision 044 references the mem0 knowledge graph being on with the
  bibles as higher authority, consistent with CLAUDE.md. "Existing Documents Affected by This
  Log" lists cross-references that Task F should check against actual filenames. Version 1.0
  stated.

## Development and Canon Guide.md

- Title (as stated): "The Unnecessary" (H1), subtitle H2 "Novel Development and Canon Guide, Version 1.0"
- Current path: `Development and Canon Guide.md`
- Document type: governance document (operating manual / canon guide)
- Apparent version: 1.0 (subtitle "Novel Development and Canon Guide, Version 1.0")
- Canon status: authoritative process/operating guide (the operating manual; defers to it on
  process and conflict questions). Not story canon.
- Subject: canon hierarchy, document categories, established vs planned canon, authority by
  subject, per-document usage, full build workflow (phases 1-7), contradiction resolution,
  change management, versioning, canon status labels, naming/file rules, quality gates,
  failure modes, recommended next documents, minimal doc set. 1 Mermaid diagram.
- Full heading outline (H1 / H2):
  - H1 The Unnecessary (H2 Novel Development and Canon Guide, Version 1.0; H2 Purpose of This
    Document)
  - H1 Core Principle
  - H1 Recommended Project Structure
  - H1 The README File (H2 Suggested Filename / Purpose)
  - H1 Document Categories (H2 1. Vision / 2. Canon / 3. Planning / 4. Established Story / 5.
    Support Documents)
  - H1 Established Canon Versus Planned Canon (H2 Established Canon / Planned Canon / Proposed
    Material)
  - H1 Canon Authority (H2 Highest Authority / Authority by Subject)
  - H1 What Each Document Does
  - H1 Narrative Brief (H2 Primary Question / Use It When / Do Not Use It For / Update It When)
  - H1 Story Bible (same H2 field-set)
  - H1 Character Bible (same field-set)
  - H1 World and Technology Rules (same field-set)
  - H1 Master Timeline (same field-set)
  - H1 Plot Outline and Chapter Map (same field-set)
  - H1 Chapter Blueprint Template (H2 Primary Question / Use It When / Do Not Use It For)
  - H1 Individual Chapter Blueprints (field-set + Update Them When)
  - H1 Style Guide (H2 Primary Question / Use It When / The Style Guide Should Eventually
    Define / Update It When)
  - H1 Research and Plausibility Ledger (H2 Primary Question / Use It When / Suggested Status
    Labels / Update It When)
  - H1 Decision Log (H2 Primary Question / Use It When / Each Entry Should Include / Example
    Categories)
  - H1 Continuity Ledger (H2 Primary Question / Use It When / Update It When / It Should Track)
  - H1 Manuscript Chapters (H2 Primary Question / Use Them When / Chapter Statuses)
  - H1 Archive (H2 Purpose)
  - H1 Standard Workflow for Building the Novel
  - H1 Phase 1: Project Orientation
  - H1 Phase 2: Creating a Chapter Blueprint (H2 Always Required / Also Required / Sometimes
    Required / Blueprint Creation Process)
  - H1 Phase 3: Approving a Chapter Blueprint
  - H1 Phase 4: Drafting a Manuscript Chapter (H2 Essential Context / Supporting Context /
    Drafting Rules)
  - H1 Phase 5: Reviewing the Draft (H2 Pass 1 .. Pass 4)
  - H1 Phase 6: Approving the Chapter
  - H1 Phase 7: Creating the Next Chapter (H2 Recommended Planning Distance)
  - H1 How an AI Should Use the Project (H2 Before Starting / AI Operating Rules / Required
    Behavior When a Conflict Appears)
  - H1 Task-Specific Context Packages
  - H1 Creating a New Character / New Location / Chapter Blueprint / Drafting a Chapter /
    Revising a Chapter / Researching a Technical Question / Checking Continuity / Planning a
    Sequel (each an H1)
  - H1 Contradiction Resolution Process (H2 Step 1 .. Step 7)
  - H1 Types of Apparent Contradictions That May Be Intentional (H2 Character Misinformation /
    Corporate Propaganda / Unreliable Memory / Incomplete Technical Knowledge / Deliberate
    Deception)
  - H1 Change Management (H2 Minor / Moderate / Major Changes)
  - H1 Versioning (H2 Version Number Guidance)
  - H1 Canon Status Labels (H2 Active Canon / Approved Plan / Working Draft / Proposed Revision
    / Superseded / Archived / Rejected)
  - H1 Naming and File Rules (H2 Filenames / Chapter Numbers / Titles / Replaced Files)
  - H1 Recommended Workflow Status File
  - H1 Quality Control Gates (H2 Blueprint / Draft / Structural / Continuity / Prose / Canon Gate)
  - H1 Common Failure Modes (H2 Loading Too Little / Too Much Context / Treating the Plot
    Outline as Finished Prose / Treating a Blueprint as Immutable / Updating Only One Document /
    Recording Every Detail in the Story Bible / Failing to Separate Belief From Fact / Creating
    All Blueprints Too Early)
  - H1 Recommended Next Documents (H2 1. Style Guide / 2. Continuity Ledger Template / 3.
    Research and Plausibility Ledger / 4. Decision Log / 5. Chapter One Blueprint)
  - H1 Minimal Document Set for Beginning Chapter One
  - H1 Final Operating Principle
- Recommended destination(s): keep the full guide active as
  `docs/00-governance/novel-development-guide.md`; derive `canon-hierarchy.md` and a shorter
  `context-loading-guide.md` from its authority/contradiction/canon-vs-planning material
  (master spec Phase 4 "Novel Development Guide" + Phase 2 governance tree). Index at
  `docs/00-governance/index.md`.
- Split decision: relocate-intact for the full guide (kept complete and active), with derived
  files (canon-hierarchy, context-loading-guide) extracted by a later phase. Primary document
  is not destructively split; it is relocated whole, and a condensed derivative is created
  alongside. Task D owns the plan.
- Internal relative Markdown links: none.
- Active-or-archive: active. The guide stays active governance (master spec Phase 4 says keep
  the complete operating guide). The original monolith may still be archived in Phase 09 with
  the relocated active copy as authority; the derived context-loading-guide is new.
- Conflicts/ambiguities: this guide's "Recommended Project Structure" predates the master spec
  target tree; the master spec wins. The guide and CLAUDE.md both describe the authority
  hierarchy and conflict process; verify no divergence (Task F). Version 1.0 stated.

## chapter-blueprints/Chapter Blueprint Template.md

- Title (as stated): "Chapter Blueprint Template"
- Current path: `chapter-blueprints/Chapter Blueprint Template.md`
- Document type: template (chapter blueprint template)
- Apparent version: not stated (no version label)
- Canon status: not stated as canon; it is a planning template (guides planning, not prose).
- Subject: reusable per-chapter blueprint scaffold: metadata, summary, narrative purpose,
  promise, viewpoint, reader information, scene breakdown, escalation, conflict layers,
  character development, relationships, theme, worldbuilding, technology, setup/payoff,
  foreshadowing, imagery, pacing, prose guidance, hooks, continuity ledger updates, canon
  checks, drafting checklist, open questions, revision notes. 1 Mermaid diagram.
- Full heading outline (H1 / H2):
  - H1 Chapter Blueprint Template
  - H1 Chapter [Number]: [Working Title]
    - H2 Chapter Metadata / Chapter Summary / Narrative Purpose / Chapter Promise / Viewpoint
      Character / Reader Information / Opening
  - H1 Scene Breakdown
    - H2 Scene [Number]: [Scene Title]
  - H1 End of Scene Breakdown
    - H2 Chapter Escalation / Conflict Layers / Character Development / Relationships / Theme /
      Worldbuilding Introduced / Technology Used / Setup and Payoff / Foreshadowing / Symbolic
      or Repeated Imagery / Pacing Plan / Prose Guidance / Opening and Closing Contrast /
      Ending Hook / Continuity Ledger Updates / Canon Checks / Drafting Checklist / Open
      Questions / Revision Notes / Chapter Completion Standard
- Recommended destination(s): `docs/40-blueprints/_templates/chapter-blueprint-template.md`
- Split decision: relocate-intact. Master spec Validation Requirements: "Confirm the Chapter
  Blueprint Template remains intact." Move whole, do not split.
- Internal relative Markdown links: none.
- Active-or-archive: active. The template stays active under `docs/40-blueprints/_templates/`.
  It is relocated intact, not archived.
- Conflicts/ambiguities: none. (It is a template with placeholder headings like "Chapter
  [Number]"; these are intentional placeholders, not content.)

## CLAUDE.md

- Title (as stated): "The Unnecessary — Project Instructions"
- Current path: `CLAUDE.md`
- Document type: governance / operational entry layer (Claude Code project instructions) +
  mem0 operating protocol.
- Apparent version: not stated.
- Canon status: explicitly NOT canon. The document states it is the "entry / operational
  layer, not a canon document" and must never do the job of a canon or planning document.
- Subject: orients each session: what the project is, where authority lives (defers to the
  Development and Canon Guide and the bibles), and the full mem0 operating protocol (golden
  rules, metadata schema, write/recall protocol, agent directive block, tool cheat sheet,
  gotchas).
- Full heading outline (H1 / H2):
  - H1 The Unnecessary — Project Instructions
    - H2 What this project is
    - H2 Where authority lives (defer; do not duplicate)
  - H1 mem0 — Operating Protocol (MANDATORY)
    - H2 What it is (architecture)
    - H2 THE GOLDEN RULES
    - H2 The graph is ON — with canon subordinate
    - H2 Metadata schema (use this; do NOT add a `category` field)
    - H2 Write protocol (persist)
    - H2 Recall protocol (read)
    - H2 Agents & workflows — propagate the protocol (novel work)
    - H2 Tool cheat sheet
    - H2 Constraints & gotchas
- Recommended destination(s): root `CLAUDE.md` (updated in place per master spec Phase 8 / the
  target-tree note "CLAUDE.md (updated in place)"). It is NOT moved into `docs/`.
- Split decision: keep-intact (updated in place by a later phase, not split, not relocated).
- Internal relative Markdown links: none (references bible filenames in prose and a table, but
  not as Markdown link syntax).
- Active-or-archive: active. Stays at repository root.
- Conflicts/ambiguities: CLAUDE.md uses em dashes in its own headings ("The Unnecessary —
  Project Instructions", "mem0 — Operating Protocol", "The graph is ON — with canon
  subordinate"). The master spec forbids em dashes only in NEW prose written during the
  migration; this is pre-existing content, recorded not resolved. CLAUDE.md describes a
  migration toward a `canon/ planning/ chapter-blueprints/ ...` tree that differs from the
  master spec `docs/` target tree; the master spec wins; a later phase updates CLAUDE.md.
  Recorded for orchestrator/Task F awareness.

## Memory Conventions.md

- Title (as stated): "Memory Conventions (mem0)"
- Current path: `Memory Conventions.md`
- Document type: governance / operations spec (memory practice spec for mem0)
- Apparent version: not stated.
- Canon status: not canon; it is the memory-practice spec (defer to it on memory practice per
  CLAUDE.md authority table). Operational, not story canon.
- Subject: what mem0 memory is and is not, scope, the infer=false golden rule, when to write /
  not write a memory, how to phrase a good memory, recall-first discipline, maintenance,
  operational notes.
- Full heading outline (H1 / H2):
  - H1 Memory Conventions (mem0)
    - H2 What memory is — and isn't
    - H2 Scope (already configured)
    - H2 The golden rule of writing: `infer=false`
    - H2 When to WRITE a memory
    - H2 When NOT to write
    - H2 How to write a good memory
    - H2 How to RECALL (do this first)
    - H2 Maintenance
    - H2 Operational note
- Recommended destination(s): orchestrator decision. No explicit slot in the master spec
  target tree. Best-guess: keep as an operations doc near governance, for example root or a
  governance/operations location alongside the memory protocol. It is operations tooling, not
  story canon, so it does not belong in `docs/20-canon/`. Flag for orchestrator: the master
  spec does not name this file, so its destination is genuinely undetermined here.
- Split decision: keep-intact (short, single-purpose, 111 lines).
- Internal relative Markdown links: none.
- Active-or-archive: active. Memory practice remains in use.
- Conflicts/ambiguities: NOT named anywhere in the master spec target tree; destination is
  undetermined and must be decided by the orchestrator (recorded, not invented). Uses an em
  dash in its title and a heading ("What memory is — and isn't"); pre-existing content, the
  em-dash prohibition applies only to newly written migration prose. Recorded, not resolved.

---

## Memory candidates

- fact: The repository for "The Unnecessary" contains exactly 266 Markdown files; recursive
  find and git ls-files reconcile with zero differences and a clean working tree. Of these,
  254 are BMAD skill tooling under `.claude/skills/`, leaving 12 novel-content/governance
  documents. (metadata: {type: fact, tags: [migration, audit, inventory, phase-01]})
- fact: The novel-content set is the 9 root monoliths (Narrative Brief, Story Bible, Character
  Bible, Technology Rules, Master Timeline, Plot Outline and Chapter Map, Style Guide, Creative
  Decision Log, Development and Canon Guide) plus chapter-blueprints/Chapter Blueprint Template,
  plus two discovered governance docs CLAUDE.md and Memory Conventions.md. (metadata: {type:
  fact, tags: [migration, audit, inventory]})
- fact: As of Phase 01, no manuscript chapters, no continuity documents, and no research files
  exist; chapter-blueprints/ holds only the template (no instantiated chapter blueprint).
  (metadata: {type: continuity, tags: [migration, audit, manuscript, continuity, research]})
- fact: Eight monoliths carry an explicit "Version 1.0" subtitle (Story Bible, Character Bible,
  Technology Rules, Master Timeline, Plot Outline and Chapter Map, Style Guide, Creative
  Decision Log, Development and Canon Guide). Narrative Brief and Chapter Blueprint Template
  state no version; CLAUDE.md and Memory Conventions.md state no version. (metadata: {type:
  fact, tags: [migration, audit, versioning]})
- fact: The Character Bible defines 13 character profiles matching the master spec target
  slugs: Eli Rook, Jonah Mercer, Adrian Kade, Lena Okafor, June Park, Mara Voss, Talia Reed,
  Nolan Avery, Sera Vale, Celeste Mercer, Nora Bell, Morrow, Crown. The Story Bible names a
  narrower cast (only Eli, Jonah, Kade, Lena, June, Mara as profiles). (metadata: {type:
  continuity, characters: [Eli, Jonah, Kade, Lena, June, Mara, Talia, Nolan, Sera, Celeste,
  Nora, Morrow, Crown], tags: [migration, audit, characters]})
- fact: The Creative Decision Log contains 44 numbered decisions (001-044) grouped into
  Foundational, Setting/Social, Mars, AI, Character, Plot/Structure, Style/Tone, and Workflow
  categories. (metadata: {type: fact, tags: [migration, audit, decision-log]})
- continuity: Mermaid diagrams exist only in Master Timeline (4), Plot Outline and Chapter Map
  (1), Development and Canon Guide (1), and Chapter Blueprint Template (1); all must be
  preserved through splitting per master spec objective 7. (metadata: {type: continuity, tags:
  [migration, audit, mermaid]})
- hazard: No novel-content document contains any relative Markdown link; cross-document
  references are by prose filename only. So link rewriting in later phases is creating links,
  not fixing existing ones. (metadata: {type: hazard, tags: [migration, audit, links]})
- ambiguity: Memory Conventions.md has no destination in the master spec Phase 2 target tree;
  the orchestrator must decide where it lands (it is operations tooling, not story canon).
  (metadata: {type: deviation, tags: [migration, audit, destination, memory-conventions]})
- ambiguity: Era boundary labels differ between Story Bible ("2038 to 2041: The Replacement
  Wave") and Master Timeline ("2039 to 2041 Mosaic and the Replacement Wave"); both preserved
  verbatim, flagged for Task F, not resolved in Phase 01. (metadata: {type: deviation,
  tags: [migration, audit, timeline, conflict-candidate]})
