#!/usr/bin/env python3
"""Generate a character portrait from a profile and embed it, for The Unnecessary.

A "party trick" derived-artifact tool. The portrait is a downstream RENDER of the
canon profile, the way the chapter audio is a render of the manuscript: fully
automatic, no human approval, regenerate any time. The profile is the source of
truth; this JPEG is a disposable output and can always be rebuilt from the file.

Reveal-safety is the load-bearing rule. The portrait is a page-visible artifact,
so it is built ONLY from page-usable appearance facts: facts tagged `[open]` or
untagged (which the profile spec treats as open). Any fact carrying a
`[reveal: ...]` or `[behavior-only]` tag is dropped, never drawn. A portrait must
never leak a future reveal.

Standard library only. The API key is read from GEMINI_API_KEY or GOOGLE_API_KEY
in the environment, falling back to the same names in the repo-root .env file,
exactly as scripts/gemini-critique.py does. The key is never printed.

Usage:
  python3 scripts/portrait-from-profile.py docs/20-canon/characters/profiles/vega-marisol.md
  python3 scripts/portrait-from-profile.py --all
  python3 scripts/portrait-from-profile.py <profile.md> [--model gemini-2.5-flash-image]
"""

import argparse
import base64
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

API_HOST = "https://generativelanguage.googleapis.com"
DEFAULT_MODEL = "gemini-2.5-flash-image"
DEFAULT_WIDTH = 500

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PROFILES_DIR = os.path.join(REPO_ROOT, "docs", "20-canon", "characters", "profiles")
PORTRAITS_DIR = os.path.join(REPO_ROOT, "docs", "20-canon", "characters", "portraits")

# The shared father/mother graph parser lives alongside this script. It is the
# single reader of the structured `## Relationships` edges, and it already
# distinguishes blood parents (father/mother) from spouses and other authority
# edges. We reuse it to topologically order generation and to find the parent
# portraits that condition each child.
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
import characters_graph as cg  # noqa: E402  (path set above; stdlib-only module)

# Profiles with no human physical layer (nonhuman intelligences) and index files
# are skipped under --all, per profile-spec.md Section 2.
SKIP_PROFILES = {"index.md", "morrow.md", "crown.md"}

# Shared house style for every portrait. Grounded near-future, documentary, worn,
# never glossy or cyberpunk-cliche. This is the constant; the character-specific
# appearance is appended below it.
STYLE_PREAMBLE = (
    "A photographic character portrait for a grounded near-future novel set in "
    "Greater Detroit in 2053. Documentary, realistic, restrained: shot like an "
    "honest editorial photograph of a real person, natural available light, "
    "slightly muted color, fine skin texture and real wear. The world has "
    "withdrawn unevenly rather than collapsed, so the look is worn-practical and "
    "lived-in, not futuristic. A single subject, head-and-shoulders to waist-up, "
    "looking toward the camera, against a plain neutral out-of-focus background. "
    "Absolutely NOT glossy, NOT a glamour shot, NOT 3D render, NOT illustration, "
    "NOT cyberpunk: no neon, no glowing implants, no holograms, no chrome, no rain-"
    "slicked city. No text, captions, watermarks, logos, or borders in the image. "
    "Render the subject's ethnicity accurately and recognizably, as a specific real "
    "person -- never a stereotype or caricature. "
    "Render the following specific person:"
)

# Tags that gate a fact as not-yet-page-visible. A sentence carrying any of these
# is dropped wholesale, never just stripped of its tag.
REVEAL_DROP_RE = re.compile(r"\[reveal:|\[behavior-only\]", re.IGNORECASE)

