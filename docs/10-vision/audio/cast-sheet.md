---
title: "Live Edition Cast Sheet"
document_type: "production-reference"
status: "active-support"
authority: "production-reference"
summary: "The casting-director's single source of truth for the LIVE / dramatized audiobook cast: which character gets which voice, the deliberate contrast map that keeps co-present speakers tellable apart by ear, and the cross-chapter consistency ledger. Derived from the canon character profiles and the existing voice assets; it is a production artifact, not a canon authority. Authored and owned by casting-director, briefed to voice-designer, consumed by live-narration-director."
tags:
  - audio
  - casting
  - live-edition
  - voice
  - production
  - cast-sheet
related:
  - "../narrative-brief.md"
  - "../../20-canon/characters/profiles/index.md"
  - "../../20-canon/characters/voices/"
  - "../../../.claude/agents/casting-director.md"
  - "../../../.claude/agents/voice-designer.md"
  - "../../../.claude/agents/live-narration-director.md"
source_documents:
  - "docs/20-canon/characters/profiles/index.md"
  - "docs/70-research/audio-roles-audit.md"
  - ".claude/agents/voice-designer.md"
  - ".claude/agents/live-narration-director.md"
---

# Live Edition Cast Sheet

> **Owner: casting-director.** This is the cast-as-a-SET decision for the LIVE / dramatized
> audiobook -- who gets which voice, the contrast map that keeps co-present speakers apart on
> the ear, and the cross-chapter consistency ledger. It DERIVES from canon (the character
> profiles own age, heritage, and temperament); it never overrides canon. It is briefed to
> [voice-designer](../../../.claude/agents/voice-designer.md) (which voices to design, to what
> contrast target) and consumed by
> [live-narration-director](../../../.claude/agents/live-narration-director.md) (which ensures
> each assigned voice is on the server and performs it). Grounding for the role:
> [audio-roles audit](../../70-research/audio-roles-audit.md), sections 1.2 and 2.1.

## How the assets are laid out

| Thing | Where |
| --- | --- |
| Character profile (owns age / heritage / temperament / Voice and Speech) | [`docs/20-canon/characters/profiles/`](../../20-canon/characters/profiles/) -- one `<slug>.md` per character |
| Voice asset (3 preview mp3s + `voice-design.json` with the chosen `default`) | [`docs/20-canon/characters/voices/`](../../20-canon/characters/voices/) -- one `<slug>/` per voice |
| Portrait (the visual sibling, next to the voices) | [`docs/20-canon/characters/portraits/`](../../20-canon/characters/portraits/) -- one `<slug>.jpg` |

A voice's grounded register (gender, age band, accent, persona) is read from the profile's
"Voice and Speech" section and mirrored by the `description` field of its `voice-design.json`.
The roster below is seeded from those existing descriptions.

## Cast roster + contrast map (banded by the axes that separate voices on the ear)

The roster is grouped by **gender** then **age band**, because those are the strongest axes a
listener uses to tell voices apart. Accent / cadence and persona / timbre are the secondary
axes that pull same-band voices apart. Two characters who are never co-present may share a band
at no cost; two who share a scene must have an audible gap on at least one axis. `default` is
the chosen preview index in that voice's `voice-design.json`.

### Male voices

