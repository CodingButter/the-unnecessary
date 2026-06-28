export const meta = {
  name: 'interpretation-audit',
  description: "Progressive two-pass clarity audit of a chapter. Two lay-readers (8th-grade and average-adult) read it paragraph by paragraph with only a sliding window of recent prior paragraphs visible (no future context, fed as text so they cannot look ahead), reporting first-read understanding and first-pass confusion; then each rereads with the full chapter and reports which confusions RESOLVED (intended seed/foreshadowing) vs which remain (real clarity bug); a clarity-auditor flags only confusions that never resolve, sparing deliberate seeds. Target via args {chapter, blueprint, window}.",
  phases: [
    { title: 'Split', detail: 'split the chapter into ordered prose paragraphs' },
    { title: 'Gist', detail: 'precompute a one-clause gist per paragraph (the reader long-term memory)' },
    { title: 'Recap', detail: 'recap-generator writes a "previously on" of prior chapter(s) the readers carry into the first read' },
    { title: 'FirstRead', detail: 'two readers interpret each paragraph: prior-chapter recap + within-chapter gist + verbatim window' },
    { title: 'Reread', detail: 'each reader rereads with full context; which first-pass confusions resolved?' },
    { title: 'Compare', detail: 'clarity-auditor flags confusion that never resolves; spares working seeds' },
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

const SPLIT = { type: 'object', required: ['paragraphs'], properties: {
  paragraphs: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, opening: { type: 'string' }, text: { type: 'string' } } }, description: 'the STORY prose paragraphs in order (skip yaml frontmatter and everything from any "Revision Notes"/critique log onward). Each: n (1-based), opening (~6 words), text (full paragraph verbatim).' },
} }

phase('Split')
log(`interpretation-audit (progressive, window=${WINDOW}, 2 readers): ${CH}`)
const split = await agent(
  `Read ${CH} and extract the STORY PROSE only, as an ordered list of paragraphs. SKIP the yaml frontmatter and SKIP everything from any "Revision Notes"/adjudication/critique log to the end of the file. A paragraph is a block separated by blank lines; keep short one-line paragraphs as their own entries; do not merge or summarize. Return each paragraph VERBATIM with a 1-based index n and its ~6-word opening. Return per schema.`,
  { schema: SPLIT, label: 'split', phase: 'Split' }
)
const paras = (split && split.paragraphs) || []

