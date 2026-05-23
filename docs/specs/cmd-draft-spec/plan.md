# Plan: cmd-draft-spec

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending

> **Plan contract.** This is the implementation strategy for `/draft-spec` (P4.8). It mirrors the per-command authoring sequence used by the other six F4 fan-out workers: copy the skeleton, fill the body, lint, run the contract test, capture.

## Approach

`/draft-spec` is a single markdown file at `.claude/commands/draft-spec.md`, copied from `.claude/commands/_meta/command-skeleton.md` and filled per the spec's §"Body-shape contract". The work is a single-file write plus two verifications (lint + pytest). No new scripts, no new templates, no tool changes.

The load-bearing sequence is: (1) author the body, (2) run `tools/lint-command.sh` to confirm the shape is convention-compliant, (3) run `scripts/tests/test_phase4_command_shape.py` to confirm the contract test passes (auto-discovers `draft-spec` via the `INSCOPE` constant; tightens from skip-to-assert when the file lands), (4) capture. The body has one P4.8-specific deviation from the convention (Step 6 — the `child-specs.md` append) that must be documented in the body's Step-6 prose so a reader of the command file alone understands why the side effect exists.

The command does NOT execute at author time; it's a slash-command definition that Claude Code interprets when a kit user invokes it. Verification is shape-only at this layer; interactive-behavior verification happens at first real use against a real Initiative folder.

## Constraints

- Must not modify `templates/pm-spec.md`. Frozen by F3.8 as of 2026-05-22.
- Must not modify `.claude/commands/_meta/command-skeleton.md` or any other F4 sibling command. The skeleton is the source the command is copied from; the siblings are their own per-command specs.
- Must not modify `tools/lint-command.sh`, `tools/lint-frontmatter.py`, `scripts/tests/test_phase4_command_shape.py`, or any other tool/test. The contract test auto-discovers the new command via `INSCOPE`.
- Must not modify `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, or any of the seven F3.x template files. Frozen.
- Must not edit `ROADMAP.md` or `docs/INVENTORY.md` in this plan's tasks — the supervising orchestrator's CAPTURE phase handles those per the brief.
- Body must stay ≤ ~120 lines (skeleton-budget; matches the convention's "≤ 120 body lines" rule for the skeleton itself, applied to the filled commands by analogy). Hard cap 150 lines; revisit only if exceeded.
- Argv `argument-hint:` must match exactly `<slug> [--from <initiative-slug>] [--force]` (per spec §"Body-shape contract" → "Frontmatter").
- Must declare all seven Procedure steps explicitly with the verbatim prompts from spec §"Per-section interactive prompts".

## Construction tests

The spec's §"Contract tests" T1–T12 are the construction-test set. They are listed per-task below. T13 is left to the supervising orchestrator's CAPTURE.

## Tasks

### Task 1: author `.claude/commands/draft-spec.md`

- **Depends on:** none
- **Tests:**
  - T1: `test -f .claude/commands/draft-spec.md` exits 0.
  - T3: The four required H2 sections appear in order: `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`.
  - T4: `argument-hint:` line matches `^argument-hint: <slug> \[--from <initiative-slug>\] \[--force\]$`.
  - T5: `description:` present, ≤ 1024 chars.
  - T6: Body cites `templates/pm-spec.md` ≥ 1 time.
  - T7: Body cites `delivery/initiatives/` ≥ 1 time.
  - T8: Body cites `child-specs.md` ≥ 2 times (Inputs/intro + Step 6 procedure).
  - T9: Body cites the F3.8 single-file destination form `delivery/initiatives/<initiative-slug>/specs/<slug>.md` ≥ 1 time.
  - T10: Body emits the chain-ambiguity annotation containing `If more PM Specs remain` ≥ 1 time.
- **Approach:**
  - `cp .claude/commands/_meta/command-skeleton.md .claude/commands/draft-spec.md`.
  - Replace `<command-name>` with `draft-spec` in H1.
  - Fill frontmatter `description:` (one sentence; e.g., "Draft a PM Spec under an existing Initiative, walking templates/pm-spec.md interactively. Appends a row to the parent Initiative's child-specs.md.") and `argument-hint:` with the artifact-creating form per spec §"Body-shape contract".
  - Fill the intro blockquote: artifact-creating; cites `templates/pm-spec.md`; cites destination; cites HANDOVERS §"Handover 5".
  - Fill `## When to run` with the three bullets from spec §"Body-shape contract" → "When to run".
  - Fill `## Inputs` with the four numbered inputs from spec §"Inputs and outputs".
  - Fill `## Procedure` with seven Step-N sub-sections per spec §"Body-shape contract" → "Procedure". Step 6 is the P4.8-specific `child-specs.md` append; the prose must explain why (load-bearing Handover-5 traceability).
  - Inside Step 3, list the per-section interactive prompts verbatim from spec §"Per-section interactive prompts".
  - Inside Step 2, list the pre-fill rules verbatim from spec §"Pre-fill rules".
  - Inside Step 5, document the linter integration (resolve repo root, run default mode, exit-code handling).
  - Inside Step 7, document the NEXT line and the chain-ambiguity annotation.
  - Fill `## What this command will not do` with the bullets from spec §"Body-shape contract" → "What this command will not do".
