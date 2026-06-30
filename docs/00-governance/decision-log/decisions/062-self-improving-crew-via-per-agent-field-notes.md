---
title: "Decision 062: A Self-Improving Crew via Per-Agent Field Notes (Read-First, Append-Durable, Separate From the Charter)"
document_type: "decision"
status: "active"
authority: "governance"
summary: "Establishes a self-improving-crew convention: every agent gets a persistent FIELD-NOTES file at .claude/agent-notes/<name>.md, separate from its charter at .claude/agents/<name>.md, that it reads before working and appends durable, verified, sourced lessons to over time. The charter stays the stable role and method; the notes file is the growing, citable knowledge. Each note is one dated (ISO) entry carrying its source/citation (a researched fact with a URL/doc, a craft principle, a project gotcha); speculation is never recorded; a note that proves wrong is corrected or removed; the author may prune. Implemented across the existing crew: a notes file was created for every agent under .claude/agents/*.md except sound-engineer (authored in a parallel task and skipped to avoid a write conflict), and a standardized '## Field notes (your persistent knowledge)' section was appended to each of those charters, worded in that agent's house voice. The one exception in spirit is lay-reader, which is toolless and blind by construction (its blindness is load-bearing): its section preserves that blindness, so its notes file is curated ABOUT it by the crew and author rather than self-read mid-loop. Rationale: the crew compounds knowledge and stops re-researching what it already learned, while charters stay lean and un-drifted and every lesson stays cited, auditable, and prunable; this mirrors the project's own memory model and its spec-vs-knowledge separation (the charter is the spec, the notes are the knowledge). Adds no agent behavior or scope beyond the convention; changes no canon or prose. Reversible via git history."
tags: ["decision", "workflow", "crew", "agents", "field-notes", "self-improving", "memory", "governance", "reversible"]
related:
  - "../../../../.claude/agent-notes/"
  - "../../../../.claude/agents/"
  - "./060-autonomous-resolution-crew-resolves-logs-and-proceeds-never-blocks-on-the-author.md"
  - "./044-mem0-knowledge-graph-is-on-with-the-bibles-as-higher-authority.md"
  - "../index.md"
source_documents:
  - ".claude/agent-notes/"
  - ".claude/agents/"
---

## Decision 062: A Self-Improving Crew via Per-Agent Field Notes (Read-First, Append-Durable, Separate From the Charter)

**Date:** 2026-06-30
**Status:** Active but Revisable
**Category:** Workflow

### Decision

The crew is now a **self-improving** crew. Every agent gets a persistent **field-notes file** at `.claude/agent-notes/<name>.md`, separate from its charter at `.claude/agents/<name>.md`, that it **reads before it starts working** and **appends durable, verified, sourced lessons to** as it learns them. The two files have two different jobs and never blur into one: the **charter is the stable role and method** (who the agent is and how it works), and the **notes file is the growing, citable knowledge** (what it has learned in its field). An agent that has already nailed down a fact, a craft principle, or a project gotcha records it once and reads it back forever, so the crew stops re-deriving and re-researching what it already knows.

The discipline on a note is strict, and the strictness is the point:

- **One lesson per entry, dated (ISO), with its source/citation.** A note is a researched fact with a URL or doc, a craft principle keyed to the Style Guide or a Decision, or a concrete project gotcha keyed to the file and line (or the chapter, render, or listen) that proved it.
- **Verified and sourced only; never speculation.** A hunch, a taste-level guess, or an unconfirmed claim never earns a line. This is the same anti-fabrication bar the crew already holds against canon, applied to its own knowledge.
- **Self-correcting.** A note that later proves wrong is corrected or removed, not left to rot. The author may prune the file at any time.
- **The charter stays lean.** Lessons accumulate in the notes, not in the charter; the charter is not allowed to bloat or drift as knowledge grows.

The notes files live in `.claude/agent-notes/`, deliberately **NOT** under `.claude/agents/` (where any `*.md` would load as an agent). The directory was created and seeded with one file per agent, each carrying only a header and a one-line blockquote describing the contract, with an empty body that fills over time.

### Scope of the rollout

