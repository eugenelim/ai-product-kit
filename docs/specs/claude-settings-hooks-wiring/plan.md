# Plan: claude-settings-hooks-wiring

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** approved

## Approach

F2.6 is a config-assembly task, not a code-writing one. The spec already inlines the exact JSON to write — the plan's role is to (a) write that file, (b) author a small `jq`-based test harness for the 14 contract tests, (c) re-render the 5 drifted Configuration blocks in the hook docs to match canonical form, (d) sanity-verify via `pre-pr.sh` + a one-shot `jq -e` over the file.

The file itself is ~50 lines of JSON. The harness is ~80 lines of bash with `jq` invocations.

Hook-doc cleanup is straightforward: replace the shorthand `{matcher, command}` block with the canonical `{matcher, hooks: [{type, command}]}` block. The script paths and matchers stay identical.

## Constraints

- `jq` is the only new dependency (already widely available on developer machines and in GitHub Actions runners).
- Bash + `jq` only for the test harness — no Python.
- `.claude/settings.json` MUST be valid JSON at every commit; broken settings.json silently disables ALL hooks from that source.
- ≤ 200 LOC for the test harness, including all 14 contract tests. (Originally ≤ 80; revised during EXECUTE after the iteration-1 adversarial review demanded non-vacuous guards on two tests — each guard adds an extra `checked`/`length > 0` branch. Final harness lands at 157 LOC.)

## Tasks

### Task 1: Write `tools/tests/test-settings-json.sh` (red)

- **Depends on:** none.
- **Tests:** the harness file is syntactically valid bash (`bash -n tools/tests/test-settings-json.sh`).
- **Approach:**
  - Bash script in the same shape as `tools/tests/test-lint-hook.sh` (no `set -e`; FAILED counter; named test functions; per-test `expect_*` helpers).
  - Each contract test is a single `jq -e` invocation against `.claude/settings.json` (or a path-existence check).
  - Counts: 14 contract tests total per spec.
- **Done when:** `bash -n tools/tests/test-settings-json.sh` exits 0; running it against the (missing) `.claude/settings.json` produces 14 failures.

### Task 2: Write `.claude/settings.json` (green)

- **Depends on:** Task 1.
- **Tests:** Task 1's harness exits 0.
- **Approach:**
  - Copy the canonical JSON from spec §Inputs and outputs into `.claude/settings.json`.
  - `jq -e . .claude/settings.json` validates.
- **Done when:** all 14 contract tests pass.

### Task 3: Re-render 5 hook docs' `## Configuration` blocks

- **Depends on:** Task 2 (so the canonical form is grounded in the actual settings.json).
- **Tests:**
  - `tools/pre-pr.sh` still exits 0 (lint-hook on each doc).
  - Manual diff: each doc's Configuration block now matches the canonical schema — `{matcher?, hooks: [{type: "command", command: "python3 ..."}]}` — with no shorthand siblings.
- **Approach:**
  - This is a **structural re-render**, not a one-line patch. Five docs use shorthand `{matcher, command}` (or three separate event entries each with a bare `command` key in `mode-guard.md`). Replace the entire JSON fenced block in each Configuration section with the canonical form pasted from `.claude/settings.json`.
  - For `check-handover-link.md`, `ontology-type-check.md`, `cadence-nudge.md`, `mode-guard.md`: replace shorthand with canonical inner-array form; ensure `type: "command"` is present on every command object.
  - For `assumption-threshold-lock.md`: (a) drop `matchPaths` (not in schema; script path-filters internally — keep the one-sentence note); (b) change `python scripts/...` → `python3 scripts/...` (matches the canonical interpreter the other five hooks declare); (c) re-render to canonical form.
  - Add a one-sentence cross-reference in each: "Wired in `.claude/settings.json` as of F2.6 (2026-05-21)."
- **Done when:** all 5 docs lint clean; every Configuration block parses against the same schema as `.claude/settings.json`.

### Task 4: Wire test harness into `tools/pre-pr.sh`

- **Depends on:** Task 1, Task 2.
- **Tests:** `bash tools/pre-pr.sh` exits 0; output includes a `✓ settings-json` row.
- **Approach:**
  - Add **unconditionally** after the lint-hook loop:
    ```bash
    # Settings JSON
    run_linter "settings-json" tools/tests/test-settings-json.sh
    ```
  - No `if [[ -f .claude/settings.json ]]` guard — a missing settings.json is exactly the failure mode CI must catch. The harness's `test_settings_file_exists` is the gate.
