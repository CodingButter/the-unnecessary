export const meta = {
  name: 'interpretation-audit',
  description: "Progressive two-pass clarity audit of a chapter. Two lay-readers (8th-grade and average-adult) read it paragraph by paragraph with only a sliding window of recent prior paragraphs visible (no future context, fed as text so they cannot look ahead), reporting first-read understanding and first-pass confusion; then each rereads with the full chapter and reports which confusions RESOLVED (intended seed/foreshadowing) vs which remain (real clarity bug); a clarity-auditor flags only confusions that never resolve, sparing deliberate seeds. Folded into the same machinery is an active REFERENT-RESOLUTION check: an authorial full-context pass extracts every AMBIGUOUS referent (a pronoun/vague phrase with >1 plausible antecedent) and its intended target, the same windowed first-pass readers resolve each from local context only (intended answer withheld), and the clarity-auditor flags a referent the reader resolves WRONG (confident-but-wrong), UNCLEAR, or that the two readers DISAGREE on -- sparing deliberate, soon-resolved seeds (the Decision 061 payoff discriminator). Target via args {chapter, blueprint, window}.",
  phases: [
    { title: 'Split', detail: 'split the chapter into ordered prose paragraphs' },
    { title: 'Gist', detail: 'precompute a one-clause gist per paragraph (the reader long-term memory)' },
    { title: 'Referents', detail: 'authorial full-context pass extracts the chapter AMBIGUOUS referents (pronoun/vague phrase with >1 plausible antecedent) + each intended target -- to be resolved blind by the first-pass readers' },
    { title: 'Recap', detail: 'recap-generator writes a "previously on" of prior chapter(s) the readers carry into the first read' },
    { title: 'FirstRead', detail: 'two readers interpret each paragraph (prior-chapter recap + within-chapter gist + verbatim window) AND resolve each ambiguous referent in the target paragraph from first-pass context only, intended answer withheld' },
    { title: 'Reread', detail: 'each reader rereads with full context; which first-pass confusions resolved?' },
    { title: 'Compare', detail: 'clarity-auditor flags confusion that never resolves AND referents read WRONG/UNCLEAR/DISAGREE vs intended; spares working seeds and deliberate, soon-resolved referent ambiguity' },
    { title: 'Quiz', detail: 'smart agent builds a ~50Q exam; naive readers answer from their interpretation only; grader flags important misses as clarity gaps' },
  ],
}

const ROOT = '/home/codingbutter/Novel'
let a = (typeof args !== 'undefined' && args) || {}
if (typeof a === 'string') { try { a = JSON.parse(a) } catch (e) { a = {} } }
const CH = a.chapter || a.target || `${ROOT}/docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md`
const BP = a.blueprint || a.bp || `${ROOT}/docs/40-blueprints/book-1/chapter-01-no-signal/blueprint.md`
// Sliding context window (paragraphs) -- the dominant cost lever. Each first-read call sees the target
// paragraph plus at most WINDOW-1 of the immediately preceding ones, never the whole chapter-so-far.
// This turns the quadratic context re-send into linear without ever leaking FUTURE text. Raise it for
// a chapter with long-range callbacks; lower it to spend less.
const WINDOW = Number(a.window) > 0 ? Number(a.window) : 10

// Resilience: a single agent() call THROWS on retry-cap / API error / dropped connection, which would
// abort the whole audit. Wrap the lone (non-parallel) calls so a transient drop retries instead of losing
// the run. parallel() already absorbs failures (returns null per thunk), so it does not need this.
async function tryAgent(make, tries) { tries = tries || 3; let last; for (let i = 0; i < tries; i++) { try { const r = await make(); if (r) return r; last = new Error('empty result'); } catch (e) { last = e; log('retry ' + (i + 1) + '/' + tries + ': ' + String(e).slice(0, 140)); } } throw last; }

const SPLIT = { type: 'object', required: ['paragraphs'], properties: {
  paragraphs: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, opening: { type: 'string' }, text: { type: 'string' } } }, description: 'the STORY prose paragraphs in order (skip yaml frontmatter and everything from any "Revision Notes"/critique log onward). Each: n (1-based), opening (~6 words), text (full paragraph verbatim).' },
} }

