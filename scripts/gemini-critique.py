#!/usr/bin/env python3
"""Gemini editorial critique for a drafted chapter of The Unnecessary.

Part of the chapter authorship pipeline (Decision 046): Opus drafts, Gemini
critiques (this script), Opus adjudicates, the author approves.

Standard library only. Sends a drafted chapter plus its grounding context
(the context pack and the blueprint) to gemini-2.5-pro and asks for STRUCTURED
editorial suggestions, never a rewrite. Gemini suggests; Opus decides.

Usage:
  python3 scripts/gemini-critique.py <chapter.md> \
      [--pack .context/<chapter>.pack.md] \
      [--blueprint docs/40-blueprints/book-1/<chapter>/blueprint.md] \
      [--out <critique.md>] [--model gemini-2.5-pro]

The API key is read from the GEMINI_API_KEY or GOOGLE_API_KEY environment
variable, falling back to the same names in the repo-root .env file. The key
is never printed.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error

API_HOST = "https://generativelanguage.googleapis.com"


def load_key():
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        val = os.environ.get(name)
        if val:
            return val.strip()
    # Fall back to .env at repo root (relative to this script's parent).
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(repo_root, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
                    if line.startswith(name + "="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def read_file(path):
    if not path or not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


RUBRIC = """You are a sharp, experienced fiction editor reviewing one chapter of a
literary near-future novel called "The Unnecessary". You are NOT the author and
you must NOT rewrite the chapter. You produce a structured list of editorial
SUGGESTIONS that the author (a separate model) will then accept or reject.

Judge the chapter ONLY against the project's own standards, provided below as
the context pack (canon, style guide, continuity) and the chapter blueprint.
Do not impose generic taste or a different style. The house style is grounded,
restrained, close-third on a single viewpoint per chapter, past tense, no em
dashes, subtext over explanation, and it avoids cyberpunk cliches.

For EACH suggestion, give:
- category: one of [prose, style, canon, continuity, reveal-safety, pacing, dialogue]
- location: a short quote or the scene/paragraph it refers to
- issue: what is weak, wrong, or risky
- suggestion: the specific change you would propose (concise)
- severity: high, medium, or low

Pay special attention to:
1. STYLE violations: any em dash; any cliche on the project's prohibited list;
   filtering ("he saw that", "he felt"), on-the-nose dialogue, telling not showing.
2. CANON or CONTINUITY contradictions against the pack.
3. REVEAL-SAFETY: anything that exposes a future reveal early, breaks the single
   viewpoint, or gives a character knowledge they should not have yet. (This is
   Chapter 1; Morrow does not exist yet and the protagonist's deep history is
   only hinted.)
4. PROSE craft: weak lines, flat sensory detail, pacing sags, a soft ending.

Be specific and concrete. Quote the text. Rank the most important suggestions
first. Do not pad. If something is genuinely strong, do not invent a problem.
Output a clean markdown document titled "# Gemini Editorial Critique" with the
suggestions grouped by severity. End with a short "## Overall" paragraph."""


def build_payload(chapter, pack, blueprint):
    prompt = (
        RUBRIC
        + "\n\n===== CHAPTER BLUEPRINT (the plan this chapter must execute) =====\n"
        + (blueprint or "(none provided)")
        + "\n\n===== CONTEXT PACK (canon, style, continuity authorities) =====\n"
        + (pack or "(none provided)")
        + "\n\n===== THE DRAFTED CHAPTER TO CRITIQUE =====\n"
        + chapter
        + "\n\n===== END. Produce the structured critique now. ====="
    )
    return {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 20000},
    }


def call_gemini(model, key, payload):
    url = API_HOST + "/v1beta/models/" + model + ":generateContent?key=" + key
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        try:
            msg = json.loads(detail).get("error", {}).get("message", detail)
        except Exception:
            msg = detail
        return None, "HTTP " + str(err.code) + ": " + msg[:500]
    except Exception as err:  # noqa: BLE001
        return None, str(err)[:500]
    cands = body.get("candidates")
    if not cands:
        return None, "no candidates: " + json.dumps(body)[:400]
    parts = cands[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts)
    if not text:
        return None, "empty text (finishReason=" + str(cands[0].get("finishReason")) + ")"
    return text, None


def main():
    ap = argparse.ArgumentParser(description="Gemini editorial critique for a chapter.")
    ap.add_argument("chapter")
    ap.add_argument("--pack", default=None)
    ap.add_argument("--blueprint", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--model", default="gemini-2.5-pro")
    ap.add_argument("--manifest", default=None,
                    help="If given, REBUILD the pack from this manifest first so the "
                         "critique can never run against a stale snapshot.")
    args = ap.parse_args()

    # Freshness guarantee: rebuild the pack from its manifest before critiquing,
    # so an out-of-date snapshot can never be reviewed as if it were current.
    if args.manifest:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        builder = os.path.join(script_dir, "build-context-pack.py")
        print("Rebuilding pack from manifest before critique (freshness guarantee)...",
              file=sys.stderr)
        rebuilt = subprocess.run([sys.executable, builder, args.manifest],
                                 capture_output=True, text=True)
        if rebuilt.returncode != 0:
            print("ERROR rebuilding pack: " + (rebuilt.stderr or rebuilt.stdout)[:400],
                  file=sys.stderr)
            return 1

    key = load_key()
    if not key:
        print("ERROR: no GEMINI_API_KEY or GOOGLE_API_KEY found in env or .env", file=sys.stderr)
        return 2
    chapter = read_file(args.chapter)
    if not chapter:
        print("ERROR: chapter file not found or empty: " + args.chapter, file=sys.stderr)
        return 2

    payload = build_payload(chapter, read_file(args.pack), read_file(args.blueprint))
    print("Sending chapter to " + args.model + " for critique (key hidden)...", file=sys.stderr)
    text, err = call_gemini(args.model, key, payload)
    if err:
        print("ERROR: " + err, file=sys.stderr)
        return 1

    out_path = args.out or (os.path.splitext(args.chapter)[0] + ".gemini-critique.md")
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(text if text.endswith("\n") else text + "\n")
    print("Critique written to " + out_path + " (" + str(len(text)) + " chars)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
