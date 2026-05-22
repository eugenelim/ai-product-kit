#!/usr/bin/env python3
"""F2.3 — hook-ontology-type-check (warn-only PreToolUse hook).

Reads a PreToolUse JSON payload from stdin. If the target file_path matches a
path glob that the ontology associates with a specific object_type but the
frontmatter omits or mismatches that type, emit a one-line nudge to stderr.

Exit 0 in every branch. Never blocks.

Stdlib + scripts.lib.frontmatter only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Optional

# Allow `from scripts.lib.frontmatter import parse` when invoked as a script.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.lib.frontmatter import parse  # noqa: E402


# --- Path → implied type table ---------------------------------------------
# Order matters only where one pattern would shadow another; the patterns
# below are mutually exclusive.
PATH_TYPE_MAP: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^strategy/intents/[^/]+\.md$"), "Strategic Intent"),
    (re.compile(r"^discovery/trees/[^/]+\.md$"), "Opportunity Solution Tree"),
    (re.compile(r"^discovery/opportunities/[^/]+\.md$"), "Opportunity"),
    (re.compile(r"^validation/assumption-maps/[^/]+\.md$"), "Assumption Map"),
    (re.compile(r"^validation/experiments/[^/]+/experiment\.md$"), "Experiment"),
    (re.compile(r"^validation/learnings/[^/]+\.md$"), "Validation Learning Memo"),
    (re.compile(r"^delivery/visions/[^/]+\.md$"), "Vision"),
    (re.compile(r"^delivery/initiatives/[^/]+/README\.md$"), "Initiative"),
    (re.compile(r"^delivery/handoff-packets/[^/]+/README\.md$"), "Handoff Packet"),
    (re.compile(r"^delivery/landings/[^/]+\.md$"), "Landing Report"),
]


def imply_type(path: str) -> Optional[str]:
    """Return the implied object_type for a path, or None if no pattern matches.

    Strips a single trailing slash before matching; the original `path` is
    still emitted verbatim in the nudge.
    """
    candidate = path[:-1] if path.endswith("/") else path
    for pattern, implied in PATH_TYPE_MAP:
        if pattern.match(candidate):
            return implied
    return None


def _format_nudge(path: str, implied: str, declared: Optional[str]) -> str:
    if declared is None:
        detail = "object_type is missing"
    else:
        detail = f"frontmatter declares {declared}"
    return (
        f"ontology-type-check: {path} implies object_type: {implied} "
        f"but {detail}"
    )


# Sentinel: distinguishes "frontmatter unusable" (silent) from "frontmatter
# present but missing object_type" (nudge).
_UNUSABLE = object()


def _safe_parse(source: str):
    """Parse frontmatter.

    Returns:
      - dict (the frontmatter data) on success.
      - _UNUSABLE if no frontmatter or malformed (degrade silently).
    """
    try:
        fm = parse(source)
    except Exception:  # noqa: BLE001 — degrade silently
        return _UNUSABLE
    if fm is None:
        return _UNUSABLE
    if fm.parse_errors:
        return _UNUSABLE
    return fm.data


def _read_disk(path: str) -> Optional[str]:
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _resolve_post_edit_source(tool_name: str, tool_input: dict) -> Optional[str]:
    """Return the source text to parse for frontmatter.

    Write: tool_input["content"].
    Edit: body-only (no '---' in old_string) uses on-disk text; frontmatter-
      touching reconstructs by applying the replacement to the disk file.
    MultiEdit: same classification across the edit list; frontmatter-touching
      applies edits sequentially to the disk file.
    """
    file_path = tool_input.get("file_path", "")

    if tool_name == "Write":
        return tool_input.get("content", "")

    if tool_name in ("Edit", "MultiEdit"):
        edits = (
            [tool_input]
            if tool_name == "Edit"
            else (tool_input.get("edits", []) or [])
        )
        touches_fm = any("---" in (e.get("old_string", "") or "") for e in edits)
        current = _read_disk(file_path)
        if not touches_fm:
            return current
        if current is None:
            return None
        for e in edits:
            old = e.get("old_string", "")
            new = e.get("new_string", "")
            if old not in current:
                return None
            current = current.replace(old, new, 1)
        return current

    return None


def check(payload: dict) -> Optional[str]:
    """Core decision function. Returns nudge string or None."""
    tool_name = payload.get("tool_name", "")
    if tool_name not in ("Write", "Edit", "MultiEdit"):
        return None

    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "")
    if not file_path:
        return None

    implied = imply_type(file_path)
    if implied is None:
        return None

    source = _resolve_post_edit_source(tool_name, tool_input)
    if source is None:
        # Couldn't load source — be silent. Don't blame the user.
        return None

    data = _safe_parse(source)
    if data is _UNUSABLE:
        # No frontmatter or malformed — degrade silently. lint-frontmatter.py
        # is responsible for shape errors; this hook only nudges on the
        # specific object_type miss.
        return None

    declared = None
    if "object_type" in data and data["object_type"] is not None:
        declared = str(data["object_type"])

    if declared == implied:
        return None

    return _format_nudge(file_path, implied, declared)


def main() -> int:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        payload = json.loads(raw)
        nudge = check(payload)
        if nudge:
            print(nudge, file=sys.stderr)
    except Exception as e:  # noqa: BLE001 — never let this hook break a session
        print(f"ontology-type-check: internal error (ignored): {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
