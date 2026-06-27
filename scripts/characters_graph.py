#!/usr/bin/env python3
"""Shared character-graph parser for The Unnecessary.

Standard library only. No third-party imports, no pip installs.

This module is the single reader of the character profiles under
docs/20-canon/characters/profiles/. Two tools consume it:

  - scripts/build-relationship-graph.py  (generates Mermaid diagrams)
  - scripts/validate-characters.py        (relational-integrity validator)

What it reads, per docs/20-canon/characters/profile-spec.md:

  - Each profile's Basic Information block: full name, common name, age,
    birth date, faction, household, occupation, viewpoint, story role.
  - Each profile's "## Relationships" section: the structured machine-readable
    edges, one per line, in the form `- relation: target`, where target is
    either a bare `lastname-firstname` slug or a Markdown link
    `[Display](slug.md)` to the target profile, with an optional trailing note
    (for example "(proposed; no profile yet)") or reveal tag. Edges may sit
    inside a fenced code block; the scanner does not care.
  - The Section-4 section headers, to support a zero-blanks completeness check.
  - docs/20-canon/timeline/character-birth-dates.md, the canonical age/birth
    spine, parsed from its Markdown table.

Graceful degradation is a contract, not a nicety. The eleven existing human
profiles predate the enrichment spec: they carry bespoke headers and NO
structured edges. They are reported as "legacy / not yet migrated", never
crashed on. Only profiles that have adopted the new schema are held to it.

Id conventions, and the bridge between them:

  - The filename and id convention is `lastname-firstname` (e.g.
    `vega-marisol`, `rook-eli`). The eleven original human profiles have been
    renamed to this form; the resolver still registers the token-reversed
    alias so any lingering `firstname-lastname` reference keeps resolving.
  - The structured edges use the new convention and are authored as Markdown
    links: vega-marisol points at `[Eli Rook](rook-eli.md)` and
    `[Nolan Avery](avery-nolan.md)`, which match the files on disk.
  - The resolver bridges this by registering both the filename stem and its
    token-reversed form (plus surname/given-name forms) as aliases, so
    `rook-eli` resolves to the `eli-rook` profile today and keeps resolving
    after the rename. This bridge is the one place the firstname/lastname
    mismatch is absorbed; everything downstream sees stable character ids.
"""

import os
import re
import unicodedata
from datetime import date


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
CHARACTERS_DIR = os.path.join(REPO_ROOT, "docs", "20-canon", "characters")
PROFILES_DIR = os.path.join(CHARACTERS_DIR, "profiles")
BIRTH_DATES_PATH = os.path.join(
    REPO_ROOT, "docs", "20-canon", "timeline", "character-birth-dates.md"
)

# Book One opens on this date (CLAUDE.md: October 3 to November 1, 2053).
# Age cross-checks measure age as of this day.
BOOK_ONE_START = date(2053, 10, 3)

# Plausible generational gap, in years, between a parent and a child.
MIN_PARENT_CHILD_GAP = 13
MAX_PARENT_CHILD_GAP = 70

# Non-human intelligences keep the behavioral template, not the human schema.
# They are parsed but excluded from human-only checks (Section 2 of the spec).
NONHUMAN_IDS = {"morrow", "crown"}

# Files in the profiles directory that are not character profiles.
NON_PROFILE_FILES = {"index.md"}

# The thirteen Section-4 house sections, in order. Zero-blanks completeness
# requires every one of these to be present and non-empty for a migrated
# (v2) human profile.
REQUIRED_SECTIONS = [
    "Basic Information",
    "Physical and Identifiers",
    "Personality",
    "Daily Life and Habits",
    "Hobbies and Interests",
    "Likes and Dislikes",
    "Relationships",
    "Voice and Speech",
    "History and Background",
    "Private History and Behavioral Roots",
    "Secrets",
    "Role and Series Potential",
    "Continuity Anchors",
]

