export const meta = {
  name: 'wire-crew',
  description: 'Wire the newly-hired specialists into the pipeline at their right cadence, then adversarially self-audit the result. Five FILE-DISJOINT wiring jobs in parallel: (1) write-chapter.js gauntlet gains copy-editor + sensitivity-reader, plus a terminal cold-reader pass; (2) revise-chapter.js the same; (3) a NEW section-review.js runs developmental-editor on an assembled act; (4) live-audiobook.js gains a casting-director pre-flight + a prooflistener post-render gate (+ a mastering step); (5) the pronunciation LEXICON is seeded into formatting.md and the audio charters point at it. Then an Audit phase syntax-checks every workflow, runs the validators, and verifies each agent is referenced where it should be. Changes are reversible (git); nothing auto-runs the pipeline.',
  phases: [
    { title: 'Wire', detail: '5 file-disjoint wiring jobs in parallel (write-chapter, revise-chapter, new section-review, live-audiobook, pronunciation lexicon)' },
    { title: 'Audit', detail: 'adversarial self-audit: syntax-check all workflows, run validators, verify every new agent is wired in at the right cadence' },
  ],
}

const NOVEL = '/home/codingbutter/Novel'
async function tryAgent(make, tries) { tries = tries || 3; let last; for (let i = 0; i < tries; i++) { try { const r = await make(); if (r) return r; last = new Error('empty result'); } catch (e) { last = e; log('retry ' + (i + 1) + '/' + tries + ': ' + String(e).slice(0, 140)); } } throw last; }
const REPORT = { type: 'object', properties: { ok: { type: 'boolean' }, summary: { type: 'string' }, details: { type: 'string' } }, required: ['ok', 'summary'] }
const AUDIT = { type: 'object', additionalProperties: false, required: ['pass', 'summary'], properties: {
  pass: { type: 'boolean' },
  checks: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { check: { type: 'string' }, result: { type: 'string' }, ok: { type: 'boolean' } }, required: ['check', 'ok'] } },
  issues: { type: 'array', items: { type: 'string' } },
  summary: { type: 'string' },
} }

const RULES = `\nGENERAL RULES: Read the target file FIRST and match its existing patterns exactly (lens objects, schema names, phase() titles, the tryAgent/parallel helpers, agentType + label + phase opts). Make the SMALLEST change that wires the role in; do not refactor unrelated code. New agents are referenced by agentType (the charters already exist: copy-editor, cold-reader, sensitivity-reader, developmental-editor, prooflistener, casting-director). After editing a .js file, RUN \`node --check <file>\` AND an AsyncFunction-construct check, and confirm it parses before reporting. Avoid em dashes in any drafted prose. Report (REPORT schema): ok, a summary, and details = the exact edits + the node --check result.`

