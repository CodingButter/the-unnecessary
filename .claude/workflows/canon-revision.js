export const meta = {
  name: 'canon-revision',
  description: 'Apply a described canon change across the right canon files, then run it through the review gauntlet (continuity + logic), adjudicate autonomously (resolve + log per Decision 060, never block on the author), and validate. args: {change, rationale?, label?}.',
  phases: [
    { title: 'Scope', detail: 'canon-scout inventories every file the change touches, the controlling authorities, and the LOCKED facts that must be preserved' },
    { title: 'Apply', detail: 'apply the change as a grounded, minimal, lock-aware edit that keeps the established core intact' },
    { title: 'Gauntlet', detail: 'continuity-auditor + logic-auditor review the change in parallel (contradiction + plausibility)' },
    { title: 'Adjudicate', detail: 'the adjudicator rules on findings, applies accepted fixes, and resolves + logs per Decision 060' },
    { title: 'Validate', detail: 'run the canon validators (links / metadata / locks) on the result' },
  ],
}

let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
A = A || {}
const CHANGE = A.change || ''
const RATIONALE = A.rationale || ''
const LABEL = A.label || 'canon-change'
if (!CHANGE) throw new Error('canon-revision requires args.change (a description of the canon change to apply)')
const NOVEL = '/home/codingbutter/Novel'

// Resilience: a lone agent() THROWS on retry-cap / API error / dropped connection. Wrap lone calls so a
// transient drop retries instead of aborting the revision. parallel() already absorbs per-thunk failures.
async function tryAgent(make, tries) { tries = tries || 3; let last; for (let i = 0; i < tries; i++) { try { const r = await make(); if (r) return r; last = new Error('empty result'); } catch (e) { last = e; log('retry ' + (i + 1) + '/' + tries + ': ' + String(e).slice(0, 140)); } } throw last; }

const REPORT = { type: 'object', properties: { ok: { type: 'boolean' }, summary: { type: 'string' }, details: { type: 'string' } }, required: ['ok', 'summary'] }

const SCOPE_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['files'],
  properties: {
    files: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { path: { type: 'string' }, why: { type: 'string' } }, required: ['path', 'why'] } },
    authorities: { type: 'array', items: { type: 'string' } },        // the canon docs that control this fact type
    locked_facts_to_preserve: { type: 'array', items: { type: 'string' } }, // locked items the edit must NOT change
    foreseen_conflicts: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
}

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

const CHANGEBLOCK = `THE CANON CHANGE TO APPLY:\n"""\n${CHANGE}\n"""\n` + (RATIONALE ? `RATIONALE: ${RATIONALE}\n` : '')

// ---- Scope ----
phase('Scope')
log('canon-revision: ' + LABEL)
const scope = await tryAgent(() => agent(
  `You are the canon-scout. A canon change is being applied to the novel "The Unnecessary"; inventory its blast radius. Read-only — create/edit NOTHING.\n` +
  CHANGEBLOCK +
  `Walk the canon (docs/20-canon/**), the Technology Rules / cloud-dependency, the affected entity files, the Master Timeline (docs/20-canon/timeline/**), and ALL manuscript chapters (docs/50-manuscript/** — BOTH approved-canon AND in-flight DRAFT prose, any status: a draft chapter is not yet canon but is the committed story and a canon change can contradict it) for anything this change touches.\n` +
  `Return: files (every canon file the change should edit, each with a one-line why); authorities (the canon docs that CONTROL this fact type, per docs/00-governance/canon-hierarchy.md); locked_facts_to_preserve (per the §14 lock model — every LOCKED fact in the blast radius the edit must NOT change, e.g. the master-timeline death facts); and foreseen_conflicts (anything in APPROVED prose, in DRAFT manuscript prose, or in a bible the change might contradict — name the file:line, and for a manuscript conflict note the chapter's STATUS, e.g. "Ch2 [draft]"). Source everything; do not guess.`,
  { schema: SCOPE_SCHEMA, phase: 'Scope', agentType: 'canon-scout' }
))
const touch = (scope && scope.files || []).map(f => f.path).filter(Boolean)
log('scope: ' + touch.length + ' file(s); ' + ((scope && scope.locked_facts_to_preserve || []).length) + ' locked fact(s) to preserve; ' + ((scope && scope.foreseen_conflicts || []).length) + ' foreseen conflict(s)')

