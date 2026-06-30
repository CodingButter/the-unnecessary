---
title: "Decision 060: Autonomous Resolution — The Crew Resolves, Logs, and Proceeds Instead of Blocking on the Author"
document_type: "decision"
status: "active"
authority: "governance"
summary: "Establishes the autonomous-resolution policy for the agent crew. When any agent hits a question, conflict, ambiguity, or unresolved finding, it must exhaust its own ability to resolve it before ever marking anything for the author: read every relevant canon and doc, apply the canon authority hierarchy (bibles win by subject; approved manuscript is canon; a blueprint is a plan, not canon; the more-specific/more-authoritative source wins; a bible reveal-gate beats a blueprint; and when a plan is internally contradictory the reveal-SAFE reading wins), consult the right specialist, and research online via research-consultant for real-world questions. It then makes a grounded best-effort decision and PROCEEDS, never blocking and never waiting on the author, recording every such call transparently in a `## Decisions Made (author may override)` log carrying the question, the decision, its grounding/authority, and confidence. This replaces the old BLOCKING author-flag disposition with loud, logged, overridable resolution. It does NOT weaken the standing rule against SILENTLY resolving a conflict: silent resolution (picking a winner with no trace, or averaging two versions) is still forbidden; this policy is its opposite, a loud and logged resolution. A genuine author-flag is reserved only for a pure creative preference with no canon-grounded best answer, and even then the crew picks the most defensible default and proceeds. Enacted by rewriting the disposition in the adjudicator and every other agent that punted a tension to the author (focus-reviewer, continuity-auditor, logic-auditor, echo-auditor, chapter-drafter, blueprint-author, entity-author, entity-extractor, audiobook-director, portrait-renderer, research-consultant, systems-engineer) and by aligning canon-hierarchy.md section 3. Reversible via git history."
tags: ["decision", "workflow", "crew", "agents", "conflict-handling", "autonomous-resolution", "governance", "reversible"]
related:
  - "../../canon-hierarchy.md"
  - "./056-character-bible-enrichment-and-two-resolved-flags.md"
  - "../index.md"
source_documents:
  - "docs/00-governance/canon-hierarchy.md"
  - ".claude/agents/adjudicator.md"
---

## Decision 060: Autonomous Resolution — The Crew Resolves, Logs, and Proceeds Instead of Blocking on the Author

**Date:** 2026-06-29
**Status:** Active but Revisable
**Category:** Workflow

### Decision

The author wants to be out of the loop while the crew produces chapters. The crew's disposition toward an unresolved finding is therefore changed across the board, from "flag it and wait" to "resolve it, log it, and proceed."

When any agent hits a question, conflict, ambiguity, or "unresolved" finding, it must **exhaust its own ability to resolve it before ever marking anything for the author.** To resolve, in order: read every relevant canon file, bible, approved chapter, blueprint, and continuity baseline; apply the canon authority hierarchy from the Development and Canon Guide and `canon-hierarchy.md` (approved manuscript is canon; a bible wins by subject; a blueprint is a plan, not an established event; the more-specific and more-authoritative source wins; a bible reveal-gate beats a blueprint; and when a plan is internally contradictory, the reveal-SAFE reading wins); consult the right specialist when the answer lives in another lane; and research online via research-consultant for real-world questions. Then make a grounded **best-effort decision and PROCEED.** Never block, never wait on the author.

Every such resolution is recorded transparently in a **`## Decisions Made (author may override)`** log: the question, the decision made, the grounding or authority it rests on (with `path:line` where load-bearing), and a confidence level. Read-only reviewers emit a decided, overridable resolution for the adjudicator to apply rather than "a suggestion for the author to decide"; edit-capable agents apply the best-effort, reveal-safe resolution to their own artifact and log it. The underlying canon-file conflict, when one exists, is still surfaced for deliberate canon-revision; the agent never edits a bible to match its own draft.

A genuine author-flag is reserved **only** for a pure creative preference with no canon-grounded best answer, and even then the crew picks the most defensible default and proceeds. The author reads the finished work plus the Decisions Made log and overrides anything.

### Reconciliation with the canon-conflict rule

The standing rule "never silently resolve a conflict" (CLAUDE.md and `canon-hierarchy.md` section 3) is **not** weakened. That rule forbids the *silent* resolution of a conflict: picking a winner with no trace, or averaging two versions into one and burying the disagreement. This policy is the **opposite** of that. It replaces the old *blocking* author-flag with resolution that is loud, logged, and overridable: the conflict is named, the controlling authority is named, the chosen reading and its grounding and confidence are written into the Decisions Made log, and the underlying canon-file conflict is still surfaced for deliberate canon-revision. What changes is only the *disposition* of an unresolved finding: the agent no longer halts the pipeline and waits on the author; it proceeds on the most defensible reveal-safe reading and leaves a transparent, overridable record. Silent merges remain banned; the bibles still win every conflict by subject; a true canon change is still enacted only by editing the owning canon file and recording a decision, never by an agent quietly asserting a fact.

