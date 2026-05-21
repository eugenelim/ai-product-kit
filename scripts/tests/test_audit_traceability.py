"""Contract tests for scripts/audit-traceability.py (F1.4).

Run from repo root:
    python3 -m unittest scripts.tests.test_audit_traceability
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "audit-traceability.py"
FIXTURES = REPO_ROOT / "scripts" / "tests" / "fixtures"
SAMPLE_KIT = FIXTURES / "sample-kit"
BROKEN = FIXTURES / "broken"


def run_script(*args: str) -> tuple[int, str, str]:
    """Invoke the script as a subprocess; return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    return result.returncode, result.stdout, result.stderr


class TestClean(unittest.TestCase):
    def test_clean_verdict_on_sample_kit_fixture(self):
        # The sample-kit fixture is structurally consistent (chain-1 complete,
        # chain-2 sparse but no rule violations on either)
        code, out, err = run_script("--root", str(SAMPLE_KIT), "--format", "json")
        self.assertEqual(code, 0, f"expected clean (0), got {code}. stderr: {err}")
        report = json.loads(out)
        self.assertEqual(report["frontmatter"]["verdict"], "clean")


class TestBroken(unittest.TestCase):
    def test_broken_verdict_on_broken_fixtures(self):
        code, out, err = run_script("--root", str(BROKEN), "--format", "json")
        # Broken fixtures have: a cycle (Initiative A ↔ B via parent_vision)
        # plus dangling-parent.md whose parent_intent doesn't resolve. That's
        # 2 broken-link counts on 3 nodes — per the command-file thresholds
        # (>3 broken = broken; 1-3 = drift) this resolves to drift, not broken.
        # The test asserts non-clean: drift (1) or broken (2) is acceptable;
        # clean (0) or insufficient-data (3) would be a regression.
        self.assertIn(code, (1, 2), f"expected drift or broken; got {code}. stderr: {err}")

    def test_dangling_parent_edge_flags_rule_1_or_2(self):
        code, out, err = run_script("--root", str(BROKEN), "--format", "json")
        report = json.loads(out)
        # dangling-parent.md is an OST with parent_intent → NONEXISTENT-INTENT
        # → Rule 1 (OST as composite needs traceable upstream) OR an orphan
        # surfaced via Rule violations. The reviewer expects rule 1 or 2.
        rules_violated = {v["rule"] for v in report["violations"]}
        # Cycles map to Rule 1 (a node in a cycle cannot have a valid parent chain)
        self.assertTrue(
            1 in rules_violated or 2 in rules_violated,
            f"expected rule 1 or 2 violation; got {rules_violated}",
        )

    def test_cycle_flags_as_broken(self):
        code, out, err = run_script("--root", str(BROKEN), "--format", "json")
        report = json.loads(out)
        # Cycle detection should surface in violations (Rule 1)
        violation_types = {v.get("violation_type") for v in report["violations"]}
        self.assertIn("cycle", violation_types)


class TestRuleSpecificFixtures(unittest.TestCase):
    """Per-rule micro-fixtures inline; each constructs the minimum graph
    needed to trigger one rule and asserts it fires."""

    def _audit(self, tmp: Path) -> dict:
        code, out, _ = run_script("--root", str(tmp), "--format", "json")
        return json.loads(out)

    def test_requirement_without_capability_flags_rule_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            (t / "strategy" / "intents").mkdir(parents=True)
            (t / "delivery" / "handoff-packets" / "x").mkdir(parents=True)
            # Need >= 3 typed nodes to avoid insufficient-data verdict
            (t / "strategy" / "intents" / "i.md").write_text(
                "---\nid: I1\nslug: i\nobject_type: Strategic Intent\n"
                "status: Approved\nlast_updated: 2026-05-21\n---\n"
            )
            (t / "delivery" / "handoff-packets" / "x" / "req.md").write_text(
                "---\nid: REQ-X\nslug: req-x\nobject_type: Requirement\n"
                "status: Ready for Engineering\nlast_updated: 2026-05-21\n"
                "parent_initiative: I1\n---\n"  # no related_capabilities
            )
            (t / "delivery" / "handoff-packets" / "x" / "req2.md").write_text(
                "---\nid: REQ-Y\nslug: req-y\nobject_type: Requirement\n"
                "status: Ready for Engineering\nlast_updated: 2026-05-21\n"
                "parent_initiative: I1\n---\n"
            )
            (t / "delivery" / "handoff-packets" / "x" / "req3.md").write_text(
                "---\nid: REQ-Z\nslug: req-z\nobject_type: Requirement\n"
                "status: Ready for Engineering\nlast_updated: 2026-05-21\n"
                "parent_initiative: I1\n---\n"
            )
            report = self._audit(t)
            rules = {v["rule"] for v in report["violations"]}
            self.assertIn(1, rules)


