---
title: "Decision 058: Sentence-Length Variation Cures Incidental Staccato, and the Style Guide Is a Guide, Not an Algorithm"
document_type: "decision"
status: "active"
authority: "governance"
summary: "Records two style refinements made while the author reviewed Chapter 1. (1) Sentence rhythm: the clipped, austere, declarative voice is kept, and short sentences remain a strength; the deliberate devices (a lone short sentence as its own paragraph for weight, and a run of short sentences doing rhetorical work) are kept; but the author noticed a recurring tic of incidental runs of short flat declaratives that pull no rhetorical weight and produce a repetitive marching meter. The established cure is variation, framing deliberate staccato with longer flowing sentences and varying the incidental runs, not eliminating short sentences. (2) Meta-principle: a preamble at the top of the Style Guide reaffirms that the guide is advisory, never a set of algorithms, the writing must never become formulaic, and the author retains ownership and the explicit right to deviate on purpose for effect, under the operating rule: when in doubt follow the style guide exactly, when trying to do something special follow your heart. Both are recorded in the Style Guide (docs/10-vision/style/core-prose.md). Reversible via git history."
tags: ["decision", "style", "prose", "sentence-rhythm", "variation", "meta-principle", "reversible"]
related:
  - "../../../10-vision/style/core-prose.md"
  - "../../../10-vision/style/index.md"
  - "./037-the-tone-is-serious-restrained-and-morally-ambiguous.md"
  - "./039-avoid-em-dashes-in-drafted-prose-and-project-copy.md"
  - "../index.md"
source_documents:
  - "docs/10-vision/style/core-prose.md"
---

## Decision 058: Sentence-Length Variation Cures Incidental Staccato, and the Style Guide Is a Guide, Not an Algorithm

**Date:** 2026-06-28
**Status:** Active but Revisable
**Category:** Style and tone

### Decision

While reviewing Chapter 1, the author noticed a recurring craft tic and, in the same pass, reaffirmed the standing of the Style Guide itself. Two related things are now recorded in the Style Guide.

**1. Sentence rhythm and variation.** The chapter voice is intentionally clipped, austere, and declarative, and short sentences are a strength that suits the tone. Two uses of the short sentence are explicitly deliberate and kept: a single short sentence standing alone as its own paragraph, for weight and white space; and a run of short sentences doing rhetorical work, such as building, listing, or a montage of accumulation. The problem is frequency. Incidental runs of short flat declaratives that are not pulling rhetorical weight create a repetitive marching rhythm, where the reader stops hearing the scene and starts hearing the meter. The established cure is variation, not the removal of short sentences: frame the deliberate staccato punches with longer flowing sentences so the punches stand out, and vary the incidental clipped runs. Vary sentence length deliberately. This was added as a "Rhythm and Variation" subsection under Sentence Style in `../../../10-vision/style/core-prose.md`.

**2. The Style Guide is a guide, not an algorithm.** A short preamble ("How to Use This Guide") was added at the top of the Style Guide, before the specific rules. It states that the document is a guide rather than a set of algorithms or rules to execute mechanically, that the writing must never become formulaic, and that the author retains ownership of the prose and the explicit right to go against the guide on purpose, for effect, with a deliberate deviation counting as a choice and not an error. The operating rule is quoted exactly: "When in doubt, follow the style guide exactly. When trying to do something special, follow your heart."

### Previous or Alternative Direction

The Style Guide already called for varied sentence lengths and warned against an entire chapter of short, dramatic sentences (core-prose.md, Sentence Style). It did not name the narrower failure mode of incidental, weight-free staccato runs, nor distinguish them from the deliberate short-sentence devices, so the two were easy to conflate. The Purpose section already noted that deviations should be deliberate, but the guide carried no top-level statement of its own advisory status; a stricter reading could treat every rule as binding. The rejected alternatives were to "fix" the marching rhythm by deleting short sentences (which would damage the established voice) and to leave the guide's authority implicit (which risks formulaic, rule-following prose).

### Reason

The clipped voice is load-bearing for the tone established in Decision 037, so the correct response to a monotonous patch is to vary the frame around the short sentences, not to surrender them. Naming the incidental-staccato tic and separating it from the deliberate devices gives reviewers a precise target and protects the intentional punches. Stating the guide's advisory status protects the prose from the opposite failure: a drafting AI or reviewer treating the guide as an algorithm and flattening voice into compliance. The meta-principle makes deliberate deviation legitimate and legible, consistent with the existing "deviations should be deliberate" note and with the advisory framing of the other style-preference decision (039).

### Consequences

- `docs/10-vision/style/core-prose.md`: a "How to Use This Guide" preamble is added before Core Prose Identity, and a "Rhythm and Variation" subsection is added under Sentence Style. No existing rule is removed or reversed.
- Reviewers and any drafting AI should flag incidental staccato runs as a variation problem, not delete short sentences, and should treat the guide as advisory, allowing deliberate, for-effect deviations.
- Chapter 1 revision can now cite this entry when smoothing the marching-rhythm passages.

### Affected Documents

- `docs/10-vision/style/core-prose.md`
- `docs/10-vision/style/index.md` (the Style Guide it indexes; no edit required)

### Reconsider Only If

The author decides the clipped voice should be loosened across the board (which would change the baseline this entry assumes), or rules that the Style Guide should be treated as binding rather than advisory (which would retract the meta-principle). Both are reversible via git history.
