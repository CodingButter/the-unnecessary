<!--
INDEX TEMPLATE, NON-CANON. Owned by Phase 03 (Governance and Indexes).

This is the single reusable per-directory index template. Every later content
phase copies this file into a directory that holds more than three meaningful
files, renames the copy to index.md, and fills in the bracketed placeholders.

It is distinct from the Phase 02 migration scaffolding stubs under
docs/_templates/ (active-document-template.md, context-manifest-template.yaml).
Those document the active-document and manifest shapes; this one documents the
index shape.

CRITICAL CAVEAT: an index summarizes and links to the authority files in its
directory. It is a navigation aid, a pointer, never a replacement canon
document. When a fact and its index summary disagree, the linked authority file
wins (master spec line 521; canon-hierarchy rule). Keep every summary short and
let the linked file carry the detail.

HOW TO USE:
  1. Copy this file into the target directory as index.md.
  2. Replace the commented front-matter shape below with a real front-matter
     block, filling in title, the directory's authority, summary, tags, related,
     and source_documents (real existing paths only). For an index, keep
     document_type "index" and status "active-support".
  3. Fill in all seven elements marked [FILL IN] below. Do not leave a bracketed
     placeholder in a finished index.
  4. Delete this comment block and the commented front-matter shape, then add the
     real front-matter block, before committing the finished index.
-->

<!--
FRONT-MATTER SHAPE FOR A FINISHED INDEX (documentation only; not a live record).

This template is a template, so it does NOT carry a real active front-matter
record of its own. The block below shows the SHAPE every finished index.md must
adopt once it is filled in. Copy it out of the comment, uncomment it, and fill
the placeholders.

The eight required fields are: title, document_type, status, authority, summary,
tags, related, source_documents.

For an index specifically:
  - document_type is always "index".
  - status is always "active-support" (an index is operational supporting
    material, neither story canon nor a plan).
  - authority matches the directory's own domain, not "governance" unless the
    index fronts a governance directory. Example: an index over docs/20-canon/
    characters/ carries authority "character-canon"; an index over
    docs/30-plot/ carries authority "plot-plan". Use the controlled authority
    vocabulary enforced by scripts/validate-metadata.py.

---
title: "<Directory Name> Index"
document_type: "index"
status: "active-support"
authority: "<the authority of this directory's domain, for example character-canon, plot-plan, blueprint, continuity, research, or governance>"
summary: "<one sentence: what this directory holds and what this index helps a reader select>"
tags:
  - index
  - <bare-tag-for-this-domain>
related:
  - "<valid relative path to a sibling or parent index, for example ../index.md>"
source_documents:
  - "<real existing path this index's directory derived from, for example archive/source-monoliths/character-bible.md>"
# Optional fields below: include only when the value is genuinely known. Never invent.
# version: "<semantic version if known, for example 1.0>"
# scope: "<for example book-1>"
# last_reviewed: "<YYYY-MM-DD, only when a real review date is on record>"
---
-->

# [FILL IN: Directory Name] Index

<!--
ELEMENT 1 of 7 -- PURPOSE OF THE DIRECTORY.
One short paragraph. State what this directory holds and why a reader would come
here. Do not restate canon; describe the directory's job.
-->

[FILL IN element 1: one short paragraph stating the purpose of this directory and what kind of files it holds.]

<!--
ELEMENT 2 of 7 -- WHICH FILE TO READ FIRST.
Name the single best entry point for a reader new to this directory. Often the
authority file or an overview. If the directory has no single entry point, say so
and point at this index plus the most load-bearing file.
-->

Read first: [FILL IN element 2: the one file a reader should open before the others, as a link, for example [overview](overview.md).]

<!--
ELEMENTS 3, 4, 5, 6 of 7 -- THE FILES TABLE.
One row per meaningful file in this directory. Fill in the four columns for each:
  - File      = element 3 entry: a relative markdown link to the file.
  - Summary   = element 4: a one or two sentence summary of that file.
  - Authority or status = element 5: the file's authority or status, for example
                "active-canon (character-canon)", "active-plan (plot-plan)",
                "active-support". Use the controlled status and authority
                vocabulary from Phase 02.
  - Load when = element 6: the common tasks that require this file, so an LLM can
                decide whether to load it.
Keep summaries short. The linked file is the authority; this row is only a pointer.
Mark any link whose target a later phase has not created yet as
"(pending: created in a later phase)".
-->

| File | Summary | Authority or status | Load when |
| ---- | ------- | ------------------- | --------- |
| [FILL IN: link to file] | [FILL IN element 4: one or two sentence summary of this file] | [FILL IN element 5: the file's authority or status] | [FILL IN element 6: the common tasks that require this file] |
| [FILL IN: link to next file] | [FILL IN element 4] | [FILL IN element 5] | [FILL IN element 6] |

<!--
ELEMENT 7 of 7 -- LINKS TO RELATED INDEXES.
Point at the parent index, sibling-directory indexes, and any cross-domain index
a reader of this directory will often need next. Mark any index a later phase has
not created yet as "(pending: created in a later phase)".
-->

## Related indexes

- [FILL IN element 7: link to the parent or governance index, for example [governance index](../index.md)]
- [FILL IN element 7: link to a related sibling index, for example a cross-domain index this directory references]

<!--
MODEL: example index table layout from master spec Phase 5 (lines 510 to 519).
Reproduced here as a worked model only. It shows how a real character-canon index
fills the columns. It is NOT canon, NOT a row to keep, and the linked paths below
are illustrative; delete this whole model block before committing a finished
index.

The spec model uses domain-specific columns (Role, Viewpoint) in addition to the
Load when and File columns. A finished index may add such domain columns when they
help a reader select files, as long as the four required signals are present:
the file link (element 3), the per-file summary (element 4), the authority or
status (element 5), and the load-when / common-tasks guidance (element 6).
-->

<!--
# Character Canon Index

Read this index before loading individual character profiles.

| Character   | Role            | Viewpoint | Load when                                            | File                               |
| ----------- | --------------- | --------: | ---------------------------------------------------- | ---------------------------------- |
| Eli Rook    | Protagonist     |       Yes | Any Eli chapter, Morrow creation, Asterion history   | [Profile](profiles/rook-eli.md)    |
| Lena Okafor | Clinic director |       Yes | Medical ethics, clinic scenes, Morrow accountability | [Profile](profiles/okafor-lena.md) |
-->

<!--
REMINDER BEFORE COMMIT: an index helps a reader (human or LLM) select files. It
must not become a replacement canon document. If you find yourself copying a
fact's full detail into this index instead of summarizing and linking, stop and
link to the owning authority file instead. The owning file wins every conflict
against an index summary.
-->
