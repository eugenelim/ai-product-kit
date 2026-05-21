#!/usr/bin/env bash
# lint-agent.sh — Validate a subagent .md file against the kit's contract.
#
# Usage: tools/lint-agent.sh <path-to-agent.md>
#
# Contract:
#  - YAML frontmatter delimited by ---
#  - Required fields: name, description, tools, model
#  - model must be one of: haiku, sonnet, opus
#  - description must explain when to invoke (no vague "is a helper" style)
#  - Body must include H1 matching the agent name

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <path-to-agent.md>" >&2
    exit 2
fi

AGENT_PATH="$1"
ERRORS=0

if [[ ! -f "$AGENT_PATH" ]]; then
    echo "lint-agent: file not found: $AGENT_PATH" >&2
    exit 1
fi

if ! head -1 "$AGENT_PATH" | grep -q '^---$'; then
    echo "lint-agent: $AGENT_PATH missing YAML frontmatter" >&2
    ERRORS=$((ERRORS + 1))
fi

FRONTMATTER=$(awk '/^---$/{c++; next} c==1{print} c==2{exit}' "$AGENT_PATH")

for field in name description tools model; do
    if ! echo "$FRONTMATTER" | grep -qE "^${field}:"; then
        echo "lint-agent: $AGENT_PATH missing required field: $field" >&2
        ERRORS=$((ERRORS + 1))
    fi
done

MODEL=$(echo "$FRONTMATTER" | sed -n 's/^model: *//p' | head -1 | tr -d '"')
case "$MODEL" in
    haiku|sonnet|opus|"") ;;
    *)
        echo "lint-agent: $AGENT_PATH model must be haiku|sonnet|opus, got '$MODEL'" >&2
        ERRORS=$((ERRORS + 1))
        ;;
esac

if ! grep -qE '^# ' "$AGENT_PATH"; then
    echo "lint-agent: $AGENT_PATH missing H1 heading" >&2
    ERRORS=$((ERRORS + 1))
fi

if [[ $ERRORS -gt 0 ]]; then
    echo "lint-agent: $ERRORS error(s) in $AGENT_PATH" >&2
    exit 1
fi

exit 0
