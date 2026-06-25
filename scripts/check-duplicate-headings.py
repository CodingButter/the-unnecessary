#!/usr/bin/env python3
"""Duplicate-authority check for The Unnecessary documentation tree.

Standard library only. No third-party imports, no pip installs.

Purpose, per master spec Phase 10 "Duplicate Authority Check":
  Look for repeated authoritative headings and duplicated long passages across
  DIFFERENT active canon files, and REPORT them. This script never deletes,
  merges, deduplicates, or rewrites anything. The report is the deliverable.
  ("Do not automatically delete duplicates. Report them.")

Scope and exclusions:
  - Scans *.md under docs/.
  - EXCLUDES any path under an archive/ directory, so historical monoliths are
    never flagged against their split successors.
  - EXCLUDES any path that contains a _templates/ directory segment (for
    example docs/00-governance/_templates/ and docs/40-blueprints/_templates/),
    so template stubs are never reported as duplicate authority.

Allowed-versus-true duplication:
  - An index file legitimately summarizes and links to its authority files.
    Files whose front-matter document_type is "index" (and any file named
    index.md) are treated leniently: their repeated headings are reported in a
    separate, lower-priority "index summary" bucket, not as authority
    collisions.
  - Very short or generic shared headings (for example "Related indexes",
    "Common tasks", "Overview", "Summary", "Index", "Files in this directory")
    are ignored entirely, because navigational scaffolding repeats by design.
  - A heading must be reasonably specific (a minimum length, more than one
    word) before a cross-file repeat counts as a possible authority collision.

Long-passage duplication:
  - Long paragraphs (a minimum character length) that appear verbatim in two or
    more different files are reported. Code fences and Mermaid blocks are
    skipped so shared diagram syntax is not flagged.

Exit code:
  - Informational only. The script returns 0 after printing its report; a human
    reviewer and the orchestrator judge each reported item. It does not gate the
    phase, and it changes no file on disk.
"""

import os
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

# A heading shorter than this (after normalization) is too generic to flag.
MIN_HEADING_LEN = 12

# A passage must be at least this many characters to count as a long passage.
MIN_PASSAGE_LEN = 240

# Generic navigational headings that repeat by design and are never flagged.
GENERIC_HEADINGS = {
    "overview",
    "summary",
    "index",
    "purpose",
    "contents",
    "common tasks",
    "related indexes",
    "related documents",
    "files in this directory",
    "files",
    "read first",
    "authority",
    "status",
    "scope",
    "notes",
    "see also",
    "how to use",
    "quick reference",
    "tags",
    "sources",
}


def is_excluded(path):
    """True for any path under archive/ or inside a _templates/ directory."""
    parts = path.replace("\\", "/").split("/")
    if "archive" in parts:
        return True
    if "_templates" in parts:
        return True
    return False


def read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.readlines()
    except OSError:
        return []


def front_matter_document_type(lines):
    """Return the document_type value from front matter, or None."""
    if not lines or lines[0].rstrip("\n") != "---":
        return None
    for index in range(1, len(lines)):
        raw = lines[index].rstrip("\n")
        if raw == "---":
            return None
        if raw[:1].isspace():
            continue
        stripped = raw.strip()
        if stripped.startswith("document_type:"):
            value = stripped.split(":", 1)[1].strip()
            return unquote(value)
    return None


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def body_start_index(lines):
    if lines and lines[0].rstrip("\n") == "---":
        for index in range(1, len(lines)):
            if lines[index].rstrip("\n") == "---":
                return index + 1
    return 0


def normalize_heading(text):
    """Lowercase, collapse whitespace, strip trailing punctuation."""
    cleaned = " ".join(text.split()).strip().lower()
    cleaned = cleaned.rstrip(".:;,")
    return cleaned


def extract_headings(lines, start_index):
    """Return a list of normalized ATX headings (lines starting with #)."""
    headings = []
    in_fence = False
    for index in range(start_index, len(lines)):
        line = lines[index].rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith("#"):
            text = stripped.lstrip("#").strip()
            norm = normalize_heading(text)
            if norm:
                headings.append(norm)
    return headings


def extract_paragraphs(lines, start_index):
    """Return normalized long paragraphs, skipping fenced and table blocks."""
    paragraphs = []
    buffer = []
    in_fence = False

    def flush():
        if not buffer:
            return
        joined = " ".join(part.strip() for part in buffer)
        joined = " ".join(joined.split())
        if len(joined) >= MIN_PASSAGE_LEN:
            paragraphs.append(joined)
        buffer.clear()

    for index in range(start_index, len(lines)):
        line = lines[index].rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if stripped == "":
            flush()
            continue
        # Skip headings, table rows, and list-only scaffolding from passages.
        if stripped.startswith("#"):
            flush()
            continue
        if stripped.startswith("|"):
            flush()
            continue
        buffer.append(stripped)

    flush()
    return paragraphs


def gather_files():
    found = []
    for root, _dirs, files in os.walk(DOCS_DIR):
        for name in files:
            if not name.endswith(".md"):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, REPO_ROOT)
            if is_excluded(rel):
                continue
            found.append(full)
    found.sort()
    return found


def is_index_file(path, doc_type):
    if os.path.basename(path).lower() == "index.md":
        return True
    if doc_type and doc_type.lower() == "index":
        return True
    return False


def doc_types_of(holders):
    """Return the set of document_type values present among holders."""
    return {doc_type for _rel, _flag, doc_type in holders}