### Previous or Alternative Direction

Under the previous direction, an agent that hit a conflict or ambiguity flagged it, named the controlling authority, recommended a resolution, and **stopped** — leaving the tension "unresolved for the author." `canon-hierarchy.md` section 3 stated this literally: "Only the orchestrator resolves a conflict; an agent flags it and stops." The adjudicator left canon conflicts "unresolved for the author"; the read-only reviewers (focus-reviewer, continuity-auditor, logic-auditor, echo-auditor) offered "a suggestion for the author to decide — never an applied change"; the drafting, blueprint, entity, audio, portrait, research, and tooling agents each punted their tensions to the author the same way. This kept the author in the loop on every snag and stalled chapter progress. The rejected alternative was to keep the blocking disposition (which contradicts the author's directive to be out of the loop) or to allow silent resolution (which would violate the never-silently-resolve rule and erode trust). This policy takes the third path: resolve loudly, log, proceed.

### Reason

The author's directive is to be out of the loop and to review the finished work, not to adjudicate each micro-conflict mid-pipeline. A blocking author-flag is the single biggest source of stalls in an otherwise autonomous crew. The fix is not to let agents resolve conflicts in the dark, which would breach the project's core trust rule, but to make resolution transparent and reversible: a loud, logged, overridable decision that the author can read and override after the fact. Grounding every decision in the canon authority hierarchy keeps the resolutions defensible; the reveal-SAFE tiebreak protects gated reveals when a plan is internally contradictory; and reserving true author-flags for pure creative preference (with a defensible default still chosen) means the pipeline never waits. Git history and the per-artifact Decisions Made log make every autonomous call traceable and reversible, consistent with the project's bias-to-action-under-git posture.

### Consequences

- The disposition in `.claude/agents/adjudicator.md` is rewritten from "flag unresolved for the author" to autonomous best-effort resolution plus a `## Decisions Made (author may override)` log in its return format. Its detection and rigor are unchanged; only what happens to an unresolved or conflicting finding changes.
- Every other agent that punted a tension to the author is updated the same way, detection intact: `focus-reviewer.md`, `continuity-auditor.md`, `logic-auditor.md`, `echo-auditor.md`, `chapter-drafter.md`, `blueprint-author.md`, `entity-author.md`, `entity-extractor.md`, `audiobook-director.md`, `portrait-renderer.md`, `research-consultant.md`, and `systems-engineer.md`. Each now carries an "Autonomous resolution — never wait on the author" section and emits a decided, overridable resolution into a Decisions Made log.
- Pure cross-crew routing and out-of-scope hand-offs (for example prose-critic routing a continuity issue to its owner) are preserved as-is; routing to the right specialist is part of the resolution machinery, not a block.
- The anti-fabrication rule is preserved exactly: a genuinely absent value or an entity that needs a new file is still routed (entity-extractor flags it for entity-author; entity-author never invents), never imagined. Autonomous resolution chooses among grounded sources; it never licenses inventing canon.
- `canon-hierarchy.md` section 3 is aligned: "an agent flags it and stops" is replaced with the autonomous-resolution disposition, while "never silently merge," "do not average," "do not pick a winner inside a canon file on your own," and the deliberate canon-revision path are kept intact.
- The author now reviews the finished work plus the Decisions Made log and overrides anything; the crew no longer waits on the author to progress a chapter.

### Affected Documents

- `.claude/agents/adjudicator.md`
- `.claude/agents/focus-reviewer.md`
- `.claude/agents/continuity-auditor.md`
- `.claude/agents/logic-auditor.md`
- `.claude/agents/echo-auditor.md`
- `.claude/agents/chapter-drafter.md`
- `.claude/agents/blueprint-author.md`
- `.claude/agents/entity-author.md`
- `.claude/agents/entity-extractor.md`
- `.claude/agents/audiobook-director.md`
- `.claude/agents/portrait-renderer.md`
- `.claude/agents/research-consultant.md`
- `.claude/agents/systems-engineer.md`
- `docs/00-governance/canon-hierarchy.md`

### Reconsider Only If

The author decides he wants to be back in the loop on conflicts before chapters proceed (which would restore the blocking author-flag), or rules that a particular class of conflict must always halt the pipeline rather than be resolved autonomously. Both are reversible via git history.