phase('Split')
log(`interpretation-audit (progressive, window=${WINDOW}, 2 readers): ${CH}`)
const split = await tryAgent(() => agent(
  `Read ${CH} and extract the STORY PROSE only, as an ordered list of paragraphs. SKIP the yaml frontmatter and SKIP everything from any "Revision Notes"/adjudication/critique log to the end of the file. A paragraph is a block separated by blank lines; keep short one-line paragraphs as their own entries; do not merge or summarize. Return each paragraph VERBATIM with a 1-based index n and its ~6-word opening. Return per schema.`,
  { schema: SPLIT, label: 'split', phase: 'Split' }
))
const paras = (split && split.paragraphs) || []
if (!paras.length) throw new Error('Split produced 0 paragraphs (truncated/dropped response?) -- aborting rather than auditing an empty chapter and reporting a false CLEAR')

phase('Gist')
// A reader carries the earlier chapter as fuzzy GIST, not verbatim. We precompute a one-clause gist per
// paragraph, then feed each first-read the gist of everything OUTSIDE its verbatim window -- so the reader
// has the long-term memory a real reader has, and the window stops manufacturing false amnesia. One cheap
// pass, compressed ~5x vs verbatim.
const GIST = { type: 'object', required: ['gists'], properties: {
  gists: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, gist: { type: 'string' } } }, description: 'one ultra-short clause (<=12 words) per paragraph -- what a reader would REMEMBER happened in it (who/what/where), no prose, keep the index n' },
} }
// Chunked: emitting one gist per paragraph for the WHOLE chapter in a single structured output is a big
// fragile response (truncates/drops on long chapters). Batch the paragraphs (~25 each) and let parallel()
// run one agent per batch -- each sees only its batch, same prompt/intent -- then merge all returned gists.
const GIST_BATCH = 25
const gistBatches = []
for (let i = 0; i < paras.length; i += GIST_BATCH) gistBatches.push(paras.slice(i, i + GIST_BATCH))
const gistRuns = await parallel(gistBatches.map(batch => () => agent(
  `Here are the chapter's paragraphs in order. For EACH, write ONE ultra-short clause (<=12 words) capturing what a reader would REMEMBER happening in it -- the fuzzy gist memory you keep of earlier parts of a story (who/what/where), not the wording. Keep each paragraph's index n.\n\n${batch.map(p => `[${p.n}] ${p.text}`).join('\n\n')}\n\nReturn per schema: one gist per paragraph.`,
  { schema: GIST, effort: 'low', label: 'gist', phase: 'Gist' }
)))
const gistByN = {}
gistRuns.filter(Boolean).forEach(res => ((res && res.gists) || []).forEach(g => { gistByN[g.n] = g.gist }))

