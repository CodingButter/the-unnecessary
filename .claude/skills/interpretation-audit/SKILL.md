---
name: interpretation-audit
description: run the clarity/interpretation audit on a chapter -- three lay-readers at different reading levels re-tell it, a clarity-auditor flags paragraphs where understanding diverges from the blueprint's intent
---

# Interpretation Audit

A comprehension test for a drafted chapter. Three lay-readers at different reading
levels (8th-grade, average adult, close reader) independently re-tell the chapter
paragraph by paragraph in their own words; a clarity-auditor aligns those retellings
against the actual prose and the blueprint's intended takeaways, flagging every
paragraph where reader understanding diverges or gets lost (real ambiguity), and
distinguishing that from mere depth-variation between reading levels.

Use this after a chapter is drafted, when you want to know whether the page lands the
way the blueprint intended — not whether the prose is good, but whether it is
*understood*.

## How to run

Invoke the workflow `.claude/workflows/interpretation-audit.js`, passing the target
chapter through `args`:

- `chapter` — absolute path to the chapter manuscript `.md` to audit.
- `blueprint` — absolute path to that chapter's blueprint (its intended takeaways).

If `args` are omitted, the workflow defaults to Chapter 1
(`docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md`) and its
blueprint.

Example args:

```json
{
  "chapter": "/home/codingbutter/Novel/docs/50-manuscript/book-1/chapter-02-<slug>/chapter-02-<slug>.md",
  "blueprint": "/home/codingbutter/Novel/docs/40-blueprints/book-1/chapter-02-<slug>/blueprint.md"
}
```

## Phases

1. **Read** — three lay-readers (8th-grade, average adult, close reader) re-tell the
   chapter in their own words, paragraph by paragraph. Each runs as a crew lay-reader.
2. **Compare** — the crew clarity-auditor aligns the retellings against the prose and
   the blueprint's intent, flagging paragraphs where understanding diverges.

The workflow returns the flagged paragraphs (located by their opening words) with the
specific divergence between what readers understood and what the blueprint intended.
