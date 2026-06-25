#!/usr/bin/env python3
"""Detect a stale context pack for The Unnecessary.

A context pack under .context/ is a frozen concatenation of source files named
by a manifest. If any of those sources changes after the pack is built, the
pack is STALE and must not be consumed (drafting, critique, validation), or a
reader will reason from out-of-date canon. This script catches that.

It compares the pack file's modification time against the modification time of
every source file the manifest lists (required, optional, and loading-order).
Any source newer than the pack means the pack is stale.

Standard library only.

Usage:
  python3 scripts/check-pack-fresh.py <manifest.yaml> <pack.md>

Exit code:
  0  pack is fresh (or any missing-but-optional sources are ignored)
  1  pack is stale (lists which sources changed) or the pack does not exist
"""

import os
import sys

KEYS = ("required_files", "optional_files", "loading_order")


def manifest_source_paths(manifest_path):
    """Return the concrete source paths a manifest lists under the file keys."""
    paths = []
    current = None
    try:
        with open(manifest_path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError as err:
        print("ERROR: cannot read manifest: " + str(err), file=sys.stderr)
        return None
    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()
        # A top-level key (no leading whitespace) ending in ':'
        if line[:1] and not line[:1].isspace() and stripped.endswith(":"):
            key = stripped[:-1].strip()
            current = key if key in KEYS else None
            continue
        if current and stripped.startswith("- "):
            value = stripped[2:].strip()
            # Drop surrounding quotes.
            if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
                value = value[1:-1]
            # Drop trailing "  (annotation)" notes some manifests use.
            value = value.split("  ")[0].strip()
            # Skip placeholders, globs, prose, and archive paths.
            if (not value or "<" in value or "*" in value or value.startswith("archive/")
                    or " " in value or "/" not in value):
                continue
            paths.append(value)
    # De-duplicate, preserve order.
    seen = set()
    out = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def main():
    if len(sys.argv) != 3:
        print("usage: check-pack-fresh.py <manifest.yaml> <pack.md>", file=sys.stderr)
        return 1
    manifest_path, pack_path = sys.argv[1], sys.argv[2]

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if not os.path.exists(pack_path):
        print("STALE: pack does not exist: " + pack_path)
        print("Rebuild it: python3 scripts/build-context-pack.py " + manifest_path)
        return 1

    pack_mtime = os.path.getmtime(pack_path)
    sources = manifest_source_paths(manifest_path)
    if sources is None:
        return 1

    stale = []
    for rel in sources:
        abs_path = rel if os.path.isabs(rel) else os.path.join(repo_root, rel)
        if not os.path.exists(abs_path):
            # Missing source is the link validator's concern, not staleness.
            continue
        if os.path.getmtime(abs_path) > pack_mtime:
            stale.append(rel)

    print("Pack freshness check")
    print("  manifest: " + manifest_path)
    print("  pack:     " + pack_path)
    print("  sources checked: " + str(len(sources)))
    if not stale:
        print("Result: FRESH. No source is newer than the pack.")
        return 0
    print("Result: STALE. " + str(len(stale)) + " source(s) changed after the pack was built:")
    for rel in stale:
        print("  - " + rel)
    print("Rebuild it: python3 scripts/build-context-pack.py " + manifest_path)
    return 1


if __name__ == "__main__":
    sys.exit(main())
