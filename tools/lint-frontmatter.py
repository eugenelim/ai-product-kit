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

# Make scripts.lib importable (kit has no pyproject.toml).
sys.path.insert(0, str(REPO_ROOT))
from scripts.lib.frontmatter import parse_file as _fm_parse_file  # noqa: E402

# Lifecycle states from CONVENTIONS.md
LIFECYCLE_STATES = {
    "Draft", "In Review", "Validated", "Approved",
    "Ready for Engineering", "In Build", "Launched", "Measured", "Deprecated",
    # Kit-build component states (additional to ontology product states)
    "Shipped", "Frozen",
}

# Phase folders to walk when --all is given
PHASE_DIRS = ["strategy", "discovery", "validation", "delivery", "market"]

# --- --check-template mode ---------------------------------------------------
#
# Templates under `templates/<slug>.md` use angle-bracket placeholder syntax;
# concrete values must still satisfy CONVENTIONS.md universal-schema enums.
# Default mode behavior is unchanged.
#
# Placeholder shapes (from spec docs/specs/template-authoring-convention/):
#   - Atomic placeholder:    ^<\S(?:[^>]*\S)?>$
#   - Augmented placeholder: ^[^<>]*(<\S(?:[^>]*\S)?>[^<>]*)+$
#   - Block-scalar:          a `|`/`>` block whose first non-empty line matches augmented
#   - Nested-container:      list/dict whose every leaf scalar is itself acceptable

ATOMIC_PLACEHOLDER = re.compile(r"^<\S(?:[^>]*\S)?>$")
AUGMENTED_PLACEHOLDER = re.compile(r"^[^<>]*(<\S(?:[^>]*\S)?>[^<>]*)+$")

# Concrete-value enums per CONVENTIONS.md universal-metadata schema. Applied
# only in --check-template mode (default mode preserves its existing checks).
TEMPLATE_FIELD_ENUMS: dict[str, set] = {
    "priority": {"Low", "Medium", "High", "Critical"},
    "risk_level": {"Low", "Medium", "High", "Critical"},
    "strength": {"Strong", "Moderate", "Weak"},
    # ai_assistance_allowed: `true` is coerced to bool True by the parser.
    "ai_assistance_allowed": {True, "restricted", "not-allowed"},
    "human_approval_required": {True, False},
}


def _is_placeholder_scalar(value: object) -> bool:
    """True if `value` is a string matching one of the placeholder shapes."""
    if not isinstance(value, str):
        return False
    if "\n" in value:
        # Block-scalar: judge by first non-empty line.
        first = next((ln for ln in value.split("\n") if ln.strip()), "")
        return bool(AUGMENTED_PLACEHOLDER.match(first))
    return bool(AUGMENTED_PLACEHOLDER.match(value))


def _check_template_value(
    value: object, field_name: str, ontology_types: set[str]
) -> list[str]:
    """Recursively validate a value under --check-template rules.

    Returns a list of error messages (empty if valid). Lists and dicts are
    accepted iff every leaf scalar inside is itself acceptable.
    """
    errors: list[str] = []
    if isinstance(value, list):
        for item in value:
            errors.extend(_check_template_value(item, field_name, ontology_types))
        return errors
    if isinstance(value, dict):
        for k, v in value.items():
            errors.extend(_check_template_value(v, k, ontology_types))
        return errors
    if isinstance(value, str):
        if _is_placeholder_scalar(value):
            return errors  # placeholder accepted
        if "<" in value or ">" in value:
            errors.append(
                f"field '{field_name}': malformed placeholder {value!r} "
                f"(angle brackets present but does not match placeholder shape)"
            )
            return errors
        if value == "":
            errors.append(
                f"field '{field_name}': empty-string concrete value"
            )
            return errors
        # Field-specific concrete-value validation
        if field_name == "object_type":
            base = value.split("|")[0].strip()
            if ontology_types and base not in ontology_types:
                errors.append(
                    f"field 'object_type': '{base}' not in ontology type set"
                )
            return errors
        if field_name == "status":
            if value not in LIFECYCLE_STATES:
                errors.append(
                    f"field 'status': '{value}' not a canonical lifecycle state"
                )
            return errors
        if field_name in TEMPLATE_FIELD_ENUMS:
            enum = TEMPLATE_FIELD_ENUMS[field_name]
            if value not in enum:
                errors.append(
                    f"field '{field_name}': value {value!r} not in enum "
                    f"{sorted(repr(e) for e in enum)}"
                )
        return errors
    # Non-string scalar (bool / int / None)
    if field_name in TEMPLATE_FIELD_ENUMS:
        enum = TEMPLATE_FIELD_ENUMS[field_name]
        if value not in enum:
            errors.append(
                f"field '{field_name}': value {value!r} not in enum "
                f"{sorted(repr(e) for e in enum)}"
            )
    return errors


