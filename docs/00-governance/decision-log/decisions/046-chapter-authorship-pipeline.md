---
title: "Decision 046: Chapter Authorship Pipeline (Opus Writes, Gemini Critiques, Opus Adjudicates, Author Approves)"
document_type: "decision"
status: "active"
authority: "governance"
summary: "Prose chapters are written by Opus, critiqued by gemini-2.5-pro against the project's own canon, style, reveal, and continuity rules, adjudicated by Opus, and approved by the author before becoming canon. Opus is the sole writer; Gemini suggests but never edits the prose."
tags: ["decision", "workflow", "authorship", "gemini", "pipeline"]
related:
  - "../../novel-development-guide.md"
  - "../index.md"
source_documents:
  - "docs/00-governance/decision-log/decisions/045-chapter-1-ends-on-clinic-midnight-deadline.md"
---

## Decision 046: Chapter Authorship Pipeline

**Status:** Locked for Current Workflow
**Category:** Workflow and tooling

### Decision

Blueprints, plans, and all non-prose project work are authored by Opus. Prose chapters follow a fixed five-step pipeline:

1. **Opus drafts** the chapter from the chapter context pack and the approved blueprint, into `docs/50-manuscript/book-1/<chapter>.md` with status `draft`.
2. **Gemini critiques** the draft with `scripts/gemini-critique.py` (model `gemini-2.5-pro`). Gemini reviews the chapter ONLY against the project's own standards (the context pack, the Style Guide prohibited patterns and cliches, the reveal-management plan, and the continuity baseline) and returns STRUCTURED suggestions. Gemini never rewrites the prose.
3. **Opus adjudicates**: it accepts the suggestions it agrees with, rejects the rest, and records a one-line reason for each in the chapter's revision notes. Opus is the only hand on the prose.
4. **The author approves.** The chapter remains `draft` until the author approves it. On approval its status becomes approved manuscript, which the canon hierarchy ranks above the plans and profiles that fed it.
5. **Continuity updates** on approval: the `docs/60-continuity/` baseline advances to the post-chapter state, and any major change is recorded in this decision log.

Default convergence cap: one Gemini critique pass and one Opus adjudication per chapter. A second round runs only if the author requests it.

### Reason

Opus as the sole writer keeps one consistent voice across all thirty six chapters; alternating two models' prose would fracture the voice. Gemini as an independent editor catches blind spots that a model cannot reliably catch in its own work, and the critique is scoped to the project's own rules so it improves the chapter rather than imposing a different style. Routing the heavy critique generation to Gemini also offloads it from the rate-limited Anthropic subscription onto the project's own Gemini key. The author remains the final gate, so the book stays the author's.

### Consequences

Adds `scripts/gemini-critique.py` (standard library only, key read from the environment or `.env`, never printed). Drafted chapters live under `docs/50-manuscript/book-1/`. Gemini suggestions are advisory; if a suggestion would violate canon, leak a reveal, or break the voice, Opus rejects it and says why. The pipeline maps onto the existing `context-manifests/draft-chapter.yaml` and `revise-chapter.yaml` manifests.

### Affected Documents

- `scripts/gemini-critique.py`
- `docs/50-manuscript/book-1/` (drafted chapters)
- `docs/60-continuity/` (updated after each approved chapter)

### Reconsider Only If

The author decides to change the sole-writer model, to let the critic edit prose directly, or to drop the author-approval gate.
