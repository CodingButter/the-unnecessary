export const meta = {
  name: 'live-audiobook',
  description: 'Produce the dramatized live-narration audiobook for a chapter, scene by scene: casting-director signs off the ensemble, then one autonomous live-narration-director per scene (adapt -> Gemini gate -> render -> normalize -> mix), a prooflistener QC gate re-rolls flagged lines, stitch, and a sound-engineer mastering pass. Skips scenes already produced. args: {book, chapter, scenes?, voiceUser?, voicePassword?}.',
  phases: [
    { title: 'Discover', detail: 'split the chapter manuscript into scenes; skip ones already produced' },
    { title: 'Cast', detail: 'casting-director pre-flight: confirm every speaking character has an assigned, contrast-checked voice (route gaps to voice-designer) and sign off the ensemble before any scene renders' },
    { title: 'Produce', detail: 'one live-narration-director per scene, sequential (single voice server)' },
    { title: 'Prooflisten', detail: 'prooflistener QC of the rendered audio vs script + pronunciation lexicon; flagged lines re-rolled through the existing render path before stitch' },
    { title: 'Stitch', detail: 'concatenate the per-scene mixes into one chapter .live.mp3' },
    { title: 'Master', detail: 'sound-engineer master: one uniform loudness + true-peak ceiling on the stitched chapter (routes the tool build to systems-engineer if not yet built)' },
  ],
}

// args may arrive as a parsed object OR (depending on launch path) a JSON string -- normalize both so a
// stringified payload can't silently fall through to the chapter-1 defaults and "produce" nothing.
let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
A = A || {}
const BOOK = A.book || 'book-1'
const CHAPTER = A.chapter || 'chapter-01-no-signal'
const ONLY = A.scenes || null
const VUSER = A.voiceUser || 'codingbutter'
const VPASS = A.voicePassword || ''
const CRED = VPASS ? ("--user " + VUSER + " --password '" + VPASS + "'") : ""
const MS = `docs/50-manuscript/${BOOK}/${CHAPTER}/${CHAPTER}.md`
const BP = `docs/40-blueprints/${BOOK}/${CHAPTER}/blueprint.md`
const ROOT = `audio/live-audio-book/${BOOK}/${CHAPTER}`
// Canonical already-produced scene the directors read for format/quality/conventions. Must point at a
// scene that actually EXISTS on disk -- NOT inside ROOT (the current chapter may be a clean slate, e.g.
// producing chapter 2 before any of its scenes exist). Defaults to chapter 1's first produced scene.
const REF = A.refCues || `audio/live-audio-book/${BOOK}/chapter-01-no-signal/scene-01-no-signal/cues.json`
log('live-audiobook args bound: book=' + BOOK + ' chapter=' + CHAPTER + ' (argsType=' + (typeof args) + ')')

// Resilience: a single agent() call THROWS on retry-cap / API error / dropped connection, which would
// abort the whole production. Wrap the lone (non-parallel) calls so a transient drop retries instead of
// losing the run. parallel() already absorbs failures (returns null per thunk), so it does not need this.
async function tryAgent(make, tries) { tries = tries || 3; let last; for (let i = 0; i < tries; i++) { try { const r = await make(); if (r) return r; last = new Error('empty result'); } catch (e) { last = e; log('retry ' + (i + 1) + '/' + tries + ': ' + String(e).slice(0, 140)); } } throw last; }

phase('Discover')
// Boundaries first, prose second. Returning every scene's FULL verbatim prose in ONE structured array is
// a big fragile response that truncates / drops the connection on a long chapter and aborts the run. This
// pass returns ONLY the scene boundaries (n, slug, opening/closing anchors, already_done) -- a tiny robust
// output that owns the boundaries once (so scenes stay contiguous + non-overlapping). Each to-produce
// scene's bulky verbatim prose is then pulled in its own small call, in parallel, and merged back by scene.
const META_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: { scenes: { type: 'array', items: {
    type: 'object', additionalProperties: false,
    properties: {
      n: { type: 'integer' }, slug: { type: 'string' },
      first_words: { type: 'string' }, last_words: { type: 'string' },
      already_done: { type: 'boolean' },
    }, required: ['n', 'slug', 'first_words', 'last_words', 'already_done'],
  } } }, required: ['scenes'],
}

