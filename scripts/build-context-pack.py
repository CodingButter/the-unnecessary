#!/usr/bin/env python3
"""Build a single Markdown context pack from a task or chapter manifest.

This is the context-pack builder for the novel "The Unnecessary" (spec Phase 9).
It reads one manifest, resolves the ordered list of Markdown files it names,
verifies that every required file exists, then concatenates those files into a
single generated pack under the repository's .context/ directory. A clear source
heading is inserted before each file and original content is copied verbatim.

Design constraints (from the master spec, Phase 9):
  - Standard library only. No pip installs, no third-party imports.
  - Reliability over cleverness. A deliberately limited YAML reader handles this
    project's manifest schema only (top-level scalars and "key:" then "  - item"
    lists); it is not a general YAML parser.
  - Required-file gaps fail the build with a nonzero exit. Optional-file gaps
    warn on stderr and are skipped.
  - Files under archive/ are refused unless they are explicitly listed in the
    manifest AND the --allow-archive flag is passed.
  - Explicit, glob-free paths only. No wildcard expansion is performed.
  - Placeholders {chapter_number}, {chapter_slug}, {previous_chapter_number} are
    substituted from --set KEY=VALUE arguments or environment variables.
  - The header records generation time (from an env var or a fixed placeholder
    when no clock is available) and the manifest path.
  - A character count and an approximate token estimate (characters / 4) are
    printed without any third-party dependency.

Manifest schema keys (all optional for the reader; the loader chooses among
them): task_name, purpose, required_files, optional_files, exclude_files,
loading_order, expected_output, canon_rules, relevant_validation_checks.

The ordered file list is taken from loading_order when present, otherwise from
required_files followed by optional_files (deduplicated, order preserved).

Usage:
  python3 scripts/build-context-pack.py <manifest.yaml> [options]

Options:
  --out PATH            Write the pack to PATH instead of an auto-named file
                       under .context/.
  --allow-archive      Permit files under archive/ that are explicitly listed.
  --set KEY=VALUE      Provide a placeholder substitution (repeatable). Also
                       read from the environment when not given here.
  -h, --help           Show this help and exit.
"""

import os
import sys

# Approximate characters-per-token ratio for a rough, dependency-free estimate.
CHARS_PER_TOKEN = 4

# Recognized placeholder names. Values come from --set or the environment.
PLACEHOLDER_KEYS = ("chapter_number", "chapter_slug", "previous_chapter_number")

# Manifest keys whose values are lists of file paths.
LIST_KEYS = (
    "required_files",
    "optional_files",
    "exclude_files",
    "loading_order",
    "canon_rules",
    "relevant_validation_checks",
)

# Manifest keys whose values are single scalars.
SCALAR_KEYS = ("task_name", "purpose", "expected_output")


def repo_root():
    """Return the repository root (the parent of this script's scripts/ dir)."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def warn(message):
    """Print a warning to stderr without halting the build."""
    sys.stderr.write("WARNING: " + message + "\n")


def fail(message, code=1):
    """Print an error to stderr and exit with a nonzero status."""
    sys.stderr.write("ERROR: " + message + "\n")
    sys.exit(code)


def strip_inline_comment(value):
    """Remove a trailing unquoted inline comment from a scalar value.

    A '#' that is preceded by whitespace and not inside quotes starts a comment.
    """
    in_single = False
    in_double = False
    result = []
    prev = ""
    for ch in value:
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double and (prev == "" or prev.isspace()):
            break
        result.append(ch)
        prev = ch
    return "".join(result).strip()


def unquote(value):
    """Strip a single matching pair of surrounding quotes, if present."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def read_manifest(path):
    """Parse this project's manifest schema into a dict.

    Deliberately limited. Supports top-level scalar entries ("key: value") and
    top-level list entries ("key:" followed by indented "- item" lines). Blank
    lines and full-line comments (starting with '#') are ignored. Nested mappings
    and flow collections are not supported and are not used by this schema.
    """
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except OSError as exc:
        fail("cannot read manifest '" + path + "': " + str(exc))

    data = {}
    current_key = None
    for raw in lines:
        # Ignore blank lines and whole-line comments.
        stripped = raw.strip()
        if stripped == "" or stripped.startswith("#"):
            continue

        # A list item belongs to the most recently seen list key.
        if stripped.startswith("- "):
            if current_key is None:
                continue
            item = strip_inline_comment(stripped[2:].strip())
            item = unquote(item)
            if item:
                data.setdefault(current_key, []).append(item)
            continue

        # Otherwise this should be a top-level "key:" or "key: value" line.
        if ":" not in raw:
            continue
        key, _, rest = raw.partition(":")
        key = key.strip()
        rest = strip_inline_comment(rest.strip())
        if rest == "":
            # Key introduces a list (or an empty scalar). Remember it for items.
            current_key = key
            data.setdefault(key, [])
        else:
            data[key] = unquote(rest)
            current_key = None

    return data