// ---- Apply ----
phase('Apply')
const apply = await tryAgent(() => agent(
  `Apply a canon change to the novel "The Unnecessary". This is an EXPLICITLY AUTHORIZED canon revision. Edit ONLY the canon files the change requires; change no story prose in approved manuscripts.\n` +
  CHANGEBLOCK +
  `SCOPE (from canon-scout): files = ${JSON.stringify(scope && scope.files || [])}; authorities = ${JSON.stringify(scope && scope.authorities || [])}; LOCKED facts that must be PRESERVED unchanged = ${JSON.stringify(scope && scope.locked_facts_to_preserve || [])}; foreseen conflicts = ${JSON.stringify(scope && scope.foreseen_conflicts || [])}.\n` +
  `RULES: (1) Minimal + grounded — make the smallest edits that fully land the change; invent nothing beyond it. (2) LOCK-AWARE (entity-spec §14): never change a LOCKED fact's value; add new/clarifying facts at the correct lock state (a fact the Technology Rules establish is canon; a deduction stays \`open\`); update the \`locks:\` map for anything you add. (3) Keep the established CORE intact — a clarification, not a rewrite. (4) Must NOT contradict approved manuscript or a bible; if you discover a real contradiction you cannot avoid, do NOT force it — record it for the gauntlet. (5) Avoid em dashes in any drafted canon prose.\n` +
  `Report (REPORT schema): ok, a summary of exactly what you changed per file, and details (the per-file edits + any lock-state you set + anything you deliberately left to the gauntlet).`,
  { schema: REPORT, phase: 'Apply', agentType: 'general-purpose' }
))

// ---- Gauntlet (continuity + logic, in parallel) ----
phase('Gauntlet')
const lenses = [
  { key: 'continuity', agentType: 'continuity-auditor',
    prompt: `Adversarially audit a just-applied CANON CHANGE for CONTRADICTION and FABRICATION against the rest of canon AND every manuscript chapter — both APPROVED and in-flight DRAFT prose. ${CHANGEBLOCK}\nFiles changed: ${JSON.stringify(touch)}. Read the changed files plus everything in their blast radius (the authorities ${JSON.stringify(scope && scope.authorities || [])}, the Master Timeline, and ALL manuscript chapters under docs/50-manuscript/** — approved Ch1 AND any DRAFT chapters: a draft chapter is not yet canon but represents the committed story, so a contradiction with DRAFT prose is a VALID FLAG). Resolve time-varying facts as-of their in-world ISO date (§9); honor reveal gates (§11). Verify by reading, never memory.\nReturn per schema: verdict = PASS | FLAGS; each finding with kind (CONTRADICTION/FABRICATION + external/internal), where = file:line for BOTH the change and the conflicting prose/canon (and for a manuscript conflict note the chapter's STATUS, e.g. "Ch2 [draft]"), problem = the claim + why it conflicts + the controlling authority, fix = recommended resolution. For a DRAFT-prose conflict, note that BECAUSE the prose is unapproved the adjudicator's resolution (Decision 060) may adjust EITHER the draft prose OR the proposed change — established/approved canon wins over both, and between two unapproved options the better mechanism wins.` },
  { key: 'logic', agentType: 'logic-auditor',
    prompt: `Pressure-test a just-applied CANON CHANGE for real-world LOGIC, LOGISTICS, and PLAUSIBILITY and for internal mechanism consistency. ${CHANGEBLOCK}\nFiles changed: ${JSON.stringify(touch)}. Use the Technology Rules + medicine canon as the model of how the world's devices work. Does the revised mechanism ADD UP (no effect-without-cause, no impossible clock/behavior), and does it stay consistent with the established mechanism it clarifies (do not let it quietly break the existing borrowed-uptime / auth-on-restart / can't-forge-correctness logic)?\nReturn per schema: verdict = PASS | FLAGS; each finding with kind = family, where = file:line, problem = the reasoning + the mechanism anchor, fix = direction.` },
]
const gauntletThunks = lenses.map(L => () => agent(L.prompt, { agentType: L.agentType, label: 'cr:gauntlet:' + L.key, phase: 'Gauntlet', schema: FINDINGS }))
let gRuns = await parallel(gauntletThunks)
const gMiss = gRuns.map((r, k) => (r ? -1 : k)).filter(k => k >= 0)
if (gMiss.length) { log('gauntlet retry-sweep: ' + gMiss.length); const re = await parallel(gMiss.map(k => gauntletThunks[k])); gMiss.forEach((k, j) => { if (re[j]) gRuns[k] = re[j] }) }
const gauntlet = {}
lenses.forEach((L, i) => { gauntlet[L.key] = gRuns[i] || { verdict: '(lens failed)', findings: [], summary: 'no result' } })
const totalFindings = lenses.reduce((s, L) => s + ((gauntlet[L.key].findings || []).length), 0)
log('gauntlet: ' + totalFindings + ' finding(s) across continuity + logic')

