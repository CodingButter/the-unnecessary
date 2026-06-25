# Audit note: Task F (Cross-Document Duplicate, Conflict, and Broken-Link Sweep)

Phase 01 Repository Audit. READ-ONLY against every project document. Authority: master spec
`migration/REPOSITORY-REORGANIZATION-SPEC.md` (wins all conflicts); runbook
`migration/plan/01-repository-audit.md`. This task runs AFTER inspectors A through E and reads
their notes to align, then verifies against the sources directly. It records findings only and
attempts NO resolution; both sides of every conflict are preserved verbatim. No em dashes are
used in this note's own prose (quoted source text may contain them and is reproduced as is).

Recommended destinations below are RECOMMENDED only; the orchestrator decides final paths.

## Method and verification performed

- Read all five upstream notes: `a-inventory.md`, `b-vision-plot-style.md`, `c-canon.md`,
  `d-governance.md`, `e-blueprints-and-discovered.md`.
- Re-verified each conflict and duplicate candidate by reading the cited source lines directly,
  not by trusting the upstream summary.
- Ran the broken-link sweep across all 12 sources for three link forms: inline `](...)`,
  reference-style `[x]: target`, and autolink `<http...>`.
- Cross-checked the Book One weekday claims against an actual calendar computation as a sanity
  pass on the timeline's internal date logic.

Sources swept (the 9 root monoliths + blueprint template + CLAUDE.md + Memory Conventions.md):
`Narrative Brief.md`, `Story Bible.md`, `Character Bible.md`, `Technology Rules.md`,
`Master Timeline.md`, `Plot Outline and Chapter Map.md`, `Style Guide.md`,
`Creative Decision Log.md`, `Development and Canon Guide.md`,
`chapter-blueprints/Chapter Blueprint Template.md`, `CLAUDE.md`, `Memory Conventions.md`.

mem0 search for the task topic returned zero stored memories (empty result set) at sweep time,
so there was no prior memory to cross-check; the bibles were used as authority. Recorded for the
orchestrator: mem0 had nothing on this audit topic.

---

## Source heading outlines processed (coordination rule 6)

Task F is a cross-document sweep, not a per-document audit, so the authoritative full H1/H2
(and deeper) heading outlines for each source live in the upstream notes that own each document.
To satisfy coordination rule 6 without duplicating those long outlines verbatim, this note
records, per source, the H1/H2 top-level outline coverage and points to the owning note. Every
source heading was processed for the sweep. The owning notes carry the exhaustive outline.

- `Narrative Brief.md` (owner: note B). H1 `Narrative Brief`; H2s: Project Title; Purpose of
  This Document; One-Sentence Premise; Condensed Story Summary; The Narrative Promise; Core
  Narrative Conflict; The World; The Protected Enclaves; Mars; The Waiting Wealthy; The
  Protagonist; The Childhood Friend; The Primary Human Antagonist; Morrow; Major Themes; Tone
  and Emotional Experience; Narrative Style; Storytelling Rules; Concepts and Directions to
  Avoid; Book One Arc; Series Direction; Canon Priority; Final Creative Standard. (H3s under The
  Protagonist/Childhood Friend/Antagonist and the eight Major Themes per note B.)
- `Story Bible.md` (owner: note C). H1 `The Unnecessary`; H2s: Complete Story Bible Version 1.0;
  Working Title; Format; Genre; Tone; Core Premise; Central Questions; The Thematic Argument;
  Time Period; The Shape of Society; The Erosion of Ordinary Life; Protected Enclaves; Mars;
  Historical Timeline; Technology Rules; Existing Artificial Intelligence; Crown; Primary
  Setting; Main Locations; Protagonist; Childhood Friend; Technology Leader; Supporting
  Characters; Morrow; Narrative Structure; Book One; Act One; Act Two; Act Three; Act Four;
  Eli's Book One Arc; Jonah's Book One Arc; Kade's Book One Arc; Mara's Book One Arc; Series
  Direction; Rules for Consistency; Research Ledger; Final Promise of the Story. (Full H3s in
  note C.)
