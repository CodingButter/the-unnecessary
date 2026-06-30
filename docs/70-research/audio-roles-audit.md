---
title: "Crew vs Industry Roles Audit (Audio Production)"
document_type: "research"
status: "reference"
authority: "research-grounding"
summary: "Companion to the book-production roles audit, covering the AUDIO side the first pass deferred: maps our five audio agents and the live-audio pipeline against the standard roles of single-narrator audiobook production and full-cast audio-drama, surfacing prioritized GAPS (audio roles we lack), OVERLOADED agents (one agent wearing 2+ audio roles), OVER-FRAGMENTED cases, and where local-model rendering and canon-locked voice design make our structure better than the industry default. A recommendation for the author to review; changes no agent files."
tags:
  - research
  - crew
  - roles-audit
  - audio
  - audiobook
  - audio-drama
  - pipeline
  - process
source: "Industry research (cited inline; Karen Commins, Pozotron, Penguin, ACX/Audible, NarrationBox, APA, SAG-AFTRA, et al.) cross-referenced against the live audio crew inventory under .claude/agents/ and the live-audio pipeline scripts. Synthesis only; no agent files changed."
related:
  - "./crew-roles-audit.md"
  - "../../.claude/agents/audiobook-director.md"
  - "../../.claude/agents/live-narration-director.md"
  - "../../.claude/agents/sound-engineer.md"
  - "../../.claude/agents/voice-designer.md"
  - "../../.claude/agents/portrait-renderer.md"
source_documents:
  - "CLAUDE.md"
  - ".claude/agents/"
  - "scripts/narrate-chapter.py"
  - "scripts/render-voice-stems.py"
  - "scripts/normalize-stems.py"
  - "scripts/mix-live-scene.py"
  - "scripts/verify-narration.py"
  - "scripts/voice-design.py"
---

# Crew vs Industry Roles Audit (Audio Production)

> Scope note. This is the companion the book-production audit (`./crew-roles-audit.md`)
> explicitly deferred: that pass exhausted its synthesis budget on the literary
> craft/editorial chain and flagged every audio agent as "out of cited scope." This
> document closes that gap, against fresh cited research on two audio domains:
> single-narrator audiobook production and full-cast audio-drama / dramatized-audiobook
> production. It audits the five audio-adjacent agents (audiobook-director,
> live-narration-director, sound-engineer, voice-designer, and the visual sibling
> portrait-renderer) and the live-audio pipeline. It recommends; it changes no agent file.

## What is structurally different about our audio production

Two facts reshape every industry role below, and they must be stated first or the audit
mis-grades the whole crew.

1. **The narrator is a LOCAL voice model, not a hired human.** Cost is power, not tokens or
   studio hours. The single most expensive, least-reversible error in human audiobook
   production, a miscast or misreading narrator that forces re-recording the whole title, is
   for us nearly free to redo. A full chapter or book re-render is a routine act, not a
   budget event. This collapses or de-fangs an entire column of industry roles whose job is
   to PREVENT expensive re-records.
2. **There is no microphone capture.** TTS has no room tone, mic distance, clipping, mouth
   clicks, or gaspy breaths. The whole Recording/Session-Engineer failure class and roughly
   half of the audio Editor's de-noise remit simply do not exist for us. The trade is that
   TTS substitutes its OWN failure class, a confident, clean, WRONG read (a dropped line, a
   garbled name, a homograph said the wrong way), which moves the risk from capture quality
   to output VERIFICATION. Hold that thought; it is the largest gap below.

We ship TWO audio products from one frozen-prose spine: a plain single-narrator chapter
audiobook (audiobook-director authors the TTS performance script consumed by
`scripts/narrate-chapter.py`) and a full-cast LIVE / dramatized edition (live-narration-director
authors a per-scene cue sheet, every line rendered in-character on the local voice server,
sound-engineer owns music/SFX/mix design, mixed by `scripts/mix-live-scene.py`).

## Crew-to-industry crosswalk (the audio agents)

