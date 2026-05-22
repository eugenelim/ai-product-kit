#!/usr/bin/env bash
# lint-hook.sh — Validate a .claude/hooks/<slug>.md against the kit's contract for hook docs.
#
# Usage: tools/lint-hook.sh <path-to-hook-doc.md>
#
# Exits 0 on clean, 1 on lint errors (including file-not-found, matching the
# sibling lint-skill.sh / lint-agent.sh convention), 2 on usage error.
#
# Contract (the rules this linter enforces):
#  - H1 present and matches `^# .+ hook$` (non-empty slug; `.+` not `.*`)
#  - Body must include `## What it does` section
#  - Body must include `## Why this matters` section
#  - Body must include `## Configuration` section
#  - Body should not exceed 250 lines (soft warning, not error)

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <path-to-hook-doc.md>" >&2
    exit 2
fi

HOOK_PATH="$1"
ERRORS=0

if [[ ! -f "$HOOK_PATH" ]]; then
    echo "lint-hook: file not found: $HOOK_PATH" >&2
    exit 1
fi

# H1 check: must match `^# .+ hook$` (non-empty slug between `# ` and ` hook`).
if ! grep -qE '^# .+ hook$' "$HOOK_PATH"; then
    echo "lint-hook: $HOOK_PATH missing H1 matching '^# <slug> hook$'" >&2
    ERRORS=$((ERRORS + 1))
fi

# Required sections.
if ! grep -qE '^## What it does' "$HOOK_PATH"; then
    echo "lint-hook: $HOOK_PATH missing '## What it does' section" >&2
    ERRORS=$((ERRORS + 1))
fi

if ! grep -qE '^## Why this matters' "$HOOK_PATH"; then
    echo "lint-hook: $HOOK_PATH missing '## Why this matters' section" >&2
    ERRORS=$((ERRORS + 1))
fi

if ! grep -qE '^## Configuration' "$HOOK_PATH"; then
    echo "lint-hook: $HOOK_PATH missing '## Configuration' section" >&2
    ERRORS=$((ERRORS + 1))
fi

# Soft warning: body length.
LINES=$(wc -l < "$HOOK_PATH")
if [[ $LINES -gt 250 ]]; then
    echo "lint-hook: WARN $HOOK_PATH is $LINES lines (soft cap 250)" >&2
fi

if [[ $ERRORS -gt 0 ]]; then
    echo "lint-hook: $ERRORS error(s) in $HOOK_PATH" >&2
    exit 1
fi

exit 0
