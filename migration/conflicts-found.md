# Conflicts Found

This is the single shared ledger for canon conflicts discovered during the migration. It was seeded empty in Phase 00. Later phases APPEND to it; no phase re-creates it.

Rules (from the master spec and Phase 00 overview):

- When two project documents disagree on a fact, preserve both statements exactly. Do not delete, merge, or paraphrase either one.
- Record the conflict here, capturing both sources, their exact conflicting statements, the file paths, and the section or heading each came from.
- Only the orchestrator resolves a conflict. Agents report conflicts; the orchestrator is the only writer of this file.
- A discovered conflict does not block splitting or indexing. It blocks silent resolution only.

Status: no conflicts recorded yet.

| ID | Phase found | Source A (file and section) | Statement A | Source B (file and section) | Statement B | Status | Resolution |
| --- | --- | --- | --- | --- | --- | --- | --- |
