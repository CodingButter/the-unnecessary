# Conflicts Found

This is the single shared ledger for canon conflicts discovered during the migration. It was seeded empty in Phase 00. Later phases APPEND to it; no phase re-creates it.

Rules (from the master spec and Phase 00 overview):

- When two project documents disagree on a fact, preserve both statements exactly. Do not delete, merge, or paraphrase either one.
- Record the conflict here, capturing both sources, their exact conflicting statements, the file paths, and the section or heading each came from.
- Only the orchestrator resolves a conflict. Agents report conflicts; the orchestrator is the only writer of this file.
- A discovered conflict does not block splitting or indexing. It blocks silent resolution only.

Status: Phase 01 recorded 6 conflict and inconsistency candidates (C1 through C6). Two are medium-severity cross-document canon conflicts (C2 era boundary, C3 viewpoint roster); the rest are a specificity gap (C1), a wording divergence (C4), and two intra-document inconsistencies (C5, C6). None is resolved (Phase 01 is read-only and does not resolve). The 10 duplicate-content overlaps (D1 through D10) are catalogued in `migration/repository-audit.md` section 6, not here, because they are overlaps to consolidate by linking (Phase 12), not factual disagreements.

| ID | Phase found | Source A (file and section) | Statement A | Source B (file and section) | Statement B | Status | Resolution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | 01 | `Story Bible.md` Act Three (L1427) | "guaranteed passage to Mars for Eli and a limited number of companions." | `Creative Decision Log.md` Decision 032 (title L1508, body L1515) | title "Kade Offers Eli Six Total Mars Seats"; body "Kade offers passage for Eli and five additional people." | open, low (specificity gap; the vague phrasing is consistent with five, but a writer reading the Story Bible alone could pick a different number) | deferred; orchestrator resolves in a later phase |
| C2 | 01 | `Story Bible.md` Historical Timeline (L535) | "### 2038 to 2041: The Replacement Wave" | `Master Timeline.md` era block (L397, L399) | "# Mosaic and the Replacement Wave" then "## 2039 to 2041" | open, MEDIUM (cross-document date-boundary disagreement, start year 2038 vs 2039; Master Timeline is the chronology authority) | deferred; orchestrator resolves in a later phase |
| C3 | 01 | `Style Guide.md` Viewpoint Characters (L132 to L142) | "Book One may use: Eli Rook, Jonah Mercer, Adrian Kade, Dr. Lena Okafor, June Park, Mara Voss, Sera Vale" | `Narrative Brief.md` Narrative Style (L412) | "Supporting viewpoints may include Lena Okafor, June Park, and Mara Voss." | open, MEDIUM (viewpoint-roster inconsistency; Sera Vale holds 2 viewpoint chapters per Plot Outline and Style Guide but is omitted from the Brief; the Brief hedges with "may include") | deferred; orchestrator resolves in a later phase |
| C4 | 01 | `Character Bible.md` Crown Origin (L1865) | "It has operated for nearly two decades when Book One begins." | `Technology Rules.md` Crown Overview (L225) | "Crown has operated continuously for approximately eighteen years by the beginning of Book One." | open, low (wording-precision divergence, not a date conflict; both reconcile to about 18 years from a 2035 origin) | deferred; orchestrator resolves in a later phase |
| C5 | 01 | `Master Timeline.md` High-Level Historical Progression Mermaid (L102) | "2052 : Mars passes its first long-duration habitability trial" | `Master Timeline.md` February 2051 prose (L826) | "Aurelia is publicly declared habitable." | open, low (intra-document diagram-versus-prose year, 2052 vs 2051; the Mermaid must be preserved verbatim and not silently fixed when these sections separate) | deferred; orchestrator resolves in a later phase |
| C6 | 01 | `Creative Decision Log.md` Decision Statuses legend (L63 to L87) | five labels defined: "Locked for Current Draft; Active but Revisable; Provisional; Rejected; Superseded" | `Creative Decision Log.md` Decisions 040 to 044 Status lines (L1816, L1862, L1909, L1966, L2019) | "Status: Locked for Current Workflow" (a sixth label not in the legend; Provisional, Rejected, and Superseded are defined but unused) | open, low (intra-document governance-metadata inconsistency; the decision-log split needs a complete status legend) | deferred; orchestrator resolves in a later phase |

## Notes on Phase 01 conflict findings

- Every statement above was verified by the orchestrator against the cited source line, not taken from an agent summary (coordination rule 7).
- C2 and C3 are the two genuine cross-document canon conflicts. C2 is a date-boundary disagreement where the Master Timeline is the established chronology authority. C3 is a viewpoint-roster inconsistency where the Brief's hedge ("may include") softens but does not erase the omission of Sera Vale.
- C1 is a specificity gap rather than a contradiction; C4 is a wording divergence that reconciles; C5 and C6 are inconsistencies inside a single document. All are recorded so no later phase resolves them silently.
- Consistency cross-checks that passed (recorded for completeness, no conflict): the October 3, 2053 opening date and weekday labels, the 36-chapter and 30-day Book One span, and the Mosaic-after-Crown ordering.
