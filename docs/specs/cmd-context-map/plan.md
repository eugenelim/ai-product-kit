# Plan: cmd-context-map

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy for shipping `.claude/commands/context-map.md`, the augmenting slash command in the Phase-4 chain that fills the placeholder `context-map.md` child inside an existing initiative folder. The spec is the contract; this plan is the path. The plan may change as we execute; substantive changes are logged in the changelog at the bottom.

## Approach

Four sequential tasks: AUTHOR the command body by copying `.claude/commands/_meta/command-skeleton.md` and substituting the augmenting-command shape per the spec's §"Body-shape contract"; LINT the resulting command file with `tools/lint-command.sh`; run the convention's pytest suite (`scripts/tests/test_phase4_command_shape.py`) to confirm the contract test passes against the newly landed command; CAPTURE — freeze spec/plan/state, mark P4.4 in ROADMAP, refresh INVENTORY.

The command file is a single Markdown document — `.claude/commands/context-map.md` — under 200 body lines. No Python, no shell, no fixtures beyond what the spec's manual-gesture verification implies (and the manual gesture is deferred to post-ship adopters, per the spec's §"Verification mode"). The work is dominated by careful prose copy from the skeleton: the augmenting-command variants of Steps 1 and 2, the eight per-section interactive prompts verbatim from the spec, and the absence of a `--from` flag.

The plan is **straight-line**: no parallel sub-tasks within this command's build. The parallelism is at the F4 fan-out level — seven workers (this command's spec is one of the seven) each ship a sibling command in their own session. Inside this session, AUTHOR → LINT → PYTEST → CAPTURE is the path.

## Constraints

- The command file MUST start from `.claude/commands/_meta/command-skeleton.md` (do not author from scratch). The skeleton's body is the convention's contract surface; copying it ensures the four convention-required H2 sections, the linter-passing H1 line, and the procedure shape land correctly the first time.
- `argument-hint:` MUST be exactly `<initiative-slug> [--force]` — the augmenting form. The contract test's `test_inscope_commands_declare_argv` keys on the literal `<initiative-slug>` token; any deviation invalidates the convention's sub-class distinction.
- The body MUST NOT contain `--from`. The convention's §"Argv contract" augmenting case explicitly excludes the flag; T10 asserts the absence.
- `tools/lint-command.sh` MUST exit 0 against the shipped command file before declaring task 2 done. Lint failures are not deferred — they're fixed in-session per the work-loop's "drift is a bug" rule.
- The eight per-section interactive prompts in the spec's §"Per-section interactive prompts" MUST appear in the command body verbatim (or with the spec-anchored distinctive substring intact per T13). Paraphrasing the prompts at command-author time is a silent drift against the spec; if a prompt's phrasing genuinely needs to change, the spec is edited first, then the body.
- Must not modify `templates/initiative/context-map.md`, `tools/lint-frontmatter.py`, `tools/lint-command.sh`, `scripts/tests/test_phase4_command_shape.py`, or any sibling command. The contract test's discovery is automatic; no test-harness wiring is required.

## Construction tests

Cross-cutting tests (named individually per task below as `Tests:`):

- T1–T10 from spec.md are the per-task gate on AUTHOR + LINT.
- T11 (`pytest scripts/tests/test_phase4_command_shape.py`) is the PYTEST gate.
- T12 (`bash tools/pre-pr.sh`) is the CAPTURE gate.
- T13 (eight per-section prompt anchors) is the AUTHOR-time gate.
- T14 (adversarial-reviewer) is the REVIEW gate at session-end.

## Tasks

### Task 1: AUTHOR `.claude/commands/context-map.md`

- **Depends on:** none
- **Tests:**
  - T1: file exists.
  - T2: `tools/lint-command.sh` exits 0 against the file.
  - T3: four convention-required H2 sections present (`When to run`, `Inputs`, `Procedure`, `What this command will not do`).
  - T4: `argument-hint:` is exactly `<initiative-slug> [--force]`.
  - T5: body cites `templates/initiative/context-map.md`.
  - T6: body cites `delivery/initiatives/`.
  - T7: `NEXT: /end-to-end-flow <initiative-slug>` appears exactly once.
  - T8: no `REVIEW:` line.
  - T9: Step 1 declares "verify ... initiative folder" and at least two `exit code 2` paths.
  - T10: no `--from` token anywhere in the file.
  - T13: each of the eight per-section prompt anchors from §"Per-section interactive prompts" appears at least once.
