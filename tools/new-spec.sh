#!/usr/bin/env bash
# new-spec.sh — Scaffold a new spec directory from the templates.
#
# Usage: tools/new-spec.sh <feature-slug>
#
# Creates docs/specs/<feature-slug>/ with spec.md, plan.md, state.json from
# templates. Refuses to overwrite an existing spec.

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <feature-slug>" >&2
    echo "feature-slug must be kebab-case, e.g. 'ontology-classifier-skill'" >&2
    exit 2
fi

SLUG="$1"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SPEC_DIR="$REPO_ROOT/docs/specs/$SLUG"
TEMPLATES="$REPO_ROOT/docs/_templates"

if [[ ! "$SLUG" =~ ^[a-z][a-z0-9-]*$ ]]; then
    echo "new-spec: slug must be kebab-case (lowercase, digits, hyphens), got '$SLUG'" >&2
    exit 1
fi

if [[ -d "$SPEC_DIR" ]]; then
    echo "new-spec: $SPEC_DIR already exists; refusing to overwrite" >&2
    exit 1
fi

if [[ ! -d "$TEMPLATES" ]]; then
    echo "new-spec: templates dir not found at $TEMPLATES" >&2
    exit 1
fi

mkdir -p "$SPEC_DIR" "$SPEC_DIR/notes"

cp "$TEMPLATES/spec.md" "$SPEC_DIR/spec.md"
cp "$TEMPLATES/plan.md" "$SPEC_DIR/plan.md"

# Substitute the slug into state.json
sed "s/<spec-slug>/$SLUG/g" "$TEMPLATES/state.json" > "$SPEC_DIR/state.json"

echo "Spec scaffolded at docs/specs/$SLUG/"
echo "  spec.md  — fill the contract"
echo "  plan.md  — fill the strategy"
echo "  state.json — session-scratch (gitignored)"
echo ""
echo "Next: complete spec.md, then plan.md, then dispatch adversarial-reviewer"
echo "against both before EXECUTE."
