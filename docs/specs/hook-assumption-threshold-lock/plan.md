# Plan: hook-assumption-threshold-lock

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** approved

## Approach

Single-file Python entry point at `scripts/check-assumption-threshold.py`. The hook doc is already the contract — the script implements it without re-deriving it.

The check is a straight pipeline:

1. Parse stdin JSON.
2. Match `tool_input.file_path` against `validation/experiments/**/results.md` (recursive); if no match, exit 0.
3. Resolve `experiment.md` in the same directory; if absent, block.
4. Parse its frontmatter; check `predeclared_threshold.success` + `.falsification` + `predeclared_at`.
5. Compare `predeclared_at` to today; reject futures.
6. Compare `os.path.getmtime(experiment.md)` to `time.time()`; design must be ≥ 1s older.
7. Override-path branch: if `override_threshold_lock: true`, validate the override fields are non-empty, append to OVERRIDE-LOG, exit 0.

Tests come first. Fixtures are constructed in a per-test `tmp_path` because the mtime is part of the contract — must control file ages precisely with `os.utime`.

## Constraints

- Python stdlib + `scripts.lib.frontmatter` only.
- ≤ 250 LOC.
- Top-level try/except catches everything → exit 0 + stderr trace (never brick a session).
- Append to OVERRIDE-LOG using `with open(..., "a")` (atomic enough for single-writer; concurrent-write hardening is D14).

## Tasks

### Task 1: Path matcher + experiment.md resolver

- **Depends on:** none.
- **Tests:**
  - `test_path_outside_glob_passes_silently`
  - `test_blocks_when_experiment_md_missing` (path matches, but sibling absent)
  - `test_recursive_path_matches_nested_experiment_dir`
- **Approach:**
  - `match_results_path(path: str) -> Path | None` returns the directory containing the results file, or None if out-of-glob.
  - Matcher uses recursive glob — pattern compiles to `re.compile(r'(^|/)validation/experiments/.+/results\.md$')` (at least one path segment between `experiments/` and `results.md`, possibly more).
  - `resolve_experiment_md(dir: Path) -> Path | None`.
- **Done when:** 3 tests pass.

### Task 2: Threshold-presence checks

- **Depends on:** Task 1.
- **Tests:**
  - `test_blocks_when_predeclared_threshold_missing`
  - `test_blocks_when_only_success_criterion_present`
  - `test_blocks_when_only_falsification_criterion_present`
  - `test_blocks_when_predeclared_at_missing`
  - `test_malformed_design_frontmatter_blocks_with_clear_reason`
  - `test_no_frontmatter_delimiters_blocks_with_clear_reason`
- **Approach:**
  - `check_threshold_fields(fm: dict) -> str | None` returning None on pass, a reason string on fail.
  - Each missing field produces a specific reason (the failure is observable in the block message).
  - `parse_file()` returns None when the file has no `---` delimiters; treat as distinct from a malformed-YAML case (which returns a Frontmatter with empty `data` + `parse_errors`).
- **Done when:** 6 tests pass.

### Task 3: Timestamp checks

- **Depends on:** Task 2.
- **Tests:**
  - `test_blocks_when_predeclared_at_after_today`
  - `test_blocks_when_design_mtime_is_after_results_write`
  - `test_allows_write_when_design_predates_with_full_threshold`
- **Approach:**
  - `check_predeclared_at(date_str: str) -> str | None` — parse via `datetime.date.fromisoformat`; reject if > today.
  - `check_mtime(experiment_path: Path) -> str | None` — design must be ≥ 1s older than `time.time()`.
  - In tests, use `os.utime` to plant precise mtimes.
- **Done when:** 3 tests pass.

### Task 4: Override path

- **Depends on:** Task 3.
- **Tests:**
  - `test_override_allows_write_and_appends_to_override_log`
  - `test_override_without_reason_blocks`
  - `test_override_without_authorizer_blocks`
  - `test_override_threshold_lock_false_does_not_unblock`
