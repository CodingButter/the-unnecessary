---
title: "The Unnecessary, Project Instructions"
document_type: "governance-guide"
status: "active"
authority: "governance"
summary: "Per-session entry layer for the novel: what the project is, where authority lives, the per-session story rules, the task-routing table, and the mem0 operating protocol."
tags:
  - governance
  - entry-point
  - mem0
related:
  - "docs/00-governance/context-loading-guide.md"
  - "docs/00-governance/canon-hierarchy.md"
source_documents:
  - "migration/REPOSITORY-REORGANIZATION-SPEC.md"
---

# The Unnecessary — Project Instructions

> Loaded into every session. This file is the **entry / operational layer**, not a
> canon document. It tells you what the project is, where authority lives, and how to
> use persistent memory. It does **not** define story canon and must never silently do
> the job of a canon or planning document.

## What this project is

**The Unnecessary** is a near-future dystopian science-fiction thriller (working title;
the Story Bible lists alternates such as *A World Without Us* and *Human Value*). It is a
**novel project, not a software product.** Book One is the first of a planned multi-book
series, written as "grounded cyberpunk" without the visual cliches.

Premise, in brief: by 2053, artificial superintelligence and autonomous robotics have made
most human labor and mass consumption unnecessary. Civilization has not collapsed in an
apocalypse — it has *withdrawn*, abandoning services unevenly in unprofitable areas. Elias
"Eli" Rook, a former Asterion systems architect who helped create the **Mosaic** orchestration
architecture, builds **Morrow**, a decentralized intelligence that makes abandoned,
incompatible systems cooperate. Asterion's founder **Adrian Kade** wants Morrow for the
Mars project (the **Aurelia Initiative**) and fears it could let abandoned communities
survive without corporate support. The danger in this story is not AI turning against
humanity but AI faithfully inheriting the priorities of the humans who own it. The core
tension is **ownership of abundance**, not scarcity. Primary setting: **Greater Detroit**.
Book One spans thirty days (October 3 to November 1, 2053).

That is the most this file should say about canon. For anything load-bearing, go to the
authorities below — do not reason from this paragraph.

## Where authority lives (defer; do not duplicate)

| Authority | Document | Owns |
|---|---|---|
| **Operating manual** | `Development and Canon Guide.md` | The canon hierarchy, conflict-handling rules, drafting discipline, context packages, workflow phases, folder structure, versioning. **Defer to it on all process and conflict questions.** |
| **Memory spec** | `Memory Conventions.md` | How mem0 is used while drafting — what to store, the metadata schema, recall-then-draft discipline. **Defer to it on memory practice.** |
| Canon (by subject) | `Narrative Brief.md`, `Story Bible.md`, `Character Bible.md`, `Technology Rules.md`, `Master Timeline.md`, `Plot Outline and Chapter Map.md`, `Style Guide.md`, `Creative Decision Log.md` | Authoritative story facts. The bibles win every conflict against memory. |

Two non-negotiable principles inherited from the Canon Guide:

1. **No document silently does another's job.** This file orients and operates; it never
   establishes, overrides, or quietly edits canon.
2. **Never silently resolve a conflict.** When documents disagree, state which conflict,
   which authority normally controls that fact type, whether approved prose is affected,
   and a recommended resolution — then follow the Canon Guide's process. Do not average
   two versions together.

The project is mid-**migration** toward a structured `docs/` tree (`docs/00-governance/`,
`docs/10-vision/`, `docs/20-canon/`, `docs/30-plot/`, `docs/40-blueprints/`,
`docs/50-manuscript/`, `docs/60-continuity/`, `docs/70-research/`), with `context-manifests/`,
`scripts/`, and `archive/` alongside. Work happens on the `migration` branch and integrates
to `main`. The separation-of-responsibilities is the load-bearing part.

## Working on the novel (per-session rules)

This is a novel project, not a software product. Before any story work, read
`docs/00-governance/context-loading-guide.md`. Never load the whole repository by default;
start from the appropriate context manifest in `context-manifests/`. Then:

