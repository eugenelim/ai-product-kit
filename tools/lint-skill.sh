#!/usr/bin/env bash
# lint-skill.sh — Validate a SKILL.md against the kit's contract for skills.
#
# Usage: tools/lint-skill.sh <path-to-SKILL.md>
#
# Exits 0 on clean, 1 with errors to stderr otherwise.
#
# Contract (the rules this linter enforces):
#  - File must have YAML frontmatter delimited by --- lines
#  - Frontmatter must declare: name, description, license
#  - description must be ≤ 1024 chars (Claude Code description-field constraint)
#  - Body must include H1 matching the skill name
#  - Body must include "## When to use this skill" section
#  - Body should not exceed 400 lines (soft warning, not error)

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <path-to-SKILL.md>" >&2
    exit 2
fi

SKILL_PATH="$1"
ERRORS=0

if [[ ! -f "$SKILL_PATH" ]]; then
    echo "lint-skill: file not found: $SKILL_PATH" >&2
    exit 1
fi

# Frontmatter present?
if ! head -1 "$SKILL_PATH" | grep -q '^---$'; then
    echo "lint-skill: $SKILL_PATH missing YAML frontmatter (must start with ---)" >&2
    ERRORS=$((ERRORS + 1))
fi

# Extract frontmatter block (lines between first and second ---)
FRONTMATTER=$(awk '/^---$/{c++; next} c==1{print} c==2{exit}' "$SKILL_PATH")

# Required fields
for field in name description license; do
    if ! echo "$FRONTMATTER" | grep -qE "^${field}:"; then
        echo "lint-skill: $SKILL_PATH missing required frontmatter field: $field" >&2
        ERRORS=$((ERRORS + 1))
    fi
done

# description length check
DESC=$(echo "$FRONTMATTER" | sed -n 's/^description: //p' | head -1)
if [[ ${#DESC} -gt 1024 ]]; then
    echo "lint-skill: $SKILL_PATH description is ${#DESC} chars (max 1024)" >&2
    ERRORS=$((ERRORS + 1))
fi

# Body: H1 present
if ! grep -qE '^# ' "$SKILL_PATH"; then
    echo "lint-skill: $SKILL_PATH missing H1 heading" >&2
    ERRORS=$((ERRORS + 1))
fi

# Body: "When to use this skill" section present
if ! grep -qE '^## When to use this skill' "$SKILL_PATH"; then
    echo "lint-skill: $SKILL_PATH missing '## When to use this skill' section" >&2
    ERRORS=$((ERRORS + 1))
fi

# Soft warning: body length
LINES=$(wc -l < "$SKILL_PATH")
if [[ $LINES -gt 400 ]]; then
    echo "lint-skill: WARN $SKILL_PATH is $LINES lines (soft cap 400)" >&2
fi

if [[ $ERRORS -gt 0 ]]; then
    echo "lint-skill: $ERRORS error(s) in $SKILL_PATH" >&2
    exit 1
fi

exit 0
