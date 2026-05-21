"""Contract tests for scripts/audit-completeness.py (F1.5)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "audit-completeness.py"
FIXTURES = REPO_ROOT / "scripts" / "tests" / "fixtures"
SAMPLE_KIT = FIXTURES / "sample-kit"


def run_script(*args: str) -> tuple[int, str, str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    return result.returncode, result.stdout, result.stderr


class TestSampleKit(unittest.TestCase):
    def test_produces_verdict_on_sample_kit_packet(self):
        # The sample-kit packet is intentionally sparse (only declares the
        # minimum fields needed for F1.1 graph tests). A sparse packet
        # legitimately produces verdict: block (many items missing). The
        # test asserts the script returns a verdict (not crash) and the
        # diagnostic mentions item counts.
        code, out, err = run_script(
            "--target", "auth-uplift",
            "--root", str(SAMPLE_KIT),
            "--format", "json",
        )
        self.assertIn(code, (0, 1, 2), f"unexpected code {code}. stderr: {err}")
        report = json.loads(out)
        self.assertIn(report["frontmatter"]["verdict"], ("pass", "needs-fixes", "block"))
        # 26 checks ran (25 items + 24a/24b split)
        self.assertEqual(report["frontmatter"]["items_checked"], 26)


class TestStructuralBlocks(unittest.TestCase):
    def test_block_verdict_on_initiative_without_handoff_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            (t / "delivery" / "initiatives" / "lone-init").mkdir(parents=True)
            (t / "delivery" / "initiatives" / "lone-init" / "README.md").write_text(
                "---\nid: INIT-X\nslug: lone-init\nobject_type: Initiative\n"
                "status: Approved\nlast_updated: 2026-05-21\nparent_vision: VIS-X\n---\n"
            )
            code, out, _ = run_script("--target", "lone-init", "--root", str(t), "--format", "json")
            self.assertEqual(code, 2, "expected block (2) when initiative has no packet")
            report = json.loads(out)
            self.assertEqual(report["frontmatter"]["verdict"], "block")
            self.assertIn("no handoff packet", report["diagnostic"].lower())


class TestJsonShape(unittest.TestCase):
    def test_json_output_shape(self):
        code, out, _ = run_script(
            "--target", "auth-uplift", "--root", str(SAMPLE_KIT), "--format", "json"
        )
        report = json.loads(out)
        self.assertIn("frontmatter", report)
        for key in ("date", "target", "items_checked", "items_passed",
                    "items_weak", "items_missing", "verdict"):
            self.assertIn(key, report["frontmatter"])


class TestItemCount(unittest.TestCase):
    def test_25_items_map_to_26_check_functions_via_24a_24b_split(self):
        # Verify via end-to-end run: a successful audit reports 26 items_checked
        # (25 ontology items + the 24a/24b split). Subprocess run avoids the
        # importlib dataclass introspection issue on Python 3.13.
        code, out, _ = run_script(
            "--target", "auth-uplift", "--root", str(SAMPLE_KIT), "--format", "json"
        )
        report = json.loads(out)
        self.assertEqual(
            report["frontmatter"]["items_checked"], 26,
            "expected 26 checks (25 items + 24a/24b split)"
        )


class TestWrite(unittest.TestCase):
    def test_write_flag_creates_report_under_packet_dir(self):
        code, out, err = run_script(
            "--target", "auth-uplift", "--root", str(SAMPLE_KIT), "--write"
        )
        # Report should be written under delivery/handoff-packets/auth-uplift/
        packet_dir = SAMPLE_KIT / "delivery" / "handoff-packets" / "auth-uplift"
        reports = list(packet_dir.glob("completeness-audit-*.md"))
        self.assertGreaterEqual(len(reports), 1)
        # Clean up so subsequent runs don't pollute the fixture
        for r in reports:
            r.unlink()
        log = packet_dir.parent / "AUDIT-LOG.md"
        if log.exists():
            log.unlink()


if __name__ == "__main__":
    unittest.main()