| Character | slug | Age band | Accent / cadence | Persona / timbre | default | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Julian Mercer | `mercer-julian` | late teens | American | curious young maker | 0 | designed |
| Mason Vance | `vance-mason` | late teens (~17) | American | withdrawal-native teen | 2 | designed |
| Evan Voss | `voss-evan` | late 20s | American | charming idle heir, polished | 0 | designed |
| Tomas Herrera | `herrera-tomas` | early 30s | American | steady night nurse, broadcast-clean | 0 | designed |
| Marcus Vance | `vance-marcus` | mid 30s | American | weathered working father | 0 | designed |
| Eli Rook | `rook-eli` | late 30s | American (flat Michigan) | dry working technician, level baritone | 2 | designed |
| Jonah Mercer | `mercer-jonah` | late 30s | American | smooth political fixer | 0 | designed |
| Ray Dorsey | `dorsey-ray` | mid 40s | flat Detroit | night-watch lineman | 2 | designed |
| Daniel Park | `park-daniel` | late 40s | American | careful enclave maintainer | 0 | designed |
| Hector Reyes | `reyes-hector` | late 50s | Detroit | genial neighborhood handyman | 0 | designed |
| Nolan Avery | `avery-nolan` | early 60s | American (Detroit) | grid elder | 0 | designed |
| Adrian Kade | `kade-adrian` | early 60s | American, studio-clean | patient gatekeeper magnate | 0 | designed |
| Bayo Adeyemi | `adeyemi-bayo` | early 60s | Nigerian (Yoruba, Lagos) under Detroit | wry retired foundryman | 0 | designed |
| Daniel Rook | `rook-daniel` | 60s | American Midwest (Michigan) | Flint repair tradesman | 0 | designed |
| Marek Vesely | `vesely-marek` | mid 60s | American | weathered hen-keeper | 0 | designed |
| Sekou Dembele | `dembele-sekou` | early 70s | West African (Bambara/French) under American | retired logistics man | 0 | designed |
| Malcolm Mercer | `mercer-malcolm` | 70s | flat Great Lakes Michigan | dry logistics magnate, worn but sharp | 0 | designed |

### Female voices

| Character | slug | Age band | Accent / cadence | Persona / timbre | default | Status |
| --- | --- | --- | --- | --- | --- | --- |
| June Park | `park-june` | late teens | American, bright | irreverent salvage-hacker | 0 | designed |
| Priya Sharma | `sharma-priya` | late 20s | American | precise clinic aide | 0 | designed |
| Alexandra Kade | `kade-alexandra` | early 30s | American | field ecologist, self-exiled heiress | 0 | designed |
| Talia Reed | `reed-talia` | mid 30s | Detroit | community coordinator, teacher | 0 | designed |
| Celeste Mercer | `mercer-celeste` | late 30s | American, crisp | composed Lakeward realist | 0 | designed |
| Nora Bell | `bell-nora` | early 40s | American, studio-clean | composed researcher | 0 | designed |
| Sera Vale | `vale-sera` | mid 40s | Canadian | composed security director | 0 | designed |
| Lena Okafor | `okafor-lena` | late 40s | Detroit under Nigerian-American household cadence | community-clinic director | 0 | designed |
| Soojin Park | `park-soojin` | late 40s | flat Detroit under soft Korean cadence | steady home caregiver | 0 | designed |
| Ngozi Okonkwo | `okonkwo-ngozi` | early 50s | Nigerian English | dignified household keeper | 0 | designed |
| Marisol Vega | `vega-marisol` | mid 50s | American (Detroit) | weathered neighborhood grocer | 0 | designed |
| Mara Voss | `voss-mara` | mid 50s | American | composed political broker | 0 | designed |
| Elaine Mercer | `mercer-elaine` | late 60s | American, close-mic | composed care administrator | 0 | designed |
| Ruth Rook | `rook-ruth` | late 60s | American | community librarian, resonant | 0 | designed |
| Aminata Diallo | `diallo-aminata` | early 70s | Guinean Fulani under American | dignified, wry survivor | 0 | designed |
| Amara Okafor | `okafor-amara` | mid 70s | Nigerian (Igbo) under Detroit | retired grocer matriarch, resonant | 0 | designed |

### Production voices (not characters)

| Voice | slug | Register | Role | default | Status |
| --- | --- | --- | --- | --- | --- |
| Narrator | `narrator` | male, early 50s, warm studio | the live edition's narrator instrument; must sit clearly apart from every character it introduces | 2 | designed |
| Past mentor | `mentor-past` | male, late 50s, warm intimate | flashback-only mentor voice | 0 | designed |

## Candidate collisions to resolve (verify co-presence, then pull apart)

