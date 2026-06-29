#!/usr/bin/env python3
"""Design a character's VOICE samples (ElevenLabs Voice Design) and save them LOCALLY.

A derived-artifact tool -- the audio counterpart to portrait-from-profile.py. It is a
downstream RENDER of the character profile, never canon. It calls
POST /v1/text-to-voice/design with a voice DESCRIPTION + a short essence TEXT, and saves
the returned preview mp3s under docs/20-canon/characters/voices/<slug>/.

It NEVER calls /v1/text-to-voice (create): nothing is ever saved to the ElevenLabs voice
library. The samples live only on disk and are always rebuildable.

The voice description and the essence line are crafted UPSTREAM by the voice-designer
agent (which reads the profile, reveal-safely). This script is the API + local-save plumbing.

Usage:
  python3 scripts/voice-design.py <slug-or-profile.md> \
      --description "<voice qualities: age, gender, accent, timbre, pace, register>" \
      --text "<~150-200 char in-character essence line (100-1000 chars; ~10-12s)>" \
      [--model eleven_multilingual_ttv_v2|eleven_ttv_v3] [--loudness 0.5] [--format mp3_44100_128]

Key from ELEVENLABS_API_KEY / XI_API_KEY (env or repo-root .env), never printed.
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

API_HOST = "https://api.elevenlabs.io"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES_DIR = os.path.join(REPO, "docs", "20-canon", "characters", "voices")
DEFAULT_MODEL = "eleven_multilingual_ttv_v2"


def load_key():
    for name in ("ELEVENLABS_API_KEY", "XI_API_KEY", "ELEVEN_API_KEY"):
        val = os.environ.get(name)
        if val:
            return val.strip()
    env_path = os.path.join(REPO, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                for name in ("ELEVENLABS_API_KEY", "XI_API_KEY"):
                    if line.startswith(name + "="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def slug_of(s):
    base = os.path.basename(s)
    return base[:-3] if base.endswith(".md") else base


def design(key, model, desc, text, loudness, fmt):
    url = API_HOST + "/v1/text-to-voice/design?output_format=" + fmt
    body = {
        "voice_description": desc,
        "model_id": model,
        "text": text,
        "auto_generate_text": False,
        "loudness": loudness,
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail).get("detail", detail)
        except Exception:
            pass
        return None, "HTTP " + str(err.code) + ": " + str(detail)[:600]
    except Exception as err:  # noqa: BLE001
        return None, str(err)[:600]


def main():
    ap = argparse.ArgumentParser(description="Design + locally save a character's voice samples (never saved to ElevenLabs).")
    ap.add_argument("profile", help="profile .md path or character slug")
    ap.add_argument("--description", required=True, help="voice qualities crafted from the profile")
    ap.add_argument("--text", required=True, help="~150-200 char in-character essence line (100-1000 chars; ~10-12s)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--loudness", type=float, default=0.5)
    ap.add_argument("--format", default="mp3_44100_128")
    args = ap.parse_args()

    key = load_key()
    if not key:
        print("ERROR: no ELEVENLABS_API_KEY / XI_API_KEY in env or .env", file=sys.stderr)
        return 2
    n = len(args.text)
    if not (100 <= n <= 1000):
        print("ERROR: --text must be 100-1000 chars (got " + str(n) + ")", file=sys.stderr)
        return 2

    slug = slug_of(args.profile)
    out_dir = os.path.join(VOICES_DIR, slug)
    os.makedirs(out_dir, exist_ok=True)
    print("Designing voice for " + slug + " (" + args.model + ", " + str(n) + " chars, key hidden)...", file=sys.stderr)

    res, err = design(key, args.model, args.description, args.text, args.loudness, args.format)
    if err:
        print("ERROR: " + err, file=sys.stderr)
        return 1
    previews = res.get("previews") or []
    if not previews:
        print("ERROR: no previews returned: " + json.dumps(res)[:300], file=sys.stderr)
        return 1

    meta = {"slug": slug, "model": args.model, "description": args.description,
            "text": res.get("text", args.text), "previews": []}
    for i, p in enumerate(previews, 1):
        b64 = p.get("audio_base_64") or p.get("audioBase64") or ""
        if not b64:
            continue
        fn = slug + "-" + str(i) + ".mp3"
        with open(os.path.join(out_dir, fn), "wb") as handle:
            handle.write(base64.b64decode(b64))
        meta["previews"].append({"file": fn, "generated_voice_id": p.get("generated_voice_id"),
                                 "duration_secs": p.get("duration_secs"), "language": p.get("language")})
        print("  saved " + fn + " (" + str(p.get("duration_secs", "?")) + "s)", file=sys.stderr)

    with open(os.path.join(out_dir, "voice-design.json"), "w", encoding="utf-8") as handle:
        json.dump(meta, handle, indent=2)
    print("Wrote " + str(len(meta["previews"])) + " samples + voice-design.json to " + out_dir
          + "  (NOT saved to ElevenLabs)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
