#!/usr/bin/env python3
"""Mix a live-narration SCENE into <scene>/scene-live.mp3 -- the STITCH tool.

Reads <scene>/cues.json + <scene>/stems.manifest.json + the scene-local normalized stems
(voice_norm/ sfx_norm/ music_norm/, produced by normalize-stems.py). Resolves FILTER
definitions scene -> chapter -> book (merging filters.json at each scope; scene-special
wins), sequences the timeline, applies each cue's filter + per-role atempo, places SFX,
lays the normalized music bed, and runs ffmpeg.

Flashback windows make a memory surface -- inside each window the present soundscape (every
MUSIC bed + every SFX input, never VOICE) is lowpassed and ducked with ~0.2s ramps, and an
`ear-ring` SFX asset (resolved scene->chapter->book, read from sfx_norm/) is overlaid as a
ringing tone across the span. Windows come from EITHER an explicit scene-level
"flashback_windows": [{"start": <sec>, "end": <sec>}, ...] field (an override), OR -- when
that field is absent -- are derived from the cue timeline: each contiguous run of in-window
voice cues becomes one window. A voice cue is in-window if it is tagged "flashback": true OR
carries filter:"flashback" -- so a clean-voiced narration cue can sit in the muffled/ringing
window (flashback:true, filter stays "none") without its own voice being treated. Most scenes
have neither, and the mix then behaves exactly as before.

It EXECUTES the cue sheet's decisions; the creative choices live in the cue sheet (authored
by an agent) and in the by-ear review that follows. Re-run after editing cues.json to
iterate by ear.

Usage: python3 scripts/mix-live-scene.py <scene>/cues.json
"""
import json
import os
import subprocess
import sys

PRE = "aresample=44100,aformat=channel_layouts=stereo"


def _nested_max(terms):
    """max() in ffmpeg's expr eval is binary, so fold a list into nested max(a,max(b,...))."""
    expr = terms[0]
    for term in terms[1:]:
        expr = "max(%s,%s)" % (expr, term)
    return expr


def in_flashback_window(cue):
    """True if a VOICE cue sits inside a derived flashback window. Window membership is
    decoupled from voice treatment: a cue counts as in-window if it is tagged
    `"flashback": true` OR it carries the `"filter": "flashback"` voice filter. That lets a
    clean-voiced narration cue be marked flashback:true (filter stays "none") so the present
    soundscape goes muffled/ringing around it while its own voice is left untreated."""
    return cue.get("flashback") is True or cue.get("filter") == "flashback"


def flashback_windows(cs):
    """Parse the optional scene-level `flashback_windows` -> list of (start, end) floats.
    Absent / malformed entries are dropped, so a scene without the field behaves as today."""
    out = []
    for w in (cs.get("flashback_windows") or []):
        try:
            s, e = float(w["start"]), float(w["end"])
        except (KeyError, TypeError, ValueError):
            continue
        if e > s:
            out.append((s, e))
    return out


def muffle_suffix(fbw):
    """Filter-chain suffix that muffles the PRESENT soundscape only inside the windows.

    asendcmd time-toggles a named lowpass (`lowpass@fb`, dry by default via mix=0) on at
    each window start and off at each end; `volume@fb` rides a per-frame (eval=frame) duck
    expression that ramps to ~x0.35 over ~0.2s at each edge and is 1.0 (clear) everywhere
    else. Appended only to MUSIC and SFX chains -- never to VOICE. Empty -> no-op (back-compat)."""
    if not fbw:
        return ""
    R, DEPTH = 0.2, 0.65
    cmds = ";".join("%.3f lowpass@fb mix 1;%.3f lowpass@fb mix 0" % (s, e) for s, e in fbw)
    traps = ["clip((t-%.3f)/%g,0,1)*clip((%.3f-t)/%g,0,1)" % (s, R, e, R) for s, e in fbw]
    duck = "1-%g*(%s)" % (DEPTH, _nested_max(traps))
    return ",asendcmd='%s',lowpass@fb=f=800:mix=0,volume@fb=volume='%s':eval=frame" % (cmds, duck)


def load_filters(scene, chapter, book, cs):
    """Merge filters book -> chapter -> scene (most-specific wins)."""
    merged = {"none": ""}
    for d in (book, chapter):
        p = os.path.join(d, "filters.json")
        if os.path.exists(p):
            try:
                merged.update({k: v for k, v in json.load(open(p)).items() if not k.startswith("_")})
            except Exception:
                pass
    merged.update(cs.get("filters", {}))
    return merged


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", p],
                       capture_output=True, text=True).stdout.strip()
    try:
        return float(r)
    except ValueError:
        return 0.5


