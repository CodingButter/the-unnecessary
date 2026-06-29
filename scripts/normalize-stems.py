#!/usr/bin/env python3
"""Master/normalize pass for a live-narration SCENE -- cue-driven + scope-resolving.

A TOOL the live-narration director (an agent) uses; it does NOT mix. For the scene's
cue sheet it resolves every referenced asset (scene -> chapter -> book; first hit wins,
so a sound generated once at its broadest reuse scope is never duplicated) and writes
loudness-normalized + light-EQ + gently-compressed copies into the scene's local
norm dirs (voice_norm/, sfx_norm/, music_norm/). The mix then reads one consistent,
scene-local base.

Targets: voice -18 LUFS, sfx -20 LUFS, music/ambiance -22 LUFS.
Usage: python3 scripts/normalize-stems.py <scene>/cues.json
"""
import glob
import json
import os
import subprocess
import sys

VOICE = ("silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.1:start_duration=0.1:"
         "stop_periods=-1:stop_threshold=-55dB:stop_duration=0.6:stop_silence=0.35,"
         "highpass=f=80,equalizer=f=3000:t=q:w=1.6:g=2.5,"
         "acompressor=threshold=-20dB:ratio=3:attack=8:release=140,"
         "loudnorm=I=-18:TP=-1.5:LRA=11")
SFX = "loudnorm=I=-20:TP=-1.5:LRA=11"
BED = "loudnorm=I=-22:TP=-2:LRA=11"
CATS = ("sfx", "music", "ambiance")


def norm(src, dst, chain):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", chain, dst],
                       capture_output=True, text=True)
    return r.returncode == 0


def resolve(name, scopes):
    for d in scopes:
        for cat in CATS:
            p = os.path.join(d, cat, name + ".mp3")
            if os.path.exists(p):
                return p
    return None


def main():
    cuesheet = sys.argv[1]
    scene = os.path.dirname(os.path.abspath(cuesheet))
    chapter = os.path.dirname(scene)
    book = os.path.dirname(os.path.dirname(chapter))
    scopes = [scene, chapter, book]
    cs = json.load(open(cuesheet, encoding="utf-8"))
    n = 0

    for f in sorted(glob.glob(scene + "/voice/stem-*.wav")):
        if norm(f, scene + "/voice_norm/" + os.path.basename(f), VOICE):
            n += 1

    seen = set()
    for cue in cs["cues"]:
        if cue.get("type") == "sfx":
            name = cue["asset"]
            if name in seen:
                continue
            seen.add(name)
            src = resolve(name, scopes)
            if not src:
                print("MISSING sfx asset: " + name, file=sys.stderr)
                continue
            chain = BED if "/ambiance/" in src else SFX
            if norm(src, scene + "/sfx_norm/" + name + ".mp3", chain):
                n += 1

    # Flashback windows reference an `ear-ring` SFX asset directly (not through a cue), so the
    # cue loop above never sees it. Normalize it here too -- resolved scene->chapter->book like
    # any other asset -- so the mix can find it in sfx_norm/. A scene has flashbacks either via
    # the explicit `flashback_windows` field OR via cues the mixer derives windows from -- those
    # tagged `"flashback": true` or carrying `"filter": "flashback"`; scenes with neither skip.
    has_flashback = bool(cs.get("flashback_windows")) or \
        any(c.get("flashback") is True or c.get("filter") == "flashback" for c in cs.get("cues", []))
    if has_flashback and "ear-ring" not in seen:
        seen.add("ear-ring")
        src = resolve("ear-ring", scopes)
        if not src:
            print("MISSING flashback asset: ear-ring", file=sys.stderr)
        else:
            chain = BED if "/ambiance/" in src else SFX
            if norm(src, scene + "/sfx_norm/ear-ring.mp3", chain):
                n += 1

    mc = cs.get("music", {})
    beds = mc if isinstance(mc, list) else [mc]  # (b) list of timed beds, or (a) single object
    seen_music = set()
    for bed in beds:
        masset = bed.get("asset")
        if not masset or masset in seen_music:
            continue
        seen_music.add(masset)
        src = resolve(masset, scopes)
        if not src:
            print("MISSING music asset: " + masset, file=sys.stderr)
        elif norm(src, scene + "/music_norm/" + masset + ".mp3", BED):
            n += 1

    print("normalized %d files into scene-local norm dirs (resolved scene->chapter->book)" % n)


if __name__ == "__main__":
    sys.exit(main())
