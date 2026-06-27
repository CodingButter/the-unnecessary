export const meta = {
  name: 'write-chapter',
  description: 'Reusable chapter authorship pipeline for the novel The Unnecessary (Decisions 046 and 048): build the context pack, Opus drafts, Gemini critiques, Opus adjudicates, then a 3-part narration-script pass (Opus directs, Gemini critiques the performance, Opus revises). Parameterized per chapter via args {number, slug, title}. Leaves the chapter as a draft for the author to approve; audio is generated separately.',
  phases: [
    { title: 'Prep', detail: 'Build the chapter context pack from its per-chapter manifest' },
    { title: 'Draft', detail: 'Opus drafts the chapter from the blueprint and pack (canon-safe, on-voice)' },
    { title: 'Critique', detail: 'Gemini (gemini-2.5-pro) critiques the draft against the project rules' },
    { title: 'Adjudicate', detail: 'Opus applies the notes it agrees with and logs accept/reject for each' },
    { title: 'Narration Script', detail: 'Opus directs a v3 performance script, Gemini critiques it, Opus revises (3-part)' },
  ],
}

// ---- Parameters (passed as Workflow args: {number, slug, title}) ----
const NOVEL = '/home/codingbutter/Novel'
let ch = args || {}
if (typeof ch === 'string') { try { ch = JSON.parse(ch) } catch (e) { ch = {} } }
if (ch.number === undefined || ch.number === null || !ch.slug) {
  throw new Error('write-chapter requires args {number, slug, title}, for example {"number":2,"slug":"the-last-supported-day","title":"The Last Supported Day"}')
}
const num = String(ch.number).padStart(2, '0')
const slug = ch.slug
const title = ch.title || ('Chapter ' + ch.number)
const stopAfter = ch.stopAfter || null   // 'adjudicate' to stop before the narration phase

const bpDir = `docs/40-blueprints/book-1/chapter-${num}-${slug}`
const manifest = `${bpDir}/context-manifest.yaml`
const blueprint = `${bpDir}/blueprint.md`
const pack = `.context/chapter-${num}-${slug}.pack.md`
const manuscript = `docs/50-manuscript/book-1/chapter-${num}-${slug}.md`
const critique = `docs/50-manuscript/book-1/chapter-${num}-${slug}.gemini-critique.md`
const narrativeScript = `docs/50-manuscript/book-1/chapter-${num}-${slug}.narrative-script.md`
const narrCritique = `docs/50-manuscript/book-1/chapter-${num}-${slug}.narrative-script.gemini-critique.md`

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

if (stopAfter === 'adjudicate' || stopAfter === 'manuscript') {
  log(`Stopping after Adjudicate (stopAfter="${stopAfter}"); narration script deferred.`)
  return {
    chapter: { number: ch.number, slug, title },
    files: { manuscript, critique, blueprint, pack },
    prep, draft, critique: crit, adjudicate: adj,
    next: `Review and approve ${manuscript} per Decision 046 (set status, update docs/60-continuity). ` +
          `Narration script deferred; generate it separately with the faithful sparse-ellipsis pass when ready.`,
  }
}

// ---- Stage 5: Narration Script — director-grade, 3-part (Opus -> Gemini -> Opus), Decision 048 ----
phase('Narration Script')
const DIRECTOR = `You are an AUDIOBOOK DIRECTOR marking a LIGHT-TOUCH performance script. The voice is the self-hosted voice server's AUDIOBOOK preset by default: steady, weary, controlled. You mark only a FEW register shifts across the whole chapter, never per-phrase emotion.
INVIOLABLE RULE: the prose WORDS are canon. Reproduce every sentence WORD FOR WORD; add ONLY bracketed register tags and scene-break lines (---). Never reword and never re-punctuate the prose.
FOUR REGISTERS, MARKED SPARINGLY: tag a register only where it GENUINELY shifts, one tag per block, never repeated every few words (redundant re-tagging is a defect and the voice server coalesces by register anyway). The registers are: default BASE, the weary controlled narration voice (use no tag, or [measured]); [flat] for automated corporate notices, machine-cold, where the calm is the threat; [tense] for strained dialogue over a failing or tense link; [grave] or [slowly] for the deliberate heavy landings and the chapter's final line. Most of the chapter is untagged BASE.
ELLIPSES: do NOT sprinkle ellipses. On the voice server they cause garble and runaway multi-second pauses. Use at most one or two in the entire chapter, only for a genuine held beat, and always placed AFTER existing punctuation. Never write ",...". Trust the prose's own commas and periods plus the steady voice to carry the line-level rhythm; the tags and ordinary punctuation do the rest. Grounded and austere throughout, never theatrical.`

