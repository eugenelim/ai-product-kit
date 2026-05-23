# Spec: cmd-sequence-initiative

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command
- **Serves kit phase:** Delivery
- **Constrained by:** [`docs/specs/phase-4-command-convention/spec.md`](../phase-4-command-convention/spec.md) — parent convention. In particular, §"Capabilities-file interstitial" mandates that this command, **and only this command among the seven**, emit a `REVIEW:` line immediately *before* the `NEXT:` line in its Step 6 chaining hint. The augmenting sub-class rules in §"Parent-artifact resolution" (skipped — parent is the initiative folder named by the positional) and §"Argv contract" (positional is `<initiative-slug>`, optional `--force`, no `--from`) also bind. Sibling references: [`docs/HANDOVERS.md`](../../HANDOVERS.md) §"Handover 5: Initiative → Spec" (the `sequence.md` child file is a required HANDOVERS-5 deliverable — DAG of specs by dependency, first-shippable subset called out); [`templates/initiative/sequence.md`](../../../templates/initiative/sequence.md) (the source body this command fills in-place); [`templates/initiative/capabilities.md`](../../../templates/initiative/capabilities.md) (the file the REVIEW interstitial points the human at — context for why this command is the one that carries it: capabilities.md has no dedicated Phase-4 command and the human MUST review it before /draft-spec runs); [`docs/specs/template-initiative/spec.md`](../template-initiative/spec.md) (the F3.7 template spec that ships the `sequence.md` child this command fills); [`tools/lint-command.sh`](../../../tools/lint-command.sh) (existing per-command shape linter); [`tools/lint-frontmatter.py`](../../../tools/lint-frontmatter.py) default-mode (the linter the command invokes against the initiative `README.md` after Step 5, since `sequence.md` itself has no frontmatter); [`.claude/skills/work-loop/SKILL.md`](../../../.claude/skills/work-loop/SKILL.md) (the build pattern this command's authoring follows); [`.claude/CLAUDE.md`](../../../.claude/CLAUDE.md) "How we work together" (one clarifying question at a time, never batch — the interactivity contract this command implements mechanically); ROADMAP P4.6.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `.claude/commands/sequence-initiative.md`, the Phase-4 template-fill slash command that walks the human through filling `delivery/initiatives/<initiative-slug>/sequence.md` — the dependency-aware delivery DAG and first-shippable subset that HANDOVERS-5 requires. **This is the ONE command in the seven that emits a `REVIEW:` line in its chaining hint** (per parent convention §"Capabilities-file interstitial"): immediately before the `NEXT: /draft-spec <first-spec-slug>` line, the command prints `REVIEW: delivery/initiatives/<initiative-slug>/capabilities.md — verify the Capability list is filled and each row traces to a parent Problem before running /draft-spec.` The REVIEW line and the NEXT line ship as a pair; emitting NEXT without the preceding REVIEW (or vice versa) is a regression. This command is artifact-**augmenting** (positional is `<initiative-slug>`; the parent IS the initiative folder; no parent resolution, no `--from`).

## Objective

`/sequence-initiative` is the third of three augmenting commands inside the Initiative folder (after `/context-map` and `/end-to-end-flow`). It does not create a new artifact; it fills the placeholder child file `delivery/initiatives/<initiative-slug>/sequence.md` (shipped by F3.7) in-place, walking the human through the dependency DAG of child specs and the first-shippable subset. The end of `/sequence-initiative` is also the transition point in the Phase-4 chain from "fleshing out the initiative" to "drafting individual specs" — which is why the command additionally surfaces a `REVIEW:` interstitial pointing the human at the initiative's `capabilities.md` (the HANDOVERS-5 child that has no dedicated Phase-4 command and gets populated incidentally during `/draft-initiative`). Without a forced human pause on capabilities, `/draft-spec` would consume a possibly-empty or possibly-untraced Capability list, and the traceability chain `Requirement → Capability → Problem` would silently break at its first downstream consumer.

The DAG itself is small but the conversation that produces it is the load-bearing piece: each edge is a human-owned sequencing decision (per the initiative README's `human_owned_decisions:` list, which names "Delivery sequencing" verbatim). The command surfaces those decisions; it does not auto-pick the first-shippable subset.

## Why now

ROADMAP P4.6 sits in the Phase-4 block, immediately after P4.4 (`/context-map`) and P4.5 (`/end-to-end-flow`) and immediately before P4.8 (`/draft-spec`). The F3.7 initiative folder template — including `sequence.md` and `capabilities.md` — shipped on 2026-05-22; the parent command convention shipped 2026-05-23 (this session); the six sibling per-command specs (cmd-draft-vision, cmd-draft-initiative, cmd-context-map, cmd-end-to-end-flow, cmd-draft-spec, cmd-handoff-packet) are being authored in parallel with this one. `/draft-spec` ships in the same fan-out wave: its NEXT-line consumer (the spec slug `/sequence-initiative` hands off to) needs `/draft-spec` shipped to be a clean handoff rather than a `(planned — ROADMAP P4.8)` annotation. Shipping `/sequence-initiative` later than the rest of the fan-out would leave the REVIEW-interstitial contract surface — uniquely held by this command per the parent convention — unimplemented and silently bypassed by any human running `/context-map → /end-to-end-flow → /draft-spec` themselves.

## Inputs and outputs

**Inputs.**

1. **Positional argument:** `<initiative-slug>` — kebab-case identifier matching `^[a-z0-9-]+$`, ≤ 80 chars. Names the existing initiative folder under `delivery/initiatives/`. No `--from` flag (augmenting commands skip parent resolution; the parent IS this initiative).
2. **Template body source:** `templates/initiative/sequence.md` — the F3.7 child file the command's walk shapes against. The target file at `delivery/initiatives/<initiative-slug>/sequence.md` already exists (created by `/draft-initiative` when it instantiated the folder); the command walks its H2 placeholders.
3. **Target file:** `delivery/initiatives/<initiative-slug>/sequence.md` — the in-place augmented child. No new artifact; no new `id:`. After successful walk, the command updates `last_updated:` on `delivery/initiatives/<initiative-slug>/README.md` to today's date.
4. **Sibling-file pre-conditions:** `delivery/initiatives/<initiative-slug>/child-specs.md` (the manifest of spec slugs the DAG references), `delivery/initiatives/<initiative-slug>/context-map.md`, `delivery/initiatives/<initiative-slug>/flow.md`. The DAG's nodes are the spec slugs from `child-specs.md`; the bounded-context groupings draw from `context-map.md`; the end-to-end flow informs leaf-vs-root reasoning. If `context-map.md` or `flow.md` still contains `<placeholder>` substrings (heuristic: any angle-bracket placeholder remaining), exit code 2 with the remediation message to run `/context-map` and/or `/end-to-end-flow` first.
5. **Linter (default mode):** `tools/lint-frontmatter.py` — run against `delivery/initiatives/<initiative-slug>/README.md` (the only frontmatter-bearing file in the initiative folder; `sequence.md` itself has no frontmatter per F3.7).

**Outputs.**

1. `delivery/initiatives/<initiative-slug>/sequence.md` — filled in-place. H2 `## Delivery sequence` contains a real Mermaid `graph LR` block with real spec slugs as node IDs, real dependency edges, and a `**First shippable subset:** <list>` callout immediately below the diagram.
2. `delivery/initiatives/<initiative-slug>/README.md` — `last_updated:` field bumped to today's date (ISO-8601).
3. **Two-line chaining emit** (stdout, last two lines, REVIEW immediately before NEXT):

   ```
   REVIEW: delivery/initiatives/<initiative-slug>/capabilities.md — verify the Capability list is filled and each row traces to a parent Problem before running /draft-spec.
   NEXT: /draft-spec <first-spec-slug>
   ```

   Where `<first-spec-slug>` is the spec slug the human names at the end of the walk as the first leaf of the DAG (typically the root of the first-shippable subset). The command **asks** for this slug explicitly as the final question of the walk; it does not auto-pick. If the human declines to name one, the NEXT line emits `NEXT: /draft-spec <slug>` with the literal placeholder `<slug>` (and the command surfaces a one-line "name the spec slug explicitly when you run /draft-spec" note above the two-line emit).

4. **Exit code** per the four-code table below.

A reader of this section should be able to write the command's interface signature without reading anything else.

## Body-shape contract

The shipped `.claude/commands/sequence-initiative.md` follows the parent convention's skeleton verbatim. The frontmatter is exactly two keys:

```yaml
---
description: Walk the human through filling delivery/initiatives/<initiative-slug>/sequence.md — the dependency DAG of child specs and first-shippable subset — and emit a REVIEW reminder pointing at capabilities.md before chaining to /draft-spec.
argument-hint: <initiative-slug> [--force]
---
```

Body H1: `# /sequence-initiative`. H2 sections in this order (per parent convention §"Body structure"):

1. `## When to run`
2. `## Inputs`
3. `## Procedure` — six numbered Step-N sub-sections per the parent convention's required steps. **Step 6 (the chaining hint) is the load-bearing deviation point**: the command emits a `REVIEW:` line *before* the `NEXT:` line. The skeleton's Step 6 already documents this (see `.claude/commands/_meta/command-skeleton.md` line 189: "For `/sequence-initiative` only, also emit a `REVIEW:` line immediately before the NEXT line"). The shipped command's Step 6 quotes the exact two-line emit verbatim, and the contract test grep-asserts both lines appear in document order REVIEW-before-NEXT.
4. `## What this command will not do` — bulleted non-behaviors, including the three augmenting-class boilerplate non-behaviors from the parent convention plus the three command-specific ones (see §"Boundaries → Never do" below).

## Per-section interactive prompts

`templates/initiative/sequence.md` has exactly one H2 — `## Delivery sequence` — containing one Mermaid `graph LR` block and one `**First shippable subset:**` callout (sourced from HANDOVERS-5 §"Required content" item 4 per `docs/specs/template-initiative/spec.md`). The command walks this single H2 with the following prompts, asked sequentially, one at a time, never batched. The order is fixed; the command does not advance until the current prompt is answered.

### `## Delivery sequence`

Prompts the command emits, in exact phrasing:

1. *"Open `child-specs.md` for this initiative. List the spec slugs that exist in the manifest. I will use these as the node IDs of the DAG. Confirm the slug list, or amend it now."*
2. *"For each spec slug, name its upstream dependencies — the specs whose output it consumes. A spec with no upstream dependencies is a root; a spec with no downstream consumers within this initiative is a leaf. I will ask you slug-by-slug. We begin with `<first-slug-from-child-specs>`. What are its upstream dependencies (zero or more, comma-separated spec slugs from this initiative's `child-specs.md`)?"* — repeated per slug, one slug at a time, in the order they appear in `child-specs.md`.
3. *"Which specs can ship in parallel? Group any specs that share no dependency edges and depend on the same upstream parents. Parallelizability is a delivery-team decision; I am asking, not deriving."*
4. *"Identify the first-shippable subset: the smallest set of specs that, shipped together, deliver an end-to-end customer outcome — even if narrower than the full Initiative. This is a human-owned sequencing decision per the initiative README's `human_owned_decisions:` list. Name the spec slugs in the first-shippable subset."*
5. *"For each spec in the first-shippable subset, confirm whether it is a leaf (the customer-facing terminal output) or a root (an upstream prerequisite). The leaf-vs-root call drives which spec `/draft-spec` should be authored first — usually the leaf, because the leaf's acceptance criteria constrain the roots."*
6. *"Render the DAG in Mermaid `graph LR` syntax inside the fenced block. Use bare alphanumeric node IDs (the spec slugs themselves, kebab-case stripped to alphanumeric-and-dashes — Mermaid tolerates dashes in node IDs). I will substitute the rendered block into `sequence.md` and replace the placeholder `SpecA[Spec A] --> SpecB[Spec B]` example block."*
7. *"Confirm the rendered DAG. Adjust nodes or edges if needed before I write the file."*
8. *"Update the `**First shippable subset:**` callout immediately below the diagram with the comma-separated spec slug list you named in step 4."*
9. *"Finally — and this is the question whose answer becomes the NEXT-line argument when this command exits — which spec slug should be drafted first via `/draft-spec`? Typically a leaf of the first-shippable subset. If you decline to name one now, the NEXT line will surface a literal placeholder and you will name it when you run `/draft-spec`."*

After the walk: Step 4 (human-owned-decisions) re-surfaces the initiative README's `human_owned_decisions:` list (specifically "Delivery sequencing", verbatim from HANDOVERS-5) and asks for explicit confirmation that the sequencing decisions just captured are owned. Step 5 runs the default-mode linter against `README.md` (not against `sequence.md` itself; `sequence.md` carries no frontmatter per F3.7). Step 6 emits the two-line REVIEW+NEXT chaining hint.

## Pre-fill rules

`/sequence-initiative` is artifact-augmenting; it does NOT pre-fill any `id:`, `slug:`, `created:`, or `parent_*:` fields (no new artifact). The only mutation outside `sequence.md` is bumping `last_updated:` on the initiative `README.md` to today's date (ISO-8601, system-clock-resolved) after Step 5 succeeds. `object_type:` is not re-asserted — `sequence.md` has no frontmatter and the initiative `README.md`'s `object_type: Initiative` is untouched.

The mechanical bump to `README.md`'s `last_updated:` is the same write the sibling augmenting commands (`/context-map`, `/end-to-end-flow`) perform. Multiple back-to-back augmenting commands on the same initiative race only on `last_updated:`; "last writer wins" is acceptable because the field is a strictly monotonic date, not a content field.

## `--force` semantics

If `sequence.md` is already filled (heuristic: contains no `<placeholder>`, `SpecA`, `SpecB`, `SpecC`, or `SpecD` substrings remaining — i.e., the F3.7 template's example placeholders have been overwritten), exit code 2 with the remediation message: `"sequence.md appears already filled. Re-run with --force to overwrite, or edit the file directly if the change is small."` If `--force` is given, proceed with the walk and overwrite the existing content. The pre-existing `last_updated:` on the initiative `README.md` is bumped to today regardless of `--force`.

## Linter integration

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`. Run `python3 <repo-root>/tools/lint-frontmatter.py <repo-root>/delivery/initiatives/<initiative-slug>/README.md` (default mode, against the README only; `sequence.md` has no frontmatter so is not linted). Report the result. If linter exits non-zero, offer to re-open the relevant README sections for correction; if the human declines or re-run still fails, exit code 3.

## Exit codes

- `0` — `sequence.md` filled, README `last_updated:` bumped, linter passed, REVIEW + NEXT two-line hint emitted.
- `1` — human aborted the walk before completion. `sequence.md` left in its partial state; resume by re-running with the same slug (and `--force` if the placeholder substrings are gone).
- `2` — pre-conditions failed. Sub-cases: (a) `delivery/initiatives/<initiative-slug>/` does not exist (remediation: run `/draft-initiative <initiative-slug>` first); (b) `sequence.md` is already filled and `--force` is not set; (c) `context-map.md` or `flow.md` still contains `<placeholder>` substrings (remediation: run `/context-map <initiative-slug>` and/or `/end-to-end-flow <initiative-slug>` first); (d) slug malformed (does not match `^[a-z0-9-]+$` or > 80 chars); (e) `child-specs.md` empty (no spec slugs to sequence — remediation: populate `child-specs.md` manually or via `/draft-spec`).
- `3` — `sequence.md` written and `README.md`'s `last_updated:` bumped, but default-mode linter exited non-zero on `README.md`; the command offered to re-open relevant README sections for correction, and the human declined (or re-ran but lint still fails). Both files persist in their known-imperfect state. Automation consumers MUST treat exit 3 as distinct from exit 0.

## Chaining hint (the load-bearing two-line emit)

`/sequence-initiative` is the ONLY command in the seven Phase-4 template-fill commands that emits a `REVIEW:` line. Per the parent convention §"Capabilities-file interstitial", the last two lines of the command's stdout, in this exact order, are:

```
REVIEW: delivery/initiatives/<initiative-slug>/capabilities.md — verify the Capability list is filled and each row traces to a parent Problem before running /draft-spec.
NEXT: /draft-spec <first-spec-slug>
```

The REVIEW line is on its own line and **precedes** the NEXT line. The two are written as a pair: emitting NEXT without REVIEW (or REVIEW without NEXT) is a regression and is grep-asserted in the contract tests. `<first-spec-slug>` is the spec slug the human named in prompt 9 of the walk (the first leaf of the DAG, typically the root of the first-shippable subset); if the human declined to name one, the NEXT line emits the literal placeholder `<slug>`. If `/draft-spec` is not yet shipped at the moment this command runs (defensive guard against an out-of-order fan-out roll-out), append `(planned — ROADMAP P4.8)` to the NEXT line per the kit-drift policy — but in practice the seven Phase-4 commands ship as one wave, so this branch is expected to be un-exercised in the first roll-out; the guard must still be implemented.

The REVIEW line is the kit's mitigation for the gap that `capabilities.md` has no dedicated Phase-4 command. Capabilities are populated incidentally during `/draft-initiative`'s Step-3 walk; without a forced human pause here, `/draft-spec` would consume a possibly-empty or possibly-untraced Capability list, and the traceability chain `Requirement → Capability → Problem` (per `/audit-traceability` Rule 1 and Rule 2) would silently break at its first downstream consumer.

## Boundaries

### Always do

- Verify `delivery/initiatives/<initiative-slug>/` exists before doing anything else. If not, exit code 2 with the remediation suggestion to run `/draft-initiative <initiative-slug>` first.
- Verify `delivery/initiatives/<initiative-slug>/README.md` exists within the folder (Step 4 reads it and Step 5 mutates it; fail-fast is cleaner than mid-walk failure). If not, exit code 2 with the remediation to restore the README from `templates/initiative/README.md` or re-run `/draft-initiative`.
- Verify `context-map.md` and `flow.md` are filled — use the same heuristic `/end-to-end-flow` itself uses for `--force` detection (no `<placeholder>` substrings AND no template-default actor identifiers like `ActorA`/`ActorB`/`TriggerEvent`/`ResponseOrSuccessOutcome` for `flow.md`). Sequencing against placeholder bounded contexts and a placeholder flow is incoherent. The DAG draws on both; sequencing a DAG against placeholder bounded contexts and a placeholder flow is incoherent. Exit 2 with remediation if either is still in placeholder form.
- Verify `child-specs.md` lists at least one spec slug. The DAG has no nodes if the manifest is empty.
- Walk the H2 prompts one at a time, sequentially, never batched. Confirm the rendered Mermaid block and the first-shippable-subset callout before writing.
- Emit the REVIEW line immediately *before* the NEXT line as the final two lines of stdout. Ship them as a pair.
- Update `last_updated:` on the initiative `README.md` to today's date after Step 5 succeeds.

### Ask first

- Adding any prompt beyond the nine listed in §"Per-section interactive prompts". The list is sized to a single H2; growing it grows the conversation surface and warrants explicit sign-off (likely via this spec's `Open Questions` rather than a quiet edit to the command body).
- Changing the order or phrasing of the REVIEW + NEXT two-line emit. The parent convention pins both the content and the precedence; changing either is a parent-convention edit, not a per-command edit.
- Auto-rendering the Mermaid block from a structured representation the command derived itself. Today the command asks the human to render the Mermaid block; the human's hand keeps the DAG coherent. Auto-rendering would be convenience tooling but would risk silently dropping edges.

### Never do

- Not emit a NEXT line without the preceding REVIEW line — they ship as a pair. (The whole point of this command's distinguishing feature is this pair; breaking it silently bypasses the capabilities-file review.)
- Not auto-pick the first-shippable subset — the human owns sequencing decisions per the initiative README's `human_owned_decisions:` list, which names "Delivery sequencing" verbatim. The command surfaces the question; the human answers it.
- Not build the DAG without consulting `context-map.md` and `flow.md` — exit code 2 with remediation if either is still in placeholder form. The DAG's nodes group by bounded context (from `context-map.md`) and its leaves correspond to end-to-end-flow terminals (from `flow.md`); sequencing without both is incoherent.
- Not overwrite an already-filled `sequence.md` without `--force`. Exit 2 with the remediation message.
- Not skip the `human_owned_decisions:` confirmation step (Step 4). The "Delivery sequencing" entry in the initiative README is the relevant one.
- Not fabricate spec slugs. If `child-specs.md` lists zero specs, exit code 2 with the remediation message; do not invent slugs to populate a DAG.
- Not batch placeholder questions — one at a time.
- Not assume the working directory is the repo root when invoking the linter — resolve repo root by walking up from the cwd until `tools/lint-frontmatter.py` is found.
- Not pre-fill `id:` or any `parent_*:` field — this is an augmenting command; no new artifact.
- Not lint `sequence.md` itself — it carries no frontmatter per F3.7; the default-mode linter is run against `README.md`.
- Not modify any sibling child file in the initiative folder (`context-map.md`, `flow.md`, `child-specs.md`, `capabilities.md`, the README aside from `last_updated:`). The command's write scope is `sequence.md` plus the one-line `last_updated:` field on `README.md`.

## Verification mode

- **Goal-based check** for the command body's shape (lint-command.sh passes; required H2 sections present; `argument-hint:` carries `<initiative-slug>`; the REVIEW and NEXT lines both appear in the body in REVIEW-before-NEXT order — Task 1 hand-rolled gate in `plan.md`).
- **Goal-based check** for the parent convention's contract tests: `scripts/tests/test_phase4_command_shape.py` passes with `sequence-initiative.md` now present (the test auto-tightens from skip to assert when the file lands; assertions: lint-command.sh exit 0; the four required H2s present; `argument-hint:` follows the augmenting-class form; the cited template path `templates/initiative/sequence.md` exists; the cited destination directory `delivery/initiatives/` exists).
- **Manual gesture** for the interactive walk (recorded against a known fixture: a stub initiative folder with placeholder `context-map.md` and `flow.md` to verify the exit-2 gating, plus a populated fixture to verify the happy path emits the REVIEW + NEXT pair in the right order).
- **Audit-driven** for kit-wide health: `tools/pre-pr.sh` exits 0.

## Contract tests

Each test is one shell line, one pytest case, or one manual gesture recorded against a fixture.

- `T1` — `.claude/commands/sequence-initiative.md` exists and `bash tools/lint-command.sh .claude/commands/sequence-initiative.md` exits 0.
- `T2` — `grep -c '^## When to run' .claude/commands/sequence-initiative.md` returns 1, same for `^## Inputs`, `^## Procedure`, `^## What this command will not do` (the four required H2s per the parent convention).
- `T3` — `awk '/^## /{print NR" "$0}' .claude/commands/sequence-initiative.md` shows the four H2s in this order: When to run, Inputs, Procedure, What this command will not do.
- `T4` — `grep -c '^argument-hint: <initiative-slug>' .claude/commands/sequence-initiative.md` returns 1 (positional is `<initiative-slug>`, NOT `<slug>`).
- `T5` — `grep -c 'templates/initiative/sequence.md' .claude/commands/sequence-initiative.md` returns >= 1 AND `test -f templates/initiative/sequence.md` exits 0 (template path cited and the path exists in the repo).
- `T6` — `grep -c 'delivery/initiatives/' .claude/commands/sequence-initiative.md` returns >= 1 AND `test -d delivery/initiatives` exits 0 (destination directory cited and exists).
- **`T7` (the load-bearing test) — `grep -nE '^REVIEW: ' .claude/commands/sequence-initiative.md` returns at least one match AND `grep -nE '^NEXT: ' .claude/commands/sequence-initiative.md` returns at least one match AND the line number of the REVIEW match is less than the line number of the NEXT match** (REVIEW precedes NEXT in the document; the pair is intact). The test is grep-asserted as a hand-rolled gate in `plan.md` Task 1, NOT parametrized in `test_phase4_command_shape.py` (the parametrized contract test does not cover the REVIEW-before-NEXT ordering because that contract is unique to this one command). The hand-rolled gate is what protects against a regression where someone edits the command body and silently drops the REVIEW line.
- `T8` — `grep -c 'capabilities.md' .claude/commands/sequence-initiative.md` returns >= 1 (the REVIEW line names the file the human must review).
- `T9` — `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (the parent convention's contract test now passes with `sequence-initiative.md` present; the test auto-asserts the in-scope-command checks against this file).
- `T10` — `bash tools/pre-pr.sh` exits 0 (kit-wide health after the command lands).
- `T11` — `grep -c '## What this command will not do' .claude/commands/sequence-initiative.md` returns 1 AND `grep -c 'Not emit a NEXT line without the preceding REVIEW line' .claude/commands/sequence-initiative.md` returns >= 1 (the command-specific Never-do about the REVIEW+NEXT pair is documented in the command body, not just the spec).
- `T12` — Manual gesture: run the command against a fixture initiative folder where `context-map.md` is still in placeholder form. Exit code 2; remediation message names `/context-map`. Recorded under `docs/specs/cmd-sequence-initiative/notes/manual-gesture-record.md` post-execute.
- `T13` — Manual gesture: run the command against a fixture initiative folder where everything is filled. Exit code 0; the last two stdout lines are REVIEW (with `capabilities.md` cited) immediately followed by NEXT (with `/draft-spec <first-spec-slug>`).

## Non-goals

- Authoring or modifying `templates/initiative/sequence.md`. F3.7 ships it; this command consumes it.
- Authoring or modifying `templates/initiative/capabilities.md`. The REVIEW line points at the *instantiated* `delivery/initiatives/<initiative-slug>/capabilities.md`, which `/draft-initiative` populates. This command does not write to capabilities.md.
- Authoring `/draft-spec` (P4.8) — a separate per-command spec in the same fan-out wave.
- Auto-rendering the Mermaid DAG from structured input. The human renders the block; the command substitutes it.
- Auto-picking the first-shippable subset. Human-owned decision, per HANDOVERS-5 and the initiative README's `human_owned_decisions:` list.
- Walking any H2 of `templates/initiative/sequence.md` other than the single `## Delivery sequence` H2 the F3.7 template ships. If F3.7 grows additional H2s, this spec needs an amendment.
- Linting `sequence.md` itself — it carries no frontmatter per F3.7; the default-mode linter is invoked against the initiative `README.md` only.
- Modifying `tools/lint-command.sh`, `tools/lint-frontmatter.py`, or `scripts/tests/test_phase4_command_shape.py`. The parent convention's contract surface is committed.
- Backfilling a REVIEW line on the other six Phase-4 commands. The parent convention §"Capabilities-file interstitial" explicitly states "Other commands in the chain do not emit a REVIEW line"; this command is the unique carrier.

## Open questions

1. **What if `child-specs.md` lists exactly one spec?** The DAG has one node and no edges; the "first-shippable subset" is trivially that one spec; the leaf-vs-root distinction collapses. Resolved here: the walk still runs (prompts 1, 4, 6, 9 are answerable for a single-spec initiative; prompts 2, 3, 5, 7, 8 short-circuit with a single iteration each). The Mermaid block is a single node with no edges. The NEXT line names that single slug.
2. **What if the human's named first-spec-slug in prompt 9 is not in `child-specs.md`?** Resolved here: the command warns ("`<slug>` not found in `child-specs.md` — confirm or amend"), asks once more, and if the human insists, emits the NEXT line with the slug as given (no hard block — perhaps the human is adding a spec slug that hasn't been written to the manifest yet). The warning is a one-time soft gate, not a hard exit.
3. **Should the REVIEW line cite a specific traceability rule from `/audit-traceability`?** The REVIEW line says "verify the Capability list is filled and each row traces to a parent Problem"; `/audit-traceability` Rule 2 ("Every Capability must trace to a Problem, Business Objective, or Policy Rule") is broader. Resolved here: keep the REVIEW line's narrower phrasing (Problem-only) because Initiative-Capability traceability terminates at Problem in the common case; mentioning Business Objective or Policy Rule would dilute the message. If a future audit pass surfaces Capabilities that legitimately trace only to Business Objectives, amend the REVIEW line in a follow-up.
4. **Should the command auto-run `/audit-traceability <initiative-slug>` after the REVIEW line?** Resolved here: no. Running an audit silently after a REVIEW that asks the human to *review* — i.e., to make a judgment — would be a substitution of mechanical check for human judgment, exactly the failure mode the kit's Human-vs-AI ownership principle is built against. The REVIEW line is intentionally a human-facing prompt, not a machine gate.
5. **What if `sequence.md` has been hand-edited and the placeholder substrings are gone but the file is incoherent?** Resolved here: the `--force` semantics absorbs this — re-running with `--force` overwrites whatever was there. The heuristic for "already filled" (no `<placeholder>`, `SpecA`, `SpecB`, `SpecC`, `SpecD`) is a coarse filter, not a coherence check.
6. **Should the command emit a REVIEW line on `child-specs.md` too?** `child-specs.md` is populated incidentally during `/draft-initiative` similarly to `capabilities.md`. Resolved here: no — the parent convention pins the REVIEW interstitial to capabilities.md alone, because the load-bearing downstream consumer is `/draft-spec` and its traceability dependency is `Requirement → Capability → Problem`, not `Spec → child-specs-manifest`. If the kit later surfaces a `child-specs.md` traceability gap, a separate REVIEW line is a parent-convention edit.

## Acceptance criteria

- [ ] `.claude/commands/sequence-initiative.md` exists, passes `bash tools/lint-command.sh`, and carries the two-key frontmatter (`description:`, `argument-hint: <initiative-slug> [--force]`) (asserted by T1, T4).
- [ ] The four required H2 sections are present in order (asserted by T2, T3).
- [ ] The body cites `templates/initiative/sequence.md` AND that template exists (asserted by T5).
- [ ] The body cites `delivery/initiatives/` AND that directory exists (asserted by T6).
- [ ] **The body contains a `REVIEW:` line AND a `NEXT:` line AND the REVIEW line precedes the NEXT line in document order (asserted by T7 — the load-bearing test).**
- [ ] The body mentions `capabilities.md` at least once (the REVIEW line's target) (asserted by T8).
- [ ] `scripts/tests/test_phase4_command_shape.py` passes with `sequence-initiative.md` present (asserted by T9).
- [ ] `bash tools/pre-pr.sh` exits 0 (asserted by T10).
- [ ] The command body's `## What this command will not do` section documents the "Not emit a NEXT line without the preceding REVIEW line" non-behavior (asserted by T11).
- [ ] Manual-gesture fixtures pass: (a) exit 2 when sibling children are still in placeholder form (T12); (b) exit 0 with REVIEW immediately before NEXT in stdout on the happy path (T13).

## Cross-references

- **Consumed by:** The Phase-4 chain — `/end-to-end-flow`'s NEXT line cites `/sequence-initiative`; `/sequence-initiative`'s NEXT line cites `/draft-spec`. The human invokes this command after `/end-to-end-flow` and before `/draft-spec`.
- **Consumes:** `docs/specs/phase-4-command-convention/spec.md` (parent convention; load-bearing for §"Capabilities-file interstitial"); `docs/specs/template-initiative/spec.md` (the F3.7 template spec); `templates/initiative/sequence.md` (template body source); `templates/initiative/capabilities.md` (the file the REVIEW interstitial points at); `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec"; `tools/lint-command.sh`; `tools/lint-frontmatter.py`; `scripts/tests/test_phase4_command_shape.py`; `.claude/commands/_meta/command-skeleton.md`; `.claude/skills/work-loop/SKILL.md`; `.claude/CLAUDE.md` "How we work together".
- **Frontmatter fields owned:** none directly. The command writes to `delivery/initiatives/<initiative-slug>/sequence.md` (no frontmatter per F3.7) and bumps `last_updated:` on the initiative `README.md` (a universal-schema field, not "owned" by this command).
- **Ontology object types touched:** Initiative (Domain D — the parent artifact named by the positional). The DAG's nodes are PM Spec instances (Domain E composite per F3.8). The REVIEW line points at Capability (Domain E). No new ontology types introduced.
