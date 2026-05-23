# Spec: cmd-draft-initiative

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** slash command
- **Serves kit phase:** Delivery
- **Constrained by:** [`docs/specs/phase-4-command-convention/spec.md`](../phase-4-command-convention/spec.md) (parent convention — body structure, argv contract, parent-resolution rule, interactive-fill behavior, pre-fill rules, linter integration, exit codes, chaining hint); `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" (the boundary contract this command gates — folder contents, README frontmatter superset, per-child required content); `templates/initiative/` (F3.7 folder template, shipped 2026-05-22 — this command instantiates); [`docs/specs/template-initiative/spec.md`](../template-initiative/spec.md) (F3.7 sibling — folder layout and per-child frontmatter resolution); `tools/lint-frontmatter.py` (default-mode linter run post-fill against the README); `tools/lint-command.sh` (shape linter for `.claude/commands/*.md`); [`.claude/skills/work-loop/SKILL.md`](../../../.claude/skills/work-loop/SKILL.md) (the build pattern this command's own development follows).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Defines `/draft-initiative <slug>` — the artifact-creating Phase-4 template-fill command that gates **Handover 5 (Initiative → Spec)**. The command reads a parent Vision, `cp -r`'s `templates/initiative/` into `delivery/initiatives/<slug>/`, walks the README's H2 placeholders interactively (one section at a time, one question at a time), pre-fills the mechanical frontmatter (`id: INIT-<NNN>`, `slug`, `created`, `last_updated`, `parent_vision`, `object_type: Initiative`), surfaces `human_owned_decisions:` for human confirmation, lints the written README in default mode, and emits `NEXT: /context-map <slug>`. The five child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) are copied verbatim from the template and **left in placeholder state** — they are filled later by `/context-map` (P4.4), `/end-to-end-flow` (P4.5), `/sequence-initiative` (P4.6), and incidentally by `/draft-spec` (P4.8, which appends to `child-specs.md`). `capabilities.md` is populated incidentally as the README walk reaches the README's Capability-list frontmatter pre-fill (see §"Per-section interactive prompts" below).

## Objective

`/draft-initiative <slug>` collapses the multi-step Initiative bootstrap (find the parent Vision; `mkdir delivery/initiatives/<slug>/`; `cp -r templates/initiative/*` into it; resolve the `id:` against the ontology's `INIT-<NNN>` prefix; pre-fill seven mechanical frontmatter fields; walk the README's three required H2s plus the optional risk-register H3; cite the parent Vision; confirm the three HANDOVERS-5 `human_owned_decisions:` strings; run default-mode `lint-frontmatter.py` on the README; emit the next-command hint) into one slash command with a single positional argument. It is the Handover-4-to-Handover-5 transition the kit currently leaves to human discipline. The command is the third in a seven-command Phase-4 chain (`/draft-vision` → **`/draft-initiative`** → `/context-map` → `/end-to-end-flow` → `/sequence-initiative` → `/draft-spec` → `/handoff-packet`); each command's NEXT line points at the immediate successor.

## Why now

ROADMAP P4.3 (`/draft-initiative`). The convention parent (`docs/specs/phase-4-command-convention/`) shipped 2026-05-23, fixing the body shape, the argv contract, the parent-resolution rule, the exit-code set, and the chaining-hint format that every in-scope Phase-4 command must follow. F3.7 (`templates/initiative/`) shipped 2026-05-22, fixing the folder layout this command instantiates — six files (`README.md`, `context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) — and the README frontmatter superset (universal-metadata schema + HANDOVERS-5 block). F3.8 (`templates/pm-spec.md`) and F3.9 (`templates/handoff-packet/`) also shipped on the same date, so the downstream chain (P4.8 `/draft-spec` and P4.11 `/handoff-packet`) has stable contract surfaces to point at. With the convention locked and all relevant F3.x templates frozen, `/draft-initiative` is unblocked. Until it ships, every initiative bootstrap is a manual `cp -r` plus seven mechanical pre-fills plus three human confirmations — exactly the surface this command exists to mechanize.

## Inputs and outputs

**Inputs.**

1. **Positional argument** — `<slug>`: the new Initiative's slug. Kebab-case (`^[a-z0-9-]+$`), ≤ 80 chars. Names both the destination folder (`delivery/initiatives/<slug>/`) and the value pre-filled into the README's `slug:` frontmatter field.
2. **Template folder** — `templates/initiative/` (F3.7, shipped 2026-05-22): a folder template containing six files: `README.md` (carries universal-metadata + HANDOVERS-5 frontmatter, three required H2s plus an optional H2/H3 pair for cross-team risk-register), `context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md` (the five narrative children carry no frontmatter).
3. **Parent artifact** — a Vision from `delivery/visions/<vision-slug>.md`. Resolution rule below. Pre-fills the README's `parent_vision:` frontmatter field. Also pre-fills `parent_intent:` from the Vision's own `parent_intent:` (transitive carry-through, since the universal-schema traceability block retains both fields per F3.7's Always-do "traceability field retention" rule).
4. **Optional flags** — `--from <vision-slug>` (explicit parent selection; overrides auto-detection); `--force` (permit overwriting an existing `delivery/initiatives/<slug>/` folder).

**Parent-resolution rule.** Candidates are read from `delivery/visions/*.md`, filtered to those whose `status:` is **not** in the terminal-or-killed set `{Deprecated}` (per the convention's "Parent-artifact resolution" rule applied to the Vision lifecycle — Vision uses the universal-schema lifecycle enum from `docs/CONVENTIONS.md` §"Lifecycle states", and `Deprecated` is the terminal value for product-track artifacts in that enum). If `--from <vision-slug>` is supplied, the command uses that slug directly (and exits code 2 if the Vision is missing or has `status: Deprecated`). Otherwise the command lists the filtered candidates, sorted by `last_updated:` descending, capped at 10. **Always confirm even when only one candidate exists** (per the convention's Open Question 7 resolution). If the candidate list is empty after filtering, exit code 2 with the remediation message: `no Vision found in delivery/visions/ with non-Deprecated status — run /draft-vision first`. Never silently pick.

**Outputs.**

A new folder `delivery/initiatives/<slug>/` containing:

- `README.md` — instantiated from `templates/initiative/README.md`. Frontmatter pre-filled mechanically (see §"Pre-fill rules") and human-filled interactively (see §"Per-section interactive prompts"). Passes `python3 tools/lint-frontmatter.py delivery/initiatives/<slug>/README.md` in default mode.
- `context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md` — **copied verbatim from `templates/initiative/`** and left in placeholder state (containing their `<placeholder>` markers, Mermaid placeholder blocks, and per-section template H3 stubs as shipped by F3.7). Filled later by their respective augmenting commands.

Plus stdout: a per-section walkthrough transcript (the questions asked and the human's answers), the linter result, and a final `NEXT: /context-map <slug>` hint line.

**Exit codes** (per convention §"Exit codes"):

- `0` — folder created, README filled and linted clean, NEXT hint emitted.
- `1` — human aborted the interactive walk before completion. Folder may exist on disk in partial state; command emits "resume by re-running `/draft-initiative <slug>` with the same slug".
- `2` — pre-conditions failed: no Vision in `delivery/visions/` after status filter, `<slug>` malformed, `delivery/initiatives/<slug>/` already exists without `--force`, `templates/initiative/` missing, `--from <vision-slug>` names a missing or `Deprecated` Vision.
- `3` — folder created and README written but `lint-frontmatter.py` exited non-zero against the README; human declined to re-open the relevant sections (or re-opened them but the re-lint still failed). Folder persists on disk in a known-imperfect state.

No other exit codes.

## Body-shape contract

The command file `.claude/commands/draft-initiative.md` follows `.claude/commands/_meta/command-skeleton.md` verbatim in body structure: H1 `# /draft-initiative`, blockquote orientation paragraph, then H2 sections in order — `## When to run`, `## Inputs`, `## Procedure` (with six Step-N H3 sub-sections matching the skeleton), `## What this command will not do`. Per the convention, the frontmatter carries `description:` (≤ 1024 chars) and `argument-hint: <slug> [--from <vision-slug>] [--force]` (artifact-creating positional form). No other frontmatter keys.

## Per-section interactive prompts

The README walk is the only interactive surface. The five child files are **not** walked by this command; they are copied verbatim and surface their placeholder content to the augmenting commands that fill them. The README has these H2 sections (per `templates/initiative/README.md` as shipped by F3.7):

1. `## What this initiative is` (required; H2)
2. `## Scope and bounded contexts` (required; H2; pointer prose)
3. `## Delivery sequencing` (required; H2; pointer prose)
4. `## Optional sections` (header-only H2; the section under it is optional and can be deleted)
5. `### Cross-team risk register` (optional H3 under `## Optional sections`)

Per-H2 prompts (the human-facing copy the command emits, verbatim — one question at a time, never batched):

**Section 1 — `## What this initiative is` (one question, asked sequentially):**

> "Restate the parent Vision (`<parent_vision-slug>`)'s `change:` field in one paragraph, scoped to what this Initiative delivers. Cite the parent Vision's slug inline. What does this Initiative deliver that the Vision promised? (One paragraph; do not list scope or sequencing — those come later.)"

**Section 2 — `## Scope and bounded contexts` (one question, then the Capability-list incidental walk):**

> "Name the bounded contexts this Initiative crosses, in one paragraph. The full per-context detail (owner, public contract, Wardley evaluation, evolution stage) will be filled by `/context-map <slug>` later — for this paragraph, name only the contexts and their roles."

After confirming the prose, the command incidentally walks the README's `capabilities:` frontmatter list (which is otherwise mechanically pre-filled to `[]`):

> "List the Capability ids (`CAP-NNN`) this Initiative requires. If you don't yet have Capability ids assigned, give the human-readable names — the command will leave the `capabilities:` frontmatter list empty and add a `TODO` comment naming the capabilities you listed, for the Capability-registry assignment to happen separately. (The Capability rows themselves go into `capabilities.md` later; this prompt only fills the README's machine-readable list.)"

This Capability-list walk is the **incidental population** mentioned in the convention's "Capabilities-file interstitial" rule — the README's `capabilities:` list is the machine-readable source per F3.7; `capabilities.md` itself remains in placeholder state until the human (or a future Capability-registry command) populates it.

**Section 3 — `## Delivery sequencing` (one question):**

> "Name the first-shippable subset and the dependency-driving spec in one paragraph. The full child-spec manifest goes into `child-specs.md` (populated by `/draft-spec` later); the dependency DAG goes into `sequence.md` (populated by `/sequence-initiative` later). For this paragraph, name only the headline subset and the spec that must ship first."

**Section 4 — `## Optional sections` / `### Cross-team risk register` (gating question, then conditional fill):**

> "Does this Initiative carry cross-team risks worth registering up-front? (yes / no — if no, the `## Optional sections` H2 and its `### Cross-team risk register` H3 will be deleted from the README per the template's deletion instruction.)"

If `yes`, follow up:

> "Name each cross-team risk in one line: who owns it, what would trigger it, what the mitigation is. One bullet per risk. The full risk register may live elsewhere (e.g., a Domain F Risk artifact); for the README this is a short call-out so reviewers know the risk is on the radar."

If `no`, the command deletes the `## Optional sections` H2 line and the entire `### Cross-team risk register` subtree (the H3 and its body placeholder) from the written README, leaving the README ending at `## Delivery sequencing`.

**Section 5 — `human_owned_decisions:` confirmation (Step 4 of the convention's procedure; per HANDOVERS-5 the three strings are pre-filled):**

For each of the three HANDOVERS-5 strings — `Bounded-context ownership assignment`, `Build vs buy decisions in the evolution check`, `Delivery sequencing` — the command asks (sequentially, never batched):

> "Confirm: do you accept ownership of the decision **`<decision-string>`** for this Initiative? (yes / no — if no, name who owns it instead; the answer is recorded in `approvals_obtained:`.)"

The command writes the resulting `approvals_obtained:` block in the universal-schema inline-list form: `approvals_obtained: ["<role-or-name>: <YYYY-MM-DD>", ...]`.

## Pre-fill rules

Per the convention's "Pre-fill rules" section, the command pre-fills the following README frontmatter fields **before** asking the human anything:

- `id: INIT-<NNN>` — derived from the ontology's Initiative prefix (`INIT-`) plus the next unused integer scanning `delivery/initiatives/*/README.md` for existing `^id: INIT-(\d+)$` and taking `max + 1` (or `001` if none exist). Zero-padded to three digits.
- `slug: <slug>` — the positional argument.
- `object_type: Initiative` — re-asserted (template already pre-fills this; defensive check).
- `created: <YYYY-MM-DD>` — today's date from the system clock at command start.
- `last_updated: <YYYY-MM-DD>` — same as `created`.
- `parent_vision: <resolved-vision-slug>` — from the parent-resolution step.
- `parent_intent: <vision's parent_intent value>` — transitive carry-through; read from the parent Vision's frontmatter.
- `capabilities: []` — empty list. **Not pre-filled with concrete ids.** The list is populated incidentally during the Section-2 interactive walk; if the human supplies no concrete ids, the list stays empty and the README body carries the names as a TODO comment (see Section-2 prompt above).