const disc = await tryAgent(() => agent(
  'Split a chapter of the novel "The Unnecessary" into its SCENES for live-audiobook production -- BOUNDARIES ONLY, do NOT return the full prose here.\n' +
  'Manuscript: ' + MS + '\nBlueprint (scene list + titles): ' + BP + '\n' +
  'Scenes in the manuscript are separated by "---" divider lines. For EACH scene return:\n' +
  '- n: 1-based scene number\n' +
  '- slug: "scene-0N-<short-kebab-title>" from the blueprint scene title, zero-padded; if a dir already exists under ' + ROOT + '/ for that scene, reuse that exact slug\n' +
  '- first_words: the scene\'s opening ~10 words, VERBATIM from the manuscript (the first words after its starting divider)\n' +
  '- last_words: the scene\'s closing ~10 words, VERBATIM from the manuscript (the last words before its ending divider)\n' +
  '- already_done: true ONLY if the file ' + ROOT + '/<slug>/scene-live.mp3 already exists on disk\n' +
  'Scenes must be CONTIGUOUS and NON-OVERLAPPING: each is exactly the block between its dividers, and no line appears in two scenes (overlap causes duplicated audio when scenes are stitched).\n' +
  'Return every scene, in order.',
  { schema: META_SCHEMA, phase: 'Discover', agentType: 'canon-scout' }
))

let scenes = (disc && disc.scenes) || []
if (ONLY) scenes = scenes.filter(s => ONLY.includes(s.slug))
const todoMeta = scenes.filter(s => !s.already_done)
log('chapter has ' + scenes.length + ' scene(s); ' + todoMeta.length + ' to produce, ' + (scenes.length - todoMeta.length) + ' already done')
if (!todoMeta.length) return { chapter: CHAPTER, produced: [], note: 'all scenes already produced' }

// Pull each to-produce scene's verbatim prose in its own small call (parallel). The boundary pass above
// fixed the anchors, so each pull just transcribes the one block between them -- a bounded per-call output.
const PROSE_SCHEMA = { type: 'object', additionalProperties: false, properties: { prose: { type: 'string' } }, required: ['prose'] }
const proseThunks = todoMeta.map(s => () => agent(
  'Return the FULL verbatim manuscript prose of ONE scene of the novel "The Unnecessary", for live-audiobook production.\n' +
  'Manuscript: ' + MS + '\n' +
  'Scenes are separated by "---" divider lines. Return scene ' + s.n + ' of ' + scenes.length + ': the divider-delimited block that BEGINS with "' + s.first_words + '" and ENDS with "' + s.last_words + '".\n' +
  'Return everything between that scene\'s "---" dividers, VERBATIM and complete, exactly as written in the manuscript -- this scene ONLY. Do NOT include the divider lines, do NOT recap the previous scene, and do NOT include any of the next scene.\n' +
  'Per schema.',
  { schema: PROSE_SCHEMA, phase: 'Discover', agentType: 'canon-scout' }
))
const proseRuns = await parallel(proseThunks)
// Retry-sweep: a dropped/null pull comes back empty; re-run just those once before producing audio from it.
const missing = proseRuns.map((r, k) => ((r && r.prose) ? -1 : k)).filter(k => k >= 0)
if (missing.length) {
  log('prose retry-sweep: re-pulling ' + missing.length + ' scene(s)')
  const re = await parallel(missing.map(k => proseThunks[k]))
  missing.forEach((k, j) => { if (re[j]) proseRuns[k] = re[j] })
}
const todo = todoMeta.map((s, i) => ({ n: s.n, slug: s.slug, prose: (proseRuns[i] && proseRuns[i].prose) || '', already_done: s.already_done }))
const emptyProse = todo.filter(s => !String(s.prose).trim())
if (emptyProse.length) throw new Error('Discover: ' + emptyProse.length + ' scene(s) returned empty prose (' + emptyProse.map(s => s.slug).join(', ') + ') -- aborting rather than producing audio from a truncated/dropped split')

