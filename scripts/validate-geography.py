#!/usr/bin/env python3
"""Geography rails -- the structural validator for The Unnecessary's entity tree.

Standard library only. No third-party imports, no pip installs. Fast enough to
run on every change, the way scripts/validate-characters.py and
scripts/validate-links.py do. It reads the entity tree through
scripts/entity_graph.py and enforces the deterministic half of entity-spec.md
section 11. The semantic half (does the prose contradict the change) stays with
the on-demand diff-judge; only mechanical, cheap, every-commit checks live here.

Checks (entity-spec.md section 11):

  REFERENTIAL    Every edge target exists -- `parent`, `owner`, `connects`, an
                 `addressed-to` street and its `between` intersections, a
                 segment's `from`/`to`, a timeline `located-in`, and `home`.
  FOLDER-PARENT  The frontmatter `parent:` agrees with the folder home (the
                 free cross-check of spec section 3). A network entity is exempt
                 -- it is positioned by edges, not containment.
  ACYCLICITY     No entity is its own containment ancestor.
  NETWORK        Each segment's `length_m` is single-source (no other entity
                 declares a length; no duplicate segment over the same pair with
                 a different length -> no contradictory route distances); a
                 segment's `from`/`to` exist; every `addressed-to` resolves to a
                 real segment with `along` in [0, 1].
  RECIPROCITY    Both ends of a symmetric edge (`connects`, `neighbor`, ...)
                 agree, with the same term.
  VOCABULARY     Every relation label is in the controlled vocabulary.
  ZERO-BLANKS    A declared `## section` is non-empty. Stubs may be stubs; a
                 declared section may not be blank.
  REVEAL-TAGS    Bracketed reveal tags are well-formed: `[open]`,
                 `[reveal: Book N]`, `[behavior-only]`.

Severity:

  ERROR    A hard violation of the contract. Fails the run.
  WARNING  An expected gap (a stub naming a not-yet-built parent, a symmetric
           counterpart still a stub). Reported, but does not fail by default.

It MUST pass on an empty or just-stubs tree: a fresh world with nothing built,
or one with only one-line stub files, has zero errors by construction.

Exit code:
  0  No errors (and, without --strict, regardless of warnings).
  1  One or more errors (or, with --strict, any error or warning).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import entity_graph as eg


ERROR = "ERROR"
WARNING = "WARNING"


class Finding:
    def __init__(self, severity, category, entity_key, message):
        self.severity = severity
        self.category = category
        self.entity_key = entity_key
        self.message = message

    def sort_key(self):
        order = 0 if self.severity == ERROR else 1
        return (order, self.category, self.entity_key, self.message)


def check_vocabulary(graph, findings):
    """Every relation label must be in the controlled vocabulary (spec 4)."""
    for entity in graph.entities.values():
        for edge in entity.edges:
            if edge.in_vocab:
                continue
            findings.append(Finding(
                ERROR, "VOCABULARY", entity.key,
                "edge `" + edge.relation + "` is not in the controlled "
                "vocabulary; map it to a directional or symmetric term or move "
                "the nuance to prose (entity-spec.md section 4)."))


def check_referential(graph, findings):
    """Every edge target, parent, address part, and home must resolve."""
    for entity in graph.entities.values():
        # Containment parent.
        parent_ref = entity.declared_parent
        if parent_ref and entity.parent_key is None:
            findings.append(Finding(
                _referential_severity(entity), "REFERENTIAL", entity.key,
                "`parent: " + str(parent_ref) + "` points at an entity that "
                "does not exist"))

        # Edge targets.
        for edge in entity.edges:
            if not edge.in_vocab:
                continue
            if edge.relation == "addressed-to":
                _check_address_refs(graph, entity, edge, findings)
                continue
            if edge.target is None:
                findings.append(Finding(
                    ERROR, "REFERENTIAL", entity.key,
                    "edge `" + edge.relation + "` has no target"))
                continue
            if edge.target_key is None:
                findings.append(Finding(
                    _referential_severity(entity), "REFERENTIAL", entity.key,
                    "edge `" + edge.relation + ": " + str(edge.target)
                    + "` points at an entity that does not exist"))

        # Home shelf.
        if entity.home and graph.resolve(entity.home) is None:
            findings.append(Finding(
                _referential_severity(entity), "REFERENTIAL", entity.key,
                "`home: " + str(entity.home) + "` does not resolve to a real "
                "entity"))

        # Timeline `located-in` (and any other set: location reference).
        for event in entity.timeline:
            if not isinstance(event, dict):
                continue
            changes = event.get("set") or {}
            if not isinstance(changes, dict):
                continue
            located = changes.get("located-in")
            if located and graph.resolve(located) is None:
                findings.append(Finding(
                    _referential_severity(entity), "REFERENTIAL", entity.key,
                    "timeline (" + str(event.get("when")) + ") sets `located-in: "
                    + str(located) + "`, which does not resolve"))


def _referential_severity(entity):
    """A stub naming a not-yet-built neighbor is a WARNING; a built-out entity
    with a dangling reference is an ERROR."""
    return WARNING if entity.is_stub else ERROR


def _check_address_refs(graph, entity, edge, findings):
    payload = edge.payload or {}
    street = payload.get("street")
    between = payload.get("between") or []
    if street and graph.resolve(street) is None:
        findings.append(Finding(
            _referential_severity(entity), "REFERENTIAL", entity.key,
            "`addressed-to.street: " + str(street) + "` does not resolve to a "
            "street"))
    for end in between:
        if graph.resolve(end) is None:
            findings.append(Finding(
                _referential_severity(entity), "REFERENTIAL", entity.key,
                "`addressed-to.between` names `" + str(end) + "`, which does "
                "not resolve to an intersection"))


def check_folder_parent(graph, findings):
    """The declared `parent:` must agree with the folder home (spec 3)."""
    for entity in graph.entities.values():
        if entity.is_network:
            continue  # positioned by edges, not single-parent containment
        declared = entity.declared_parent
        folder = entity.parent_from_folder
        if declared and folder and declared != folder:
            findings.append(Finding(
                ERROR, "FOLDER-PARENT", entity.key,
                "frontmatter `parent: " + str(declared) + "` disagrees with the "
                "folder home `" + str(folder) + "` (a misfile: one home per "
                "entity, spec section 3)"))
        elif folder and not declared:
            findings.append(Finding(
                WARNING, "FOLDER-PARENT", entity.key,
                "sits in folder `" + str(folder) + "` but declares no `parent:` "
                "(the containment edge lives on the child)"))


def check_acyclicity(graph, findings):
    """No entity is its own containment ancestor (spec 11)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}

    def visit(node, stack):
        color[node] = GRAY
        stack.append(node)
        parent = graph.containment_parent(node)
        if parent is not None:
            if color.get(parent, WHITE) == GRAY:
                cycle = stack[stack.index(parent):] + [parent]
                findings.append(Finding(
                    ERROR, "ACYCLICITY", node,
                    "containment cycle: " + " -> ".join(cycle)))
            elif color.get(parent, WHITE) == WHITE:
                visit(parent, stack)
        stack.pop()
        color[node] = BLACK

    for node in sorted(graph.entities):
        if color.get(node, WHITE) == WHITE:
            visit(node, [])


