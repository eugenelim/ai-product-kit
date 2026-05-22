#!/usr/bin/env python3
"""check-handover-link — PreToolUse hook script (F2.1).

Reads a PreToolUse JSON payload from stdin and decides whether a proposed
Write|Edit|MultiEdit on a kit artifact is permitted under the kit's seven
canonical handover contracts (docs/HANDOVERS.md).

- Exit 0: allowed (possibly with a stderr warning for a dangling parent
  target or for an uppercase phase-root path).
- Exit 2: blocked. Stdout carries `{"decision":"block","reason":...}`.
- Any uncaught error degrades to exit 0 + stderr — the hook never bricks a
  session.

Dependencies: Python stdlib only + `scripts.lib.frontmatter`.
"""

from __future__ import annotations

import json
import os
import re
import sys
import traceback
from pathlib import Path

# Make `scripts.lib.frontmatter` importable when this file is executed directly.
_THIS = Path(__file__).resolve()
_REPO_ROOT_DEFAULT = _THIS.parent.parent
if str(_REPO_ROOT_DEFAULT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT_DEFAULT))

from scripts.lib.frontmatter import parse  # noqa: E402


# --- The load-bearing table -------------------------------------------------
# Source of truth: docs/HANDOVERS.md (handovers 1–7). Each rule: anchored
# regex against the repo-relative POSIX path, required parent_* field(s),
# handover number, human label.
HANDOVER_RULES = [
    {"glob": re.compile(r"^strategy/intents/[^/]+\.md$"),
     "required": [], "handover": 1, "label": "Strategic Intent"},
    {"glob": re.compile(r"^discovery/trees/[^/]+\.md$"),
     "required": ["parent_intent"], "handover": 2, "label": "OST"},
    {"glob": re.compile(r"^validation/learnings/[^/]+\.md$"),
     "required": ["parent_opportunity"], "handover": 3,
     "label": "Validation Learning Memo"},
    {"glob": re.compile(r"^delivery/visions/[^/]+\.md$"),
     "required": ["parent_learning", "parent_intent"], "handover": 4,
     "label": "Vision"},
    {"glob": re.compile(r"^delivery/initiatives/[^/]+/README\.md$"),
     "required": ["parent_vision"], "handover": 5, "label": "Initiative"},
    {"glob": re.compile(r"^delivery/handoff-packets/[^/]+/README\.md$"),
     "required": ["parent_initiative"], "handover": 6, "label": "Handoff Packet"},
    {"glob": re.compile(r"^delivery/landings/[^/]+\.md$"),
     "required": ["parent_vision", "parent_handoff_packet"], "handover": 7,
     "label": "Landing Report"},
]

# Per-field parent target resolver (from the fourth column of the spec's
# path table). initiative/handoff-packet → README.md; others → flat .md.
PARENT_RESOLVERS = {
    "parent_intent": lambda s: f"strategy/intents/{s}.md",
    "parent_opportunity": lambda s: f"discovery/opportunities/{s}.md",
    "parent_learning": lambda s: f"validation/learnings/{s}.md",
    "parent_vision": lambda s: f"delivery/visions/{s}.md",
    "parent_initiative": lambda s: f"delivery/initiatives/{s}/README.md",
    "parent_handoff_packet": lambda s: f"delivery/handoff-packets/{s}/README.md",
}

_PHASE_ROOT_RE = re.compile(r"^(strategy|discovery|validation|delivery)/", re.IGNORECASE)


def _relpath(file_path: str, repo_root: Path) -> str:
    """POSIX-style repo-relative path; fall back to input if outside repo."""
    p = Path(file_path)
    try:
        return p.resolve().relative_to(repo_root.resolve()).as_posix()
    except (ValueError, OSError):
        return file_path.replace(os.sep, "/")


def match_rule(rel_path: str):
    """Return the matching HANDOVER_RULES entry or None."""
    for rule in HANDOVER_RULES:
        if rule["glob"].match(rel_path):
            return rule
    return None


def reconstruct_frontmatter(payload_tool_input: dict, on_disk_text: str) -> str:
    """For Edit/MultiEdit: return the text whose frontmatter we validate.

    - Frontmatter-touching = any edit's `old_string` contains `---`. Apply
      all edits in order to the on-disk text.
    - Body-only = no `---` in any `old_string` → return on-disk text unchanged
      (the edit is not changing parent_* fields; disk is authoritative).
    """
    if "edits" in payload_tool_input:
        edits = payload_tool_input.get("edits") or []
    elif "old_string" in payload_tool_input:
        edits = [{
            "old_string": payload_tool_input.get("old_string", ""),
            "new_string": payload_tool_input.get("new_string", ""),
        }]
    else:
        edits = []

    if not any("---" in (e.get("old_string") or "") for e in edits):
        return on_disk_text

    text = on_disk_text
    for e in edits:
        old = e.get("old_string") or ""
        if old:
            text = text.replace(old, e.get("new_string") or "", 1)
    return text


