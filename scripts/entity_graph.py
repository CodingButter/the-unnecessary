#!/usr/bin/env python3
"""Shared entity-graph parser/walker for The Unnecessary.

Standard library only. No third-party imports, no pip installs. No side effects
on import: the module only defines constants, classes, and functions; nothing
walks the disk until a caller invokes build_graph().

This module is the single reader of the entity tree described in
docs/00-governance/entity-spec.md. It is the geography sibling of
scripts/characters_graph.py and is meant to serve every entity family that
follows the universal contract (places, the street network, items, factions,
events). Two tools consume it today:

  - scripts/validate-geography.py        (the geography rails / validator)
  - (future) view generators             (street map, route tables, indexes)

What an entity file is (entity-spec.md sections 2-4):

  - One markdown file per entity. Three parts:
      * frontmatter (yaml)  -> title, entity_type, status, authority, `parent`
        (the single CONTAINMENT edge, stored on the child), summary, tags.
      * prose body          -> ## sections, hand-edited narrative canon.
      * a fenced ```yaml block holding structured facts and the non-containment
        EDGES: directional (`owner`, `addressed-to`, ...) and symmetric
        (`connects`, `neighbor`, ...), plus network facts a segment owns once
        (`street`, `from`, `to`, `length_m`) and a `home` + `timeline` for the
        entity's state through in-world time.

Because the stdlib ships no YAML parser, this module carries a compact,
dependency-free YAML *subset* parser (parse_yaml) sufficient for frontmatter and
the fenced blocks: block maps and sequences (indent-structured), inline flow maps
`{ a: 1, b: [x, y] }` and flow sequences `[x, y]`, quoted and bare scalars,
ISO dates kept as strings, `# ` comments. It is deliberately small, not a
general YAML engine; it parses what the spec authors write.

Two derived structures, never stored, always walked (spec section 5):

  CONTAINMENT TREE   built from each child's `parent` edge AND its folder home,
                     which must AGREE (spec section 3's free cross-check). The
                     child-list of any entity is literally the contents of its
                     same-named sibling folder; parents never list children.
  EDGE GRAPH         every non-containment relationship, directional or symmetric,
                     read from the fenced ```yaml `edges:` block.

Public surface (importable, no side effects):

  parse_yaml(text)                      -> dict/list/scalar (the subset parser)
  split_frontmatter(text)               -> (frontmatter_text, body_text)
  extract_yaml_blocks(body)             -> [block_text, ...]  (fenced ```yaml)
  parse_entity(path, root)              -> Entity
  build_graph(geography_dir=...)        -> EntityGraph   (walks the tree)

  EntityGraph methods:
    resolve(ref)                        bare id OR rel-path -> canonical key
    get(ref)                            -> Entity or None
    containment_parent(key)             the agreed parent (declared/folder)
    children_of(key) / descendants_of(key)
    ancestors_of(key)                   walk parents upward (acyclic when valid)
    directional_links() / symmetric_links()
    segments() / streets()              network entities
    whats_on_street(street_ref)         addresses sitting on a street's segments
    resolve_address(addr)               linear reference -> AddressResolution
    address_distance(a, b)              shortest path over segments (metres)
    shortest_path_distance(node_a, node_b)
    state_as_of(ref, when)              replay the timeline to an in-world date
    location_of(ref, when)              convenience: where it is on that date

Graceful degradation is a contract. A missing tree yields an empty graph with a
warning, never a crash. Legacy files that are not entities (no `entity_type`, no
fenced block, no `parent`) are skipped, not failed on.
"""

import os
import re
import heapq
from datetime import date


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

# The geography entity tree root. The legacy story-bible location files under
# docs/20-canon/world/locations/ were PROMOTED IN PLACE to entity files (spec
# section 7): the city greater-detroit.md sits at the root, and districts,
# buildings, rooms, and objects nest in same-named sibling folders beneath it.
# Files in this tree that are not entities -- no entity_type, no parent, no fenced
# yaml block, e.g. mars-sites.md and the index.md files -- are skipped, not failed
# on. An absent or empty tree is valid; the rails must pass on nothing-yet.
GEOGRAPHY_DIR = os.path.join(REPO_ROOT, "docs", "20-canon", "world", "locations")

# Other entity domains the geography graph must RESOLVE into but does not itself
# validate. A building's `owner`/`landlord` and a person's `residence` cross the
# geography/character seam (entity-spec sections 4 and 12): people are not spatially
# contained, so they live in their own area in a format the character tooling owns.
# We register their identities -- the filename stem `lastname-firstname`, exactly
# what the geography edges name -- as resolution-only externals, so cross-tree edge
# targets resolve without subjecting the character files to the geography rails.
CHARACTER_PROFILES_DIR = os.path.join(
    REPO_ROOT, "docs", "20-canon", "characters", "profiles"
)

# Book One opens on this date (CLAUDE.md: October 3 to November 1, 2053). When a
# caller asks for "current" state without a date, this is the natural t=0.
BOOK_ONE_START = date(2053, 10, 3)

