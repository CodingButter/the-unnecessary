export const meta = {
  name: 'logic-audit',
  description: "Logic/logistics/plausibility audit of a chapter: a recap-generator first produces a 'previously on' recap of the prior chapter(s) keyed to this chapter, then the logic-auditor pressure-tests the chapter (with that recap + canon as plausibility anchors) for things that don't add up -- impossible clocks/travel/counts, devices defying their own mechanism, effects without causes -- even when no canon fact is broken. Target via args {chapter, blueprint, prior}.",
  phases: [
    { title: 'Recap', detail: "recap-generator: prior-chapter 'previously on', keyed to this chapter" },
    { title: 'Audit', detail: 'logic-auditor pressure-tests the chapter with the recap + canon anchors' },
  ],
}

const ROOT = '/home/codingbutter/Novel'
const a = (typeof args !== 'undefined' && args) || {}
const CH = a.chapter || `${ROOT}/docs/50-manuscript/book-1/chapter-02-the-last-supported-day/chapter-02-the-last-supported-day.md`
const BP = a.blueprint || `${ROOT}/docs/40-blueprints/book-1/chapter-02-the-last-supported-day/blueprint.md`
const PRIOR = a.prior || `${ROOT}/docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md`

// Resilience: a single agent() call THROWS on retry-cap / API error / dropped connection, which would
// abort the whole audit. Wrap the lone (non-parallel) calls so a transient drop retries instead of losing
// the run. parallel() already absorbs failures (returns null per thunk), so it does not need this.
async function tryAgent(make, tries) { tries = tries || 3; let last; for (let i = 0; i < tries; i++) { try { const r = await make(); if (r) return r; last = new Error('empty result'); } catch (e) { last = e; log('retry ' + (i + 1) + '/' + tries + ': ' + String(e).slice(0, 140)); } } throw last; }

phase('Recap')
const recap = await tryAgent(() => agent(
  `Produce a "PREVIOUSLY ON" recap for the chapter at ${CH}. Read the prior chapter(s) at ${PRIOR} and the current chapter's blueprint at ${BP}. Write a tight, SELECTIVE recap of ONLY the prior-chapter beats, facts, character states, and setups that THIS chapter draws on or pays off (per its blueprint) -- especially established care patterns, schedules, who-knows-what, and physical/medical facts a reader would carry in. Skip everything the current chapter does not lean on. Return the recap as plain text.`,
  { agentType: 'recap-generator', label: 'recap', phase: 'Recap' }
))

phase('Audit')
const FINDINGS = { type: 'object', required: ['findings'], properties: {
  findings: { type: 'array', items: { type: 'object', properties: {
    where: { type: 'string', description: 'paragraph opening or file:line' },
    problem: { type: 'string', description: 'what does not add up, in real-world terms' },
    kind: { type: 'string', description: 'time-of-day / spatial / count / mechanism / cause-effect / sequence' },
    severity: { type: 'string' },
  } } },
  summary: { type: 'string' },
} }
const audit = await tryAgent(() => agent(
  `Pressure-test the chapter at ${CH} for real-world LOGIC, LOGISTICS, and PLAUSIBILITY errors -- things that do not ADD UP even if they break no canon fact.\n\n` +
  `Carry this PRIOR-CHAPTER RECAP as the memory a real reader of this chapter would have (use it to judge whether events are plausible given what was already established):\n\n=== PREVIOUSLY ON ===\n${recap}\n=== END RECAP ===\n\n` +
  `Also use the canon as plausibility anchors where relevant: the Technology Rules under ${ROOT}/docs/20-canon/technology/**, ${ROOT}/docs/20-canon/technology/infrastructure/ (incl. medicine.md if present), and the Master Timeline. Flag every place where the timing/time-of-day vs activity, the physical/spatial logistics, the counts, a device behaving against its own mechanism, or a cause-and-effect does not hold up. For each: where (paragraph opening / file:line), what does not add up, its kind, and a severity. Be concrete and skeptical. Return per schema.`,
  { agentType: 'logic-auditor', schema: FINDINGS, label: 'audit', phase: 'Audit' }
))

return { recap, audit }
