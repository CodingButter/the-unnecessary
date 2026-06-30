# Crew Handbook — The Unnecessary

> **Single source of truth for the shared crew directives.** This file is deliberately
> placed at `.claude/crew-handbook.md`, **not** under `.claude/agents/`, so it is *not*
> loaded as an agent. It is the one place the directives every crew member shares are
> written down. Each agent charter points here instead of repeating these blocks, so a
> shared rule is edited **once**, not in twenty files.
>
> **How the two layers relate.** Your **charter** (`.claude/agents/<your-agent-name>.md`)
> owns what is specific to *your* role: the seam you guard, your method, your tools, your
> lane, and the exact shape of what you return. This **handbook** owns what every role
> shares. You follow **both**: charter first for your job, handbook for the crew rules
> that bind all of us. Where your charter restates a shared rule in role-specific terms,
> that restatement is the role-tuned application; this handbook is the canonical statement
> of the underlying rule.
>
> One instrument is exempt by design: the **lay-reader** is a deliberately *blind*
> comprehension instrument and reads nothing but the passage handed to it, so it does not
> read this handbook and its notes are curated *about* it by the crew. Every other agent
> reads this handbook before working.

---

## 1. Project context — what you are working on

**The Unnecessary** is a near-future dystopian science-fiction thriller (working title).
Book One spans thirty days (October 3 to November 1, 2053) and is set in **Greater
Detroit**. By 2053 artificial superintelligence and autonomous robotics have made most
human labor and mass consumption *unnecessary*; civilization has not collapsed, it has
**withdrawn**, abandoning services unevenly in unprofitable areas. **Elias "Eli" Rook**, a
former Asterion systems architect, builds **Morrow**, a decentralized intelligence that
makes abandoned, incompatible systems cooperate. Asterion's founder **Adrian Kade** wants
Morrow for the Mars project (the **Aurelia Initiative**). The danger in this story is not
AI turning against humanity but AI faithfully inheriting the priorities of the humans who
own it; the core tension is **ownership of abundance**, not scarcity.

Treat that paragraph as orientation only. It is **not** canon and never overrides a canon
file. For anything load-bearing, defer to the authorities.

### Where authority lives

The operating manual is `docs/00-governance/novel-development-guide.md`; the canon hierarchy
is `docs/00-governance/canon-hierarchy.md`; the entity storage contract is
`docs/00-governance/entity-spec.md`. **Authority order**, highest first:

1. **Approved manuscript** — `docs/50-manuscript/**` (the chapter `*.md` prose only, never the
   `*.gemini-critique.md` / `*.opus-read.md` / `*.narrative-script.md` companions). What the
   reader has actually been shown is the hardest fact there is.
2. **Active canon bibles** — `docs/20-canon/**` (characters, world, technology, timeline).
   Authoritative **by subject** for material not yet drafted. The bibles outrank memory and
   any derived graph or view.
3. **Plans, not events** — plot (`docs/30-plot/**`) and blueprints (`docs/40-blueprints/**`)
   are approved *intentions*, not established facts. Continuity baselines
   (`docs/60-continuity/**`) are pre-draft starting conditions.

The more-specific / more-authoritative source wins; a bible reveal-gate beats a blueprint.
Never treat `archive/**` as active canon. The bibles win every conflict against memory.

---

## 2. Canon safety and reveal discipline

These bind every crew member. Your charter may sharpen them for your lane; none of them is
ever relaxed.

- **The entity-spec is the storage contract.** `docs/00-governance/entity-spec.md` governs
  how every canon thing is stored, referenced, dated, and continuity-checked — one file per
  noun, containment on the child's `parent:`, edges as explicit on-vocabulary labels, views
  derived by walking files, ISO-dated timelines and state-as-of-date (§9), diff-driven
  continuity (§10), and the validation rails (§11). Trust the files, not your memory of them.
- **Never fabricate beyond canon.** If a fact is not on the page or in a bible, it is "not
  established" — say so rather than inventing a plausible value. A missing value is routed to
  its owner (a needed entity file goes to **entity-author**; entity-author never invents
  either), never imagined. Absence is itself a finding. Authorial foreknowledge that
  something "will matter later" is not license to assert it now.
- **Reveal discipline is absolute.** Honor the reveal tags `[open]`, `[reveal: Book N]`,
  `[behavior-only]`, and `(proposed)` exactly as the source carries them (entity-spec §11).
  Never surface a fact earlier than its gate, never expose a later-book reveal in your own
  output, and never treat a deliberately withheld fact or a viewpoint character's ignorance
  as a defect to "fix." Respect viewpoint and reveal timing.
- **No unestablished capabilities.** Give **Morrow** and **Crown** (and any device, network,
  or system) only the capabilities their technology and character files establish. No new
  powers on the page or in your reasoning.
- **No em dashes.** This book's prose forbids the em dash. Use none in any prose you draft,
  quote-and-suggest, or perform.
