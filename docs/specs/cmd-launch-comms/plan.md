# Plan: cmd-launch-comms

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

Four serial tasks, each a coherent commit-sized unit of work, ordered so the templates (substantive content) ship before the command (which references them). The command's body cites the template paths and the per-audience H2 structure verbatim; if the templates land second, the command file's references would dangle through PLAN-phase review.

1. **Ship the three audience-distinct template files** at `templates/launch-comms/{internal.md, blog.md, email.md}`. Each carries universal-schema frontmatter, the proposed `object_type: Launch Communication`, an audience-specific H2 list, and a `human_owned_decisions:` list keyed to the audience (customer-facing-copy approval for blog and email; runbook / kill-switch accuracy for internal). The per-audience H2 asymmetry — internal has `## Kill-switch and rollback plan`; blog has `## Headline`; email has `## Subject line` — is encoded in the file structure so the audience-distinct contract is mechanical, not advisory.

2. **Ship the slash-command file** at `.claude/commands/launch-comms.md`. Copy `.claude/commands/_meta/command-skeleton.md`, specialise the four required H2s per the spec's §"Procedure," declare the three convention-deviations in the opening blockquote and in the file's `Constrained by:` line, and embed the per-audience prompt set from the spec verbatim. The body cites `templates/launch-comms/`, `delivery/launch-comms/`, and `delivery/handoff-packets/` so the contract-test grep checks all hit.

3. **Pass linters and contract tests.** `bash tools/lint-command.sh .claude/commands/launch-comms.md` exits 0. `python3 tools/lint-frontmatter.py --check-template templates/launch-comms/internal.md templates/launch-comms/blog.md templates/launch-comms/email.md` exits 0. The H2-asymmetry greps (T11, T12, T13) and the customer-facing-copy-approval grep (T14) all pass. `bash tools/pre-pr.sh` exits 0 (no kit-wide regression).

4. **CAPTURE** — freeze `spec.md` Status to `Shipped (<date>)`, freeze `plan.md` Status to `Done (<date>)`, flip the ROADMAP P4.13 checkbox, append a one-line `INVENTORY.md` row under §"Slash commands" naming the new command. Per the supervisor's brief, CAPTURE is the supervisor's responsibility across all four shipped Phase-4 post-ship commands, not this spec's executor.

The component is **not** a runnable Python script; it is a prose procedure for Claude Code to follow interactively, plus three markdown template files. No Python entry-point ships. The contract tests gate file-shape; a manual gesture (recorded at CAPTURE) gates audience-distinct behaviour.

## Constraints

