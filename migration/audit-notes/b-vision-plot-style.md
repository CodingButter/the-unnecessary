# Audit note: Task B (Vision, Plot, and Style Documents)

Phase 01 repository audit. READ-ONLY. Authority: `migration/REPOSITORY-REORGANIZATION-SPEC.md` (wins all conflicts), operationalized by `migration/plan/01-repository-audit.md`. Destinations below are RECOMMENDED only; the orchestrator decides final paths. No em dashes are used in this note.

Documents audited (three, as assigned):
- `/home/codingbutter/Novel/Narrative Brief.md`
- `/home/codingbutter/Novel/Plot Outline and Chapter Map.md`
- `/home/codingbutter/Novel/Style Guide.md`

Verification performed: a repo grep for Markdown links of the form `[text](target)` across all three files returned NONE. A grep for `^## Chapter [0-9]+:` in the Plot Outline returned exactly 36 contiguous entries (1 through 36, no gaps, no duplicates).

---

## Narrative Brief.md

- Title (as stated in the doc): `Narrative Brief` (H1 line 1). The project title named inside is "The Unnecessary" (under the "Project Title" section).
- Current path: `/home/codingbutter/Novel/Narrative Brief.md`
- Document type: vision / creative-direction brief (highest-level creative direction document for the novel and its sequels).
- Apparent version: not stated. No version label or YAML front matter present in the file.
- Canon status: not stated as an explicit status label (no "active-canon" string). However the document self-describes as the highest authority: under "Canon Priority" it lists itself as #1 of 10 and states "The Narrative Brief controls the intent and identity of the project." Treat as active top-level vision canon; the explicit status string is "not stated".
- Subject (1-2 lines): The highest-level creative direction for the novel. Establishes premise, narrative promise, core conflict, world, enclaves, Mars, key characters (Eli, Jonah, Kade), Morrow, themes, tone, style, storytelling rules, things to avoid, Book One arc, series direction, and the canon priority order.

### FULL heading outline (Narrative Brief.md)

- H1: `Narrative Brief`
  - H2: `Project Title`
  - H2: `Purpose of This Document`
  - H2: `One-Sentence Premise`
  - H2: `Condensed Story Summary`
  - H2: `The Narrative Promise`
  - H2: `Core Narrative Conflict`
  - H2: `The World`
  - H2: `The Protected Enclaves`
  - H2: `Mars`
  - H2: `The Waiting Wealthy`
  - H2: `The Protagonist`
    - H3: `Elias "Eli" Rook`
  - H2: `The Childhood Friend`
    - H3: `Jonah Mercer`
  - H2: `The Primary Human Antagonist`
    - H3: `Adrian Kade`
  - H2: `Morrow`
  - H2: `Major Themes`
    - H3: `Economic Usefulness Versus Human Worth`
    - H3: `Ownership of Abundance`
    - H3: `Complicity`
    - H3: `Neglect as Violence`
    - H3: `Responsibility Without Ownership`
    - H3: `Freedom Versus Protection`
    - H3: `Social Value After Labor`
    - H3: `The Repetition of Abandonment`
  - H2: `Tone and Emotional Experience`
  - H2: `Narrative Style`
  - H2: `Storytelling Rules`
  - H2: `Concepts and Directions to Avoid`
  - H2: `Book One Arc`
  - H2: `Series Direction`
  - H2: `Canon Priority`
  - H2: `Final Creative Standard`

### Recommended destination

- `docs/10-vision/narrative-brief.md` (per master spec Phase 2 tree and Phase 4 "Narrative Brief" guidance: keep mostly intact, it is meant to be short and read first).

### Split decision

- `relocate-intact`.
- Rationale: The spec (Phase 4) explicitly says keep the Narrative Brief mostly intact and do not split unnecessarily because it is short and read first. The whole file maps to a single destination file `docs/10-vision/narrative-brief.md`. No clean internal seam justifies a split, and the document's value is its single-read orientation function. No proposed heading boundaries (no split).
- Note for orchestrator (do not act in this phase): Several Narrative Brief sections overlap in subject with canon authorities (themes overlap Story Bible "central questions and themes"; character sketches overlap Character Bible; storytelling/technology rules overlap Technology Rules; Book One Arc and Series Direction overlap Story Bible and Plot Outline; Narrative Style overlaps Style Guide). The spec's Phase 12 "Avoid Canon Duplication" rule would have these remain summaries in the vision doc that link to the subject authorities. This is a duplication-management concern for later phases, not a reason to split the brief now.

### Internal relative Markdown links found

- None. (Grep for `[text](target)` returned nothing in this file.) The "Canon Priority" section names other documents in prose (Story Bible, Character Bible, etc.) but uses no Markdown link syntax.

### Active-or-archive determination

- `relocate-intact` and active. Reason: this is the live top-level vision/creative-direction document; the spec keeps it as an active first-read file at `docs/10-vision/narrative-brief.md`. It is not a monolith to be split, so the "archive-after-split" path does not apply. The original would be relocated/copied per later-phase mechanics, but Phase 01 moves nothing.

### Conflicts / ambiguities observed (recorded, not resolved)

