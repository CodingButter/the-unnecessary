#!/usr/bin/env python3
"""Lock-model rails -- the immutability validator for The Unnecessary's entities.

Standard library only. No third-party imports, no pip installs. No side effects on
import: the module only defines constants, classes, and functions; nothing walks the
disk or shells out to git until a caller invokes main(). It is READ-ONLY on canon --
it never writes an entity file, never installs a git hook, and never edits the spec.
It reuses the fenced-yaml subset parser in scripts/entity_graph.py (the single reader
of the entity tree); it does not re-implement parsing.

THE LOCK MODEL (the convention this script enforces). Every structured fact, edge, and
timeline entry in an entity's fenced ```yaml block carries a lock state:

  locked    established by approved prose or a bible; IMMUTABLE; carries `by:` source.
  proposed  asserted by draft prose; carries `by:`; hardens to locked on approval.
  open      deduced / mutable; must not contradict a locked item or a bible.

The scalar facts/edges/timeline stay as-is; a parallel `locks:` map keyed by dotted
path carries the state. Dotted keys are `facts.<key>`, `edges.<label>`, and
`timeline.<0-based-index>`:

    facts: { capability: continuous-respiratory-support }
    edges: { owner: okafor-lena }
    timeline:
      - { when: 2053-10-03T23:59, set: { remote_auth: lost } }
    locks:
      facts.capability: { state: locked, by: b1-ch1 }
      edges.owner:      { state: locked, by: b1-ch1 }
      timeline.0:       { state: locked, by: master-timeline }

Checks:

  COVERAGE      Every fact / edge / timeline entry SHOULD carry a `locks` entry.
                Un-stated items are reported as WARNINGS with a count and a sample
                (pre-sweep the tree is mostly un-stated -- expected, not a failure).
  IMMUTABILITY  The core. With `--diff <ref>` (default HEAD), for every entity file
                changed against the ref the OLD (`git show <ref>:<path>`) and NEW
                (working tree) blocks are parsed. If any item whose OLD lock state was
                `locked` has a CHANGED value, was REMOVED, or had its lock entry
                DOWNGRADED away from `locked`, that is an ERROR. Adding new items and
                promoting open -> proposed -> locked are ALLOWED. Timeline entries are
                matched by content (when + set), not by raw index, so inserting a new
                dated entry does not falsely trip a locked one; the freeform `note:` is
                prose and is not part of the immutable value.
  INTRA-FILE    An open / proposed item must not duplicate a `locked` key with a
                different value in the same file (e.g. two fenced blocks disagreeing,
                or one block re-asserting a locked fact at a different value) -> ERROR.
                Conflicting lock STATES declared for one dotted path -> ERROR.
  SCHEMA        state is one of {locked, proposed, open}; a locked / proposed lock
                carries `by:`; every dotted-path lock key resolves to a real fact /
                edge / timeline index -> else ERROR.

Severity:

  ERROR    A hard violation of the lock contract. Fails the run.
  WARNING  An expected gap (an un-stated item in the un-migrated tree). Reported, but
           does not fail by default.

It MUST pass on the current (pre-sweep) tree: nothing is locked yet, so there is nothing
to violate -- only COVERAGE warnings. Legacy / non-entity markdown (no fenced block with
facts / edges / timeline) is skipped, never failed on.

Exit code:
  0  No errors (and, without --strict, regardless of warnings).
  1  One or more errors (or, with --strict, any error or warning).
"""

import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import entity_graph as eg


ERROR = "ERROR"
WARNING = "WARNING"

VALID_STATES = ("locked", "proposed", "open")
STATES_NEEDING_SOURCE = ("locked", "proposed")

# Default canon root and the parts of the tree that are scaffolding, not entities.
DEFAULT_ROOT = os.path.join(eg.REPO_ROOT, "docs", "20-canon")
SKIP_DIR_PARTS = ("_templates",)
SKIP_NAMES = ("index.md",)

