# Plan: tool-lint-hook

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** pending

## Approach

Mirror `tools/lint-skill.sh` exactly in structure: `set -euo pipefail`, an `ERRORS` counter, stderr-only error reporting, `exit 1` on any error. Replace the rule body with the four hook-doc rules from the spec. No new language — pure bash + grep/awk.

Order of work: build the linter against the only existing hook doc (`.claude/hooks/assumption-threshold-lock.md`); write the test harness with one fixture per rule; wire the call sites in `tools/pre-pr.sh` and `.github/workflows/lint.yml`.

## Constraints

- Bash + coreutils (grep, awk, wc, head) only. No Python, no jq, no curl.
- ≤ 100 LOC.
- Errors to stderr, exit codes per spec.
- Skip files named `README.md` at the *call sites* (pre-pr.sh, lint.yml), not in the linter itself — same convention as the F2 CI fix for agents.

## Tasks

### Task 1: Author the test harness and fixtures

- **Depends on:** none.
- **Tests:** the harness file exists and is syntactically valid bash (`bash -n tools/tests/test-lint-hook.sh` exits 0).
- **Approach:**
  - Create `tools/tests/test-lint-hook.sh` — a bash script that runs each contract test (named function per test, asserts on exit code + stderr substring). **Do NOT use `set -e`** in the harness — it must continue past per-test failures and report them all. Use a `FAILED` counter and a final `exit $FAILED`.
  - Create `tools/tests/fixtures/lint-hook/`:
    - `good.md` — minimal valid hook doc (H1 with non-empty slug ending " hook", What/Why/Configuration sections).
    - `missing-h1.md`, `missing-what.md`, `missing-why.md`, `missing-config.md`, `wrong-h1.md` (H1 missing " hook" suffix), `empty-slug-h1.md` (literal `# hook` line), `long.md` (300 blank lines past the four sections — soft-warn fixture).
  - Test harness exit 0 if every assertion holds, non-zero otherwise.
- **Done when:** `bash -n tools/tests/test-lint-hook.sh` exits 0 AND the harness file lists one named function per contract test in spec §Contract tests.

### Task 2: Implement `tools/lint-hook.sh` (green)

- **Depends on:** Task 1.
- **Tests:** Task 1's harness passes.
- **Approach:**
  - Copy the skeleton of `tools/lint-skill.sh` verbatim (set -euo, ERRORS, usage check, file-exists check → **exit 1** on missing file, matching siblings).
  - Replace the rules with:
    - H1 check: `grep -qE '^# .+ hook$' "$HOOK_PATH"` — error if missing. (`.+`, not `.*`, to require non-empty slug.)
    - Section checks: `grep -qE '^## What it does'`, `grep -qE '^## Why this matters'`, `grep -qE '^## Configuration'`.
    - Soft warn (exact format): `LINES=$(wc -l < "$HOOK_PATH"); [[ $LINES -gt 250 ]] && echo "lint-hook: WARN $HOOK_PATH is $LINES lines (soft cap 250)" >&2`.
  - Make executable: `chmod +x tools/lint-hook.sh`.
- **Done when:** `bash tools/tests/test-lint-hook.sh` exits 0; `bash tools/lint-hook.sh .claude/hooks/assumption-threshold-lock.md` exits 0 (the existing doc passes all four rules — verify by inspection).

### Task 3: Wire into pre-pr.sh

- **Depends on:** Task 2.
- **Tests:** `bash tools/pre-pr.sh` exits 0; the script's `FAILED` counter is 0; the new linter is invoked at least once on `.claude/hooks/assumption-threshold-lock.md` (verified by running it standalone before pre-pr.sh).
- **Approach:**
  - Add a hooks block in `tools/pre-pr.sh` modeled after the agents block:
    ```bash
    for hook in .claude/hooks/*.md; do
        [[ -f "$hook" ]] || continue
        [[ "$(basename "$hook")" == "README.md" ]] && continue
        run_linter "lint-hook $hook" tools/lint-hook.sh "$hook"
    done
    ```
- **Done when:** `bash tools/pre-pr.sh` exits 0 with FAILED=0 and includes lint-hook lines in its output.

### Task 4: Wire into GitHub Actions

- **Depends on:** Task 2.
- **Tests:** `.github/workflows/lint.yml` `jq`-validates as YAML; the new step is named `lint-hook` and uses the same readme-skip pattern as `lint-agent`.
- **Approach:**
  - Add a `lint-hook` step in the `artifacts` job, mirroring the existing `lint-agent` step but looping `.claude/hooks/*.md`:
    ```yaml
    - name: lint-hook
      run: |
        set -e
        for f in .claude/hooks/*.md; do
          [ -f "$f" ] || continue
          [ "$(basename "$f")" = "README.md" ] && continue
          echo "::group::$f"
          bash tools/lint-hook.sh "$f"
          echo "::endgroup::"
        done
    ```
- **Done when:** the file parses; on the next push, the CI run completes with the new step green.

### Task 5: Update reference docs (CAPTURE)

- **Depends on:** Tasks 2–4.
- **Tests:** none (doc-only).
- **Approach:**
  - `docs/INVENTORY.md` — add a row for `tools/lint-hook.sh` under the kit-infrastructure section, matching the existing `lint-skill.sh` row's shape.
  - `ROADMAP.md` — check off **F0.10**, append `**Shipped:** <date>`.
- **Done when:** both edits land, `ROADMAP.md` shows F0.10 checked.

## Rollout

- F2.1, F2.2, F2.3, F2.4, F2.5, F2.8 each write a `.claude/hooks/<slug>.md`; this linter is what makes their docs gateable in CI.
- No other consumer; nothing else needs updating.

## Risks

- **Rule overreach.** Adding rules beyond H1 + 3 sections risks the linter rejecting future legitimate hook docs. Mitigation: spec explicitly caps the rule set at four; new rules require a spec amendment.
- **H1 suffix requirement is brittle.** If a future hook adopts a different naming (e.g., `# guard-credentials (PreToolUse)`), the rule fails. Mitigation: the spec calls this out as Open Question 1; if it bites, drop the suffix requirement in a follow-up.

## Changelog

- 2026-05-21: Initial plan.
- 2026-05-21: Addressed adversarial review (8 findings). File-not-found exit is **1** (matches siblings), not 2. H1 regex changed `.*` → `.+`. Removed red-phase "Done when" criterion that conflicted with bash strict-mode; harness now uses no `set -e` and reports each test. Soft-warn exact format pinned. Acceptance criterion 4 now ties to Task 2 done-when. README skip clarified as call-site behavior, not linter behavior.
- 2026-05-21: EXECUTE complete. 11 contract tests pass. `tools/pre-pr.sh` stays green with the new lint-hook row. `tools/lint-hook.sh .claude/hooks/assumption-threshold-lock.md` exits 0. ROADMAP F0.10 checked off.
- 2026-05-21: INVENTORY.md backfill — added "## Linters (kit-meta)" section catalogueing all four sibling linters (`lint-skill.sh`, `lint-agent.sh`, `lint-command.sh`, `lint-hook.sh`) + `lint-frontmatter.py`. Initially skipped as scope creep but resolved by adopting a single new section with consistent backfill rather than an ad-hoc row.
