export const meta = {
  name: 'live-audiobook',
  description: 'Produce the dramatized live-narration audiobook for a chapter, scene by scene: one autonomous live-narration-director per scene (adapt -> Gemini gate -> render -> normalize -> mix). Skips scenes already produced. args: {book, chapter, scenes?, voiceUser?, voicePassword?}.',
  phases: [
    { title: 'Discover', detail: 'split the chapter manuscript into scenes; skip ones already produced' },
    { title: 'Produce', detail: 'one live-narration-director per scene, sequential (single voice server)' },
    { title: 'Stitch', detail: 'concatenate the per-scene mixes into one chapter .live.mp3' },
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

return { chapter: CHAPTER, produced: reports.map(x => x.slug), reports, stitch }
