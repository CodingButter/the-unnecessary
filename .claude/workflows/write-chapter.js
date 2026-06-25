export const meta = {
  name: 'write-chapter',
  description: 'Reusable chapter authorship pipeline for the novel The Unnecessary (Decisions 046 and 048): build the context pack, Opus drafts, Gemini critiques, Opus adjudicates, Opus marks a narration script. Parameterized per chapter via args {number, slug, title}. Leaves the chapter as a draft for the author to approve; audio is generated separately.',
  phases: [
    { title: 'Prep', detail: 'Build the chapter context pack from its per-chapter manifest' },
    { title: 'Draft', detail: 'Opus drafts the chapter from the blueprint and pack (canon-safe, on-voice)' },
    { title: 'Critique', detail: 'Gemini (gemini-2.5-pro) critiques the draft against the project rules' },
    { title: 'Adjudicate', detail: 'Opus applies the notes it agrees with and logs accept/reject for each' },
    { title: 'Narration Script', detail: 'Opus marks the final prose with Eleven v3 audio tags into a separate narration script' },
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
const narrativeScript = `docs/50-manuscript/book-1/chapter-${num}-${slug}.narrative-script.md`

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
  `  python3 scripts/gemini-critique.py ${manuscript} --pack ${pack} --blueprint ${blueprint} --out ${critique} --manifest ${manifest}\n` +
  `(The --manifest flag rebuilds the pack first so the critique can never run against a stale snapshot.)\n` +
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

// ---- Stage 5: Narration Script (Opus, Decision 048) ----
phase('Narration Script')
const narr = await agent(
  `You are Opus, preparing a PERFORMANCE NARRATION SCRIPT for chapter ${ch.number} ("${title}") of "The Unnecessary". A text-to-speech tool (ElevenLabs Eleven v3) will read it aloud and interprets bracketed audio tags as stage directions.\n` +
  `READ the final adjudicated prose at ${NOVEL}/${manuscript} (use ONLY the prose body; ignore the YAML front matter and the "## Adjudication Log"). WRITE a new file ${NOVEL}/${narrativeScript}.\n` +
  `INVIOLABLE RULE: the prose words are canon and must NOT change. Reproduce every sentence WORD FOR WORD. You may ONLY add (a) bracketed v3 audio tags and (b) ellipses for pacing. Do not add, cut, reorder, or reword any prose.\n` +
  `Mark up with RESTRAINT to match the book's grounded, weary register (NOT melodrama). Tags affect ~the next 4-5 words: use sparingly, e.g. [quietly], [slowly], [softly], [weary], [flat], [tense], [hesitant]. Read the automated notices flat and administrative. Use ellipses for held pauses (v3 may ignore formal break tags). Preserve scene breaks as lines of ---.\n` +
  `FORMAT: (1) YAML front matter (document_type "narration-script", status "draft", authority "narration", title "${title} (Narration Script)", a one-line summary, tags [narration, book-1, chapter-${num}, performance-script], related ["./chapter-${num}-${slug}.md"], source_documents ["${manuscript}"]); (2) a "## Voice Direction" section of overall direction (not spoken); (3) a "## Performance Script" section with the tagged prose (the only part read aloud).\n` +
  `VERIFY: stripping your tags/ellipses leaves words identical to the manuscript; ZERO em dashes; no forbidden reveal introduced. Report word-for-word fidelity, approx tag count, and any judgment calls. Do NOT generate audio. Do not write memories.`,
  { label: `ch${num}:narration-script`, phase: 'Narration Script', schema: REPORT }
)

return {
  chapter: { number: ch.number, slug, title },
  files: { manuscript, critique, blueprint, pack, narrativeScript },
  prep, draft, critique: crit, adjudicate: adj, narrationScript: narr,
  next: `Review ${manuscript} and approve it (set status approved-canon, update docs/60-continuity) per Decision 046. ` +
        `Review ${narrativeScript}, then generate audio on your go: python3 scripts/narrate-chapter.py ${narrativeScript}`,
}
