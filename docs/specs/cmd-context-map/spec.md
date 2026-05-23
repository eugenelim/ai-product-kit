# Spec: cmd-context-map

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command
- **Serves kit phase:** Delivery
- **Constrained by:** [`docs/specs/phase-4-command-convention/spec.md`](../phase-4-command-convention/spec.md) (parent convention — body structure, argv contract, parent-artifact-resolution rule for augmenting commands, interactive-fill behavior, pre-fill rules, linter integration, exit codes, chaining hint, in-scope command list); `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" (required content for `context-map.md` — per bounded context: owner, public contract, commodity-vs-custom Wardley, evolution stage); `templates/initiative/context-map.md` (the in-place child file this command fills — H2 set, H3 sub-template, source-of-truth comments); [`docs/specs/template-initiative/spec.md`](../template-initiative/spec.md) (F3.7 sibling — the folder template this child file lives inside; required H2 set for `context-map.md` and absence of frontmatter); `tools/lint-frontmatter.py` (default-mode linter the command runs against the filled child); `tools/lint-command.sh` (shape linter against the command file itself); [`.claude/skills/work-loop/SKILL.md`](../../../.claude/skills/work-loop/SKILL.md) (build pattern); [`.claude/CLAUDE.md`](../../../.claude/CLAUDE.md) "How we work together" (one-question-at-a-time, never batch — the interactivity contract this command enforces mechanically).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `.claude/commands/context-map.md` — the slash command that fills `delivery/initiatives/<initiative-slug>/context-map.md` interactively. This is an **artifact-augmenting** command per the parent convention: the positional argument is `<initiative-slug>` (an existing initiative folder), and the command fills the placeholder child file in place. It does NOT create a new artifact; the child file is created in placeholder form by `/draft-initiative` (P4.3) when the initiative folder is scaffolded from `templates/initiative/`. There is no `--from` flag (per the convention's §"Argv contract" augmenting case — the parent is the initiative named by the positional). The command walks the two H2 sections of the child file one section at a time, asks the human one question per placeholder, lints the filled file, updates `last_updated:` on the initiative README, and emits `NEXT: /end-to-end-flow <initiative-slug>`.

## Objective

P4.4 ships the slash command `/context-map`. Today, an initiative author who has just run `/draft-initiative` ends up with a folder containing a placeholder-shaped `context-map.md` (H2 headings + `<placeholder>` body bullets per F3.7). The author then has to (a) decide what "bounded context" means for this initiative, (b) enumerate the contexts in scope, (c) assign a named owner per context, (d) write down the public contract, (e) make the commodity-vs-custom Wardley call, (f) name the evolution stage — for every context — without leaking any one of those decisions into the wrong stage of conversation. The kit's "one question at a time, never batch" rule from `.claude/CLAUDE.md` is load-bearing; without it, the four HANDOVERS-5 fields get smeared across context blocks and the bounded-context-vs-context-vs-shared-shape distinction collapses. This command makes the walk mechanical: positional `<initiative-slug>`, verify the folder exists, locate the placeholder child file, walk H2s sequentially, lint, bump the README's `last_updated:`, emit the NEXT line.

The command is an **artifact-augmenting** command per the parent convention. It is one of three augmenting commands in the Phase-4 chain (`/context-map`, `/end-to-end-flow`, `/sequence-initiative`) that together turn the placeholder folder shipped by F3.7 into a filled Initiative folder ready for `/draft-spec`.

The closest prior context in the repo is `docs/specs/phase-4-command-convention/` (the parent convention shipped 2026-05-23 — defines the augmenting-command argv contract that has no `--from` and skips parent resolution), `docs/specs/template-initiative/` (the F3.7 sibling — defines the H2 set and the no-frontmatter rule on `context-map.md`), and `docs/specs/cmd-draft-initiative/` (the sibling artifact-creating command that scaffolds the initiative folder this command augments).

## Why now

ROADMAP P4.4 sits in the Phase-4 (Delivery) block. The parent convention (`phase-4-command-convention`) shipped 2026-05-23; F3.7 (`templates/initiative/`) shipped 2026-05-22. With both upstream contracts stable, the augmenting-command trio (`/context-map`, `/end-to-end-flow`, `/sequence-initiative`) can fan out in parallel — each one fills a single child file inside an initiative folder. Until P4.4 ships, the `context-map.md` placeholder shipped by F3.7 has no command-side filler: kit users have to walk the file's H2 set manually, re-deriving the four HANDOVERS-5 fields each time, and the kit's "one question at a time" rule is enforced only by author discipline. P4.4 makes the walk mechanical.

P4.4 also stabilizes the augmenting-command pattern for the other two siblings (P4.5 `/end-to-end-flow`, P4.6 `/sequence-initiative`) — each one mirrors P4.4's shape (positional `<initiative-slug>`, Step 1 = verify folder, Step 2 = locate placeholder child, Steps 3–5 = walk-confirm-lint, Step 6 = NEXT with the next augmenting command in the chain).

## Inputs and outputs

**Inputs.**

- The positional argument `<initiative-slug>` — kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. Names an existing initiative folder under `delivery/initiatives/`.
- `templates/initiative/context-map.md` — the source-of-shape child file. F3.7 ships this with H1 + orientation paragraph + two H2 sections (`## Bounded contexts in this initiative` and `## Per-bounded-context detail`) + a repeated H3 sub-template (`### <Bounded context name>` with four labeled body fields). This command does NOT copy or re-read the template at runtime; it walks the placeholders in the destination child file. The template path is named in the command body so the contract test (`test_inscope_commands_cite_template_path`) recognizes the augmenting-child path pattern.
- `delivery/initiatives/<initiative-slug>/context-map.md` — the in-place target. Already exists in placeholder form (created by `/draft-initiative` when the initiative folder was scaffolded from `templates/initiative/`). Contains `<placeholder>` substrings until this command fills them.
- `delivery/initiatives/<initiative-slug>/README.md` — the initiative README. Read for the `human_owned_decisions:` list (Step 4 surfacing) and the `parent_vision:` field (for orientation). Written for the `last_updated:` field (bumped to today after Step 5 succeeds).
- `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" §"Required content" item 1 — the four fields per bounded context (owner, public contract, commodity-vs-custom Wardley, evolution stage). This command's per-section interactive prompts (§"Per-section interactive prompts" below) quote the four fields verbatim.
- `tools/lint-frontmatter.py` — the default-mode linter the command runs against the filled child. The child file has no YAML frontmatter per F3.7's OQ4 resolution; the default-mode linter therefore has no frontmatter to validate on the child itself. However, the linter is also run against `delivery/initiatives/<initiative-slug>/README.md` after the `last_updated:` bump to confirm the README's frontmatter still parses (catches accidental corruption of the README during the bump). The linter command is the single command `python3 <repo-root>/tools/lint-frontmatter.py <readme-path>` per the convention §"Linter integration".

**Outputs.**

1. `.claude/commands/context-map.md` — new file. The slash-command body. Conforms to the parent convention's body structure (H2 sections `When to run`, `Inputs`, `Procedure`, `What this command will not do`), argv contract (`argument-hint: <initiative-slug> [--force]` — note the absence of `--from`), and chaining hint (`NEXT: /end-to-end-flow <initiative-slug>`). The body's full shape is contracted in §"Body-shape contract" below.
2. **No new artifact** — `context-map.md` is filled in place; no destination directory is created. The initiative folder must pre-exist; the child file must pre-exist (in placeholder form).
3. **Side effect:** `delivery/initiatives/<initiative-slug>/README.md`'s `last_updated:` field is set to today's date (ISO-8601, resolved from system clock at command-end). The README's `last_updated:` is the universal-schema field every Initiative README carries per F3.7.
4. **stdout:** the interactive walk's questions and confirmations; the linter's result; the `NEXT:` line as the last output line.

A reader of this section should be able to construct the command's argv parser and procedure shell without reading anything else.

## Body-shape contract

The new `.claude/commands/context-map.md` ships with this body skeleton, copied from `.claude/commands/_meta/command-skeleton.md` and filled per the parent convention's authoring-a-new-in-scope-command guidance:

```markdown
---
description: Fill the bounded-contexts narrative inside an existing initiative folder — walks templates/initiative/context-map.md's H2s interactively, one question at a time, then lints and bumps the initiative README's last_updated.
argument-hint: <initiative-slug> [--force]
---