The command does **not** pre-fill any other frontmatter field. The human is never asked to type any of the pre-filled mechanical fields — they are written before the interactive walk begins.

## Folder-template specifics

`/draft-initiative` is the only Phase-4 command (besides `/handoff-packet`) that instantiates a **folder template** rather than a single file. The relevant rules:

- **`cp -r`, not `cp`.** Step 2 of the procedure copies the entire `templates/initiative/` folder to `delivery/initiatives/<slug>/`. The five child files are copied verbatim — bytes-identical to the template — and left in placeholder state. They are NOT walked, NOT pre-filled, and NOT modified by `/draft-initiative` beyond the `cp -r` itself.
- **Augmenting-command surface.** The five child files exist in placeholder state explicitly so that `/context-map <slug>` (P4.4), `/end-to-end-flow <slug>` (P4.5), and `/sequence-initiative <slug>` (P4.6) can find their target child files in a predictable location and walk them in-place. Without the `cp -r`, those three commands would have to create the child files themselves, duplicating the F3.7 template content in three places.
- **`child-specs.md` and `capabilities.md` have no dedicated P4.x command.** They are filled incidentally: `child-specs.md` is appended to by `/draft-spec` (P4.8) when a child spec is created (the table grows one row per `/draft-spec` invocation); `capabilities.md` is populated by the human (or a future Capability-registry command) using the names captured in Section 2 above as a starting point.

