"""Contract tests for scripts/mode-guard.py.

17 tests total: 6 helper + 2 SessionStart + 4 UPE + 5 PreToolUse(Skill).
See docs/specs/hook-mode-guard/spec.md § Contract tests.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


def _load_mode_guard():
    """Import scripts/mode-guard.py despite the hyphenated module path."""
    here = Path(__file__).resolve().parents[2]
    src = here / "scripts" / "mode-guard.py"
    spec = importlib.util.spec_from_file_location("mode_guard", src)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


mg = _load_mode_guard()


class TmpClaudeMd:
    """Context manager yielding a Path to a temp `.claude/CLAUDE.md` with given content."""

    def __init__(self, content: str | None):
        self.content = content
        self.tmp: tempfile.TemporaryDirectory | None = None

    def __enter__(self) -> Path:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        claudemd = root / ".claude" / "CLAUDE.md"
        claudemd.parent.mkdir(parents=True, exist_ok=True)
        if self.content is not None:
            claudemd.write_text(self.content, encoding="utf-8")
        return claudemd

    def __exit__(self, *args):
        assert self.tmp is not None
        self.tmp.cleanup()


# ---------------------------------------------------------------------------
# read_mode() helper — 6 tests
# ---------------------------------------------------------------------------
class TestReadMode(unittest.TestCase):
    def test_reads_greenfield_mode_from_claudemd(self):
        with TmpClaudeMd("# heading\n\nmode: greenfield\n\n## next\n") as p:
            self.assertEqual(mg.read_mode(p), "greenfield")

    def test_reads_enterprise_mode_from_claudemd(self):
        with TmpClaudeMd("mode: enterprise\n") as p:
            self.assertEqual(mg.read_mode(p), "enterprise")

    def test_returns_none_when_mode_undeclared(self):
        with TmpClaudeMd("# project\n\nno mode line here\n") as p:
            self.assertIsNone(mg.read_mode(p))

    def test_returns_none_when_mode_unknown_value(self):
        with TmpClaudeMd("mode: enterprise-lite\n") as p:
            self.assertIsNone(mg.read_mode(p))

    def test_returns_none_when_claudemd_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(mg.read_mode(Path(tmp) / "nonexistent.md"))

    def test_handles_crlf_line_endings(self):
        with TmpClaudeMd("# heading\r\n\r\nmode: greenfield\r\n\r\nmore\r\n") as p:
            self.assertEqual(mg.read_mode(p), "greenfield")


# ---------------------------------------------------------------------------
# SessionStart event — 2 tests
# ---------------------------------------------------------------------------
class TestSessionStart(unittest.TestCase):
    def test_session_start_emits_active_mode_context(self):
        code, stdout, stderr = mg.session_start("greenfield")
        self.assertEqual(code, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "SessionStart")
        ctx = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("greenfield", ctx)
        self.assertIn("/wardley-map", ctx)

    def test_session_start_warns_on_missing_mode(self):
        code, stdout, stderr = mg.session_start(None)
        self.assertEqual(code, 0)
        self.assertEqual(stdout, "")
        self.assertIn("mode-guard", stderr)


# ---------------------------------------------------------------------------
# UserPromptExpansion event — 4 tests
# ---------------------------------------------------------------------------
class TestUserPromptExpansion(unittest.TestCase):
    def test_upe_blocks_wrong_mode_command(self):
        payload = {
            "hook_event_name": "UserPromptExpansion",
            "expansion_type": "slash_command",
            "command_name": "wardley-map",
            "command_args": "",
            "prompt": "/wardley-map",
        }
        code, stdout, stderr = mg.handle_upe("greenfield", payload)
        self.assertEqual(code, 0)
        out = json.loads(stdout)
        self.assertEqual(out["decision"], "block")
        self.assertIn("/wardley-map is blocked in greenfield mode", out["reason"])
        self.assertIn("/competitive-research", out["reason"])
        self.assertIn("change mode: to enterprise", out["reason"])
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "UserPromptExpansion")

    def test_upe_allows_correct_mode_command(self):
        payload = {"hook_event_name": "UserPromptExpansion", "command_name": "competitive-research"}
        code, stdout, stderr = mg.handle_upe("greenfield", payload)
        self.assertEqual(code, 0)
        self.assertEqual(stdout, "")

    def test_upe_allows_shared_command_in_any_mode(self):
        for mode in ("greenfield", "enterprise"):
            for cmd in ("strategy-refresh", "phase-guide"):
                payload = {"hook_event_name": "UserPromptExpansion", "command_name": cmd}
                code, stdout, _ = mg.handle_upe(mode, payload)
                self.assertEqual(code, 0, f"{mode}/{cmd}")
                self.assertEqual(stdout, "", f"{mode}/{cmd}")

    def test_upe_emits_stderr_notice_when_mode_undeclared(self):
        payload = {"hook_event_name": "UserPromptExpansion", "command_name": "wardley-map"}
        code, stdout, stderr = mg.handle_upe(None, payload)
        self.assertEqual(code, 0)
        self.assertEqual(stdout, "")
        self.assertIn("mode-guard", stderr)
        self.assertIn("undeclared", stderr)


# ---------------------------------------------------------------------------
# PreToolUse on Skill event — 6 tests (5 named in spec + non-skill tool defensive)
# ---------------------------------------------------------------------------
class TestPreToolUseSkill(unittest.TestCase):
    def test_pretooluse_skill_blocks_wrong_mode(self):
        payload = {
            "tool_name": "Skill",
            "tool_input": {"skill_name": "wardley-map", "skill_input": ""},
        }
        code, stdout, stderr = mg.handle_pretooluse_skill("greenfield", payload)
        self.assertEqual(code, 2)
        out = json.loads(stdout)
        self.assertEqual(out["decision"], "block")
        self.assertIn("/wardley-map is blocked in greenfield mode", out["reason"])

    def test_pretooluse_skill_allows_correct_mode(self):
        payload = {"tool_name": "Skill", "tool_input": {"skill_name": "competitive-research"}}
        code, stdout, _ = mg.handle_pretooluse_skill("greenfield", payload)
        self.assertEqual(code, 0)
        self.assertEqual(stdout, "")

    def test_pretooluse_skill_allows_shared_skill(self):
        payload = {"tool_name": "Skill", "tool_input": {"skill_name": "phase-guide"}}
        code, stdout, _ = mg.handle_pretooluse_skill("greenfield", payload)
        self.assertEqual(code, 0)
        self.assertEqual(stdout, "")

    def test_pretooluse_ignores_non_skill_tool(self):
        payload = {"tool_name": "Write", "tool_input": {"file_path": "/tmp/foo"}}
        code, stdout, _ = mg.handle_pretooluse_skill("greenfield", payload)
        self.assertEqual(code, 0)
        self.assertEqual(stdout, "")

    def test_pretooluse_skill_emits_stderr_notice_when_mode_undeclared(self):
        payload = {"tool_name": "Skill", "tool_input": {"skill_name": "wardley-map"}}
        code, stdout, stderr = mg.handle_pretooluse_skill(None, payload)
        self.assertEqual(code, 0)
        self.assertEqual(stdout, "")
        self.assertIn("mode-guard", stderr)
        self.assertIn("undeclared", stderr)

    def test_pretooluse_skill_emits_stderr_notice_when_mode_unknown_value(self):
        # read_mode() returns None for unknown values; handle_pretooluse_skill sees None.
        payload = {"tool_name": "Skill", "tool_input": {"skill_name": "wardley-map"}}
        code, stdout, stderr = mg.handle_pretooluse_skill(None, payload)
        self.assertEqual(code, 0)
        self.assertEqual(stdout, "")
        self.assertIn("mode-guard", stderr)


if __name__ == "__main__":
    unittest.main()
