# Plan: cmd-draft-initiative

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy for `/draft-initiative <slug>`. Unlike the spec, this document is allowed to change as you learn. When it changes substantially, note why in the changelog at the bottom.

## Approach

`/draft-initiative` is a single markdown command file — `.claude/commands/draft-initiative.md` — that follows the convention's body shape verbatim. It is **prose-procedure** (Claude interprets the body to drive the interactive walk), not a script. No Python is written for this command; the interactivity is the model running the documented procedure against the parent Vision and the F3.7 folder template. The command file copies its shape from `.claude/commands/_meta/command-skeleton.md`, fills in the per-command specifics (parent family `delivery/visions/`, template `templates/initiative/`, destination `delivery/initiatives/<slug>/`, per-H2 prompts, NEXT line `NEXT: /context-map <slug>`), and lands under `.claude/commands/`.

Work is sequential within a single session, against the spec's contract tests T1–T13 as the gate. Three load-bearing decisions: (a) the command authors the README only — the five child files are `cp -r`-copied verbatim and left in placeholder state for downstream commands; (b) the lint after fill covers the README only, not the five children (the convention's "lint the written artifact" step is interpreted as "lint the artifact this command wrote", which is the README); (c) the Capability list is captured during the Section-2 walk as human-readable names if no `CAP-NNN` ids exist, and surfaced as a TODO comment in the README body — `capabilities.md` itself is not touched.