def check_network(graph, findings):
    """Segment length is single-source; from/to exist; addresses resolve."""
    segments = graph.segments()

    # length_m single-source: a segment owns it; nothing else declares a length.
    for entity in graph.entities.values():
        if entity.length_m is not None and not entity.is_segment:
            findings.append(Finding(
                ERROR, "NETWORK", entity.key,
                "declares `length_m` but is not a segment; segment length is "
                "single-source (the segment owns it, spec section 7)"))

    # No two segments span the same intersection pair with different lengths
    # (that would imply two contradictory route distances).
    by_pair = {}
    for seg in segments:
        a = graph.resolve(seg.seg_from)
        b = graph.resolve(seg.seg_to)
        if a is None or b is None:
            if seg.seg_from is not None and graph.resolve(seg.seg_from) is None:
                findings.append(Finding(
                    _referential_severity(seg), "NETWORK", seg.key,
                    "segment `from: " + str(seg.seg_from) + "` is not a known "
                    "intersection"))
            if seg.seg_to is not None and graph.resolve(seg.seg_to) is None:
                findings.append(Finding(
                    _referential_severity(seg), "NETWORK", seg.key,
                    "segment `to: " + str(seg.seg_to) + "` is not a known "
                    "intersection"))
            continue
        if not isinstance(seg.length_m, (int, float)):
            findings.append(Finding(
                WARNING, "NETWORK", seg.key,
                "segment has resolved endpoints but no numeric `length_m` "
                "(distances through it cannot be computed yet)"))
            continue
        pair = tuple(sorted((a, b)))
        by_pair.setdefault(pair, []).append((seg.key, float(seg.length_m)))

    for pair, entries in by_pair.items():
        lengths = {round(length, 6) for _key, length in entries}
        if len(lengths) > 1:
            detail = ", ".join(k + "=" + str(v) for k, v in sorted(entries))
            findings.append(Finding(
                ERROR, "NETWORK", sorted(k for k, _ in entries)[0],
                "intersections " + pair[0] + " / " + pair[1] + " are spanned by "
                "segments of disagreeing length (" + detail + "): contradictory "
                "route distances"))

    # Every addressed-to resolves to a real segment with along in [0, 1].
    for entity in graph.entities.values():
        for edge in entity.edges:
            if edge.relation != "addressed-to":
                continue
            resolution = graph.resolve_address(edge.payload or {})
            if not resolution.resolved:
                findings.append(Finding(
                    _referential_severity(entity), "NETWORK", entity.key,
                    "`addressed-to` does not resolve to a real segment "
                    "(no segment on `" + str(resolution.street) + "` between its "
                    "two intersections)"))
                continue
            if resolution.along is not None and not resolution.along_in_range:
                findings.append(Finding(
                    ERROR, "NETWORK", entity.key,
                    "`addressed-to.along` is " + str(resolution.along)
                    + ", outside the required [0, 1] range"))


