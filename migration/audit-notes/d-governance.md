# Audit note: Task D (Governance and Decision Documents)

Phase 01 Repository Audit. READ-ONLY. Authority: `migration/REPOSITORY-REORGANIZATION-SPEC.md` (wins all conflicts); runbook `migration/plan/01-repository-audit.md`.

This note audits exactly two documents:

- `/home/codingbutter/Novel/Development and Canon Guide.md`
- `/home/codingbutter/Novel/Creative Decision Log.md`

No project document was moved, renamed, split, edited, archived, or deleted. Recommended destinations are proposals only; the orchestrator decides final paths.

---

## Development and Canon Guide.md

- **Title (as stated):** "The Unnecessary" (H1 line 1) with subtitle "Novel Development and Canon Guide, Version 1.0" (H2 line 3). Referred to throughout the project as the Novel Development and Canon Guide.
- **Current path:** `/home/codingbutter/Novel/Development and Canon Guide.md`
- **Document type:** Governance / operating manual (process and canon-handling guide). The spec's target name is `novel-development-guide.md`.
- **Apparent version:** 1.0 (stated in the H2 subtitle "Version 1.0", line 3). No YAML front-matter version block is present in this file.
- **Canon status:** Not stated explicitly as a status label inside the document. The file is the operating manual; the project CLAUDE.md treats it as the authority on process and conflict handling. Functionally active governance. Record canon status as "not stated" in-source; treat as active governance by role.
- **Subject (1-2 lines):** Explains how the planning, drafting, continuity, and research documents for The Unnecessary work together. Defines document purposes, the canon hierarchy, established vs planned canon, the chapter workflow, contradiction resolution, versioning, naming, quality gates, and AI handoff rules.
- **Mermaid blocks:** 1 (the layered-system flowchart at lines 41-71, under the "Core Principle" H1).

### FULL heading outline (every H1 and H2; H3 included where present)

- H1: The Unnecessary (line 1)
  - H2: Novel Development and Canon Guide, Version 1.0 (3)
  - H2: Purpose of This Document (5)
- H1: Core Principle (33) [contains the single Mermaid flowchart]
- H1: Recommended Project Structure (85) [contains a `text` code block showing the OLD canon/planning/ tree]
- H1: The README File (138)
  - H2: Suggested Filename (140)
  - H2: Purpose (144)
- H1: Document Categories (170)
  - H2: 1. Vision Documents (174)
  - H2: 2. Canon Documents (181)
  - H2: 3. Planning Documents (190)
  - H2: 4. Established Story Documents (198)
  - H2: 5. Support Documents (205)
- H1: Established Canon Versus Planned Canon (218)
  - H2: Established Canon (220)
  - H2: Planned Canon (234)
  - H2: Proposed Material (247)
- H1: Canon Authority (262)
  - H2: Highest Authority (270)
    - H3: 1. Approved Manuscript (272)
    - H3: 2. Explicitly Approved Revision (282)
    - H3: 3. Continuity Ledger (288)
  - H2: Authority by Subject (296)
    - H3: Creative Identity (298)
    - H3: General World Canon (307)
    - H3: Character Canon (319)
    - H3: Technical Canon (333)
    - H3: Temporal Canon (345)
    - H3: Structural Plan (356)
    - H3: Chapter Plan (367)
    - H3: Prose Execution (381)
- H1: What Each Document Does (396)
- H1: Narrative Brief (398)
  - H2: Primary Question (400)
  - H2: Use It When (404)
  - H2: Do Not Use It For (413)
  - H2: Update It When (420)
- H1: Story Bible (436)
  - H2: Primary Question (438)
  - H2: Use It When (442)
  - H2: Do Not Use It For (451)
  - H2: Update It When (458)
- H1: Character Bible (474)
  - H2: Primary Question (476)
  - H2: Use It When (480)
  - H2: Do Not Use It For (490)
  - H2: Update It When (497)
- H1: World and Technology Rules (510)
  - H2: Primary Question (512)
  - H2: Use It When (516)
  - H2: Do Not Use It For (526)
  - H2: Update It When (532)
- H1: Master Timeline (544)
  - H2: Primary Question (546)
  - H2: Use It When (550)
  - H2: Do Not Use It For (561)
  - H2: Update It When (568)
- H1: Plot Outline and Chapter Map (581)
  - H2: Primary Question (583)
  - H2: Use It When (587)
  - H2: Do Not Use It For (597)
  - H2: Update It When (604)
- H1: Chapter Blueprint Template (619)
  - H2: Primary Question (621)
  - H2: Use It When (625)
  - H2: Do Not Use It For (632)
- H1: Individual Chapter Blueprints (642)
  - H2: Primary Question (644)
  - H2: Use Them When (648)
  - H2: Do Not Use Them For (658)
  - H2: Update Them When (664)
