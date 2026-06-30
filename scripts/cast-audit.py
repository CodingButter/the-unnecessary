#!/usr/bin/env python3
"""Acoustic ensemble-audit + voice-selection tool for the LIVE / dramatized audiobook.

Standard library only (numpy is used IF importable, else a pure-Python cosine). NO side
effects on import: this module only defines constants and functions; nothing walks the
disk, reads a file, hits the network, or prints until main() is called under __main__.

WHAT IT DOES
  1. Reads the cast roster (docs/10-vision/audio/cast-sheet.md), each character's voice
     SAMPLES (docs/20-canon/characters/voices/<slug>/<slug>-N.mp3 + voice-design.json),
     and the live cue sheets (audio/live-audio-book/**/scene-*/cues.json).
  2. CO-PRESENCE: two characters are co-present iff one of their cue `role`s speaks in
     the same scene. The co-presence map is computed purely from the cue sheets and is
     emitted even when the embedding server is not yet live.
  3. EMBED each candidate sample via POST {API}/api/embed (multipart `file`), CACHING the
     returned vector to cast-embeddings.json keyed by repo-relative path + content hash, so
     re-runs never re-embed an unchanged clip. Server vectors are L2-normalized (cosine ==
     dot), but cosine() normalizes anyway so synthetic / un-normalized vectors also work.
  4. PICK-OF-3 ENSEMBLE OPTIMIZATION: each character has up to 3 candidate samples; choose
     ONE per character to MAXIMIZE separation among CO-PRESENT pairs (minimize the worst-case
     co-present cosine == maximize the minimum pairwise distance). Solved EXACTLY by iterating
     the Cartesian product of candidate choices when that product is small (<= --exact-cap),
     greedy hill-climb otherwise.
  5. REPORTS (markdown + json): the collision matrix, the co-present collisions, the
     recommended sample per character, and which voices still collide after the best
     selection (-> REGENERATION candidates).
  6. --upload (OFF by default): POST each winner to {API}/api/voices with overwrite=true
     under a stable name (the slug).

  --selftest proves the co-presence parse, the cosine matrix, and the pick-of-3 optimizer on
  SYNTHETIC embeddings with a known-optimal selection, with NO disk or network access -- so
  the logic is validated before /api/embed exists. If /api/embed is not live (404/501 or
  unreachable) the tool prints "embed endpoint not live yet" and STILL emits the co-presence
  map plus the selftest.

The /api/embed and /api/voices auth REUSES the renderer's pattern (resolve_credentials() +
auth_header() + the proxy-bypass opener) from scripts/narrate-chapter-voiceserver.py; those
small helpers are replicated here (not imported) to keep this a self-contained stdlib script
-- the source module's filename is hyphenated and importing it just for two 15-line helpers
would pull in ~1400 unrelated lines.

Usage:
  python3 scripts/cast-audit.py --selftest
  python3 scripts/cast-audit.py [--api http://voice.codingbutter.com] [--threshold 0.75]
                                [--out-dir docs/10-vision/audio/_generated/cast-audit]
                                [--upload]
"""

import argparse
import base64
import binascii
import hashlib
import itertools
import json
import math
import os
import random
import re
import sys
import urllib.error
import urllib.request

# numpy is optional: used only to speed the pairwise matrix if present; the pure-Python
# cosine() below is the reference and the results are identical at this scale.
try:
    import numpy as _np  # noqa: F401
    HAVE_NUMPY = True
except Exception:  # noqa: BLE001
    HAVE_NUMPY = False

# Direct (proxy-bypassing) opener + browser UA, mirroring narrate-chapter-voiceserver.py:
# the voice API is a direct call and the public host's Cloudflare WAF 403s python-urllib's
# default User-Agent. Constructing the opener is a pure object build (no I/O on import).
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
_OPENER.addheaders = [("User-Agent",
                       "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")]

DEFAULT_API = "http://voice.codingbutter.com"

# Repo root = the parent of scripts/. All default paths resolve from here.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CAST_SHEET = os.path.join(REPO_ROOT, "docs", "10-vision", "audio", "cast-sheet.md")
DEFAULT_VOICES_DIR = os.path.join(REPO_ROOT, "docs", "20-canon", "characters", "voices")
DEFAULT_CUES_ROOT = os.path.join(REPO_ROOT, "audio", "live-audio-book")
DEFAULT_OUT_DIR = os.path.join(REPO_ROOT, "docs", "10-vision", "audio", "_generated",
                               "cast-audit")

# Default collision threshold on the cosine of two L2-normalized speaker embeddings.
# 0.75 is a deliberate, documented starting point: with cosine in [-1, 1], same-speaker
# pairs from x-vector / ECAPA-style speaker encoders typically land well above ~0.7 and
# distinct speakers well below, so ~0.75 marks "close enough on the ear to risk confusion."
# It is a heuristic, not a law -- override with --threshold once the live model's own
# same/different distribution is measured against these samples.
DEFAULT_THRESHOLD = 0.75

# Exact pick-of-3 search when the product of per-character candidate counts is <= this;
# greedy hill-climb above it. optimize_selection PRECOMPUTES the candidate-vs-candidate
# cosine for every co-present pair, so each selection's score is a handful of table lookups
# (no vector math) -- which makes an exact 3^k sweep cheap well past a naive estimate. The
# cap is set so the full live ensemble (~3^12) is still solved EXACTLY in a few seconds;
# greedy only takes over for an implausibly large cast. The selftest exercises both paths.
DEFAULT_EXACT_CAP = 2000000

# Cue `role`s that are NOT a single cast character with candidate samples, mapped to the
# roster slug that voices them. Only the narrator family needs an alias (the role token
# "narration"/"notice" is not a hyphen-part of the slug "narrator"); every real character
# role resolves by token-matching a slug part (eli -> rook-eli, dorsey -> dorsey-ray, ...).
ROLE_ALIASES = {
    "narration": "narrator",
    "notice": "narrator",
    "narrator": "narrator",
}