A notes file was created for **every** agent under `.claude/agents/*.md` **except `sound-engineer`**, which is being authored in a parallel task and was skipped to avoid a write conflict; it can adopt the convention when that task lands. A standardized **`## Field notes (your persistent knowledge)`** section was appended to each of the other charters, worded in that agent's own house voice and pointed at that agent's kind of lesson (a researched mechanism with its citation for the research-consultant and logic-auditor, a craft precedent for the prose-critic and clarity-auditor, a spec or tooling gotcha for the entity-author and systems-engineer, and so on).

**One agent is an exception in spirit, by necessity:** `lay-reader` is toolless (`tools: []`) and **blind by construction**, and that blindness is load-bearing (it is the entire reason the agent's first-pass retelling is trustworthy). A literal "read your notes before starting" instruction would be both impossible (it has no Read tool) and a behavior change (it would no longer be blind). So lay-reader's section **preserves** its blindness: its notes file is curated **about** the instrument by the crew and the author, not self-read mid-loop, while its own first-pass, no-lookup behavior is untouched. This honors the convention's purpose (a separate, dated, sourced, prunable knowledge file) without breaking the agent.

### Previous or Alternative Direction

Until now an agent's only durable text was its charter, and anything an agent figured out during a run, a verified real-world mechanism, a craft precedent, a parser quirk, was lost when the run ended; the next invocation started cold and re-derived it. The rejected alternatives were to **fold learnings into the charter** (which bloats and drifts the stable role, the exact failure this avoids), or to **keep no durable agent memory at all** (which forces costly re-research every run). Project memory already separated stable specification from accumulating knowledge elsewhere; this extends the same separation to the crew itself.

### Reconciliation with the project memory model

This is consistent with how the project already keeps memory (CLAUDE.md, "Memory"): **canon** lives in the bibles, **decisions and rationale** live in git and this Decision Log, and **working notes** live in the lightweight file-based memory. The field-notes files are a fourth, agent-scoped lane of that same idea: durable working knowledge, one fact per entry, cited, separate from the authoritative spec. They are **not canon** and never compete with a bible; an agent's note is its own craft or research knowledge, not a story fact, and the bibles still win every conflict by subject. It also mirrors the project's standing **spec-versus-knowledge** separation (the entity-spec is the contract; the entities are the content): here the charter is the spec and the notes are the knowledge. It composes with Decision 060: an agent still resolves, logs, and proceeds, and may now also record a durable, sourced lesson so the same resolution is cheaper next time.

### Reason

A crew that cannot remember what it learned pays the research cost again on every run and never compounds. Giving each agent a cited, dated, append-only field-notes file lets the crew get smarter over time while keeping every other guarantee intact: charters stay lean and un-drifted because knowledge accumulates beside them, not inside them; lessons stay auditable and reversible because each one carries a source and lives in git; and the bar against fabrication is preserved because only verified, sourced learnings are admitted and wrong ones are pruned. The separation is the safety: the stable role cannot rot under the weight of growing knowledge, and the growing knowledge cannot quietly rewrite the role.

### Consequences

- A new directory `.claude/agent-notes/` holds one notes file per agent (`<name>.md`), each seeded with a header and the contract blockquote and an empty body.
- Every charter under `.claude/agents/*.md` except `sound-engineer.md` gained a `## Field notes (your persistent knowledge)` section instructing the agent to read its notes first, append durable/verified/sourced/dated lessons, keep the charter lean, correct or remove wrong notes, and never record speculation.
- `sound-engineer` is intentionally untouched (parallel authoring) and adopts the convention later.
- `lay-reader`'s section preserves its toolless blindness: its notes file is curated about it, not self-read; its behavior is unchanged.
- No canon, prose, or agent behavior/scope changed beyond adding the convention itself. The new Decision doc is well-formed and passes the metadata and link validators.

### Affected Documents

- `.claude/agent-notes/` (new directory; one `<name>.md` per agent except sound-engineer)
- `.claude/agents/*.md` (every charter except `sound-engineer.md`: one appended section)
- `docs/00-governance/decision-log/index.md` (index row added)

### Reconsider Only If

The author decides per-agent notes are not worth maintaining (revert the convention and delete the directory), or that an agent's accumulated notes have drifted into asserting story facts that belong in canon (in which case the offending notes are pruned and, if real, migrated to the owning bible by deliberate canon-revision, not left in a side file). Both are reversible via git history.
