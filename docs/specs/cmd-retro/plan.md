# Plan: cmd-retro

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for `/retro`. Allowed to change as you learn; substantive shifts logged in the §"Changelog" below. The spec is the contract; this is how we build to it.

## Approach

`/retro` is a slash-command markdown file at `.claude/commands/retro.md` plus a small optional template at `templates/retro.md`. The command body's load-bearing content is a Procedure step that asks five fixed questions in a fixed order, one at a time, with confirmation between each. The template is light: frontmatter + five empty H2 sections, used to avoid hand-typing the frontmatter on every retro and to give the F3-style template linter something to check.

**Sequence rationale.** Build the template first (it's the smaller, more constrained artifact — its frontmatter and five H2 headings define the literals the command body must mirror). Then build the command body to consume the template. Then build the contract tests (CT-1 through CT-8). The order isolates the literal strings (the five questions) to one file first, so when the command body is authored it can grep-verify against the template.

**Why not skip the template.** The spec deems it optional but ships it for symmetry with the rest of Phase 4. The template carries the frontmatter scaffold (universal-metadata schema + retro-specific traceability fields) so the command doesn't have to inline a multi-line YAML block as a heredoc; that's a real ergonomics win. The template also gives the F3-style `--check-template` linter a target, which makes the contract test for the written-artifact shape mechanical.

**The five questions as load-bearing literals.** Both the template's H2 headings and the command body's prompt strings must contain the exact five literals: `What worked?`, `What didn't?`, `What surprised us?`, `What would we repeat?`, `What would we change?`. CT-2 (grep + line-number ordering) is the gate. Authoring discipline: write the five strings once in a constants comment at the top of the plan's task notes, copy-paste from there into both files, never hand-type to avoid typos.

**Component type for `tools/lint-frontmatter.py --check-template`.** The template is a single-file markdown (per F3 authoring convention §"File layout" → "Single-file template"); no folder. Placeholder syntax uses angle brackets per the convention. Frontmatter ordering: universal-metadata schema first, then a `# Handover-specific fields` comment block with retro-specific fields. `object_type: Decision` is pre-filled (template identity); all other fields are placeholders.

## Constraints

- **Must not introduce new top-level folders** under `delivery/` (AGENTS.md guard). Destination paths are `delivery/landings/<slug>-retro.md` and `delivery/handoff-packets/<slug>/retro.md` only.
- **Must not modify `templates/landing-report.md`.** F3.10 is shipped and frozen. The retro is adjacent, not nested.
- **Must not edit `INVENTORY.md` or `ROADMAP.md`** in the PLAN phase. Those are CAPTURE-phase concerns (out of scope per the orchestrator's instructions).
- **Must not write `.claude/commands/retro.md` or `templates/retro.md`** in the PLAN phase. Those are EXECUTE-phase. The plan describes the implementation; the spec describes the contract.
- **Must keep the description ≤ 1024 chars** (`tools/lint-command.sh` enforces).
- **Must follow the Phase-4 template-fill convention's body structure** (When to run / Inputs / Procedure / What this command will not do) even though the command deviates from the convention in three documented ways (per spec §"Boundaries → Deviations").
- **Must use angle-bracket placeholder syntax** in the template (per F3 §"Placeholder syntax").
- **Must atomic-write the destination file** when the command runs (write to `<dest>.tmp` then `os.replace` — same pattern used by the other Phase-4 commands' implementation guidance).

## Construction tests

Cross-cutting tests that span tasks. Per-task tests live under §"Tasks" → `Tests:` subsections.

- **Cross-cutting CT-2 ordering test:** a shell script that greps `.claude/commands/retro.md` for each of the five question literals, asserts each is found at least once, and asserts the first occurrence of each is in strictly ascending line order. This is the single most load-bearing test. It must be authored in Task 3 (Contract tests) and run as part of `tools/pre-pr.sh`.
- **Cross-cutting template-vs-command literal-string parity check:** the same five literals appear in both `templates/retro.md` (as H2 headings) and `.claude/commands/retro.md` (as prompts and/or quoted heading-text references). A grep-diff between the two files for the literal strings must be empty.

## Tasks

### Task 1: Template ships and lints clean

- **Depends on:** none
- **Tests:**
  - `tools/lint-frontmatter.py --check-template templates/retro.md` exits 0.
  - `grep -c '^## What' templates/retro.md` returns exactly 5.
  - `grep -n '^## ' templates/retro.md` lists the five `What...` H2 headings in the fixed order (line numbers strictly ascending).
  - The template's frontmatter declares `object_type: Decision` pre-filled and `human_approval_required: false` pre-filled; other universal-schema fields are angle-bracket placeholders.
- **Approach:**
  - Copy `templates/_meta/template-skeleton.md` to `templates/retro.md`.
  - Frontmatter block: universal-metadata schema in canonical order; `object_type: Decision` and `human_approval_required: false` pre-filled (template identity); `parent_landing:`, `parent_handoff_packet:`, `parent_vision:` as angle-bracket placeholders; `human_owned_decisions:` placeholder list (the explicit decisions the retro surfaces, e.g., "stop doing X"); `# Handover-specific fields` comment block carrying `retro_scope: <landing | handoff>` and `retro_facilitator: <name>` placeholders.
  - Body: H1 (`# Retrospective: <slug>`), intro blockquote citing HANDOVERS-7 and noting the retro is adjacent-not-inside to the landing report, then five H2 sections in fixed order with the exact heading text from CT-2. Each H2 has a one-line italic prompt placeholder beneath. Then a `## Cross-references` H2 stub.
  - Do not include optional sections beyond the five required H2s plus the cross-references stub (per F3 §"Required vs optional sections" — required sections appear verbatim; optional sections are out of scope for the retro because the five questions are the entire required body).
- **Done when:** the three lint/grep checks above all pass.

### Task 2: Command file ships and lints clean

- **Depends on:** Task 1
- **Tests:**
  - `tools/lint-command.sh .claude/commands/retro.md` exits 0.
  - Frontmatter `description:` is ≤ 1024 chars.
  - Frontmatter `argument-hint:` is exactly `<slug> [--scope landing|handoff] [--force]`.
  - Body contains the five literal question strings, each at least once, with first occurrences in strictly ascending line order (the cross-cutting CT-2 test).
  - Body contains both `one at a time` (or `one per turn`) AND `never batch` as literal substrings (CT-4).
  - Body contains both literal destination-path templates: `delivery/landings/<slug>-retro.md` and `delivery/handoff-packets/<slug>/retro.md` (CT-5).
  - Body contains an `## Exit codes` section naming 0, 1, 2, 3 with the convention's semantics (CT-6).
  - Body's NEXT line names `/strategy-refresh` and the planned-per-ROADMAP-P7.1 annotation (CT-8).
  - Body declares the three Phase-4 convention deviations in `## What this command will not do` (per spec acceptance criterion).
- **Approach:**
  - Copy `.claude/commands/_meta/command-skeleton.md` to `.claude/commands/retro.md`.
  - Frontmatter: `description:` ≤ 1024 chars, summarizing the facilitator shape, the five questions, the two destination paths, and the upstream-pin behavior. `argument-hint: <slug> [--scope landing|handoff] [--force]`.
  - H1: `# /retro`.
  - Intro blockquote: "Phase-4 terminal **facilitator** (deviates from the template-fill convention — see §'What this command will not do'). Asks five fixed questions in a fixed order, one at a time, never batched, and assembles answers into a retro markdown file adjacent to the upstream Landing Report or Handoff Packet. Gates the bridge from Handover 7 back into Phase 1 Strategy at the next cadence."
  - `## When to run`: after a Landing Report has been signed off OR after a Handoff Packet has shipped but before its 30-day measurement window has elapsed.
  - `## Inputs`: positional `<slug>` (upstream artifact's slug — restate the deviation explicitly), `--scope landing|handoff`, `--force`, `templates/retro.md` (the kit-provided template the command consumes), the upstream artifact body (read-only).
  - `## Procedure`: numbered steps.
    - Step 1 — resolve upstream artifact. If `--scope landing`, check `delivery/landings/<slug>.md` exists; else `delivery/handoff-packets/<slug>/README.md` exists. If no `--scope`, prefer landing if both candidates exist; if only one exists, pick it; if neither, exit 2. If BOTH exist and no `--scope`, exit 2 demanding the flag (per spec non-goal — "auto-resolve across multiple candidates").
    - Step 2 — instantiate the template. Copy `templates/retro.md` to the resolved destination. Pre-fill `id: RETRO-<NNN>` (scan `delivery/landings/*-retro.md` and `delivery/handoff-packets/*/retro.md` for max id + 1; or `001` if none); `slug:` (positional); `created:`, `last_updated:` (today); `parent_landing:` or `parent_handoff_packet:` (resolved upstream slug); `parent_vision:` (transitive carry-through from upstream); `retro_scope:` (resolved value); `object_type: Decision` (re-assert).
    - Step 3 — walk the five questions one at a time. For each: ask the literal question, wait, echo the answer back, ask "confirm or revise", then write into the corresponding H2 section. Restate the "one at a time, never batch" rule in prose.
    - Step 4 — surface `human_owned_decisions:` for explicit human confirmation. The retro's `human_owned_decisions:` captures any decisions the retro surfaces (e.g., "stop doing X", "double down on Y"). Ask the human to enumerate.
    - Step 5 — lint the written file via `python3 <repo-root>/tools/lint-frontmatter.py <written-path>` (default mode). Resolve repo root as nearest-ancestor-containing-`tools/lint-frontmatter.py`. Exit 3 if linter non-zero and human declines re-open.
    - Step 6 — emit the NEXT line: `NEXT: /strategy-refresh (planned — ROADMAP P7.1; Phase-4 chain ends here, the kit re-enters Phase 1 Strategy on a cadence decision, not an auto-chain)`.
  - `## Exit codes`: 0, 1, 2, 3 with the convention's semantics. State that exit 2 ALSO fires when both upstream candidates exist and `--scope` is absent.
  - `## What this command will not do`: enumerate the spec's `Never do` boundaries verbatim PLUS the three Phase-4 convention deviations.
- **Done when:** all eight CT-1..CT-8 checks pass against the written `.claude/commands/retro.md`.

### Task 3: Contract test script ships and runs green

- **Depends on:** Task 1, Task 2
- **Tests:**
  - `bash scripts/tests/test_cmd_retro_contract.sh` exits 0 against the just-shipped command + template.
  - The script's checks include: CT-1 (lint-command), CT-2 (five literals in order in `.claude/commands/retro.md`), CT-3 (template H2 count), CT-4 (interactivity contract strings), CT-5 (both destination paths), CT-6 (exit codes 0,1,2,3 present), CT-7 (lint-frontmatter --check-template), CT-8 (NEXT line literal).
  - The script is wired into `tools/pre-pr.sh` (or `tools/pre-pr.sh` discovers `scripts/tests/test_cmd_retro_contract.sh` and runs it).
- **Approach:**
  - Author `scripts/tests/test_cmd_retro_contract.sh` as a POSIX shell script using `grep -n`, `wc -l`, and `awk` for the ordering check. No Python dependencies.
  - The ordering check works as: for each of the five literals, run `grep -n -F '<literal>' .claude/commands/retro.md | head -1 | cut -d: -f1` and capture the first line number. Assert the five line numbers form a strictly ascending sequence.
  - Add a wiring line to `tools/pre-pr.sh` (if the aggregator does not auto-discover `scripts/tests/*.sh`). If `pre-pr.sh` already discovers test scripts by glob, no edit needed; declare so explicitly in the changelog.
  - The script exits non-zero on first failure with a one-line `lint-cmd-retro: <which check> failed` to stderr. Mirror the style of `tools/lint-command.sh`.
- **Done when:** the contract test passes on the just-shipped artifacts AND fails on a deliberately-broken copy (mutate one of the five literals; run; assert non-zero). The deliberately-broken check is a fingerprint mutation only — do not commit the broken copy.

### Task 4: Fresh-session manual gesture against a fixture

- **Depends on:** Task 2, Task 3
- **Tests:**
  - In a fresh Claude Code session: invoke `/retro fixture-landing` against a fixture at `scripts/tests/fixtures/retro-landing/delivery/landings/fixture-landing.md` (the fixture is a minimal HANDOVERS-7-shaped landing report). The session walks the five questions in order, one at a time, captures answers, writes `scripts/tests/fixtures/retro-landing/delivery/landings/fixture-landing-retro.md`, runs the linter, and emits the NEXT line.
  - The fresh-session run produces a retro file whose body has the five H2 sections with the captured answers verbatim (no synthesis, no summary).
  - The fresh-session run does NOT batch the five questions into a single prompt.
- **Approach:**
  - Create the fixture under `scripts/tests/fixtures/retro-landing/` with one minimal landing report.
  - Record the gesture (the human prompts + Claude's prompts + the human's answers) in `docs/specs/cmd-retro/notes/manual-verification-<YYYY-MM-DD>.md` per the F1-G1 precedent (the kit's manual-gesture verification artifact pattern).
  - This task is the spec's audit-driven verification mode in practice. It is the gate for declaring the command "Shipped" — the contract tests in Task 3 catch shape failures but not facilitation-style failures (e.g., a command body that contains the five literals but, at runtime, the implementing agent still batches them). The manual gesture catches that.
- **Done when:** the recorded notes file shows the five answers captured verbatim, in order, one at a time, and the written file passes `tools/lint-frontmatter.py` default mode.

## Rollout

Once Tasks 1–4 ship and verify clean:

- **AGENTS.md:** add `/retro` to the "Commands you'll need" catalog if that catalog lists Phase-4 commands. (It currently lists only the three audits + `/phase-guide` + `/cadence-check` as planned. `/retro` may not warrant a row there; the full catalog lives in INVENTORY.md per the convention.)
- **INVENTORY.md:** add a row for `/retro` under Phase 4 → Delivery. The row names the slash command, its component type (command + template), the destination paths, and the upstream artifacts it reads. **Out of scope for the PLAN phase per the orchestrator's instruction; this is a CAPTURE-phase note.**
- **ROADMAP.md:** check off P4.15 once Task 4 verifies clean. **Out of scope for the PLAN phase per the orchestrator's instruction; this is a CAPTURE-phase note.**
- **docs/HANDOVERS.md:** no edit needed. HANDOVERS-7 names the Landing Report; the retro is adjacent and does not change HANDOVERS-7's contract.
- **`.claude/skills/` or `.claude/agents/`:** no new skill or agent needed. `/retro` is self-contained.
- **No new caller wiring** — `/retro` is a human-invoked terminal facilitator. The only callers are humans (and, future, `/cadence-check` per P7.5 as a "retros owed" surfacing).

If, after shipping, no INVENTORY row exists and no documentation links to `/retro`, the command is unreachable to new adopters. The CAPTURE phase must include at minimum: INVENTORY row + a one-line mention in the AGENTS.md "Commands you'll need" section OR in the relevant phase-4-commands README.

## Risks

- **Risk 1: the five literals drift between template and command.** If a future edit changes "What surprised us?" to "What surprised the team?" in one file but not the other, CT-2 and the cross-cutting parity check both fail, but a careless author might fix only one file. **Mitigation:** the cross-cutting parity check in §"Construction tests" is the gate.
- **Risk 2: an implementing agent satisfies CT-2 by literally pasting the five strings into the command body as a single batched block** (e.g., `"Walk me through: What worked? What didn't? What surprised us? What would we repeat? What would we change?"`). CT-2 passes (all five literals present, in order), but the facilitation is batched. **Mitigation:** CT-4 catches this by requiring `one at a time` and `never batch` as separate literal substrings. The manual gesture (Task 4) catches it definitively.
- **Risk 3: the command body's destination-path-resolution logic ends up describing a parent-resolution numbered-list picker (copy-paste drift from `/draft-spec`)**. **Mitigation:** spec §"Boundaries → Deviations" and the implementation's `## What this command will not do` both explicitly forbid the picker. The cross-cutting adversarial-reviewer should catch a regression here.
- **Risk 4: the template adds optional sections (e.g., "Action items", "Owner assignments")** that creep the retro into a planning artifact. **Mitigation:** Task 1 explicitly forbids optional sections beyond the five required H2s + cross-references stub. F3 §"Required vs optional sections" supports this.
- **Risk 5: ambiguity between scope=handoff and scope=landing when both upstream candidates exist.** **Mitigation:** spec non-goal 4 + command body's `## Exit codes` section both name the "demand `--scope` when both exist" behavior. Exit 2.
- **Risk 6: a future ROADMAP P7.1 (`/strategy-refresh`) ships and the NEXT line's "(planned — ROADMAP P7.1)" annotation goes stale.** **Mitigation:** the kit-drift policy mandates demote-and-annotate; when P7.1 ships, a one-line edit removes the parenthetical. Add a CAPTURE-phase reminder when P7.1 ships.

## Changelog

Append entries when the plan changes substantially during execution. Format: `<YYYY-MM-DD>: <one-line description of the change and why>`.

-