# ---------------------------------------------------------------------------
# Controlled relationship vocabulary (profile-spec.md, "Relationship model").
#
# There are exactly two legal classes of edge, and nothing else:
#
#   DIRECTIONAL  Stored exactly once, on the DEPENDENT end, pointing at the
#                AUTHORITY. The inverse is DERIVED by traversal and NEVER
#                written down. `creator-of` is the single deliberate exception:
#                it is authored on the creator (the authority) pointing at the
#                creation, because there is one creator of record and the fact
#                reads from the creator's side; its derived inverse is
#                `created-by`. A `father` edge on A pointing at B means "B is
#                A's father", so B is A's PARENT; the inverse `child` (B -> A)
#                is derived, never stored.
#
#   SYMMETRIC    The same relation from both ends. Stored on BOTH profiles and
#                reciprocity-checked: if A says `friend: B`, B says `friend: A`.
#
# Anything outside this vocabulary is OFF-VOCAB and is rejected by the
# validator. Stored derived inverses (son, daughter, grandfather, mother-of,
# mentor-of, owner-of, employees, ...) are a defect; they are computed here by
# traversal instead.
# ---------------------------------------------------------------------------

# Directional term -> (storer_end, derived_inverse_label).
#   storer_end "dependent": the edge SOURCE is the dependent and the TARGET is
#                           the authority (the normal case).
#   storer_end "authority": the edge SOURCE is the authority and the TARGET is
#                           the dependent (only `creator-of`).
DIRECTIONAL_META = {
    "father":     ("dependent", "child"),
    "mother":     ("dependent", "child"),
    "guardian":   ("dependent", "ward"),
    "employer":   ("dependent", "employee"),
    "reports-to": ("dependent", "direct-report"),
    "mentor":     ("dependent", "mentee"),
    "landlord":   ("dependent", "tenant"),
    "owner":      ("dependent", "owns"),
    "patient-of": ("dependent", "patient"),
    "creator-of": ("authority", "created-by"),
}
DIRECTIONAL_RELATIONS = set(DIRECTIONAL_META)

SYMMETRIC_RELATIONS = {
    "spouse", "former-spouse", "sibling", "friend", "rival", "adversary",
    "colleague", "neighbor", "partner", "acquaintance",
}

VOCAB = DIRECTIONAL_RELATIONS | SYMMETRIC_RELATIONS

# Biological-parent edges are capped at one each per character.
BIO_PARENT_RELATIONS = {"father", "mother"}

# Ancestry edges, used for the acyclicity check (no one is their own ancestor).
ANCESTRY_RELATIONS = {"father", "mother", "guardian"}

# Relation categories, used to route validation and rendering.
CAT_PARENT = "parent"        # father, mother: the family-tree backbone
CAT_AUTHORITY = "authority"  # guardian/employer/mentor/landlord/owner/
                             # reports-to/patient-of/creator-of
CAT_SYMMETRIC = "symmetric"  # the symmetric set
CAT_OFFVOCAB = "off-vocab"   # not in the controlled vocabulary


def relation_category(relation):
    """Classify a relation token into one of the four routing categories."""
    if relation in BIO_PARENT_RELATIONS:
        return CAT_PARENT
    if relation in DIRECTIONAL_RELATIONS:
        return CAT_AUTHORITY
    if relation in SYMMETRIC_RELATIONS:
        return CAT_SYMMETRIC
    return CAT_OFFVOCAB


def authority_dependent(relation, source_id, target_id):
    """Return (authority_id, dependent_id) for a directional relation.

    For every dependent-stored relation the target is the authority; for the
    single authority-stored relation (`creator-of`) the source is the authority.
    Returns None for a non-directional relation.
    """
    meta = DIRECTIONAL_META.get(relation)
    if meta is None:
        return None
    if meta[0] == "authority":
        return source_id, target_id
    return target_id, source_id


# --- Small text helpers -------------------------------------------------------