- Document-naming mismatch (record only): The Narrative Brief "Canon Priority" list names item 4 as "World and Technology Rules" and includes a "Continuity Ledger" (items 7) and "Research and Plausibility Ledger" (item 9). The repository's actual file is `Technology Rules.md` (no "World and" prefix), and there is no `Continuity Ledger.md` or `Research and Plausibility Ledger.md` present in the root scan. This is a naming/inventory ambiguity to flag for the orchestrator; it is not resolved here.
- Canon-priority ordering vs. project CLAUDE.md (record only): The Narrative Brief's "Canon Priority" lists Plot Outline (#5) above Master Timeline (#6) and Style Guide (#8). The project `CLAUDE.md` authority table and `Development and Canon Guide.md` may state the hierarchy differently. Cross-document hierarchy reconciliation is a Task F / orchestrator concern; recorded here as an ambiguity only.
- No explicit version or status label anywhere in the file (unlike the Plot Outline and Style Guide, which both carry "Version 1.0"). Recorded as "not stated" rather than inferred.

---

## Plot Outline and Chapter Map.md

- Title (as stated in the doc): H1 `The Unnecessary`; immediately followed by H2 `Plot Outline and Chapter Map, Version 1.0`. The working document title is "Plot Outline and Chapter Map".
- Current path: `/home/codingbutter/Novel/Plot Outline and Chapter Map.md`
- Document type: plot outline and chapter map (Book One narrative structure: act structure, chapter-by-chapter map, subplot map, reveal management, drafting rules, scene-card template).
- Apparent version: `Version 1.0` (stated in the H2 line "Plot Outline and Chapter Map, Version 1.0").
- Canon status: not stated as an explicit status string. It is planning material (the spec routes it to `30-plot/`, treated as approved plans rather than already-established events). The document itself says "the major movement of the novel should remain consistent with this outline unless deliberately revised." Treat as active plot-plan canon; explicit status label is "not stated".
- Subject (1-2 lines): Converts Story Bible, Character Bible, Technology Rules, and Master Timeline into a complete narrative structure for Book One. Defines act structure, the order of events, the viewpoint and dramatic purpose of every chapter, subplot setup/payoff, reveal timing, and chapter ending hooks. Contains all 36 chapter plot-map entries.

### FULL heading outline (Plot Outline and Chapter Map.md)

Note on structure: this document uses BOTH H1 (`#`) and H2 (`##`) at the top level. Act headers and several structural sections are H1; the individual chapter entries are H2 nested conceptually under their act's H1. Sub-fields inside each chapter entry are H3. Below, every H1 and H2 is listed; H3 sub-fields are listed once for a representative chapter and then summarized because they repeat per chapter (the spec splits the Plot Outline per chapter, so the per-chapter H3 pattern is load-bearing and recorded explicitly).

- H1: `The Unnecessary`
  - H2: `Plot Outline and Chapter Map, Version 1.0`
  - H2: `Purpose of This Document`
- H1: `Book Information`
  - H2: `Working Title`
  - H2: `Planned Length`
  - H2: `Chapter Count`
  - H2: `Average Chapter Length`
  - H2: `Story Duration`
  - H2: `Narrative Perspective`
  - H2: `Primary Viewpoint Distribution` (contains the viewpoint-distribution table: Eli 15, Lena 5, Jonah 5, June 4, Kade 3, Sera 2, Mara 2; plus note that Morrow/Crown have no internal viewpoints and Talia/Nolan/Celeste/Nora have no viewpoint chapters in Book One)
- H1: `Structural Decision`
- H1: `Story Spine`
- H1: `Major Structural Beats`
  - H2: `Opening Image`
  - H2: `Inciting Incident`
  - H2: `Commitment to the Story`
  - H2: `First Major Turn`
  - H2: `First Pressure Point`
  - H2: `Midpoint`
  - H2: `Second Major Turn`
  - H2: `Second Pressure Point`
  - H2: `Crisis`
  - H2: `Climax`
  - H2: `Resolution`
  - H2: `Final Image`
- H1: `Act Structure` (contains a Mermaid `flowchart LR` block, lines 203-220)
- H1: `Act One: Service Terminated`
  - H2: `Chapters 1 through 8`
  - H2: `Dates`
  - H2: `Function of the Act`
  - H2: `Act One Emotional Movement`
  - H2: `Chapter 1: No Signal` (H3 sub-fields: `Purpose`, `Chapter Movement`, `Character Movement`, `Information Revealed`, `Ending Hook`)
  - H2: `Chapter 2: The Last Supported Day` (H3: `Purpose`, `Chapter Movement`, `Character Movement`, `Information Revealed`, `Ending Hook`)
  - H2: `Chapter 3: Priority Tier` (H3 same pattern)
  - H2: `Chapter 4: Northglass` (H3 same pattern)
  - H2: `Chapter 5: MOR-0` (H3 same pattern)
  - H2: `Chapter 6: Terms of Access` (H3 same pattern)
  - H2: `Chapter 7: Blackout` (H3 same pattern)
  - H2: `Chapter 8: The Empty City` (H3 same pattern)
- H1: `Act Two: A Version of Normal`
  - H2: `Chapters 9 through 18`
  - H2: `Dates`
  - H2: `Function of the Act`
  - H2: `Act Two Emotional Movement`
  - H2: `Chapter 9: One Full Day` (H3 sub-fields vary per chapter: most use `Purpose`, `Chapter Movement`, `Character Movement`, `Ending Hook`; some add `Information Revealed`; Ch 17 adds `Midpoint Revelation`)
  - H2: `Chapter 10: Local Service`
  - H2: `Chapter 11: Who Decides`
  - H2: `Chapter 12: Clear Water`
  - H2: `Chapter 13: The Visitor`
  - H2: `Chapter 14: A Name`
  - H2: `Chapter 15: Cargo`
  - H2: `Chapter 16: Choices`
  - H2: `Chapter 17: The Shape of a Lie` (adds H3 `Midpoint Revelation`)
  - H2: `Chapter 18: Consideration`