- `Character Bible.md` (owner: note C). H1 per entity (`The Unnecessary`, Core Character
  Principles, Primary Cast, the 13 character H1s, Nonhuman Characters, Relationship Map,
  Viewpoint Guidance, Dialogue Differentiation, Character Continuity Fields, Final Character
  Standard) with profile-field H2s under each. (Full per-character H2 field lists in note C.)
- `Technology Rules.md` (owner: note C). H1 system blocks: Foundational Rule; The Technological
  State of the World; Levels of Artificial Intelligence; Consciousness and Personhood; Crown;
  Morrow; Crown and Morrow; Computing Hardware; Energy; Communications; Cloud Dependency and
  Digital Ownership; Identity Money and Access; Robotics; Transportation; Medicine; Manufacturing
  and Materials; Security and Surveillance; Weapons and Conflict; Government Technology; Protected
  Enclaves; Community Infrastructure; Northglass; Mars and the Aurelia Initiative; Scientific
  Progress; Information and Propaganda; Hard Plot Restrictions; Failure Rules; Technology in
  Scenes; Continuity Questions for Every Technical Scene; Canon Summary. (Full H2s in note C.)
- `Master Timeline.md` (owner: note C). H1 era/section blocks: Timeline Authority; High-Level
  Historical Progression; Causal Progression of the World; Principal Character Birth Dates;
  Before the Transformation; The Assistance Era; The Compression Era; General Autonomy; The
  Intelligence Acceleration; Mosaic and the Replacement Wave; Infrastructure Bargains; The
  Aurelia Initiative; Market Withdrawal; The Support Collapse; The Preservation Years; The Final
  Months Before Book One; Book One Calendar; Book One Overview; Detailed Book One Timeline; Act
  Two; Act Three; Act Four; Book One Character Knowledge Timeline; Secret Timeline; Parallel
  Character Progression; Timing and Travel Rules During Book One; Timeline Continuity Rules;
  Open Timeline Questions; Final Chronological Standard. (Daily-entry H2/H3 in note C; 4 Mermaid
  blocks.)
- `Plot Outline and Chapter Map.md` (owner: note B). H1 blocks: Book Information; Structural
  Decision; Story Spine; Major Structural Beats; Act Structure; Act One; Act Two; Act Three; Act
  Four; Subplot Map; Reveal Management; Chapter Tension Pattern; Drafting Rules for Chapters;
  Scene Card Template; Final Structural Standard. 36 chapter H2 entries (1 through 36); per-chapter
  H3 sub-fields. (Full outline in note B; 1 Mermaid block.)
- `Style Guide.md` (owner: note B). H1 blocks from Core Prose Identity through Final Style
  Standard, including per-character voice H1s and the seven Style Review Process passes. (Full
  H1/H2/H3 in note B.)
- `Creative Decision Log.md` (owner: note D). H1: How to Use; Decision Statuses; Decision Entry
  Template; eight category H1s (Foundational Story, Setting and Social Structure, Mars,
  Artificial Intelligence, Character, Plot and Structure, Style and Tone, Workflow); Explicitly
  Rejected Concepts; Open Decisions; Existing Documents Affected by This Log; Future Update
  Procedure; Final Principle. 44 decision H2s (001 through 044). (Full enumeration in note D.)
- `Development and Canon Guide.md` (owner: note D). H1 blocks from Core Principle through Final
  Operating Principle (the per-document usage H1s, the seven-phase workflow, contradiction
  resolution, change management, versioning, canon status labels, naming rules, quality gates,
  failure modes). (Full H1/H2/H3 in note D; 1 Mermaid block.)
- `chapter-blueprints/Chapter Blueprint Template.md` (owner: note E). H1: Chapter Blueprint
  Template; Chapter [Number]: [Working Title]; Scene Breakdown; End of Scene Breakdown. (Full
  H2/H3 in note E; 1 Mermaid block.)
