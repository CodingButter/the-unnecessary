export const meta = {
  name: 'audio-roles-audit',
  description: 'Complete the crew-roles audit for the AUDIO side (the half that did not land in the first pass -- the book/editorial research filled the synthesis budget and truncated the audio streams). Web-research the standard roles in single-narrator AUDIOBOOK production and full-cast AUDIO-DRAMA / dramatized-audiobook production, inventory our 5 audio agents + the live-audio pipeline, then synthesize audio-side GAPS / OVERLOADED / OVER-FRAGMENTED, grounded + cited + prioritized. Writes docs/70-research/audio-roles-audit.md (companion to crew-roles-audit.md).',
  phases: [
    { title: 'Research+Inventory', detail: 'web-research audiobook + audio-drama production roles (parallel) + inventory the audio agents/pipeline' },
    { title: 'Synthesize', detail: 'audio-side gaps / splits / merges, grounded + prioritized; write the doc' },
  ],
}

const NOVEL = '/home/codingbutter/Novel'
async function tryAgent(make, tries) { tries = tries || 3; let last; for (let i = 0; i < tries; i++) { try { const r = await make(); if (r) return r; last = new Error('empty result'); } catch (e) { last = e; log('retry ' + (i + 1) + '/' + tries + ': ' + String(e).slice(0, 140)); } } throw last; }

const ROLES = {
  type: 'object', additionalProperties: false, required: ['domain', 'roles'],
  properties: {
    domain: { type: 'string' },
    roles: { type: 'array', items: { type: 'object', additionalProperties: false,
      properties: {
        role: { type: 'string' }, responsibilities: { type: 'string' }, why_it_matters: { type: 'string' },
        usually_its_own_role: { type: 'boolean' }, combined_with: { type: 'string' },
      }, required: ['role', 'responsibilities', 'why_it_matters', 'usually_its_own_role'] } },
    sources: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' },
  },
}
const INVENTORY = {
  type: 'object', additionalProperties: false, required: ['agents'],
  properties: {
    agents: { type: 'array', items: { type: 'object', additionalProperties: false,
      properties: { agent: { type: 'string' }, role: { type: 'string' }, scope: { type: 'string' }, spans: { type: 'array', items: { type: 'string' } } },
      required: ['agent', 'role', 'scope'] } },
    overlaps: { type: 'array', items: { type: 'string' } }, pipeline: { type: 'string' }, summary: { type: 'string' },
  },
}
const REPORT = { type: 'object', properties: { ok: { type: 'boolean' }, summary: { type: 'string' }, details: { type: 'string' } }, required: ['ok', 'summary'] }

const DOMAINS = [
  { key: 'audiobook', label: 'AUDIOBOOK PRODUCTION (single-narrator)',
    ask: 'Research the standard professional roles in producing a single-narrator AUDIOBOOK to a professional standard. Cover at least: narrator, audiobook director, producer, casting director, recording engineer, editor, prooflistener / QC, and mastering engineer, plus any others a serious production staffs. For EACH: responsibilities, why_it_matters (what it specifically CATCHES that the others do not), usually-its-own-role vs combined on smaller productions.' },
  { key: 'audiodrama', label: 'AUDIO DRAMA / FULL-CAST DRAMATIZED AUDIOBOOK / RADIO DRAMA',
    ask: 'Research the standard professional roles in producing an AUDIO DRAMA / full-cast dramatized audiobook / radio or podcast drama. Cover at least: adapter / dramatist, director, casting director, sound designer, composer / music supervisor, foley / SFX artist, dialogue editor, re-recording / mix engineer, mastering engineer, and showrunner / creative producer, plus any others proven important. For EACH: responsibilities, why_it_matters, usually-its-own-role vs combined.' },
]