- H1: `Act Three: The Invitation`
  - H2: `Chapters 19 through 28`
  - H2: `Dates`
  - H2: `Function of the Act`
  - H2: `Act Three Emotional Movement`
  - H2: `Chapter 19: Recognition`
  - H2: `Chapter 20: Six Seats`
  - H2: `Chapter 21: The List`
  - H2: `Chapter 22: No One Man`
  - H2: `Chapter 23: Property`
  - H2: `Chapter 24: Unauthorized Intelligence`
  - H2: `Chapter 25: The Copy`
  - H2: `Chapter 26: No Invitation`
  - H2: `Chapter 27: Survival Is a Requirement`
  - H2: `Chapter 28: Emergency Order`
- H1: `Act Four: Containment`
  - H2: `Chapters 29 through 36`
  - H2: `Dates`
  - H2: `Function of the Act`
  - H2: `Act Four Emotional Movement`
  - H2: `Chapter 29: Terms of Shutdown`
  - H2: `Chapter 30: The Family Decision`
  - H2: `Chapter 31: Harm Without Permission`
  - H2: `Chapter 32: Conditional Access`
  - H2: `Chapter 33: The Other Threat` (adds H3 `Information Revealed`)
  - H2: `Chapter 34: Open Circuit`
  - H2: `Chapter 35: The Right to End` (uses H3 `Apparent Resolution` in place of/alongside the usual sub-fields)
  - H2: `Chapter 36: After Midnight` (uses H3 `Final Line`)
- H1: `Subplot Map`
  - H2: `Jonah and the Mercer Family` (table)
  - H2: `Mara and the Excluded Wealthy` (table)
  - H2: `Lena and the Clinic` (table)
  - H2: `June and Her Father` (table)
  - H2: `Nolan and the Loss of Human Knowledge` (table)
  - H2: `Talia and Community Governance` (table)
  - H2: `Kade and Crown` (table)
  - H2: `Morrow's Personhood` (table)
- H1: `Reveal Management`
  - H2: `Reveals That Occur in Book One`
  - H2: `Revelations Reserved for Later Books`
- H1: `Chapter Tension Pattern`
  - H2: `Act One Tension`
  - H2: `Act Two Tension`
  - H2: `Act Three Tension`
  - H2: `Act Four Tension`
- H1: `Drafting Rules for Chapters`
- H1: `Scene Card Template`
  - H2: `Scene Identification`
  - H2: `Scene Purpose`
  - H2: `Character Goal`
  - H2: `Opposition`
  - H2: `Information State`
  - H2: `Turn`
  - H2: `Ending Condition`
  - H2: `Continuity Impact`
- H1: `Final Structural Standard`

Per-chapter H3 sub-field inventory (the repeating pattern the spec relies on when splitting one concise file per chapter): the common sub-fields are `Purpose`, `Chapter Movement`, `Character Movement`, `Information Revealed` (present in some chapters, absent in others), and `Ending Hook`. Variations: Ch 17 adds `Midpoint Revelation`; Ch 33 includes `Information Revealed`; Ch 35 uses `Apparent Resolution`; Ch 36 uses `Final Line` instead of `Ending Hook`. Each chapter also carries inline bold metadata lines (Date, Viewpoint, Primary setting) immediately under its H2, not as headings.

### CRITICAL chapter-entry count (spec validation requirement)

- Total chapter plot-map entries: EXACTLY 36.
- Numbering: 1 through 36, contiguous, no gaps, no duplicates, in order.
- Verified by `grep -cE '^## Chapter [0-9]+:'` returning 36 and the full enumerated list of `## Chapter N:` headings (chapters 1-8 in Act One, 9-18 in Act Two, 19-28 in Act Three, 29-36 in Act Four).
- Chapter titles, viewpoints, and dates (for the per-chapter split mapping):
  - Ch 1 "No Signal" / Eli / Fri Oct 3
  - Ch 2 "The Last Supported Day" / Lena / Fri Oct 3
  - Ch 3 "Priority Tier" / Eli / Sat Oct 4
  - Ch 4 "Northglass" / June / Sun Oct 5
  - Ch 5 "MOR-0" / Eli / Mon Oct 6
  - Ch 6 "Terms of Access" / Eli / Tue Oct 7
  - Ch 7 "Blackout" / Eli / Wed Oct 8
  - Ch 8 "The Empty City" / Kade / Wed night Oct 8
  - Ch 9 "One Full Day" / Eli / Thu Oct 9
  - Ch 10 "Local Service" / June / Fri Oct 10
  - Ch 11 "Who Decides" / Eli / Sat Oct 11
  - Ch 12 "Clear Water" / Lena / Sun Oct 12
  - Ch 13 "The Visitor" / Jonah / Mon Oct 13
  - Ch 14 "A Name" / June / Tue Oct 14
  - Ch 15 "Cargo" / Eli / Wed Oct 15
  - Ch 16 "Choices" / Lena / Thu Oct 16
  - Ch 17 "The Shape of a Lie" / Eli / Fri Oct 17 (midpoint)
  - Ch 18 "Consideration" / Jonah / Sat-Sun Oct 18-19
  - Ch 19 "Recognition" / Kade / Mon Oct 20
  - Ch 20 "Six Seats" / Eli / Tue Oct 21
  - Ch 21 "The List" / Jonah / Tue night Oct 21
  - Ch 22 "No One Man" / Eli / Wed Oct 22
  - Ch 23 "Property" / Sera / Thu Oct 23
  - Ch 24 "Unauthorized Intelligence" / Mara / Fri Oct 24
  - Ch 25 "The Copy" / June / Sat Oct 25
  - Ch 26 "No Invitation" / Mara / Sat night Oct 25
  - Ch 27 "Survival Is a Requirement" / Eli / Sun Oct 26
  - Ch 28 "Emergency Order" / Sera / Mon Oct 27
  - Ch 29 "Terms of Shutdown" / Eli / Tue Oct 28
  - Ch 30 "The Family Decision" / Jonah / Tue night Oct 28
  - Ch 31 "Harm Without Permission" / Lena / Wed Oct 29
  - Ch 32 "Conditional Access" / Jonah / Thu Oct 30
  - Ch 33 "The Other Threat" / Kade / Thu night Oct 30
  - Ch 34 "Open Circuit" / Eli / Fri Oct 31 (morning/afternoon)
  - Ch 35 "The Right to End" / Eli / Fri Oct 31 (evening-midnight)
  - Ch 36 "After Midnight" / Lena / Sat Nov 1

