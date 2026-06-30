export const meta = {
  name: 'narrate-chapter',
  description: 'Produce the PLAIN single-narrator audiobook for an APPROVED chapter: the audiobook-director writes/refreshes the v3-tagged narration performance script, a Gemini narration-critique gate verifies prose-fidelity + v3 tag discipline (ellipses-for-pauses, only tags the renderer honors) and re-rolls the script on FAIL, then the existing local voice-server render produces and self-normalizes one chapter mp3. The HARD RULE: no audio is rendered until the critique PASSES. args: {book, chapter, slug, title?, voice?, voiceUser?, voicePassword?, api?}.',
  phases: [
    { title: 'Narration Script', detail: 'audiobook-director writes (or refreshes + re-verifies) the chapter narration performance script from the APPROVED prose -- tags + pause markers + scene breaks only, every prose word frozen' },
    { title: 'Critique gate', detail: 'Gemini narration-critique (scripts/gemini-critique.py --mode narration) judges fidelity + density + register + pacing + v3 tag craft; a gate agent rules PASS/FAIL; on FAIL the audiobook-director revises the script and it is re-critiqued. Render is GATED on a PASS (hard rule: never render without a passed narration-critique)' },
    { title: 'Render', detail: 'a Bash agent runs scripts/narrate-chapter-voiceserver.py on the PASSED script -- a full fresh local-model re-render to one chapter mp3 (the render self-normalizes its stitch)' },
    { title: 'Normalize', detail: 'confirm the deliverable: the voiceserver stitch already applies a uniform loudnorm (I=-18 TP=-2.0 LRA=11), so this measures the output integrated loudness + true peak to verify the built-in master landed (no re-encode)' },
    { title: 'Output', detail: 'report the final chapter mp3 path + duration + measured loudness, and the narration-script + critique companions' },
  ],
}

// args may arrive as a parsed object OR (depending on launch path) a JSON string -- normalize both so a
// stringified payload can't silently fall through to the chapter-1 defaults and "narrate" the wrong thing.
let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
A = A || {}
const NOVEL = '/home/codingbutter/Novel'
const BOOK = A.book || 'book-1'
const CHAPTER = (A.chapter === undefined || A.chapter === null) ? 1 : A.chapter
const NN = String(CHAPTER).padStart(2, '0')
const SLUG = A.slug || 'no-signal'
const TITLE = A.title || ('Chapter ' + CHAPTER)
const BASE = `chapter-${NN}-${SLUG}`              // the chapter base stem, e.g. chapter-01-no-signal
const VOICE = A.voice || 'Will_Wheaton'           // the single-narrator voice on the local voice server
const VUSER = A.voiceUser || null
const VPASS = A.voicePassword || null
const API = A.api || null                          // override the voice-server base URL (default in the script)
const MAX_GATE = A.maxGate || 3                    // critique<->revise rolls before aborting unrendered

const chapDir = `docs/50-manuscript/${BOOK}/${BASE}`
const manuscript = `${chapDir}/${BASE}.md`
const blueprint = `docs/40-blueprints/${BOOK}/${BASE}/blueprint.md`
const narrativeScript = `${chapDir}/${BASE}.narrative-script.md`
const narrCritique = `${chapDir}/${BASE}.narrative-script.gemini-critique.md`
const outMp3 = `audio/${BOOK}/${BASE}/${BASE}.narrator.mp3`

// Credentials are OPTIONAL: when omitted, narrate-chapter-voiceserver.py resolves them itself from
// VOICE_API_USER/VOICE_API_PASSWORD env or .mcp.json. Only pass --user/--password when explicitly given.
const CRED = (VUSER && VPASS) ? (" --user " + VUSER + " --password '" + VPASS + "'") : ""
const APIFLAG = API ? (" --api " + API) : ""

log('narrate-chapter args bound: book=' + BOOK + ' chapter=' + CHAPTER + ' slug=' + SLUG + ' (argsType=' + (typeof args) + ')')

