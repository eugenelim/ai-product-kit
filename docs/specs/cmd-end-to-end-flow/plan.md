# Plan: cmd-end-to-end-flow

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy for `.claude/commands/end-to-end-flow.md` (ROADMAP P4.5). The spec is the source-of-truth for behavior; this plan sequences the build.

## Approach

The command file is a single ≤ 200-line markdown file. Author it by copying `.claude/commands/_meta/command-skeleton.md`, then fill it for the AUGMENTING sub-class: positional `<initiative-slug>`, no `--from`, augmenting-branch instructions on every Step. Lint with `tools/lint-command.sh` and the parent F4 contract test (`scripts/tests/test_phase4_command_shape.py`). Capture (commit + roadmap flip + state freeze) only after both gates are clean.

Three load-bearing constraints from the spec govern the body:

1. The hard pre-condition: `context-map.md` must be already filled. Step 1 enforces this with an exit-2 remediation pointing at `/context-map` (spec §"Open questions" Q1 resolution).
2. Mermaid-safe identifiers. Every prompt that elicits an actor / message label restates the no-angle-brackets rule because Mermaid's tokenizer breaks on `<`/`>`.
3. The single H2 (`## End-to-end customer flow`) walks eight prompts in spec-pinned order. Every prompt is quoted verbatim in the spec; the command body re-quotes them inside Step 3.

Sequence: author → lint → pytest → CAPTURE. No parallelism inside this single-file deliverable.

## Constraints

- Must not introduce new top-level dependencies. The command file is markdown; no Python, no shell.
- Must stay ≤ 200 body lines (spec T8). Terser is better; the command is a procedure, not an essay.
- Must use angle-bracket placeholder syntax in the command body's prose (the kit's universal placeholder rule) BUT must explicitly forbid angle brackets inside the Mermaid block the command tells the kit user to write. Restate the distinction in the body so an adopter reading the command file sees it.
- Must not modify `templates/initiative/flow.md`, `templates/initiative/context-map.md`, the parent convention, the linter, or the contract test.
- Must not add a `REVIEW:` line to the chaining hint (spec Never-do; that line belongs to `/sequence-initiative`).
- Must cite the parent convention by spec path in the orientation paragraph.

## Construction tests

Cross-cutting tests are listed in spec §"Contract tests" (T1–T13). All other tests live under per-task `Tests:` subsections below.

## Tasks

### Task 1: Author `.claude/commands/end-to-end-flow.md`

- **Depends on:** none
- **Tests:**
  - T1: `test -f .claude/commands/end-to-end-flow.md` exits 0.
  - T2: `bash tools/lint-command.sh .claude/commands/end-to-end-flow.md` exits 0.
  - T3: Frontmatter has exactly two keys (`description:`, `argument-hint:`).
  - T4: `argument-hint: <initiative-slug> [--force]` exactly (no `--from`).
  - T5: Four required H2 sections present in order.
  - T6: Body cites `templates/initiative/flow.md` and `delivery/initiatives/<initiative-slug>/flow.md`.
  - T7: Body cites `context-map.md` as a pre-condition AND names the `/context-map` remediation.
  - T8: Body wc -l ≤ 200.
  - T10: Body contains `NEXT: /sequence-initiative <initiative-slug>`.
  - T11: Body contains no `^REVIEW:` line.
- **Approach:**
  - Copy `.claude/commands/_meta/command-skeleton.md` to `.claude/commands/end-to-end-flow.md`.
  - Replace H1 placeholder with `# /end-to-end-flow`.
  - Set frontmatter `description:` to a one-sentence purpose (≤ 1024 chars) naming HANDOVERS-5 §"Required content" item 2 and the AUGMENTING sub-class.
  - Set `argument-hint: <initiative-slug> [--force]`. Delete the skeleton's `[--from <parent-slug>]` token entirely.
  - Replace skeleton's orientation paragraph with the spec §"Body-shape contract" item 3 paragraph.
  - Replace `## When to run` bullets with the spec §"Body-shape contract" item 4 list.
  - Replace `## Inputs` numbered list with the spec §"Body-shape contract" item 5 list.
  - Replace `## Procedure` Step-N sub-sections with the AUGMENTING-branch text per spec §"Body-shape contract" item 6: Step 1 validates folder + `context-map.md` filled; Step 2 locates the in-place `flow.md`; Step 3 walks the eight prompts from spec §"Per-section interactive prompts" verbatim; Step 4 surfaces `human_owned_decisions:`; Step 5 bumps README `last_updated:` + lints README; Step 6 emits NEXT.
  - Replace `## What this command will not do` bullets with the parent-convention defaults plus the per-command Never-do items from spec §"Boundaries → Never do" (Mermaid-safe-identifier enforcement; no auto-generation without confirmation; no `<>` inside fenced block; no lint against `flow.md` itself; no REVIEW line).
  - Inline-cite spec §"Open questions" Q1 resolution (context-map must be filled — exit 2) in Step 1's body.
  - Inline-cite the eight per-section prompts verbatim from spec §"Per-section interactive prompts" inside Step 3.
