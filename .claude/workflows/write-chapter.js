export const meta = {
  name: 'write-chapter',
  description: 'Full chapter authorship pipeline for the novel The Unnecessary: build the context pack, provision missing referenced canon entities, Opus drafts, the full review crew runs a parallel gauntlet (prose-critic, focus-reviewer, continuity-auditor, echo-auditor, clarity-auditor, logic-auditor + the Gemini cross-model lens), the adjudicator decides accept/reject on every finding and applies the accepted fixes, the entity-extractor mines the draft for new canon (backfilled PROPOSED, not locked), then a 3-part narration-script pass (Opus directs, Gemini critiques the performance, Opus revises). Parameterized per chapter via args {number, slug, title}. Leaves the chapter as a draft for the author to approve; audio is generated separately.',
  phases: [
    { title: 'Prep', detail: 'Build the chapter context pack from its per-chapter manifest' },
    { title: 'Provision', detail: 'Birth any blueprint-referenced canon entity whose file does not exist yet (entity-author, one per missing entity, in parallel) so both references exist before drafting (spec section 8)' },
    { title: 'Draft', detail: 'chapter-drafter writes the chapter from the blueprint and pack (canon-safe, on-voice)' },
    { title: 'Gauntlet', detail: 'Full review crew in parallel: prose-critic, focus-reviewer, continuity-auditor, echo-auditor, clarity-auditor, logic-auditor, plus the Gemini cross-model critique. A barrier: all findings collected before adjudication' },
    { title: 'Adjudicate', detail: 'adjudicator decides accept/reject on every gauntlet finding, applies the accepted fixes to the manuscript prose, and logs each decision' },
    { title: 'Extract', detail: 'entity-extractor mines the drafted prose for new canon entities + timeline events (PROPOSED, since the chapter is still draft), then entity-author births any new entity files (spec sections 10a + 14)' },
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
const stopAfter = ch.stopAfter || null   // 'adjudicate' (stop before Extract+narration) or 'extract' (stop before narration)
const bookN = ch.book || 1               // paths are book-1 scoped; the lock-source tag uses this
const proposedBy = `b${bookN}-ch${ch.number}` // §14 lock source stamp for draft-sourced facts (e.g. b1-ch2)

const bpDir = `docs/40-blueprints/book-1/chapter-${num}-${slug}`
const manifest = `${bpDir}/context-manifest.yaml`
const blueprint = `${bpDir}/blueprint.md`
const chapDir = `docs/50-manuscript/book-1/chapter-${num}-${slug}`
const pack = `.context/chapter-${num}-${slug}.pack.md`
const manuscript = `${chapDir}/chapter-${num}-${slug}.md`
const critique = `${chapDir}/chapter-${num}-${slug}.gemini-critique.md`
const narrativeScript = `${chapDir}/chapter-${num}-${slug}.narrative-script.md`
const narrCritique = `${chapDir}/chapter-${num}-${slug}.narrative-script.gemini-critique.md`

const REPORT = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    summary: { type: 'string' },
    details: { type: 'string' },
  },
  required: ['ok', 'summary'],
}

// Provision scout output: the blueprint's referenced entities and whether each canon file already exists.
const REFS_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['entities'],
  properties: { entities: { type: 'array', items: {
    type: 'object', additionalProperties: false,
    properties: {
      ref: { type: 'string' },            // blueprint reference id (e.g. 412-perry/kitchen) or character name
      intended_path: { type: 'string' },  // where the canon file belongs / lives
      entity_type: { type: 'string' },    // character | city | district | building | room | object | street-segment | ...
      parent: { type: 'string' },         // containment parent id, or a character's residence anchor; '' if root
      door: { type: 'string' },           // which of the three doors (§3) it crosses
      focus: { type: 'string' },          // blueprint focus level: blur | sketch | sharp | crisp
      exists: { type: 'boolean' },        // does the canon file already exist on disk
      why: { type: 'string' },            // one-line note
    },
    required: ['ref', 'intended_path', 'entity_type', 'exists', 'why'],
  } } },
}

// Uniform structured findings every gauntlet lens returns, so the adjudicator can rule on a single bundle.
const FINDINGS = {
  type: 'object', additionalProperties: false,
  required: ['verdict', 'findings'],
  properties: {
    verdict: { type: 'string' },          // the lens's own one-line verdict (ship/revise, PASS/FLAGS, CLEAR/AMBIGUOUS, fresh/echoes-flagged, FOCUS n hit/...)
    findings: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: {
        severity: { type: 'string' },     // blocker|major|minor|nit, or high|medium|low — the lens's own scale
        kind: { type: 'string' },         // the lens-specific class (dimension / FABRICATION|CONTRADICTION / family / mode A|B + MOTIF|SELF-ECHO|QUESTION / FRICTION|LOST|... / entity name)
        where: { type: 'string' },        // file:line or paragraph anchor + short quote (BOTH beats when a finding spans two)
        problem: { type: 'string' },      // what is wrong / why it conflicts / what does not add up
        fix: { type: 'string' },          // direction of a fix only — never an applied change
        out_of_scope: { type: 'boolean' },// true for one-line routed pointers outside this lens's lane
      },
      required: ['severity', 'kind', 'where', 'problem'],
    } },
    summary: { type: 'string' },
  },
}