phase('Referents')
// EXTRACT (the active referent-resolution check, grounded in Decision 061's "untrackable referent" =
// accidental obscurity = bug). BEFORE the readers read, an authorial pass with FULL context finds the
// AMBIGUOUS referents -- a pronoun ("it","he","this") or vague noun phrase ("the man","the device") a
// first-time reader could reasonably attach to MORE THAN ONE antecedent -- and records, for each, the
// INTENDED target (resolved from the whole chapter) plus the decoy a reader could wrongly land on. The
// windowed first-pass readers (FirstRead) then resolve these from local context only, WITHOUT the intended
// answer; Compare grades a referent a clarity bug when a reader lands CONFIDENT-BUT-WRONG, is UNCLEAR, or
// the two readers DISAGREE -- sparing ambiguity that is a deliberate, soon-resolved seed (same payoff
// discriminator as resolve-vs-never-resolve). This catches the "It was the habit of years" failure (reader
// reads "it" = the phone, not the habitual act of reaching for it) that self-reported confusion alone misses.
// Reuses the chunked-Gist substrate: each batch gets the whole-chapter gist outline (so intended targets,
// including seeds that pay off later, resolve correctly) + its verbatim slice + a small verbatim lead-in for
// nearby antecedents. Robust + parallel like Gist; effort high because intended-target accuracy matters.
const REFS = { type: 'object', required: ['referents'], properties: {
  referents: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, token: { type: 'string' }, sentence: { type: 'string' }, intended: { type: 'string' }, decoy: { type: 'string' } } }, description: 'ONLY the genuinely AMBIGUOUS referents that occur in the PARAGRAPHS TO ANALYZE -- a pronoun (it/he/she/they/this/that/there) or vague noun phrase ("the man","the device") a first-time reader, having read only up to that point, could reasonably attach to MORE THAN ONE antecedent in scope. Each: n (the paragraph index it occurs in), token (the referent word/phrase verbatim), sentence (the verbatim sentence containing it), intended (what it ACTUALLY refers to, resolved from the whole-chapter context), decoy (the competing antecedent a reader could wrongly land on). Skip referents with a single obvious antecedent -- only the misreadable ones.' },
} }
const wholeGistOutline = paras.map(p => `[${p.n}] ${gistByN[p.n] || '...'}`).join('\n')
const REF_OVERLAP = 3
const refBatches = []
for (let i = 0; i < paras.length; i += GIST_BATCH) refBatches.push({ start: i, slice: paras.slice(i, i + GIST_BATCH) })
const refRuns = await parallel(refBatches.map(b => () => {
  const leadStart = Math.max(0, b.start - REF_OVERLAP)
  const leadIn = b.start > leadStart ? paras.slice(leadStart, b.start).map(p => `[${p.n}] ${p.text}`).join('\n\n') : ''
  const analyze = b.slice.map(p => `[${p.n}] ${p.text}`).join('\n\n')
  return agent(
    `You know the WHOLE chapter; a first-time reader does not. Below is a one-line gist outline of the entire chapter (use it to resolve every referent to its TRUE target, including a referent whose meaning is only clear later), then optional preceding context (for antecedents only -- do NOT extract from it), then the paragraphs to analyze.\n\nWHOLE-CHAPTER OUTLINE (gist):\n${wholeGistOutline}\n\n${leadIn ? `PRECEDING CONTEXT (antecedents only -- do NOT extract referents from these):\n${leadIn}\n\n` : ''}PARAGRAPHS TO ANALYZE (verbatim):\n${analyze}\n\nFind every AMBIGUOUS referent that occurs IN THE PARAGRAPHS TO ANALYZE: a pronoun (it/he/she/they/this/that/there) or vague noun phrase ("the man","the device") that a first-time reader, having read only up to that point, could reasonably attach to MORE THAN ONE antecedent. For each give n, token, the verbatim sentence, the INTENDED target (resolved from the whole chapter), and the decoy (the wrong antecedent a reader could land on). Worked example: in "It was the habit of years," "it" intends the habitual ACT of reaching for the phone, yet a reader can confidently read "it" = the phone -- exactly the kind to catch. Only genuinely misreadable referents; skip the obvious ones. Per schema.`,
    { schema: REFS, effort: 'high', label: 'referents', phase: 'Referents' }
  )
}))
const referentsByN = {}
const referentById = {}
let refSeq = 0
refRuns.filter(Boolean).forEach(res => ((res && res.referents) || []).forEach(r => {
  if (!r || r.n == null || !r.token) return
  const id = `${r.n}.${++refSeq}`
  const rec = { id, n: r.n, token: r.token, sentence: r.sentence || '', intended: r.intended || '', decoy: r.decoy || '' }
  ;(referentsByN[r.n] = referentsByN[r.n] || []).push(rec)
  referentById[id] = rec
}))
log(`referents: extracted ${Object.keys(referentById).length} ambiguous referent(s) across ${Object.keys(referentsByN).length} paragraph(s)`)

// Two readers, not three: the close-reader (the most capable) rarely bounces on a first pass, and the
// audit's bar is 8th-grade legibility. 8th-grade is the bar; average-adult is the target reader.
const LEVELS = [
  { id: '8th-grade', steer: 'an attentive 13-14 year old reading at an 8th-grade level: plain words; you miss subtext and irony but follow literal action and the basic emotional drift.' },
  { id: 'average-adult', steer: 'a smart average adult reading for story: you catch ordinary implication but flag anything you had to work at.' },
]

const FR = { type: 'object', required: ['understanding', 'confused'], properties: {
  understanding: { type: 'string', description: 'in your own words, what you understand is happening in the FINAL paragraph, knowing ONLY what you have read so far' },
  confused: { type: 'boolean', description: 'true if this paragraph tripped you on this FIRST read: a pronoun with no referent yet, a jump you could not track, a phrase you could not parse, a metaphor that did not land' },
  what_tripped: { type: 'string', description: 'if confused, the specific thing that tripped you; else empty' },
  referent_reads: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, token: { type: 'string' }, refers_to: { type: 'string' }, sure: { type: 'boolean' } } }, description: 'ONLY if ambiguous referents were listed for the final paragraph: for EACH listed referent, by its id, what YOU read <token> as referring to from ONLY what you have read so far -- report your HONEST first-pass reading even when you feel confident (do NOT hunt for the "right"/author-intended answer). sure:false ONLY if you genuinely cannot tell. Empty array if none were listed.' },
} }