const narrWrite = await agent(
  `${DIRECTOR}\n\nREAD the final prose at ${NOVEL}/${manuscript} (prose body only; ignore the YAML front matter and the "## Adjudication Log"). WRITE ${NOVEL}/${narrativeScript} with exactly: (1) YAML front matter (document_type "narration-script", status "draft", authority "narration", title "${title} (Narration Script)", a one-line summary, tags [narration, book-1, chapter-${num}, performance-script], related ["./chapter-${num}-${slug}.md"], source_documents ["${manuscript}"]); (2) a DETAILED "## Voice Direction" section (overall direction, per-register approach, pacing philosophy, the intensity arc and the two peaks; not spoken); (3) a "## Performance Script" section that OPENS with a spoken chapter-title line (the chapter number spelled as a word, for example "[measured] Chapter Two. ... ${title}.") and then the prose densely and purposefully directed with audio tags and ellipses, scene breaks as lines of ---.\n` +
  `VERIFY: stripping every tag and ellipsis leaves words IDENTICAL to the manuscript prose (run a token diff); ZERO em dashes; no forbidden reveal. Report word-for-word fidelity (with your diff method), approximate tag count, and your main directorial choices per register. Do not write memories.`,
  { label: `ch${num}:narr-write`, phase: 'Narration Script', schema: REPORT }
)

const narrCrit = await agent(
  `Run EXACTLY this command from ${NOVEL} and report the result:\n` +
  `  python3 scripts/gemini-critique.py ${narrativeScript} --mode narration --reference ${manuscript} --out ${narrCritique}\n` +
  `This sends the narration script to gemini-2.5-pro acting as an audiobook director, judging fidelity to the prose, direction density, register distinction, pacing, v3 tag craft, and tone fit. The critique lands in ${narrCritique} (a SEPARATE file). After it succeeds, READ ${narrCritique} and summarize the key suggestions grouped by severity, with a total count. If the command fails, report the exact error and do not invent a critique.`,
  { label: `ch${num}:narr-critique`, phase: 'Narration Script', effort: 'low', schema: REPORT }
)

const narrFix = await agent(
  `${DIRECTOR}\n\nYou are the director adjudicating an editor's notes on YOUR narration script. READ ${NOVEL}/${narrativeScript} and the critique ${NOVEL}/${narrCritique}.\n` +
  `For EACH suggestion decide ACCEPT or REJECT and apply accepted changes directly to ${narrativeScript} (still adding ONLY tags and ellipses; never change a prose word). Reject anything that would tip into melodrama or contradict the book's register.\n` +
  `Append a "## Narration Adjudication Log" section at the END of the file listing each note with your decision and a one-line reason.\n` +
  `VERIFY again: stripping tags/ellipses leaves words identical to ${manuscript}; ZERO em dashes; no forbidden reveal. Report accepted/rejected counts and the final tag count. Do not write memories.`,
  { label: `ch${num}:narr-fix`, phase: 'Narration Script', schema: REPORT }
)

return {
  chapter: { number: ch.number, slug, title },
  files: { manuscript, critique, blueprint, pack, narrativeScript, narrCritique },
  prep, draft, critique: crit, adjudicate: adj,
  narration: { write: narrWrite, critique: narrCrit, fix: narrFix },
  next: `Review ${manuscript} and approve it (set status approved-canon, update docs/60-continuity) per Decision 046. ` +
        `Review ${narrativeScript}, then generate audio on your go: python3 scripts/narrate-chapter.py ${narrativeScript}`,
}