// entity-extractor output: door-crossing nouns to construct + timeline backfills it recorded.
const EXTRACT = {
  type: 'object', additionalProperties: false,
  required: ['files_needed', 'backfilled'],
  properties: {
    files_needed: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: {
        path: { type: 'string' },         // intended canon file path for entity-author to construct
        entity_type: { type: 'string' },
        parent: { type: 'string' },       // containment parent, or a character's residence anchor
        door: { type: 'string' },         // which of the three doors it crossed
        why: { type: 'string' },          // one-line why, including any dated fact to seed (PROPOSED)
      },
      required: ['path', 'entity_type', 'why'],
    } },
    backfilled: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: { entity: { type: 'string' }, date: { type: 'string' }, fact: { type: 'string' }, lock: { type: 'string' } },
      required: ['entity', 'fact'],
    } },
    conflicts: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: { what: { type: 'string' }, detail: { type: 'string' } }, required: ['what'],
    } },
    summary: { type: 'string' },
  },
}

// Resilience: a single agent() call THROWS on retry-cap / API error / dropped connection, which would
// abort the whole pipeline. Wrap the lone (non-parallel) calls so a transient drop retries instead of
// losing the run; on a real result it returns immediately, so behavior is unchanged on success.
async function tryAgent(make, tries) { tries = tries || 3; let last; for (let i = 0; i < tries; i++) { try { const r = await make(); if (r) return r; last = new Error('empty result'); } catch (e) { last = e; log('retry ' + (i + 1) + '/' + tries + ': ' + String(e).slice(0, 140)); } } throw last; }

// House rules shared by the creative (Opus) stages.
const RULES = `This is the literary near-future novel "The Unnecessary". Authoritative grounding for THIS chapter is the context pack at ${NOVEL}/${pack} (canon, the Style Guide, character profiles, continuity, the project rules in CLAUDE.md) and the approved blueprint at ${NOVEL}/${blueprint} (the scene-by-scene plan). Defer to them; the blueprint provides every per-chapter specific (viewpoint, date, scenes, beats, ending).
HOUSE STYLE: grounded, restrained, serious, close-third on a single viewpoint per chapter, past tense, free indirect, subtext over explanation, no cyberpunk cliches, quiet dread that accumulates beneath a competent surface. NO EM DASHES anywhere (verify with grep before finishing).
CANON SAFETY: hold the chapter's single viewpoint; the reader knows only what the viewpoint character perceives. Do not expose future reveals, do not give any AI or system unestablished capabilities, keep each technology within its canonical failure modes, and respect the timeline's event order. Treat the blueprint as an approved plan; do not contradict it.`

// ---- Stage 1: Prep (build the context pack) ----
phase('Prep')
log(`write-chapter: chapter ${num} "${title}" (slug ${slug})`)
const prep = await tryAgent(() => agent(
  `Run EXACTLY this command from ${NOVEL} and report the result:\n` +
  `  python3 scripts/build-context-pack.py ${manifest}\n` +
  `This builds the Chapter ${ch.number} context pack at ${pack}. Confirm the pack file exists afterward and report its approximate token estimate. ` +
  `If the command fails (for example the per-chapter manifest ${manifest} or the blueprint ${blueprint} does not exist), STOP and report the exact error: the precondition is that the chapter's blueprint and context-manifest already exist.`,
  { label: `ch${num}:prep`, phase: 'Prep', effort: 'low', schema: REPORT }
))
if (prep && prep.ok === false) {
  log('Prep failed; halting before drafting. Fix the precondition (blueprint + manifest) and rerun.')
  return { halted: 'prep', prep }
}

