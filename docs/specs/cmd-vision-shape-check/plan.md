# Plan: cmd-vision-shape-check

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending (set by supervisor after cross-cutting review)

> **Plan contract.** Implementation strategy for `.claude/commands/vision-shape-check.md`. The spec is the contract; this plan is the path.

## Approach

Copy `.claude/commands/_meta/command-skeleton.md` as the starting scaffold to get the frontmatter shape and the four-H2 outer skeleton (`## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`) for free. Then surgically replace the skeleton's body — specifically Steps 2 through 4 of the Procedure — with the analyst-shape Steps 1 → 2 → 3 declared in the spec. Keep the outer H2 frame; collapse `## Inputs` into a one-paragraph inputs declaration inside `## When to run` (or as a sibling paragraph between `## When to run` and `## Procedure`) since the analyst shape's "input" is trivially "one positional, one Vision file" and does not warrant its own H2. The deviation from the skeleton is declared verbatim inside `## What this command will not do`, citing the spec's F4-non-applicability sentence. Final body target: ≤ 120 lines.

The work is one command file plus a manual-gesture verification against a fixture Vision. No script, no test harness, no new dependency. The sequencing is: (T1) author the command file → (T2) lint and self-check. The CAPTURE-phase work (INVENTORY row, ROADMAP flip) is the supervisor's job and is deliberately out of scope for this plan; it is named in §"Rollout" for completeness.

## Constraints

- Body ≤ 120 lines (skeleton parity; the spec caps the body).
- Stdlib only at runtime — the command is a markdown prompt-file; no script dependencies introduced.
- Must pass `tools/lint-command.sh` exit 0.
- Must not introduce a new top-level folder or file outside `.claude/commands/`.
- Must not modify `templates/`, `tools/`, `docs/CONVENTIONS.md`, `docs/HANDOVERS.md`, `INVENTORY.md`, or `ROADMAP.md` from this plan.
- Must not touch `~/.ssh`, `.env*`, or any credential path (guard-credentials hook hard-blocks; do not propose).
- Must declare the F4-template-fill-convention deviation verbatim in the body.
- One clarifying question at a time at runtime; never batch (`.claude/CLAUDE.md` rule, load-bearing in Step 2).

## Construction tests

No cross-cutting construction tests beyond what's listed per-task below. The spec's T1–T6 are the gate; they are evaluated under Task 2.

## Tasks

### Task 1: Author `.claude/commands/vision-shape-check.md`

- **Depends on:** none
- **Tests:**
  - Body length ≤ 120 lines (`wc -l < .claude/commands/vision-shape-check.md`).
  - H1 line is exactly `# /vision-shape-check`.
  - Frontmatter `description:` is one sentence, ends with a period, ≤ 1024 chars.
  - Body contains both `## When to run` and `## Procedure`.
  - Body's `## What this command will not do` section contains the verbatim sentence: "This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply."
  - Body's Step 3 (Procedure → H3) names all three labels `PHASE:`, `VERDICT:`, `NEXT:` in order; names both verdict values `initiative` and `single-spec`; names both downstream commands `/draft-initiative` and `/draft-spec`.
- **Approach:**
  - Copy `.claude/commands/_meta/command-skeleton.md` to `.claude/commands/vision-shape-check.md`.
  - Replace the frontmatter `description:` placeholder with a one-sentence analyst-shape description (e.g., "Reads a Vision's `crosses_teams:` field and emits a verdict recommending `/draft-initiative` (cross-team) or `/draft-spec` (single team), asking at most one clarifying boolean if the field is ambiguous.").
  - Replace `argument-hint:` placeholder with `<slug>` (no flags).
  - Replace the H1 with `# /vision-shape-check`.
  - Rewrite the one-paragraph blurb under the H1 to describe the analyst shape (one Vision in, three-line verdict out).
  - Rewrite `## When to run` triggers (e.g., "After `/draft-vision` completes", "When a Vision has been edited and you need a fresh verdict", "Before deciding between `/draft-initiative` and `/draft-spec`").
  - Collapse the skeleton's `## Inputs` H2 into a one-paragraph inputs declaration inside `## When to run` (or as a sibling paragraph between `## When to run` and `## Procedure`). The analyst shape's inputs are trivial enough that a dedicated H2 wastes lines.
  - Rewrite `## Procedure` with three H3 Steps mapping to the spec's Step 1 (read Vision and resolve `crosses_teams:`), Step 2 (ask one clarifying boolean if and only if ambiguous), Step 3 (emit PHASE/VERDICT/NEXT header). Each Step is a single short paragraph plus a bullet or two; do not over-elaborate.
  - Rewrite `## What this command will not do` with the analyst-shape Never-do list from the spec, leading with the verbatim F4-non-applicability sentence.