### Recommended destination(s) and split mapping

- `split` into `docs/30-plot/book-1/` per master spec Phase 2 tree and Phase 4 "Plot Outline and Chapter Map" guidance.
- Proposed heading-range to destination mapping (recommended only; orchestrator decides final boundaries):
  - `docs/30-plot/book-1/index.md`: H1 `The Unnecessary` + H2 `Plot Outline and Chapter Map, Version 1.0` + H2 `Purpose of This Document` + H1 `Book Information` (Working Title, Planned Length, Chapter Count, Average Chapter Length, Story Duration, Narrative Perspective) + H1 `Final Structural Standard` (closing framing). The index summarizes and links to authority files.
  - `docs/30-plot/book-1/story-spine.md`: H1 `Story Spine` + H1 `Structural Decision` (opening/closing mirror image).
  - `docs/30-plot/book-1/major-beats.md`: H1 `Major Structural Beats` (all twelve H2 beats: Opening Image through Final Image) + H1 `Act Structure` (including the Mermaid `flowchart LR` block, which must be preserved verbatim) + H1 `Chapter Tension Pattern` (the four act-tension H2s).
  - `docs/30-plot/book-1/act-1.md`: H1 `Act One: Service Terminated` and its H2 metadata blocks (`Chapters 1 through 8`, `Dates`, `Function of the Act`, `Act One Emotional Movement`). Note: the act file holds the act-level framing; the per-chapter entries go to the chapters/ files.
  - `docs/30-plot/book-1/act-2.md`: H1 `Act Two: A Version of Normal` and its act-level H2 metadata blocks.
  - `docs/30-plot/book-1/act-3.md`: H1 `Act Three: The Invitation` and its act-level H2 metadata blocks.
  - `docs/30-plot/book-1/act-4.md`: H1 `Act Four: Containment` and its act-level H2 metadata blocks.
  - `docs/30-plot/book-1/chapters/chapter-01.md` ... `chapter-36.md`: one concise file per chapter from each `## Chapter N: Title` H2 plus its inline Date/Viewpoint/Primary-setting lines and its H3 sub-fields (`Purpose`, `Chapter Movement`, `Character Movement`, `Information Revealed` where present, `Ending Hook`/`Final Line`, plus chapter-specific extras such as Ch 17 `Midpoint Revelation`, Ch 35 `Apparent Resolution`, Ch 36 `Final Line`). These are the concise plot-map entries and must remain distinct from full chapter blueprints (spec: "Chapter plot-map files must remain different from full chapter blueprints").
  - `docs/30-plot/book-1/chapters/index.md`: a chapters index table (new index file the orchestrator/later phase creates; sourced from the chapter list above).
  - `docs/30-plot/book-1/subplot-map.md`: H1 `Subplot Map` (all eight subplot H2 tables, preserved as tables).
  - `docs/30-plot/book-1/reveal-management.md`: H1 `Reveal Management` (both H2s: Reveals in Book One, Revelations Reserved for Later Books).
  - Viewpoint distribution: H2 `Primary Viewpoint Distribution` (the viewpoint table) maps to a viewpoint-distribution destination. The master spec Phase 2 plot tree does not list a dedicated `viewpoint-distribution.md` under `30-plot/`, while spec Phase 4 says "Viewpoint distribution if not stored elsewhere". RECOMMENDED: place the viewpoint-distribution table in `docs/30-plot/book-1/index.md` (or a `viewpoint-distribution.md` sibling if the orchestrator prefers a standalone file), and cross-reference `docs/20-canon/characters/viewpoint-rules.md` which owns viewpoint rules. Flagged below as an ambiguity for orchestrator decision.
  - `Drafting Rules for Chapters` (H1) and `Scene Card Template` (H1, with its eight H2 sub-sections): these are process/drafting-craft content, not plot-map content. RECOMMENDED destinations: `Drafting Rules for Chapters` could live in the plot index or in governance/style; `Scene Card Template` is a reusable template and fits the blueprint-template area (`docs/40-blueprints/_templates/` neighborhood) OR a plot index appendix. Flagged below as an ambiguity; orchestrator decides. No heading is dropped.
- Coordination-rule-6 assurance: every H1 and every H2 above has a proposed destination; no source heading is left unmapped.

### Internal relative Markdown links found

- None. Grep for `[text](target)` returned nothing. The document references Story Bible, Character Bible, Technology Rules, Master Timeline, and a Continuity Ledger in prose only, with no link syntax. It contains one Mermaid block and many Markdown tables (no links inside them).

### Active-or-archive determination

