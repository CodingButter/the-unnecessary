---
title: "Decision 044: mem0 Knowledge Graph Is On, With the Bibles as Higher Authority"
document_type: "decision"
status: "superseded"
authority: "governance"
summary: "The self-hosted mem0 knowledge graph is on, with relationships extracted by Gemini into Neo4j, while the bibles remain the higher authority and graph links are treated as recall hints requiring periodic pruning."
tags: ["decision", "workflow", "tooling", "mem0", "knowledge-graph"]
related:
  - "../../novel-development-guide.md"
  - "../index.md"
source_documents:
  - "archive/source-monoliths/creative-decision-log.md"
---

## Decision 044: mem0 Knowledge Graph Is On, With the Bibles as Higher Authority

**Status:** Locked for Current Workflow
**Category:** Workflow and tooling

### Decision

The self-hosted **mem0** knowledge graph is **on**. Relationships are extracted by **Gemini** (`gemini-2.5-flash-lite`, via `GOOGLE_API_KEY`) and stored in **Neo4j** (local `:7687`, Docker container `mem0-neo4j`).

Memory writes that relate entities should set `enable_graph=true` so the links are built.

All memory writes use `infer=false`. The graph extraction runs independently of `infer`, so the zero-cost policy is unaffected.

The bibles remain the higher authority. The graph aids recall of how characters, places, organizations, and decisions connect, but it does not establish canon and never overrides a bible.

### Previous or Alternative Direction

The previous stance, recorded in **Memory Conventions.md**, was that the knowledge graph was **off, deliberately**, on the reasoning that relationships live in the bibles and that LLM-extracted relationships would be less accurate than canon. Recall was vector-only.

### Reason

The graph gives cheap, free relationship recall (who connects to what, what the migration touches) without invoking the rate-limited path. Gemini extraction is independent of `infer`, so it adds no cost and no **HTTP 429** risk. The accuracy concern is addressed by subordinating the graph to the bibles rather than by disabling it.

### Consequences

The graph may produce relationships that diverge from bible canon. These are treated as recall hints, not truth, and must be verified against the relevant bible before anything load-bearing relies on them.

Divergent or stale graph links require **periodic pruning**.

Recall stays vector-first. Agents search memory, then cross-check against the bible, then draft.

### Affected Documents

- Memory Conventions.md
- CLAUDE.md
- .mcp.json
- .claude/hooks/mem0-recall.sh

No approved manuscript prose is affected. This is a tooling and workflow decision only; no story canon changes.

### Reconsider Only If

The Gemini-extracted graph proves more confusing than useful in practice (for example, persistent contradictions with the bibles that outpace pruning), or the cost or rate-limit profile of graph extraction changes.