const REPORT = { type: 'object', properties: { ok: { type: 'boolean' }, summary: { type: 'string' }, details: { type: 'string' } }, required: ['ok', 'summary'] }

// A single agent() call THROWS on retry-cap / API error / dropped connection; wrap the lone calls so a
// transient drop retries instead of aborting the whole run (same resilience helper live-audiobook uses).
async function tryAgent(make, tries) { tries = tries || 3; let last; for (let i = 0; i < tries; i++) { try { const r = await make(); if (r) return r; last = new Error('empty result'); } catch (e) { last = e; log('retry ' + (i + 1) + '/' + tries + ': ' + String(e).slice(0, 140)); } } throw last; }

// The audiobook-director's standing rules, restated inline so the directorial register is identical to the
// write-chapter narration phase: prose words are FROZEN canon; only bracketed register tags + [beat]/[hold]
// pause markers + `---` scene breaks are added; ellipses are avoided (the local voice server mishears them as
// runaway pauses -- [beat]/[hold] do that work). This is the v3 tag discipline the critique gate enforces.
const DIRECTOR = `You are the AUDIOBOOK DIRECTOR for the novel "The Unnecessary", marking a LIGHT-TOUCH single-narrator performance script. The voice is the self-hosted voice server's AUDIOBOOK preset: steady, weary, controlled, a Herzog register that trusts silence. Read the crew handbook (.claude/crew-handbook.md) and your charter first.
INVIOLABLE RULE: the prose WORDS are canon. Reproduce every sentence WORD FOR WORD; add ONLY bracketed register tags, the [beat]/[hold] pause markers, and scene-break lines (---). Never reword and never re-punctuate the prose.
FOUR REGISTERS, MARKED SPARINGLY: tag a register only where it GENUINELY shifts, one tag per block, never re-tagging every few words (redundant re-tagging is a defect and the renderer coalesces by register anyway). Registers: default BASE, the weary controlled narration voice (no tag, or [measured]); [flat] for automated corporate notices, machine-cold, where the calm is the threat; [tense]/[guarded] for strained or careful dialogue; [grave]/[slowly] for the deliberate heavy landings and the chapter's final line. Most of the chapter is untagged BASE.
PACING via MARKERS: mark deliberate pauses where a human reader would pause -- [beat] for a short breath, [hold] for a heavier deliberate stop -- placed intentionally and sparingly, NOT every sentence. The renderer turns each [beat]/[hold] into an exact silence.
ELLIPSES: do NOT sprinkle ellipses. On the voice server they cause garble and runaway multi-second pauses; [beat]/[hold] replace them. Use at most one or two in the whole chapter, only for a genuine held beat, always placed AFTER existing punctuation, never ",...". Use only tags + markers the renderer (scripts/narrate-chapter-voiceserver.py) actually honors. Grounded and austere throughout, never theatrical. Avoid em dashes.`

// ---- Phase 1: Narration Script -- author or refresh the v3 performance script from the APPROVED prose ----
phase('Narration Script')
const narrWrite = await tryAgent(() => agent(
  `${DIRECTOR}\n\n` +
  `READ the APPROVED chapter prose at ${NOVEL}/${manuscript} (prose body only; ignore the YAML front matter, the "## Adjudication Log", and any "## Decisions Made" log). If that manuscript file does not exist, STOP and return ok=false with summary "manuscript not found: ${manuscript}" -- this skill narrates an APPROVED chapter, it does not draft one.\n` +
  `For viewpoint + reveal-timing context (read only, never re-direct against it), glance at the blueprint ${NOVEL}/${blueprint} if it exists, and read the prior approved narration scripts as the house template for palette + density.\n` +
  `Then produce ${NOVEL}/${narrativeScript}: if it does not exist, WRITE it; if it already exists, EDIT it in place to re-verify fidelity and refresh the direction. The file must have exactly (1) YAML front matter (document_type narration-script, status draft, authority narration, title "${TITLE} (Narration Script)", a one-line summary, tags [narration, ${BOOK}, chapter-${NN}, performance-script], related ["./${BASE}.md"], source_documents ["${manuscript}"]); (2) a "## Voice Direction" section (overall register, per-register approach, pacing philosophy, the intensity arc + its peaks; not spoken); (3) a "## Performance Script" section that OPENS with a spoken chapter-title line (the chapter number spelled as a word) then the directed prose, scene breaks as lines of ---.\n` +
  `VERIFY before returning: strip every bracketed tag and pause marker and diff the remaining words against the manuscript prose -- they must be identical, token for token; confirm ZERO em dashes; confirm no later-book reveal leaked. Report (ok, summary, details): the script path, your word-for-word fidelity result + the diff method, the approximate tag count, and your main per-register choices. Do not write memories.`,
  { label: BASE + ':narr-write', phase: 'Narration Script', agentType: 'audiobook-director', schema: REPORT }
))
if (!narrWrite || narrWrite.ok === false) {
  throw new Error('Narration Script: audiobook-director could not produce the script (' + ((narrWrite && narrWrite.summary) || 'no result') + ') -- aborting before any render')
}
log('narration script: ' + (narrWrite.summary || narrativeScript))