- `archive-after-split` (and active until split). Reason: this is a monolith the spec splits across `docs/30-plot/book-1/`. Per spec Phase 11, after all sections have confirmed destinations and the split is verified, the original moves to `archive/source-monoliths/`. Phase 01 archives nothing; the determination only informs Phase 09. The split files become the active authority.

### Conflicts / ambiguities observed (recorded, not resolved)

- Viewpoint-distribution destination ambiguity: spec Phase 4 says split out "Viewpoint distribution if not stored elsewhere," but the master spec Phase 2 `30-plot/` tree lists no `viewpoint-distribution.md`, and a separate `docs/20-canon/characters/viewpoint-rules.md` exists. Whether the per-chapter viewpoint counts table belongs in the plot index, a standalone plot file, or is folded into character viewpoint-rules is an orchestrator call. Recorded, not resolved.
- `Drafting Rules for Chapters` and `Scene Card Template` placement ambiguity: these are craft/process sections inside a plot document; the spec's per-document split guidance for the Plot Outline does not assign them an explicit destination. They must not be lost (coordination rule 6). Orchestrator should decide whether they go to the plot index, governance, style, or the blueprints/templates area. Recorded, not resolved.
- Potential cross-document overlap (duplication, not conflict): the chapter-by-chapter Dates duplicate date facts owned by `Master Timeline.md` (spec Phase 4 Master Timeline guidance: "Do not duplicate detailed chapter summaries from the plot files"). The viewpoint table overlaps `Style Guide.md` "Viewpoint Characters" and the Narrative Brief "Narrative Style". These are Phase 12 duplication-management concerns for the orchestrator; recorded here, not resolved. (Note one apparent surface difference to verify in Task F: the Style Guide "Viewpoint Characters" list includes Mara and Sera and seven names; the Plot Outline viewpoint table assigns chapter counts to seven characters including Mara and Sera. Consistent on membership; the question is only where the authority lives.)
- "Version 1.0" is stated; no explicit canon-status string. Recorded as such.

---

## Style Guide.md

- Title (as stated in the doc): H1 `The Unnecessary`; immediately followed by H2 `Prose and Style Guide, Version 1.0`. The working document title is "Prose and Style Guide" (and the YAML `document` field confirms "Prose and Style Guide").
- Current path: `/home/codingbutter/Novel/Style Guide.md`
- Document type: prose and style guide (voice, viewpoint, dialogue, character voices, AI dialogue, exposition, emotion, pacing, formatting, prohibited patterns, revision process and checklist).
- Apparent version: `Version 1.0` (stated in H2 line and in YAML `version: "1.0"`).
- Canon status: STATED. YAML front matter (lines 5-16) gives `status: "active style canon"`, `last_updated: "2026-06-24"`, `project: "The Unnecessary"`, and `applies_to: [chapter blueprints, manuscript chapters, interludes, revision passes]`. This is the only of the three Task B documents with an explicit machine-readable status and front matter.
- Subject (1-2 lines): Defines how The Unnecessary should sound and feel on the page: narrative voice, viewpoint, tense, distance, sentence rhythm, dialogue, internal thought, emotional expression, technical exposition, worldbuilding, action/violence, suspense, chapter openings/endings, per-character language, Morrow and Crown AI dialogue, formatting, and stylistic habits/cliches to avoid, plus a multi-pass review process and an approval checklist.

### FULL heading outline (Style Guide.md)

Note: this document also mixes H1 and H2 at the top level. The opening title block and "Purpose" sit under the first H1; then most major sections are H1 with H2 (and some H3) subsections. Every H1 and H2 is listed; H3 entries are included where the spec splits deeper (per-character and per-pass detail is load-bearing for the split).

- H1: `The Unnecessary`
  - H2: `Prose and Style Guide, Version 1.0` (followed by a YAML code block carrying document/version/status/applies_to)
  - H2: `Purpose of This Document`
- H1: `Core Prose Identity`
- H1: `Central Stylistic Principle`
  - H2: `Show the Withdrawal Through What Stops Working`
- H1: `Narrative Perspective`
  - H2: `Person`
  - H2: `Tense`
  - H2: `Viewpoint Style`
  - H2: `Viewpoint Characters`
  - H2: `One Viewpoint Per Chapter`
  - H2: `No Omniscient Leakage`
- H1: `Narrative Distance`
  - H2: `Default Distance`
  - H2: `Move Closer During`
  - H2: `Move Slightly Farther During`
  - H2: `Avoid Camera-Only Prose`
- H1: `Free Indirect Style`
- H1: `Internal Thought`
  - H2: `Default Method`
  - H2: `Questions in Internal Thought`
- H1: `Sentence Style`
  - H2: `General Rhythm`
  - H2: `Paragraph Length`
  - H2: `Fragments`
- H1: `Punctuation`
  - H2: `Em Dashes`
  - H2: `Semicolons`
  - H2: `Colons`
  - H2: `Ellipses`
  - H2: `Exclamation Marks`
- H1: `Diction`
  - H2: `Preferred Language`
  - H2: `Avoid Artificially Futuristic Vocabulary`
  - H2: `Avoid Excessive Corporate Coinages`
  - H2: `Avoid Generic Dystopian Vocabulary`
- H1: `Description`
  - H2: `Description Must Serve Viewpoint`
    - H3: `Eli Notices`
    - H3: `Lena Notices`
    - H3: `Jonah Notices`
    - H3: `June Notices`
    - H3: `Kade Notices`
    - H3: `Mara Notices`
    - H3: `Sera Notices`
  - H2: `Selective Description`
  - H2: `Familiar Before Futuristic`
  - H2: `Avoid Decorative Catalogues`