- Must follow the parent convention (`docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands") where applicable. The three named deviations (output is a folder of interactively-filled siblings; parent is a Handoff Packet not an Initiative; output is post-ship copy) are declared in `Constrained by:` and in the command file's opening blockquote. Any *additional* deviation surfaces as a blocking adversarial-review finding.
- Must NOT modify `templates/handoff-packet/`, `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `tools/lint-command.sh`, `tools/lint-frontmatter.py`, `.claude/commands/_meta/command-skeleton.md`, or any other existing kit component. The contract surfaces those files own are upstream of this spec.
- Must NOT introduce a runnable Python script. The kit's slash-command convention is prose-procedure.
- Must NOT produce undifferentiated copy across the three audience templates. The H2-asymmetry contract (per-audience section lists that do not overlap) is the mechanical encoding of the audience-distinct rule; an executor that ships three near-identical templates fails the manual-gesture review and the H2-asymmetry contract tests (T11, T12, T13).
- Must NOT auto-publish, auto-send, or auto-link any draft to any external surface. The command writes to disk and exits.
- Must NOT commit a new ontology type without first confirming with the supervisor (open question 2). If the supervisor authorises the RFC route, the RFC lands as part of CAPTURE; if the supervisor defers, `Launch Communication` ships as a proposed value in the template frontmatter and the ontology audit at REVIEW will flag it (intentional — the flag becomes the supervisor's RFC trigger).
- Must NOT exceed the body-line soft cap (`.claude/commands/launch-comms.md` ≤ 220 body lines). The per-audience prompt verbatims push the body longer than `/handoff-packet`'s; trim back to per-prompt summaries plus a reference to the spec if the file grows past the cap.
- Must NOT introduce a fourth audience without the supervisor's explicit OK and a per-command-spec deviation note. If the audience set grows to 4+, the supervisor decides whether to split into multiple commands (per spec open question 1).

## Construction tests

Cross-cutting tests live in spec §"Contract tests" (T1–T16). Per-task tests are listed inline below.

## Tasks

### Task 1: `templates/launch-comms/{internal.md, blog.md, email.md}` shipped

- **Depends on:** none
- **Tests:**
  - `T9` — `test -f templates/launch-comms/internal.md && test -f templates/launch-comms/blog.md && test -f templates/launch-comms/email.md` (three files exist).
  - `T10` — `python3 tools/lint-frontmatter.py --check-template templates/launch-comms/internal.md templates/launch-comms/blog.md templates/launch-comms/email.md` exits 0 (all three pass template-mode lint).
  - `T11` — `grep -c "^## " templates/launch-comms/internal.md` returns 5, `grep -c "^## " templates/launch-comms/blog.md` returns 5, `grep -c "^## " templates/launch-comms/email.md` returns 4 (deliberate-asymmetry contract).
  - `T12` — `grep -c "^## Subject line$" templates/launch-comms/email.md` returns 1; same grep against the other two returns 0 (subject-line section unique to email).
  - `T13` — `grep -cE "^## Kill-switch" templates/launch-comms/internal.md` returns 1; same grep against the other two returns 0 (kill-switch section unique to internal).
  - `T14` — `grep -c "human_owned_decisions" templates/launch-comms/blog.md` returns ≥ 1; same against `email.md` returns ≥ 1 (customer-facing-copy approval surfaced).
- **Approach:**
  - `mkdir -p templates/launch-comms`.
  - Write `internal.md` with the H2 list from spec §"Inputs and outputs (template files)" — `## What shipped`, `## Who owns what at launch`, `## Kill-switch and rollback plan`, `## Internal FAQ`, `## Talking points for customer-facing teams`. Frontmatter: universal-schema base + `object_type: Launch Communication`, `audience: internal-team`, `parent_handoff_packet: <placeholder>`, plus `human_owned_decisions:` with runbook + kill-switch entries.
  - Write `blog.md` with H2s `## Headline`, `## What this means for you`, `## How it works`, `## Who this is for`, `## Get started`. Frontmatter: same base + `audience: external-blog` + `human_owned_decisions:` with customer-facing-copy approval, factual-accuracy, marketing/legal/compliance review entries.
  - Write `email.md` with H2s `## Subject line`, `## Preview text`, `## Body`, `## Call to action`. Frontmatter: same base + `audience: customer-email` + same three customer-facing-copy `human_owned_decisions:` entries as blog (factual accuracy applies equally to subject lines and email body claims).
  - Confirm each file passes `--check-template` mode of `tools/lint-frontmatter.py` (which accepts angle-bracket placeholders where concrete values would otherwise be required).
- **Done when:** T9, T10, T11, T12, T13, T14 all pass.

### Task 2: `.claude/commands/launch-comms.md` shipped

- **Depends on:** Task 1
- **Tests:**
  - `T1` — `test -f .claude/commands/launch-comms.md` exits 0.
  - `T3` — `grep -cE "^## (When to run|Inputs|Procedure|What this command will not do)" .claude/commands/launch-comms.md` returns 4.
  - `T4` — `grep -cE "^argument-hint: <slug>" .claude/commands/launch-comms.md` returns 1.
  - `T5` — `grep -c "templates/launch-comms/" .claude/commands/launch-comms.md` returns ≥ 1.
  - `T6` — `grep -c "delivery/launch-comms/" .claude/commands/launch-comms.md` returns ≥ 1.
  - `T7` — `grep -c "delivery/handoff-packets/" .claude/commands/launch-comms.md` returns ≥ 1.
  - `T8` — `grep -cE "^NEXT: /launch-checklist <slug>" .claude/commands/launch-comms.md` returns ≥ 1.
  - `T17` — `grep -c "untouched" .claude/commands/launch-comms.md` returns ≥ 1 (per-file overwrite contract documented in command body).
- **Approach:**
  - `cp .claude/commands/_meta/command-skeleton.md .claude/commands/launch-comms.md`.
  - Replace the `description:` placeholder with the one-sentence summary from spec §"Spec contract" blockquote.
  - Replace `argument-hint:` with `<slug> [--audience internal|external|email|blog|all] [--from <handoff-packet-slug>] [--force]`; delete the augmenting-sub-class HTML comment hint lines.
  - Replace the `# /<command-name>` H1 with `# /launch-comms`.
  - Replace the opening blockquote with the spec's blockquote naming the three audience drafts, the customer-facing-copy human-owned-decisions, the no-auto-publish rule, the destination `delivery/launch-comms/<slug>/`, and the three convention deviations.
  - In `## When to run`, list three triggers: (a) feature has shipped or is about to ship and the parent Handoff Packet's `status:` is post-audit; (b) the kit user wants the three audience drafts assembled in one walk; (c) the comms have not yet been routed to the named approvers.
  - In `## Inputs`, list the seven inputs from spec §"Inputs and outputs."
  - In `## Procedure`, keep the six skeleton steps and specialise per spec §"Procedure": Step 1 — `delivery/handoff-packets/` candidate filter; Step 2 — `mkdir -p delivery/launch-comms/<slug>/` and per-`--audience` copy from `templates/launch-comms/`; Step 3 — walk the per-audience prompt sets per spec §"Per-audience differentiation"; Step 4 — surface human-owned decisions per audience (customer-facing-copy approval for blog and email); Step 5 — lint each written file; Step 6 — `NEXT: /launch-checklist <slug>` with `(planned — ROADMAP P4.14)` suffix if unshipped.
  - In `## What this command will not do`, list the eight non-behaviours from spec §"Boundaries → Never do": no undifferentiated copy; no auto-publish; no fabrication; no skipping the customer-facing-copy-approval step; no modifying `templates/launch-comms/`; no new ontology type without an RFC; no Option-B destination; no silent parent pick.
  - Keep body ≤ 220 lines. Per-audience prompts may be cited by reference to the spec for length control (e.g., "see `docs/specs/cmd-launch-comms/spec.md` §'Per-audience differentiation' for the verbatim prompts; the prompts are repeated below").
- **Done when:** T1, T3, T4, T5, T6, T7, T8 all pass.

### Task 3: linters and contract tests green

- **Depends on:** Task 2
- **Tests:**
  - `T2` — `bash tools/lint-command.sh .claude/commands/launch-comms.md` exits 0.
  - `T15` — `bash tools/pre-pr.sh` exits 0 (no kit-wide regression).
- **Approach:**
  - Run `bash tools/lint-command.sh .claude/commands/launch-comms.md`; iterate on body-shape issues until green. Most likely failure modes: missing one of the four required H2s (T3 catches this first); `argument-hint:` not starting with `<slug>` (T4); stray placeholder syntax in the command body.
  - Run `bash tools/pre-pr.sh`; iterate on any kit-wide regression. Most likely failure source: the new `templates/launch-comms/` directory triggers a discovery in `tools/lint-frontmatter.py` default mode (which walks `PHASE_DIRS = ["strategy", "discovery", "validation", "delivery", "market"]` — the `templates/` directory is NOT in `PHASE_DIRS`, so default-mode lint should skip it; verify by inspection before relying on the behaviour).
  - If `tools/pre-pr.sh` regresses on a different surface, debug to root cause; do NOT mask with a skip flag.
- **Done when:** T2, T15 both pass.

### Task 4: CAPTURE

- **Depends on:** Task 3
- **Tests:**
  - `grep -cE "^- \[x\] \*\*P4\.13\*\*" ROADMAP.md` returns 1 after CAPTURE (the row flipped from `[ ]` to `[x]`).
  - `grep -c "launch-comms" docs/INVENTORY.md` returns ≥ 1 (the new command appears in the slash-command inventory).
  - `grep -c "Shipped" docs/specs/cmd-launch-comms/spec.md` returns ≥ 1 (the spec Status is `Shipped (<date>)`).
  - `grep -c "Done" docs/specs/cmd-launch-comms/plan.md` returns ≥ 1 (the plan Status is `Done (<date>)`).
  - If `Launch Communication` is to be added as a new ontology type, an RFC under `docs/rfc/` is opened (or the supervisor has explicitly deferred per open question 2's resolution).
- **Approach:** Per the supervisor's brief, CAPTURE is the supervisor's responsibility across all four shipped Phase-4 post-ship commands, not this spec's executor. This task is named here so the work-loop has a known completion gate; the actual edits to `ROADMAP.md`, `docs/INVENTORY.md`, `spec.md` Status, and `plan.md` Status happen in the supervisor's CAPTURE stage. The executor must NOT touch any of those files inside its own stage.
- **Done when:** Supervisor's CAPTURE commit lands.

## Rollout

- `.claude/commands/launch-comms.md` is auto-discovered by Claude Code's slash-command palette; no caller-side updates needed.
- `templates/launch-comms/` is a new top-level template family directory. The kit's `tools/lint-frontmatter.py` default mode does NOT walk `templates/` (it walks `PHASE_DIRS` only); the `--check-template` mode is what gates these files in CI. No CI changes needed (CI's `scripts/tests/test_templates_instantiate.py` runs `--check-template` against every template; new template files are auto-discovered).
- `docs/INVENTORY.md` gains a one-line row under §"Slash commands" naming `/launch-comms` and its purpose. CAPTURE-phase, supervisor-owned.
- `ROADMAP.md` P4.13 checkbox flips from `[ ]` to `[x]`. CAPTURE-phase, supervisor-owned.
- `AGENTS.md` does NOT need editing — the Phase-4 chain is already described there generically; the per-command addition goes in `docs/INVENTORY.md`.
- `delivery/launch-comms/` is the new family directory the command creates on first invocation; no committed-empty placeholder is needed.
- The ontology proposal (`Launch Communication`) surfaces at REVIEW; the supervisor decides whether to open an RFC under `docs/rfc/` or defer.

## Risks

- **R1 — Executor produces undifferentiated copy across the three templates.** Mitigation: the H2-asymmetry contract (T11, T12, T13) and the per-audience H2 lists encode the differentiation mechanically. The adversarial-reviewer subagent in Stage 2 must specifically check that the three templates have non-overlapping H2 lists and audience-distinct prompts.
- **R2 — Executor ships only one template file (e.g., a single multi-audience `launch-comms.md` template).** Mitigation: T9 fails if any of the three files is missing; spec §"Acceptance criteria" lists the three-file requirement explicitly.
- **R3 — Executor adds the fourth audience (Slack / social) without supervisor OK.** Mitigation: spec open question 1 names the supervisor's split-decision authority; spec §"Boundaries → Ask first" requires sign-off; the adversarial-reviewer checks for any audience beyond the canonical three.
- **R4 — Executor commits a new ontology type `Launch Communication` to `context/frameworks/ontology.md` without an RFC.** Mitigation: spec open question 2 and §"Boundaries → Never do" forbid this without sign-off; the supervisor's CAPTURE decides the RFC route.
- **R5 — Executor adds `--non-interactive` mode or auto-publish behaviour.** Mitigation: spec §"Non-goals" and §"Boundaries → Never do" rule them out; adversarial-reviewer must flag.
- **R6 — Executor nests the destination under `delivery/handoff-packets/<slug>/launch-comms/` (Option B).** Mitigation: spec §"Destination path resolution" explicitly names Option B and rejects it; T6 grep ("delivery/launch-comms/") would still pass on an Option B implementation (the substring would appear in `delivery/handoff-packets/<slug>/launch-comms/`); adversarial-reviewer must check the documented path is Option A specifically. **Consider adding a stronger contract test that greps for the negative case** at REVIEW phase if the supervisor wants the asymmetry mechanically enforced.
- **R7 — `tools/lint-frontmatter.py` default mode rejects the new `delivery/launch-comms/` family directory when first-run drafts land there.** Mitigation: each written audience draft carries universal-schema frontmatter (pre-filled by the command in Step 2); the default-mode linter discovers and accepts the file. If a discovered path produces a discovery-list change the linter rejects on a structural basis (e.g., the family directory needs an explicit allowlist), debug to root cause and surface to the supervisor — do not silence with a per-file exclusion.
- **R8 — The body of `.claude/commands/launch-comms.md` exceeds the 220-line soft cap because the three audiences' prompt verbatims are inline.** Mitigation: Task 2's Approach allows citing the spec by reference for verbatim prompts; trim back if the body exceeds the cap.

## Changelog

-
- 2026-05-23: Shipped Wave-4 EXECUTE alongside three sibling post-ship specs; cross-cutting adversarial review surfaced and addressed 9 PLAN-phase + 3 REVIEW-phase findings (see commit messages for the load-bearing fixes).