- `CLAUDE.md` (owner: notes A and E). H1: The Unnecessary - Project Instructions; mem0 -
  Operating Protocol. H2s as in note E; 1 H3 (Directive block).
- `Memory Conventions.md` (owner: notes A and E). H1: Memory Conventions (mem0); 9 H2s as in
  note E.

---

# SWEEP 3 FIRST: BROKEN-LINK DETECTION (the load-bearing count)

This sweep is reported first because it is unambiguous and gates the structured return value.

- **Inline relative Markdown links `](...)`: ZERO across all 12 sources.** Per-file count
  (inline `](...)`): each of the 12 sources returned 0. Total = 0.
- **Reference-style link definitions `[label]: target`: ZERO across all 12 sources.**
- **Autolinks `<http...>`: ZERO across all 12 sources.**
- Therefore **links_checked_count = 0** and **broken_links = none**. There is nothing to
  resolve and nothing broken, because no source document contains any Markdown link of any form.

**Important nuance for later phases (recorded, not a broken link):** several documents reference
other documents by bare filename in prose or inside backtick code spans, NOT as Markdown links.
These are not links and are excluded from the count above, but they ARE stale path references
that a later link-creation phase must handle:

- `Creative Decision Log.md` -> "Existing Documents Affected by This Log" (lines 2173 to 2182)
  lists eight backtick paths in the OLD folder scheme: `canon/narrative-brief.md`,
  `canon/story-bible.md`, `canon/character-bible.md`, `canon/world-and-technology-rules.md`,
  `canon/master-timeline.md`, `planning/plot-outline-and-chapter-map.md`,
  `chapter-blueprints/_chapter-blueprint-template.md`, `novel-development-and-canon-guide.md`.
  None of these paths exists on disk today (the actual files are space-named root monoliths such
  as `Story Bible.md`), and none matches the master spec `docs/` target tree. They are text in a
  code-style list, not clickable links; recorded for the path-reconciliation phase, not as broken
  links in the link-sweep sense.
- `CLAUDE.md`, `Memory Conventions.md`, the blueprint template, the Style Guide, the Plot
  Outline, and the Narrative Brief reference bible filenames in prose or backticks (for example
  `Character Bible.md`, `Story Bible.md`). Those filenames DO currently resolve at the repo root
  but are not Markdown links, so they neither count toward links_checked_count nor as broken
  links. They will become outdated once files move under `docs/`.

Bottom line: **links_checked_count = 0; broken_links = none.** Every relative Markdown link in
every source has been checked (there are none). Link rewriting in later phases is a
link-CREATION task, not a broken-link-FIX task.

---

# SWEEP 1: DUPLICATE DETECTION

Repeated AUTHORITATIVE content across DIFFERENT documents that risks divergence if one copy is
edited and the others are not. Intentional cross-references are excluded; these are substantive
restatements of canon facts. None of the items below is a contradiction (those are in Sweep 2);
each is a single fact stored in more than one authority.

### D1. Eli Rook's age (38) stated in three authorities
- `Story Bible.md` "Protagonist > Age" (line 819): "Thirty-eight."
- `Character Bible.md` Eli "Basic Information" (line 7): "Age at the beginning of Book One: 38".
- `Master Timeline.md` "Principal Character Birth Dates" table (line 142): "Elias Rook |
  February 11, 2015 | 38"; prose (line 181) "Elias Rook is born in Flint."
- Kind: duplicated character fact (Story Bible vs Character Bible vs Master Timeline).
- Consistent in value (all 38). Divergence risk: editing the birth date or age in one place
  would silently desync the others. Per master spec Phase 12, age authority is the character
  profile and the birth date authority is the timeline; the Story Bible copy should become a
  link/summary. Recorded.