## Linter integration

After the interactive walk completes (Step 5 of the convention procedure), the command runs `python3 <repo-root>/tools/lint-frontmatter.py delivery/initiatives/<slug>/README.md` in **default mode** (not `--check-template`). The README is now a real product artifact under `delivery/`, which is in the default-mode `PHASE_DIRS` list.

**The lint covers `README.md` only.** The five child placeholder files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) are template-shaped — they contain `<placeholder>` markers, Mermaid placeholder identifiers, and per-section H3 stubs that would fail default-mode linting if visited. This is intentional and load-bearing: F3.7's spec resolves the per-child-frontmatter question (OQ4) by giving the five files **no frontmatter at all**, which means `lint-frontmatter.py` in default mode (which walks `PHASE_DIRS` and validates YAML-frontmatter on files that have it) treats the five children as prose-only files and does not raise on them. The linter's default-mode pass therefore exits 0 over the whole folder even though the five children remain in placeholder state.

The lint after `/draft-initiative` **covers `README.md` only**; the five child files are linted by their respective augmenting commands after they fill them: `/context-map` lints `context-map.md`, `/end-to-end-flow` lints `flow.md`, `/sequence-initiative` lints `sequence.md`, and `/draft-spec` lints whatever it touches in `child-specs.md`. `capabilities.md` is linted by whichever command first writes substantive content to it (out of scope for `/draft-initiative`).