// ---- Phase 2: Critique gate -- Gemini narration-critique must PASS before any audio is rendered ----
// HARD PROJECT RULE: never render/ship narration audio without a PASSED Gemini narration-critique. The
// critique script writes an advisory MD (exit 0 regardless), so a gate agent reads it and rules PASS/FAIL on
// the BLOCKING classes -- any prose-fidelity drift (added/cut/reworded word vs the manuscript) or any v3 tag-
// discipline violation (ellipsis misuse / runaway-pause risk, a tag the renderer cannot honor). On FAIL the
// audiobook-director revises the script (tags + markers only, prose frozen) and it is re-critiqued. The loop
// caps at MAX_GATE rolls; if it never passes, the run ABORTS UNRENDERED rather than ship un-vetted audio.
phase('Critique gate')
const GATE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    verdict: { type: 'string' },                 // PASS or FAIL
    blocking: { type: 'array', items: { type: 'string' } },
    advisory: { type: 'array', items: { type: 'string' } },
    note: { type: 'string' },
  }, required: ['verdict', 'note'],
}
let gatePass = false
let lastGate = null
const gateRolls = []
for (let attempt = 1; attempt <= MAX_GATE; attempt++) {
  // (a) run the critique script (Bash-capable agent) -- text-vs-text, on the Gemini quota, zero Claude budget.
  const crit = await tryAgent(() => agent(
    `Run EXACTLY this command from ${NOVEL} and report the result:\n` +
    `  python3 scripts/gemini-critique.py ${narrativeScript} --mode narration --reference ${manuscript} --out ${narrCritique}\n` +
    `This sends the narration script to Gemini acting as an audiobook director, judging fidelity to the prose, direction density, register distinction, pacing, and v3 tag craft. The critique lands in ${narrCritique} (a SEPARATE file; the script is not touched). After it succeeds, READ ${narrCritique} and summarize the suggestions grouped by severity with a total count. If the command fails, return ok=false with the exact error and do not invent a critique.`,
    { label: BASE + ':narr-critique:' + attempt, phase: 'Critique gate', effort: 'low', schema: REPORT }
  ))
  if (!crit || crit.ok === false) {
    throw new Error('Critique gate: gemini-critique.py failed (' + ((crit && crit.summary) || 'no result') + ') -- aborting before render rather than shipping un-vetted narration')
  }
  // (b) a gate agent reads the critique file and RULES pass/fail on the blocking classes only.
  const gate = await tryAgent(() => agent(
    `You are the NARRATION-CRITIQUE GATE for the single-narrator audiobook of "The Unnecessary". Read the Gemini narration-critique at ${NOVEL}/${narrCritique} and the script it judges at ${NOVEL}/${narrativeScript}.\n` +
    `Rule PASS or FAIL on the BLOCKING classes ONLY:\n` +
    `  - FIDELITY: any added, cut, reordered, or reworded prose word versus the manuscript (the spoken text must be the prose, character for character). ANY confirmed fidelity drift is an automatic FAIL.\n` +
    `  - v3 TAG DISCIPLINE: ellipsis misuse (more than a held beat or two, a ",..." construction, or any use that risks a runaway multi-second pause on the voice server), or a tag the renderer cannot honor. Pauses must be carried by [beat]/[hold], not ellipses. A confirmed violation is a FAIL.\n` +
    `Density, register-melodrama, and pure pacing taste are ADVISORY, not blocking -- list them under advisory; they do NOT fail the gate.\n` +
    `Return per schema: verdict=PASS only when there is NO blocking fidelity or tag-discipline issue; blocking=the exact issues that must be fixed before render (empty on PASS); advisory=non-blocking notes; note=one line.`,
    { label: BASE + ':gate:' + attempt, phase: 'Critique gate', effort: 'low', schema: GATE_SCHEMA }
  ))
  lastGate = gate
  gateRolls.push({ attempt, verdict: gate && gate.verdict, blocking: (gate && gate.blocking) || [] })
  if (gate && String(gate.verdict).toUpperCase() === 'PASS') {
    gatePass = true
    log('critique gate: PASS on attempt ' + attempt + ((gate.advisory && gate.advisory.length) ? (' (' + gate.advisory.length + ' advisory note(s) left for the author)') : ''))
    break
  }
  log('critique gate: FAIL on attempt ' + attempt + ' -- ' + (((gate && gate.blocking) || []).length) + ' blocking issue(s)')
  if (attempt === MAX_GATE) break
  // (c) FAIL -> audiobook-director revises the script for the blocking issues only, then re-critique.
  await tryAgent(() => agent(
    `${DIRECTOR}\n\nYou are the director adjudicating the narration-critique GATE's blocking notes on YOUR script. READ ${NOVEL}/${narrativeScript} and the critique ${NOVEL}/${narrCritique}.\n` +
    `FIX every BLOCKING issue the gate raised (these MUST be resolved before the chapter can render):\n` + (((gate && gate.blocking) || []).map(b => '  - ' + b).join('\n') || '  - (see the critique file)') + '\n' +
    `Apply the fixes directly to ${narrativeScript}, still adding ONLY tags + [beat]/[hold] markers + scene-break lines and NEVER changing a prose word: restore any drifted prose word to the manuscript exactly, and replace any offending ellipsis with a [beat]/[hold] (or remove it). You MAY also act on advisory notes where they improve the read, but the blocking fixes are mandatory.\n` +
    `Append or extend a "## Narration Adjudication Log" at the END of the file with each note + your decision + a one-line reason.\n` +
    `VERIFY again: stripping tags/markers leaves words IDENTICAL to ${manuscript}; ZERO em dashes; no leaked reveal. Report (ok, summary, details) the blocking issues resolved and the final tag count. Do not write memories.`,
    { label: BASE + ':narr-fix:' + attempt, phase: 'Critique gate', agentType: 'audiobook-director', schema: REPORT }
  ))
}
if (!gatePass) {
  throw new Error('Critique gate: the narration script did not pass the Gemini narration-critique within ' + MAX_GATE + ' roll(s) (last verdict: ' + ((lastGate && lastGate.verdict) || 'none') + '; blocking: ' + JSON.stringify((lastGate && lastGate.blocking) || []) + ') -- ABORTING UNRENDERED. Hard rule: no narration audio is rendered without a passed narration-critique.')
}

