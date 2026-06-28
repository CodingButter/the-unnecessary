#!/usr/bin/env python3
"""General-purpose Gemini call -- a cross-model second opinion for the workflows.

Sends an arbitrary TASK prompt plus one or more content files to a Gemini model and
prints the response (or writes it to --out). Standard library only. The API key is read
from GEMINI_API_KEY / GOOGLE_API_KEY (env or repo-root .env) and is NEVER printed.

Intended for REVIEW / AUDIT cross-checks (a second, different-company opinion alongside
Claude) -- NOT for drafting prose, where the authorial voice must stay single-model.
Runs on the Gemini quota, so it does NOT consume the Claude token budget.

Usage:
  python3 scripts/gemini.py --task "<reviewer mandate>" --file <chapter.md> [--file <ref.md> ...] \
      [--model gemini-3-pro-preview] [--out <file>] [--temp 0.4]
  python3 scripts/gemini.py --task-file <prompt.md> --file <chapter.md>

Good models on this key (use --model): gemini-3-pro-preview (deep reasoning / audits),
gemini-3.1-pro-preview (newest pro), gemini-pro-latest (stable alias), gemini-3.5-flash
(fast / cheap / high-volume, e.g. lay-readers).
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_HOST = "https://generativelanguage.googleapis.com"
DEFAULT_MODEL = "gemini-pro-latest"  # stable alias; pinned previews (e.g. gemini-3-pro-preview) get retired and 404


def load_key():
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        val = os.environ.get(name)
        if val:
            return val.strip()
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


def call_gemini(model, key, prompt, temp, max_tokens):
    url = API_HOST + "/v1beta/models/" + model + ":generateContent?key=" + key
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temp, "maxOutputTokens": max_tokens},
    }
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        try:
            msg = json.loads(detail).get("error", {}).get("message", detail)
        except Exception:
            msg = detail
        return None, "HTTP " + str(err.code) + ": " + msg[:600]
    except Exception as err:  # noqa: BLE001
        return None, str(err)[:600]
    cands = body.get("candidates")
    if not cands:
        return None, "no candidates: " + json.dumps(body)[:400]
    parts = cands[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts)
    if not text:
        return None, "empty text (finishReason=" + str(cands[0].get("finishReason")) + ")"
    return text, None


def main():
    ap = argparse.ArgumentParser(description="General Gemini cross-model call (review/audit).")
    ap.add_argument("--task", default=None, help="the reviewer mandate / prompt")
    ap.add_argument("--task-file", default=None, help="read the prompt from a file instead")
    ap.add_argument("--file", action="append", default=[], help="content file(s) to include; repeatable")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--temp", type=float, default=0.4)
    ap.add_argument("--max-tokens", type=int, default=20000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    key = load_key()
    if not key:
        print("ERROR: no GEMINI_API_KEY or GOOGLE_API_KEY in env or .env", file=sys.stderr)
        return 2
    task = args.task
    if not task and args.task_file and os.path.exists(args.task_file):
        with open(args.task_file, "r", encoding="utf-8") as handle:
            task = handle.read()
    if not task:
        print("ERROR: --task or --task-file is required", file=sys.stderr)
        return 2

    chunks = [task]
    for path in args.file:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as handle:
                chunks.append("\n\n===== FILE: " + path + " =====\n" + handle.read())
        else:
            print("WARN: file not found, skipping: " + path, file=sys.stderr)
    prompt = "".join(chunks)

    print("Gemini " + args.model + " (key hidden), prompt " + str(len(prompt)) + " chars...", file=sys.stderr)
    text, err = call_gemini(args.model, key, prompt, args.temp, args.max_tokens)
    if err:
        print("ERROR: " + err, file=sys.stderr)
        return 1
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text if text.endswith("\n") else text + "\n")
        print("Wrote " + args.out + " (" + str(len(text)) + " chars)", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
