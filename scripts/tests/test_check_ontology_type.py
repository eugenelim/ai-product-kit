"""Contract tests for scripts/check-ontology-type.py (F2.3).

Run from repo root:
    python3 -m unittest scripts.tests.test_check_ontology_type
"""

from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "check-ontology-type.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_ontology_type", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


MOD = _load_module()


def _payload_write(path: str, content: str) -> dict:
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": path, "content": content},
    }


def _payload_edit(path: str, old: str, new: str) -> dict:
    return {
        "tool_name": "Edit",
        "tool_input": {"file_path": path, "old_string": old, "new_string": new},
    }


def _payload_multiedit(path: str, edits: list[dict]) -> dict:
    return {
        "tool_name": "MultiEdit",
        "tool_input": {"file_path": path, "edits": edits},
    }


def _fm(object_type: str | None) -> str:
    if object_type is None:
        return "---\nslug: foo\n---\nbody\n"
    return f"---\nobject_type: {object_type}\nslug: foo\n---\nbody\n"


class TestPathMatching(unittest.TestCase):
    def test_silent_for_path_outside_table(self):
        payload = _payload_write(
            "delivery/initiatives/auth/specs/foo.md", _fm(None)
        )
        self.assertIsNone(MOD.check(payload))

    def test_handles_experiment_design_path(self):
        self.assertEqual(
            MOD.imply_type("validation/experiments/exp-001/experiment.md"),
            "Experiment",
        )

    def test_silent_for_experiment_results_path(self):
        payload = _payload_write(
            "validation/experiments/exp-001/results.md", _fm(None)
        )
        self.assertIsNone(MOD.check(payload))

    def test_trailing_slash_in_path_handled(self):
        # Sanity: imply_type strips trailing slash before matching.
        self.assertEqual(
            MOD.imply_type("delivery/visions/foo.md/"), "Vision"
        )


class TestNudgeBehavior(unittest.TestCase):
    def test_warns_when_object_type_missing_on_implied_path(self):
        payload = _payload_write("delivery/visions/foo.md", _fm(None))
        nudge = MOD.check(payload)
        self.assertIsNotNone(nudge)
        self.assertIn("Vision", nudge)
        self.assertIn("delivery/visions/foo.md", nudge)

    def test_warns_when_object_type_mismatched(self):
        payload = _payload_write("delivery/visions/foo.md", _fm("Initiative"))
        nudge = MOD.check(payload)
        self.assertIsNotNone(nudge)
        self.assertIn("Vision", nudge)
        self.assertIn("Initiative", nudge)

    def test_warns_on_case_mismatch(self):
        payload = _payload_write("delivery/visions/foo.md", _fm("vision"))
        nudge = MOD.check(payload)
        self.assertIsNotNone(nudge)
        # The lowercase "vision" should appear in the detail.
        self.assertIn("vision", nudge)

    def test_silent_when_object_type_matches_exactly(self):
        payload = _payload_write("delivery/visions/foo.md", _fm("Vision"))
        self.assertIsNone(MOD.check(payload))

    def test_landing_path_implies_landing_report(self):
        payload = _payload_write("delivery/landings/foo.md", _fm(None))
        nudge = MOD.check(payload)
        self.assertIsNotNone(nudge)
        self.assertIn("Landing Report", nudge)

    def test_warning_format_includes_path_and_implied_type(self):
        payload = _payload_write("delivery/visions/foo.md", _fm(None))
        nudge = MOD.check(payload)
        self.assertIsNotNone(nudge)
        # One line, expected shape.
        self.assertEqual(nudge.count("\n"), 0)
        self.assertTrue(nudge.startswith("ontology-type-check: "))
        self.assertIn(
            "ontology-type-check: delivery/visions/foo.md implies object_type: Vision but",
            nudge,
        )