# /context-map

> Augmenting command that fills `delivery/initiatives/<initiative-slug>/context-map.md` in place. Gates HANDOVERS-5 (Initiative → Spec) by populating the bounded-context fields HANDOVERS-5 §"Required content" item 1 requires (owner, public contract, commodity-vs-custom Wardley, evolution stage). Consumes `templates/initiative/context-map.md` as the source-of-shape (already instantiated by `/draft-initiative` in placeholder form). This is an artifact-augmenting command: it fills a placeholder child file inside an existing initiative folder; it does NOT create a new artifact.

## When to run

- Immediately after `/draft-initiative <initiative-slug>` completes successfully and emits `NEXT: /context-map <initiative-slug>`.
- When refining the bounded-context narrative of an initiative whose folder exists but whose `context-map.md` is still placeholder-shaped (contains `<placeholder>` substrings).
- When re-walking the contexts for an already-filled `context-map.md` (requires `--force`).

## Inputs

1. The positional arg `<initiative-slug>` — kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. Names an existing initiative folder under `delivery/initiatives/`.
2. `templates/initiative/context-map.md` — the F3.7 source-of-shape child file (H2 set and H3 sub-template).
3. The initiative folder named by the positional: `delivery/initiatives/<initiative-slug>/`. No parent resolution — augmenting commands take the parent (the initiative) as the positional argument per the convention's §"Argv contract" augmenting case and §"Parent-artifact resolution" (which explicitly skips resolution for augmenting commands).
4. The child file: `delivery/initiatives/<initiative-slug>/context-map.md`. Must already exist in placeholder form (created by `/draft-initiative` when the initiative folder was scaffolded from `templates/initiative/`).

