#!/usr/bin/env python3
"""Assemble the approved Book One manuscript into publishable EBOOK files.

Standard library only (plus the external `pandoc` toolchain, and `wkhtmltopdf`
for the best-effort PDF). No third-party Python imports, no pip installs. No side
effects on import: this module only defines constants and functions until a caller
invokes main().

This is a derive-only generator. It READS the approved chapter manuscripts under
docs/50-manuscript/book-1/<chapter>/<chapter>.md, extracts the STORY PROSE from
each (stripping the YAML front-matter and dropping everything from the first
appended editorial-log marker onward), and assembles one clean document. It then
shells out to pandoc to WRITE, into build/ebook/ (a build artifact directory, not
canon and never committed):

  the-unnecessary-book-1.md     the assembled clean-prose source (intermediate)
  the-unnecessary-book-1.epub   the EPUB (priority output)
  the-unnecessary-book-1.pdf    the PDF (best-effort; only if a no-LaTeX pdf
                                engine such as wkhtmltopdf/weasyprint is present)

The chapter set and order are data-driven: the book directory is globbed for
chapter-* folders and sorted, so adding chapter-04 needs no code change. The tool
never edits canon and never writes into docs/.
"""

import glob
import os
import re
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_DIR = os.path.join(REPO_ROOT, "docs", "50-manuscript", "book-1")
OUTPUT_DIR = os.path.join(REPO_ROOT, "build", "ebook")

BOOK_TITLE = "The Unnecessary"
BOOK_SUBTITLE = "Book One"
OUTPUT_STEM = "the-unnecessary-book-1"
# Stable identifier so a re-run does not churn the EPUB's unique id needlessly.
BOOK_IDENTIFIER = "urn:uuid:7a6f2c10-0000-4000-8000-theunnecessary1"