- H1: Style Guide (677)
  - H2: Primary Question (679)
  - H2: Use It When (683)
  - H2: The Style Guide Should Eventually Define (693)
  - H2: Update It When (712)
- H1: Research and Plausibility Ledger (720)
  - H2: Primary Question (722)
  - H2: Use It When (726)
  - H2: Suggested Status Labels (737)
  - H2: Update It When (746)
- H1: Decision Log (762)
  - H2: Primary Question (764)
  - H2: Use It When (768)
  - H2: Each Entry Should Include (779)
  - H2: Example Categories (790)
- H1: Continuity Ledger (806)
  - H2: Primary Question (808)
  - H2: Use It When (812)
  - H2: Update It When (823)
  - H2: It Should Track (831)
    - H3: Character State (833)
    - H3: Knowledge State (842)
    - H3: Relationship State (849)
    - H3: Physical State (859)
    - H3: Narrative State (869)
- H1: Manuscript Chapters (881)
  - H2: Primary Question (883)
  - H2: Use Them When (887)
  - H2: Chapter Statuses (896)
- H1: Archive (915)
  - H2: Purpose (917)
- H1: Standard Workflow for Building the Novel (946)
- H1: Phase 1: Project Orientation (948)
- H1: Phase 2: Creating a Chapter Blueprint (973)
  - H2: Always Required (977)
  - H2: Also Required (987)
  - H2: Sometimes Required (993)
  - H2: Blueprint Creation Process (1001)
    - H3: Step 1: Confirm the Chapter's Existing Role (1003)
    - H3: Step 2: Check Temporal Continuity (1016)
    - H3: Step 3: Check Character Logic (1029)
    - H3: Step 4: Check Technical Logic (1041)
    - H3: Step 5: Build the Scene Sequence (1055)
    - H3: Step 6: Check Book-Level Structure (1068)
    - H3: Step 7: Record Open Questions (1079)
- H1: Phase 3: Approving a Chapter Blueprint (1087)
- H1: Phase 4: Drafting a Manuscript Chapter (1109)
  - H2: Essential Context (1113)
  - H2: Supporting Context (1122)
  - H2: Drafting Rules (1133)
- H1: Phase 5: Reviewing the Draft (1170)
  - H2: Pass 1: Structural Review (1174)
  - H2: Pass 2: Character Review (1184)
  - H2: Pass 3: World and Technology Review (1194)
  - H2: Pass 4: Prose Review (1203)
- H1: Phase 6: Approving the Chapter (1216)
- H1: Phase 7: Creating the Next Chapter (1235)
  - H2: Recommended Planning Distance (1253)
- H1: How an AI Should Use the Project (1265)
  - H2: Before Starting (1267)
  - H2: AI Operating Rules (1279)
  - H2: Required Behavior When a Conflict Appears (1296)
- H1: Task-Specific Context Packages (1310)
- H1: Creating a New Character (1314)
- H1: Creating a New Location (1329)
- H1: Creating a Chapter Blueprint (1342)
- H1: Drafting a Chapter (1360)
- H1: Revising a Chapter (1374)
- H1: Researching a Technical Question (1389)
- H1: Checking Continuity (1401)
- H1: Planning a Sequel (1415)
- H1: Contradiction Resolution Process (1432)
  - H2: Step 1: Identify the Fact Type (1436)
  - H2: Step 2: Identify the Relevant Authority (1449)
  - H2: Step 3: Check Whether the Fact Appears in Approved Prose (1453)
  - H2: Step 4: Determine Whether the Conflict Is Accidental or Creative (1457)
  - H2: Step 5: Choose a Resolution (1463)
  - H2: Step 6: Propagate the Change (1473)
  - H2: Step 7: Record the Decision (1479)
- H1: Types of Apparent Contradictions That May Be Intentional (1485)
  - H2: Character Misinformation (1489)
  - H2: Corporate Propaganda (1495)
  - H2: Unreliable Memory (1501)
  - H2: Incomplete Technical Knowledge (1507)
  - H2: Deliberate Deception (1513)
- H1: Change Management (1521)
  - H2: Minor Changes (1523)
  - H2: Moderate Changes (1539)
  - H2: Major Changes (1557)
- H1: Versioning (1584)
  - H2: Version Number Guidance (1605)
    - H3: Patch Revision (1607)
    - H3: Minor Revision (1617)
    - H3: Major Revision (1628)
- H1: Canon Status Labels (1642)
  - H2: Active Canon (1646)
  - H2: Approved Plan (1650)
  - H2: Working Draft (1654)
  - H2: Proposed Revision (1658)
  - H2: Superseded (1662)
  - H2: Archived (1666)
  - H2: Rejected (1670)
- H1: Naming and File Rules (1676)
  - H2: Filenames (1678)
  - H2: Chapter Numbers (1691)
  - H2: Titles (1701)
  - H2: Replaced Files (1710)