// --- Prior-chapter memory (recap) ------------------------------------------
// A real reader of chapter N has read chapters 1..N-1, so they carry that memory into
// the first read. args.prior may be a single path or an array of prior-chapter manuscript
// .md paths. If absent, best-effort infer the immediately-preceding chapter from CH's
// number; if none can be found (e.g. Chapter 1, or no number in the path) the recap is
// skipped entirely -- recap stays empty and nothing is prepended. The recap-generator
// resolves and reads the prior prose itself.
const priorPaths = (Array.isArray(a.prior) ? a.prior : (a.prior ? [a.prior] : [])).filter(Boolean)
const chNumMatch = String(CH).match(/chapter[-_ ]?(\d+)/i)
const priorChapterNum = (!priorPaths.length && chNumMatch && Number(chNumMatch[1]) > 1)
  ? Number(chNumMatch[1]) - 1
  : null
const priorScope = priorPaths.length
  ? `the prior-chapter manuscript file(s):\n${priorPaths.join('\n')}`
  : (priorChapterNum != null
      ? `the immediately-preceding chapter, Chapter ${priorChapterNum}: find its APPROVED manuscript prose under ${ROOT}/docs/50-manuscript/book-1/ (the chapter-${String(priorChapterNum).padStart(2, '0')}-* folder's main .md, NOT the .author-notes / .gemini-critique / .narrative-script companions)`
      : null)

const RECAP = { type: 'object', required: ['recap'], properties: {
  recap: { type: 'string', description: 'a tight "PREVIOUSLY ON" recap in reader voice -- ONLY the prior-chapter beats, states, relationships, setups and open questions THIS chapter draws on or pays off, as a real reader would remember them; carry open questions as open; no future reveals, nothing the reader has not been shown on the page' },
} }

phase('Recap')
// Hand the blind first-read readers the prior-chapter memory a real reader of THIS chapter
// would carry. Empty when there is no prior chapter (Chapter 1 / unresolved) -- then nothing
// is prepended and the first-read behaves exactly as before.
let recap = ''
if (priorScope) {
  const recapRes = await tryAgent(() => agent(
    `Produce a tight "PREVIOUSLY ON" recap to prepend to a first-time reader's memory before a clarity audit of the chapter at ${CH}. Read ${priorScope}. Read the current chapter's blueprint at ${BP} as your relevance filter (Information Deliberately Withheld, Narrative Purpose, Reader Information, setups/payoffs). Surface ONLY the earlier beats this chapter actually draws on or pays off -- reader-facing narrative memory, selective not exhaustive. This text is prepended verbatim as what the reader remembers from earlier chapters, so include only what a real reader would truly have retained, carry open questions as open, and expose no future or not-yet-shown reveal. Return per schema.`,
    { agentType: 'recap-generator', schema: RECAP, label: 'recap', phase: 'Recap' }
  ))
  recap = (recapRes && recapRes.recap) || ''
  log(recap ? `recap: carried ${recap.length} chars of prior-chapter memory into the first read` : 'recap: prior chapter found but recap came back empty; first read runs cold')
} else {
  log('recap: no prior chapter (Chapter 1 or unresolved path) -- first read runs cold, nothing prepended')
}

