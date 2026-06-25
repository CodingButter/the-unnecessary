---
title: "migration-map"
document_type: "migration-report"
phase: "01"
title_text: "Phase 01: Draft Migration Map"
status: "draft"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
authored_by: "phase-01"
---

# Phase 01: Draft Migration Map (Source to Destination)

> Draft mapping aligned to the master spec Phase 2 target tree. Phase 01 is the sole author of this map. Destinations are the orchestrator's recommended calls; later phases execute them and the human review points in `migration/repository-audit.md` section 10 should be confirmed first. No file is moved by authoring this map.

Legend: **relocate-intact** moves the whole file unchanged; **keep-intact** stays where it is; **split** divides into the listed per-section destinations. Every destination path is relative to the repository root.

## 1. Whole-file moves

| Source | Destination | Decision | Note |
|---|---|---|---|
| `Narrative Brief.md` | `docs/10-vision/narrative-brief.md` | relocate-intact | Short, read-first; spec Phase 4 keeps it intact. |
| `Development and Canon Guide.md` | `docs/00-governance/novel-development-guide.md` | relocate-intact | Kept whole as active governance; `context-loading-guide.md` and `canon-hierarchy.md` are derived from it later, not carved out of it. |
| `chapter-blueprints/Chapter Blueprint Template.md` | `docs/40-blueprints/_templates/chapter-blueprint-template.md` | relocate-intact | Spec validation requires the template remain intact. |
| `CLAUDE.md` | `CLAUDE.md` (root) | keep-intact | Updated in place in a later governance phase (spec Phase 8); never moved into `docs/`. |
| `Memory Conventions.md` | `docs/00-governance/memory-conventions.md` | relocate-intact | Added artifact; destination is an orchestrator decision (audit section 10). Alternative: keep at root. |

## 2. Split mappings

### 2.1 Story Bible to `docs/20-canon/world/`

