"""Contract tests for scripts/audit-spec-linkage.py (P4.10).

Run from repo root:
    python3 -m pytest scripts/tests/test_audit_spec_linkage.py -v
    python3 -m unittest scripts.tests.test_audit_spec_linkage
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "audit-spec-linkage.py"


def run_script(*args: str, cwd: Path | None = None) -> tuple[int, str, str]:
    """Invoke the script as a subprocess; return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd or REPO_ROOT),
    )
    return result.returncode, result.stdout, result.stderr


def write_initiative(root: Path, slug: str) -> Path:
    """Create delivery/initiatives/<slug>/README.md with valid Initiative frontmatter."""
    d = root / "delivery" / "initiatives" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "README.md").write_text(
        f"---\n"
        f"id: INI-{slug}\n"
        f"slug: {slug}\n"
        f"object_type: Initiative\n"
        f"status: active\n"
        f"last_updated: 2026-05-23\n"
        f"parent_vision: VIS-stub\n"
        f"---\n"
        f"# {slug}\n"
    )
    (d / "specs").mkdir(exist_ok=True)
    return d


def write_spec(
    root: Path,
    initiative_slug: str,
    spec_slug: str,
    parent_initiative: str | None,
) -> Path:
    """Create delivery/initiatives/<i>/specs/<s>.md with optional parent_initiative."""
    p = root / "delivery" / "initiatives" / initiative_slug / "specs" / f"{spec_slug}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    fm_lines = [
        "---",
        f"id: FEAT-{spec_slug}",
        f"slug: {spec_slug}",
        "object_type: Feature",
        "status: Draft",
        "last_updated: 2026-05-23",
    ]
    if parent_initiative is not None:
        fm_lines.append(f"parent_initiative: {parent_initiative}")
    fm_lines.append("---")
    fm_lines.append(f"# {spec_slug}\n")
    p.write_text("\n".join(fm_lines))
    return p


class TestCleanCase(unittest.TestCase):
    def test_clean_verdict_on_well_linked_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            write_initiative(t, "init-a")
            write_spec(t, "init-a", "spec-1", parent_initiative=f"INI-init-a")
            write_spec(t, "init-a", "spec-2", parent_initiative=f"INI-init-a")
            write_spec(t, "init-a", "spec-3", parent_initiative=f"INI-init-a")
            code, out, err = run_script("--root", str(t), "--format", "json")
            self.assertEqual(code, 0, f"expected clean (0); got {code}. stderr: {err}")
            # Strip the three-line header before parsing JSON
            payload = _strip_header(out)
            report = json.loads(payload)
            self.assertEqual(report["frontmatter"]["verdict"], "clean")
            self.assertEqual(report["frontmatter"]["specs_audited"], 3)
            self.assertEqual(report["frontmatter"]["broken_links"], 0)


