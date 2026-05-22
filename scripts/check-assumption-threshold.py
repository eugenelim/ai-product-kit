#!/usr/bin/env python3
"""check-assumption-threshold (F2.2) — PreToolUse hook script.

Refuses to write `validation/experiments/**/results.md` unless a sibling
`experiment.md` exists with a predeclared falsification threshold whose
design file predates the write by >= 1s. Contract:
`.claude/hooks/assumption-threshold-lock.md`. On override-path allow, appends
a one-line entry to `<repo-root>/validation/experiments/OVERRIDE-LOG.md`.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Optional

# Ensure the repo root is on sys.path so `scripts.lib.frontmatter` resolves
# regardless of how the hook is invoked.
_THIS = Path(__file__).resolve()
_REPO_ROOT = _THIS.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.lib.frontmatter import parse_file  # noqa: E402

_RESULTS_RE = re.compile(r"(^|/)validation/experiments/.+/results\.md$")
_MTIME_FLOOR_SEC = 1.0


def match_results_path(file_path: str) -> Optional[Path]:
    """Return the experiment directory containing results.md, or None if out-of-glob."""
    if not file_path:
        return None
    # Normalize to forward-slash for regex matching; preserve original for Path ops.
    norm = file_path.replace("\\", "/")
    if not _RESULTS_RE.search(norm):
        return None
    return Path(file_path).parent


def resolve_experiment_md(exp_dir: Path) -> Optional[Path]:
    candidate = exp_dir / "experiment.md"
    if candidate.is_file():
        return candidate
    return None


def _nonempty(val: Any) -> bool:
    if val is None:
        return False
    if isinstance(val, str):
        return val.strip() != ""
    if isinstance(val, (list, dict)):
        # The parser maps `key: ` (empty trailing value with no continuation)
        # to an empty list. Treat as empty.
        return len(val) > 0
    return True


def check_threshold_fields(fm_data: dict) -> Optional[str]:
    """Return None on pass; a reason string on fail."""
    threshold = fm_data.get("predeclared_threshold")
    if threshold is None:
        return "experiment.md missing `predeclared_threshold:` block"
    if not isinstance(threshold, dict):
        return "experiment.md `predeclared_threshold:` must be a map with `success` and `falsification`"
    success_ok = _nonempty(threshold.get("success"))
    falsification_ok = _nonempty(threshold.get("falsification"))
    if not success_ok and not falsification_ok:
        return "experiment.md `predeclared_threshold:` missing both `success` and `falsification`"
    if not success_ok:
        return "experiment.md `predeclared_threshold.success` missing or empty"
    if not falsification_ok:
        return "experiment.md `predeclared_threshold.falsification` missing or empty"
    if not _nonempty(fm_data.get("predeclared_at")):
        return "experiment.md missing `predeclared_at:` date"
    return None


def check_predeclared_at(date_val: Any) -> Optional[str]:
    """Reject future-dated `predeclared_at`. Return None on pass."""
    if not isinstance(date_val, str):
        date_val = str(date_val)
    try:
        d = datetime.date.fromisoformat(date_val.strip())
    except ValueError:
        return f"experiment.md `predeclared_at:` is not a valid YYYY-MM-DD date: {date_val!r}"
    today = datetime.date.today()
    if d > today:
        return (
            f"experiment.md `predeclared_at: {date_val}` is in the future "
            f"(today is {today.isoformat()}) — threshold cannot be predeclared after the fact"
        )
    return None


def check_mtime(experiment_path: Path, now: Optional[float] = None) -> Optional[str]:
    """The design file's mtime must be <= now - 1.0 seconds."""
    if now is None:
        now = time.time()
    mtime = os.path.getmtime(experiment_path)
    if mtime > now - _MTIME_FLOOR_SEC:
        return (
            f"experiment.md mtime ({mtime:.3f}) is not at least "
            f"{_MTIME_FLOOR_SEC:.1f}s older than the results-write event ({now:.3f}) — "
            f"design file must predate results"
        )
    return None


def is_override_requested(fm_data: dict) -> bool:
    """Strict `is True` per spec — `false`, `None`, `0`, `"true"` string all return False."""
    return fm_data.get("override_threshold_lock") is True


def check_override_fields(fm_data: dict) -> Optional[str]:
    """When override requested, validate the supporting fields. Return None on pass."""
    if not _nonempty(fm_data.get("override_reason")):
        return "override_threshold_lock requested but `override_reason:` is empty"
    if not _nonempty(fm_data.get("override_authorized_by")):
        return "override_threshold_lock requested but `override_authorized_by:` is empty"
    if not _nonempty(fm_data.get("override_authorized_at")):
        return "override_threshold_lock requested but `override_authorized_at:` is empty"
    return None


def append_override_log(
    repo_root: Path,
    experiment_id: str,
    authorizer: str,
    reason: str,
) -> None:
    """Append a one-line entry to validation/experiments/OVERRIDE-LOG.md."""
    log_dir = repo_root / "validation" / "experiments"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "OVERRIDE-LOG.md"
    today = datetime.date.today().isoformat()
    # Collapse newlines in reason so each override is a single line.
    reason_one_line = " ".join(reason.split())
    line = (
        f"- {today} {experiment_id} "
        f'override_authorized_by={authorizer} reason="{reason_one_line}"\n'
    )
    if not log_path.exists():
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("# OVERRIDE-LOG\n\n")
            f.write(line)
    else:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line)


def _block(reason: str) -> tuple[int, str]:
    return 2, json.dumps({"decision": "block", "reason": reason})


def check(payload: dict, *, repo_root: Optional[Path] = None) -> tuple[int, str]:
    """Pure-function core. Returns (exit_code, stdout_str)."""
    if repo_root is None:
        repo_root = _REPO_ROOT

    tool_name = payload.get("tool_name")
    if tool_name != "Write":
        return 0, ""
    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path", "")

    exp_dir = match_results_path(file_path)
    if exp_dir is None:
        return 0, ""

    experiment_md = resolve_experiment_md(exp_dir)
    if experiment_md is None:
        return _block(f"no experiment.md found in {exp_dir.as_posix()} — predeclared threshold required before writing results.md")

    fm = parse_file(experiment_md)
    if fm is None:
        return _block(f"design file has no frontmatter (no `---` delimiters): {experiment_md.as_posix()}")
    if fm.parse_errors and not fm.data:
        return _block(
            f"experiment.md frontmatter parse failed for {experiment_md.as_posix()}: "
            f"{'; '.join(fm.parse_errors)}"
        )

    data = fm.data

    # Override branch FIRST.
    if is_override_requested(data):
        reason = check_override_fields(data)
        if reason is not None:
            return _block(reason)
        append_override_log(
            repo_root=repo_root,
            experiment_id=exp_dir.name,
            authorizer=str(data.get("override_authorized_by", "")),
            reason=str(data.get("override_reason", "")),
        )
        return 0, ""

    # Threshold-presence checks.
    reason = check_threshold_fields(data)
    if reason is not None:
        return _block(reason)

    # predeclared_at <= today.
    reason = check_predeclared_at(data["predeclared_at"])
    if reason is not None:
        return _block(reason)

    # mtime check: design file must predate the write by >= 1s.
    reason = check_mtime(experiment_md)
    if reason is not None:
        return _block(reason)

    return 0, ""


def main() -> int:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        payload = json.loads(raw)
        exit_code, stdout_str = check(payload)
        if stdout_str:
            sys.stdout.write(stdout_str)
        return exit_code
    except Exception:
        # Never brick a session — fail-open with stderr trace.
        traceback.print_exc(file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