# A heading (## ...) or bold-only line (**...**) whose text matches one of these
# words marks the start of the appended editorial logs. Story prose carries no
# sub-headings -- only the single H1 chapter title -- so matching on these
# editorial words (rather than "any H2") avoids ever cutting real prose, while
# still catching every log marker seen in canon: "Adjudication Log", "Prose
# Revision Log", "Clarity-revision pass", "Canon-alignment pass", "Revision
# Notes", etc.
EDITORIAL_RE = re.compile(
    r"(adjudication|revision|canon-alignment|alignment\s+pass|editorial)",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
BOLD_LINE_RE = re.compile(r"^\*\*(.+?)\*\*\s*$")
THEMATIC_BREAK_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")

# Candidate no-LaTeX PDF engines, in order of preference. The first one found on
# PATH is used; if none is present the PDF step is skipped (EPUB is the priority).
PDF_ENGINES = ["wkhtmltopdf", "weasyprint", "prince", "pagedjs-cli"]


def find_tool(name):
    """Return a usable path to `name`, preferring scripts/bin/ then PATH."""
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", name)
    if os.path.isfile(local) and os.access(local, os.X_OK):
        return local
    return shutil.which(name)


def strip_frontmatter(text):
    """Drop a leading YAML front-matter block (between the top --- fences)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[i + 1:])
    # Unterminated fence: treat as no front-matter rather than discarding all.
    return text


def is_editorial_marker(line):
    """True if `line` is a heading or bold-only marker that opens editorial logs."""
    m = HEADING_RE.match(line)
    if m and len(m.group(1)) >= 2 and EDITORIAL_RE.search(m.group(2)):
        return True
    b = BOLD_LINE_RE.match(line)
    if b and EDITORIAL_RE.search(b.group(1)):
        return True
    return False


def extract_prose(text):
    """Return (h1_title_or_None, clean_prose_without_h1) for one chapter file.

    Strips the YAML front-matter, cuts everything from the first editorial-log
    marker onward, trims trailing scene-break rules / blank lines, and lifts out
    the H1 chapter title (so the caller can re-emit one normalized heading).
    """
    body = strip_frontmatter(text)
    lines = body.splitlines()

    # Cut at the first appended editorial-log marker.
    cut = len(lines)
    for i, line in enumerate(lines):
        if is_editorial_marker(line):
            cut = i
            break
    lines = lines[:cut]

    # Trim trailing blank lines and dangling scene-break rules (e.g. the `---`
    # that sat just before the Adjudication Log heading).
    while lines and (not lines[-1].strip() or THEMATIC_BREAK_RE.match(lines[-1])):
        lines.pop()

    # Lift out the first H1 (the chapter title); leave the rest of the prose.
    h1_title = None
    out = []
    for line in lines:
        m = HEADING_RE.match(line)
        if h1_title is None and m and len(m.group(1)) == 1:
            h1_title = m.group(2).strip()
            continue
        out.append(line)

    # Collapse leading blank lines left after removing the H1.
    while out and not out[0].strip():
        out.pop(0)

    return h1_title, "\n".join(out).strip()


def title_from_slug(slug):
    """'chapter-02-the-last-supported-day' -> 'Chapter 2: The Last Supported Day'."""
    parts = slug.split("-")
    if len(parts) >= 3 and parts[0] == "chapter" and parts[1].isdigit():
        number = int(parts[1])
        words = " ".join(w.capitalize() for w in parts[2:])
        return "Chapter {}: {}".format(number, words)
    # Unrecognized slug shape: title-case the whole thing rather than guess.
    return " ".join(w.capitalize() for w in slug.split("-"))


APPROVED_STATUSES = {"approved-canon", "approved"}


def chapter_status(md_path):
    """Return the manuscript's frontmatter `status:` value (lowercased), or '' if none."""
    with open(md_path, "r", encoding="utf-8") as fh:
        in_fm = False
        for i, line in enumerate(fh):
            s = line.strip()
            if i == 0 and s == "---":
                in_fm = True
                continue
            if in_fm:
                if s == "---":
                    break
                if s.lower().startswith("status:"):
                    return s.split(":", 1)[1].strip().strip('"').strip("'").lower()
    return ""


def discover_chapters(book_dir):
    """Glob chapter-* folders, sorted; publish ONLY approved chapters (drafts are skipped + logged)."""
    chapters = []
    for folder in sorted(glob.glob(os.path.join(book_dir, "chapter-*"))):
        if not os.path.isdir(folder):
            continue
        slug = os.path.basename(folder)
        md_path = os.path.join(folder, slug + ".md")
        if not os.path.isfile(md_path):
            sys.stderr.write(
                "WARN: no main manuscript for {} (expected {})\n".format(slug, md_path)
            )
            continue
        status = chapter_status(md_path)
        if status not in APPROVED_STATUSES:
            sys.stderr.write(
                "SKIP: {} status is '{}', not approved -- excluded from the published ebook\n".format(
                    slug, status or "none")
            )
            continue
        chapters.append((slug, md_path))
    return chapters


def assemble_markdown(chapters):
    """Build the combined clean-prose markdown (YAML metadata + title page + chapters)."""
    out = []
    out.append("---")
    out.append('title: "{}"'.format(BOOK_TITLE))
    out.append('subtitle: "{}"'.format(BOOK_SUBTITLE))
    out.append("lang: en-US")
    out.append('identifier: "{}"'.format(BOOK_IDENTIFIER))
    out.append("---")
    out.append("")

    for slug, md_path in chapters:
        with open(md_path, "r", encoding="utf-8") as fh:
            text = fh.read()
        h1_title, prose = extract_prose(text)
        display = h1_title if h1_title else title_from_slug(slug)
        out.append("# {}".format(display))
        out.append("")
        out.append(prose)
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def build_epub(pandoc, source_md, out_path):
    cmd = [
        pandoc, source_md,
        "--from", "markdown",
        "--to", "epub",
        "--toc", "--toc-depth=1",
        "--split-level=1",
        "-o", out_path,
    ]
    subprocess.run(cmd, check=True)


def build_pdf(pandoc, source_md, out_path):
    """Best-effort PDF via a no-LaTeX HTML engine. Returns (ok, engine_or_reason)."""
    engine = None
    for candidate in PDF_ENGINES:
        if find_tool(candidate):
            engine = candidate
            break
    if engine is None:
        return False, "no no-LaTeX pdf engine on PATH ({})".format(
            ", ".join(PDF_ENGINES)
        )
    cmd = [
        pandoc, source_md,
        "--from", "markdown",
        "--pdf-engine", engine,
        "--toc", "--toc-depth=1",
        "-o", out_path,
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        return False, "{} failed (exit {})".format(engine, exc.returncode)
    return True, engine


def main():
    pandoc = find_tool("pandoc")
    if not pandoc:
        sys.stderr.write(
            "ERROR: pandoc not found (scripts/bin/pandoc or on PATH). "
            "Install it before building the ebook.\n"
        )
        return 2

    chapters = discover_chapters(BOOK_DIR)
    if not chapters:
        sys.stderr.write("ERROR: no chapters found under {}\n".format(BOOK_DIR))
        return 2

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    source_md = os.path.join(OUTPUT_DIR, OUTPUT_STEM + ".md")
    epub_path = os.path.join(OUTPUT_DIR, OUTPUT_STEM + ".epub")
    pdf_path = os.path.join(OUTPUT_DIR, OUTPUT_STEM + ".pdf")

    combined = assemble_markdown(chapters)
    with open(source_md, "w", encoding="utf-8") as fh:
        fh.write(combined)

    print("Assembled {} chapter(s):".format(len(chapters)))
    for slug, _ in chapters:
        print("  - {}".format(slug))

    build_epub(pandoc, source_md, epub_path)
    print("EPUB: {} ({} bytes)".format(epub_path, os.path.getsize(epub_path)))

    ok, info = build_pdf(pandoc, source_md, pdf_path)
    if ok:
        print("PDF:  {} ({} bytes) via {}".format(
            pdf_path, os.path.getsize(pdf_path), info))
    else:
        print("PDF:  skipped -- {}".format(info))

    return 0


if __name__ == "__main__":
    sys.exit(main())
