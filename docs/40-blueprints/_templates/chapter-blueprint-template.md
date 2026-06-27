---
title: "Chapter Blueprint Template"
document_type: "blueprint-template"
status: "active-support"
authority: "blueprint"
summary: "Canonical template copied for each chapter blueprint. Defines the required sections, scene breakdown, and drafting checks before a chapter can be drafted."
tags:
  - blueprint
  - template
  - planning
  - drafting
related:
  - "../../30-plot/book-1/index.md"
  - "../../00-governance/novel-development-guide.md"
source_documents:
  - "archive/source-monoliths/chapter-blueprint-template.md"
---

# Chapter Blueprint Template

> Copy this file for each chapter and replace all bracketed placeholders.
> Suggested filename: `chapter-##-short-title.md`

---

# Chapter [Number]: [Working Title]

## Chapter Metadata

```yaml
chapter_number: [number]
working_title: "[title]"
act: "[act number and name]"
story_date: "[date or date range]"
story_date_iso: "[YYYY-MM-DD, or a start/end pair for a range]"
time_of_day: "[morning, afternoon, evening, night, or exact time]"
primary_viewpoint: "[character]"
tense: "past"
person: "close third person"
primary_location: "[location]"
secondary_locations:
  - "[location]"
estimated_word_count: [number]
planned_scene_count: [number]
chapter_status: "blueprint"
```

---

## Chapter Summary

Write a concise summary of what happens in the chapter.

This should describe the chapter’s complete movement in approximately one to three paragraphs, including:

- Where the viewpoint character begins
- What they are trying to accomplish
- What interferes with that goal
- What they decide or discover
- How the chapter ends differently from how it began

---

## Narrative Purpose

### Primary Purpose

State the single most important reason this chapter exists.

Examples:

- Introduce a major character
- Create an immediate crisis
- Reveal a hidden motivation
- Change a relationship
- Force a moral decision
- Escalate the central conflict
- Pay off an earlier setup

### Secondary Purposes

- [Secondary purpose]
- [Secondary purpose]
- [Secondary purpose]

### Why This Chapter Cannot Be Removed

Explain what would be lost or become unclear if the chapter did not exist.

If this section cannot be answered convincingly, the chapter may need to be combined with another chapter.

---

## Chapter Promise

What experience should this chapter provide the reader?

This is not a plot summary. It is the dramatic promise.

Examples:

- A normal morning gradually reveals that an entire neighborhood has been abandoned.
- A technical repair becomes a moral decision.
- A trusted friendship begins turning into a betrayal.
- A successful rescue reveals that Morrow has acted without permission.

---

## Viewpoint Character

### External Goal

What does the viewpoint character consciously want during this chapter?

### Internal Pressure

What emotional need, fear, guilt, belief, or contradiction affects their decisions?

### Starting Emotional State

How does the viewpoint character feel at the beginning?

### Ending Emotional State

How do they feel at the end?

### False Assumption

What does the viewpoint character believe at the beginning that is challenged during the chapter?

### Decision

What meaningful choice does the viewpoint character make?

The decision should create a consequence that cannot be completely undone.

---

## Reader Information

### What the Viewpoint Character Knows

- [Known fact]
- [Known fact]

### What the Viewpoint Character Does Not Know

- [Unknown fact]
- [Unknown fact]

### What the Reader Already Knows

- [Relevant established fact]
- [Relevant established fact]

### New Information Revealed

- [New revelation]
- [New revelation]

### Information Deliberately Withheld

Identify mysteries, lies, omissions, or facts that should remain hidden.

- [Withheld information]
- [Reason for withholding it]

---

## Focus

A single section for every focused entity in this chapter, whether it is a
character, an item or object, or a location. For each entity that matters, record
the focus ambition and the revelation target. This is the per-chapter slice of the
reader's knowledge-state: what the reader should know or feel about this entity by
the end of the chapter. The levels across chapters compose the entity's focus curve.
Revelation is motivated by the scene and delivered image over inventory, never
padded to hit a level. Only entities you deliberately sharpen earn a focus entry; do
not list everything that appears.

### Levels

The level is a coarse ambition, not a numeric score.

- **blur:** present but barely individuated. A function or a role, glimpsed.
- **sketch:** a few defining strokes. The reader could pick them out of a crowd.
- **sharp:** clearly drawn and specific. Voice, body, and want are legible.
- **crisp:** fully present and dimensional. The reader knows them from the inside.

### Focus Targets

Duplicate the appropriate block below for every focused entity. Each entry carries a
pointer to the entity's bible file, a Level, and a Revelation target along the axes
appropriate to its type. The revelation target is qualitative intent in service of
the story, not a quota.

> Note: item and location bibles may not exist yet. The entity pointer is
> forward-compatible — point it at the file path the entity will live at, even if
> that file has not been written, so the reference resolves once the bible exists.

