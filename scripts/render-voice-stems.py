#!/usr/bin/env python3
"""Render the VOICE stems for a live-narration cue sheet -- one wav per voice cue.

A TOOL the live-narration director (an agent) uses. It GENERATES per-line voice audio by
POSTing each {"type":"voice"} cue to the voice server's /api/generate. Filtering, SFX,
ducking, and the mix are downstream (normalize-stems.py + mix-live-scene.py).

Per-cue text uses the cue's 'tts' (pronunciation-corrected) if present, else 'text'. Tuning
per role comes from the cue sheet's "tuning" block (per-cue overrides win), else the built-in
defaults. NOTE: the narrator is intended to stay at the SET narration tuning, not a scene-
expressive one -- scenes tune CHARACTERS, not the narrator.

  --role ROLE re-renders ONLY that role's cues; other roles' stems are left untouched and
  their durations re-probed so the manifest stays complete (cheap re-rolls during iteration).

Usage:
  python3 scripts/render-voice-stems.py <cuesheet.json> [--role ROLE] --user U --password P
Creds: --user/--password, else VOICE_API_USER / VOICE_API_PASSWORD env.
"""
import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error

DEFAULT_API = "http://voice.codingbutter.com"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# role -> (server voice id, exaggeration, cfg_weight, temperature) -- defaults; cue sheet "tuning" overrides
# NOTE: the cue sheet "tuning" block can override the numbers but NOT the voice id, so every
# speaking role must be registered here. Unknown roles fall back to the narrator voice.
ROLE_TUNING = {
    "narration":   ("narrator", 0.40, 0.50, 0.65),  # original designed narrator (commercial; replaced Will_Wheaton clone)
    "notice":      ("narrator", 0.30, 0.55, 0.50),  # automated machine notice (processed via 'notice' filter)
    "eli":         ("eli_rook",     0.45, 0.50, 0.70),
    "eli_thought": ("eli_rook",     0.35, 0.55, 0.65),
    "lena":        ("lena_okafor",  0.50, 0.50, 0.72),
    "tomas":       ("tomas_herrera", 0.45, 0.50, 0.62),  # steady night nurse, calm/dry (ch2)
    "dorsey":      ("raymond_dorsey", 0.50, 0.50, 0.65),
    "marisol":     ("marisol_vega",   0.50, 0.50, 0.70),
    "mason":       ("mason_vance",     0.50, 0.50, 0.70),
    "elder":       ("elder_customer",  0.50, 0.50, 0.60),  # render-only generic elder customer (ch1 s3 stranger; not canon)
    "mentor":      ("mentor-past",     0.50, 0.50, 0.55),  # reveal-safe past mentor (flashback voice; unnamed, not canon)
    # ch2 s3 ward patients -- rendered by CLONING each character's canon voice-design sample
    # inline (see ROLE_SAMPLE); not saved as named server voices, so the id below is a label.
    "reyes":       ("hector_reyes",    0.50, 0.50, 0.60),
    "diallo":      ("aminata_diallo",  0.45, 0.50, 0.60),
    "dembele":     ("sekou_dembele",   0.45, 0.52, 0.58),
    "adeyemi":     ("bayo_adeyemi",    0.45, 0.52, 0.58),
}

# Roles rendered by cloning a character's LOCAL canon voice-design sample inline via
# /api/generate's sample_base64 (no saved/named server voice needed). The sample is the
# default preview from each character's voice-design.json -- their canon voice, nothing invented.
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _vsample(slug, fname):
    return os.path.join(_REPO, "docs", "20-canon", "characters", "voices", slug, fname)
ROLE_SAMPLE = {
    "reyes":   _vsample("reyes-hector", "reyes-hector-1.mp3"),
    "diallo":  _vsample("diallo-aminata", "diallo-aminata-1.mp3"),
    "dembele": _vsample("dembele-sekou", "dembele-sekou-1.mp3"),
    "adeyemi": _vsample("adeyemi-bayo", "adeyemi-bayo-1.mp3"),
}


def auth_header(user, pw):
    if not (user and pw):
        return {}
    tok = base64.b64encode(("%s:%s" % (user, pw)).encode("utf-8")).decode("ascii")
    return {"Authorization": "Basic " + tok}


def probe_dur(path):
    if not os.path.exists(path):
        return None
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True).stdout.strip()
    try:
        return float(r)
    except ValueError:
        return None