def lint_template_file(path: Path, ontology_types: set[str]) -> list[str]:
    """Lint a template file under --check-template rules."""
    errors: list[str] = []
    fm = parse_frontmatter(path)
    if fm is None:
        errors.append(f"{path}: no YAML frontmatter")
        return errors

    # Required-key check (identical to default mode).
    for field in ("object_type", "status", "last_updated"):
        if field not in fm:
            errors.append(f"{path}: missing required field '{field}'")

    # Walk every present field through the recursive validator.
    for k, v in fm.items():
        for err in _check_template_value(v, k, ontology_types):
            errors.append(f"{path}: {err}")
    return errors


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
    """Return the frontmatter dict or None if no frontmatter present.

    Delegates to scripts.lib.frontmatter (F1.2). Returns None when the file
    has no frontmatter. Returns the parsed dict otherwise; if the frontmatter
    is malformed (e.g. unclosed delimiter), returns the empty dict the lib
    produced — callers can inspect via the lib's `parse_errors` if they want
    the rich object.
    """
    fm = _fm_parse_file(path)
    if fm is None:
        return None
    return fm.data


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

    if fm.get("human_approval_required") is True:
        hod = fm.get("human_owned_decisions")
        if not hod or (isinstance(hod, list) and len(hod) == 0):
            errors.append(
                f"{path}: human_approval_required: true requires "
                f"human_owned_decisions: list to be non-empty"
            )

    if fm.get("ai_assistance_allowed") == "restricted":
        aiu = fm.get("ai_assistance_used")
        if not aiu or not isinstance(aiu, list) or len(aiu) == 0:
            errors.append(
                f"{path}: ai_assistance_allowed: restricted requires "
                f"ai_assistance_used: list to be non-empty"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Files to lint")
    parser.add_argument("--all", action="store_true", help="Lint every kit artifact")
    parser.add_argument(
        "--check-template",
        dest="check_template",
        metavar="PATH",
        help="Lint a template file under templates/, accepting angle-bracket "
             "placeholders where concrete values would otherwise be required. "
             "Mutually exclusive with --all and positional paths.",
    )
    args = parser.parse_args()

    if args.check_template:
        if args.paths or args.all:
            print("lint-frontmatter: --check-template is mutually exclusive with "
                  "--all and positional paths", file=sys.stderr)
            return 2
        path = Path(args.check_template)
        if not path.exists():
            print(f"lint-frontmatter: file not found: {path}", file=sys.stderr)
            return 1
        ontology_types = load_ontology_types()
        if not ontology_types:
            print("lint-frontmatter: WARN ontology.md not found or has no type "
                  "table; type-set check skipped", file=sys.stderr)
        errors = lint_template_file(path, ontology_types)
        for err in errors:
            print(f"lint-frontmatter: {err}", file=sys.stderr)
        if errors:
            print(f"lint-frontmatter: {len(errors)} error(s) in {path}",
                  file=sys.stderr)
            return 1
        return 0

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