# How many missing-lock paths to list per file in a COVERAGE warning.
COVERAGE_SAMPLE = 6


class Finding:
    def __init__(self, severity, category, entity_key, message):
        self.severity = severity
        self.category = category
        self.entity_key = entity_key
        self.message = message

    def sort_key(self):
        order = 0 if self.severity == ERROR else 1
        return (order, self.category, self.entity_key, self.message)


# ===========================================================================
# Parsing one entity's structured block into a lock-aware document.
# ===========================================================================


class LockedDoc:
    """The lock-relevant structured content of one entity file.

    `facts` / `edges` are the merged mappings; `timeline` the merged list; `locks`
    the merged dotted-path -> {state, by} map -- all merged across the file's fenced
    ```yaml blocks exactly the way entity_graph reads them (later block wins). `blocks`
    keeps the per-block parse so the intra-file check can see cross-block disagreement
    that the merge would otherwise hide.
    """

    def __init__(self):
        self.facts = {}
        self.edges = {}
        self.timeline = []
        self.locks = {}
        self.blocks = []   # list of (facts, edges, timeline, locks) per fenced block

    @property
    def in_scope(self):
        """An entity is in lock scope once it has any lockable item."""
        return bool(self.items())

    def items(self):
        """Every lockable item as (dotted_path, comparable_value).

        facts.<key> and edges.<label> carry their value directly; timeline.<i> carries
        its content (when + set) -- the load-bearing structured fact, not the prose note.
        """
        out = []
        for key in self.facts:
            out.append(("facts." + str(key), self.facts[key]))
        for label in self.edges:
            out.append(("edges." + str(label), self.edges[label]))
        for index, entry in enumerate(self.timeline):
            out.append(("timeline." + str(index), _timeline_content(entry)))
        return out

    def value_at(self, path):
        """The comparable value for a dotted path, or None if it does not resolve."""
        ns, name = _split_path(path)
        if ns == "facts" and name in self.facts:
            return self.facts[name]
        if ns == "edges" and name in self.edges:
            return self.edges[name]
        if ns == "timeline":
            index = _as_index(name)
            if index is not None and 0 <= index < len(self.timeline):
                return _timeline_content(self.timeline[index])
        return _MISSING

    def resolves(self, path):
        ns, name = _split_path(path)
        if ns == "facts":
            return name in self.facts
        if ns == "edges":
            return name in self.edges
        if ns == "timeline":
            index = _as_index(name)
            return index is not None and 0 <= index < len(self.timeline)
        return False

    def state_of(self, path):
        entry = self.locks.get(path)
        if isinstance(entry, dict):
            return entry.get("state")
        return None


_MISSING = object()


def _split_path(path):
    """Split a dotted lock key into (namespace, name); name is '' when absent."""
    text = str(path)
    if "." in text:
        ns, name = text.split(".", 1)
        return ns, name
    return text, ""


def _as_index(name):
    try:
        return int(str(name))
    except (TypeError, ValueError):
        return None


def _timeline_content(entry):
    """The immutable content of a timeline entry: when + set, never the prose note."""
    if isinstance(entry, dict):
        return {"when": entry.get("when"), "set": entry.get("set")}
    return entry


def _canon(value):
    """A deterministic, order-independent string form for value comparison.

    Maps are sorted by key; sequences are sorted (edge target lists are unordered),
    so `connects: [a, b]` and `[b, a]` compare equal and a list reorder is not a
    spurious mutation.
    """
    if isinstance(value, dict):
        return "{" + ",".join(
            str(k) + "=" + _canon(value[k]) for k in sorted(value, key=str)
        ) + "}"
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(sorted(_canon(item) for item in value)) + "]"
    return str(value)


