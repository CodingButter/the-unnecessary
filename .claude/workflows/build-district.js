export const meta = {
  name: 'build-district',
  description: "Build a district's geography entity system per docs/00-governance/entity-spec.md: scout established canon, stand up the parser + validator rails and per-type scaling templates, author the named district as a grounded fractal entity tree, validate to green and generate the derived map, then adversarially audit the tree for fabrication/contradiction. The district is parameterized via args {slug, name}; each phase is run by the matching crew specialist (canon-scout, systems-engineer, entity-author, continuity-auditor).",
  phases: [
    { title: 'Ground', detail: 'canon-scout inventories established geography for the target district' },
    { title: 'Rails', detail: 'systems-engineer builds the entity_graph parser + validate-geography; entity-author writes per-type templates' },
    { title: 'Populate', detail: 'entity-author authors the target district as a grounded entity tree' },
    { title: 'Verify', detail: 'systems-engineer validates to green + generates the derived map' },
    { title: 'Audit', detail: 'continuity-auditor adversarially checks the tree for fabrication/contradiction' },
  ],
}

const ROOT = '/home/codingbutter/Novel'
const SPEC = 'docs/00-governance/entity-spec.md'

// ---- Parameters (passed as Workflow args: {slug, name}) ----
let a = args || {}
if (typeof a === 'string') { try { a = JSON.parse(a) } catch (e) { a = {} } }
const districtSlug = a.slug || a.district || null
const districtName = a.name || a.title || (districtSlug ? districtSlug.replace(/-/g, ' ') : null)
if (!districtSlug) {
  throw new Error('build-district requires args {slug, name}, for example {"slug":"elis-neighborhood","name":"Elis neighborhood"} or {"slug":"cass-corridor","name":"Cass Corridor"}')
}

const INVENTORY = { type: 'object', required: ['established', 'file_layout', 'placement', 'stubs'], properties: {
  established: { type: 'string', description: "Every piece of geography ESTABLISHED in Book 1 canon so far: named streets, corners/intersections, named places (Eli's shop/Northglass, Lena's clinic, the grocery, the mesh hub, etc.), the district(s) + withdrawal status, and any stated distances/travel-times. Cite a source file for each (Ch1/Ch2 manuscript, blueprints, world/location files, master timeline). Mark canon vs merely implied." },
  file_layout: { type: 'string', description: "The existing docs/20-canon/world/ structure: what files/dirs exist, and any existing elis-neighborhood/location files the new tree must integrate with rather than duplicate." },
  placement: { type: 'string', description: "Recommended root path + folder convention for the new fractal entity tree (city/district/building/room per the spec), and how to reconcile with existing world files (extend/link, never delete existing canon)." },
  stubs: { type: 'string', description: "Which entities the story has NOT looked at yet (leave as stubs) vs which are established enough to flesh out." },
} }

const AUDIT = { type: 'object', required: ['grounded', 'issues'], properties: {
  grounded: { type: 'boolean', description: "true ONLY if every authored geography fact traces to established canon or is a clearly-marked just-in-time stub, with nothing invented that contradicts Ch1/Ch2, the blueprints, or the master timeline." },
  issues: { type: 'array', items: { type: 'object', properties: { file: { type: 'string' }, problem: { type: 'string' }, severity: { type: 'string' } } }, description: "Any fabrication, contradiction, or spec violation. Empty if clean." },
  summary: { type: 'string' },
} }

