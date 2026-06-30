export const meta = {
  name: 'crew-roles-audit',
  description: 'Audit the agent crew against real-world professional roles. Web-research the standard roles in (a) book writing + editorial, (b) audiobook production, (c) audio-drama / full-cast dramatized-audiobook production; inventory our current agents; then synthesize GAPS (industry roles we lack), OVERLOADED agents (one agent doing 2+ distinct industry roles -> split), and OVER-FRAGMENTED cases (several agents doing one industry role -> merge), grounded + cited + prioritized. Writes docs/70-research/crew-roles-audit.md.',
  phases: [
    { title: 'Research+Inventory', detail: 'web-research industry roles for book/audiobook/audio-drama (parallel) + inventory our current crew' },
    { title: 'Synthesize', detail: 'gaps / overloaded(split) / over-fragmented(merge), grounded + prioritized; write the recommendation doc' },
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
        role: { type: 'string' },                  // the professional role/title
        responsibilities: { type: 'string' },       // what it owns
        why_it_matters: { type: 'string' },          // what it CATCHES / adds that others miss -- the case for it being its own role
        usually_its_own_role: { type: 'boolean' },   // true if the industry keeps it a distinct specialist; false if often combined
        combined_with: { type: 'string' },           // roles it is commonly merged with on smaller productions
      }, required: ['role', 'responsibilities', 'why_it_matters', 'usually_its_own_role'] } },
    sources: { type: 'array', items: { type: 'string' } },   // cited URLs / references
    summary: { type: 'string' },
  },
}

const INVENTORY = {
  type: 'object', additionalProperties: false, required: ['agents'],
  properties: {
    agents: { type: 'array', items: { type: 'object', additionalProperties: false,
      properties: {
        agent: { type: 'string' },                   // file/name
        role: { type: 'string' },                    // its one-line role
        scope: { type: 'string' },                   // what it actually does (from its charter)
        spans: { type: 'array', items: { type: 'string' } }, // distinct concerns it bundles (for spotting too-many-hats)
      }, required: ['agent', 'role', 'scope'] } },
    overlaps: { type: 'array', items: { type: 'string' } },   // pairs/sets of agents whose scope overlaps
    summary: { type: 'string' },
  },
}

const REPORT = { type: 'object', properties: { ok: { type: 'boolean' }, summary: { type: 'string' }, details: { type: 'string' } }, required: ['ok', 'summary'] }

const DOMAINS = [
  { key: 'book', label: 'BOOK WRITING + EDITORIAL (a literary novel)',
    ask: 'Research the standard professional roles in writing, editing, and preparing a literary NOVEL for publication (craft/editorial, NOT business/marketing). Cover at least: author/writer, developmental/structural editor, line editor, copy editor, proofreader, story/continuity editor, researcher/fact-checker, beta readers, sensitivity/authenticity reader, and any others proven important. For EACH: responsibilities, why_it_matters (what it specifically CATCHES that the others do not), whether it is usually its own role vs combined.' },
  { key: 'audiobook', label: 'AUDIOBOOK PRODUCTION (single-narrator)',
    ask: 'Research the standard professional roles in producing a single-narrator AUDIOBOOK. Cover at least: narrator, audiobook director, producer, casting, recording/recording engineer, editor, prooflistener/QC, and mastering engineer, plus any others proven important. For EACH: responsibilities, why_it_matters, usually-its-own-role vs combined.' },
  { key: 'audiodrama', label: 'AUDIO DRAMA / FULL-CAST DRAMATIZED AUDIOBOOK / RADIO DRAMA',
    ask: 'Research the standard professional roles in producing an AUDIO DRAMA / full-cast dramatized audiobook / radio drama / podcast drama. Cover at least: adapter/dramatist, director, casting director, sound designer, composer / music supervisor, foley / SFX artist, dialogue editor, re-recording / mix engineer, mastering, and showrunner / creative producer, plus any others proven important. For EACH: responsibilities, why_it_matters, usually-its-own-role vs combined.' },
]