def parse_locked_doc(text):
    """Parse an entity file's text into a LockedDoc. Never raises on content."""
    doc = LockedDoc()
    if not text:
        return doc
    _fm, body = eg.split_frontmatter(text)
    merged = {}
    for block_text in eg.extract_yaml_blocks(body):
        parsed = eg.parse_yaml(block_text)
        if not isinstance(parsed, dict):
            continue
        b_facts = parsed.get("facts") if isinstance(parsed.get("facts"), dict) else {}
        b_edges = parsed.get("edges") if isinstance(parsed.get("edges"), dict) else {}
        b_time = parsed.get("timeline") if isinstance(parsed.get("timeline"), list) else []
        b_locks = parsed.get("locks") if isinstance(parsed.get("locks"), dict) else {}
        doc.blocks.append((b_facts, b_edges, b_time, b_locks))
        merged.update(parsed)
    doc.facts = merged.get("facts") if isinstance(merged.get("facts"), dict) else {}
    doc.edges = merged.get("edges") if isinstance(merged.get("edges"), dict) else {}
    doc.timeline = merged.get("timeline") if isinstance(merged.get("timeline"), list) else []
    doc.locks = merged.get("locks") if isinstance(merged.get("locks"), dict) else {}
    return doc


# ===========================================================================
# Walking the tree (working copy) for coverage / schema / intra-file checks.
# ===========================================================================


def _is_skipped(path):
    parts = path.replace(os.sep, "/").split("/")
    if os.path.basename(path) in SKIP_NAMES:
        return True
    return any(part in SKIP_DIR_PARTS for part in parts)


def walk_entity_files(root):
    """Yield (rel_key, abs_path) for every candidate entity markdown under root."""
    if not os.path.isdir(root):
        return
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            if _is_skipped(path):
                continue
            yield _rel_key(path, root), path


def _rel_key(path, root):
    rel = os.path.relpath(path, root)
    rel = rel[:-3] if rel.endswith(".md") else rel
    return rel.replace(os.sep, "/")