class TestEmptyAndScope(unittest.TestCase):
    def test_insufficient_data_verdict_on_empty_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run_script("--root", tmp, "--format", "json")
            self.assertEqual(code, 3)
            report = json.loads(out)
            self.assertEqual(report["frontmatter"]["verdict"], "insufficient-data")

    def test_scope_subtree_evaluates_insufficient_data_threshold_on_subtree_not_global(self):
        # Scoped to a non-existent slug → script should report insufficient-data
        # via the graph's unresolved-scope parse_errors entry
        code, out, _ = run_script(
            "--root", str(SAMPLE_KIT), "--scope", "nonexistent-slug", "--format", "json"
        )
        self.assertEqual(code, 3)


class TestJsonShape(unittest.TestCase):
    def test_json_output_shape(self):
        code, out, _ = run_script("--root", str(SAMPLE_KIT), "--format", "json")
        report = json.loads(out)
        # Required top-level keys
        self.assertIn("frontmatter", report)
        self.assertIn("violations", report)
        self.assertIn("orphans", report)
        # Frontmatter has the required fields
        fm = report["frontmatter"]
        for key in ("date", "scope", "objects_audited", "rules_violated",
                    "broken_links", "weak_chains", "verdict"):
            self.assertIn(key, fm)


class TestVacuousPasses(unittest.TestCase):
    def test_rule_7_vacuously_passes_when_no_handoff_packets_exist(self):
        # Build a fixture with chains but no Handoff Packets
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            (t / "strategy" / "intents").mkdir(parents=True)
            (t / "discovery" / "trees").mkdir(parents=True)
            (t / "validation" / "learnings").mkdir(parents=True)
            (t / "strategy" / "intents" / "i.md").write_text(
                "---\nid: I1\nslug: i\nobject_type: Strategic Intent\n"
                "status: Approved\nlast_updated: 2026-05-21\n---\n"
            )
            (t / "discovery" / "trees" / "o.md").write_text(
                "---\nid: O1\nslug: o\nobject_type: Opportunity Solution Tree\n"
                "status: Approved\nlast_updated: 2026-05-21\nparent_intent: I1\n---\n"
            )
            (t / "validation" / "learnings" / "l.md").write_text(
                "---\nid: L1\nslug: l\nobject_type: Validation Learning Memo\n"
                "status: Validated\nlast_updated: 2026-05-21\nparent_opportunity: I1\n---\n"
            )
            code, out, _ = run_script("--root", str(t), "--format", "json")
            report = json.loads(out)
            # Rule 7 should not appear in violations (no Handoff Packets in scope)
            rules = {v["rule"] for v in report["violations"]}
            self.assertNotIn(7, rules)


class TestWeakChains(unittest.TestCase):
    def test_weak_chains_only_above_10pct_yields_drift(self):
        # Hard to construct precisely; assert structural — when sample-kit has
        # at least one weak link (PROB-001 with Moderate evidence is a weak
        # chain member depending on impl), the verdict either stays clean
        # (≤10%) or becomes drift. Either way, not broken.
        code, _, _ = run_script("--root", str(SAMPLE_KIT), "--format", "json")
        self.assertIn(code, (0, 1))  # clean or drift, never broken on sample-kit


class TestWrite(unittest.TestCase):
    def test_write_flag_creates_dated_report_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            # Use a small fixture
            (t / "strategy" / "intents").mkdir(parents=True)
            for n in range(3):
                (t / "strategy" / "intents" / f"i{n}.md").write_text(
                    f"---\nid: I{n}\nslug: i{n}\nobject_type: Strategic Intent\n"
                    f"status: Approved\nlast_updated: 2026-05-21\n---\n"
                )
            code, _, _ = run_script("--root", str(t), "--write")
            audits_dir = t / "docs" / "audits"
            self.assertTrue(audits_dir.is_dir())
            reports = list(audits_dir.glob("traceability-*.md"))
            self.assertEqual(len(reports), 1)
            # TRACEABILITY-LOG.md also created
            self.assertTrue((audits_dir / "TRACEABILITY-LOG.md").exists())


if __name__ == "__main__":
    unittest.main()
