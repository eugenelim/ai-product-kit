# Plan: cmd-draft-vision

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

The component is one file: `.claude/commands/draft-vision.md`. The parent F4 convention has done the hard architectural work — body structure, argv contract, parent-resolution, interactive-fill, pre-fill, linter integration, exit codes, and the chaining hint are all locked. This worker's job is to **copy the skeleton and fill it** for `/draft-vision` specifically: substitute the per-command values from `spec.md` §"Per-section interactive prompts", §"Parent-artifact-resolution rule", §"Pre-fill rules", §"Linter integration", §"Chaining hint", and §"Boundaries → Never do".

Sequence: (1) author `.claude/commands/draft-vision.md` by copying `.claude/commands/_meta/command-skeleton.md` and applying the per-command fill; (2) lint the new file with `tools/lint-command.sh`; (3) run the contract test suite to confirm the five parametrized in-scope cases for `draft-vision` flip from skip to pass; (4) run CAPTURE — flip ROADMAP P4.1 checkbox, update INVENTORY, freeze `spec.md` and `plan.md` Status fields.

The load-bearing property of this sequence: the skeleton is the contract. No improvisation on body structure, no re-ordering of Steps, no new H2s. Per-command additions live only in the documented hook points (the H2 prompts inside Step 3; the `killed`-memo refusal inside the `## What this command will not do` list; the `NEXT:` line in Step 6). Everything else is mechanical substitution.

## Constraints

- Must not modify `templates/vision.md` (F3.6 frozen).
- Must not modify `docs/specs/phase-4-command-convention/spec.md` or its convention text in `docs/CONVENTIONS.md`.
- Must not modify `.claude/commands/_meta/command-skeleton.md` or `.claude/commands/_meta/README.md`.
- Must not modify `tools/lint-command.sh`, `tools/lint-frontmatter.py`, or any other `tools/` script.
- Must not modify `scripts/tests/test_phase4_command_shape.py` — the test is auto-tightening; it consumes the command file's existence, no test-code change is permitted.
- Must not introduce new frontmatter keys on the *command file* (only `description:` and `argument-hint:`, per convention).
- Must not introduce new frontmatter keys on the *written Vision artifact* (only the HANDOVERS-4 set, per spec §"Boundaries → Ask first").
- Must not add new ontology types.
- Body of `.claude/commands/draft-vision.md` ≤ 120 lines (skeleton parity).
- The six H2 prompts and three H3 tier prompts in spec §"Per-section interactive prompts" must appear in the command body verbatim — they are the per-command fill, not optional polish.

## Construction tests

No cross-cutting tests beyond the per-task tests below. The contract is per-file (the new command file) and per-test (the five parametrized cases plus `tools/pre-pr.sh`); both are covered task-local.

## Tasks

### Task 1: author `.claude/commands/draft-vision.md` by copying the skeleton and filling per the spec

- **Depends on:** none
- **Tests:**
  - `bash tools/lint-command.sh .claude/commands/draft-vision.md` exits 0 (spec T1).
  - Body contains all four required H2s in order: `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do` (spec T2).
  - `argument-hint:` starts with `<slug>` (spec T3).
  - Body contains `templates/vision.md` and that path exists (spec T4).
  - Body contains a `delivery/visions/` path and the directory exists (spec T5).
  - H1 is exactly `# /draft-vision` (spec T9).
  - Body ≤ 120 lines (spec T7).
  - `description:` present and ≤ 1024 chars (spec T8).
  - The six H2 prompts and three H3 tier prompts from spec §"Per-section interactive prompts" appear in the body verbatim.
  - The `killed`-memo refusal text appears in `## What this command will not do` and in the Step-1 prose.