#### Character — [Character]

- **Bible pointer:** [path to this character's profile]
- **Level:** [blur | sketch | sharp | crisp]
- **Revelation target:**
  - **Physical:** [what the reader should know or feel about how this person looks, moves, or sounds]
  - **Emotional:** [what the reader should feel from or about this person]
  - **Interior:** [what the reader should understand of this person's inner state, want, or contradiction]
- **Voice and heritage pointer:** Pull this character's "Voice and Speech" section
  and their heritage signals (accent under "Movement and voice", "Birthplace" and
  "Faction or class" in Basic Information, and "Early Life" under History and
  Background) from their profile, so they are written specifically and never as the
  cultural default.

#### Item / Object — [Item]

- **Bible pointer:** [path to this item's bible, or the path it will live at]
- **Level:** [blur | sketch | sharp | crisp]
- **Revelation target:**
  - **Appearance:** [the sensory detail of the object — how it looks, feels, sounds, weighs]
  - **Significance:** [what it means, what it foreshadows, or why it matters in the story]
  - **Provenance:** [where it came from, who made it, and who holds it now]

#### Location — [Location]

- **Bible pointer:** [path to this location's bible, or the path it will live at]
- **Level:** [blur | sketch | sharp | crisp]
- **Revelation target:**
  - **Physical-spatial:** [the layout, scale, and concrete geography the reader should grasp]
  - **Atmosphere:** [the mood, light, sound, and feel of being in the place]
  - **Significance:** [what the place means, what it foreshadows, or why it matters in the story]

### Usage Note

- The level is a coarse ambition (blur, sketch, sharp, crisp), not a score and not
  a quota.
- The revelation target is qualitative intent in service of the story along the
  entity-appropriate axes. It is explicitly not a checklist to fill.
- Name attributes, not values — single source of truth. The revelation target names
  *which* attributes or dimensions the reader should come to know this chapter (the
  strap, the face, the accents on the face), never their concrete values. The values
  themselves (a brown strap, an ivory face, three diamonds) live only in the entity's
  bible file. At drafting time the prose pulls each named attribute's value from that
  file. This keeps one source of truth: revise a detail in the entity's file and the
  blueprint's instruction still holds, automatically revealing the new value. The
  blueprint controls the revelation pacing — which attributes, when; the file controls
  the truth — their values; the two never duplicate. So a blueprint says "reveal the
  watch's strap, face, and accents," never "the watch has a brown strap."
- The levels across chapters compose the entity's focus curve. An entity may be
  a blur in one chapter and crisp in another by design.
- Deliver revelation image over inventory. A single concrete image earns a level; a
  list of traits does not.
- Never pad a scene to hit a level. If the scene does not motivate the revelation,
  the target is wrong, not the prose. Hold to the lower level instead.
- Only entities you deliberately sharpen earn a focus entry. If you are not choosing
  to bring an entity into focus, leave it out.
- Respect the bible's reveal tags (`[open]`, `[reveal: Book N]`, `[behavior-only]`,
  `(proposed)`) so focus never leaks a gated fact.

---

## Opening

### Opening Image

Describe the first concrete image, sound, sensation, action, or line of dialogue.

### Opening Situation

What is happening when the chapter begins?

Avoid beginning with background explanation unless the information is immediately necessary.

### Immediate Question

What question should make the reader continue beyond the opening page?

---

# Scene Breakdown

Duplicate the following section for every scene.

---

## Scene [Number]: [Scene Title]

### Scene Metadata

```yaml
date: "[date]"
date_iso: "[YYYY-MM-DD]"
start_time: "[time or approximate time]"
start_iso: "[YYYY-MM-DDTHH:MM, 24h; approximate ok]"
duration: "[approximate duration]"
viewpoint: "[character]"
location: "[specific location]"
characters_present:
  - "[character]"
```

### Scene Purpose

What must this scene accomplish that no other scene currently accomplishes?

### Viewpoint Goal

What does the viewpoint character want before the scene ends?

### Opposition

Who or what prevents them from getting it?

Opposition may come from:

- Another character
- A failing system
- Missing information
- Time pressure
- Physical danger
- A moral conflict
- The viewpoint character’s own fear or contradiction

### Stakes

What will happen if the viewpoint character fails?

The stakes should be specific to this scene.

### Entry Condition

What is true when the scene begins?

### Major Beats

1. [Opening action or discovery]
2. [Escalation]
3. [Complication]
4. [Decision, discovery, or confrontation]
5. [Result]

### Scene Turn

What new fact, failure, arrival, decision, or reversal changes the direction of the scene?

### Exit Condition

What is true when the scene ends that was not true when it began?

### Emotional Movement

**Beginning:** [emotion]
**End:** [emotion]

### Relationship Movement

Identify any relationship changed by the scene.

**Characters:** [character and character]
**Before:** [relationship condition]
**After:** [relationship condition]

### Information Revealed

- [Fact revealed to the viewpoint character]
- [Fact revealed only to the reader]
- [Lie or misunderstanding introduced]

### Technology and Worldbuilding

List only the technology or world details required by the scene.

For each important system, establish:

- What it does
- Who controls it
- Where its power comes from
- What limits it
- What can fail

Avoid explaining information that does not affect the scene.

### Sensory Anchor

Choose two or three concrete details that make the location feel physical.

- [Visual detail]
- [Sound]
- [Smell, temperature, texture, or bodily sensation]

### Dialogue Objective

What is each major speaker trying to obtain, hide, or avoid?

| Character   | Wants       | Hides or avoids  |
| ----------- | ----------- | ---------------- |
| [Character] | [Objective] | [Hidden concern] |
| [Character] | [Objective] | [Hidden concern] |

### Subtext

What is the scene actually about beneath the literal conversation or action?

### Continuity Changes

- [New injury]
- [Object gained or lost]
- [Location changed]
- [Promise made]
- [Secret learned]
- [Resource spent]
- [System damaged or activated]

### Scene Ending

Write the intended final image, revelation, decision, or line direction.

The scene should not simply stop after the information has been delivered.

---

# End of Scene Breakdown

---

## Chapter Escalation

Explain how tension increases across the chapter.

```mermaid
flowchart LR
    A[Opening condition] --> B[First complication]
    B --> C[Escalation]
    C --> D[Major turn]
    D --> E[Chapter ending]
```

Replace each placeholder with chapter-specific events.

---

## Conflict Layers

### External Conflict

What practical or physical problem drives the chapter?

### Interpersonal Conflict

Which characters want incompatible outcomes?

### Internal Conflict

What does the viewpoint character want that conflicts with their beliefs, fear, guilt, or identity?

### Thematic Conflict

What larger question does the chapter dramatize?

Do not merely state the theme. Explain how the characters’ decisions embody it.

---

## Character Development

### Viewpoint Character

What does this chapter reveal about the character that the reader did not previously understand?

### Supporting Characters

| Character   | What this chapter reveals or changes |
| ----------- | ------------------------------------ |
| [Character] | [Development]                        |
| [Character] | [Development]                        |

### Character Contradictions

Identify any moment where a character’s behavior conflicts with their stated values.

This is often more revealing than a direct explanation of personality.

---

## Relationships

Track every relationship that meaningfully changes.

| Relationship            | Starting condition | Ending condition | Cause of change |
| ----------------------- | ------------------ | ---------------- | --------------- |
| [Character / Character] | [Before]           | [After]          | [Cause]         |

---

## Theme

### Primary Theme

Which established theme is active in this chapter?

### Thematic Question

Phrase the theme as a question raised by the events.

Example:

> Is a service truly public if its owner may withdraw it whenever the people using it stop being profitable?

### Competing Answers

Which characters or systems embody different answers?

Avoid allowing the narration to settle the argument too easily.

---

## Worldbuilding Introduced

List new canonical facts established in this chapter.

- [World fact]
- [Institutional fact]
- [Social condition]
- [Historical detail]
- [Location detail]

Only include facts that should be remembered in future chapters.

---

## Technology Used

| Technology or system | Capability shown | Limitation shown | Controller               |
| -------------------- | ---------------- | ---------------- | ------------------------ |
| [System]             | [Capability]     | [Limitation]     | [Person or organization] |

Confirm that every capability is compatible with the World and Technology Rules.

---

## Setup and Payoff

### Setups Introduced

| Setup                             | Intended payoff |    Expected chapter |
| --------------------------------- | --------------- | ------------------: |
| [Detail, object, secret, or line] | [Future use]    | [Number or unknown] |

### Earlier Setups Paid Off

| Earlier setup | Original chapter | Payoff in this chapter |
| ------------- | ---------------: | ---------------------- |
| [Setup]       |         [Number] | [Payoff]               |

### Red Herrings

Identify any intentionally misleading clue.

Do not create a red herring without knowing what the eventual truth will be.

---

## Foreshadowing

List subtle elements that prepare the reader for later developments.

- [Foreshadowed event]
- [How it appears naturally in this chapter]
- [When it should pay off]

Foreshadowing should serve the current scene even if the later payoff is never recognized.

---

## Symbolic or Repeated Imagery

Identify any recurring image, object, sound, or environmental detail.

Examples:

- Dead streetlights
- Authentication warnings
- Construction lights on an empty Mars
- Machines waiting for permission
- Screens returning to life

Explain what the image means in this chapter without forcing the symbolism into the prose.

---

## Pacing Plan

### Opening Pace

[Slow, moderate, urgent]

### Middle Pace

[Slow, moderate, urgent]

### Ending Pace

[Slow, moderate, urgent]

### Intended Balance

Approximate proportions:

- Action and physical activity: [percentage]
- Dialogue and interpersonal conflict: [percentage]
- Internal reflection: [percentage]
- Description and worldbuilding: [percentage]

These percentages are guidelines, not strict measurements.

---

## Prose Guidance

### Tone

Describe the chapter’s tone.

### Narrative Distance

How closely should the narration follow the viewpoint character’s immediate thoughts and senses?

### Description Priorities

What should receive detailed description?

What should remain brief?

### Dialogue Style

What qualities should dominate the dialogue?

### Technical Explanation Limit

Identify what the reader must understand and what can remain unexplained.

### Language to Avoid

List any terms, clichés, metaphors, emotional shortcuts, or exposition styles that would weaken the chapter.

---

## Opening and Closing Contrast

### Opening Condition

Summarize the practical, emotional, and relational state at the beginning.

### Closing Condition

Summarize the state at the end.

### Irreversible Change

What has happened that cannot be completely restored?

Every chapter should contain at least one irreversible change, even if it is only a change in knowledge or trust.

---

## Ending Hook

### Hook Type

Choose the primary type:

- Discovery
- Decision
- Threat
- Reversal
- Unanswered question
- Arrival
- Failure
- Moral dilemma
- Image
- Line of dialogue

### Intended Hook

Describe the exact revelation, image, action, or question ending the chapter.

### Reader Question

What specific question should the reader carry into the next chapter?

---

## Continuity Ledger Updates

After drafting, transfer these facts into the Continuity Ledger.

### Character State

| Character   | Location   | Physical state | Emotional state |
| ----------- | ---------- | -------------- | --------------- |
| [Character] | [Location] | [Condition]    | [Condition]     |

### Knowledge Changes

| Character   | Information learned | Source   |
| ----------- | ------------------- | -------- |
| [Character] | [Information]       | [Source] |

### Relationship Changes

- [Change]

### Resources

- [Resource gained]
- [Resource lost]
- [Resource damaged]
- [Resource spent]

### Injuries and Physical Consequences

- [Injury or consequence]

### Promises, Threats, and Obligations

- [Promise]
- [Threat]
- [Debt or obligation]

### Secrets

- [Secret created]
- [Secret shared]
- [Secret exposed]

### Technology State

- [System activated]
- [System damaged]
- [Access granted]
- [Access revoked]
- [New capability discovered]

### Location Changes

- [Location detail established or changed]

---

## Canon Checks

Before drafting, verify the chapter against:

- [ ] Narrative Brief
- [ ] Story Bible
- [ ] Character Bible
- [ ] World and Technology Rules
- [ ] Master Timeline
- [ ] Plot Outline and Chapter Map
- [ ] Previous chapter blueprints
- [ ] Existing Continuity Ledger

---

## Drafting Checklist

Before the prose draft is considered complete:

- [ ] The viewpoint remains consistent.
- [ ] The viewpoint character wants something specific.
- [ ] Opposition appears early enough.
- [ ] The chapter contains a meaningful decision or discovery.
- [ ] At least one relationship changes.
- [ ] Technology obeys established limitations.
- [ ] Worldbuilding emerges through action or conflict.
- [ ] Exposition does not halt the story.
- [ ] Dialogue voices remain distinct.
- [ ] The ending condition differs from the opening condition.
- [ ] The final beat creates momentum.
- [ ] New canon has been recorded in the Continuity Ledger.
- [ ] No later reveal has been exposed prematurely.
- [ ] No character knows information they have not yet learned.
- [ ] No unresolved contradiction has been silently ignored.

---

## Open Questions

List decisions that do not need to be finalized before drafting.

- [Open question]
- [Open question]

Open questions should not include anything required for the chapter to function.

---

## Revision Notes

Use this section after the chapter is drafted.

### What Worked

- [Note]

### What Needs Revision

- [Note]

### Continuity Problems

- [Note]

### Pacing Problems

- [Note]

### Character Problems

- [Note]

### Changes Made to Canon

- [Note]

---

## Chapter Completion Standard

The chapter is ready for manuscript drafting when:

1. Every scene has a clear purpose.
2. The viewpoint character has a specific goal.
3. The opposition and stakes are concrete.
4. The chapter contains a meaningful turn.
5. The ending changes the story’s direction or understanding.
6. Required technology and world rules are established.
7. Character knowledge remains chronologically accurate.
8. The chapter creates forward momentum.
9. The blueprint provides direction without dictating every sentence.
10. A writer can draft the chapter without inventing major plot decisions during prose composition.