| Agent | Closest audio industry role(s) | Coverage |
|---|---|---|
| audiobook-director | Audiobook Director + Script-Prep/Pronunciation (single-narrator edition) | Covered |
| live-narration-director | Adapter/Dramatist + Director + ensemble Casting + line Producer (live edition) | Covered, overloaded (see 2) |
| sound-engineer | Sound Designer + Composer + Re-recording/Mix Engineer + Mastering TARGETS | Covered, one separable seam (see 2) |
| voice-designer | Voice/character design (single voice in isolation), NOT ensemble casting | Covered (partial; see 1.2) |
| portrait-renderer | Visual asset production (NOT an audio role; listed as voice-designer's sibling) | Out of audio scope |
| (none) | **Prooflistener / audio QC** (rendered audio vs script) | **GAP (see 1.1)** |
| (none) | **Casting Director** (the ensemble as a SET) | **GAP (see 1.2)** |
| (none) | **Mastering Engineer** (book-level loudness uniformity) | **GAP (see 1.3)** |
| (machine) | Narrator | The local voice model |
| process / human | Commissioning editor, Producer, Ops coordinator, Music supervisor, Platform QA | Externalized |

The honest headline: on the audio side the risk is GAPS, not redundancy. The crew is lean.
Where the book side was richly staffed with diagnosers, the audio side has strong AUTHORING
(direction, adaptation, voice design, mix design) and almost no VERIFICATION or
cast-as-a-whole ownership.

---

## 1. GAPS: proven audio roles with NO agent (candidate HIRES)

### 1.1 Prooflistener / audio QC of the RENDERED output  [PRIORITY: HIGH]
- Industry role: **Prooflistener / Quality Control** [Karen Commins; Book Riot; davebooks QC].
  Listens to the full recording WHILE reading the manuscript and flags every deviation:
  misreads, dropped or doubled words, missing lines, mispronunciations, and especially
  pronunciation INCONSISTENCY between chapters, producing a timestamped pickup list.
- What it would catch/add: the one error class invisible to everyone who is not listening
  against the text. For us this is the native TTS failure mode, a clean confident render
  that says the wrong but plausible word, drops a clause, swallows a line, says a number or a
  homograph wrong, or pronounces "Asterion" or "Aurelia" one way in chapter two and another
  in chapter nine. None of our current gates touch this. The audiobook-director's
  tag-strip-and-diff verifies the SCRIPT matches the manuscript (text vs text), and the
  Gemini fidelity gate critiques the live cue SHEET against the prose (text vs text). Neither
  listens to the produced AUDIO. The script can be perfect and the render still wrong.
- How it fits our pipeline: a terminal **prooflistener** pass that runs AFTER render, against
  the script and the canon pronunciation list, emitting a timestamped re-roll list that
  routes back to whichever agent owns that line (audiobook-director for the single-narrator
  edition, live-narration-director for a live scene). It should build on `scripts/verify-narration.py`,
  which already exists as the natural hook for an automated audio-vs-text check. Because our
  re-rolls are cheap (local model), a precise pickup list is high-leverage: the fix is nearly
  free once the defect is NAMED.
- Could an existing audio agent absorb it? No, by construction. The value of a proofer is a
  second set of ears that did NOT perform the take; live-narration-director and
  audiobook-director cannot QC their own renders without the familiarity blindness the role
  exists to defeat. This is the single highest-value audio hire.

### 1.2 Casting Director, the ensemble as a SET (distinct from voice-designer)  [PRIORITY: HIGH]
- Industry role: **Casting Director** [Backstage; Barnes & Noble full-cast feature; NarratorList].
  Translates the book into a voice spec, then casts the whole ensemble so characters are
  instantly tellable apart by ear, with deliberate spread of age, register, and timbre and
  chemistry across the cast.
- What it would catch/add: full-cast audio lives or dies on voice DISTINCTIVENESS across the
  ensemble, and nobody owns the ensemble today. voice-designer designs ONE voice from ONE
  profile in isolation (`scripts/voice-design.py`, three previews, canon-locked). It never
  asks "do these two characters sound too alike in a two-hander," "is the register spread
  across the whole cast wide enough," or "is this character's voice the same in chapter nine
  as in chapter one." live-narration-director only PROVISIONS what already exists ("ensure
  every speaking voice is on the server; never invent a voice"). So the cast falls into a
  seam: voice-designer designs each voice blind to the others, live-narration-director
  consumes whatever is there, and no role decides or audits the cast as a whole.
- How it fits our pipeline: a **casting-director** role that owns the cast SHEET, who gets a
  voice, the deliberate contrast map (so no two co-present speakers collide), and
  cross-chapter voice consistency. It briefs voice-designer (which voices to design and to
  what contrast target) and signs off the ensemble before live scenes render. This is the
  natural home for the casting function currently smeared across two agents and a seam.
- Could an existing audio agent absorb it? Partially, and that is exactly the OVERLOAD in 2.1.
  The cleanest move is to LIFT ensemble casting out of live-narration-director rather than
  pile it onto voice-designer, whose remit is deliberately one-voice and reveal-safe.

### 1.3 Mastering Engineer, book-level loudness and spec uniformity  [PRIORITY: MED-HIGH]
- Industry role: **Mastering Engineer** [NarrationBox ACX/LUFS guide; ACX mastering with Alex;
  ACX producer checklist]. Final technical polish across the WHOLE title: consistent loudness,
  true-peak ceiling, noise floor, and uniform per-file masters so the listener never hits a
  loudness jump, with strict platform-spec compliance.
- What it would catch/add: consistency ACROSS the book, not within a scene. sound-engineer
  owns loudness/LUFS, true-peak, and master-chain TARGETS and the per-scene mix;
  `scripts/normalize-stems.py` normalizes within a scene; `scripts/mix-live-scene.py` mixes one
  scene. Nobody owns the title-level pass that makes every scene and chapter sit at the same
  perceived loudness and emits one spec-compliant deliverable for the whole book. Per-scene
  mixing done well still leaves scene-to-scene loudness drift, the exact thing mastering
  exists to remove, and the industry's most common rejection cause (noise floor and loudness
  inconsistency) maps directly onto our multi-scene, multi-chapter assembly.