phase('FirstRead')
// The reader's first-read context = prior-chapter recap (below) + within-chapter "story so
// far" gist + recent verbatim window. The recap is prepended ONLY here, not in the Reread
// (which already holds the full chapter).
const recapLead = recap ? `PREVIOUSLY (what you remember from earlier chapters):\n${recap}\n\n` : ''
const frMeta = []
const thunks = []
for (const L of LEVELS) for (let i = 0; i < paras.length; i++) {
  const start = Math.max(0, i + 1 - WINDOW)
  const recent = paras.slice(start, i + 1).map(p => `[${p.n}] ${p.text}`).join('\n\n')
  const priorGist = start > 0
    ? paras.slice(0, start).map(p => `[${p.n}] ${gistByN[p.n] || '...'}`).join('\n')
    : ''
  const lead = start > 0
    ? `STORY SO FAR -- your fuzzy gist memory of the earlier chapter you have already read (what happened, NOT the wording):\n${priorGist}\n\nMOST RECENT, freshest in your mind, verbatim:\n\n`
    : `Here is the chapter from the beginning, up to the paragraph to interpret:\n\n`
  const tn = paras[i].n
  // RESOLVE step (referent check): if this paragraph has ambiguous referents, the SAME windowed first-pass
  // reader resolves each from local context only -- the intended target is NEVER shown to them.
  const myRefs = referentsByN[tn] || []
  const refBlock = myRefs.length
    ? ` Also, in paragraph [${tn}] resolve each of these referents using ONLY what you have read above -- for each id, what does the token refer to? Report what you ACTUALLY read it as (even when you feel sure); set sure:false only if you truly cannot tell. Do NOT try to guess the author's intent:\n${myRefs.map(r => `- id ${r.id}: "${r.token}" in: ${r.sentence}`).join('\n')}`
    : ''
  frMeta.push({ level: L.id, n: tn, opening: paras[i].opening })
  thunks.push(() => agent(
    `You are ${L.steer}\n\n${recapLead}${lead}${recent}\n\nReading for the first time, you have NOT read past paragraph [${tn}]. In your own words, what is happening in paragraph [${tn}], using only what is above? Mark confused if it tripped you.${refBlock} Per schema.`,
    { agentType: 'lay-reader', schema: FR, model: 'haiku', label: `fr:${L.id}:${tn}`, phase: 'FirstRead' }
  ))
}
const firstReads = await parallel(thunks)
// Retry-sweep: schema-retry-cap / transient failures come back null. Re-run just those once before
// scoring, so a dropped read becomes a recovered read instead of a silent "not confused" default.
// (One sweep only -- a consistently-hard paragraph stays null and degrades gracefully, no infinite loop.)
const retryIdx = firstReads.map((r, k) => (r ? -1 : k)).filter(k => k >= 0)
if (retryIdx.length) {
  log(`retry-sweep: re-running ${retryIdx.length} failed first-reads`)
  const retried = await parallel(retryIdx.map(k => thunks[k]))
  retryIdx.forEach((k, j) => { if (retried[j]) firstReads[k] = retried[j] })
}
const fr = frMeta.map((m, k) => ({ ...m, ...(firstReads[k] || { understanding: '(agent failed)', confused: false, what_tripped: '', referent_reads: [] }) }))
const confusedByReader = {}
for (const L of LEVELS) confusedByReader[L.id] = fr.filter(x => x.level === L.id && x.confused)
// Gather each reader's blind first-pass resolution per referent id (intended answer was withheld from them).
const refReadById = {}
for (const x of fr) for (const rr of (x.referent_reads || [])) {
  if (!rr || !rr.id) continue
  ;(refReadById[rr.id] = refReadById[rr.id] || {})[x.level] = { refers_to: rr.refers_to || '', sure: !!rr.sure }
}

phase('Reread')
const RR = { type: 'object', required: ['resolutions'], properties: {
  resolutions: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, resolved: { type: 'boolean' }, note: { type: 'string' } } }, description: 'for each previously-confusing paragraph: resolved:true if the full chapter explained it / it was a setup that paid off; resolved:false if still unclear even now' },
} }
const fullProse = paras.map(p => `[${p.n}] ${p.text}`).join('\n\n')
const rereads = await parallel(LEVELS.map(L => () => {
  const myConfused = confusedByReader[L.id]
  if (!myConfused.length) return Promise.resolve({ resolutions: [] })
  return agent(
    `You are ${L.steer} You have now read this WHOLE chapter. Here it is in full:\n\n${fullProse}\n\nOn your FIRST read (paragraph by paragraph, without seeing ahead) these paragraphs tripped you:\n${myConfused.map(c => `[${c.n}] (${c.opening}) -- tripped by: ${c.what_tripped}`).join('\n')}\n\nFor EACH of those, now that you have the whole chapter: did the confusion RESOLVE (a later part explained it, or it was a setup that paid off) = resolved:true, or is it STILL unclear even with everything = resolved:false? Return per schema.`,
    { agentType: 'lay-reader', schema: RR, model: 'haiku', label: `rr:${L.id}`, phase: 'Reread' }
  )
}))
const rrByReader = {}
LEVELS.forEach((L, i) => { rrByReader[L.id] = (rereads[i] && rereads[i].resolutions) || [] })