def substitute_placeholders(text, mapping):
    """Replace {placeholder} tokens in a path using the provided mapping."""
    for key in PLACEHOLDER_KEYS:
        token = "{" + key + "}"
        if token in text and key in mapping:
            text = text.replace(token, mapping[key])
    return text


def collect_placeholder_values(set_args):
    """Build the placeholder map from --set arguments, then the environment."""
    mapping = {}
    for key in PLACEHOLDER_KEYS:
        env_value = os.environ.get(key)
        if env_value is not None:
            mapping[key] = env_value
    for pair in set_args:
        if "=" not in pair:
            fail("--set expects KEY=VALUE, got '" + pair + "'")
        key, _, value = pair.partition("=")
        key = key.strip()
        if key not in PLACEHOLDER_KEYS:
            warn("ignoring unknown placeholder key '" + key + "'")
            continue
        mapping[key] = value
    return mapping


def ordered_file_list(manifest):
    """Return the ordered list of paths to load.

    Prefer loading_order. Fall back to required_files then optional_files,
    preserving order and removing duplicates.
    """
    if manifest.get("loading_order"):
        source = list(manifest["loading_order"])
    else:
        source = list(manifest.get("required_files", [])) + list(
            manifest.get("optional_files", [])
        )
    seen = set()
    ordered = []
    for item in source:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def is_archive_path(rel_path):
    """Return True when a path points under an archive/ directory."""
    norm = rel_path.replace("\\", "/").lstrip("./")
    return norm == "archive" or norm.startswith("archive/")


def generation_time():
    """Return a generation timestamp string.

    Read from CONTEXT_PACK_TIME or SOURCE_DATE_EPOCH-style overrides when set so
    builds can be made deterministic. Otherwise use the system clock. If the
    clock is unavailable for any reason, fall back to a fixed placeholder.
    """
    override = os.environ.get("CONTEXT_PACK_TIME")
    if override:
        return override
    try:
        import datetime

        return datetime.datetime.now().isoformat(timespec="seconds")
    except Exception:
        return "unknown-time"


def build_pack(manifest_path, out_path, allow_archive, placeholder_map):
    """Resolve, read, and concatenate manifest files into one pack string."""
    root = repo_root()
    manifest = read_manifest(manifest_path)

    required = [
        substitute_placeholders(p, placeholder_map)
        for p in manifest.get("required_files", [])
    ]
    optional = [
        substitute_placeholders(p, placeholder_map)
        for p in manifest.get("optional_files", [])
    ]
    required_set = set(required)
    optional_set = set(optional)

    ordered = [substitute_placeholders(p, placeholder_map) for p in ordered_file_list(manifest)]

    # If loading_order was empty we already built ordered from required+optional.
    # If loading_order names a path not classified as required/optional, treat it
    # as required for existence purposes only when it is not in optional_set.
    explicit_listing = set(required) | set(optional)

    # First pass: existence and archive policy checks before reading anything.
    missing_required = []
    for rel in ordered:
        is_required = rel in required_set or (rel not in optional_set and rel in explicit_listing)
        # Paths that appear only in loading_order without being optional default
        # to required, matching "verify every required path exists".
        if rel not in optional_set:
            is_required = True

        if is_archive_path(rel):
            if not (allow_archive and rel in explicit_listing):
                fail(
                    "refusing archive path '" + rel + "'. List it explicitly in the "
                    "manifest and pass --allow-archive to include it."
                )

        abs_path = os.path.join(root, rel)
        if not os.path.isfile(abs_path):
            if rel in optional_set and rel not in required_set:
                warn("optional file missing, skipping: " + rel)
            elif is_required:
                missing_required.append(rel)

    # Optional files declared in the manifest but absent from the load order are
    # still checked so a missing optional always warns, per "warn about missing
    # optional files". These are never added to the pack body (only ordered
    # paths are concatenated); the warning is the deliverable.
    ordered_set = set(ordered)
    for rel in optional:
        if rel in ordered_set or rel in required_set:
            continue
        if is_archive_path(rel):
            # An archive optional outside the load order is simply not included
            # and not warned about; archive inclusion is governed above.
            continue
        if not os.path.isfile(os.path.join(root, rel)):
            warn("optional file missing, skipping: " + rel)

    if missing_required:
        for rel in missing_required:
            sys.stderr.write("ERROR: required file missing: " + rel + "\n")
        fail(
            "build aborted: " + str(len(missing_required)) + " required file(s) missing",
            code=2,
        )

    # Second pass: assemble the pack. Optional missing files are skipped quietly
    # here since they were already warned about above.
    task_name = manifest.get("task_name", "(unnamed task)")
    purpose = manifest.get("purpose", "")
    gen_time = generation_time()

    header_lines = [
        "<!--",
        "  GENERATED CONTEXT PACK. Do not edit by hand.",
        "  This file is a disposable concatenation produced by",
        "  scripts/build-context-pack.py and is git-ignored under .context/.",
        "-->",
        "",
        "# Context Pack: " + str(task_name),
        "",
        "- manifest: " + manifest_path,
        "- generated: " + gen_time,
    ]
    if purpose:
        header_lines.append("- purpose: " + str(purpose))
    header_lines.append("")
    header_lines.append("---")
    header_lines.append("")

    body_parts = []
    included = []
    for rel in ordered:
        abs_path = os.path.join(root, rel)
        if not os.path.isfile(abs_path):
            # Already handled (optional missing); skip silently in assembly.
            continue
        try:
            with open(abs_path, "r", encoding="utf-8") as handle:
                content = handle.read()
        except OSError as exc:
            fail("cannot read listed file '" + rel + "': " + str(exc))
        body_parts.append("# ===== SOURCE: " + rel + " =====")
        body_parts.append("")
        body_parts.append(content)
        # Guarantee separation between files without altering original content.
        if not content.endswith("\n"):
            body_parts.append("")
        body_parts.append("")
        included.append(rel)

    pack_text = "\n".join(header_lines) + "\n".join(body_parts)
    return pack_text, included, task_name