- **Approach:**
  - `cp .claude/commands/_meta/command-skeleton.md .claude/commands/draft-vision.md`.
  - Replace the H1 `# /<command-name>` with `# /draft-vision`.
  - Fill the frontmatter `description:` with a single sentence: *"Draft a `delivery/visions/<slug>.md` Vision from a surviving learning memo by walking the F3.6 Vision template interactively per the Phase-4 template-fill command convention."* (within 1024 chars).
  - Fill `argument-hint: <slug> [--from <learning-slug>] [--force]` (creating-command form; replace the skeleton's generic `<parent-slug>` with the specific `<learning-slug>`).
  - Replace the lead blockquote `<One paragraph...>` with a paragraph naming HANDOVERS-4, the F3.6 template, the destination `delivery/visions/<slug>.md`, and that this is a **creating** command.
  - Fill `## When to run` with three triggers: "After a learning memo's status flips to `survived`"; "When starting the Validation → Delivery handover and no Vision yet exists for the chosen learning"; "Before invoking `/draft-initiative` for the first time on a new initiative slug".
  - Fill `## Inputs` per spec §"Inputs and outputs": (1) the positional `<slug>`; (2) `templates/vision.md`; (3) parent: a memo in `validation/learnings/` with `status:` not in `{killed}` (resolution rule below); (4) `--from <learning-slug>` (optional, explicit-parent override).
  - In `## Procedure` → Step 1, write the creating-command branch with the `validation/learnings/` family, the `{killed}` filter, the `last_updated:` sort, the cap-at-10, the always-confirm-even-on-single-candidate rule, the empty-list remediation suggestion ("run `/learning-memo` first"), and the belt-and-suspenders `killed`-via-`--from` refusal.
  - In Step 2, name the destination `delivery/visions/<slug>.md`, the source `templates/vision.md`, and the eight pre-fill fields (`id: VIS-<NNN>`, `slug`, `created`, `last_updated`, `parent_learning`, `parent_intent`, `object_type: Vision`, `status: Draft`).
  - In Step 3, inline the six H2 prompts and three H3 tier prompts verbatim from spec §"Per-section interactive prompts". This is the load-bearing per-command fill.
  - In Step 4, name the three HANDOVERS-4 `human_owned_decisions:` entries (customer-shaped framing of the value proposition / differentiator selection / predicted outcome thresholds) and the requirement to record confirmations in `approvals_obtained:`.
  - In Step 5, restate the linter invocation `python3 <repo-root>/tools/lint-frontmatter.py delivery/visions/<slug>.md` and the exit-3 path.
  - In Step 6, set the literal NEXT line: `NEXT: /draft-initiative <initiative-slug>`. No REVIEW line.
  - In `## What this command will not do`, keep the skeleton's six generic non-behaviors and append the per-command additions: "Not write a vision when the chosen learning memo's `status:` is `killed`"; "Not fabricate `predicted_outcomes[*].kpi_id` or `counter_metrics[*].kpi_id` — ask the human for each"; "Not pre-fill `human_owned_decisions:` with anything other than the three HANDOVERS-4 entries"; "Not auto-invoke `/draft-initiative`"; "Not author multiple Visions in one invocation".
  - Verify body ≤ 120 lines after edits (trim verbose prose if needed; the skeleton's six steps are non-negotiable but per-command fill prose can be tight).
- **Done when:** `.claude/commands/draft-vision.md` exists at the path; all eight per-task tests pass.

### Task 2: lint the new command file with `tools/lint-command.sh`

- **Depends on:** Task 1
- **Tests:**
  - `bash tools/lint-command.sh .claude/commands/draft-vision.md` exits 0 (already in Task 1; restated here as the lint-only gate before running the broader pytest suite).
- **Approach:**
  - Run the linter directly.
  - If exit non-zero, surface the linter output, fix the H2 / frontmatter / H1 issue, re-run. Iteration cap from state.json applies (5 in-session).
- **Done when:** linter exits 0 cleanly.

### Task 3: run the contract test suite and confirm the five parametrized in-scope cases for `draft-vision` pass

- **Depends on:** Task 2
- **Tests:**
  - `python3 -m pytest scripts/tests/test_phase4_command_shape.py -v` exits 0 (spec T6).
  - In the verbose output, the five parametrized cases for `draft-vision` show `PASSED` (not `SKIPPED`): `test_inscope_commands_pass_lint[draft-vision]`, `test_inscope_commands_have_required_h2s[draft-vision]`, `test_inscope_commands_declare_argv[draft-vision]`, `test_inscope_commands_cite_template_path[draft-vision]`, `test_inscope_commands_cite_destination_path[draft-vision]`.
  - The other six commands continue to show `SKIPPED` (they don't yet exist; the auto-skip is the contract).
- **Approach:**
  - Run the pytest command from any cwd (the test resolves REPO_ROOT relative to its own path).
  - Inspect the `-v` output for the five parametrized cases.
  - If any of the five fails, the fix is per-test specific: lint failure → adjust frontmatter / H1 / required H2s; missing H2 → add to body; argv mismatch → fix `argument-hint:`; missing template-path mention → ensure `templates/vision.md` is cited in the body; missing destination-path mention → ensure `delivery/visions/` appears.
- **Done when:** pytest exits 0; all five `draft-vision` parametrized cases are `PASSED`.

### Task 4: CAPTURE — flip ROADMAP P4.1 checkbox, update INVENTORY, freeze spec.md + plan.md Status

- **Depends on:** Task 3
- **Tests:**
  - `grep -E "^- \[x\] \*\*P4\.1\*\*" ROADMAP.md` returns one line.
  - `grep -E "Shipped: 20[0-9]{2}-[0-9]{2}-[0-9]{2}" ROADMAP.md | grep "P4.1"` returns one line.
  - `grep -E "/draft-vision" docs/INVENTORY.md` shows the row in shipped form.
  - `spec.md` header `Status:` is `Shipped (<date>)`.
  - `plan.md` header `Status:` is `Done` and `Plan review:` is `approved`.
  - `bash tools/pre-pr.sh` exits 0 (spec T10).
- **Approach:**
  - In `ROADMAP.md`, flip the P4.1 row from `[ ]` to `[x]` and append `Shipped: <YYYY-MM-DD>` per the F3 plan's CAPTURE-phase convention.
  - In `docs/INVENTORY.md`, update the `/draft-vision` row to reflect shipped status (path, shipped-on date) per the INVENTORY-row format used by the other shipped commands.
  - In `docs/specs/cmd-draft-vision/spec.md`, change `Status: PLAN-phase` to `Status: Shipped (<YYYY-MM-DD>)`.
  - In `docs/specs/cmd-draft-vision/plan.md`, change `Status: PLAN-phase` to `Status: Done` and `Plan review: pending` to `Plan review: approved`.
  - Run `bash tools/pre-pr.sh` as the kit-wide health gate.
- **Done when:** all four artifacts (ROADMAP, INVENTORY, spec, plan) reflect shipped status; `tools/pre-pr.sh` exits 0.

## Rollout

- **ROADMAP.md** — P4.1 row flips to `[x]` with `Shipped:` date in Task 4.
- **docs/INVENTORY.md** — the `/draft-vision` row updates to shipped status in Task 4.
- **No `AGENTS.md` change required** — the command is the first link in the documented Phase-4 chain (per `docs/HANDOVERS.md` and the F4 convention); the chain is already documented, this command instantiates it.
- **No skill / agent / audit changes required** — `/draft-vision` is the producer; downstream consumers (`/draft-initiative`, `/audit-portfolio-coherence`) already reference the Vision artifact at `delivery/visions/<slug>.md`; no consumer needs an update.
- **Callers exist** — the F4 convention spec names `cmd-draft-vision` as a consumer (P4.1 row in the convention's §"Cross-references"). The command file is reachable via the slash-command palette as soon as it ships at `.claude/commands/draft-vision.md`. Not unreachable.

## Risks

- **Risk 1 — Iteration churn on the six H2 prompts.** The spec specifies the prompt phrasing verbatim, but the linter doesn't gate prompt presence — only the human reviewer can verify the prompts landed correctly. Mitigation: Task 1's "Done when" requires the verbatim copy; supervisor's Stage-4 REVIEW pass catches drift.
- **Risk 2 — Body length creep above 120 lines.** Six steps + per-command fill + nine prompt blocks adds up. Mitigation: trim prose, but never trim the prompts themselves (they're the load-bearing fill). If trim isn't enough, escalate as an Open Question to the supervisor — increasing the body cap is a convention-level decision, not per-command.
- **Risk 3 — `id: VIS-<NNN>` collision.** If two adopters run `/draft-vision` concurrently in different worktrees and both compute the same next-integer, the merge creates two Visions with the same id. Out of scope for this command — the next-id-derivation rule is the convention's; remediation is to widen the convention (e.g., switch to ULIDs) in a follow-up. Surface as a Risk in the command's body if needed; do not unilaterally widen the rule here.

## Changelog

-
- 2026-05-23: EXECUTE / REVIEW / CAPTURE completed in supervisor's batch fan-out across all seven F4 template-fill commands. Body lint clean; inscope contract tests pass; pre-pr green.
