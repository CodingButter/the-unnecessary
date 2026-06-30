export const meta = {
  name: 'section-review',
  description: 'Run the developmental-editor on an ASSEMBLED act/section of "The Unnecessary" -- its cadence is section/book-level, NOT per-chapter. The developmental-editor reads the assembled chapters (and their blueprints if present) as one continuous whole and returns a PRIORITIZED DEVELOPMENTAL REVISION LETTER (arc, pacing, structure + chapter ORDER, character-arc motivation across chapters, theme coherence/drift, setup/payoff balance, what to cut/expand/reorder). It DIAGNOSES only; developmental changes are AUTHOR decisions and too large to auto-apply, so the deliverable is the LETTER (plus optional routed flags), written to docs/30-plot/section-reviews/. Manuscripts are never auto-edited. args: {book, label, chapters?} where chapters is an optional list of chapter slugs (default: Glob all chapters in the book\'s manuscript dir).',
  phases: [
    { title: 'Review', detail: 'developmental-editor reads the assembled chapters (+ blueprints if present) and returns a prioritized developmental revision letter on arc, pacing, structure + chapter order, character-arc motivation, theme, and setup/payoff; it DIAGNOSES only and never edits prose' },
    { title: 'Record', detail: 'write the revision letter to docs/30-plot/section-reviews/<book>-<label>.md (create the dir; valid 8-field YAML frontmatter so validators pass); the letter plus optional routed flags is the deliverable -- no manuscript is auto-edited' },
  ],
}

let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
A = A || {}
const BOOK = A.book || 'book-1'
if (!A.label) throw new Error('section-review requires args {book, label} (+ optional chapters[] of chapter slugs)')
const LABEL = String(A.label)
const labelSlug = LABEL.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'section'
const CHAPTERS = Array.isArray(A.chapters) ? A.chapters.filter(Boolean).map(String) : null   // optional explicit chapter slugs; default = Glob all
const NOVEL = '/home/codingbutter/Novel'
const manuscriptDir = `docs/50-manuscript/${BOOK}`
const blueprintDir = `docs/40-blueprints/${BOOK}`
const outDir = 'docs/30-plot/section-reviews'
const outFile = `${outDir}/${BOOK}-${labelSlug}.md`

async function tryAgent(make, tries) { tries = tries || 3; let last; for (let i = 0; i < tries; i++) { try { const r = await make(); if (r) return r; last = new Error('empty result'); } catch (e) { last = e; log('retry ' + (i + 1) + '/' + tries + ': ' + String(e).slice(0, 140)); } } throw last; }

const REPORT = { type: 'object', properties: { ok: { type: 'boolean' }, summary: { type: 'string' }, details: { type: 'string' } }, required: ['ok', 'summary'] }

// Workflow JS has no filesystem access; the chapter set is enumerated by the developmental-editor's own Glob
// tool (the codebase convention for file enumeration -- see the echo-auditor lenses). When `chapters` is
// supplied we constrain it to that explicit, ordered slug list; otherwise the agent globs the whole section.
const chapterScope = CHAPTERS && CHAPTERS.length
  ? `Read ONLY these chapters, in this order: ${CHAPTERS.join(', ')}. Each chapter's prose lives under ${NOVEL}/${manuscriptDir}/<chapter-dir>/<chapter-dir>.md (the directory name embeds the slug, e.g. chapter-01-no-signal); read each chapter's blueprint under ${NOVEL}/${blueprintDir}/<same-dir>/blueprint.md when it exists.`
  : `Glob ALL chapter-* directories under ${NOVEL}/${manuscriptDir}/ and read every chapter's prose (<dir>/<dir>.md) in chapter-number order; for each, read its blueprint under ${NOVEL}/${blueprintDir}/<same-dir>/blueprint.md when present.`

