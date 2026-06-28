---
name: interpretation-audit
description: progressive two-pass clarity audit of a chapter -- two lay-readers (8th-grade, average-adult) re-tell it paragraph by paragraph seeing only what came before (no future context), then reread with the full chapter; a clarity-auditor flags only confusion that never resolves and spares deliberate seeds
---

# Interpretation Audit

A comprehension test for a drafted chapter that reproduces how a real reader actually
experiences it: **sequentially, with no knowledge they have not earned yet.**

Two lay-readers (an 8th-grade reader, the legibility bar, and an average-adult reader,
the target) read the chapter **paragraph by paragraph**, each paragraph seen with only a
sliding window of the *preceding* paragraphs and **nothing that comes after** — fed as
text so they cannot look ahead. Each reports, in their own words, what they understood and
whether the paragraph tripped them on that first pass. Then each **rereads with the whole
chapter** and reports which of their first-pass confusions *resolved*. Finally a
clarity-auditor classifies every first-pass confusion:

- **Real clarity bug** — confusing on first read AND still unresolved with full context.
- **Working seed** — confusing on first read but *resolved later* (foreshadowing, a setup
  that pays off, a deliberately-withheld fact from the blueprint). **Spared, not flagged.**

That bug-vs-seed split is the point: it lets the chapter keep its intended mysteries (a
reader not yet knowing what a "zone" is, is a hook, not a defect) while catching the
confusion that never lands.

Use this after a chapter is drafted, to learn whether the page lands the way the blueprint
intended — not whether the prose is *good*, but whether it is *understood* on a first read.

## How to run

Invoke the workflow `.claude/workflows/interpretation-audit.js`, passing the target chapter
through `args`:

- `chapter` — absolute path to the chapter manuscript `.md` to audit.
- `blueprint` — absolute path to that chapter's blueprint (its intended takeaways and
  deliberately-withheld set).
- `window` — optional; how many recent paragraphs each reader holds on the first pass
  (default 10). This is the dominant cost lever: lower it to spend fewer tokens, raise it
  for a chapter with long-range callbacks.

If `args` are omitted, the workflow defaults to Chapter 1.

Example args:

```json
{
  "chapter": "/home/codingbutter/Novel/docs/50-manuscript/book-1/chapter-02-<slug>/chapter-02-<slug>.md",
  "blueprint": "/home/codingbutter/Novel/docs/40-blueprints/book-1/chapter-02-<slug>/blueprint.md",
  "window": 10
}
```

## Phases

1. **Split** — extract the chapter's story prose as an ordered list of paragraphs.
2. **FirstRead** — each of the two crew lay-readers interprets every paragraph seeing only
   the recent prior paragraphs (no future text), marking first-pass confusion.
3. **Reread** — each lay-reader rereads with the full chapter and reports which first-pass
   confusions resolved.
4. **Compare** — the crew clarity-auditor flags only confusion that never resolves (real
   bugs) and lists the confusion that resolved as intended working seeds.

The workflow returns `bugs` (the real ones to fix) and `working_seeds` (intended, spared),
each located by paragraph number and opening words.

## Cost note

Progressive reveal is inherently heavier than a single whole-chapter read, because each
paragraph is its own read. Two readers (not three) and the sliding `window` keep it bounded
— roughly a fifth of a naive full-prefix, three-reader run — so a per-chapter audit does
not blow the token budget.
