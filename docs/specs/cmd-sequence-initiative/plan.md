# Plan: cmd-sequence-initiative

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for `/sequence-initiative` — the Phase-4 augmenting slash command that fills `delivery/initiatives/<initiative-slug>/sequence.md` and is the unique carrier of the REVIEW interstitial pointing at `capabilities.md` before chaining to `/draft-spec`.

## Approach

`/sequence-initiative` is a single markdown file at `.claude/commands/sequence-initiative.md`. It carries the two-key frontmatter (`description:`, `argument-hint: <initiative-slug> [--force]`) and a body that follows the parent convention's skeleton (`.claude/commands/_meta/command-skeleton.md`) verbatim. The load-bearing deviation from the skeleton is Step 6 of the Procedure — the chaining hint — where this command, alone among the seven Phase-4 template-fill commands, emits a `REVIEW:` line *immediately before* the `NEXT:` line per the parent convention §"Capabilities-file interstitial".

Three properties of the implementation strategy:

1. **Copy-from-skeleton, then specialize.** Start by copying `.claude/commands/_meta/command-skeleton.md` to `.claude/commands/sequence-initiative.md`. Fill the angle-bracket placeholders per the spec. Adapt the augmenting-class branches in Step 1 (validate folder exists) and Step 2 (locate child file; skip `id:` pre-fill). Specialize Step 3 with the nine prompts from spec §"Per-section interactive prompts". Quote the REVIEW + NEXT two-line emit verbatim in Step 6.
2. **Hand-rolled gate before parametrized test.** The REVIEW-before-NEXT ordering is unique to this command and is NOT covered by `scripts/tests/test_phase4_command_shape.py`'s parametrized assertions (which check H2 presence, argv form, and cited paths — not internal line ordering of the chaining hint). Task 1's `Tests:` block therefore includes a hand-rolled grep gate that runs as part of VERIFY before declaring done. This is the regression guard against silent drift of the REVIEW line in future edits.
3. **No template / linter / test-harness modifications.** The parent convention's contract surface (skeleton, lint-command.sh, test_phase4_command_shape.py) is committed. This command consumes it; it does not modify it.

## Constraints

- Must pass `bash tools/lint-command.sh .claude/commands/sequence-initiative.md` with exit 0.
- Must not modify `.claude/commands/_meta/command-skeleton.md`, `tools/lint-command.sh`, `tools/lint-frontmatter.py`, `scripts/tests/test_phase4_command_shape.py`, or any sibling Phase-4 command file (`draft-vision.md`, `draft-initiative.md`, `context-map.md`, `end-to-end-flow.md`, `draft-spec.md`, `handoff-packet.md` — none of which exist yet but ship in the same fan-out wave).
- Must not modify any template file under `templates/`. F3.7 is committed.
- Must not introduce new ontology types.
- The `argument-hint:` frontmatter value MUST begin with the literal token `<initiative-slug>` (NOT `<slug>`) — this is how `scripts/tests/test_phase4_command_shape.py` distinguishes augmenting from creating commands.
- The REVIEW line and NEXT line MUST both appear in the body in document order REVIEW-before-NEXT. The hand-rolled gate in Task 1's `Tests:` block enforces this.
- Body length budget: target ≤ 150 lines; hard cap 200 lines. The skeleton ships at ~67 lines; nine prompts plus the per-command non-behaviors are expected to extend it. If the body exceeds 200 lines, surface as a plan-changelog entry and re-scope.

## Construction tests

Construction tests live under per-task `Tests:` subsections below. No cross-cutting tests beyond what Task 1 specifies.

## Tasks

### Task 1: Author `.claude/commands/sequence-initiative.md` and verify shape