phase('Cast')
// casting-director PRE-FLIGHT: own the ensemble as a SET before any scene renders. It confirms every speaking
// character in this chapter has an assigned, contrast-checked voice in the cast sheet (no co-present collision,
// cross-chapter consistency clean) and signs the sheet. Any unassigned/undesigned voice is ROUTED to voice-designer
// (which owns the design endpoint; casting-director has no Bash) and the ensemble is re-signed -- the same author-
// then-route shape write-chapter uses for provisioning. The Produce phase is GATED on the sign-off.
const CAST_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    signed_off: { type: 'boolean' },
    cast_sheet: { type: 'string' },
    needs_design: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: { slug: { type: 'string' }, contrast_target: { type: 'string' }, why: { type: 'string' } },
      required: ['slug', 'contrast_target'],
    } },
    note: { type: 'string' },
  }, required: ['signed_off', 'note'],
}
async function castSignoff(reSignNote) {
  return tryAgent(() => agent(
    'You are the casting-director. Confirm + sign off the live-audiobook CAST for the novel "The Unnecessary" chapter "' + CHAPTER + '" BEFORE any scene renders.\n' +
    'Cast sheet (read + maintain + sign): docs/10-vision/audio/cast-sheet.md\n' +
    'Manuscript (the speaking characters in scope): ' + MS + '\nBlueprint (scene list + who is co-present): ' + BP + '\n' +
    'Determine EVERY speaking character in this chapter, confirm each has an assigned, contrast-checked voice (no co-present collision on the ear, cross-chapter consistency clean), and update + sign the cast sheet.\n' +
    'For any character with NO assigned voice, or whose voice still needs designing or re-rolling, return it in needs_design with its canon slug and the contrast target it must hit (the audible gap vs its co-present neighbors). Do NOT design it yourself (you have no Bash) -- the pipeline routes each to voice-designer right after you, then re-runs your sign-off.\n' +
    (reSignNote || '') +
    'Return per schema: signed_off=true ONLY when every speaking character in scope is assigned + contrast-checked with nothing left to design; cast_sheet=the cast-sheet path; needs_design=the voices to route (empty when fully cast); note=one line.',
    { schema: CAST_SCHEMA, label: 'cast:' + CHAPTER, phase: 'Cast', agentType: 'casting-director' }
  ))
}
let cast = await castSignoff(null)
const toDesign = ((cast && cast.needs_design) || []).filter(v => v && v.slug)
let castDesigned = []
if (toDesign.length) {
  log('cast: ' + toDesign.length + ' voice(s) need designing -- routing to voice-designer before render')
  castDesigned = await parallel(toDesign.map(v => () => agent(
    'You are the voice-designer. The casting-director needs ONE voice designed for the LIVE edition of "The Unnecessary" before scenes render.\n' +
    'Character slug: ' + v.slug + '\nContrast target it must hit (the audible gap vs its co-present neighbors): ' + (v.contrast_target || '(see cast sheet)') + '\nWhy: ' + (v.why || '(see cast sheet)') + '\n' +
    'Read the character profile, craft the voice description + essence line, and run scripts/voice-design.py for this character so the samples + voice-design.json are saved locally and the live render can use the voice. Report the voice slug, the description, and the saved samples + folder path.',
    { label: 'cast:design:' + v.slug, phase: 'Cast', agentType: 'voice-designer' }
  )))
  cast = await castSignoff('NOTE: voice-designer has just designed the previously-missing voice(s) (' + toDesign.map(v => v.slug).join(', ') + '); re-confirm the full ensemble and sign off.\n')
}
if (!cast || cast.signed_off !== true) {
  throw new Error('Cast: casting-director did not sign off the ensemble (' + ((cast && cast.note) || 'no result') + ') -- aborting before render rather than producing scenes with an unassigned or colliding voice')
}
log('cast: ensemble signed off (' + (cast.cast_sheet || 'docs/10-vision/audio/cast-sheet.md') + ')')