- Treat approved manuscript as established canon.
- Treat active canon files (`docs/20-canon/**`) as authoritative by subject.
- Treat plot files and blueprints as approved plans, not already-established events.
- Never use archived files (`archive/**`) as active canon.
- Flag conflicts instead of silently resolving them.
- Do not change canon unless explicitly asked.
- Avoid em dashes in drafted prose.
- Preserve viewpoint and reveal timing.
- Update continuity after approved manuscript changes.
- Record major revisions in the Decision Log.
- Do not expose future reveals in earlier chapter work.
- Do not give Morrow or Crown unestablished capabilities.

## Task routing

Start each task from its context manifest (the manifest files are created in a later
migration phase; until then, treat these as the intended entry points):

| Task | Start with |
| --- | --- |
| Create chapter blueprint | `context-manifests/create-chapter-blueprint.yaml` |
| Draft chapter | `context-manifests/draft-chapter.yaml` |
| Revise chapter | `context-manifests/revise-chapter.yaml` |
| Check continuity | `context-manifests/continuity-check.yaml` |
| Revise canon | `context-manifests/canon-revision.yaml` |
| Research technology | `context-manifests/technology-research.yaml` |

---

# mem0 — Operating Protocol (MANDATORY)

We run a **self-hosted mem0** as persistent, cross-session memory. Use it on every task.
This section is the operational protocol; `Memory Conventions.md` is the fuller spec on
*what* to store and *how to phrase it* — defer to it.

## What it is (architecture)

| Layer | Backend | Notes |
|---|---|---|
| Vector store | **Qdrant** (local `:6333`), collection `novel_memory` | semantic search |
| Embeddings | **Ollama** `nomic-embed-text`, **768 dims** (local `:11434`) | never change dims without rebuilding the collection |
| Graph / relationships | **Neo4j** (local `:7687`, Docker container `mem0-neo4j`) | entity linking — **ON** |
| Graph extraction LLM | **Gemini** (`gemini-2.5-flash-lite`, via `GOOGLE_API_KEY`) | builds relationships; independent of `infer` |
| Memory scope | `user_id = "novel"` | always use this scope |

Config lives in `.mcp.json` (`mem0` server block). Recall on session start is wired via
`.claude/hooks/mem0-recall.sh` + `.claude/settings.json` (search-only, free, no 429).

## THE GOLDEN RULES

1. **ALWAYS write with `infer=false`.** Never `infer=true`. `infer=true` invokes the main
   LLM, which runs on the throttled Claude **subscription** token and fails with **HTTP
   429** — we are zero-cost, there is no paid Anthropic key. `infer=false` stores text
   verbatim via local embeddings: fast, free, reliable. Gemini still builds the graph
   independently of `infer`.
2. **Set `enable_graph=true`** on writes that contain relationships between entities
   (characters, places, organizations, AI systems, decisions). Gemini extracts the links;
   this is free and does not touch Anthropic.
3. **Always scope to `user_id="novel"`.** Do not invent other scopes.
4. **Recall before you act.** Search mem0 — and the relevant bible — at the start of a task.

## The graph is ON — with canon subordinate

The Neo4j knowledge graph runs (Gemini extraction). It aids recall of how entities relate;
it does **not** establish canon. **The bibles outrank the graph in every conflict.**
LLM-extracted relationships may drift from bible canon and will need **periodic pruning** —
treat graph links as recall hints, never as authority.

## Metadata schema (use this; do NOT add a `category` field)

Attach `metadata` so memories can be filtered:

```json
{ "type": "decision", "chapter": 9, "characters": ["Eli"], "tags": ["morrow", "continuity"] }
```

`type` ∈ `{ decision, fact, continuity, deviation, hazard }`. Plus `chapter`, `characters`,
`tags`. This is the schema in `Memory Conventions.md` — match it exactly.

## Write protocol (persist)

Save a memory when you settle something **durable and not already in a bible or git**.
Canonical write shape:

```
add_memory(
  text="<one atomic, self-contained fact with its story anchor>",
  user_id="novel",
  infer=false,            # ALWAYS
  enable_graph=true,      # when the fact has relationships
  metadata={"type": "decision", "chapter": 9, "characters": ["Eli"], "tags": ["morrow"]}
)
```