// ---- Stage 2: Provision (just-in-time birth of referenced entities, spec §8) ----
// "Make sure both references exist before drafting": scout the blueprint's referenced entities, then
// birth (in parallel) any whose canon file does not exist yet. Grounded ONLY in established canon — a stub
// by default (no prose exists yet to source from), deeper only where the bibles already support it.
phase('Provision')
const scout = await tryAgent(() => agent(
  `You are the canon-scout. Read spec §8 (blueprint binding / just-in-time birth) and §3 (the three doors) of ${NOVEL}/docs/00-governance/entity-spec.md, then read the chapter ${ch.number} blueprint at ${NOVEL}/${blueprint}.\n` +
  `List every entity the blueprint REFERENCES per §8 — from its "## Focus" section AND from each scene's "references:" block (entity + focus). If the blueprint predates structured "references:" blocks, infer the referenced entities from the Focus section and the scene descriptions.\n` +
  `For EACH referenced entity return: ref (the blueprint id or character name); intended_path (the canon FILE path where it belongs — spatial entities ride the folder tree under docs/20-canon/world/locations/greater-detroit/... with containment on the CHILD; characters live under docs/20-canon/characters/profiles/... located by a residence edge); entity_type; parent (its containment parent id, or a character's residence anchor; '' if root); door (which of the three §3 doors it crosses); focus (the blueprint's focus level for it); and exists — CHECK ON DISK with Glob/Grep whether that canon file already EXISTS (true) or must be born (false).\n` +
  `Read-only inventory: do NOT create or edit any file. Return per schema.`,
  { label: `ch${num}:provision-scout`, phase: 'Provision', schema: REFS_SCHEMA }
))
const refs = (scout && scout.entities) || []
const toBirth = refs.filter(e => e && e.exists === false && e.intended_path)
log(`provision: blueprint references ${refs.length} entit${refs.length === 1 ? 'y' : 'ies'}; ${toBirth.length} missing — birthing before draft`)
let provisioned = []
if (toBirth.length) {
  provisioned = await parallel(toBirth.map(e => () => agent(
    `You are the entity-author. Construct (or extend, if a partial file exists) the ONE canon entity file the chapter ${ch.number} blueprint references but which does not exist yet: intended path ${NOVEL}/${e.intended_path}.\n` +
    `entity_type ${e.entity_type}; containment parent / residence anchor: ${e.parent || '(root — none)'}; door crossed (§3): ${e.door || '(see blueprint)'}; blueprint focus: ${e.focus || '(see blueprint)'}. The blueprint is ${NOVEL}/${blueprint}; the project's entity spec is ${NOVEL}/docs/00-governance/entity-spec.md.\n` +
    `This is PRE-DRAFT: no chapter prose exists yet, so a STUB is the right default (frontmatter + parent + a one-line description), going deeper ONLY where established canon already supports it. Ground every fact ONLY in established canon (the bibles, plot, the Decision Log). Per §14 lock state: bible-established facts are locked/as-is; anything you deduce to furnish the file is \`open\` — there is NO draft prose yet, so nothing here is \`proposed\`.\n` +
    `Place it by containment (parent on the CHILD, never edit an ancestor). Self-validate against scripts/validate-metadata.py. Report the absolute path, created vs extended, entity_type, parent, the door that justified it, edges + any timeline, validation status, and any canon-silence or conflict flagged (never resolved).`,
    { agentType: 'entity-author', label: `ch${num}:provision:${(e.ref || e.intended_path).slice(-40)}`, phase: 'Provision', schema: REPORT }
  )))
} else {
  log('provision: all referenced entities already have canon files; nothing to birth')
}

// ---- Stage 3: Draft (chapter-drafter) ----
phase('Draft')
const draft = await tryAgent(() => agent(
  // Role (prose writer, house style, viewpoint, canon-safety, reveal discipline, no-em-dash)
  // lives in the chapter-drafter crew file; this prompt passes only the per-chapter task.
  `Authoritative grounding for THIS chapter is the context pack at ${NOVEL}/${pack} and the approved blueprint at ${NOVEL}/${blueprint}; defer to them (the blueprint provides every per-chapter specific: viewpoint, date, scenes, beats, ending). Read the pack and the blueprint in full, then WRITE the complete prose of "${title}" (chapter ${ch.number}) to a NEW file ${NOVEL}/${manuscript}.\n` +
  `Execute the blueprint scene by scene. Add YAML front matter: title "${title}", document_type "manuscript-chapter", status "draft", authority "manuscript", a one-sentence summary, tags (manuscript, book-1, chapter-${num}), related links to ../../../40-blueprints/book-1/chapter-${num}-${slug}/blueprint.md and ../../../30-plot/book-1/chapters/chapter-${num}.md, source_documents the blueprint path.\n` +
  `CHARACTER FOCUS: load the blueprint's "## Character Focus" targets and, for every focused character, pull their "Voice and Speech" section plus their heritage signals (accent under "Movement and voice", "Birthplace" and "Faction or class" in Basic Information, and "Early Life" under History and Background) from their profile in the pack. Render each focused character in that specific voice and bring them to their intended focus level (blur, sketch, sharp, or crisp) along the named axes (physical, emotional, interior). Deliver it image over inventory, never a trait list; respect their reveal tags; and actively write the particularity IN, so no character defaults to the unmarked cultural norm. Do not pad a scene to hit a level: if a target is not motivated by the scene, hold to the lower level.\n` +
  `Write the best chapter you can: precise, restrained, alive on the page. When done, grep the file to confirm ZERO em dashes, confirm the ending matches the blueprint, and confirm no forbidden reveal leaked. Report word count and those confirmations. Do not write memories.`,
  { agentType: 'chapter-drafter', label: `ch${num}:draft`, phase: 'Draft', schema: REPORT }
))