def main():
    cuesheet = sys.argv[1]
    scene = os.path.dirname(os.path.abspath(cuesheet))
    chapter = os.path.dirname(scene)
    book = os.path.dirname(os.path.dirname(chapter))
    cs = json.load(open(cuesheet, encoding="utf-8"))
    man = {m["i"]: m for m in json.load(open(os.path.join(scene, "stems.manifest.json"), encoding="utf-8"))}
    filters = load_filters(scene, chapter, book, cs)
    tuning = cs.get("tuning", {})
    VDIR, SDIR, MDIR = scene + "/voice_norm", scene + "/sfx_norm", scene + "/music_norm"
    fbw_explicit = flashback_windows(cs)  # explicit scene-level field; overrides derivation below
    MUF = "\x00FBM\x00"  # sentinel written into SFX chains; swapped for the real muffle post-loop

    inputs, chains, labels, t, n = [], [], [], 0.0, 0
    flash_spans, run = [], None  # windows derived from contiguous filter=="flashback" voice cues
    for ci, cue in enumerate(cs["cues"]):
        typ = cue.get("type")
        t += cue.get("gap_before", 0.0)
        ms = int(t * 1000)
        if typ == "voice":
            m = man[ci]
            f = VDIR + "/" + m["file"]
            d = dur(f)  # probe the NORMALIZED (silence-trimmed) stem so the timeline matches
            filt = filters.get(cue.get("filter", "none"), "")
            tempo = tuning.get(cue.get("role"), {}).get("tempo", 1.0)
            parts = [PRE]
            if filt:
                parts.append(filt)
            if abs(tempo - 1.0) > 0.001:
                parts.append("atempo=%.3f" % tempo)
                d = d / tempo
            chains.append("[%d:a]%s,adelay=%d|%d[a%d]" % (n, ",".join(parts), ms, ms, n))
            labels.append("[a%d]" % n)
            inputs.append((f, []))
            n += 1
            cstart = t
            t += d
            if in_flashback_window(cue):           # extend / open the current derived window
                run = [cstart, t] if run is None else [run[0], t]
            elif run is not None:                  # a non-flashback voice cue closes the run
                flash_spans.append(tuple(run))
                run = None
        elif typ == "sfx":
            if run is not None:                    # any non-flashback cue closes the run
                flash_spans.append(tuple(run))
                run = None
            f = SDIR + "/" + cue["asset"] + ".mp3"
            d = dur(f)
            g = cue.get("gain", 0.5)
            chains.append("[%d:a]%s,volume=%s,adelay=%d|%d%s[a%d]" % (n, PRE, g, ms, ms, MUF, n))
            labels.append("[a%d]" % n)
            inputs.append((f, []))
            n += 1
            if cue["asset"] != "room-ambiance":
                t += d
    if run is not None:
        flash_spans.append(tuple(run))

    # Explicit field wins; otherwise use the windows derived from flashback-tagged voice cues.
    # Now that the windows are known, build the muffle and swap it into the SFX chains.
    fbw = fbw_explicit if fbw_explicit else flash_spans
    MUFFLE = muffle_suffix(fbw)
    chains = [c.replace(MUF, MUFFLE) for c in chains]

    total = t + 1.0
    mc = cs.get("music", {})
    if isinstance(mc, list):
        # (b) timed beds: each bed is its own input + chain, NOT looped. Placed at `start`
        # via adelay, trimmed to `dur` of the asset, at volume=gain, with afade IN at the
        # bed's start and afade OUT ending at the bed's end. Overlapping [start, start+dur]
        # windows crossfade through the abutting fades. All fold into the existing amix.
        for bed in mc:
            masset = bed["asset"]
            bg = bed.get("gain", 0.2)
            bstart = bed.get("start", 0.0)
            bdur = bed.get("dur")
            if bdur is None:
                bdur = max(0.0, total - bstart)
            bfi = bed.get("fade_in", 3)
            bfo = bed.get("fade_out", 4)
            bms = int(bstart * 1000)
            chains.append("[%d:a]%s,atrim=0:%.2f,volume=%s,afade=t=in:st=0:d=%s,"
                          "afade=t=out:st=%.2f:d=%s,adelay=%d|%d%s[mus%d]"
                          % (n, PRE, bdur, bg, bfi, max(0.0, bdur - bfo), bfo, bms, bms, MUFFLE, n))
            labels.append("[mus%d]" % n)
            inputs.append((MDIR + "/" + masset + ".mp3", []))
            n += 1
    else:
        # (a) single bed: looped to fill the whole scene (unchanged back-compat path).
        mg = mc.get("gain", 0.2)
        masset = mc.get("asset", "tension-bed")
        chains.append("[%d:a]%s,atrim=0:%.2f,volume=%s,afade=t=in:st=0:d=4,afade=t=out:st=%.2f:d=5%s[mus]"
                      % (n, PRE, total, mg, max(0.0, total - 5), MUFFLE))
        labels.append("[mus]")
        inputs.append((MDIR + "/" + masset + ".mp3", ["-stream_loop", "-1"]))
        n += 1

    # Flashback EAR-RING overlay: one extra mix input per window. Looped to fill, trimmed and
    # cross-faded to span [S,E], at a low gain, delayed to start at S. Added AFTER `total` is
    # fixed, so it is a pure overlay and does NOT advance the timeline.
    for s, e in fbw:
        wd = e - s
        sms = int(s * 1000)
        chains.append("[%d:a]%s,atrim=0:%.2f,volume=0.5,afade=t=in:st=0:d=0.2,"
                      "afade=t=out:st=%.2f:d=0.2,adelay=%d|%d[ring%d]"
                      % (n, PRE, wd, max(0.0, wd - 0.2), sms, sms, n))
        labels.append("[ring%d]" % n)
        inputs.append((SDIR + "/ear-ring.mp3", ["-stream_loop", "-1"]))
        n += 1

    fc = ";".join(chains) + ";" + "".join(labels) + \
        ("amix=inputs=%d:duration=longest:normalize=0,alimiter=limit=0.95[mix]" % len(labels))
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for p, opts in inputs:
        cmd += opts + ["-i", p]
    out = scene + "/scene-live.mp3"
    cmd += ["-filter_complex", fc, "-map", "[mix]", "-t", "%.2f" % total,
            "-c:a", "libmp3lame", "-q:a", "2", out]
    print("inputs=%d  timeline=%.1fs  filters=%d (resolved scene->chapter->book)  flashback_windows=%d"
          % (len(inputs), total, len(filters), len(fbw)))
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("FFMPEG ERR:\n" + r.stderr[-1500:] if r.returncode else "MIXED -> " + out)


if __name__ == "__main__":
    sys.exit(main())