If `lint-frontmatter.py` exits non-zero on the README:

- The command surfaces the linter's stderr to the human.
- The command offers to re-open the relevant README sections (whichever sections own the failing fields) for correction.
- If the human accepts and the re-fill lints clean on re-run, the command exits 0 normally.
- If the human declines (or re-fills but the lint still fails), the command exits 3 with the linter output surfaced and the folder left on disk in a known-imperfect state.

## Chaining hint

Last line of stdout, formatted exactly:

```
NEXT: /context-map <slug>
```

Where `<slug>` is the Initiative slug just created. `/context-map` is the augmenting command that fills `context-map.md`; per the convention's chain `/draft-initiative` → `/context-map` → `/end-to-end-flow` → `/sequence-initiative` → `/draft-spec` → `/handoff-packet`, `/context-map` is the immediate next step.

The command does **not** emit a `REVIEW:` line — the `REVIEW: delivery/initiatives/<slug>/capabilities.md — verify the Capability list is filled and each row traces to a parent Problem before running /draft-spec.` line is `/sequence-initiative`'s responsibility per the convention's "Capabilities-file interstitial" rule.

If `/context-map` is not yet shipped at the time `/draft-initiative` runs, the NEXT line is `NEXT: /context-map <slug> (planned — ROADMAP P4.4)` per the kit-drift policy.