- H1: `Environmental Tone`
- H1: `Technology in Prose`
  - H2: `Explain Through Need`
  - H2: `Three-Layer Technical Rule`
    - H3: `1. Human Consequence`
    - H3: `2. Physical Cause`
    - H3: `3. Limitation`
  - H2: `Avoid Lecture Dialogue`
  - H2: `Use Disagreement to Explain`
  - H2: `No Magical Interfaces`
- H1: `Artificial Intelligence Dialogue`
- H1: `Morrow`
  - H2: `General Voice`
  - H2: `Early Morrow`
  - H2: `Developing Morrow`
  - H2: `Emotional Claims`
  - H2: `Questions`
  - H2: `Humor`
- H1: `Crown`
  - H2: `General Voice`
  - H2: `With Kade`
  - H2: `With the Public`
  - H2: `With Engineers`
  - H2: `With Morrow`
- H1: `Dialogue`
  - H2: `General Rule`
  - H2: `Subtext`
  - H2: `Avoid Perfect Speeches`
  - H2: `Dialogue Tags`
  - H2: `Adverbs`
  - H2: `Names in Dialogue`
- H1: `Character Voice Guide`
- H1: `Eli Rook`
  - H2: `Dialogue`
  - H2: `Internal Narration`
  - H2: `Avoid`
- H1: `Jonah Mercer`
  - H2: `Dialogue`
  - H2: `Internal Narration`
  - H2: `Avoid`
- H1: `Adrian Kade`
  - H2: `Dialogue`
  - H2: `Internal Narration`
  - H2: `Avoid`
- H1: `Lena Okafor`
  - H2: `Dialogue`
  - H2: `Internal Narration`
  - H2: `Avoid`
- H1: `June Park`
  - H2: `Dialogue`
  - H2: `Internal Narration`
  - H2: `Avoid`
- H1: `Mara Voss`
  - H2: `Dialogue`
  - H2: `Internal Narration`
  - H2: `Avoid`
- H1: `Sera Vale`
  - H2: `Dialogue`
  - H2: `Internal Narration`
  - H2: `Avoid`
- H1: `Talia Reed`
  - H2: `Dialogue`
  - H2: `Internal Presence`
  - H2: `Avoid`
- H1: `Nolan Avery`
  - H2: `Dialogue`
  - H2: `Avoid`
- H1: `Emotional Writing`
  - H2: `Restraint`
  - H2: `Physical Signals`
  - H2: `Tears`
  - H2: `Trauma`
- H1: `Moral and Philosophical Content`
  - H2: `Dramatize Before Explaining`
  - H2: `Avoid Authorial Verdicts`
  - H2: `No Debate-Club Dialogue`
- H1: `Worldbuilding Exposition`
  - H2: `The Reader Does Not Need Everything Immediately`
  - H2: `Historical Context`
  - H2: `Official Language`
- H1: `Action and Suspense`
  - H2: `Action Must Remain Legible`
  - H2: `Technical Action`
  - H2: `Violence`
  - H2: `Autonomous Security`
- H1: `Pacing`
  - H2: `Overall Novel Rhythm`
    - H3: `Act One`
    - H3: `Act Two`
    - H3: `Act Three`
    - H3: `Act Four`
  - H2: `Within Chapters`
- H1: `Chapter Openings`
  - H2: `Opening Principle`
- H1: `Chapter Endings`
- H1: `Scene Transitions`
- H1: `Recurring Imagery`
  - H2: `Supported Motifs`
    - H3: `Dead and Returning Lights`
    - H3: `Machines Waiting for Permission`
    - H3: `Authentication Messages`
    - H3: `Heat`
    - H3: `Empty Infrastructure`
    - H3: `Construction Lights on Mars`
    - H3: `Boundaries of Maintenance`
  - H2: `Use With Restraint`
- H1: `Humor`
- H1: `Romance and Intimacy`
- H1: `Profanity`
- H1: `Names and Terminology`
  - H2: `Artificial Intelligence`
  - H2: `Organizations and Locations`
  - H2: `Population Language`
  - H2: `Mars`
- H1: `Formatting Conventions`
  - H2: `Chapter Headings`
  - H2: `Dates and Locations`
  - H2: `Numbers`
  - H2: `Time`
  - H2: `Italics`
  - H2: `Interface Text`
- H1: `Prose Habits to Avoid`
  - H2: `Generic AI-Writing Patterns`
  - H2: `Excessive Binary Contrasts`
  - H2: `Repetitive Threes`
  - H2: `Empty Intensifiers`
  - H2: `Emotional Explanation After Strong Dialogue`
  - H2: `Overuse of "Seemed"`
  - H2: `Overuse of Character Names`
  - H2: `Excessive Backstory`
- H1: `Cliches to Avoid`
  - H2: `Science Fiction Cliches`
  - H2: `Dystopian Cliches`
  - H2: `Character Cliches`
- H1: `Drafting With Another AI`
  - H2: `AI Drafting Instruction`
  - H2: `AI Creativity Boundary`
- H1: `Style Review Process`
  - H2: `Pass 1: Viewpoint`
  - H2: `Pass 2: Character Voice`
  - H2: `Pass 3: Exposition`
  - H2: `Pass 4: Prose Rhythm`
  - H2: `Pass 5: Emotional Restraint`
  - H2: `Pass 6: World Consistency`
  - H2: `Pass 7: AI-Sounding Language`
- H1: `Chapter Style Checklist`
- H1: `Final Style Standard`