### D2. Condensed character profiles duplicated in Story Bible vs Character Bible
- `Story Bible.md` "Protagonist", "Childhood Friend", "Technology Leader", "Supporting
  Characters" (Lena, June, Mara), and "Morrow" sections restate condensed versions of profiles
  that the `Character Bible.md` owns in full (Eli, Jonah, Kade, Lena, June, Mara, Morrow).
- Kind: duplicated character canon. The Story Bible carries a NARROWER cast (no Talia, Nolan,
  Sera, Celeste, Nora). Divergence risk on any shared field (wants, fears, moral boundary).
  Resolve by linking on split (Phase 12), not merging. Recorded.

### D3. Condensed technology summaries duplicated in Story Bible vs Technology Rules
- `Story Bible.md` H2 "Technology Rules", "Existing Artificial Intelligence", "Crown" restate
  capability material that `Technology Rules.md` owns in full (Crown, Morrow, AI levels).
- Kind: duplicated technical canon (Story Bible vs Technology Rules). Divergence risk on Crown
  and Morrow capability wording. Resolve by linking. Recorded.

### D4. Historical timeline duplicated in Story Bible vs Master Timeline
- `Story Bible.md` H2 "Historical Timeline" (H3 era entries 2026 through 2053) restates the
  chronology that `Master Timeline.md` owns in full (era H1 blocks 1992 through 2053).
- Kind: duplicated temporal canon (Story Bible vs Master Timeline). This pair also produces the
  era-label divergence recorded as C2 in Sweep 2 (a real boundary-year difference). Resolve by
  making the timeline the single authority and linking from the Story Bible. Recorded.

### D5. Northglass description duplicated in Story Bible vs Technology Rules vs Decision Log
- `Story Bible.md` "Main Locations > Northglass" (lines 761 to 777): "Northglass is Asterion's
  abandoned Great Lakes research campus." and "Northglass becomes the physical foundation of
  Morrow."
- `Technology Rules.md` H1 "Northglass" (lines 1388 to 1442): "Northglass was Asterion's Great
  Lakes research and testing campus." and "Northglass provides capability, not a finished mind."
- `Creative Decision Log.md` "Decision 007: Northglass Is an Abandoned Asterion Campus" (lines
  442 to 463): "Northglass is a former Asterion Great Lakes research campus ..." and "Northglass
  provides capability and history, not a finished intelligence waiting to be discovered."
- Kind: duplicated world/tech/decision content. Consistent in substance. Divergence risk across
  three authorities. Master spec Phase 12: world description vs tech capability vs decision
  rationale should each hold their slice and link. Recorded.

### D6. Mars seat offer ("six total / five additional") restated in three places (consistent)
- `Creative Decision Log.md` "Decision 032: Kade Offers Eli Six Total Mars Seats" body (line
  1515): "Kade offers passage for Eli and five additional people."
- `Plot Outline and Chapter Map.md` Ch 20 (line 1251): "Passage to Mars for Eli and five people
  of his choosing"; Ch 21 (line 1297): "There are six seats including Eli, but Jonah's immediate
  family alone requires five additional places."
- `Master Timeline.md` (line 1408): "Mars passage for Eli and five people of his choosing".
- Kind: duplicated plot fact (decision vs plot vs timeline). All three reconcile to SIX TOTAL =
  Eli plus five. The decision TITLE says "Six Total" while the bodies say "five additional"; this
  is the same number expressed two ways. Divergence risk: a careless reader could read "five" and
  "six" as conflicting. Recorded here as a duplicate-with-presentation-risk; see C1 in Sweep 2 for
  the related Story Bible specificity gap. Authority for the number: Decision Log (it is a
  decision), echoed by Plot and Timeline.

### D7. Chapter count (36) and 30-day span restated across four+ documents (consistent)
- `Creative Decision Log.md` Decision 029 (line 1402): "The current outline contains 36 chapters."
- `Plot Outline and Chapter Map.md` "Chapter Count" (line 39): "36 chapters".
- `Master Timeline.md` and `Story Bible.md` also frame Book One as 36 chapters across Oct 3 to
  Nov 1, 2053 (per notes A and C).
