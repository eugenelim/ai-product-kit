# Plan: frontmatter-parser

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

## Approach

Write `scripts/lib/frontmatter.py` as a stdlib-only parser, designed against the contract tests first (TDD). The parser is a small state machine over the frontmatter block: track current key, current list (if any), current nested-map (if any), current quoted state. Kit frontmatter is small (~30 fields, ~5-line average per artifact) so performance is not a concern — readability wins.

Reference points:
1. `tools/lint-frontmatter.py:_parse_yaml_subset()` lines 87-113 — the inline version the new lib must subsume.
2. Real kit frontmatter usage across `.claude/agents/*.md`, `.claude/commands/*.md`, `.claude/hooks/*.md`, and the example blocks in `docs/HANDOVERS.md`.

Tests drive implementation: write the regression test first, confirm it passes on the OLD parser (via temporarily importing `_parse_yaml_subset`), then write the new lib, then confirm the regression test passes against the new lib.

## Constraints

- Stdlib only.
- ≤ ~250 LOC for the library.
- Lib is read-only; doesn't write files. Migration of `lint-frontmatter.py` is Task 3.

## Tasks

### Task 1: Write `scripts/tests/test_frontmatter.py` with all contract tests (red)

- **Depends on:** none
- **Tests:** all 14 named contract tests from spec §Contract tests. The regression test walks the repo.
- **Approach:**
  - Create `scripts/lib/__init__.py`, `scripts/tests/__init__.py`, `scripts/tests/test_frontmatter.py`.
  - Each test is a `unittest.TestCase` method. Inline-string fixtures for most; the regression test walks the repo.
  - Tests assume `scripts.lib.frontmatter.parse(str)` and `parse_file(Path)` exist; the suite fails ImportError until Task 2 lands.
- **Done when:** `python3 -m unittest scripts.tests.test_frontmatter` runs and reports 14 errors/failures.

### Task 2: Implement `scripts/lib/frontmatter.py` (green)

- **Depends on:** Task 1.
- **Tests:** all Task 1 tests pass.
- **Approach:**
  - `@dataclass Frontmatter` per spec.
  - `FrontmatterError(Exception)`.
  - `parse(source: str) -> Optional[Frontmatter]` — returns None if no leading `---\n...\n---\n`.
  - `parse_file(path: Path) -> Optional[Frontmatter]`.
  - Internal `_parse_block(block: str) -> tuple[dict, list[str]]` — line-by-line state machine: scalars, block lists, inline lists, nested-map markers (record key with parsed sub-dict at one level), quoted strings, comments, `|` literal, `>` folded.
  - Coercion: bare `true`/`false`/`null` → bool/None; integers → int; quoted always str.
- **Done when:** `python3 -m unittest scripts.tests.test_frontmatter` exits 0.

### Task 3: Migrate `tools/lint-frontmatter.py` to use the library

- **Depends on:** Task 2.
- **Tests:**
  - Before-migration baseline: capture `python3 tools/lint-frontmatter.py --all; echo $?` exit code (currently 0).
  - After-migration: same command, same exit code.
  - The `human_approval_required` check (line ~144 of `lint-frontmatter.py`) updated from `fm.get("human_approval_required") == "true"` to `fm.get("human_approval_required") is True` (per the spec's documented coercion change).
- **Approach:**
  - Add `sys.path` insert at top of `tools/lint-frontmatter.py`: `sys.path.insert(0, str(Path(__file__).resolve().parent.parent))` so it can `from scripts.lib.frontmatter import parse_file`. (Rationale: the kit has no `pyproject.toml`; the sys.path insert is the simplest portable approach. F1.4-F1.7 replicate this pattern.)
  - Replace `parse_frontmatter()` and `_parse_yaml_subset()` body with delegation to the lib.
  - Update the `human_approval_required` truthy check per spec.
  - Keep all lifecycle-state / ontology-type / required-field checks in place.
- **Done when:** migration tests pass; `python3 tools/lint-frontmatter.py --all` exits 0.

## Rollout

- F1.3, F1.4, F1.5, F1.6, F1.7 import `from scripts.lib.frontmatter import parse_file`.
- The `_parse_yaml_subset` in `lint-frontmatter.py` is removed.
- ROADMAP F1.2 checked off. INVENTORY: no new row (shared infra).
- `.gitkeep` in `scripts/lib/` removed.

## Risks

- **Behavioral drift between old inline parser and new lib.** Regression test (`test_existing_kit_files_parse_compatibly`) mitigates by enumerating acceptable upgrades and failing on anything else.
- **Parser too permissive.** The `test_collects_non_fatal_parse_errors` test covers: duplicate top-level key, value that looks like a nested key but is at top level (e.g., `key value:` without colon discipline), tab-indented list item (tab vs space ambiguity — recorded as a parse_error, not silently parsed).
- **Tab characters in fixtures.** Old parser uses two-space indent; tabs fail in both. Pre-existing; new lib treats tab as a parse_error so the failure is visible.
- **Invocation context for unittest.** Tests assume `python3 -m unittest scripts.tests.test_frontmatter` is run from the repo root. The kit has no `pyproject.toml`. Document this in the test module's docstring: "Run from repo root: `python3 -m unittest scripts.tests.test_frontmatter`. Running from `scripts/` will fail with ImportError."

## Changelog

- 2026-05-21: Initial plan.