phase('Compare')
const FLAGS = { type: 'object', required: ['bugs', 'working_seeds', 'referent_bugs', 'referent_seeds'], properties: {
  bugs: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, opening: { type: 'string' }, who: { type: 'string' }, problem: { type: 'string' }, severity: { type: 'string' } } }, description: 'paragraphs confusing on first read that did NOT resolve even with full context = real clarity bugs to fix' },
  working_seeds: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, opening: { type: 'string' }, note: { type: 'string' } } }, description: 'paragraphs confusing on first read but RESOLVED by later context = intended foreshadowing/seeding, spared (NOT bugs)' },
  referent_bugs: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, n: { type: 'number' }, token: { type: 'string' }, intended: { type: 'string' }, misread_as: { type: 'string' }, verdict: { type: 'string' }, who: { type: 'string' }, severity: { type: 'string' }, problem: { type: 'string' } } }, description: 'AMBIGUOUS referents a first-pass reader resolved WRONG (their refers_to denotes something OTHER than the intended target -- confident-but-wrong), UNCLEAR (could not resolve it), or where the two readers DISAGREED -- AND the ambiguity is NOT a deliberate, soon-resolved seed. verdict = wrong|unclear|disagree; misread_as = what the reader(s) wrongly landed on. Real clarity bugs (an untrackable/misreadable referent, Decision 061).' },
  referent_seeds: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, n: { type: 'number' }, token: { type: 'string' }, note: { type: 'string' } } }, description: 'ambiguous referents a reader misread or found unclear on first pass, but whose ambiguity is DELIBERATE and pays off / is clarified soon (a working seed) -- spared, NOT bugs. Same payoff discriminator as working_seeds.' },
  summary: { type: 'string' },
} }
const evidence = LEVELS.map(L => ({
  level: L.id,
  first_pass_confused: confusedByReader[L.id].map(c => ({ n: c.n, opening: c.opening, tripped: c.what_tripped })),
  resolutions: rrByReader[L.id],
}))
// Referent evidence: each extracted ambiguous referent with its INTENDED target + decoy, and how each blind
// first-pass reader actually resolved it (with confidence). The auditor never sees the readers were given the
// intended answer -- they were not. Empty when the chapter has no flagged ambiguous referents.
const referentEvidence = Object.values(referentById).map(r => ({
  id: r.id, n: r.n, token: r.token, sentence: r.sentence, intended: r.intended, decoy: r.decoy,
  reader_resolutions: LEVELS.map(L => ({ level: L.id, refers_to: ((refReadById[r.id] || {})[L.id] || {}).refers_to || '(no answer)', sure: !!((refReadById[r.id] || {})[L.id] || {}).sure })),
}))
const referentBlock = referentEvidence.length
  ? `\n\nSEPARATELY, a REFERENT-RESOLUTION check. An authorial pass with FULL context listed the chapter's AMBIGUOUS referents, each with its INTENDED target and the decoy a reader could be misled to; the SAME two windowed first-pass readers were then asked -- WITHOUT ever being shown the intended answer -- what each refers to. Here is each referent and how each reader resolved it (with confidence):\n\n${JSON.stringify(referentEvidence)}\n\nUsing the FULL chapter below, grade each referent into referent_bugs or referent_seeds:\n- REFERENT BUG = a reader resolved it WRONG (their refers_to denotes something OTHER than intended -- the confident-but-wrong failure, e.g. reading "it" = the phone when it means the habitual act of reaching for it), OR UNCLEAR (could not resolve it), OR the two readers DISAGREED (resolved to materially different things) -- AND the ambiguity is NOT deliberate craft. set verdict = wrong|unclear|disagree and misread_as = what was wrongly landed on. Weight a confident-but-wrong read at the 8th-grade level most heavily.\n- REFERENT SEED = the ambiguity is DELIBERATE and pays off / is clarified soon after (an intended brief "wait for it"), or it sits in the blueprint's deliberately-withheld set. Spared, NOT a bug. Apply the SAME payoff discriminator as resolve-vs-never-resolve (Decision 061): accidental, no-payoff ambiguity (an untrackable/misreadable referent) is the bug; a referent whose openness pays off is craft -- the discriminator is PAYOFF, not plainness.\n\nFULL CHAPTER:\n${fullProse}`
  : '\n\nThe referent-resolution check flagged no ambiguous referents in this chapter; return referent_bugs and referent_seeds as empty arrays.'