# Inline tags to strip from kept text: [open], [open, behaviorized], (proposed), etc.
TAG_STRIP_RE = re.compile(r"\[(?:open|behaviorized|[^\]]*)\]")
# Meta parentheticals (editorial asides about canon, not description) to remove.
META_PAREN_RE = re.compile(
    r"\((?:[^()]*?(?:proposed|canon|Section\s|consistent|ties to|echoes|per\s|"
    r"established|no profile|awaiting|veto|world-consistent|reading of|invented|"
    r"spine|the chapter|Chapter\s|grounds|grounded|except the)[^()]*)\)",
    re.IGNORECASE,
)
# Inline code spans in these profiles are always repo-relative path references.
CODE_SPAN_RE = re.compile(r"`[^`]*`")
# The dedicated **Heritage:** field inside the Coloring sub-block. It is pulled
# out and rendered explicitly so Gemini draws the stated ethnic/national
# ancestry, instead of inferring it from complexion plus surname. Reveal-safe:
# a heritage line carrying a reveal/behavior-only tag is dropped like any fact.
HERITAGE_LINE_RE = re.compile(r"^\*\*Heritage:\*\*\s*(.+?)\s*$", re.IGNORECASE)


def prefer_ipv4():
    """Make urllib try IPv4 before IPv6. The Gemini host advertises IPv6, but in
    many containers and sandboxes IPv6 is blackholed, and urllib (unlike curl,
    which uses Happy Eyeballs) tries the advertised IPv6 addresses first and
    stalls for minutes on connect before falling back. Sorting IPv4 first makes
    requests return in seconds; harmless where IPv6 works, since IPv4 still does."""
    original = socket.getaddrinfo

    def ipv4_first(host, port, family=0, *args, **kwargs):
        results = original(host, port, family, *args, **kwargs)
        return sorted(results, key=lambda r: 0 if r[0] == socket.AF_INET else 1)

    socket.getaddrinfo = ipv4_first


