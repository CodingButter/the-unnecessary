export const meta = {
  name: 'interpretation-audit',
  description: "Clarity audit of a chapter by comprehension test: three lay-readers at different reading levels (8th-grade, average adult, close reader) independently re-tell the chapter paragraph by paragraph in their own words; a clarity-auditor aligns the retellings against the actual prose and the blueprint's intended takeaways, flagging any paragraph where readers diverge or get lost (real ambiguity), distinguishing that from mere depth-variation. The target chapter is parameterized via args {chapter, blueprint}; the readers run as crew lay-readers and the comparator as the crew clarity-auditor.",
  phases: [
    { title: 'Read', detail: 'three lay-readers (8th-grade, average adult, close reader) re-tell the chapter in their own words' },
    { title: 'Compare', detail: 'a clarity-auditor flags paragraphs where understanding diverges from intent' },
  ],
}

const ROOT = '/home/codingbutter/Novel'
const CH1 = `${ROOT}/docs/50-manuscript/book-1/chapter-01-no-signal/chapter-01-no-signal.md`
const CH1_BP = `${ROOT}/docs/40-blueprints/book-1/chapter-01-no-signal/blueprint.md`

// ---- Parameters (passed as Workflow args: {chapter, blueprint}) ----
let a = args || {}
if (typeof a === 'string') { try { a = JSON.parse(a) } catch (e) { a = {} } }
const CHAPTER = a.chapter || a.target || CH1
const BP = a.blueprint || a.bp || CH1_BP

const RETELL = { type: 'object', required: ['paragraphs'], properties: {
  paragraphs: { type: 'array', items: { type: 'object', properties: {
    opening: { type: 'string', description: 'first ~6 words of the paragraph, verbatim, to locate it' },
    understanding: { type: 'string', description: 'what you think is happening, in your OWN words at your reading level' },
    confused: { type: 'boolean', description: 'true if you genuinely could not follow this paragraph' },
  } } },
} }

const FLAGS = { type: 'object', required: ['flagged'], properties: {
  flagged: { type: 'array', items: { type: 'object', properties: {
    opening: { type: 'string' },
    excerpt: { type: 'string' },
    divergence: { type: 'string', description: 'how the three readers understood it differently, or who got lost' },
    intended: { type: 'string', description: 'what the paragraph actually means to convey (from prose + blueprint)' },
    severity: { type: 'string' },
  } } },
  clean_count: { type: 'number', description: 'paragraphs where all three converged on the same basic drift' },
  summary: { type: 'string' },
} }

phase('Read')
log(`interpretation-audit: ${CHAPTER}`)
const LEVELS = [
  { id: '8th-grade', steer: 'Read at an 8th-grade level: use plain words, do not reach for literary subtext, just tell what is literally happening, and say plainly whenever a sentence loses you.' },
  { id: 'average-adult', steer: 'Read as a smart average adult reading for story, not for English class: tell what is happening and what it means to you, and flag anything you had to read twice.' },
  { id: 'close-reader', steer: 'Read as a careful literary close-reader: tell what each paragraph means, including its subtext and intent.' },
]
const retellings = await parallel(LEVELS.map(L => () => agent(
  `Read the whole story prose of the chapter at ${CHAPTER}. ${L.steer} Read ONLY the narrative prose (skip the yaml frontmatter and skip everything from any "Revision Notes" / adjudication / critique log to the end of the file). Go paragraph by paragraph and, in your OWN words, say what you think is happening in each -- do NOT quote the prose back, re-tell it. Mark confused:true on any paragraph you genuinely could not follow. Return per the schema.`,
  { agentType: 'lay-reader', schema: RETELL, label: `read:${L.id}`, phase: 'Read' }
).catch(() => null)))

phase('Compare')
const named = LEVELS.map((L, i) => ({ level: L.id, retelling: retellings[i] }))
const compare = await agent(
  `You are auditing this chapter for CLARITY by comparison. Read the actual prose at ${CHAPTER} and the chapter blueprint at ${BP} (for the INTENDED takeaway of each beat). Then study these three independent reader retellings, one per reading level:\n\n${JSON.stringify(named)}\n\nFor each story paragraph, compare the three readers' understandings against each other AND against what the paragraph actually intends. FLAG a paragraph when the readers CONTRADICT each other about the basic meaning, or any reader got lost, or they collectively missed the intended point -- that is real ambiguity. Do NOT flag a paragraph merely because the 8th-grader caught less subtext than the close-reader; depth-variation is fine as long as all three get the same basic drift. The bar: anyone at an 8th-grade level should be able to follow the drift, even if not every nuance. For each flag give the paragraph opening, a short excerpt, exactly how the readers diverged, what it actually intends, and a severity. Return per the schema.`,
  { agentType: 'clarity-auditor', schema: FLAGS, label: 'compare', phase: 'Compare' }
)

return { chapter: CHAPTER, blueprint: BP, retellings: retellings.filter(Boolean), compare }
