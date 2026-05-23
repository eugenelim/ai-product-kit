# Plan: cmd-spec-impact-analysis

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

Author one file: `.claude/commands/spec-impact-analysis.md`. Start from `.claude/commands/_meta/command-skeleton.md` as the H2 scaffold, then surgically replace skeleton Steps 2–4 (template-instantiation, interactive H2-walk, human_owned_decisions confirmation) with the analyst-graph-traversal Steps documented in the spec's §"Body-shape contract":

1. Resolve the spec folder (positional + optional `--from-initiative`).
2. Build the typed graph via `scripts.lib.graph.build(root)`.
3. Walk upward / downward / sideways via the existing `Graph` queries; detect cross-team boundaries against the parent initiative's `crosses_teams:` list; surface risk flags (orphan ancestors, dangling edges, high-risk Requirement count, cycle membership).
4. Emit the three labelled header lines plus five report H2 sections to stdout. No artifact write.

Keep `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do` as the four H2 anchors so the linter and the kit's "one shape across slash-commands" pattern remain intact. Body ≤ 120 lines (skeleton parity).

The command file itself is markdown — it has no Python code. The Python it *describes the human (or the next agent) running* is the existing `scripts.lib.graph` library plus standard-library glue. No new Python ships with this spec.

The author copies the command-skeleton, replaces argv (`<spec-slug> [--from-initiative <initiative-slug>]`), replaces the four Procedure Steps with the four analyst Steps above, replaces "What this command will not do" with the spec's §"Boundaries → Never do" bullets, and authors the `description:` frontmatter (≤ 1024 chars; one sentence).

## Constraints

- **No graph-traversal reimplementation.** The command body MUST cite `scripts/lib/graph.py` (or `scripts.lib.graph`) and explicitly state that traversal is delegated. Reviewer T7 checks this.
- **No artifact write under any code path.** Reviewer T5 + acceptance-criterion: no `Write`, no `Edit`, no append. The command's body explicitly enumerates the "stdout only" contract.
- **Stdlib-only inside any Python the command instructs a runtime caller to invoke.** The consumed library (`scripts.lib.graph`) is itself stdlib + `pyyaml`; this command does not add new dependencies. (Clarification: the command file is markdown — Python only enters via the *consumed* library, not via per-command code.)
- **Body ≤ 120 lines** to remain readable in a single screen and to match the skeleton-parity convention across Phase-4 commands.
- **Three labelled header lines verbatim.** `PHASE: ...`, `VERDICT: ...`, `NEXT: ...`, in that order, ALL-CAPS labels, `:` and a single space. This shape is shared with Wave-3 siblings P4.2 and P4.10; cross-cutting reviewer enforces.
- **Four-code exit semantics** mirror the Phase-4 convention: 0 success, 1 internal error, 2 pre-conditions failed, 3 reserved.
- **F4-deviation declaration verbatim** in the command body — the sentence the spec's T5 locks.

## Construction tests

(All per-task tests live under Tasks below. No cross-cutting tests beyond the seven contract tests T1–T7 already enumerated in the spec.)

## Tasks

### Task 1: Author `.claude/commands/spec-impact-analysis.md` per the spec

- **Depends on:** none.
- **Tests:** (Tests-before-Approach — these gate the task; running them is the success criterion.)
  - T1 — `tools/lint-command.sh .claude/commands/spec-impact-analysis.md` exits 0.
  - T2 — Body H2 sections appear in order: `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`.
  - T3 — Body H1 is exactly `# /spec-impact-analysis`.
  - T4 — `description:` frontmatter ≤ 1024 chars.
  - T5 — Body contains the verbatim F4-deviation declaration sentence (per spec §"Contract tests" T5).
  - T6 — Body declares the three-line verdict-header shape and the four verdict labels with precedence.
  - T7 — Body cites `scripts/lib/graph.py` (or `scripts.lib.graph`) and explicitly states no traversal reimplementation.
