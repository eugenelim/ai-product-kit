"""Contract tests for scripts/check-handover-link.py (F2.1).

Run from repo root:
    python3 -m unittest scripts.tests.test_check_handover_link

The hook is a PreToolUse guard on Write|Edit|MultiEdit that requires the
required `parent_*` frontmatter field(s) for any artifact under one of the
seven canonical handover paths in docs/HANDOVERS.md.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "check-handover-link.py"


def _load_module():
    """Load scripts/check-handover-link.py as a module (the filename has a hyphen,
    so we cannot use normal `import`)."""
    spec = importlib.util.spec_from_file_location(
        "check_handover_link", SCRIPT_PATH
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


chl = _load_module()


def make_payload(tool_name, file_path, **kwargs):
    """Build a PreToolUse stdin JSON payload."""
    tool_input = {"file_path": str(file_path)}
    tool_input.update(kwargs)
    return {"tool_name": tool_name, "tool_input": tool_input}


class TestPathGlobMatcher(unittest.TestCase):
    """Task 1: HANDOVER_RULES table and match_rule()."""

    def test_strategy_intent_matches(self):
        rule = chl.match_rule("strategy/intents/foo.md")
        self.assertIsNotNone(rule)
        self.assertEqual(rule["handover"], 1)
        # parent_diagnosis is optional → required is empty for Handover 1
        self.assertEqual(rule["required"], [])

    def test_discovery_tree_matches(self):
        rule = chl.match_rule("discovery/trees/foo.md")
        self.assertIsNotNone(rule)
        self.assertIn("parent_intent", rule["required"])

    def test_initiative_readme_path_pattern(self):
        # README.md under <slug>/ matches
        rule = chl.match_rule("delivery/initiatives/foo/README.md")
        self.assertIsNotNone(rule)
        self.assertEqual(rule["handover"], 5)
        # Nested specs do NOT match Handover 5
        self.assertIsNone(chl.match_rule("delivery/initiatives/foo/specs/bar.md"))
        # Flat <slug>.md is NOT Handover 5 either
        self.assertIsNone(chl.match_rule("delivery/initiatives/foo.md"))

    def test_path_outside_handover_globs_passes_silently(self):
        self.assertIsNone(chl.match_rule("tools/some-script.py"))
        self.assertIsNone(chl.match_rule("context/README.md"))
        # When passed through check(), should exit 0 with no output
        with tempfile.TemporaryDirectory() as td:
            payload = make_payload(
                "Write",
                Path(td) / "tools" / "x.py",
                content="print('hi')\n",
            )
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 0)
            self.assertIsNone(out)
            self.assertIsNone(err)


class TestFrontmatterCheck(unittest.TestCase):
    """Task 2: required-fields and override semantics."""

    def _write_payload(self, td, rel_path, content):
        path = Path(td) / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        return make_payload("Write", path, content=content)

    def test_allows_write_with_required_parent_field(self):
        with tempfile.TemporaryDirectory() as td:
            content = "---\nobject_type: Opportunity Solution Tree\nparent_intent: some-intent\n---\nbody\n"
            payload = self._write_payload(td, "discovery/trees/foo.md", content)
            code, out, err = chl.check(payload, repo_root=Path(td))
            # parent_intent target file does not exist → exit 0 with stderr warning
            self.assertEqual(code, 0)

    def test_blocks_write_when_parent_field_missing(self):
        with tempfile.TemporaryDirectory() as td:
            content = "---\nobject_type: Opportunity Solution Tree\n---\nbody\n"
            payload = self._write_payload(td, "discovery/trees/foo.md", content)
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 2)
            self.assertIsNotNone(out)
            blob = json.loads(out)
            self.assertEqual(blob["decision"], "block")
            self.assertIn("parent_intent", blob["reason"])

    def test_landing_requires_both_parent_fields(self):
        with tempfile.TemporaryDirectory() as td:
            # Missing parent_handoff_packet
            content = "---\nobject_type: Landing Report\nparent_vision: v\n---\n"
            payload = self._write_payload(td, "delivery/landings/foo.md", content)
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 2)
            self.assertIn("parent_handoff_packet", json.loads(out)["reason"])

            # Missing parent_vision
            content2 = "---\nobject_type: Landing Report\nparent_handoff_packet: h\n---\n"
            payload2 = self._write_payload(td, "delivery/landings/bar.md", content2)
            code2, out2, _ = chl.check(payload2, repo_root=Path(td))
            self.assertEqual(code2, 2)
            self.assertIn("parent_vision", json.loads(out2)["reason"])

    def test_vision_requires_both_parent_fields(self):
        with tempfile.TemporaryDirectory() as td:
            # Missing parent_intent
            content = "---\nobject_type: Vision\nparent_learning: l\n---\n"
            payload = self._write_payload(td, "delivery/visions/foo.md", content)
            code, out, _ = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 2)
            self.assertIn("parent_intent", json.loads(out)["reason"])

            # Missing parent_learning
            content2 = "---\nobject_type: Vision\nparent_intent: i\n---\n"
            payload2 = self._write_payload(td, "delivery/visions/bar.md", content2)
            code2, out2, _ = chl.check(payload2, repo_root=Path(td))
            self.assertEqual(code2, 2)
            self.assertIn("parent_learning", json.loads(out2)["reason"])

    def test_strategy_intent_passes_without_parent_diagnosis(self):
        with tempfile.TemporaryDirectory() as td:
            content = "---\nobject_type: Strategic Intent\nmode: greenfield\n---\nbody\n"
            payload = self._write_payload(td, "strategy/intents/foo.md", content)
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 0)
            self.assertIsNone(out)

    def test_override_with_all_fields_unblocks_and_logs(self):
        with tempfile.TemporaryDirectory() as td:
            content = (
                "---\n"
                "object_type: Opportunity Solution Tree\n"
                "override_handover_link: true\n"
                "override_reason: backfilling a tree imported from legacy planning doc\n"
                "override_authorized_by: jane.doe\n"
                "override_authorized_at: 2026-05-21\n"
                "---\n"
            )
            payload = self._write_payload(td, "discovery/trees/foo.md", content)
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 0)
            log_path = Path(td) / "delivery" / "HANDOVER-OVERRIDE-LOG.md"
            self.assertTrue(log_path.exists(), "override log file not created")
            text = log_path.read_text(encoding="utf-8")
            self.assertIn("discovery/trees/foo.md", text)
            self.assertIn("jane.doe", text)

    def test_override_without_reason_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            content = (
                "---\n"
                "object_type: Opportunity Solution Tree\n"
                "override_handover_link: true\n"
                "override_reason: \n"
                "override_authorized_by: jane.doe\n"
                "override_authorized_at: 2026-05-21\n"
                "---\n"
            )
            payload = self._write_payload(td, "discovery/trees/foo.md", content)
            code, out, _ = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 2)

    def test_override_without_authorizer_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            content = (
                "---\n"
                "object_type: Opportunity Solution Tree\n"
                "override_handover_link: true\n"
                "override_reason: filling in for legacy import\n"
                "override_authorized_by: \n"
                "override_authorized_at: 2026-05-21\n"
                "---\n"
            )
            payload = self._write_payload(td, "discovery/trees/foo.md", content)
            code, out, _ = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 2)

    def test_override_false_does_not_unblock(self):
        with tempfile.TemporaryDirectory() as td:
            content = (
                "---\n"
                "object_type: Opportunity Solution Tree\n"
                "override_handover_link: false\n"
                "override_reason: should not matter\n"
                "override_authorized_by: jane.doe\n"
                "override_authorized_at: 2026-05-21\n"
                "---\n"
            )
            payload = self._write_payload(td, "discovery/trees/foo.md", content)
            code, out, _ = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 2)


class TestEditSemantics(unittest.TestCase):
    """Task 3: Edit / MultiEdit reconstruction."""

    def test_edit_with_frontmatter_touching_old_string_reconstructs_proposed_state(self):
        with tempfile.TemporaryDirectory() as td:
            on_disk = (
                "---\n"
                "object_type: Opportunity Solution Tree\n"
                "---\n"
                "body\n"
            )
            path = Path(td) / "discovery" / "trees" / "foo.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(on_disk, encoding="utf-8")
            # Edit replaces the frontmatter to add parent_intent
            payload = {
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": str(path),
                    "old_string": "---\nobject_type: Opportunity Solution Tree\n---\n",
                    "new_string": "---\nobject_type: Opportunity Solution Tree\nparent_intent: some-intent\n---\n",
                },
            }
            code, out, err = chl.check(payload, repo_root=Path(td))
            # parent_intent present → no block; dangling target → exit 0 + stderr
            self.assertEqual(code, 0)

    def test_edit_body_only_uses_on_disk_frontmatter(self):
        with tempfile.TemporaryDirectory() as td:
            on_disk = (
                "---\n"
                "object_type: Opportunity Solution Tree\n"
                "parent_intent: some-intent\n"
                "---\n"
                "Original body line.\n"
            )
            path = Path(td) / "discovery" / "trees" / "foo.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(on_disk, encoding="utf-8")
            # Body-only edit (no --- in old_string)
            payload = {
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": str(path),
                    "old_string": "Original body line.",
                    "new_string": "Replaced body line.",
                },
            }
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 0)
            self.assertIsNone(out)

    def test_multiedit_treated_as_sequence_of_edits(self):
        with tempfile.TemporaryDirectory() as td:
            on_disk = (
                "---\n"
                "object_type: Opportunity Solution Tree\n"
                "---\n"
                "Old body.\n"
            )
            path = Path(td) / "discovery" / "trees" / "foo.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(on_disk, encoding="utf-8")
            payload = {
                "tool_name": "MultiEdit",
                "tool_input": {
                    "file_path": str(path),
                    "edits": [
                        {
                            "old_string": "---\nobject_type: Opportunity Solution Tree\n---\n",
                            "new_string": "---\nobject_type: Opportunity Solution Tree\nparent_intent: some-intent\n---\n",
                        },
                        {
                            "old_string": "Old body.",
                            "new_string": "New body.",
                        },
                    ],
                },
            }
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 0)


class TestDanglingAndDegraded(unittest.TestCase):
    """Task 4: dangling-link warnings + degraded paths."""

    def test_warns_when_parent_target_file_missing(self):
        with tempfile.TemporaryDirectory() as td:
            content = "---\nobject_type: Opportunity Solution Tree\nparent_intent: nonexistent-slug\n---\n"
            path = Path(td) / "discovery" / "trees" / "foo.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            payload = make_payload("Write", path, content=content)
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 0)
            self.assertIsNotNone(err)
            self.assertIn("nonexistent-slug", err)

    def test_dangling_parent_initiative_resolves_to_readme_not_flat_md(self):
        with tempfile.TemporaryDirectory() as td:
            # Create the flat-file form — it should NOT satisfy the resolver
            flat = Path(td) / "delivery" / "initiatives" / "foo.md"
            flat.parent.mkdir(parents=True, exist_ok=True)
            flat.write_text("decoy", encoding="utf-8")
            content = (
                "---\n"
                "object_type: Handoff Packet\n"
                "parent_initiative: foo\n"
                "---\n"
            )
            path = Path(td) / "delivery" / "handoff-packets" / "p" / "README.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            payload = make_payload("Write", path, content=content)
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 0)
            self.assertIsNotNone(err)
            self.assertIn("foo", err)

            # Now create the README form — resolver should now find it
            readme = Path(td) / "delivery" / "initiatives" / "foo" / "README.md"
            readme.parent.mkdir(parents=True, exist_ok=True)
            readme.write_text("real", encoding="utf-8")
            code2, _, err2 = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code2, 0)
            self.assertIsNone(err2)

    def test_dangling_parent_vision_resolves_to_flat_md_not_readme(self):
        with tempfile.TemporaryDirectory() as td:
            # Decoy README-style
            readme = Path(td) / "delivery" / "visions" / "foo" / "README.md"
            readme.parent.mkdir(parents=True, exist_ok=True)
            readme.write_text("decoy", encoding="utf-8")
            content = (
                "---\n"
                "object_type: Initiative\n"
                "parent_vision: foo\n"
                "---\n"
            )
            path = Path(td) / "delivery" / "initiatives" / "i" / "README.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            payload = make_payload("Write", path, content=content)
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 0)
            self.assertIsNotNone(err)

            # Now create flat — should satisfy
            flat = Path(td) / "delivery" / "visions" / "foo.md"
            flat.write_text("real", encoding="utf-8")
            code2, _, err2 = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code2, 0)
            self.assertIsNone(err2)

    def test_malformed_frontmatter_degrades_to_warning_not_crash(self):
        with tempfile.TemporaryDirectory() as td:
            # Unclosed --- delimiter
            content = "---\nobject_type: Opportunity Solution Tree\nparent_intent: x\n"
            path = Path(td) / "discovery" / "trees" / "foo.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            payload = make_payload("Write", path, content=content)
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 0)
            self.assertIsNone(out)
            self.assertIsNotNone(err)

    def test_uppercase_path_warns_but_does_not_block(self):
        with tempfile.TemporaryDirectory() as td:
            content = "---\nobject_type: Vision\n---\n"
            path = Path(td) / "Delivery" / "Visions" / "foo.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            payload = make_payload("Write", path, content=content)
            code, out, err = chl.check(payload, repo_root=Path(td))
            self.assertEqual(code, 0)
            self.assertIsNone(out)
            self.assertIsNotNone(err)
            self.assertIn("uppercase", err.lower())


class TestEntryPoint(unittest.TestCase):
    """Task 5: subprocess end-to-end against stdin JSON protocol."""

    def test_subprocess_block_via_stdin(self):
        with tempfile.TemporaryDirectory() as td:
            content = "---\nobject_type: Opportunity Solution Tree\n---\n"
            file_path = Path(td) / "discovery" / "trees" / "foo.md"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            payload = make_payload("Write", file_path, content=content)
            env = os.environ.copy()
            env["KIT_REPO_ROOT"] = str(td)
            proc = subprocess.run(
                [sys.executable, str(SCRIPT_PATH)],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                env=env,
                cwd=str(REPO_ROOT),
            )
            self.assertEqual(proc.returncode, 2)
            self.assertTrue(proc.stdout.strip())
            blob = json.loads(proc.stdout)
            self.assertEqual(blob["decision"], "block")
            self.assertIn("parent_intent", blob["reason"])


if __name__ == "__main__":
    unittest.main()
