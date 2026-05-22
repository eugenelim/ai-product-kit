# Plan: lint-frontmatter-ai-assistance-allowed

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** approved

> **Plan contract.** Tiny code change; the bulk of the work is fixtures and tests.

## Approach

Python edit + four small markdown fixtures + four tests. Tests come before code (TDD). The new rule lives in `lint_file()` immediately after the existing `human_approval_required` block, so future readers see the two policy guards as a pair.

## Constraints

- Stdlib only (no new dependencies).
- Linter total length stays under 200 lines (currently 175).
- Test fixtures must be valid markdown with frontmatter that satisfies the universal-required fields (`object_type`, `status`, `last_updated`) — otherwise the existing rules fire and confuse the new test's signal.

## Tasks

### Task 1: locate or scaffold the linter test harness

- **Depends on:** none
- **Tests:**
  - Discover whether `scripts/tests/test_lint_frontmatter.py` exists; if not, create one using the subprocess-invocation pattern from existing `scripts/tests/test_audit_*.py`.
- **Approach:**
  - Glob `scripts/tests/test_lint_frontmatter*` — if a file exists, extend it; otherwise create.
  - The harness invokes `python3 tools/lint-frontmatter.py <fixture-path>` as a subprocess and asserts on exit code + stderr substring.
- **Done when:** the harness file is in place and runs (even if empty).

### Task 2: write the five fixtures + five tests (red)

- **Depends on:** Task 1
- **Tests:** the tests themselves are the deliverable.
- **Approach:**
  - Create `scripts/tests/fixtures/lint-frontmatter/restricted-missing/artifact.md` — frontmatter with `ai_assistance_allowed: restricted` and no `ai_assistance_used`; plus the universal-required fields (`object_type`, `status`, `last_updated`) set to satisfy existing rules.
  - Create `restricted-empty/artifact.md` — same plus `ai_assistance_used: []`.
  - Create `restricted-scalar-string/artifact.md` — same plus `ai_assistance_used: "drafted prose"` (string, not list — closes the non-list-type gap).
  - Create `restricted-ok/artifact.md` — same plus `ai_assistance_used: ["drafted prose"]`.
  - Create `true-no-used/artifact.md` — `ai_assistance_allowed: true` (YAML boolean) with no `ai_assistance_used`.
  - **Parser-type assertion:** add a small unit test that reads the `restricted-ok` and `true-no-used` fixtures via `scripts.lib.frontmatter.parse_file` and asserts: `parsed["ai_assistance_allowed"] == "restricted"` (string) for restricted-ok; `parsed["ai_assistance_allowed"] is True` (bool) for true-no-used. If the parser coerces or quotes either value, the spec's logic breaks and the implementer must surface that as a finding before proceeding.
  - Write the five contract tests per the spec.
  - Run them — first three fail (rule not implemented); latter two should pass already.
- **Done when:** test file runs; first three tests fail as expected; latter two pass; parser-type assertion passes.

### Task 3: implement the rule (green)

- **Depends on:** Task 2
- **Tests:** all five from Task 2 pass.
- **Approach:**
  - In `tools/lint-frontmatter.py`, immediately after the `human_approval_required` block, add:
    ```python
    if fm.get("ai_assistance_allowed") == "restricted":
        aiu = fm.get("ai_assistance_used")
        if not aiu or not isinstance(aiu, list) or len(aiu) == 0:
            errors.append(
                f"{path}: ai_assistance_allowed: restricted requires "
                f"ai_assistance_used: list to be non-empty"
            )
    ```
  - Note the strengthened check: `not isinstance(aiu, list)` rejects scalar strings, dicts, ints — anything non-list. This deliberately diverges from the existing `human_approval_required` rule's shape (which has the same latent bug); the divergence is recorded in Task 5.
- **Done when:** all five tests pass; `tools/pre-pr.sh` exits 0.

### Task 4: regression check against the live kit

- **Depends on:** Task 3
- **Tests:** `python3 tools/lint-frontmatter.py --all` exits 0.
- **Approach:**
  - Run the linter against every artifact under PHASE_DIRS.
  - Expected: exit 0. If it does not, log the failing artifact path as a finding and address it in a separate commit before merging this PR — do NOT silently relax the rule.
- **Done when:** linter exits 0 against the kit, OR the failing artifact is fixed in a separate commit.

### Task 5: update INVENTORY + record the deferred existing-rule fix

- **Depends on:** Task 3
- **Tests:**
  - `grep -nE "ai_assistance_allowed" docs/INVENTORY.md` returns ≥1 hit.
  - `grep -c "F0.14" ROADMAP.md` returns ≥1 hit (the defer is tracked as a new ROADMAP item).
- **Approach:**
  - In the `tools/lint-frontmatter.py` row of the "Linters (kit-meta)" table, append "+ `ai_assistance_allowed: restricted` ⇒ non-empty `ai_assistance_used` (list)" to the Rules cell.
  - Add `F0.14` to ROADMAP under the Foundation 0-X section (`lint-frontmatter-non-list-retrofit`), naming F0.12-D1 as the source.
  - Local working detail in `notes/deferred-findings.md` (gitignored per `docs/specs/**/notes/`) — session scratch only.
- **Done when:** both tests pass.

## Rollout

- The new rule is automatically wired via `tools/pre-pr.sh` (which already runs `lint-frontmatter.py --all`) and `.github/workflows/lint.yml`.
- INVENTORY.md row for `tools/lint-frontmatter.py` gets a rules-cell update via Task 5.
- ROADMAP.md F0.12 row checked off in CAPTURE.

## Risks

- **Existing shipped artifacts violate the new rule.** Mitigation: Task 4 verifies against `--all`. If a violation appears, log it as a finding and either fix the artifact in this PR or defer per work-loop scope discipline.
- **`ai_assistance_allowed` parsed as YAML boolean.** The value `true` is YAML-true (a boolean); the value `restricted` is a string. The check uses `== "restricted"`, which won't match a YAML-boolean True. Mitigation: the frontmatter parser returns the value as it parses — verify in Task 2 that the `true-no-used` fixture is correctly parsed (likely returns Python `True`, which won't equal `"restricted"`, so the rule won't fire — correct behavior).

## Changelog

-