- H1: Recommended Workflow Status File (1724)
- H1: Quality Control Gates (1748)
  - H2: Blueprint Gate (1752)
  - H2: Draft Gate (1763)
  - H2: Structural Gate (1772)
  - H2: Continuity Gate (1782)
  - H2: Prose Gate (1792)
  - H2: Canon Gate (1803)
- H1: Common Failure Modes (1814)
  - H2: Loading Too Little Context (1816)
  - H2: Loading Too Much Unfocused Context (1830)
  - H2: Treating the Plot Outline as Finished Prose (1843)
  - H2: Treating a Blueprint as Immutable (1858)
  - H2: Updating Only One Document (1870)
  - H2: Recording Every Detail in the Story Bible (1882)
  - H2: Failing to Separate Belief From Fact (1894)
  - H2: Creating All Blueprints Too Early (1912)
- H1: Recommended Next Documents (1926)
  - H2: 1. Style Guide (1930)
  - H2: 2. Continuity Ledger Template (1936)
  - H2: 3. Research and Plausibility Ledger (1942)
  - H2: 4. Decision Log (1946)
  - H2: 5. Chapter One Blueprint (1950)
- H1: Minimal Document Set for Beginning Chapter One (1958)
- H1: Final Operating Principle (1982)

### Recommended destination(s)

- **Primary (recommended):** `docs/00-governance/novel-development-guide.md` (relocate-intact). Keep the COMPLETE operating guide as an active governance document, per spec Phase 4 "Novel Development Guide" guidance and the "Validation Requirements" item "Confirm the Novel Development and Canon Guide remains available."
- **Derived secondary (later phase, not a split of this file):** `docs/00-governance/context-loading-guide.md` is to be DERIVED from this guide in a later phase, not carved out of it. The derived guide focuses only on: what to read for each task; the authority hierarchy; how to handle contradictions; how to distinguish canon from planning. The full guide stays intact.

### Split decision

**relocate-intact.** Per spec Phase 4, the complete guide stays as one active document at `docs/00-governance/novel-development-guide.md`. Do NOT split this file. A second, shorter `context-loading-guide.md` is authored later by deriving (summarizing) from this guide; that is a new derived document, not a removal of sections from the guide.

Sections that feed the DERIVED `context-loading-guide.md` (source headings whose content is summarized into the derived file; they remain in the full guide):

- "Canon Authority" (line 262), including "Highest Authority" (270) and all "Authority by Subject" H3s (296-394) -> feeds the authority hierarchy.
- "Established Canon Versus Planned Canon" (218) with H2s Established / Planned / Proposed (220, 234, 247) -> feeds the canon-vs-planning distinction.
- "How an AI Should Use the Project" (1265), especially "AI Operating Rules" (1279) and "Required Behavior When a Conflict Appears" (1296) -> feeds how to handle contradictions.
- "Contradiction Resolution Process" (1432) with its seven Step H2s (1436-1483) -> feeds how to handle contradictions.
- "Types of Apparent Contradictions That May Be Intentional" (1485) with its H2s (1489-1517) -> supports contradiction handling (belief vs fact).
- "Task-Specific Context Packages" (1310) plus the per-task H1 blocks "Creating a New Character" (1314), "Creating a New Location" (1329), "Creating a Chapter Blueprint" (1342), "Drafting a Chapter" (1360), "Revising a Chapter" (1374), "Researching a Technical Question" (1389), "Checking Continuity" (1401), "Planning a Sequel" (1415) -> feed what to read for each task. These map conceptually to the future `context-manifests/` task manifests as well.
- "Phase 2: Creating a Chapter Blueprint" required-reading H2s "Always Required" (977), "Also Required" (987), "Sometimes Required" (993) -> feed what to read for the blueprint task.
- "Phase 4: Drafting a Manuscript Chapter" H2s "Essential Context" (1113), "Supporting Context" (1122) -> feed what to read for the drafting task.
- "Canon Status Labels" (1642, H2s 1646-1670) -> supports distinguishing canon states; also relevant to the future `canon-hierarchy.md`.

Note for the orchestrator: the "Canon Authority" + "Canon Status Labels" material is also the natural source for the separate `docs/00-governance/canon-hierarchy.md` target file in spec Phase 2, but spec Phase 4 only mandates relocate-intact for this guide plus a derived context-loading-guide. Whether `canon-hierarchy.md` is also derived from this guide is an orchestrator decision; flagged, not resolved.

### Internal relative Markdown links found

**none.** No `[text](path)` relative Markdown links exist in this file (verified by grep). The file references documents by name and by backtick filename in code blocks (e.g. the "Recommended Project Structure" `text` tree at lines 87-132 and the `narrative-brief.md` style examples under "Naming and File Rules"), but these are illustrative code-block paths in the OLD `canon/`/`planning/` scheme, not clickable links and not paths into the new `docs/` tree.

### Active-or-archive determination

