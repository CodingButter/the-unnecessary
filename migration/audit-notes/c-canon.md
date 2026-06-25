# Audit note: Task C (Canon documents: world, character, technology, timeline)

Scope: read-only audit of the four canon monoliths under `/home/codingbutter/Novel/`.
Authority: `migration/REPOSITORY-REORGANIZATION-SPEC.md` (master spec) wins all conflicts; runbook `migration/plan/01-repository-audit.md` operationalizes it.

Method note: heading outlines below were extracted with an awk pass that skips fenced code blocks, so Mermaid-internal `###` date lines and other code content are not miscounted as headings. Internal Markdown link scan (`](...)`) returned zero hits in all four files; therefore "Internal relative Markdown links" is "none" for every document. mem0 search returned HTTP 503 (Gemini high demand) at audit time and could not be consulted; bibles outrank memory regardless, so this does not affect findings.

---

## Story Bible.md

- Title (as stated): "The Unnecessary" (H1); document self-labels under "Complete Story Bible, Version 1.0".
- Current path: `/home/codingbutter/Novel/Story Bible.md`
- Document type: canon monolith (world and broad-plot bible).
- Apparent version: 1.0 (stated: "Complete Story Bible, Version 1.0").
- Canon status: active canon. Per project `CLAUDE.md`, the Story Bible is an authoritative canon document by subject (world and broad plot). The bible's own text says "The Story Bible controls the world and broad plot canon." Not explicitly labeled "active-canon" with that string, but unambiguously active canon.
- Subject: world premise, themes, social strata, infrastructure decline, protected enclaves, Mars/Aurelia, primary setting and locations (Greater Detroit, Eli's neighborhood, Lakeward, Northglass, neighborhood network, Mars), historical timeline summary, broad Book One act structure and per-character arcs, series direction, consistency rules. Contains condensed character and technology overviews that duplicate the dedicated bibles.

### Full heading outline (Story Bible)
- H1: The Unnecessary
  - H2: Complete Story Bible, Version 1.0
  - H2: Working Title
  - H2: Format
  - H2: Genre
  - H2: Tone
  - H2: Core Premise
  - H2: Central Questions
  - H2: The Thematic Argument
  - H2: Time Period
  - H2: The Shape of Society
    - H3: The Gatekeepers
    - H3: The Protected Wealthy
    - H3: Everyone Else
  - H2: The Erosion of Ordinary Life
  - H2: Protected Enclaves
  - H2: Mars
    - H3: The Mars Development Network
    - H3: Admission to Mars
    - H3: The Waiting Wealthy
  - H2: Historical Timeline
    - H3: 2026 to 2030: The Assistance Era
    - H3: 2031 to 2034: The Compression Era
    - H3: 2035: General Autonomy
    - H3: 2036 to 2038: The Intelligence Acceleration
    - H3: 2038 to 2041: The Replacement Wave
    - H3: 2041: The Labor Break
    - H3: 2042: The Infrastructure Bargains
    - H3: 2043: The Aurelia Initiative
    - H3: 2044 to 2047: Market Withdrawal
    - H3: 2047: The Support Collapse
    - H3: 2048 to 2052: The Preservation Years
    - H3: 2053: The Novel Begins
  - H2: Technology Rules
  - H2: Existing Artificial Intelligence
  - H2: Crown
  - H2: Primary Setting
  - H2: Main Locations
    - H3: Eli's Neighborhood
    - H3: Lakeward
    - H3: Northglass
    - H3: The Neighborhood Network
    - H3: Mars
  - H2: Protagonist
    - H3: Name
    - H3: Age
    - H3: Former Career
    - H3: His Complicity
    - H3: Present Life
    - H3: Personality
    - H3: What He Wants
    - H3: What He Needs
    - H3: Greatest Fear
    - H3: Moral Boundary
  - H2: Childhood Friend
    - H3: Name
    - H3: Age
    - H3: Background
    - H3: Present Life
    - H3: His Family's Mars Problem
    - H3: Personality
    - H3: What He Wants
    - H3: His Betrayal
    - H3: Moral Conflict
  - H2: Technology Leader
    - H3: Name
    - H3: Age
    - H3: Position
    - H3: Relationship With Eli
    - H3: Philosophy
    - H3: His Social View of Mars
    - H3: What He Wants
    - H3: Why He Is Dangerous
  - H2: Supporting Characters
    - H3: Dr. Lena Okafor
    - H3: June Park
    - H3: Mara Voss
  - H2: Morrow
    - H3: Name
    - H3: Original Purpose
    - H3: Architecture
    - H3: Foundational Principles
    - H3: The Moral Problem
    - H3: Personality
    - H3: The Core Mystery
    - H3: Why Asterion Wants It
  - H2: Narrative Structure
  - H2: Book One
  - H2: Act One: Service Terminated
  - H2: Act Two: A Version of Normal
  - H2: Act Three: The Invitation
  - H2: Act Four: Containment
  - H2: Eli's Book One Arc
  - H2: Jonah's Book One Arc
  - H2: Kade's Book One Arc
  - H2: Mara's Book One Arc
  - H2: Series Direction
    - H3: Book One: The Unnecessary
    - H3: Book Two
    - H3: Book Three
  - H2: Rules for Consistency
  - H2: Research Ledger
  - H2: Final Promise of the Story

Counts: 1 H1, 38 H2, 64 H3. 0 Mermaid blocks.

### Recommended destination(s) (Story Bible) - recommended, orchestrator decides
Split into `docs/20-canon/world/` per master spec Phase 4. Proposed heading-to-file mapping:
- `world/core-premise.md` <= H2 Core Premise; H2 The Thematic Argument; H2 Time Period; H2 Format; H2 Genre; H2 Tone; H2 Working Title (the "narrative promise" framing). Note: H2 Final Promise of the Story also belongs to core-premise/narrative-promise.
- `world/central-questions-and-themes.md` (target tree lists both `central-questions-and-themes.md` and `themes-and-questions.md`; orchestrator to pick one canonical name) <= H2 Central Questions; H2 The Thematic Argument may instead live here (orchestrator decides whether thematic argument sits with premise or themes); H2 Final Promise of the Story may alternatively map here.
- `world/social-structure.md` <= H2 The Shape of Society + H3 The Gatekeepers, H3 The Protected Wealthy, H3 Everyone Else.
- `world/infrastructure-decline.md` <= H2 The Erosion of Ordinary Life.
- `world/protected-enclaves.md` <= H2 Protected Enclaves.
- `world/mars-and-aurelia.md` <= H2 Mars + H3 The Mars Development Network, H3 Admission to Mars, H3 The Waiting Wealthy.
- `world/locations/index.md` plus per-location files <= H2 Primary Setting (Greater Detroit) -> `world/locations/greater-detroit.md`; H2 Main Locations children: H3 Eli's Neighborhood -> `elis-neighborhood.md`; H3 Lakeward -> `lakeward.md`; H3 Northglass -> `northglass.md`; H3 The Neighborhood Network -> include in `greater-detroit.md` or its own (spec target tree has no `neighborhood-network.md`; orchestrator decides, recommend folding into greater-detroit or elis-neighborhood); H3 Mars (locations) -> `world/locations/mars-sites.md`.
- `world/book-1-arc.md` <= H2 Book One; H2 Act One/Two/Three/Four; H2 Eli's/Jonah's/Kade's/Mara's Book One Arc; H2 Narrative Structure (broad-arc level only; do not duplicate Plot Outline detail).
- `world/series-direction.md` <= H2 Series Direction + H3 Book One/Two/Three.
- `world/consistency-rules.md` <= H2 Rules for Consistency.
- `world/government-and-corporations.md` (target tree has this file) <= currently no dedicated Story Bible H2; government/corporation material is distributed across Shape of Society, Historical Timeline, and Tech Rules. Orchestrator: may be sourced cross-document; flag as likely sparse from Story Bible alone.
- `70-research/` (deferred) <= H2 Research Ledger is a research-topic list, not world canon; recommend it route to research, not world. Orchestrator decides; do NOT lose it.
- Link-not-duplicate (master spec Phase 12): H2 Technology Rules, H2 Existing Artificial Intelligence, H2 Crown -> these are condensed tech summaries; canonical authority is `docs/20-canon/technology/*`. H2 Protagonist, H2 Childhood Friend, H2 Technology Leader, H2 Supporting Characters, H2 Morrow -> condensed character profiles; canonical authority is `docs/20-canon/characters/profiles/*`. The Historical Timeline H2 -> canonical authority is `docs/20-canon/timeline/*`. World files should summarize and link, not re-state these.

### Split decision (Story Bible): split
Boundaries above. Every H2/H3 mapped to a destination or explicitly flagged as link-only (defer to character/tech/timeline authorities). No heading left unmapped.

### Internal relative Markdown links (Story Bible): none found.

### Active-or-archive (Story Bible): active, archive-after-split.
Reason: authoritative active world/broad-plot canon now; per master spec Phase 11 the monolith is archived to `archive/source-monoliths/` only AFTER all sections have confirmed split destinations and are verified (Phase 09, not Phase 01).

### Conflicts/ambiguities observed (Story Bible) - record only, do not resolve
- Internal duplication (cross-document): Story Bible embeds condensed Crown overview, condensed character profiles (Eli, Jonah, Kade, Lena, June, Mara, Morrow), condensed Technology Rules, and a Historical Timeline that all overlap with the dedicated Character Bible, Technology Rules, and Master Timeline. This is intra-corpus duplication the split must resolve via links (master spec Phase 12), not a factual contradiction.
- Story Bible Act Three states Kade offers "guaranteed passage to Mars for Eli and a limited number of companions" (number unspecified). Master Timeline Oct 21 specifies "Mars passage for Eli and five people of his choosing"; Character Bible (Kade Book One Arc / Story role) does not fix a number. Specificity gap, not a hard contradiction; the precise count "five" lives only in the timeline. Record for the cross-document sweep (Task F).
- Story Bible supporting-character set (Lena, June, Mara) is a subset of the fuller Character Bible cast (which adds Talia, Nolan, Sera, Celeste, Nora). Not a conflict; the Story Bible is intentionally a subset, but note for completeness so no character is dropped on split.

---

## Character Bible.md

- Title (as stated): "The Unnecessary" (H1); self-labels under "Character Bible, Version 1.0".
- Current path: `/home/codingbutter/Novel/Character Bible.md`
- Document type: canon monolith (character bible).
- Apparent version: 1.0 (stated: "Character Bible, Version 1.0").
- Canon status: active canon. Document states "This Character Bible controls how the people inside that world think, speak, behave, and change," and project `CLAUDE.md` lists it as authoritative character canon. The bibles win every conflict against memory.
- Subject: identities, histories, motivations, relationships, voices, secrets, and arcs of major and recurring characters; shared cast-level content (core principles, relationship map, viewpoint guidance, dialogue differentiation, continuity fields, final standard).

### Full heading outline (Character Bible)
Note: in this document each named character is an H1; their canonical fields are H2. There are no H3 headings. Section structure below; H1 marked, H2 nested.
- H1: The Unnecessary
  - H2: Character Bible, Version 1.0
  - H2: Purpose of This Document
- H1: Core Character Principles
- H1: Primary Cast
- H1: Elias "Eli" Rook
  - H2: Basic Information / Physical Appearance / Early Life / Education / Career at Asterion / Complicity / Departure From Asterion / Personal Life / Present Life / Public Personality / Private Personality / Sense of Humor / External Goal / Internal Need / Greatest Fear / Core Contradiction / Moral Boundary / What Could Make Him Cross It / Secret / False Belief / Truth He Must Learn / Book One Arc / Long-Term Arc / Speech Pattern / Writing Rules
- H1: Jonah Mercer
  - H2: Basic Information / Physical Appearance / Early Life / Family / Marriage / Career / Public Personality / Private Personality / Sense of Humor / External Goal / Internal Need / Greatest Fear / Core Contradiction / Moral Boundary / What Could Make Him Cross It / Secret / False Belief / Truth He Must Learn / Book One Arc / Long-Term Arc / Speech Pattern / Writing Rules
- H1: Adrian Kade
  - H2: Basic Information / Physical Appearance / Background / Relationship With Eli / Family and Personal Life / Philosophy / View of Human Value / View of Mars / Public Personality / Private Personality / Sense of Humor / External Goal / Internal Need / Greatest Fear / Core Contradiction / Moral Boundary / What Could Make Him Cross It / Secret / False Belief / Truth He Refuses / Book One Arc / Long-Term Arc / Speech Pattern / Writing Rules
- H1: Dr. Lena Okafor
  - H2: Basic Information / Physical Appearance / Background / Collapse of Her Hospital / Family / Personality / Relationship With Eli / External Goal / Internal Need / Greatest Fear / Core Contradiction / Moral Boundary / What Could Make Her Cross It / Secret / False Belief / Truth She Must Learn / Book One Arc / Speech Pattern / Writing Rules
- H1: June Park
  - H2: Basic Information / Physical Appearance / Early Life / Education / Personality / Relationship With Eli / Relationship With Morrow / External Goal / Internal Need / Greatest Fear / Core Contradiction / Moral Boundary / What Could Make Her Cross It / Secret / False Belief / Truth She Must Learn / Book One Arc / Speech Pattern / Writing Rules
- H1: Mara Voss
  - H2: Basic Information / Physical Appearance / Political History / Relationship With Asterion / Family / Personality / External Goal / Internal Need / Greatest Fear / Core Contradiction / Moral Boundary / What Could Make Her Cross It / Secret / False Belief / Truth She Must Learn / Book One Arc / Long-Term Arc / Speech Pattern / Writing Rules
- H1: Talia Reed
  - H2: Basic Information / Physical Appearance / Background / Personality / Relationship With Eli / External Goal / Internal Need / Greatest Fear / Core Contradiction / Moral Boundary / What Could Make Her Cross It / Secret / False Belief / Truth She Must Learn / Book One Arc / Speech Pattern
- H1: Nolan Avery
  - H2: Basic Information / Physical Appearance / Background / Personality / Relationship With Eli / External Goal / Internal Need / Greatest Fear / Moral Boundary / Secret / Story Function
- H1: Sera Vale
  - H2: Basic Information / Physical Appearance / Background / Personality / External Goal / Internal Need / Greatest Fear / Core Contradiction / Moral Boundary / What Could Make Her Cross It / Secret / Speech Pattern
- H1: Celeste Mercer
  - H2: Basic Information / Personality / Relationship With Jonah / External Goal / Secret / Book One Function
- H1: Nora Bell
  - H2: Basic Information / Background / Relationship With Eli / Current Position / External Goal / Internal Need / Secret / Story Function
- H1: Nonhuman Characters
- H1: Morrow
  - H2: Classification / Story Role / Origin / Initial Capabilities / Public Personality / Relationship With Eli / Relationship With June / Relationship With Lena / Relationship With Talia / Core Goal / Greatest Threat / Core Contradiction / Secret / Book One Arc / Long-Term Arc / Speech Rules
- H1: Crown
  - H2: Classification / Story Role / Origin / Personality / Relationship With Kade / Relationship With Morrow / Core Goal / Core Contradiction / Secret / Speech Rules
- H1: Relationship Map
  - H2: Eli and Jonah / Eli and Kade / Eli and Lena / Eli and June / Eli and Talia / Jonah and Celeste / Jonah and Kade / Kade and Crown / Kade and Mara / Morrow and Crown
- H1: Viewpoint Guidance
  - H2: Primary Viewpoint / Secondary Viewpoints / Viewpoint Rule
- H1: Dialogue Differentiation
  - H2: Eli / Jonah / Kade / Lena / June / Mara / Talia / Nolan / Sera / Morrow / Crown
- H1: Character Continuity Fields
- H1: Final Character Standard

Counts: 22 H1, 233 H2, 0 H3. 0 Mermaid blocks. (The 22 H1 count includes the title H1, the two front-matter section H1s "Core Character Principles" and "Primary Cast", the "Nonhuman Characters" divider H1, and the four shared-content H1s "Relationship Map", "Viewpoint Guidance", "Dialogue Differentiation", "Character Continuity Fields", "Final Character Standard" alongside the 13 character H1s.)

### Every character profile detected (with exact heading and proposed slug)
13 character profiles (master spec target tree expects one file per major/recurring character under `docs/20-canon/characters/profiles/`):
1. "Elias \"Eli\" Rook" -> `profiles/eli-rook.md`
2. "Jonah Mercer" -> `profiles/jonah-mercer.md`
3. "Adrian Kade" -> `profiles/adrian-kade.md`
4. "Dr. Lena Okafor" -> `profiles/lena-okafor.md`
5. "June Park" -> `profiles/june-park.md`
6. "Mara Voss" -> `profiles/mara-voss.md`
7. "Talia Reed" -> `profiles/talia-reed.md`
8. "Nolan Avery" -> `profiles/nolan-avery.md`
9. "Sera Vale" -> `profiles/sera-vale.md`
10. "Celeste Mercer" -> `profiles/celeste-mercer.md`
11. "Nora Bell" -> `profiles/nora-bell.md`
12. "Morrow" (under "Nonhuman Characters") -> `profiles/morrow.md`
13. "Crown" (under "Nonhuman Characters") -> `profiles/crown.md`

Note: master spec Phase 2 sample tree lists exactly these 13 profile slugs (eli-rook, jonah-mercer, adrian-kade, lena-okafor, june-park, mara-voss, talia-reed, nolan-avery, sera-vale, celeste-mercer, nora-bell, morrow, crown). The Character Bible's cast matches the spec one-to-one. Off-page characters named only inside profiles (e.g., Alexandra Kade, Evan Voss, Malcolm Mercer, Celeste's/Jonah's children Julian and Amelia, June's parents Daniel and Soo-jin Park, Lena's mother Amara) do NOT have their own profiles and should remain inline in the relevant profile, not be split out.

### Canonical fields present per profile (master spec Phase 4 field list)
Reference field set: basic info, appearance, history, personality, external goal, internal need, fear, contradiction, moral boundary, secret, false belief, truth/growth, Book One arc, long-term arc, speech pattern, writing rules, relationships.
- Eli: ALL present (history split across Early Life/Education/Career/Complicity/Departure/Personal Life/Present Life; personality split Public/Private/Sense of Humor; relationships via Relationship With + global Relationship Map). Has Long-Term Arc, Writing Rules.
- Jonah: ALL present (history via Early Life/Family/Marriage/Career). Has Long-Term Arc, Writing Rules.
- Kade: ALL present, plus extra fields View of Human Value, View of Mars, Philosophy; "truth" phrased as "Truth He Refuses". Has Long-Term Arc, Writing Rules.
- Lena: present except no Long-Term Arc heading; has Book One Arc, Writing Rules, Secret, False Belief, Truth She Must Learn.
- June: present except no Long-Term Arc heading; has Book One Arc, Writing Rules.
- Mara: ALL present incl. Long-Term Arc and Writing Rules.
- Talia: present except no Long-Term Arc and NO Writing Rules heading; has Secret, False Belief, Truth She Must Learn, Book One Arc, Speech Pattern.
- Nolan: REDUCED profile - has Basic Info, Appearance, Background, Personality, Relationship With Eli, External Goal, Internal Need, Greatest Fear, Moral Boundary, Secret, Story Function. Missing: Core Contradiction, What Could Make Him Cross It, False Belief, Truth, Book One Arc (per se), Long-Term Arc, Speech Pattern, Writing Rules. ("Primary viewpoint: No.")
- Sera: has Basic Info, Appearance, Background, Personality, External Goal, Internal Need, Greatest Fear, Core Contradiction, Moral Boundary, What Could Make Her Cross It, Secret, Speech Pattern. Missing: False Belief, Truth, Book One Arc, Long-Term Arc, Writing Rules. ("No in Book One.")
- Celeste: REDUCED - Basic Info, Personality, Relationship With Jonah, External Goal, Secret, Book One Function. Missing appearance, most psych fields.
- Nora: REDUCED - Basic Info, Background, Relationship With Eli, Current Position, External Goal, Internal Need, Secret, Story Function. Missing appearance, most psych fields.
- Morrow (nonhuman): Classification, Story Role, Origin, Initial Capabilities, Public Personality, Relationships (Eli/June/Lena/Talia), Core Goal, Greatest Threat, Core Contradiction, Secret, Book One Arc, Long-Term Arc, Speech Rules. Uses AI-flavored field names rather than human ones.
- Crown (nonhuman): Classification, Story Role, Origin, Personality, Relationships (Kade/Morrow), Core Goal, Core Contradiction, Secret, Speech Rules. No Book One Arc / Long-Term Arc headings.
Record: reduced profiles are intentional (minor or later-book characters); the split must preserve exactly the fields present and must NOT fabricate missing fields (master spec / runbook prohibit inventing content).

### Shared (non-profile) content -> own files
- "Relationship Map" (H1 + 10 H2 pairings) -> `docs/20-canon/characters/relationship-map.md`.
- "Dialogue Differentiation" (H1 + 11 per-character H2) -> `docs/20-canon/characters/dialogue-differentiation.md`.
- "Viewpoint Guidance" (H1: Primary Viewpoint / Secondary Viewpoints / Viewpoint Rule) -> `docs/20-canon/characters/viewpoint-rules.md`.
- "Core Character Principles" (H1) and "Final Character Standard" (H1) -> recommend `docs/20-canon/characters/index.md` framing content, or a `characters/principles.md` (target tree has no explicit principles file; orchestrator decides). Do not lose.
- "Character Continuity Fields" (H1) -> this is the per-character continuity-ledger field list; recommend it inform `docs/60-continuity/` (Phase 07) rather than a static profile. Orchestrator decides; do not lose.
- "Purpose of This Document" (H2 under title) -> fold into `characters/index.md`.
- "Nonhuman Characters" (H1 divider) -> structural divider; its children (Morrow, Crown) become profiles; the divider itself becomes index grouping, not a file.

### Recommended destination(s) (Character Bible): `docs/20-canon/characters/` (profiles + shared files + index) as mapped above. recommended; orchestrator decides.

### Split decision (Character Bible): split
One file per character (13), plus relationship-map.md, dialogue-differentiation.md, viewpoint-rules.md, and index/principles handling. Boundaries are the per-character H1 ranges and the four shared H1 ranges. No heading unmapped.

### Internal relative Markdown links (Character Bible): none found.

### Active-or-archive (Character Bible): active, archive-after-split. (Same Phase 11 rationale as Story Bible.)

### Conflicts/ambiguities observed (Character Bible) - record only
- Cross-document duplication: condensed versions of these same profiles appear in the Story Bible; Morrow/Crown behavioral identity here overlaps with capability rules in Technology Rules. Resolve by linking on split (Phase 12), not by merging.
- Crown operational duration: Character Bible (Crown Origin) says Crown "has operated for nearly two decades when Book One begins"; Technology Rules says "approximately eighteen years"; Master Timeline fixes Crown's general autonomy at March 2035 (18 years before 2053) and continuity rule 1 says "Crown has existed since 2035." All three reconcile to ~18 years; "nearly two decades" is a looser restatement. Minor wording ambiguity, not a hard date conflict. Flagged for Task F.
- Field-completeness asymmetry: several profiles (Nolan, Celeste, Nora, Sera, Talia, Crown) lack one or more of the master spec's canonical fields. This is a source-completeness observation, not a conflict; do not invent the missing fields during split.

---

## Technology Rules.md

- Title (as stated): "The Unnecessary" (H1); self-labels under "World and Technology Rules, Version 1.0".
- Current path: `/home/codingbutter/Novel/Technology Rules.md`
- Document type: canon monolith (world-and-technology rules bible).
- Apparent version: 1.0 (stated: "World and Technology Rules, Version 1.0").
- Canon status: active canon. Document states its purpose is "to prevent technology from changing whenever the plot requires a convenient solution"; project `CLAUDE.md` lists `Technology Rules.md` as authoritative technology canon. Note: the project authority table calls this file "Technology Rules.md" while the doc's internal title is "World and Technology Rules" - a filename/title mismatch, recorded below.
- Subject: technological capabilities, physical limits, AI levels, Crown, Morrow, Crown-vs-Morrow, computing, energy, communications, cloud dependency, identity/money, robotics, transportation, medicine, manufacturing, security, conflict, government tech, protected enclaves, community infrastructure, Northglass, Mars/Aurelia, scientific progress, information/propaganda, hard plot restrictions, failure rules, scene guidance, continuity questions, canon summary.

### Full heading outline (Technology Rules)
- H1: The Unnecessary
  - H2: World and Technology Rules, Version 1.0
  - H2: Purpose of This Document
- H1: Foundational Rule
  - H2: Intelligence Does Not Eliminate Physics
- H1: The Technological State of the World
  - H2: General Machine Reasoning / Artificial Superintelligence / Mature Physical Autonomy
- H1: Levels of Artificial Intelligence
  - H2: Embedded Systems / Specialized Agents / General Autonomous Systems / Artificial Superintelligence
- H1: Consciousness and Personhood
- H1: Crown
  - H2: Overview / Crown's Capabilities / Crown's Limitations / Crown's Governance / Crown's Communication
- H1: Morrow
  - H2: Overview / Morrow's Core Advantage / Distributed Architecture / Morrow's Early Capabilities / Morrow's Growth / Morrow's Moral Architecture / Morrow's Access Rules / Morrow's Survival
- H1: Crown and Morrow
  - H2: Fundamental Difference / Relative Strength / Interaction
- H1: Computing Hardware
  - H2: Advanced Processors / Hardware Longevity / Data Centers / Cooling
- H1: Energy
  - H2: Energy Is the Primary Constraint / Regional Grids / Microgrids / Load Shedding / Protected Enclaves
- H1: Communications
  - H2: The Public Internet / Local Networks / Cellular Networks / Satellites / Communication Delays With Mars
- H1: Cloud Dependency and Digital Ownership
  - H2: The Unsupported World / Corporate Locks / Eli's Work
- H1: Identity, Money, and Access
  - H2: Digital Identity / Money / Access Is More Important Than Wealth
- H1: Robotics
  - H2: General Rule / Construction Robots / Maintenance Robots / Domestic Robots / Manufacturing Robots / Self-Repair / Robotic Reproduction
- H1: Transportation
  - H2: Autonomous Vehicles / Freight / Air Travel / Spaceflight
- H1: Medicine
  - H2: Advanced Medicine / Unsupported Medicine / Medical AI / Allocation Systems
- H1: Manufacturing and Materials
  - H2: Automated Production / Ordinary Communities / Additive Manufacturing
- H1: Security and Surveillance
  - H2: Protected Surveillance / Public Surveillance / Autonomous Security Machines / Morrow and Surveillance
- H1: Weapons and Conflict
  - H2: General Rule / Civilian Weapons / Corporate Force / Cyber Conflict
- H1: Government Technology
  - H2: Government Condition / Automated Administration / Enforcement
- H1: Protected Enclaves
  - H2: Infrastructure / Vulnerability / Technology Gap
- H1: Community Infrastructure
  - H2: Human Knowledge / Apprenticeship / Coordination Problem
- H1: Northglass
  - H2: Facility History / Why It Was Abandoned / Remaining Technology / Morrow's Origin at Northglass
- H1: Mars and the Aurelia Initiative
  - H2: General State / Why Machines Arrive First / Martian Systems / Settlement Design / Resource Independence / Human Capacity / Mars Communication / Mars Failure Risks
- H1: Scientific Progress
  - H2: Superintelligence Acceleration / Limits on Deployment
- H1: Information and Propaganda
  - H2: Corporate Messaging / Synthetic Media / Reliable Evidence
- H1: Hard Plot Restrictions
  - H2: Morrow Cannot Instantly Access Everything / Crown Cannot Instantly Locate Morrow / Morrow Cannot Create Advanced Hardware / Mars Cannot Become Fully Independent Overnight / Robots Cannot Repair Everything / AI Cannot Predict People Perfectly / AI Cannot Solve Moral Conflict Mathematically / Technology Cannot Remove Politics / Decentralization Does Not Guarantee Freedom / Centralization Does Not Guarantee Evil
- H1: Failure Rules
  - H2: Software Failure / Hardware Failure / Human Failure / Institutional Failure / AI Failure
- H1: Technology in Scenes
- H1: Continuity Questions for Every Technical Scene
- H1: Canon Summary

Counts: 31 H1, 113 H2, 0 H3. 0 Mermaid blocks.

### Recommended destination(s) (Technology Rules) - recommended; orchestrator decides
Split by system into `docs/20-canon/technology/` per master spec Phase 4 / Phase 2 target tree:
- `technology/foundational-rules.md` <= H1 Foundational Rule (Intelligence Does Not Eliminate Physics); H1 The Technological State of the World.
- `technology/ai/index.md` + `intelligence-levels.md` <= H1 Levels of Artificial Intelligence (Embedded/Specialized/General Autonomous/Superintelligence).
- `technology/ai/consciousness-and-personhood.md` <= H1 Consciousness and Personhood.
- `technology/ai/crown.md` <= H1 Crown (Overview/Capabilities/Limitations/Governance/Communication).
- `technology/ai/morrow.md` <= H1 Morrow (Overview/Core Advantage/Distributed Architecture/Early Capabilities/Growth/Moral Architecture/Access Rules/Survival).
- `technology/ai/crown-vs-morrow.md` <= H1 Crown and Morrow (Fundamental Difference/Relative Strength/Interaction).
- computing: target tree has no standalone `computing.md`; recommend `technology/infrastructure/` or a `computing.md` under technology root for H1 Computing Hardware (Advanced Processors/Hardware Longevity/Data Centers/Cooling). Orchestrator decides exact filename; spec Phase 4 split list names "computing".
- `technology/infrastructure/energy.md` <= H1 Energy.
- `technology/infrastructure/communications.md` <= H1 Communications.
- `technology/infrastructure/cloud-dependency.md` <= H1 Cloud Dependency and Digital Ownership.
- `technology/infrastructure/identity-and-money.md` <= H1 Identity, Money, and Access.
- `technology/infrastructure/community-infrastructure.md` <= H1 Community Infrastructure.
- `technology/robotics-and-manufacturing.md` <= H1 Robotics + H1 Manufacturing and Materials.
- `technology/transportation.md` <= H1 Transportation.
- `technology/medicine.md` <= H1 Medicine.
- `technology/security-and-conflict.md` <= H1 Security and Surveillance + H1 Weapons and Conflict.
- government tech: spec Phase 4 lists "government technology"; target tree world has `government-and-corporations.md`. H1 Government Technology -> recommend `technology/government-technology.md` OR fold into world/government-and-corporations.md. Orchestrator decides; do not lose.
- protected enclaves (tech): H1 Protected Enclaves (Infrastructure/Vulnerability/Technology Gap) -> tech-side enclave rules; recommend folding enclave infra into `technology/infrastructure/` or a `technology/protected-enclaves.md`. World-side enclave canon lives separately in `world/protected-enclaves.md`. Flag the world/tech overlap.
- `technology/ai/morrow.md` or `technology/northglass.md`: H1 Northglass (Facility History/Why Abandoned/Remaining Technology/Morrow's Origin at Northglass) - spec lists "Northglass" as a tech split; target tree has no `technology/northglass.md` but does have `world/locations/northglass.md`. Recommend tech-relevant Northglass content (remaining technology, Morrow origin) cross-link with the world location file. Orchestrator decides home; do not duplicate.
- `technology/mars-technology.md` <= H1 Mars and the Aurelia Initiative (technology aspects). Cross-link with `world/mars-and-aurelia.md`.
- scientific progress: H1 Scientific Progress -> recommend `technology/foundational-rules.md` appendix or its own `technology/scientific-progress.md`. Orchestrator decides.
- information/propaganda: H1 Information and Propaganda -> not in spec tech split list; recommend `technology/` (e.g., `information-and-media.md`) or world/government-and-corporations. Orchestrator decides; do not lose.
- `technology/hard-plot-restrictions.md` <= H1 Hard Plot Restrictions (all 10 H2). PRESERVE VERBATIM (see flagged rules below).
- `technology/failure-rules.md` <= H1 Failure Rules (5 H2). PRESERVE VERBATIM.
- scene/continuity guidance: H1 Technology in Scenes; H1 Continuity Questions for Every Technical Scene -> these are drafting-discipline aids, not capability canon; recommend they route to `docs/10-vision/style/technology-in-prose.md` or `60-continuity/`. Orchestrator decides; do not lose.
- `technology/index.md` <= H1 Canon Summary (as index framing) + H2 Purpose of This Document.

### FLAGGED rules that limit plot convenience (preserve verbatim) - master spec Phase 4 / runbook Task C requirement
Hard restrictions (H1 "Hard Plot Restrictions" - "The following solutions must not be used without a deliberate canon revision."):
- "Morrow Cannot Instantly Access Everything" - cannot take over arbitrary systems without access, vulnerabilities, or cooperation.
- "Crown Cannot Instantly Locate Morrow" - Crown can infer and investigate, not automatically know every location.
- "Morrow Cannot Create Advanced Hardware" - cannot build cutting-edge processors in a neighborhood workshop.
- "Mars Cannot Become Fully Independent Overnight" - requires years of construction, testing, supply buildup.
- "Robots Cannot Repair Everything" - severe damage/missing parts/unusual environments still require improvisation.
- "AI Cannot Predict People Perfectly" - models produce probabilities, not certainty.
- "AI Cannot Solve Moral Conflict Mathematically" - cannot produce an objectively correct answer everyone must accept.
- "Technology Cannot Remove Politics".
- "Decentralization Does Not Guarantee Freedom".
- "Centralization Does Not Guarantee Evil".
Failure-rule mandates (H1 "Failure Rules"): "Every important technology should have at least one visible failure mode." Categories: Software / Hardware / Human / Institutional / AI Failure. "No technology should fail only because someone forgot an obvious solution. Failures should emerge from plausible constraints."
Other "cannot/never/must not" constraint statements embedded outside those two sections (also limit plot convenience; preserve verbatim):
- Foundational Rule list (Intelligence Does Not Eliminate Physics): AI cannot Create matter from nothing / Ignore energy requirements / Instantly build physical infrastructure / Repair machines without parts or tools / Know information it cannot access or infer / Predict chaotic human behavior with certainty / Communicate without a physical channel / Operate destroyed hardware / Bypass every security system automatically / Control every connected device / Manufacture advanced components without specialized equipment / Prevent all accidents / Solve every moral disagreement.
- Crown's Limitations: "Crown cannot freely access every network"; requires legal authority/credentials/physical access/etc.; "It can advise against a decision and still be required to execute it."
- Crown's Governance: "Crown cannot legally rewrite its foundational ownership structure."
- Morrow's Access Rules: "Morrow cannot automatically control a system merely because it is connected to a network."
- Morrow "cannot initially" list (Early Capabilities): Control distant infrastructure / Design revolutionary technology instantly / Defeat Crown in direct computation / Operate every device it discovers / Manufacture advanced processors / Read private thoughts / Predict all human actions / Copy itself without compatible hardware and network access.
- Distributed Architecture: "Destroying one node may remove specific memories or abilities... A distributed copy is not always a perfect copy." (Morrow can be injured.)
- Cyber Conflict: "Neither Crown nor Morrow can type one command and take over the world."
- Mars Communication: one-way delay several to >20 minutes; "There is no real-time conversation between Earth and Mars."
- Crown and Morrow / Interaction: "Crown and Morrow cannot simply absorb one another."
- Crown duration: "approximately eighteen years" (a fixed quantitative anchor - cross-check with timeline).
These must survive the split unaltered; orchestrator should keep them as quoted rules, not paraphrase.

### Split decision (Technology Rules): split
By system per boundaries above. Every H1/H2 mapped or explicitly flagged for orchestrator routing (computing filename, government tech home, scientific progress, information/propaganda, scene-and-continuity aids). No heading unmapped or lost.

### Internal relative Markdown links (Technology Rules): none found.

### Active-or-archive (Technology Rules): active, archive-after-split. (Phase 11 rationale.)

### Conflicts/ambiguities observed (Technology Rules) - record only
- Filename vs internal title mismatch: file is `Technology Rules.md` (and `CLAUDE.md` authority table calls it "Technology Rules.md"), but the document's own title line is "World and Technology Rules, Version 1.0." The content covers world systems plus technology. Not a canon contradiction; a naming/scoping ambiguity to note so the split correctly routes world-vs-tech material (e.g., Protected Enclaves and Northglass appear in BOTH this file and the Story Bible/world tree). Flagged for Task F.
- World/tech overlap: H1 Protected Enclaves, H1 Northglass, H1 Mars and the Aurelia Initiative, H1 Government Technology all have world-canon counterparts in the Story Bible. The split must link, not duplicate (Phase 12); decide a single authority per fact (tech capability vs world description). Recorded, not resolved.
- Crown duration "approximately eighteen years" vs Character Bible "nearly two decades" - see Character Bible ambiguity note; reconciles to 2035 origin. Flagged for Task F.

---

## Master Timeline.md

- Title (as stated): "The Unnecessary" (H1); self-labels under "Master Timeline, Version 1.0".
- Current path: `/home/codingbutter/Novel/Master Timeline.md`
- Document type: canon monolith (chronology bible).
- Apparent version: 1.0 (stated: "Master Timeline, Version 1.0").
- Canon status: active canon. Document states "This document establishes the chronological canon" and "This Master Timeline defines when everything happens"; project `CLAUDE.md` lists it as authoritative timeline canon.
- Subject: chronological canon - AI rise, Crown/Mosaic development, labor replacement, infrastructure erosion, Mars construction, enclave formation, character histories and birth dates, month-by-month pre-Book-One run-up, day-by-day Book One events, per-character knowledge timelines, secret timeline, travel/timing rules, continuity rules, open questions.

### Full heading outline (Master Timeline)
- H1: The Unnecessary
  - H2: Master Timeline, Version 1.0
  - H2: Purpose of This Document
- H1: Timeline Authority
  - H2: Fixed Dates / Fixed Years / Approximate Periods
- H1: High-Level Historical Progression  [contains Mermaid block #1: `timeline`]
- H1: Causal Progression of the World  [contains Mermaid block #2: `flowchart TD`]
- H1: Principal Character Birth Dates  [Markdown table, 15 characters]
- H1: Before the Transformation
  - H2: 1992 to 2014  (H3 date entries: 1992, 2007, 2013, 2014, 2015, 2021, 2024)
- H1: The Assistance Era
  - H2: 2026 to 2030  (H3: 2026, 2027, 2028, 2029, 2030)
- H1: The Compression Era
  - H2: 2031 to 2034  (H3: 2031, 2032, 2033, 2034)
- H1: General Autonomy
  - H2: 2035  (H3: March 2035, June 2035, Late 2035)
- H1: The Intelligence Acceleration
  - H2: 2036 to 2038  (H3: 2036, 2037, 2038)
- H1: Mosaic and the Replacement Wave
  - H2: 2039 to 2041  (H3: February 2039, August 2039, 2040, September 2040, Late 2040, Early 2041, Summer 2041, Autumn 2041, December 2041)
- H1: Infrastructure Bargains
  - H2: 2042  (H3: February 2042, May 2042, July 2042, September 2042, November 2042)
- H1: The Aurelia Initiative
  - H2: 2043  (H3: January 2043, March 2043, June 2043, August 2043, October 2043)
- H1: Market Withdrawal
  - H2: 2044 to 2046  (H3: 2044, April 2044, September 2044, 2045, Early 2045, Late 2045, 2046, June 2046, November 2046)
- H1: The Support Collapse
  - H2: 2047  (H3: January 2047, March 2047, April 2047, May 2047, July 2047, August 2047, September 2047, October 2047, November 2047, December 2047)
- H1: The Preservation Years
  - H2: 2048  (H3: February 2048, April 2048, June 2048, August 2048, October 2048, December 2048)
  - H2: 2049  (H3: March 2049, June 2049, August 2049, November 2049)
  - H2: 2050  (H3: February 2050, May 2050, September 2050, December 2050)
  - H2: 2051  (H3: February 2051, April 2051, July 2051, October 2051)
  - H2: 2052  (H3: January 2052, March 2052, May 2052, July 2052, August 2052, November 2052, December 2052)
- H1: The Final Months Before Book One
  - H2: January to September 2053  (H3: January 2053, February 2053, March 2053, April 2053, May 2053, June 2053, July 2053, August 2053, September 2053)
- H1: Book One Calendar
  - H2: Canonical Opening Date / Canonical Final Date
- H1: Book One Overview  [contains Mermaid block #3: `gantt`]
- H1: Detailed Book One Timeline
  - H2: Friday, October 3, 2053  (H3: Morning, Midday, Afternoon, Evening, Character Knowledge)
  - H2: Saturday, October 4, 2053
  - H2: Sunday, October 5, 2053  (H3: Northglass Entry)
  - H2: Monday, October 6, 2053
  - H2: Tuesday, October 7, 2053
  - H2: Wednesday, October 8, 2053
  - (Act Two H1 divider) H1: Act Two: A Version of Normal
  - H2: Thursday, October 9, 2053 ... H2: Sunday, October 19, 2053 (daily)
  - (Act Three H1 divider) H1: Act Three: The Invitation
  - H2: Monday, October 20 ... H2: Sunday, October 26, 2053 (daily)
  - (Act Four H1 divider) H1: Act Four: Containment
  - H2: Monday, October 27 ... H2: Friday, October 31, 2053 (H3: Morning, Afternoon, Evening, Night)
  - H2: Saturday, November 1, 2053  (H3: 12:04 a.m., 12:07, 12:08, 12:09, 12:10, 12:12, 12:15, 12:17 a.m., End State)
- H1: Book One Character Knowledge Timeline
  - H2: Eli / Jonah / Lena / June / Kade / Mara / Sera  (each a per-character knowledge table)
- H1: Secret Timeline  [table of 11 secrets with who-knows and when-revealed]
- H1: Parallel Character Progression  [contains Mermaid block #4: `flowchart LR` with Eli/Jonah/Kade/Morrow subgraphs]
- H1: Timing and Travel Rules During Book One
  - H2: Greater Detroit / Communications / Technical Work
- H1: Timeline Continuity Rules  [18 numbered rules]
- H1: Open Timeline Questions
- H1: Final Chronological Standard

Counts: 30 H1, 63 H2, 113 H3 (H3s are dated sub-entries; daily Book One entries Oct 9-19 and Oct 20-26 are H2 with no H3 children). 4 Mermaid blocks.

### Mermaid block inventory (COUNT = 4; must be preserved as valid blocks)
1. Lines 69-107: `timeline` - "The Unnecessary: Historical Progression" (13 dated milestones 2026-2053). Under H1 "High-Level Historical Progression".
2. Lines 113-127: `flowchart TD` - "Causal Progression of the World" (nodes A through M). Under H1 "Causal Progression of the World".
3. Lines 982-1010: `gantt` - "Book One Timeline" (Acts One-Four with dated task bars and a Nov 1 milestone). Under H1 "Book One Overview".
4. Lines 1796-1829: `flowchart LR` - "Parallel Character Progression" (subgraphs Eli E1-E6, Jonah J1-J6, Kade K1-K6, Morrow M1-M6). Under H1 "Parallel Character Progression".
All four open with ```` ```mermaid ```` and close with ```` ``` ````; fence pairing verified (open lines 69/113/982/1796, close lines 107/127/1010/1829). Preserve verbatim on split; do not reformat.

### Date-entry / table inventory
- Birth-dates table: 15 characters with exact birth dates and Book-One ages (Adrian Kade, Nolan Avery, Mara Voss, Lena Okafor, Sera Vale, Nora Bell, Jonah Mercer, Elias Rook, Celeste Mercer, Talia Reed, Alexandra Kade, Evan Voss, Julian Mercer, June Park, Amelia Mercer).
- Historical dated entries (H3 year/month headings) span 1992 through September 2053; Book One daily entries span Oct 3 - Nov 1, 2053; Nov 1 has minute-level entries (12:04-12:17 a.m.).
- Per-character knowledge tables: 7 (Eli, Jonah, Lena, June, Kade, Mara, Sera).
- Secret Timeline table: 11 rows.
- Timeline Continuity Rules: 18 numbered canonical constraints.
- Open Timeline Questions: 15 deliberately-unresolved questions.

### Recommended destination(s) (Master Timeline) - recommended; orchestrator decides
Split per master spec Phase 4 into `docs/20-canon/timeline/`:
- `timeline/index.md` <= H1 Timeline Authority (Fixed Dates/Fixed Years/Approximate Periods); H1 High-Level Historical Progression (Mermaid #1) as the compact high-level chronology; H1 Causal Progression of the World (Mermaid #2); H1 Final Chronological Standard; H2 Purpose of This Document. Keep Mermaid #1 and #2 here as the index visualizations.
- `timeline/character-birth-dates.md` <= H1 Principal Character Birth Dates (the 15-row table).
- `timeline/historical/2026-2034-...md` <= H1 Before the Transformation (1992-2014) + H1 The Assistance Era (2026-2030) + H1 The Compression Era (2031-2034). (Spec filename `2026-2034-assistance-and-compression.md`; note pre-2026 birth/childhood entries 1992-2024 must be retained, recommend leading this file or folding into birth-dates/index. Do not lose 1992-2024.)
- `timeline/historical/2035-2041-...md` <= H1 General Autonomy (2035) + H1 The Intelligence Acceleration (2036-2038) + H1 Mosaic and the Replacement Wave (2039-2041). (Spec `2035-2041-autonomy-and-labor-break.md`.)
- `timeline/historical/2042-2047-...md` <= H1 Infrastructure Bargains (2042) + H1 The Aurelia Initiative (2043) + H1 Market Withdrawal (2044-2046) + H1 The Support Collapse (2047). (Spec `2042-2047-infrastructure-and-support-collapse.md`.)
- `timeline/historical/2048-2052-...md` <= H1 The Preservation Years (2048-2052). (Spec `2048-2052-preservation-years.md`.)
- `timeline/book-1/pre-book-2053.md` <= H1 The Final Months Before Book One (Jan-Sep 2053).
- `timeline/book-1/index.md` <= H1 Book One Calendar (opening/final dates) + H1 Book One Overview (Mermaid #3 gantt). Keep the gantt here.
- `timeline/book-1/act-1-timeline.md` <= Detailed Book One Oct 3-8 (H2 days under "Detailed Book One Timeline" before the Act Two divider).
- `timeline/book-1/act-2-timeline.md` <= H1 Act Two: A Version of Normal (Oct 9-19).
- `timeline/book-1/act-3-timeline.md` <= H1 Act Three: The Invitation (Oct 20-26).
- `timeline/book-1/act-4-timeline.md` <= H1 Act Four: Containment (Oct 27 - Nov 1, incl. minute-level Nov 1).
- `timeline/book-1/character-knowledge-timeline.md` <= H1 Book One Character Knowledge Timeline (7 tables) + H1 Parallel Character Progression (Mermaid #4). Keep Mermaid #4 here (or in index; orchestrator decides). 
- `timeline/book-1/secret-timeline.md` <= H1 Secret Timeline (11-row table).
- Travel/timing and continuity rules: H1 Timing and Travel Rules During Book One -> recommend `timeline/book-1/index.md` appendix or its own file; H1 Timeline Continuity Rules (18 rules) -> recommend `timeline/index.md` or a `timeline/continuity-rules.md`; H1 Open Timeline Questions -> recommend `timeline/index.md` or route to `60-continuity`/`70-research`. Orchestrator decides; do not lose any.
Do NOT duplicate detailed chapter summaries from plot files (master spec Phase 4 caveat); the Book One daily entries here are the timeline view, distinct from plot-map/chapter files.

### Split decision (Master Timeline): split
By historical period and Book One act per boundaries above; index retains compact chronology + Mermaid #1/#2/#3 (and #4 with knowledge timeline). Every H1/H2/H3 mapped; pre-2026 entries, travel rules, continuity rules, and open questions explicitly flagged for routing so none is lost. All 4 Mermaid blocks preserved.

### Internal relative Markdown links (Master Timeline): none found.

### Active-or-archive (Master Timeline): active, archive-after-split. (Phase 11 rationale.)

### Conflicts/ambiguities observed (Master Timeline) - record only, do not resolve
- Kade's offer companion count: Master Timeline (Oct 21) fixes "Mars passage for Eli and five people of his choosing"; Story Bible (Act Three) says only "a limited number of companions." The number five exists only here. Specificity gap, flagged for Task F (not a contradiction).
- Crown duration cross-check: Master Timeline continuity rule 1 ("Crown has existed since 2035") and March-2035 general-autonomy entry give 18 years to 2053; agrees with Technology Rules' "approximately eighteen years" and is the harder anchor than Character Bible's "nearly two decades." No date conflict; wording-precision difference only.
- Mosaic chronology: Master Timeline places first Mosaic prototype Aug 2039 and integration into Crown 2040, i.e., Mosaic post-dates Crown (continuity rule 2 confirms "Mosaic is developed after Crown"). Story Bible's narrative ("his most important contribution was Mosaic") and Technology Rules ("Mosaic-derived orchestration") are consistent with this ordering. No conflict; recorded for Task F to confirm no later doc reverses the order.
- High-Level Historical Progression Mermaid (Mermaid #1) includes milestones 2050 ("Autonomous Martian industry becomes partially self-expanding") and 2052 ("Mars passes its first long-duration habitability trial") that correspond to detailed prose entries (May 2050 self-expanding chain; 2050-2051 commissioning crew). The Mermaid says "2052: Mars passes its first long-duration habitability trial" while prose puts the 16-person commissioning crew at Sep 2050 (142 Martian days) returning Feb 2051 and Aurelia "publicly declared habitable" Feb 2051; the Jan-2052 prose entry is a six-month simulated agricultural load. The Mermaid's "2052 long-duration habitability trial" is a compressed summary label, not an exact-date claim; potential summarization mismatch between the diagram milestone year and the prose habitability declaration (2051 vs 2052). Record for Task F; do not resolve.
- "Approximate Periods" caveat (Timeline Authority) explicitly says some changes are gradual and should not be rewritten as single events; relevant when later phases map year-range H2s to single files.

---

## Memory candidates

- none. (All durable facts surfaced here are already established in the bibles or are migration-process observations recorded in this audit note and the Phase 01 deliverables; per protocol, do not store facts already in a bible. mem0 was additionally unavailable - HTTP 503 - during this audit, so no recall cross-check was possible; bibles were used as authority instead. The orchestrator may, if desired, persist the following migration-process notes, but they are not story canon: (1) all four canon monoliths are Version 1.0, active canon, and contain zero internal Markdown links; (2) Master Timeline holds exactly 4 Mermaid blocks that must be preserved on split; (3) Character Bible cast of 13 profiles matches the master spec target tree one-to-one; (4) the Kade-offer companion count "five" is fixed only in the Master Timeline.)
