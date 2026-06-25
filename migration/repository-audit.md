---
title: "repository-audit"
document_type: "migration-report"
phase: "01"
title_text: "Phase 01: Repository Audit"
status: "complete"
spec: "migration/REPOSITORY-REORGANIZATION-SPEC.md"
read_only: true
---

# Phase 01: Repository Audit

> Read-only audit. No project document was moved, split, renamed, archived, or rewritten. The only writes are the reports under `migration/` and the working notes under `migration/audit-notes/`. Master spec `migration/REPOSITORY-REORGANIZATION-SPEC.md` is authoritative; this report operationalizes its Phase 1.

This audit was produced by six read-only inspector agents (Tasks A through F per the runbook Agent Delegation Plan), each writing only its own note file under `migration/audit-notes/`. The orchestrator assembled this report, verified every load-bearing finding against the source lines (not agent summaries), and is the sole writer of this file, of `migration/migration-map.md`, and of the conflict appends to `migration/conflicts-found.md`.

## 1. Inventory completeness

- A recursive `find` for `*.md` (excluding `.git`) returns **266** files; `git ls-files '*.md'` returns **266** files; a `comm` of the two sorted lists shows **zero** differences and `git status --porcelain` is clean. The two inventories reconcile exactly: no tracked-but-missing, no present-but-untracked Markdown.
- Of the 266 Markdown files, **254** are `.claude/skills/**` BMAD tooling assets (infrastructure, not novel content). That leaves **12** novel-content and governance documents in scope for canon migration.
- Confirmed **absent** at Phase 01 (proven by `find` plus content `grep`, not assumed): manuscript chapters, continuity documents, research files, and any filled chapter blueprints beyond the template. The directories `docs/`, `archive/`, `context-manifests/`, `scripts/`, and `.context/` also do not yet exist. `chapter-blueprints/` holds exactly one file, the template.
- Mermaid total across the corpus is **7** blocks (Master Timeline 4, Plot Outline 1, Development and Canon Guide 1, Chapter Blueprint Template 1); no other document contains a Mermaid block. All must survive any later split.
- No novel-content or governance document contains any relative Markdown link of any form. Broken-link count is **0**; later-phase link work is link creation, not repair.

## 2. Existing file tree (scoped)

Novel-content monoliths (repository root):

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
chapter-blueprints/
  Chapter Blueprint Template.md   (only file in the folder)