phase('Research+Inventory')
log('audio-roles-audit: 2 audio-industry research streams + audio-crew inventory')
const researchThunks = DOMAINS.map(d => () => agent(
  `You are the research-consultant. RESEARCH ONLINE (WebSearch / WebFetch) the real-world professional roles in this audio-production domain and bring back CITED findings -- do not rely on memory alone.\n` +
  `DOMAIN: ${d.label}\n${d.ask}\n` +
  `Favor authoritative sources (APA/Audio Publishers Association, ACX/Audible production guides, audio-drama and radio-drama production handbooks, real production credits, SAG-AFTRA). Return per schema: domain, roles[] (role, responsibilities, why_it_matters, usually_its_own_role, combined_with), sources (the URLs you used), and a one-line summary. Be thorough; name every distinct role a serious production staffs.`,
  { schema: ROLES, agentType: 'research-consultant', label: 'research:' + d.key, phase: 'Research+Inventory' }
))
const inventoryThunk = () => agent(
  `Inventory the AUDIO side of the novel-production crew "The Unnecessary". Read these 5 agent charters under ${NOVEL}/.claude/agents/: audiobook-director.md, live-narration-director.md, sound-engineer.md, voice-designer.md, portrait-renderer.md (read the role-specific body; ignore the shared crew-handbook pointer). ALSO read the live-audio pipeline to understand the real production: ${NOVEL}/scripts/ (render-voice-stems, normalize-stems, mix-live-scene, stitch-chapter, embed-character-voice) and a sample cues.json under ${NOVEL}/audio/live-audio-book/**. For EACH agent return: agent, role, scope, spans (distinct concerns it bundles). Also return overlaps (audio agents whose scope overlaps) and pipeline (a 2-3 sentence description of how a live scene is actually produced today, stem by stem). Read-only. Per schema.`,
  { schema: INVENTORY, agentType: 'general-purpose', label: 'inventory:audio-crew', phase: 'Research+Inventory' }
)
const all = await parallel([...researchThunks, inventoryThunk])
const research = DOMAINS.map((d, i) => all[i]).filter(Boolean)
const inventory = all[DOMAINS.length] || { agents: [], overlaps: [], pipeline: '', summary: '(inventory failed)' }
log(`research: ${research.length}/${DOMAINS.length} audio domains; inventory: ${(inventory.agents || []).length} audio agents`)

phase('Synthesize')
const synth = await tryAgent(() => agent(
  `Synthesize the AUDIO-SIDE crew-vs-industry roles audit for the novel-production system "The Unnecessary" and WRITE it to ${NOVEL}/docs/70-research/audio-roles-audit.md (create it; YAML frontmatter: title, document_type "research", status "reference", authority "research-grounding", a one-line summary, tags, a related list that ONLY references files that EXIST -- e.g. "./crew-roles-audit.md", "../../.claude/agents/sound-engineer.md", "../../.claude/agents/live-narration-director.md" -- and source_documents pointing only at real paths, so it passes validate-metadata AND validate-links). This is the companion to docs/70-research/crew-roles-audit.md, which covered the book/editorial chain and explicitly deferred the audio side to this pass.\n\n` +
  `AUDIO INDUSTRY ROLES (researched, cited):\n${JSON.stringify(research).slice(0, 20000)}\n\n` +
  `OUR CURRENT AUDIO CREW + PIPELINE (inventory):\n${JSON.stringify(inventory).slice(0, 9000)}\n\n` +
  `We produce TWO audio products: a plain single-narrator chapter audiobook (audiobook-director authors the TTS performance script) and a full-cast LIVE / dramatized audiobook (live-narration-director authors a per-scene cue sheet, renders each line in-character on a local voice server, and the new sound-engineer owns music/SFX/mix design). Voices render on a LOCAL model (cost is power, not tokens). Produce three clearly-separated, PRIORITIZED sections, each item grounded in the cited research and aware of THIS pipeline:\n` +
  `1. GAPS -- audio-production roles proven important that we have NO agent for (candidate HIRES). For each: the role, what it would catch/add, how it fits our live-audio pipeline, priority (high/med/low), and whether an existing audio agent could absorb it instead. Pay special attention to: a casting director distinct from voice-designer; a dialogue editor / QC prooflistener (catches dropped lines, fluffs, bad takes, consistency across a chapter); and a mastering engineer (final loudness/consistency across the whole book vs per-scene mixing).\n` +
  `2. OVERLOADED -- audio agents bundling 2+ distinct industry roles (candidate SPLITS). The live-narration-director historically bundled adaptation + voice/casting direction + sound/mix; the sound-engineer already carved out sound design + mix. Assess whether the remaining director (dramatist/adapter + voice/casting director) should split further, or is right at our scale.\n` +
  `3. OVER-FRAGMENTED -- several audio agents doing one industry role (candidate MERGES), if any.\n` +
  `End with a short PRIORITIZED RECOMMENDATION (3-5 highest-value audio moves) and an explicit note of anything where our audio structure is BETTER than the industry default (e.g. local-model rendering, the canon-locked voice design). Cite sources. Recommendation only -- change no agent files.\n` +
  `Report (REPORT schema): ok, a summary naming the top audio gap(s) + any real split, and the doc path.`,
  { schema: REPORT, agentType: 'general-purpose', label: 'synthesize:audio-audit', phase: 'Synthesize' }
))

return { research, inventory, synthesis: synth, doc: 'docs/70-research/audio-roles-audit.md' }
