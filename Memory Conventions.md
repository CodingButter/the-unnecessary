# Memory Conventions (mem0)

How agents use the semantic memory while drafting this novel. Read this before
writing or recalling memories.

## What memory is — and isn't

mem0 is the project's **running ledger of drafting decisions and established
micro-facts** — the things we settle as we write that aren't yet (or never will
be) canon documents. It is searched by *meaning*, not by exact words.

It is **NOT** the source of truth for canon. The authoritative record lives in
the bibles, and they win every conflict:

- `Character Bible.md`, `Story Bible.md` — characters, world, relationships
- `Master Timeline.md`, `Plot Outline and Chapter Map.md` — events, sequence
- `Technology Rules.md` — what's possible, the hard constraints
- `Style Guide.md`, `Narrative Brief.md` — voice and intent
- `Creative Decision Log.md` — the long-form rationale record

> If a memory and a bible disagree, the bible is right. Fix or delete the memory.

## Scope (already configured)

- Qdrant collection: **`novel_memory`** — isolated to this project
- `user_id`: **`novel`**
- Knowledge graph: **on.** Relationships are extracted by **Gemini**
  (`gemini-2.5-flash-lite`) and stored in **Neo4j** (local `:7687`, container
  `mem0-neo4j`). Set `enable_graph=true` on writes whose text relates entities, so the
  links get built. The graph aids recall of how characters, places, and decisions connect.
  It is **not** canon: the bibles remain the higher authority and win every conflict.
  Expect LLM-extracted relationships to drift from bible canon over time, and prune them
  periodically. Recall stays vector-first; treat graph links as hints, then verify against
  the relevant bible.

This namespace is separate from every other mem0 project. Do not write to or read
from any other collection or user_id.

## The golden rule of writing: `infer=false`

**ALWAYS call `add_memory` with `infer=false`.** Never `infer=true`. `infer=true`
invokes the main LLM on the throttled Claude subscription token and fails with **HTTP
429** — this project is zero-cost, with no paid Anthropic key. `infer=false` stores the
text verbatim via local Ollama embeddings: fast, free, reliable. Gemini still builds the
knowledge graph independently of `infer`, so you lose nothing by setting it false.

Gotcha: the vector write commits *before* the graph step. If a graph write errors with
`"Ollama embed() returned no embeddings"` (Gemini emitted an empty entity, likelier for
symbol-dense text), the memory is already stored. **Do not blindly retry** — each retry
duplicates the vector. Rephrase to avoid bare symbols/operators if you want the graph link.

## When to WRITE a memory

Write when we *decide* or *establish* something that a future scene must respect
and that isn't already captured in a bible:

- A drafting decision: "We let Kael's lie about the relay stand uncorrected;
  payoff deferred to the climax."
- An established micro-fact: "The Cathedral bells are cracked — they thud, never
  ring. Established in ch. 9."
- A deviation from the outline, with the reason.
- A continuity hazard we noticed: "Two characters can't both be in the Vault in
  ch. 12 — needs reconciling."
- A voice/word choice ruling not big enough for the Style Guide.

## When NOT to write

- Anything already in a bible — don't duplicate canon; cite the bible instead.
- Transient conversation, todos, or process chatter.
- Speculation we haven't committed to. Memory is for decisions, not maybes.
- Large passages of prose. Store the *decision about* the prose, not the prose.

## How to write a good memory

One atomic fact per memory, self-contained, with its anchor in the story:

> "Established ch. 9: the relay room has no working comms — Kael cut the line
>  himself. This is why no one calls for help in ch. 11."

Bad (vague, non-atomic):
> "Kael did some stuff with the relay and it matters later."

Attach `metadata` so memories can be filtered, e.g.:

```json
{ "type": "decision", "chapter": 9, "characters": ["Kael"], "tags": ["relay", "continuity"] }
```

Suggested `type` values: `decision`, `fact`, `continuity`, `deviation`, `hazard`.

## How to RECALL (do this first)

**Search before you write a scene, and before answering any continuity
question.** The point of memory is to not contradict ourselves.

1. `search_memories` with a meaning-rich query ("what has been established about
   the relay room and comms"), not single keywords.
2. Cross-check anything load-bearing against the relevant bible.
3. Only then draft.

## Maintenance

- When a memory is superseded, `update_memory` it (don't leave a stale fact).
- When a decision graduates to canon, record it in the bible and delete or trim
  the memory so there's one source of truth.
- Keep memories honest: a wrong memory is worse than no memory.

## Operational note

Changes to the mem0 namespace require **restarting Claude Code** — the running
server holds its env at launch.
