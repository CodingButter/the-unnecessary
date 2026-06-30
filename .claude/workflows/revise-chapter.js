export const meta = {
  name: 'revise-chapter',
  description: 'Revise an EXISTING chapter through a diagnose -> fix -> verify loop: run the review gauntlet on the current prose (optionally compose interpretation-audit for empirical reader-clarity), the adjudicator applies accepted fixes autonomously (Decision 060 + the clarity-first rule Decision 061: fix accidental obscurity, spare deliberate seeds; never block), then re-check the revised prose to confirm the flags resolved with no new breakage. General-purpose (clarity, continuity, logic, line-edits). args: {book, number, slug, title?, notes?, empiricalClarity?, window?}.',
  phases: [
    { title: 'Diagnose', detail: 'review gauntlet on the existing prose (+ optional interpretation-audit for empirical clarity), seeded with the author/reader notes' },
    { title: 'Adjudicate', detail: 'adjudicator applies accepted fixes per Decision 060/061; fixes accidental obscurity, spares seeds; logs overridable decisions' },
    { title: 'Verify', detail: 'terminal cold-read of the finalized prose (errors-only, no upstream context) routed back through the adjudicator, then re-run the key lenses on the revised prose: flags resolved? no new em-dash / reveal-leak / viewpoint break?' },
  ],
}

let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
A = A || {}
const BOOK = A.book || 'book-1'
if (A.number === undefined || A.number === null || !A.slug) throw new Error('revise-chapter requires args {number, slug} (+ optional title, notes, empiricalClarity, window)')
const num = String(A.number).padStart(2, '0')
const slug = A.slug
const title = A.title || ('Chapter ' + A.number)
const NOTES = A.notes || ''                       // author/reader feedback or pasted prior-audit findings to focus the pass
const EMPIRICAL = !!A.empiricalClarity            // compose a fresh interpretation-audit for lay-reader clarity data
const WINDOW = Number(A.window) > 0 ? Number(A.window) : 10
const NOVEL = '/home/codingbutter/Novel'
const manuscript = `docs/50-manuscript/${BOOK}/chapter-${num}-${slug}/chapter-${num}-${slug}.md`
const blueprint = `docs/40-blueprints/${BOOK}/chapter-${num}-${slug}/blueprint.md`

async function tryAgent(make, tries) { tries = tries || 3; let last; for (let i = 0; i < tries; i++) { try { const r = await make(); if (r) return r; last = new Error('empty result'); } catch (e) { last = e; log('retry ' + (i + 1) + '/' + tries + ': ' + String(e).slice(0, 140)); } } throw last; }

const REPORT = { type: 'object', properties: { ok: { type: 'boolean' }, summary: { type: 'string' }, details: { type: 'string' } }, required: ['ok', 'summary'] }
const FINDINGS = {
  type: 'object', additionalProperties: false, required: ['verdict', 'findings'],
  properties: {
    verdict: { type: 'string' },
    findings: { type: 'array', items: { type: 'object', additionalProperties: false, properties: {
      severity: { type: 'string' }, kind: { type: 'string' }, where: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' }, out_of_scope: { type: 'boolean' },
    }, required: ['severity', 'kind', 'where', 'problem'] } },
    summary: { type: 'string' },
  },
}

const CLARITY = `CLARITY-FIRST STANDARD (Decision 061, docs/10-vision/style/core-prose.md "Clarity Is the Default"): clarity is the default; prose must be legible on first pass / first listen. Ambiguity is justified ONLY as a deliberate device -- genuine foreshadowing that pays off later, or a new concept clearly explained soon. ACCIDENTAL obscurity (unclear agent, untrackable referent, a misreadable poetic inversion, a no-payoff puzzle) is a BUG to fix; the discriminator is PAYOFF, not plainness, so clear-and-poetic prose is protected. The bar is higher at openings and in audio.`
const NOTEBLOCK = NOTES ? `AUTHOR / READER NOTES to focus this revision (treat as priority signal, verify against the prose):\n"""\n${NOTES}\n"""\n` : ''

// ---- Diagnose ----
phase('Diagnose')
log(`revise-chapter: ch${num} "${title}"` + (EMPIRICAL ? ' (+ empirical interpretation-audit)' : ''))
let empirical = null
if (EMPIRICAL) {
  try { empirical = await workflow('interpretation-audit', { chapter: `${NOVEL}/${manuscript}`, blueprint: `${NOVEL}/${blueprint}`, window: WINDOW }) ; log('interpretation-audit composed: empirical clarity data gathered') }
  catch (e) { log('interpretation-audit compose failed (' + String(e).slice(0, 120) + '); proceeding with the gauntlet only') }
}
const empiricalBlock = empirical ? `EMPIRICAL READER-CLARITY DATA (from interpretation-audit -- never-resolving confusions are real bugs, resolving ones are kept seeds):\n${JSON.stringify(empirical).slice(0, 6000)}\n` : ''