def _read(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return None


# ===========================================================================
# Checks.
# ===========================================================================


def check_schema(key, doc, findings):
    """state vocabulary, required `by:`, and dotted-path resolvability (spec 11)."""
    for path, entry in doc.locks.items():
        if not isinstance(entry, dict):
            findings.append(Finding(
                ERROR, "SCHEMA", key,
                "lock `" + str(path) + "` is malformed: expected a mapping like "
                "`{ state: locked, by: <source> }`"))
            continue
        if not doc.resolves(path):
            findings.append(Finding(
                ERROR, "SCHEMA", key,
                "lock key `" + str(path) + "` resolves to no real fact / edge / "
                "timeline index in this file"))
        state = entry.get("state")
        if state not in VALID_STATES:
            findings.append(Finding(
                ERROR, "SCHEMA", key,
                "lock `" + str(path) + "` has state `" + str(state) + "`, not one "
                "of {locked, proposed, open}"))
            continue
        if state in STATES_NEEDING_SOURCE and not entry.get("by"):
            findings.append(Finding(
                ERROR, "SCHEMA", key,
                "lock `" + str(path) + "` is " + state + " but carries no `by:` "
                "source (locked / proposed items must name their authority)"))


def check_coverage(key, doc, findings):
    """Every lockable item should carry a lock state; un-stated ones are warnings."""
    missing = [path for path, _value in doc.items() if path not in doc.locks]
    if not missing:
        return
    sample = ", ".join(missing[:COVERAGE_SAMPLE])
    if len(missing) > COVERAGE_SAMPLE:
        sample += ", ..."
    findings.append(Finding(
        WARNING, "COVERAGE", key,
        str(len(missing)) + " of " + str(len(doc.items())) + " structured items "
        "carry no lock state (pre-sweep / un-stated): " + sample))
    return len(missing)


def check_intrafile(key, doc, findings):
    """An open/proposed item must not contradict a locked value of the same key, and
    one dotted path must not be declared with two different lock states."""
    # Conflicting lock states across blocks for one path.
    by_path_state = {}
    for _f, _e, _t, b_locks in doc.blocks:
        for path, entry in b_locks.items():
            if isinstance(entry, dict):
                by_path_state.setdefault(str(path), set()).add(entry.get("state"))
    for path, states in by_path_state.items():
        real = {s for s in states if s is not None}
        if len(real) > 1:
            findings.append(Finding(
                ERROR, "INTRA-FILE", key,
                "lock `" + path + "` is declared with conflicting states ("
                + ", ".join(sorted(str(s) for s in real)) + ") in one file"))

    # Same facts/edges key asserted with different values where one assertion is
    # locked (cross-block disagreement the merge would otherwise hide).
    defs = {}   # (namespace, name) -> list of (canon_value, state)
    for b_facts, b_edges, _t, b_locks in doc.blocks:
        for namespace, mapping in (("facts", b_facts), ("edges", b_edges)):
            for name, value in mapping.items():
                path = namespace + "." + str(name)
                entry = b_locks.get(path)
                state = entry.get("state") if isinstance(entry, dict) else None
                defs.setdefault((namespace, str(name)), []).append((_canon(value), state))
    for (namespace, name), records in defs.items():
        values = {cv for cv, _s in records}
        if len(values) <= 1:
            continue
        locked_values = {cv for cv, s in records if s == "locked"}
        if locked_values:
            findings.append(Finding(
                ERROR, "INTRA-FILE", key,
                "`" + namespace + "." + name + "` is asserted with disagreeing "
                "values where one is locked (" + " | ".join(sorted(values))
                + "); an open/proposed item may not contradict a locked one"))


def check_immutability(ref, root, findings, stats):
    """Diff against `ref`: a locked item may not change value, vanish, or be
    downgraded away from locked. New items and promotions are allowed."""
    if not _git_ref_ok(ref):
        stats["git_ok"] = False
        return
    stats["git_ok"] = True
    rel_root = os.path.relpath(root, eg.REPO_ROOT)
    changed = _git_changed(ref, rel_root)
    if changed is None:
        stats["git_ok"] = False
        return
    examined = 0
    for rel_path in changed:
        if not rel_path.endswith(".md") or _is_skipped(rel_path):
            continue
        old_text = _git_show(ref, rel_path)
        new_text = _read(os.path.join(eg.REPO_ROOT, rel_path))
        old_doc = parse_locked_doc(old_text)
        new_doc = parse_locked_doc(new_text)
        # Only files with locked items in the OLD revision constrain anything.
        old_locked = [p for p, _v in old_doc.items() if old_doc.state_of(p) == "locked"]
        if not old_locked:
            continue
        examined += 1
        if new_text is None:
            findings.append(Finding(
                ERROR, "IMMUTABILITY", rel_path,
                "file was deleted but held " + str(len(old_locked)) + " locked "
                "item(s); locked canon may not be destroyed"))
            continue
        _diff_one(rel_path, old_doc, new_doc, old_locked, findings)
    stats["examined"] = examined


def _diff_one(key, old_doc, new_doc, old_locked, findings):
    for path in old_locked:
        ns, _name = _split_path(path)
        if ns in ("facts", "edges"):
            new_value = new_doc.value_at(path)
            if new_value is _MISSING:
                findings.append(Finding(
                    ERROR, "IMMUTABILITY", key,
                    "locked `" + path + "` was removed; a locked item is immutable"))
                continue
            if _canon(new_value) != _canon(old_doc.value_at(path)):
                findings.append(Finding(
                    ERROR, "IMMUTABILITY", key,
                    "locked `" + path + "` changed value (was `"
                    + _canon(old_doc.value_at(path)) + "`, now `"
                    + _canon(new_value) + "`)"))
                continue
            if new_doc.state_of(path) != "locked":
                findings.append(Finding(
                    ERROR, "IMMUTABILITY", key,
                    "locked `" + path + "` was downgraded to `"
                    + str(new_doc.state_of(path)) + "`; locked is immutable"))
        elif ns == "timeline":
            _diff_timeline_entry(key, old_doc, new_doc, path, findings)


def _diff_timeline_entry(key, old_doc, new_doc, path, findings):
    """Match a locked OLD timeline entry to NEW by content, so inserts/reorders are
    allowed but mutating or deleting the locked entry, or downgrading it, is not."""
    old_content = _canon(old_doc.value_at(path))
    matches = [
        index for index in range(len(new_doc.timeline))
        if _canon(_timeline_content(new_doc.timeline[index])) == old_content
    ]
    if not matches:
        findings.append(Finding(
            ERROR, "IMMUTABILITY", key,
            "locked `" + path + "` (" + old_content + ") was changed or removed; a "
            "locked timeline entry is immutable"))
        return
    if not any(new_doc.state_of("timeline." + str(i)) == "locked" for i in matches):
        findings.append(Finding(
            ERROR, "IMMUTABILITY", key,
            "locked timeline entry (" + old_content + ") survives but its lock was "
            "downgraded away from locked; locked is immutable"))


# ===========================================================================
# Git plumbing (read-only; no hooks, no writes).
# ===========================================================================


def _git(args):
    try:
        proc = subprocess.run(
            ["git", "-C", eg.REPO_ROOT] + args,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except OSError:
        return None
    return proc


def _git_ref_ok(ref):
    proc = _git(["rev-parse", "--verify", "--quiet", ref + "^{commit}"])
    return proc is not None and proc.returncode == 0


def _git_changed(ref, rel_root):
    proc = _git(["diff", "--name-only", ref, "--", rel_root])
    if proc is None or proc.returncode != 0:
        return None
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def _git_show(ref, rel_path):
    proc = _git(["show", ref + ":" + rel_path])
    if proc is None or proc.returncode != 0:
        return None
    return proc.stdout


# ===========================================================================
# Driver.
# ===========================================================================


def run_checks(root, ref):
    findings = []
    stats = {"files": 0, "in_scope": 0, "items": 0, "missing": 0,
             "git_ok": None, "examined": 0}
    for key, path in walk_entity_files(root):
        stats["files"] += 1
        doc = parse_locked_doc(_read(path))
        if not doc.in_scope:
            continue
        stats["in_scope"] += 1
        stats["items"] += len(doc.items())
        check_schema(key, doc, findings)
        missing = check_coverage(key, doc, findings)
        if missing:
            stats["missing"] += missing
        check_intrafile(key, doc, findings)
    check_immutability(ref, root, findings, stats)
    return findings, stats


def _parse_args(argv):
    ref = "HEAD"
    root = DEFAULT_ROOT
    strict = False
    index = 0
    while index < len(argv):
        token = argv[index]
        if token == "--diff":
            if index + 1 < len(argv) and not argv[index + 1].startswith("-"):
                ref = argv[index + 1]
                index += 1
        elif token.startswith("--diff="):
            ref = token.split("=", 1)[1]
        elif token == "--root":
            if index + 1 < len(argv):
                root = argv[index + 1]
                index += 1
        elif token.startswith("--root="):
            root = token.split("=", 1)[1]
        elif token == "--strict":
            strict = True
        index += 1
    if not os.path.isabs(root):
        root = os.path.join(eg.REPO_ROOT, root)
    return ref, root, strict


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    ref, root, strict = _parse_args(argv)

    findings, stats = run_checks(root, ref)
    errors = [f for f in findings if f.severity == ERROR]
    warnings = [f for f in findings if f.severity == WARNING]

    print("Lock-model validation for The Unnecessary")
    print("Canon root: " + root)
    print("Entity files scanned: " + str(stats["files"])
          + " (" + str(stats["in_scope"]) + " carry structured items)")
    print("Lockable items: " + str(stats["items"])
          + " (" + str(stats["items"] - stats["missing"]) + " stated, "
          + str(stats["missing"]) + " un-stated)")
    if stats["git_ok"]:
        print("Immutability diff vs `" + ref + "`: "
              + str(stats["examined"]) + " changed file(s) with locked items examined")
    else:
        print("Immutability diff vs `" + ref + "`: skipped (ref unavailable or "
              "not a git tree)")
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