- How it fits our pipeline: a book-level **mastering** pass that runs after all scenes/chapters
  render, measuring integrated loudness per file and applying one uniform correction plus a
  final true-peak ceiling, producing the deliverable masters. It is a different TIMING (after
  everything exists) and a different OBJECTIVE (uniformity, not this scene's balance) from
  sound-engineer's per-scene design.
- Could an existing audio agent absorb it? Yes, most naturally sound-engineer, IF its remit is
  explicitly extended from per-scene mix to a title-level master with the book-wide loudness
  target as its own deliverable. The watch-item (see 2.2) is to not let "I balanced each
  scene" be mistaken for "the book is mastered." A thin dedicated mastering role is the
  alternative if sound-engineer's plate is full.

### 1.4 Dialogue editor / take-assembly quality  [PRIORITY: MED]
- Industry role: **Audio / Sound Editor** [Pozotron; common-mode post-production]. Selects best
  takes, fixes pacing and inter-sentence gaps, and drops re-recorded pickups in invisibly.
- What it would catch/add: with TTS the click/breath/de-noise half of this role evaporates (a
  structural win, see below), but the OTHER half is real: choosing the best of several re-rolls,
  fixing pacing and gap length between lines, and making a re-rolled pickup sit seamlessly next
  to its neighbors. live-narration-director already re-rolls by ear with --only/--role, which
  is take-selection by another name, so the function is partially present but informal and
  per-scene.
- Could an existing audio agent absorb it? Yes. Fold the take-assembly judgment into the
  prooflistener's pickup list (1.1) plus live-narration-director's existing re-roll loop. Not a
  separate hire at our scale; rated MED and parked behind 1.1.

### 1.5 Script-prep / pronunciation LEXICON owner (cross-book consistency)  [PRIORITY: MED]
- Industry role: **Script-Prep / Pronunciation Researcher** [Karen Commins; Penguin audiobook
  roles]. Builds the pronunciation guide (names, places, invented and technical terms) before
  record so the narrator and director are not solving them live.
- What it would catch/add: today pronunciation prep is distributed and per-edition,
  live-narration-director authors a per-scene "tts" field (heteronyms, numbers and years spelled
  out), audiobook-director does its own pronunciation pass. Nobody owns a single project-wide
  pronunciation LEXICON, so "Mosaic," "Asterion," "Aurelia," "Morrow," and "Kade" are re-decided
  per scene and can drift. This is the same consistency theme as 1.1 and 1.3, front-loaded.
- Could an existing agent absorb it? Best move is cross-product: fold an owned pronunciation
  lexicon into the BOOK-side copy-editor's style sheet (a gap the companion audit already
  recommends hiring), and have both audio editions read from it. One lexicon, two consumers.

### 1.6 Externalized-by-design roles (no hire)  [PRIORITY: LOW]
- **Commissioning / Acquiring editor, Showrunner / Exec producer, Line producer, Title /
  ops coordinator**: the strategic "should this exist, on this budget, in this form" and the
  scheduling/packaging functions live with the human author and the orchestration skills
  (`/live-audiobook` and the pipeline scripts). Process-as-code, not a missing agent.