## Procedure

### Step 1 — verify the initiative folder and child file exist

Verify `delivery/initiatives/<initiative-slug>/` exists. If not, exit code 2 with the remediation message: "no initiative folder found at `delivery/initiatives/<initiative-slug>/` — run `/draft-initiative <initiative-slug>` first."

Verify `delivery/initiatives/<initiative-slug>/README.md` exists. If not, exit code 2 with the remediation message: "initiative folder present but `README.md` missing — restore it from `templates/initiative/README.md` or re-run `/draft-initiative <initiative-slug>` (the README is the source of `human_owned_decisions:` walked in Step 4 and the target of the `last_updated:` bump in Step 5)."

Verify `delivery/initiatives/<initiative-slug>/context-map.md` exists. If not, exit code 2 with the remediation message: "no `context-map.md` found inside the initiative folder — run `/draft-initiative <initiative-slug>` first (the child file is created in placeholder form when the initiative folder is scaffolded from `templates/initiative/`)."

This is the augmenting-command equivalent of the convention's Step 1. There is NO parent-artifact resolution; the parent IS the initiative folder named by the positional.

### Step 2 — locate the placeholder child file and check it's still placeholder-shaped

Open `delivery/initiatives/<initiative-slug>/context-map.md`. If the file contains no `<placeholder>` substrings (heuristic for "already filled") and `--force` is not set, exit code 2 with the remediation message: "`context-map.md` appears already filled (no `<placeholder>` substrings remain). Re-run with `--force` to walk the H2s again and overwrite."

Augmenting commands do NOT pre-fill `id:` — there is no new artifact. They DO update `last_updated:` on the initiative README to today's date after Step 5 succeeds (Step 5 sub-step below).

### Step 3 — walk H2 sections one at a time

For each H2 in `context-map.md`, in document order, ask the human the questions named under §"Per-section interactive prompts" in this command's spec (and quoted verbatim in this body when this command is authored). Ask one question per placeholder, sequentially. Within `## Per-bounded-context detail`, the H3 sub-template `### <Bounded context name>` repeats per bounded context — walk one full H3 block (four labeled fields) before asking whether to add another bounded context. Confirm the section's filled content before advancing to the next H2.

Never batch. The kit's "one question at a time" rule from `.claude/CLAUDE.md` is load-bearing.

### Step 4 — surface human-owned decisions

Read the initiative README's `human_owned_decisions:` list (per F3.7 the README carries HANDOVERS-5's three strings verbatim: `Bounded-context ownership assignment`, `Build vs buy decisions in the evolution check`, `Delivery sequencing`). The first two are directly relevant to this command's walk. Present each to the human and ask for explicit confirmation that the decision is owned (and where applicable, signed off). Record confirmations in the initiative README's `approvals_obtained:` list (append, do not overwrite).