// ---- Research (3 web streams) + Inventory (our crew), all in parallel ----
phase('Research+Inventory')
log('crew-roles-audit: 3 industry-research streams + crew inventory')
const researchThunks = DOMAINS.map(d => () => agent(
  `You are the research-consultant. RESEARCH ONLINE (WebSearch / WebFetch) the real-world professional roles in this domain and bring back cited findings -- do not rely on memory alone.\n` +
  `DOMAIN: ${d.label}\n${d.ask}\n` +
  `Favor authoritative sources (industry orgs, professional guides, production credits, audio-drama/audiobook production handbooks). Return per schema: domain, roles[] (role, responsibilities, why_it_matters, usually_its_own_role, combined_with), sources (the URLs you used), and a one-line summary. Be thorough; name every distinct role a serious production staffs.`,
  { schema: ROLES, agentType: 'research-consultant', label: 'research:' + d.key, phase: 'Research+Inventory' }
))
const inventoryThunk = () => agent(
  `Inventory the agent crew of the novel-production system "The Unnecessary". Read every .claude/agents/*.md under ${NOVEL}. For EACH agent return: agent (name), role (its one-line job), scope (what it actually does, from its charter -- read the role-specific body, ignore any shared crew-handbook pointer / boilerplate), and spans (the list of DISTINCT concerns it bundles, so we can spot an agent wearing too many hats). Also return overlaps: sets of agents whose responsibilities overlap. Read-only. Per schema.`,
  { schema: INVENTORY, agentType: 'general-purpose', label: 'inventory:crew', phase: 'Research+Inventory' }
)
const all = await parallel([...researchThunks, inventoryThunk])
const research = DOMAINS.map((d, i) => all[i]).filter(Boolean)
const inventory = all[DOMAINS.length] || { agents: [], overlaps: [], summary: '(inventory failed)' }
log(`research: ${research.length}/${DOMAINS.length} domains; inventory: ${(inventory.agents || []).length} agents`)

// ---- Synthesize: map crew vs industry -> gaps / splits / merges ----
phase('Synthesize')
const synth = await tryAgent(() => agent(
  `Synthesize a CREW-vs-INDUSTRY roles audit for the novel-production system "The Unnecessary" and WRITE it to ${NOVEL}/docs/70-research/crew-roles-audit.md (create it; add proper YAML frontmatter: title, document_type "research", status "reference", authority "research-grounding", a one-line summary, tags, related, source_documents -- so it passes validate-metadata).\n\n` +
  `INDUSTRY ROLES (researched, cited):\n${JSON.stringify(research).slice(0, 14000)}\n\n` +
  `OUR CURRENT CREW (inventory):\n${JSON.stringify(inventory).slice(0, 8000)}\n\n` +
  `Produce three clearly-separated, PRIORITIZED sections, each item grounded in the research (cite the industry role it maps to) and aware of our actual pipeline (we draft chapters through a gauntlet + adjudicator; we produce a single-narrator audiobook and a full-cast LIVE audiobook with the live-narration-director + the new sound-engineer):\n` +
  `1. GAPS -- industry roles proven important that we have NO agent for (candidate HIRES). For each: the role, what it would catch/add, how it fits our pipeline, priority (high/med/low), and whether an existing agent could absorb it instead.\n` +
  `2. OVERLOADED -- our agents that bundle what the industry treats as 2+ DISTINCT roles (candidate SPLITS). For each: the agent, the distinct roles it is wearing, the risk of one generalist doing each shallowly, and the recommended split (or why keeping it combined is fine at our scale).\n` +
  `3. OVER-FRAGMENTED -- places where SEVERAL of our agents do what is really ONE industry role (candidate MERGES), if any. For each: the agents, the single role, and whether merging helps or the separation is deliberate/valuable.\n` +
  `End with a short PRIORITIZED RECOMMENDATION (the 3-5 highest-value moves) and an explicit note of anything where our structure is BETTER than the industry default (do not recommend change for its own sake). Cite sources. This is a recommendation for the author to review -- do not change any agent files.\n` +
  `Report (REPORT schema): ok, a summary naming the top gaps + the top split, and the doc path.`,
  { schema: REPORT, agentType: 'general-purpose', label: 'synthesize:audit', phase: 'Synthesize' }
))

return { research, inventory, synthesis: synth, doc: 'docs/70-research/crew-roles-audit.md' }