- **Done when:** the file exists at `.claude/commands/vision-shape-check.md`, all six T-tests in the spec evaluate clean by visual inspection, and body line count is ≤ 120.

### Task 2: Lint and manual-gesture self-check

- **Depends on:** Task 1
- **Tests:**
  - **T1:** `tools/lint-command.sh .claude/commands/vision-shape-check.md` exits 0.
  - **Manual gesture (recorded in this plan, not automated):** mentally stand up three fixture Visions at `delivery/visions/<fixture>-{true,false,missing}.md` whose `crosses_teams:` is set to `true`, `false`, and absent respectively. Walk the command body against each fixture and confirm the three verdict-header outputs match the spec (`initiative`, `single-spec`, asks-boolean-then-matching-verdict). Record the gesture pass in `state.json` under `manual_gesture_passed: true`. (No fixture files are committed; the gesture is a static-read review against the spec.)
- **Approach:**
  - Run `tools/lint-command.sh .claude/commands/vision-shape-check.md`.
  - If non-zero, read the linter's stderr, fix the named issue in `.claude/commands/vision-shape-check.md`, re-run. Iterate up to 3 times; if still failing, stop and re-plan.
  - Walk the body against the spec's T1–T6 by inspection; confirm each.
  - Walk the body against the spec's three fixture cases by inspection; confirm the verdict-header reproduction.
- **Done when:** `tools/lint-command.sh` exits 0, and the six spec T-tests plus the three manual-gesture cases pass on visual review.

## Rollout

The command is reachable as soon as it ships: a human types `/vision-shape-check <slug>` after `/draft-vision`. No existing audit, command, agent, or skill needs to be updated to call this one (it is human-invoked, not chain-invoked).

Doc updates required at CAPTURE phase — **these are the supervisor's job, not this plan's**:

- `docs/INVENTORY.md` — new row under the Phase-4 commands family for `/vision-shape-check`.
- `ROADMAP.md` — flip P4.2 row from `[ ]` to `[x]`, add `**Shipped:** <date>`.
- Both spec and plan move `Status:` to `Approved` then `Shipped` post-execute.

If the supervisor skips either doc update, the command is shipped-but-unreachable in the kit's discovery surface. Surface that gap if it happens.

## Risks

- **Cross-cutting verdict-header drift.** P4.9 and P4.10 also adopt PHASE/VERDICT/NEXT. If those specs diverge on label casing, ordering, or punctuation, the kit ends up with three near-identical-but-non-interoperable analyst commands. Mitigation: the cross-cutting reviewer (wave-3) audits all three at once. This plan's verdict-header strings are stated verbatim in the spec so divergence is detectable.
- **The F4-non-applicability deviation is silently lost in the body.** A future editor "cleaning up" the body might drop the verbatim deviation sentence as boilerplate. Mitigation: T5 in the spec's contract tests guards it; the deviation sentence is also surfaced in §"Boundaries → Always do".
- **`crosses_teams:` semantics drift.** If `docs/HANDOVERS.md` §"Handover 4" later re-defines the field (e.g., to a list), this command's binary-boolean read breaks. Open Question Q2 in the spec captures this; mitigation is to surface the gap and ask the human, not silently parse.
- **Skeleton-copy inertia.** Copying the skeleton risks dragging in template-fill language (parent-resolution, pre-fill, linter on the written artifact) that doesn't apply here. Mitigation: Task 1's approach lists the surgical replacements explicitly; Task 2 visually walks every H2 against the spec.

## Changelog

- 2026-05-23: PLAN → EXECUTE → VERIFY → REVIEW → CAPTURE in one session as part of Wave 3 (P4.2 + P4.9 + P4.10). Cross-cutting impl review surfaced one body-shape drift: the implementation includes `## Inputs` and `## Exit codes` H2s that the spec's body-shape contract had not enumerated. Resolved by expanding the canonical body-shape list in the spec (less risky than removing useful content). Final body 74 lines, well under the 120-line cap.
