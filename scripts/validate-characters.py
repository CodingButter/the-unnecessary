#!/usr/bin/env python3
"""Relational-integrity validator for The Unnecessary character profiles.

Standard library only. No third-party imports, no pip installs. Fast enough to
run on every change, the way scripts/validate-links.py does.

It reads the cast through scripts/characters_graph.py and checks the mechanical
relational contract from docs/20-canon/characters/profile-spec.md, the
"Relationship model" subsection. Rules go to this script; semantic judgement
(does the personality square with the backstory) stays with the Reconcile agent.

The model has exactly two legal edge classes:

  DIRECTIONAL  Stored once, on the dependent end, pointing at the authority
               (creator-of is authored on the creator). The inverse is DERIVED,
               never stored. Directional edges are NOT reciprocity-checked.
  SYMMETRIC    Stored on both ends; reciprocity-checked with the SAME term.

Checks:

  OFF-VOCAB     Every edge label is in the controlled vocabulary. A derived
                inverse (son, grandfather, mother-of, mentor-of, owner-of) or a
                freeform label (board-keeper-for) is rejected: map it, DROP it,
                or RE-HOME it to prose.
  RECIPROCITY   Every SYMMETRIC edge is matched from the other side with the
                same term. If A says `friend: B`, B says `friend: A`. Directional
                edges are exempt: their inverse is derived, not stored.
  CARDINALITY   At most one `father` and one `mother` per character.
  ACYCLICITY    No character is their own ancestor over father/mother/guardian.
  AGE LADDERS   A parent is older than their child by a plausible generational
                gap, cross-checked against the canonical birth-date spine.
  SURNAME       Members of one family share a surname; the filename surname
                agrees with the profile.
  ZERO-BLANKS   Every Section-4 house section is present and non-empty.
  REFERENTIAL   Every in-vocabulary edge points at a real profile.

Severity:

  ERROR    A hard violation of the contract. Fails the run.
  WARNING  An expected gap during the in-progress migration: a legacy profile
           with no structured edges, an edge to a still-proposed person, or a
           reciprocity pair that cannot be checked until the counterpart
           migrates. Reported, but does not fail by default.

Exit code:
  0  No errors (and, without --strict, regardless of warnings).
  1  One or more errors (or, with --strict, any error or warning).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import characters_graph as cg


ERROR = "ERROR"
WARNING = "WARNING"


class Finding:
    def __init__(self, severity, category, char_id, message):
        self.severity = severity
        self.category = category
        self.char_id = char_id
        self.message = message

    def sort_key(self):
        order = 0 if self.severity == ERROR else 1
        return (order, self.category, self.char_id, self.message)


def _spine_slugs(graph):
    """Id-form slugs for every person in the birth-date spine, both orders."""
    slugs = set()
    for key in graph.spine:
        slugs.add(key)
        reversed_form = cg.reverse_slug(key)
        if reversed_form:
            slugs.add(reversed_form)
    return slugs


def check_vocabulary(graph, findings):
    """Reject every off-vocabulary label. The mapping in profile-spec.md says,
    for each old label, whether to map it to a controlled term, DROP it as a
    derived inverse, or RE-HOME it to prose.
    """
    for char in graph.human_characters():
        for edge in char.edges:
            if edge.in_vocab:
                continue
            findings.append(Finding(
                ERROR, "OFF-VOCAB", char.id,
                "edge `" + edge.relation + ": " + edge.target_slug
                + "` is not in the controlled vocabulary. Map it to a "
                "directional or symmetric term, DROP it if it is a derived "
                "inverse, or RE-HOME it to prose (see profile-spec.md, "
                "the relationship model and its mapping table)."))


def check_referential(graph, findings):
    """Every in-vocabulary edge must resolve, unless it is a deliberate open
    slot, a proposed person, or a canon person in the spine whose profile is
    pending. Off-vocabulary edges are reported by check_vocabulary instead.
    """
    spine_slugs = _spine_slugs(graph)
    for char in graph.human_characters():
        for edge in char.edges:
            if not edge.in_vocab or edge.target_id is not None:
                continue
            if edge.open_slot:
                findings.append(Finding(
                    WARNING, "REFERENTIAL", char.id,
                    "edge `" + edge.relation + ": " + edge.target_slug
                    + "` is a deliberate open canon slot / unassigned "
                    "placeholder (no profile by design)"))
            elif edge.proposed:
                findings.append(Finding(
                    WARNING, "REFERENTIAL", char.id,
                    "edge `" + edge.relation + ": " + edge.target_slug
                    + "` points at a person with no profile yet (marked "
                    "proposed)"))
            elif (edge.target_slug in spine_slugs
                  or cg.reverse_slug(edge.target_slug) in spine_slugs):
                findings.append(Finding(
                    WARNING, "REFERENTIAL", char.id,
                    "edge `" + edge.relation + ": " + edge.target_slug
                    + "` names a canon person in the birth-date spine whose "
                    "profile is pending (not yet generated)"))
            else:
                findings.append(Finding(
                    ERROR, "REFERENTIAL", char.id,
                    "edge `" + edge.relation + ": " + edge.target_slug
                    + "` points at an unknown profile (no such character "
                    "and not in the birth-date spine)"))


def check_reciprocity(graph, findings):
    """Reciprocity is scoped to SYMMETRIC types only. A symmetric edge must be
    answered by the SAME symmetric term from the other side. Directional edges
    are exempt: the inverse is derived, never stored, so a back edge would be a
    defect, not a requirement.
    """
    for src_id, tgt_id, relation, _edge in graph.symmetric_links():
        char = graph.characters[src_id]
        target = graph.characters.get(tgt_id)
        if target is None or target.is_nonhuman:
            continue
        if not target.has_structured_edges:
            findings.append(Finding(
                WARNING, "RECIPROCITY", char.id,
                "counterpart `" + target.id + "` has no structured edges yet; "
                "reciprocity for symmetric `" + relation + "` unverifiable "
                "(legacy)"))
            continue

        same = [
            te for te in target.edges
            if te.is_symmetric and te.relation == relation
            and graph.resolve(te.target_slug) == src_id
        ]
        if same:
            continue

        other = [
            te for te in target.edges
            if te.is_symmetric and graph.resolve(te.target_slug) == src_id
        ]
        if other:
            rels = ", ".join(sorted(te.relation for te in other))
            findings.append(Finding(
                ERROR, "RECIPROCITY", char.id,
                "`" + src_id + " -[" + relation + "]- " + target.id
                + "` is symmetric and expects `" + relation + "` back, but "
                + target.id + " asserts: " + rels))
        else:
            findings.append(Finding(
                ERROR, "RECIPROCITY", char.id,
                "`" + src_id + " -[" + relation + "]- " + target.id
                + "` has no reciprocal `" + relation + "` edge back from `"
                + target.id + "` (symmetric edges are stored on both ends)"))


def check_cardinality(graph, findings):
    """At most one father and one mother per character."""
    for char in graph.human_characters():
        fathers = set()
        mothers = set()
        for edge in char.edges:
            key = edge.target_id or edge.target_slug
            if edge.relation == "father":
                fathers.add(key)
            elif edge.relation == "mother":
                mothers.add(key)
        if len(fathers) > 1:
            findings.append(Finding(
                ERROR, "CARDINALITY", char.id,
                "has " + str(len(fathers)) + " `father` edges: "
                + ", ".join(sorted(fathers)) + " (at most one allowed)"))
        if len(mothers) > 1:
            findings.append(Finding(
                ERROR, "CARDINALITY", char.id,
                "has " + str(len(mothers)) + " `mother` edges: "
                + ", ".join(sorted(mothers)) + " (at most one allowed)"))


def check_acyclicity(graph, findings):
    """No character is their own ancestor over the directional ancestry edges
    (father, mother, guardian)."""
    parents_of = {}
    for authority, dependent, relation, _edge in graph.directional_links():
        if relation in cg.ANCESTRY_RELATIONS:
            parents_of.setdefault(dependent, set()).add(authority)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}

    def visit(node, stack):
        color[node] = GRAY
        stack.append(node)
        for parent in sorted(parents_of.get(node, ())):
            if color.get(parent, WHITE) == GRAY:
                cycle = stack[stack.index(parent):] + [parent]
                findings.append(Finding(
                    ERROR, "ACYCLICITY", node,
                    "ancestry cycle: " + " -> ".join(cycle)))
                continue
            if color.get(parent, WHITE) == WHITE:
                visit(parent, stack)
        stack.pop()
        color[node] = BLACK

    for node in sorted(parents_of):
        if color.get(node, WHITE) == WHITE:
            visit(node, [])


def check_age_ladders(graph, findings):
    """A father/mother is older than their child by a plausible gap."""
    for parent_id, child_id, _relation in graph.parent_child_pairs():
        parent = graph.characters[parent_id]
        child = graph.characters[child_id]
        p_bd = parent.effective_birth_date
        c_bd = child.effective_birth_date
        if p_bd is None or c_bd is None:
            continue
        gap = cg.years_between(p_bd, c_bd)
        if gap <= 0:
            findings.append(Finding(
                ERROR, "AGE-LADDER", child_id,
                "parent `" + parent_id + "` (" + str(p_bd) + ") is not older "
                "than child `" + child_id + "` (" + str(c_bd) + ")"))
        elif gap < cg.MIN_PARENT_CHILD_GAP:
            findings.append(Finding(
                ERROR, "AGE-LADDER", child_id,
                "parent `" + parent_id + "` is only " + str(gap) + " years "
                "older than child `" + child_id + "` (minimum plausible gap is "
                + str(cg.MIN_PARENT_CHILD_GAP) + ")"))
        elif gap > cg.MAX_PARENT_CHILD_GAP:
            findings.append(Finding(
                ERROR, "AGE-LADDER", child_id,
                "parent `" + parent_id + "` is " + str(gap) + " years older "
                "than child `" + child_id + "` (above the plausible gap of "
                + str(cg.MAX_PARENT_CHILD_GAP) + ")"))


def check_spine_age_agreement(graph, findings):
    """Profile-stated age and birth date must agree with the canonical spine."""
    for char in graph.human_characters():
        if char.spine_age is not None and char.age is not None:
            if char.spine_age != char.age:
                findings.append(Finding(
                    ERROR, "AGE-LADDER", char.id,
                    "profile age " + str(char.age) + " disagrees with the "
                    "birth-date spine age " + str(char.spine_age)))
        if char.spine_birth_date and char.birth_date:
            if char.spine_birth_date != char.birth_date:
                findings.append(Finding(
                    ERROR, "AGE-LADDER", char.id,
                    "profile birth date " + str(char.birth_date) + " disagrees "
                    "with the spine " + str(char.spine_birth_date)))


def check_surnames(graph, findings):
    """Filename surname agreement, plus family-component surname agreement over
    father/mother (derived) and the symmetric `sibling` edges."""
    for char in graph.human_characters():
        if not char.surname:
            findings.append(Finding(
                WARNING, "SURNAME", char.id,
                "no surname could be derived from the profile"))
            continue
        if char.surname not in char.id.split("-"):
            findings.append(Finding(
                ERROR, "SURNAME", char.id,
                "profile surname `" + char.surname + "` does not appear in the "
                "filename id `" + char.id + "`"))

    adjacency = {}

    def link(a, b):
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)

    for parent_id, child_id, _relation in graph.parent_child_pairs():
        link(parent_id, child_id)
    for char in graph.human_characters():
        for edge in char.edges:
            if edge.relation == "sibling" and edge.target_id:
                link(char.id, edge.target_id)

    seen = set()
    for start in sorted(adjacency):
        if start in seen:
            continue
        component = []
        queue = [start]
        seen.add(start)
        while queue:
            node = queue.pop()
            component.append(node)
            for nxt in sorted(adjacency.get(node, ())):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        surnames = {}
        for node in component:
            ch = graph.characters.get(node)
            if ch and ch.surname:
                surnames.setdefault(ch.surname, []).append(node)
        if len(surnames) > 1:
            detail = "; ".join(
                s + ": " + ", ".join(sorted(ids))
                for s, ids in sorted(surnames.items())
            )
            findings.append(Finding(
                ERROR, "SURNAME", sorted(component)[0],
                "family group has disagreeing surnames (" + detail
                + ") -- spouses who married in are expected to differ; blood "
                "relatives are not"))


def check_completeness(graph, findings):
    for char in graph.human_characters():
        missing = char.missing_sections
        empty = sorted(s for s in char.empty_sections if s in cg.REQUIRED_SECTIONS)
        if char.is_v2:
            for section in missing:
                findings.append(Finding(
                    ERROR, "ZERO-BLANKS", char.id,
                    "missing required section: `## " + section + "`"))
            for section in empty:
                findings.append(Finding(
                    ERROR, "ZERO-BLANKS", char.id,
                    "required section is present but empty: `## " + section + "`"))
        else:
            findings.append(Finding(
                WARNING, "ZERO-BLANKS", char.id,
                "legacy profile not yet migrated to the enrichment schema "
                "(missing " + str(len(missing)) + " of "
                + str(len(cg.REQUIRED_SECTIONS)) + " house sections)"))


def run_checks(graph):
    findings = []
    check_vocabulary(graph, findings)
    check_referential(graph, findings)
    check_reciprocity(graph, findings)
    check_cardinality(graph, findings)
    check_acyclicity(graph, findings)
    check_age_ladders(graph, findings)
    check_spine_age_agreement(graph, findings)
    check_surnames(graph, findings)
    check_completeness(graph, findings)
    return findings


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    strict = "--strict" in argv

    graph = cg.build_graph()
    findings = run_checks(graph)

    errors = [f for f in findings if f.severity == ERROR]
    warnings = [f for f in findings if f.severity == WARNING]

    human = graph.human_characters()
    v2 = [c for c in human if c.is_v2]
    edges = [e for c in human for e in c.edges]
    off_vocab = [e for e in edges if not e.in_vocab]

    print("Character relational-integrity validation for The Unnecessary")
    print("Profiles directory: " + cg.PROFILES_DIR)
    print("Human profiles checked: " + str(len(human)))
    print("Migrated (v2, structured edges or full schema): " + str(len(v2)))
    print("Birth-date spine rows: " + str(len(graph.spine)))
    print("Structured edges examined: " + str(len(edges))
          + " (" + str(len(edges) - len(off_vocab)) + " in-vocabulary, "
          + str(len(off_vocab)) + " off-vocabulary)")
    print("")

    for label, bucket in (("ERRORS", errors), ("WARNINGS", warnings)):
        if not bucket:
            continue
        print(label + " (" + str(len(bucket)) + "):")
        for f in sorted(bucket, key=Finding.sort_key):
            print("  [" + f.category + "] " + f.char_id)
            print("      " + f.message)
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
