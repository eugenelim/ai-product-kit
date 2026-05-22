#!/usr/bin/env bash
# pre-pr.sh — Aggregate enforcement hook. Runs every linter and reports.
#
# Usage: tools/pre-pr.sh [<file> ...]
#
# When given file paths (typically by a pre-commit hook), lints only those.
# When given no arguments, lints everything under the kit's artifact paths.
#
# Exits 0 on clean, non-zero on the first failure category.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

FAILED=0

run_linter() {
    local label="$1"
    shift
    if "$@"; then
        echo "✓ $label"
    else
        echo "✗ $label" >&2
        FAILED=$((FAILED + 1))
    fi
}

echo "== pre-pr: kit enforcement =="

# Skills
for skill in .claude/skills/*/SKILL.md; do
    [[ -f "$skill" ]] || continue
    run_linter "lint-skill $skill" tools/lint-skill.sh "$skill"
done

# Agents
for agent in .claude/agents/*.md; do
    [[ -f "$agent" ]] || continue
    [[ "$(basename "$agent")" == "README.md" ]] && continue
    run_linter "lint-agent $agent" tools/lint-agent.sh "$agent"
done

# Commands
for cmd in .claude/commands/*.md; do
    [[ -f "$cmd" ]] || continue
    run_linter "lint-command $cmd" tools/lint-command.sh "$cmd"
done

# Hooks
for hook in .claude/hooks/*.md; do
    [[ -f "$hook" ]] || continue
    [[ "$(basename "$hook")" == "README.md" ]] && continue
    run_linter "lint-hook $hook" tools/lint-hook.sh "$hook"
done

# Frontmatter (sample: phase folder artifacts only, when present)
if [[ -d strategy ]] || [[ -d discovery ]] || [[ -d validation ]] || [[ -d delivery ]]; then
    # Only run --all when there's at least one phase artifact to lint, to avoid
    # noise in a freshly-initialized kit.
    artifact_count=$(find strategy discovery validation delivery -name '*.md' 2>/dev/null | wc -l)
    if [[ $artifact_count -gt 0 ]]; then
        run_linter "lint-frontmatter --all" python3 tools/lint-frontmatter.py --all
    fi
fi

if [[ $FAILED -gt 0 ]]; then
    echo "" >&2
    echo "pre-pr: $FAILED linter(s) failed" >&2
    exit 1
fi

echo "== pre-pr: all green =="
exit 0
