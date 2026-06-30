#!/usr/bin/env bash
#
# install.sh -- one-time wiring of the tracked git hooks for The Unnecessary.
#
# Points git at scripts/hooks/ (this tracked directory) instead of the untracked
# .git/hooks/, so the canon pre-push gate (spec section 10) travels with the clone.
# Idempotent: safe to re-run. Run it once per fresh clone:
#
#     bash scripts/hooks/install.sh
#
# It does exactly one thing -- the equivalent of:
#
#     git config core.hooksPath scripts/hooks
#
set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "${REPO_ROOT}" ]; then
    echo "install: not inside a git work tree. Run from within the repo." >&2
    exit 1
fi
cd "${REPO_ROOT}" || exit 1

git config core.hooksPath scripts/hooks
chmod +x scripts/hooks/pre-push 2>/dev/null || true

echo "install: core.hooksPath -> $(git config --get core.hooksPath)"
echo "install: canon pre-push gate is now active for this clone."