# ---------------------------------------------------------------------------
# Controlled relationship vocabulary (entity-spec.md section 4). Two legal
# classes, same model the character system uses, extended for geography.
#
#   DIRECTIONAL  stored ONCE on the dependent end, pointing at the authority.
#                The inverse is DERIVED by traversal, never written. `creator-of`
#                is the single authority-stored exception. `parent` is the
#                containment edge and lives in FRONTMATTER, not the edges block,
#                but is listed here so the same machine classifies it.
#   SYMMETRIC    written on BOTH ends and reciprocity-checked (`connects`,
#                `neighbor`, the inherited social set).
#
# `addressed-to` is directional AND structured: its value is a linear-reference
# mapping { street, between:[A,B], along, side }, not a bare id. Off-vocabulary
# labels are rejected by the validator; freeform nuance goes in prose.
# ---------------------------------------------------------------------------

# relation -> (storer_end, derived_inverse_label)
DIRECTIONAL_META = {
    "parent":       ("dependent", "child"),       # containment (frontmatter)
    "owner":        ("dependent", "owns"),
    "landlord":     ("dependent", "tenant"),
    "residence":    ("dependent", "resident"),    # person -> building
    "located-in":   ("dependent", "contains"),    # movable thing -> container
    "addressed-to": ("dependent", "address-of"),  # building -> street position
    "father":       ("dependent", "child"),
    "mother":       ("dependent", "child"),
    "guardian":     ("dependent", "ward"),
    "employer":     ("dependent", "employee"),
    "reports-to":   ("dependent", "direct-report"),
    "mentor":       ("dependent", "mentee"),
    "patient-of":   ("dependent", "patient"),
    "creator-of":   ("authority", "created-by"),
}
DIRECTIONAL_RELATIONS = set(DIRECTIONAL_META)

SYMMETRIC_RELATIONS = {
    "connects", "neighbor", "spouse", "former-spouse", "sibling", "friend",
    "rival", "adversary", "colleague", "partner", "acquaintance",
}

VOCAB = DIRECTIONAL_RELATIONS | SYMMETRIC_RELATIONS

# Edge relations whose value is a structured mapping, not a bare id / id-list.
STRUCTURED_RELATIONS = {"addressed-to"}

# The containment edge is special-cased: it lives in frontmatter and drives the
# folder tree, so it is excluded from the generic edges-block walk.
CONTAINMENT_RELATION = "parent"

# Geography entity types. PLACES ride the folder tree (single-parent
# containment); the NETWORK types are positioned by edges, not containment, so
# they are exempt from the folder/parent cross-check.
PLACE_TYPES = {"city", "district", "building", "place", "room", "object"}
NETWORK_TYPES = {"intersection", "segment", "street"}

# Reveal-tagging (spec section 11). A bracketed tag must be one of these forms.
REVEAL_TAG_RE = re.compile(r"\[([^\]]+)\]")
VALID_REVEAL_RE = re.compile(
    r"^(open|behavior-only|reveal:\s*book\s+\w+)$", re.IGNORECASE
)

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
    "december": 12,
}
ISO_DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
MONTH_DATE_RE = re.compile(r"([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})")


# ===========================================================================
# A compact, dependency-free YAML *subset* parser.
#
# Supports exactly what entity files use: block maps and sequences structured by
# indentation, inline flow maps `{ k: v }` and sequences `[a, b]`, quoted and
# bare scalars (ints, floats, bools, null, ISO dates kept as strings), and `# `
# comments. It is intentionally minimal; it is not a general YAML engine.
# ===========================================================================


def _strip_comment(line):
    """Drop a trailing/whole-line `#` comment, honoring quotes."""
    quote = None
    out = []
    for index, char in enumerate(line):
        if quote:
            out.append(char)
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
            out.append(char)
            continue
        if char == "#" and (index == 0 or line[index - 1] in " \t"):
            break
        out.append(char)
    return "".join(out).rstrip()


def _logical_lines(text):
    """(indent, content) for every non-blank, comment-stripped line."""
    items = []
    for raw in text.splitlines():
        line = _strip_comment(raw)
        if line.strip() == "":
            continue
        indent = len(line) - len(line.lstrip(" "))
        items.append((indent, line.strip()))
    return items


def _split_kv(text):
    """Split `key: value` at the first top-level `:` followed by space/EOL.

    Returns (key, separator, value); separator is ':' on a hit, '' otherwise.
    Honors quotes and bracket nesting so a colon inside `{...}`, `[...]`, or a
    quoted string is never mistaken for the key separator.
    """
    depth = 0
    quote = None
    for index, char in enumerate(text):
        if quote:
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
            continue
        if char in "[{":
            depth += 1
            continue
        if char in "]}":
            depth -= 1
            continue
        if char == ":" and depth == 0:
            if index + 1 >= len(text) or text[index + 1] in " \t":
                return text[:index], ":", text[index + 1:]
    return text, "", ""