- Kind: duplicated structural fact. Consistent. Authority: Decision Log (decision) plus Plot
  Outline (structure). Low divergence risk because the number is load-bearing and widely echoed,
  but still multi-sourced. Recorded.

### D8. Viewpoint distribution / viewpoint-character set restated in three documents
- `Style Guide.md` "Viewpoint Characters" (lines 134 to 144): Eli, Jonah, Kade, Lena, June, Mara,
  Sera Vale; Morrow and Crown excluded.
- `Plot Outline and Chapter Map.md` "Primary Viewpoint Distribution": per-character chapter counts
  (Eli 15, Lena 5, Jonah 5, June 4, Kade 3, Sera 2, Mara 2) per note B.
- `Narrative Brief.md` "Narrative Style" (lines 404 to 412): Eli primary; Jonah and Kade; "Supporting
  viewpoints may include Lena Okafor, June Park, and Mara Voss."
- Kind: duplicated viewpoint canon across style, plot, and vision documents. The Style Guide and
  Plot Outline agree on seven viewpoint characters including Sera; the Narrative Brief enumerates
  only Lena, June, and Mara as supporting viewpoints and omits Sera. The membership divergence is
  recorded as conflict C3 in Sweep 2 (Sera). Recorded here as duplication of the viewpoint fact.

### D9. Per-character voice / speech rules duplicated in Character Bible vs Style Guide
- `Character Bible.md` "Dialogue Differentiation" (11 per-character H2s) and each profile's
  "Speech Pattern" / "Writing Rules" fields.
- `Style Guide.md` "Character Voice Guide" plus per-character H1 voice blocks (Eli, Jonah, Kade,
  Lena, June, Mara, Sera, Talia, Nolan) and the Morrow/Crown voice sections.
- Kind: duplicated voice guidance (character canon vs style canon). Master spec Phase 12 says
  prose rules belong in style files and character facts in profiles; the boundary between
  "speech pattern" (profile) and "voice/dialogue rules" (style) overlaps. Divergence risk if one
  is edited. Recorded; the orchestrator decides the single authority on split.

### D10. Morrow and Crown behavioral identity duplicated across Character Bible, Technology Rules, Story Bible, Style Guide
- Morrow/Crown appear as: characters (`Character Bible.md` profiles), capability rules
  (`Technology Rules.md` Crown/Morrow/Crown-and-Morrow), condensed overview (`Story Bible.md`),
  and dialogue voice (`Style Guide.md` Morrow/Crown). Personhood also in
  `Technology Rules.md` "Consciousness and Personhood" and Decision 014 to 018.
- Kind: cross-domain duplication of the same two entities. Substance is consistent (the Crown
  duration wording divergence is the one exception, recorded as C4). Master spec Phase 12 example
  explicitly calls for the behavioral identity (character file), architecture/capabilities (tech
  file), and progression (plot files) to link rather than duplicate. Recorded.

---

# SWEEP 2: CONFLICT DETECTION

Contradictory or divergent canonical statements across documents. Both sides preserved verbatim
with file and heading. NO resolution attempted. Severity: high if load-bearing canon a reader
would act on; low if cosmetic wording. The orchestrator decides which rise to recorded conflicts
for `migration/conflicts-found.md`.

### C1. Kade's Mars offer: "limited number of companions" (Story Bible) vs "five / six total" (Decision Log, Plot, Timeline)
- Severity: **low** (specificity gap, not a numeric contradiction).
- `Story Bible.md` Act Three (line 1427): "... and guaranteed passage to Mars for Eli and a
  limited number of companions."
- `Creative Decision Log.md` Decision 032 (line 1515): "Kade offers passage for Eli and five
  additional people." Title (line 1508): "Kade Offers Eli Six Total Mars Seats."
