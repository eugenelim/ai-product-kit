#!/usr/bin/env python3
"""mode-guard.py — Three-event hook enforcing kit greenfield/enterprise mode.

Reads `mode:` from `.claude/CLAUDE.md` and:
- SessionStart: injects a one-block reminder via hookSpecificOutput.additionalContext.
- UserPromptExpansion (user typed `/wardley-map`): blocks via exit 0 + decision JSON.
- PreToolUse on Skill (model invoked Skill tool): blocks via exit 2 + decision JSON.

Stdlib only. See docs/specs/hook-mode-guard/spec.md for the full contract.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple

# Mode → blocked-commands map (single source of truth — see spec § Inputs and outputs).
BLOCKED_BY_MODE = {
    "greenfield": ["wardley-map", "internal-jtbd-interview", "value-chain-evolution"],
    "enterprise": ["competitive-research", "market-scan", "jtbd-analogues"],
}
# `phase-guide` listed explicitly though the implicit "not in BLOCKED is allowed" rule
# already permits it — defensive against accidental list inclusion.
SHARED = {"strategy-refresh", "strategic-intent", "audit-portfolio-coherence",
          "cadence-check", "phase-guide"}

_MODE_RE = re.compile(r'^mode:\s*(greenfield|enterprise)\s*$', re.MULTILINE)


def read_mode(claudemd_path: Path) -> Optional[str]:
    """Return 'greenfield' or 'enterprise' if declared; None otherwise.

    Strict-anchor regex — only the two known values match. `enterprise-lite` returns None.
    """
    try:
        text = claudemd_path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return None
    match = _MODE_RE.search(text)
    if match is None:
        return None
    return match.group(1).strip()


def find_repo_root() -> Optional[Path]:
    """Ascend __file__'s parent chain until `.claude/` found, or use CLAUDE_WORKSPACE env var."""
    env_root = os.environ.get("CLAUDE_WORKSPACE")
    if env_root:
        candidate = Path(env_root)
        if (candidate / ".claude").is_dir():
            return candidate
    here = Path(__file__).resolve().parent
    for parent in [here, *here.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return None


def _other_mode(mode: str) -> str:
    return "enterprise" if mode == "greenfield" else "greenfield"


def _suggested_allowed(mode: str) -> str:
    """Suggest the opposite-mode counterpart command from the other blocked list."""
    other = _other_mode(mode)
    return BLOCKED_BY_MODE[other][0]


def _block_reason(cmd: str, mode: str) -> str:
    return (
        f"mode-guard: /{cmd} is blocked in {mode} mode. "
        f"Use /{_suggested_allowed(mode)} instead, or change mode: to "
        f"{_other_mode(mode)} in .claude/CLAUDE.md."
    )


def session_start(mode: Optional[str]) -> Tuple[int, str, str]:
    """Return (exit_code, stdout_json, stderr) for SessionStart event."""
    if mode is None:
        return (0, "", "mode-guard: mode undeclared in .claude/CLAUDE.md — enforcement inactive\n")
    blocked = ", ".join(f"/{c}" for c in BLOCKED_BY_MODE[mode])
    context = (
        f"Active kit mode: {mode}.\n"
        f"Blocked slash commands in this mode: {blocked}.\n"
        f"Shared (never blocked): /strategy-refresh, /strategic-intent, "
        f"/audit-portfolio-coherence, /cadence-check, /phase-guide.\n"
        f"Switch mode by editing the `mode:` line in .claude/CLAUDE.md."
    )
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }
    return (0, json.dumps(payload), "")


def handle_upe(mode: Optional[str], payload: dict) -> Tuple[int, str, str]:
    """UserPromptExpansion path (user-typed slash command).

    Block protocol: exit 0 + stdout {"decision":"block","reason":...,"hookSpecificOutput":...}.
    """
    cmd = payload.get("command_name", "")
    if mode is None:
        return (0, "", "mode-guard: mode undeclared in .claude/CLAUDE.md — enforcement inactive\n")
    if cmd in SHARED:
        return (0, "", "")
    if cmd in BLOCKED_BY_MODE.get(mode, []):
        reason = _block_reason(cmd, mode)
        out = {
            "decision": "block",
            "reason": reason,
            "hookSpecificOutput": {"hookEventName": "UserPromptExpansion"},
        }
        return (0, json.dumps(out), "")
    return (0, "", "")


def handle_pretooluse_skill(mode: Optional[str], payload: dict) -> Tuple[int, str, str]:
    """PreToolUse on Skill path (model-invoked Skill tool).

    Block protocol: exit 2 + stdout {"decision":"block","reason":...}.
    Non-Skill tool: exit 0 silently (defensive — matcher should filter at harness level).
    """
    if payload.get("tool_name") != "Skill":
        return (0, "", "")
    tool_input = payload.get("tool_input") or {}
    cmd = tool_input.get("skill_name", "")
    if mode is None:
        return (0, "", "mode-guard: mode undeclared in .claude/CLAUDE.md — enforcement inactive\n")
    if cmd in SHARED:
        return (0, "", "")
    if cmd in BLOCKED_BY_MODE.get(mode, []):
        reason = _block_reason(cmd, mode)
        out = {"decision": "block", "reason": reason}
        return (2, json.dumps(out), "")
    return (0, "", "")


def dispatch(payload: dict, claudemd_path: Path) -> Tuple[int, str, str]:
    """Dispatch by event. Unknown events exit 0 silently."""
    event = payload.get("hook_event_name")
    if event == "UserPromptExpansion":
        return handle_upe(read_mode(claudemd_path), payload)
    if event == "SessionStart":
        return session_start(read_mode(claudemd_path))
    if payload.get("tool_name") == "Skill":
        return handle_pretooluse_skill(read_mode(claudemd_path), payload)
    return (0, "", "")


def main() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        sys.stderr.write("mode-guard: invalid JSON on stdin\n")
        return 0
    try:
        root = find_repo_root()
        if root is None:
            sys.stderr.write("mode-guard: could not locate repo root (.claude/ ancestor)\n")
            return 0
        claudemd = root / ".claude" / "CLAUDE.md"
        exit_code, stdout, stderr = dispatch(payload, claudemd)
        if stdout:
            sys.stdout.write(stdout)
        if stderr:
            sys.stderr.write(stderr)
        return exit_code
    except Exception as exc:  # degrade safely — never block on unhandled error
        sys.stderr.write(f"mode-guard: degraded ({exc!r})\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