## Boundaries

### Always do

- Follow the parent convention's body shape, argv contract, parent-resolution rule, pre-fill rules, linter integration, and exit-code set verbatim. Any deviation is documented explicitly here as "deviates from `phase-4-command-convention` §X for reason Y".
- `cp -r templates/initiative/` to `delivery/initiatives/<slug>/` — copy the whole folder, including the five placeholder children, before the interactive walk begins.
- Pre-fill `id: INIT-<NNN>` by scanning `delivery/initiatives/*/README.md` for the highest existing `INIT-` integer and taking `max + 1` (zero-padded to three digits). If no initiatives exist, use `INIT-001`.
- Pre-fill `parent_intent:` transitively from the resolved parent Vision's `parent_intent:` field. This carries the upstream traceability chain through the README's universal-schema traceability block without asking the human.
- Walk the README's H2s one at a time, in source order, asking one question per placeholder per section. Never batch questions across sections; never batch across H3 sub-sections within a section.
- Surface the three HANDOVERS-5 `human_owned_decisions:` strings (`Bounded-context ownership assignment`, `Build vs buy decisions in the evolution check`, `Delivery sequencing`) for individual confirmation before exiting. Record the confirmations in `approvals_obtained:`.
- Run `lint-frontmatter.py` in default mode against the written README before declaring success. Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`; do not assume the working directory is the repo root.
- Emit `NEXT: /context-map <slug>` as the last line of stdout on exit 0.

### Ask first

- Pre-filling the README's `capabilities:` list with concrete `CAP-NNN` ids without an explicit Capability-registry source. The default behavior is to leave the list empty and add a TODO comment in the README body naming the human-readable Capability names the human supplied during the Section-2 walk; pre-filling concrete ids implies a registry lookup that this command does not implement.
- Walking any of the five child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) interactively. Each child has its own augmenting command (or, for `child-specs.md`/`capabilities.md`, an incidental fill path); walking them here would duplicate scope and break the chain.
- Treating `--from <vision-slug>` as anything other than an exact-match selector against `delivery/visions/*.md` filenames. Fuzzy matching, partial slugs, or globs are out of scope; the human supplies the exact slug or chooses from the auto-detected candidate list.

### Never do

- Write an Initiative when the chosen parent Vision's `status:` is `Deprecated`. The parent-resolution step's status filter excludes `Deprecated` from the candidate list; `--from <vision-slug>` against a `Deprecated` Vision exits code 2 with the remediation suggestion to revive the Vision via a status update or pick a different parent.
- Pre-fill the `capabilities:` list with concrete values. Populate the list incidentally during the README walk (Section 2); if the human supplies names but no `CAP-NNN` ids, leave the list empty and capture the names as a TODO comment in the README body for separate Capability-registry assignment.
- Silently pick a parent Vision when multiple candidates exist (or when only one candidate exists — the convention's "always confirm" rule applies per Open Question 7 of the parent spec).
- Overwrite an existing `delivery/initiatives/<slug>/` folder without `--force`. If the destination exists and `--force` is not set, exit code 2 with the remediation suggestion to re-run with `--force` or pick a different slug.
- Modify, walk, lint, or pre-fill any of the five child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) beyond the `cp -r` itself. They are left in placeholder state for the augmenting commands.
- Add a frontmatter key to the README not present in either the universal-metadata schema or HANDOVERS-5's Handover-5 frontmatter block. The README's frontmatter superset is pinned by F3.7's spec; adding a key would silently bypass `template-initiative`'s contract.
- Modify `templates/initiative/` or any of its child files. The template is frozen by F3.7's spec; this command consumes the template by copy, not by reference.
- Run `lint-frontmatter.py` against any of the five child files. They are intentionally in placeholder state until their augmenting commands fill them; linting them here would surface false-positive failures on every `/draft-initiative` run.
- Auto-invoke `/context-map`, `/end-to-end-flow`, `/sequence-initiative`, or any other downstream command. Per parent spec Open Question 4 (resolved), the human runs each command separately. `/draft-initiative`'s NEXT line names `/context-map <slug>` as the immediate next step; the human decides when to run it.

## Verification mode

- **Goal-based check** for the command's body shape: `tools/lint-command.sh .claude/commands/draft-initiative.md` exits 0; the body matches the skeleton verbatim in H2 structure; the `argument-hint:` frontmatter is the literal `<slug> [--from <vision-slug>] [--force]` form. The convention's contract test `scripts/tests/test_phase4_command_shape.py` auto-detects the command once it lands and asserts H2 presence, argv form, template-path existence, and destination-path existence.
- **Manual gesture** for the interactive walk: against a fixture parent Vision under `delivery/visions/<fixture-slug>.md`, run `claude` and execute `/draft-initiative <fixture-initiative-slug>`; confirm the per-section prompts emit in source order, the `human_owned_decisions:` confirmation surfaces all three HANDOVERS-5 strings, the linter runs default-mode against the README only, and the NEXT line emits exactly `NEXT: /context-map <fixture-initiative-slug>`. The fixture is checked in under `docs/specs/cmd-draft-initiative/notes/manual-gesture-fixture.md`.
- **Audit-driven** for kit-wide health: `tools/pre-pr.sh` exits 0 after the command lands; `python3 tools/lint-frontmatter.py --all` exits 0 (the command modifies no existing product artifacts under `delivery/`, so default-mode coverage is unchanged); `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (auto-tightening from skipped to active for the `draft-initiative` row).

## Contract tests

Each test is one shell line or one pytest assertion. They are the gate.

- `T1` — `.claude/commands/draft-initiative.md` exists. `test -f .claude/commands/draft-initiative.md`.
- `T2` — `bash tools/lint-command.sh .claude/commands/draft-initiative.md` exits 0.
- `T3` — The command file has all four convention-required H2 sections: `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`. Asserted by `scripts/tests/test_phase4_command_shape.py::test_inscope_commands_have_required_h2s` (auto-tightens once the file exists).
- `T4` — `argument-hint:` frontmatter value matches the artifact-creating positional form: starts with the literal `<slug>` token. Asserted by `test_inscope_commands_declare_argv` against `POSITIONAL["draft-initiative"] == "<slug>"`.
- `T5` — Command body cites the template path `templates/initiative/` and the path exists. Asserted by `test_inscope_commands_cite_template_path` (regex permits the trailing slash on folder templates).
- `T6` — Command body cites the destination path under `delivery/` and the family directory `delivery/initiatives/` exists. Asserted by `test_inscope_commands_cite_destination_path`.
- `T7` — Procedure body's six Step-N sub-sections appear in order: Step 1 (resolve parent), Step 2 (instantiate template), Step 3 (walk placeholders one section at a time), Step 4 (surface human-owned decisions), Step 5 (lint), Step 6 (emit NEXT hint). Asserted by a grep-with-line-numbers monotonicity check.
- `T8` — Exit-code documentation matches the convention's four-code set (0, 1, 2, 3) exactly. No extras. Asserted by `grep -cE '^\- \`[0-3]\`' .claude/commands/draft-initiative.md` returning exactly 4.
- `T9` — Manual-gesture fixture exists: `test -f docs/specs/cmd-draft-initiative/notes/manual-gesture-fixture.md`.
- `T10` — `bash tools/pre-pr.sh` exits 0.
- `T11` — `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0.
- `T12` — Command's NEXT line in the documented procedure is exactly `NEXT: /context-map <slug>` (or with the `(planned — ROADMAP P4.4)` suffix if P4.4 is unshipped at the time `/draft-initiative` lands). Asserted by `grep -E 'NEXT: /context-map' .claude/commands/draft-initiative.md` returning ≥ 1.
- `T13` — Command body does NOT emit a `REVIEW:` line (that is `/sequence-initiative`'s responsibility per the convention's Capabilities-file interstitial rule). Asserted by `grep -c '^REVIEW:' .claude/commands/draft-initiative.md` returning 0.

## Non-goals

- Authoring `/context-map`, `/end-to-end-flow`, `/sequence-initiative`, `/draft-spec`, or `/handoff-packet`. Each is its own per-command spec in the F4 fan-out.
- Walking, modifying, linting, or pre-filling any of the five child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) beyond the `cp -r` copy from the template.
- Auto-invoking downstream commands. Per parent spec OQ4 (resolved), the chain is sequential and human-driven; `/draft-initiative` emits a single NEXT hint, not a triple.
- Modifying `templates/initiative/` or any other F3.x template. Templates are frozen as of 2026-05-22.
- Modifying `tools/lint-frontmatter.py`, `tools/lint-command.sh`, or any other kit script. The command is a consumer of these scripts, not a modifier.
- Implementing a Capability-registry lookup that would resolve human-readable names to `CAP-NNN` ids during the Section-2 walk. The list stays empty when no ids are supplied; the names are captured as a TODO comment for separate resolution.
- Resolving the universal-lifecycle-vs-HANDOVERS-5-`active|paused|done` enum mismatch on `status:` (F3.7 OQ1). The command writes the HANDOVERS-5-pinned value (`active` on first instantiation, per the human's confirmation); if the default-mode linter fails on the value, the command exits code 3 and surfaces the failure — but it does not edit the linter or the convention to resolve the mismatch.
- Implementing a `--dry-run` flag. Deferred per parent convention Open Question 1.
- Implementing `tools/new-command.sh` or any command-scaffolder. Deferred per parent convention Open Question 5.

## Open questions

1. **Should `/draft-initiative` auto-emit a triple `NEXT:` block naming `/context-map`, `/end-to-end-flow`, and `/sequence-initiative` together?** Resolved by parent spec Open Question 4 (resolved): no. The chain is sequential and human-driven; each command's NEXT line points only at the immediate next step. `/draft-initiative` → `/context-map`; `/context-map` → `/end-to-end-flow`; `/end-to-end-flow` → `/sequence-initiative`; `/sequence-initiative` → `/draft-spec` (or `/handoff-packet`).
2. **How should the command handle a parent Vision whose `status:` is missing or malformed?** Treat as if the Vision were `Deprecated` for filtering purposes — exclude from the candidate list, exit code 2 if `--from` names it, surface the malformed-status as the reason. Defensive default; revisit if any kit user reports the behavior is wrong.
3. **What if the human supplies a Capability name during the Section-2 walk that already exists as a `CAP-NNN` id elsewhere in the kit?** Out of scope for this command. The Section-2 walk captures names as a TODO comment; reconciliation against an existing Capability registry is a separate command (likely a Capability-registry-management command not yet in ROADMAP). If a future ROADMAP row ships that command, `/draft-initiative` may grow a registry-lookup integration; defer until then.
4. **Should the Section-4 `## Optional sections` / `### Cross-team risk register` deletion behavior leave a YAML comment in the README marking that the section was deleted, or remove all trace?** Resolved here: remove all trace. The template's deletion instruction (`Delete the heading and all unused sections below if none apply.`) is unambiguous; leaving a YAML comment would create a kit-specific convention not present in F3.7's contract. If a kit user later wants to add a risk register, they edit the README directly.

## Acceptance criteria

- [ ] `.claude/commands/draft-initiative.md` exists, follows the convention's body shape, and passes `tools/lint-command.sh`.
- [ ] The command's `argument-hint:` frontmatter is exactly `<slug> [--from <vision-slug>] [--force]`.
- [ ] The command body cites `templates/initiative/` as the consumed template and `delivery/initiatives/<slug>/` as the destination.
- [ ] The command body documents the six Step-N procedure sub-sections in convention order.
- [ ] The command body documents the four exit codes (0, 1, 2, 3) verbatim from the convention.
- [ ] The command body emits `NEXT: /context-map <slug>` as its chaining hint and does NOT emit a `REVIEW:` line.
- [ ] `scripts/tests/test_phase4_command_shape.py` exits 0 with the `draft-initiative` row tightened from skipped to active.
- [ ] `tools/pre-pr.sh` exits 0.
- [ ] Manual-gesture fixture under `docs/specs/cmd-draft-initiative/notes/manual-gesture-fixture.md` is checked in and the fixture run produces the expected folder and NEXT line.
- [ ] No new ontology type added; `templates/initiative/` unmodified; no other F3.x template touched; no `tools/` script modified.

## Cross-references

- **Consumed by:** kit users running `/draft-initiative` to bootstrap an Initiative; the convention's contract test `scripts/tests/test_phase4_command_shape.py` (which walks `.claude/commands/draft-initiative.md` once it exists); the downstream chain (`/context-map`, `/end-to-end-flow`, `/sequence-initiative`, `/draft-spec`, `/handoff-packet`) which assumes `/draft-initiative` has already produced the folder layout they target.
- **Consumes:** `docs/specs/phase-4-command-convention/spec.md` (the parent convention); `docs/HANDOVERS.md` §"Handover 5"; `templates/initiative/` (F3.7); `docs/specs/template-initiative/spec.md` (sibling spec — folder layout, per-child frontmatter resolution); `tools/lint-frontmatter.py` (default mode, post-fill lint of the README); `tools/lint-command.sh` (shape lint of the command file itself); `.claude/commands/_meta/command-skeleton.md` (the copy source); `.claude/skills/work-loop/SKILL.md` (build pattern).
- **Frontmatter fields owned:** the command pre-fills (at instantiation time, not at the schema level) `id: INIT-<NNN>`, `slug`, `object_type: Initiative`, `created`, `last_updated`, `parent_vision`, `parent_intent`, `capabilities: []` on the README. The README's frontmatter superset (universal-metadata + HANDOVERS-5) is owned by F3.7's spec; this command consumes that superset by reference.
- **Ontology object types touched:** Initiative (Domain D; instantiated by this command via the README's `object_type:` value). Vision (Domain D; referenced as the parent via `parent_vision:`). Strategic Intent (Domain D; referenced transitively via `parent_intent:` carried from the parent Vision). Capability (Domain E; referenced via the README's `capabilities:` list — populated incidentally during the Section-2 walk; not instantiated here).