phase('Ground')
log(`build-district: "${districtName}" (slug ${districtSlug})`)
const [inventory, rails, templates] = await parallel([
  () => agent(
    `Scout the EXISTING canon of "The Unnecessary" (repo ${ROOT}) for the established geography of the district "${districtName}" (slug ${districtSlug}), to ground a new geography entity tree. Read the geography + time/state sections of ${ROOT}/${SPEC} first. Determine exactly what this district has ESTABLISHED -- named streets, corners/intersections, named places, the district + withdrawal status, and any stated distances/travel-times -- and the existing docs/20-canon/world/ file layout the new tree must integrate with rather than duplicate. Recommend the root path + folder convention for the new fractal tree. Cite a source file for every fact; distinguish canon from merely implied. Write NO files. Return per the schema.`,
    { agentType: 'canon-scout', schema: INVENTORY, label: 'ground', phase: 'Ground' }
  ),
  () => agent(
    `Build the GEOGRAPHY RAILS for "The Unnecessary" (repo ${ROOT}), implementing ${ROOT}/${SPEC}. Two scripts:\n\n1) ${ROOT}/scripts/entity_graph.py -- shared parser/walker. Walks entity markdown files, parses frontmatter + the fenced \`\`\`yaml edge block(s), builds the CONTAINMENT tree (from each child's parent edge AND its folder location, which must agree) and the EDGE graph (directional + symmetric). Provides importable functions to: resolve linear-reference ADDRESSES (addressed-to: {street, between:[A,B], along, side}); compute shortest-path DISTANCES over segments (each segment owns street/from/to/length_m once); derive children/contents and "what's on a street"; and resolve an entity's state AS OF an in-world date by replaying its timeline events.\n\n2) ${ROOT}/scripts/validate-geography.py -- validator importing entity_graph. Per spec section 11: referential integrity; folder/parent cross-check; containment acyclicity; network consistency (segment length single-source; from/to exist; addresses resolve with along in [0,1]; no contradictory route distances); symmetric reciprocity; zero-blanks WITHIN declared sections (stubs allowed); reveal-tag respect. Print a clear PASS/FAIL summary like the existing validators. It MUST pass on an empty/just-stubs tree.\n\nAST-parse both. Return UNDER 120 words: public functions + checks, and confirm both parse.`,
    { agentType: 'systems-engineer', label: 'rails', phase: 'Rails' }
  ),
  () => agent(
    `Create the per-type SCALING TEMPLATES for the geography entity system of "The Unnecessary" (repo ${ROOT}), implementing ${ROOT}/${SPEC} (read sections 2, 3, 6, 7, 9 first). One template markdown file per geography entity TYPE under ${ROOT}/docs/20-canon/world/_templates/ : district, street, intersection, segment, building, room, object. Each template shows: frontmatter (entity_type, status, authority, the parent containment edge); prose body sections appropriate to the type (a CEILING not a floor -- fillable as deep or shallow as a scene needs); and a fenced \`\`\`yaml block with that type's edges + an optional timeline (keyed to in-world date). Show the addressed-to linear-reference shape on building; the street/from/to/length_m + connects shape on segment/intersection. Each template is itself a one-line-placeholder STUB so it doubles as a copyable starting point. Match the quality of ${ROOT}/docs/40-blueprints/_templates/chapter-blueprint-template.md. Return UNDER 100 words: templates created + key fields each carries.`,
    { agentType: 'entity-author', label: 'templates', phase: 'Rails' }
  ),
])
const inv = inventory || { established: '(scout failed)', file_layout: '', placement: '', stubs: '' }

phase('Populate')
const populate = await agent(
  `Author the district "${districtName}" (slug ${districtSlug}) as a geography entity tree for "The Unnecessary" (repo ${ROOT}), implementing ${ROOT}/${SPEC} and using the templates in ${ROOT}/docs/20-canon/world/_templates/.\n\nGROUND STRICTLY in this canon inventory. Do NOT invent geography that contradicts it; where canon is silent, create a minimal one-line STUB, never fabricated detail:\nESTABLISHED:\n${inv.established}\n\nEXISTING FILE LAYOUT (integrate with, do NOT delete or duplicate existing canon):\n${inv.file_layout}\n\nPLACEMENT:\n${inv.placement}\n\nSTUB vs FLESH:\n${inv.stubs}\n\nBuild the fractal tree per the spec: the city -> "${districtName}" (district, withdrawal status in prose) -> the established PLACES as building entities (each with a parent edge to the district and an addressed-to linear-reference) -> the INTERSECTIONS + SEGMENTS connecting them (length_m ONLY where canon gives/strongly implies a distance; otherwise omit length or mark approximate -- never fabricate precise distances). Use the file+sibling-folder convention; parent on the child; fenced yaml edge blocks. Flesh out only what canon established for this district; everything else is a one-line stub. Return UNDER 150 words: the tree created (path list), grounded vs stubbed, and any canon-forced judgment call.`,
  { agentType: 'entity-author', label: 'populate', phase: 'Populate' }
)

phase('Verify')
const verify = await agent(
  `Verify and finalize the "${districtName}" geography foundation in ${ROOT}. (1) Run \`python3 scripts/validate-geography.py\`, \`python3 scripts/validate-metadata.py\`, \`python3 scripts/validate-links.py\`; FIX every error in the new geography files or the scripts until ALL THREE pass -- fix the real problem, never weaken a check to pass it. (2) Then write ${ROOT}/scripts/build-geo-map.py (stdlib, importing entity_graph) that DERIVES and writes a generated view -- a Mermaid street-network map + a containment tree + a "what's on each street" index -- into ${ROOT}/docs/20-canon/world/_generated/ each with a "DO NOT EDIT - generated" banner; run it. Return UNDER 130 words: final validator results (quote the PASS lines), what the map generator produced, and what you fixed.`,
  { agentType: 'systems-engineer', label: 'verify', phase: 'Verify' }
)

phase('Audit')
const audit = await agent(
  `Adversarially AUDIT the newly-authored "${districtName}" geography tree under ${ROOT}/docs/20-canon/world/** against established canon. Read the new entity files, then Ch1/Ch2 manuscript (${ROOT}/docs/50-manuscript/book-1/**), blueprints (${ROOT}/docs/40-blueprints/book-1/**), and the master timeline (${ROOT}/docs/20-canon/timeline/**). Catch any FABRICATION (a street, distance, place, or detail invented and stated as canon that the source does not support) or CONTRADICTION (geography conflicting with Ch1/Ch2). A clearly-marked just-in-time stub is fine; an invented precise fact is not. Be skeptical and specific. Return per the schema.`,
  { agentType: 'continuity-auditor', schema: AUDIT, label: 'audit', phase: 'Audit' }
)

return { district: { slug: districtSlug, name: districtName }, inventory: inv, rails, templates, populate, verify, audit }
