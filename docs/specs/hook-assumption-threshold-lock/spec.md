# Spec: hook-assumption-threshold-lock

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** hook (PreToolUse — Write)
- **Serves kit phase:** Validation (the kit's signature guard)
- **Constrained by:** `.claude/hooks/assumption-threshold-lock.md` (the existing doc — the contract for what the script must do); `docs/HANDOVERS.md` Handover 3; F1.2 (`scripts/lib/frontmatter`); F0.10; `.claude/skills/work-loop/SKILL.md`

> **Spec contract.** Defines `scripts/check-assumption-threshold.py`. Matches the algorithm already documented in `.claude/hooks/assumption-threshold-lock.md`. Blocks any Write to `validation/experiments/**/results.md` unless a sibling `experiment.md` with a predeclared falsification threshold existed *before* the results file was first written.

## Objective

Build the Python script the existing hook doc names. The doc is authoritative for the algorithm shape — this spec implements it and **extends it** in one place: a fourth check on `predeclared_at`. The script reads PreToolUse stdin, confirms (a) the target matches `validation/experiments/**/results.md`, (b) a sibling `experiment.md` exists with `predeclared_threshold:` containing both `success:` and `falsification:` keys, (c) **[spec extension beyond doc step 3]** the `experiment.md`'s frontmatter-declared `predeclared_at:` date is on or before today (catches future-dated threshold tampering), and (d) the design file's mtime predates this write by ≥ 1 second. On any failure, the hook blocks with a JSON `decision: block`. The hook doc will be amended in CAPTURE to surface the new step (c) in its numbered list.

This is the kit's "signature" guard — the single hook AGENTS.md cites as "the most important." Until it ships, validation theatre is structurally possible.

## Why now

The hook doc has shipped since v3. The script it names has not. Every validation experiment in the kit today can be post-rationalized — exactly the failure mode the doc warns about. F1.2 ships the frontmatter parser; F0.10 ships the doc linter; nothing else is blocking.

D14 (hook-assumption-threshold-lock-hardening) extends this hook with tamper-resistant timestamps and a machine-checkable threshold schema — explicitly deferred and not in scope here. This spec ships the mtime-based version the doc already documents.

## Inputs and outputs

**Inputs.**
- Stdin: PreToolUse JSON with `tool_name: "Write"` and `tool_input.file_path` matching `validation/experiments/<id>/results.md`.
- Disk: the sibling `validation/experiments/<id>/experiment.md` and its mtime.
- Optional: `validation/experiments/OVERRIDE-LOG.md` (append target on override path).

**Outputs.**
- Exit 0: write allowed. No stdout.
- Exit 2: write blocked. Stdout = JSON `{"decision":"block","reason":"<one-line>"}`. The reason names which check failed.
- Side effect on override path: appends a one-line entry to `validation/experiments/OVERRIDE-LOG.md` (creates the file if absent) recording the override.

**Required frontmatter on `experiment.md`** (verbatim from the existing hook doc):

```yaml
object_type: Experiment
predeclared_threshold:
  success: <quantitative criterion>
  falsification: <quantitative criterion>
predeclared_at: <YYYY-MM-DD>     # must be ≤ today
```

**Override frontmatter** (also from the doc):

```yaml
override_threshold_lock: true
override_reason: <one-paragraph>
override_authorized_by: <name>
override_authorized_at: <YYYY-MM-DD>
```

## Boundaries

### Always do
- Operate as a PreToolUse hook reading stdin.
- Match strict path glob `validation/experiments/**/results.md` (recursive, matches both flat `validation/experiments/exp-001/results.md` AND nested `validation/experiments/2026/q1/exp-001/results.md`). The double-star is the authoritative form from `.claude/hooks/assumption-threshold-lock.md`.
- Read `experiment.md` from the same directory as the proposed `results.md`.
- Compare mtimes via `os.path.getmtime` (NOT `os.lstat` — symlinked design files use the target's mtime; that's a known limitation per Non-goals). The design file's mtime must be ≤ `time.time() - 1.0` (anchor: the moment the hook fires). Re-writes to the same `results.md` are evaluated against the same rule with a fresher `time.time()`, which is intentional — the design file remains the threshold predecessor and the gate stays consistent across re-writes.
- On override path: allow the write AND append to `OVERRIDE-LOG.md` with date, experiment id, reason, authorizer.

### Ask first
- Adding additional schema fields beyond `predeclared_threshold.{success,falsification}` + `predeclared_at`. Default: only those three.
- Changing the override file location from `validation/experiments/OVERRIDE-LOG.md`. Default: doc-specified path.

### Never do
- Use anything beyond `os.path.getmtime` for the timestamp check — D14 will introduce git-commit-based proof; that's a future spec.
- Block writes outside the strict path glob.
- Delete or rotate `OVERRIDE-LOG.md`.
- Read or modify files outside the experiment's directory + the OVERRIDE-LOG path.

## Verification mode

- **TDD.** Unit tests under `scripts/tests/test_check_assumption_threshold.py`.
- **Goal-based check.** `tools/lint-hook.sh .claude/hooks/assumption-threshold-lock.md` exits 0 (the existing doc — must already lint clean once F0.10 ships).
- **Manual gesture.** With the hook wired: writing a `validation/experiments/test/results.md` without a sibling `experiment.md` produces a visible block message; creating `experiment.md` with the required frontmatter, waiting one second, then retrying succeeds.

## Contract tests

- `test_allows_write_when_design_predates_with_full_threshold` — `experiment.md` with full frontmatter exists, mtime ≥ 2s old → exit 0.
- `test_blocks_when_experiment_md_missing` — no design file in the directory → exit 2 with reason naming the missing file.
- `test_blocks_when_predeclared_threshold_missing` — design file exists but no `predeclared_threshold:` block → exit 2.
- `test_blocks_when_only_success_criterion_present` — `predeclared_threshold.success` set but `falsification` missing → exit 2.
- `test_blocks_when_only_falsification_criterion_present` — opposite of above → exit 2.
- `test_blocks_when_predeclared_at_missing` → exit 2.
- `test_blocks_when_predeclared_at_after_today` — `predeclared_at: 2099-01-01` → exit 2 with reason naming future-date.
- `test_blocks_when_design_mtime_is_after_results_write` — design file created after the moment of the write (simulated via temp dir + utime) → exit 2 with reason about timestamp ordering.
- `test_override_allows_write_and_appends_to_override_log` — `override_threshold_lock: true` + reason + authorizer + authorized_at set → exit 0; `OVERRIDE-LOG.md` gets a new line containing the experiment id, date, authorizer.
- `test_override_without_reason_blocks` — `override_threshold_lock: true` but `override_reason` empty → exit 2.
- `test_override_without_authorizer_blocks` — flag + reason set, `override_authorized_by:` empty → exit 2.
- `test_override_threshold_lock_false_does_not_unblock` — `override_threshold_lock: false` is treated as no-override (normal threshold checks apply). Implementation must use strict `is True`, not truthy.
- `test_path_outside_glob_passes_silently` — `validation/learnings/foo.md` Write call → exit 0, no log line.
- `test_malformed_design_frontmatter_blocks_with_clear_reason` — `experiment.md` exists but YAML inside the `---` delimiters is malformed → exit 2 with reason mentioning parse failure (not a crash).
- `test_no_frontmatter_delimiters_blocks_with_clear_reason` — `experiment.md` exists but has no `---` delimiters at all (parser returns None) → exit 2 with a distinct reason ("design file has no frontmatter"), not conflated with malformed-YAML.
- `test_recursive_path_matches_nested_experiment_dir` — `validation/experiments/2026/q1/exp-001/results.md` Write call → glob matches, hook applies.

## Non-goals

- Validating the *quality* of the threshold (whether `≥15%` is "real"). That's the `assumption-skeptic` agent (P3.2).
- Cross-checking the parent Assumption Map. That's `/audit-vision-evidence` (P3.12).
- Git-commit-based timestamp proof. That's D14.
- Schema validation of `predeclared_threshold.success` / `.falsification` content shape. Free-form strings; the human-readable criterion is the contract.
- Detecting mtime tampering (e.g., `touch -t` backdating, symlinking an older file in as `experiment.md`). Honor-system at this layer; D14 will harden via git-commit-based ordering.
- Enforcing `object_type: Experiment` on the design file. A markdown file in the experiment directory with the right threshold fields passes structurally; semantic typing is left to `/audit-traceability` and the F2.3 nudge hook. (Deferred; documented as known limitation.)
- Validating `override_authorized_at:` format (must be `YYYY-MM-DD` per the hook doc but free-form-string accepted at this layer — honor-system, same as mtime).

## Open questions

1. **Sub-second mtime skew.** A "wait at least 1s" floor is brittle on fast filesystems. The spec adopts a 1-second safety floor; the broader fix (git-commit-based ordering) is D14.

2. **First-write detection.** This hook fires on every Write to `results.md`. A second Write to the same file after the first succeeded is also gated by the same check — that's correct (the design file still predates the write). No change needed.

## Acceptance criteria

- [ ] `scripts/check-assumption-threshold.py` exists, stdlib + `scripts.lib.frontmatter` only, ≤ 250 LOC.
- [ ] `scripts/tests/test_check_assumption_threshold.py` exists; all 15 contract tests pass.
- [ ] `.claude/hooks/assumption-threshold-lock.md` updated to include `predeclared_at` check in its "What it does" numbered list (was steps 1–4; now 1–5). All other content unchanged.
- [ ] `python3 -m unittest scripts.tests.test_check_assumption_threshold` exits 0.
- [ ] PLAN / VERIFY / REVIEW gates exit 0.
- [ ] **Depends on:** F0.10 (`tools/lint-hook.sh`) must ship before VERIFY can run.

## Cross-references

- **Consumed by:** F2.6 (claude-settings-hooks-wiring); the manual-gesture verification in P3.7 (cmd-run-assumption-test).
- **Consumes:** `scripts.lib.frontmatter` (F1.2).
- **Frontmatter fields owned:** `predeclared_threshold.{success,falsification}`, `predeclared_at`, `override_threshold_lock`, `override_reason`, `override_authorized_by`, `override_authorized_at`.
- **Ontology object types touched:** Experiment, Validation Learning Memo (via the Domain B objects the experiment links to).
