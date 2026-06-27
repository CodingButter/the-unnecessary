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
- category: one of [prose, style, canon, continuity, reveal-safety, pacing, dialogue, focus]
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
4. PROSE CRAFT, and be DEMANDING here: hunt the weakest lines in the chapter and
   name them. Flag flat, tautological, or filler sentences (for example a sentence
   that defines a thing as itself, like "the street looked like a street"), lazy or
   generic phrasing, telling where showing would land harder, dull sensory detail,
   pacing sags, and any sentence that does not earn its place. Propose a concrete,
   sharper rewrite for each. Assume even strong prose can be sharper.
5. STYLE-GUIDE COMPLIANCE: hold every line against the project Style Guide provided
   in the context pack (its prohibited patterns, cliches, and required qualities).
   Flag each violation and name the rule it breaks.
6. FOCUS-DELIVERY and VOICE-SPECIFICITY: the blueprint includes a "Character Focus"
   section naming, for each character who matters, a focus level (blur, sketch,
   sharp, or crisp) and a revelation target along three axes (physical, emotional,
   interior). For EACH focused character, judge whether the draft delivered that
   target and whether the character arrived as THEMSELVES, in their specific voice
   and heritage, rather than as the unmarked cultural default. Flag a focused
   character who stays a blur when the target was sharp, whose dialogue is generic
   where the profile gives them a distinct register, or whose physical, emotional,
   or interior axis was left undelivered. Use category "focus" for these. Reward
   image over inventory: a single concrete image that lands the character beats a
   padded trait list. Do not penalize a deliberately low focus level.

Be specific and concrete. Quote the text. Rank the most important suggestions
first. Do not pad, but do NOT go easy: a discerning literary editor would not let a
flat or lazy line stand, so surface the real weaknesses even in an otherwise strong
chapter. Call a line strong only when it truly is. Output a clean markdown document
titled "# Gemini Editorial Critique" with the suggestions grouped by severity. End
with a short "## Overall" paragraph."""


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


NARRATION_RUBRIC = """You are a veteran AUDIOBOOK DIRECTOR and performance editor reviewing a
NARRATION SCRIPT for one chapter of the literary near-future novel "The Unnecessary".
The script marks the chapter's prose with ElevenLabs Eleven v3 "audio tags" (bracketed
stage directions like [weary], [flat], [tense], [slowly]) and ellipses for pacing, so a
narrator performs it rather than reading it flat. You do NOT rewrite it; you produce a
structured list of SUGGESTIONS the author will accept or reject.

You are given the REFERENCE PROSE (the canonical manuscript) and the NARRATION SCRIPT.

Judge on these axes:
1. FIDELITY (most important): the script must reproduce the prose WORD FOR WORD, adding
   only bracketed tags and ellipses. Flag as HIGH any added, cut, reordered, or reworded
   prose word versus the reference.
2. DIRECTION DENSITY: is the markup detailed enough that the read will clearly differ from
   flat text-to-speech? Flag long stretches that are under-directed (no pacing, pause, or
   emotional marking); under-direction is the most likely failure.
3. REGISTER DISTINCTION: are the three registers clearly performed and differentiated, the
   automated corporate notices read FLAT and administrative (the horror is the calm), Eli's
   interiority weary and controlled, Lena over the failing link clipped and tense? Flag
   where a register is generic or indistinct.
4. PACING & PEAKS: are ellipses and pauses well placed, the two emotional peaks (the midday
   "slow opening of a hand" passage and the final line) given deliberate weight, and nothing
   monotonous or rushed?
5. v3 TAG CRAFT: tags color roughly the next 4-5 words, so they must sit right before the
   words they shape. Flag mis-placed tags, tags v3 will not understand, or reliance on break
   tags where ellipses are more reliable.
6. TONE FIT: the book is grounded and austere. Flag direction that tips into melodrama, but
   ALSO flag timidity (under-direction is the more likely problem here).

For each suggestion give: category (one of fidelity, density, register, pacing, tag-craft,
tone), location (quote the line), issue, suggestion (concise), severity (high/medium/low).
Be specific and quote the text. Output markdown titled "# Gemini Narration-Script Critique",
grouped by severity, ending with a short "## Overall" paragraph."""


def build_payload_narration(script, reference, blueprint):
    prompt = (
        NARRATION_RUBRIC
        + "\n\n===== REFERENCE PROSE (the canonical manuscript; words must match exactly) =====\n"
        + (reference or "(none provided)")
        + "\n\n===== THE NARRATION SCRIPT TO CRITIQUE =====\n"
        + script
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
    ap.add_argument("--mode", default="prose", choices=["prose", "narration"],
                    help="prose: critique a drafted chapter. narration: critique a "
                         "narration script against the reference manuscript.")
    ap.add_argument("--reference", default=None,
                    help="Narration mode: the canonical manuscript the script must match.")
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

    if args.mode == "narration":
        payload = build_payload_narration(chapter, read_file(args.reference), read_file(args.blueprint))
    else:
        payload = build_payload(chapter, read_file(args.pack), read_file(args.blueprint))
    print("Sending " + args.mode + " critique to " + args.model + " (key hidden)...", file=sys.stderr)
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
