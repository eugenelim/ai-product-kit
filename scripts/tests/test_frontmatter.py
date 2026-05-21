"""Contract tests for scripts.lib.frontmatter (F1.2).

Run from repo root:
    python3 -m unittest scripts.tests.test_frontmatter

Running from any other directory will fail with ImportError — the kit has
no pyproject.toml; the module path is rooted at the repo root.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.lib.frontmatter import (
    Frontmatter,
    FrontmatterError,
    parse,
    parse_file,
)


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestScalars(unittest.TestCase):
    def test_parses_string_scalar(self):
        fm = parse("---\nfoo: bar\n---\nbody\n")
        self.assertEqual(fm.data["foo"], "bar")

    def test_parses_quoted_scalar(self):
        fm = parse("---\na: \"double\"\nb: 'single'\n---\n")
        self.assertEqual(fm.data["a"], "double")
        self.assertEqual(fm.data["b"], "single")

    def test_quoted_value_with_inner_quote(self):
        # The old parser mangled "it's" → it' by stripping both quote types
        fm = parse("---\nq: \"it's complicated\"\n---\n")
        self.assertEqual(fm.data["q"], "it's complicated")

    def test_value_with_space_unquoted(self):
        fm = parse("---\nstatus: In Review\n---\n")
        self.assertEqual(fm.data["status"], "In Review")

    def test_value_with_literal_pipe(self):
        # `|` mid-value is a literal pipe, not a block-scalar marker
        fm = parse("---\nai_assistance_allowed: true | restricted | not-allowed\n---\n")
        self.assertEqual(
            fm.data["ai_assistance_allowed"], "true | restricted | not-allowed"
        )

    def test_path_in_value(self):
        fm = parse("---\nparent_intent: ../intents/north-star.md\n---\n")
        self.assertEqual(fm.data["parent_intent"], "../intents/north-star.md")


class TestCoercion(unittest.TestCase):
    def test_parses_int_scalar(self):
        fm = parse("---\nn: 42\n---\n")
        self.assertEqual(fm.data["n"], 42)
        self.assertIsInstance(fm.data["n"], int)

    def test_bool_coercion_native(self):
        # Behavior delta from old parser: bare `true` → bool True (not "true")
        fm = parse("---\nhuman_approval_required: true\nflag: false\n---\n")
        self.assertIs(fm.data["human_approval_required"], True)
        self.assertIs(fm.data["flag"], False)

    def test_null_coercion(self):
        fm = parse("---\nx: null\n---\n")
        self.assertIsNone(fm.data["x"])

    def test_quoted_true_stays_string(self):
        fm = parse('---\nx: "true"\n---\n')
        self.assertEqual(fm.data["x"], "true")
        self.assertIsInstance(fm.data["x"], str)


class TestLists(unittest.TestCase):
    def test_parses_block_list(self):
        src = "---\nrelated_problems:\n  - PROB-001\n  - PROB-002\n---\n"
        fm = parse(src)
        self.assertEqual(fm.data["related_problems"], ["PROB-001", "PROB-002"])

    def test_parses_inline_list(self):
        fm = parse("---\nrelated_personas: [PERS-001, PERS-002, PERS-003]\n---\n")
        self.assertEqual(
            fm.data["related_personas"], ["PERS-001", "PERS-002", "PERS-003"]
        )

    def test_inline_list_with_trailing_comma(self):
        fm = parse("---\nxs: [a, b, c,]\n---\n")
        self.assertEqual(fm.data["xs"], ["a", "b", "c"])


class TestNestedMaps(unittest.TestCase):
    def test_parses_nested_map_one_level(self):
        src = (
            "---\n"
            "outcome:\n"
            "  id: OUT-001\n"
            "  metric: activation\n"
            "---\n"
        )
        fm = parse(src)
        self.assertEqual(fm.data["outcome"], {"id": "OUT-001", "metric": "activation"})

    def test_parses_list_of_maps(self):
        # evidence_basis: depth-2 list-of-maps
        src = (
            "---\n"
            "evidence_basis:\n"
            "  - source: interview\n"
            "    strength: Strong\n"
            "    link: ./i1.md\n"
            "  - source: ticket\n"
            "    strength: Weak\n"
            "    link: ./t1.md\n"
            "---\n"
        )
        fm = parse(src)
        self.assertEqual(len(fm.data["evidence_basis"]), 2)
        self.assertEqual(fm.data["evidence_basis"][0]["source"], "interview")
        self.assertEqual(fm.data["evidence_basis"][0]["strength"], "Strong")
        self.assertEqual(fm.data["evidence_basis"][1]["source"], "ticket")


class TestMultilineScalars(unittest.TestCase):
    def test_handles_pipe_literal_string(self):
        src = (
            "---\n"
            "summary: |\n"
            "  Line one.\n"
            "  Line two.\n"
            "next: bar\n"
            "---\n"
        )
        fm = parse(src)
        self.assertEqual(fm.data["summary"], "Line one.\nLine two.")
        self.assertEqual(fm.data["next"], "bar")

    def test_handles_gt_folded_string(self):
        src = (
            "---\n"
            "summary: >\n"
            "  Line one\n"
            "  continues here.\n"
            "next: bar\n"
            "---\n"
        )
        fm = parse(src)
        # Folded: newlines become spaces; result has single space between
        self.assertIn("Line one", fm.data["summary"])
        self.assertIn("continues here.", fm.data["summary"])
        self.assertNotIn("\n", fm.data["summary"].strip())
        self.assertEqual(fm.data["next"], "bar")


class TestComments(unittest.TestCase):
    def test_preserves_comments_in_raw_block(self):
        src = "---\n# a comment\nfoo: bar\n---\n"
        fm = parse(src)
        self.assertIn("# a comment", fm.raw_block)
        self.assertNotIn("# a comment", repr(fm.data))


class TestEdgeCases(unittest.TestCase):
    def test_returns_none_on_no_frontmatter(self):
        self.assertIsNone(parse("just body text\n"))

    def test_tolerates_unclosed_frontmatter(self):
        # Unclosed: leading --- but no closing ---
        fm = parse("---\nfoo: bar\nno closing line here\n")
        self.assertIsNotNone(fm)
        self.assertEqual(fm.data, {})
        self.assertEqual(fm.raw_block, "")
        self.assertTrue(any("unclosed" in e.lower() for e in fm.parse_errors))

    def test_round_trip_preserves_byte_range(self):
        src = "---\nfoo: bar\n---\nbody\n"
        fm = parse(src)
        start, end = fm.byte_range
        self.assertEqual(src[start:end], fm.raw_block)

    def test_collects_non_fatal_parse_errors(self):
        # Duplicate top-level key
        src = "---\nfoo: a\nfoo: b\n---\n"
        fm = parse(src)
        self.assertEqual(fm.data["foo"], "b")  # last wins
        self.assertTrue(any("duplicate" in e.lower() for e in fm.parse_errors))

    def test_handles_windows_line_endings_crlf(self):
        src = "---\r\nfoo: bar\r\n---\r\nbody\r\n"
        fm = parse(src)
        self.assertIsNotNone(fm)
        self.assertEqual(fm.data["foo"], "bar")

    def test_parse_file_returns_frontmatter_object(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as f:
            f.write("---\nobject_type: Test\n---\nbody\n")
            tmp = Path(f.name)
        try:
            fm = parse_file(tmp)
            self.assertIsNotNone(fm)
            self.assertEqual(fm.data["object_type"], "Test")
        finally:
            tmp.unlink()

    def test_parse_file_returns_none_when_no_frontmatter(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as f:
            f.write("just body\n")
            tmp = Path(f.name)
        try:
            self.assertIsNone(parse_file(tmp))
        finally:
            tmp.unlink()


class TestRegressionCompatWithKit(unittest.TestCase):
    """Compat regression: load every repo .md file with frontmatter via both
    the old _parse_yaml_subset (imported from tools/lint-frontmatter.py) and
    the new library. For every top-level key the OLD parser populated with
    a non-empty value, assert the new lib's value is either:
      (a) identical, or
      (b) a more-precisely-typed version (bool/None/int instead of string), or
      (c) a populated dict where the old parser stored [] for nested maps it
          couldn't parse, or
      (d) a populated list where the old parser stored the raw string for
          inline lists it couldn't parse.
    Any other divergence fails.
    """

    @staticmethod
    def _legacy_parse_yaml_subset(block: str) -> dict:
        """Verbatim snapshot of the pre-F1.2 inline parser body from
        tools/lint-frontmatter.py (pre-migration). Preserved here so the
        regression gate compares against actual old behavior, not the
        migrated tool that now delegates to the new lib.
        """
        out: dict = {}
        current_key = None
        current_list: list | None = None
        for raw in block.splitlines():
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            if raw.startswith("  - ") and current_list is not None:
                current_list.append(raw[4:].strip().strip('"').strip("'"))
                continue
            if raw.startswith("  ") and current_key is not None:
                continue  # nested map — not parsed, just recorded presence
            if ":" in raw:
                key, _, val = raw.partition(":")
                key = key.strip()
                val = val.strip()
                if val == "":
                    current_key = key
                    current_list = []
                    out[key] = current_list
                else:
                    out[key] = val.strip('"').strip("'")
                    current_key = key
                    current_list = None
        return out

    @classmethod
    def _legacy_parse_file(cls, path: Path) -> dict | None:
        """Verbatim snapshot of the pre-F1.2 `parse_frontmatter` from lint-frontmatter."""
        text = path.read_text()
        if not text.startswith("---\n"):
            return None
        end = text.find("\n---\n", 4)
        if end == -1:
            return None
        return cls._legacy_parse_yaml_subset(text[4:end])

    def setUp(self):
        # Compare against the LEGACY parser snapshot (not the migrated tool,
        # which now delegates to the new lib — that would be a vacuous comparison).
        self.old_parse = self._legacy_parse_file

    def _all_md_files(self):
        skips = {".git", "__pycache__", "node_modules", ".worktrees"}
        for p in REPO_ROOT.rglob("*.md"):
            if any(s in p.parts for s in skips):
                continue
            yield p

    def test_existing_kit_files_parse_compatibly(self):
        for path in self._all_md_files():
            try:
                old_fm = self.old_parse(path)
            except Exception:
                continue  # old parser failed; not a regression target
            if old_fm is None:
                continue
            new_fm = parse_file(path)
            if old_fm:  # legacy parser returned non-empty dict
                self.assertIsNotNone(
                    new_fm,
                    f"Regression on {path}: legacy parser found frontmatter "
                    f"(non-empty dict) but new lib returned None.",
                )
            if new_fm is None:
                continue
            for key, old_val in old_fm.items():
                if not old_val and old_val != 0 and old_val is not False:
                    # Old parser stored empty (None, "", [], {}) — new lib may
                    # store something richer (e.g., parsed nested map). Skip.
                    continue
                new_val = new_fm.data.get(key)
                # Accept identical
                if old_val == new_val:
                    continue
                # Accept bool/int/None upgrade from string
                if isinstance(old_val, str) and old_val.lower() in ("true", "false", "null"):
                    expected = {"true": True, "false": False, "null": None}[old_val.lower()]
                    if new_val == expected:
                        continue
                if isinstance(old_val, str) and old_val.isdigit():
                    if new_val == int(old_val):
                        continue
                # Accept list-from-inline-list-string
                if isinstance(old_val, str) and old_val.startswith("[") and isinstance(new_val, list):
                    continue
                # Accept list-of-dicts upgrade (legacy parser truncated list-of-maps
                # to ["first_key: first_value"] at the first `- ` line; new lib
                # parses the full structure)
                if (
                    isinstance(old_val, list)
                    and isinstance(new_val, list)
                    and len(new_val) >= len(old_val)
                    and any(isinstance(item, dict) for item in new_val)
                ):
                    continue
                # Anything else is a regression
                self.fail(
                    f"Regression on {path} key '{key}': "
                    f"old={old_val!r} ({type(old_val).__name__}) "
                    f"new={new_val!r} ({type(new_val).__name__})"
                )


if __name__ == "__main__":
    unittest.main()