These are same-band pairs the descriptions place close on the ear. A collision only counts if the
two characters are ever **co-present in a scene** -- the casting-director verifies co-presence
against the manuscript and blueprints before acting. Where canon forbids re-designing a voice,
the two-hander is routed to live-narration-director as a performance / pacing note instead.

- **Julian Mercer vs Mason Vance** -- both male, late teens. Different households; verify whether
  they share scenes. If co-present, brief voice-designer to widen the gap (a different age read or
  cadence on one).
- **Eli Rook vs Jonah Mercer** -- both male, late 30s, American. Persona already separates them
  (dry technician vs smooth fixer); confirm the gap holds in any shared scene.
- **Adrian Kade vs Nolan Avery** -- both male, early 60s, American. Adeyemi's Nigerian cadence
  separates the third early-60s male; Kade vs Avery lean on persona / timbre. Verify co-presence.
- **Elaine Mercer vs Ruth Rook** -- both female, late 60s, American. Different households; if
  co-present, pull apart on timbre.
- **Aminata Diallo vs Amara Okafor** -- both elderly female with West-African cadence under
  American. The closest pair on the sheet; if ever co-present, this needs the widest deliberate
  separation (distinct cadence, register, or persona). Highest-priority check.

## Per-chapter sign-off

### chapter-01 -- "No Signal" (book-1) -- SIGNED 2026-06-30

Speaking roster determined from the approved manuscript
(`docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md`), not the blueprint's
placeholder "background" list. Co-presence taken per scene from the manuscript prose.

**Canon-slugged voiced characters in scope (all DESIGNED, assets verified on disk):**

| Character | slug | Scenes voiced | Register (grounded) | default | Asset verified |
| --- | --- | --- | --- | --- | --- |
| Eli Rook | `rook-eli` | 1-4 (viewpoint) | M, late 30s, flat Michigan, dry level baritone | 2 | yes |
| Marisol Vega | `vega-marisol` | 2 (grocery counter) | F, mid 50s, Detroit, weathered grocer | 0 | yes |
| Mason Vance | `vance-mason` | 3 (the doorbell, "Vance's boy... seventeen") | M, ~17, flat Detroit, clipped withdrawal-native teen | 2 | yes |
| Lena Okafor | `okafor-lena` | 4 (over the mesh link) | F, late 40s, Detroit under Nigerian-American cadence, low even alto | 0 | yes |
| Narrator | `narrator` | 1-4 (close third) | M, early 50s, warm studio | 2 | yes |

`vance-mason` description ("late teens, about 17... flat working Detroit accent") matches the
manuscript's "Vance's boy came first with the doorbell, seventeen" (chapter-01:83); the boy is
Marcus Vance's son, voiced as Mason.

**Co-presence and contrast map (collision only counts among co-present voices):**