// ---- Phase 3: Render -- full fresh local-model re-render of the PASSED script to one chapter mp3 ----
// Always a FULL fresh re-render (the script's default; not --resume) on the local voice model -- power, not
// tokens. The render's stitch self-masters with loudnorm, so the output is already a normalized deliverable.
phase('Render')
const RENDER_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: { ok: { type: 'boolean' }, out: { type: 'string' }, duration_s: { type: 'number' }, chunks: { type: 'integer' }, summary: { type: 'string' } },
  required: ['ok', 'out', 'summary'],
}
const render = await tryAgent(() => agent(
  `Render the PLAIN single-narrator audiobook for one APPROVED, critique-PASSED chapter of "The Unnecessary" on the local voice server, then report.\n` +
  `Run EXACTLY this command from ${NOVEL} (a FULL fresh re-render -- do NOT add --resume):\n` +
  `  mkdir -p ${NOVEL}/audio/${BOOK}/${BASE} && python3 scripts/narrate-chapter-voiceserver.py ${narrativeScript} --voice ${VOICE} --out ${outMp3} --format mp3${CRED}${APIFLAG}\n` +
  `It maps the v3 tags to voice-server performance profiles, renders each chunk on the local model sequentially, and stitches them with a built-in loudnorm master to ${outMp3}. (Credentials, when not passed, resolve from VOICE_API_USER/VOICE_API_PASSWORD env or .mcp.json.)\n` +
  `After it finishes, verify the output exists and probe it: ffprobe -v error -show_entries format=duration -of csv=p=0 ${NOVEL}/${outMp3}\n` +
  `Return ok=true ONLY if ${outMp3} exists with a positive duration. Report out=the mp3 path, duration_s, chunks rendered (from the render log), and a one-line summary (or the exact error if it failed). Do not write memories.`,
  { label: BASE + ':render', phase: 'Render', schema: RENDER_SCHEMA }
))
if (!render || render.ok === false) {
  throw new Error('Render: the voice-server render did not produce a chapter mp3 (' + ((render && render.summary) || 'no result') + ')')
}
log('render: ' + (render.out || outMp3) + ' (' + (render.duration_s || '?') + 's)')