- **Music supervisor**: its core function is rights/clearance, which is largely moot because we
  GENERATE music and SFX (ElevenLabs endpoints), incurring no licensing liability. A structural
  win, not a gap.
- **Platform / Retailer QA (ACX/Audible)**: an external gate that only exists once we distribute.
  Not applicable now; when it is, `scripts/verify-narration.py` plus the mastering pass (1.3)
  become the internal stand-in.
- **Accent / dialect coach, Script/story editor**: engaged ad hoc in industry; covered for us
  by voice-designer's prep, live-narration-director's adaptation, and the Gemini fidelity gate.

---

## 2. OVERLOADED: audio agents wearing 2+ distinct roles (candidate SPLITS)

### 2.1 live-narration-director  [SPLIT: lift CASTING out; keep adapter+director together]
- Distinct industry roles it wears: (a) **Adapter / Dramatist** (prose to cues.json, writing for
  the ear, narrator says only what cannot be heard); (b) **Director** (per-line performance
  tuning, reveal-safe tone, pacing); (c) **ensemble Casting** (voice provisioning and de-facto
  assignment); (d) **line Producer** (running render -> normalize -> mix). The sound-engineer
  already carved sound design and mix off this agent, a healthy precedent.
- Assessment: the ADAPTER and DIRECTOR functions share one "make this scene play as heard drama"
  mind and one toolchain; splitting them would cut a single creative act in half. Keep combined.
  The PRODUCER function is just executing mechanical scripts; harmless to keep. The genuinely
  different lens is CASTING: deciding and auditing the cast as a SET (whole-ensemble
  distinctiveness, cross-chapter voice consistency) is a different altitude from directing THIS
  scene's performance, and it is precisely the unowned seam in 1.2.
- Recommendation: do NOT split adapter from director. DO lift ensemble casting out into the
  casting-director role (1.2), which then briefs voice-designer and signs off the cast before
  live scenes render. This is the top real split on the audio side, and it is the same kind of
  clean carve-out that worked when sound-engineer was split off.

### 2.2 sound-engineer  [SPLIT: NO; one watch-item on mastering]
- Distinct roles it wears: **Sound Designer** + **Composer** + **Re-recording/Mix Engineer** +
  **Mastering (targets)**. Like the book side's four-agent continuity system, these read as
  several jobs but are one coherent chair, everything under and around the voice, sharing one
  craft and one control surface (the cues.json schema and the mixer it owns).
- The one separable piece is BOOK-LEVEL MASTERING (1.3): per-scene mix and whole-title master
  differ in timing and objective. Recommendation: keep the chair intact, but make the title-level
  master an EXPLICIT deliverable of this agent (or a thin dedicated mastering pass) so per-scene
  balance is never mistaken for a mastered book.

### 2.3 audiobook-director  [SPLIT: NO]
- It wears **Director** (single-narrator performance markup) plus a sliver of **Script-Prep**
  (its own pronunciation and tag discipline) and a sliver of fidelity-proofing (the
  tag-strip-and-diff against the manuscript). These are one tight single-edition job. The text
  diff is SCRIPT-vs-manuscript fidelity, NOT audio QC, so it does not secretly cover 1.1. Keep.

Top split-candidate to name: **live-narration-director**, by lifting ENSEMBLE CASTING out (2.1).

---

## 3. OVER-FRAGMENTED: several agents on ONE audio role (candidate MERGES)

The honest finding: there is no audio over-fragmentation to merge. The audio chain is lean and,
if anything, UNDER-staffed (the gaps in section 1), the opposite of the book side's rich
diagnoser bench.

- voice-designer and portrait-renderer are siblings by MECHANISM (both render a derived artifact
  from a canon profile) but are different industry roles (voice/casting vs visual). Not one role,
  not a merge. portrait-renderer is not an audio role at all and is excluded from the audio count.
- voice-designer (design one voice) + live-narration-director (provision and perform) +
  sound-engineer (everything under the voice) are three DISTINCT roles, not three agents doing
  one role. No merge.
- No merge recommended anywhere on the audio side.

---

## Prioritized recommendation (highest-value audio moves)

1. **HIRE an audio prooflistener / QC** that listens to the RENDERED output against the script
   and the canon pronunciation list and emits a timestamped re-roll list, built on
   `scripts/verify-narration.py`. This closes the native TTS failure mode (clean-but-wrong reads,
   dropped lines, inconsistent name pronunciation) that NO current gate touches. Highest-value
   because our re-rolls are nearly free once the defect is named. [HIGH]
