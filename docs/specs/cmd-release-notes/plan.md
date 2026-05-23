# Plan: cmd-release-notes

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

Two kit components, three tasks, executed in dependency order:

1. **Task 1 — write the template `templates/release-notes.md`** as a single Markdown file (≤ 60 lines). It is the smaller, more contained piece, so it goes first; the command's body will reference its exact H2 names, and writing the template first stops the command's prose from drifting from the template's shape. The template's frontmatter follows the universal-metadata schema with the four pre-filled fields (`object_type`, `status`, `ai_assistance_allowed`, `human_approval_required`) the spec mandates, plus a pre-populated `human_owned_decisions:` entry. Body has two required H2s (`## What's new`, `## Features in this release`) and one optional H2 (`### Known limitations` under `## Optional sections`). Verify with `tools/lint-frontmatter.py --check-template templates/release-notes.md` and `scripts/tests/test_templates_instantiate.py`.

2. **Task 2 — write the command file `.claude/commands/release-notes.md`** using `.claude/commands/_meta/command-skeleton.md` as the starting skeleton. Override the skeleton on three points (per the spec's F4-deviation list): replace the single-parent resolution with the two-flag (default-handoff-packet / `--from-landing`) variant; replace the `NEXT: /<command>` line with the human-review prompt; pre-populate `human_owned_decisions:` with the canonical entry. The frontmatter has exactly two keys: `description:` (one sentence, ≤ 1024 chars, mentions both parent paths and the human-review NEXT) and `argument-hint:` (exactly `<slug> [--from-landing <landing-slug>] [--force]`). Body H2s, in order: `## When to run`, `## Inputs`, `## Procedure` (Steps 1–7), `## Exit codes`, `## What this command will not do`. The `## What this command will not do` section explicitly names the three non-behaviours the spec's CT-5 asserts: "auto-publish", "internal jargon", "metrics not in".

3. **Task 3 — verify the integrated pair** by running `tools/lint-command.sh`, `tools/lint-frontmatter.py --check-template`, and `scripts/tests/test_templates_instantiate.py`, and walking the acceptance criteria in spec.md.

The "template first, command second" order is load-bearing — the command file references the template's H2 names verbatim, so authoring the command against an unwritten template would create drift.

The jargon heuristic is a tiny in-prose token list defined here (not as a separate script): `kubernetes`, `microservice`, `microservices`, `feature flag`, `feature-flag`, `rollout %`, `canary`, `dogfood`, `internal-only`, `internal only`, `eng-only`, `eng only`, `mvp` (lower-case match, case-insensitive). The list is captured in the command's `## Procedure` Step 3.2 description, not as a separate file or script. If a kit user wants a different list, they edit the command file (it's prose, intentionally).

## Constraints

- Must not introduce any new top-level dependencies. The command is pure prose; the template is pure Markdown. No Python script ships under this spec.
- The template file must be ≤ 60 lines including frontmatter (kept small so `/release-notes`'s interactive walk doesn't drag).
- The command file must pass `tools/lint-command.sh` exactly — no special-casing.
- The template file must pass `tools/lint-frontmatter.py --check-template` exactly — no special-casing.
- Must not modify `tools/lint-command.sh`, `tools/lint-frontmatter.py`, or any other linter to accommodate this command. If the linters reject something, the command/template is wrong, not the linter.
- Must not modify `scripts/tests/test_templates_instantiate.py`. The new template must integrate by being added to the directory the test walks.
- Must not modify `.claude/commands/_meta/command-skeleton.md`. The deviations are declared in this spec's `Constrained by:` block; the skeleton stays canonical.
- Must atomic-write only via the kit's standard file-write tooling at EXECUTE time (Write tool). No streaming partial writes.
- No git operations. Commits are the supervisor's job.

## Construction tests

The per-task tests are listed under each task below. The only cross-cutting check is **acceptance-criteria walk** at the end of Task 3: every checkbox in `spec.md`'s `## Acceptance criteria` is ticked before the spec's status flips to `Implementing`.

## Tasks

### Task 1: `templates/release-notes.md` exists and passes both template linters