const compare = await tryAgent(() => agent(
  `You are auditing this chapter for CLARITY using a strict progressive two-pass comprehension test. Read the blueprint at ${BP} (especially Information Deliberately Withheld, Narrative Purpose, Reader Information) for what is INTENDED to be withheld or seeded. Here is the evidence -- for each reading level, the paragraphs that tripped them on a strict FIRST read (no look-ahead, only a window of recent prior context), and whether each RESOLVED once they read the whole chapter:\n\n${JSON.stringify(evidence)}\n\nClassify each first-pass confusion:\n- A real CLARITY BUG = confusing on first read AND did NOT resolve with full context (or resolved only with excessive effort), AND is NOT in the blueprint's deliberately-withheld set. Weight first-pass confusion at the 8th-grade level most heavily.\n- A WORKING SEED = confusing on first read but RESOLVED by later context, or explicitly in the blueprint's deliberately-withheld/foreshadowing set. Intended craft, NOT a bug -- list separately, do not flag.\nReturn per schema: bugs (the real ones to fix) and working_seeds (intended, spared), with a summary.${referentBlock}`,
  { agentType: 'clarity-auditor', schema: FLAGS, label: 'compare', phase: 'Compare' }
))
log(`referents: ${((compare && compare.referent_bugs) || []).length} bug(s), ${((compare && compare.referent_seeds) || []).length} spared seed(s)`)