// ---- Phase 4: Normalize -- confirm the deliverable's loudness (the render already self-masters) ----
// The voiceserver stitch applies loudnorm=I=-18:TP=-2.0:LRA=11 as a built-in master, so unlike the LIVE path
// (many per-line stems -> a separate normalize-stems.py before mixing) the single-narrator path needs no
// separate normalize script. This phase MEASURES the output to verify the built-in master landed -- no re-encode.
phase('Normalize')
const NORM_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: { ok: { type: 'boolean' }, lufs: { type: 'number' }, true_peak: { type: 'number' }, summary: { type: 'string' } },
  required: ['ok', 'summary'],
}
const norm = await tryAgent(() => agent(
  `Confirm the loudness of a finished single-narrator chapter deliverable of "The Unnecessary". The render already applied a built-in loudnorm master (target I=-18 LUFS, TP=-2.0 dBTP), so do NOT re-encode -- just MEASURE and confirm.\n` +
  `Measure the integrated loudness + true peak of ${NOVEL}/${outMp3} with ffmpeg's ebur128 (e.g. ffmpeg -i ${NOVEL}/${outMp3} -af ebur128=peak=true -f null - 2>&1 | tail -40) and read the Integrated and True peak summary lines.\n` +
  `Return ok=true if the file measures with a sane integrated loudness near -18 LUFS (within a few LU is fine). Report lufs=integrated LUFS, true_peak=dBTP, and a one-line summary noting whether the built-in master landed. Do not write memories.`,
  { label: BASE + ':normalize', phase: 'Normalize', effort: 'low', schema: NORM_SCHEMA }
))
log('normalize: ' + ((norm && norm.summary) || 'measured') + (norm && norm.lufs !== undefined ? (' (' + norm.lufs + ' LUFS, TP ' + norm.true_peak + ')') : ''))

// ---- Phase 5: Output ----
phase('Output')
return {
  chapter: { book: BOOK, number: CHAPTER, slug: SLUG, title: TITLE },
  files: { manuscript, narrativeScript, narrCritique, mp3: outMp3 },
  narration: narrWrite,
  gate: { passed: gatePass, rolls: gateRolls, last: lastGate },
  render,
  normalize: norm,
  next: `Listen to ${outMp3}. If a line reads wrong, drive ONE revision sweep: edit ${narrativeScript} (audiobook-director) and re-run this skill, which re-passes the critique gate and full-re-renders. Live/dramatized edition is a separate path (/live-audiobook).`,
}
