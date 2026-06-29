#!/usr/bin/env python3
"""Stitch a chapter's per-scene live mixes into ONE continuous chapter file.

Concatenates <chapter>/scene-*/scene-live.mp3 in order (zero-padded slugs sort correctly),
inserts a short beat of silence between scenes, and applies a final loudness pass so scenes
that mixed to slightly different levels sit consistently across the whole chapter.

Output: <chapter>/<chapter-basename>.live.mp3

Usage: python3 scripts/stitch-chapter.py <chapter-dir> [--gap 2.0] [--lufs -18]
"""
import argparse
import glob
import os
import subprocess
import sys


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
    try:
        return float(r)
    except ValueError:
        return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter")
    ap.add_argument("--gap", type=float, default=2.0, help="silent beat between scenes (s)")
    ap.add_argument("--lufs", type=float, default=-18.0, help="final integrated loudness target")
    a = ap.parse_args()
    ch = os.path.abspath(a.chapter.rstrip("/"))
    scenes = sorted(glob.glob(ch + "/scene-*/scene-live.mp3"))
    if not scenes:
        print("no scene-*/scene-live.mp3 under " + ch, file=sys.stderr)
        return 1
    out = ch + "/" + os.path.basename(ch) + ".live.mp3"

    fc = []
    for i in range(len(scenes)):
        pad = "" if i == len(scenes) - 1 else ",apad=pad_dur=%.2f" % a.gap
        fc.append("[%d:a]aformat=sample_rates=44100:channel_layouts=stereo%s[s%d]" % (i, pad, i))
    labels = "".join("[s%d]" % i for i in range(len(scenes)))
    fc.append("%sconcat=n=%d:v=0:a=1,loudnorm=I=%.1f:TP=-1.5:LRA=11[out]"
              % (labels, len(scenes), a.lufs))

    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for s in scenes:
        cmd += ["-i", s]
    cmd += ["-filter_complex", ";".join(fc), "-map", "[out]", "-c:a", "libmp3lame", "-q:a", "2", out]

    print("stitching %d scenes (gap %.1fs, target %.1f LUFS):" % (len(scenes), a.gap, a.lufs))
    for s in scenes:
        print("  + %-52s %5.0fs" % (os.path.relpath(s, ch), dur(s)))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print("FFMPEG ERR:\n" + r.stderr[-1500:], file=sys.stderr)
        return 1
    print("DONE -> %s  (%.0fs)" % (out, dur(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
