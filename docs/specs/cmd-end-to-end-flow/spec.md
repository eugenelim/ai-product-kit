# Spec: cmd-end-to-end-flow

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command
- **Serves kit phase:** Delivery
- **Constrained by:** [`docs/specs/phase-4-command-convention/spec.md`](../phase-4-command-convention/spec.md) (parent convention — argv contract, body structure, parent-resolution / pre-fill / linter integration / exit codes / chaining-hint rules; this command is an artifact-AUGMENTING command per that convention, so parent-artifact resolution is SKIPPED and `--from` is NOT in argv; **deviates from the convention's `Boundaries → Always do` 120-body-line skeleton-parity guideline**: this command's body cap is ≤ 200 lines because the eight Mermaid-specific prompt blocks plus the four exit-code blocks plus the per-command Never-do list will not compress below ~170 lines without sacrificing prompt-copy clarity. Surfaced here per the convention's `Boundaries → Never do` rule that documented deviations are acceptable, undocumented ones are not.); [`docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md`](../phase-4-command-convention/notes/per-command-spec-checklist.md) (five-row authoring checklist this spec satisfies); [`docs/HANDOVERS.md`](../../HANDOVERS.md) §"Handover 5: Initiative → Spec" §"Required content" item 2 (`flow.md` — Mermaid sequence diagram of end-to-end customer flow across bounded contexts); [`templates/initiative/flow.md`](../../../templates/initiative/flow.md) (the child file body this command walks in-place); [`docs/specs/template-initiative/spec.md`](../template-initiative/spec.md) (F3.7 — the Initiative folder template; pins the `flow.md` child filename and the per-child no-frontmatter rule); [`tools/lint-command.sh`](../../../tools/lint-command.sh) (shape linter the command file itself must pass); [`tools/lint-frontmatter.py`](../../../tools/lint-frontmatter.py) default mode (post-fill linter run against the initiative `README.md` after its `last_updated:` is bumped); [`.claude/skills/work-loop/SKILL.md`](../../../.claude/skills/work-loop/SKILL.md) (the build pattern this spec's plan follows); [`.claude/CLAUDE.md`](../../../.claude/CLAUDE.md) "How we work together" (one-question-at-a-time, no batching — the interactivity contract this command implements).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `.claude/commands/end-to-end-flow.md` — the artifact-AUGMENTING Phase-4 slash command that fills `delivery/initiatives/<initiative-slug>/flow.md` in-place by walking the kit user one prompt at a time through the Mermaid `sequenceDiagram` body and its caption prose. Implements ROADMAP P4.5. Sub-class: AUGMENTING (per parent convention §"Argv contract"); positional is `<initiative-slug>`; NO parent-artifact resolution; NO `--from` flag; target file pre-exists as a placeholder inside the F3.7-instantiated initiative folder; pre-condition `context-map.md` must be filled (the swimlanes ARE the context-map's bounded contexts — see §"Open questions" Q1 resolution).

## Objective

`/end-to-end-flow <initiative-slug>` is the second of three artifact-augmenting Phase-4 commands that turn the placeholder children of an F3.7-instantiated initiative folder into HANDOVERS-5-compliant content. Today, after `/draft-initiative` (P4.3) scaffolds `delivery/initiatives/<slug>/`, the kit user inherits a `flow.md` child file whose body is a Mermaid `sequenceDiagram` template with placeholder participants (`ActorA`, `ActorB`) and a placeholder caption — and no guided way to fill it. They would have to read HANDOVERS-5 §"Required content" item 2 ("Mermaid sequence diagram of end-to-end customer flow across contexts"), read `context-map.md` to recover the bounded contexts, decide which actors and swimlanes participate in the happy path, design the sequence, decide which error / async branches belong in scope, and write Mermaid-safe identifiers — all without the kit's "one question at a time" guardrail. This command collapses that into a guided interactive walk that emits a single filled `flow.md` whose Mermaid block renders cleanly and whose caption names the trigger, actors, and success outcome. The command does NOT create a new artifact; it fills an existing placeholder child within an existing initiative folder. The kit-user experience: `/end-to-end-flow <initiative-slug>` → guided fill → lint-passed `flow.md` → `NEXT: /sequence-initiative <initiative-slug>` chain hint.

The closest prior context in the repo is the parent convention's skeleton (`.claude/commands/_meta/command-skeleton.md`) which this command copies, and the sibling P4.4 (`/context-map`) which establishes the bounded-context names this command's swimlanes must match.

## Why now

ROADMAP P4.5 sits in the F4 block — the seven Phase-4 template-fill commands the parent convention (`phase-4-command-convention`, shipped 2026-05-23) made parallelizable. P4.5's `Depends on:` line names F3.7 (`templates/initiative/`) and the parent convention; both shipped. F4.4 (`/context-map`, P4.4) is the immediate upstream chain link: its NEXT hint points at `/end-to-end-flow`. Until P4.5 ships, the chain `/draft-initiative` → `/context-map` → `/end-to-end-flow` → `/sequence-initiative` → `/draft-spec` → `/handoff-packet` has a gap; the kit user must hand-fill `flow.md` after `/context-map` completes. The cost of NOT shipping P4.5 is silent: kit users would either skip the Mermaid diagram entirely (HANDOVERS-5 §"Required content" item 2 unsatisfied — `/audit-completeness` will flag) or write malformed Mermaid (angle-bracket placeholders inside the fenced block, breaking GitHub's renderer — F3.7's spec OQ6 calls this out explicitly). Shipping P4.5 closes the chain gap and codifies the Mermaid-safe-identifier discipline as an interactive guardrail rather than after-the-fact remediation.

## Inputs and outputs

**Inputs.**

- The positional argument — `<initiative-slug>`. Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. Names the **existing** initiative folder at `delivery/initiatives/<initiative-slug>/`; the command does NOT create the folder.
- `templates/initiative/flow.md` — the F3.7-shipped child file template. The command does NOT copy it (the folder template was copied into `delivery/initiatives/<initiative-slug>/` by `/draft-initiative`); the command reads the template as a *reference* for the expected H2 structure when walking the kit user through the existing in-place placeholder file.
- `delivery/initiatives/<initiative-slug>/flow.md` — the in-place placeholder child file the command fills. Pre-exists in `<placeholder>`-bearing form per F3.7.
- `delivery/initiatives/<initiative-slug>/context-map.md` — the in-place child file containing the bounded-context list whose names this command's Mermaid swimlanes (`participant` declarations) must match. **Hard pre-condition:** must be already filled (no `<placeholder>` substrings). If still in placeholder form, exit 2 with remediation to run `/context-map` first. See §"Open questions" Q1.
- `delivery/initiatives/<initiative-slug>/README.md` — read for the initiative's `parent_vision:` and `human_owned_decisions:` lists (Step 4 surfaces the decisions for confirmation). Mutated in Step 5: `last_updated:` bumped to today's ISO-8601 date.
- `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" §"Required content" item 2 — source-of-truth for the flow.md required content (Mermaid sequence diagram + cross-context flow + happy path + actors + success outcome).
- `tools/lint-frontmatter.py` (default mode) — run against `delivery/initiatives/<initiative-slug>/README.md` after the `last_updated:` bump (Step 5). The README is what carries frontmatter; `flow.md` itself carries no frontmatter per F3.7's OQ4 resolution, so the linter is run against the README that was mutated by this command, not against the flow file itself.

**Outputs.**

1. `.claude/commands/end-to-end-flow.md` — the slash-command file itself. Frontmatter: `description:` (≤ 1024 chars; one-sentence purpose), `argument-hint: <initiative-slug> [--force]` (NO `--from`, per AUGMENTING sub-class). Body: H1 = `# /end-to-end-flow`, then four required H2 sections per parent convention §"Body structure": `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`. ≤ 200 body lines.
2. `delivery/initiatives/<initiative-slug>/flow.md` — the filled child file. **No frontmatter** (per F3.7 OQ4 resolution: narrative diagram file). Body matches the H2 structure of `templates/initiative/flow.md`: a single H2 (`## End-to-end customer flow`) with a Mermaid `sequenceDiagram` fenced block and a one-paragraph caption underneath. The fenced block contains real CamelCase actor names (matching `context-map.md`'s bounded contexts), real trigger / response messages, and any error / async branches the kit user confirmed; no `<placeholder>` substrings remain. The caption names the trigger event, the actors involved, and the success outcome in prose.
3. `delivery/initiatives/<initiative-slug>/README.md` — `last_updated:` field bumped to today's ISO-8601 date. No other mutations.

**The command does NOT write.**

- A new artifact under `delivery/`. Augmenting commands fill a pre-existing placeholder.
- A new `id:` (no new artifact).
- The initiative folder, its README, `context-map.md`, `child-specs.md`, `sequence.md`, or `capabilities.md`. Out of scope.
- Any file under `templates/`. The template is read-only reference.

A reader of this section should be able to write the command's interface signature without reading anything else.

## Body-shape contract

The `.claude/commands/end-to-end-flow.md` file body MUST contain (in order):

1. **Frontmatter.** YAML between `---` markers with exactly two keys: `description:` (one sentence, ≤ 1024 chars) and `argument-hint: <initiative-slug> [--force]`. No other keys.
2. **H1.** `# /end-to-end-flow`.
3. **Orientation paragraph.** One blockquote paragraph naming: that this is an artifact-AUGMENTING command; that it fills `delivery/initiatives/<initiative-slug>/flow.md` in-place; that it gates HANDOVERS-5 §"Required content" item 2; that the parent template is `templates/initiative/flow.md`; that it is the third link in the chain `/draft-initiative` → `/context-map` → `/end-to-end-flow` → `/sequence-initiative`.
4. **`## When to run`.** Bulleted list of triggers (at minimum: after `/context-map` has run cleanly on the same initiative; before `/sequence-initiative`; when the initiative's bounded contexts have stabilized).
5. **`## Inputs`.** Numbered list. Items in order: (a) the positional arg `<initiative-slug>`; (b) `templates/initiative/flow.md` (reference); (c) the in-place child file `delivery/initiatives/<initiative-slug>/flow.md`; (d) the pre-condition file `delivery/initiatives/<initiative-slug>/context-map.md` (must be filled); (e) the initiative `README.md`.
6. **`## Procedure`.** Numbered Step-N sub-sections: Step 1 — validate the initiative folder exists, validate `README.md` exists within it (exit 2 if missing — Step 4 reads it and Step 5 mutates it; an early exit is cleaner than a mid-walk failure), validate `context-map.md` filled (exit 2 if missing/in-placeholder); Step 2 — locate the in-place `flow.md` child (exit 2 if already filled and `--force` not set); Step 3 — walk the H2 sections one prompt at a time per the §"Per-section interactive prompts" list below; Step 4 — surface README `human_owned_decisions:` for explicit confirmation; Step 5 — bump `last_updated:` on the initiative README, run `tools/lint-frontmatter.py` against the README, report; Step 6 — emit `NEXT: /sequence-initiative <initiative-slug>`.
7. **`## What this command will not do`.** Bulleted list per parent convention §"Body structure" item 4 plus the per-command Never-do items in §"Boundaries → Never do" below.

## Per-section interactive prompts

`templates/initiative/flow.md` has exactly one H2 section (`## End-to-end customer flow`) containing a Mermaid `sequenceDiagram` fenced block and a one-paragraph caption. The command walks the kit user through the single H2 by asking the following prompts in this order — one question at a time, never batched. Verbatim phrasing the command emits:

### H2: `## End-to-end customer flow`

1. **Actor list (Mermaid `participant` declarations).** _"Looking at `context-map.md`, which bounded contexts participate in this end-to-end flow as actors? List them in the order they first appear in the happy path, using bare CamelCase identifiers (Mermaid's tokenizer breaks on angle brackets). Example: `Frontend`, `OrdersService`, `PaymentGateway`."_
2. **Swimlanes per bounded context.** _"For each bounded context you named, confirm whether it appears as a single `participant` line or whether you want to split it into multiple swimlanes (e.g., `OrdersServiceAPI` and `OrdersServiceWorker`). One swimlane per Mermaid `participant` declaration. If unsure, prefer one per bounded context."_
3. **Trigger event.** _"What is the trigger event that starts the happy path? Name the actor that initiates it and the event label. This becomes the first `->>` arrow in the diagram. Example: `User ->> Frontend: PlaceOrder`."_
4. **Happy-path sequence.** _"Walk me through the happy-path sequence one message at a time. For each message: source actor, destination actor, message label (CamelCase, no angle brackets), and whether it is a request (`->>`) or a response (`-->>`). Say `done` when the happy path reaches the success outcome."_
5. **Success outcome.** _"What is the success outcome — the final response or state change that completes the happy path? This becomes the caption's `<success outcome>` and the diagram's last arrow."_
6. **Error / failure branches.** _"Are there error or failure branches that belong in scope for this end-to-end flow? If yes, name each branch by its trigger condition and the actors involved. If the flow is happy-path-only at this stage, say `none` — error branches can be added later by re-running with `--force`."_
7. **Async / out-of-band boundaries.** _"Are there async or out-of-band boundaries in the flow — e.g., a message queue, a webhook, an eventual-consistency boundary that the diagram must represent? If yes, name each and the actors on either side. If the flow is fully synchronous, say `none`."_
8. **Caption prose.** _"Write a one-paragraph caption naming the trigger event, the actors involved, and the success outcome. Angle-bracket placeholders are fine in this prose (Mermaid's tokenizer constraint applies only inside the fenced block)."_

Confirm the filled H2 section's content with the kit user before advancing to Step 4 (the `human_owned_decisions:` surfacing). The full Mermaid block is rendered for the kit user (as raw markdown — the command does not invoke a Mermaid renderer) for visual confirmation before write.

## Pre-fill rules

The command does NOT pre-fill `id:`, `slug:`, `created:`, or `parent_*:` — `flow.md` carries **no frontmatter** per F3.7's OQ4 resolution; there is no per-file mechanical metadata to pre-fill. The only pre-fill the command performs is on the initiative `README.md`: `last_updated:` is bumped to today's ISO-8601 date (resolved from the system clock at command-start) after Step 5's interactive walk completes and before Step 5's linter run. The `last_updated:` bump is the only mutation outside `flow.md` itself.

## --force semantics

Without `--force`, the command exits 2 if `flow.md` is already filled (heuristic: contains no `<placeholder>` substrings AND no `ActorA`/`ActorB`/`TriggerEvent`/`ResponseOrSuccessOutcome` template-default identifiers). With `--force`, the command proceeds to overwrite the existing filled content via the same interactive walk — the kit user re-answers every prompt; the prior content is replaced wholesale, not merged. The command does NOT support a partial-edit / amend mode; that's deferred per parent convention's OQ on `--dry-run` and partial-edit (no ROADMAP row).

## Linter integration

Per parent convention §"Linter integration". After Step 5's `last_updated:` bump on the initiative `README.md`, the command resolves the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`, then runs `python3 <repo-root>/tools/lint-frontmatter.py delivery/initiatives/<initiative-slug>/README.md` (default mode). The linter is NOT run against `flow.md` itself — `flow.md` carries no frontmatter, so default-mode lint has nothing to assert against it. If the README lint exits non-zero, the command offers to re-open the README's frontmatter for correction; if the kit user declines, exit 3 per the convention.

## Exit codes

Per parent convention §"Exit codes". Four codes:

- `0` — `flow.md` filled, README `last_updated:` bumped, README lint passed, NEXT hint emitted.
- `1` — kit user aborted the interactive walk before completion. `flow.md` left in whatever partial state was on disk at abort time (the command does NOT roll back partial writes); a "resume by re-running with `--force`" hint is emitted.
- `2` — pre-conditions failed. Cases: `delivery/initiatives/<initiative-slug>/` does not exist (remediation: run `/draft-initiative <initiative-slug>` first); `context-map.md` still in placeholder form (remediation: run `/context-map <initiative-slug>` first); `flow.md` already filled and `--force` not set (remediation: re-run with `--force` to overwrite); positional slug malformed (remediation: pass a kebab-case slug matching `^[a-z0-9-]+$`). `flow.md` not mutated.
- `3` — `flow.md` written but the post-fill README lint exited non-zero; the kit user was offered re-open and declined (or accepted but re-run still failed). README `last_updated:` persists; the README's frontmatter is in a known-imperfect state.

## Chaining hint

Per parent convention §"Chaining hint". The command's last output line is exactly: `NEXT: /sequence-initiative <initiative-slug>`. No `REVIEW:` line — that is `/sequence-initiative`'s responsibility (the capabilities.md interstitial), not this command's.

## Boundaries

### Always do

- Validate `delivery/initiatives/<initiative-slug>/` exists AND `context-map.md` is already filled (no `<placeholder>` substrings) before any interactive prompt. The pre-condition pair is load-bearing: the Mermaid `participant` list is sourced from `context-map.md`, so a placeholder context-map leaves the diagram structurally undefined.
- Use Mermaid-safe identifiers inside every fenced `mermaid` block — bare CamelCase, no angle brackets. Restate this constraint in the actor-list prompt verbatim. The kit's `templates/initiative/flow.md` template ships with this constraint quoted in prose; the command enforces it interactively.
- Walk the H2 section's prompts one at a time, sequentially. Confirm the section's filled content (the rendered Mermaid block plus caption) before advancing to Step 4. The interactivity contract from `.claude/CLAUDE.md` is load-bearing.
- Cite HANDOVERS-5 §"Required content" item 2 in the command body's orientation paragraph.
- Bump `last_updated:` on the initiative README to today's ISO-8601 date in Step 5. The bump is the one and only metadata mutation outside `flow.md` itself.

### Ask first

- Adding a second H2 section to `flow.md` (e.g., an "Alternate flows" section separate from the main `sequenceDiagram`). HANDOVERS-5 specifies one section; expanding to two would require a HANDOVERS-5 amendment.
- Inferring actor names from any source other than `context-map.md`. The kit user names the actors; the command does not auto-derive them. If the kit user wants to add an actor not present in `context-map.md`, the command surfaces a warning and asks for explicit confirmation (the actor list and the bounded-context list should match, but the kit user owns the decision).
- Supporting Mermaid diagram types other than `sequenceDiagram` (e.g., a `flowchart` for swimlane visualization). Out of scope for P4.5; `sequence.md` (P4.6) uses `graph`/`flowchart`, this command uses `sequenceDiagram` exclusively.

### Never do

- Invent a bounded-context name not present in `context-map.md` — if `context-map.md` is still in placeholder form, exit 2 with remediation to run `/context-map` first. The swimlanes ARE the context-map's bounded contexts; inventing actors would silently desynchronize the two files.
- Auto-generate Mermaid syntax without confirming the actors / swimlanes with the kit user first. The command does NOT pre-draft a sequence diagram and ask the user to approve; it walks the prompts in order, building the diagram one arrow at a time as the user dictates.
- Use angle-bracket placeholder syntax inside the fenced `mermaid` block. Mermaid's tokenizer breaks on `<` and `>`; the template's prose explicitly notes this. The command enforces it by rejecting any answer containing `<` or `>` inside the fenced block and asking for a CamelCase rephrasing.
- Skip the `human_owned_decisions:` confirmation step (parent convention rule). Even though `flow.md` itself carries no frontmatter, the initiative README's `human_owned_decisions:` list applies to the whole folder; the command surfaces the three HANDOVERS-5-pinned decisions (`Bounded-context ownership assignment`, `Build vs buy decisions in the evolution check`, `Delivery sequencing`) for the kit user to acknowledge, even though only the first is directly relevant to flow.
- Run `tools/lint-frontmatter.py` against `flow.md` itself. `flow.md` carries no frontmatter; running default-mode lint against it is a category error.
- Modify any file under `templates/` or any other `delivery/` artifact. The command writes exactly two files: `delivery/initiatives/<initiative-slug>/flow.md` (content rewrite) and `delivery/initiatives/<initiative-slug>/README.md` (`last_updated:` bump).
- Add a `REVIEW:` line to the chaining hint. That belongs to `/sequence-initiative` per parent convention §"Capabilities-file interstitial"; this command emits NEXT only.
- Add new ontology types. Same rule as the parent convention's "Never do."

## Verification mode

- **Goal-based check** for the command file's shape: H1, four required H2 sections, two-key frontmatter, `argument-hint:` matches `<initiative-slug> [--force]` exactly, ≤ 200 body lines, `tools/lint-command.sh` exits 0.
- **Audit-driven** for the parent convention's contract test: `python3 -m pytest scripts/tests/test_phase4_command_shape.py -k end-to-end-flow` exits 0 (auto-discovers this command via the parent convention's `INSCOPE` constant once it's on disk).
- **Manual gesture** for the interactive walk: against a fixture initiative folder under a tempdir (folder created by hand from `templates/initiative/`, `context-map.md` pre-filled with two bounded-context names), run the command, answer the eight prompts, confirm `flow.md` is written with a syntactically valid Mermaid block, no `<placeholder>` substrings remain, the README `last_updated:` is bumped. Re-run against the same fixture without `--force` and confirm exit 2.
- **Manual gesture** for the pre-condition guards: run against a non-existent initiative slug (expect exit 2 with remediation naming `/draft-initiative`); run against an initiative whose `context-map.md` still contains `<placeholder>` substrings (expect exit 2 with remediation naming `/context-map`).

## Contract tests

Each test is one shell line or one pytest case. They are the gate.

- `T1` — `test -f .claude/commands/end-to-end-flow.md` (the command file exists).
- `T2` — `bash tools/lint-command.sh .claude/commands/end-to-end-flow.md` exits 0.
- `T3` — Frontmatter has exactly two keys (`description:`, `argument-hint:`). Asserted by a python one-liner that parses YAML.
- `T4` — `grep -E '^argument-hint: <initiative-slug> \[--force\]$' .claude/commands/end-to-end-flow.md` returns 1 (argv contract matches AUGMENTING sub-class; no `--from`).
- `T5` — Required H2 sections present in order: `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`. Asserted by `grep -n` monotonicity check.
- `T6` — Body cites `templates/initiative/flow.md` and `delivery/initiatives/<initiative-slug>/flow.md` at least once each. Asserted by `grep -c`.
- `T7` — Body cites `context-map.md` as a pre-condition AND names the exit-2 remediation. Asserted by `grep -c 'context-map\.md'` ≥ 2 AND `grep -c '/context-map'` ≥ 1.
- `T8` — Body wc -l ≤ 200.
- `T9` — `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (the parent contract test auto-discovers this command via `INSCOPE`).
- `T10` — Body contains the literal string `NEXT: /sequence-initiative <initiative-slug>` (the chaining hint is documented in the command body, even though emitted at runtime). Asserted by `grep -c`.
- `T11` — Body does NOT contain `REVIEW:` (per Never-do: this command emits NEXT only; the REVIEW line belongs to `/sequence-initiative`). Asserted by `grep -c '^REVIEW:'` returns 0.
- `T12` — `bash tools/pre-pr.sh` exits 0 (kit-wide health check after the command lands).
- `T13` — ROADMAP P4.5 checkbox flipped (CAPTURE-phase predicate): `grep -c '^- \[x\] \*\*P4\.5\*\*' ROADMAP.md` returns 1.

## Non-goals

- Authoring the other six in-scope Phase-4 commands (P4.1, P4.3, P4.4, P4.6, P4.8, P4.11). Separate specs; run in parallel under the parent F4 fan-out.
- Implementing a Mermaid syntax validator. The command relies on the kit user's confirmation of the rendered block; mechanical Mermaid linting is out of scope for the whole kit (F3.7 §"Open questions" Q6 resolution).
- Modifying `templates/initiative/flow.md`, `templates/initiative/context-map.md`, or any other F3.x template. Templates are frozen per their own F3.x specs.
- Modifying `tools/lint-frontmatter.py`, `tools/lint-command.sh`, `scripts/tests/test_phase4_command_shape.py`, or `tools/pre-pr.sh`. The command consumes them as-is.
- Auto-deriving the actor list from `context-map.md` programmatically. The kit user names the actors interactively; auto-derivation would defeat the "one question at a time" contract.
- Supporting partial-edit / amend mode. Re-running with `--force` is full replacement; partial edits are out of scope.
- Chaining beyond `/sequence-initiative`. The NEXT line names the immediate successor only; multi-hop chains are out of scope.
- Adding any new ontology type. Same rule as parent convention.

## Open questions

1. **Should `/end-to-end-flow` REQUIRE `context-map.md` to be already-filled, or just warn?** _Resolved here: **require** (exit 2 with remediation). The Mermaid swimlanes ARE the context-map's bounded contexts; allowing the command to proceed with a placeholder context-map would either (a) force the kit user to invent actor names that desynchronize from the eventual context-map, or (b) leave the diagram structurally undefined. The cost of requiring it: one extra `/context-map` invocation before `/end-to-end-flow`. The cost of warn-only: silent desynchronization between two files in the same folder that downstream audits (`/audit-traceability`, `/audit-completeness`) may not catch because neither file carries machine-readable cross-references. The exit-2 remediation message names `/context-map` explicitly._

## Acceptance criteria

- [ ] `.claude/commands/end-to-end-flow.md` exists; passes `tools/lint-command.sh`; carries the two-key frontmatter (`description:`, `argument-hint: <initiative-slug> [--force]`); H1 is `# /end-to-end-flow`; the four required H2 sections are present in order; body ≤ 200 lines.
- [ ] Body cites `templates/initiative/flow.md`, `delivery/initiatives/<initiative-slug>/flow.md`, `context-map.md` (as pre-condition), HANDOVERS-5 §"Required content" item 2, and the parent convention.
- [ ] Body documents all eight per-section interactive prompts verbatim (actor list, swimlanes, trigger event, happy-path sequence, success outcome, error/failure branches, async boundaries, caption prose).
- [ ] Body documents the four exit codes (0/1/2/3) with the AUGMENTING-specific exit-2 cases (folder missing, `context-map.md` in placeholder form, already-filled without `--force`, malformed slug).
- [ ] Body documents the `last_updated:` bump on the initiative README as the only mutation outside `flow.md` itself.
- [ ] Body documents `NEXT: /sequence-initiative <initiative-slug>` as the chaining hint, with no `REVIEW:` line.
- [ ] All contract tests pass: T1–T13.
- [ ] No new ontology type added; no F3.x template modified; no `tools/` script modified; no other slash command modified.

## Cross-references

- **Consumed by:** kit users running the Phase-4 chain on an initiative; `/audit-completeness` (indirectly, when verifying HANDOVERS-5 §"Required content" item 2 is satisfied).
- **Consumes:** `docs/specs/phase-4-command-convention/spec.md` (parent convention); `docs/HANDOVERS.md` §"Handover 5"; `templates/initiative/flow.md` (reference); `templates/initiative/context-map.md` (pre-condition file's template, by reference); `docs/specs/template-initiative/spec.md` (F3.7); `tools/lint-command.sh`; `tools/lint-frontmatter.py`; `.claude/commands/_meta/command-skeleton.md` (copied as starting point).
- **Frontmatter fields owned:** none directly. The command bumps `last_updated:` on the initiative README; it does not own any new frontmatter field.
- **Ontology object types touched:** Business Workflow / Flow (Domain G — the `flow.md` body content represents this type; not instantiated as a typed artifact because `flow.md` carries no frontmatter per F3.7's OQ4). Initiative (Domain D — the parent folder, mutated via `last_updated:` bump on its README).