REVEAL_TAG_RE = re.compile(r"\[[^\]]*\]")
PAREN_NOTE_RE = re.compile(r"\([^)]*\)")
# A structured edge line: a bullet whose lead token is a lowercase, hyphenated
# relation, then a colon, then a target and an optional trailing note. The
# target is parsed in a second step (see _split_target) because the live
# generation run emits sentinel placeholders alongside real slugs.
EDGE_LINE_RE = re.compile(r"^\s*-\s+([a-z][a-z0-9-]*)\s*:\s*(.*)$")
# A real, resolvable profile slug (the spec's lastname-firstname id form).
SLUG_RE = re.compile(r"[a-z0-9][a-z0-9-]+$")
# A Markdown-link edge target: `[Display](id.md)` plus optional trailing text.
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)\s*(.*)$")
FIELD_RE = re.compile(r"^\*\*([^:*]+):\*\*\s*(.*)$")
DATE_RE = re.compile(r"([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})")

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
    "december": 12,
}


def strip_tags(value):
    """Remove inline reveal/visibility tags and parenthetical notes from a value."""
    value = REVEAL_TAG_RE.sub("", value)
    value = PAREN_NOTE_RE.sub("", value)
    return value.strip().strip(".").strip()


def slugify(text):
    """Lowercase, hyphenate a name token sequence into an id-style slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def _split_target(rest):
    """Split the text after `relation:` into (target, note).

    Handles three target shapes seen in real profiles:
      - a real slug:            `rook-eli            (note)`
      - an uppercase sentinel:  `OPEN-CANON-SLOT     (note)`
      - an angle placeholder:   `<unassigned ids>    (note)`
    The angle form may contain a space, so it is read up to the closing `>`.
    """
    rest = rest.strip()
    if not rest:
        return "", ""
    # Markdown-link target form: `[Display](id.md)` with an optional trailing
    # note or reveal tag. The id is the link target's basename without `.md`.
    link = MD_LINK_RE.match(rest)
    if link:
        url = link.group(1).split("#", 1)[0].strip()
        # Strip a leading "./" so a graph-view-resolvable link such as
        # `[Display](./rook-eli.md)` yields the same id as a bare `rook-eli.md`.
        if url.startswith("./"):
            url = url[2:]
        base = url.rsplit("/", 1)[-1]
        if base.endswith(".md"):
            base = base[:-3]
        return base, link.group(2).strip()
    if rest.startswith("<"):
        close = rest.find(">")
        if close != -1:
            return rest[: close + 1], rest[close + 1:].strip()
        return rest, ""
    parts = rest.split(None, 1)
    target = parts[0]
    note = parts[1].strip() if len(parts) > 1 else ""
    return target, note


def is_real_slug(target):
    """True when a target is a resolvable id-form slug, not a sentinel."""
    return bool(SLUG_RE.fullmatch(target))


def reverse_slug(slug):
    """Swap a two-token `a-b` slug into `b-a`. Returns None when not two tokens."""
    parts = slug.split("-")
    if len(parts) == 2 and parts[0] and parts[1]:
        return parts[1] + "-" + parts[0]
    return None


def parse_date(text):
    """Parse a 'Month D, YYYY' date into a datetime.date, or None."""
    match = DATE_RE.search(text)
    if not match:
        return None
    month = MONTHS.get(match.group(1).lower())
    if month is None:
        return None
    try:
        return date(int(match.group(3)), month, int(match.group(2)))
    except ValueError:
        return None


def years_between(earlier, later):
    """Whole years from `earlier` to `later`, by calendar."""
    years = later.year - earlier.year
    if (later.month, later.day) < (earlier.month, earlier.day):
        years -= 1
    return years


def fold_accents(text):
    """Reduce accented Latin letters to ASCII so 'Dembélé' becomes 'Dembele'."""
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def name_head(value):
    """The leading run of a Full name field, before any tag or citation prose.

    Real profiles append canon citations after the name, for example
    'Ruth Rook [open] (surname Rook is canon...). Maiden name proposed as ...'.
    The actual name is the text before the first '[' or '(', so the surname is
    not mistaken for a word in the trailing prose.
    """
    cut = len(value)
    for marker in ("[", "("):
        index = value.find(marker)
        if index != -1:
            cut = min(cut, index)
    return value[:cut].strip().rstrip(".").strip()


def name_tokens(full_name):
    """Lowercased alphabetic tokens of a name, titles and nicknames removed."""
    cleaned = fold_accents(name_head(full_name))
    cleaned = re.sub(r"[“”‘’\"']", " ", cleaned)
    tokens = []
    for raw in cleaned.split():
        token = re.sub(r"[^A-Za-z-]", "", raw).lower().strip("-")
        if not token:
            continue
        if token in ("dr", "mr", "mrs", "ms", "the"):
            continue
        tokens.append(token)
    return tokens


# --- Data carriers ------------------------------------------------------------


class Edge:
    """One structured relationship edge authored on a source profile."""

    def __init__(self, source_id, relation, target_slug, note, raw, line_no):
        self.source_id = source_id
        self.relation = relation
        self.target_slug = target_slug
        self.note = note
        self.raw = raw
        self.line_no = line_no
        # A sentinel target (OPEN-CANON-SLOT, <unassigned ids>) is a deliberate
        # placeholder for a not-yet-assigned person, not a resolvable profile.
        self.open_slot = not is_real_slug(target_slug)
        # A target the author has explicitly marked as not-yet-real, or a slot.
        lowered = note.lower()
        self.proposed = (
            self.open_slot
            or "proposed" in lowered
            or "no profile yet" in lowered
        )
        # Resolved target character id, filled in by the graph builder.
        self.target_id = None

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
    def category(self):
        return relation_category(self.relation)


class Character:
    """A parsed character profile plus its derived facts."""

    def __init__(self, char_id, path):
        self.id = char_id
        self.path = path
        self.display_name = char_id
        self.full_name = ""
        self.common_name = ""
        self.surname = ""
        self.given_name = ""
        self.fields = {}
        self.age = None
        self.birth_date = None          # datetime.date from the profile body
        self.faction = ""
        self.edges = []
        self.aliases = set()
        self.present_sections = set()
        self.empty_sections = set()
        self.has_structured_edges = False
        self.is_nonhuman = char_id in NONHUMAN_IDS
        # Spine (birth-dates table) facts, attached by the builder.
        self.spine_birth_date = None
        self.spine_age = None
        # Whether this profile has adopted the enrichment (v2) schema.
        self.is_v2 = False

    @property
    def effective_birth_date(self):
        """Prefer the canonical spine date; fall back to the profile's own."""
        return self.spine_birth_date or self.birth_date

    @property
    def missing_sections(self):
        return [s for s in REQUIRED_SECTIONS if s not in self.present_sections]


