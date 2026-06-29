export const meta = {
  name: 'live-audiobook',
  description: 'Produce the dramatized live-narration audiobook for a chapter, scene by scene: one autonomous live-narration-director per scene (adapt -> Gemini gate -> render -> normalize -> mix). Skips scenes already produced. args: {book, chapter, scenes?, voiceUser?, voicePassword?}.',
  phases: [
    { title: 'Discover', detail: 'split the chapter manuscript into scenes; skip ones already produced' },
    { title: 'Produce', detail: 'one live-narration-director per scene, sequential (single voice server)' },
  ],
}

const BOOK = (args && args.book) || 'book-1'
const CHAPTER = (args && args.chapter) || 'chapter-01-no-signal'
const ONLY = (args && args.scenes) || null
const VUSER = (args && args.voiceUser) || 'codingbutter'
const VPASS = (args && args.voicePassword) || ''
const CRED = VPASS ? ("--user " + VUSER + " --password '" + VPASS + "'") : ""
const MS = `docs/50-manuscript/${BOOK}/${CHAPTER}/${CHAPTER}.md`
const BP = `docs/40-blueprints/${BOOK}/${CHAPTER}/blueprint.md`
const ROOT = `audio/live-audio-book/${BOOK}/${CHAPTER}`

phase('Discover')
const SCENES_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: { scenes: { type: 'array', items: {
    type: 'object', additionalProperties: false,
    properties: {
      n: { type: 'integer' }, slug: { type: 'string' },
      prose: { type: 'string' }, already_done: { type: 'boolean' },
    }, required: ['n', 'slug', 'prose', 'already_done'],
  } } }, required: ['scenes'],
}

const disc = await agent(
  'Split a chapter of the novel "The Unnecessary" into its SCENES for live-audiobook production.\n' +
  'Manuscript: ' + MS + '\nBlueprint (scene list + titles): ' + BP + '\n' +
  'Scenes in the manuscript are separated by "---" divider lines. For EACH scene return:\n' +
  '- n: 1-based scene number\n' +
  '- slug: "scene-0N-<short-kebab-title>" from the blueprint scene title, zero-padded; if a dir already exists under ' + ROOT + '/ for that scene, reuse that exact slug\n' +
  '- prose: the FULL verbatim manuscript text of that scene (everything between its dividers)\n' +
  '- already_done: true ONLY if the file ' + ROOT + '/<slug>/scene-live.mp3 already exists on disk\n' +
  'Scenes must be CONTIGUOUS and NON-OVERLAPPING: each prose block is exactly the text between its dividers, and no line appears in two scenes (overlap causes duplicated audio when scenes are stitched).\n' +
  'Return every scene, in order.',
  { schema: SCENES_SCHEMA, phase: 'Discover', agentType: 'canon-scout' }
)

let scenes = (disc && disc.scenes) || []
if (ONLY) scenes = scenes.filter(s => ONLY.includes(s.slug))
const todo = scenes.filter(s => !s.already_done)
log('chapter has ' + scenes.length + ' scene(s); ' + todo.length + ' to produce, ' + (scenes.length - todo.length) + ' already done')
if (!todo.length) return { chapter: CHAPTER, produced: [], note: 'all scenes already produced' }

phase('Produce')
const reports = []
for (const s of todo) {                 // SEQUENTIAL: the voice server is a single local model
  const sceneDir = ROOT + '/' + s.slug
  const r = await agent(
    'Produce the LIVE / dramatized audiobook for ONE scene, fully and autonomously, per your standing rules and the proven pipeline.\n' +
    'Scene: Chapter "' + CHAPTER + '", scene ' + s.n + ' -> ' + s.slug + '\n' +
    'Scene directory (create it; write cues.json + voice/ here): ' + sceneDir + '\n' +
    'Reference an already-produced scene for format/quality/conventions (READ it first): ' + ROOT + '/scene-01-no-signal/cues.json\n' +
    'Original scene prose -- adapt from THIS, faithfully:\n"""\n' + s.prose + '\n"""\n' +
    'SCENE BOUNDARY: adapt ONLY this prose. Do NOT recap the previous scene closing beat or pre-empt the next scene opening; begin at this prose first line and end at its last. (Recapping/overrunning duplicates audio when scenes are stitched.)\n' +
    'Run the WHOLE pipeline yourself: author ' + sceneDir + '/cues.json (all adaptation rules) -> Gemini gate against this exact prose, revise until CLEAN -> resolve/generate SFX + music + filters by scope (reuse book/chapter assets; generate only genuinely-new ones via ElevenLabs REST) -> render (scripts/render-voice-stems.py ' + sceneDir + '/cues.json ' + CRED + ') -> normalize (scripts/normalize-stems.py ' + sceneDir + '/cues.json) -> mix (scripts/mix-live-scene.py ' + sceneDir + '/cues.json) -> ' + sceneDir + '/scene-live.mp3.\n' +
    'Report (<120 words): cue sheet path, Gemini verdict + revisions, assets generated vs reused, final mp3 path + duration, and any blocker.',
    { label: 'scene:' + s.slug, phase: 'Produce', agentType: 'live-narration-director' }
  )
  reports.push({ slug: s.slug, report: r })
}
return { chapter: CHAPTER, produced: reports.map(x => x.slug), reports }