// ---- Review (DIAGNOSE only; developmental-editor is read-only) ----
phase('Review')
log(`section-review: ${BOOK} "${LABEL}" -- ` + (CHAPTERS && CHAPTERS.length ? `${CHAPTERS.length} chapter(s)` : 'all chapters (glob)'))
const letter = await tryAgent(() => agent(
  `You are the developmental-editor performing a SECTION / ACT-LEVEL developmental read of "The Unnecessary". Your cadence is section/book-level, NOT per-chapter: assemble the chapters and read them as one continuous whole. You DIAGNOSE only -- you NEVER edit manuscript prose and you never apply a change.\n` +
  chapterScope + `\n` +
  `Evaluate the ARCHITECTURE of the assembled section and weigh each lens:\n` +
  `- ARC: the dramatic throughline across the section -- does it build, escalate, and turn with intent.\n` +
  `- PACING: sagging middles, rushed turns, scenes that earn their length vs ones that stall or repeat.\n` +
  `- STRUCTURE + chapter ORDER: does the current sequence build correctly, or should chapters be reordered / merged / split.\n` +
  `- CHARACTER-ARC motivation ACROSS chapters: does each arc move on credible, prepared cause (not just plot convenience).\n` +
  `- THEME coherence and drift: is the book's ownership-of-abundance spine consistently in view, or does it wander.\n` +
  `- SETUP / PAYOFF balance: promises planted vs paid; orphaned setups; payoffs that arrive unprepared.\n` +
  `- what to CUT, EXPAND, or REORDER.\n` +
  `Honor reveal gates and viewpoint -- a deliberately withheld reveal is a feature, not a structural gap. Read blueprints as approved PLANS, not as already-established events.\n` +
  `Return per the REPORT schema. ok:true. summary = a one-paragraph state-of-the-section verdict. details = the FULL PRIORITIZED DEVELOPMENTAL REVISION LETTER as markdown: lead with the biggest structural issues, group findings under the lenses above, each item concrete and anchored to chapter(s). END the letter with a "## Routed Flags" section that NAMES an owner for any actionable item WITHOUT applying it -- an item that needs FRESH scene prose -> chapter-drafter (by name); a LOCAL structural fix -> adjudicator (by name). Developmental changes are AUTHOR decisions; do NOT edit any manuscript, blueprint, or canon file.`,
  { schema: REPORT, phase: 'Review', agentType: 'developmental-editor', label: 'section:review:' + labelSlug }
))
const letterBody = (letter && letter.details) || (letter && letter.summary) || '(developmental-editor returned no letter body)'
log(`review: developmental revision letter assembled (${letterBody.length} chars)`)

// ---- Record (persist the letter; manuscripts are NOT touched) ----
// The developmental-editor is read-only (Read/Grep/Glob), so a Write-capable agent persists the letter. The
// full file content is assembled here so the writer reproduces it verbatim -- 8 required frontmatter fields,
// document-relative `related` and repo-root-relative `source_documents` that resolve, so the validators pass.
phase('Record')
const frontmatter =
  `---\n` +
  `title: "Section Review: ${LABEL} (${BOOK})"\n` +
  `document_type: "section-review"\n` +
  `status: "active-plan"\n` +
  `authority: "plot-plan"\n` +
  `summary: "Developmental revision letter for the assembled ${LABEL} of ${BOOK}: arc, pacing, structure and chapter order, character-arc motivation, theme, and setup/payoff, diagnosed by the developmental-editor. Author decisions; not auto-applied."\n` +
  `tags:\n  - plot\n  - section-review\n  - ${BOOK}\n  - ${labelSlug}\n` +
  `related:\n  - "../${BOOK}/index.md"\n  - "../${BOOK}/story-spine.md"\n  - "../${BOOK}/major-beats.md"\n` +
  `source_documents:\n  - "${manuscriptDir}/"\n` +
  `---\n`
const fileContent =
  frontmatter +
  `\n# Section Review: ${LABEL} (${BOOK})\n\n` +
  `> Developmental revision letter (diagnostic). Developmental changes are AUTHOR decisions; nothing here is auto-applied. Produced by the section-review workflow (developmental-editor).\n\n` +
  letterBody + `\n`
const rec = await tryAgent(() => agent(
  `Persist a developmental revision letter for "The Unnecessary" to disk. This is a pure WRITE task -- do NOT edit, draft, or critique anything; do NOT touch any manuscript, blueprint, or canon file.\n` +
  `Create the directory ${NOVEL}/${outDir} if it does not exist, then WRITE the file ${NOVEL}/${outFile} with EXACTLY the content between the <<<BEGIN-FILE>>> and <<<END-FILE>>> markers below -- verbatim, byte-for-byte, including the YAML frontmatter. Do not add, drop, reorder, or reword anything; the markers themselves are NOT part of the file.\n` +
  `<<<BEGIN-FILE>>>\n${fileContent}<<<END-FILE>>>\n` +
  `Then confirm. Report (REPORT schema): ok, summary = the path written + a one-line note that the deliverable is a diagnostic letter (author decides, no manuscript edited), details = the routed-flag owners named in the letter, if any.`,
  { schema: REPORT, phase: 'Record', agentType: 'general-purpose', label: 'section:record:' + labelSlug }
))
log(`record: revision letter written -> ${outFile}`)

return { section: { book: BOOK, label: LABEL }, chapters: CHAPTERS || '(all)', outFile, review: letter, record: rec }
