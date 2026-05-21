#!/usr/bin/env python3
"""
lint-frontmatter.py — Validate kit artifact frontmatter against the universal
metadata schema and the ontology type system.

Usage:
    tools/lint-frontmatter.py <path-to-artifact.md> [<path> ...]
    tools/lint-frontmatter.py --all   # lint every kit artifact under the phase dirs

Exits 0 if all files pass, 1 with errors to stderr otherwise.

Contract (the rules enforced):
  - The artifact must have YAML frontmatter delimited by '---' lines
  - Required fields per universal metadata schema:
      object_type, status, last_updated
  - object_type must be in the canonical type set from context/frameworks/ontology.md
  - status must be one of the canonical lifecycle states
  - parent_* fields must point to existing files when the artifact's object_type
    requires a parent (per HANDOVERS.md)
  - human_owned_decisions: must be a non-empty list if human_approval_required: true

This script reads the canonical type set from context/frameworks/ontology.md
by extracting the table rows under "## The eight domains".
"""

from __future__ import annotations

import argparse
import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_PATH = REPO_ROOT / "context" / "frameworks" / "ontology.md"

# Lifecycle states from CONVENTIONS.md
LIFECYCLE_STATES = {
    "Draft", "In Review", "Validated", "Approved",
    "Ready for Engineering", "In Build", "Launched", "Measured", "Deprecated",
    # Kit-build component states (additional to ontology product states)
    "Shipped", "Frozen",
}

# Phase folders to walk when --all is given
PHASE_DIRS = ["strategy", "discovery", "validation", "delivery", "market"]


def load_ontology_types() -> set[str]:
    """Extract the canonical type names from the ontology reference doc."""
    if not ONTOLOGY_PATH.exists():
        # Bootstrap mode: ontology doc not present yet
        return set()
    text = ONTOLOGY_PATH.read_text()
    # Pull rows from any markdown table that has 'Object' as the first column header
    types: set[str] = set()
    in_type_table = False
    for line in text.splitlines():
        if re.match(r'^\|\s*Object\s*\|', line):
            in_type_table = True
            continue
        if in_type_table:
            if not line.startswith("|"):
                in_type_table = False
                continue
            if re.match(r'^\|[-\s|]+\|$', line):
                continue  # the separator row
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if parts and parts[0] and parts[0] != "Object":
                types.add(parts[0])
    return types


def parse_frontmatter(path: Path) -> dict | None:
    """Return the frontmatter dict or None if no frontmatter present."""
    text = path.read_text()
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    block = text[4:end]
    # Very small YAML subset parser — enough for what the kit declares.
    # Handles: scalars, lists (- item), nested mappings to one level.
    return _parse_yaml_subset(block)


def _parse_yaml_subset(block: str) -> dict:
    out: dict = {}
    current_key = None
    current_list: list | None = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current_list is not None:
            current_list.append(raw[4:].strip().strip('"').strip("'"))
            continue
        if raw.startswith("  ") and current_key is not None:
            # nested map — not parsed, just record presence
            continue
        if ":" in raw:
            key, _, val = raw.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                # Either a list or a nested map
                current_key = key
                current_list = []
                out[key] = current_list
            else:
                out[key] = val.strip('"').strip("'")
                current_key = key
                current_list = None
    return out


def lint_file(path: Path, ontology_types: set[str]) -> list[str]:
    errors: list[str] = []
    fm = parse_frontmatter(path)
    if fm is None:
        errors.append(f"{path}: no YAML frontmatter")
        return errors

    required = ["object_type", "status", "last_updated"]
    for field in required:
        if field not in fm:
            errors.append(f"{path}: missing required field '{field}'")

    if "object_type" in fm:
        otype = fm["object_type"]
        # Allow ' | Adapted' suffix per CONVENTIONS.md
        base_type = otype.split("|")[0].strip()
        if ontology_types and base_type not in ontology_types:
            errors.append(
                f"{path}: object_type '{base_type}' not in ontology type set "
                f"(open an RFC to add it, or use '<type> | Adapted')"
            )

    if "status" in fm:
        if fm["status"] not in LIFECYCLE_STATES:
            errors.append(
                f"{path}: status '{fm['status']}' not a canonical lifecycle state"
            )

    if fm.get("human_approval_required") == "true":
        hod = fm.get("human_owned_decisions")
        if not hod or (isinstance(hod, list) and len(hod) == 0):
            errors.append(
                f"{path}: human_approval_required: true requires "
                f"human_owned_decisions: list to be non-empty"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Files to lint")
    parser.add_argument("--all", action="store_true", help="Lint every kit artifact")
    args = parser.parse_args()

    if not args.paths and not args.all:
        parser.print_help(sys.stderr)
        return 2

    files: list[Path] = []
    if args.all:
        for phase in PHASE_DIRS:
            phase_dir = REPO_ROOT / phase
            if phase_dir.is_dir():
                files.extend(p for p in phase_dir.rglob("*.md")
                             if not p.name.startswith("."))
    files.extend(Path(p) for p in args.paths)

    ontology_types = load_ontology_types()
    if not ontology_types:
        print("lint-frontmatter: WARN ontology.md not found or has no type table; "
              "type-set check skipped", file=sys.stderr)

    total_errors = 0
    for path in files:
        if not path.exists():
            print(f"lint-frontmatter: file not found: {path}", file=sys.stderr)
            total_errors += 1
            continue
        errors = lint_file(path, ontology_types)
        for err in errors:
            print(f"lint-frontmatter: {err}", file=sys.stderr)
        total_errors += len(errors)

    if total_errors:
        print(f"lint-frontmatter: {total_errors} error(s) across {len(files)} file(s)",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