class Graph:
    """The whole parsed cast: characters, resolver, spine, and warnings."""

    def __init__(self):
        self.characters = {}        # id -> Character
        self.alias_index = {}       # alias -> id
        self.alias_collisions = []  # (alias, existing_id, new_id)
        self.spine = {}             # normalized-name -> (date, age, raw_name)
        self.parse_warnings = []    # human-readable strings

    def add(self, character):
        self.characters[character.id] = character

    def build_alias_index(self):
        # Pass 1: every profile owns its own id outright. A profile's filename
        # stem is its canonical id and always wins.
        for char in self.characters.values():
            self.alias_index[char.id] = char.id
        # Pass 2: secondary aliases (the token-reversed form, surname/given-name
        # combinations) fill only the gaps. This means a stray or token-reversed
        # file can never hijack a real profile's own id (for example a leftover
        # `eli-rook.md` stub must not capture the slug `rook-eli`).
        for char in self.characters.values():
            for alias in sorted(char.aliases):
                if alias == char.id:
                    continue
                if alias in self.alias_index and self.alias_index[alias] != char.id:
                    self.alias_collisions.append(
                        (alias, self.alias_index[alias], char.id)
                    )
                    continue
                self.alias_index[alias] = char.id

    def resolve(self, slug):
        """Resolve an edge target slug to a character id, or None.

        Tries the slug directly, then its token-reversed form. This is the
        bridge between the spec's lastname-firstname ids and the current
        firstname-lastname filenames.
        """
        if slug in self.alias_index:
            return self.alias_index[slug]
        reversed_form = reverse_slug(slug)
        if reversed_form and reversed_form in self.alias_index:
            return self.alias_index[reversed_form]
        return None

    def human_characters(self):
        return [c for c in self.characters.values() if not c.is_nonhuman]

    def ordered(self):
        return [self.characters[k] for k in sorted(self.characters)]

    # -- The directional graph and its derived inverses --------------------
    #
    # Only the controlled vocabulary is parsed into the graph. Directional
    # edges are stored once; everything that points the other way (children,
    # grandparents, employees, mentees, owned things, ...) is DERIVED here by
    # traversal and never read from the profiles.

    def directional_links(self, resolved_only=True):
        """Yield (authority_id, dependent_id, relation, edge) for in-vocab
        directional edges, with the authority/dependent ends normalized per
        DIRECTIONAL_META. When resolved_only is False, an unresolved target
        (a proposed person or open slot) yields its raw slug as the missing
        end so callers can still render a placeholder.
        """
        for char in self.characters.values():
            for edge in char.edges:
                if not edge.is_directional:
                    continue
                if edge.target_id is None and resolved_only:
                    continue
                target = edge.target_id or edge.target_slug
                authority, dependent = authority_dependent(
                    edge.relation, char.id, target
                )
                yield authority, dependent, edge.relation, edge

    def symmetric_links(self, resolved_only=True):
        """Yield (source_id, target_id, relation, edge) for in-vocab symmetric
        edges. These are stored on both ends; reciprocity is the validator's
        job, not this reader's.
        """
        for char in self.characters.values():
            for edge in char.edges:
                if not edge.is_symmetric:
                    continue
                if edge.target_id is None and resolved_only:
                    continue
                target = edge.target_id or edge.target_slug
                yield char.id, target, edge.relation, edge

    def parents_of(self):
        """child_id -> list of (parent_id, relation) from stored, resolved
        father/mother edges. The backbone for derivation and acyclicity.
        """
        out = {}
        for char in self.human_characters():
            for edge in char.edges:
                if edge.relation in BIO_PARENT_RELATIONS and edge.target_id:
                    out.setdefault(char.id, []).append(
                        (edge.target_id, edge.relation)
                    )
        return out

    def parent_child_pairs(self):
        """Deduped, sorted (parent_id, child_id, relation) derived from the
        stored father/mother edges. The same family backbone both the validator
        and the renderer read, so neither re-derives it locally.
        """
        seen = {}
        for child_id, plist in self.parents_of().items():
            for parent_id, relation in plist:
                seen.setdefault((parent_id, child_id), relation)
        return [(p, c, seen[(p, c)]) for (p, c) in sorted(seen)]

    def derived_inverse_edges(self):
        """Derive, by traversal, the inverse edges that are never stored.

        Returns a sorted list of dicts {source, target, relation, basis}:
          - the direct inverse of every resolved directional edge
            (parent --child--> child, mentor --mentee--> mentee,
             creation --created-by--> creator, ...);
          - two-hop grandparent / grandchild from the father/mother backbone.
        """
        derived = []
        for authority, dependent, relation, edge in self.directional_links():
            inverse = DIRECTIONAL_META[relation][1]
            if DIRECTIONAL_META[relation][0] == "dependent":
                src, dst = authority, dependent
            else:
                src, dst = dependent, authority
            derived.append(
                {"source": src, "target": dst, "relation": inverse,
                 "basis": relation}
            )

        parents = self.parents_of()
        for child_id, plist in parents.items():
            for parent_id, _ in plist:
                for grandparent_id, _ in parents.get(parent_id, []):
                    derived.append(
                        {"source": grandparent_id, "target": child_id,
                         "relation": "grandchild", "basis": "father/mother x2"})
                    derived.append(
                        {"source": child_id, "target": grandparent_id,
                         "relation": "grandparent", "basis": "father/mother x2"})

        derived.sort(key=lambda d: (d["source"], d["relation"], d["target"]))
        return derived


