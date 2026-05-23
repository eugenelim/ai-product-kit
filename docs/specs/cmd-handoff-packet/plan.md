# Plan: cmd-handoff-packet

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

Three serial steps, each a coherent commit-sized unit of work:

1. **Author the command file** by copying `.claude/commands/_meta/command-skeleton.md` to `.claude/commands/handoff-packet.md` and filling in the `/handoff-packet`-specific content: frontmatter (`description:`, `argument-hint:`), H1, opening blockquote, the four required H2 sections, the per-section step refinements that consume the F3.9 folder template, and the per-section non-behaviors that anchor the 22-child-placeholder choice. The skeleton's "creating commands" branches (Steps 1–2) and per-step prose are kept; the augmenting-command alternatives are deleted on copy. The body cites `templates/handoff-packet/`, `delivery/handoff-packets/`, `delivery/initiatives/` (parent family), and `/audit-completeness <slug>` (NEXT line).
2. **Pass the linters and the contract test.** `bash tools/lint-command.sh .claude/commands/handoff-packet.md` exits 0 (no body-shape regressions). `python3 -m pytest scripts/tests/test_phase4_command_shape.py -k handoff_packet` exits 0 (the parent convention's seven assertions for the `handoff-packet` row all pass — file exists, H2 superset present, argv contract starts with `<slug>`, cited template path exists, cited destination family directory exists). `bash tools/pre-pr.sh` exits 0 (no kit-wide regression).
3. **CAPTURE** — freeze `spec.md` Status to `Shipped (<date>)`, freeze `plan.md` Status to `Done (<date>)`, flip the ROADMAP P4.11 checkbox, append a one-line `INVENTORY.md` row under §"Slash commands" naming the new command. Per the supervisor's brief: CAPTURE is a separate stage handled by the supervisor across all seven shipped commands, not by this spec's executor.

The component is **not** a runnable Python script; it is a prose procedure for Claude Code to follow interactively. No Python entry-point ships. The contract test gates the file's *shape*; a manual gesture (recorded at CAPTURE phase under `notes/manual-gesture.md`) gates the file's *behavior*.

## Constraints

- Must follow the parent convention (`docs/specs/phase-4-command-convention/spec.md`) verbatim. Any deviation surfaces as a per-command-spec note in `Constrained by:` and an entry in `Boundaries → Never do`; this spec has zero deviations.
- Must NOT modify `templates/handoff-packet/`, `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `tools/lint-command.sh`, `tools/lint-frontmatter.py`, `scripts/audit-completeness.py`, or `.claude/commands/audit-completeness.md`. The contract surface those files own is upstream of this spec.
- Must NOT introduce a runnable Python script. The kit's slash-command convention is prose-procedure; the F1.5 audit script is the only Python the chain touches at runtime.
- Must NOT pre-fill the 22 child files. This is the load-bearing design decision (spec §"Boundaries → Never do"); any executor deviation is a blocking adversarial-review finding.
- Must NOT emit a `REVIEW:` line. Only `/sequence-initiative` does, per the parent convention's "Capabilities-file interstitial" sub-section.
- Must keep the command file ≤ 200 body lines (the skeleton ships ≤ 120; the F3.9 specialization adds the per-section prompts but stays under the soft cap). If it grows, the per-section prompt text has drifted toward the spec's prose; trim back to the H2-prompt summary.

## Construction tests

Cross-cutting tests live in spec §"Contract tests" (T1–T11). Per-task tests are listed inline below.

## Tasks

### Task 1: `.claude/commands/handoff-packet.md` shipped

- **Depends on:** none
- **Tests:**
  - `T1` — `test -f .claude/commands/handoff-packet.md` exits 0.
  - `T4` — `grep -cE "^## (When to run|Inputs|Procedure|What this command will not do)" .claude/commands/handoff-packet.md` returns 4.
  - `T5` — `grep -cE "^argument-hint: <slug>" .claude/commands/handoff-packet.md` returns 1.
  - `T6` — `grep -c "templates/handoff-packet/" .claude/commands/handoff-packet.md` returns ≥ 1.
  - `T7` — `grep -c "delivery/handoff-packets/" .claude/commands/handoff-packet.md` returns ≥ 1.
  - `T8` — `grep -c "^NEXT: /audit-completeness <slug>$" .claude/commands/handoff-packet.md` returns ≥ 1.
  - `T9` — `grep -c "_meta/command-skeleton.md" .claude/commands/handoff-packet.md` returns 0.
- **Approach:**
  - `cp .claude/commands/_meta/command-skeleton.md .claude/commands/handoff-packet.md`.
  - Replace the frontmatter `description:` placeholder with the one-sentence summary from spec §"Body-shape contract."
  - Replace the `argument-hint:` line with `<slug> [--from <initiative-slug>] [--force]` (creating-sub-class form; parent named as `<initiative-slug>`); delete the augmenting-sub-class HTML comment hint lines.
  - Replace the `# /<command-name>` H1 with `# /handoff-packet`.
  - Replace the opening blockquote with the spec §"Body-shape contract" opening blockquote naming HANDOVERS-6, the F3.9 template, the README's three H2s, and the 22-child-placeholder design point.
  - In `## Inputs`, list the five inputs from spec §"Inputs and outputs" (positional `<slug>`, F3.9 template path, parent Initiative resolution rule, `--from` flag, `--force` flag).
  - In `## Procedure`, keep the six skeleton steps and specialize each per spec §"Body-shape contract" (Step 1 — `delivery/initiatives/` candidate filter; Step 2 — `cp -r templates/handoff-packet/ delivery/handoff-packets/<slug>/`; Step 3 — walk the README's three H2s only; Step 4 — confirm `human_owned_decisions:`; Step 5 — lint README only; Step 6 — `NEXT: /audit-completeness <slug>`). Delete the augmenting-command alternatives at each step.
  - In `## What this command will not do`, list the ten non-behaviors from spec §"Body-shape contract" — specifically the two load-bearing ones: "Not pre-fill the 22 child files" and "Not declare the packet `Ready for Engineering`."
- **Done when:** `T1`, `T4`–`T9` all pass.

### Task 2: linters and contract test green

- **Depends on:** Task 1
- **Tests:**
  - `T2` — `bash tools/lint-command.sh .claude/commands/handoff-packet.md` exits 0.
  - `T3` — `python3 -m pytest scripts/tests/test_phase4_command_shape.py -k handoff_packet` exits 0 (all parent-convention assertions for the `handoff-packet` row pass).
  - `T10` — `bash tools/pre-pr.sh` exits 0 (no kit-wide regression).
- **Approach:**
  - Run `bash tools/lint-command.sh .claude/commands/handoff-packet.md`; iterate on body-shape issues until green.
  - Run `python3 -m pytest scripts/tests/test_phase4_command_shape.py`; the `handoff-packet` row should no longer be auto-skipped. Iterate until all seven parent-convention assertions pass.
  - Run `bash tools/pre-pr.sh`; iterate on any kit-wide regression. The most likely regression source is a stray placeholder syntax violation or a missing H2; the prior two tests should catch those first.
- **Done when:** `T2`, `T3`, `T10` all pass.

### Task 3: CAPTURE

- **Depends on:** Task 2
- **Tests:**
  - `grep -cE "^- \[x\] \*\*P4\.11\*\*" ROADMAP.md` returns 1 after CAPTURE (the row flipped from `[ ]` to `[x]`).
  - `grep -c "handoff-packet" docs/INVENTORY.md` returns ≥ 1 (the new command appears in the slash-command inventory).
  - `grep -c "Shipped" docs/specs/cmd-handoff-packet/spec.md` returns ≥ 1 (the spec Status is `Shipped (<date>)`).
  - `grep -c "Done" docs/specs/cmd-handoff-packet/plan.md` returns ≥ 1 (the plan Status is `Done (<date>)`).
- **Approach:** Per the supervisor's brief, CAPTURE is the supervisor's responsibility across all seven shipped commands, not this spec's executor. This task is named here so the work-loop has a known completion gate; the actual edits to `ROADMAP.md`, `docs/INVENTORY.md`, `spec.md` Status, and `plan.md` Status happen in the supervisor's two-commit CAPTURE stage. The executor must NOT touch any of those files inside its own stage.
- **Done when:** Supervisor's CAPTURE commit lands.

## Rollout

- `.claude/commands/handoff-packet.md` is auto-discovered by Claude Code's slash-command palette; no caller-side updates needed.
- `docs/INVENTORY.md` gains a one-line row under §"Slash commands" naming `/handoff-packet` and its purpose. CAPTURE phase only, supervisor-owned.
- `ROADMAP.md` P4.11 checkbox flips from `[ ]` to `[x]`. CAPTURE phase only, supervisor-owned.
- `AGENTS.md` does NOT need editing — the phase-4 chain is already described there generically; the per-command additions go in `docs/INVENTORY.md`.
- The parent convention's contract test (`scripts/tests/test_phase4_command_shape.py`) auto-tightens once `.claude/commands/handoff-packet.md` exists; no test code changes needed.

## Risks

- **R1 — Executor pre-fills the 22 child files.** Mitigation: the spec's load-bearing design point is restated in this plan's Constraints, in Task 1's Approach, and in the spec's Boundaries → Never do (twice). The adversarial-reviewer subagent in Stage 2 must specifically check that the executor did NOT pre-fill any of the 22 children from the parent spec(s).
- **R2 — Executor adds a runnable Python entry-point.** Mitigation: spec §"Non-goals" rules it out explicitly; the kit's slash-command convention is prose-procedure-only.
- **R3 — Executor includes an `## Optional sections` H2 on the command file.** Mitigation: the parent convention's body-structure contract names exactly four H2s; `## Optional sections` is not one of them and would fail `tools/lint-command.sh` if it shadowed any required H2. (The skeleton itself does not include the heading; this risk is small but flagged.)
- **R4 — `delivery/handoff-packets/` family directory does not exist in the repo, breaking the contract test's "cited destination directory exists" assertion.** Mitigation: verified at PLAN-phase time (`ls delivery/` shows `handoff-packets/` present); risk closed.
- **R5 — The F3.9 template's README H2 list changes between PLAN-phase and EXECUTE-phase.** Mitigation: F3.9 shipped 2026-05-22 and is frozen by its own spec; the three H2s (Product brief, Folder index, Ready-for-engineering test) are pinned by `docs/specs/template-handoff-packet/spec.md` T8b. Risk closed unless an out-of-scope edit lands.

## Changelog

-
- 2026-05-23: EXECUTE / REVIEW / CAPTURE completed in supervisor's batch fan-out across all seven F4 template-fill commands. Body lint clean; inscope contract tests pass; pre-pr green.