**DO save:** drafting decisions and rationale; established micro-facts ("Established ch. 9:
…"); deviations from the outline with reasons; continuity hazards; small voice rulings.
**DON'T save:** anything already in a bible (cite the bible instead); secrets/keys; prose
passages (store the *decision about* the prose); duplicates — search first and
`update_memory` instead of re-adding. Write standalone sentences, not pronouns or
session-relative phrasing.

## Recall protocol (read)

- The **SessionStart hook auto-injects** relevant memories — read them as ground truth.
- For any new scene, topic, or continuity question, `search_memories` with a meaning-rich
  query first, then **cross-check anything load-bearing against the relevant bible**, then
  draft.
- Use `mcp_search_graph` / `mcp_get_entity` to discover relationships — as hints, not canon.

## Agents & workflows — propagate the protocol (novel work)

Subagents and workflow agents do NOT inherit this file. The orchestrator propagates it:

1. **Every** agent/workflow prompt MUST include the **directive block below** (verbatim).
2. Agents **search mem0 first AND read the relevant bible first** — drafters, researchers,
   and continuity-checkers all ground in canon before producing anything.
3. Agents **do not write memories directly.** They return a **`## Memory candidates`**
   section listing standalone, durable facts. The **orchestrator dedupes and writes them**
   with `infer=false` — this keeps the graph consistent and avoids concurrent duplicate or
   contradictory nodes.
4. At the end of a meaningful unit of work, the orchestrator persists the curated outcomes
   (this replaces the disabled auto-save Stop hook).

### Directive block (paste verbatim into agent/workflow prompts)

```
MEMORY + CANON: This is the novel "The Unnecessary" (user_id="novel" for mem0).
Before starting, (a) load mcp__mem0__search_memories and search your task topic, and
(b) read the relevant bible(s) — they outrank memory and the graph on all canon.
Do NOT write memories yourself, and do NOT silently resolve doc conflicts (flag them).
In your final report add a "## Memory candidates" section: a bullet list of standalone,
durable facts (decisions, gotchas, continuity, deviations, hazards) worth persisting with
metadata {type, chapter, characters, tags} — or "none". The orchestrator writes them
with infer=false.
```

## Tool cheat sheet

| Need | Tool | Key args |
|---|---|---|
| Save a fact | `mcp__mem0__add_memory` | `text`, `user_id="novel"`, `infer=false`, `enable_graph=true` |
| Find by meaning | `mcp__mem0__search_memories` | `query`, `user_id="novel"` |
| Browse all | `mcp__mem0__get_memories` | `user_id="novel"`, `limit` |
| Fix a fact | `mcp__mem0__update_memory` | `memory_id`, `text` |
| Entity's relationships | `mcp__mem0__mcp_get_entity` | `name` (exact) |
| Search the graph | `mcp__mem0__mcp_search_graph` | `query` |
| Who holds memories | `mcp__mem0__list_entities` | — |
| Wipe a scope | `mcp__mem0__delete_all_memories` | `user_id` (destructive) |

## Constraints & gotchas

- **`infer=true` ⇒ 429.** Single most important rule. A RateLimitError on write means you
  used `infer=true`; retry with `infer=false`.
- **Neo4j must be running** for graph writes/reads. Container `mem0-neo4j`
  (`docker start mem0-neo4j` if down; `--restart unless-stopped`).
- **`"Ollama embed() returned no embeddings"` on a graph write** ⇒ Gemini emitted an
  empty/whitespace entity (likelier for text dense with symbols like `infer=false` /
  `HTTP 429`); embedding the empty string returns no vector and the graph step throws.
  **CRITICAL:** the vector memory commits *before* the graph step, so the error does **not**
  roll it back — the memory is already stored. **Do NOT blindly retry** (each retry stores a
  duplicate). Treat the vector write as done; to get graph links, rephrase to avoid bare
  symbols/operators.
- **Embedding dims fixed at 768** (nomic). Changing model/dims requires rebuilding the
  `novel_memory` collection.
- **Graph LLM is Gemini**, keyed by `GOOGLE_API_KEY` (mapped from `${GEMINI_API_KEY}` in
  `.mcp.json`). Not the rate-limited path.
- **Stop auto-save hook is intentionally NOT installed** — it hardcodes `infer=true` and
  would 429. Persistence-out is the orchestrator's curated-write job.
- **After changing `.mcp.json` or the hook, restart Claude Code** — MCP servers and hooks
  read their config only at launch.