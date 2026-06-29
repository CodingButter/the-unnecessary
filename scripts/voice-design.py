#!/usr/bin/env python3
"""Design a character's VOICE samples (ElevenLabs Voice Design) and save them LOCALLY.

A derived-artifact tool -- the audio counterpart to portrait-from-profile.py. It is a
downstream RENDER of the character profile, never canon. It calls
POST /v1/text-to-voice/design with a voice DESCRIPTION + a short essence TEXT, and saves
the returned preview mp3s under docs/20-canon/characters/voices/<slug>/, alongside a
voice-design.json that records the description, the text, each preview's
generated_voice_id + duration, and a "default" index (0-based) for the chosen sample.

It NEVER calls /v1/text-to-voice (create): nothing is ever saved to the ElevenLabs voice
library. The samples live only on disk and are always rebuildable.

The voice-design.json is the SEED + the choice: it holds everything needed to (a) regenerate
the design later for free with --regen (no agent / no token cost); (b) record which sample
is the default via --set-default N (no re-render); and (c) later promote a chosen preview to
a real ElevenLabs voice via create-from-preview using its generated_voice_id, if ever wanted.

Usage:
  # First time (the voice-designer agent crafts description + text):
  python3 scripts/voice-design.py <slug-or-profile.md> \
      --description "<voice qualities>" --text "<~150-200 char essence line (100-1000 chars; ~10-12s)>" \
      [--model eleven_multilingual_ttv_v2|eleven_ttv_v3] [--loudness 0.5] [--format mp3_44100_128]

  # Regenerate later for free, straight from the stored seed (no agent):
  python3 scripts/voice-design.py <slug> --regen

  # Record which sample you liked (0-based index), no re-render, no API call:
  python3 scripts/voice-design.py <slug> --set-default 2

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
DEFAULT_MODEL = "eleven_ttv_v3"  # v3: inline expression tags in the sample text for finer control; fall back to eleven_multilingual_ttv_v2 if unavailable


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


def load_seed(seed_path):
    if os.path.exists(seed_path):
        try:
            with open(seed_path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except Exception:
            return None
    return None


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
    ap.add_argument("--description", default=None, help="voice qualities crafted from the profile")
    ap.add_argument("--text", default=None, help="~150-200 char in-character essence line (100-1000 chars; ~10-12s)")
    ap.add_argument("--model", default=None)
    ap.add_argument("--loudness", type=float, default=0.5)
    ap.add_argument("--format", default="mp3_44100_128")
    ap.add_argument("--regen", action="store_true",
                    help="regenerate from the stored voice-design.json (no description/text, no agent cost)")
    ap.add_argument("--set-default", type=int, default=None, metavar="N",
                    help="record the default sample index (0-based) in voice-design.json; no re-render, no API call")
    args = ap.parse_args()

    slug = slug_of(args.profile)
    out_dir = os.path.join(VOICES_DIR, slug)
    seed_path = os.path.join(out_dir, "voice-design.json")
    prior = load_seed(seed_path)

    # Mode: just record the chosen default index. No re-render, no API.
    if args.set_default is not None:
        if not prior:
            print("ERROR: no voice-design.json at " + seed_path, file=sys.stderr)
            return 2
        npv = len(prior.get("previews", []))
        if not (0 <= args.set_default < npv):
            print("ERROR: --set-default must be 0.." + str(npv - 1) + " (got " + str(args.set_default) + ")", file=sys.stderr)
            return 2
        prior["default"] = args.set_default
        with open(seed_path, "w", encoding="utf-8") as handle:
            json.dump(prior, handle, indent=2)
        chosen = prior["previews"][args.set_default].get("file")
        print("default for " + slug + " set to index " + str(args.set_default) + " (" + str(chosen) + ")", file=sys.stderr)
        return 0

    key = load_key()
    if not key:
        print("ERROR: no ELEVENLABS_API_KEY / XI_API_KEY in env or .env", file=sys.stderr)
        return 2

    # Resolve the seed (description / text / model). --regen, or a bare call with an existing
    # voice-design.json, reads it back so a regeneration costs ZERO agent tokens.
    description, text, model = args.description, args.text, args.model
    if args.regen or (not description and not text):
        if prior:
            description = description or prior.get("description")
            text = text or prior.get("text")
            model = model or prior.get("model")
            print("Regenerating " + slug + " from its voice-design.json seed (no agent / no token cost).", file=sys.stderr)
        elif args.regen:
            print("ERROR: --regen but no seed at " + seed_path, file=sys.stderr)
            return 2
    model = model or DEFAULT_MODEL

    if not description or not text:
        print("ERROR: need --description and --text (or --regen with an existing voice-design.json)", file=sys.stderr)
        return 2
    n = len(text)
    if not (100 <= n <= 1000):
        print("ERROR: text must be 100-1000 chars (got " + str(n) + ")", file=sys.stderr)
        return 2

    os.makedirs(out_dir, exist_ok=True)
    print("Designing voice for " + slug + " (" + model + ", " + str(n) + " chars, key hidden)...", file=sys.stderr)

    res, err = design(key, model, description, text, args.loudness, args.format)
    if err:
        print("ERROR: " + err, file=sys.stderr)
        return 1
    previews = res.get("previews") or []
    if not previews:
        print("ERROR: no previews returned: " + json.dumps(res)[:300], file=sys.stderr)
        return 1

    # Preserve a prior default index across a regen if it still points at a real sample; else 0.
    prior_default = (prior or {}).get("default", 0)
    default_idx = prior_default if isinstance(prior_default, int) and 0 <= prior_default < len(previews) else 0

    meta = {"slug": slug, "model": model, "description": description,
            "text": res.get("text", text), "default": default_idx, "previews": []}
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

    with open(seed_path, "w", encoding="utf-8") as handle:
        json.dump(meta, handle, indent=2)
    print("Wrote " + str(len(meta["previews"])) + " samples + voice-design.json (default index "
          + str(default_idx) + ") to " + out_dir + "  (NOT saved to ElevenLabs; --regen rebuilds from this seed)",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
