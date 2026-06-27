#!/usr/bin/env python3
"""Relationship-diagram generator for The Unnecessary.

Standard library only. No third-party imports, no pip installs.

Reads the character profiles through scripts/characters_graph.py and emits the
relational views as Mermaid diagrams into
docs/20-canon/characters/relationships/:

  - family-tree.md      Parent/child (DERIVED from the stored father/mother
                        edges), plus spouse and sibling.
  - faction-map.md      Characters grouped by faction, with working allegiances
                        (symmetric and authority edges).
  - social-web.md       Every stored, in-vocabulary edge, labelled.
  - derived-graph.md    The inverse edges DERIVED by traversal and never stored
                        (child, mentee, employee, grandparent, created-by, ...).
  - index.md            A banner naming this generator as the only author.

The generator honors the controlled relationship model in profile-spec.md: it
renders ONLY the controlled vocabulary. Off-vocabulary labels (still present in
not-yet-migrated profiles) are skipped and counted, not drawn. Directional edges
are stored once; their inverses are computed by the graph reader and drawn in
derived-graph.md so the derivation is visible.

These files are a COMPILED ARTIFACT, the way a binary is an output of source.
They are never hand-edited. Each carries a "DO NOT EDIT - generated" banner.
The single source of truth is the Relationships section of each profile.

The output is deterministic and idempotent: nodes and edges are sorted and no
timestamp is written, so re-running on unchanged profiles produces byte-for-byte
identical files (clean `git diff`, safe to gate in CI).

Usage:
  build-relationship-graph.py            Write the diagrams.
  build-relationship-graph.py --check    Do not write; exit non-zero if any
                                         generated file is missing or stale.

Exit code:
  0  Files written (or, with --check, already up to date).
  1  With --check, one or more files are missing or out of date.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import characters_graph as cg

RELATIONSHIPS_DIR = os.path.join(cg.CHARACTERS_DIR, "relationships")
GENERATOR = "scripts/build-relationship-graph.py"
BANNER = "DO NOT EDIT - generated from profiles by " + GENERATOR

# Symmetric relations drawn in the family tree (the rest are social).
FAMILY_SYMMETRIC = {"spouse", "former-spouse", "sibling"}


def _node_id(key):
    """A Mermaid-safe node id (alphanumerics and underscores only)."""
    return "n_" + re.sub(r"\W", "_", key)


def _escape_label(text):
    return (
        text.replace('"', "'").replace("<", "[").replace(">", "]").strip()
    )


def _front_matter(title, summary):
    return [
        "---",
        'title: "' + title + '"',
        'document_type: "generated-diagram"',
        'status: "generated"',
        'authority: "character-canon"',
        'summary: "' + summary + '"',
        "tags:",
        "  - character",
        "  - relationships",
        "  - generated",
        "related:",
        '  - "../profile-spec.md"',
        "source_documents: []",
        "---",
        "",
    ]


def _label_for(graph, key, proposed=False):
    """Display label for a node, real or proposed/unresolved placeholder."""
    char = graph.characters.get(key)
    if char is not None:
        return _escape_label(char.display_name or char.id)
    label = _escape_label(key)
    if proposed:
        return label + " (proposed)"
    return label + " (unresolved)"


def render_family_tree(graph):
    """Parent/child is DERIVED from the stored father/mother edges; spouse and
    sibling are symmetric and drawn once."""
    nodes = {}
    edge_lines = []
    used = set()

    def ensure(key, proposed=False):
        node = _node_id(key)
        if node not in nodes:
            nodes[node] = _label_for(graph, key, proposed)
        used.add(node)
        return node

    # Parent --> child, derived from stored father/mother.
    for parent_id, child_id, relation in graph.parent_child_pairs():
        parent = ensure(parent_id)
        child = ensure(child_id)
        edge_lines.append(
            "    " + parent + ' -->|"' + relation + '"| ' + child)

    # Spouse / former-spouse / sibling, symmetric, drawn once per pair.
    undirected_seen = set()
    for src_id, tgt_id, relation, edge in graph.symmetric_links(resolved_only=False):
        if relation not in FAMILY_SYMMETRIC:
            continue
        a_key, b_key = src_id, tgt_id
        a = ensure(a_key)
        b = ensure(b_key, proposed=edge.proposed)
        pair = (frozenset((a, b)), relation)
        if pair in undirected_seen:
            continue
        undirected_seen.add(pair)
        lo, hi = sorted((a, b))
        edge_lines.append("    " + lo + ' ---|"' + relation + '"| ' + hi)

    lines = ["```mermaid", "%% " + BANNER, "graph TD"]
    for node in sorted(used):
        lines.append('    ' + node + '["' + nodes[node] + '"]')
    if not used:
        lines.append('    empty["No family edges authored yet"]')
    lines.extend(edge_lines)
    lines.append("```")
    return _wrap(
        "Family Tree",
        "Generated family structure for The Unnecessary. Parent/child is "
        "derived from the stored father/mother edges; spouse and sibling are "
        "symmetric.",
        lines,
    )


def render_faction_map(graph):
    lines = ["```mermaid", "%% " + BANNER, "graph TD"]

    by_faction = {}
    for char in graph.human_characters():
        by_faction.setdefault(char.faction or "Unclassified", []).append(char)

    placed = set()
    counter = 0
    for faction in sorted(by_faction):
        counter += 1
        sub_id = "f" + str(counter)
        lines.append('    subgraph ' + sub_id + '["' + _escape_label(faction) + '"]')
        for char in sorted(by_faction[faction], key=lambda c: c.id):
            node = _node_id(char.id)
            placed.add(node)
            lines.append(
                '        ' + node + '["' + _escape_label(char.display_name) + '"]')
        lines.append("    end")

    edge_lines = []
    loose = {}

    def ensure_loose(key, proposed):
        node = _node_id(key)
        if node not in placed and node not in loose:
            loose[node] = _label_for(graph, key, proposed)
        return node

    # Authority edges (directional, non-family), drawn in the authored
    # direction: source -.-> target with the stored relation label.
    for authority, dependent, relation, edge in graph.directional_links(resolved_only=False):
        if relation in cg.BIO_PARENT_RELATIONS:
            continue
        tgt_key = edge.target_id or edge.target_slug
        src = ensure_loose(edge.source_id, edge.proposed)
        dst = ensure_loose(tgt_key, edge.proposed)
        edge_lines.append("    " + src + ' -.->|"' + relation + '"| ' + dst)

    # Symmetric social edges (not the family ones), drawn once per pair.
    undirected_seen = set()
    for src_id, tgt_id, relation, edge in graph.symmetric_links(resolved_only=False):
        if relation in FAMILY_SYMMETRIC:
            continue
        src = ensure_loose(src_id, edge.proposed)
        dst = ensure_loose(tgt_id, edge.proposed)
        pair = (frozenset((src, dst)), relation)
        if pair in undirected_seen:
            continue
        undirected_seen.add(pair)
        lo, hi = sorted((src, dst))
        edge_lines.append("    " + lo + ' -.-|"' + relation + '"| ' + hi)

    for node in sorted(loose):
        lines.append('    ' + node + '["' + loose[node] + '"]')
    lines.extend(sorted(edge_lines))
    lines.append("```")
    return _wrap(
        "Faction and Allegiance Map",
        "Generated grouping of the cast by faction, with working allegiances "
        "(authority and symmetric edges) drawn from the profiles.",
        lines,
    )


def render_social_web(graph):
    """Every stored, in-vocabulary edge, in its authored direction. Directional
    edges are arrows; symmetric edges are a single undirected line per pair."""
    nodes = {}
    used = set()
    edge_lines = []

    def ensure(key, proposed=False):
        node = _node_id(key)
        if node not in nodes:
            nodes[node] = _label_for(graph, key, proposed)
        used.add(node)
        return node

    for authority, dependent, relation, edge in graph.directional_links(resolved_only=False):
        # Draw in the AUTHORED direction (source -> target) for readability.
        src = ensure(edge.source_id)
        tgt_key = edge.target_id or edge.target_slug
        tgt = ensure(tgt_key, proposed=edge.proposed)
        edge_lines.append("    " + src + ' -->|"' + relation + '"| ' + tgt)

    undirected_seen = set()
    for src_id, tgt_id, relation, edge in graph.symmetric_links(resolved_only=False):
        src = ensure(src_id)
        tgt = ensure(tgt_id, proposed=edge.proposed)
        pair = (frozenset((src, tgt)), relation)
        if pair in undirected_seen:
            continue
        undirected_seen.add(pair)
        lo, hi = sorted((src, tgt))
        edge_lines.append("    " + lo + ' ---|"' + relation + '"| ' + hi)

    lines = ["```mermaid", "%% " + BANNER, "graph LR"]
    for node in sorted(used):
        lines.append('    ' + node + '["' + nodes[node] + '"]')
    if not used:
        lines.append('    empty["No in-vocabulary edges authored yet"]')
    lines.extend(sorted(edge_lines))
    lines.append("```")
    return _wrap(
        "Social Web",
        "Generated overall social web: every stored, in-vocabulary "
        "relationship edge across the cast of The Unnecessary.",
        lines,
    )


def render_derived_graph(graph):
    """The inverse edges DERIVED by traversal and never stored: child, mentee,
    employee, tenant, ward, owns, patient, created-by, and the two-hop
    grandparent / grandchild."""
    nodes = {}
    used = set()
    edge_lines = []

    def ensure(key):
        node = _node_id(key)
        if node not in nodes:
            nodes[node] = _label_for(graph, key)
        used.add(node)
        return node

    for d in graph.derived_inverse_edges():
        src = ensure(d["source"])
        dst = ensure(d["target"])
        edge_lines.append(
            "    " + src + ' -.->|"' + d["relation"] + ' (derived)"| ' + dst)

    lines = ["```mermaid", "%% " + BANNER, "graph LR"]
    for node in sorted(used):
        lines.append('    ' + node + '["' + nodes[node] + '"]')
    if not used:
        lines.append('    empty["No directional edges to derive inverses from yet"]')
    lines.extend(sorted(edge_lines))
    lines.append("```")
    return _wrap(
        "Derived Inverse Graph",
        "Generated inverse relationships, computed by traversal of the stored "
        "directional edges and never authored in a profile.",
        lines,
    )


def render_index(graph):
    human = graph.human_characters()
    migrated = [c for c in human if c.has_structured_edges]
    edges = [e for c in human for e in c.edges]
    off_vocab = sorted({e.relation for e in edges if not e.in_vocab})
    lines = [
        "# Character Relationship Diagrams",
        "",
        "> " + BANNER,
        "",
        "These diagrams are a compiled artifact. They are never hand-edited.",
        "The single source of truth is the `## Relationships` section of each",
        "profile under `../profiles/`. Edit a relationship there, then re-run",
        "`" + GENERATOR + "`.",
        "",
        "The generator renders only the controlled relationship vocabulary",
        "(see `../profile-spec.md`). Directional edges are stored once on the",
        "dependent end; their inverses are derived by traversal and shown in",
        "the derived graph below.",
        "",
        "## Views",
        "",
        "- [Family Tree](./family-tree.md)",
        "- [Faction and Allegiance Map](./faction-map.md)",
        "- [Social Web](./social-web.md)",
        "- [Derived Inverse Graph](./derived-graph.md)",
        "",
        "## Source status",
        "",
        "- Profiles read: " + str(len(human)),
        "- Profiles with structured edges (migrated): " + str(len(migrated)),
        "- Profiles still legacy (no structured edges): "
        + str(len(human) - len(migrated)),
        "- In-vocabulary edges drawn: "
        + str(len([e for e in edges if e.in_vocab])),
        "- Derived inverse edges: " + str(len(graph.derived_inverse_edges())),
        "- Off-vocabulary labels still to migrate ("
        + str(len(off_vocab)) + "): "
        + (", ".join(off_vocab) if off_vocab else "none"),
        "",
        "As the remaining profiles migrate to the controlled vocabulary,",
        "re-running the generator fills these diagrams in automatically.",
        "",
    ]
    return "\n".join(
        _front_matter(
            "Character Relationship Diagrams",
            "Generated index and banner for the compiled relationship diagrams.",
        )
        + lines
    )


def _wrap(title, summary, mermaid_lines):
    header = _front_matter(title, summary)
    body = [
        "# " + title,
        "",
        "> " + BANNER,
        "",
    ]
    return "\n".join(header + body + mermaid_lines + [""])


def _outputs(graph):
    return {
        "index.md": render_index(graph),
        "family-tree.md": render_family_tree(graph),
        "faction-map.md": render_faction_map(graph),
        "social-web.md": render_social_web(graph),
        "derived-graph.md": render_derived_graph(graph),
    }


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    check_only = "--check" in argv

    graph = cg.build_graph()
    outputs = _outputs(graph)

    edges = [e for c in graph.human_characters() for e in c.edges]
    off_vocab = [e for e in edges if not e.in_vocab]

    print("Relationship-graph generator for The Unnecessary")
    print("Profiles read: " + str(len(graph.characters)))
    print("Output directory: " + RELATIONSHIPS_DIR)
    print("In-vocabulary edges: " + str(len(edges) - len(off_vocab))
          + " | off-vocabulary skipped: " + str(len(off_vocab))
          + " | derived inverses: " + str(len(graph.derived_inverse_edges())))
    if graph.parse_warnings:
        print("Notices: " + str(len(graph.parse_warnings)) + " profile(s) lack "
              "structured edges (legacy, not yet migrated).")
    print("")

    if check_only:
        stale = []
        for name, content in sorted(outputs.items()):
            path = os.path.join(RELATIONSHIPS_DIR, name)
            if not os.path.exists(path):
                stale.append((name, "missing"))
                continue
            with open(path, "r", encoding="utf-8") as handle:
                if handle.read() != content:
                    stale.append((name, "out of date"))
        if stale:
            print("Result: FAIL. Generated diagrams are stale:")
            for name, why in stale:
                print("  " + name + ": " + why)
            print("Run: python3 " + GENERATOR)
            return 1
        print("Result: PASS. All generated diagrams are up to date.")
        return 0

    if not os.path.isdir(RELATIONSHIPS_DIR):
        os.makedirs(RELATIONSHIPS_DIR)

    for name, content in sorted(outputs.items()):
        path = os.path.join(RELATIONSHIPS_DIR, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
        print("  wrote " + os.path.relpath(path, cg.REPO_ROOT))

    print("")
    print("Result: OK. Diagrams generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