def _scalar(text):
    """Coerce a bare scalar token to int/float/bool/None, else a clean string."""
    text = text.strip()
    if len(text) >= 2 and (
        (text[0] == '"' and text[-1] == '"')
        or (text[0] == "'" and text[-1] == "'")
    ):
        return text[1:-1]
    lowered = text.lower()
    if lowered in ("", "null", "~"):
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"[+-]?\d+", text):
        try:
            return int(text)
        except ValueError:
            pass
    if re.fullmatch(r"[+-]?\d*\.\d+", text):
        try:
            return float(text)
        except ValueError:
            pass
    return text


def _split_flow(inner):
    """Split flow-collection contents on top-level commas (honoring nesting)."""
    items = []
    depth = 0
    quote = None
    cur = ""
    for char in inner:
        if quote:
            cur += char
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
            cur += char
            continue
        if char in "[{":
            depth += 1
            cur += char
            continue
        if char in "]}":
            depth -= 1
            cur += char
            continue
        if char == "," and depth == 0:
            items.append(cur)
            cur = ""
            continue
        cur += char
    if cur.strip() != "":
        items.append(cur)
    return items


def _parse_flow_map(text):
    text = text.strip()
    inner = text[1:-1] if text.startswith("{") and text.endswith("}") else text
    result = {}
    for part in _split_flow(inner):
        key, sep, val = _split_kv(part.strip())
        if not sep:
            continue
        result[_scalar(key.strip())] = _parse_value(val.strip())
    return result


def _parse_flow_seq(text):
    text = text.strip()
    inner = text[1:-1] if text.startswith("[") and text.endswith("]") else text
    return [_parse_value(p.strip()) for p in _split_flow(inner) if p.strip() != ""]


def _parse_value(text):
    text = text.strip()
    if text == "":
        return None
    if text[0] == "{":
        return _parse_flow_map(text)
    if text[0] == "[":
        return _parse_flow_seq(text)
    return _scalar(text)


class _Cursor:
    """A forward-only cursor over (indent, content) logical lines."""

    def __init__(self, items):
        self.items = items
        self.index = 0

    def peek(self):
        return self.items[self.index] if self.index < len(self.items) else None

    def advance(self):
        self.index += 1


def parse_yaml(text):
    """Parse the YAML subset used by entity files into Python data.

    Returns a dict for a mapping document, a list for a sequence document, a
    scalar for a lone scalar, or {} for an empty document. Never raises on the
    shapes entity files use; malformed input degrades to partial data.
    """
    cursor = _Cursor(_logical_lines(text))
    if cursor.peek() is None:
        return {}
    parsed = _parse_block(cursor, -1)
    return parsed if parsed is not None else {}


def _parse_block(cursor, parent_indent):
    """Parse the block whose lines are indented deeper than parent_indent."""
    line = cursor.peek()
    if line is None:
        return None
    indent, content = line
    if indent <= parent_indent:
        return None
    if content.startswith("- ") or content == "-":
        return _parse_seq(cursor, indent)
    return _parse_map(cursor, indent)


def _parse_map(cursor, indent):
    result = {}
    while True:
        line = cursor.peek()
        if line is None:
            break
        ind, content = line
        if ind != indent or content.startswith("- ") or content == "-":
            break
        key, sep, val = _split_kv(content)
        if not sep:
            break
        cursor.advance()
        val = val.strip()
        if val == "":
            result[_scalar(key.strip())] = _parse_block(cursor, indent)
        else:
            result[_scalar(key.strip())] = _parse_value(val)
    return result


def _parse_seq(cursor, indent):
    result = []
    while True:
        line = cursor.peek()
        if line is None:
            break
        ind, content = line
        if ind != indent or not (content.startswith("- ") or content == "-"):
            break
        cursor.advance()
        item = content[1:].strip()
        if item == "":
            result.append(_parse_block(cursor, indent))
            continue
        key, sep, val = _split_kv(item)
        if sep:
            # A mapping item: first key sits inline on the dash line; any further
            # keys of the same item live one column deeper (the content column).
            mapping = {}
            val = val.strip()
            if val == "":
                mapping[_scalar(key.strip())] = _parse_block(cursor, indent + 1)
            else:
                mapping[_scalar(key.strip())] = _parse_value(val)
            continuation = _parse_block(cursor, indent)
            if isinstance(continuation, dict):
                mapping.update(continuation)
            result.append(mapping)
        else:
            result.append(_parse_value(item))
    return result


# ===========================================================================
# File splitting: frontmatter, prose body, fenced ```yaml blocks.
# ===========================================================================


