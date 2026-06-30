---
title: "Decision 061: Clarity Is the Default — Accidental Obscurity Is a Bug, Deliberate Withholding Is Not"
document_type: "decision"
status: "active"
authority: "governance"
summary: "Formalizes the author's standing 'clarity over literary density' direction into a named craft rule the whole crew follows: prose must be legible on the first pass (and, for audio, the first listen). The rule draws one precise line. Earned ambiguity stays: a withheld fact, a seeded foreshadow that pays off later, a subtext felt before it is named, a new concept explained a beat after it appears (a brief intentional 'wait for it'). Accidental obscurity is a clarity bug to fix: a poetic inversion whose agent is unclear (the worked example, 'the phone woke before he did,' which reads as if the phone acted), an untrackable referent, or a mini-puzzle with no payoff. The discriminator is PAYOFF, not plainness: vivid poetic prose that lands is the style's strength and is protected (the notice settling behind his sternum); only a line that forces a re-read, poetic or plain, is the target. The bar is doubly strict at chapter OPENINGS (no prior context) and in AUDIO (linear, unrereadable). Recorded as a named 'Clarity Is the Default' section in the Style Guide (docs/10-vision/style/core-prose.md), enforced by sharpening the clarity-auditor's standard (detection method unchanged), and identified as the explicit craft standard behind the interpretation-audit's resolve-vs-never-resolve distinction. Reconciles with Decision 058 (the guide is advisory, deliberate deviation is allowed) and with the working 'clarity over literary density' memory note it formalizes. Reversible via git history."
tags: ["decision", "style", "prose", "clarity", "craft-rule", "accidental-obscurity", "audio", "reversible"]
related:
  - "../../../10-vision/style/core-prose.md"
  - "../../../../.claude/agents/clarity-auditor.md"
  - "./058-sentence-variation-and-the-style-guide-is-a-guide.md"
  - "./037-the-tone-is-serious-restrained-and-morally-ambiguous.md"
  - "../index.md"
source_documents:
  - "docs/10-vision/style/core-prose.md"
  - ".claude/agents/clarity-auditor.md"
---

## Decision 061: Clarity Is the Default — Accidental Obscurity Is a Bug, Deliberate Withholding Is Not

**Date:** 2026-06-30
**Status:** Active but Revisable
**Category:** Style and tone

### Decision

The author's standing direction, **favor first-pass clarity over literary density**, is now a named craft rule the whole crew follows. The principle: prose must be legible on the **first pass**, and for audio on the **first listen**. A line that yields its plain meaning only on a second read has already failed; in audio, where the listener cannot go back, it fails twice. Clarity is the floor under the rest of the Style Guide, not a competitor to it.

The rule draws **one precise line**, and getting the line right is the whole point:

- **Earned ambiguity stays.** A withheld fact, a seeded foreshadow that pays off later, a subtext the reader feels before they can name it, a new concept introduced a beat before it is explained: this is the design working. A brief, intentional "wait for it" is a tool. The restrained voice, the subtext, and the deliberate slow reveal of the world all remain untouched.
- **Accidental obscurity is a clarity bug to fix.** A poetic inversion whose agent is unclear, an untrackable referent, or a mini-puzzle with no payoff is not depth; it is friction the author did not mean to create and the reader gets nothing for. It is fixed like a typo, not defended as a style.

The discriminator is **payoff, not plainness.** Vivid, poetic prose that lands on the first pass is the style's strength and is explicitly protected; the example kept in the guide is the notice settling behind his sternum. Only a line that forces a re-read, poetic or plain, is the target. The bar is **doubly strict** at two places: **chapter openings**, which have no prior context to lean on and carry the highest clarity bar, and **audio**, which is linear and cannot be reread, so anything that depends on re-reading is broken for the listener by definition.

The worked example of accidental obscurity, recorded in the Style Guide:

> The phone woke before he did.

Read as intended, the man wakes to his ringing phone; read as written, the phone is the agent that "woke" on its own, opening a momentary who-or-what-is-awake puzzle that pays off nothing. The fix preserves the image and removes only the accidental agent ("The phone was ringing before he was awake.").