- **Depends on:** none (the parent convention's skeleton and contract test are already shipped per `docs/specs/phase-4-command-convention/`).
- **Tests:**
  - `bash tools/lint-command.sh .claude/commands/sequence-initiative.md` exits 0 (T1).
  - `grep -c '^## When to run' .claude/commands/sequence-initiative.md` returns 1; same for `^## Inputs`, `^## Procedure`, `^## What this command will not do` (T2).
  - `awk '/^## /{print NR" "$0}' .claude/commands/sequence-initiative.md` reports the four H2s in the convention-required order (T3).
  - `grep -c '^argument-hint: <initiative-slug>' .claude/commands/sequence-initiative.md` returns 1 (T4).
  - `grep -c 'templates/initiative/sequence.md' .claude/commands/sequence-initiative.md` returns >= 1 (T5).
  - `grep -c 'delivery/initiatives/' .claude/commands/sequence-initiative.md` returns >= 1 (T6).
  - **The hand-rolled REVIEW-before-NEXT gate (T7):** run the following shell pipeline and assert exit 0 —
    ```bash
    REVIEW_LINE=$(grep -nE '^REVIEW: ' .claude/commands/sequence-initiative.md | head -1 | cut -d: -f1)
    NEXT_LINE=$(grep -nE '^NEXT: ' .claude/commands/sequence-initiative.md | head -1 | cut -d: -f1)
    test -n "$REVIEW_LINE" && test -n "$NEXT_LINE" && [ "$REVIEW_LINE" -lt "$NEXT_LINE" ]
    ```
    This asserts both lines exist AND the REVIEW line precedes the NEXT line in the document. **This test is NOT in the parametrized `scripts/tests/test_phase4_command_shape.py`** — it is unique to this command and is the regression guard against silent drift of the REVIEW line in future edits to the command body.
  - `grep -c 'capabilities.md' .claude/commands/sequence-initiative.md` returns >= 1 (T8).
  - `grep -c 'Not emit a NEXT line without the preceding REVIEW line' .claude/commands/sequence-initiative.md` returns >= 1 (T11).
- **Approach:**
  - `cp .claude/commands/_meta/command-skeleton.md .claude/commands/sequence-initiative.md`.
  - Replace the frontmatter `description:` placeholder with the one-sentence purpose from `spec.md` §"Body-shape contract".
  - Replace `argument-hint:` with `<initiative-slug> [--force]` (augmenting form; remove the creating-class comment block).
  - Replace `# /<command-name>` with `# /sequence-initiative`.
  - Replace the opening paragraph blockquote with a one-paragraph statement of what this command produces, that it is augmenting, that it gates HANDOVERS-5, and that it is the unique carrier of the REVIEW interstitial.
  - Fill `## When to run` with three triggers: (a) after `/end-to-end-flow` returns 0; (b) when the initiative's child-specs manifest is populated and the human is ready to sequence delivery; (c) before `/draft-spec` is invoked for the first time inside this initiative.
  - Fill `## Inputs` with the five-item input list from `spec.md` §"Inputs and outputs". Item 1 = positional; item 2 = template body source; item 3 = target file; item 4 = sibling-file pre-conditions; item 5 = linter (default mode).
  - Fill `## Procedure` Step 1 with the augmenting branch (validate `delivery/initiatives/<initiative-slug>/` exists; exit 2 with remediation if not).
  - Fill Step 2 with the augmenting branch (locate `sequence.md` inside the initiative folder; check for the F3.7 placeholder substrings; exit 2 if already filled and `--force` not set; verify `context-map.md` and `flow.md` are filled — no `<placeholder>` substrings — and `child-specs.md` has at least one spec slug; exit 2 with the relevant remediation if any check fails).
  - Fill Step 3 with the nine prompts from `spec.md` §"Per-section interactive prompts" → `### \`## Delivery sequence\``, quoted verbatim with their exact phrasing.
  - Fill Step 4 with the `human_owned_decisions:` walk per the parent skeleton — re-surface the initiative README's "Delivery sequencing" entry verbatim.
  - Fill Step 5 with the linter invocation against `README.md` (not against `sequence.md`).
  - Fill Step 6 with the **exact two-line emit** verbatim from `spec.md` §"Chaining hint":
    ```
    REVIEW: delivery/initiatives/<initiative-slug>/capabilities.md — verify the Capability list is filled and each row traces to a parent Problem before running /draft-spec.
    NEXT: /draft-spec <first-spec-slug>
    ```
    REVIEW immediately before NEXT, both on their own lines. Surround the two-line emit with a sentence explaining that REVIEW precedes NEXT and that they ship as a pair.
  - Fill `## What this command will not do` with the augmenting-class boilerplate plus the three command-specific Never-do lines from `spec.md` §"Boundaries → Never do": (a) "Not emit a NEXT line without the preceding REVIEW line — they ship as a pair"; (b) "Not auto-pick the first-shippable subset — the human owns sequencing decisions per the initiative README's `human_owned_decisions:` list"; (c) "Not build the DAG without consulting `context-map.md` and `flow.md` — exit code 2 with remediation if either is still in placeholder form".
  - Run the eight construction tests listed above. All must pass before this task is done.
- **Done when:** all eight construction tests pass; the command body is between 80 and 200 lines; the file is committed (CAPTURE phase handles the commit per the parent-fan-out plan).

### Task 2: Confirm parent-convention contract test now passes

- **Depends on:** Task 1.
- **Tests:**
  - `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (T9). With `sequence-initiative.md` now present, the parametrized test's previously-skipped cases for this command name auto-tighten to assert: lint-command.sh exit 0; the four required H2s; argv form (`<initiative-slug>`); the cited template path exists; the cited destination directory exists. All five should pass with no further code changes to the test module.
  - If any parametrized assertion fails, the failure is in this command's body — fix the body in Task 1 (re-open it), not the test. The contract test is committed surface.
- **Approach:**
  - Run pytest.
  - If green: proceed to Task 3.
  - If red: read the failing assertion, identify which property of the command body is mis-specified, return to Task 1 to fix the body.
- **Done when:** pytest exits 0.

### Task 3: Kit-wide health check

- **Depends on:** Task 1, Task 2.
- **Tests:**
  - `bash tools/pre-pr.sh` exits 0 (T10).
- **Approach:**
  - Run pre-pr.sh; if anything fails, identify whether the failure traces to this command's authoring or to an unrelated kit drift. If the former, return to Task 1; if the latter, surface as a plan-changelog entry and escalate (do not silently absorb).
- **Done when:** pre-pr exits 0.

### Task 4: CAPTURE — manual gesture record, ROADMAP flip, INVENTORY update

- **Depends on:** Task 1, Task 2, Task 3.
- **Tests:**
  - `docs/specs/cmd-sequence-initiative/notes/manual-gesture-record.md` exists and contains the two manual-gesture records (T12, T13) per `spec.md` §"Contract tests".
  - ROADMAP.md P4.6 checkbox flipped: `grep -c '^- \[x\] \*\*P4\.6\*\*' ROADMAP.md` returns 1.
  - INVENTORY.md (or its successor) lists `/sequence-initiative` in the "Phase-4 slash commands" section (mechanism TBD per the parent-fan-out plan; if the fan-out's Stage 5 CAPTURE owns INVENTORY updates wholesale, this sub-task is no-op here).
  - Spec status flipped to `Shipped (YYYY-MM-DD)` and plan status flipped to `Done` in the bullet blocks.
- **Approach:**
  - Author the manual-gesture record file under `notes/`, walking through both fixture scenarios (T12 exit-2 and T13 exit-0) and capturing the actual stdout for both. If a fixture initiative folder is unavailable at CAPTURE time, mark the record as "deferred to first real instantiation" and surface that as an open question.
  - Flip the ROADMAP checkbox.
  - Update spec.md and plan.md status fields.
  - Hand off to the parent-fan-out's Stage 5 supervisor for the commit and push.
- **Done when:** all four sub-tests pass and the parent supervisor has confirmed the commit.

## Rollout

- **Consumer updates:** `/end-to-end-flow` (P4.5, shipping in the same fan-out wave) names `/sequence-initiative` in its NEXT line — that wiring is owned by the cmd-end-to-end-flow spec, not by this one. No edit to existing commands here.
- **Doc updates:** AGENTS.md / .claude/CLAUDE.md / docs/INVENTORY.md updates for the seven new Phase-4 commands are owned by the parent fan-out's Stage 5 CAPTURE step, not by this per-command plan. The exception is the manual-gesture record file under `notes/`, which lives under this spec.
- **ROADMAP.md:** P4.6 checkbox flipped in Task 4.

If the supervisor's Stage 5 owns all kit-wide doc updates, this command's per-command rollout is bounded to: the command file, the manual-gesture record, the ROADMAP checkbox, and the spec/plan status flips.

## Risks

1. **Silent drift of the REVIEW line.** Future edits to the command body (e.g., a maintainer compacting Step 6) could drop or re-order the REVIEW line. Mitigation: T7 hand-rolled gate is the regression guard; documented prominently in this plan and in `spec.md`.
2. **Parametrized test divergence.** If the parametrized contract test in `scripts/tests/test_phase4_command_shape.py` evolves to enforce additional convention-specific assertions, this command's body may need to update. Mitigation: Task 2 runs the test post-authoring; any failure surfaces immediately.
3. **F3.7 template H2 growth.** If a future amendment to F3.7 adds H2s to `templates/initiative/sequence.md`, the nine-prompt walk in this command's Step 3 becomes incomplete. Mitigation: spec.md §"Non-goals" pins the command to the single `## Delivery sequence` H2; any F3.7 growth requires a per-command spec amendment.
4. **Fixture-availability gap at CAPTURE.** If no real initiative folder exists at CAPTURE time, T12 and T13 manual gestures are deferred. Mitigation: Task 4 records the deferral explicitly; the gate downgrades to "first real instantiation" rather than blocking ship.
5. **Race with sibling augmenting commands.** `/context-map`, `/end-to-end-flow`, `/sequence-initiative` all bump `last_updated:` on the initiative README. Mitigation: "last writer wins" is acceptable; the field is a monotonic date. Documented in `spec.md` §"Pre-fill rules".

## Changelog

-
- 2026-05-23: EXECUTE / REVIEW / CAPTURE completed in supervisor's batch fan-out across all seven F4 template-fill commands. Body lint clean; inscope contract tests pass; pre-pr green.