def _read_on_disk(file_path: str) -> str:
    try:
        return Path(file_path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _override_state(data: dict):
    """Return (active, block_reason_if_partial).

    Active iff `override_handover_link is True` (strict) AND all three
    companion fields are non-empty strings. If the flag is True but a
    companion is missing/empty, returns (False, reason) so the caller blocks.
    """
    if data.get("override_handover_link") is not True:
        return False, None
    missing = []
    for name in ("override_reason", "override_authorized_by", "override_authorized_at"):
        val = data.get(name)
        if not isinstance(val, str) or not val.strip():
            missing.append(name)
    if missing:
        return False, (
            "override_handover_link is true but missing/empty: "
            + ", ".join(missing)
        )
    return True, None


def _append_override_log(repo_root: Path, rel_path: str, data: dict) -> None:
    """Append a one-line entry to delivery/HANDOVER-OVERRIDE-LOG.md (best-effort)."""
    log_path = repo_root / "delivery" / "HANDOVER-OVERRIDE-LOG.md"
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        new_file = not log_path.exists()
        with log_path.open("a", encoding="utf-8") as f:
            if new_file:
                f.write(
                    "# Handover-link override log\n\n"
                    "One line per override accepted by the "
                    "`check-handover-link` hook. If this list grows, the kit "
                    "is silently phase-skipping.\n\n"
                )
            f.write(
                "- {d} | {p} | by={w} | reason={r}\n".format(
                    d=data.get("override_authorized_at", ""), p=rel_path,
                    w=data.get("override_authorized_by", ""),
                    r=data.get("override_reason", ""),
                )
            )
    except OSError:
        pass


def _has_value(data: dict, field: str) -> bool:
    val = data.get(field)
    if val is None:
        return False
    if isinstance(val, str):
        return val.strip() != ""
    return True


def check(payload: dict, repo_root: Path | None = None):
    """Apply the handover-link rule.

    Returns (exit_code, stdout_json_or_None, stderr_msg_or_None).
    """
    repo_root = Path(repo_root or _REPO_ROOT_DEFAULT)
    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path")
    if not file_path:
        return 0, None, None

    rel_path = _relpath(file_path, repo_root)
    rule = match_rule(rel_path)
    if rule is None:
        # Soft nudge for uppercase paths under a phase root.
        if rel_path != rel_path.lower() and _PHASE_ROOT_RE.match(rel_path):
            return (
                0, None,
                f"check-handover-link: ontology-naming-convention: "
                f"uppercase path under a phase root: {rel_path}",
            )
        return 0, None, None

    # Determine the text whose frontmatter we validate.
    if tool_name == "Write":
        text = tool_input.get("content") or ""
    elif tool_name in ("Edit", "MultiEdit"):
        text = reconstruct_frontmatter(tool_input, _read_on_disk(file_path))
    else:
        return 0, None, None

    fm = parse(text)
    if fm is None or fm.parse_errors:
        return (
            0, None,
            f"check-handover-link: could not parse frontmatter for "
            f"{rel_path}; skipping required-field check",
        )
    data = fm.data or {}

    # Override path first.
    active, override_block = _override_state(data)
    if override_block is not None:
        return 2, json.dumps({"decision": "block", "reason": override_block}), None
    if active:
        _append_override_log(repo_root, rel_path, data)
        return 0, None, None

    # Required-fields check.
    missing = [f for f in rule["required"] if not _has_value(data, f)]
    if missing:
        reason = (
            f"{rule['label']} at {rel_path} is missing required parent "
            f"field(s): {', '.join(missing)} "
            f"(Handover {rule['handover']} per docs/HANDOVERS.md)"
        )
        return 2, json.dumps({"decision": "block", "reason": reason}), None

    # Dangling-link warnings (allow + stderr).
    warnings = []
    for field_name in rule["required"]:
        slug = data.get(field_name)
        if not isinstance(slug, str) or not slug.strip():
            continue
        resolver = PARENT_RESOLVERS.get(field_name)
        if resolver is None:
            continue
        target = repo_root / resolver(slug.strip())
        if not target.exists():
            try:
                disp = target.relative_to(repo_root)
            except ValueError:
                disp = target
            warnings.append(f"{field_name}: {slug} → expected {disp} (not found)")
    if warnings:
        return (
            0, None,
            "check-handover-link: dangling parent link(s) for "
            + rel_path + "; " + "; ".join(warnings),
        )
    return 0, None, None


def main() -> int:
    """stdin → JSON payload → check() → stdout/stderr/exit-code."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        payload = json.loads(raw)
        env_root = os.environ.get("KIT_REPO_ROOT")
        repo_root = Path(env_root) if env_root else _REPO_ROOT_DEFAULT
        code, out, err = check(payload, repo_root=repo_root)
        if out:
            sys.stdout.write(out + ("" if out.endswith("\n") else "\n"))
        if err:
            sys.stderr.write(err + ("" if err.endswith("\n") else "\n"))
        return code
    except Exception:  # noqa: BLE001 — top-level safety net
        sys.stderr.write("check-handover-link: internal error; degraded to allow\n")
        sys.stderr.write(traceback.format_exc())
        return 0


if __name__ == "__main__":
    sys.exit(main())