GENERATOR = "scripts/cast-audit.py"


# ------------------------------------------------------------------------------------
# Credentials + auth (replicated pattern from narrate-chapter-voiceserver.py).
# ------------------------------------------------------------------------------------

def resolve_credentials(cli_user, cli_password):
    """(user, password) for HTTP Basic auth, resolved from CLI flags, then the
    VOICE_API_USER/VOICE_API_PASSWORD env vars, then the voice block in ./.mcp.json.
    Returns (None, None) if nothing is found."""
    user = cli_user or os.environ.get("VOICE_API_USER")
    pw = cli_password or os.environ.get("VOICE_API_PASSWORD")
    if user and pw:
        return user, pw
    try:
        with open(os.path.join(REPO_ROOT, ".mcp.json"), "r", encoding="utf-8") as fh:
            env = json.load(fh)["mcpServers"]["voice"]["env"]
        user = user or env.get("VOICE_API_USER")
        pw = pw or env.get("VOICE_API_PASSWORD")
    except Exception:  # noqa: BLE001  (.mcp.json missing or shaped differently)
        pass
    return user, pw


def auth_header(user, password):
    """{'Authorization': 'Basic ...'} for the given creds, or {} when either is missing."""
    if not (user and password):
        return {}
    token = base64.b64encode(("%s:%s" % (user, password)).encode("utf-8")).decode("ascii")
    return {"Authorization": "Basic " + token}


# ------------------------------------------------------------------------------------
# Cosine + similarity matrix (pure Python; numpy only as an optional fast path).
# ------------------------------------------------------------------------------------

def cosine(a, b):
    """Cosine similarity of two equal-length numeric vectors. Normalizes both, so it is
    correct for un-normalized (synthetic) vectors too; for the server's L2-normalized
    vectors it equals the dot product. Returns 0.0 if either vector is zero-length."""
    s = na = nb = 0.0
    for x, y in zip(a, b):
        s += x * y
        na += x * x
        nb += y * y
    if na <= 0.0 or nb <= 0.0:
        return 0.0
    return s / (math.sqrt(na) * math.sqrt(nb))


def similarity_matrix(labels, vectors):
    """Full symmetric cosine matrix for `labels` -> {(label_i, label_j): cos} for i < j,
    plus the diagonal at 1.0. `vectors` is a parallel list of vectors."""
    out = {}
    n = len(labels)
    for i in range(n):
        out[(labels[i], labels[i])] = 1.0
        for j in range(i + 1, n):
            c = cosine(vectors[i], vectors[j])
            out[(labels[i], labels[j])] = c
            out[(labels[j], labels[i])] = c
    return out


# ------------------------------------------------------------------------------------
# Cast roster + candidate samples.
# ------------------------------------------------------------------------------------

def _table_rows(md_text):
    """Yield (header_cells, [data_row_cells, ...]) for every GitHub-style markdown table in
    `md_text`. A table is a run of consecutive lines beginning with '|'; the second line is
    the dashes separator and is skipped. Cells are stripped of surrounding whitespace and
    backticks/asterisks."""

    def cells(line):
        parts = [c.strip().strip("`*").strip() for c in line.strip().strip("|").split("|")]
        return parts

    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i])
                i += 1
            if len(block) >= 2:
                header = cells(block[0])
                data = [cells(r) for r in block[2:]]   # skip the dashes separator row
                yield header, data
        else:
            i += 1