- **Done when:** all tests T1, T3–T10 pass. The body is ≤ ~120 lines.

### Task 2: lint the command file

- **Depends on:** Task 1
- **Tests:**
  - T2: `bash tools/lint-command.sh .claude/commands/draft-spec.md` exits 0.
- **Approach:**
  - Run the linter; surface any errors; iterate on the body until exit 0.
  - Common failures: H1 missing leading `/`; frontmatter `description:` over 1024 chars; YAML frontmatter malformed.
- **Done when:** lint-command exits 0.

### Task 3: run the F4 contract test

- **Depends on:** Task 2
- **Tests:**
  - T11: `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0.
  - T12: `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Run the F4 contract test; it auto-discovers `draft-spec` via the convention's `INSCOPE` constant and tightens from skip-to-assert.
  - The test asserts: lint-command passes; required H2s present; `argument-hint:` starts with `<slug>` per the `POSITIONAL` map (artifact-creating sub-class); cited template path `templates/pm-spec.md` exists; cited destination directory `delivery/initiatives/` exists.
  - Run pre-pr; iterate if anything regresses.
- **Done when:** pytest and pre-pr both exit 0.

### Task 4: CAPTURE — update spec status

- **Depends on:** Task 3
- **Tests:** none (documentation-only)
- **Approach:**
  - Flip `state.json` `plan_review_status` from `pending` to `approved` only after the supervising orchestrator's review.
  - Flip the spec header `Status:` from `Draft` to `Shipped (<YYYY-MM-DD>)` at CAPTURE time per the supervisor's two-commit rollout.
  - Leave ROADMAP and INVENTORY edits to the supervisor's CAPTURE pass — not in this plan per the brief.
- **Done when:** spec status flipped and state.json updated.

## Rollout

This command is reached via the `/draft-spec` slash invocation from any kit user inside the repo. No other audit, command, agent, or skill needs to be updated to call it:

- `/phase-guide` already names the Phase-4 chain abstractly; no edit required.
- `/audit-spec-linkage` (planned, not yet shipped) will read the PM Specs this command writes and verify their `parent_initiative:` resolves — but its spec is downstream; no edit here.
- `/handoff-packet` (P4.11, same fan-out batch) reads PM Specs as its primary per-feature input; its spec will cite this command as the producer; no edit here.

Doc updates handled by the supervisor's CAPTURE phase:

- `ROADMAP.md` P4.8 row → `Shipped: <YYYY-MM-DD>`.
- `docs/INVENTORY.md` — add a row for `/draft-spec` under "Phase 4 — Delivery slash commands" (or equivalent table) per the kit's INVENTORY convention.

## Risks

- **Risk: the F4 contract test's `INSCOPE` list does not include `draft-spec`.** Mitigation: confirmed by reading `docs/specs/phase-4-command-convention/spec.md` §"Outputs" item 4 — `INSCOPE` already lists `"draft-spec"` and `POSITIONAL["draft-spec"] = "<slug>"`. No test-file edit needed.
- **Risk: the `child-specs.md` append step is not validated by any kit-side test at command-author time.** Mitigation: the side effect is a runtime behavior, exercised at first real use; the spec documents it explicitly and the body explains it; downstream `/audit-spec-linkage` and `/handoff-packet` consume the result and will catch drift if the side effect goes missing. Not a blocker for ship.
- **Risk: REQ-NNN per-Initiative numbering vs FEAT-NNN kit-wide numbering inconsistency confuses adopters.** Mitigation: spec §"Open questions" Q3 and Q4 document both choices and the rationale (REQ aggregates per-Initiative in Handover 6; FEAT is universal-schema `id:` which must be kit-unique). If a reviewer disagrees, surface as a follow-up convention amendment; do not block ship.
- **Risk: EARS classification stored as inline HTML comment may collide with future linter behavior.** Mitigation: spec §"Open questions" Q7 acknowledges this and pins the resolution as "bridge form until P4.7 ships". The current default-mode linter walks frontmatter only, so the HTML comment is currently invisible; if P4.7 changes that, P4.7's spec amends `/draft-spec`.
- **Risk: body exceeds ~120 lines once all seven procedure steps + interactive prompts are inlined.** Mitigation: keep procedure-step prose in bullet form and abbreviate the prompt list to a one-line-per-H2 summary in the body; rely on the spec for the long-form rationale. Hard cap 150 lines; revisit if exceeded.

## Changelog

-
- 2026-05-23: EXECUTE / REVIEW / CAPTURE completed in supervisor's batch fan-out across all seven F4 template-fill commands. Body lint clean; inscope contract tests pass; pre-pr green.