- **Approach:**
  - Override path runs *before* the threshold checks. Required override fields: `override_threshold_lock is True` (strict equality, not truthy — `false`, `None`, `0`, `"true"` string all fail the check), `override_reason` (non-empty), `override_authorized_by` (non-empty), `override_authorized_at` (non-empty; format not validated — honor-system per Non-goals).
  - Append a single line to `<repo-root>/validation/experiments/OVERRIDE-LOG.md` formatted: `- <YYYY-MM-DD> <experiment-id> override_authorized_by=<name> reason="<reason>"`.
  - If the log file doesn't exist, create with a one-line H1 + empty list, then append.
- **Done when:** 4 tests pass.

### Task 5: Entry point + JSON protocol

- **Depends on:** Tasks 1–4.
- **Tests:**
  - Subprocess test: pipe JSON to the script; assert exit code and stdout JSON shape on a known-bad and known-good fixture.
- **Approach:**
  - `if __name__ == "__main__":` reads stdin, calls `check(payload) -> (exit_code, stdout_str, stderr_str)`, writes per the hook protocol, exits.
- **Done when:** the subprocess test passes.

### Task 6: Verify against existing hook doc

- **Depends on:** Tasks 1–5.
- **Tests:** `bash tools/lint-hook.sh .claude/hooks/assumption-threshold-lock.md` exits 0 (the existing doc must already pass once F0.10 ships).
- **Approach:** spot-check that script behavior matches the doc — if any divergence, surface it via Open Question. No code change unless divergence found.
- **Done when:** the lint passes and a manual diff against the doc surfaces no discrepancies.

### Task 7: Update reference docs (CAPTURE)

- **Depends on:** Tasks 1–6.
- **Tests:** none.
- **Approach:**
  - `AGENTS.md` — update the "Don't write experiment results without a predeclared threshold" line to drop the "*(planned)*" qualifier on this hook.
  - `docs/INVENTORY.md` — add a row under hooks (the doc already exists; this row now reflects script-shipped status).
  - `ROADMAP.md` — check off F2.2, append `**Shipped:** <date>`.
- **Done when:** all three edits land.

## Rollout

- F2.6 wires the hook into `.claude/settings.json` matcher `Write` → `validation/experiments/**/results.md`. Until that ships, this script is shippable but inert in real sessions.
- **CAPTURE task adds:** edit `.claude/hooks/assumption-threshold-lock.md` to insert step (c) "Confirms `predeclared_at:` is on or before today" between current steps 2 and 3 of the numbered list. Spec/script and doc must agree.
- D14 stays open for the hardening pass.

## Risks

- **Mtime is honor-system.** A motivated author can backdate via `touch -t`. The spec acknowledges this; D14 introduces git-commit-based ordering. Mitigation here: nothing — accepted limitation.
- **OVERRIDE-LOG concurrent append.** Two concurrent overrides could interleave. Single-user single-session is the realistic case for the kit; D14 covers concurrent-write.
- **Hook doc drift.** If someone edits `.claude/hooks/assumption-threshold-lock.md` mid-build, the script may stop matching its contract. Mitigation: Task 6 is an explicit diff check; surface drift as a Open Question.

## Changelog

- 2026-05-21: Initial plan.
- 2026-05-21: Addressed adversarial review (10 findings). Path glob upgraded to `**/` (recursive) to match hook doc. `predeclared_at` check now explicitly documented as a doc extension, with CAPTURE-phase doc update. Added `override_threshold_lock_false_does_not_unblock` and `override_without_authorizer_blocks` contract tests; required `is True` (strict) check. Added `no_frontmatter_delimiters` test distinct from malformed-YAML. Added symlink-mtime and `object_type` non-goals as known limitations. Added F0.10 dependency.
- 2026-05-21: Shipped. `scripts/check-assumption-threshold.py` (241 LOC, stdlib + `scripts.lib.frontmatter` only) and `scripts/tests/test_check_assumption_threshold.py` (18 tests = 15 contract tests + 1 nested-path glob test + 2 subprocess entry-point tests) both green via `python3 -m unittest scripts.tests.test_check_assumption_threshold`. `tools/lint-hook.sh .claude/hooks/assumption-threshold-lock.md` and `tools/pre-pr.sh` exit 0. `.claude/hooks/assumption-threshold-lock.md` "What it does" list amended to insert the `predeclared_at <= today` check between former steps 2 and 3 (now five numbered steps instead of four). Script is inert until F2.6 wires it into `.claude/settings.json`.