# --- Parsing ------------------------------------------------------------------


def _read_lines(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.readlines()


def _body_start(lines):
    if lines and lines[0].rstrip("\n") == "---":
        for index in range(1, len(lines)):
            if lines[index].rstrip("\n") == "---":
                return index + 1
    return 0


def parse_profile(path):
    """Parse one profile file into a Character. Never raises on content."""
    char_id = os.path.splitext(os.path.basename(path))[0]
    char = Character(char_id, path)

    try:
        lines = _read_lines(path)
    except OSError as error:
        char.parse_error = str(error)
        return char

    start = _body_start(lines)

    current_section = None
    section_has_body = {}

    for index in range(start, len(lines)):
        raw = lines[index].rstrip("\n")
        stripped = raw.strip()

        if raw.startswith("# ") and not raw.startswith("## "):
            char.display_name = stripped[2:].strip()
            continue

        if raw.startswith("## "):
            current_section = stripped[3:].strip()
            char.present_sections.add(current_section)
            section_has_body.setdefault(current_section, False)
            continue

        # Track whether the current section has any real body content.
        if current_section is not None and stripped:
            if not stripped.startswith("###") and not stripped.startswith(">"):
                if stripped not in ("```",):
                    section_has_body[current_section] = True

        # Discrete **Label:** value fields.
        field_match = FIELD_RE.match(raw)
        if field_match:
            label = field_match.group(1).strip()
            value = field_match.group(2).strip()
            char.fields[label] = value

        # Structured edges only count inside the Relationships section.
        if current_section == "Relationships":
            edge_match = EDGE_LINE_RE.match(raw)
            if edge_match:
                relation = edge_match.group(1)
                target, note = _split_target(edge_match.group(2))
                if target:
                    char.edges.append(
                        Edge(char_id, relation, target, note, stripped, index + 1)
                    )

    char.has_structured_edges = len(char.edges) > 0
    char.empty_sections = {
        s for s in char.present_sections if not section_has_body.get(s, False)
    }

    _derive_basic_facts(char)
    _build_aliases(char)

    present = len(char.present_sections & set(REQUIRED_SECTIONS))
    char.is_v2 = char.has_structured_edges or present >= 10

    return char


def _get_field(char, *labels):
    """Return the first matching field value, scanning by label prefix."""
    for label, value in char.fields.items():
        for wanted in labels:
            if label.lower().startswith(wanted.lower()):
                return value
    return ""


def _derive_basic_facts(char):
    char.full_name = _get_field(char, "Full name")
    char.common_name = strip_tags(_get_field(char, "Common name"))

    tokens = name_tokens(char.full_name) or name_tokens(char.display_name)
    if tokens:
        char.given_name = tokens[0]
        char.surname = tokens[-1]

    age_value = _get_field(char, "Age")
    age_match = re.search(r"\d+", age_value)
    if age_match:
        char.age = int(age_match.group(0))

    birth_value = _get_field(char, "Birth date")
    if birth_value:
        char.birth_date = parse_date(strip_tags(birth_value))

    faction_value = _get_field(char, "Faction or class", "Faction")
    if faction_value:
        char.faction = _normalize_faction(strip_tags(faction_value))
    else:
        char.faction = _infer_faction(char)


def _normalize_faction(text):
    lowered = text.lower()
    if "gatekeeper" in lowered:
        return "Gatekeepers"
    if "protected" in lowered:
        return "Protected Wealthy"
    if "everyone else" in lowered:
        return "Everyone Else"
    # Use the leading clause as a best-effort label.
    return text.split(",")[0].split(".")[0].strip()


def _infer_faction(char):
    """Best-effort faction for legacy profiles lacking the explicit field."""
    haystack = (
        _get_field(char, "Story role") + " " + _get_field(char, "Occupation")
    ).lower()
    if "gatekeeper" in haystack:
        return "Gatekeepers"
    if "protected" in haystack:
        return "Protected Wealthy"
    if "community" in haystack or "neighborhood" in haystack:
        return "Everyone Else"
    return "Unclassified"


def _build_aliases(char):
    aliases = {char.id}
    reversed_id = reverse_slug(char.id)
    if reversed_id:
        aliases.add(reversed_id)
    if char.surname and char.given_name:
        aliases.add(slugify(char.surname + "-" + char.given_name))
        aliases.add(slugify(char.given_name + "-" + char.surname))
    if char.surname and char.common_name:
        aliases.add(slugify(char.surname + "-" + char.common_name))
        aliases.add(slugify(char.common_name + "-" + char.surname))
    char.aliases = {a for a in aliases if a}


def parse_birth_dates(path=BIRTH_DATES_PATH):
    """Parse the canonical birth-date table into normalized-name -> facts."""
    spine = {}
    try:
        lines = _read_lines(path)
    except OSError:
        return spine

    for raw in lines:
        if not raw.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        name = cells[0]
        if name.lower() in ("character", "") or set(name) <= set("-: "):
            continue
        birth = parse_date(cells[1])
        age_match = re.search(r"\d+", cells[2])
        age = int(age_match.group(0)) if age_match else None
        key = "-".join(name_tokens(name))
        if key:
            spine[key] = (birth, age, name)
    return spine


def _attach_spine(graph):
    """Match each character to a birth-dates row by surname + given name."""
    # Index spine rows by surname for tolerant matching.
    by_surname = {}
    for key, (birth, age, raw_name) in graph.spine.items():
        tokens = key.split("-")
        if tokens:
            by_surname.setdefault(tokens[-1], []).append((tokens, birth, age))

    for char in graph.characters.values():
        if not char.surname:
            continue
        candidates = by_surname.get(char.surname, [])
        for tokens, birth, age in candidates:
            given = tokens[0] if tokens else ""
            if given == char.given_name or given == char.common_name:
                char.spine_birth_date = birth
                char.spine_age = age
                break
        else:
            # Sole surname match is accepted ONLY when the profile carries no
            # parsable given name. A character whose given name simply differs
            # from the spine row (a same-surname relative, e.g. a mother) must
            # NOT inherit the wrong person's date.
            if len(candidates) == 1 and not char.given_name:
                _, birth, age = candidates[0]
                char.spine_birth_date = birth
                char.spine_age = age


def build_graph(profiles_dir=PROFILES_DIR, birth_dates_path=BIRTH_DATES_PATH):
    """Read every profile and the spine, returning a resolved Graph."""
    graph = Graph()

    if not os.path.isdir(profiles_dir):
        graph.parse_warnings.append("profiles directory not found: " + profiles_dir)
        return graph

    for name in sorted(os.listdir(profiles_dir)):
        if not name.endswith(".md") or name in NON_PROFILE_FILES:
            continue
        path = os.path.join(profiles_dir, name)
        char = parse_profile(path)
        graph.add(char)
        if not char.is_nonhuman and not char.has_structured_edges:
            graph.parse_warnings.append(
                char.id + ": no structured relationship edges (legacy, not yet "
                "migrated to the enrichment schema)"
            )

    graph.spine = parse_birth_dates(birth_dates_path)
    graph.build_alias_index()
    _attach_spine(graph)

    # Resolve every real-slug edge target to a character id. Sentinel
    # placeholders (open slots) are left unresolved by design.
    for char in graph.characters.values():
        for edge in char.edges:
            if not edge.open_slot:
                edge.target_id = graph.resolve(edge.target_slug)

    return graph


if __name__ == "__main__":
    # A tiny self-report so the module can be sanity-run on its own.
    g = build_graph()
    print("characters_graph self-report")
    print("Profiles parsed: " + str(len(g.characters)))
    edges = [e for c in g.characters.values() for e in c.edges]
    in_vocab = [e for e in edges if e.in_vocab]
    off_vocab = [e for e in edges if not e.in_vocab]
    print("Structured edges found: " + str(len(edges)))
    print("  in-vocabulary: " + str(len(in_vocab))
          + " (" + str(len([e for e in in_vocab if e.is_directional]))
          + " directional, "
          + str(len([e for e in in_vocab if e.is_symmetric])) + " symmetric)")
    print("  off-vocabulary (to be migrated): " + str(len(off_vocab)))
    print("Derived inverse edges (by traversal): "
          + str(len(g.derived_inverse_edges())))
    print("Spine rows: " + str(len(g.spine)))
    print("")
    for char in g.ordered():
        flag = "v2" if char.is_v2 else "legacy"
        bad = sorted({e.relation for e in char.edges if not e.in_vocab})
        suffix = ("  off-vocab=" + ",".join(bad)) if bad else ""
        print(
            "  " + char.id + "  [" + flag + "]  surname="
            + (char.surname or "?") + "  edges=" + str(len(char.edges)) + suffix
        )