def default_out_path(manifest_path):
    """Derive a default output path under .context/ from the manifest name."""
    root = repo_root()
    context_dir = os.path.join(root, ".context")
    base = os.path.basename(manifest_path)
    stem = base
    for ext in (".yaml", ".yml", ".json"):
        if stem.endswith(ext):
            stem = stem[: -len(ext)]
            break
    if stem in ("context-manifest", ""):
        # Disambiguate using the parent directory name when the manifest is the
        # generic per-chapter "context-manifest.yaml".
        parent = os.path.basename(os.path.dirname(os.path.abspath(manifest_path)))
        if parent:
            stem = parent
    return os.path.join(context_dir, stem + ".pack.md")


def parse_args(argv):
    """A small, dependency-free argument parser for this script's options."""
    manifest_path = None
    out_path = None
    allow_archive = False
    set_args = []

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("-h", "--help"):
            sys.stdout.write(__doc__ + "\n")
            sys.exit(0)
        elif arg == "--allow-archive":
            allow_archive = True
        elif arg == "--out":
            i += 1
            if i >= len(argv):
                fail("--out requires a path")
            out_path = argv[i]
        elif arg.startswith("--out="):
            out_path = arg[len("--out="):]
        elif arg == "--set":
            i += 1
            if i >= len(argv):
                fail("--set requires KEY=VALUE")
            set_args.append(argv[i])
        elif arg.startswith("--set="):
            set_args.append(arg[len("--set="):])
        elif arg.startswith("-"):
            fail("unknown option '" + arg + "'")
        else:
            if manifest_path is None:
                manifest_path = arg
            else:
                fail("unexpected extra argument '" + arg + "'")
        i += 1

    if manifest_path is None:
        fail("usage: build-context-pack.py <manifest.yaml> [--out PATH] "
             "[--allow-archive] [--set KEY=VALUE]")
    return manifest_path, out_path, allow_archive, set_args


def main(argv):
    manifest_path, out_path, allow_archive, set_args = parse_args(argv)

    if not os.path.isfile(manifest_path):
        fail("manifest not found: " + manifest_path)

    placeholder_map = collect_placeholder_values(set_args)

    pack_text, included, task_name = build_pack(
        manifest_path, out_path, allow_archive, placeholder_map
    )

    if out_path is None:
        out_path = default_out_path(manifest_path)

    out_dir = os.path.dirname(os.path.abspath(out_path))
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        fail("cannot create output directory '" + out_dir + "': " + str(exc))

    try:
        with open(out_path, "w", encoding="utf-8") as handle:
            handle.write(pack_text)
    except OSError as exc:
        fail("cannot write pack '" + out_path + "': " + str(exc))

    char_count = len(pack_text)
    token_estimate = char_count // CHARS_PER_TOKEN

    sys.stdout.write("Built context pack for task: " + str(task_name) + "\n")
    sys.stdout.write("  manifest: " + manifest_path + "\n")
    sys.stdout.write("  output:   " + out_path + "\n")
    sys.stdout.write("  files included: " + str(len(included)) + "\n")
    for rel in included:
        sys.stdout.write("    - " + rel + "\n")
    sys.stdout.write("  characters: " + str(char_count) + "\n")
    sys.stdout.write(
        "  approx tokens (chars/" + str(CHARS_PER_TOKEN) + "): "
        + str(token_estimate) + "\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