### Step 5 — lint the filled file and bump the README's last_updated

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`; do not assume the working directory is the repo root.

Run `python3 <repo-root>/tools/lint-frontmatter.py <repo-root>/delivery/initiatives/<initiative-slug>/README.md` (default mode). The child file `context-map.md` has no frontmatter (per F3.7's OQ4 resolution) and is not separately linted — the linter has nothing to validate on a frontmatter-less file. The README lint catches accidental corruption during the `last_updated:` bump.

- If the linter exits 0: bump the README's `last_updated:` field to today's date (ISO-8601, resolved from system clock at command-end). Proceed to Step 6.
- If the linter exits non-zero: offer to re-open the relevant sections for correction. If the human accepts and the corrections lint clean on re-run, bump `last_updated:` and proceed to Step 6 normally. If the human declines (or re-runs but lint still fails), exit code 3 with the linter output surfaced and the file left on disk. Do NOT bump `last_updated:` in the exit-3 path.

### Step 6 — emit the next-command hint

Last line of output, formatted exactly:

```
NEXT: /end-to-end-flow <initiative-slug>
```

Do NOT emit a `REVIEW:` line — only `/sequence-initiative` emits the `REVIEW: delivery/initiatives/<initiative-slug>/capabilities.md ...` line per the convention's §"Capabilities-file interstitial".

## What this command will not do

- Not create a new artifact — fills a placeholder child file in place.
- Not skip the Wardley-lite commodity-vs-custom evolution check for any context.
- Not auto-pick the bounded-context owner — always ask.
- Not overwrite an already-filled `context-map.md` without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the initiative README lacks a referenced field, ask, do not invent.
- Not batch placeholder questions — one at a time.
- Not assume the working directory is the repo root when invoking the linter.
- Not modify the initiative README beyond `last_updated:` and `approvals_obtained:`.
- Not touch `flow.md`, `sequence.md`, `child-specs.md`, or `capabilities.md` inside the same folder — those have their own commands.
```

The skeleton above is reviewed before execution, not authored during it. The author copies `.claude/commands/_meta/command-skeleton.md` and substitutes the augmenting-command path through the per-section rules in the skeleton (the `<command-name>`, the `argument-hint:` augmenting form, the augmenting variant of Steps 1/2, the per-command non-behaviors).

## Per-section interactive prompts

`templates/initiative/context-map.md` has two H2 sections, in this order: `## Bounded contexts in this initiative` and `## Per-bounded-context detail`. The latter contains a repeated H3 sub-template `### <Bounded context name>` with four labeled body fields. This command emits the following human-facing prompts, in document order, one question at a time.

### `## Bounded contexts in this initiative` — orientation paragraph

1. "What does 'bounded context' mean for this initiative? Write a one-sentence definition scoped to the initiative — the boundary criterion you'll use to decide whether two pieces of work belong in the same context or in different contexts."
2. "Which bounded contexts are explicitly **in scope** for this initiative? List them as a comma-separated list of short names — each name will become an H3 sub-section under §Per-bounded-context detail."
3. "Which bounded contexts are explicitly **out of scope** for this initiative? List them as a comma-separated list of short names. (Naming what's out of scope here prevents downstream specs from quietly absorbing the boundary.)"

### `## Per-bounded-context detail` — one H3 block per bounded context

For each bounded context named in the previous H2's question 2, walk one full H3 block (four labeled fields). The four prompts below are HANDOVERS-5 §"Required content" item 1 verbatim.

For context `<name>`:

4. **Owner.** "Who owns context `<name>`? Name a single human or team. Do NOT pick on the human's behalf, even if only one candidate is obvious from the initiative's `crosses_teams:` list — always ask. Per the initiative README's `human_owned_decisions:` list, bounded-context ownership assignment is a human-owned decision."
5. **Public contract.** "What is the public contract of context `<name>`? Write a one-sentence summary of the boundary contract — the API, event schema, or shared shape that other contexts depend on. If multiple other contexts depend on different surfaces of `<name>`, name the most load-bearing one and add a note about the others."
6. **Commodity vs custom (Wardley).** "Pick one for context `<name>`: `commodity` | `utility` | `product` | `custom`. The Wardley-lite evolution check — per the initiative README's `human_owned_decisions:` list (`Build vs buy decisions in the evolution check`), this is a human-owned decision. If the call is unclear, prefer `custom` and add a one-line note explaining the uncertainty. Do not skip this prompt for any context."
7. **Evolution stage.** "Pick one for context `<name>`: `genesis` | `custom` | `product` | `commodity`. Evolution stage names where the context is *today*; the Wardley call in the previous question names where it should be. The two often agree; when they disagree, the disagreement is itself the surfaced finding."

After all four fields are filled for context `<name>`:

8. **Add another context?** "Add another bounded context block under §Per-bounded-context detail? `y` to walk the next context, `n` to advance to Step 4 (human-owned-decisions confirmation)."

The eight prompts above are the verbatim copy this command emits. They are reviewed at spec time (now), not improvised at command-runtime. If the prompts need to change, the change is a spec edit followed by a re-author of the command body — not a quiet runtime drift.