phase('Gist')
// A reader carries the earlier chapter as fuzzy GIST, not verbatim. We precompute a one-clause gist per
// paragraph, then feed each first-read the gist of everything OUTSIDE its verbatim window -- so the reader
// has the long-term memory a real reader has, and the window stops manufacturing false amnesia. One cheap
// pass, compressed ~5x vs verbatim.
const GIST = { type: 'object', required: ['gists'], properties: {
  gists: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, gist: { type: 'string' } } }, description: 'one ultra-short clause (<=12 words) per paragraph -- what a reader would REMEMBER happened in it (who/what/where), no prose, keep the index n' },
} }
const gistRes = await agent(
  `Here are the chapter's paragraphs in order. For EACH, write ONE ultra-short clause (<=12 words) capturing what a reader would REMEMBER happening in it -- the fuzzy gist memory you keep of earlier parts of a story (who/what/where), not the wording. Keep each paragraph's index n.\n\n${paras.map(p => `[${p.n}] ${p.text}`).join('\n\n')}\n\nReturn per schema: one gist per paragraph.`,
  { schema: GIST, effort: 'low', label: 'gist', phase: 'Gist' }
)
const gistByN = {}
;((gistRes && gistRes.gists) || []).forEach(g => { gistByN[g.n] = g.gist })

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
  const recapRes = await agent(
    `Produce a tight "PREVIOUSLY ON" recap to prepend to a first-time reader's memory before a clarity audit of the chapter at ${CH}. Read ${priorScope}. Read the current chapter's blueprint at ${BP} as your relevance filter (Information Deliberately Withheld, Narrative Purpose, Reader Information, setups/payoffs). Surface ONLY the earlier beats this chapter actually draws on or pays off -- reader-facing narrative memory, selective not exhaustive. This text is prepended verbatim as what the reader remembers from earlier chapters, so include only what a real reader would truly have retained, carry open questions as open, and expose no future or not-yet-shown reveal. Return per schema.`,
    { agentType: 'recap-generator', schema: RECAP, label: 'recap', phase: 'Recap' }
  )
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
  frMeta.push({ level: L.id, n: tn, opening: paras[i].opening })
  thunks.push(() => agent(
    `You are ${L.steer}\n\n${recapLead}${lead}${recent}\n\nReading for the first time, you have NOT read past paragraph [${tn}]. In your own words, what is happening in paragraph [${tn}], using only what is above? Mark confused if it tripped you. Per schema.`,
    { agentType: 'lay-reader', schema: FR, label: `fr:${L.id}:${tn}`, phase: 'FirstRead' }
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
const fr = frMeta.map((m, k) => ({ ...m, ...(firstReads[k] || { understanding: '(agent failed)', confused: false, what_tripped: '' }) }))
const confusedByReader = {}
for (const L of LEVELS) confusedByReader[L.id] = fr.filter(x => x.level === L.id && x.confused)

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
    { agentType: 'lay-reader', schema: RR, label: `rr:${L.id}`, phase: 'Reread' }
  )
}))
const rrByReader = {}
LEVELS.forEach((L, i) => { rrByReader[L.id] = (rereads[i] && rereads[i].resolutions) || [] })

phase('Compare')
const FLAGS = { type: 'object', required: ['bugs', 'working_seeds'], properties: {
  bugs: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, opening: { type: 'string' }, who: { type: 'string' }, problem: { type: 'string' }, severity: { type: 'string' } } }, description: 'paragraphs confusing on first read that did NOT resolve even with full context = real clarity bugs to fix' },
  working_seeds: { type: 'array', items: { type: 'object', properties: { n: { type: 'number' }, opening: { type: 'string' }, note: { type: 'string' } } }, description: 'paragraphs confusing on first read but RESOLVED by later context = intended foreshadowing/seeding, spared (NOT bugs)' },
  summary: { type: 'string' },
} }
const evidence = LEVELS.map(L => ({
  level: L.id,
  first_pass_confused: confusedByReader[L.id].map(c => ({ n: c.n, opening: c.opening, tripped: c.what_tripped })),
  resolutions: rrByReader[L.id],
}))
const compare = await agent(
  `You are auditing this chapter for CLARITY using a strict progressive two-pass comprehension test. Read the blueprint at ${BP} (especially Information Deliberately Withheld, Narrative Purpose, Reader Information) for what is INTENDED to be withheld or seeded. Here is the evidence -- for each reading level, the paragraphs that tripped them on a strict FIRST read (no look-ahead, only a window of recent prior context), and whether each RESOLVED once they read the whole chapter:\n\n${JSON.stringify(evidence)}\n\nClassify each first-pass confusion:\n- A real CLARITY BUG = confusing on first read AND did NOT resolve with full context (or resolved only with excessive effort), AND is NOT in the blueprint's deliberately-withheld set. Weight first-pass confusion at the 8th-grade level most heavily.\n- A WORKING SEED = confusing on first read but RESOLVED by later context, or explicitly in the blueprint's deliberately-withheld/foreshadowing set. Intended craft, NOT a bug -- list separately, do not flag.\nReturn per schema: bugs (the real ones to fix) and working_seeds (intended, spared), with a summary.`,
  { agentType: 'clarity-auditor', schema: FLAGS, label: 'compare', phase: 'Compare' }
)

return { paragraphs: paras.length, window: WINDOW, readers: LEVELS.map(L => L.id), prior_recap_chars: recap ? recap.length : 0, first_pass_confusions: fr.filter(x => x.confused).length, compare }