- `Plot Outline and Chapter Map.md` Ch 20 (line 1251): "Passage to Mars for Eli and five people
  of his choosing." Ch 21 (line 1297): "There are six seats including Eli ..."
- `Master Timeline.md` (line 1408): "Mars passage for Eli and five people of his choosing."
- Nature: the Story Bible leaves the number unspecified ("a limited number"); the other three fix
  it at six total (Eli + five). They do not contradict; the Story Bible is simply vaguer. The
  precise count lives only outside the Story Bible. Preserved both ways; not resolved.

### C2. "Replacement Wave" era boundary: 2038 to 2041 (Story Bible) vs 2039 to 2041 (Master Timeline)
- Severity: **low to medium** (a one-year era-boundary divergence in temporal canon).
- `Story Bible.md` "Historical Timeline" (line 535): H3 "2038 to 2041: The Replacement Wave".
- `Master Timeline.md` (lines 397 to 399): H1 "Mosaic and the Replacement Wave", H2 "2039 to 2041".
- Nature: the same era is labeled with a different START YEAR (2038 vs 2039) and a slightly
  different name ("The Replacement Wave" vs "Mosaic and the Replacement Wave"). The Master Timeline
  is the chronology authority. The "Approximate Periods" caveat in the Master Timeline's "Timeline
  Authority" section notes some changes are gradual, which may explain a fuzzy boundary, but the
  labels still differ on the page. Both preserved verbatim; not resolved.

### C3. Sera Vale as a viewpoint character: present (Style Guide, Plot Outline) vs absent (Narrative Brief)
- Severity: **low to medium** (a soft inconsistency a reader consulting only the Brief would miss).
- `Style Guide.md` "Viewpoint Characters" (line 142): lists "Sera Vale" among the seven viewpoint
  characters.
- `Plot Outline and Chapter Map.md` "Primary Viewpoint Distribution": assigns Sera 2 viewpoint
  chapters (per note B; Ch 23 and Ch 28 are Sera viewpoint chapters per note B's chapter list).
- `Narrative Brief.md` "Narrative Style" (line 412): "Supporting viewpoints may include Lena
  Okafor, June Park, and Mara Voss." Sera is NOT named.
- Nature: the Brief uses hedge language ("may include") and names only three supporting
  viewpoints, omitting Sera, who holds viewpoint chapters in both the Plot Outline and the Style
  Guide. Not a hard contradiction because of the "may include" hedge, but a coverage divergence.
  Both preserved verbatim; not resolved.

### C4. Crown operating duration: "nearly two decades" (Character Bible) vs "approximately eighteen years" (Technology Rules) vs "since 2035" (Master Timeline)
- Severity: **low** (wording-precision divergence; all reconcile to about 18 years).
- `Character Bible.md` Crown "Origin" (line 1865): "It has operated for nearly two decades when
  Book One begins."
- `Technology Rules.md` Crown "Overview" (line 225): "Crown has operated continuously for
  approximately eighteen years by the beginning of Book One."
- `Master Timeline.md` "Timeline Continuity Rules" rule 1 (line 1878): "Crown has existed since
  2035." plus the "General Autonomy" entry placing Crown's general autonomy in March 2035 (18 years
  before 2053).
- Nature: "nearly two decades" is a looser restatement of "approximately eighteen years"; both
  agree with a 2035 origin. No date contradiction; only the Character Bible's phrasing is fuzzier.
  Both preserved verbatim; not resolved.

### C5. Mars habitability milestone year: Mermaid "2052" vs prose "Feb 2051 publicly declared habitable" (same document, Master Timeline)
- Severity: **low** (intra-document summarization-label divergence, not cross-document).
- `Master Timeline.md` High-Level Historical Progression Mermaid (line 102): "2052 : Mars passes
  its first long-duration habitability trial".
- `Master Timeline.md` prose, "2051 > February 2051" (line 826): "Aurelia is publicly declared
  habitable."