- **Depends on:** none
- **Tests:**
  - **T1.1 — Template-linter pass.** `python3 tools/lint-frontmatter.py --check-template templates/release-notes.md` exits 0.
  - **T1.2 — Test-templates-instantiate pass.** `pytest scripts/tests/test_templates_instantiate.py -q` exits 0 with the new template included.
  - **T1.3 — Frontmatter pre-fills.** Grep-assertions on the written file: `object_type: Customer Communication` present (literal), `status: Draft` present, `ai_assistance_allowed: restricted` present, `human_approval_required: true` present, and a `human_owned_decisions:` block containing the literal substring `Approval of customer-facing claims`. (Spec CT-7.)
  - **T1.4 — Required H2s.** Grep-assertions: `^## What's new$` present, `^## Features in this release$` present, `^## Optional sections$` present, and `^### Known limitations$` present beneath the optional-sections heading. (Spec CT-8.)
  - **T1.5 — Line cap.** `wc -l templates/release-notes.md` ≤ 60.
- **Approach:**
  - Start from the universal-metadata frontmatter ordering in `docs/CONVENTIONS.md` §"Universal metadata schema".
  - Pre-fill `object_type`, `status`, `ai_assistance_allowed`, `human_approval_required`. Pre-populate `human_owned_decisions:` with the literal canonical entry.
  - All other frontmatter fields are angle-bracket placeholders per `docs/CONVENTIONS.md` §"Placeholder syntax".
  - Add a `# Handover-specific fields` YAML comment block below the universal block, containing `parent_handoff_packet:` and `parent_landing:` as alternative placeholders (one is filled per invocation; the other is omitted by the command, not left in the file).
  - Body: H1 = `# Release notes`, intro blockquote citing HANDOVERS-7 and HUMAN-AI-OWNERSHIP zone 1+3, then `## What's new` with a one-paragraph angle-bracket placeholder, then `## Features in this release` with a bulleted angle-bracket placeholder showing the 3-to-7 expected count, then `## Optional sections` containing `### Known limitations` with a bulleted placeholder.
- **Done when:** T1.1–T1.5 all pass.

### Task 2: `.claude/commands/release-notes.md` exists, passes lint-command, and matches the spec's interactivity + non-behaviour clauses

