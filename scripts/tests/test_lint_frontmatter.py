"""Contract tests for tools/lint-frontmatter.py (F0.12 — ai_assistance_allowed rule).

Run from repo root:
    python3 -m unittest scripts.tests.test_lint_frontmatter
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "tools" / "lint-frontmatter.py"
FIXTURES = REPO_ROOT / "scripts" / "tests" / "fixtures" / "lint-frontmatter"


def run(*args: str) -> tuple[int, str, str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    return result.returncode, result.stdout, result.stderr


ERR_MSG = "ai_assistance_allowed: restricted requires ai_assistance_used: list to be non-empty"


class TestRestrictedRule(unittest.TestCase):
    def test_restricted_without_ai_assistance_used_fails(self):
        code, _, err = run(str(FIXTURES / "restricted-missing" / "artifact.md"))
        self.assertEqual(code, 1, f"expected exit 1, stderr was: {err}")
        self.assertIn(ERR_MSG, err)

    def test_restricted_with_empty_ai_assistance_used_fails(self):
        code, _, err = run(str(FIXTURES / "restricted-empty" / "artifact.md"))
        self.assertEqual(code, 1, f"expected exit 1, stderr was: {err}")
        self.assertIn(ERR_MSG, err)

    def test_restricted_with_scalar_string_ai_assistance_used_fails(self):
        code, _, err = run(str(FIXTURES / "restricted-scalar-string" / "artifact.md"))
        self.assertEqual(code, 1, f"expected exit 1, stderr was: {err}")
        self.assertIn(ERR_MSG, err)

    def test_restricted_with_nonempty_list_ai_assistance_used_passes(self):
        code, _, err = run(str(FIXTURES / "restricted-ok" / "artifact.md"))
        self.assertEqual(code, 0, f"expected exit 0, stderr was: {err}")

    def test_not_restricted_with_empty_ai_assistance_used_passes(self):
        code, _, err = run(str(FIXTURES / "true-no-used" / "artifact.md"))
        self.assertEqual(code, 0, f"expected exit 0, stderr was: {err}")


class TestParserTypeAssertions(unittest.TestCase):
    """Verifies the parser returns the Python types the linter rule depends on."""

    def test_restricted_value_parses_as_string(self):
        sys.path.insert(0, str(REPO_ROOT))
        from scripts.lib.frontmatter import parse_file
        fm = parse_file(FIXTURES / "restricted-ok" / "artifact.md")
        self.assertEqual(fm.data["ai_assistance_allowed"], "restricted")

    def test_true_value_parses_as_bool(self):
        sys.path.insert(0, str(REPO_ROOT))
        from scripts.lib.frontmatter import parse_file
        fm = parse_file(FIXTURES / "true-no-used" / "artifact.md")
        self.assertIs(fm.data["ai_assistance_allowed"], True)


if __name__ == "__main__":
    unittest.main()