2. **CARVE OUT a casting director** (the ensemble as a SET, distinct from voice-designer) by
   lifting ensemble casting out of live-narration-director. Owns cast distinctiveness,
   the contrast map, and cross-chapter voice consistency; briefs voice-designer and signs off the
   cast before live scenes render. [HIGH]
3. **ESTABLISH a book-level MASTERING pass** for loudness and spec uniformity across all scenes
   and chapters, as an explicit deliverable of sound-engineer (or a thin dedicated role). Distinct
   in timing and objective from per-scene mixing. [MED-HIGH]
4. **OWN a cross-book pronunciation LEXICON**, folded into the book-side copy-editor's style sheet
   and read by both audio editions, so invented names are said the same everywhere. [MED]
5. **Resist over-splitting.** Keep adapter+director together in live-narration-director and keep
   sound-design+mix together in sound-engineer. The audio risk is gaps, not fragmentation; do not
   merge or further fragment the existing chain. [structural]

## Where our audio structure is BETTER than the industry default (do not "fix")

- **Local-model narration inverts the cost of error.** The industry's single most expensive,
  least-reversible failure, a miscast or misreading narrator forcing a full re-record, is for us
  a routine, near-free re-render. This is why a precise QC pickup list (rec 1) is so high-leverage
  and why our whole-book re-renders are practical. [vs ACX narrator-producer economics]
- **No dirty capture is possible.** TTS has no mic noise, room tone, clipping, mouth clicks, or
  breaths, so the entire Recording/Session-Engineer failure class and half the Editor's de-noise
  work do not exist. The trade is a NEW failure class (confident misreads), which rec 1 targets.
  [vs Pozotron/common-mode capture-and-edit chain]
- **Canon-locked voice design.** voice-designer reads age, heritage, and persona straight from the
  canon profile and is reveal-safe, so a character's voice is derived from the same single source
  as the prose and cannot drift from canon the way an independently-cast human narrator can.
  [vs Backstage casting-from-audition model]
- **Generated music and SFX remove the rights function.** Because score and effects are generated,
  the Music Supervisor's licensing/clearance liability is largely moot. [vs audio-drama music
  supervision]
- **Two editions from one frozen-prose spine.** The single-narrator and full-cast editions both
  derive from the same approved prose, an alignment industry productions do not get for free.
- **Mix design is a CONTROL SURFACE owned as code.** The cues.json schema and the mixer that
  sound-engineer owns make the mix reproducible and inspectable, closer to process-as-code than a
  human mix desk. [vs studio re-recording mix]

## Sources

- Karen Commins, 7 players on an audiobook production team - https://karencommins.com/2017/03/7-players-audiobook-production-team.html
- Pozotron, the key roles behind every great audiobook - https://blog.pozotron.com/the-key-roles-behind-every-great-audiobook
- Penguin, job roles in audiobooks - https://www.penguin.co.uk/about/company-articles/job-roles-in-audiobooks
- NarratorList, production personnel - https://narratorlist.com/production-personnel/
- Backstage, audiobook narrator voiceover casting process - https://www.backstage.com/magazine/article/audiobook-narrator-voiceover-casting-process-70276/
- Book Riot, audiobook proofing - https://bookriot.com/audiobook-proofing/
- davebooks, QC / prooflistening - http://davebooks.com/qc.html
- Common-mode, audiobook post-production - https://www.common-mode.com/audiobook-post-production
- NarrationBox, audiobook mastering RMS/LUFS/noise floor ACX guide - https://narrationbox.com/blog/audiobook-mastering-rms-lufs-noise-floor-acx-guide
- ACX, narrators and studios - https://www.acx.com/mp/how-it-works/narrators-and-studios
- ACX producer's checklist - https://help.acx.com/s/article/the-acx-producer-s-checklist
- ACX, mastering audiobooks with Alex the audio scientist - https://www.acx.com/mp/blog/mastering-audiobooks-with-alex-the-audio-scientist
- Audio Publishers Association (APA) - https://www.audiopub.org/about-the-apa
- SAG-AFTRA, audiobooks - https://www.sagaftra.org/contracts-industry-resources/audiobooks
- Barnes & Noble, an insider's look at producing full-cast audiobooks - https://www.barnesandnoble.com/blog/an-insiders-look-at-producing-full-cast-audiobooks/