- **Scene 1 (Eli's home):** Eli + narrator only. The night's mesh messages ("Dorsey", "the
  library") are rendered as TEXT on the board (chapter-01:35,38), narrator-read, not voiced. No
  character collision. Eli (M late 30s baritone) sits clearly under the narrator (M early 50s warm
  studio) on age + persona.
- **Scene 2 (the street / grocery):** Eli + Marisol + narrator. Gender separates Marisol (F mid
  50s) from both males; the corner boy's "morning, Mr. Rook" (chapter-01:61) is reported speech,
  incidental. No collision.
- **Scene 3 (the shop) -- the only dense same-gender cluster:** Eli + Mason + the unnamed old man
  + narrator are all MALE and co-present. Separated by age band and persona: Mason ~17 clipped teen
  / Eli late 30s dry baritone / old man ~60 / narrator early 50s neutral studio. The three slugged
  voices span teen / late-30s / early-50s with distinct personas and are tellable apart by ear. The
  old man is the one incidental gap (see routing below).
- **Scene 4 (the mesh call):** Eli + Lena + narrator. Gender separates Lena (F late 40s alto) from
  both males; her voice is deliberately degraded by the thin-link performance, widening the gap
  further. No collision.

**Verdict:** every canon speaking character in scope is assigned and contrast-checked; no
co-present collision is unresolved; all five assets verified present on disk. Nothing to route to
voice-designer (no un-cast canon slug). SIGNED.

**Incidental voicing routed to live-narration-director (not a designable cast slug):**

- **The unnamed old man** (chapter-01:107-115, "Older, sixty maybe," asks Eli where he learned his
  work). Substantial single-scene speaker but with NO canon slug or profile, so he is not a
  voice-designer brief and not a cast-sheet assignment. Director to voice him as an incidental
  ~60-year-old Detroit-accented male, audibly OLDER than Eli and accent-distinct from the
  neutral-studio narrator, so the Scene-3 male cluster stays four-way separable. Do NOT borrow a
  named character's voice for him -- in particular not Nolan Avery (`avery-nolan`), who is
  referenced by name elsewhere in this same chapter (chapter-01:69) as a different, non-speaking
  neighbor; reusing Avery's instrument would misidentify the old man on the ear.
- **Mesh text senders (Dorsey, "the library") and the corner boy:** narrator-read text / reported
  speech as written; no character voice required this chapter.

## Cross-chapter consistency ledger

The chosen voice for each character (its `voice-design.json` `default` index, description, and
tags) is the **locked reference**. Any later re-design or re-render is checked back against it
before it ships, so a character is the same instrument in chapter nine as in chapter one. Record
each legitimate change here with its grounding and the chapters affected.

The five voices above are now the **locked reference** for these characters from chapter-01
forward; any later re-design or re-render is checked back against them before it ships.

| Date (ISO) | Character | Change | Grounding | Chapters affected |
| --- | --- | --- | --- | --- |
| 2026-06-30 | rook-eli, vega-marisol, vance-mason, okafor-lena, narrator | Locked as Ch1 reference (no change) | Asset descriptions + `default` verified on disk; match chapter-01 prose | ch1 |

## Sign-off

The casting-director signs off the ensemble before live scenes render: every speaking character
in scope is assigned, every candidate collision among co-present speakers is resolved, and the
consistency ledger is clean.

- **Status: ACTIVE.** Per-chapter sign-off in progress. **chapter-01 (book-1): SIGNED 2026-06-30**
  -- every canon speaking character in scope assigned + contrast-checked, all five assets verified
  on disk, no co-present collision unresolved, ledger clean. Later chapters pending their own
  co-presence verification.
- **Last signed:** 2026-06-30 -- chapter-01-no-signal (book-1).

## Decisions Made (author may override)

| Question | Decision | Grounding / authority | Confidence |
| --- | --- | --- | --- |
| Is the unnamed "old man, sixty maybe" (chapter-01:107) a designable cast voice? | No. He has no canon slug or profile, so he is not a voice-designer brief. Routed to live-narration-director as an incidental ~60 Detroit-accented male, older than Eli and accent-distinct from the narrator; he does not block sign-off (nothing to design). | Manuscript chapter-01:107-115 (unnamed); charter -- cast strictly at canon level, do not invent canon; needs_design requires a canon slug. | high |
| Does using `dorsey-ray`'s existing voice for the Dorsey mesh message count him as a voiced character here? | No. Dorsey appears only as a written mesh message on the board (chapter-01:35), narrator-read text, not spoken dialogue. Not a voiced role this chapter. | Manuscript chapter-01:35,38 render the mesh notes as text, not speech. | high |
| Is the Scene-3 four-way male cluster (Eli, Mason, old man, narrator) tellable apart? | Yes. Age bands span teen / late-30s / ~60 / early-50s with distinct personas; the old man's incidental voice is briefed to stay accent-distinct from the neutral-studio narrator. No re-design of any slugged voice needed. | Asset descriptions (`vance-mason`, `rook-eli`, `narrator`); co-presence from chapter-01 Scene 3 prose. | high |