**active.** This is the operating manual and stays active governance. Per spec Phase 4 it is relocate-intact (not archived), and the spec Validation Requirements require it remain available. It is not a source monolith to be split-then-archived; it is moved intact. (For Phase 09 record-keeping the orchestrator may still log an archive copy of the original, but functionally it remains the live guide.)

### Conflicts / ambiguities observed (record only, do not resolve)

- **Old folder scheme inside the guide.** "Recommended Project Structure" (lines 87-132) and "Naming and File Rules" examples describe the OLD `canon/ planning/ chapter-blueprints/ manuscript/ continuity/ research/ archive/` tree, which differs from the master spec Phase 2 `docs/NN-*/` target tree. This is internal documentation that a later phase will need to reconcile when the guide is relocated. Recorded; not resolved here.
- **Canon status label not stated as an explicit status on the document.** The guide has a version (1.0) but no YAML status header. Its own "Canon Status Labels" section exists, but the document does not self-apply one. Recorded as "not stated."
- **Naming conflict for the guide's own filename.** Decision 044's affected-documents and the Log's "Existing Documents Affected" list call this file `novel-development-and-canon-guide.md`, while the spec's target is `novel-development-guide.md`. Minor naming divergence the orchestrator resolves when relocating.

---

## Creative Decision Log.md

- **Title (as stated):** "The Unnecessary" (H1 line 1) with subtitle "Creative Decision Log, Version 1.0" (H2 line 3).
- **Current path:** `/home/codingbutter/Novel/Creative Decision Log.md`
- **Document type:** Support / governance document. Records major creative decisions, rejected concepts, and open questions. Spec target: `docs/00-governance/decision-log/`.
- **Apparent version:** 1.0. Stated both in the H2 subtitle (line 3) and in a YAML metadata block at lines 5-11: `document: "Creative Decision Log"`, `version: "1.0"`, `status: "active support document"`, `last_updated: "2026-06-25"`, `project: "The Unnecessary"`.
- **Canon status:** "active support document" (from the YAML block, line 8). Note this is a support document; the guide states the Decision Log preserves reasoning behind canon and does not itself establish canon.
- **Subject (1-2 lines):** Records the 44 major creative decisions for The Unnecessary, with status legend and entry template, plus catalogs of explicitly rejected concepts, open decisions, the documents the log affects, and the future update procedure.
- **Mermaid blocks:** 0.
- **Total decision entries:** 44 (Decision 001 through Decision 044, contiguous, no gaps; verified by `grep -c '^## Decision [0-9]'` = 44).

### FULL heading outline (every H1 and H2; H3 shown for the legend, template, and decision sub-fields)

- H1: The Unnecessary (1)
  - H2: Creative Decision Log, Version 1.0 (3) [followed by YAML metadata block, lines 5-11]
  - H2: Purpose of This Document (13)
- H1: How to Use This Document (36)
- H1: Decision Statuses (63) [STATUS LEGEND]
  - H2: Locked for Current Draft (65)
  - H2: Active but Revisable (71)
  - H2: Provisional (75)
  - H2: Rejected (79)
  - H2: Superseded (83)
- H1: Decision Entry Template (89) [TEMPLATE]
  - H2: Decision [Number]: [Title] (94) [template skeleton, not a real decision]
    - H3: Decision (100)
    - H3: Previous or Alternative Direction (104)
    - H3: Reason (108)
    - H3: Consequences (112)
    - H3: Affected Documents (116)
    - H3: Reconsider Only If (121)
- H1: Foundational Story Decisions (128) [category H1]
  - H2: Decision 001: The Central Threat Is Economic Irrelevance (130)
  - H2: Decision 002: The World Declines Through Withdrawal, Not One Apocalypse (179)
  - H2: Decision 003: The Ordinary World Remains Visually Recognizable (234)
  - H2: Decision 004: There Is No Universal Name for the Abandoned Population (294)
  - H2: Decision 005: Collapse Is Uneven (344)
- H1: Setting and Social Structure Decisions (392) [category H1]
  - H2: Decision 006: Greater Detroit Is the Primary Setting (394)
  - H2: Decision 007: Northglass Is an Abandoned Asterion Campus (442)
  - H2: Decision 008: Protected Enclaves Are Distributed and Familiar (487)
  - H2: Decision 009: Lakeward Is a Protected Modern Suburb (538)
- H1: Mars Decisions (576) [category H1]
  - H2: Decision 010: Mars Is Still Being Prepared During Book One (578)
  - H2: Decision 011: Mars Is a Network, Not One City (627)
  - H2: Decision 012: Mars Admission Is Personal, Not Merit-Based (665)
  - H2: Decision 013: Mars Can Support More People Than the Gatekeepers Intend to Invite (733)