- Nature: the Mermaid milestone (a long-duration habitability TRIAL labeled 2052) and the prose
  event (public habitability DECLARATION in Feb 2051) are arguably different events, but the year
  label divergence (2051 vs 2052) inside one authority is a summarization-label mismatch worth a
  later look. Both preserved verbatim; not resolved. Recorded because the Mermaid must be preserved
  on split and a future reader may treat the diagram year as canon.

### C6. Decision Log status-label legend vs labels actually used (intra-document)
- Severity: **low** (governance metadata inconsistency, not story canon).
- `Creative Decision Log.md` "Decision Statuses" legend (lines 63 to 87) defines exactly FIVE
  labels: "Locked for Current Draft", "Active but Revisable", "Provisional", "Rejected",
  "Superseded".
- Actual `**Status:**` values used across the 44 entries (verified by extraction): "Locked for
  Current Draft" (32, plus 1 with trailing whitespace), "Active but Revisable" (7), and "Locked
  for Current Workflow" (5, on decisions 040 to 044). "Provisional", "Rejected", and "Superseded"
  are defined but used by zero current entries.
- Nature: "Locked for Current Workflow" (used by the five Workflow decisions) is NOT in the
  legend; three defined labels are unused. Also one entry carries a trailing-whitespace variant of
  "Locked for Current Draft". This is an internal governance-metadata inconsistency the index/legend
  reconciliation in a later phase must address. Recorded; not resolved.

### Cross-document statements checked and found CONSISTENT (no conflict)
Recorded so the orchestrator knows these were examined, not skipped:
- Book One opening date "Friday, October 3, 2053" matches across Plot Outline (Ch 1 date) and
  Master Timeline ("Canonical Opening Date", line 962). The weekday is astronomically correct
  (Oct 3 2053 is a Friday; Oct 31 2053 is a Friday; Nov 1 2053 is a Saturday), so the
  day-of-week labels in the timeline and plot are internally and externally consistent.
- Chapter count 36 and the 30-day span agree across Decision Log, Plot Outline, Story Bible, and
  Master Timeline (see D7).
- Mosaic-after-Crown ordering is consistent: Master Timeline continuity rule 2 (line 1880)
  "Mosaic is developed after Crown ..."; Technology Rules describes "Mosaic-derived orchestration"
  building on general autonomous systems; Story Bible narrates Mosaic as Eli's contribution within
  Asterion. No ordering reversal found.
- Northglass substance (Great Lakes Asterion campus; foundation of Morrow but not a finished
  mind) is consistent across Story Bible, Technology Rules, and Decision 007 (see D5); the overlap
  is duplication, not conflict.

---

## Per-source sweep summary table

| Source | Inline links | Duplicates involving it | Conflicts involving it |
|---|---:|---|---|
| Narrative Brief.md | 0 | D8 | C3 |
| Story Bible.md | 0 | D1, D2, D3, D4, D5, D10 | C1, C2 |
| Character Bible.md | 0 | D1, D2, D9, D10 | C4 |
| Technology Rules.md | 0 | D3, D5, D10 | C4 |
| Master Timeline.md | 0 | D1, D4, D6, D7, D10 (timeline echoes) | C2, C4, C5 |
| Plot Outline and Chapter Map.md | 0 | D6, D7, D8 | C1, C3 |
| Style Guide.md | 0 | D8, D9, D10 | C3 |
| Creative Decision Log.md | 0 | D5, D6, D7 | C1, C6 |
| Development and Canon Guide.md | 0 | (none substantive) | (none) |
| chapter-blueprints/Chapter Blueprint Template.md | 0 | (none) | (none) |
| CLAUDE.md | 0 | (restates premise by design; not a divergence-risk duplicate) | (none) |
| Memory Conventions.md | 0 | (none) | (none) |

---

## Conflicts / ambiguities for the orchestrator (record, do not resolve)

- C1 through C6 above are the candidate conflicts. The orchestrator decides which become recorded
  entries in `migration/conflicts-found.md` and how they are framed. None is resolved here; both
  sides of each are preserved verbatim above.