```

Discovered governance and operational documents (root, not in the runbook's named monolith list):

```text
CLAUDE.md                 (operational entry layer; explicitly non-canon)
Memory Conventions.md     (mem0 memory-practice spec; explicitly non-canon)
```

Infrastructure and tooling (not subject to canon migration):

```text
.env  .envrc  .gitignore  .mcp.json  .audio/ (empty)
.claude/hooks/mem0-recall.sh  .claude/settings.json  .claude/settings.local.json
.claude/screenshots/  .claude/skills/** (254 BMAD skill *.md plus .toml/.csv/.py/.html assets)
migration/REPOSITORY-REORGANIZATION-SPEC.md   (master spec, read-only authority)
migration/conflicts-found.md                  (Phase 00 seeded ledger)
migration/repository-audit.md  migration/migration-map.md  (this phase's deliverables)
migration/audit-notes/{a..f}*.md              (this phase's working notes)
migration/plan/00..09-*.md                    (phase runbooks)
```

## 3. Per-document audit

Heading counts below are the orchestrator's verified `grep` counts (`^# `, `^## `, `^### `, `^```mermaid`). Where an inspector reported a slightly different count, the divergence was a counting-method difference (for example headings inside fenced blocks) and is immaterial: it never affects a split mapping. Apparent version and canon status are recorded exactly as the source states them; "not stated" means the source carries no such label and nothing was invented.

| # | Document | Path | Version | Canon status | H1 / H2 / H3 / Mermaid | Split decision | Destination root |
|---|---|---|---|---|---|---|---|
| 1 | Narrative Brief | `Narrative Brief.md` | not stated | Vision authority by subject (self-named #1 in its Canon Priority); no status string | 1 / 23 / 11 / 0 | relocate-intact | `docs/10-vision/narrative-brief.md` |
| 2 | Story Bible | `Story Bible.md` | 1.0 | active world and broad-plot canon | 1 / 38 / 64 / 0 | split | `docs/20-canon/world/` |
| 3 | Character Bible | `Character Bible.md` | 1.0 | active character canon | 22 / 233 / 0 / 0 | split | `docs/20-canon/characters/` |
| 4 | World and Technology Rules | `Technology Rules.md` | 1.0 | active technology canon | 31 / 113 / 0 / 0 | split | `docs/20-canon/technology/` |
| 5 | Master Timeline | `Master Timeline.md` | 1.0 | active chronology canon | 30 / 63 / 113 / 4 | split | `docs/20-canon/timeline/` |
| 6 | Plot Outline and Chapter Map | `Plot Outline and Chapter Map.md` | 1.0 | approved plan (not established prose) | 16 / 95 / 157 / 1 | split | `docs/30-plot/book-1/` |
| 7 | Prose and Style Guide | `Style Guide.md` | 1.0 | active style canon (YAML status in doc) | 48 / 129 / 21 / 0 | split | `docs/10-vision/style/` |
| 8 | Creative Decision Log | `Creative Decision Log.md` | 1.0 | active decision record; per-entry statuses | 17 / 63 / 245 / 0 | split | `docs/00-governance/decision-log/` |
| 9 | Novel Development and Canon Guide | `Development and Canon Guide.md` | 1.0 | active process and operating manual (not story canon) | 52 / 126 / 26 / 1 | relocate-intact (derive context-loading-guide) | `docs/00-governance/novel-development-guide.md` |
| 10 | Chapter Blueprint Template | `chapter-blueprints/Chapter Blueprint Template.md` | not stated | planning template; spec requires it remain intact | 4 / 28 / 79 / 1 | relocate-intact | `docs/40-blueprints/_templates/chapter-blueprint-template.md` |
| 11 | The Unnecessary, Project Instructions | `CLAUDE.md` | not stated | explicitly NOT canon; operational entry layer | 2 / 11 / 1 / 0 | keep-intact (updated in place later) | root `CLAUDE.md` |
| 12 | Memory Conventions (mem0) | `Memory Conventions.md` | not stated | NOT canon; memory-practice spec | 1 / 9 / 0 / 0 | relocate-intact (destination flagged) | `docs/00-governance/memory-conventions.md` (orchestrator decision; see section 10) |

### Subjects and ambiguities per document

1. **Narrative Brief.** Highest-level creative orientation: premise, narrative promise, core conflict, world, enclaves, Mars, character sketches, Morrow, themes, tone, style, storytelling rules, Book One arc, series direction, canon priority. Ambiguity: no version or status label, unlike the eight "Version 1.0" monoliths; recorded as not stated. Its Canon Priority list names "World and Technology Rules", a "Continuity Ledger", and a "Research and Plausibility Ledger"; on disk the file is `Technology Rules.md` and neither ledger exists. Naming and inventory drift, recorded for later reconciliation, not a story-canon conflict.
2. **Story Bible.** World and story foundation. Ambiguity: embeds condensed character profiles, condensed technology and Crown overviews, and a historical timeline that overlap the dedicated bibles (resolve by linking in Phase 12). Carries a deliberately narrower cast (Lena, June, Mara) than the Character Bible. Source of conflict C2 (era label) and several duplicates.
3. **Character Bible.** Full per-character canon. Verified: exactly **13** character profiles (Eli Rook, Jonah Mercer, Adrian Kade, Lena Okafor, June Park, Mara Voss, Talia Reed, Nolan Avery, Sera Vale, Celeste Mercer, Nora Bell, Morrow, Crown), matching the master spec's 13 profile slugs one to one, plus four shared sections (Relationship Map, Viewpoint Guidance, Dialogue Differentiation, Character Continuity Fields) and three framing sections (Core Character Principles, Primary Cast, Final Character Standard). Ambiguity: several minor or later characters (Nolan, Celeste, Nora, Sera, Talia, Crown) carry reduced field sets; missing fields must not be fabricated on split.
4. **World and Technology Rules.** Technology system rules and hard limits. Ambiguity: internal title is "World and Technology Rules" while the file is `Technology Rules.md`; it covers world systems (Protected Enclaves, Northglass, Mars) that also live in the Story Bible (link, do not duplicate). Plot-limiting rules requiring verbatim preservation were flagged: all 10 Hard Plot Restrictions, the 5 Failure Rules plus the visible-failure-mode rule, the Foundational "Intelligence Does Not Eliminate Physics" cannot-list, Crown and Morrow access and governance constraints, the no-real-time Earth-to-Mars-conversation rule, and the "neither can absorb the other" rule.
5. **Master Timeline.** Chronology authority. Four Mermaid blocks at lines 69 to 107, 113 to 127, 982 to 1010, and 1796 to 1829 (fence pairing verified). Ambiguities: day-level Book One calendar overlaps the Plot Outline; era label differs from the Story Bible (conflict C2); a Mermaid milestone year (2052) appears to relabel a prose habitability date (Feb 2051) (conflict C5).
6. **Plot Outline and Chapter Map.** Story spine, beats, four acts, **36** chapter plot-map entries (verified contiguous, Chapter 1 through Chapter 36, no gaps or duplicates), subplot map, reveal management. Ambiguity: per-chapter dates restate Master Timeline facts; viewpoint distribution, Drafting Rules, and the Scene Card Template have no native Phase 2 plot destination (orchestrator routes them in the migration map; none is dropped).
7. **Prose and Style Guide.** Full prose-rule canon, carries an in-document YAML status of "active style canon". Ambiguity: per-character voice sections overlap the Character Bible's Dialogue Differentiation and Speech Pattern fields (style-versus-character authority boundary, Phase 12); a few craft sections (Drafting With Another AI, Action and Suspense, Recurring Imagery, Humor, Romance) have no dedicated Phase 2 file and are folded by the migration map.
8. **Creative Decision Log.** **44** numbered decisions (verified 001 through 044 contiguous, no gaps) across 8 category groups, plus a status legend, an entry template, rejected concepts, open decisions, affected-documents list, and update procedure. Ambiguities: Decisions 040 to 044 use a status label ("Locked for Current Workflow") absent from the five-label legend (conflict C6); the "Existing Documents Affected" list references an old folder scheme and a guide filename that differ from the spec tree; the entry-template heading matches the real-decision pattern and must be excluded from the per-decision split so it does not become "001".
9. **Novel Development and Canon Guide.** Operating manual and canon hierarchy. Kept intact as active governance; a shorter `context-loading-guide.md` is derived from it in a later phase. Ambiguity: its "Recommended Project Structure" predates the spec `docs/` tree (master spec wins, later phase updates it).
10. **Chapter Blueprint Template.** Reusable per-chapter scaffold. Relocated intact; the master spec validation requires it remain intact. Ambiguity: it references an "Existing Continuity Ledger" that does not yet exist; expected, since continuity files are created only after chapters are approved (spec Phase 13).
11. **CLAUDE.md.** Root session-entry and project-instructions file plus the mem0 operating protocol. Explicitly non-canon and self-described as the entry/operational layer. Stays at root; updated in place in a later governance phase. Ambiguity: it describes a `canon/ planning/ migration/` tree that differs from the spec `docs/` tree (master spec wins); contains em dashes in its own pre-existing prose (the em-dash ban applies only to new migration prose).
12. **Memory Conventions.md.** mem0 memory-practice spec, explicitly non-canon. Active and in use. Ambiguity: the master spec target tree does not enumerate a slot for it; its destination is an orchestrator decision (see section 10).

## 4. Heading coverage plan

For every document marked **split**, every level-2 source heading (and the deeper headings the spec splits on, namely per-chapter and per-decision entries) maps to a planned destination. No source heading is left unmapped. Documents marked relocate-intact or keep-intact move whole, so every heading travels with the file. The per-section destinations are enumerated in `migration/migration-map.md`; the coverage guarantee per split document is summarized here.

- **Story Bible (1 H1, 38 H2, 64 H3).** Each top-level world section maps to a `docs/20-canon/world/` file (core-premise, central-questions-and-themes, social-structure, infrastructure-decline, protected-enclaves, mars-and-aurelia, locations/* for the five settings, book-1-arc, series-direction, consistency-rules). The condensed character, technology, and historical-timeline sections map to link-only references to their owning authorities (they are not duplicated). The Research Ledger section seeds `docs/70-research/`. All 38 H2 sections are accounted for.
- **Character Bible (22 H1, 233 H2).** Each of the 13 character H1 spans, with all of its H2 fields, maps to `profiles/<slug>.md`. The Relationship Map, Viewpoint Guidance, and Dialogue Differentiation H1 spans map to `relationship-map.md`, `viewpoint-rules.md`, and `dialogue-differentiation.md`. Character Continuity Fields informs `docs/60-continuity/` (Phase 07) and is not lost. Framing sections map to `characters/index.md`. Every H1 span and its H2 fields are covered.
- **World and Technology Rules (31 H1, 113 H2).** Each system H1 block maps to a `docs/20-canon/technology/` file (foundational-rules, ai/{intelligence-levels, consciousness-and-personhood, crown, morrow, crown-vs-morrow}, infrastructure/{energy, communications, cloud-dependency, identity-and-money, community-infrastructure}, robotics-and-manufacturing, transportation, medicine, security-and-conflict, mars-technology, hard-plot-restrictions, failure-rules). World-overlap blocks (Government Technology, Protected Enclaves, Northglass, Information and Propaganda, Scientific Progress, Computing Hardware) are routed in the migration map and cross-linked rather than duplicated. The 10 Hard Plot Restrictions and 5 Failure Rules move verbatim. All 113 H2 sections are accounted for.
- **Master Timeline (30 H1, 63 H2, 113 H3).** Era H1 blocks map to `historical/*` period files; Book One day-by-day act blocks map to `book-1/act-1-timeline` through `act-4-timeline`; pre-book months to `pre-book-2053`; birth-dates table to `character-birth-dates`; the knowledge tables to `character-knowledge-timeline`; the secret table to `secret-timeline`. The index keeps the compact chronology. All four Mermaid blocks are assigned (three to the index, one to the knowledge timeline) and preserved verbatim. Travel rules, continuity rules, and open questions are routed in the migration map. All H1 and H2 sections are accounted for.
- **Plot Outline and Chapter Map (16 H1, 95 H2, 157 H3).** Story Spine, Major Structural Beats, the four Act H1 blocks, Subplot Map, and Reveal Management map to their `docs/30-plot/book-1/` files. Each of the 36 `## Chapter N` H2 entries, with its H3 sub-fields, maps to `chapters/chapter-NN.md`. The single Mermaid (Act Structure) moves with major-beats and is preserved. Viewpoint distribution, Drafting Rules, and Scene Card Template are routed in the migration map. All 95 H2 sections are accounted for; all 36 chapters are represented.
- **Prose and Style Guide (48 H1, 129 H2, 21 H3).** Sections map to the 12 `docs/10-vision/style/` files (index, core-prose, viewpoint, dialogue, character-voices, ai-dialogue, technology-in-prose, emotion-and-moral-content, pacing-and-structure, formatting, prohibited-patterns, revision-checklist). Per-character voice H1 blocks map to character-voices; the 7-pass review and checklist map to revision-checklist; "Drafting With Another AI" is routed in the migration map. All sections are accounted for.
- **Creative Decision Log (17 H1, 63 H2, 245 H3).** Each of the 44 `## Decision NNN` H2 entries maps to `decisions/NNN-slug.md`. The 8 category H1 headings become index groupings and the Category field. The status legend, How-to-Use, rejected concepts, open decisions, affected-documents list, update procedure, and final principle map to the `decision-log/index.md` and adjacent files. The entry template maps to its own template file and is excluded from the per-decision split. All 44 decisions plus all framing sections are accounted for.

## 5. Active versus archive determination

Nothing is archived in Phase 01; archival is deferred to Phase 09. The determinations below inform that later step.

| Document | Determination |
|---|---|
| Narrative Brief | active; relocate-intact, source monolith archived in Phase 09 after the relocated copy is verified |
| Story Bible | active; split, source monolith archived in Phase 09 after sections confirm destinations |
| Character Bible | active; split, archived in Phase 09 |
| World and Technology Rules | active; split, archived in Phase 09 |
| Master Timeline | active; split, archived in Phase 09 |
| Plot Outline and Chapter Map | active; split, archived in Phase 09 |
| Prose and Style Guide | active; split, archived in Phase 09 |
| Creative Decision Log | active; split, archived in Phase 09 |
| Novel Development and Canon Guide | active; relocated whole as active governance, original monolith archived in Phase 09 with the relocated copy as authority |
| Chapter Blueprint Template | active; relocated intact under `_templates/`, NOT archived (it is a live template) |
| CLAUDE.md | active; stays at repository root, updated in place, never archived |
| Memory Conventions.md | active; relocated (destination flagged), original handled like the other relocations |

## 6. Duplicate detection

Ten authoritative-content overlaps were found. All are substantively consistent today; each is a divergence risk if edited in one place only. None is a contradiction; resolution is by linking to a single authority in Phase 12, not by deletion in Phase 01.

| # | Overlapping content | Location A | Location B | Owning authority (target) |
|---|---|---|---|---|
| D1 | Eli Rook age (38) | Story Bible Protagonist (L819); Character Bible Eli Basic Information | Master Timeline Birth Dates (L142) | character profile (age) + timeline (birth date) |
| D2 | Condensed character profiles (Eli, Jonah, Kade, Lena, June, Mara, Morrow) | Story Bible character sections | Character Bible per-character profiles | Character Bible |
| D3 | Condensed technology / Crown / AI summaries | Story Bible Technology and Crown sections | Technology Rules Crown / Morrow / AI levels | Technology Rules |
| D4 | Historical chronology (eras 2026 to 2053) | Story Bible Historical Timeline | Master Timeline era blocks | Master Timeline |
| D5 | Northglass description | Story Bible Main Locations (L761); Technology Rules Northglass (L1388) | Decision Log Decision 007 (L442) | world location file + decision link |
| D6 | Mars seat offer (six total, five additional) | Decision Log Decision 032 (L1515); Master Timeline (L1408) | Plot Outline Ch20 (L1251), Ch21 (L1297) | decision file + timeline |
| D7 | Chapter count (36) and 30-day span | Decision Log Decision 029 (L1402); Plot Outline Chapter Count (L39) | Story Bible and Master Timeline Book One framing | plot files |
| D8 | Viewpoint-character set and distribution | Style Guide Viewpoint Characters (L132 to 144); Plot Outline Primary Viewpoint Distribution | Narrative Brief Narrative Style (L404 to 412) | plot files (see conflict C3) |
| D9 | Per-character voice and speech guidance | Character Bible Dialogue Differentiation and profile Speech Pattern / Writing Rules | Style Guide Character Voice Guide and per-character voice blocks | Phase 12 authority boundary decision |
| D10 | Morrow and Crown identity and personhood | Character Bible Morrow/Crown profiles; Technology Rules Crown / Morrow / Consciousness | Story Bible overviews; Style Guide voice sections | character profile + technology file |

## 7. Conflict detection

Six conflict and inconsistency candidates were found and verified by the orchestrator against the cited source lines. Two are genuine cross-document canon conflicts (C2, C3); the remainder are a specificity gap (C1), a wording-precision divergence (C4), and two intra-document inconsistencies (C5, C6). None was resolved during the Phase 01 audit itself (the audit is read-only). All six are recorded with both statements preserved verbatim in `migration/conflicts-found.md` (IDs C1 through C6). After the audit checkpoint, under explicit user authorization, the orchestrator resolved all six by aligning each outlier document to its authority; the ledger Resolution column records each edit and they live in a separate follow-on commit. Summary of the conflicts as found:

| ID | Severity | Nature | A | B |
|---|---|---|---|---|
| C1 | low | specificity gap (Kade Mars-seat count) | Story Bible L1427 "a limited number of companions" | Decision Log Decision 032 L1508/L1515 "Six Total" / "five additional" |
| C2 | medium | cross-document date-boundary conflict | Story Bible L535 "2038 to 2041: The Replacement Wave" | Master Timeline L397/L399 "Mosaic and the Replacement Wave" / "2039 to 2041" |
| C3 | medium | cross-document viewpoint-roster conflict | Style Guide L132 to L142 lists Sera Vale as a viewpoint character | Narrative Brief L412 omits Sera ("Lena, June, and Mara") |
| C4 | low | wording-precision divergence (Crown age) | Character Bible L1865 "nearly two decades" | Technology Rules L225 "approximately eighteen years" |
| C5 | low | intra-document diagram-versus-prose year | Master Timeline L102 Mermaid "2052 ... habitability trial" | Master Timeline L826 prose "publicly declared habitable" (Feb 2051) |
| C6 | low | intra-document governance-metadata | Decision Log legend L65 to L83 (five labels) | Decisions 040 to 044 L1816 to L2019 "Locked for Current Workflow" (undefined label) |

Consistency cross-checks that passed: the October 3, 2053 opening date and weekday labels, the 36-chapter and 30-day span, and the Mosaic-after-Crown ordering.

## 8. Broken-link detection

Every source was swept for relative Markdown links of every form (inline `](...)`, reference-style, autolink). **Zero** relative Markdown links exist in any of the 12 novel-content and governance documents, so `links_checked_count` is 0 and there are no broken links. Stale path references to an old folder scheme exist as bare text in the Decision Log's "Existing Documents Affected" list and in a few backtick filename mentions; these are not Markdown links and are recorded as later path-reconciliation items, not broken links. Link work in later phases is link creation, not repair.

## 9. Master spec Phase 1 coverage

The master spec Phase 1 "audit should contain" list and the relevant Validation Requirements are satisfied:

- Existing file tree: section 2.
- Document title, current path, apparent version, canon status, approximate subject, recommended destination, split decision: section 3 (table and per-document subjects) and `migration/migration-map.md`.
- Conflicts or ambiguities: sections 3, 6, 7 and the ledger.
- Duplicate, obsolete, partial, superseded versions: no obsolete or superseded versions exist (every monolith is the single Version 1.0 or an unversioned current file); duplicated content is catalogued in section 6.
- Broken links: section 8 (none).
- Repeated information across documents: section 6.
- Sections that can be split safely: section 4 and the migration map.
- Validation-relevant counts confirmed against source: 36 chapter plot-map entries (Chapter 1 to 36 contiguous), 13 character profiles matching the spec slugs, 44 decisions (001 to 044) contiguous, the Chapter Blueprint Template present and intact, 7 Mermaid blocks total.

## 10. Items for human review

- **Memory Conventions.md destination.** The master spec target tree does not enumerate a slot for it. Recommended destination: `docs/00-governance/memory-conventions.md` (an added artifact, like the Phase 03 `README.md`). Alternative: keep it at the repository root next to `CLAUDE.md`. Orchestrator recommendation is the governance folder; please confirm before Phase 02 fixes the tree.
- **The two medium-severity conflicts (C2, C3) were resolved post-audit under user authorization.** C2 (Replacement Wave era start year) was fixed by aligning the Story Bible to the Master Timeline (2039); C3 (Sera Vale viewpoint) was fixed by adding her to the Narrative Brief supporting-viewpoint roster. The four low-severity items (C1, C4, C5, C6) were resolved at the same time. See the ledger Resolution column; no open canon conflict remains from Phase 01.
- **Flagged destination decisions** for sections without a native Phase 2 home (Plot viewpoint distribution, Drafting Rules, Scene Card Template; Style "Drafting With Another AI", Action/Imagery/Humor/Romance; Technology Government/Computing/Scientific-Progress/Information-and-Propaganda; Timeline travel rules, continuity rules, open questions). The migration map records the orchestrator's proposed routing for each; confirm before Phase 04/05 act on them.
- **"Not stated" version and status entries.** Narrative Brief, Chapter Blueprint Template, CLAUDE.md, and Memory Conventions.md carry no version label, and several documents carry no explicit canon-status string. These were recorded as not stated rather than invented; confirm this is acceptable to carry forward, or supply the missing labels.

## 11. Read-only proof

`git status --porcelain` at the end of Phase 01 shows only `migration/audit-notes/` and the two new reports under `migration/` as additions; `git diff` shows zero changes to any tracked file. No monolith, no blueprint, no `archive/`, and no `docs/` path was created or touched. Coordination rules 6 (every source section identified) and 7 (orchestrator verified findings against source, not summaries) were honored.