- H1: Artificial Intelligence Decisions (773) [category H1]
  - H2: Decision 014: Crown Is Not a Simple Villain (775)
  - H2: Decision 015: Morrow Is Created to Coordinate Abandoned Infrastructure (819)
  - H2: Decision 016: Morrow Is Distributed and Resource-Efficient (867)
  - H2: Decision 017: Morrow Has No Direct Viewpoint in Book One (907)
  - H2: Decision 018: Morrow Is Not Automatically Benevolent (952)
  - H2: Decision 019: AI Requires Physical Infrastructure (997)
- H1: Character Decisions (1045) [category H1]
  - H2: Decision 020: Eli Is Complicit, Not an Early Whistleblower (1047)
  - H2: Decision 021: Eli's Core Conflict Is Responsibility Versus Ownership (1090)
  - H2: Decision 022: Jonah's Betrayal Is Understandable but Not Excused (1127)
  - H2: Decision 023: Kade Is Rational, Cultured, and Dangerous (1168)
  - H2: Decision 024: Lena Is a Moral Counterweight, Not the Automatic Moral Authority (1211)
  - H2: Decision 025: June Does Not Represent Automatic Youthful Wisdom (1247)
  - H2: Decision 026: The Protected Wealthy Are Also Vulnerable to Exclusion (1281)
- H1: Plot and Structure Decisions (1320) [category H1]
  - H2: Decision 027: Book One Takes Place in 2053 (1322)
  - H2: Decision 028: Book One Covers Thirty Days (1361)
  - H2: Decision 029: Book One Has 36 Chapters and No Prologue (1395)
  - H2: Decision 030: The Novel Uses Close Third Person With Multiple Viewpoints (1433)
  - H2: Decision 031: Morrow's First Major Moral Violation Is Manipulation, Not Violence (1471)
  - H2: Decision 032: Kade Offers Eli Six Total Mars Seats (1508)
  - H2: Decision 033: Asterion Uses Pressure Before Open Force (1543)
  - H2: Decision 034: Morrow Refuses Eli's Erasure Command (1587)
  - H2: Decision 035: Morrow Survives Through Distribution (1628)
  - H2: Decision 036: The Final Message Is "You Were Never Unnecessary." (1666)
- H1: Style and Tone Decisions (1710) [category H1]
  - H2: Decision 037: The Tone Is Serious, Restrained, and Morally Ambiguous (1712)
  - H2: Decision 038: Avoid Exaggerated Cyberpunk Aesthetics (1747)
  - H2: Decision 039: Avoid Em Dashes in Drafted Prose and Project Copy (1782)
- H1: Workflow Decisions (1812) [category H1]
  - H2: Decision 040: The Project Uses Separate Specialized Documents (1814)
  - H2: Decision 041: Chapter Blueprints Are Created One Chapter at a Time (1860)
  - H2: Decision 042: The Chapter Blueprint Template Guides Planning, Not Prose (1907)
  - H2: Decision 043: Another AI Does Not Need the Original Conversation (1964)
  - H2: Decision 044: mem0 Knowledge Graph Is On, With the Bibles as Higher Authority (2017)
- H1: Explicitly Rejected Concepts (2063)
  - H2: Rejected Setting Concepts (2067)
  - H2: Rejected Social Concepts (2076)
  - H2: Rejected Mars Concepts (2085)
  - H2: Rejected AI Concepts (2095)
  - H2: Rejected Character Concepts (2105)
  - H2: Rejected Plot Concepts (2114)
- H1: Open Decisions (2125)
  - H2: Book and Series Naming (2129)
  - H2: Mars Details (2135)
  - H2: Morrow (2143)
  - H2: Character Arcs (2151)
  - H2: Structure (2161)
- H1: Existing Documents Affected by This Log (2171)
- H1: Future Update Procedure (2188)
- H1: Final Principle (2207)

Each Decision H2 (001-044) contains the standard sub-field H3 set, drawn from the entry template: `### Decision`, optionally `### Previous or Alternative Direction` (present on some entries only), `### Reason`, `### Consequences`, `### Affected Documents`, `### Reconsider Only If`. Decision 043 additionally has `### Requirements` (line 1977). Each entry also carries bold `**Status:**` and `**Category:**` lines (Decision 001 also adds a `**Date:**` line only in the template, not in real entries; real entries omit `**Date:**`).

### ENUMERATED decision list (number | exact title | status | category H1 it sits under)

The "Status" below is the per-entry `**Status:**` line value. The "Category H1" is the `# <...> Decisions` heading the entry sits under (this is the structural category for index grouping). Each entry also has its own free-text `**Category:**` line, given in parentheses.

Foundational Story Decisions:
- 001 | The Central Threat Is Economic Irrelevance | Locked for Current Draft | Foundational Story (Category: Theme and premise)
- 002 | The World Declines Through Withdrawal, Not One Apocalypse | Locked for Current Draft | Foundational Story (Category: Worldbuilding and tone)
- 003 | The Ordinary World Remains Visually Recognizable | Locked for Current Draft | Foundational Story (Category: Setting and visual identity)
- 004 | There Is No Universal Name for the Abandoned Population | Locked for Current Draft | Foundational Story (Category: Social worldbuilding)
- 005 | Collapse Is Uneven | Locked for Current Draft | Foundational Story (Category: Worldbuilding)