phase('Produce')
const reports = []
for (const s of todo) {                 // SEQUENTIAL: the voice server is a single local model
  const sceneDir = ROOT + '/' + s.slug
  const r = await tryAgent(() => agent(
    'Produce the LIVE / dramatized audiobook for ONE scene, fully and autonomously, per your standing rules and the proven pipeline.\n' +
    'Scene: Chapter "' + CHAPTER + '", scene ' + s.n + ' -> ' + s.slug + '\n' +
    'Scene directory (create it; write cues.json + voice/ here): ' + sceneDir + '\n' +
    'Reference an already-produced scene for format/quality/conventions (READ it first): ' + REF + '\n' +
    'Original scene prose -- adapt from THIS, faithfully:\n"""\n' + s.prose + '\n"""\n' +
    'SCENE BOUNDARY: adapt ONLY this prose. Do NOT recap the previous scene closing beat or pre-empt the next scene opening; begin at this prose first line and end at its last. (Recapping/overrunning duplicates audio when scenes are stitched.)\n' +
    'Run the WHOLE pipeline yourself: author ' + sceneDir + '/cues.json (all adaptation rules) -> Gemini gate against this exact prose, revise until CLEAN -> resolve/generate SFX + music + filters by scope (reuse book/chapter assets; generate only genuinely-new ones via ElevenLabs REST) -> render (scripts/render-voice-stems.py ' + sceneDir + '/cues.json ' + CRED + ') -> normalize (scripts/normalize-stems.py ' + sceneDir + '/cues.json) -> mix (scripts/mix-live-scene.py ' + sceneDir + '/cues.json) -> ' + sceneDir + '/scene-live.mp3.\n' +
    'Report (<120 words): cue sheet path, Gemini verdict + revisions, assets generated vs reused, final mp3 path + duration, and any blocker.',
    { label: 'scene:' + s.slug, phase: 'Produce', agentType: 'live-narration-director' }
  ))
  reports.push({ slug: s.slug, report: r })
}