Verification is goal-based (lint-command + the convention's contract test auto-tightens for this row) plus a one-shot manual-gesture run against a fixture parent Vision, captured under `notes/manual-gesture-fixture.md`. No new pytest is added; the existing `scripts/tests/test_phase4_command_shape.py` covers the convention-level assertions.

## Constraints

- **No new top-level dependencies.** The command is prose-procedure; no Python, no shell scripts, no new tools.
- **No modification of `templates/initiative/`.** F3.7's template is frozen; the command consumes it by copy.
- **No modification of `tools/lint-frontmatter.py`, `tools/lint-command.sh`, or `scripts/tests/test_phase4_command_shape.py`.** The command is a consumer; convention enforcement stays in the parent spec's test module.
- **Command file body ≤ 250 lines.** The convention's body skeleton is ~70 lines; the per-command additions (prompts, pre-fill rules, exit codes, NEXT line specifics) bring the total under 250 lines. If the file grows beyond that during authoring, surface as a finding.
- **`description:` frontmatter ≤ 1024 chars** (per `tools/lint-command.sh`).
- **`argument-hint:` frontmatter exactly `<slug> [--from <vision-slug>] [--force]`** (per the convention's argv contract; the `<slug>` token is load-bearing for the contract test's positional check).
- **One question at a time across the entire interactive walk.** Restated in the command body's Step 3; load-bearing per `.claude/CLAUDE.md`.

## Construction tests

Cross-cutting tests (per-task tests live under Tasks below):

- Spec contract tests T1–T13 pass after the command file lands (T9 also requires the manual-gesture fixture).
- The contract test `scripts/tests/test_phase4_command_shape.py` auto-tightens from skipped to active for the `draft-initiative` row and passes.

## Tasks

### Task 1: Author `.claude/commands/draft-initiative.md`

- **Depends on:** none
- **Tests:**
  - T1 — `test -f .claude/commands/draft-initiative.md` (file exists)
  - T2 — `bash tools/lint-command.sh .claude/commands/draft-initiative.md` exits 0
  - T3 — body contains all four convention-required H2 sections (`## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`)
  - T4 — `argument-hint:` starts with the literal `<slug>` token
  - T5 — body cites `templates/initiative/` and the path exists in the repo
  - T6 — body cites `delivery/initiatives/<slug>/` and `delivery/initiatives/` exists in the repo
  - T7 — six Step-N sub-sections appear in convention order
  - T8 — exactly four exit-code documentation lines (0, 1, 2, 3)
  - T12 — body contains `NEXT: /context-map <slug>`
  - T13 — body does NOT contain a `REVIEW:` line
- **Approach:**
  - Copy `.claude/commands/_meta/command-skeleton.md` to `.claude/commands/draft-initiative.md` as the starting body.
  - Replace the skeleton's placeholder H1 `# /<command-name>` with `# /draft-initiative`.
  - Fill the blockquote orientation paragraph: this is an artifact-creating command that gates Handover 5 (Initiative → Spec), consumes `templates/initiative/`, writes `delivery/initiatives/<slug>/`, leaves the five child files in placeholder state.
  - Fill `## When to run` with three triggers: (a) after a Vision is approved and `status:` is in the active set; (b) when a single bet (intent → vision) needs to be decomposed into deliverable scope; (c) at the start of a quarterly delivery planning session against a chosen Vision.
  - Fill `## Inputs` with the four-item list from the spec's §"Inputs and outputs": positional `<slug>`, template path `templates/initiative/`, parent Vision from `delivery/visions/<vision-slug>.md` (with the parent-resolution rule restated inline), optional flags.
  - Fill `## Procedure` with the six Step-N sub-sections, restating the convention's verbatim wording for each Step plus the per-command additions: Step 1 names `delivery/visions/` as the parent family and the `Deprecated` filter; Step 2 specifies `cp -r` (not `cp`) and lists the seven pre-fill fields; Step 3 enumerates the README H2 walk in source order with the verbatim prompts from spec §"Per-section interactive prompts"; Step 4 enumerates the three HANDOVERS-5 `human_owned_decisions:` strings; Step 5 specifies default-mode lint against the README only; Step 6 specifies the `NEXT: /context-map <slug>` line.
  - Fill `## What this command will not do` with the convention's six baseline non-behaviors plus the per-command additions: "Not write an Initiative when the chosen parent Vision's `status:` is `Deprecated`"; "Not pre-fill the `capabilities:` list with concrete ids — populate it incidentally during the README walk"; "Not modify, walk, or lint any of the five child files beyond the `cp -r` copy"; "Not auto-invoke `/context-map`, `/end-to-end-flow`, `/sequence-initiative`, or any other downstream command".
  - Fill the frontmatter: `description:` is one sentence describing what `/draft-initiative` produces and which Handover it gates (≤ 1024 chars); `argument-hint: <slug> [--from <vision-slug>] [--force]`.
- **Done when:** all per-task tests above pass. The command file is on disk and the lint and contract-test gates are clean.

### Task 2: Lint the command file

- **Depends on:** Task 1
- **Tests:**
  - `bash tools/lint-command.sh .claude/commands/draft-initiative.md` exits 0 (re-asserts T2 as a standalone gate)
  - `python3 -m pytest scripts/tests/test_phase4_command_shape.py -k draft_initiative` exits 0 (the convention's per-command assertions run cleanly against the new file)
  - `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 overall (no regression on the other six in-scope rows)
- **Approach:**
  - Run `bash tools/lint-command.sh .claude/commands/draft-initiative.md`. If it fails, read the linter's stderr and fix the surfaced issue (typically: missing `description:`, `description:` over 1024 chars, missing H1, body missing `## When to run`/`## Procedure`). Iterate up to three times; if still failing, surface as a finding.
  - Run `python3 -m pytest scripts/tests/test_phase4_command_shape.py`. If `test_inscope_commands_cite_template_path` or `test_inscope_commands_cite_destination_path` fails, verify the body cites the literal paths `templates/initiative/` and `delivery/initiatives/` respectively; if the regex doesn't match, adjust the body's prose to make the path citation literal.
- **Done when:** both pytest and lint-command exit 0 against the new command file.

### Task 3: Manual-gesture fixture

- **Depends on:** Task 2
- **Tests:**
  - T9 — `test -f docs/specs/cmd-draft-initiative/notes/manual-gesture-fixture.md`
  - The fixture documents (in prose): a sample parent Vision under `delivery/visions/<fixture-slug>.md` (slug, frontmatter `parent_intent:`, `status:`), the expected `/draft-initiative <fixture-initiative-slug>` invocation, the per-section prompts the human should see in source order, the expected `human_owned_decisions:` confirmations, the expected default-mode linter outcome on the README, and the expected `NEXT: /context-map <fixture-initiative-slug>` line.
- **Approach:**
  - Author `docs/specs/cmd-draft-initiative/notes/manual-gesture-fixture.md` with a prose script: "Given fixture Vision `<fixture-slug>` with `status: Approved`, run `/draft-initiative <fixture-initiative-slug>`. Expect (1) parent-candidate confirmation lists the fixture Vision; (2) Section-1 prompt asks for the parent Vision's `change:` restatement; (3) Section-2 prompt asks for bounded contexts then capabilities; (4) Section-3 prompt asks for first-shippable subset; (5) Section-4 prompt asks whether the optional risk register applies; (6) three sequential `human_owned_decisions:` confirmations; (7) `lint-frontmatter.py` runs against the README only and exits 0; (8) stdout ends with `NEXT: /context-map <fixture-initiative-slug>`."
  - Note the load-bearing assertions: prompts emit in source order; the five child files are bytes-identical to the template; the linter is run against the README only (not the children); the NEXT line is the literal `NEXT: /context-map <fixture-initiative-slug>` (no REVIEW line).
  - The fixture is prose-only; it does not require a real fixture Vision to be checked into `delivery/visions/`. The "manual-gesture" is the human reading the fixture and walking through the command's documented behavior to confirm correctness.
- **Done when:** the fixture file exists and documents the eight expected behaviors above.

### Task 4: Kit-wide health re-assert

- **Depends on:** Task 3
- **Tests:**
  - T10 — `bash tools/pre-pr.sh` exits 0
  - T11 — `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (re-asserts the convention's contract test passes with the `draft-initiative` row active)
  - `python3 tools/lint-frontmatter.py --all` exits 0 (sanity check that this command's authoring did not modify any product artifact under `delivery/`)
- **Approach:**
  - Run `bash tools/pre-pr.sh`. If it fails, read the surfaced finding and fix the underlying issue (typically: a stray YAML-frontmatter validation failure elsewhere in the kit unrelated to this change; if so, surface and pause).
  - Run `python3 tools/lint-frontmatter.py --all`. This command modifies no product artifacts; default-mode coverage should be unchanged.
- **Done when:** `pre-pr.sh`, the convention pytest, and `--all` linter all exit 0.

### Task 5: CAPTURE

- **Depends on:** Task 4
- **Tests:**
  - Spec frontmatter bullet block updated: `Status: Shipped (<today>)` (where `<today>` is the ISO-8601 date when REVIEW closes clean)
  - Plan frontmatter bullet block updated: `Status: Done (<today>)`
  - State file (`state.json`) marked `iteration_count` reflecting the actual iteration count, `last_commit_sha` populated, and the file remains gitignored (the kit's convention)
  - Git commit lands the new command file plus the spec/plan freeze; no ROADMAP edit (per the supervisor's instructions — supervisor handles ROADMAP/INVENTORY in Stage 5)
- **Approach:**
  - Edit `spec.md` to flip Status to `Shipped (<date>)`.
  - Edit `plan.md` to flip Status to `Done (<date>)` and add a changelog entry if the plan changed substantively during execution.
  - Stage `.claude/commands/draft-initiative.md`, `docs/specs/cmd-draft-initiative/spec.md`, `docs/specs/cmd-draft-initiative/plan.md`, and `docs/specs/cmd-draft-initiative/notes/manual-gesture-fixture.md`. Do not stage `state.json` (gitignored).
  - Commit per the kit's commit convention (see `.claude/CLAUDE.md` and the per-repo git author config).
- **Done when:** the commit lands clean and the contract-test gate stays green on the resulting branch.

## Rollout

- **Existing callers updated?** None. The command is new; no existing audit, command, agent, or skill references it. The chain of downstream commands (`/context-map`, `/end-to-end-flow`, `/sequence-initiative`, `/draft-spec`, `/handoff-packet`) will reference `/draft-initiative` as their parent-resolution upstream once they ship — but those references live in *their* specs, not in `/draft-initiative`.
- **AGENTS.md / reference doc updates?** Out of scope per the supervisor's instructions. The supervisor handles INVENTORY.md and ROADMAP.md updates in Stage 5.
- **INVENTORY.md row?** Out of scope per the supervisor's instructions.
- **No callers, no doc updates?** The command is the entry point for kit users at the Handover-4-to-Handover-5 transition; the "caller" is the human kit user invoking the slash command. The chain downstream is documented in the parent convention spec. The component is reachable.

## Risks

- **Risk: command file body grows past 250 lines.** The convention's skeleton is ~70 lines; per-command additions (prompts, pre-fill rules, exit codes, NEXT line) push toward 200-250. If authoring spills past 250, surface as a finding — the command may need a `notes/` companion file to host the verbatim prompts, with the command body citing them by reference. Mitigation: tight prose in the procedure section; prompts inline rather than re-introduced as a separate H2 inside the command file.
- **Risk: `lint-frontmatter.py --check-template` vs default mode confusion at lint-step time.** The convention specifies default mode against the written artifact. The command body must say "default mode" explicitly and must NOT pass `--check-template`. Mitigation: the command body's Step 5 prose names the flag explicitly as `(default mode, NOT --check-template)`.
- **Risk: default-mode linter raises on the five placeholder children when it walks `delivery/initiatives/<slug>/`.** Per the spec's §"Linter integration" section, the five children have no frontmatter and the linter (default mode) treats them as prose files; the linter exits 0 over the whole folder. If empirical testing during Task 2 surfaces a regression (linter walks them, parses something, raises), the command's Step 5 invocation needs to be scoped to the README path explicitly (`python3 tools/lint-frontmatter.py delivery/initiatives/<slug>/README.md`) rather than walking the folder. The spec already specifies the README-only invocation; this is a no-op risk if the spec is followed verbatim.
- **Risk: HANDOVERS-5 `active | paused | done` enum conflicts with the universal-schema `LIFECYCLE_STATES` enum during the post-fill lint.** Per F3.7 OQ1 (deferred), instantiating a real Initiative with `status: active` may fail the default-mode linter. If so, the command exits code 3 surfacing the linter failure — but it does not edit the linter or the convention. This is documented in the spec's Open Question 2 / Non-goals; the resolution is deferred to a separate spec.
- **Risk: parent-Vision auto-detection regresses against an existing Vision in the kit.** Mitigation: the command body's Step 1 prose names the exact glob (`delivery/visions/*.md`), the exact filter (status not in `{Deprecated}`), the exact sort key (`last_updated:` desc), and the exact cap (10). Verifiable against the kit's current state during Task 3.

## Changelog

-
- 2026-05-23: EXECUTE / REVIEW / CAPTURE completed in supervisor's batch fan-out across all seven F4 template-fill commands. Body lint clean; inscope contract tests pass; pre-pr green.