This is recorded as a named **"Clarity Is the Default"** section in `docs/10-vision/style/core-prose.md`, beside the existing Central Stylistic Principle, and enforced by sharpening the **clarity-auditor** (`.claude/agents/clarity-auditor.md`): it now names accidental obscurity (unclear agent, untrackable referent, no-payoff puzzle) as a real clarity bug and spares deliberate seeds (a confusion that resolves later) and concepts explained soon, with its detection method (lay-reader retellings) left intact. The rule is identified as the explicit craft standard behind the interpretation-audit's **resolve-vs-never-resolve** distinction: a confusion that never resolves is the bug; one that resolves with full context is a working seed.

### Reconciliation with "clarity over literary density" and Decision 058

This formalizes the working **"clarity over literary density"** direction, which until now lived only as a session memory note and the working bias stated in the over-writing section of the Style Guide. It does not change that direction; it gives it a name, a precise line, and crew-wide authority. The note's own test is preserved exactly: the bar is "does it land on the first pass," not "is it plain," and clear-and-poetic prose that already reads clean is never flattened as "too simple."

It is fully consistent with **Decision 058** (the Style Guide is a guide, not an algorithm). Clarity is a **default and a bias**, not a mechanical rule to execute against every sentence. A deliberate, for-effect deviation, here a deliberately seeded confusion that the author means to pay off, is a choice and not an error, exactly as 058 affirms. The clarity rule does not forbid mystery; it forbids **accidental** mystery. Decision 058's operating rule still governs: when in doubt, follow the guide and write for first-pass clarity; when doing something special, seed the confusion on purpose and pay it off.

### Previous or Alternative Direction

The Style Guide already carried a "standing bias is clarity over density, show do not tell, trust the image" inside the over-writing section, and the Final Style Standard already asked that the narration "remain clear enough that the reader always understands what is happening." But clarity was never stated as its own named principle, the line between intended withholding and accidental obscurity was never drawn explicitly, and the audio and chapter-opening cases were not called out. The "clarity over literary density" preference existed only as a working memory note, not as canon craft. The rejected alternatives were to leave clarity as an implicit bias (which let dense or inverted lines be defended as "earned weight") or to state it so flatly that it read as "make everything plain," which would have flattened the voice and explained away intended mystery, the opposite of the intent.

### Reason

The author judges the plot and story interesting enough to carry the reader, so the prose does not need to be maximally literary everywhere, and a line that forces a re-read at an important beat costs more than the flourish is worth, especially in audio where there is no glance backward. Naming clarity as the default and drawing the payoff line precisely gives every drafter and reviewer one shared, defensible standard, and protects the voice from both failure modes at once: it stops accidental obscurity from hiding behind "depth," and it stops a literal reading from flattening intended subtext and slow reveal. Anchoring the clarity-auditor and the interpretation-audit to the same standard means the automated clarity passes now judge against an explicit rule rather than an implicit feel.

### Consequences

- `docs/10-vision/style/core-prose.md`: a named **"Clarity Is the Default"** section is added after the Central Stylistic Principle, with the two-confusions line, the "phone woke before he did" worked example, and the openings/audio emphasis. No existing rule is removed or reversed.
- `.claude/agents/clarity-auditor.md`: a "standard you judge against" block, a sharpened FRICTION definition naming the accidental-obscurity signatures, and a payoff-keyed spare in its discipline step are added. Its **detection method (lay-reader retellings) is unchanged**; only the standard it judges against is sharpened.
- The whole crew (drafter, prose-critic, adjudicator, and the clarity/interpretation passes) now treats first-pass legibility as the default and accidental obscurity as a real bug, while sparing deliberate seeds and soon-explained concepts.
- The interpretation-audit's resolve-vs-never-resolve distinction is now backed by a stated craft rule rather than an implicit one.
- The voice is unchanged: restraint, subtext, slow world-reveal, and clear-and-poetic imagery all remain protected.

### Affected Documents

- `docs/10-vision/style/core-prose.md`
- `.claude/agents/clarity-auditor.md`
- `docs/00-governance/decision-log/index.md` (index row added)

### Reconsider Only If

The author decides the prose should lean into literary density at the cost of first-pass legibility, or rules that a particular kind of intended ambiguity is being over-flagged as accidental obscurity (which would adjust where the payoff line sits, not retract the principle). Both are reversible via git history.