phase('Prooflisten')
// prooflistener POST-RENDER QC gate -- the ONLY check that listens to the rendered OUTPUT. It reviews each produced
// scene's audio against that scene's cues.json script + the pronunciation lexicon (the render already wrote a per-
// scene qc.json via verify-narration.py), adds the two cross-chapter checks the verifier cannot do alone (proper-
// noun vs lexicon spelling, and name-vs-other-chapters pronunciation drift), and emits a TIMESTAMPED re-roll list
// keyed to scene + cue index + role. Advisory-but-acted: re-rolls are near-free, so flagged scenes go back through
// the existing render path (live-narration-director) before stitch. Non-aborting -- a re-roll drop is logged, not fatal.
const PROOF_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    verdict: { type: 'string' },
    rerolls: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: {
        slug: { type: 'string' },
        cues: { type: 'array', items: { type: 'integer' } },
        roles: { type: 'array', items: { type: 'string' } },
        timestamp: { type: 'string' }, class: { type: 'string' },
        expected: { type: 'string' }, fix: { type: 'string' },
      }, required: ['slug', 'class', 'expected'],
    } },
    pronunciation: { type: 'array', items: { type: 'string' } },
    note: { type: 'string' },
  }, required: ['verdict', 'note'],
}
const proof = await tryAgent(() => agent(
  'You are the prooflistener. QC the RENDERED audio of "The Unnecessary" chapter "' + CHAPTER + '" scene by scene BEFORE it is stitched -- the only gate that listens to the OUTPUT.\n' +
  'Produced scene dirs (each holds cues.json + the rendered voice stems + scene-live.mp3, and the render wrote a per-scene qc.json via verify-narration.py): ' + todo.map(s => ROOT + '/' + s.slug).join(', ') + '\n' +
  'Pronunciation lexicon: scripts/data/pronunciation-lexicon.json\n' +
  'For EACH scene: read its qc.json and run/re-run scripts/verify-narration.py over the rendered stems vs that scene\'s cues.json script where you need fresh transcripts, reason over the diffs against the lexicon, and ADD the two checks the verifier does not do alone -- (a) every canon proper noun\'s transcription vs its lexicon spelling, and (b) how each proper noun transcribed in THIS chapter vs the SAME name in other rendered chapters (a divergence is a pronunciation-drift candidate).\n' +
  'Emit a TIMESTAMPED re-roll list keyed to scene slug + cue index + role, each defect named (DROPPED/DOUBLED/MISSING-LINE | GARBLE/WRONG-WORD | HOMOGRAPH | NUMBER-MISREAD | PRONUNCIATION-DRIFT) with EXPECTED vs what the audio said and the tts/script fix where unambiguous. You DIAGNOSE and ROUTE only -- never re-render or edit a deliverable; the pipeline routes each flagged scene back to the live-narration-director to re-roll.\n' +
  'Return per schema: verdict=CLEAN or RE-ROLLS NEEDED; rerolls grouped by scene slug (cues + roles + timestamp + class + expected + fix); pronunciation=cross-chapter drift candidates to front-load into the lexicon; note=one line.',
  { schema: PROOF_SCHEMA, label: 'prooflisten:' + CHAPTER, phase: 'Prooflisten', agentType: 'prooflistener' }
))
// Act on the pickup list: group flagged cues by scene and re-roll each through the existing render path. SEQUENTIAL
// (single voice server), like Produce. A re-roll failure is logged, never fatal -- the already-produced mix stands.
const proofRerolls = ((proof && proof.rerolls) || []).filter(r => r && r.slug && todo.some(s => s.slug === r.slug))
const reBySlug = {}
for (const r of proofRerolls) { (reBySlug[r.slug] = reBySlug[r.slug] || []).push(r) }
const reSlugs = Object.keys(reBySlug)
const rerollReports = []
if (reSlugs.length) {
  log('prooflisten: ' + ((proof && proof.verdict) || '') + ' -- re-rolling ' + reSlugs.length + ' scene(s): ' + reSlugs.join(', '))
  for (const slug of reSlugs) {           // SEQUENTIAL: the voice server is a single local model
    const sceneDir = ROOT + '/' + slug
    const flags = reBySlug[slug]
    const rr = await tryAgent(() => agent(
      'Re-roll ONLY the prooflistener-flagged lines in ONE already-produced live scene, then re-mix it -- the existing render path, targeted. Do NOT re-adapt the scene or touch any clean line.\n' +
      'Scene: Chapter "' + CHAPTER + '", scene ' + slug + '\nScene directory (cues.json + voice/ already here): ' + sceneDir + '\n' +
      'Prooflistener pickup list for this scene (re-roll exactly these cues/roles):\n' + JSON.stringify(flags) + '\n' +
      'For each flag: apply the named tts/script fix in ' + sceneDir + '/cues.json where one is given (a pronunciation correction in the cue tts field, a number spelled out), then re-render just the affected cues (scripts/render-voice-stems.py ' + sceneDir + '/cues.json --role <role> ' + CRED + ' re-rolls only that role, leaving the rest untouched), re-normalize (scripts/normalize-stems.py ' + sceneDir + '/cues.json) and re-mix (scripts/mix-live-scene.py ' + sceneDir + '/cues.json) so ' + sceneDir + '/scene-live.mp3 is refreshed.\n' +
      'Report (<100 words): which cues/roles re-rolled, the fixes applied, and the refreshed mp3 path + duration.',
      { label: 'reroll:' + slug, phase: 'Prooflisten', agentType: 'live-narration-director' }
    ))
    rerollReports.push({ slug, report: rr })
  }
} else {
  log('prooflisten: ' + ((proof && proof.verdict) || 'no result') + ' -- no re-rolls before stitch')
}