// ---- Stage 4: Gauntlet (full review crew in parallel + the Gemini cross-model lens) ----
// Replaces the lone Gemini critique. Six crew lenses (each a read-only specialist returning structured
// findings) PLUS the Gemini cross-model critique (an independent model that has caught issues the crew
// missed) all run concurrently. This is a BARRIER: every finding is collected before adjudication.
phase('Gauntlet')
const lenses = [
  { key: 'prose', agentType: 'prose-critic',
    prompt:
      `Adversarial CRAFT pass on the drafted chapter (voice, pacing, sentence-level clarity, cliche, show-don't-tell, dialogue distinctness, sensory grounding). Draft: ${NOVEL}/${manuscript}. Blueprint: ${NOVEL}/${blueprint}. Read both in full and judge against the Style Guide under ${NOVEL}/docs/10-vision/style/**.\n` +
      `Return per schema: verdict = ship | revise | major-rework; findings each with severity (blocker|major|minor|nit), kind = the craft dimension, where = exact quote + ≈anchor, problem = what's wrong, fix = direction only. Set out_of_scope:true on any one-line pointer to a suspected continuity/canon issue or a suspected reader-comprehension failure (route, do not adjudicate).` },
  { key: 'focus', agentType: 'focus-reviewer',
    prompt:
      `Audit the draft against the blueprint's "## Focus" contract. Blueprint: ${NOVEL}/${blueprint}. Draft: ${NOVEL}/${manuscript}. For every focused entity judge: did it land its intended Level and surface its named Revelation axes as IMAGE not inventory, with no padding, and is each named axis renderable given the bible's reveal tag on that axis (entity-spec §8/§11).\n` +
      `Return per schema: verdict = "FOCUS n hit / n partial / n miss"; one finding per partial/miss with kind = entity name, where = locator/short quote, problem = level/axis result, fix = one minimal direction. A blueprint-vs-bible focus conflict goes in a finding with out_of_scope:true (state it, do not resolve). An off-axis gated leak: out_of_scope:true, routed to continuity-auditor.` },
  { key: 'continuity', agentType: 'continuity-auditor',
    prompt:
      `Adversarially audit the draft for FABRICATION and CONTRADICTION on BOTH passes: chapter-vs-canon (external — bibles, prior approved chapters, the Master Timeline, continuity baselines) AND chapter-vs-itself (internal state ledger: object-state, presence/possession, character-state, sequence/time). Draft: ${NOVEL}/${manuscript}. Binding blueprint: ${NOVEL}/${blueprint}. Resolve each time-varying fact as-of the scene's in-world ISO date (entity-spec §9); honor reveal gates (§11). Verify by reading/grepping, never memory.\n` +
      `Return per schema: verdict = PASS | FLAGS; findings each with kind = class + subtype (and external/internal), where = file:line for BOTH the establishing and conflicting beats, problem = the claim + why it conflicts or is unsupported + the controlling authority, fix = recommended resolution (never applied). Route raw physical impossibility to logic-auditor with out_of_scope:true.` },
  { key: 'echo', agentType: 'echo-auditor',
    prompt:
      `Cross-chapter FRESHNESS pass: audit this draft against every approved/prior chapter that PRECEDES it (Glob the manuscript tree to find them). Draft: ${NOVEL}/${manuscript}. If this is Chapter 1 (no predecessors exist), return verdict "fresh" with no findings. Distinguish a deliberate MOTIF (varies/escalates/recontextualizes — keep) from lazy SELF-ECHO / concept re-explanation (mode A / mode B — flag); when intent is genuinely ambiguous, flag it as a QUESTION, not a verdict. Cross-check setups-and-payoffs for sanctioned callbacks.\n` +
      `Return per schema: verdict = fresh | echoes-flagged; findings each with kind = "mode A|B + MOTIF|SELF-ECHO|QUESTION", severity (blocker|major|minor|nit|question), where = BOTH the prior source file:line and the new instance ≈anchor with quotes, problem = why it does/doesn't earn the return, fix = cut | vary | assume-and-reference.` },
  { key: 'clarity', agentType: 'clarity-auditor',
    prompt:
      `First-pass LEGIBILITY pass on the draft. NOTE: your full contract consumes independent lay-reader retellings (the separate interpretation-audit pipeline produces those for the deep two-pass audit). In THIS gauntlet you are NOT handed retellings, so do a single-read first-pass friction PREDICTION and mark any call you cannot ground in real reader evidence as UNVERIFIED. Draft: ${NOVEL}/${manuscript}. Blueprint: ${NOVEL}/${blueprint} — the intended takeaway is ONLY Narrative Purpose / Chapter Promise / Reader Information; everything under "Information Deliberately Withheld" (and any reveal tag) is sacred and must NOT be flagged.\n` +
      `Predict, against the 8th-grade first-pass floor: FRICTION (a sentence that forces a re-read), LOST (an untrackable pronoun/speaker/cause), CONTRADICTION (a beat that reads two incompatible ways), MISSED-POINT (the beat's intended narrative takeaway likely won't land). Depth is not a defect; deliberate mystery is not a finding. Return per schema: verdict = CLEAR | AMBIGUOUS; findings each with kind, severity (low|medium|high), where = paragraph anchor, problem = the friction + the blueprint meaning at risk. Recommend the full interpretation-audit in summary for the empirical pass.` },
  { key: 'logic', agentType: 'logic-auditor',
    prompt:
      `Pressure-test the draft for real-world LOGIC, LOGISTICS, and PLAUSIBILITY — things that do not ADD UP even when they break no canon fact. Draft: ${NOVEL}/${manuscript}. Blueprint (scene dates + clock): ${NOVEL}/${blueprint}. Use the Technology Rules, medicine canon, and Master Timeline as a MODEL of how the world's devices/bodies/clock work (a plausibility anchor), not a value-checklist. Establish each scene's clock; build a feasibility ledger.\n` +
      `Test all four families: TIME-OF-DAY vs ACTIVITY, SPATIAL/OBJECT LOGISTICS, MEDICAL/TECHNICAL mechanism, CAUSE-EFFECT/SEQUENCE. Return per schema: verdict = PASS | FLAGS; findings each with kind = family, severity (blocker|major|minor|nit), where = file:line (BOTH beats when it spans two), problem = the physical/temporal/causal reasoning + the mechanism anchor (path:line) or "real-world physics, canon silent", fix = direction only. When a symptom is also a canon-value mismatch, mark it out_of_scope and note the continuity overlap; keep your finding on the plausibility angle.` },
]

