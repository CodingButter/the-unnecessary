---
title: "phase-04-canon-migration"
document_type: "migration-runbook"
phase: "04"
title_text: "Phase 04: Canon Migration"
depends_on:
  - "03"
status: "planned"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# Phase 04: Canon Migration

This runbook is subordinate to the authoritative master spec at
migration/REPOSITORY-REORGANIZATION-SPEC.md. If anything in this runbook ever
conflicts with that spec, the spec wins. Read the spec sections named in
"Inputs" before executing any step here. This is a planning document only. No
migration is performed by writing or reading this file.

## 1. Purpose

Split the four canon monoliths into the target canon tree under docs/20-canon/
so that a future LLM can load only the canon relevant to a given task instead of
the whole bible. This phase moves the established facts of the world, the cast,
the technology, and the chronology of "The Unnecessary" into focused files, each
governed by a per-directory index.md, without changing a single canonical fact.

Concretely, when later executed, this phase produces:

- docs/20-canon/world/** including a locations/ subtree
- docs/20-canon/characters/** with one profile per character plus shared
  relationship-map.md and viewpoint-rules.md
- docs/20-canon/technology/** split by system, including ai/ and
  infrastructure/ subtrees and the rules that limit plot convenience
- docs/20-canon/timeline/** split by historical period and Book One act
- a per-directory index.md in every canon directory that holds more than three
  meaningful files

The phase is internally subdivided by domain. Each of the four domains (world,
characters, technology, timeline) is migrated, indexed, validated, and committed
as its own checkpoint BEFORE the next domain begins. This keeps the working tree
recoverable at domain granularity and prevents a half-migrated canon from
poisoning later phases.

This phase does NOT archive the source monoliths. Archival of the originals is
deferred entirely to Phase 09 per the master spec Phase 11. The originals remain
untouched at the repo root throughout this phase and serve as the verification
baseline.

## 2. Dependencies

- Phase 03 MUST be complete and committed before this phase starts. Phase 03
  establishes the target directory skeleton, the metadata conventions, and the
  governance and vision docs that canon files reference. Phase 04 writes into the
  docs/20-canon/ tree that Phase 03 created.
- A clean working tree at the Phase 03 checkpoint commit. Confirm
  `git status` is clean before starting domain 1.
- The four source monoliths MUST still exist at the repo root and be unmodified:
  "Story Bible.md", "Character Bible.md", "Technology Rules.md",
  "Master Timeline.md".

Downstream consumers that depend on THIS phase: Phase 05 plot migration links
into character and timeline canon, and Phase 09 archival cannot run until every
section of these four monoliths has a confirmed destination here. Every
top-level Technology Rules section now has a named owner in this runbook,
including "Computing Hardware" (infrastructure/computing-hardware.md, T2) and
"Northglass" (technology/northglass.md facility plus ai/morrow.md origin, T3 and
T1), so the Phase 09 archival coverage gate is satisfiable once this phase
completes.

## 3. Inputs

Source monoliths to be split (read-only baseline, repo root, exact filenames):

- "Story Bible.md" (world canon, locations, plus character and tech overviews
  that must be summarized-and-linked, not duplicated)
- "Character Bible.md" (one file per character; shared relationship map and
  viewpoint or dialogue rules)
- "Technology Rules.md" (technology canon split by system)
- "Master Timeline.md" (chronology split by historical period and Book One act;
  contains 4 Mermaid blocks that MUST be preserved verbatim)

Master spec sections to read for operational detail (authoritative):

- Master spec Phase 4, subsections "Story Bible", "Character Bible",
  "World and Technology Rules", and "Master Timeline". These define the exact
  split boundaries.
- Master spec Phase 2 for the exact target tree under docs/20-canon/.
- Master spec Phase 3 for the required YAML front matter shape and fields.
- Master spec Phase 5 for index.md requirements.
- Master spec Phase 12 for the no-duplication rules across domains.
- Master spec "Validation Requirements" for the canon-specific completion checks.

Observed source structure (from heading inventory, to guide the split; the spec
remains the authority on boundaries):

- Story Bible: core premise, central questions, thematic argument, time period,
  shape of society (gatekeepers, protected wealthy, everyone else), erosion of
  ordinary life, protected enclaves, Mars and the Mars Development Network,
  primary setting, main locations (Eli's neighborhood, Lakeward, Northglass,
  the neighborhood network, Mars), series direction, rules for consistency. It
  also carries character and Morrow and Crown overviews that belong primarily in
  the characters and technology domains.
- Character Bible: profiles for Eli Rook, Jonah Mercer, Adrian Kade, Lena
  Okafor, June Park, Mara Voss, Talia Reed, Nolan Avery, Sera Vale, Celeste
  Mercer, Nora Bell, plus nonhuman Morrow and Crown; a Relationship Map section;
  Viewpoint Guidance; and Dialogue Differentiation.
- Technology Rules: foundational rule, intelligence levels, consciousness and
  personhood, Crown, Morrow, Crown and Morrow comparison, computing, energy,
  communications, cloud dependency, identity and money, robotics, transportation,
  medicine, manufacturing, security and surveillance, weapons and conflict,
  government technology, protected enclaves, community infrastructure, Northglass,
  Mars and Aurelia, hard plot restrictions, failure rules.
- Master Timeline: timeline authority, high-level progression, character birth
  dates, pre-transformation through the preservation years (2026 through 2052),
  the final months before Book One, the Book One calendar, the detailed Book One
  timeline by act (act one through act four), the Book One character knowledge
  timeline, and the secret timeline. Four Mermaid diagrams appear in this file.

## 4. Allowed Changes

Create and edit ONLY the following, all under docs/20-canon/:

- docs/20-canon/index.md (top-level canon index; see orchestrator rule on shared
  indexes)
- docs/20-canon/world/** including:
  - docs/20-canon/world/index.md
  - docs/20-canon/world/core-premise.md
  - docs/20-canon/world/social-structure.md
  - docs/20-canon/world/infrastructure-decline.md
  - docs/20-canon/world/protected-enclaves.md
  - docs/20-canon/world/mars-and-aurelia.md
  - docs/20-canon/world/government-and-corporations.md
  - docs/20-canon/world/themes-and-questions.md
  - docs/20-canon/world/locations/index.md
  - docs/20-canon/world/locations/greater-detroit.md
  - docs/20-canon/world/locations/elis-neighborhood.md
  - docs/20-canon/world/locations/lakeward.md
  - docs/20-canon/world/locations/northglass.md
  - docs/20-canon/world/locations/mars-sites.md
- docs/20-canon/characters/** including:
  - docs/20-canon/characters/index.md
  - docs/20-canon/characters/relationship-map.md
  - docs/20-canon/characters/viewpoint-rules.md
  - docs/20-canon/characters/profiles/*.md (one kebab-case file per character,
    for example eli-rook.md, jonah-mercer.md, adrian-kade.md, lena-okafor.md,
    june-park.md, mara-voss.md, talia-reed.md, nolan-avery.md, sera-vale.md,
    celeste-mercer.md, nora-bell.md, morrow.md, crown.md)
- docs/20-canon/technology/** including:
  - docs/20-canon/technology/index.md
  - docs/20-canon/technology/foundational-rules.md
  - docs/20-canon/technology/ai/index.md and ai/*.md (intelligence-levels.md,
    crown.md, morrow.md, crown-vs-morrow.md, consciousness-and-personhood.md).
    ai/morrow.md is the named owner of the Technology Rules "Morrow's Origin at
    Northglass" material (Morrow-origin authority). The Technology Rules
    "AI Cannot Solve Moral Conflict Mathematically" rule is a plot-limiting rule
    and is owned verbatim by hard-plot-restrictions.md (see T3); ai/morrow.md and
    ai/consciousness-and-personhood.md summarize-and-link to it, never copy it.
  - docs/20-canon/technology/infrastructure/*.md (energy.md, communications.md,
    cloud-dependency.md, identity-and-money.md, community-infrastructure.md,
    computing-hardware.md). computing-hardware.md is the named owner of the
    Technology Rules "Computing Hardware" section (advanced processors, hardware
    longevity, data centers, cooling).
  - docs/20-canon/technology/northglass.md (named owner of the Technology Rules
    "Northglass" facility material: facility history, why it was abandoned, and
    remaining technology). This is the technology-side Northglass authority that
    the world-domain locations/northglass.md cross-link in W3 resolves to. The
    "Morrow's Origin at Northglass" subsection is NOT owned here; northglass.md
    summarizes the origin in one or two sentences and links to ai/morrow.md,
    which is the single Morrow-origin authority (no duplication, master spec
    Phase 12).
  - docs/20-canon/technology/robotics-and-manufacturing.md, medicine.md,
    transportation.md, security-and-conflict.md, mars-technology.md,
    hard-plot-restrictions.md, failure-rules.md
- docs/20-canon/timeline/** including:
  - docs/20-canon/timeline/index.md
  - docs/20-canon/timeline/character-birth-dates.md
  - docs/20-canon/timeline/historical/*.md
    (2026-2034-assistance-and-compression.md,
    2035-2041-autonomy-and-labor-break.md,
    2042-2047-infrastructure-and-support-collapse.md,
    2048-2052-preservation-years.md)
  - docs/20-canon/timeline/book-1/index.md and book-1/*.md (pre-book-2053.md,
    act-1-timeline.md, act-2-timeline.md, act-3-timeline.md, act-4-timeline.md,
    character-knowledge-timeline.md, secret-timeline.md)

All new filenames MUST be lowercase kebab-case. All active canon files MUST carry
YAML front matter per the master spec Phase 3 shape. Prose written by agents
(index summaries, archive-pointer notes) MUST avoid em dashes. Canonical prose
copied from the monoliths MUST be moved verbatim, not paraphrased.

The exact file list above is the planned target. The orchestrator owns final
path choices and may adjust to match real content and the master spec Phase 2
tree; agents propose, orchestrator ratifies.

## 5. Prohibited Changes

- Do NOT modify, move, split, rename, paraphrase, or archive any of the four
  source monoliths or any other file at the repo root. The originals stay exactly
  where they are. Archival of these monoliths is Phase 09 only (master spec
  Phase 11). Any agent that touches a root monolith has failed its task.
- Do NOT create, edit, or delete anything under archive/ in this phase.
- Do NOT touch any directory outside docs/20-canon/: not docs/00-governance/,
  10-vision/, 30-plot/, 40-blueprints/, 50-manuscript/, 60-continuity/,
  70-research/, not context-manifests/, scripts/, .context/, or migration/
  (other than this runbook, which is already authored).
- Do NOT duplicate canon across domains. Per master spec Phase 12: character
  facts live in profiles, technology capabilities live in technology files,
  dates live in timeline files, world and location facts live in world files.
  Where a concept crosses domains (for example Morrow appears in characters,
  technology, and timeline), the secondary location summarizes in one or two
  sentences and links to the authority. Do NOT copy a full Morrow or Crown
  section into more than one domain.
- Do NOT invent, correct, reconcile, or "improve" any canonical fact. If two
  sources disagree, do NOT silently resolve it; flag it for the orchestrator
  (see Human Review Points).
- Do NOT alter, reflow, or "fix" Mermaid diagrams from the Master Timeline; move
  the fenced blocks verbatim into the destination timeline files.
- Do NOT invent version history or metadata values not present in the source.
- Two or more parallel agents MUST NOT edit the same index.md, the same
  manifest, or any other shared file at the same time. Shared-index edits are
  reserved to the orchestrator (see Orchestrator Responsibilities).

## 6. Agent Delegation Plan

The phase runs domain by domain. WITHIN a domain, profile or system files are
independent and may be split by parallel agents because each writes a distinct,
non-overlapping file. The per-domain index.md is written LAST and by a single
writer (the orchestrator or one dedicated agent), never concurrently with the
content agents. Domains run in sequence: world, then characters, then technology,
then timeline. Each domain is fully validated and committed before the next.

General rule for every agent task below: agents read the relevant monolith
(read-only) and the relevant master spec subsection, then write only their
assigned destination files. No agent edits a shared index. No agent edits another
agent's files. The orchestrator verifies by diffing the new files against the
source headings and by running the validation checks in section 10.

### Domain 1: World (source: "Story Bible.md")

Task W1: World core and society
- Exact scope: split the Story Bible world canon into core-premise.md,
  social-structure.md (gatekeepers, protected wealthy, everyone else),
  infrastructure-decline.md (erosion of ordinary life), themes-and-questions.md
  (central questions and thematic argument), government-and-corporations.md.
- Inputs: "Story Bible.md" (read-only); master spec Phase 4 "Story Bible";
  Phase 3 metadata shape.
- Expected output: the five world-root files above with front matter and verbatim
  canonical prose; no character profiles or tech rules duplicated, only links.
- Read-only or may-edit: may-edit ONLY its five destination files.
- Files it may touch: docs/20-canon/world/core-premise.md,
  social-structure.md, infrastructure-decline.md, themes-and-questions.md,
  government-and-corporations.md.
- Files it must not touch: any index.md, any other domain, the source monolith,
  archive/, anything outside docs/20-canon/world/.
- Orchestrator verification: confirm every "shape of society", "erosion",
  "central questions", and "thematic argument" heading from Story Bible maps to
  exactly one destination heading; grep the new files for any pasted full
  character or technology section (must be absent).

Task W2: Enclaves and Mars overview
- Exact scope: split protected-enclaves.md and mars-and-aurelia.md from the
  Story Bible enclave and Mars sections. Mars settlement and tech specifics
  remain summarized here and link to the technology domain Mars file.
- Inputs: "Story Bible.md" (read-only); master spec Phase 4 and Phase 12.
- Expected output: two world-root files with front matter; Mars tech detail
  linked, not duplicated.
- Read-only or may-edit: may-edit ONLY its two destination files.
- Files it may touch: docs/20-canon/world/protected-enclaves.md,
  docs/20-canon/world/mars-and-aurelia.md.
- Files it must not touch: indexes, other domains, source monolith, archive/.
- Orchestrator verification: confirm enclave and Mars overview headings are
  represented; confirm Mars technical detail is a link to technology/mars,
  not a copy.

Task W3: Locations subtree
- Exact scope: split the Story Bible "Main Locations" section into one file per
  location: greater-detroit.md, elis-neighborhood.md, lakeward.md,
  northglass.md, mars-sites.md (the neighborhood network folds into the
  appropriate location file or greater-detroit.md per orchestrator decision).
- Inputs: "Story Bible.md" (read-only); master spec Phase 4 and Phase 2 tree.
- Expected output: the location files above with front matter. Northglass world
  context here is a location-level summary that links to the named technology
  destinations rather than duplicating them: it links to
  docs/20-canon/technology/northglass.md for the facility history, abandonment,
  and remaining technology (owned by T3), and to
  docs/20-canon/technology/ai/morrow.md for the Morrow-origin-at-Northglass
  material (owned by T1). Both targets are created in this phase, so the
  cross-link resolves.
- Read-only or may-edit: may-edit ONLY its location files.
- Files it may touch: docs/20-canon/world/locations/greater-detroit.md,
  elis-neighborhood.md, lakeward.md, northglass.md, mars-sites.md.
- Files it must not touch: locations/index.md, world-root files, other domains,
  source monolith, archive/.
- Orchestrator verification: each named location heading maps to a file; no
  location prose lost; the northglass.md cross-links to
  technology/northglass.md and technology/ai/morrow.md resolve to files that
  exist after T1 and T3 complete.

### Domain 2: Characters (source: "Character Bible.md")

Task C1 through Cn: per-character profiles (parallelizable, one agent per
character or small batches of characters)
- Exact scope: for each character, copy the full profile from the Character
  Bible into docs/20-canon/characters/profiles/<kebab>.md, preserving every
  field the master spec Phase 4 requires (basic information, appearance, history,
  personality, external goal, internal need, fear, contradiction, moral
  boundary, secret, false belief, truth or needed growth, Book One arc,
  long-term arc, speech pattern, writing rules, relationships). One file each for
  eli-rook, jonah-mercer, adrian-kade, lena-okafor, june-park, mara-voss,
  talia-reed, nolan-avery, sera-vale, celeste-mercer, nora-bell, morrow, crown.
- Inputs: "Character Bible.md" (read-only); master spec Phase 4 "Character
  Bible"; Phase 3 metadata shape.
- Expected output: one profile file per assigned character with front matter and
  verbatim canonical content; Morrow and Crown profiles carry behavioral identity
  only and link to the technology AI files for architecture and capabilities
  (no duplication, master spec Phase 12).
- Read-only or may-edit: may-edit ONLY the specific profile file(s) assigned.
- Files it may touch: only the assigned profiles/<character>.md file(s).
- Files it must not touch: characters/index.md, relationship-map.md,
  viewpoint-rules.md, any other character's file, other domains, source monolith,
  archive/.
- Orchestrator verification: for each character, confirm every required field
  heading is present and content matches the source; confirm the Morrow and
  Crown profiles link to technology rather than copying capability lists.
- Concurrency note: because each agent writes a distinct profile file, multiple
  character agents may run in parallel safely. They MUST NOT share a file.

Task C-shared: relationship map and viewpoint or dialogue rules
- Exact scope: move the Character Bible "Relationship Map" into
  relationship-map.md, and "Viewpoint Guidance" plus "Dialogue Differentiation"
  into viewpoint-rules.md (dialogue differentiation may instead route to a style
  file if the orchestrator decides; default is viewpoint-rules.md as the shared
  home noted in the deliverables).
- Inputs: "Character Bible.md" (read-only); master spec Phase 4.
- Expected output: relationship-map.md and viewpoint-rules.md with front matter.
- Read-only or may-edit: may-edit ONLY those two files.
- Files it may touch: docs/20-canon/characters/relationship-map.md,
  docs/20-canon/characters/viewpoint-rules.md.
- Files it must not touch: characters/index.md, any profile, other domains,
  source monolith, archive/.
- Concurrency note: this task MUST NOT run while any agent is editing those two
  files; only one writer per shared file. It may run in parallel with the
  per-profile agents because it touches different files.
- Orchestrator verification: confirm all relationship pairings and the viewpoint
  rule and per-character dialogue entries are represented.

### Domain 3: Technology (source: "Technology Rules.md")

Task T1: Foundations and AI subtree
- Exact scope: foundational-rules.md (the foundational rule plus failure-related
  framing that belongs at the root), and ai/index.md content source material plus
  ai/intelligence-levels.md, ai/crown.md, ai/morrow.md, ai/crown-vs-morrow.md,
  ai/consciousness-and-personhood.md. ai/morrow.md is the single named owner of
  the Technology Rules "Morrow's Origin at Northglass" subsection (the
  Morrow-origin authority); the origin prose moves here verbatim. The
  technology-side "Northglass" facility section itself is owned by T3
  (technology/northglass.md), which summarizes the origin and links back to
  ai/morrow.md, so the W3 world cross-link resolves to a real destination.
- Plot-limiting rule handling: the Technology Rules
  "AI Cannot Solve Moral Conflict Mathematically" rule is a plot-limiting rule.
  It is NOT owned in T1. It is preserved verbatim by T3 in
  hard-plot-restrictions.md (where it physically sits in the source, under
  "Hard Plot Restrictions"). ai/morrow.md and ai/consciousness-and-personhood.md
  reference it with a one or two sentence summary and a link to
  hard-plot-restrictions.md; they MUST NOT paraphrase or restate the rule, so its
  plot-limiting wording is not orphaned and is not duplicated.
- Inputs: "Technology Rules.md" (read-only); master spec Phase 4 "World and
  Technology Rules"; Phase 12.
- Expected output: the foundational file and the ai/ system files with front
  matter; capabilities and limitations preserved exactly; Crown and Morrow tech
  files hold architecture and capabilities and link to the character profiles for
  behavioral identity, not the other way around; ai/morrow.md carries the
  Morrow-origin-at-Northglass material verbatim and links to
  technology/northglass.md for facility context and to hard-plot-restrictions.md
  for the moral-conflict rule.
- Read-only or may-edit: may-edit ONLY the foundational file and ai/ system files
  (NOT ai/index.md).
- Files it may touch: docs/20-canon/technology/foundational-rules.md and
  docs/20-canon/technology/ai/intelligence-levels.md, crown.md, morrow.md,
  crown-vs-morrow.md, consciousness-and-personhood.md.
- Files it must not touch: technology/index.md, ai/index.md, infrastructure
  files, technology/northglass.md, other domains, source monolith, archive/.
- Orchestrator verification: confirm every Crown, Morrow, and Crown-and-Morrow
  capability and limitation is present; confirm the "Morrow's Origin at
  Northglass" prose landed verbatim in ai/morrow.md and nowhere else; confirm
  ai/morrow.md links to technology/northglass.md and to hard-plot-restrictions.md
  rather than copying their content; confirm no behavioral-identity prose is
  duplicated from the character profiles.

Task T2: Infrastructure subtree
- Exact scope: infrastructure/energy.md, communications.md, cloud-dependency.md,
  identity-and-money.md, community-infrastructure.md, and computing-hardware.md
  from the corresponding Technology Rules sections. computing-hardware.md is the
  named owner of the Technology Rules "Computing Hardware" top-level section and
  all of its subsections (advanced processors, hardware longevity, data centers,
  cooling); this is the destination that closes the unrouted-computing gap.
- Inputs: "Technology Rules.md" (read-only); master spec Phase 4 (the Phase 4
  split list names "computing" explicitly).
- Expected output: the six infrastructure files with front matter; energy as the
  primary constraint and load-shedding rules preserved; the full Computing
  Hardware section moved verbatim into computing-hardware.md with no subsection
  dropped.
- Read-only or may-edit: may-edit ONLY those six files.
- Files it may touch: docs/20-canon/technology/infrastructure/*.md as listed
  (energy.md, communications.md, cloud-dependency.md, identity-and-money.md,
  community-infrastructure.md, computing-hardware.md).
- Files it must not touch: any index, ai/ files, technology/northglass.md, other
  domains, source monolith, archive/.
- Orchestrator verification: confirm energy, communications, cloud, identity,
  community, and computing sections map one-to-one; confirm every Computing
  Hardware subsection (advanced processors, hardware longevity, data centers,
  cooling) lands in computing-hardware.md and nowhere else.

Task T3: Domain-system files, Northglass facility, and plot-limiting rules
- Exact scope: robotics-and-manufacturing.md, medicine.md, transportation.md,
  security-and-conflict.md, mars-technology.md, northglass.md,
  hard-plot-restrictions.md, failure-rules.md. The Technology Rules "Hard Plot
  Restrictions" and "Failure Rules" sections MUST be preserved verbatim because
  they limit plot convenience; preserve any other rule whose wording constrains
  what AI or machines can do. The "Hard Plot Restrictions" section includes the
  "AI Cannot Solve Moral Conflict Mathematically" rule, which MUST be reproduced
  verbatim in hard-plot-restrictions.md; this is the single authority for that
  rule, and the ai/ files (T1) link to it rather than restate it.
- northglass.md (technology-side Northglass authority): move the Technology Rules
  "Northglass" facility material verbatim (facility history, why it was
  abandoned, remaining technology). The "Morrow's Origin at Northglass"
  subsection is owned by ai/morrow.md (T1), so northglass.md summarizes that
  origin in one or two sentences and links to ai/morrow.md; it does NOT copy the
  origin prose. This file is what the world-domain locations/northglass.md
  cross-link (W3) resolves to, closing the dangling-cross-link gap.
- Inputs: "Technology Rules.md" (read-only); master spec Phase 4 ("Preserve any
  rule whose wording limits plot convenience"; the Phase 4 split list names
  "Northglass" explicitly); Phase 12 for the Northglass-to-Morrow-origin link.
- Expected output: the eight files above with front matter, restriction wording
  intact, and the Northglass facility material verbatim with a link (not a copy)
  to the Morrow-origin authority.
- Read-only or may-edit: may-edit ONLY those eight files.
- Files it may touch: the eight technology-root files listed (including
  docs/20-canon/technology/northglass.md).
- Files it must not touch: any index, ai/ and infrastructure/ files (including
  ai/morrow.md), other domains, source monolith, archive/.
- Orchestrator verification: diff hard-plot-restrictions.md and failure-rules.md
  line by line against the source to confirm no restriction softened or dropped,
  and confirm "AI Cannot Solve Moral Conflict Mathematically" is present verbatim
  in hard-plot-restrictions.md; confirm the Northglass facility material is in
  northglass.md and that the Morrow-origin content is linked to ai/morrow.md, not
  duplicated here.

### Domain 4: Timeline (source: "Master Timeline.md")

Task M1: Historical periods
- Exact scope: split the pre-Book-One chronology into
  historical/2026-2034-assistance-and-compression.md,
  2035-2041-autonomy-and-labor-break.md,
  2042-2047-infrastructure-and-support-collapse.md,
  2048-2052-preservation-years.md, plus character-birth-dates.md. Any Mermaid
  diagram in these ranges moves verbatim.
- Inputs: "Master Timeline.md" (read-only, contains 4 Mermaid blocks); master
  spec Phase 4 "Master Timeline".
- Expected output: the historical period files plus character-birth-dates.md
  with front matter; Mermaid fenced blocks preserved exactly.
- Read-only or may-edit: may-edit ONLY those files.
- Files it may touch: docs/20-canon/timeline/character-birth-dates.md and
  docs/20-canon/timeline/historical/*.md as listed.
- Files it must not touch: timeline/index.md, book-1/ files, other domains,
  source monolith, archive/.
- Orchestrator verification: confirm every year heading from 2026 through 2052
  lands in exactly one period file; confirm Mermaid blocks render as valid fenced
  blocks; confirm no detailed chapter summaries pulled in from plot files.

Task M2: Book One timeline subtree
- Exact scope: split the final months and detailed Book One timeline into
  book-1/pre-book-2053.md, act-1-timeline.md, act-2-timeline.md,
  act-3-timeline.md, act-4-timeline.md, character-knowledge-timeline.md,
  secret-timeline.md.
- Inputs: "Master Timeline.md" (read-only); master spec Phase 4 and Phase 12.
- Expected output: the book-1 timeline files with front matter; act split matches
  the source act boundaries (act one through act four); knowledge and secret
  timelines preserved.
- Read-only or may-edit: may-edit ONLY those files.
- Files it may touch: docs/20-canon/timeline/book-1/*.md as listed (NOT
  book-1/index.md).
- Files it must not touch: timeline/index.md, book-1/index.md, historical files,
  other domains, source monolith, archive/.
- Orchestrator verification: confirm act boundaries match the source; confirm the
  character knowledge timeline and secret timeline are complete; confirm dates
  are not duplicated into plot files in a later phase by leaving timeline as the
  authority here.

### Index writers (one per domain, run after content agents, never concurrent)

Index task per domain: write the per-directory index.md files for that domain
(for example world/index.md and world/locations/index.md; characters/index.md;
technology/index.md, ai/index.md; timeline/index.md, book-1/index.md). Each index
follows master spec Phase 5: purpose, read-first pointer, file table, one or two
sentence summary per file, authority or status, common tasks per file, links to
related indexes. Index files summarize and link; they never become replacement
canon.
- Read-only or may-edit: may-edit ONLY the index.md files of the current domain.
- Concurrency rule: only ONE index writer runs at a time per shared index. No
  content agent runs against a directory while its index is being written.
- The top-level docs/20-canon/index.md is reserved to the orchestrator.

## 7. Orchestrator Responsibilities

Reserved to the main instance and never delegated:

- Final path and filename choices, including any deviation from the planned file
  list to match real content or the master spec Phase 2 tree.
- Canon-conflict resolution. If agents flag two sources that disagree, or a
  cross-domain fact that has no clear owner, the orchestrator decides where the
  authority lives and records the conflict for human review. Agents never resolve
  conflicts.
- All shared-index edits: docs/20-canon/index.md and every per-directory
  index.md. The orchestrator either writes these itself or assigns exactly one
  index writer at a time and serializes them. Parallel agents never edit a shared
  index or manifest.
- Sequencing the four domains and enforcing the per-domain checkpoint: a domain
  is not "done" until its content files, its indexes, its validation, and its git
  commit are all complete. The next domain does not start before that.
- Archival approval. The orchestrator confirms that NO archival happens in this
  phase and that the source monoliths remain untouched. Archival is Phase 09.
- Acceptance of agent work: reading each new file against the source headings,
  running the validation checks in section 10, and rejecting or re-dispatching any
  agent output that paraphrases canon, duplicates across domains, drops a
  restriction, or touches a forbidden path.
- Cross-domain link integrity: ensuring that summarize-and-link references (for
  example Morrow appearing in characters, technology, and timeline) point to the
  single authority and do not duplicate content.

## 8. Execution Steps

1. Confirm Phase 03 is committed and `git status` is clean. Confirm the four
   source monoliths exist and are unmodified at the repo root.
2. Re-read master spec Phase 4 subsections, Phase 2 tree, Phase 3 metadata,
   Phase 5 indexes, and Phase 12 no-duplication rules. The spec governs all
   boundary decisions.
3. Domain 1, World: dispatch tasks W1, W2, W3 in parallel (distinct files).
4. Orchestrator verifies W1 to W3 against Story Bible headings; resolves any
   flagged conflict; confirms no character or tech section was duplicated.
5. Orchestrator writes world/index.md and world/locations/index.md (single
   writer, no concurrent content edits).
6. Run validation (section 10) scoped to docs/20-canon/world/. Fix issues.
7. Checkpoint commit for the world domain (see section 13).
8. Domain 2, Characters: dispatch per-character profile agents in parallel plus
   the C-shared agent (all touch distinct files).
9. Orchestrator verifies every required profile field per character, confirms
   Morrow and Crown profiles link to technology, verifies relationship map and
   viewpoint rules complete.
10. Orchestrator writes characters/index.md (single writer).
11. Run validation scoped to docs/20-canon/characters/. Fix issues.
12. Checkpoint commit for the characters domain.
13. Domain 3, Technology: dispatch T1, T2, T3 in parallel (distinct files).
14. Orchestrator verifies capabilities and limitations preserved, line-diffs the
    hard-plot-restrictions and failure-rules files against source, confirms no
    behavioral identity duplicated from profiles.
15. Orchestrator writes technology/index.md and technology/ai/index.md (single
    writer).
16. Run validation scoped to docs/20-canon/technology/. Fix issues.
17. Checkpoint commit for the technology domain.
18. Domain 4, Timeline: dispatch M1 and M2 in parallel (distinct files).
19. Orchestrator verifies year and act coverage, confirms the 4 Mermaid blocks
    moved verbatim and render as valid fenced blocks, confirms knowledge and
    secret timelines complete.
20. Orchestrator writes timeline/index.md and timeline/book-1/index.md (single
    writer).
21. Run validation scoped to docs/20-canon/timeline/. Fix issues.
22. Orchestrator writes or finalizes the top-level docs/20-canon/index.md linking
    the four domain indexes.
23. Checkpoint commit for the timeline domain and the canon top-level index. This
    closes the phase.
24. Confirm the four source monoliths are still present and byte-identical to the
    Phase 03 baseline (they were never to be touched).

## 9. Deliverables

- docs/20-canon/world/** with index.md, a locations/ subtree, and an index.md in
  locations/.
- docs/20-canon/characters/** with index.md, relationship-map.md (shared),
  viewpoint-rules.md (shared), and one profile per character under profiles/.
- docs/20-canon/technology/** with index.md, foundational-rules.md, an ai/
  subtree with its own index.md (ai/morrow.md owning the Morrow-origin material),
  an infrastructure/ subtree that includes computing-hardware.md (the Computing
  Hardware authority), a technology/northglass.md facility authority, the
  per-system root files, and the preserved hard-plot-restrictions.md (including
  the verbatim "AI Cannot Solve Moral Conflict Mathematically" rule) and
  failure-rules.md.
- docs/20-canon/timeline/** with index.md, character-birth-dates.md, a
  historical/ subtree split by period, and a book-1/ subtree split by act with
  its own index.md, plus the character-knowledge-timeline.md and
  secret-timeline.md.
- docs/20-canon/index.md tying the four domain indexes together.
- A per-directory index.md in every canon directory with more than three
  meaningful files.
- Four git checkpoint commits, one per domain.
- The four source monoliths remain at the repo root, untouched.

## 10. Validation

All checks below MUST pass for the relevant domain before its checkpoint, and all
must pass across docs/20-canon/ before the phase is considered complete.

- Coverage: every meaningful heading in each source monolith maps to exactly one
  destination file. No canonical section is lost. Compare source headings to
  split-file headings (the heading inventory in section 3 is the starting map; the
  spec boundaries govern). Specifically confirm the Technology Rules "Computing
  Hardware" section lands in infrastructure/computing-hardware.md, the "Northglass"
  facility section lands in technology/northglass.md, and the "Morrow's Origin at
  Northglass" subsection lands in ai/morrow.md, each in exactly one place.
- No duplication: no full character profile, technology capability list, date
  table, or location section appears in more than one domain. Cross-domain
  references are short summaries with links to the single authority (master spec
  Phase 12). A duplicate-authority scan finds no repeated long passages across
  active canon files.
- Restriction preservation: hard-plot-restrictions.md and failure-rules.md
  reproduce the source restriction wording verbatim; no plot-limiting rule is
  softened, generalized, or dropped. In particular the "AI Cannot Solve Moral
  Conflict Mathematically" rule is present verbatim in hard-plot-restrictions.md
  and is referenced by link (not restated) from ai/morrow.md and
  ai/consciousness-and-personhood.md.
- Mermaid integrity: all 4 Master Timeline Mermaid blocks appear verbatim in the
  destination timeline files and remain valid fenced ```mermaid blocks.
- Metadata: every active canon file carries the required YAML front matter fields
  per master spec Phase 3 (title, document_type, status, authority, summary,
  tags, related, source_documents), with valid relative paths in related.
- Index conformance: every directory with more than three meaningful files has an
  index.md meeting the master spec Phase 5 requirements, and each index links to
  the authority files rather than restating canon.
- Link integrity: all relative Markdown links and all front-matter related and
  source_documents paths resolve to existing files within the new tree.
- Character completeness: a profile exists for every established character, and
  each profile contains every required field from master spec Phase 4.
- Source untouched: the four root monoliths are byte-identical to the Phase 03
  baseline; nothing under archive/ was created or changed.
- No em dashes in any agent-written prose (index summaries, notes).

## 11. Human Review Points

Pause for human review when:

- Any canon conflict is discovered (two sources disagree, or a value is
  ambiguous). The orchestrator records both statements and the conflict; it does
  NOT silently choose. A human ratifies the resolution before the affected
  domain is committed.
- A cross-domain fact has no obvious authority owner (for example a Mars detail
  that could live in world, technology, or timeline). The orchestrator proposes
  the owner; a human confirms before finalizing links.
- The split boundary for any file is genuinely unclear from the source and the
  spec. Surface the choice rather than guessing.
- Before each per-domain checkpoint commit, present a short diff summary (files
  created, headings mapped, conflicts flagged) for human sign-off.

## 12. Completion Criteria

- [ ] Phase 03 confirmed complete and committed; working tree clean at start.
- [ ] World domain split into docs/20-canon/world/** including locations/, with
      indexes, validated and committed.
- [ ] Characters domain split into docs/20-canon/characters/** with one profile
      per character plus shared relationship-map.md and viewpoint-rules.md, with
      index, validated and committed.
- [ ] Technology domain split into docs/20-canon/technology/** by system,
      including ai/ and infrastructure/ subtrees, with hard-plot-restrictions.md
      and failure-rules.md preserved verbatim, with indexes, validated and
      committed.
- [ ] Technology "Computing Hardware" routed to
      infrastructure/computing-hardware.md; "Northglass" facility routed to
      technology/northglass.md; "Morrow's Origin at Northglass" routed to
      ai/morrow.md; "AI Cannot Solve Moral Conflict Mathematically" preserved
      verbatim in hard-plot-restrictions.md. No section unrouted.
- [ ] The world locations/northglass.md cross-links resolve to
      technology/northglass.md and technology/ai/morrow.md (both created here).
- [ ] Timeline domain split into docs/20-canon/timeline/** by historical period
      and Book One act, with all 4 Mermaid blocks preserved, with indexes,
      validated and committed.
- [ ] docs/20-canon/index.md links the four domain indexes.
- [ ] Every canon directory with more than three meaningful files has an
      index.md meeting the spec Phase 5 requirements.
- [ ] No canon duplicated across domains; cross-domain references are
      summarize-and-link only.
- [ ] All canon files carry required YAML front matter; all relative links and
      related paths resolve.
- [ ] A profile exists for every established character with all required fields.
- [ ] The four source monoliths remain untouched at the repo root; nothing was
      archived (archival is Phase 09).
- [ ] No em dashes in agent-written prose.

## 13. Checkpoint

This phase uses four per-domain checkpoint commits. A domain MUST be committed
before the next domain begins, and the final commit MUST land before Phase 05
starts. Each commit is made only after that domain's validation passes and the
orchestrator accepts the work.

Suggested commit messages:

- World domain:
  `phase-04: migrate world canon and locations into docs/20-canon/world`
- Characters domain:
  `phase-04: migrate character profiles, relationship map, and viewpoint rules into docs/20-canon/characters`
- Technology domain:
  `phase-04: migrate technology rules by system into docs/20-canon/technology, restrictions preserved`
- Timeline domain (closes the phase):
  `phase-04: migrate master timeline by period and Book One act into docs/20-canon/timeline, mermaid preserved; complete canon migration`

Do NOT proceed to Phase 05 until all four checkpoints exist, the canon top-level
index is committed, and the source monoliths are confirmed untouched. Archival of
the monoliths remains deferred to Phase 09.