- **Done when:** all ten Task-1 tests pass.

### Task 2: Run `tools/lint-command.sh` and the parent F4 contract test

- **Depends on:** Task 1
- **Tests:**
  - T2 (re-verified): `bash tools/lint-command.sh .claude/commands/end-to-end-flow.md` exits 0.
  - T9: `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (the parent contract test auto-discovers via `INSCOPE`).
- **Approach:**
  - Invoke `tools/lint-command.sh` once. Fix any failures by editing the command file in place; never edit the linter.
  - Invoke `python3 -m pytest scripts/tests/test_phase4_command_shape.py` (the full test module — the parent's INSCOPE constant already names `end-to-end-flow`). Fix any failures.
  - If pytest reports a missing required H2, missing template-path citation, or missing destination-path citation, edit the body to add it; do not edit the test.
- **Done when:** both T2 and T9 pass cleanly with no warnings.

### Task 3: Kit-wide health check (`tools/pre-pr.sh`)

- **Depends on:** Task 2
- **Tests:**
  - T12: `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Run `tools/pre-pr.sh`. If it surfaces a regression unrelated to this command, surface it as an Open Question on the spec; do not fix in this task.
- **Done when:** T12 passes.

### Task 4: CAPTURE — roadmap flip, status freeze

- **Depends on:** Task 3
- **Tests:**
  - T13: `grep -c '^- \[x\] \*\*P4\.5\*\*' ROADMAP.md` returns 1.
- **Approach:**
  - Flip ROADMAP P4.5 checkbox from `[ ]` to `[x]`.
  - Update this spec's Status to `Shipped (<today>)`.
  - Update this plan's Status to `Done (<today>)`.
  - Set state.json `last_commit_sha:` after the commit lands (handled by the supervisor's commit phase, not this plan).
- **Done when:** T13 passes AND spec/plan status fields read Shipped / Done.

## Rollout

- Adopters of the kit gain `/end-to-end-flow <initiative-slug>` as the third link in the Phase-4 chain `/draft-initiative` → `/context-map` → `/end-to-end-flow` → `/sequence-initiative` → `/draft-spec` → `/handoff-packet`. No existing audit, command, agent, or skill needs an update (the parent convention's contract test auto-discovers the new file via `INSCOPE`).
- `docs/INVENTORY.md` does NOT need a new row at this layer — the seven F4 commands are tracked under the parent convention's INVENTORY row (per the parent spec's Outputs item 6 / ROADMAP cross-reference policy). If INVENTORY policy diverges, surface as a finding in the supervisor's adversarial review, not in this plan.
- AGENTS.md does NOT need an edit — the slash-command palette is the kit's surface; AGENTS.md references the chain conceptually under `docs/HANDOVERS.md` §"Handover 5".

## Risks

- **Risk: the kit user runs `/end-to-end-flow` against an initiative whose `context-map.md` is filled with the bounded contexts but in non-standard naming (e.g., space-separated names instead of CamelCase).** Mitigation: the actor-list prompt restates the Mermaid CamelCase constraint and asks for explicit CamelCase identifiers; the command does not auto-derive from `context-map.md`, so non-standard naming in that file does not propagate to the Mermaid block.
- **Risk: Mermaid syntax errors slip past the `--force` overwrite path.** Mitigation: out of scope per spec Non-goals — the kit has no Mermaid validator. Manual visual confirmation in Step 3 is the gate; T1–T13 do not assert Mermaid validity.
- **Risk: the body exceeds 200 lines because the eight prompts and the four exit codes are both verbose.** Mitigation: keep the eight prompts as short quoted strings; defer per-prompt rationale to this spec, not the command body.
- **Risk: the `last_updated:` bump on the README races a concurrent `/context-map` or `/sequence-initiative` run on the same initiative.** Mitigation: kit users run the Phase-4 chain sequentially per parent convention §"Capabilities-file interstitial"; concurrent edits are out of scope.

## Changelog

-
- 2026-05-23: EXECUTE / REVIEW / CAPTURE completed in supervisor's batch fan-out across all seven F4 template-fill commands. Body lint clean; inscope contract tests pass; pre-pr green.