- **Depends on:** Task 1 (the command body cites Task 1's H2 names verbatim — must not drift)
- **Tests:**
  - **T2.1 — Command-linter pass.** `bash tools/lint-command.sh .claude/commands/release-notes.md` exits 0. (Spec CT-1.)
  - **T2.2 — H1 exact.** `head -1 (after frontmatter)` of the file matches `^# /release-notes$`. (Spec CT-2.)
  - **T2.3 — Body sections present.** `grep -E '^## (When to run|Inputs|Procedure|Exit codes|What this command will not do)$'` returns five matches. (Spec CT-3 + AC line on body order.)
  - **T2.4 — Argument-hint exact.** Grep the frontmatter for `^argument-hint: <slug> \[--from-landing <landing-slug>\] \[--force\]$`. (Spec CT-4.)
  - **T2.5 — Non-behaviour mentions.** `grep` for the three literal tokens in `## What this command will not do`: `auto-publish`, `internal jargon`, `metrics not in`. All three present. (Spec CT-5.)
  - **T2.6 — Description length.** Frontmatter `description:` is ≤ 1024 chars (lint-command enforces; this test re-asserts in pytest-shape for completeness). (Spec CT-10.)
- **Approach:**
  - Copy `.claude/commands/_meta/command-skeleton.md` to `.claude/commands/release-notes.md`.
  - Replace skeleton placeholders with the concrete content from spec.md's §"Procedure" and §"Interactivity contract".
  - Step 1 of `## Procedure` branches on `--from-landing`: default branch walks `delivery/handoff-packets/`; flag-set branch reads `delivery/landings/<landing-slug>.md`.
  - Step 3 of `## Procedure` lists the interactivity prompts verbatim from spec.md §"Interactivity contract", in source order, with the jargon-heuristic token list rendered inline as prose: "the heuristic flags any of `kubernetes`, `microservice`, `microservices`, `feature flag`, `feature-flag`, `rollout %`, `canary`, `dogfood`, `internal-only`, `internal only`, `eng-only`, `eng only`, `mvp` (case-insensitive)."
  - Step 7 emits the NEXT line as the *last* line of stdout: `NEXT: /launch-comms <slug>` (the Wave-4 post-ship chain continuation; the customer-facing-copy human-review gate is enforced by the pre-populated `human_owned_decisions:` entry, not by the NEXT line).
  - `## What this command will not do` lists at minimum: (1) overwrite without `--force`, (2) skip the `human_owned_decisions:` confirmation, (3) fabricate evidence (with literal "metrics not in" cross-reference), (4) batch placeholder questions, (5) silently pick a parent, (6) assume CWD is repo root for the linter, (7) auto-publish to any external surface, (8) accept "internal jargon" without prompting, (9) modify the parent packet/landing, (10) touch git.
  - End the file with the literal `$ARGUMENTS` footer that the existing shipped F4 commands carry (sentinel for the slash-command-palette renderer).
- **Done when:** T2.1–T2.6 all pass.

### Task 3: Acceptance-criteria walk closes the spec

- **Depends on:** Task 1, Task 2
- **Tests:**
  - **T3.1 — All acceptance-criteria checkboxes flip to checked.** Walk `docs/specs/cmd-release-notes/spec.md` §"Acceptance criteria"; each `[ ]` becomes `[x]` only when its predicate is verified.
  - **T3.2 — pre-pr gate clean.** `bash tools/pre-pr.sh` exits 0. (Verifies the wider integration.)
  - **T3.3 — Spec status flip.** `Status:` in spec.md flips from `Draft` to `Implementing` once T3.1 and T3.2 pass. (Mechanical edit; supervisor performs.)
- **Approach:**
  - Run each acceptance criterion's verification command, tick the box only when green.
  - Run `tools/pre-pr.sh` against the workspace; expect a clean pass.
  - Hand back to supervisor for the spec-status flip + INVENTORY/ROADMAP/commit work (out of scope for this spec).
- **Done when:** T3.1–T3.3 all pass.

## Rollout

- **INVENTORY.md:** add a row for `/release-notes` under Phase-4 commands. (Supervisor performs at CAPTURE phase — out of this spec's task scope.)
- **ROADMAP.md:** flip P4.12 to `[x]`, append a `**Shipped:** <date>` annotation. (Supervisor.)
- **AGENTS.md:** no change required — AGENTS.md does not enumerate every Phase-4 command individually. Verify at REVIEW that no link to a planned `/release-notes` reference needs unblocking.
- **`docs/CONVENTIONS.md`:** no change required — the F4 template-fill convention sub-section already documents the deviation-declaration pattern this spec uses. If the cross-cutting REVIEW agrees the post-ship sub-class deserves its own paragraph in the convention, that's a follow-up RFC, not this spec's job.
- **No new callers:** the command is human-invoked. No audit, hook, or other command calls `/release-notes` directly. That's expected for a post-ship comms command.
- **Discoverability:** the slash-command palette discovers `.claude/commands/release-notes.md` automatically via the existing discovery mechanism — no manual wire-up.

## Risks

- **R1 — Template growth.** If P4.13 lands variants and the template needs splitting, the rollout cost is moving `templates/release-notes.md` into `templates/launch-comms/release-notes.md` and updating the command's path reference. Cost is low; surface as an open question in spec, not as a Task.
- **R2 — Jargon heuristic false positives.** A customer-domain word that happens to match a heuristic token (e.g., "canary" deployment vs "canary" the bird) could prompt unnecessarily. Mitigated by making the prompt non-blocking — the human always overrides. Surface as spec open question 5.
- **R3 — Two-parent confusion.** The `--from-landing` path is a flag-conditional behaviour that humans may forget exists. Mitigated by the `description:` frontmatter explicitly naming both parent paths so the palette renderer surfaces both.
- **R4 — F4 contract test breakage.** If a Phase-4-convention contract test exists at EXECUTE time and asserts mutual-exclusion between the two existing sub-classes (creating / augmenting), it will fail on `/release-notes`. Mitigation: at EXECUTE time, inspect `scripts/tests/` for the test, and either (a) skip it for `/release-notes` with a pytest marker if the test author anticipated the post-ship sub-class, or (b) escalate the deviation to the supervisor as an open spec question. Do not modify the test silently.

## Changelog

-
- 2026-05-23: Shipped Wave-4 EXECUTE alongside three sibling post-ship specs; cross-cutting adversarial review surfaced and addressed 9 PLAN-phase + 3 REVIEW-phase findings (see commit messages for the load-bearing fixes).
