<!--
PLACEHOLDER TEMPLATE, NON-CANON. Phase 02 migration scaffolding.
This file documents the active-document YAML front-matter SHAPE only.
It contains zero canonical story content. Copy it, fill the placeholders,
and replace this comment when authoring a real active document in a later phase.
Controlled values for `status` and `authority` are defined in
the schema enforced by scripts/validate-metadata.py. Filenames use lowercase kebab-case.
-->
---
title: "<Human readable title>"
document_type: "<one value from the document_type enum, for example character-profile>"
status: "<one value from the status enum, for example active-canon>"
authority: "<one value from the authority enum, for example character-canon>"
summary: "<one sentence describing what this document is the authority for>"
tags:
  - <bare-tag>
  - <bare-tag>
related:
  - "<valid relative path to a related file, for example ../relationship-map.md>"
source_documents:
  - "<path into the archived monolith this was split from, for example archive/source-monoliths/character-bible.md>"
# Optional fields below: include only when the value is genuinely known. Never invent.
# version: "<semantic version if known, for example 1.0>"
# scope: "<for example book-1>"
# last_reviewed: "<YYYY-MM-DD, only when a real review date is on record>"
---

<!-- Document body begins here. The front matter above is required on every active document. -->