### Recommended destination(s) and split mapping

- `split` into `docs/10-vision/style/` per master spec Phase 2 tree and Phase 4 "Style Guide" guidance.
- The Phase 2 tree lists these style destinations: `index.md`, `core-prose.md`, `viewpoint.md`, `dialogue.md`, `character-voices.md`, `ai-dialogue.md`, `technology-in-prose.md`, `emotion-and-moral-content.md`, `pacing-and-structure.md`, `formatting.md`, `prohibited-patterns.md`, `revision-checklist.md`. Proposed source-section to destination mapping (recommended only):
  - `docs/10-vision/style/index.md`: H1 `The Unnecessary` + H2 `Prose and Style Guide, Version 1.0` (with the YAML block) + H2 `Purpose of This Document` + H1 `Final Style Standard` (closing standard). Index summarizes and links to the split files.
  - `docs/10-vision/style/core-prose.md`: H1 `Core Prose Identity` + H1 `Central Stylistic Principle` (Show the Withdrawal Through What Stops Working) + H1 `Sentence Style` + H1 `Punctuation` (including Em Dashes) + H1 `Diction` + H1 `Description` (with the seven per-character "X Notices" H3s) + H1 `Environmental Tone` + H1 `Free Indirect Style` + H1 `Internal Thought`. (Core prose-craft cluster.)
  - `docs/10-vision/style/viewpoint.md`: H1 `Narrative Perspective` (Person, Tense, Viewpoint Style, Viewpoint Characters, One Viewpoint Per Chapter, No Omniscient Leakage) + H1 `Narrative Distance` (Default Distance, Move Closer/Farther, Avoid Camera-Only Prose). This is the "Point of view and narrative distance" file from spec Phase 4.
  - `docs/10-vision/style/dialogue.md`: H1 `Dialogue` (General Rule, Subtext, Avoid Perfect Speeches, Dialogue Tags, Adverbs, Names in Dialogue).
  - `docs/10-vision/style/character-voices.md`: H1 `Character Voice Guide` + the per-character H1 blocks `Eli Rook`, `Jonah Mercer`, `Adrian Kade`, `Lena Okafor`, `June Park`, `Mara Voss`, `Sera Vale`, `Talia Reed`, `Nolan Avery` (each with their Dialogue / Internal Narration (or Internal Presence) / Avoid H2s).
  - `docs/10-vision/style/ai-dialogue.md`: H1 `Artificial Intelligence Dialogue` + H1 `Morrow` + H1 `Crown` (the Morrow/Crown voice sections). This is the "Morrow and Crown dialogue" file.
  - `docs/10-vision/style/technology-in-prose.md`: H1 `Technology in Prose` (Explain Through Need, Three-Layer Technical Rule with its three H3s, Avoid Lecture Dialogue, Use Disagreement to Explain, No Magical Interfaces) + H1 `Worldbuilding Exposition` (Reader Does Not Need Everything, Historical Context, Official Language). This is "Technology and exposition".
  - `docs/10-vision/style/emotion-and-moral-content.md`: H1 `Emotional Writing` (Restraint, Physical Signals, Tears, Trauma) + H1 `Moral and Philosophical Content` (Dramatize Before Explaining, Avoid Authorial Verdicts, No Debate-Club Dialogue). This is "Emotion and moral content".
  - `docs/10-vision/style/pacing-and-structure.md`: H1 `Pacing` (Overall Novel Rhythm with four act H3s, Within Chapters) + H1 `Chapter Openings` (with Opening Principle) + H1 `Chapter Endings` + H1 `Scene Transitions` + H1 `Action and Suspense` (Action Must Remain Legible, Technical Action, Violence, Autonomous Security) + H1 `Recurring Imagery` (Supported Motifs with seven H3s, Use With Restraint) + H1 `Humor` + H1 `Romance and Intimacy`. This is "Pacing, openings, and endings" (broadened to hold the structure/suspense/imagery craft sections so no heading is orphaned). Orchestrator may prefer to route `Action and Suspense`, `Recurring Imagery`, `Humor`, and `Romance and Intimacy` to core-prose instead; flagged below.
  - `docs/10-vision/style/formatting.md`: H1 `Formatting Conventions` (Chapter Headings, Dates and Locations, Numbers, Time, Italics, Interface Text) + H1 `Names and Terminology` (Artificial Intelligence, Organizations and Locations, Population Language, Mars) + H1 `Profanity`. This is the "Formatting" file (with naming/terminology and profanity conventions folded in; orchestrator may split naming out).
  - `docs/10-vision/style/prohibited-patterns.md`: H1 `Prose Habits to Avoid` (all eight H2s) + H1 `Cliches to Avoid` (Science Fiction / Dystopian / Character cliches). This is "Prohibited patterns and cliches".
  - `docs/10-vision/style/revision-checklist.md`: H1 `Style Review Process` (Passes 1 through 7) + H1 `Chapter Style Checklist`. This is the "Revision checklist" file.
  - `Drafting With Another AI` (H1, with AI Drafting Instruction and AI Creativity Boundary): this is process guidance for delegating prose drafting. The Phase 2 style tree has no dedicated destination. RECOMMENDED: place in the style index or in `docs/00-governance/` (context-loading/process). Flagged below as an ambiguity. No heading dropped.
- Coordination-rule-6 assurance: every H1 and every H2 in the outline above has a proposed destination; the only sections needing an orchestrator decision are noted in the ambiguities list. No heading is left unmapped.

### Internal relative Markdown links found

