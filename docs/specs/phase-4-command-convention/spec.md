# Spec: phase-4-command-convention

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** convention text + skeleton file + contract test
- **Serves kit phase:** Meta (kit infrastructure — the contract for the seven Phase-4 template-fill slash commands)
- **Constrained by:** ROADMAP P4.1, P4.3, P4.4, P4.5, P4.6, P4.8, P4.11 (the seven commands that consume this convention); `docs/HANDOVERS.md` Handovers 4, 5, 6 (the boundary contracts the commands gate); `docs/CONVENTIONS.md` §"Universal metadata schema", §"Specs and Plans", §"Templates — `templates/<slug>.md`" (the parent F3 convention this spec mirrors in shape and consumes by reference); `docs/specs/template-authoring-convention/spec.md` (the F3 precedent for "parent-convention-then-fan-out"; PM specs live at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>/` per its OQ2); `tools/lint-command.sh` (existing per-command shape linter); `tools/lint-frontmatter.py` (default-mode linter the commands run against the artifacts they write); `.claude/skills/work-loop/SKILL.md` (the build pattern every F4 worker follows); `.claude/CLAUDE.md` "How we work together" (one-question-at-a-time, no batching — the interactivity contract this spec encodes mechanically).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Defines the authoring convention every Phase-4 *template-fill* slash command must follow, ships a literal `.claude/commands/_meta/command-skeleton.md` they copy from, and ships a contract test (`scripts/tests/test_phase4_command_shape.py`) that mechanically validates each command once authored. The whole point: collapse seven "shape" decisions into one and turn seven serialized work-loops into seven parallel ones — mirroring what `template-authoring-convention` did for F3.1–F3.10.

## Objective

Three coupled deliverables that, together, make P4.1, P4.3, P4.4, P4.5, P4.6, P4.8, and P4.11 safely parallelizable:

1. **A short authoring convention** appended to `docs/CONVENTIONS.md` as a new §"Phase-4 Template-Fill Commands — `.claude/commands/draft-*.md` and siblings" sub-section. Names body structure, argv contract, parent-artifact resolution, interactive-fill behavior, pre-fill rules, linter integration, exit codes, chaining hint, and the in-scope command list.
2. **A literal command skeleton** at `.claude/commands/_meta/command-skeleton.md` that every in-scope worker copies and fills. One file. ≤ 120 body lines. No domain-specific content — only shape contract. The skeleton's H1 is a `<placeholder>` so the skeleton itself is not a runnable slash command.
3. **A contract test** at `scripts/tests/test_phase4_command_shape.py`. Walks the seven in-scope command paths (whichever exist at test-time — the test is auto-skipped for paths that don't yet exist, so it ships green before P4.1 lands and tightens as each worker ships). For each existing in-scope path, asserts: `tools/lint-command.sh` exits 0; the convention-required H2 sections exist; the `argument-hint:` frontmatter follows the argv contract; the documented `templates/` path the command consumes exists in the repo; the documented destination directory exists under `delivery/`. A separate `test_skeleton_passes_lint_command` runs `tools/lint-command.sh` against the skeleton itself.

The convention is scoped to the **seven template-fill commands** that share a single shape: read parent artifact → consume kit template → walk placeholders interactively → write filled artifact → lint → emit next-command hint. The other nine ROADMAP P4.x items (P4.2, P4.7, P4.9, P4.10, P4.12, P4.13, P4.14, P4.15, P4.16) are explicitly **out of scope** and get individual specs in the F4 fan-out.

## Why now

P4.1, P4.3, P4.4, P4.5, P4.6, P4.8, and P4.11 are seven of the next sixteen ROADMAP items in the Phase-4 (Delivery) block. They share contract surface: all seven instantiate a kit-provided F3.x template (or write into an existing initiative folder per F3.7) by walking the placeholders interactively with a single human. Authoring this convention before fanning out collapses seven "shape" decisions into one and turns seven serialized loops into seven parallel ones. The cost is one short loop. The cost of *not* doing it is seven commands that drift on argv parsing, parent-resolution, interactivity, pre-fill rules, and exit-code conventions, then a remediation pass that touches all seven.

The F3 precedent (`template-authoring-convention`, shipped 2026-05-22) demonstrated the payoff: ten parallel F3.x template specs landed in a single session because the shape was locked first. F4 is one row larger in the convention's reach (seven commands vs ten templates), but the move is the same.

F3.6, F3.7, F3.8, F3.9 (the four F3.x templates these commands consume) shipped on 2026-05-22; the contract surface this spec consumes is therefore stable.

## Inputs and outputs

**Inputs.**

- `docs/HANDOVERS.md` §§ "Handover 4: Vision → Initiative", "Handover 5: Initiative → Spec", "Handover 6: Spec → Engineering Handoff Packet" — the source contracts for the artifacts the seven commands produce. Frontmatter superset on each artifact's README is quoted directly from here in the per-command specs (not in this convention spec).
- `docs/CONVENTIONS.md` §"Universal metadata schema" — the universal frontmatter superset every written artifact carries. The commands pre-fill the mechanical subset (`id`, `slug`, `created`, `last_updated`, the resolved `parent_*`).
- `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" — the parent F3 convention. This spec consumes that convention by reference; this spec adds the *command*-side contract that pairs with the F3 *template*-side contract.
- `docs/specs/template-authoring-convention/spec.md` — the F3 precedent in shape. OQ2's resolution (PM specs live at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>/`) is the destination path P4.8 (`/draft-spec`) cites in its per-command spec.
- `templates/vision.md` (F3.6, shipped 2026-05-22) — single-file template for the Vision artifact. P4.1 consumes.
- `templates/initiative/` (F3.7, shipped 2026-05-22) — folder template with `README.md`, `context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`. P4.3 instantiates the folder; P4.4, P4.5, P4.6 fill specific child files (`context-map.md`, `flow.md`, `sequence.md` respectively) interactively, as refinement commands operating on an existing initiative folder. The remaining children (`child-specs.md`, `capabilities.md`) are not the target of a P4.x command at this time — they are populated incidentally by `/draft-initiative` (P4.3) and by `/draft-spec` (P4.8, which appends to `child-specs.md`).
- `templates/pm-spec.md` (F3.8, shipped 2026-05-22) — single-file template for the PM Spec artifact. P4.8 consumes.
- `templates/handoff-packet/` (F3.9, shipped 2026-05-22) — folder template with README + 21 narrative children + `requirements.yaml`. P4.11 consumes.
- `tools/lint-command.sh` — existing shape linter for `.claude/commands/*.md`. Enforces: YAML frontmatter present, `description:` field present and ≤ 1024 chars, H1 starts with `/`, body has `## When to run` or `## Procedure`. This convention is layered on top; the convention adds further H2-section, argv, and behavioral requirements that lint-command.sh does not enforce.
- `tools/lint-frontmatter.py` (default mode, NOT `--check-template`) — the linter the commands run against the artifact they wrote, **after** placeholder fill. Default mode walks `PHASE_DIRS = ["strategy", "discovery", "validation", "delivery", "market"]` per `template-authoring-convention` §"Outputs" item 4 — `delivery/` is in scope so artifacts written by the seven commands are linted in default mode.
- `.claude/skills/work-loop/SKILL.md` — the build pattern every F4 worker follows. This convention does not modify the skill; it relies on it.
- `.claude/CLAUDE.md` "How we work together" — "One clarifying question at a time. Never batch." The interactivity contract this spec encodes mechanically in the convention text.
- `.claude/commands/phase-guide.md`, `.claude/commands/audit-traceability.md`, `.claude/commands/audit-completeness.md`, `.claude/commands/audit-portfolio-coherence.md`, `.claude/commands/competitive-research.md` — the five existing slash commands the kit ships. Their body structure (H1 = `/<name>`, then H2 sections including `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`) is the structural precedent this convention codifies. **None** of the five are template-fill commands (audits and a research command); they share the body skeleton but not the template-fill behavior. The convention's behavioral rules (parent resolution, interactive fill, etc.) are additive on top of the shape they already follow.

**Outputs.**

1. `docs/CONVENTIONS.md` — new §"Phase-4 Template-Fill Commands — `.claude/commands/draft-*.md` and siblings" sub-section appended after the existing §"Templates — `templates/<slug>.md`" sub-section (so templates and the commands that consume them sit adjacent in the conventions doc). Exact text contract in §"Convention-text contract" below.
2. `.claude/commands/_meta/command-skeleton.md` — new file. Exact text contract in §"Skeleton-text contract" below. Skeleton's H1 is `# /<command-name>` with `<command-name>` as a literal angle-bracket placeholder — by construction, the skeleton is not a runnable slash command (Claude Code resolves slash commands by exact filename match, and `command-skeleton.md` is not in the form `<verb>.md` that the slash-command lookup needs; additionally the `_meta/` directory is conventionally non-loaded). The skeleton passes `tools/lint-command.sh` because lint-command.sh's H1 regex is `^# /` which the literal `# /<command-name>` line matches (the `/` is the load-bearing character; lint-command does not validate the verb).
3. `.claude/commands/_meta/README.md` — new file. One-paragraph index that explains what `_meta/` is for (skeleton + future command-build helpers), names the skeleton, and points to this convention. **No YAML frontmatter** — this README is prose-only documentation, not a kit artifact. The contract test (output 4 below) explicitly skips this README.
4. `scripts/tests/test_phase4_command_shape.py` — new pytest file. Test cases:
   - `test_skeleton_passes_lint_command` — runs `tools/lint-command.sh .claude/commands/_meta/command-skeleton.md`; asserts exit 0. **Unconditional** — must always pass.
   - `test_skeleton_uses_placeholder_h1` — asserts the skeleton's H1 line contains `<command-name>` (angle-bracket placeholder, not a runnable command name).
   - `test_inscope_commands_pass_lint` — for each path in the **in-scope command list** (defined as a module-level constant `INSCOPE = ["draft-vision", "draft-initiative", "context-map", "end-to-end-flow", "sequence-initiative", "draft-spec", "handoff-packet"]`), if `.claude/commands/<name>.md` exists, run `tools/lint-command.sh` and assert exit 0; if the file does not exist, mark the case `pytest.skip("not yet shipped")`. **Auto-tightens** — the test starts green (no in-scope commands exist yet) and tightens as P4.x workers ship.
   - `test_inscope_commands_have_required_h2s` — for each existing in-scope command, assert the body contains all of: `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`. (Convention requires four; lint-command requires one — the test enforces the convention superset.)
   - `test_inscope_commands_declare_argv` — for each existing in-scope command, parse the frontmatter and assert `argument-hint:` is present and starts with either the literal `<slug>` (artifact-creating commands: `draft-vision`, `draft-initiative`, `draft-spec`, `handoff-packet`) or the literal `<initiative-slug>` (artifact-augmenting commands: `context-map`, `end-to-end-flow`, `sequence-initiative`). The expected positional per command is encoded in a second module-level constant `POSITIONAL = {"draft-vision": "<slug>", "draft-initiative": "<slug>", "context-map": "<initiative-slug>", "end-to-end-flow": "<initiative-slug>", "sequence-initiative": "<initiative-slug>", "draft-spec": "<slug>", "handoff-packet": "<slug>"}`. The test reads from POSITIONAL.
   - `test_inscope_commands_cite_template_path` — for each existing in-scope command, search the body for at least one path matching `templates/(?:[a-z0-9-]+/)*[a-z0-9-]+(\.md|/)` AND assert that path exists in the repo. Catches drift where a command points to a template that doesn't exist (e.g., a renamed F3 template). The regex permits multi-level template paths so augmenting-command bodies can cite specific children of folder templates (e.g., `templates/initiative/context-map.md`) and still pass.
   - `test_inscope_commands_cite_destination_path` — for each existing in-scope command, search the body for at least one `delivery/<subdir>/` path AND assert the parent directory `delivery/<subdir>/` exists in the repo (the artifact slug itself need not exist; only the family directory). Catches drift where a command points to a destination directory the kit doesn't have.
   - `test_inscope_count_is_seven` — sanity check that `len(INSCOPE) == 7` and `len(POSITIONAL) == 7`. Guards against silent in-scope-list drift in either direction.
5. `docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md` — a one-page checklist that each F4 worker's per-command spec is expected to satisfy. Restates the convention as a checklist for spec authors (not for command runtime). Five rows: (a) cites this convention as `Constrained by:` in the spec header, (b) names the template path consumed, (c) names the destination write path, (d) declares the parent-artifact-resolution rule (auto-detect vs explicit `--from`), (e) enumerates the per-section interactive prompts with the human-facing copy. **Not gated by the contract test** — the checklist is editorial guidance, not machine-checkable.
6. `ROADMAP.md` — Phase 4 block prepended with a one-line cross-reference ("P4.1, P4.3, P4.4, P4.5, P4.6, P4.8, P4.11 items consume the command convention from `docs/specs/phase-4-command-convention/`. Read that spec first; copy `.claude/commands/_meta/command-skeleton.md` to start each command."). No checkboxes flipped; the seven rows remain unchecked.

A reader of this section should be able to construct the diff without reading anything else.

## Convention-text contract

The new §"Phase-4 Template-Fill Commands — `.claude/commands/draft-*.md` and siblings" sub-section in `docs/CONVENTIONS.md` ships with this exact body (reviewed before execution, not authored during it):

> ### Phase-4 Template-Fill Commands — `.claude/commands/draft-*.md` and siblings
>
> Seven slash commands in Phase 4 (Delivery) share a single behavioral shape: read a parent product artifact → consume a kit-provided F3.x template (single file or folder) → walk the template's placeholders interactively with a single human → write the filled artifact under `delivery/` → run `tools/lint-frontmatter.py` (default mode) against the written file → emit a "next command in the chain" hint. The seven split into two sub-classes:
>
> - **Artifact-creating commands** (4): `/draft-vision` (P4.1), `/draft-initiative` (P4.3), `/draft-spec` (P4.8), `/handoff-packet` (P4.11). These take a new-artifact slug as their positional argument and write to a *new* destination path (`delivery/visions/<slug>.md`, `delivery/initiatives/<slug>/`, `delivery/initiatives/<initiative-slug>/specs/<spec-slug>/`, `delivery/handoff-packets/<slug>/`). They pre-fill an `id:` derived from the slug.
> - **Artifact-augmenting commands** (3): `/context-map` (P4.4), `/end-to-end-flow` (P4.5), `/sequence-initiative` (P4.6). These take an *existing* initiative slug as their positional argument and write (or replace) a specific child file within `delivery/initiatives/<initiative-slug>/` (`context-map.md`, `flow.md`, `sequence.md` respectively). They do **not** create a new artifact; they fill a placeholder child within an existing folder. They do not pre-fill `id:` (no new artifact).
>
> The other nine ROADMAP P4.x items (analytical commands, audits, comms commands, the retro facilitator, the EARS-lint skill, the roadmap-skeptic agent) are out of scope; they ship under their own per-item specs.
>
> **Body structure.** Every in-scope command's body has these H2 sections, in this order:
> 1. `## When to run` — bulleted list of triggers.
> 2. `## Inputs` — numbered list. First item is always "the slug (positional arg)"; second is always the template-path the command consumes; subsequent items name parent-artifact-resolution rules and any other input.
> 3. `## Procedure` — numbered Step-N sub-sections. Procedure must include, at minimum: Step 1 — resolve parent artifact; Step 2 — instantiate template at destination; Step 3 — walk placeholders one section at a time (NEVER batch — restates the kit's interactivity contract from `.claude/CLAUDE.md`); Step 4 — surface `human_owned_decisions:` for explicit human confirmation; Step 5 — run `tools/lint-frontmatter.py <written-path>` and report the result; Step 6 — emit the "next command in the chain" hint.
> 4. `## What this command will not do` — bulleted list of explicit non-behaviors. At minimum: "Not overwrite an existing artifact at the destination without `--force`"; "Not skip the `human_owned_decisions:` confirmation step"; "Not fabricate evidence — if the parent artifact lacks a referenced field, ask, do not invent"; "Not batch placeholder questions — one at a time".
>
> **Frontmatter.** Required keys: `description:` (≤ 1024 chars; one-sentence purpose; the slash-command palette renders this) and `argument-hint:` (string, see Argv contract below). No other frontmatter keys.
>
> **Argv contract.** First positional argument is a kebab-case identifier matching `^[a-z0-9-]+$` and ≤ 80 chars, naming the *operated-upon* artifact:
> - For **artifact-creating commands**, the positional is `<slug>` — the slug of the new artifact to be created.
> - For **artifact-augmenting commands**, the positional is `<initiative-slug>` — the slug of the existing initiative folder whose child file the command fills.
>
> The `argument-hint:` frontmatter value names the positional explicitly using one of those two tokens (literal `<slug>` or literal `<initiative-slug>`) so the contract test can distinguish the two sub-classes. Optional flags follow:
> - `--from <parent-slug>` — explicit parent-artifact selection; overrides auto-detection.
> - `--force` — permit overwriting an existing artifact at the destination (creating commands) or an already-filled child file (augmenting commands).
> - `--dry-run` is **not** part of the convention (deferred per Open Question 3).
>
> Example `argument-hint:` values: `<slug> [--from <parent-slug>] [--force]` (creating); `<initiative-slug> [--force]` (augmenting — `--from` is not applicable because the parent is the initiative itself, named by the positional).
>
> **Parent-artifact resolution.** Applies to artifact-creating commands; augmenting commands skip this step (the parent — the initiative folder named by the positional `<initiative-slug>` — is already named explicitly). If `--from <parent-slug>` is given, use it. Otherwise, list the candidate parent artifacts (the family directory's contents) filtered by `status:` not in the **terminal-or-killed set**: `Deprecated` (product-artifact track per `docs/CONVENTIONS.md` §"Lifecycle states"), plus `killed` for Learning Memos (per `docs/HANDOVERS.md` Handover 3, where Learning-Memo `status:` is `survived | killed`). If the candidate list exceeds 10, present the 10 most recently updated (sorted by `last_updated:` descending) and suggest `--from <parent-slug>` for explicit selection of an older candidate. If the candidate list is empty, exit with code 2 and a remediation suggestion naming the prerequisite command. Always confirm even when only one candidate exists (per Open Question 7). **Never silently pick** — the auto-pick failure mode is the silent failure HANDOVERS-4/5/6 are designed to prevent (a vision draft attached to the wrong learning memo, an initiative attached to the wrong vision).
>
> **Interactive fill.** Walk the template's placeholders **one H2 section at a time**. If an H2 contains H3 sub-sections, treat each H3 as a separate fill unit; do not advance to the next H2 until every H3 within the current H2 is confirmed. Within a section: ask the human one question per placeholder, sequentially. **Never batch.** Confirm the section's filled content before advancing. The kit's "one clarifying question at a time" rule from `.claude/CLAUDE.md` is load-bearing here.
>
> **Pre-fill rules.** Before asking the human anything, the command pre-fills the mechanical fields the template's frontmatter declares as placeholders:
> - `id:` — derived from slug per the ontology type prefix (e.g., a Vision is `VIS-<NNN>` where `<NNN>` is the next unused integer in `delivery/visions/`).
> - `slug:` — the positional argument.
> - `created:` — today's date, ISO-8601, resolved from the system clock at command-start.
> - `last_updated:` — same as `created` on first instantiation.
> - `parent_*:` fields — resolved parent slug from the resolution step above.
> - `object_type:` — already pre-filled in the template per the F3 authoring convention; the command re-asserts it (a defensive check).
>
> The human is never asked to type a mechanical field. If a mechanical field cannot be resolved (e.g., no parent artifact exists), the command stops and reports the missing pre-condition with a remediation suggestion (e.g., "no learning memo found in `validation/learnings/` — run `/learning-memo` first").
>
> **Linter integration.** After the interactive fill completes, the command resolves the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py` (do not assume the working directory is the repo root), then runs `python3 tools/lint-frontmatter.py <written-artifact-path>` (default mode, NOT `--check-template` — the artifact is now a real product artifact, not a template) and surfaces the linter's exit code and any errors to the human. If the linter exits non-zero, the command does not declare success; it offers to re-open the relevant sections for correction.
>
> **Exit codes.**
> - `0` — artifact written, linter passed, next-command hint emitted.
> - `1` — human aborted the interactive walk before completion (artifact left at its partial state on disk; the command emits a "resume by re-running with the same slug" hint).
> - `2` — pre-conditions failed (no parent artifact, slug malformed, destination already exists without `--force`, template path missing, candidate parent list empty). Artifact not written.
> - `3` — artifact was written but the post-fill linter exited non-zero; the command offered to re-open relevant sections for correction and the human declined (or accepted but did not re-run the lint). Artifact persists on disk in a known-imperfect state. Automation consumers MUST treat exit 3 as distinct from exit 0 (the file exists but its frontmatter does not pass the kit's default-mode linter).
>
> **Chaining hint.** The command's last output line names the next command in the Phase 4 chain, formatted exactly: `NEXT: /<command-name> <slug>`. The chain is `/draft-vision` → `/draft-initiative` → (`/context-map`, `/end-to-end-flow`, `/sequence-initiative` in any order) → `/draft-spec` (per child spec) → `/handoff-packet`. `/handoff-packet`'s NEXT line names `/audit-completeness <slug>` (Phase 5 entry, the existing command). If a chain successor is not yet shipped, the NEXT line uses the canonical name plus `(planned — ROADMAP P<row>)` per the kit-drift policy.
>
> **Capabilities-file interstitial.** `delivery/initiatives/<slug>/capabilities.md` is HANDOVERS-5 required content but has no dedicated Phase-4 command (capabilities are typically populated incidentally during `/draft-initiative`'s Step-3 walk). `/sequence-initiative`'s NEXT line MUST therefore include a reviewer-prompt second line: `REVIEW: delivery/initiatives/<slug>/capabilities.md — verify the Capability list is filled and each row traces to a parent Problem before running /draft-spec.` This is a NEXT-output additional line, not an automated check; the human is responsible for the review. Other commands in the chain do not emit a REVIEW line.
>
> **Authoring a new in-scope command.** Copy `.claude/commands/_meta/command-skeleton.md`. Read the relevant `docs/HANDOVERS.md` row (4, 5, or 6) for the artifact this command produces. Read the F3.x template the command will consume. Fill the per-command spec under `docs/specs/cmd-<verb>/` first; the `per-command-spec-checklist.md` in this convention's `notes/` enumerates what that spec must include.

## Skeleton-text contract

`.claude/commands/_meta/command-skeleton.md` ships with this exact body. Comments preserved (they're the author guidance the F4 workers read while filling).

```markdown
---
description: <one sentence, ≤ 1024 chars — the slash-command palette renders this>
argument-hint: <slug> [--from <parent-slug>] [--force]
# ↑ For artifact-creating commands. For augmenting commands (context-map,
# end-to-end-flow, sequence-initiative) use: <initiative-slug> [--force]
---

# /<command-name>

> <One paragraph: what this command produces, which HANDOVERS row it gates, which template it consumes, what artifact it writes (creating) OR which child file it fills (augmenting). State explicitly whether this is a creating or augmenting command.>

## When to run

- <Trigger 1 — e.g., "After a learning memo's status flips to survived">
- <Trigger 2>
- <Trigger N>

## Inputs

1. The positional arg — `<slug>` (creating commands; the new artifact's slug) OR `<initiative-slug>` (augmenting commands; the existing initiative folder). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars.
2. `templates/<template-path>` — the F3.x template this command consumes.
3. Parent artifact: `<delivery|validation|…>/<parent-family>/<parent-slug>` (creating commands; resolution rule below) OR the initiative folder named by the positional (augmenting commands; no resolution).
4. `<any other input — e.g., a fixture, a configuration file>`

## Procedure

### Step 1 — resolve parent artifact (creating commands) OR validate initiative folder exists (augmenting commands)

**Creating:** If `--from <parent-slug>` is given, use it. Otherwise list candidates from `<parent-family>/` whose `status:` is not in the terminal-or-killed set, sorted by `last_updated:` descending and capped at 10. Present as a numbered list; ask the human to pick one (or to specify `--from` for an older candidate). Never silently pick. If the candidate list is empty, exit with code 2 and surface the missing pre-condition with a remediation suggestion (e.g., "no <parent-type> found in <parent-family>/ — run `/<prerequisite-command>` first").

**Augmenting:** Verify `delivery/initiatives/<initiative-slug>/` exists. If not, exit code 2 with the remediation suggestion to run `/draft-initiative` first.

### Step 2 — instantiate the template (creating) OR locate the child file (augmenting)

**Creating:** Copy `templates/<template-path>` to `<delivery>/<destination-family>/<slug>.md` (or, for folder templates, `cp -r` to `<delivery>/<destination-family>/<slug>/`). If the destination exists and `--force` is not set, exit with code 2 and a remediation suggestion. Pre-fill mechanical fields (`id`, `slug`, `created`, `last_updated`, the resolved `parent_*`, `object_type`).

**Augmenting:** The target child file already exists inside the initiative folder (created by `/draft-initiative`). If the child file is already filled (heuristic: contains no `<placeholder>` substrings) and `--force` is not set, exit code 2 with the remediation suggestion to re-run with `--force`. Augmenting commands do NOT pre-fill `id:` (no new artifact); they update `last_updated:` on the initiative `README.md` to today's date after Step 5 succeeds.

### Step 3 — walk placeholders one H2 section at a time

For each H2 in the template body (or the child file), ask one question per placeholder, sequentially. If an H2 contains H3 sub-sections, treat each H3 as a separate fill unit and confirm all H3s within an H2 before advancing. Never batch. Confirm the section's filled content before advancing.

### Step 4 — surface human-owned decisions

Read the template's `human_owned_decisions:` frontmatter list (for creating commands) or the initiative README's `human_owned_decisions:` list (for augmenting commands). For each entry, present it to the human and ask for explicit confirmation that the decision is owned and (where applicable) signed off. Record the confirmations in `approvals_obtained:`.

### Step 5 — lint the written artifact

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`; do not assume the working directory is the repo root. Run `python3 <repo-root>/tools/lint-frontmatter.py <written-path>` (default mode). Report the result.

- If the linter exits 0: proceed to Step 6.
- If the linter exits non-zero: offer to re-open the relevant sections for correction. If the human accepts and the corrections lint clean on re-run, proceed to Step 6 normally. If the human declines (or re-runs but lint still fails), exit code 3 with the linter output surfaced and the artifact left on disk.

### Step 6 — emit the next-command hint

Last line of output, formatted exactly: `NEXT: /<next-command-name> <positional>`. If the next command isn't yet shipped, append `(planned — ROADMAP P<row>)`. For `/sequence-initiative` only, also emit a `REVIEW: delivery/initiatives/<initiative-slug>/capabilities.md — verify the Capability list is filled and each row traces to a parent Problem before running /draft-spec.` line immediately before the NEXT line.

## What this command will not do

- Not overwrite an existing artifact (creating) or already-filled child (augmenting) without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the parent artifact lacks a referenced field, ask, do not invent.
- Not batch placeholder questions — one at a time.
- Not silently pick a parent artifact when multiple candidates exist (creating commands only).
- Not assume the working directory is the repo root when invoking the linter.
- <Add per-command non-behaviors here — e.g., "Not write a vision without citing a learning memo with `status: survived`".>
```

## Boundaries

### Always do

- Quote `docs/CONVENTIONS.md` (universal-metadata schema and the §"Templates" sub-section authored by `template-authoring-convention`) verbatim for every shared-shape claim in the convention text. The Phase-4 command convention is a re-projection of those two, not a parallel source of truth.
- Keep `.claude/commands/_meta/command-skeleton.md` ≤ 120 body lines. If it grows, the convention has become a parallel source of truth and we have a drift problem.
- Use angle-bracket placeholder syntax exclusively in the skeleton (matching the F3 placeholder rule).
- Restate the kit's "one question at a time, never batch" rule from `.claude/CLAUDE.md` directly in the convention text — that rule is load-bearing for the commands' interactivity guarantee.

### Ask first

- Adding any new shared field to the convention's argv contract beyond `<slug>`, `--from`, `--force` (e.g., `--dry-run`, `--non-interactive`). The argv contract is the most copied surface; growing it grows the convention's reach and warrants explicit sign-off.
- Expanding the in-scope command list beyond the seven named here (e.g., later folding `/release-notes` or `/launch-checklist` into the convention). The list of seven is the unit of fan-out parallelism; growing it after the fan-out is mid-flight defeats the point.
- Modifying `tools/lint-command.sh` to enforce convention-specific rules. That couples a generic linter to a phase-specific convention. Keep convention enforcement in `scripts/tests/test_phase4_command_shape.py`.

### Never do

- Add new ontology types. Phase-4 commands instantiate existing ontology types (Vision, Initiative, PM Spec, Handoff Packet, Context Map, Flow, Sequence) — they don't introduce new ones. Same rule as F0.11 and F3 template-authoring-convention's "Never do" section.
- Treat any of the seven commands as "convention-exempt" inside this spec. The convention is the contract; if a command needs to deviate, that's a separate per-command spec deviation surfaced explicitly via its own adversarial review, not a quiet exception here.
- Edit any of the other nine ROADMAP P4.x rows (P4.2, P4.7, P4.9, P4.10, P4.12, P4.13, P4.14, P4.15, P4.16) other than to add the cross-reference pointer named in §"Outputs" item 6. Those rows remain owned by their own future specs.
- Walk `.claude/commands/` from any default-mode linter (e.g., adding command discovery to `tools/lint-frontmatter.py`). Out of scope; commands are not product artifacts and don't carry universal-schema frontmatter.
- Tighten `tools/lint-command.sh`'s H1 regex beyond `^# /` without amending the skeleton's H1 placeholder simultaneously. The skeleton's H1 is the literal `# /<command-name>`, which passes the current `^# /` check (the `/` is the load-bearing character). A future hardening that requires a real verb (e.g., `^# /[a-z][a-z0-9-]*`) would silently break the skeleton; if anyone proposes that hardening, the skeleton's H1 must be updated in the same change.

## Verification mode

- **Goal-based check** for the docs and skeleton edits (greps assert added phrases; CONVENTIONS.md still parses as valid Markdown; lint-command.sh exits 0 against the skeleton).
- **TDD** for the contract test: tests come before the data they assert against. The seven in-scope command-name strings are committed to the test module's `INSCOPE` constant in the same change as the test; subsequent F4 workers consume the constant via `cat scripts/tests/test_phase4_command_shape.py | grep INSCOPE`.
- **Audit-driven** for kit-wide health: `tools/pre-pr.sh` exits 0.

The skeleton itself is **not** verified by manual gesture (no real command run against a fixture) — the skeleton is a copyable shape contract, not a runnable command. Manual-gesture verification is the responsibility of each per-command spec's verify phase, not this convention's.

**Why no `lint-command.sh` mode (in contrast to F3's `--check-template` mode on `lint-frontmatter.py`).** F3 added a new linter mode because templates carry universal-schema frontmatter that is otherwise machine-checked in default mode — without `--check-template`, the linter rejects placeholders. Phase-4 commands carry only `description:` and `argument-hint:`, neither of which has placeholder-vs-concrete-value ambiguity at lint time; the convention's assertions (H2 sections present, argv form correct, cited paths exist) are about *body content and cross-file references*, not frontmatter validity. The pytest module is the natural home for those assertions; adding a `lint-command.sh --check-convention` mode would duplicate pytest logic in shell with no upside. If a future convention rule emerges that *is* a per-file frontmatter check, the right move is to extend `lint-command.sh`; for now, pytest is the right tool.

## Contract tests

Each test is one shell line or one pytest case. They are the gate.

- `T1` — `grep -c "### Phase-4 Template-Fill Commands" docs/CONVENTIONS.md` returns exactly 1.
- `T2` — `test -f .claude/commands/_meta/command-skeleton.md && [[ $(wc -l < .claude/commands/_meta/command-skeleton.md) -le 120 ]]` (skeleton stays terse).
- `T3` — `test -f .claude/commands/_meta/README.md` (index exists).
- `T4` — `bash tools/lint-command.sh .claude/commands/_meta/command-skeleton.md` exits 0 (the skeleton passes the linter every in-scope command must pass).
- `T5` — `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (the contract test passes; in-scope commands that don't yet exist are auto-skipped per the test's design).
- `T6` — `grep -c "<command-name>" .claude/commands/_meta/command-skeleton.md` returns ≥ 1 (skeleton uses the placeholder verb, not a real verb — by construction not a runnable slash command).
- `T7` — `bash tools/pre-pr.sh` exits 0 (no regression on kit-wide health).
- `T8` — `grep -E "^- \[ \] \*\*P4\.(1|3|4|5|6|8|11)\*\*" ROADMAP.md | wc -l` returns 7 (the seven in-scope rows still exist and remain unchecked at the time this spec ships).
- `T9` — `grep -c "phase-4-command-convention" ROADMAP.md` returns ≥ 1 (the cross-reference was added to the Phase 4 block per Outputs item 6).
- `T10` — `grep -c "phase-4-command-convention" docs/CONVENTIONS.md` returns 0 (the convention text does not self-reference this spec slug — it references the convention as the canonical home, not the spec; protects against a circular link).
- `T11` — `grep -nE "^# /<command-name>" .claude/commands/_meta/command-skeleton.md` returns exactly 1 (H1 is the documented angle-bracket placeholder).
- `T12` — `test -f docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md` (the per-command spec checklist exists; F4 workers consume it).
- `T12b` — `grep -cE "^- \[ \] " docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md` returns at least 5 (the five rows from §"Outputs" item 5 are present as checklist items — protects against the file being created empty).
- `T13` — `python3 tools/lint-frontmatter.py --all` exits 0 (no regression on default-mode behavior across the existing kit; this spec touches no `delivery/` artifacts).
- `T14` — Convention sub-section appears AFTER the §"Templates — `templates/<slug>.md`" sub-section in `docs/CONVENTIONS.md`. `awk '/^### Templates — \`templates\/<slug>\.md\`/{seen=1} /^### Phase-4 Template-Fill Commands/{if(seen){found=1; exit 0} else exit 1} END{if(!found) exit 1}' docs/CONVENTIONS.md` exits 0. Mirrors F3's T14d positional check. (The END guard catches "neither section present" or "only Templates present" — those leave `found` unset and exit 1.)
- `T15` — Exit code 3 is documented in the convention text. `grep -c "^> - \`3\` — artifact was written but the post-fill linter exited non-zero" docs/CONVENTIONS.md` returns exactly 1 (the four exit-code lines appear under the same quoted-section).

## Non-goals

- Authoring any of the seven in-scope commands themselves. Those are separate specs (cmd-draft-vision, cmd-draft-initiative, cmd-context-map, cmd-end-to-end-flow, cmd-sequence-initiative, cmd-draft-spec, cmd-handoff-packet) that run in parallel after this one ships.
- Authoring the nine out-of-scope items in Phase 4 (P4.2, P4.7, P4.9, P4.10, P4.12, P4.13, P4.14, P4.15, P4.16). Each gets its own per-item spec. This convention does not constrain their shape.
- A second-tier "analytical command convention" covering P4.2 and P4.9. May or may not emerge as a future spec once those two are scoped; not assumed here.
- A "comms command convention" covering P4.12, P4.13, P4.14. Same — may emerge later.
- Modifying `tools/lint-command.sh` to enforce the convention's H2-section requirement. The contract test is the right home for convention-specific assertions; the generic linter stays generic.
- Adding a `tools/new-command.sh` scaffolder analogous to `tools/new-spec.sh`. Convenience tooling; deferable. Surfaced as Open Question 5.
- Modifying any of the seven F3.x templates the in-scope commands consume. Templates are frozen by their own F3.x specs as of 2026-05-22; the commands wrap them, they don't change them.
- Touching `tools/lint-frontmatter.py`. The default-mode behavior across `delivery/` is what the commands rely on; no changes needed.

## Open questions

1. **Should `--dry-run` be in the argv contract?** A `--dry-run` flag would let a human preview the artifact Claude would write before committing it to disk. _Resolved here: no, defer. The interactive walk already serves as a preview — the human sees and confirms each section before the file is written. Add `--dry-run` only if adopters request batch / non-interactive use; track as a separate ROADMAP candidate (Phase-4 polish, not blocker)._
2. **Where does `/draft-spec` (P4.8) instantiate to?** _Resolved by reference: `delivery/initiatives/<initiative-slug>/specs/<spec-slug>/`, per `template-authoring-convention` OQ2 (shipped 2026-05-22). P4.8's per-command spec cites this resolution. If a Phase-4 fan-out worker disagrees, it surfaces as a finding in their own adversarial review and we reconcile then._
3. **Should `/handoff-packet` (P4.11) chain into `/audit-completeness <slug>` or into a TBD `/handoff-packet-finalize` command?** _Resolved here: chain into `/audit-completeness <slug>`. `/audit-completeness` is shipped (prose-procedure, plus the F1.5 script); it is the natural Phase-4 exit and Phase-5 entry. The packet README's four `*_review_passed:` audit-gate fields imply running `/audit-completeness` plus the two reviewer subagents next; the chain hint surfaces the audit explicitly, and the per-command spec can name the reviewer-subagent steps in `## What this command will not do` (it doesn't auto-run reviewers; the human does)._
4. **Should `/draft-initiative` (P4.3) auto-invoke `/context-map`, `/end-to-end-flow`, `/sequence-initiative` after scaffolding the folder, or stop and let the human run them separately?** _Resolved here: stop and let the human run them separately. F3.7 ships the folder template with placeholder children; `/draft-initiative` instantiates the folder (Step 2) and fills the README's interactive sections (Step 3); the three child-filling commands run independently afterwards because each requires its own focused interactive walk (the bounded-context list is a different conversation than the Mermaid flow which is a different conversation than the sequencing DAG). The `/draft-initiative` NEXT line names `/context-map <slug>` as the immediate next step; `/context-map`'s NEXT names `/end-to-end-flow`; `/end-to-end-flow`'s NEXT names `/sequence-initiative`; `/sequence-initiative`'s NEXT names `/draft-spec <first-spec-slug>` (or `/handoff-packet <slug>` if the initiative has only one spec already drafted)._
5. **Ship `tools/new-command.sh` alongside the skeleton?** _Resolved here: no, defer. Seven F4 workers each `cp .claude/commands/_meta/command-skeleton.md .claude/commands/<verb>.md` manually; convenience tooling is justified only when adopters start authoring commands outside the P4 fan-out. Track as a separate ROADMAP candidate._
6. **`--from <parent-slug>` argument: positional or flag?** _Resolved here: flag. Positional after `<slug>` (i.e., `<slug> <parent-slug>`) is ambiguous against the future possibility of multiple positional args; the flag form is unambiguous and self-documenting in `argument-hint:`. The cost is two extra characters at the command line._
7. **Auto-pick when only one candidate parent exists?** _Resolved here: no — always confirm, even when only one candidate exists. The confirmation cost is one keystroke; the silent-failure cost when the one candidate turns out to be the wrong one (e.g., stale, superseded by an in-flight one not yet on disk) is high. Restated in the convention text under "Parent-artifact resolution"._
8. **What if a per-command spec needs to *deviate* from the convention** (e.g., a command needs two positional args, or needs to write to two destinations)? _Resolved here: the deviation is documented explicitly in the per-command spec's `Constrained by:` block as "deviates from `phase-4-command-convention` §X for reason Y", surfaced in the per-command adversarial review, and — if the deviation seems likely to recur — proposed as a convention amendment via a follow-up edit to this spec. Quiet deviations are forbidden by the work-loop's "drift is a bug" rule. The `## Boundaries → Never do` line "treat any of the seven commands as convention-exempt inside this spec" formalizes this._

## Acceptance criteria

- [ ] `docs/CONVENTIONS.md` gains the §"Phase-4 Template-Fill Commands — `.claude/commands/draft-*.md` and siblings" sub-section with the exact body in §"Convention-text contract."
- [ ] `.claude/commands/_meta/command-skeleton.md` exists, matches the §"Skeleton-text contract" body, is ≤ 120 body lines, and passes `tools/lint-command.sh`.
- [ ] `.claude/commands/_meta/README.md` exists, points to the skeleton and the convention, and carries no YAML frontmatter.
- [ ] `scripts/tests/test_phase4_command_shape.py` exists and implements the eight test cases enumerated in §"Outputs" item 4. Module-level `INSCOPE` constant lists the seven verb names. Test passes (auto-skipping the not-yet-shipped commands).
- [ ] `docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md` exists with the five-row checklist enumerated in §"Outputs" item 5.
- [ ] `ROADMAP.md` Phase 4 block has the one-line cross-reference; no checkboxes flipped.
- [ ] All contract tests pass: T1–T15 (T14 = sub-section placement after F3 Templates; T15 = exit-code 3 documented).
- [ ] No new ontology type added; no out-of-scope ROADMAP rows edited; no F3.x template modified; no existing slash command modified; no `tools/` script modified.

## Cross-references

- **Consumed by:** P4.1 (cmd-draft-vision), P4.3 (cmd-draft-initiative), P4.4 (cmd-context-map), P4.5 (cmd-end-to-end-flow), P4.6 (cmd-sequence-initiative), P4.8 (cmd-draft-spec), P4.11 (cmd-handoff-packet). Any future template-fill command in Phase 4 that adopters propose.
- **Consumes:** `docs/CONVENTIONS.md`, `docs/HANDOVERS.md`, `tools/lint-command.sh`, `tools/lint-frontmatter.py`, the seven F3.x templates (F3.6, F3.7, F3.8, F3.9), `docs/specs/template-authoring-convention/spec.md`, `.claude/skills/work-loop/SKILL.md`, `.claude/CLAUDE.md`.
- **Frontmatter fields owned:** none directly; specifies the argv contract for the `argument-hint:` field of in-scope commands.
- **Ontology object types touched:** none directly; the seven commands instantiate Vision (Domain D), Initiative (Domain D), Context Map (Domain G), Business Workflow / Flow (Domain G), Sequence / Initiative Plan (Domain D/G), PM Spec (Domain E composite), Handoff Packet (Domain H composite). All seven types already exist in the ontology.