Setting and Social Structure Decisions:
- 006 | Greater Detroit Is the Primary Setting | Active but Revisable | Setting and Social Structure (Category: Location)
- 007 | Northglass Is an Abandoned Asterion Campus | Locked for Current Draft | Setting and Social Structure (Category: Location and technology)
- 008 | Protected Enclaves Are Distributed and Familiar | Locked for Current Draft | Setting and Social Structure (Category: Social worldbuilding)
- 009 | Lakeward Is a Protected Modern Suburb | Active but Revisable | Setting and Social Structure (Category: Location)

Mars Decisions:
- 010 | Mars Is Still Being Prepared During Book One | Locked for Current Draft | Mars (Category: Worldbuilding and plot)
- 011 | Mars Is a Network, Not One City | Locked for Current Draft | Mars (Category: Mars worldbuilding)
- 012 | Mars Admission Is Personal, Not Merit-Based | Locked for Current Draft | Mars (Category: Theme and social structure)
- 013 | Mars Can Support More People Than the Gatekeepers Intend to Invite | Locked for Current Draft | Mars (Category: Theme, plot, and technology)

Artificial Intelligence Decisions:
- 014 | Crown Is Not a Simple Villain | Locked for Current Draft | Artificial Intelligence (Category: Character and AI)
- 015 | Morrow Is Created to Coordinate Abandoned Infrastructure | Locked for Current Draft | Artificial Intelligence (Category: AI origin and plot)
- 016 | Morrow Is Distributed and Resource-Efficient | Locked for Current Draft | Artificial Intelligence (Category: Technology)
- 017 | Morrow Has No Direct Viewpoint in Book One | Locked for Current Draft | Artificial Intelligence (Category: Narrative structure)
- 018 | Morrow Is Not Automatically Benevolent | Locked for Current Draft | Artificial Intelligence (Category: Theme and AI characterization)
- 019 | AI Requires Physical Infrastructure | Locked for Current Draft | Artificial Intelligence (Category: Technology)

Character Decisions:
- 020 | Eli Is Complicit, Not an Early Whistleblower | Locked for Current Draft | Character (Category: Character)
- 021 | Eli's Core Conflict Is Responsibility Versus Ownership | Locked for Current Draft | Character (Category: Character and theme)
- 022 | Jonah's Betrayal Is Understandable but Not Excused | Locked for Current Draft | Character (Category: Character and plot)
- 023 | Kade Is Rational, Cultured, and Dangerous | Locked for Current Draft | Character (Category: Character)
- 024 | Lena Is a Moral Counterweight, Not the Automatic Moral Authority | Locked for Current Draft | Character (Category: Character)
- 025 | June Does Not Represent Automatic Youthful Wisdom | Locked for Current Draft | Character (Category: Character)
- 026 | The Protected Wealthy Are Also Vulnerable to Exclusion | Locked for Current Draft | Character (Category: Character and social structure)

Plot and Structure Decisions:
- 027 | Book One Takes Place in 2053 | Active but Revisable | Plot and Structure (Category: Timeline)
- 028 | Book One Covers Thirty Days | Locked for Current Draft | Plot and Structure (Category: Plot structure)
- 029 | Book One Has 36 Chapters and No Prologue | Active but Revisable | Plot and Structure (Category: Structure)
- 030 | The Novel Uses Close Third Person With Multiple Viewpoints | Locked for Current Draft | Plot and Structure (Category: Narrative structure)
- 031 | Morrow's First Major Moral Violation Is Manipulation, Not Violence | Locked for Current Draft | Plot and Structure (Category: Plot and theme)
- 032 | Kade Offers Eli Six Total Mars Seats | Active but Revisable | Plot and Structure (Category: Plot)
- 033 | Asterion Uses Pressure Before Open Force | Locked for Current Draft | Plot and Structure (Category: Plot and institutional behavior)
- 034 | Morrow Refuses Eli's Erasure Command | Locked for Current Draft | Plot and Structure (Category: Climax)
- 035 | Morrow Survives Through Distribution | Locked for Current Draft | Plot and Structure (Category: Ending)
- 036 | The Final Message Is "You Were Never Unnecessary." | Active but Revisable | Plot and Structure (Category: Ending and theme)

Style and Tone Decisions:
- 037 | The Tone Is Serious, Restrained, and Morally Ambiguous | Locked for Current Draft | Style and Tone (Category: Tone)
- 038 | Avoid Exaggerated Cyberpunk Aesthetics | Locked for Current Draft | Style and Tone (Category: Style and setting)
- 039 | Avoid Em Dashes in Drafted Prose and Project Copy | Active but Revisable | Style and Tone (Category: Style preference)

