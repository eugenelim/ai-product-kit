"""Contract tests for scripts/check-assumption-threshold.py (F2.2).

Run from repo root:
    python3 -m unittest scripts.tests.test_check_assumption_threshold
"""

from __future__ import annotations

import datetime
import importlib.util
import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "check-assumption-threshold.py"


def _load_module():
    # The script name uses a hyphen — load via importlib so tests can call
    # the pure-function core directly with a synthetic repo_root.
    spec = importlib.util.spec_from_file_location(
        "check_assumption_threshold", str(SCRIPT_PATH)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MOD = _load_module()


def _write_experiment(
    exp_dir: Path,
    *,
    threshold_success: str | None = ">=40% completion",
    threshold_falsification: str | None = "<15% completion -> assumption killed",
    predeclared_at: str | None = None,
    override_threshold_lock: object | None = None,
    override_reason: str | None = None,
    override_authorized_by: str | None = None,
    override_authorized_at: str | None = None,
    raw_body: str | None = None,
    mtime_age_s: float = 5.0,
) -> Path:
    """Write a sibling experiment.md with controllable frontmatter and mtime."""
    exp_dir.mkdir(parents=True, exist_ok=True)
    path = exp_dir / "experiment.md"
    if raw_body is not None:
        path.write_text(raw_body, encoding="utf-8")
    else:
        lines = ["---", "object_type: Experiment"]
        if threshold_success is not None or threshold_falsification is not None:
            lines.append("predeclared_threshold:")
            if threshold_success is not None:
                lines.append(f"  success: {threshold_success}")
            if threshold_falsification is not None:
                lines.append(f"  falsification: {threshold_falsification}")
        if predeclared_at is not None:
            lines.append(f"predeclared_at: {predeclared_at}")
        if override_threshold_lock is not None:
            lines.append(f"override_threshold_lock: {str(override_threshold_lock).lower() if isinstance(override_threshold_lock, bool) else override_threshold_lock}")
        if override_reason is not None:
            lines.append(f"override_reason: {override_reason}")
        if override_authorized_by is not None:
            lines.append(f"override_authorized_by: {override_authorized_by}")
        if override_authorized_at is not None:
            lines.append(f"override_authorized_at: {override_authorized_at}")
        lines.append("---")
        lines.append("body")
        lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")

    # Plant the desired mtime (relative to wall clock now).
    target = time.time() - mtime_age_s
    os.utime(path, (target, target))
    return path


def _run_check(payload: dict, repo_root: Path) -> tuple[int, str]:
    return MOD.check(payload, repo_root=repo_root)


def _payload_for(results_path: Path) -> dict:
    return {"tool_name": "Write", "tool_input": {"file_path": str(results_path)}}


class TestPathMatcher(unittest.TestCase):
    def test_path_outside_glob_passes_silently(self):
        # validation/learnings/foo.md is outside the strict glob.
        with TempKit() as kit:
            outside = kit.root / "validation" / "learnings" / "foo.md"
            code, out = _run_check(_payload_for(outside), kit.root)
            self.assertEqual(code, 0)
            self.assertEqual(out, "")

    def test_recursive_path_matches_nested_experiment_dir(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "2026" / "q1" / "exp-001"
            _write_experiment(
                exp_dir,
                predeclared_at=datetime.date.today().isoformat(),
                mtime_age_s=5.0,
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 0, msg=f"expected pass; got out={out}")


class TestPresenceChecks(unittest.TestCase):
    def test_blocks_when_experiment_md_missing(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-missing"
            exp_dir.mkdir(parents=True, exist_ok=True)
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            payload = json.loads(out)
            self.assertEqual(payload["decision"], "block")
            self.assertIn("experiment.md", payload["reason"])

    def test_blocks_when_predeclared_threshold_missing(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                threshold_success=None,
                threshold_falsification=None,
                predeclared_at=datetime.date.today().isoformat(),
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            self.assertIn("predeclared_threshold", json.loads(out)["reason"])

    def test_blocks_when_only_success_criterion_present(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                threshold_success=">=40% completion",
                threshold_falsification=None,
                predeclared_at=datetime.date.today().isoformat(),
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            self.assertIn("falsification", json.loads(out)["reason"])

    def test_blocks_when_only_falsification_criterion_present(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                threshold_success=None,
                threshold_falsification="<15% completion",
                predeclared_at=datetime.date.today().isoformat(),
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            self.assertIn("success", json.loads(out)["reason"])

    def test_blocks_when_predeclared_at_missing(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(exp_dir, predeclared_at=None)
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            self.assertIn("predeclared_at", json.loads(out)["reason"])

    def test_malformed_design_frontmatter_blocks_with_clear_reason(self):
        # Frontmatter delimiters present but YAML inside is garbage.
        body = "---\nthis is not: : valid: yaml::\n  bad indent line\n---\nbody\n"
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            # Build a file whose parsed Frontmatter has empty data + parse_errors.
            _write_experiment(exp_dir, raw_body=body)
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            reason = json.loads(out)["reason"]
            # Should mention parse failure, not crash.
            self.assertTrue(
                "parse" in reason.lower() or "predeclared_threshold" in reason,
                msg=f"unexpected reason: {reason}",
            )

    def test_no_frontmatter_delimiters_blocks_with_clear_reason(self):
        # No --- delimiters at all; parser returns None.
        body = "no frontmatter here\njust prose\n"
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(exp_dir, raw_body=body)
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            reason = json.loads(out)["reason"]
            # Distinct from malformed-YAML reason.
            self.assertIn("no frontmatter", reason.lower())


class TestTimestampChecks(unittest.TestCase):
    def test_allows_write_when_design_predates_with_full_threshold(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                predeclared_at=datetime.date.today().isoformat(),
                mtime_age_s=5.0,
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 0, msg=f"expected pass; got out={out}")
            self.assertEqual(out, "")

    def test_blocks_when_predeclared_at_after_today(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                predeclared_at="2099-01-01",
                mtime_age_s=5.0,
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            reason = json.loads(out)["reason"]
            self.assertIn("future", reason.lower())

    def test_blocks_when_design_mtime_is_after_results_write(self):
        # Design file's mtime is fresher than now - 1s — fails the floor.
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                predeclared_at=datetime.date.today().isoformat(),
                mtime_age_s=0.0,  # mtime ~= now
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            reason = json.loads(out)["reason"]
            self.assertTrue(
                "mtime" in reason.lower() or "predate" in reason.lower(),
                msg=f"unexpected reason: {reason}",
            )


class TestOverridePath(unittest.TestCase):
    def test_override_allows_write_and_appends_to_override_log(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                threshold_success=None,
                threshold_falsification=None,
                predeclared_at=None,
                override_threshold_lock=True,
                override_reason="organic A/B test discovered after the fact",
                override_authorized_by="alice",
                override_authorized_at=datetime.date.today().isoformat(),
                mtime_age_s=5.0,
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 0, msg=f"expected override pass; got out={out}")
            log = kit.root / "validation" / "experiments" / "OVERRIDE-LOG.md"
            self.assertTrue(log.exists())
            log_text = log.read_text(encoding="utf-8")
            self.assertIn("exp-001", log_text)
            self.assertIn("alice", log_text)
            self.assertIn(datetime.date.today().isoformat(), log_text)

    def test_override_without_reason_blocks(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                override_threshold_lock=True,
                override_reason="",
                override_authorized_by="alice",
                override_authorized_at=datetime.date.today().isoformat(),
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            self.assertIn("override_reason", json.loads(out)["reason"])

    def test_override_without_authorizer_blocks(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                override_threshold_lock=True,
                override_reason="organic test",
                override_authorized_by="",
                override_authorized_at=datetime.date.today().isoformat(),
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            self.assertIn("override_authorized_by", json.loads(out)["reason"])

    def test_override_threshold_lock_false_does_not_unblock(self):
        # override_threshold_lock: false is treated as no-override — normal checks apply.
        # Threshold is missing, so the run must block on threshold (not on override).
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                threshold_success=None,
                threshold_falsification=None,
                predeclared_at=None,
                override_threshold_lock=False,
                override_reason="should be ignored",
                override_authorized_by="alice",
                override_authorized_at=datetime.date.today().isoformat(),
            )
            results = exp_dir / "results.md"
            code, out = _run_check(_payload_for(results), kit.root)
            self.assertEqual(code, 2)
            # The block reason must reference the threshold, not the override.
            reason = json.loads(out)["reason"]
            self.assertIn("predeclared_threshold", reason)


class TestEntryPoint(unittest.TestCase):
    """Subprocess test: pipe JSON to the script; assert exit code + stdout."""

    def test_subprocess_blocks_on_missing_experiment_md(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            exp_dir.mkdir(parents=True, exist_ok=True)
            results = exp_dir / "results.md"
            payload = json.dumps(_payload_for(results))
            proc = subprocess.run(
                [sys.executable, str(SCRIPT_PATH)],
                input=payload,
                capture_output=True,
                text=True,
                cwd=str(kit.root),
            )
            self.assertEqual(proc.returncode, 2)
            out = json.loads(proc.stdout)
            self.assertEqual(out["decision"], "block")

    def test_subprocess_allows_when_design_predates(self):
        with TempKit() as kit:
            exp_dir = kit.root / "validation" / "experiments" / "exp-001"
            _write_experiment(
                exp_dir,
                predeclared_at=datetime.date.today().isoformat(),
                mtime_age_s=5.0,
            )
            results = exp_dir / "results.md"
            payload = json.dumps(_payload_for(results))
            proc = subprocess.run(
                [sys.executable, str(SCRIPT_PATH)],
                input=payload,
                capture_output=True,
                text=True,
                cwd=str(kit.root),
            )
            self.assertEqual(proc.returncode, 0, msg=f"stderr={proc.stderr}")
            self.assertEqual(proc.stdout, "")


# ---- Test helpers ---------------------------------------------------------


class TempKit:
    """Context manager that creates a temp dir as the kit root."""

    def __init__(self):
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()

    def __enter__(self):
        self.root = Path(self._tmp.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
