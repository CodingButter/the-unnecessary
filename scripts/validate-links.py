#!/usr/bin/env python3
"""Link validator for The Unnecessary documentation tree.

Standard library only. No third-party imports, no pip installs.

What it checks, per master spec Phase 10 "Link Validator":
  - Relative Markdown links of the form ](path) inside the body.
  - Front-matter "related:" paths, resolved DOCUMENT-RELATIVE (from the
    directory of the file that declares them).
  - Front-matter "source_documents:" paths, resolved REPOSITORY-ROOT-RELATIVE
    (from the repository root), because those point back at the original
    monoliths and migrated files that live relative to the repo root.

It deliberately skips:
  - Absolute web links (http:, https:) and mailto: links.
  - Pure in-page anchors that start with "#".
  - The anchor fragment of any link (everything from the first "#").
  - Angle-bracket placeholders such as <existing-path> that appear only in
    template documents (a target containing "<" or ">" is treated as a
    non-path placeholder and ignored).

Scope:
  - All *.md files under docs/.
  - Optionally all *.md files under context-manifests/ when that directory
    exists (it holds Markdown indexes whose links also point into docs/).

Exit code:
  - 0 when every resolved target exists.
  - 1 when any target is broken (reported with the declaring file and the
    raw target string).

Front-matter reader:
  - The front matter is the block between the first two lines that are exactly
    "---". Only list items under "related:" and "source_documents:" are read.
  - The reader is intentionally small. It understands "key:" followed by
    indented "- value" list items and stops the current list when a new
    top-level key (no leading whitespace, ending in ":") appears.
"""

import os
import sys


# Resolve the repository root as the parent of this script's scripts/ folder.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

# Directories scanned for Markdown files. docs/ is required; context-manifests/
# is scanned only if present.
SCAN_DIRS = ["docs", "context-manifests"]


def is_skippable_target(raw):
    """Return True for targets that are not local file paths to validate."""
    target = raw.strip()
    if target == "":
        return True
    lowered = target.lower()
    if lowered.startswith("http://") or lowered.startswith("https://"):
        return True
    if lowered.startswith("mailto:"):
        return True
    if target.startswith("#"):
        return True
    # Angle-bracket placeholders from template files are not real paths.
    if "<" in target or ">" in target:
        return True
    return False


def strip_anchor(target):
    """Drop any #fragment so the file part can be checked on disk."""
    if "#" in target:
        return target.split("#", 1)[0]
    return target


def read_front_matter_lists(lines):
    """Return (related, source_documents) lists from the front matter block.

    The block is the text between the first two lines equal to "---". Only the
    two keys we care about are parsed; everything else in the block is ignored.
    """
    if not lines or lines[0].rstrip("\n") != "---":
        return [], []

    # Find the closing fence.
    end = None
    for index in range(1, len(lines)):
        if lines[index].rstrip("\n") == "---":
            end = index
            break
    if end is None:
        return [], []

    related = []
    source_documents = []
    current = None

    for index in range(1, end):
        raw = lines[index].rstrip("\n")
        stripped = raw.strip()
        if stripped == "":
            continue

        # A new top-level key (no leading whitespace) switches or closes lists.
        if not raw[:1].isspace():
            if stripped.startswith("related:"):
                current = related
                continue
            if stripped.startswith("source_documents:"):
                current = source_documents
                continue
            # Any other top-level key ends the list we were collecting.
            current = None
            continue

        # Indented list item under the active key.
        if current is not None and stripped.startswith("- "):
            value = stripped[2:].strip()
            value = unquote(value)
            if value:
                current.append(value)

    return related, source_documents


def unquote(value):
    """Remove a single matching pair of surrounding quotes if present."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def extract_inline_links(lines, start_index):
    """Yield raw targets from ](target) occurrences in the body.

    A minimal scanner: it finds "](" then reads up to the matching ")". This
    avoids a regex dependency on balanced parentheses, which these docs do not
    use inside link targets.
    """
    targets = []
    for index in range(start_index, len(lines)):
        line = lines[index]
        pos = 0
        while True:
            marker = line.find("](", pos)
            if marker == -1:
                break
            close = line.find(")", marker + 2)
            if close == -1:
                break
            target = line[marker + 2:close]
            targets.append(target)
            pos = close + 1
    return targets


def body_start_index(lines):
    """Return the line index where the body begins (after front matter)."""
    if lines and lines[0].rstrip("\n") == "---":
        for index in range(1, len(lines)):
            if lines[index].rstrip("\n") == "---":
                return index + 1
    return 0


def target_exists(path):
    """A target exists if it resolves to a file or a directory on disk."""
    return os.path.exists(path)


def check_file(md_path, broken):
    """Validate one Markdown file, appending (md_path, kind, raw) to broken."""
    try:
        with open(md_path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError as error:
        broken.append((md_path, "read-error", str(error)))
        return

    file_dir = os.path.dirname(md_path)

    # Inline relative Markdown links, resolved document-relative.
    start = body_start_index(lines)
    for raw in extract_inline_links(lines, start):
        if is_skippable_target(raw):
            continue
        file_part = strip_anchor(raw).strip()
        if file_part == "":
            # Link was a pure anchor that we already skip above; guard anyway.
            continue
        if is_skippable_target(file_part):
            continue
        resolved = os.path.normpath(os.path.join(file_dir, file_part))
        if not target_exists(resolved):
            broken.append((md_path, "markdown-link", raw))

    # Front-matter related (document-relative) and source_documents
    # (repository-root-relative).
    related, source_documents = read_front_matter_lists(lines)

    for raw in related:
        if is_skippable_target(raw):
            continue
        file_part = strip_anchor(raw).strip()
        if is_skippable_target(file_part) or file_part == "":
            continue
        resolved = os.path.normpath(os.path.join(file_dir, file_part))
        if not target_exists(resolved):
            broken.append((md_path, "related", raw))

    for raw in source_documents:
        if is_skippable_target(raw):
            continue
        file_part = strip_anchor(raw).strip()
        if is_skippable_target(file_part) or file_part == "":
            continue
        resolved = os.path.normpath(os.path.join(REPO_ROOT, file_part))
        if not target_exists(resolved):
            broken.append((md_path, "source_documents", raw))


def gather_markdown_files():
    """Return a sorted list of *.md files under the scanned directories."""
    found = []
    for rel_dir in SCAN_DIRS:
        base = os.path.join(REPO_ROOT, rel_dir)
        if not os.path.isdir(base):
            continue
        for root, _dirs, files in os.walk(base):
            # Skip _templates/ directories: template files carry illustrative
            # example links and placeholder front matter, not real targets.
            _dirs[:] = [d for d in _dirs if d != "_templates"]
            for name in files:
                if name.endswith(".md"):
                    found.append(os.path.join(root, name))
    found.sort()
    return found


def main():
    md_files = gather_markdown_files()
    broken = []

    for md_path in md_files:
        check_file(md_path, broken)

    print("Link validation for The Unnecessary")
    print("Repository root: " + REPO_ROOT)
    print("Markdown files scanned: " + str(len(md_files)))
    print("")

    if not broken:
        print("Result: PASS. No broken link, related, or source_documents target found.")
        return 0

    print("Result: FAIL. Broken targets found: " + str(len(broken)))
    print("")
    for md_path, kind, raw in broken:
        rel = os.path.relpath(md_path, REPO_ROOT)
        print("  [" + kind + "] " + rel)
        print("      target: " + raw)
    return 1


if __name__ == "__main__":
    sys.exit(main())