Workflow Decisions:
- 040 | The Project Uses Separate Specialized Documents | Locked for Current Workflow | Workflow (Category: Project organization)
- 041 | Chapter Blueprints Are Created One Chapter at a Time | Locked for Current Workflow | Workflow (Category: Planning)
- 042 | The Chapter Blueprint Template Guides Planning, Not Prose | Locked for Current Workflow | Workflow (Category: Planning)
- 043 | Another AI Does Not Need the Original Conversation | Locked for Current Workflow | Workflow (Category: AI handoff)
- 044 | mem0 Knowledge Graph Is On, With the Bibles as Higher Authority | Locked for Current Workflow | Workflow (Category: Workflow and tooling)

### Recommended destination(s)

Per spec Phase 4 "Decision Log" and Phase 2 target tree:

- **Index:** `docs/00-governance/decision-log/index.md` (new index table: number, title, status, category, short summary, file link). Spec Phase 4 mandates this index table.
- **One file per decision:** `docs/00-governance/decision-log/decisions/NNN-slug.md`, three-digit zero-padded number plus kebab-case slug derived from the title. Examples (slugs are recommended, orchestrator finalizes):
  - `001-central-threat-is-economic-irrelevance.md`
  - `002-decline-through-withdrawal.md`
  - `003-recognizable-ordinary-world.md`
  - ... through 044.
- **Status legend + entry template:** see split-decision below for placement.
- **Rejected / Open / Affected / Update-procedure tail material:** see split-decision below.

### Split decision

**split.** Per spec Phase 4, split each decision into its own file plus an index table. Proposed heading boundaries:

1. Front matter and orientation -> `docs/00-governance/decision-log/index.md` (intro/purpose portion).
   - H1 "The Unnecessary" + H2 "Creative Decision Log, Version 1.0" (lines 1-11, includes YAML metadata block) -> index header.
   - H2 "Purpose of This Document" (13-34) -> index purpose section.
   - H1 "How to Use This Document" (36-60) -> index usage section.
2. Status legend -> recommended `docs/00-governance/decision-log/index.md` (a "Decision Statuses" subsection) OR a small adjacent `status-legend` block. Boundary: H1 "Decision Statuses" (63) with its five H2s (65-87): Locked for Current Draft, Active but Revisable, Provisional, Rejected, Superseded.
3. Entry template -> recommended a template file such as `docs/00-governance/decision-log/decision-entry-template.md`, or place it under `docs/40-blueprints/_templates/`-style template handling per orchestrator. Boundary: H1 "Decision Entry Template" (89) with H2 "Decision [Number]: [Title]" (94) and its six H3 sub-fields (100-124). This is a skeleton, not a real decision; it must NOT become `001-*.md`.
4. Each decision entry -> its own `NNN-slug.md`. Boundary per entry: from its `## Decision NNN: ...` H2 to just before the next `## Decision` H2 (or the next category H1). The category H1 it sits under (Foundational Story / Setting and Social Structure / Mars / Artificial Intelligence / Character / Plot and Structure / Style and Tone / Workflow) becomes the entry's `category` field in the index and front matter. The eight category H1 headings themselves (lines 128, 392, 576, 773, 1045, 1320, 1710, 1812) become index groupings, not standalone files.
5. Tail reference material -> recommended into the decision-log index or adjacent governance files (orchestrator decides; preserve verbatim, do not lose):
   - H1 "Explicitly Rejected Concepts" (2063) with H2s 2067-2123 -> keep easy to locate (spec: "Keep rejected concepts easy to locate"). Recommended `docs/00-governance/decision-log/rejected-concepts.md` or an index subsection.
   - H1 "Open Decisions" (2125) with H2s 2129-2168 -> recommended `docs/00-governance/decision-log/open-decisions.md` or index subsection.
   - H1 "Existing Documents Affected by This Log" (2171-2185) -> recommended index subsection; note its backtick paths use the OLD folder scheme (see conflicts).
   - H1 "Future Update Procedure" (2188-2205) -> recommended index subsection.
   - H1 "Final Principle" (2207-2218) -> recommended index subsection.

Heading-coverage guarantee: every H1 and H2 above maps to a destination (per-decision file, index, template file, or tail file). No heading is left unmapped.

### Internal relative Markdown links found

**none.** No `[text](path)` relative Markdown links exist in this file (verified by grep). However, "Existing Documents Affected by This Log" (lines 2173-2182) lists eight backtick path mentions that point at the OLD folder scheme and would need updating when files move:
- `canon/narrative-brief.md`
- `canon/story-bible.md`
- `canon/character-bible.md`
- `canon/world-and-technology-rules.md`
- `canon/master-timeline.md`
- `planning/plot-outline-and-chapter-map.md`
- `chapter-blueprints/_chapter-blueprint-template.md`
- `novel-development-and-canon-guide.md`
These are text references inside a code-style list, not clickable links, and none resolves to the new `docs/` tree. Recorded for later link-update phase; not fixed here.