def main():
    files = gather_files()

    # heading -> set of (relpath, is_index, doc_type)
    heading_map = {}
    # passage -> set of (relpath, is_index, doc_type)
    passage_map = {}

    for path in files:
        lines = read_lines(path)
        rel = os.path.relpath(path, REPO_ROOT)
        doc_type = front_matter_document_type(lines) or "unknown"
        index_flag = is_index_file(path, doc_type)
        start = body_start_index(lines)

        for heading in extract_headings(lines, start):
            if heading in GENERIC_HEADINGS:
                continue
            if len(heading) < MIN_HEADING_LEN:
                continue
            if len(heading.split()) < 2:
                continue
            heading_map.setdefault(heading, set()).add((rel, index_flag, doc_type))

        for passage in extract_paragraphs(lines, start):
            passage_map.setdefault(passage, set()).add((rel, index_flag, doc_type))

    # Partition repeats into three buckets so the "true duplication" signal is
    # not drowned by structural scaffolding:
    #
    #   cross_domain  : shared across files of MORE THAN ONE document_type, none
    #                   of them an index. This is the genuine duplicate-authority
    #                   risk (for example an act heading living in a timeline
    #                   file AND a world file AND a plot file).
    #   index_summary : at least one sharer is an index file. An index that
    #                   summarizes and links to its authority is allowed.
    #   structural    : shared only among files of a SINGLE document_type (a
    #                   parallel family built from one template, for example
    #                   every character-state file having an "active goals"
    #                   section). Reported as a count and a summary line only,
    #                   because uniform section skeletons are expected by design.
    cross_domain_headings = []
    index_summary_headings = []
    structural_headings = []

    for heading, holders in sorted(heading_map.items()):
        files_holding = sorted({rel for rel, _flag, _dt in holders})
        if len(files_holding) < 2:
            continue
        has_index = any(flag for _rel, flag, _dt in holders)
        types = doc_types_of(holders)
        if has_index:
            index_summary_headings.append((heading, files_holding, sorted(types)))
        elif len(types) >= 2:
            cross_domain_headings.append((heading, files_holding, sorted(types)))
        else:
            structural_headings.append((heading, files_holding, sorted(types)))

    # Long passages get the same partitioning. A verbatim passage that crosses
    # document_type boundaries is the strongest duplicate-authority signal.
    cross_domain_passages = []
    structural_passages = []
    index_passages = []

    for passage, holders in sorted(passage_map.items()):
        files_holding = sorted({rel for rel, _flag, _dt in holders})
        if len(files_holding) < 2:
            continue
        has_index = any(flag for _rel, flag, _dt in holders)
        types = doc_types_of(holders)
        if has_index:
            index_passages.append((passage, files_holding))
        elif len(types) >= 2:
            cross_domain_passages.append((passage, files_holding))
        else:
            structural_passages.append((passage, files_holding))

    print("Duplicate-authority report for The Unnecessary")
    print("Docs root: " + DOCS_DIR)
    print("Active canon files scanned: " + str(len(files)))
    print("(archive/ and any _templates/ directory excluded)")
    print("")

    print("=== Cross-domain authoritative headings (HIGH priority) ===")
    print("A specific heading living in two or more files of DIFFERENT")
    print("document_type is the genuine duplicate-authority risk: the same fact")
    print("may be stated in more than one place that claims authority.")
    print("")
    if not cross_domain_headings:
        print("None found.")
    else:
        print("Count: " + str(len(cross_domain_headings)))
        print("")
        for heading, holders, types in cross_domain_headings:
            print('  heading: "' + heading + '"')
            print("      document_types: " + ", ".join(types))
            for rel in holders:
                print("      - " + rel)
    print("")

    print("=== Index-summary heading repeats (allowed when they link to authority) ===")
    if not index_summary_headings:
        print("None found.")
    else:
        print("Count: " + str(len(index_summary_headings)))
        print("These involve at least one index file. An index summarizing and")
        print("linking to its authority is allowed, not a duplication failure.")
        print("")
        for heading, holders, _types in index_summary_headings:
            print('  heading: "' + heading + '"')
            for rel in holders:
                print("      - " + rel)
    print("")

    print("=== Structural heading repeats within a single document_type (LOW priority) ===")
    print("These headings repeat across a parallel family built from one")
    print("template (for example every character-state file). Uniform section")
    print("skeletons are expected by design and are not duplicate authority.")
    if not structural_headings:
        print("None found.")
    else:
        print("Count: " + str(len(structural_headings)))
        print("(headings listed without per-file expansion to keep the signal clear)")
        for heading, holders, types in structural_headings:
            print('  heading: "' + heading + '"  (' + ", ".join(types)
                  + ", " + str(len(holders)) + " files)")
    print("")

    print("=== Cross-domain duplicated long passages (HIGH priority) ===")
    print("A long passage repeated verbatim across files of different")
    print("document_type is the strongest duplicate-authority signal.")
    print("Reported, never edited.")
    print("")
    if not cross_domain_passages:
        print("None found.")
    else:
        print("Count: " + str(len(cross_domain_passages)))
        print("")
        for passage, holders in cross_domain_passages:
            preview = passage[:160]
            if len(passage) > 160:
                preview = preview + " ..."
            print("  passage: " + preview)
            for rel in holders:
                print("      - " + rel)
            print("")

    print("=== Structural or index long-passage repeats (LOW priority) ===")
    print("Passages repeated within one document_type family, or that involve")
    print("an index file (shared footers, shared baseline preambles). Expected")
    print("scaffolding, not duplicate authority.")
    low_priority_passages = structural_passages + index_passages
    if not low_priority_passages:
        print("None found.")
    else:
        print("Count: " + str(len(low_priority_passages)))
        print("")
        for passage, holders in low_priority_passages:
            preview = passage[:120]
            if len(passage) > 120:
                preview = preview + " ..."
            print("  passage: " + preview)
            print("      shared by " + str(len(holders)) + " files")
    print("")

    print("Report only. No file was changed. Exit code is informational.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