const WP = [
  { key: 'write-chapter', label: 'wire:write-chapter',
    spec: `Wire three editorial roles into ${NOVEL}/.claude/workflows/write-chapter.js (the per-chapter authoring pipeline; phases Prep->Provision->Draft->Gauntlet->Adjudicate->Resolution->Extract->Narration).\n` +
      `1. In the GAUNTLET phase's parallel lens array, ADD two lenses matching the existing lens shape + the FINDINGS schema the others use: (a) copy-editor -- MECHANICS audit (grammar/spelling/punctuation/usage/homophones/hyphenation/capitalization/number+term consistency, and the no-em-dash rule); findings route to the adjudicator like the other lenses. (b) sensitivity-reader -- ADVISORY lived-standpoint triage that SELF-SCOPES (if the chapter depicts no specific identity/lived experience it returns verdict CLEAR with no findings); its findings are ADVISORY, never auto-applied.\n` +
      `2. ADD a TERMINAL cold-reader pass AFTER the Adjudicate (and Resolution) phase, in its own phase (e.g. phase('Cold read')): a single cold-reader agent given ONLY the FINALIZED prose path + any narration script path and NO earlier-stage context (no diagnosis, no revision log) -- it returns an errors-only list (homophones, dropped/doubled/transposed words, mis-keyed names, a self-contradicting micro-detail, errors a prior edit introduced). Route its list to a final adjudicator micro-fix (apply the mechanical corrections) OR, if simpler, append it to a "## Cold-Read Fixes" log and apply via the existing adjudicator pattern. It must NOT receive the gauntlet context (familiarity blindness is the point).\n` +
      `3. UPDATE the adjudicator prompt in this workflow so it (a) applies copy-editor mechanics fixes, and (b) treats sensitivity-reader findings as ADVISORY -- surface them in a "## Sensitivity Flags (advisory, author decides)" section, never silently edit prose for them.\n` +
      `Preserve all 8 existing phases and the reveal-safety / lock / extraction logic.` + RULES },

  { key: 'revise-chapter', label: 'wire:revise-chapter',
    spec: `Wire the same editorial roles into ${NOVEL}/.claude/workflows/revise-chapter.js (phases Diagnose->Adjudicate->Verify).\n` +
      `1. In the DIAGNOSE phase's lenses array, ADD copy-editor (mechanics, FINDINGS schema, routes to adjudicator) and sensitivity-reader (advisory, self-scoping) -- matching the existing lens objects.\n` +
      `2. ADD a TERMINAL cold-reader pass AFTER Adjudicate (before or as part of Verify): a cold-reader given ONLY the revised FINALIZED prose, NO diagnosis/revision-log context, returning an errors-only list; route corrections through the existing adjudicator/verify pattern.\n` +
      `3. UPDATE the adjudicate prompt: apply copy-editor mechanics fixes; treat sensitivity-reader findings as ADVISORY (a "## Sensitivity Flags (advisory)" note, never silent edits).\n` +
      `Preserve the Diagnose/Adjudicate/Verify structure and the CLARITY-first logic.` + RULES },

  { key: 'section-review', label: 'wire:section-review',
    spec: `CREATE a new workflow ${NOVEL}/.claude/workflows/section-review.js that runs the developmental-editor on an ASSEMBLED act/section (its cadence is section/book-level, NOT per-chapter). Model its structure (meta with name+description+phases, the tryAgent helper, REPORT schema, agentType/label/phase opts) on the existing ${NOVEL}/.claude/workflows/revise-chapter.js. args: {book, label, chapters?} where chapters is an optional list of chapter slugs (default: Glob all chapters in the book's manuscript dir).\n` +
      `Phase 'Review': the developmental-editor reads the assembled chapters (and their blueprints if present) and returns a PRIORITIZED DEVELOPMENTAL REVISION LETTER -- arc, pacing (sagging middles / rushed turns), structure + chapter ORDER, character-arc motivation across chapters, theme coherence/drift, setup/payoff balance, what to cut/expand/reorder. It DIAGNOSES only.\n` +
      `Phase 'Record': WRITE the revision letter to ${NOVEL}/docs/30-plot/section-reviews/<book>-<label>.md (create the dir; valid 8-field YAML frontmatter so validators pass) and return a summary. Developmental changes are AUTHOR decisions and too large to auto-apply -- the deliverable is the LETTER plus, optionally, routed flags (fresh-prose items named to chapter-drafter, local structural fixes to the adjudicator). Do NOT auto-edit manuscripts.\n` +
      `node --check + AsyncFunction-construct check the new file before reporting.` + RULES },

  { key: 'live-audiobook', label: 'wire:live-audiobook',
    spec: `Wire two audio roles + a mastering step into ${NOVEL}/.claude/workflows/live-audiobook.js (the per-scene live/dramatized pipeline: a live-narration-director per scene -> stitch). Edit ONLY this workflow file (do not touch the python scripts or any charter).\n` +
      `1. ADD a casting-director PRE-FLIGHT step BEFORE any scene renders: the casting-director reads/confirms the cast sheet (docs/10-vision/audio/cast-sheet.md), ensures every speaking character in the chapter has an assigned, contrast-checked voice, and signs off the ensemble (routing any unassigned/undesigned voice to voice-designer) before scenes go to render. Gate the render on this sign-off.\n` +
      `2. ADD a prooflistener POST-RENDER gate AFTER scenes render (the render already runs verify-narration.py producing qc.json): the prooflistener (Bash) reviews the rendered audio vs the script + the pronunciation lexicon, adds cross-chapter pronunciation-consistency checks, and emits a timestamped re-roll list; route flagged lines back to re-render (the existing render path) before stitch. Keep it advisory-but-acted (re-rolls are near-free).\n` +
      `3. ADD a book/chapter-level MASTERING step AFTER stitch: a sound-engineer pass that measures integrated loudness per stitched file and applies one uniform loudness + true-peak ceiling for a consistent deliverable (the audit's gap 1.3). If it needs a script that does not yet exist, have the step ROUTE the build to systems-engineer by name rather than inventing inline; the wiring should call the step and tolerate a routed (not-yet-built) result.\n` +
      `Match the workflow's existing scene-loop + stitch patterns; preserve the live-narration-director per-scene flow.` + RULES },

  { key: 'pronunciation-lexicon', label: 'wire:lexicon',
    spec: `Establish the single project-wide pronunciation LEXICON (audit gap 1.5) and point the audio agents at it.\n` +
      `1. In ${NOVEL}/docs/10-vision/style/formatting.md, under the Copy-Edit Consistency Ledger's recurring-term-treatment / pronunciation column, SEED the canonical pronunciation of the load-bearing invented proper nouns. GREP the canon (docs/20-canon/**) + the character profiles for the real names and spell out each pronunciation simply (syllable hyphenation + stress), at minimum: Asterion, Aurelia, Mosaic, Morrow, Crown, Kade (Adrian Kade), Eli Rook, Jonah Mercer, Lena Okafor, June Park, Northglass, Aminata Diallo, Amara Okafor -- and any other recurring invented/technical term you find. Keep formatting.md's frontmatter valid; do not duplicate existing rows.\n` +
      `2. Add a short "read the pronunciation lexicon in docs/10-vision/style/formatting.md before rendering / verifying" instruction to THREE audio charters so they all consult one source: ${NOVEL}/.claude/agents/audiobook-director.md, ${NOVEL}/.claude/agents/live-narration-director.md, ${NOVEL}/.claude/agents/prooflistener.md. Surgical additions only; preserve everything else (especially live-narration-director's recent casting carve-out).\n` +
      `3. Run \`python3 scripts/validate-metadata.py\` and \`python3 scripts/validate-links.py\` from ${NOVEL}; both must pass 0 errors.` + RULES },
]