// The Gemini cross-model critique (existing script): one additional independent lens, kept verbatim.
const geminiLensPrompt =
  `Run EXACTLY this command from ${NOVEL} and report the result:\n` +
  `  python3 scripts/gemini-critique.py ${manuscript} --pack ${pack} --blueprint ${blueprint} --out ${critique} --manifest ${manifest}\n` +
  `(The --manifest flag rebuilds the pack first so the critique can never run against a stale snapshot.)\n` +
  `This sends the drafted chapter to gemini-2.5-pro for an editorial critique that lands in ${critique} (a SEPARATE file; the prose is not touched). The critique now also applies a FOCUS-DELIVERY lens: for each character named in the blueprint's "## Character Focus", it judges whether the draft delivered that character's revelation target (physical, emotional, interior) to the intended focus level and whether they read in their specific voice and heritage rather than the cultural default. This is a judgment check alongside the existing consistency and contradiction critique. After it succeeds, READ ${critique} and return a concise summary of the highest-value suggestions grouped by severity, plus the total number of suggestions; surface any focus-delivery shortfalls as their own group, naming the character and the axis that fell short. If the command fails, report the exact error and do not invent a critique.`

const gauntletThunks = [
  ...lenses.map(L => () => agent(L.prompt, { agentType: L.agentType, label: `ch${num}:gauntlet:${L.key}`, phase: 'Gauntlet', schema: FINDINGS })),
  () => agent(geminiLensPrompt, { label: `ch${num}:gauntlet:gemini`, phase: 'Gauntlet', effort: 'low', schema: REPORT }),
]
let gauntletRuns = await parallel(gauntletThunks)
// Retry-sweep: a schema-retry-cap / dropped lens comes back null; re-run just those once before adjudication
// so a transient drop becomes a recovered review instead of a silently-missing lens. One sweep only.
const gMissing = gauntletRuns.map((r, k) => (r ? -1 : k)).filter(k => k >= 0)
if (gMissing.length) {
  log(`gauntlet retry-sweep: re-running ${gMissing.length} failed lens(es)`)
  const gRe = await parallel(gMissing.map(k => gauntletThunks[k]))
  gMissing.forEach((k, j) => { if (gRe[j]) gauntletRuns[k] = gRe[j] })
}
// Assemble the crew findings bundle for the adjudicator (the Gemini lens is handed via its file path).
const gauntletFindings = {}
lenses.forEach((L, i) => { gauntletFindings[L.key] = gauntletRuns[i] || { verdict: '(lens failed)', findings: [], summary: 'lens returned no result' } })
const geminiRun = gauntletRuns[lenses.length] || null
const totalFindings = lenses.reduce((s, L) => s + ((gauntletFindings[L.key].findings || []).length), 0)
log(`gauntlet: collected ${totalFindings} crew finding(s) across ${lenses.length} lenses + Gemini critique at ${critique}`)