def generate(api, voice, text, exg, cfg, temp, auth, out_path, sample_path=None):
    url = api.rstrip("/") + "/api/generate"
    payload = {"text": text, "format": "wav", "normalize": True,
               "exaggeration": exg, "cfg_weight": cfg, "temperature": temp}
    if sample_path:
        # clone-from-sample: send the character's canon voice sample inline; no server voice id
        with open(sample_path, "rb") as fh:
            payload["sample_base64"] = base64.b64encode(fh.read()).decode("ascii")
        payload["sample_format"] = (os.path.splitext(sample_path)[1].lstrip(".").lower() or "mp3")
    else:
        payload["voice"] = voice
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "audio/wav", "User-Agent": UA}
    headers.update(auth)
    last = None
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, data=body, headers=headers)
            # Stream the FULL body to disk -- a single resp.read() intermittently returns a
            # truncated body (no error raised), so copy chunk-by-chunk until EOF, then verify
            # the result by DECODING it rather than trusting the byte count or the header.
            with urllib.request.urlopen(req, timeout=600) as resp:
                d = resp.headers.get("X-Duration-Seconds")
                with open(out_path, "wb") as h:
                    shutil.copyfileobj(resp, h)
            try:
                claimed = float(d) if d else None
            except (TypeError, ValueError):
                claimed = None
            decoded = probe_dur(out_path)
            if not decoded:
                last = "empty/undecodable audio"
            elif claimed is not None and decoded < 0.9 * claimed:
                # truncated download: header claims more audio than actually decoded
                last = "truncated: decoded %.2fs < claimed %.2fs" % (decoded, claimed)
            else:
                # store the DECODED duration, not the header (server pads/over-claims)
                return decoded, None
            if attempt < 3:
                time.sleep(2 * attempt)
                continue
            break
        except urllib.error.HTTPError as e:
            last = "HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:200])
            if 500 <= e.code < 600 and attempt < 3:
                time.sleep(2 * attempt)
                continue
            break
        except Exception as e:  # noqa: BLE001
            last = str(e)[:200]
            if attempt < 3:
                time.sleep(2 * attempt)
                continue
            break
    return None, last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cuesheet")
    ap.add_argument("--api", default=DEFAULT_API)
    ap.add_argument("--user", default=os.environ.get("VOICE_API_USER"))
    ap.add_argument("--password", default=os.environ.get("VOICE_API_PASSWORD"))
    ap.add_argument("--role", default=None, help="render ONLY this role's cues; preserve the rest")
    ap.add_argument("--only", default=None, help="comma-separated cue indices to render; preserve the rest")
    a = ap.parse_args()
    only_set = set(int(x) for x in a.only.split(",")) if a.only else None

    cs = json.load(open(a.cuesheet, encoding="utf-8"))
    scene_tuning = cs.get("tuning", {})
    base = os.path.dirname(os.path.abspath(a.cuesheet))
    vdir = os.path.join(base, "voice")
    os.makedirs(vdir, exist_ok=True)
    auth = auth_header(a.user, a.password)
    if not auth:
        print("WARN: no creds (--user/--password or env); /api/generate will 401", file=sys.stderr)

    manifest, ok, fail, skip = [], 0, 0, 0
    for idx, cue in enumerate(cs["cues"]):
        if cue.get("type") != "voice":
            manifest.append({"i": idx, "type": cue.get("type"), "asset": cue.get("asset"),
                             "gain": cue.get("gain"), "gap_before": cue.get("gap_before", 0.0)})
            continue
        role = cue["role"]
        bt = ROLE_TUNING.get(role, ROLE_TUNING["narration"])
        st = scene_tuning.get(role, {})
        voice = bt[0]
        exg = cue.get("exaggeration", st.get("exaggeration", bt[1]))
        cfg = cue.get("cfg_weight", st.get("cfg_weight", bt[2]))
        temp = cue.get("temperature", st.get("temperature", bt[3]))
        out = os.path.join(vdir, "stem-%03d-%s.wav" % (idx, role))
        entry = {"i": idx, "type": "voice", "role": role, "voice": voice,
                 "file": os.path.basename(out), "filter": cue.get("filter", "none"),
                 "gap_before": cue.get("gap_before", 0.3), "text": cue["text"]}
        if (a.role and role != a.role) or (only_set is not None and idx not in only_set):
            entry["dur"] = probe_dur(out)
            entry["err"] = None
            manifest.append(entry)
            skip += 1
            continue
        text = cue.get("tts") or cue["text"]
        sample_path = ROLE_SAMPLE.get(role)
        print("[%03d] %-11s %s ..." % (idx, role, text[:46].replace("\n", " ")), file=sys.stderr)
        dur, err = generate(a.api, voice, text, exg, cfg, temp, auth, out, sample_path)
        if err:
            print("      ERROR: %s" % err, file=sys.stderr)
            fail += 1
        else:
            ok += 1
        entry["dur"] = dur
        entry["err"] = err
        manifest.append(entry)

    json.dump(manifest, open(os.path.join(base, "stems.manifest.json"), "w", encoding="utf-8"), indent=2)
    print("DONE: %d rendered, %d preserved, %d failed -> %s" % (ok, skip, fail, vdir), file=sys.stderr)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
