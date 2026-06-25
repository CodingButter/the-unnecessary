#!/usr/bin/env python3
"""Metadata validator for The Unnecessary documentation tree.

Standard library only. No third-party imports, no pip installs.

What it checks, per master spec Phase 10 "Metadata Validator" and the required
field list in spec Phase 3:

  Every active document *.md under docs/ that has YAML front matter must
  declare all eight required top-level fields:

      title
      document_type
      status
      authority
      summary
      tags
      related
      source_documents

For each file the validator reports any missing field. It exits non-zero when
any active document is missing one or more required fields, so it can gate the
phase.

Files without any front matter at all are skipped with a notice rather than
failed. Some templates intentionally omit front matter (for example a stub that
opens with an HTML comment), and those are not active documents to enforce. The
chapter-blueprint template DOES carry front matter, so it is checked normally.

Front-matter reader:
  - The front matter is the block between the first two lines that are exactly
    "---".
  - A top-level field is a line with no leading whitespace whose text before
    the first ":" is the field name. This is enough to confirm presence; the
    validator checks presence, not value shape.
"""

import os
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

REQUIRED_FIELDS = [
    "title",
    "document_type",
    "status",
    "authority",
    "summary",
    "tags",
    "related",
    "source_documents",
]


def has_front_matter(lines):
    """True when the file opens with a --- fence and has a closing fence."""
    if not lines or lines[0].rstrip("\n") != "---":
        return False
    for index in range(1, len(lines)):
        if lines[index].rstrip("\n") == "---":
            return True
    return False


def front_matter_top_keys(lines):
    """Return the set of top-level field names declared in the front matter."""
    keys = set()
    if not has_front_matter(lines):
        return keys

    for index in range(1, len(lines)):
        raw = lines[index]
        if raw.rstrip("\n") == "---":
            break
        # Skip indented lines (list items, nested values).
        if raw[:1].isspace():
            continue
        stripped = raw.strip()
        if stripped == "" or stripped.startswith("#"):
            continue
        if ":" in stripped:
            key = stripped.split(":", 1)[0].strip()
            if key:
                keys.add(key)
    return keys


def gather_markdown_files():
    found = []
    for root, _dirs, files in os.walk(DOCS_DIR):
        for name in files:
            if name.endswith(".md"):
                found.append(os.path.join(root, name))
    found.sort()
    return found


def main():
    md_files = gather_markdown_files()

    checked = 0
    skipped = []
    failures = []

    for md_path in md_files:
        try:
            with open(md_path, "r", encoding="utf-8") as handle:
                lines = handle.readlines()
        except OSError as error:
            failures.append((md_path, ["read-error: " + str(error)]))
            continue

        if not has_front_matter(lines):
            skipped.append(md_path)
            continue

        checked += 1
        keys = front_matter_top_keys(lines)
        missing = [field for field in REQUIRED_FIELDS if field not in keys]
        if missing:
            failures.append((md_path, missing))

    print("Metadata validation for The Unnecessary")
    print("Docs root: " + DOCS_DIR)
    print("Markdown files found: " + str(len(md_files)))
    print("Documents with front matter checked: " + str(checked))
    print("Documents without front matter skipped: " + str(len(skipped)))
    print("")

    if skipped:
        print("Notice: skipped (no front matter, treated as non-active or template):")
        for md_path in skipped:
            print("  - " + os.path.relpath(md_path, REPO_ROOT))
        print("")

    if not failures:
        print("Result: PASS. Every checked document declares all required fields.")
        return 0

    print("Result: FAIL. Documents missing required fields: " + str(len(failures)))
    print("Required fields: " + ", ".join(REQUIRED_FIELDS))
    print("")
    for md_path, missing in failures:
        rel = os.path.relpath(md_path, REPO_ROOT)
        print("  " + rel)
        print("      missing: " + ", ".join(missing))
    return 1


if __name__ == "__main__":
    sys.exit(main())