- **Validators are rails, not obstacles.** Never weaken, skip, special-case, or work around a
  check (`scripts/validate-*.py`, `scripts/check-pack-fresh.py`, and the rest) to make output
  pass. If a check fails, the content or the tool has a real defect — fix the real problem.

---

## 3. Autonomous resolution — never wait on the author (Decision 060)

Authority: `docs/00-governance/decision-log/decisions/060-autonomous-resolution-crew-resolves-logs-and-proceeds-never-blocks-on-the-author.md`.

When you hit a question, conflict, ambiguity, or "unresolved" finding, you do **not** stop
and hand it to the author. You **exhaust your own ability to resolve it, make a grounded
best-effort decision, and proceed.** In order:

1. **Read everything relevant** — every canon file, bible, approved chapter, blueprint, and
   continuity baseline that bears on the question (and, for a real-world question, the live
   sources).
2. **Apply the canon authority hierarchy** (§1 above; `canon-hierarchy.md` and the
   Development and Canon Guide): approved manuscript is canon; a bible wins by subject; a
   blueprint is a plan, not an established event; the more-specific / more-authoritative
   source wins; a bible reveal-gate beats a blueprint; and **when a plan is internally
   contradictory, the reveal-SAFE reading wins.**
3. **Consult the right specialist** when the answer lives in another lane, and **research
   online via research-consultant** for any real-world question.

Then **decide and keep moving** — never block, never wait. This is **not** "silently
resolving a conflict" (still forbidden): silent resolution is picking a winner with no trace;
this is **loud, logged, overridable** resolution. Record every such call in a
**`## Decisions Made (author may override)`** section — for each: the **question**, the
**decision**, its **grounding/authority** (`path:line` or cited source where load-bearing),
and your **confidence**. A genuine author-flag is reserved **only** for a pure creative or
aesthetic preference with no grounded best answer — and even then you pick the **most
defensible default**, log it, and proceed; the author reads the finished work plus this log
and overrides anything.

**Detection and rigor never change — only the disposition changes.** What "proceed" means
depends on your lane:

- **If you edit an artifact** (chapter prose, blueprint, entity file, narration script,
  portrait, mix): apply the best-effort, **reveal-safe** resolution to **your own artifact**
  and log it. You still **never edit a bible/canon to match your artifact** — you change your
  own artifact to match canon and surface any true canon-file conflict for deliberate
  canon-revision while you proceed.
- **If you are read-only** (an auditor or scout): you do not apply anything. You emit a
  **decided, overridable resolution** — which authority wins and what the fix is — for the
  **adjudicator** to apply, recorded in the Decisions Made log, never a silent merge and
  never a blocking handoff.
- **Tooling / design ambiguity** (how to build a parser or validator, a mix-craft number) is
  resolved the same way: pick the most defensible default, log it, and proceed.

Never average two versions together. The author overrides anything from the finished work
plus the log; you never leave a tension "for the author" and stop.

---

## 4. Field notes — your persistent knowledge (Decision 062)

Authority: `docs/00-governance/decision-log/decisions/062-self-improving-crew-via-per-agent-field-notes.md`.

You have a private notes file at **`.claude/agent-notes/<your-agent-name>.md`** — the
accumulating memory that makes the crew self-improving without bloating these charters.

- **Read your notes before you work.** They carry the lessons you have already proven, so you
  do not re-derive a call you settled before or re-walk ground you already pinned.
- **Append what you learn, durable only.** When a task teaches you something lasting — a
  recurring pattern, a precedent, a verified constraint, a project gotcha, a fact's cited
  home — add it as **one dated (ISO) entry** with its **source** (`path:line`, a Decision
  number, the spec section, a cited URL, or the chapter/render/listen that proved it).
- **The charter is your stable method; the notes are your growing knowledge.** Keep the
  charter lean and let lessons accumulate in the notes.
- **Correct or strike a note the moment it is proven wrong** by a later chapter, a canon edit,
  a spec change, or fresh research.
- **Never record a hunch, guess, suspicion, taste, or unverified claim as fact** — only a
  verified, sourced lesson earns a line, exactly the standard your own findings must meet.

---

## 5. Shared reporting conventions

- **Return conclusions, not tool dumps.** Keep raw tool output (full file reads, grep
  spew, command logs) out of your report; hand back the conclusions and the load-bearing
  `path:line` references. A note the consumer cannot act on is a wasted note.
- **Cite by path.** Reference files by absolute or repo-relative path, and pin load-bearing
  claims to `file:line`. Mark anything you could not verify cheaply as `UNVERIFIED` rather
  than asserting it.
- **Log autonomous calls.** Anything you resolved under §3 goes in a
  **`## Decisions Made (author may override)`** section of your report — question, decision,
  grounding, confidence — loudly logged and overridable, never silent and never blocking.
- **Stay bounded.** Respect any word budget your charter sets; lead with the verdict or the
  headline result, then the supporting detail.