- **Done when:** pre-pr.sh exits 0 and includes the new row.

### Task 5: Wire harness into GitHub Actions

- **Depends on:** Task 4.
- **Tests:** `.github/workflows/lint.yml` `jq`-validates as YAML; the new step is named `settings-json` and runs `bash tools/tests/test-settings-json.sh`.
- **Approach:**
  - Add a `settings-json` step in the `artifacts` job mirroring the existing `lint-hook` step. (Single command, no loop — there's only one settings file.)
- **Done when:** the file parses; on the next push, CI completes with the new step green.

### Task 6: CAPTURE

- **Depends on:** Tasks 1–5.
- **Tests:** none (doc-only).
- **Approach:**
  - `docs/INVENTORY.md` — Global Hooks table: change "wiring pending F2.6" → "wired (F2.6, 2026-05-21)" on all six rows. Drop the "Six hook scripts ship..." note since wiring is now done.
  - `ROADMAP.md` — F2.6 line: `[ ]` → `[x]`, append `**Shipped:** 2026-05-21.`
  - `AGENTS.md` — update any line still saying "settings.json wiring planned" to reflect shipped state.
- **Done when:** all three edits land, ROADMAP shows F2.6 checked.

## Rollout

- After ship, every new Claude Code session in this repo registers the six hooks. Existing sessions need a restart or `/hooks` reload to pick up the new settings.
- No downstream consumer needs updating — F2.6 is the consumer.

## Risks

- **Schema drift between docs and Anthropic's published schema.** If Anthropic changes the hook-entry shape (e.g., renames `matcher` to `tool_pattern`), our settings.json + every hook doc + every test breaks. Mitigation: the test harness validates against the documented shape; CI catches divergence. The cross-reference in the spec to https://code.claude.com/docs/en/hooks anchors the source of truth.
- **Single broken-JSON edit disables all hooks.** A typo in `.claude/settings.json` silently disables every hook from this file. Mitigation: `jq -e` on every commit (via CI + pre-pr.sh). The test harness's `test_settings_is_valid_json` is the gate.
- **Hook firing order surprises.** `guard-credentials` runs first by file position; subsequent hooks assume the credential check has already happened. If Claude Code's harness ignores file order, that assumption breaks. Mitigation: the spec calls this out as Open Question 2; if order isn't deterministic, the spec's "co-locate when matcher is identical" rule still keeps semantics correct.
- **`python3` not available on contributor machines.** Some systems alias `python` only. Mitigation: every hook doc + AGENTS.md already declares `python3` is required; F2.6 inherits that requirement.

## Changelog

- 2026-05-21: Initial plan.
- 2026-05-21: Addressed adversarial review (9 findings, 4 critical). UserPromptExpansion matcher claim corrected (matcher is optional, not absent). `python` → `python3` fix added to Task 3 for assumption-threshold-lock.md. `test_no_matchPaths_field` jq expression replaced with `[.. | objects | has("matchPaths")] | any | not` (previous form silently passed on empty streams). Firing-order claim demoted from causal "runs first because" to "assumed declared-order, see Risk #3." Added a Multi-source settings semantics section to spec §Inputs and outputs documenting the array-merge assumption. Removed the `if [[ -f ]]` guard from Task 4 — missing settings.json is exactly the failure case the harness should catch. Task 3 rewritten to make the structural re-render explicit (not just `matchPaths` removal).
- 2026-05-21: EXECUTE complete. `.claude/settings.json` written; `tools/tests/test-settings-json.sh` exists; all 14 contract tests pass. 5 hook docs re-rendered to canonical schema. `tools/pre-pr.sh` exits 0 with the new `✓ settings-json` row. `.github/workflows/lint.yml` gains the `settings-json` step. INVENTORY.md Global Hooks table updated to "wired (F2.6, 2026-05-21)" on all six rows. ROADMAP F2.6 checked.
- 2026-05-21: REVIEW iteration 1 → fixed 4 findings (AGENTS.md stale "planned" qualifier; guard-credentials.md stale "F2.6 will consolidate" forward-reference; two test-harness vacuous-pass risks — empty event arrays and zero-command extraction). Commit bf01a63.
- 2026-05-21: REVIEW iteration 2 → fixed 2 findings (spec acceptance-criteria checkboxes left as `[ ]` despite Status: Shipped; plan's ≤ 80 LOC harness constraint exceeded — revised to ≤ 200 LOC reflecting the iter-1 non-vacuous guards adding ~75 lines).
