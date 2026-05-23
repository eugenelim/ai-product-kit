"""Contract tests for the Phase-4 template-fill command convention.

See: docs/specs/phase-4-command-convention/spec.md (§"Outputs" item 4) and
     docs/CONVENTIONS.md §"Phase-4 Template-Fill Commands — `.claude/commands/draft-*.md` and siblings".

The seven in-scope commands ship via the F4 fan-out (ROADMAP P4.1, P4.3, P4.4,
P4.5, P4.6, P4.8, P4.11). At the time this test module ships, none of the seven
exist; the parametrized inscope tests therefore auto-skip via pytest.skip and
tighten as each worker lands its command file.

Run from any cwd:
    python3 -m pytest scripts/tests/test_phase4_command_shape.py -v
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMANDS_DIR = REPO_ROOT / ".claude" / "commands"
SKELETON_PATH = COMMANDS_DIR / "_meta" / "command-skeleton.md"
LINT_COMMAND = REPO_ROOT / "tools" / "lint-command.sh"

# The seven in-scope template-fill commands. Order matches the chain:
# draft-vision → draft-initiative → (context-map, end-to-end-flow,
# sequence-initiative) → draft-spec → handoff-packet.
INSCOPE = [
    "draft-vision",
    "draft-initiative",
    "context-map",
    "end-to-end-flow",
    "sequence-initiative",
    "draft-spec",
    "handoff-packet",
]

# Per-command expected positional argument token in `argument-hint:`.
# Creating commands take a new-artifact slug; augmenting commands take the
# existing initiative folder's slug.
POSITIONAL = {
    "draft-vision": "<slug>",
    "draft-initiative": "<slug>",
    "context-map": "<initiative-slug>",
    "end-to-end-flow": "<initiative-slug>",
    "sequence-initiative": "<initiative-slug>",
    "draft-spec": "<slug>",
    "handoff-packet": "<slug>",
}

REQUIRED_H2S = [
    "## When to run",
    "## Inputs",
    "## Procedure",
    "## What this command will not do",
]


def _command_path(name: str) -> Path:
    return COMMANDS_DIR / f"{name}.md"


def _skip_if_missing(name: str) -> Path:
    path = _command_path(name)
    if not path.exists():
        pytest.skip(f"{name}: not yet shipped at .claude/commands/{name}.md")
    return path


def _frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    if end < 0:
        return ""
    return text[4:end]


def _body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end < 0:
        return text
    return text[end + 5 :]


def test_skeleton_passes_lint_command() -> None:
    result = subprocess.run(
        ["bash", str(LINT_COMMAND), str(SKELETON_PATH)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, (
        f"lint-command.sh failed on skeleton:\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_skeleton_uses_placeholder_h1() -> None:
    text = SKELETON_PATH.read_text(encoding="utf-8")
    h1_lines = [ln for ln in text.splitlines() if ln.startswith("# /")]
    assert h1_lines, "skeleton has no H1 starting with '# /'"
    assert any("<command-name>" in ln for ln in h1_lines), (
        f"skeleton H1 does not use the <command-name> placeholder; "
        f"found H1 lines: {h1_lines}"
    )


def test_inscope_count_is_seven() -> None:
    assert len(INSCOPE) == 7, f"INSCOPE has {len(INSCOPE)} entries, expected 7"
    assert len(POSITIONAL) == 7, (
        f"POSITIONAL has {len(POSITIONAL)} entries, expected 7"
    )
    assert set(INSCOPE) == set(POSITIONAL.keys()), (
        "INSCOPE and POSITIONAL keys diverged"
    )


@pytest.mark.parametrize("name", INSCOPE)
def test_inscope_commands_pass_lint(name: str) -> None:
    path = _skip_if_missing(name)
    result = subprocess.run(
        ["bash", str(LINT_COMMAND), str(path)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, (
        f"lint-command.sh failed on {name}:\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


@pytest.mark.parametrize("name", INSCOPE)
def test_inscope_commands_have_required_h2s(name: str) -> None:
    path = _skip_if_missing(name)
    body = _body(path)
    missing = [h2 for h2 in REQUIRED_H2S if h2 not in body]
    assert not missing, (
        f"{name}: missing required H2 section(s): {missing}"
    )


@pytest.mark.parametrize("name", INSCOPE)
def test_inscope_commands_declare_argv(name: str) -> None:
    path = _skip_if_missing(name)
    fm = _frontmatter(path)
    match = re.search(r"^argument-hint:\s*(.+)$", fm, re.MULTILINE)
    assert match, f"{name}: no argument-hint: in frontmatter"
    hint = match.group(1).strip()
    expected = POSITIONAL[name]
    assert hint.startswith(expected), (
        f"{name}: argument-hint must start with {expected!r}; got {hint!r}"
    )


@pytest.mark.parametrize("name", INSCOPE)
def test_inscope_commands_cite_template_path(name: str) -> None:
    path = _skip_if_missing(name)
    body = _body(path)
    matches = re.findall(r"templates/(?:[a-z0-9-]+/)*[a-z0-9-]+(?:\.md|/)", body)
    assert matches, (
        f"{name}: body cites no `templates/<name>.md` or `templates/<name>/` path"
    )
    found_existing = False
    for cited in matches:
        candidate = REPO_ROOT / cited.rstrip("/")
        if candidate.exists():
            found_existing = True
            break
    assert found_existing, (
        f"{name}: cites template path(s) {matches} but none exist on disk"
    )


@pytest.mark.parametrize("name", INSCOPE)
def test_inscope_commands_cite_destination_path(name: str) -> None:
    path = _skip_if_missing(name)
    body = _body(path)
    matches = re.findall(r"delivery/[a-z0-9-]+/", body)
    assert matches, (
        f"{name}: body cites no `delivery/<family>/` destination path"
    )
    found_existing = False
    for cited in matches:
        family_dir = REPO_ROOT / cited
        if family_dir.is_dir():
            found_existing = True
            break
    assert found_existing, (
        f"{name}: cites destination path(s) {matches} but none exist as a "
        f"directory under the repo root"
    )