## Pre-fill rules

Augmenting commands do **not** pre-fill `id:` — there is no new artifact. The child file `context-map.md` has no frontmatter at all (per F3.7's OQ4 resolution); there is nothing to pre-fill on the child.

The command DOES update `last_updated:` on `delivery/initiatives/<initiative-slug>/README.md` to today's date (ISO-8601, resolved from system clock at command-end) after Step 5's lint passes. This is the only side effect on the README beyond the `approvals_obtained:` append from Step 4.

If the initiative README is missing or unreadable at Step 5 time, exit code 2 with the remediation message: "initiative README not readable — `last_updated:` cannot be bumped. Verify `delivery/initiatives/<initiative-slug>/README.md` exists and parses."

## --force semantics

Per the convention's §"Argv contract" augmenting case, `--force` permits re-walking an already-filled `context-map.md`. The heuristic for "already filled" is: the file contains no `<placeholder>` substrings (Step 2). Without `--force`, an already-filled file triggers exit code 2 with the remediation to re-run with `--force`. With `--force`, Step 2 proceeds and Step 3 walks the H2s normally; the previously filled content is overwritten in place by the new walk's confirmations.

`--force` does NOT bypass Step 4 (human-owned-decisions confirmation) or Step 5 (lint). The flag's scope is the "is the child already filled?" check in Step 2 and nothing else.

## Linter integration

After Step 4 completes, the command resolves the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py` (per the convention §"Linter integration" — do not assume the working directory is the repo root), then runs `python3 <repo-root>/tools/lint-frontmatter.py <repo-root>/delivery/initiatives/<initiative-slug>/README.md` in default mode (NOT `--check-template` — the README is now a real product artifact, not a template).

The child file `context-map.md` has no frontmatter per F3.7's OQ4 resolution; default-mode `lint-frontmatter.py` has no frontmatter to validate on a frontmatter-less file. The README lint is the relevant gate because the README is the artifact whose `last_updated:` field this command bumps; if the bump accidentally corrupts the README's frontmatter, the linter catches it.

The linter's exit code is surfaced to the human verbatim. Exit 0 proceeds to the `last_updated:` bump; non-zero offers re-open-for-correction per Step 5's branching logic.

## Exit codes

Per the convention's §"Exit codes" (four codes, identical across all seven in-scope commands):

- `0` — child file walked, README `last_updated:` bumped, linter passed, NEXT line emitted.
- `1` — human aborted the interactive walk before completion. The child file is left in whatever partial state Step 3 reached at abort time; the command emits a "resume by re-running with the same slug (and `--force` if the partial fill removed `<placeholder>` substrings)" hint. The README's `last_updated:` is NOT bumped.
- `2` — pre-conditions failed: initiative folder missing (Step 1); `context-map.md` missing inside the folder (Step 1); file already filled without `--force` (Step 2); README not readable at Step 5 time. The child file is not modified.
- `3` — child walked successfully but the post-fill README lint exited non-zero, and the human declined to re-open for correction (or accepted but did not lint clean on re-run). The child file persists in its filled state on disk; the README's `last_updated:` is NOT bumped. Automation consumers MUST treat exit 3 as distinct from exit 0.

## Chaining hint

Last output line, formatted exactly:

```
NEXT: /end-to-end-flow <initiative-slug>
```

The chain is `/draft-initiative` → `/context-map` → `/end-to-end-flow` → `/sequence-initiative` → `/draft-spec` per the convention's §"Chaining hint" and Open Question 4. `/end-to-end-flow` (P4.5) is the next augmenting command in the chain.

If `/end-to-end-flow` is not yet shipped at the time `/context-map` runs (i.e., P4.5 has not landed), the NEXT line uses the canonical name plus `(planned — ROADMAP P4.5)` per the convention's kit-drift policy. As of this spec's drafting (2026-05-23), P4.4, P4.5, P4.6 are in parallel fan-out and all three are expected to ship in the same session; the `(planned — …)` suffix is the safety net for the case where P4.5 lands after P4.4.

This command does NOT emit a `REVIEW:` line. Per the convention's §"Capabilities-file interstitial", only `/sequence-initiative` emits the REVIEW line. `/context-map`'s NEXT is the bare one-line form.

## Boundaries

### Always do

- Cite the parent convention (`docs/specs/phase-4-command-convention/spec.md`) as `Constrained by:` in this spec's header block.
- Treat `<initiative-slug>` as the positional argument — NOT `<slug>`. The augmenting-command sub-class is named in the convention's argv contract by the literal `<initiative-slug>` token; the contract test (`test_inscope_commands_declare_argv`) distinguishes augmenting from creating by exactly this token.
- Skip parent-artifact resolution entirely. The parent IS the initiative folder named by the positional. No `--from` flag, no candidate listing, no auto-detection.
- Emit `NEXT: /end-to-end-flow <initiative-slug>` as the last output line on a successful run.
- Quote HANDOVERS-5 §"Required content" item 1's four fields verbatim in the per-section interactive prompts (Owner, Public contract, Commodity vs custom (Wardley), Evolution stage). These are the load-bearing surface and re-phrasing them risks drift against HANDOVERS.
- Restate the kit's "one question at a time, never batch" rule explicitly in the command body's Step 3 — the load-bearing interactivity guarantee.
- Resolve the repo root as the nearest ancestor containing `tools/lint-frontmatter.py` before invoking the linter; do not assume the working directory is the repo root.

### Ask first

- Adding any additional prompt to the per-section walk beyond the eight named in §"Per-section interactive prompts". The prompt set is the contract; growing it grows the command's interaction surface and warrants explicit sign-off.
- Bumping any field on the initiative README beyond `last_updated:` and `approvals_obtained:`. The command's side-effect surface on the README is contracted; growing it risks silent edits to load-bearing fields.
- Touching any other file inside the initiative folder. `flow.md`, `sequence.md`, `child-specs.md`, `capabilities.md` are owned by other commands (P4.5, P4.6, and indirect populators).
- Adding a `--from` flag (creating-command shape). This would contradict the convention's §"Argv contract" augmenting case and invalidate the contract test's distinction between creating and augmenting commands.

### Never do

- Create a new artifact at any path. The child file already exists in placeholder form; this command fills it in place.
- Skip the Wardley-lite commodity-vs-custom evolution check for any bounded context. The four HANDOVERS-5 fields are non-negotiable.
- Auto-pick the bounded-context owner — always ask the human, even when only one candidate is obvious from the initiative README's `crosses_teams:` list. The convention's §"Parent-artifact resolution" auto-pick failure mode (silent failure) applies analogously to the owner-assignment step here.
- Modify the initiative README beyond `last_updated:` (bumped on success) and `approvals_obtained:` (appended at Step 4). Touching any other README field would silently widen the command's contract.
- Touch `templates/initiative/context-map.md`. The template is the source-of-shape, frozen by F3.7; the command writes to the destination child file, not back to the template.
- Modify any other child of the initiative folder (`flow.md`, `sequence.md`, `child-specs.md`, `capabilities.md`). Each has its own command or its own populator.
- Treat this command as convention-exempt. The seven in-scope commands all conform to the convention; deviations are surfaced explicitly via this spec's adversarial review, not absorbed quietly.
- Pre-fill `id:` on anything. Augmenting commands have no new artifact.

## Verification mode

- **Goal-based check** for the command file's shape: `tools/lint-command.sh .claude/commands/context-map.md` exits 0; the four convention-required H2 sections are present (`## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`); the `argument-hint:` frontmatter is exactly `<initiative-slug> [--force]` (the augmenting form, no `--from`); the body cites `templates/initiative/context-map.md` (the source-of-shape) and `delivery/initiatives/` (the destination family); the chaining hint names `/end-to-end-flow <initiative-slug>`.
- **Audit-driven** for the convention's contract test: `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (the test auto-discovers `.claude/commands/context-map.md` once it lands and asserts the convention's argv form, H2 set, cited paths). When this command ships, the test tightens from skip-for-context-map to pass-for-context-map.
- **Manual gesture** for end-to-end behavior: run `/context-map <initiative-slug>` against a fixture initiative folder (created by `/draft-initiative` against a fixture vision) and confirm the walk emits the eight prompts in document order, one at a time; the README `last_updated:` is bumped on success; the NEXT line names `/end-to-end-flow <initiative-slug>` exactly. The fixture lives under `scripts/tests/fixtures/` or is created on-the-fly; details belong to plan.md.
- **Adversarial review** by the `adversarial-reviewer` subagent against this spec, against the parent convention, and against HANDOVERS-5. Max 3 review passes per work-loop default.