const lenses = [
  { key: 'clarity', agentType: 'clarity-auditor',
    prompt: `${CLARITY}\nReview the EXISTING chapter prose for first-pass / first-listen legibility under that standard. Manuscript (STORY PROSE only -- ignore frontmatter and any "Adjudication Log"/"Decisions Made"/revision log): ${NOVEL}/${manuscript}. Blueprint (the intended takeaway + the sacred "Information Deliberately Withheld"): ${NOVEL}/${blueprint}.\n${NOTEBLOCK}${empiricalBlock}Flag ACCIDENTAL obscurity (unclear agent/referent, misreadable inversion, no-payoff puzzle) as a real bug; SPARE deliberate seeds (a confusion that resolves later) and concepts explained soon. Return per schema: verdict CLEAR|AMBIGUOUS; each finding with kind, severity, where = paragraph/quote anchor, problem = the friction + the meaning at risk, fix = direction.` },
  { key: 'prose', agentType: 'prose-critic',
    prompt: `Adversarial CRAFT pass on the EXISTING chapter prose (voice, rhythm, cliche, show-don't-tell, dialogue, sensory grounding), judged against the Style Guide (docs/10-vision/style/**), including the new "Clarity Is the Default" section. Manuscript: ${NOVEL}/${manuscript}. Blueprint: ${NOVEL}/${blueprint}.\n${NOTEBLOCK}Return per schema: verdict; each finding with severity, kind, where = exact quote + anchor, problem, fix = direction only. out_of_scope:true on a routed continuity/canon pointer.` },
  { key: 'continuity', agentType: 'continuity-auditor',
    prompt: `Audit the EXISTING chapter for CONTRADICTION / FABRICATION vs canon + the chapter's own internal state, so any clarity edits we make do not break continuity. Manuscript: ${NOVEL}/${manuscript}. Blueprint: ${NOVEL}/${blueprint}. Resolve time-varying facts as-of the scene's ISO date (§9); honor reveal gates (§11).\n${NOTEBLOCK}Return per schema: verdict PASS|FLAGS; each finding with kind, where = file:line for both beats, problem + controlling authority, fix.` },
  { key: 'echo', agentType: 'echo-auditor',
    prompt: `Cross-chapter FRESHNESS pass on the EXISTING chapter vs the approved/prior chapters that precede it (Glob the manuscript tree). Manuscript: ${NOVEL}/${manuscript}. If chapter 1 (no predecessors), verdict "fresh".\n${NOTEBLOCK}Return per schema: verdict fresh|echoes-flagged; each finding with kind (mode A|B + MOTIF|SELF-ECHO|QUESTION), severity, where = both source + instance, problem, fix = cut|vary|assume-and-reference.` },
  { key: 'copyedit', agentType: 'copy-editor',
    prompt: `MECHANICS-only audit of the EXISTING chapter prose (grammar, spelling/homophones, punctuation, missing/doubled/transposed words, em dashes [forbidden], and consistency-of-treatment drift -- hyphenation, capitalization, number style, recurring-term treatment), flagged against the house style sheet (${NOVEL}/docs/10-vision/style/formatting.md) and Style Guide -- NOT craft, NOT canon facts. Manuscript (STORY PROSE only -- ignore frontmatter and any "Revision Log"/"Sensitivity Flags"/"Adjudication Log"/"Decisions Made"): ${NOVEL}/${manuscript}. Blueprint: ${NOVEL}/${blueprint}.\n${NOTEBLOCK}Diagnose only; route every fix to the adjudicator (do not edit the manuscript). You may extend the style sheet's Consistency Ledger for a new house decision. Return per schema: verdict CLEAN|FLAGGED; each finding with kind (grammar|spelling/homophone|punctuation|missing/doubled word|em-dash|treatment-drift), severity, where = path:line + exact quote, problem = the rule it breaks, fix = corrected form. out_of_scope:true on a routed craft/continuity/clarity pointer.` },
  { key: 'sensitivity', agentType: 'sensitivity-reader',
    prompt: `ADVISORY lived-standpoint triage of the EXISTING chapter: surface portrayals that might MISREPRESENT (AUTHENTICITY) or might OFFEND / do HARM (SENSITIVITY: stereotypes, harmful tropes, unintentional bias). Manuscript (STORY PROSE only): ${NOVEL}/${manuscript}. Blueprint (what the depiction is for): ${NOVEL}/${blueprint}.\n${NOTEBLOCK}You are ADVISORY and TRIAGE ONLY -- never sign off, never block, never edit; route load-bearing cases to a HUMAN reader from the depicted community. SELF-SCOPE: if the chapter depicts no specific identity / lived experience with enough specificity to misrepresent or harm, return verdict NONE with empty findings -- do not manufacture findings. Otherwise return per schema: verdict NONE|FLAGS; each finding with kind = AUTHENTICITY|SENSITIVITY (the lens), severity = low (triage note)|load-bearing (route to human), where = quoted passage + anchor, problem = the approximate concern + confidence, fix = an advisory note OR "route to a human reader" -- never a required edit.` },
]
const gThunks = lenses.map(L => () => agent(L.prompt, { agentType: L.agentType, label: 'rev:diag:' + L.key, phase: 'Diagnose', schema: FINDINGS }))
let gRuns = await parallel(gThunks)
const gMiss = gRuns.map((r, k) => (r ? -1 : k)).filter(k => k >= 0)
if (gMiss.length) { log('diagnose retry-sweep: ' + gMiss.length); const re = await parallel(gMiss.map(k => gThunks[k])); gMiss.forEach((k, j) => { if (re[j]) gRuns[k] = re[j] }) }
const diagnosis = {}
lenses.forEach((L, i) => { diagnosis[L.key] = gRuns[i] || { verdict: '(lens failed)', findings: [], summary: 'no result' } })
const totalFindings = lenses.reduce((s, L) => s + ((diagnosis[L.key].findings || []).length), 0)
log(`diagnose: ${totalFindings} finding(s) across ${lenses.length} lenses` + (empirical ? ' + empirical audit' : ''))

