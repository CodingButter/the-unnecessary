export const meta = {
  name: 'write-chapter',
  description: 'Reusable chapter authorship pipeline for the novel The Unnecessary (Decision 046): build the context pack, Opus drafts, Gemini critiques, Opus adjudicates. Parameterized per chapter via args {number, slug, title}. Leaves the chapter as a draft for the author to approve.',
  phases: [
    { title: 'Prep', detail: 'Build the chapter context pack from its per-chapter manifest' },
    { title: 'Draft', detail: 'Opus drafts the chapter from the blueprint and pack (canon-safe, on-voice)' },
    { title: 'Critique', detail: 'Gemini (gemini-2.5-pro) critiques the draft against the project rules' },
    { title: 'Adjudicate', detail: 'Opus applies the notes it agrees with and logs accept/reject for each' },
  ],
}

// ---- Parameters (passed as Workflow args: {number, slug, title}) ----
const NOVEL = '/home/codingbutter/Novel'
const ch = args || {}
if (ch.number === undefined || ch.number === null || !ch.slug) {
  throw new Error('write-chapter requires args {number, slug, title}, for example {"number":2,"slug":"the-last-supported-day","title":"The Last Supported Day"}')
}
const num = String(ch.number).padStart(2, '0')
const slug = ch.slug
const title = ch.title || ('Chapter ' + ch.number)

const bpDir = `docs/40-blueprints/book-1/chapter-${num}-${slug}`
const manifest = `${bpDir}/context-manifest.yaml`
const blueprint = `${bpDir}/blueprint.md`
const pack = `.context/chapter-${num}-${slug}.pack.md`
const manuscript = `docs/50-manuscript/book-1/chapter-${num}-${slug}.md`
const critique = `docs/50-manuscript/book-1/chapter-${num}-${slug}.gemini-critique.md`

const REPORT = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    summary: { type: 'string' },
    details: { type: 'string' },
  },
  required: ['ok', 'summary'],
}

// House rules shared by the creative (Opus) stages.
const RULES = `This is the literary near-future novel "The Unnecessary". Authoritative grounding for THIS chapter is the context pack at ${NOVEL}/${pack} (canon, the Style Guide, character profiles, continuity, the project rules in CLAUDE.md) and the approved blueprint at ${NOVEL}/${blueprint} (the scene-by-scene plan). Defer to them; the blueprint provides every per-chapter specific (viewpoint, date, scenes, beats, ending).
HOUSE STYLE: grounded, restrained, serious, close-third on a single viewpoint per chapter, past tense, free indirect, subtext over explanation, no cyberpunk cliches, quiet dread that accumulates beneath a competent surface. NO EM DASHES anywhere (verify with grep before finishing).
CANON SAFETY: hold the chapter's single viewpoint; the reader knows only what the viewpoint character perceives. Do not expose future reveals, do not give any AI or system unestablished capabilities, keep each technology within its canonical failure modes, and respect the timeline's event order. Treat the blueprint as an approved plan; do not contradict it.`

// ---- Stage 1: Prep (build the context pack) ----
phase('Prep')
log(`write-chapter: chapter ${num} "${title}" (slug ${slug})`)
const prep = await agent(
  `Run EXACTLY this command from ${NOVEL} and report the result:\n` +
  `  python3 scripts/build-context-pack.py ${manifest}\n` +
  `This builds the Chapter ${ch.number} context pack at ${pack}. Confirm the pack file exists afterward and report its approximate token estimate. ` +
  `If the command fails (for example the per-chapter manifest ${manifest} or the blueprint ${blueprint} does not exist), STOP and report the exact error: the precondition is that the chapter's blueprint and context-manifest already exist.`,
  { label: `ch${num}:prep`, phase: 'Prep', effort: 'low', schema: REPORT }
)
if (prep && prep.ok === false) {
  log('Prep failed; halting before drafting. Fix the precondition (blueprint + manifest) and rerun.')
  return { halted: 'prep', prep }
}

// ---- Stage 2: Draft (Opus) ----
phase('Draft')
const draft = await agent(
  `${RULES}\n\nYou are Opus, the sole prose writer. Read the pack and the blueprint in full, then WRITE the complete prose of "${title}" (chapter ${ch.number}) to a NEW file ${NOVEL}/${manuscript}.\n` +
  `Execute the blueprint scene by scene. Add YAML front matter: title "${title}", document_type "manuscript-chapter", status "draft", authority "manuscript", a one-sentence summary, tags (manuscript, book-1, chapter-${num}), related links to ../../40-blueprints/book-1/chapter-${num}-${slug}/blueprint.md and ../../30-plot/book-1/chapters/chapter-${num}.md, source_documents the blueprint path.\n` +
  `Write the best chapter you can: precise, restrained, alive on the page. When done, grep the file to confirm ZERO em dashes, confirm the ending matches the blueprint, and confirm no forbidden reveal leaked. Report word count and those confirmations. Do not write memories.`,
  { label: `ch${num}:draft`, phase: 'Draft', schema: REPORT }
)

// ---- Stage 3: Critique (Gemini via the script) ----
phase('Critique')
const crit = await agent(
  `Run EXACTLY this command from ${NOVEL} and report the result:\n` +
  `  python3 scripts/gemini-critique.py ${manuscript} --pack ${pack} --blueprint ${blueprint} --out ${critique}\n` +
  `This sends the drafted chapter to gemini-2.5-pro for an editorial critique that lands in ${critique} (a SEPARATE file; the prose is not touched). After it succeeds, READ ${critique} and return a concise summary of the highest-value suggestions grouped by severity, plus the total number of suggestions. If the command fails, report the exact error and do not invent a critique.`,
  { label: `ch${num}:critique`, phase: 'Critique', effort: 'low', schema: REPORT }
)

// ---- Stage 4: Adjudicate (Opus) ----
phase('Adjudicate')
const adj = await agent(
  `${RULES}\n\nYou are Opus, the author, adjudicating an editor's notes on your own chapter. READ the drafted chapter ${NOVEL}/${manuscript} and the Gemini critique ${NOVEL}/${critique}.\n` +
  `For EACH Gemini suggestion, decide: ACCEPT (it genuinely improves the chapter and respects canon, style, viewpoint, and reveal-safety) or REJECT (it violates the voice, canon, reveal timing, or is not an improvement). Apply every ACCEPTED change directly to ${manuscript}; you are the only hand on the prose. Reject anything that would break the house style, leak a reveal, or contradict canon, even if it sounds like a polish.\n` +
  `Append an "## Adjudication Log" section at the END of ${manuscript} (after the prose) listing each suggestion with your decision (accept or reject) and a one-line reason. Keep the chapter status "draft" (the author approves separately).\n` +
  `Before finishing: grep to confirm STILL zero em dashes, the ending is unchanged in intent, and no forbidden reveal was introduced by any accepted edit. Report: number accepted, number rejected, final word count, and the confirmations. Do not write memories.`,
  { label: `ch${num}:adjudicate`, phase: 'Adjudicate', schema: REPORT }
)

return {
  chapter: { number: ch.number, slug, title },
  files: { manuscript, critique, blueprint, pack },
  prep, draft, critique: crit, adjudicate: adj,
  next: `Review ${manuscript} and approve it (set status approved-canon and update docs/60-continuity) per Decision 046.`,
}