// ---- Stage 5: Adjudicate (the adjudicator agent decides + applies) ----
phase('Adjudicate')
const adj = await tryAgent(() => agent(
  `${RULES}\n\nYou are the adjudicator. READ the FULL drafted chapter ${NOVEL}/${manuscript} and the approved blueprint ${NOVEL}/${blueprint} (its "## Focus" section governs focus/reveal intent) before ruling on anything.\n` +
  `Here are the GAUNTLET findings from the review crew (prose-critic, focus-reviewer, continuity-auditor, echo-auditor, clarity-auditor, logic-auditor), as structured JSON:\n${JSON.stringify(gauntletFindings)}\n\n` +
  `ALSO read the Gemini cross-model critique at ${NOVEL}/${critique} and treat each of its suggestions as additional findings. (echo-auditor and logic-auditor are extra lenses beyond your named four; rule on their findings the same way.)\n` +
  `For EVERY finding decide ACCEPT or REJECT with a one-line reason grounded in the draft or a controlling authority (Style Guide for craft; the bibles/approved manuscript for facts; the blueprint for focus + reveal timing). Reject anything that fights an authority, leaks a gated reveal, breaks viewpoint, or is out of scope. APPLY every accepted ruling as a surgical Edit to ${manuscript} ONLY — never touch the narration / performance script (it is the audiobook-director's derived artifact, regenerated from your corrected manuscript). If an accepted finding needs FRESH scene prose (more than a local repair), ACCEPT it but ROUTE it back to chapter-drafter by name; do not draft it yourself.\n` +
  `Append a "## Adjudication Log" section at the END of ${manuscript} (after the prose) with one row per finding: [source lens] severity — short claim -> ACCEPT/REJECT, one-line reason. Keep the chapter status "draft" (the author approves separately).\n` +
  `Before finishing: grep to confirm STILL zero em dashes, viewpoint and the POV character's knowledge state are intact, and no forbidden reveal was introduced by any accepted edit. Report: number accepted, number rejected, items routed back to chapter-drafter, final word count, any unresolved canon conflict (flagged, never resolved), and the confirmations. Do not write memories.`,
  { agentType: 'adjudicator', label: `ch${num}:adjudicate`, phase: 'Adjudicate', schema: REPORT }
))

if (stopAfter === 'adjudicate' || stopAfter === 'manuscript') {
  log(`Stopping after Adjudicate (stopAfter="${stopAfter}"); Extract + narration script deferred.`)
  return {
    chapter: { number: ch.number, slug, title },
    files: { manuscript, critique, blueprint, pack },
    prep, provision: provisioned, draft, gauntlet: gauntletFindings, gemini: geminiRun, adjudicate: adj,
    next: `Review and approve ${manuscript} per Decision 046 (set status, update docs/60-continuity). ` +
          `Entity extraction (proposed-canon backfill) and the narration script were deferred; rerun without stopAfter, or with stopAfter="extract", when ready.`,
  }
}