- **Approach:**
  - Copy `.claude/commands/_meta/command-skeleton.md` to `.claude/commands/spec-impact-analysis.md`.
  - Replace frontmatter: `description:` (one sentence ≤ 1024 chars summarizing the spec's Objective); `argument-hint: <spec-slug> [--from-initiative <initiative-slug>]`.
  - Replace H1 with `# /spec-impact-analysis`.
  - Author the `## When to run` triggers (after editing a spec; before requesting handoff-packet generation; during a cross-team review).
  - Author the `## Inputs` block — positional, flag, consumed library API surface.
  - Replace `## Procedure` Steps 1–6 with four Steps per spec §"Body-shape contract".
  - Author the `## What this command will not do` list from spec §"Boundaries → Never do".
  - Inline the F4-deviation declaration sentence verbatim near the top of `## Procedure` (visible to both reader and grep-based reviewer).
  - Inline the verdict-header shape and precedence in `## Procedure` Step 4 with a fenced code block sample of the stdout shape.
- **Done when:** all seven Tests above pass via manual reproduction (lint script + `grep`).

### Task 2: Lint and self-check before declaring EXECUTE complete

- **Depends on:** Task 1.
- **Tests:** (Tests-before-Approach.)
  - `tools/lint-command.sh .claude/commands/spec-impact-analysis.md` exits 0.
  - Manual gesture against an existing in-kit spec — the command author (or supervisor) reads the body end-to-end and confirms the stdout report shape would be unambiguous if a human-or-agent followed it step-by-step. (Phase-4 commands are interpreted by Claude at runtime, not executed by a Python entrypoint, so "manual gesture" here means a tabletop walk-through of the body against a real spec folder.)
- **Approach:**
  - Run `tools/lint-command.sh` on the written file.
  - If T1 fails, fix and re-run. Hard iteration cap: 3 (a Phase-4 command file shouldn't take more).
  - Spot-check T2 through T7 with `grep -F` patterns.
- **Done when:** lint exits 0 and all spot-checks return their expected match.

## Rollout

CAPTURE-phase work; **supervisor handles, this plan does not do**:

- INVENTORY row update for `/spec-impact-analysis` (add or flip from planned-to-shipped).
- ROADMAP P4.9 row flip from `[ ]` to `[x]` with `Shipped: <date>`.
- Spec status flip from `Draft` → `Approved` (after plan review) → `Shipped` (after CAPTURE).
- Commit of the spec/plan pair (Task 1 of supervisor's chain).
- A second commit covering the implementation file (Task 2 of supervisor's chain).

No additional caller wiring is required — the command is invoked by humans (or by the orchestrator agent when a slash-command is typed). No audit, no other command, no skill calls `/spec-impact-analysis` programmatically.

## Risks

- **Risk:** the F4-deviation declaration sentence drifts from the spec's T5 (e.g., section-symbol vs dashed-section variant) and the cross-cutting reviewer flags T5 as failing.
  - **Mitigation:** Open-question in spec already names both variants as acceptable. Author picks one and commits to it; the test grep tolerates both.

- **Risk:** the verdict-header shape across the three Wave-3 siblings (P4.2, P4.9, P4.10) diverges in spacing (e.g., one uses `PHASE :` with a space-before-colon, another uses `PHASE:`).
  - **Mitigation:** spec locks the shape verbatim. Cross-cutting reviewer is named in the supervisor's plan as the single integrator across the three; this risk is owned at that level.

- **Risk:** the F1 graph's lack of spec→spec dependency modeling leaves "Downstream consumers" empty for nearly every real spec, weakening the command's perceived value.
  - **Mitigation:** spec's Open Question already surfaces this. The command states the limit explicitly in the report when the section is empty. Follow-up extension is a separate ROADMAP row, not this one.

- **Risk:** ambiguous spec-slug detection (multiple initiatives) trips up users who don't know about `--from-initiative`.
  - **Mitigation:** exit code 2 with the explicit remediation "ambiguous; pass --from-initiative". Documented in the command body's `## What this command will not do` bullet "Not silently pick when multiple matches".

## Changelog

- (none yet — initial draft)