def load_key():
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        val = os.environ.get(name)
        if val:
            return val.strip()
    env_path = os.path.join(REPO_ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
                    if line.startswith(name + "="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def read_file(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def section_body(text, header):
    """Return the body of a `## <header>` section, up to the next `## ` header."""
    pattern = re.compile(r"^##\s+" + re.escape(header) + r"\s*$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        return None
    start = m.end()
    nxt = re.search(r"^##\s+", text[start:], re.MULTILINE)
    return text[start:start + nxt.start()] if nxt else text[start:]


def clean_fact(sentence):
    """Strip reveal/visibility tags, meta parentheticals, and path refs from a
    kept sentence, then tidy whitespace. The reveal/behavior-only DROP decision
    happens before this; here we only cosmetically clean page-safe text."""
    s = TAG_STRIP_RE.sub("", sentence)
    s = META_PAREN_RE.sub("", s)
    s = CODE_SPAN_RE.sub("", s)
    # A stripped citation leaves a dangling "per" (e.g. "registered, per `path`." ->
    # "registered, per."). Drop the orphaned connective.
    s = re.sub(r",?\s*\bper\b\s*(?=[.,;]|$)", "", s)
    s = re.sub(r"\([^()]*\)", lambda mo: mo.group(0) if len(mo.group(0)) < 40 else "", s)
    s = re.sub(r"\s+([.,;:])", r"\1", s)      # space before punctuation
    s = re.sub(r"\(\s*\)", "", s)             # empty parens
    s = re.sub(r"\s{2,}", " ", s).strip()
    s = re.sub(r"[,;]\s*$", ".", s).strip()
    return s


def extract_appearance(text):
    """Build the reveal-safe appearance description from Physical and Identifiers.

    Walks the sub-blocks, drops any sentence carrying a reveal: or behavior-only
    tag, cleans the rest, and returns labeled lines, the dedicated Heritage value
    (or None), plus a count of reveal-gated facts that were filtered (for
    reporting)."""
    body = section_body(text, "Physical and Identifiers")
    if body is None:
        return None, None, 0
    blocks = []          # (label, cleaned prose)
    heritage = None      # the dedicated **Heritage:** field, rendered explicitly
    state = {"label": None, "buf": [], "dropped": 0}

    def flush():
        label = state["label"]
        if label is None:
            return
        paragraph = " ".join(state["buf"]).strip()
        if not paragraph:
            return
        kept = []
        for sent in re.split(r"(?<=[.!?])\s+", paragraph):
            if not sent.strip():
                continue
            if REVEAL_DROP_RE.search(sent):
                state["dropped"] += 1   # reveal-gated fact, never drawn
                continue
            cleaned = clean_fact(sent)
            if cleaned and cleaned != ".":
                kept.append(cleaned)
        if kept:
            blocks.append((label, " ".join(kept)))

    for line in body.splitlines():
        sub = re.match(r"^###\s+(.+?)\s*$", line)
        if sub:
            flush()
            state["label"] = sub.group(1).strip()
            state["buf"] = []
            continue
        herit = HERITAGE_LINE_RE.match(line.strip())
        if herit:
            # Pull the Heritage field out of the Coloring prose and render it on
            # its own labeled line. Drop it if reveal/behavior-gated; otherwise
            # clean it the same way as any kept page-safe fact.
            raw = herit.group(1).strip()
            if REVEAL_DROP_RE.search(raw):
                state["dropped"] += 1
            else:
                cleaned = clean_fact(raw)
                if cleaned and cleaned != ".":
                    heritage = cleaned
            continue
        if line.strip():
            state["buf"].append(line.strip())
    flush()
    return blocks, heritage, state["dropped"]


def field_value(text, label):
    """Return the inline `**Label:** value` from Basic Information, cleaned, or None."""
    m = re.search(r"^\*\*" + re.escape(label) + r":\*\*\s*(.+?)\s*$", text, re.MULTILINE)
    if not m:
        return None
    val = clean_fact(re.split(r"(?<=[.!?])\s+", m.group(1))[0])
    return val or None


def display_name(text):
    m = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    return m.group(1).strip() if m else "Unknown"


def age_value(text):
    """Pull the integer age from the 'Age at the start of Book One:' field.

    The label is variable ('Age', 'Age at the start of Book One'), so match the
    'Age...:' prefix and read the first number. Returns a string or None."""
    m = re.search(r"^\*\*Age[^:*]*:\*\*\s*(.+)$", text, re.MULTILINE)
    if not m:
        return None
    num = re.search(r"\d+", m.group(1))
    return num.group(0) if num else None


def build_prompt(text):
    """Assemble the full image prompt, or return (None, reason) if no Physical
    section exists (e.g. a nonhuman profile).

    The subject description LEADS with the character's heritage as the first,
    hardest-weighted descriptor, because the front of an image prompt dominates
    what the model renders. Putting the stated ethnic and national ancestry first
    (rather than in a trailing field) makes the correct race come out reliably,
    instead of being inferred from complexion plus surname."""
    blocks, heritage, dropped = extract_appearance(text)
    if blocks is None:
        return None, "no 'Physical and Identifiers' section (nonhuman or non-profile)", dropped
    name = display_name(text)
    occupation = field_value(text, "Occupation")
    faction = field_value(text, "Faction or class")
    age = age_value(text)
    descriptor = []
    if age:
        descriptor.append("a " + age + "-year-old")
    if occupation:
        descriptor.append(occupation.rstrip("."))
    if faction:
        descriptor.append("social class " + faction.rstrip("."))
    detail = ", ".join(descriptor)
    if heritage:
        subject = ("Subject -- heritage first, render this ethnicity accurately and "
                   "recognizably: " + heritage.rstrip(".") + ". This specific person is "
                   + name + ((", " + detail) if detail else "") + ".")
    else:
        subject = "Subject: " + name + ((", " + detail) if detail else "") + "."
    appearance_lines = [subject]
    for label, prose in blocks:
        appearance_lines.append(label + ": " + prose)
    prompt = STYLE_PREAMBLE + "\n\n" + "\n".join(appearance_lines)
    return prompt, None, dropped


def family_instruction(n, age=None):
    """The conditioning sentence appended when parent reference portraits are
    attached. The references exist ONLY to transfer inherited facial genetics;
    age, pose, wardrobe, framing, and setting must come from the subject's own
    description and never be copied from the parent photo. Without this hard
    guard the model reproduces the parent image almost verbatim, aged and posed
    identically."""
    noun = "parent" if n == 1 else "parents"
    img = "image" if n == 1 else "images"
    is_are = "is a portrait" if n == 1 else "are portraits"
    age_clause = ""
    if age:
        age_clause = (
            " AGE IS CRITICAL: render this subject as a " + age + "-year-old at "
            "their own life stage. The " + noun + " in the reference " + img + " may "
            "look decades older; do NOT age this subject up toward them -- younger "
            "skin, less or no gray, fewer lines, a younger build."
        )
    return (
        "FAMILY RESEMBLANCE, FACE ONLY: the additional reference " + img + " " + is_are
        + " of this subject's biological " + noun + ", attached for ONE purpose: to "
        "carry inherited facial genetics -- bone structure, skin tone, eye and hair "
        "colour, and a few family features. Use the reference " + img + " for the face "
        "ONLY. Do NOT copy the " + noun + "'s pose, camera angle, crop, expression, "
        "clothing, or background; this subject has their own distinct pose, expression, "
        "wardrobe, and setting from the description above. The result must read as a "
        "completely separate photograph of a different, younger individual who merely "
        "resembles the " + noun + " -- not the same person and not the same shot."
        + age_clause
    )


def call_gemini_image(model, key, prompt, reference_images=None):
    """POST to <model>:generateContent asking for an image; return (png_bytes, err).

    Uses the documented image-generation surface: generationConfig.responseModalities
    requesting IMAGE, with the bytes returned base64 in candidates[].content.parts[]
    .inlineData.data. Matches the auth pattern of scripts/gemini-critique.py.

    reference_images is an optional list of (mime_type, raw_bytes) inputs. gemini-
    2.5-flash-image accepts multiple images in one request, so the parent
    portrait(s) are attached here as additional inlineData parts alongside the
    text prompt, which lets a child portrait inherit a family resemblance."""
    url = API_HOST + "/v1beta/models/" + model + ":generateContent?key=" + key
    parts = [{"text": prompt}]
    for mime, raw in (reference_images or []):
        parts.append({"inlineData": {
            "mimeType": mime,
            "data": base64.b64encode(raw).decode("ascii"),
        }})
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        try:
            msg = json.loads(detail).get("error", {}).get("message", detail)
        except Exception:  # noqa: BLE001
            msg = detail
        return None, "HTTP " + str(err.code) + ": " + msg[:500]
    except Exception as err:  # noqa: BLE001
        return None, str(err)[:500]
    cands = body.get("candidates")
    if not cands:
        return None, "no candidates: " + json.dumps(body)[:400]
    parts = cands[0].get("content", {}).get("parts", [])
    for part in parts:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            try:
                return base64.b64decode(inline["data"]), None
            except Exception as err:  # noqa: BLE001
                return None, "bad base64: " + str(err)[:200]
    reason = cands[0].get("finishReason")
    note = "".join(p.get("text", "") for p in parts)[:300]
    return None, "no image in response (finishReason=" + str(reason) + ") " + note


def resize_to_jpeg(png_bytes, out_path, width):
    """Downscale raw PNG bytes (the model's output) to <width> px wide (aspect
    preserved) and re-encode as JPEG at quality ~82 in a single ffmpeg pass,
    writing the result to out_path. ffmpeg is already a repo dependency, so no
    Pillow/PIL is pulled in. scale=<width>:-2 keeps the height even and the
    aspect ratio intact; -q:v 4 is ffmpeg's JPEG quality knob (~82, lower is
    better, 2-31 range). JPEG keeps the repo lean as the image set grows.
    Returns (ok, err)."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(png_bytes)
        tmp_path = tmp.name
    try:
        proc = subprocess.run(
            ["ffmpeg", "-y", "-i", tmp_path,
             "-vf", "scale=" + str(width) + ":-2", "-q:v", "4", out_path],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        if proc.returncode != 0:
            return False, proc.stderr.decode("utf-8", "replace")[-400:]
        return True, None
    except Exception as err:  # noqa: BLE001
        return False, str(err)[:400]
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


def embed_in_profile(profile_path, slug, name):
    """Insert the portrait image under the Physical heading. Idempotent: if a
    line already references ../portraits/<slug>.jpg, leave the file untouched."""
    text = read_file(profile_path)
    rel = "../portraits/" + slug + ".jpg"
    if rel in text:
        return "already embedded"
    embed = "![Portrait of " + name + "](" + rel + ")"
    pattern = re.compile(r"^(##\s+Physical[^\n]*)$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        return "no Physical heading to embed under"
    insert_at = m.end()
    new_text = text[:insert_at] + "\n\n" + embed + text[insert_at:]
    with open(profile_path, "w", encoding="utf-8") as handle:
        handle.write(new_text)
    return "embedded"


def parent_references(parent_ids):
    """Resolve blood-parent character ids to existing portrait JPEGs.

    Returns (refs, attached, missing): refs is a list of (mime, bytes) ready for
    the image call, attached/missing are the parent ids whose portrait did / did
    not exist on disk. Only father/mother ids should be passed here; spouses are
    never references."""
    refs, attached, missing = [], [], []
    for pid in (parent_ids or []):
        p_path = os.path.join(PORTRAITS_DIR, pid + ".jpg")
        try:
            with open(p_path, "rb") as handle:
                refs.append(("image/jpeg", handle.read()))
            attached.append(pid)
        except OSError:
            missing.append(pid)
    return refs, attached, missing


def generate_for(profile_path, model, key, width=DEFAULT_WIDTH,
                 parent_ids=None, force=False):
    """Render one profile. Returns (ok, message).

    When the character has profiled blood parent(s) whose portrait already
    exists, those JPEGs are attached as reference images so the face inherits a
    family resemblance. An existing portrait is kept unless force is set."""
    text = read_file(profile_path)
    name = display_name(text)
    slug = os.path.splitext(os.path.basename(profile_path))[0]
    out_path = os.path.join(PORTRAITS_DIR, slug + ".jpg")
    if os.path.exists(out_path) and not force:
        return True, "EXISTS " + slug + ": kept " + out_path + " (use --force to regenerate)"
    prompt, reason, dropped = build_prompt(text)
    if prompt is None:
        return False, "skip " + os.path.basename(profile_path) + ": " + reason
    refs, attached, missing = parent_references(parent_ids)
    if refs:
        prompt = prompt + "\n\n" + family_instruction(len(refs), age_value(text))
    print("Generating portrait for " + name + " [" + slug + "] via " + model
          + " (dropped " + str(dropped) + " reveal/behavior-gated facts; key hidden)...",
          file=sys.stderr)
    if attached:
        print("  family conditioning: attaching " + str(len(attached))
              + " parent reference image(s): "
              + ", ".join(a + ".jpg" for a in attached), file=sys.stderr)
    if missing:
        print("  family conditioning: " + str(len(missing))
              + " profiled parent(s) had no portrait yet, generating without: "
              + ", ".join(m + ".jpg" for m in missing), file=sys.stderr)
    if not (parent_ids or []):
        print("  family conditioning: no profiled blood parents; prompt only (root).",
              file=sys.stderr)
    png, err = call_gemini_image(model, key, prompt, refs)
    if err:
        return False, "FAILED " + slug + ": " + err
    os.makedirs(PORTRAITS_DIR, exist_ok=True)
    # Downscale to ~<width>px wide and re-encode as JPEG before saving +
    # embedding: the portrait is a repo artifact, so the full-res PNG model
    # output is needless weight, and JPEG keeps the growing image set lean.
    ok, resize_err = resize_to_jpeg(png, out_path, width)
    if not ok:
        return False, "FAILED " + slug + ": resize: " + resize_err
    sized = os.path.getsize(out_path)
    status = embed_in_profile(profile_path, slug, name)
    ref_note = (" [conditioned on " + ", ".join(attached) + "]") if attached else ""
    return True, "OK " + slug + ": wrote " + out_path + " (" + str(len(png)) \
        + " bytes src -> " + str(sized) + " bytes @ " + str(width) + "px), embed " \
        + status + ref_note


def topo_order(slugs, parents_map):
    """Order slugs so every profiled blood parent precedes its child.

    Roots (no profiled blood parent within the selected set) come first in stable
    sorted order; a child is emitted only once all its in-set parents are placed.
    Parents outside the selected set do not gate ordering -- their portraits are
    expected to already exist on disk. Any residual cycle is appended in stable
    order rather than dropped, so generation never stalls."""
    sel = set(slugs)
    placed = set()
    ordered = []
    pending = list(slugs)
    while pending:
        progressed = False
        still = []
        for slug in pending:
            in_set_parents = [p for p in parents_map.get(slug, []) if p in sel]
            if all(p in placed for p in in_set_parents):
                ordered.append(slug)
                placed.add(slug)
                progressed = True
            else:
                still.append(slug)
        if not progressed:
            ordered.extend(still)
            break
        pending = still
    return ordered


def main():
    ap = argparse.ArgumentParser(description="Generate and embed a character portrait from a profile.")
    ap.add_argument("profile", nargs="*",
                    help="Path(s) to character profile .md; rendered in topological "
                         "(parents-before-children) order")
    ap.add_argument("--all", action="store_true", help="Walk every profile in profiles/")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="Gemini image model id")
    ap.add_argument("--width", type=int, default=DEFAULT_WIDTH,
                    help="Max portrait width in px; aspect preserved (default %(default)s)")
    ap.add_argument("--force", action="store_true",
                    help="Regenerate even if the portrait JPEG already exists")
    args = ap.parse_args()

    if not args.all and not args.profile:
        ap.error("give one or more profile paths or --all")

    prefer_ipv4()
    key = load_key()
    if not key:
        print("ERROR: no GEMINI_API_KEY or GOOGLE_API_KEY in env or .env", file=sys.stderr)
        return 2

    # Build the family graph once. parents_map maps a child slug to its profiled
    # blood-parent slugs (father/mother only; spouses and other authority edges
    # are excluded by graph.parents_of). It drives both the topological ordering
    # and which parent portraits condition each child.
    graph = cg.build_graph()
    parents_map = {child: [pid for (pid, _rel) in plist]
                   for child, plist in graph.parents_of().items()}

    if args.all:
        slugs = [os.path.splitext(f)[0]
                 for f in sorted(os.listdir(PROFILES_DIR))
                 if f.endswith(".md") and f not in SKIP_PROFILES]
        path_for = {s: os.path.join(PROFILES_DIR, s + ".md") for s in slugs}
    else:
        slugs, path_for = [], {}
        for p in args.profile:
            s = os.path.splitext(os.path.basename(p))[0]
            slugs.append(s)
            path_for[s] = p

    ordered = topo_order(slugs, parents_map)

    failures = 0
    for slug in ordered:
        path = path_for.get(slug, os.path.join(PROFILES_DIR, slug + ".md"))
        if not os.path.exists(path):
            print("FAILED: profile not found: " + path, file=sys.stderr)
            failures += 1
            continue
        parent_ids = list(parents_map.get(slug, []))
        ok, message = generate_for(path, args.model, key, args.width, parent_ids, args.force)
        print(message, file=sys.stderr)
        if not ok and not message.startswith("skip "):
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