def check_reciprocity(graph, findings):
    """Each symmetric edge is answered by the same term from the other side."""
    for src_key, tgt_key, relation, _edge in graph.symmetric_links():
        target = graph.entities.get(tgt_key)
        if target is None:
            continue  # referential check already reports an unknown target
        same = [
            te for te in target.edges
            if te.is_symmetric and te.relation == relation
            and te.target_key == src_key
        ]
        if same:
            continue
        if target.is_stub:
            findings.append(Finding(
                WARNING, "RECIPROCITY", src_key,
                "counterpart `" + tgt_key + "` is a stub; reciprocity for "
                "symmetric `" + relation + "` not yet verifiable"))
            continue
        other = [
            te for te in target.edges
            if te.is_symmetric and te.target_key == src_key
        ]
        if other:
            rels = ", ".join(sorted(te.relation for te in other))
            findings.append(Finding(
                ERROR, "RECIPROCITY", src_key,
                "`" + src_key + " -[" + relation + "]- " + tgt_key + "` expects "
                "`" + relation + "` back, but " + tgt_key + " asserts: " + rels))
        else:
            findings.append(Finding(
                ERROR, "RECIPROCITY", src_key,
                "`" + src_key + " -[" + relation + "]- " + tgt_key + "` has no "
                "reciprocal `" + relation + "` edge back (symmetric edges are "
                "stored on both ends)"))


def check_zero_blanks(graph, findings):
    """A declared `## section` may not be empty (spec 6 / 11)."""
    for entity in graph.entities.values():
        for section in sorted(entity.empty_sections):
            findings.append(Finding(
                ERROR, "ZERO-BLANKS", entity.key,
                "declared section is present but empty: `## " + section + "` "
                "(a stub may be a stub, but a declared section may not be blank)"))


def check_reveal_tags(graph, findings):
    """Bracketed reveal tags must be well-formed (spec 11)."""
    for entity in graph.entities.values():
        for tag in entity.reveal_tags:
            if not eg.VALID_REVEAL_RE.match(tag.strip()):
                findings.append(Finding(
                    WARNING, "REVEAL-TAGS", entity.key,
                    "bracketed tag `[" + tag + "]` is not a recognized reveal "
                    "form (`[open]`, `[reveal: Book N]`, `[behavior-only]`)"))


def run_checks(graph):
    findings = []
    check_vocabulary(graph, findings)
    check_referential(graph, findings)
    check_folder_parent(graph, findings)
    check_acyclicity(graph, findings)
    check_network(graph, findings)
    check_reciprocity(graph, findings)
    check_zero_blanks(graph, findings)
    check_reveal_tags(graph, findings)
    return findings


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    strict = "--strict" in argv
    positional = [a for a in argv if not a.startswith("-")]
    geography_dir = positional[0] if positional else eg.GEOGRAPHY_DIR

    graph = eg.build_graph(geography_dir)
    findings = run_checks(graph)

    errors = [f for f in findings if f.severity == ERROR]
    warnings = [f for f in findings if f.severity == WARNING]

    edges = [e for ent in graph.entities.values() for e in ent.edges]
    stubs = [e for e in graph.entities.values() if e.is_stub]

    print("Geography structural validation for The Unnecessary")
    print("Geography tree: " + geography_dir)
    print("Entities parsed: " + str(len(graph.entities))
          + " (" + str(len(stubs)) + " stubs)")
    print("Segments: " + str(len(graph.segments()))
          + "  Streets: " + str(len(graph.streets())))
    print("Structured edges examined: " + str(len(edges)))
    print("")

    for warning in graph.parse_warnings:
        # Only the missing-tree note is interesting; per-file skips are noise.
        if "tree not found" in warning:
            print("Note: " + warning)
            print("")

    for label, bucket in (("ERRORS", errors), ("WARNINGS", warnings)):
        if not bucket:
            continue
        print(label + " (" + str(len(bucket)) + "):")
        for finding in sorted(bucket, key=Finding.sort_key):
            print("  [" + finding.category + "] " + finding.entity_key)
            print("      " + finding.message)
        print("")

    if errors:
        print("Result: FAIL. " + str(len(errors)) + " error(s), "
              + str(len(warnings)) + " warning(s).")
        return 1
    if strict and warnings:
        print("Result: FAIL (--strict). 0 errors, " + str(len(warnings))
              + " warning(s) treated as failures.")
        return 1
    print("Result: PASS. 0 errors, " + str(len(warnings)) + " warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