phase('Wire')
log('wire-crew: 5 file-disjoint wiring jobs in parallel')
const wired = await parallel(WP.map(w => () => agent(w.spec, { agentType: 'general-purpose', label: w.label, phase: 'Wire', schema: REPORT })))
const wireOk = WP.filter((w, i) => wired[i] && wired[i].ok).map(w => w.key)
const wireBad = WP.filter((w, i) => !wired[i] || !wired[i].ok).map(w => w.key)
log(`wire: ${wireOk.length}/${WP.length} ok` + (wireBad.length ? ' -- needs-attention: ' + wireBad.join(', ') : ''))

phase('Audit')
log('wire-crew: adversarial self-audit')
const auditThunks = [
  () => agent(
    `ADVERSARIALLY self-audit the JS workflow wiring just applied to "The Unnecessary". Be a skeptic: assume something is broken and find it. From ${NOVEL} run and reason over:\n` +
    `- \`node --check\` on EVERY file in .claude/workflows/*.js (all must parse). Also do an AsyncFunction-construct check on write-chapter.js, revise-chapter.js, section-review.js, live-audiobook.js, wire-crew.js (strip the leading "export " from meta, construct \`new (async function(){}).constructor('args','agent','parallel','pipeline','phase','log','budget','workflow', body)\`) -- each must construct without SyntaxError.\n` +
    `- VERIFY each new agent is actually referenced by agentType where it should be: grep that write-chapter.js references copy-editor + sensitivity-reader + cold-reader; revise-chapter.js references copy-editor + sensitivity-reader + cold-reader; section-review.js references developmental-editor; live-audiobook.js references casting-director + prooflistener (+ a mastering/sound-engineer step). Report any that are MISSING.\n` +
    `- VERIFY the agentType strings exactly match real charter filenames under .claude/agents/ (a typo'd agentType silently falls back to the default agent -- a real bug). List every agentType used in the 4 workflows and confirm each has a matching .claude/agents/<name>.md.\n` +
    `- CHECK the cold-reader is wired as a TERMINAL pass (after adjudicate, denied earlier context) and NOT just dropped into the parallel gauntlet; and that sensitivity-reader output is treated as ADVISORY (not auto-applied). Read the relevant sections to confirm.\n` +
    `Return per AUDIT schema: pass (true only if all checks pass), checks[] (each with result + ok), issues[] (every concrete problem found, with file + what is wrong), summary.`,
    { schema: AUDIT, agentType: 'general-purpose', label: 'audit:workflows', phase: 'Audit' }),
  () => agent(
    `ADVERSARIALLY self-audit the DOCS + charter changes from the crew wiring of "The Unnecessary". From ${NOVEL}:\n` +
    `- Run \`python3 scripts/validate-metadata.py\` and \`python3 scripts/validate-links.py\`; both must be 0 errors. Report any error lines verbatim.\n` +
    `- VERIFY the pronunciation lexicon: docs/10-vision/style/formatting.md must contain seeded pronunciations for the load-bearing names (at least Asterion, Aurelia, Mosaic, Morrow, Kade); and audiobook-director.md, live-narration-director.md, prooflistener.md must each now reference reading that lexicon. Report any missing.\n` +
    `- VERIFY live-narration-director.md still has its casting CARVE-OUT intact (consumes the cast sheet, does not OWN casting) AND now also references the lexicon -- the lexicon edit must not have reverted the carve-out.\n` +
    `- CONFIRM no em dashes were introduced in any changed doc/charter (grep).\n` +
    `Return per AUDIT schema: pass, checks[], issues[], summary.`,
    { schema: AUDIT, agentType: 'general-purpose', label: 'audit:docs', phase: 'Audit' }),
]
const audits = await parallel(auditThunks)
const allPass = audits.every(a => a && a.pass)
const allIssues = audits.filter(Boolean).flatMap(a => a.issues || [])
log(`audit: ${allPass ? 'PASS' : 'ISSUES'} -- ${allIssues.length} issue(s)` + (allIssues.length ? ': ' + allIssues.slice(0, 3).join(' | ') : ''))

return { wired: wireOk, needsAttention: wireBad, wireReports: wired, audit: { pass: allPass, issues: allIssues, reports: audits } }