// ---- Adjudicate (autonomous, Decision 060 + 061) ----
phase('Adjudicate')
const adj = await tryAgent(() => agent(
  `You are the adjudicator. An EXISTING chapter of "The Unnecessary" was reviewed for revision; rule on every finding and APPLY accepted fixes to the prose. Operate under the AUTONOMOUS-RESOLUTION policy (Decision 060): resolve by the authority hierarchy, never hand a question to the author; and the CLARITY-FIRST rule (Decision 061).\n` +
  CLARITY + `\n` +
  `Manuscript (edit the STORY PROSE only; never touch a derived narration script): ${NOVEL}/${manuscript}. Blueprint (the sacred withheld reveals + intended focus): ${NOVEL}/${blueprint}.\n` +
  NOTEBLOCK +
  `Gauntlet findings as JSON:\n${JSON.stringify(diagnosis)}\n` + (empirical ? `Empirical reader-clarity (interpretation-audit):\n${JSON.stringify(empirical).slice(0, 4000)}\n` : '') +
  `For EVERY finding: ACCEPT or REJECT with a one-line grounded reason; APPLY accepted fixes as surgical edits. FIX accidental obscurity; SPARE (reject edits to) deliberate seeds / foreshadowing / concepts explained soon -- the discriminator is payoff, not plainness, so do not flatten clear-and-poetic lines. APPLY accepted copy-editor MECHANICS fixes (grammar, spelling/homophone, punctuation, em-dash removal, missing/doubled/transposed words, treatment drift) as surgical edits. Treat every sensitivity-reader finding as ADVISORY ONLY: never apply it as a silent edit and never block on it -- record them verbatim (see the Sensitivity Flags note below). A fix that needs FRESH scene prose (not a local repair): ACCEPT and ROUTE to chapter-drafter by name; do not draft it yourself. Preserve viewpoint, reveal gates, and the restrained voice.\n` +
  `Append a "## Revision Log (author may override)" section at the END of the manuscript: one row per finding -> ACCEPT/REJECT + one-line reason, and for any non-trivial call the grounding + an override path. Keep status as-is (the author re-approves separately).\n` +
  `If any sensitivity-reader findings exist, append a separate "## Sensitivity Flags (advisory)" section at the END of the manuscript: one entry per finding -> lens (AUTHENTICITY/SENSITIVITY), the quoted passage, the approximate concern, and its disposition (an advisory note, or "route to a HUMAN reader from the depicted community" for load-bearing cases). These are flags for the author, NEVER silent edits and never a block.\n` +
  `Before finishing: grep to confirm ZERO em dashes, viewpoint + the POV character's knowledge intact, and no forbidden reveal introduced by any edit. Report (REPORT schema): accepted / rejected counts, items routed to chapter-drafter, and the confirmations.`,
  { schema: REPORT, phase: 'Adjudicate', agentType: 'adjudicator' }
))

