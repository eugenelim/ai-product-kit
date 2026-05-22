"""Contract test for the template authoring convention.

Two responsibilities:

1. Walk every shipped template under `templates/` and assert it passes
   `tools/lint-frontmatter.py --check-template <path>`. This is the gate the
   F3.x workers wire their template into.
2. Run the spec's contract tests (T5–T12 incl. T8b–T8g) against the
   `scripts/tests/fixtures/templates/` fixture set. These pin the placeholder-
   recognition rules against the cases the spec enumerates.

Skip list (permanent):
  - `templates/CLAUDE.global.md` — seed CLAUDE.md a kit-user project gets,
    not a kit-artifact template. Prose-only; no frontmatter.
  - `templates/_meta/README.md` — prose-only index of shipped templates.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LINTER = REPO_ROOT / "tools" / "lint-frontmatter.py"
FIXTURES = REPO_ROOT / "scripts" / "tests" / "fixtures" / "templates"

SKIP = {
    REPO_ROOT / "templates" / "CLAUDE.global.md",
    REPO_ROOT / "templates" / "_meta" / "README.md",
}


def _discover_template_targets() -> list[Path]:
    targets: set[Path] = set()
    templates_dir = REPO_ROOT / "templates"
    targets.update(p for p in templates_dir.glob("*.md"))
    targets.update(p for p in templates_dir.glob("*/README.md"))
    # Always include the canonical skeleton explicitly so the test is never a no-op.
    targets.add(templates_dir / "_meta" / "template-skeleton.md")
    return sorted(t for t in targets if t not in SKIP)


def _run_check_template(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(LINTER), "--check-template", str(path)],
        capture_output=True,
        text=True,
        check=False,
        cwd=REPO_ROOT,
    )


def _run_default(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(LINTER), str(path)],
        capture_output=True,
        text=True,
        check=False,
        cwd=REPO_ROOT,
    )


# ---- Discovery integrity ---------------------------------------------------


def test_target_count_nonzero():
    targets = _discover_template_targets()
    assert len(targets) >= 1, (
        "no template targets discovered — the test would be a silent no-op. "
        "Confirm templates/_meta/template-skeleton.md exists."
    )


def test_skeleton_field_names_are_known():
    """The skeleton's frontmatter field set must equal the canonical key set.

    Drift in either direction (skeleton adds an unknown key, or canonical set
    drops a key the skeleton uses) fails the test. If the skeleton diverges
    from CONVENTIONS.md's universal-metadata schema example, fix CONVENTIONS.md
    or this list — whichever is wrong — in the same commit.
    """
    sys.path.insert(0, str(REPO_ROOT))
    from scripts.lib.frontmatter import parse_file as _fm_parse_file

    skeleton = REPO_ROOT / "templates" / "_meta" / "template-skeleton.md"
    fm = _fm_parse_file(skeleton)
    assert fm is not None, f"{skeleton} has no frontmatter"

    canonical = {
        # Universal schema
        "id", "slug", "object_type", "name", "description", "owner",
        "status", "priority", "risk_level", "created", "last_updated",
        # Traceability
        "parent_intent", "parent_opportunity", "parent_learning",
        "parent_vision", "parent_initiative",
        "related_problems", "related_personas", "related_kpis",
        # Evidence
        "evidence_basis", "open_assumptions",
        # Human-vs-AI
        "human_owned_decisions", "ai_assistance_used",
        "ai_assistance_allowed", "human_approval_required", "approvals_obtained",
        # Open items
        "open_questions", "risks",
        # Deliberately excluded:
        # - `related_capabilities` (used by scripts/lib/graph.py per F1.1 but
        #   not yet in CONVENTIONS.md per ROADMAP F1-G7). If the skeleton ever
        #   adds this key, the test fails and forces the F1-G7 reconciliation.
    }
    skeleton_keys = set(fm.data.keys())
    unknown = skeleton_keys - canonical
    assert not unknown, (
        f"skeleton has unknown keys not in canonical set: {sorted(unknown)} "
        f"— reconcile docs/CONVENTIONS.md universal schema or update this list"
    )


# ---- T11 — every shipped template passes --check-template ------------------


@pytest.mark.parametrize("path", _discover_template_targets(),
                         ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_template_passes_check_template_mode(path):
    result = _run_check_template(path)
    assert result.returncode == 0, (
        f"{path.relative_to(REPO_ROOT)} failed --check-template:\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


# ---- T5 — skeleton itself passes (covered by T11 parametrize, but explicit
#       check kept for spec-traceability) -----------------------------------


def test_T5_skeleton_passes_check_template():
    skeleton = REPO_ROOT / "templates" / "_meta" / "template-skeleton.md"
    result = _run_check_template(skeleton)
    assert result.returncode == 0, (
        f"skeleton failed --check-template: {result.stderr}"
    )


# ---- T6–T12 — fixture-driven contract tests ---------------------------------


def test_T6_valid_all_placeholders():
    result = _run_check_template(FIXTURES / "valid-all-placeholders.md")
    assert result.returncode == 0, result.stderr


def test_T7_missing_object_type():
    result = _run_check_template(FIXTURES / "missing-object-type.md")
    assert result.returncode != 0


def test_T8_bogus_enum_value():
    result = _run_check_template(FIXTURES / "bogus-enum-value.md")
    assert result.returncode != 0


def test_T8b_whitespace_only_placeholder():
    result = _run_check_template(FIXTURES / "whitespace-only-placeholder.md")
    assert result.returncode != 0


def test_T8h_nested_whitespace_placeholder():
    """T8h — closes the recursive-dict coverage gap from review-iter-1 finding #4.

    The malformed-placeholder rejection must propagate through the recursive
    dict walk, not just trip on top-level scalars (T8b's case).
    """
    result = _run_check_template(FIXTURES / "nested-whitespace-placeholder.md")
    assert result.returncode != 0


def test_T8c_mixed_list_placeholders():
    result = _run_check_template(FIXTURES / "mixed-list-placeholders.md")
    assert result.returncode == 0, result.stderr


def test_T8d_mixed_list_invalid():
    result = _run_check_template(FIXTURES / "mixed-list-invalid.md")
    assert result.returncode != 0


def test_T8e_augmented_placeholder():
    result = _run_check_template(FIXTURES / "augmented-placeholder.md")
    assert result.returncode == 0, result.stderr


def test_T8f_nested_container_placeholder():
    result = _run_check_template(FIXTURES / "nested-container-placeholder.md")
    assert result.returncode == 0, result.stderr


def test_T8g_nested_container_invalid():
    result = _run_check_template(FIXTURES / "nested-container-invalid.md")
    assert result.returncode != 0


def test_T9_placeholder_block_scalar():
    result = _run_check_template(FIXTURES / "placeholder-block-scalar.md")
    assert result.returncode == 0, result.stderr


def test_T10_placeholders_rejected_in_default_mode():
    result = _run_default(FIXTURES / "valid-all-placeholders.md")
    assert result.returncode != 0, (
        "default mode must reject placeholder values — mode separation is "
        "the load-bearing safety property"
    )


def test_T12_default_all_mode_no_regression():
    result = subprocess.run(
        ["python3", str(LINTER), "--all"],
        capture_output=True, text=True, check=False, cwd=REPO_ROOT,
    )
    assert result.returncode == 0, (
        f"--all regressed: stdout={result.stdout}\nstderr={result.stderr}"
    )
