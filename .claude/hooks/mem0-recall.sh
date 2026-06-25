#!/usr/bin/env bash
# mem0 SessionStart recall hook — Novel project.
#
# Auto-injects relevant cross-session memories into each new Claude Code session
# as additionalContext. This is the persistence-IN half of mem0 (recall);
# the persistence-OUT half (writes) is done deliberately with infer=false
# during the session — see CLAUDE.md "mem0 operating protocol".
#
# Why a wrapper instead of the bare `mem0-hook-context` the installer writes:
#   1. The entry point lives inside the uvx-managed env, not on PATH.
#   2. The hook process does NOT inherit the MEM0_* config from .mcp.json,
#      so we must re-export it here. The recall-relevant values below MUST mirror
#      .mcp.json or the hook queries the wrong Qdrant collection / wrong embedding
#      dims. The graph vars (MEM0_NEO4J_*, MEM0_GRAPH_LLM_*, GOOGLE_API_KEY) are
#      intentionally omitted: recall never touches the graph.
#
# Recall is search-only. The project-wide knowledge graph is ON (see CLAUDE.md and
# .mcp.json), but it is NOT queried on this read path: the context hook disables the
# graph internally and embeds the query via local Ollama. No Anthropic or Gemini call
# is made on recall, so it never hits a rate limit. Safe to run on every session start.

export MEM0_PROVIDER=anthropic
export MEM0_EMBED_PROVIDER=ollama
export MEM0_EMBED_MODEL=nomic-embed-text
export MEM0_EMBED_DIMS=768
export MEM0_OLLAMA_URL=http://localhost:11434
export MEM0_QDRANT_URL=http://localhost:6333
export MEM0_COLLECTION=novel_memory
export MEM0_USER_ID=novel

# If uvx is unavailable, emit the non-fatal hook response so session start
# is never blocked.
command -v uvx >/dev/null 2>&1 || { echo '{"continue":true,"suppressOutput":true}'; exit 0; }

exec uvx \
  --from "git+https://github.com/elvismdev/mem0-mcp-selfhosted.git@a4f538afc60ca13a9f5975e6a11fd36e578393ac" \
  --with "mem0ai[graph,llms]<2" \
  mem0-hook-context