| Source section(s) | Destination |
|---|---|
| Core Premise, Thematic Argument, Time Period, Format/Genre/Tone/Working Title | `world/core-premise.md` |
| Central Questions (and Final Promise) | `world/central-questions-and-themes.md` |
| The Shape of Society | `world/social-structure.md` |
| The Erosion of Ordinary Life | `world/infrastructure-decline.md` |
| Protected Enclaves | `world/protected-enclaves.md` |
| Mars | `world/mars-and-aurelia.md` |
| Primary Setting, Main Locations (Greater Detroit, Eli's neighborhood, Lakeward, Northglass, Mars sites) | `world/locations/greater-detroit.md`, `elis-neighborhood.md`, `lakeward.md`, `northglass.md`, `mars-sites.md` |
| Book One, Act One to Four, per-character Book One arcs, Narrative Structure | `world/book-1-arc.md` |
| Series Direction | `world/series-direction.md` |
| Rules for Consistency | `world/consistency-rules.md` |
| Condensed character sections | link-only to `docs/20-canon/characters/profiles/*` (not duplicated) |
| Condensed technology and Crown sections | link-only to `docs/20-canon/technology/*` (not duplicated) |
| Historical Timeline section | link-only to `docs/20-canon/timeline/*` (not duplicated; source of conflict C2) |
| Research Ledger | seeds `docs/70-research/` (deferred until research exists) |

### 2.2 Character Bible to `docs/20-canon/characters/`

One file per character under `profiles/`. Each H1 character span carries all its H2 fields into its file.

| Source H1 | Destination |
|---|---|
| Elias "Eli" Rook | `profiles/eli-rook.md` |
| Jonah Mercer | `profiles/jonah-mercer.md` |
| Adrian Kade | `profiles/adrian-kade.md` |
| Dr. Lena Okafor | `profiles/lena-okafor.md` |
| June Park | `profiles/june-park.md` |
| Mara Voss | `profiles/mara-voss.md` |
| Talia Reed | `profiles/talia-reed.md` |
| Nolan Avery | `profiles/nolan-avery.md` |
| Sera Vale | `profiles/sera-vale.md` |
| Celeste Mercer | `profiles/celeste-mercer.md` |
| Nora Bell | `profiles/nora-bell.md` |
| Morrow (Nonhuman Characters) | `profiles/morrow.md` |
| Crown (Nonhuman Characters) | `profiles/crown.md` |
| Relationship Map | `characters/relationship-map.md` |
| Viewpoint Guidance | `characters/viewpoint-rules.md` |
| Dialogue Differentiation | `characters/dialogue-differentiation.md` |
| Character Continuity Fields | informs `docs/60-continuity/` (Phase 07); not lost |
| Core Character Principles, Primary Cast, Final Character Standard | `characters/index.md` |

### 2.3 World and Technology Rules to `docs/20-canon/technology/`

| Source H1 block(s) | Destination |
|---|---|
| Foundational Rule, Technological State of the World | `technology/foundational-rules.md` |
| Levels of Artificial Intelligence | `technology/ai/intelligence-levels.md` |
| Consciousness and Personhood | `technology/ai/consciousness-and-personhood.md` |
| Crown | `technology/ai/crown.md` |
| Morrow | `technology/ai/morrow.md` |
| Crown and Morrow | `technology/ai/crown-vs-morrow.md` |
| Energy | `technology/infrastructure/energy.md` |
| Communications | `technology/infrastructure/communications.md` |
| Cloud Dependency | `technology/infrastructure/cloud-dependency.md` |
| Identity, Money, Access | `technology/infrastructure/identity-and-money.md` |
| Community Infrastructure | `technology/infrastructure/community-infrastructure.md` |
| Robotics, Manufacturing and Materials | `technology/robotics-and-manufacturing.md` |
| Transportation | `technology/transportation.md` |
| Medicine | `technology/medicine.md` |
| Security and Surveillance, Weapons and Conflict | `technology/security-and-conflict.md` |
| Mars and the Aurelia Initiative | `technology/mars-technology.md` (cross-link `world/mars-and-aurelia.md`) |
| Hard Plot Restrictions (10) | `technology/hard-plot-restrictions.md` (verbatim) |
| Failure Rules (5) | `technology/failure-rules.md` (verbatim) |
| Computing Hardware | `technology/foundational-rules.md` appendix (orchestrator call; alt: `technology/computing.md`) |
| Government Technology, Information and Propaganda | `world/government-and-corporations.md` (orchestrator call; cross-link from technology) |
| Protected Enclaves (tech facets) | cross-link to `world/protected-enclaves.md` (home is world; tech facets linked) |
| Northglass (tech facets) | cross-link to `world/locations/northglass.md` (home is world) |
| Scientific Progress | `technology/foundational-rules.md` appendix (orchestrator call) |
| Technology in Scenes, Continuity Questions | `docs/10-vision/style/technology-in-prose.md` (craft guidance; orchestrator call) |
| Canon Summary, Purpose | `technology/index.md` |

### 2.4 Master Timeline to `docs/20-canon/timeline/`

| Source section(s) | Destination |
|---|---|
| Timeline Authority, High-Level Historical Progression (Mermaid 1), Causal Progression (Mermaid 2), Final Chronological Standard, Purpose | `timeline/index.md` (compact chronology; Mermaid 1 and 2 preserved) |
| Principal Character Birth Dates (15 rows) | `timeline/character-birth-dates.md` |
| Before the Transformation (1992 to 2024), Assistance Era, Compression Era (to 2034) | `timeline/historical/2026-2034-assistance-and-compression.md` |
| General Autonomy (2035), Intelligence Acceleration (2036 to 2038), Mosaic and Replacement Wave (2039 to 2041) | `timeline/historical/2035-2041-autonomy-and-labor-break.md` |
| Infrastructure Bargains (2042), Aurelia Initiative (2043), Market Withdrawal (2044 to 2046), Support Collapse (2047) | `timeline/historical/2042-2047-infrastructure-and-support-collapse.md` |
| Preservation Years (2048 to 2052) | `timeline/historical/2048-2052-preservation-years.md` |
| Final Months Before Book One (Jan to Sep 2053) | `timeline/book-1/pre-book-2053.md` |
| Book One Calendar and Overview (Mermaid 3 gantt) | `timeline/book-1/index.md` |
| Detailed Book One Oct 3 to 8 | `timeline/book-1/act-1-timeline.md` |
| Act Two (Oct 9 to 19) | `timeline/book-1/act-2-timeline.md` |
| Act Three (Oct 20 to 26) | `timeline/book-1/act-3-timeline.md` |
| Act Four (Oct 27 to Nov 1) | `timeline/book-1/act-4-timeline.md` |
| Book One Character Knowledge Timeline (7 tables), Parallel Character Progression (Mermaid 4) | `timeline/book-1/character-knowledge-timeline.md` |
| Secret Timeline (11-row table) | `timeline/book-1/secret-timeline.md` |
| Timing and Travel Rules | `timeline/book-1/index.md` appendix (orchestrator call) |
| Timeline Continuity Rules (18) | `timeline/index.md` (orchestrator call) |
| Open Timeline Questions (15) | `timeline/index.md` (orchestrator call; some may seed `docs/70-research/`) |

All four Mermaid blocks are preserved verbatim across `timeline/index.md` (three) and `character-knowledge-timeline.md` (one). Conflict C5 (the 2052-versus-2051 habitability label) is carried in the ledger and must not be silently fixed when these sections separate.

### 2.5 Plot Outline and Chapter Map to `docs/30-plot/book-1/`

| Source section(s) | Destination |
|---|---|
| Title block, Purpose, Book Information, Final Structural Standard | `book-1/index.md` |
| Story Spine, Structural Decision | `book-1/story-spine.md` |
| Major Structural Beats, Act Structure (Mermaid, preserved), Chapter Tension Pattern | `book-1/major-beats.md` |
| Act One (and act metadata) | `book-1/act-1.md` |
| Act Two | `book-1/act-2.md` |
| Act Three | `book-1/act-3.md` |
| Act Four | `book-1/act-4.md` |
| Each `## Chapter N: Title` entry (1 to 36), with its Date/Viewpoint/Setting and H3 sub-fields | `book-1/chapters/chapter-01.md` to `chapter-36.md` (concise plot-map entries, distinct from blueprints) |
| Subplot Map | `book-1/subplot-map.md` |
| Reveal Management | `book-1/reveal-management.md` |
| Primary Viewpoint Distribution | `book-1/index.md` (orchestrator call; alt: standalone `viewpoint-distribution.md`) |
| Drafting Rules for Chapters, Scene Card Template | `docs/40-blueprints/_templates/` adjacent (orchestrator call; craft scaffolding, not dropped) |

### 2.6 Prose and Style Guide to `docs/10-vision/style/`

| Source section(s) | Destination |
|---|---|
| Title block, Purpose, Final Style Standard | `style/index.md` |
| Core Prose Identity, Central Stylistic Principle, Sentence Style, Punctuation, Diction, Description, Environmental Tone, Free Indirect Style, Internal Thought | `style/core-prose.md` |
| Narrative Perspective, Narrative Distance | `style/viewpoint.md` |
| Dialogue (general, subtext, tags, adverbs, names) | `style/dialogue.md` |
| Character Voice Guide, per-character voice H1 blocks | `style/character-voices.md` |
| Artificial Intelligence Dialogue, Morrow, Crown | `style/ai-dialogue.md` |
| Technology in Prose, Worldbuilding Exposition | `style/technology-in-prose.md` |
| Emotional Writing, Moral and Philosophical Content | `style/emotion-and-moral-content.md` |
| Pacing, Chapter Openings, Chapter Endings, Scene Transitions, Action and Suspense, Recurring Imagery, Humor, Romance and Intimacy | `style/pacing-and-structure.md` |
| Formatting Conventions, Names and Terminology, Profanity | `style/formatting.md` |
| Prose Habits to Avoid, Cliches to Avoid | `style/prohibited-patterns.md` |
| Style Review Process (Passes 1 to 7), Chapter Style Checklist | `style/revision-checklist.md` |
| Drafting With Another AI | `docs/00-governance/` adjacent (orchestrator call; delegation guidance, not dropped) |

### 2.7 Creative Decision Log to `docs/00-governance/decision-log/`

| Source section(s) | Destination |
|---|---|
| Title, Purpose, How to Use | `decision-log/index.md` |
| Decision Statuses legend (five labels) | `decision-log/index.md` (statuses subsection; note the undefined sixth label, conflict C6) |
| Decision Entry Template (no number) | `decision-log/decision-entry-template.md` (excluded from the per-decision split) |
| Each `## Decision NNN: Title` (001 to 044) | `decision-log/decisions/NNN-slug.md` (44 files) |
| 8 category H1 headings | become index groupings and the per-decision Category field |
| Explicitly Rejected Concepts | `decision-log/index.md` subsection or `rejected-concepts.md` |
| Open Decisions | `decision-log/index.md` subsection or `open-decisions.md` |
| Existing Documents Affected (old-scheme paths) | `decision-log/index.md` subsection; old paths flagged for reconciliation |
| Future Update Procedure, Final Principle | `decision-log/index.md` subsections |

The index table carries: decision number, title, status, category, short summary, file link.

## 3. Deferred and added destinations

- `docs/70-research/` is deferred; no research material exists. The Story Bible Research Ledger and some Master Timeline open questions seed it later.
- `docs/50-manuscript/` is deferred; no approved chapter exists. The directory is created empty in Phase 02; contents wait for a real approved chapter.
- `docs/60-continuity/` is mostly new (Phase 07); the Character Continuity Fields and the timeline knowledge/secret tables inform it but do not move into it.
- `README.md` (root) and `project-status.md` (root) are new artifacts created in later phases (03 and the spec Phase 14), not mapped from any source.
- `docs/00-governance/canon-hierarchy.md` and `docs/00-governance/context-loading-guide.md` are derived from the Development and Canon Guide later; they are not separate sources.

## 4. Orchestrator decisions and open flags

The following routing calls are the orchestrator's recommendation and are flagged for human confirmation (audit section 10) before the executing phase acts:

- Memory Conventions.md to `docs/00-governance/memory-conventions.md` (alt: keep at root).
- Technology Rules world-overlap blocks (Government Technology, Protected Enclaves, Northglass, Information and Propaganda) routed to the `world/` tree with cross-links from `technology/`, so each fact has one home.
- Technology Computing Hardware and Scientific Progress folded into `technology/foundational-rules.md` appendices.
- Plot viewpoint distribution to `book-1/index.md`; Plot Drafting Rules and Scene Card Template kept with the blueprint templates.
- Style "Drafting With Another AI" routed to governance.
- Timeline travel rules, continuity rules, and open questions kept in the timeline index (some open questions may seed research).

No conflict is resolved by this map itself. Conflicts C1 through C6 were resolved post-audit under user authorization, with each fix recorded in `migration/conflicts-found.md`; duplicates D1 through D10 remain for link-consolidation in Phase 12, not handled by this map.