class TestViolationKinds(unittest.TestCase):
    def test_missing_parent_initiative_flags_violation(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            write_initiative(t, "init-a")
            write_spec(t, "init-a", "spec-1", parent_initiative=f"INI-init-a")
            write_spec(t, "init-a", "spec-2", parent_initiative=f"INI-init-a")
            write_spec(t, "init-a", "spec-missing", parent_initiative=None)
            code, out, err = run_script("--root", str(t), "--format", "json")
            self.assertIn(code, (1, 2), f"expected drift or broken; got {code}. stderr: {err}")
            report = json.loads(_strip_header(out))
            types = {v["violation_type"] for v in report["violations"]}
            self.assertIn("missing-parent-initiative", types)
            slugs = {v["spec_slug"] for v in report["violations"]}
            self.assertIn("spec-missing", slugs)

    def test_dangling_parent_initiative_flags_violation(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            write_initiative(t, "init-a")
            write_spec(t, "init-a", "spec-1", parent_initiative=f"INI-init-a")
            write_spec(t, "init-a", "spec-2", parent_initiative=f"INI-init-a")
            write_spec(t, "init-a", "spec-dangling", parent_initiative="INI-nonexistent")
            code, out, err = run_script("--root", str(t), "--format", "json")
            self.assertIn(code, (1, 2), f"expected drift or broken; got {code}. stderr: {err}")
            report = json.loads(_strip_header(out))
            types = {v["violation_type"] for v in report["violations"]}
            self.assertIn("dangling-parent-initiative", types)
            slugs = {v["spec_slug"] for v in report["violations"]}
            self.assertIn("spec-dangling", slugs)


class TestEdgeCases(unittest.TestCase):
    def test_list_valued_parent_initiative_coerces_to_first_element(self):
        """A YAML list value for parent_initiative should not produce a misleading
        'dangling' violation against the stringified list. After coercion to the
        first element, if that element resolves, the spec is clean."""
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            write_initiative(t, "init-a")
            write_spec(t, "init-a", "spec-1", parent_initiative="INI-init-a")
            write_spec(t, "init-a", "spec-2", parent_initiative="INI-init-a")
            # Raw write a spec whose parent_initiative is a YAML list
            p = t / "delivery" / "initiatives" / "init-a" / "specs" / "spec-list.md"
            p.write_text(
                "---\n"
                "id: FEAT-spec-list\n"
                "slug: spec-list\n"
                "object_type: Feature\n"
                "status: Draft\n"
                "last_updated: 2026-05-23\n"
                "parent_initiative:\n"
                "  - INI-init-a\n"
                "  - INI-other\n"
                "---\n"
                "# spec-list\n"
            )
            code, out, _ = run_script("--root", str(t), "--format", "json")
            report = json.loads(_strip_header(out))
            slugs = {v["spec_slug"] for v in report["violations"]}
            self.assertNotIn(
                "spec-list", slugs,
                "list-valued parent_initiative should coerce to first element and resolve",
            )

    def test_whitespace_only_parent_initiative_is_missing_not_dangling(self):
        """A whitespace-only parent_initiative value is semantically empty; it should
        produce a missing-parent-initiative violation, not dangling-parent-initiative."""
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            write_initiative(t, "init-a")
            write_spec(t, "init-a", "spec-1", parent_initiative="INI-init-a")
            write_spec(t, "init-a", "spec-2", parent_initiative="INI-init-a")
            p = t / "delivery" / "initiatives" / "init-a" / "specs" / "spec-ws.md"
            p.write_text(
                "---\n"
                "id: FEAT-spec-ws\n"
                "slug: spec-ws\n"
                "object_type: Feature\n"
                "status: Draft\n"
                "last_updated: 2026-05-23\n"
                'parent_initiative: "   "\n'
                "---\n"
                "# spec-ws\n"
            )
            code, out, _ = run_script("--root", str(t), "--format", "json")
            report = json.loads(_strip_header(out))
            ws = [v for v in report["violations"] if v["spec_slug"] == "spec-ws"]
            self.assertEqual(len(ws), 1)
            self.assertEqual(ws[0]["violation_type"], "missing-parent-initiative")


class TestScope(unittest.TestCase):
    def test_scope_subtree_limits_audited_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            write_initiative(t, "init-a")
            write_initiative(t, "init-b")
            write_spec(t, "init-a", "spec-a1", parent_initiative="INI-init-a")
            write_spec(t, "init-a", "spec-a2", parent_initiative="INI-init-a")
            write_spec(t, "init-a", "spec-a3", parent_initiative="INI-init-a")
            # init-b has a broken spec — should be excluded when scoped to init-a
            write_spec(t, "init-b", "spec-b1", parent_initiative=None)
            code, out, _ = run_script(
                "--root", str(t), "--scope", "init-a", "--format", "json"
            )
            self.assertEqual(code, 0, "init-a alone is clean")
            report = json.loads(_strip_header(out))
            self.assertEqual(report["frontmatter"]["specs_audited"], 3)
            slugs = {v["spec_slug"] for v in report["violations"]}
            self.assertNotIn("spec-b1", slugs)


class TestWrite(unittest.TestCase):
    def test_write_flag_creates_dated_report_file_and_appends_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            write_initiative(t, "init-a")
            for i in range(3):
                write_spec(t, "init-a", f"spec-{i}", parent_initiative="INI-init-a")
            code, _, _ = run_script("--root", str(t), "--write")
            self.assertEqual(code, 0)
            audits_dir = t / "docs" / "audits"
            self.assertTrue(audits_dir.is_dir())
            reports = list(audits_dir.glob("spec-linkage-*.md"))
            self.assertEqual(len(reports), 1, f"expected exactly one report; got {reports}")
            log = audits_dir / "SPEC-LINKAGE-LOG.md"
            self.assertTrue(log.exists())
            log_text = log.read_text()
            self.assertIn("scope=all", log_text)
            self.assertIn("verdict=clean", log_text)
            # The persisted report MUST NOT include the three-line stdout header
            report_text = reports[0].read_text()
            self.assertFalse(
                report_text.lstrip().startswith("PHASE:"),
                "persisted report must not begin with the three-line stdout header",
            )


class TestJsonShape(unittest.TestCase):
    def test_json_output_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            write_initiative(t, "init-a")
            for i in range(3):
                write_spec(t, "init-a", f"spec-{i}", parent_initiative="INI-init-a")
            code, out, _ = run_script("--root", str(t), "--format", "json")
            self.assertEqual(code, 0)
            report = json.loads(_strip_header(out))
            self.assertIn("frontmatter", report)
            self.assertIn("violations", report)
            self.assertIn("orphans", report)
            fm = report["frontmatter"]
            for key in ("date", "scope", "specs_audited", "broken_links", "verdict"):
                self.assertIn(key, fm)


class TestInsufficientData(unittest.TestCase):
    def test_insufficient_data_verdict_on_small_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            write_initiative(t, "init-a")
            # Only 2 specs — under the 3-spec threshold
            write_spec(t, "init-a", "spec-1", parent_initiative="INI-init-a")
            write_spec(t, "init-a", "spec-2", parent_initiative="INI-init-a")
            code, out, _ = run_script("--root", str(t), "--format", "json")
            self.assertEqual(code, 3, "fewer than 3 specs in scope → insufficient-data")
            report = json.loads(_strip_header(out))
            self.assertEqual(report["frontmatter"]["verdict"], "insufficient-data")

    def test_clean_verdict_when_no_specs_in_scope_is_insufficient_data_not_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            # Initiative present, zero specs
            write_initiative(t, "init-a")
            write_initiative(t, "init-b")
            write_initiative(t, "init-c")
            code, out, _ = run_script("--root", str(t), "--format", "json")
            self.assertEqual(code, 3, "zero specs MUST be insufficient-data, not clean")
            report = json.loads(_strip_header(out))
            self.assertEqual(report["frontmatter"]["verdict"], "insufficient-data")


class TestStdoutHeader(unittest.TestCase):
    def test_stdout_header_present_before_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            write_initiative(t, "init-a")
            for i in range(3):
                write_spec(t, "init-a", f"spec-{i}", parent_initiative="INI-init-a")
            code, out, _ = run_script("--root", str(t), "--format", "markdown")
            lines = out.splitlines()
            self.assertTrue(lines[0].startswith("PHASE: "))
            self.assertTrue(lines[1].startswith("VERDICT: "))
            self.assertTrue(lines[2].startswith("NEXT: "))


def _strip_header(stdout: str) -> str:
    """Strip the three-line PHASE/VERDICT/NEXT header (and any blank separator) before JSON/markdown payload."""
    lines = stdout.splitlines()
    # First three labelled lines are the header. Drop them, plus a single trailing blank.
    if len(lines) >= 3 and lines[0].startswith("PHASE:") and lines[1].startswith("VERDICT:") and lines[2].startswith("NEXT:"):
        body = lines[3:]
        if body and body[0] == "":
            body = body[1:]
        return "\n".join(body)
    return stdout


if __name__ == "__main__":
    unittest.main()
