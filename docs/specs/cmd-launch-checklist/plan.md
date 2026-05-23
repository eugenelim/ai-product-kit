# Plan: cmd-launch-checklist

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

Three serial commit-sized stages. **Templates are authored within this plan, not in a sibling spec** — supervisor brief mandates "If you ship a template, that's a separate task in the plan with its own tests" (singular plan, plural tasks). This plan therefore owns Task 0 (the four per-change-type template files) alongside Tasks 1–3 (the command file and gates).

0. **Author the four per-change-type template files** at `templates/launch-checklist/{new-feature,breaking-change,pricing,regulated}.md`. Each is a single-file template with universal-metadata frontmatter (proposed `object_type: Launch Checklist` per spec Open Question 6 — RFC-pending), a `change_type:` field pre-filled to the file's lens, `human_owned_decisions:` pre-populated with the change-type's canonical decisions, and a body containing exactly one `## Checklist` H2 whose body is the numbered checkbox list from spec §"Per-change-type checklist items" (items pinned verbatim by content and count: new-feature 10, breaking-change 12, pricing 11, regulated 13). Each item is a `- [ ]` line in source order. Templates pass `tools/lint-frontmatter.py --check-template`.

1. **Author the command file.** Copy `.claude/commands/_meta/command-skeleton.md` to `.claude/commands/launch-checklist.md` and specialize per spec §"Deviations from command-skeleton": frontmatter (`description:` ≤ 1024 chars naming the change-type-aware operational-artifact behavior; `argument-hint: <handoff-packet-slug> [--change-type new-feature|breaking-change|pricing|regulated] [--force]`), H1 (`# /launch-checklist`), opening blockquote (the spec's `> **Spec contract.**` paragraph minus the spec-specific language), four required H2s (`## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`). Step 1 resolves the parent **Handoff Packet** under `delivery/handoff-packets/` (not an Initiative); Step 2 asks for / accepts `--change-type`, then (before copy) for `breaking-change`/`regulated` checks `launch-considerations.md` for placeholder-shape and surfaces a blocking prompt if found (per spec §"Inputs and outputs" input 6), then copies `templates/launch-checklist/<change-type>.md` to `delivery/handoff-packets/<slug>/launch-checklist.md`; if the destination exists and `--force` is set, FIRST echo the existing file's `[x]`-confirmed items and `approvals_obtained:` and ask the human to confirm the overwrite (per spec §"Boundaries → Ask first"); Step 3 walks the checklist items one at a time; Step 4 confirms `human_owned_decisions:`; Step 5 lints the written artifact; Step 6 bumps the parent packet's README `last_updated:` and emits `NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5.x)` followed by the one-line `/retro` commentary.

2. **Pass the linters.** `bash tools/lint-command.sh .claude/commands/launch-checklist.md` exits 0; `bash tools/pre-pr.sh` exits 0. The command does NOT have a per-convention pytest contract test (the P4 Template-Fill convention's `scripts/tests/test_phase4_command_shape.py` does not auto-detect this file because the convention explicitly excludes the nine post-ship P4.x items).

3. **CAPTURE** — flip `spec.md` Status to `Shipped (<date>)`, flip `plan.md` Status to `Done (<date>)`, flip the ROADMAP P4.14 checkbox to `[x]`, append `docs/INVENTORY.md` rows under §"Slash commands" naming the new command and under §"Templates" naming the four template files. Per the supervisor brief, CAPTURE is the supervisor's responsibility across all four post-ship commands batch, not this spec's executor.

The component is **not** a runnable Python script; it is a prose procedure for Claude Code to follow interactively. No Python entry-point ships. The verification surface is the goal-based check (T1–T15) plus a manual gesture recorded at CAPTURE.

## Constraints

- Must follow `.claude/commands/_meta/command-skeleton.md` for the four required H2s and the four-code exit-code contract. Deviations from the F4 Template-Fill convention are limited to the four declared in spec §"Convention applicability"; any additional deviation surfaces as a blocking adversarial-review finding.
- Must NOT introduce a runnable Python script. The kit's slash-command convention is prose-procedure.
- Must NOT pre-fill checklist items with `[x]` confirmations. Load-bearing design decision (spec §"Boundaries → Never do"); any executor deviation is a blocking adversarial-review finding.
- Must NOT touch `templates/handoff-packet/launch-considerations.md`, `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `tools/lint-command.sh`, `tools/lint-frontmatter.py`, or `scripts/audit-completeness.py`. The contract surface those files own is upstream.
- Must author the four per-change-type template files inside this plan's Task 0 (NOT a sibling spec). The four file contents are pinned by spec §"Per-change-type checklist items" verbatim; deviation from that pinned content is a blocking adversarial-review finding.
- Must NOT emit a `REVIEW:` line. Only `/sequence-initiative` does.
- Must NOT add a fifth change-type lens beyond the four pinned. Open Question 2 is the gate.
- Command file body must stay ≤ ~250 lines (the skeleton ships ≤ 120; the per-item walk prose adds 50–80 lines; budget 250 to leave breathing room for the change-type-resolution prose in Step 2). If the file blows past 250 lines, the per-item prompt verbatim has drifted toward the spec — trim back to the H2-prompt summary.
- The NEXT-line annotation `(planned — ROADMAP P5.x)` must appear verbatim. T7 anchors it.

## Construction tests

Cross-cutting tests live in spec §"Contract tests" (T1–T15). Per-task tests are listed inline below.

## Tasks

### Task 0: Four per-change-type template files shipped at `templates/launch-checklist/`

- **Depends on:** none
- **Tests:**
  - `T13` — `test -f templates/launch-checklist/new-feature.md && test -f templates/launch-checklist/breaking-change.md && test -f templates/launch-checklist/pricing.md && test -f templates/launch-checklist/regulated.md`.
  - `T14` — for each of the four template files, `grep -cE "^## Checklist"` returns 1.
  - `T15` — numbered-item counts match: new-feature 10, breaking-change 12, pricing 11, regulated 13. Form: `grep -cE "^[0-9]+\\." templates/launch-checklist/<change-type>.md` returns the expected count.
  - For each of the four files: `python3 tools/lint-frontmatter.py --check-template templates/launch-checklist/<change-type>.md` exits 0.
  - `scripts/tests/test_templates_instantiate.py` continues to pass with the four new templates included.
- **Approach:**
  - `mkdir -p templates/launch-checklist`.
  - For each change-type, copy `templates/_meta/template-skeleton.md` (or compose directly per F3 single-file template convention) and fill:
    - Frontmatter: universal-metadata block with pre-fills `object_type: Launch Checklist` (proposed — open question 6), `change_type: <new-feature|breaking-change|pricing|regulated>`, `status: Draft`, `ai_assistance_allowed: restricted` (the per-item confirmations are human acts; AI must never pre-fill), `human_approval_required: true`. `human_owned_decisions:` pre-populated with the change-type's canonical entries (e.g., `pricing` lists "Pricing model sign-off" and "Grandfathering policy approval"; `regulated` lists "Legal/compliance sign-off" and "Named compliance-officer accountability"; `breaking-change` lists "Sunset date commitment" and "Rollback-or-stop-the-bleeding owner"; `new-feature` lists "Beta cohort selection" and "Customer comms approval").
    - Body: H1 `# Launch checklist: <change-type>`, intro blockquote citing the spec's §"Per-change-type checklist items" and the relationship to `launch-considerations.md`, then exactly one `## Checklist` H2 whose body is the numbered checkbox list from spec §"Per-change-type checklist items" — items pinned **verbatim** (do not paraphrase). Each item: `<N>. - [ ] <item text from spec>` (the leading number is the spec's item index; the checkbox is unchecked).
  - Confirm each file passes `--check-template` mode.
- **Done when:** T13, T14, T15 pass and each file lints clean.

### Task 1: `.claude/commands/launch-checklist.md` shipped with correct shape

- **Depends on:** Task 0
- **Tests:**
  - `T1` — `test -f .claude/commands/launch-checklist.md` exits 0.
  - `T3` — `grep -cE "^## (When to run|Inputs|Procedure|What this command will not do)" .claude/commands/launch-checklist.md` returns 4.
  - `T4` — `grep -cE "^argument-hint: <handoff-packet-slug>" .claude/commands/launch-checklist.md` returns 1.
  - `T5` — `grep -c "templates/launch-checklist/" .claude/commands/launch-checklist.md` returns ≥ 1.
  - `T6` — `grep -c "delivery/handoff-packets/" .claude/commands/launch-checklist.md` returns ≥ 1.
  - `T7` — `grep -c "^NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5\\.x)$" .claude/commands/launch-checklist.md` returns ≥ 1.
  - `T8` — `grep -cE "(new-feature|breaking-change|pricing|regulated)" .claude/commands/launch-checklist.md` returns ≥ 4.
  - `T9` — `grep -c "launch-considerations.md" .claude/commands/launch-checklist.md` returns ≥ 1.
  - `T10` — `grep -c "_meta/command-skeleton.md" .claude/commands/launch-checklist.md` returns 0.
- **Approach:**
  - `cp .claude/commands/_meta/command-skeleton.md .claude/commands/launch-checklist.md`.
  - Replace the frontmatter `description:` placeholder with: "Walk the change-type-aware launch checklist for an existing Handoff Packet — pick one of {new-feature, breaking-change, pricing, regulated}, copy the corresponding per-change-type template into the packet folder, walk the 10–13 items one at a time recording confirm/note/n-a per item, lint the written artifact, and chain to /landing-report." (single sentence, ≤ 1024 chars).
  - Replace the `argument-hint:` line with `<handoff-packet-slug> [--change-type new-feature|breaking-change|pricing|regulated] [--force]`. Delete the augmenting-sub-class HTML comment hint lines.
  - Replace the H1 with `# /launch-checklist`.
  - Replace the opening blockquote with a one-paragraph adaptation of spec §"Spec contract" naming HANDOVERS-6 / Handover 7 boundary, the four change-type templates, the extends-not-duplicates relationship to `launch-considerations.md`, and the `NEXT: /landing-report` chain.
  - In `## When to run`, list the triggers: (a) after the Handoff Packet's four `*_review_passed:` audit-gate fields are filled (i.e., the packet is sealed for engineering); (b) after engineering has named the launch window and change-type; (c) before the launch lever is pulled — the checklist is the operational gate.
  - In `## Inputs`, list the nine inputs from spec §"Inputs and outputs": positional `<handoff-packet-slug>`, `--change-type` flag, `--force` flag, the four template files under `templates/launch-checklist/`, the parent packet README, `launch-considerations.md`, `risks.md`, `requirements.yaml`, and `tools/lint-frontmatter.py`.
  - In `## Procedure`, keep the six-step skeleton structure and specialize each step per spec §"Deviations from command-skeleton":
    - Step 1: candidate Handoff Packets from `delivery/handoff-packets/` filtered by `status:` not equal to `Deprecated`. If `--from` is not used (none for this command — the positional is the parent, so `--from` is omitted from the argv hint entirely), the positional names the packet directly. Confirm the packet choice even when only one candidate exists (per F4 convention OQ7).
    - Step 2: if `--change-type` is absent, ask "Which change type is this launch? Choose one: new-feature, breaking-change, pricing, regulated." Then `cp templates/launch-checklist/<change-type>.md delivery/handoff-packets/<slug>/launch-checklist.md`. Pre-fill mechanical frontmatter (slug, change_type, created, last_updated, parent_handoff_packet, parent_initiative/vision/intent carried from packet README). If destination exists and `--force` is not set, exit 2.
    - Step 3: walk the checklist items one at a time (per spec §"Interactivity contract"). Per item: echo the item text, ask confirm/note/n-a, record inline, confirm back to the human, advance.
    - Step 4: confirm `human_owned_decisions:` (template ships per-change-type canonical list).
    - Step 5: run `python3 <repo-root>/tools/lint-frontmatter.py delivery/handoff-packets/<slug>/launch-checklist.md`. On non-zero, offer to re-open; exit 3 if declined or re-run fails.
    - Step 6: bump parent packet README `last_updated:` to today's date. Emit `NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5.x)`.
  - In `## What this command will not do`, list the seven non-behaviors from spec §"Boundaries → Never do" — specifically the load-bearing two: "Not pre-fill checklist items with `[x]` confirmations" and "Not touch `launch-considerations.md`".
  - Add the four-code exit-code block: `0` (success), `1` (human aborted), `2` (pre-conditions failed — slug malformed, destination exists without --force, packet not found, packet status == Deprecated, template missing, --change-type value invalid), `3` (lint failed post-write, human declined re-open).
- **Done when:** T1, T3–T10 all pass.

### Task 2: linters and pre-pr green

- **Depends on:** Task 0, Task 1
- **Tests:**
  - `T2` — `bash tools/lint-command.sh .claude/commands/launch-checklist.md` exits 0.
  - `T11` — `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Run `bash tools/lint-command.sh .claude/commands/launch-checklist.md`; iterate on body-shape issues until green. Likely failures: missing required H2, malformed frontmatter, body-line-count over a soft cap if the linter enforces one.
  - Run `bash tools/pre-pr.sh`; iterate on any kit-wide regression. Most likely regression source is a stray placeholder syntax violation; the prior test catches most of those first.
  - Task 0 must already be green (its T13–T15 tests anchor the template files); if any of those tests regressed since Task 0, return there.
- **Done when:** T2, T11 both pass; Task 0's T13–T15 remain green.

### Task 3: CAPTURE

- **Depends on:** Task 2
- **Tests:**
  - `grep -cE "^- \\[x\\] \\*\\*P4\\.14\\*\\*" ROADMAP.md` returns 1 after CAPTURE (the row flipped from `[ ]` to `[x]`).
  - `grep -c "launch-checklist" docs/INVENTORY.md` returns ≥ 1 (the new command appears in the slash-command inventory).
  - `grep -c "Shipped" docs/specs/cmd-launch-checklist/spec.md` returns ≥ 1 (the spec Status is `Shipped (<date>)`).
  - `grep -c "Done" docs/specs/cmd-launch-checklist/plan.md` returns ≥ 1 (the plan Status is `Done (<date>)`).
- **Approach:** Per the supervisor brief, CAPTURE is the supervisor's responsibility across the four post-ship commands batch, not this spec's executor. This task is named here so the work-loop has a known completion gate; the actual edits to `ROADMAP.md`, `docs/INVENTORY.md`, `spec.md` Status, and `plan.md` Status happen in the supervisor's CAPTURE commit. The executor must NOT touch any of those files inside its own EXECUTE stage.
- **Done when:** Supervisor's CAPTURE commit lands.

## Rollout

- `.claude/commands/launch-checklist.md` is auto-discovered by Claude Code's slash-command palette; no caller-side updates needed.
- `docs/INVENTORY.md` gains a one-line row under §"Slash commands" naming `/launch-checklist` and its purpose ("Change-type-aware post-ship operational gate. Reads a Handoff Packet, picks one of four change-type templates, walks 10–13 items one at a time, writes `delivery/handoff-packets/<slug>/launch-checklist.md`."). CAPTURE phase only, supervisor-owned.
- `ROADMAP.md` P4.14 checkbox flips from `[ ]` to `[x]`. CAPTURE phase only, supervisor-owned.
- `AGENTS.md` does NOT need editing — the phase-4 chain is described generically; per-command additions go in `docs/INVENTORY.md`. The "Commands you'll need" section may eventually gain a `/launch-checklist` line; that is the supervisor's call.
- Templates are authored within this same plan (Task 0); no sibling per-template spec is required or recommended. The four template files at `templates/launch-checklist/{new-feature,breaking-change,pricing,regulated}.md` ship in the same wave as the command file.
- The future `/landing-report` command (P5.x) will need to read `delivery/handoff-packets/*/launch-checklist.md` as input. That's a downstream concern; this spec only emits the NEXT hint with the `(planned …)` annotation.
- No `audit-*` command consumes the checklist in v1. A future `/audit-launches` could; not on the roadmap.

## Risks

- **R1 — Executor pre-fills checklist items with `[x]` confirmations.** Mitigation: spec's load-bearing decision is restated in this plan's Constraints, in Task 1's Approach (specifically Step 3 prose), and in the spec's Boundaries → Never do. Adversarial-review must explicitly check no checklist item arrived in the written command file body with a `[x]` marker.
- **R2 — Executor adds a runnable Python entry-point.** Mitigation: spec §"Non-goals" rules it out; kit's slash-command convention is prose-procedure-only.
- **R3 — Executor authors the four per-change-type template files with content drifting from spec §"Per-change-type checklist items."** Mitigation: spec §"Per-change-type checklist items" pins the items verbatim; Task 0's Approach mandates verbatim copy (no paraphrase); T15 enforces item counts; adversarial-reviewer at REVIEW phase greps for representative item literals from the spec.
- **R4 — `templates/launch-checklist/` directory is missing or templates fail `--check-template` lint.** Mitigation: Task 0 is gated by T13–T15 plus the per-file lint check. Templates must ship before Task 1 (command file references the directory).
- **R5 — Executor adds a fifth change-type lens.** Mitigation: spec Open Question 2 is the gate; only the supervisor or a follow-up spec can authorize this. Adversarial-review checks for unauthorized lens additions.
- **R6 — The NEXT-line `(planned — ROADMAP P5.x)` annotation drifts** (e.g., to `(planned — ROADMAP P5.1)` once the row is assigned a number). Mitigation: T7's exact-match anchor catches drift at lint time. If P5.x gets a concrete row number before this spec ships, the EXECUTE stage updates T7 and the body annotation together — supervisor must surface the row-number assignment as a planned coordination point.
- **R7 — The four-template item content drifts during template-spec EXECUTE.** Mitigation: spec §"Per-change-type checklist items" pins the items by number and content; the template-spec author treats those as the contract. T15 enforces item counts; manual gesture would catch item-content drift but is recorded only at CAPTURE.
- **R8 — `delivery/handoff-packets/` family directory is empty when the manual gesture runs.** Mitigation: the kit ships a fixture Handoff Packet at CAPTURE time; if no fixture exists, the manual gesture is recorded as "tested against an authored-during-test fixture" with the fixture committed to the repo.

## Changelog

-
