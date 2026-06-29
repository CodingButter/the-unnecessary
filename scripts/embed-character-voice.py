#!/usr/bin/env python3
"""Embed a character's DEFAULT voice sample into their profile, under the portrait.

Mirrors the portrait embed: a clickable <audio> player plus a fallback link, pointing at the
default sample recorded in docs/20-canon/characters/voices/<slug>/voice-design.json. Inserts
the block right after the portrait line. Idempotent -- replaces any prior voice block,
delimited by <!-- voice:start --> / <!-- voice:end -->.

Usage: python3 scripts/embed-character-voice.py <slug>
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILES = os.path.join(REPO, "docs", "20-canon", "characters", "profiles")
VOICES = os.path.join(REPO, "docs", "20-canon", "characters", "voices")
START, END = "<!-- voice:start -->", "<!-- voice:end -->"


def main():
    slug = sys.argv[1]
    vj = os.path.join(VOICES, slug, "voice-design.json")
    prof = os.path.join(PROFILES, slug + ".md")
    if not os.path.exists(vj):
        print("no voice-design.json for " + slug, file=sys.stderr)
        return 1
    if not os.path.exists(prof):
        print("no profile for " + slug, file=sys.stderr)
        return 1
    d = json.load(open(vj, encoding="utf-8"))
    previews = d.get("previews", [])
    if not previews:
        print("no previews for " + slug, file=sys.stderr)
        return 1
    idx = d.get("default", 0)
    if not (isinstance(idx, int) and 0 <= idx < len(previews)):
        idx = 0
    f = previews[idx]["file"]
    rel = "../voices/%s/%s" % (slug, f)
    block = ('%s\n_Voice (default sample):_\n\n'
             '<audio controls src="%s"></audio>\n\n'
             '[Play voice](%s)\n%s') % (START, rel, rel, END)

    text = open(prof, encoding="utf-8").read()
    text = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", text, flags=re.S)
    m = re.search(r'(?m)^!\[[^\]]*\]\(\.\./portraits/[^)]+\)\s*\n', text)
    if not m:
        print("no portrait line in " + slug + "; skipping", file=sys.stderr)
        return 1
    i = m.end()
    text = text[:i] + "\n" + block + "\n" + text[i:]
    with open(prof, "w", encoding="utf-8") as h:
        h.write(text)
    print("embedded voice (%s, default index %d) in %s" % (f, idx, slug))
    return 0


if __name__ == "__main__":
    sys.exit(main())