def load_roster(cast_sheet_path):
    """Parse the cast sheet's roster tables into a list of {"name", "slug"} dicts, sorted by
    slug. A roster table is any markdown table whose header has a 'slug' column; the first
    column is the character/voice name. Non-roster tables (the asset-layout, contrast, and
    consistency-ledger tables have no 'slug' header) are ignored. Returns [] if the file is
    missing (degrade gracefully)."""
    try:
        with open(cast_sheet_path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return []
    seen, roster = set(), []
    for header, data in _table_rows(text):
        lower = [h.lower() for h in header]
        if "slug" not in lower:
            continue
        slug_col = lower.index("slug")
        for row in data:
            if len(row) <= slug_col:
                continue
            slug = row[slug_col]
            name = row[0] if row else ""
            if not slug or " " in slug or not re.match(r"^[a-z0-9][a-z0-9-]*$", slug):
                continue
            if slug in seen:
                continue
            seen.add(slug)
            roster.append({"name": name, "slug": slug})
    roster.sort(key=lambda r: r["slug"])
    return roster


def load_candidates(voices_dir, slug):
    """Candidate samples for a slug. Returns {"samples": [abs paths], "default": idx} where
    samples come from voices/<slug>/voice-design.json's `previews` (in order), falling back
    to a sorted glob of <slug>-*.mp3 when the json is missing (legacy / not yet migrated).
    `default` is clamped into range. Returns None if the voice dir has no samples."""
    vdir = os.path.join(voices_dir, slug)
    if not os.path.isdir(vdir):
        return None
    samples, default = [], 0
    design = os.path.join(vdir, "voice-design.json")
    if os.path.isfile(design):
        try:
            with open(design, "r", encoding="utf-8") as fh:
                d = json.load(fh)
            for p in d.get("previews", []):
                f = p.get("file")
                if f and os.path.isfile(os.path.join(vdir, f)):
                    samples.append(os.path.join(vdir, f))
            try:
                default = int(d.get("default", 0))
            except (TypeError, ValueError):
                default = 0
        except (ValueError, OSError):
            samples = []
    if not samples:   # legacy / no json: glob the previews directly
        samples = sorted(os.path.join(vdir, f) for f in os.listdir(vdir)
                         if re.match(re.escape(slug) + r"-\d+\.(mp3|wav|m4a|flac)$", f))
    if not samples:
        return None
    default = max(0, min(default, len(samples) - 1))
    return {"samples": samples, "default": default}


# ------------------------------------------------------------------------------------
# Role -> slug resolution + co-presence.
# ------------------------------------------------------------------------------------

def resolve_role(role, slug_set):
    """Resolve one cue `role` to a roster slug. Returns (slug_or_None, status) where status
    is 'ok', 'ambiguous' (the role token matched >1 roster slug -- never guessed), or
    'unmapped' (no match; e.g. the non-canon render-only 'elder'). Resolution order:
      1. exact slug match,
      2. an explicit ROLE_ALIASES entry (the narrator family),
      3. a token of the role equals a hyphen-part of exactly one roster slug
         (eli -> rook-eli, dorsey -> dorsey-ray, eli_thought -> rook-eli)."""
    r = (role or "").strip().lower()
    if not r:
        return None, "unmapped"
    if r in slug_set:
        return r, "ok"
    if r in ROLE_ALIASES:
        target = ROLE_ALIASES[r]
        return (target, "ok") if target in slug_set else (None, "unmapped")
    tokens = [t for t in re.split(r"[^a-z0-9]+", r) if t]
    matches = set()
    for slug in slug_set:
        parts = slug.split("-")
        if any(t in parts for t in tokens):
            matches.add(slug)
    if len(matches) == 1:
        return next(iter(matches)), "ok"
    if len(matches) > 1:
        return None, "ambiguous"
    return None, "unmapped"


def build_copresence(scene_role_map, slug_set):
    """Pure co-presence builder. `scene_role_map` is {scene_id: [role, ...]} (the voice-cue
    roles per scene). Returns a dict:
      copairs   : {frozenset({slugA, slugB}): [scene, ...]} co-present pairs and where,
      present   : {scene: [slug, ...]} resolved cast slugs speaking in each scene,
      resolved  : {role: slug} the mapping actually used,
      unmapped  : {role: [scene, ...]} roles that resolved to no cast slug,
      ambiguous : {role: [scene, ...]} roles whose token matched >1 slug.
    Two characters are co-present iff they both speak in the same scene."""
    copairs, present, resolved = {}, {}, {}
    unmapped, ambiguous = {}, {}
    for scene in sorted(scene_role_map):
        here = set()
        for role in scene_role_map[scene]:
            slug, status = resolve_role(role, slug_set)
            if status == "ok":
                here.add(slug)
                resolved[role] = slug
            elif status == "ambiguous":
                ambiguous.setdefault(role, set()).add(scene)
            else:
                unmapped.setdefault(role, set()).add(scene)
        present[scene] = sorted(here)
        for a, b in itertools.combinations(sorted(here), 2):
            copairs.setdefault(frozenset((a, b)), set()).add(scene)
    return {
        "copairs": {k: sorted(v) for k, v in copairs.items()},
        "present": present,
        "resolved": resolved,
        "unmapped": {k: sorted(v) for k, v in unmapped.items()},
        "ambiguous": {k: sorted(v) for k, v in ambiguous.items()},
    }


def read_cue_sheets(cues_root):
    """Walk cues_root for scene-*/cues.json and return {scene_id: [voice-cue role, ...]}.
    scene_id is the cue sheet's `scene` field, else its repo-relative directory path. Cue
    sheets that fail to parse are skipped (their path is collected in the second return)."""
    scene_role_map, bad = {}, []
    for dirpath, _dirs, files in os.walk(cues_root):
        if "cues.json" not in files:
            continue
        path = os.path.join(dirpath, "cues.json")
        try:
            with open(path, "r", encoding="utf-8") as fh:
                cs = json.load(fh)
        except (ValueError, OSError):
            bad.append(path)
            continue
        scene = cs.get("scene") or os.path.relpath(dirpath, REPO_ROOT)
        roles = [c.get("role") for c in cs.get("cues", [])
                 if c.get("type") == "voice" and c.get("role")]
        scene_role_map.setdefault(scene, []).extend(roles)
    return scene_role_map, sorted(bad)


# ------------------------------------------------------------------------------------
# Pick-of-3 ensemble optimization.
# ------------------------------------------------------------------------------------

def _worst_and_total(sel, pairs, vecs):
    """For a selection {slug: idx}, return (worst_sim, total_sim) over co-present `pairs`
    (each a (slugA, slugB) tuple) using each slug's chosen candidate vector."""
    worst, total = -1.0, 0.0
    for a, b in pairs:
        c = cosine(vecs[a][sel[a]], vecs[b][sel[b]])
        total += c
        if c > worst:
            worst = c
    return worst, total


def optimize_selection(nodes, vecs, copairs, default_idx, exact_cap=DEFAULT_EXACT_CAP):
    """Choose ONE candidate per node to MINIMIZE the worst-case co-present cosine (==
    maximize the minimum pairwise distance among co-present speakers).

      nodes       : iterable of slugs that have candidate vectors,
      vecs        : {slug: [vec, ...]} the candidate vectors per slug,
      copairs     : iterable of frozenset({a, b}) co-present pairs,
      default_idx : {slug: idx} each slug's canon default preview (the 'before' selection),
      exact_cap   : exact search when product(candidate counts of multi-candidate nodes
                    that appear in a pair) <= this; greedy hill-climb otherwise.

    Returns (selection {slug: idx}, worst_sim, method) where method is 'exact', 'greedy',
    or 'trivial' (no co-present pairs). Single-candidate nodes are fixed at index 0.
    Tie-break: among equal worst-case, prefer the lower total co-present similarity."""
    nodes = list(nodes)
    pairs = [tuple(sorted(p)) for p in copairs
             if all(s in vecs for s in p)]
    base = {s: max(0, min(default_idx.get(s, 0), len(vecs[s]) - 1)) for s in nodes}
    if not pairs:
        return base, 0.0, "trivial"

    # Precompute the candidate-vs-candidate cosine table for each co-present pair, so scoring
    # a selection is a few O(1) lookups rather than O(dim) vector math. This is what makes the
    # exact sweep affordable for the whole ensemble.
    pcos = {}
    for a, b in pairs:
        pcos[(a, b)] = [[cosine(vecs[a][i], vecs[b][j]) for j in range(len(vecs[b]))]
                        for i in range(len(vecs[a]))]

    def score(sel):
        worst, total = -1.0, 0.0
        for a, b in pairs:
            c = pcos[(a, b)][sel[a]][sel[b]]
            total += c
            if c > worst:
                worst = c
        return worst, total

    in_pair = set()
    for a, b in pairs:
        in_pair.add(a)
        in_pair.add(b)
    multi = [s for s in nodes if s in in_pair and len(vecs[s]) > 1]

    product = 1
    for s in multi:
        product *= len(vecs[s])

    if product <= exact_cap:
        best_sel, best_key = None, None
        ranges = [range(len(vecs[s])) for s in multi]
        for combo in itertools.product(*ranges):
            sel = dict(base)
            for s, i in zip(multi, combo):
                sel[s] = i
            key = score(sel)
            if best_key is None or key < best_key:
                best_key, best_sel = key, sel
        return best_sel, best_key[0], "exact"

    # Greedy hill-climb fallback (implausibly large cast only): from the canon defaults,
    # repeatedly switch the single node-index that most improves (worst, total); stop at a
    # local optimum. A handful of random restarts reduce (do not eliminate) local-optimum
    # lock-in -- the residual collisions it reports may be pessimistic, but never spurious.
    def hill_climb(start):
        sel = dict(start)
        cur = score(sel)
        for _ in range(1000):
            best_move, best_after = None, cur
            for s in multi:
                for i in range(len(vecs[s])):
                    if i == sel[s]:
                        continue
                    trial = dict(sel)
                    trial[s] = i
                    after = score(trial)
                    if after < best_after:
                        best_after, best_move = after, (s, i)
            if best_move is None:
                break
            sel[best_move[0]] = best_move[1]
            cur = best_after
        return sel, cur

    rng = random.Random(0)   # deterministic restarts -> idempotent output
    best_sel, best_key = hill_climb(base)
    for _ in range(8):
        start = {s: rng.randrange(len(vecs[s])) for s in nodes}
        sel, key = hill_climb(start)
        if key < best_key:
            best_sel, best_key = sel, key
    return best_sel, best_key[0], "greedy"


# ------------------------------------------------------------------------------------
# Embedding cache + /api/embed + /api/voices.
# ------------------------------------------------------------------------------------

def _sha12(data):
    return hashlib.sha256(data).hexdigest()[:12]


def load_cache(path):
    """Load the embedding cache (key -> {path, sha, embedding, dim, model}); {} if absent."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except (ValueError, OSError):
        return {}


def save_cache(path, cache):
    """Write the cache sorted by key, no timestamp, so an unchanged world yields no diff."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, indent=2, sort_keys=True)
        fh.write("\n")


def cache_key(sample_path):
    """Stable cache key for a sample = '<repo-relative path>@<sha12 of bytes>'. Returns
    (key, sha, data_bytes); raises OSError if the file can't be read."""
    with open(sample_path, "rb") as fh:
        data = fh.read()
    sha = _sha12(data)
    rel = os.path.relpath(sample_path, REPO_ROOT)
    return "%s@%s" % (rel, sha), sha, data


def _multipart(fields, files):
    """Build a multipart/form-data body. fields: {name: str}; files: {name: (filename,
    bytes, content_type)}. Returns (content_type_header, body_bytes)."""
    boundary = "----castaudit" + binascii.hexlify(os.urandom(12)).decode("ascii")
    out = []
    for name, value in fields.items():
        out.append(("--%s\r\n" % boundary).encode())
        out.append(('Content-Disposition: form-data; name="%s"\r\n\r\n' % name).encode())
        out.append(("%s\r\n" % value).encode())
    for name, (filename, data, ctype) in files.items():
        out.append(("--%s\r\n" % boundary).encode())
        out.append(('Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
                    % (name, filename)).encode())
        out.append(("Content-Type: %s\r\n\r\n" % ctype).encode())
        out.append(data)
        out.append(b"\r\n")
    out.append(("--%s--\r\n" % boundary).encode())
    return ("multipart/form-data; boundary=%s" % boundary), b"".join(out)


_AUDIO_CT = {"mp3": "audio/mpeg", "wav": "audio/wav", "m4a": "audio/mp4",
             "flac": "audio/flac", "ogg": "audio/ogg"}


def embed_clip(api, auth, sample_path, data=None):
    """POST one clip to {api}/api/embed (multipart `file`). Returns (vector_dict, status):
      ('ok', {'embedding':[...], 'dim':int, 'model':str}) keyed as (result, 'ok'),
      (None, 'not_live')  -- 404 / 501 / unreachable (server build in progress),
      (None, 'auth')      -- 401 / 403 (missing or rejected credentials),
      (None, 'http_NNN' | 'bad-response' | 'error:...') -- other failures.
    `data` may be passed to avoid re-reading the file."""
    if data is None:
        with open(sample_path, "rb") as fh:
            data = fh.read()
    ext = os.path.splitext(sample_path)[1].lower().lstrip(".")
    ctype = _AUDIO_CT.get(ext, "application/octet-stream")
    content_type, body = _multipart({}, {"file": (os.path.basename(sample_path), data, ctype)})
    headers = {"Content-Type": content_type, "Accept": "application/json"}
    headers.update(auth or {})
    req = urllib.request.Request(api.rstrip("/") + "/api/embed", data=body, headers=headers)
    try:
        with _OPENER.open(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
        emb = payload.get("embedding")
        if not isinstance(emb, list) or not emb:
            return None, "bad-response"
        return ({"embedding": [float(x) for x in emb],
                 "dim": int(payload.get("dim", len(emb))),
                 "model": str(payload.get("model", ""))}, "ok")
    except urllib.error.HTTPError as err:
        if err.code in (404, 501):
            return None, "not_live"
        if err.code in (401, 403):
            return None, "auth"
        return None, "http_%d" % err.code
    except urllib.error.URLError:
        return None, "not_live"   # connection refused / DNS failure: server not up yet
    except Exception as err:  # noqa: BLE001
        return None, "error:" + str(err)[:120]


def upload_voice(api, auth, name, sample_path, overwrite=True):
    """POST a winner sample to {api}/api/voices (multipart) under `name`, overwrite=true.
    Returns (ok_bool, detail)."""
    with open(sample_path, "rb") as fh:
        data = fh.read()
    ext = os.path.splitext(sample_path)[1].lower().lstrip(".")
    ctype = _AUDIO_CT.get(ext, "application/octet-stream")
    fields = {"name": name, "overwrite": "true" if overwrite else "false"}
    content_type, body = _multipart(fields, {"file": (os.path.basename(sample_path), data, ctype)})
    headers = {"Content-Type": content_type, "Accept": "application/json"}
    headers.update(auth or {})
    req = urllib.request.Request(api.rstrip("/") + "/api/voices", data=body, headers=headers)
    try:
        with _OPENER.open(req, timeout=120) as resp:
            return True, resp.read().decode("utf-8", "replace")[:200]
    except urllib.error.HTTPError as err:
        return False, "HTTP %d: %s" % (err.code, err.read().decode("utf-8", "replace")[:200])
    except Exception as err:  # noqa: BLE001
        return False, str(err)[:200]


# ------------------------------------------------------------------------------------
# Report rendering (markdown + json), idempotent: sorted, no timestamps, DO NOT EDIT.
# ------------------------------------------------------------------------------------

def _fmt_pair(p):
    return " + ".join(sorted(p))


def render_copresence_md(cop, scene_role_map):
    """Markdown for the co-presence section (always computable, server or not)."""
    lines = []
    lines.append("## Co-presence map\n")
    lines.append("Two characters are co-present iff one of their cue roles speaks in the "
                 "same scene. Derived from the live cue sheets.\n")
    lines.append("- Scenes parsed: **%d**" % len(scene_role_map))
    lines.append("- Co-present cast pairs: **%d**\n" % len(cop["copairs"]))

    lines.append("### Co-present pairs\n")
    if cop["copairs"]:
        lines.append("| Pair | Scenes |")
        lines.append("| --- | --- |")
        for pair in sorted(cop["copairs"], key=_fmt_pair):
            lines.append("| %s | %s |" % (_fmt_pair(pair), ", ".join(cop["copairs"][pair])))
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("### Speakers present per scene\n")
    lines.append("| Scene | Cast present |")
    lines.append("| --- | --- |")
    for scene in sorted(cop["present"]):
        lines.append("| %s | %s |" % (scene, ", ".join(cop["present"][scene]) or "_(none)_"))
    lines.append("")

    if cop["unmapped"] or cop["ambiguous"]:
        lines.append("### Roles not mapped to a cast slug\n")
        lines.append("These cue roles did not resolve to a single roster character and are "
                     "EXCLUDED from collision analysis (reported, never guessed).\n")
        lines.append("| Role | Why | Scenes |")
        lines.append("| --- | --- | --- |")
        for role in sorted(cop["unmapped"]):
            lines.append("| %s | no matching cast slug | %s |"
                         % (role, ", ".join(cop["unmapped"][role])))
        for role in sorted(cop["ambiguous"]):
            lines.append("| %s | ambiguous (matched >1 slug) | %s |"
                         % (role, ", ".join(cop["ambiguous"][role])))
        lines.append("")
    return "\n".join(lines)


def render_report_md(ctx):
    """Assemble the full markdown report from the context dict built in main()."""
    banner = ("<!-- DO NOT EDIT - generated by %s. Re-run the tool; edit the cast sheet, "
              "voice samples, or cue sheets, never this file. -->" % GENERATOR)
    head = [
        banner,
        "",
        "# Cast Acoustic Ensemble Audit\n",
        "> **DO NOT EDIT - generated.** Acoustic co-presence + voice-separation audit for "
        "the live edition. Produced by `%s` from the cast sheet, the per-character voice "
        "samples, and the live cue sheets. Re-run to refresh." % GENERATOR,
        "",
        "- API: `%s`" % ctx["api"],
        "- Collision threshold (cosine): **%.3f**" % ctx["threshold"],
        "- Embedding endpoint: **%s**" % ("live" if ctx["embed_live"] else "NOT live yet"),
        "",
    ]
    body = [render_copresence_md(ctx["cop"], ctx["scene_role_map"])]

    if not ctx["embed_live"]:
        body.append("## Acoustic analysis\n")
        body.append("_Skipped: the `/api/embed` endpoint is not live yet "
                    "(`%s`). The co-presence map above is final and the audit re-runs "
                    "automatically once the endpoint answers._\n" % ctx["embed_status"])
        return "\n".join(head + body)

    # Collision matrix (default/canon selection) over co-present nodes.
    body.append("## Collision matrix (canon-default samples)\n")
    nodes = ctx["nodes"]
    if nodes:
        body.append("Cosine similarity among co-present cast using each character's current "
                    "canon default preview. Model: `%s`, dim %s.\n"
                    % (ctx["model"], ctx["dim"]))
        header = "| | " + " | ".join(nodes) + " |"
        sep = "| --- " * (len(nodes) + 1) + "|"
        body.append(header)
        body.append(sep)
        for a in nodes:
            row = ["**%s**" % a]
            for b in nodes:
                row.append("1.000" if a == b else "%.3f" % ctx["matrix"][(a, b)])
            body.append("| " + " | ".join(row) + " |")
        body.append("")

    body.append("## Co-present collisions (canon-default samples)\n")
    if ctx["before_collisions"]:
        body.append("Pairs above the threshold with the current canon picks:\n")
        body.append("| Pair | Cosine | Scenes |")
        body.append("| --- | --- | --- |")
        for pair, sim in ctx["before_collisions"]:
            body.append("| %s | %.3f | %s |"
                        % (_fmt_pair(pair), sim, ", ".join(ctx["cop"]["copairs"][pair])))
    else:
        body.append("_None: every co-present pair is already separated under the canon "
                    "defaults._")
    body.append("")

    body.append("## Recommended selection (pick-of-3)\n")
    body.append("Optimizer: **%s**, worst-case co-present cosine after selection: **%.3f** "
                "(lower is better).\n" % (ctx["method"], ctx["worst_after"]))
    body.append("| Character | Chosen preview | Index | Canon default | Re-pick? |")
    body.append("| --- | --- | --- | --- | --- |")
    for slug in nodes:
        chosen = ctx["selection"][slug]
        dflt = ctx["default_idx"][slug]
        fname = os.path.basename(ctx["samples"][slug][chosen])
        body.append("| %s | %s | %d | %d | %s |"
                    % (slug, fname, chosen, dflt, "**yes**" if chosen != dflt else "no"))
    body.append("")

    body.append("## Residual collisions after best selection (REGENERATION candidates)\n")
    if ctx["after_collisions"]:
        body.append("These co-present pairs still exceed the threshold even with the best "
                    "sample choice -- the voices are too close; one of each pair should be "
                    "RE-DESIGNED (voice-designer) to widen the gap:\n")
        body.append("| Pair | Cosine | Scenes |")
        body.append("| --- | --- | --- |")
        for pair, sim in ctx["after_collisions"]:
            body.append("| %s | %.3f | %s |"
                        % (_fmt_pair(pair), sim, ", ".join(ctx["cop"]["copairs"][pair])))
    else:
        body.append("_None: the best selection separates every co-present pair below the "
                    "threshold. No regeneration needed._")
    body.append("")
    return "\n".join(head + body)


def build_report_json(ctx):
    """Structured equivalent of the markdown report (sorted, deterministic)."""
    out = {
        "api": ctx["api"],
        "threshold": ctx["threshold"],
        "embed_endpoint_live": ctx["embed_live"],
        "embed_status": ctx["embed_status"],
        "scenes_parsed": len(ctx["scene_role_map"]),
        "copresent_pairs": sorted(
            ({"pair": sorted(p), "scenes": ctx["cop"]["copairs"][p]}
             for p in ctx["cop"]["copairs"]),
            key=lambda d: d["pair"]),
        "present_by_scene": {s: ctx["cop"]["present"][s] for s in sorted(ctx["cop"]["present"])},
        "role_resolution": {r: ctx["cop"]["resolved"][r] for r in sorted(ctx["cop"]["resolved"])},
        "unmapped_roles": ctx["cop"]["unmapped"],
        "ambiguous_roles": ctx["cop"]["ambiguous"],
    }
    if ctx["embed_live"]:
        out["model"] = ctx["model"]
        out["dim"] = ctx["dim"]
        out["optimizer"] = ctx["method"]
        out["worst_case_cosine_after"] = ctx["worst_after"]
        out["selection"] = {
            slug: {"index": ctx["selection"][slug],
                   "preview": os.path.basename(ctx["samples"][slug][ctx["selection"][slug]]),
                   "canon_default": ctx["default_idx"][slug],
                   "repick": ctx["selection"][slug] != ctx["default_idx"][slug]}
            for slug in sorted(ctx["nodes"])}
        out["collisions_default"] = sorted(
            ({"pair": sorted(p), "cosine": round(s, 6)} for p, s in ctx["before_collisions"]),
            key=lambda d: d["pair"])
        out["regeneration_candidates"] = sorted(
            ({"pair": sorted(p), "cosine": round(s, 6)} for p, s in ctx["after_collisions"]),
            key=lambda d: d["pair"])
    return out


# ------------------------------------------------------------------------------------
# Self-test: synthetic embeddings with a KNOWN-optimal selection. No disk / no network.
# ------------------------------------------------------------------------------------

def run_selftest():
    """Validate the co-presence parse, the cosine matrix, and the pick-of-3 optimizer on
    hand-built vectors with a known collision and a known optimum. Returns 0 on PASS, 1 on
    the first failure (printing which check failed)."""
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)
            print("  FAIL: " + msg)
        else:
            print("  ok:   " + msg)

    # --- cosine normalization + known values ---
    check(abs(cosine([1, 0, 0], [1, 0, 0]) - 1.0) < 1e-9, "cosine identical == 1.0")
    check(abs(cosine([1, 0, 0], [0, 1, 0]) - 0.0) < 1e-9, "cosine orthogonal == 0.0")
    check(abs(cosine([2, 0, 0], [1, 0, 0]) - 1.0) < 1e-9,
          "cosine normalizes un-normalized vectors ([2,0,0] vs [1,0,0] == 1.0)")
    check(abs(cosine([0, 0, 0], [1, 0, 0])) < 1e-9, "cosine zero-vector guarded == 0.0")

    # --- co-presence parse: aaa/bbb/ccc are cast; 'narr' is a production/unmapped role ---
    slug_set = {"aaa", "bbb", "ccc", "narrator", "rook-eli", "rook-ruth"}
    # alias + token resolution
    check(resolve_role("aaa", slug_set) == ("aaa", "ok"), "resolve exact slug")
    check(resolve_role("narration", slug_set) == ("narrator", "ok"), "resolve alias narration->narrator")
    check(resolve_role("eli", slug_set) == ("rook-eli", "ok"), "resolve token eli->rook-eli")
    check(resolve_role("eli_thought", slug_set) == ("rook-eli", "ok"),
          "resolve compound token eli_thought->rook-eli")
    check(resolve_role("rook", slug_set)[1] == "ambiguous",
          "ambiguous token rook (rook-eli vs rook-ruth) flagged, not guessed")
    check(resolve_role("elder", slug_set)[1] == "unmapped", "unmapped role elder reported")

    # No 'narrator' in this slug_set, so 'narration' resolves as unmapped (production role)
    # and only the three cast characters drive co-presence -- the isolated known scenario.
    scene_role_map = {
        "s1": ["aaa", "bbb", "narration"],
        "s2": ["bbb", "ccc"],
        "s3": ["aaa", "ccc", "elder"],
    }
    cop = build_copresence(scene_role_map, {"aaa", "bbb", "ccc"})
    pairs = set(cop["copairs"].keys())
    expected = {frozenset(("aaa", "bbb")), frozenset(("bbb", "ccc")), frozenset(("aaa", "ccc"))}
    check(pairs == expected, "co-presence pairs == {aaa-bbb, bbb-ccc, aaa-ccc}")
    check("elder" in cop["unmapped"] and "narration" in cop["unmapped"],
          "unmapped 'elder'/'narration' surfaced in co-presence output")

    # --- similarity matrix ---
    labels = ["aaa", "bbb", "ccc"]
    default_vecs = [[1, 0, 0], [1, 0, 0], [1, 0, 0]]   # all default to axis x -> all collide
    mat = similarity_matrix(labels, default_vecs)
    check(abs(mat[("aaa", "bbb")] - 1.0) < 1e-9, "matrix: default aaa vs bbb == 1.0 (collision)")

    # --- pick-of-3 optimization with a KNOWN optimum ---
    # Each of aaa/bbb/ccc has 3 candidates = the 3 orthogonal axes; all DEFAULT to axis x.
    # Default selection -> worst-case cosine 1.0 (every pair identical). The optimum assigns
    # the three nodes distinct axes -> worst-case cosine 0.0. Optimum worst-case == 0.0.
    vecs = {
        "aaa": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "bbb": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "ccc": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    }
    default_idx = {"aaa": 0, "bbb": 0, "ccc": 0}

    before_worst, _ = _worst_and_total(default_idx,
                                       [tuple(sorted(p)) for p in expected], vecs)
    check(abs(before_worst - 1.0) < 1e-9, "default selection worst-case cosine == 1.0")

    for label, cap in (("exact", DEFAULT_EXACT_CAP), ("greedy", 0)):
        sel, worst, method = optimize_selection(["aaa", "bbb", "ccc"], vecs, expected,
                                                 default_idx, exact_cap=cap)
        check(method == label, "optimizer used the %s path (cap=%d)" % (label, cap))
        check(abs(worst - 0.0) < 1e-9,
              "%s: optimized worst-case cosine == 0.0 (known optimum)" % label)
        chosen_axes = {sel["aaa"], sel["bbb"], sel["ccc"]}
        check(len(chosen_axes) == 3,
              "%s: optimum assigns three distinct axes %s" % (label, sorted(chosen_axes)))

    # --- collision flagging at threshold 0.75 before vs after ---
    thr = 0.75
    pairs_t = [tuple(sorted(p)) for p in expected]
    before = [p for p in pairs_t if cosine(vecs[p[0]][0], vecs[p[1]][0]) > thr]
    check(len(before) == 3, "all 3 pairs collide at threshold 0.75 under defaults")
    sel, _, _ = optimize_selection(["aaa", "bbb", "ccc"], vecs, expected, default_idx)
    after = [p for p in pairs_t if cosine(vecs[p[0]][sel[p[0]]], vecs[p[1]][sel[p[1]]]) > thr]
    check(len(after) == 0, "no residual collisions after best selection at threshold 0.75")

    print("")
    if failures:
        print("SELFTEST: FAIL (%d check(s) failed)" % len(failures))
        return 1
    print("SELFTEST: PASS")
    return 0


# ------------------------------------------------------------------------------------
# Main.
# ------------------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="Cast acoustic ensemble-audit + voice selection.")
    ap.add_argument("--api", default=DEFAULT_API)
    ap.add_argument("--user", default=None)
    ap.add_argument("--password", default=None)
    ap.add_argument("--cast-sheet", default=DEFAULT_CAST_SHEET)
    ap.add_argument("--voices-dir", default=DEFAULT_VOICES_DIR)
    ap.add_argument("--cues-root", default=DEFAULT_CUES_ROOT)
    ap.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--exact-cap", type=int, default=DEFAULT_EXACT_CAP)
    ap.add_argument("--no-cache", action="store_true", help="force re-embed (ignore cache)")
    ap.add_argument("--upload", action="store_true",
                    help="POST winners to /api/voices (overwrite=true). OFF by default.")
    ap.add_argument("--selftest", action="store_true",
                    help="run synthetic self-test only (no disk/network); exit 0 on pass")
    args = ap.parse_args(argv)

    if args.selftest:
        print("SELFTEST: synthetic co-presence + cosine + pick-of-3\n")
        return run_selftest()

    # 1. Roster + candidates.
    roster = load_roster(args.cast_sheet)
    slug_set = {r["slug"] for r in roster}
    if not slug_set:
        print("ERROR: no roster slugs parsed from %s" % args.cast_sheet, file=sys.stderr)
        return 2

    # 2. Co-presence from the cue sheets (always computable).
    scene_role_map, bad = read_cue_sheets(args.cues_root)
    if bad:
        print("WARN: skipped %d unparseable cue sheet(s): %s"
              % (len(bad), ", ".join(bad)), file=sys.stderr)
    cop = build_copresence(scene_role_map, slug_set)

    # Participating cast = every slug that speaks in some scene. Only these can collide by
    # co-presence, so only their candidates are embedded (saves API calls; non-co-present
    # cast carry no co-presence risk).
    participating = sorted({s for present in cop["present"].values() for s in present})
    samples = {}
    default_idx = {}
    missing_samples = []
    for slug in participating:
        cand = load_candidates(args.voices_dir, slug)
        if not cand:
            missing_samples.append(slug)
            continue
        samples[slug] = cand["samples"]
        default_idx[slug] = cand["default"]
    if missing_samples:
        print("WARN: no voice samples for participating slug(s): %s"
              % ", ".join(missing_samples), file=sys.stderr)

    auth = auth_header(*resolve_credentials(args.user, args.password))
    cache_path = os.path.join(args.out_dir, "cast-embeddings.json")
    cache = {} if args.no_cache else load_cache(cache_path)

    # 3. Embed every candidate (cached). Stop early if the endpoint is not live.
    embed_live = True
    embed_status = "ok"
    vecs = {}          # slug -> [vec per candidate]
    model = dim = None
    cache_dirty = False
    for slug in participating:
        if slug not in samples:
            continue
        vlist = []
        for path in samples[slug]:
            try:
                key, _sha, data = cache_key(path)
            except OSError as err:
                print("WARN: cannot read sample %s: %s" % (path, err), file=sys.stderr)
                vlist = None
                break
            entry = cache.get(key)
            if entry is None:
                result, status = embed_clip(args.api, auth, path, data=data)
                if status != "ok":
                    embed_live = False
                    embed_status = status
                    break
                entry = {"path": os.path.relpath(path, REPO_ROOT), "sha": _sha,
                         "embedding": result["embedding"], "dim": result["dim"],
                         "model": result["model"]}
                cache[key] = entry
                cache_dirty = True
            vlist.append(entry["embedding"])
            model = entry.get("model", model)
            dim = entry.get("dim", dim)
        if not embed_live:
            break
        if vlist:
            vecs[slug] = vlist

    if cache_dirty and embed_live:
        save_cache(cache_path, cache)

    # 4. + 5. Optimize + collisions (only when embeddings exist).
    ctx = {
        "api": args.api, "threshold": args.threshold, "cop": cop,
        "scene_role_map": scene_role_map, "embed_live": embed_live,
        "embed_status": embed_status, "samples": samples, "default_idx": default_idx,
    }
    if embed_live and vecs:
        nodes = sorted(vecs)
        ctx["nodes"] = nodes
        ctx["model"] = model or ""
        ctx["dim"] = dim
        # Full default-sample matrix among co-present nodes.
        ctx["matrix"] = similarity_matrix(
            nodes, [vecs[s][min(default_idx.get(s, 0), len(vecs[s]) - 1)] for s in nodes])
        copairs = [p for p in cop["copairs"] if all(s in vecs for s in p)]
        # Before: collisions under canon defaults.
        before = []
        for p in copairs:
            a, b = sorted(p)
            ia = min(default_idx.get(a, 0), len(vecs[a]) - 1)
            ib = min(default_idx.get(b, 0), len(vecs[b]) - 1)
            s = cosine(vecs[a][ia], vecs[b][ib])
            if s > args.threshold:
                before.append((p, s))
        ctx["before_collisions"] = sorted(before, key=lambda x: (-x[1], _fmt_pair(x[0])))
        # Optimize.
        sel, worst, method = optimize_selection(nodes, vecs, copairs, default_idx,
                                                 exact_cap=args.exact_cap)
        ctx["selection"], ctx["worst_after"], ctx["method"] = sel, worst, method
        # After: residual collisions.
        after = []
        for p in copairs:
            a, b = sorted(p)
            s = cosine(vecs[a][sel[a]], vecs[b][sel[b]])
            if s > args.threshold:
                after.append((p, s))
        ctx["after_collisions"] = sorted(after, key=lambda x: (-x[1], _fmt_pair(x[0])))
    else:
        ctx["embed_live"] = embed_live and bool(vecs)
        if not vecs and embed_live:
            ctx["embed_status"] = "no embeddings (no participating samples)"

    # Write reports (idempotent: sorted, no timestamps, DO NOT EDIT banner).
    os.makedirs(args.out_dir, exist_ok=True)
    md_path = os.path.join(args.out_dir, "cast-audit.md")
    json_path = os.path.join(args.out_dir, "cast-audit.json")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(render_report_md(ctx).rstrip() + "\n")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(build_report_json(ctx), fh, indent=2, sort_keys=True)
        fh.write("\n")

    # 6. Upload winners (opt-in).
    if args.upload and ctx["embed_live"]:
        if not auth:
            print("WARN: --upload requested but no credentials resolved; skipping upload",
                  file=sys.stderr)
        else:
            for slug in ctx["nodes"]:
                path = samples[slug][ctx["selection"][slug]]
                ok, detail = upload_voice(args.api, auth, slug, path, overwrite=True)
                print("UPLOAD %-16s %s  (%s)" % (slug, "OK" if ok else "FAIL", detail),
                      file=sys.stderr)

    # Console summary.
    if not ctx["embed_live"]:
        print("embed endpoint not live yet (%s)" % ctx["embed_status"])
    print("co-presence: %d scene(s), %d co-present pair(s)"
          % (len(scene_role_map), len(cop["copairs"])))
    if ctx["embed_live"]:
        print("acoustic: %d node(s), optimizer=%s, worst-case cosine after=%.3f, "
              "%d default collision(s), %d residual"
              % (len(ctx["nodes"]), ctx["method"], ctx["worst_after"],
                 len(ctx["before_collisions"]), len(ctx["after_collisions"])))
    print("reports: %s , %s" % (os.path.relpath(md_path, REPO_ROOT),
                                 os.path.relpath(json_path, REPO_ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
