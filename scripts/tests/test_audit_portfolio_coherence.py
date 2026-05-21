"""Contract tests for scripts/audit-portfolio-coherence.py (F1.6)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "audit-portfolio-coherence.py"
FIXTURES = REPO_ROOT / "scripts" / "tests" / "fixtures"


def run_script(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    return result.returncode, result.stdout, result.stderr


def _write_intent(d: Path, name: str, **fm):
    base = {
        "id": fm.get("id", name.upper()),
        "slug": name,
        "object_type": "Strategic Intent",
        "status": fm.get("status", "Approved"),
        "last_updated": "2026-05-21",
    }
    base.update(fm)
    lines = ["---"]
    for k, v in base.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("# " + name)
    (d / f"{name}.md").write_text("\n".join(lines) + "\n")


class TestEmptyPortfolio(unittest.TestCase):
    def test_no_portfolio_verdict_on_empty_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run_script("--root", tmp, "--format", "json")
            self.assertEqual(code, 3)
            report = json.loads(out)
            self.assertEqual(report["frontmatter"]["verdict"], "no-portfolio")


class TestSingleArtifact(unittest.TestCase):
    def test_single_artifact_emits_one_line_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            (t / "strategy" / "intents").mkdir(parents=True)
            _write_intent(t / "strategy" / "intents", "solo")
            code, out, _ = run_script("--root", tmp, "--format", "json")
            self.assertEqual(code, 0)
            report = json.loads(out)
            self.assertEqual(report["frontmatter"]["artifacts_audited"], 1)
            self.assertEqual(report["frontmatter"]["pairs_checked"], 0)


class TestCoherentPortfolio(unittest.TestCase):
    def test_clean_verdict_on_coherent_portfolio(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            d = t / "strategy" / "intents"
            d.mkdir(parents=True)
            # Two intents with non-conflicting axes (both reinforce on resources)
            _write_intent(d, "intent-a", resource_claims="hire 2 engineers",
                          capability_focus="auth", market_posture="enterprise")
            _write_intent(d, "intent-b", resource_claims="hire 2 engineers",
                          capability_focus="auth", market_posture="enterprise")
            code, out, _ = run_script("--root", tmp, "--format", "json")
            self.assertEqual(code, 0)
            report = json.loads(out)
            self.assertEqual(report["frontmatter"]["verdict"], "clean")


class TestSequenced(unittest.TestCase):
    def test_sequenced_pair_does_not_flag_as_incoherent(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            d = t / "strategy" / "intents"
            d.mkdir(parents=True)
            _write_intent(d, "first", capability_focus="auth")
            _write_intent(d, "second", capability_focus="billing", sequencing_after="FIRST")
            code, out, _ = run_script("--root", tmp, "--format", "json")
            # sequenced pair should not flag as incoherent
            report = json.loads(out)
            for p in report.get("pairs", []):
                if "FIRST" in (p.get("a"), p.get("b")) and "SECOND" in (p.get("a"), p.get("b")):
                    self.assertEqual(p.get("label"), "sequenced")


class TestJsonShape(unittest.TestCase):
    def test_json_output_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            d = t / "strategy" / "intents"
            d.mkdir(parents=True)
            _write_intent(d, "a")
            _write_intent(d, "b")
            code, out, _ = run_script("--root", tmp, "--format", "json")
            report = json.loads(out)
            self.assertIn("frontmatter", report)
            for key in ("date", "artifacts_audited", "pairs_checked",
                        "contradictions_flagged", "verdict"):
                self.assertIn(key, report["frontmatter"])


class TestUnknownAxes(unittest.TestCase):
    def test_unknown_axis_does_not_flag_as_incoherent(self):
        # Pair with no axis claims should not produce a contradiction.
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            d = t / "strategy" / "intents"
            d.mkdir(parents=True)
            _write_intent(d, "a")
            _write_intent(d, "b")
            code, out, _ = run_script("--root", tmp, "--format", "json")
            report = json.loads(out)
            self.assertNotEqual(report["frontmatter"]["verdict"], "incoherent")


if __name__ == "__main__":
    unittest.main()