- None. Grep for `[text](target)` returned nothing. The Purpose section names other documents (Narrative Brief, Story Bible, Character Bible, Technology Rules) in prose without link syntax. The file contains fenced code blocks (the YAML metadata block, a markdown chapter-heading example, and a `text` scene-break example) but no Markdown links.

### Active-or-archive determination

- `archive-after-split` (and active until split). Reason: a monolith the spec splits across `docs/10-vision/style/`. Per spec Phase 11, after all sections have confirmed destinations and the split is verified, the original moves to `archive/source-monoliths/`. Phase 01 archives nothing. The split style files become the active style authority.

### Conflicts / ambiguities observed (recorded, not resolved)

- `Drafting With Another AI` destination ambiguity: it is delegation/process guidance, not a prose-style category in the Phase 2 style tree. Orchestrator decides whether it lives in the style index, governance, or a context-loading guide. Recorded, not resolved.
- "Pacing-and-structure overflow" ambiguity: the Phase 2 style tree lists `pacing-and-structure.md` but the Style Guide also contains `Action and Suspense`, `Recurring Imagery`, `Humor`, and `Romance and Intimacy`, which have no dedicated Phase 2 destination. RECOMMENDED grouping them under `pacing-and-structure.md` (or `core-prose.md`); orchestrator decides. Recorded, not resolved.
- `Names and Terminology` and `Profanity` placement: folded into `formatting.md` in the recommendation, but they could equally be standalone or join `core-prose.md` / `prohibited-patterns.md`. The naming list (Crown, Morrow, Mosaic, Asterion, Northglass, Lakeward, Aurelia Initiative) overlaps the Narrative Brief and canon authorities; Phase 12 duplication concern. Recorded, not resolved.
- Cross-document overlap (duplication, not conflict): the Style Guide "Viewpoint Characters" list and the per-character voice sections overlap the Character Bible (character voice/speech patterns) and the Plot Outline (viewpoint distribution). Spec Phase 12 says prose rules belong in style files and character facts belong in profiles; the orchestrator must decide where voice/speech-pattern authority lives (style character-voices.md vs character profiles' "speech pattern" / "writing rules" fields). Recorded for Task F / orchestrator, not resolved.
- Surface detail to verify in Task F (record only, do not resolve): Style Guide "Viewpoint Characters" lists seven names (Eli, Jonah, Kade, Lena, June, Mara, Sera) and the Plot Outline viewpoint table lists the same seven with chapter counts. The Narrative Brief "Narrative Style" instead says supporting viewpoints "may include Lena Okafor, June Park, and Mara Voss" and does not name Sera as a viewpoint. This is a possible soft inconsistency (Sera as viewpoint character present in Plot Outline and Style Guide but not enumerated in the Narrative Brief's viewpoint sentence). Preserved verbatim here for Task F; not resolved.

---

## Memory candidates

- Fact: The Plot Outline and Chapter Map (Version 1.0) contains exactly 36 chapter plot-map entries, numbered 1 through 36 contiguously across four acts (Act One ch 1-8, Act Two ch 9-18, Act Three ch 19-28, Act Four ch 29-36). Metadata: {type: fact, chapter: null, characters: [], tags: [plot-outline, chapter-map, migration, validation]}.
- Fact: Book One spans Friday October 3, 2053 through Saturday November 1, 2053; planned 36 chapters, approximately 115,000 to 130,000 words; close third person, multiple viewpoints. Metadata: {type: fact, tags: [plot-outline, book-1, structure]}.
- Fact: Plot Outline viewpoint distribution: Eli 15, Lena 5, Jonah 5, June 4, Kade 3, Sera 2, Mara 2; Morrow and Crown receive no internal viewpoints; Talia, Nolan, Celeste, Nora have no viewpoint chapters in Book One. Metadata: {type: fact, characters: [Eli, Lena, Jonah, June, Kade, Sera, Mara], tags: [viewpoint, plot-outline]}.
- Continuity hazard: The Narrative Brief has no version label or canon-status string and no YAML front matter, unlike the Plot Outline (Version 1.0) and Style Guide (Version 1.0, status "active style canon"). The Brief's own "Canon Priority" list, however, names it the #1 authority controlling project intent. Metadata: {type: continuity, tags: [narrative-brief, version, canon-status, migration]}.
- Continuity hazard / naming ambiguity: The Narrative Brief "Canon Priority" list references "World and Technology Rules", "Continuity Ledger", and "Research and Plausibility Ledger", but the repo's actual file is "Technology Rules.md" and no "Continuity Ledger" or "Research and Plausibility Ledger" file exists in the root scan. Metadata: {type: hazard, tags: [naming, inventory, canon-priority, migration]}.
- Decision (recommended, orchestrator to confirm): Per the master spec, Narrative Brief should relocate intact to docs/10-vision/narrative-brief.md (no split); Plot Outline splits into docs/30-plot/book-1/ (story-spine, major-beats, act-1..4, chapters/chapter-01..36, subplot-map, reveal-management, plus index for viewpoint distribution); Style Guide splits into docs/10-vision/style/ across the 12 listed style files. Metadata: {type: decision, tags: [migration, split-plan, vision, plot, style]}.
- Hazard (possible soft inconsistency, unresolved): Sera Vale is listed as a viewpoint character in both the Style Guide and the Plot Outline viewpoint table, but the Narrative Brief's "Narrative Style" sentence names only Lena, June, and Mara as supporting viewpoints and omits Sera. Flagged for Task F; not resolved. Metadata: {type: hazard, characters: [Sera], tags: [viewpoint, continuity, cross-document]}.