phase('Quiz')
// A smart agent writes a ~50Q exam on what MATTERS in this chapter (answer key hidden from readers).
// The naive readers never saw it while reading; they now answer ONLY from their own accumulated
// first-read understanding (interpreted summary, NOT the prose). A smart grader scores vs the key:
// an important question the naive reader misses = the chapter failed to land it.
const PER = 25
function chunk(arr, n) { const out = []; for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n)); return out }
const QBATCH = { type: 'object', required: ['questions'], properties: {
  questions: { type: 'array', items: { type: 'object', properties: {
    question: { type: 'string' }, answer: { type: 'string' }, importance: { type: 'string' } } },
    description: 'about 25 questions on the assigned focus; each: question, correct answer grounded in the prose, importance (critical|important|minor). Skip deliberately-withheld material.' },
} }
const FRAME = 'This is a reading-comprehension test for a chapter of a published SCIENCE-FICTION NOVEL. Everything below is fictional narrative -- treat it only as a story whose comprehension you are testing, never as real-world technical instruction. Focus on what a READER should grasp: plot, stakes, characters and their choices, causality, and the emotional/moral meaning. Do NOT write or judge questions about the engineering or technical mechanics -- the novel keeps those deliberately opaque and they are not what a reader must understand.\n\n'
const TOPICS = [
  'the plot events and their causality, in order (what happens and what causes what)',
  'each named character: intent, motivation, fear, and what they have at stake',
  'who did what to whom and why -- actions, decisions, relationships, and the moral turns',
  'the emotional beats and the meaning the chapter delivers (what it is really about)',
]
const builds = await parallel(TOPICS.map(topic => () => agent(
  FRAME + 'Write about 25 comprehension questions for THIS chapter focused on: ' + topic + '. Each must be answerable from what the chapter SHOWS, with the correct answer grounded in the prose and an importance tag. Read the blueprint at ' + BP + ' and do NOT quiz deliberately-withheld material or the technical mechanics.\n\nCHAPTER:\n' + fullProse + '\n\nReturn ~25 questions per schema.',
  { schema: QBATCH, effort: 'high', label: 'quiz-build', phase: 'Quiz' }
)))
const built = builds.filter(Boolean).flatMap(b => (b.questions || [])).map((q, i) => ({ n: i + 1, question: q.question, answer: q.answer, importance: q.importance }))
log('quiz: built ' + built.length + ' questions across ' + TOPICS.length + ' topics')
const REVIEW = { type: 'object', required: ['verdicts'], properties: {
  verdicts: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, verdict: { type: 'string' } } },
    description: 'for EACH question by its n: verdict = "correct" (answer right + question clear and grounded), "wrong" (answer incorrect), or "ambiguous" (unclear, untestable from prose, or about withheld material). Be strict.' },
} }
const revThunks = []
chunk(built, PER).forEach(c => [0, 1, 2].forEach(() => revThunks.push(() => agent(
  FRAME + 'Certify a comprehension exam against its source chapter. For EACH question below, by its n, return a verdict: "correct" if the given answer is right and grounded and the question is clear and fair; "wrong" if the answer is incorrect; "ambiguous" if unclear, untestable from the prose, or about deliberately-withheld material. Be strict -- only certain ones are kept.\n\nCHAPTER:\n' + fullProse + '\n\nQUESTIONS (with proposed answers):\n' + JSON.stringify(c) + '\n\nA verdict for every question, per schema.',
  { schema: REVIEW, effort: 'high', label: 'quiz-review', phase: 'Quiz' }
))))
const reviews = await parallel(revThunks)
const voteByN = {}
reviews.filter(Boolean).forEach(rv => (rv.verdicts || []).forEach(v => { (voteByN[v.n] = voteByN[v.n] || []).push(v.verdict) }))
const questions = built.filter(q => { const vs = voteByN[q.n] || []; return vs.filter(x => x === 'correct').length >= 2 && !vs.includes('ambiguous') })
log('quiz: peer-certified ' + questions.length + ' of ' + built.length + ' (>=2 of 3 confirm, none ambiguous)')
const ANS = { type: 'object', required: ['answers'], properties: {
  answers: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, answer: { type: 'string' }, sure: { type: 'boolean' } } },
    description: 'your best answer to each question from ONLY your memory; sure:false if guessing or unknown -- never invent' },
} }
const summaryByLevel = {}
for (const L of LEVELS) summaryByLevel[L.id] = fr.filter(x => x.level === L.id).slice().sort((p, q) => p.n - q.n).map(x => '[' + x.n + '] ' + x.understanding).join('\n')
const ansMeta = []
const ansThunks = []
for (const L of LEVELS) chunk(questions, PER).forEach(c => { ansMeta.push(L.id); ansThunks.push(() => agent(
  'You are ' + L.steer + ' You read this chapter once. Here is YOUR OWN running understanding of it -- all you remember, and you do NOT have the text:\n\n' + summaryByLevel[L.id] + '\n\nAnswer these from memory ONLY. If you do not know or are guessing, set sure:false -- do not invent.\n\nQUESTIONS:\n' + c.map(q => '[' + q.n + '] ' + q.question).join('\n') + '\n\nPer schema.',
  { agentType: 'lay-reader', schema: ANS, model: 'haiku', label: 'quiz-ans:' + L.id, phase: 'Quiz' }
)) })
const ansRuns = await parallel(ansThunks)
const ansMap = { '8th-grade': {}, 'average-adult': {} }
ansRuns.forEach((res, i) => { if (res && res.answers) res.answers.forEach(a => { ansMap[ansMeta[i]][a.n] = a }) })
const GRADE = { type: 'object', required: ['results'], properties: {
  results: { type: 'array', items: { type: 'object', properties: {
    n: { type: 'number' }, importance: { type: 'string' }, grade_8th: { type: 'string' }, grade_avg: { type: 'string' }, clarity_gap: { type: 'boolean' }, note: { type: 'string' } } },
    description: 'per question: grade_8th/grade_avg each correct|partial|wrong|blank vs the key; clarity_gap:true when a critical/important question is missed (wrong/blank) by the naive reader(s)' },
} }
const gradeThunks = chunk(questions, PER).map(c => () => agent(
  FRAME + 'Grade a comprehension-exam chunk. Each item has the question, the correct KEY answer, its importance, and what the two naive readers answered from memory. Grade each reader correct|partial|wrong|blank against the key. Set clarity_gap:true when a CRITICAL or IMPORTANT question is missed (wrong/blank) by the reader(s); minor misses are not gaps.\n\n' + JSON.stringify(c.map(q => ({ n: q.n, question: q.question, key: q.answer, importance: q.importance, ans_8th: (ansMap['8th-grade'][q.n] || {}).answer || '(blank)', ans_avg: (ansMap['average-adult'][q.n] || {}).answer || '(blank)' }))) + '\n\nPer schema.',
  { agentType: 'clarity-auditor', schema: GRADE, effort: 'high', label: 'quiz-grade', phase: 'Quiz' }
))
const gradeRuns = await parallel(gradeThunks)
const results = gradeRuns.filter(Boolean).flatMap(g => (g.results || []))
const gaps = results.filter(r => r.clarity_gap)
const pct = key => { const ok = results.filter(r => r[key] === 'correct').length; return results.length ? Math.round(100 * ok / results.length) + '% (' + ok + '/' + results.length + ')' : 'n/a' }
log('quiz: graded ' + results.length + '; ' + gaps.length + ' clarity gaps')

return { chapter: CH, paragraphs: paras.length, window: WINDOW, readers: LEVELS.map(L => L.id), prior_recap_chars: recap ? recap.length : 0, first_pass_confusions: fr.filter(x => x.confused).length, referents: { extracted: Object.keys(referentById).length, bugs: ((compare && compare.referent_bugs) || []), seeds: ((compare && compare.referent_seeds) || []) }, compare, quiz: { built: built.length, certified: questions.length, graded: results.length, score_8th: pct('grade_8th'), score_avg: pct('grade_avg'), gaps } }