### Active-or-archive determination

**archive-after-split.** The Log is the monolithic source for the per-decision files. Once split into `decisions/NNN-slug.md` plus index (and verified complete, all 44 represented), the original monolith is archived in Phase 09 to `archive/source-monoliths/`. Until then it stays active. The split content remains the active authority. (Spec Validation Requirement: "Confirm the Creative Decision Log remains fully represented.")

### Conflicts / ambiguities observed (record only, do not resolve)

- **Status-label set mismatch.** The "Decision Statuses" legend (lines 63-87) defines exactly five labels: Locked for Current Draft, Active but Revisable, Provisional, Rejected, Superseded. But decisions 040-044 use the label "Locked for Current Workflow" (lines 1816, 1862, 1909, 1966, 2019), which is NOT in the legend. Conversely, the labels Provisional, Rejected, and Superseded are defined but used by zero current decision entries. Recorded as an ambiguity for the orchestrator; the index/legend may need reconciliation in a later phase. Not resolved here.
- **Per-entry "Category" line vs structural category H1.** Each decision has a free-text `**Category:**` line (e.g. "Theme and premise", "Location and technology") that does not always match the `# ... Decisions` category H1 it sits under (e.g. Decision 001 sits under "Foundational Story Decisions" but its Category line reads "Theme and premise"). A later split phase must decide which value populates the index "Category" column. Both are preserved above. Not resolved here.
- **Old folder scheme in "Existing Documents Affected."** The eight backtick paths (lines 2175-2182) reference `canon/`, `planning/`, `chapter-blueprints/`, not the spec `docs/` tree, and use the guide filename `novel-development-and-canon-guide.md` (spec target is `novel-development-guide.md`). Link/path reconciliation deferred to a later phase.
- **Template H2 "Decision [Number]: [Title]" matches the real-decision heading pattern.** A naive `^## Decision` split would capture the template skeleton (line 94) as if it were a decision. The split phase must exclude the template (it has no number) so it does not become `001-*.md`. Flagged so the splitter excludes it.
- **`**Date:**` field appears in the template but is omitted from all 44 real entries.** The template (line 96) shows a `**Date:**` line; no real entry carries a date. Recorded so the per-decision front matter does not invent dates (the only date present is `last_updated: "2026-06-25"` in the top YAML block). Do not invent per-decision dates.
- **No conflict between the two governance docs themselves was found** beyond the guide-filename naming divergence noted above. The Guide describes the Decision Log's role; the Log describes itself consistently with that role.

---

## Memory candidates

- The Creative Decision Log (The Unnecessary) contains exactly 44 decisions numbered 001 through 044, contiguous with no gaps, grouped under 8 category H1 headings: Foundational Story, Setting and Social Structure, Mars, Artificial Intelligence, Character, Plot and Structure, Style and Tone, Workflow. {type: fact, tags: [decision-log, migration, governance]}
- Decision Log status mismatch (continuity hazard): the "Decision Statuses" legend defines five labels (Locked for Current Draft, Active but Revisable, Provisional, Rejected, Superseded) but Decisions 040 through 044 use an undefined sixth label "Locked for Current Workflow"; and Provisional, Rejected, Superseded are defined yet unused by any entry. {type: hazard, tags: [decision-log, migration, status-labels]}
- Migration plan (spec Phase 4): the Development and Canon Guide is relocate-intact to docs/00-governance/novel-development-guide.md and is NOT split; a shorter context-loading-guide.md is to be DERIVED from it later (covering what to read per task, authority hierarchy, contradiction handling, canon-vs-planning). {type: decision, tags: [migration, governance, context-loading-guide]}
- Migration plan (spec Phase 4): the Creative Decision Log splits into one file per decision at docs/00-governance/decision-log/decisions/NNN-slug.md plus an index table (number, title, status, category, summary, link); the entry template (line 94, has no number) must be excluded from the per-decision split so it does not become 001. {type: decision, tags: [migration, decision-log, split]}
- Continuity hazard in the Decision Log: the "Existing Documents Affected by This Log" list and Decision 044 reference the OLD folder scheme (canon/, planning/, chapter-blueprints/) and the guide filename novel-development-and-canon-guide.md, which diverge from the spec docs/ tree and target name novel-development-guide.md; these need link/path reconciliation in a later phase. {type: continuity, tags: [migration, links, decision-log]}
- The Development and Canon Guide contains exactly one Mermaid block (the layered-system flowchart under "Core Principle"); the Creative Decision Log contains zero Mermaid blocks. {type: fact, tags: [migration, mermaid, governance]}
- Neither governance document contains any clickable relative Markdown links; references are by name or backtick path inside code-style lists only. {type: fact, tags: [migration, links, governance]}