// ---- Stage 6: Extract (prose as a source — backfill PROPOSED canon, spec §10a + §14) ----
// A freshly-drafted chapter is DRAFT, not approved: every fact/timeline entry mined from it is lock state
// PROPOSED (by: bN-chN), NOT locked. It hardens to locked only when the chapter is approved (§14). Extract
// is non-gating enrichment that sits before narration, so a hard failure here is logged and the pipeline
// continues to the narration phase rather than discarding the drafted + adjudicated work.
phase('Extract')
let extract = null
let born = []
try {
  extract = await tryAgent(() => agent(
    `You are the entity-extractor. Mine the just-DRAFTED chapter prose for new canon along the two channels of spec §10a. Drafted prose: ${NOVEL}/${manuscript} (read the STORY PROSE only — IGNORE the YAML front matter and the "## Adjudication Log"). The scene anchor date(s) come from the blueprint ${NOVEL}/${blueprint} (ISO 8601). The governing spec is ${NOVEL}/docs/00-governance/entity-spec.md (§3 the three doors, §9 timelines, §10a backfill, §14 lock state).\n` +
    `Channel (a) DETECT door-crossing nouns (§3): for each noun that crosses a door, EMIT a file-needed flag with the intended canon path, entity_type, parent (containment parent, or residence anchor for a character), which door, and a one-line why (fold any dated fact to seed into the why). Do NOT construct files yourself.\n` +
    `Channel (b) BACKFILL timeline events into ALREADY-EXISTING entity files only, keyed to the scene's in-world ISO date (never chapter number).\n` +
    `CRITICAL — lock state: this is DRAFT, not approved, prose. So EVERY fact / edge / timeline entry you record from this chapter's prose is lock state PROPOSED, stamped \`by: ${proposedBy}\`, per §14 — NOT locked. Use the §14 \`locks:\` dotted-path encoding (e.g. \`timeline.3: { state: proposed, by: ${proposedBy} }\`), never \`locked\`. Reconcile each claim against the entity's timeline and the Master Timeline: consistent -> do nothing; new -> backfill PROPOSED; contradiction with an already-LOCKED item (a bible fact or earlier approved chapter) -> FLAG it, do NOT record it, never silently resolve.\n` +
    `Return per schema: files_needed (for entity-author to construct), backfilled (entity, ISO date, fact, lock=proposed), conflicts (flagged, unresolved), and a summary.`,
    { agentType: 'entity-extractor', label: `ch${num}:extract`, phase: 'Extract', schema: EXTRACT }
  ))
  const filesNeeded = ((extract && extract.files_needed) || []).filter(f => f && f.path)
  log(`extract: ${filesNeeded.length} new entity file(s) flagged; ${((extract && extract.backfilled) || []).length} timeline backfill(s) (proposed); ${((extract && extract.conflicts) || []).length} conflict(s) flagged`)
  if (filesNeeded.length) {
    born = await parallel(filesNeeded.map(f => () => agent(
      `You are the entity-author. Construct the ONE new canon entity file the entity-extractor flagged from the drafted chapter ${ch.number}: intended path ${NOVEL}/${f.path}.\n` +
      `entity_type ${f.entity_type}; containment parent / residence anchor: ${f.parent || '(determine from §3 containment)'}; door crossed (§3): ${f.door || '(see why)'}. Why / seed: ${f.why}. The drafted prose is ${NOVEL}/${manuscript}; the entity spec is ${NOVEL}/docs/00-governance/entity-spec.md.\n` +
      `Ground every fact ONLY in established canon plus this chapter's drafted prose. CRITICAL — lock state (§14): the prose that establishes this entity is a DRAFT (chapter ${ch.number}), so EVERY fact / edge / timeline you record FROM this chapter's prose is lock state PROPOSED, stamped \`by: ${proposedBy}\`, using the §14 \`locks:\` dotted-path encoding ({ state: proposed, by: ${proposedBy} }) — NOT locked. Facts you pull from already-established bible canon keep their locked/established state; pure deductions stay \`open\`.\n` +
      `Place it by containment (parent on the CHILD; never edit an ancestor). Self-validate against scripts/validate-metadata.py. Report the absolute path, created vs extended, entity_type, parent, the door that justified it, edges written, timeline + the lock state of each entry, validation status, and any conflict flagged (never resolved).`,
      { agentType: 'entity-author', label: `ch${num}:extract-birth:${f.path.slice(-40)}`, phase: 'Extract', schema: REPORT }
    )))
  } else {
    log('extract: no new entity files needed; backfills (if any) landed in existing files')
  }
} catch (e) {
  log(`extract: phase failed after retries (${String(e).slice(0, 140)}); continuing to narration — the drafted + adjudicated manuscript is preserved on disk`)
}

if (stopAfter === 'extract') {
  log('Stopping after Extract (stopAfter="extract"); narration script deferred.')
  return {
    chapter: { number: ch.number, slug, title },
    files: { manuscript, critique, blueprint, pack },
    prep, provision: provisioned, draft, gauntlet: gauntletFindings, gemini: geminiRun, adjudicate: adj,
    extract: { report: extract, born },
    next: `Review and approve ${manuscript} per Decision 046; on approval, the proposed entity facts harden to locked (§14). ` +
          `Narration script deferred; generate it separately with the faithful sparse-ellipsis pass when ready.`,
  }
}