def _read(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def split_frontmatter(text):
    """Return (frontmatter_text, body_text). Empty frontmatter when absent."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                return "\n".join(lines[1:index]), "\n".join(lines[index + 1:])
    return "", text


FENCE_RE = re.compile(r"```[ \t]*ya?ml[ \t]*\r?\n(.*?)\r?\n[ \t]*```", re.DOTALL)


def extract_yaml_blocks(body):
    """Return the contents of every fenced ```yaml block in a prose body."""
    return [match.group(1) for match in FENCE_RE.finditer(body)]


# ===========================================================================
# Date / timeline helpers (spec section 9).
# ===========================================================================


def parse_when(value):
    """Parse a timeline `when` into a datetime.date, or None.

    Accepts an ISO `YYYY-MM-DD`, a `Month D, YYYY`, or an approximate
    `{ circa: 2050 }` mapping (resolved to Jan 1 of that year).
    """
    if value is None:
        return None
    if isinstance(value, dict):
        circa = value.get("circa")
        if circa is None:
            return None
        match = re.search(r"\d{4}", str(circa))
        if not match:
            return None
        try:
            return date(int(match.group(0)), 1, 1)
        except ValueError:
            return None
    if isinstance(value, date):
        return value
    text = str(value)
    iso = ISO_DATE_RE.search(text)
    if iso:
        try:
            return date(int(iso.group(1)), int(iso.group(2)), int(iso.group(3)))
        except ValueError:
            return None
    month = MONTH_DATE_RE.search(text)
    if month:
        num = MONTHS.get(month.group(1).lower())
        if num:
            try:
                return date(int(month.group(3)), num, int(month.group(2)))
            except ValueError:
                return None
    return None


def _coerce_date(value):
    if value is None or isinstance(value, date):
        return value
    return parse_when(value)


# ===========================================================================
# Data carriers.
# ===========================================================================


class Edge:
    """One non-containment relationship edge authored on a source entity.

    `target` is the raw reference string for simple edges. For a structured
    edge (`addressed-to`) `payload` holds the linear-reference mapping and
    `target` is the street it names. `target_key` is the resolved canonical key,
    filled in by the graph builder, or None when unresolved.
    """

    def __init__(self, source_key, relation, target, payload=None):
        self.source_key = source_key
        self.relation = relation
        self.target = target
        self.payload = payload
        self.target_key = None

    @property
    def in_vocab(self):
        return self.relation in VOCAB

    @property
    def is_directional(self):
        return self.relation in DIRECTIONAL_RELATIONS

    @property
    def is_symmetric(self):
        return self.relation in SYMMETRIC_RELATIONS

    @property
    def is_structured(self):
        return self.relation in STRUCTURED_RELATIONS


class Entity:
    """A parsed entity file plus its derived facts."""

    def __init__(self, key, path):
        self.key = key                 # canonical id == rel-path under the root
        self.path = path
        self.entity_id = key.rsplit("/", 1)[-1]   # bare filename-stem id
        self.rel_path = key
        self.frontmatter = {}
        self.data = {}                 # merged fenced ```yaml block(s)
        self.title = None
        self.entity_type = None
        self.status = None
        self.declared_parent = None    # `parent:` from frontmatter (raw ref)
        self.parent_from_folder = None # bare id implied by the folder home
        self.edges = []
        # Network facts a segment owns once (spec section 7).
        self.street = None
        self.seg_from = None
        self.seg_to = None
        self.length_m = None
        # Time/state (spec section 9).
        self.home = None
        self.timeline = []
        # Prose completeness.
        self.present_sections = set()
        self.empty_sections = set()
        # Reveal tags found anywhere structural.
        self.reveal_tags = []
        # Did this file parse as an entity at all?
        self.is_entity = False
        self.parse_error = None
        # Resolved containment parent key, filled by the builder.
        self.parent_key = None

    @property
    def is_network(self):
        return self.entity_type in NETWORK_TYPES

    @property
    def is_segment(self):
        return self.entity_type == "segment" or (
            self.seg_from is not None and self.seg_to is not None
        )

    @property
    def is_stub(self):
        """A stub: no edges, no network facts, no timeline -- frontmatter + prose."""
        return not self.edges and not self.is_segment and not self.timeline


class ExternalRef:
    """A resolution-only stand-in for an entity owned by ANOTHER domain.

    Geography edges legitimately point out of the spatial tree -- a building's
    `owner` or a person's `residence` names a character. Characters live in their
    own area, in a format the character tooling parses and validates; the geography
    rails only need their identity to EXIST so the reference resolves. An ExternalRef
    carries just that (a bare-id key and the domain it came from) and is never
    iterated by the geography checks: the validator walks `graph.entities`, while
    externals live in `graph.externals` and are reachable only through `resolve`.
    """

    def __init__(self, key, domain):
        self.key = key
        self.entity_id = key
        self.domain = domain
        self.is_external = True


class AddressResolution:
    """The result of resolving an `addressed-to` linear reference."""

    def __init__(self, addr):
        self.addr = addr
        self.street = None          # raw street ref
        self.between = []           # [raw A, raw B]
        self.along = None
        self.side = None
        self.segment = None         # the resolved Entity, or None
        self.node_from = None       # resolved key of the segment's `from`
        self.node_to = None         # resolved key of the segment's `to`
        self.length = None
        self.dist_from = None       # metres from this address to node_from
        self.dist_to = None         # metres from this address to node_to

    @property
    def resolved(self):
        return self.segment is not None

    @property
    def along_in_range(self):
        return isinstance(self.along, (int, float)) and 0.0 <= self.along <= 1.0


# ===========================================================================
# Entity parsing.
# ===========================================================================


def _rel_key(path, root):
    """Canonical key for a file: its path under root, '/'-joined, no extension."""
    rel = os.path.relpath(path, root)
    rel = rel[:-3] if rel.endswith(".md") else rel
    return rel.replace(os.sep, "/")


def _normalize_ref(ref):
    """Normalize an edge/parent reference to a comparable key string."""
    if ref is None:
        return None
    ref = str(ref).strip()
    ref = ref.split("#", 1)[0].strip()
    if ref.startswith("./"):
        ref = ref[2:]
    if ref.endswith(".md"):
        ref = ref[:-3]
    return ref.strip("/") if "/" in ref else ref


def _collect_reveal_tags(*texts):
    tags = []
    for text in texts:
        if not text:
            continue
        for match in REVEAL_TAG_RE.findall(str(text)):
            tags.append(match.strip())
    return tags


def _build_edges(source_key, edges_block, entity):
    """Turn the parsed `edges:` mapping into Edge objects.

    Values may be a bare id (single directional/symmetric target), a list of
    ids (multi-target symmetric, e.g. `connects: [a, b]`), or a structured
    mapping (`addressed-to`).
    """
    if not isinstance(edges_block, dict):
        return
    for relation, value in edges_block.items():
        relation = str(relation)
        if relation in STRUCTURED_RELATIONS and isinstance(value, dict):
            street = value.get("street")
            entity.edges.append(Edge(source_key, relation, street, payload=value))
            continue
        if isinstance(value, list):
            for item in value:
                entity.edges.append(Edge(source_key, relation, item))
        elif isinstance(value, dict):
            # An unexpected mapping for a non-structured relation: keep it as a
            # payload so the validator can flag it rather than dropping data.
            entity.edges.append(Edge(source_key, relation, None, payload=value))
        elif value is not None:
            entity.edges.append(Edge(source_key, relation, value))


def parse_entity(path, root):
    """Parse one entity file into an Entity. Never raises on content."""
    key = _rel_key(path, root)
    entity = Entity(key, path)

    try:
        text = _read(path)
    except OSError as error:
        entity.parse_error = str(error)
        return entity

    fm_text, body = split_frontmatter(text)
    frontmatter = parse_yaml(fm_text) if fm_text.strip() else {}
    if not isinstance(frontmatter, dict):
        frontmatter = {}
    entity.frontmatter = frontmatter
    entity.title = frontmatter.get("title")
    entity.entity_type = frontmatter.get("entity_type")
    entity.status = frontmatter.get("status")
    entity.declared_parent = _normalize_ref(frontmatter.get(CONTAINMENT_RELATION))

    # Folder home: the parent is the basename of the containing folder, unless
    # the file sits at the root (a city), where there is no folder parent.
    folder = os.path.dirname(os.path.abspath(path))
    if os.path.abspath(folder) != os.path.abspath(root):
        entity.parent_from_folder = os.path.basename(folder)

    # Merge every fenced ```yaml block into one data mapping.
    data = {}
    for block in extract_yaml_blocks(body):
        parsed = parse_yaml(block)
        if isinstance(parsed, dict):
            data.update(parsed)
    entity.data = data

    entity.street = _normalize_ref(data.get("street")) if data.get("street") else data.get("street")
    entity.seg_from = _normalize_ref(data.get("from")) if data.get("from") else data.get("from")
    entity.seg_to = _normalize_ref(data.get("to")) if data.get("to") else data.get("to")
    entity.length_m = data.get("length_m")
    entity.home = _normalize_ref(data.get("home")) if data.get("home") else data.get("home")
    timeline = data.get("timeline")
    entity.timeline = timeline if isinstance(timeline, list) else []

    _build_edges(key, data.get("edges"), entity)

    # Prose sections + zero-blanks (a declared `## section` must be non-empty).
    current = None
    has_body = {}
    for raw in body.split("\n"):
        stripped = raw.strip()
        if raw.startswith("## "):
            current = stripped[3:].strip()
            entity.present_sections.add(current)
            has_body.setdefault(current, False)
            continue
        if raw.startswith("# ") and not raw.startswith("## "):
            current = None
            continue
        if current is not None and stripped and not stripped.startswith("# "):
            has_body[current] = True
    entity.empty_sections = {
        section for section in entity.present_sections if not has_body.get(section)
    }

    entity.reveal_tags = _collect_reveal_tags(
        frontmatter.get("reveal"), entity.status, *(e.target for e in entity.edges)
    )

    entity.is_entity = (
        entity.entity_type is not None
        or entity.declared_parent is not None
        or bool(data)
    )
    return entity


# ===========================================================================
# The graph: walk, resolve, derive.
# ===========================================================================


class EntityGraph:
    """Every parsed entity, the resolver, and the derived views."""

    def __init__(self):
        self.entities = {}        # key (rel-path) -> Entity (the validated tree)
        self.externals = {}       # bare id -> ExternalRef (resolve-only, another domain)
        self.id_index = {}        # bare id -> set of keys (collision-aware; both kinds)
        self.parse_warnings = []
        self._network = None      # cached adjacency

    # -- registration / resolution -----------------------------------------

    def add(self, entity):
        self.entities[entity.key] = entity
        self.id_index.setdefault(entity.entity_id, set()).add(entity.key)

    def add_external(self, entity_id, domain):
        """Register a resolution-only node from another entity domain.

        The geography rails never iterate these; they exist so a cross-tree edge
        target -- an `owner` who is a character, a `residence` -- resolves. The key
        is the bare id, since other domains are referenced by id, not by a path in
        the geography tree. A real geography entity of the same id always wins (the
        external is not registered over it), so the spatial tree stays authoritative.
        """
        if entity_id in self.entities or entity_id in self.externals:
            return
        self.externals[entity_id] = ExternalRef(entity_id, domain)
        self.id_index.setdefault(entity_id, set()).add(entity_id)

    def resolve(self, ref):
        """Resolve a reference to a canonical key, or None.

        Three reference shapes are accepted, in priority order, matching how the
        spec authors edges (sections 4, 8, 9):
          1. a full rel-path from the root (the canonical key);
          2. a bare id (the filename stem), e.g. `jonah-house` or `rook-eli`;
          3. a SUFFIX path, e.g. `412-perry/kitchen`, naming the tail of a key.
        Resolution sees both the spatial entities and the resolution-only externals
        from other domains, so a cross-tree edge target resolves. A bare id or suffix
        resolves only when UNAMBIGUOUS; an ambiguous reference returns None by design
        (the validator then reports it).
        """
        ref = _normalize_ref(ref)
        if ref is None:
            return None
        if ref in self.entities or ref in self.externals:
            return ref
        if "/" not in ref:
            keys = self.id_index.get(ref)
            if keys and len(keys) == 1:
                return next(iter(keys))
            return None
        suffix = "/" + ref
        matches = [key for key in self.entities if key.endswith(suffix)]
        matches += [key for key in self.externals if key.endswith(suffix)]
        if len(matches) == 1:
            return matches[0]
        return None

    def get(self, ref):
        """Resolve a reference and return the Entity (or ExternalRef), or None."""
        key = self.resolve(ref)
        if key is None:
            return None
        return self.entities.get(key) or self.externals.get(key)

    # -- containment (spec section 3) --------------------------------------

    def containment_parent(self, key):
        """The resolved containment-parent key of an entity, or None at the root."""
        entity = self.entities.get(key)
        if entity is None:
            return None
        return entity.parent_key

    def children_of(self, key):
        """Keys whose containment parent resolves to this entity."""
        return sorted(
            child.key for child in self.entities.values()
            if child.parent_key == key
        )

    def descendants_of(self, key):
        """All keys contained, recursively, beneath an entity."""
        out = []
        stack = list(self.children_of(key))
        seen = set()
        while stack:
            child = stack.pop()
            if child in seen:
                continue
            seen.add(child)
            out.append(child)
            stack.extend(self.children_of(child))
        return sorted(out)

    def ancestors_of(self, key):
        """Containment ancestors from the entity upward; stops on a cycle."""
        out = []
        seen = set()
        current = self.containment_parent(key)
        while current is not None and current not in seen:
            seen.add(current)
            out.append(current)
            current = self.containment_parent(current)
        return out

    # -- the edge graph (spec section 4) -----------------------------------

    def directional_links(self, resolved_only=True):
        """Yield (source_key, target_key_or_ref, relation, edge) for in-vocab
        directional edges (containment `parent` excluded -- it is its own view)."""
        for entity in self.entities.values():
            for edge in entity.edges:
                if not edge.is_directional or edge.relation == CONTAINMENT_RELATION:
                    continue
                if edge.target_key is None and resolved_only:
                    continue
                yield entity.key, edge.target_key or edge.target, edge.relation, edge

    def symmetric_links(self, resolved_only=True):
        """Yield (source_key, target_key_or_ref, relation, edge) for in-vocab
        symmetric edges. Reciprocity is the validator's job, not this reader's."""
        for entity in self.entities.values():
            for edge in entity.edges:
                if not edge.is_symmetric:
                    continue
                if edge.target_key is None and resolved_only:
                    continue
                yield entity.key, edge.target_key or edge.target, edge.relation, edge

    # -- the street network (spec section 7) -------------------------------

    def segments(self):
        """Every segment entity (by type, or by carrying from/to)."""
        return [e for e in self.entities.values() if e.is_segment]

    def streets(self):
        """Every street entity."""
        return [e for e in self.entities.values() if e.entity_type == "street"]

    def whats_on_street(self, street_ref):
        """Keys of entities whose `addressed-to` names this street (derived)."""
        target = self.resolve(street_ref) or _normalize_ref(street_ref)
        out = []
        for entity in self.entities.values():
            for edge in entity.edges:
                if edge.relation != "addressed-to":
                    continue
                edge_street = self.resolve(edge.target) or _normalize_ref(edge.target)
                if edge_street == target:
                    out.append(entity.key)
        return sorted(set(out))

    def segments_of_street(self, street_ref):
        """Keys of the segments that make up a street (derived membership)."""
        target = self.resolve(street_ref) or _normalize_ref(street_ref)
        return sorted(
            seg.key for seg in self.segments()
            if (self.resolve(seg.street) or seg.street) == target
        )

    def build_network(self):
        """Undirected adjacency over intersections, weighted by segment length.

        node_key -> list of (neighbor_key, length_m, segment_key). The single
        source of each length is the segment that owns it.
        """
        adjacency = {}
        for seg in self.segments():
            node_a = self.resolve(seg.seg_from)
            node_b = self.resolve(seg.seg_to)
            weight = seg.length_m
            if node_a is None or node_b is None:
                continue
            if not isinstance(weight, (int, float)):
                continue
            adjacency.setdefault(node_a, []).append((node_b, float(weight), seg.key))
            adjacency.setdefault(node_b, []).append((node_a, float(weight), seg.key))
        return adjacency

    def shortest_path_distance(self, node_a, node_b, adjacency=None):
        """Dijkstra shortest distance (metres) between two intersection keys."""
        if node_a == node_b:
            return 0.0
        if adjacency is None:
            adjacency = self.build_network()
        if node_a not in adjacency or node_b not in adjacency:
            return None
        dist = {node_a: 0.0}
        heap = [(0.0, node_a)]
        while heap:
            cost, node = heapq.heappop(heap)
            if node == node_b:
                return cost
            if cost > dist.get(node, float("inf")):
                continue
            for neighbor, weight, _seg in adjacency.get(node, ()):
                nxt = cost + weight
                if nxt < dist.get(neighbor, float("inf")):
                    dist[neighbor] = nxt
                    heapq.heappush(heap, (nxt, neighbor))
        return None

    # -- addresses are linear references (spec section 7) ------------------

    def _find_segment(self, street_ref, between):
        """The segment matching a street and an unordered intersection pair."""
        target_street = self.resolve(street_ref) or _normalize_ref(street_ref)
        wanted = {
            self.resolve(between[0]) if len(between) > 0 else None,
            self.resolve(between[1]) if len(between) > 1 else None,
        }
        for seg in self.segments():
            seg_street = self.resolve(seg.street) or _normalize_ref(seg.street)
            ends = {self.resolve(seg.seg_from), self.resolve(seg.seg_to)}
            if seg_street == target_street and ends == wanted and None not in ends:
                return seg
        return None

    def resolve_address(self, addr):
        """Resolve an `addressed-to` mapping to an AddressResolution.

        `addr` = { street, between:[A, B], along (0..1), side }. `along` is
        measured from between[0] toward between[1]; it is re-oriented to the
        owning segment's own from/to so distances compose correctly.
        """
        result = AddressResolution(addr)
        if not isinstance(addr, dict):
            return result
        result.street = addr.get("street")
        result.between = list(addr.get("between") or [])
        result.along = addr.get("along")
        result.side = addr.get("side")
        if len(result.between) != 2:
            return result
        seg = self._find_segment(result.street, result.between)
        if seg is None:
            return result
        result.segment = seg
        result.node_from = self.resolve(seg.seg_from)
        result.node_to = self.resolve(seg.seg_to)
        result.length = seg.length_m
        if isinstance(result.along, (int, float)) and isinstance(seg.length_m, (int, float)):
            # Re-orient `along` onto the segment's own from->to direction.
            a_key = self.resolve(result.between[0])
            along_seg = result.along if a_key == result.node_from else 1.0 - result.along
            result.dist_from = along_seg * float(seg.length_m)
            result.dist_to = (1.0 - along_seg) * float(seg.length_m)
        return result

    def address_distance(self, addr_a, addr_b):
        """Shortest network distance (metres) between two addresses, or None."""
        ra = self.resolve_address(addr_a)
        rb = self.resolve_address(addr_b)
        if not (ra.resolved and rb.resolved):
            return None
        if ra.dist_from is None or rb.dist_from is None:
            return None
        if ra.segment.key == rb.segment.key:
            return abs(ra.dist_from - rb.dist_from)
        adjacency = self.build_network()
        best = None
        ends_a = ((ra.node_from, ra.dist_from), (ra.node_to, ra.dist_to))
        ends_b = ((rb.node_from, rb.dist_from), (rb.node_to, rb.dist_to))
        for node_a, off_a in ends_a:
            for node_b, off_b in ends_b:
                if node_a is None or node_b is None:
                    continue
                span = self.shortest_path_distance(node_a, node_b, adjacency)
                if span is None:
                    continue
                total = off_a + span + off_b
                if best is None or total < best:
                    best = total
        return best

    # -- time / state (spec section 9) -------------------------------------

    def state_as_of(self, ref, when=None):
        """Replay an entity's timeline to an in-world date and return its state.

        Starts from the home/initial values and applies each `set:` whose `when`
        is on or before the requested date (None means latest). The same axis
        carries backstory and on-page events alike.
        """
        entity = self.get(ref)
        if entity is None:
            return {}
        cutoff = _coerce_date(when)
        state = {}
        if entity.home is not None:
            state["home"] = entity.home
            state["located-in"] = entity.home
        events = []
        for event in entity.timeline:
            if not isinstance(event, dict):
                continue
            stamp = parse_when(event.get("when"))
            if stamp is None:
                continue
            events.append((stamp, event))
        events.sort(key=lambda pair: pair[0])
        for stamp, event in events:
            if cutoff is not None and stamp > cutoff:
                continue
            changes = event.get("set")
            if isinstance(changes, dict):
                state.update(changes)
        return state

    def location_of(self, ref, when=None):
        """Where an entity is on a given in-world date (its `located-in`)."""
        return self.state_as_of(ref, when).get("located-in")


def _resolve_all(graph):
    """Resolve every parent and edge target to a canonical key, in place."""
    for entity in graph.entities.values():
        parent_ref = entity.declared_parent or entity.parent_from_folder
        entity.parent_key = graph.resolve(parent_ref) if parent_ref else None
        for edge in entity.edges:
            if edge.target is not None:
                edge.target_key = graph.resolve(edge.target)


def _register_external_domain(graph, directory, domain):
    """Register every `*.md` filename stem under `directory` as an external.

    These are the resolution-only nodes of another entity domain (today: the
    character profiles). A missing directory is fine -- cross-tree edges into it
    simply stay unresolved, which the validator then reports. Index files are not
    entities and are skipped.
    """
    if not os.path.isdir(directory):
        return
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".md") or name == "index.md":
            continue
        graph.add_external(name[:-3], domain)