- The stale old-folder path references in the Decision Log "Existing Documents Affected" list and
  the bare-filename references in CLAUDE.md, Memory Conventions.md, the Style Guide, the Plot
  Outline, and the Narrative Brief are path-reconciliation items for a later link-creation phase,
  not broken Markdown links (there are no Markdown links to break).
- Memory Conventions.md has no destination slot in the master spec Phase 2 tree (flagged by notes
  A and E); not a conflict, an unprovisioned-destination ambiguity for the orchestrator.

---

## Memory candidates

- continuity: In "The Unnecessary", Kade's Mars offer is six total seats (Eli plus five
  additional). The Decision Log title 032 says "Six Total Mars Seats"; the Decision 032 body,
  the Plot Outline (Ch 20/21), and the Master Timeline all say "five additional / five people of
  his choosing"; the Story Bible says only "a limited number of companions" (no count). All
  reconcile to six total; the count is fixed everywhere except the Story Bible.
  (metadata: {type: continuity, characters: [Kade, Eli, Jonah], tags: [mars, plot, conflict-candidate, migration]})
- hazard: Era-boundary divergence: the Story Bible labels the era "2038 to 2041: The Replacement
  Wave" while the Master Timeline labels it "Mosaic and the Replacement Wave, 2039 to 2041" (start
  year 2038 vs 2039). Master Timeline is the chronology authority; both preserved, unresolved in
  Phase 01. (metadata: {type: hazard, tags: [timeline, era, conflict-candidate, migration]})
- hazard: Sera Vale holds viewpoint chapters in the Style Guide ("Viewpoint Characters") and the
  Plot Outline (2 chapters), but the Narrative Brief "Narrative Style" names only Lena, June, and
  Mara as supporting viewpoints and omits Sera. Soft inconsistency; the Brief uses "may include".
  (metadata: {type: hazard, characters: [Sera], tags: [viewpoint, cross-document, conflict-candidate, migration]})
- continuity: Crown's operating duration is stated as "nearly two decades" (Character Bible),
  "approximately eighteen years" (Technology Rules), and origin "since 2035" / General Autonomy
  March 2035 (Master Timeline). All reconcile to about 18 years to 2053; only the Character Bible
  phrasing is looser. (metadata: {type: continuity, characters: [Crown], tags: [timeline, crown, conflict-candidate, migration]})
- hazard: The Creative Decision Log "Decision Statuses" legend defines five labels (Locked for
  Current Draft, Active but Revisable, Provisional, Rejected, Superseded), but Decisions 040 to 044
  use an undefined sixth label "Locked for Current Workflow", and Provisional/Rejected/Superseded
  are defined yet unused. (metadata: {type: hazard, tags: [decision-log, status-labels, governance, migration]})
- fact: No source document in "The Unnecessary" (the 9 monoliths + blueprint template + CLAUDE.md
  + Memory Conventions.md) contains any relative Markdown link (inline, reference-style, or
  autolink); the broken-link count is zero and link work in later phases is link CREATION, not
  repair. (metadata: {type: fact, tags: [migration, links, audit, phase-01]})
- hazard: The Decision Log "Existing Documents Affected by This Log" list references the OLD
  folder scheme (canon/, planning/, chapter-blueprints/) and the filename
  novel-development-and-canon-guide.md; none of these paths exists on disk or matches the master
  spec docs/ tree, so they need path reconciliation in a later phase. They are not Markdown links.
  (metadata: {type: hazard, tags: [migration, paths, decision-log, links])
- continuity: The Master Timeline High-Level Historical Progression Mermaid labels "2052: Mars
  passes its first long-duration habitability trial" while the same document's prose puts "Aurelia
  is publicly declared habitable" at February 2051; a summarization-label year divergence (2051 vs
  2052) inside one authority. (metadata: {type: continuity, tags: [timeline, mars, mermaid, conflict-candidate, migration]})