## Contract tests

Each test is one shell line or one pytest case.

- `T1` — `.claude/commands/context-map.md` exists: `test -f .claude/commands/context-map.md` exits 0.
- `T2` — `bash tools/lint-command.sh .claude/commands/context-map.md` exits 0.
- `T3` — The four convention-required H2 sections are present in the command body: `grep -c '^## When to run' .claude/commands/context-map.md` returns 1; same for `## Inputs`, `## Procedure`, `## What this command will not do`.
- `T4` — The `argument-hint:` frontmatter matches the augmenting form exactly: `grep -E '^argument-hint: <initiative-slug> \[--force\]$' .claude/commands/context-map.md` returns 1. Also asserts the absence of `--from` (a `--from`-containing argument-hint would fail this regex).
- `T5` — The body cites the source-of-shape template path: `grep -c 'templates/initiative/context-map\.md' .claude/commands/context-map.md` returns ≥ 1. (The contract test's `test_inscope_commands_cite_template_path` runs this assertion and additionally confirms the cited path exists in the repo.)
- `T6` — The body cites the destination family directory: `grep -c 'delivery/initiatives/' .claude/commands/context-map.md` returns ≥ 1. (The contract test's `test_inscope_commands_cite_destination_path` asserts the directory exists.)
- `T7` — The chaining hint names the next augmenting command in the chain: `grep -cE '^NEXT: /end-to-end-flow <initiative-slug>$' .claude/commands/context-map.md` returns 1. (The hint appears inside a fenced code block in the body, demonstrating the output the command emits.)
- `T8` — The body does NOT emit a `REVIEW:` line: `grep -c '^REVIEW:' .claude/commands/context-map.md` returns 0. (Only `/sequence-initiative` emits REVIEW per the convention.)
- `T9` — The body declares the augmenting Step 1 (verify folder existence + exit 2 on missing): `grep -c 'verify .* initiative folder' .claude/commands/context-map.md` returns ≥ 1 AND `grep -c 'exit code 2' .claude/commands/context-map.md` returns ≥ 2 (Step 1 and Step 2 both emit exit 2 paths; allow ≥ 2 to be tolerant of phrasing).
- `T10` — The body declares no `--from` flag: `grep -c -- '--from' .claude/commands/context-map.md` returns 0. The augmenting sub-class explicitly forbids the flag.
- `T11` — `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 — the convention's contract test passes with `.claude/commands/context-map.md` now landed (the test's auto-discovery picks it up).
- `T12` — `bash tools/pre-pr.sh` exits 0 (kit-wide health check; no regression).
- `T13` — The eight per-section interactive prompts named in §"Per-section interactive prompts" appear in the command body. Asserted by spec-anchor grep: `grep -c "What does 'bounded context' mean for this initiative" .claude/commands/context-map.md` returns ≥ 1; same anchor checks for the seven other prompts (one shell line each, against the prompt's distinctive substring). Each prompt's anchor is the first six-to-eight-word substring of the prompt's literal copy. If a prompt is paraphrased in the command body, the anchor check fails and the spec/body must be re-synced.
- `T14` — Adversarial-reviewer subagent returns 0 Blocking findings against this command's shipped body versus this spec, the parent convention, and HANDOVERS-5.

## Non-goals

- Modifying the initiative README beyond `last_updated:` (bumped on success) and `approvals_obtained:` (appended at Step 4).
- Touching any other child file inside the initiative folder. `flow.md`, `sequence.md`, `child-specs.md`, `capabilities.md` are owned by other commands or by other populators; this command does not modify them.
- Modifying `templates/initiative/context-map.md`. The source-of-shape is frozen by F3.7; deviations require a separate F3.7 amendment, not a P4.4 edit.
- Modifying `tools/lint-frontmatter.py` or `tools/lint-command.sh`. The linters' contract is upstream; this command runs them, it doesn't change them.
- Authoring `/end-to-end-flow` (P4.5) or `/sequence-initiative` (P4.6). Sibling specs in the augmenting trio; each runs in parallel under its own per-command spec.
- Adding a `--dry-run` flag. Deferred per the convention's Open Question 1.
- Adding a `--non-interactive` flag. The kit's interactivity contract is load-bearing; non-interactive use is out of scope.
- Auto-validating the bounded-context names against a future kit-wide bounded-context vocabulary doc. F3.7's `context-map.md` comment notes that vocabulary doc is planned (under P4.4); shipping the vocab doc itself is a separate concern from shipping the command that fills the child file.
- Walking `.claude/commands/context-map.md` from any default-mode linter. The command file is not a product artifact; per the convention, it's outside `lint-frontmatter.py`'s default-mode scope.

## Open questions

1. **Should `--force` re-walk also reset `approvals_obtained:` or append?** A `--force` re-walk re-asks the Step 4 human-owned-decisions confirmation. The current resolution is **append** — the new confirmation timestamps are appended to the existing `approvals_obtained:` list, preserving the audit trail of all confirmations across runs. The alternative (reset on `--force`) would silently lose audit history. Resolved here in favor of append; surfaced because the alternative is defensible if a future ROADMAP row formalizes "current approval vs historical approvals" distinction. If the alternative is chosen later, this command's Step 4 surfaces as a one-line spec edit.
2. **What if `<placeholder>` appears legitimately inside a context name?** The heuristic for "already filled" (Step 2) is "no `<placeholder>` substring remains". If a human types a context name like "Identity (placeholder until renaming sprint)", the heuristic would mis-classify the file as still-placeholder on the next `--force`-less re-run. Resolved here: documented as a known edge case; mitigation is the angle brackets — the template's placeholders use angle-bracket syntax exclusively (`<placeholder>`), and a legitimate human-typed context name should not include angle brackets. If a context name does need angle brackets, the human is asked to escape them or rename. Tracked as a candidate future hardening (regex-based check vs substring) under Phase-4 polish, not a P4.4 blocker.
3. **Should Step 5's lint additionally validate that all `<placeholder>` substrings in `context-map.md` are gone after the walk?** Currently no — the lint runs against the README, not the child. Resolved here: no additional check, because the walk in Step 3 explicitly confirms each placeholder fill before advancing, making a post-walk substring check redundant. If a future ROADMAP row formalizes "post-walk completeness check" as a kit-wide rule, this command's Step 5 gains the check at that point.

## Acceptance criteria

- [ ] `.claude/commands/context-map.md` exists and matches the §"Body-shape contract" body (asserted by T1, T2, T3).
- [ ] `argument-hint:` is exactly `<initiative-slug> [--force]` — augmenting form, no `--from` (asserted by T4, T10).
- [ ] Body cites `templates/initiative/context-map.md` and `delivery/initiatives/` (asserted by T5, T6).
- [ ] Chaining hint reads `NEXT: /end-to-end-flow <initiative-slug>` exactly; no `REVIEW:` line (asserted by T7, T8).
- [ ] Body declares the augmenting Step 1 (verify folder; exit 2 on missing) (asserted by T9).
- [ ] All eight per-section interactive prompts appear in the body, verbatim per their distinctive substring anchors (asserted by T13).
- [ ] `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (asserted by T11).
- [ ] `bash tools/pre-pr.sh` exits 0 (asserted by T12).
- [ ] Adversarial-reviewer subagent returns no Blocking findings (asserted by T14).
- [ ] No new ontology type added; no out-of-scope ROADMAP rows edited; no F3.x template modified; no `tools/` script modified; no other command modified.

## Cross-references

- **Consumed by:** ROADMAP P4.5 (`/end-to-end-flow`) — the chain successor; its NEXT line is emitted by this command. ROADMAP P4.10 (`/audit-spec-linkage`, planned) — walks `delivery/initiatives/<slug>/` for spec linkage; reads the bounded-context narrative this command fills. Future audits that read `context-map.md` for HANDOVERS-5 §"Required content" item 1 compliance.
- **Consumes:** `docs/specs/phase-4-command-convention/spec.md` (parent convention, including §"Argv contract" augmenting case and §"Parent-artifact resolution" augmenting case); `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" §"Required content" item 1 (four bounded-context fields); `templates/initiative/context-map.md` (source-of-shape, F3.7); `delivery/initiatives/<initiative-slug>/README.md` and `delivery/initiatives/<initiative-slug>/context-map.md` (read-write targets at runtime); `tools/lint-frontmatter.py` (default-mode linter on the README); `tools/lint-command.sh` (shape linter on the command file); `.claude/commands/_meta/command-skeleton.md` (the body skeleton this command copies from).
- **Frontmatter fields owned:** none directly. The command writes `last_updated:` on the initiative README (universal-schema field, owned by `docs/CONVENTIONS.md`) and appends to `approvals_obtained:` (also universal-schema). The child file `context-map.md` has no frontmatter per F3.7's OQ4.
- **Ontology object types touched:** Initiative (Domain D; the artifact whose folder hosts the child file this command fills). Capability (Domain E; referenced indirectly through the README's `capabilities:` list and the future `capabilities.md` walk, not modified here). The kit has no "Bounded Context" ontology type per F3.7's "Never do" rule — bounded contexts are a narrative-level concept inside the Initiative composite, not a standalone Domain row.