// ---- Adjudicate (autonomous, Decision 060) ----
phase('Adjudicate')
const adj = await tryAgent(() => agent(
  `You are the adjudicator. A CANON CHANGE was applied to the novel "The Unnecessary" and reviewed by the gauntlet. Rule on every finding and FIX the canon files; operate under the AUTONOMOUS-RESOLUTION policy (Decision 060): you do NOT hand questions to the author — you resolve them by the canon authority hierarchy (docs/00-governance/canon-hierarchy.md), apply the most defensible reading, and PROCEED.\n` +
  CHANGEBLOCK +
  `Gauntlet findings (continuity + logic), as JSON:\n${JSON.stringify(gauntlet)}\n` +
  `For EVERY finding: ACCEPT or REJECT with a one-line grounded reason, and APPLY accepted fixes as surgical edits to the changed canon files. A REJECT must cite the authority that overrides the finding. If a finding reveals the change genuinely breaks approved prose or a bible, REPAIR the change so it stops conflicting (the established canon wins; the new clarification yields). Preserve all LOCKED facts. Keep the established core intact.\n` +
  `Append (or create) a "## Decisions Made (author may override)" section in the most relevant changed canon file (or the Technology Rules doc) recording each non-trivial call: the question, the decision, the grounding authority (path:line), confidence, and a one-line override path. NEVER block; reserve a bare author-note only for a pure creative preference with no grounded answer, and even then pick a default.\n` +
  `Report (REPORT schema): number accepted / rejected, what you repaired, any residual risk, and confirm no locked fact changed and no approved prose was contradicted.`,
  { schema: REPORT, phase: 'Adjudicate', agentType: 'adjudicator' }
))

// ---- Validate ----
phase('Validate')
const val = await tryAgent(() => agent(
  `Run the canon validators for "The Unnecessary" from ${NOVEL} and report results. Run EXACTLY:\n` +
  `  python3 scripts/validate-links.py\n  python3 scripts/validate-metadata.py\n  python3 scripts/validate-locks.py --root docs/20-canon\n` +
  `Report (REPORT schema): ok = true only if all three pass with 0 ERRORs; summary = one line per validator (PASS/FAIL + error count); details = any ERROR lines verbatim. Do not edit anything.`,
  { schema: REPORT, phase: 'Validate', label: 'cr:validate', agentType: 'general-purpose' }
))

return { change: LABEL, scope, apply, gauntlet, adjudicate: adj, validate: val, files: touch }