phase('Stitch')
// Concatenate the per-scene mixes into one continuous chapter file. Deterministic Bash step; one agent
// runs it and reports the result so the workflow is end-to-end (script -> final chapter .live.mp3).
const STITCH_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: { ok: { type: 'boolean' }, out: { type: 'string' }, duration_s: { type: 'number' }, scenes_stitched: { type: 'integer' }, note: { type: 'string' } },
  required: ['ok', 'out', 'note'],
}
const stitch = await tryAgent(() => agent(
  'Stitch a chapter of "The Unnecessary" live audiobook into ONE continuous chapter file, then report.\n' +
  'Run EXACTLY: python3 scripts/stitch-chapter.py ' + ROOT + '\n' +
  'It concatenates ' + ROOT + '/scene-*/scene-live.mp3 in slug order and writes ' + ROOT + '/' + CHAPTER + '.live.mp3.\n' +
  'After it runs, verify the output exists and probe it: ffprobe -v error -show_entries format=duration -of csv=p=0 ' + ROOT + '/' + CHAPTER + '.live.mp3\n' +
  'Also count the scene inputs: ls ' + ROOT + '/scene-*/scene-live.mp3 | wc -l\n' +
  'Return ok=true ONLY if the .live.mp3 exists with a positive duration. Report out=output path, duration_s, scenes_stitched, and a one-line note (or the error if it failed).',
  { schema: STITCH_SCHEMA, label: 'stitch:' + CHAPTER, phase: 'Stitch', agentType: 'live-narration-director' }
))

phase('Master')
// sound-engineer book/chapter-level MASTER (audio-roles audit gap 1.3): measure integrated loudness on the stitched
// chapter file and apply ONE uniform loudness + true-peak ceiling so the chapter sits at a consistent deliverable
// level. stitch-chapter.py already does a per-stitch loudnorm, but NOT a uniform book-level master. If no script does
// that yet, the sound-engineer ROUTES the build to systems-engineer BY NAME rather than inventing the tool inline;
// this wiring TOLERATES a routed (not-yet-built) result -- a routed/deferred master is logged, never fatal.
const MASTER_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    ok: { type: 'boolean' }, mastered: { type: 'boolean' }, out: { type: 'string' },
    lufs_in: { type: 'number' }, lufs_out: { type: 'number' }, true_peak: { type: 'number' },
    routed: { type: 'string' }, note: { type: 'string' },
  }, required: ['ok', 'note'],
}
let master = null
if (stitch && stitch.ok) {
  const stitched = ROOT + '/' + CHAPTER + '.live.mp3'
  master = await tryAgent(() => agent(
    'You are the sound-engineer. MASTER the stitched chapter file of "The Unnecessary" live audiobook to ONE uniform loudness + true-peak ceiling so the chapter is a consistent deliverable (audio-roles audit gap 1.3).\n' +
    'Stitched chapter file: ' + stitched + '\n' +
    'First MEASURE its integrated loudness + true peak (ffmpeg ebur128 / loudnorm print or ffprobe). Then APPLY a single uniform loudness normalization + true-peak ceiling across the whole file and write the mastered deliverable.\n' +
    'TOOLING RULE: stitch-chapter.py does a per-stitch loudness pass but there is NO uniform book/chapter-level MASTER script yet. If running the master needs a script that does not exist, do NOT invent the tool inline -- ROUTE the build to systems-engineer BY NAME (state the exact script + interface to build under scripts/ and the loudness + TP target), and return routed=that brief with mastered=false. Where a suitable script DOES already exist, run it and return mastered=true.\n' +
    'Return per schema: ok; mastered (true only if a mastered file was actually written); out=the mastered file path; lufs_in/lufs_out/true_peak measured; routed=the systems-engineer build brief (empty when none needed); note=one line.',
    { schema: MASTER_SCHEMA, label: 'master:' + CHAPTER, phase: 'Master', agentType: 'sound-engineer' }
  ))
  if (master && master.routed) {
    log('master: book-level mastering tool not built yet -- routed to systems-engineer: ' + String(master.routed).slice(0, 160))
  } else if (master && master.mastered) {
    log('master: ' + (master.out || stitched) + ' mastered to uniform loudness (in ' + master.lufs_in + ' -> out ' + master.lufs_out + ' LUFS, TP ' + master.true_peak + ')')
  } else {
    log('master: ' + ((master && master.note) || 'no result'))
  }
} else {
  log('master: skipped -- stitch did not produce a chapter file')
}

return { chapter: CHAPTER, produced: reports.map(x => x.slug), reports, cast, castDesigned, proof, rerolls: rerollReports, stitch, master }