def build_graph(geography_dir=GEOGRAPHY_DIR, reference_dirs=None):
    """Walk the entity tree under geography_dir and return a resolved graph.

    A missing tree yields an empty graph plus a warning -- never a crash. Only
    files that parse as entities (an `entity_type`, a `parent`, or a fenced
    ```yaml block) are added; legacy non-entity markdown is skipped.

    `reference_dirs` is a list of (directory, domain) pairs naming OTHER entity
    domains whose identities must resolve but which this graph does not validate
    (default: the character profiles). Their filename stems are registered as
    resolution-only externals so cross-tree edges -- a building's `owner`, a
    `residence` -- resolve. Resolution runs AFTER both the tree and the externals
    are loaded, so load order does not matter.
    """
    if reference_dirs is None:
        reference_dirs = [(CHARACTER_PROFILES_DIR, "character")]

    graph = EntityGraph()
    if not os.path.isdir(geography_dir):
        graph.parse_warnings.append(
            "geography tree not found (an empty tree is valid): " + geography_dir
        )
    else:
        for dirpath, _dirnames, filenames in os.walk(geography_dir):
            for name in sorted(filenames):
                if not name.endswith(".md") or name == "index.md":
                    continue
                path = os.path.join(dirpath, name)
                entity = parse_entity(path, geography_dir)
                if not entity.is_entity:
                    graph.parse_warnings.append(
                        entity.key + ": not an entity file (no entity_type, parent, "
                        "or fenced yaml block); skipped"
                    )
                    continue
                graph.add(entity)

    for directory, domain in reference_dirs:
        _register_external_domain(graph, directory, domain)

    _resolve_all(graph)
    return graph


if __name__ == "__main__":
    # A tiny self-report so the module can be sanity-run on its own.
    g = build_graph()
    print("entity_graph self-report")
    print("Geography root: " + GEOGRAPHY_DIR)
    print("Entities parsed: " + str(len(g.entities))
          + "  (externals registered: " + str(len(g.externals)) + ")")
    edges = [e for ent in g.entities.values() for e in ent.edges]
    print("Structured edges: " + str(len(edges))
          + " (" + str(len([e for e in edges if e.in_vocab])) + " in-vocab)")
    print("Segments: " + str(len(g.segments()))
          + "  Streets: " + str(len(g.streets())))
    for warning in g.parse_warnings:
        print("  warning: " + warning)
    for ent in sorted(g.entities):
        entity = g.entities[ent]
        parent = entity.parent_key or "(root)"
        print("  " + ent + "  [" + str(entity.entity_type) + "]  parent="
              + parent + "  edges=" + str(len(entity.edges)))