- **Approach:**
  - `cp .claude/commands/_meta/command-skeleton.md .claude/commands/context-map.md` (start from the skeleton).
  - Replace the `<command-name>` placeholder with `context-map` (H1 becomes `# /context-map`).
  - Replace `description:` with the spec's one-sentence frontmatter description.
  - Replace `argument-hint:` with the augmenting form `<initiative-slug> [--force]` and delete the comment line about the augmenting variant (no longer needed once the augmenting form is the live value). Also delete the `<slug> [--from <parent-slug>] [--force]` creating-form line.
  - Replace the orientation blockquote with the spec's body-shape-contract blockquote (the "Augmenting command that fills …" paragraph stating the command is augmenting, naming the destination child file, citing the parent convention and HANDOVERS-5).
  - Fill `## When to run` with the three bullets from §"Body-shape contract".
  - Fill `## Inputs` with the four numbered items.
  - Fill `## Procedure` with six Step-N sub-sections (the augmenting variants of Steps 1 and 2 from the skeleton, plus Steps 3–6 per the spec).
  - In Step 3, name the eight per-section interactive prompts verbatim from the spec.
  - In Step 6, emit the NEXT line inside a fenced code block (matches T7's regex which expects the `NEXT: …` line on its own).
  - Fill `## What this command will not do` with the ten bullets from §"Body-shape contract", augmenting-specific.
- **Done when:** T1–T10 and T13 all pass.

### Task 2: LINT — confirm `tools/lint-command.sh` exits 0

- **Depends on:** Task 1
- **Tests:**
  - T2 (re-run): `bash tools/lint-command.sh .claude/commands/context-map.md` exits 0.
- **Approach:**
  - Run the shape linter against the shipped file.
  - If lint fails, inspect the error, fix the source of the failure in `.claude/commands/context-map.md` (typically: missing `description:`, body has no `## When to run` or `## Procedure`, H1 doesn't start with `/`), re-run.
  - Cap fixes at 2 iterations; if lint still fails after 2 fixes, surface the failure to the supervisor — it likely indicates a skeleton-vs-linter drift that needs a convention-level edit, not a per-command fix.
- **Done when:** lint exits 0.

### Task 3: PYTEST — confirm the convention's contract test passes

- **Depends on:** Task 2
- **Tests:**
  - T11: `python3 -m pytest scripts/tests/test_phase4_command_shape.py -v` exits 0.
- **Approach:**
  - Run the convention's contract test. It auto-discovers `.claude/commands/context-map.md` (now present) and runs:
    - `test_inscope_commands_pass_lint` (cross-check of T2)
    - `test_inscope_commands_have_required_h2s` (cross-check of T3)
    - `test_inscope_commands_declare_argv` against the `POSITIONAL` map entry `"context-map": "<initiative-slug>"` (cross-check of T4)
    - `test_inscope_commands_cite_template_path` against `templates/initiative/context-map.md` (cross-check of T5)
    - `test_inscope_commands_cite_destination_path` against `delivery/initiatives/` (cross-check of T6)
  - If any sub-test fails, the failure points at a specific convention-contract violation. Fix the violation in `.claude/commands/context-map.md`; do NOT modify the test, the convention, or the constants.
- **Done when:** pytest exits 0 with the five relevant test cases passing for `context-map`.

### Task 4: CAPTURE — freeze spec/plan/state, mark ROADMAP P4.4, refresh INVENTORY

- **Depends on:** Task 3
- **Tests:**
  - T12: `bash tools/pre-pr.sh` exits 0.
  - T14: dispatch the `adversarial-reviewer` subagent against `.claude/commands/context-map.md` versus this spec, the parent convention, and HANDOVERS-5; assert 0 Blocking findings.
- **Approach:**
  - Mark `spec.md` Status `Shipped (<YYYY-MM-DD>)`.
  - Mark `plan.md` Status `Done` and the Plan review line `approved`.
  - Update `state.json`: `plan_review_status: "approved"`, `iteration_count` to the actual count.
  - Edit `ROADMAP.md`: flip P4.4's checkbox to `[x]` and append the ship date.
  - Edit `docs/INVENTORY.md`: add the row for `/context-map` under the Phase-4 commands section (slug, type=command, status=shipped, ship-date, brief description, link to this spec).
  - Run `tools/pre-pr.sh` and confirm exit 0.
  - Dispatch `adversarial-reviewer`; iterate on any Blocking finding within the 3-pass limit. Non-Blocking findings: capture in the spec's §"Open questions" or defer per the kit's "small defers same session" rule.
- **Done when:** T12 and T14 both pass; the four file edits are committed; the supervisor is notified that P4.4 is ready for the shared commit.

## Rollout

- `/context-map` is reachable as a slash command immediately after the `.claude/commands/context-map.md` file lands — Claude Code resolves slash commands by filename. No registry edit required.
- `.claude/CLAUDE.md` and `AGENTS.md` reference Phase-4 commands generically; neither file needs editing for an individual augmenting command to land. The convention's cross-reference in ROADMAP is sufficient.
- `docs/INVENTORY.md` does need a new row for `/context-map` (Task 4 above).
- The chain successor `/end-to-end-flow` (P4.5) reads `/context-map`'s NEXT line as its trigger; P4.5 is in parallel fan-out and ships in the same F4 batch. If P4.5 ships after P4.4 in the same session, no edit needed; if P4.5 slips, this command's NEXT line remains accurate (it names the planned command; the convention's kit-drift policy permits `(planned — ROADMAP P4.5)` as a suffix in that case, surfaced by the body's NEXT-line logic).
- No existing audit, command, agent, or skill needs to be updated to call `/context-map`. The command is consumer-driven (a human or `/draft-initiative`'s NEXT line invokes it).

## Risks

- **Risk: prompt drift between spec and command body.** The eight per-section interactive prompts are the load-bearing user-facing surface; paraphrasing them silently at command-author time would survive the convention's contract test (which doesn't check prompt copy) but would surface only at adversarial review. Mitigation: T13's anchor checks (one grep per prompt's distinctive substring) catch the drift mechanically. If T13 fails, the body is re-edited to restore the verbatim phrasing.
- **Risk: skeleton-vs-augmenting-form mismatch.** The skeleton ships with the creating-command form as the live `argument-hint:` and the augmenting form as a comment. The AUTHOR step (Task 1) explicitly deletes the creating-form line and promotes the augmenting form. If the author misses this substitution, T4 catches it (and the resulting `argument-hint:` would fail T4's exact-match regex).
- **Risk: NEXT-line phrasing drift.** The NEXT line must be exactly `NEXT: /end-to-end-flow <initiative-slug>` per T7's regex. If the author writes `NEXT /end-to-end-flow` (no colon) or `NEXT: /end-to-end-flow $1`, the test fails. Mitigation: T7's anchor is the literal string.
- **Risk: P4.5 (`/end-to-end-flow`) doesn't ship in the same session, leaving a NEXT line pointing at a non-existent command.** Mitigation: the convention's kit-drift policy permits the `(planned — ROADMAP P4.5)` suffix; the body cites this in §"Chaining hint". The default body lands without the suffix (assuming same-session ship); if P4.5 slips, the suffix is added in a follow-up edit at session-end.
- **Risk: adversarial reviewer surfaces a Blocking finding that requires a spec change.** Mitigation: spec is editable in-session per the work-loop's "drift is a bug" rule; if the finding is structural (e.g., the augmenting Step 1 should check for the README's existence before checking the child file's existence), edit the spec, re-execute Task 1's prompt-copy edits, re-run T2 and T11.

## Changelog

-
- 2026-05-23: EXECUTE / REVIEW / CAPTURE completed in supervisor's batch fan-out across all seven F4 template-fill commands. Body lint clean; inscope contract tests pass; pre-pr green.