// ---- Verify ----
phase('Verify')
// Terminal cold read: a fresh-eyes, errors-ONLY proofread of the now-FINALIZED prose, denied all diagnosis / revision-log context.
const cold = await tryAgent(() => agent(
  `You are the cold-reader: the crew's terminal, fresh-eyes, errors-ONLY proofread. Read the now-FINALIZED chapter prose as a stranger and surface ONLY mechanical errors -- homophone / wrong-word swaps, dropped / doubled / transposed words, misspellings or a mis-keyed character / place name, surface self-contradictions, and errors a prior edit INTRODUCED (an orphaned clause, a broken punctuation pair). Manuscript STORY PROSE ONLY: ${NOVEL}/${manuscript}.\n` +
  `Stay COLD: read NOTHING upstream -- ignore and do NOT read the appended "## Revision Log" / "## Sensitivity Flags" sections, the blueprint, any diagnosis history, or any *.gemini-critique.md / *.opus-read.md companions. Earlier-stage context would destroy the cold read; if handed any, decline it and say so.\n` +
  `Diagnose only; edit nothing. Return per schema: verdict CLEAN|ERRORS FOUND; each finding with kind (HOMOPHONE|DROPPED-WORD|DOUBLED-WORD|TRANSPOSITION|MISSPELLING/NAME|SELF-CONTRADICTION|INTRODUCED-BY-EDIT), severity, where = paragraph / line anchor + exact quote, problem, fix = the unambiguous mechanical correction where one exists else FLAG ONLY. Mark CANDIDATE in kind where confirming needs canon (a name) or a continuity call.`,
  { schema: FINDINGS, phase: 'Verify', agentType: 'cold-reader' }
))
const coldFindings = (cold && cold.findings) || []
log(`cold-read: ${coldFindings.length} mechanical error(s)` + (coldFindings.length ? '' : ' -- clean'))
let coldAdj = null
if (coldFindings.length) {
  coldAdj = await tryAgent(() => agent(
    `You are the adjudicator. A terminal cold-read of the FINALIZED chapter surfaced mechanical errors; rule on each and APPLY accepted fixes to the STORY PROSE (Decision 060, autonomous; never block, never hand it to the author). Manuscript (edit STORY PROSE only; never a derived narration script): ${NOVEL}/${manuscript}.\n` +
    `Cold-read findings as JSON:\n${JSON.stringify(cold)}\n` +
    `For each: ACCEPT and apply the surgical mechanical fix, or REJECT with a one-line grounded reason (a deliberate adaptation, a gated detail, a false positive); a CANDIDATE that needs canon -> confirm against the bible before applying, else REJECT. Append the dispositions to the existing "## Revision Log (author may override)" under a "Cold-read" subhead. Before finishing: grep to confirm ZERO em dashes and that no edit broke viewpoint or a reveal gate. Report (REPORT schema): accepted / rejected counts and the confirmations.`,
    { schema: REPORT, phase: 'Verify', agentType: 'adjudicator' }
  ))
}
const VLENS = [
  { key: 'clarity', agentType: 'clarity-auditor', prompt: `${CLARITY}\nRE-CHECK the now-REVISED chapter prose: did the previously-flagged accidental obscurity RESOLVE, and did the edits introduce any NEW first-pass confusion? Manuscript: ${NOVEL}/${manuscript}. Blueprint: ${NOVEL}/${blueprint}. Prior diagnosis: ${JSON.stringify(diagnosis.clarity || {}).slice(0, 2500)}.\nReturn per schema: verdict CLEAR|AMBIGUOUS; findings only for anything STILL unclear or newly introduced.` },
  { key: 'continuity', agentType: 'continuity-auditor', prompt: `RE-CHECK the now-REVISED chapter for any CONTRADICTION/FABRICATION introduced by the revision edits. Manuscript: ${NOVEL}/${manuscript}. Blueprint: ${NOVEL}/${blueprint}.\nReturn per schema: verdict PASS|FLAGS; findings only for newly-introduced problems.` },
]
let vRuns = await parallel(VLENS.map(L => () => agent(L.prompt, { agentType: L.agentType, label: 'rev:verify:' + L.key, phase: 'Verify', schema: FINDINGS })))
const verify = {}
VLENS.forEach((L, i) => { verify[L.key] = vRuns[i] || { verdict: '(verify lens failed)', findings: [], summary: 'no result' } })
const residual = VLENS.reduce((s, L) => s + ((verify[L.key].findings || []).length), 0)
log(`verify: ${residual} residual/new finding(s) after the revision` + (residual ? ' -- review the Revision Log' : ' -- clean'))

return { chapter: { number: A.number, slug, title }, manuscript, empirical: !!empirical, diagnosis, adjudicate: adj, coldRead: cold, coldReadAdjudicate: coldAdj, verify, residual }