class TestEditSemantics(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self.tmp.name)
        # Mirror the repo path layout under tmpdir so relative-path matching
        # holds and the on-disk read works via absolute path.
        # The hook's path-matching is on the tool_input.file_path string
        # itself, so we'll use the path-as-string for matching but write the
        # disk fixture at that same path under tmpdir.

    def tearDown(self):
        self.tmp.cleanup()

    def _write_fixture(self, rel_path: str, body: str) -> str:
        full = self.tmpdir / rel_path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(body, encoding="utf-8")
        return str(full)

    def test_edit_body_only_uses_on_disk_frontmatter(self):
        # On-disk has correct object_type; edit doesn't touch frontmatter.
        full = self._write_fixture(
            "delivery/visions/foo.md",
            "---\nobject_type: Vision\nslug: foo\n---\noriginal body\n",
        )
        # NOTE: imply_type matches on the string. To keep the match working,
        # we need the file_path to match the kit's relative-path table even
        # though we read from tmpdir. The simplest way: keep file_path the
        # absolute tmpdir path AND assert imply_type covers the suffix.
        # Instead, monkey-patch imply_type for this test or use a relative
        # path that resolves correctly. We'll use chdir to tmpdir.
        import os
        cwd = os.getcwd()
        os.chdir(self.tmpdir)
        try:
            payload = _payload_edit(
                "delivery/visions/foo.md",
                "original body",
                "updated body",
            )
            self.assertIsNone(MOD.check(payload))
        finally:
            os.chdir(cwd)

    def test_edit_that_changes_object_type_to_mismatch_warns(self):
        # File at delivery/initiatives/foo/README.md, edit rewrites the
        # object_type line to "Vision" — the path implies "Initiative".
        self._write_fixture(
            "delivery/initiatives/foo/README.md",
            "---\nobject_type: Initiative\nslug: foo\n---\nbody\n",
        )
        import os
        cwd = os.getcwd()
        os.chdir(self.tmpdir)
        try:
            payload = _payload_edit(
                "delivery/initiatives/foo/README.md",
                "---\nobject_type: Initiative\nslug: foo\n---",
                "---\nobject_type: Vision\nslug: foo\n---",
            )
            nudge = MOD.check(payload)
            self.assertIsNotNone(nudge)
            self.assertIn("Initiative", nudge)
            self.assertIn("Vision", nudge)
        finally:
            os.chdir(cwd)

    def test_edit_that_does_not_change_frontmatter_stays_silent(self):
        # old_string contains `---` but the replacement keeps object_type
        # identical (e.g., adds a comment).
        self._write_fixture(
            "delivery/visions/foo.md",
            "---\nobject_type: Vision\nslug: foo\n---\nbody\n",
        )
        import os
        cwd = os.getcwd()
        os.chdir(self.tmpdir)
        try:
            payload = _payload_edit(
                "delivery/visions/foo.md",
                "---\nobject_type: Vision\nslug: foo\n---",
                "---\nobject_type: Vision\nslug: foo\nnote: ok\n---",
            )
            self.assertIsNone(MOD.check(payload))
        finally:
            os.chdir(cwd)

    def test_multiedit_evaluated_against_final_state(self):
        # Intermediate edit sets object_type to "Initiative" briefly,
        # final edit restores it to "Vision". Hook must be silent.
        self._write_fixture(
            "delivery/visions/foo.md",
            "---\nobject_type: Vision\nslug: foo\n---\nbody\n",
        )
        import os
        cwd = os.getcwd()
        os.chdir(self.tmpdir)
        try:
            payload = _payload_multiedit(
                "delivery/visions/foo.md",
                [
                    {
                        "old_string": "---\nobject_type: Vision\nslug: foo\n---",
                        "new_string": "---\nobject_type: Initiative\nslug: foo\n---",
                    },
                    {
                        "old_string": "---\nobject_type: Initiative\nslug: foo\n---",
                        "new_string": "---\nobject_type: Vision\nslug: foo\n---",
                    },
                ],
            )
            self.assertIsNone(MOD.check(payload))
        finally:
            os.chdir(cwd)


class TestDegradedPaths(unittest.TestCase):
    def test_malformed_frontmatter_silent_not_crash(self):
        # Unclosed delimiter — parse() returns Frontmatter with parse_errors.
        # The hook should treat that as no usable frontmatter and stay silent.
        malformed = "---\nobject_type: Vision\nslug: foo\nbody-without-close\n"
        payload = _payload_write("delivery/visions/foo.md", malformed)
        # Either silent (preferred) or a "missing" nudge — spec says silent.
        self.assertIsNone(MOD.check(payload))


class TestSubprocess(unittest.TestCase):
    """Smoke-test the actual entry point with a stdin payload."""

    def test_subprocess_nudge_case(self):
        payload = _payload_write("delivery/visions/foo.md", _fm(None))
        proc = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, "")
        self.assertIn("ontology-type-check:", proc.stderr)
        self.assertIn("Vision", proc.stderr)

    def test_subprocess_silent_case(self):
        payload = _payload_write("delivery/visions/foo.md", _fm("Vision"))
        proc = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(proc.stderr, "")


if __name__ == "__main__":
    unittest.main()