// ---- Stage 7: Narration Script — director-grade, 3-part (Opus -> Gemini -> Opus), Decision 048 ----
phase('Narration Script')
const DIRECTOR = `You are an AUDIOBOOK DIRECTOR marking a LIGHT-TOUCH performance script. The voice is the self-hosted voice server's AUDIOBOOK preset by default: steady, weary, controlled. You mark only a FEW register shifts across the whole chapter, never per-phrase emotion.
INVIOLABLE RULE: the prose WORDS are canon. Reproduce every sentence WORD FOR WORD; add ONLY bracketed register tags and scene-break lines (---). Never reword and never re-punctuate the prose.
FOUR REGISTERS, MARKED SPARINGLY: tag a register only where it GENUINELY shifts, one tag per block, never repeated every few words (redundant re-tagging is a defect and the voice server coalesces by register anyway). The registers are: default BASE, the weary controlled narration voice (use no tag, or [measured]); [flat] for automated corporate notices, machine-cold, where the calm is the threat; [tense] for strained dialogue over a failing or tense link; [grave] or [slowly] for the deliberate heavy landings and the chapter's final line. Most of the chapter is untagged BASE.
PACING: mark deliberate pauses where a human reader would actually pause -- for breath, for weight, before a turn, after a landing. Use [beat] for a short breath and [hold] for a heavier, deliberate pause. Place them intentionally and sparingly, NOT at every sentence; the steady voice and ordinary punctuation carry normal rhythm. These markers are how you control pacing now -- the renderer turns each [beat]/[hold] into an exact silence -- so you no longer need ellipses at all.
ELLIPSES: do NOT sprinkle ellipses. On the voice server they cause garble and runaway multi-second pauses. Use at most one or two in the entire chapter, only for a genuine held beat, and always placed AFTER existing punctuation. Never write ",...". Trust the prose's own commas and periods plus the steady voice to carry the line-level rhythm; the tags and ordinary punctuation do the rest. Grounded and austere throughout, never theatrical.`

const narrWrite = await tryAgent(() => agent(
  `${DIRECTOR}\n\nREAD the final prose at ${NOVEL}/${manuscript} (prose body only; ignore the YAML front matter and the "## Adjudication Log"). WRITE ${NOVEL}/${narrativeScript} with exactly: (1) YAML front matter (document_type "narration-script", status "draft", authority "narration", title "${title} (Narration Script)", a one-line summary, tags [narration, book-1, chapter-${num}, performance-script], related ["./chapter-${num}-${slug}.md"], source_documents ["${manuscript}"]); (2) a DETAILED "## Voice Direction" section (overall direction, per-register approach, pacing philosophy, the intensity arc and the two peaks; not spoken); (3) a "## Performance Script" section that OPENS with a spoken chapter-title line (the chapter number spelled as a word, for example "[measured] Chapter Two. ... ${title}.") and then the prose densely and purposefully directed with audio tags and ellipses, scene breaks as lines of ---.\n` +
  `VERIFY: stripping every tag and ellipsis leaves words IDENTICAL to the manuscript prose (run a token diff); ZERO em dashes; no forbidden reveal. Report word-for-word fidelity (with your diff method), approximate tag count, and your main directorial choices per register. Do not write memories.`,
  { label: `ch${num}:narr-write`, phase: 'Narration Script', schema: REPORT }
))

const narrCrit = await tryAgent(() => agent(
  `Run EXACTLY this command from ${NOVEL} and report the result:\n` +
  `  python3 scripts/gemini-critique.py ${narrativeScript} --mode narration --reference ${manuscript} --out ${narrCritique}\n` +
  `This sends the narration script to gemini-2.5-pro acting as an audiobook director, judging fidelity to the prose, direction density, register distinction, pacing, v3 tag craft, and tone fit. The critique lands in ${narrCritique} (a SEPARATE file). After it succeeds, READ ${narrCritique} and summarize the key suggestions grouped by severity, with a total count. If the command fails, report the exact error and do not invent a critique.`,
  { label: `ch${num}:narr-critique`, phase: 'Narration Script', effort: 'low', schema: REPORT }
))

const narrFix = await tryAgent(() => agent(
  `${DIRECTOR}\n\nYou are the director adjudicating an editor's notes on YOUR narration script. READ ${NOVEL}/${narrativeScript} and the critique ${NOVEL}/${narrCritique}.\n` +
  `For EACH suggestion decide ACCEPT or REJECT and apply accepted changes directly to ${narrativeScript} (still adding ONLY tags and ellipses; never change a prose word). Reject anything that would tip into melodrama or contradict the book's register.\n` +
  `Append a "## Narration Adjudication Log" section at the END of the file listing each note with your decision and a one-line reason.\n` +
  `VERIFY again: stripping tags/ellipses leaves words identical to ${manuscript}; ZERO em dashes; no forbidden reveal. Report accepted/rejected counts and the final tag count. Do not write memories.`,
  { label: `ch${num}:narr-fix`, phase: 'Narration Script', schema: REPORT }
))

return {
  chapter: { number: ch.number, slug, title },
  files: { manuscript, critique, blueprint, pack, narrativeScript, narrCritique },
  prep, provision: provisioned, draft,
  gauntlet: gauntletFindings, gemini: geminiRun, adjudicate: adj,
  extract: { report: extract, born },
  narration: { write: narrWrite, critique: narrCrit, fix: narrFix },
  next: `Review ${manuscript} and approve it (set status approved-canon, update docs/60-continuity) per Decision 046 — on approval the proposed entity facts (§14) harden to locked. ` +
        `Review ${narrativeScript}, then generate audio on your go: python3 scripts/narrate-chapter.py ${narrativeScript}`,
}
