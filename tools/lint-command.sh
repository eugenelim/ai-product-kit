#!/usr/bin/env bash
# lint-command.sh — Validate a .claude/commands/*.md file against the kit's contract.
#
# Usage: tools/lint-command.sh <path-to-command.md>
#
# Contract:
#  - YAML frontmatter delimited by ---
#  - Required fields: description (argument-hint optional)
#  - description must be ≤ 1024 chars
#  - Body must include H1 matching the slash command name
#  - Body should declare "## When to run" or "## Procedure"

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <path-to-command.md>" >&2
    exit 2
fi

CMD_PATH="$1"
ERRORS=0

if [[ ! -f "$CMD_PATH" ]]; then
    echo "lint-command: file not found: $CMD_PATH" >&2
    exit 1
fi

if ! head -1 "$CMD_PATH" | grep -q '^---$'; then
    echo "lint-command: $CMD_PATH missing YAML frontmatter" >&2
    ERRORS=$((ERRORS + 1))
fi

FRONTMATTER=$(awk '/^---$/{c++; next} c==1{print} c==2{exit}' "$CMD_PATH")

if ! echo "$FRONTMATTER" | grep -qE "^description:"; then
    echo "lint-command: $CMD_PATH missing required field: description" >&2
    ERRORS=$((ERRORS + 1))
fi

DESC=$(echo "$FRONTMATTER" | sed -n 's/^description: //p' | head -1)
if [[ ${#DESC} -gt 1024 ]]; then
    echo "lint-command: $CMD_PATH description is ${#DESC} chars (max 1024)" >&2
    ERRORS=$((ERRORS + 1))
fi

if ! grep -qE '^# /' "$CMD_PATH"; then
    echo "lint-command: $CMD_PATH H1 should begin with '/' (the slash command name)" >&2
    ERRORS=$((ERRORS + 1))
fi

if ! grep -qE '^## (When to run|Procedure)' "$CMD_PATH"; then
    echo "lint-command: $CMD_PATH missing '## When to run' or '## Procedure' section" >&2
    ERRORS=$((ERRORS + 1))
fi

if [[ $ERRORS -gt 0 ]]; then
    echo "lint-command: $ERRORS error(s) in $CMD_PATH" >&2
    exit 1
fi

exit 0
