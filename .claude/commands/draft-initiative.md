---
description: Instantiate the F3.7 folder template at delivery/initiatives/<slug>/ — copy README plus five placeholder children, walk the README's H2 sections interactively, pre-fill mechanical metadata, lint the README, and chain to /context-map.
argument-hint: <slug> [--from <vision-slug>] [--force]
---

# /draft-initiative

> Artifact-creating Phase-4 template-fill command (folder-template sub-case). Reads an active Vision from `delivery/visions/`; `cp -r` the `templates/initiative/` folder to `delivery/initiatives/<slug>/`; walks the README's H2 sections one at a time interactively; leaves the five child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) in placeholder state for the augmenting commands. Gates Handover 5 (Initiative → Spec) by establishing the initiative folder its child specs will live under.

## When to run

- After a Vision has shipped (`status: Active` in `delivery/visions/`) and the team is ready to commit to a cross-team initiative under it.
- Before any of the three augmenting commands (`/context-map`, `/end-to-end-flow`, `/sequence-initiative`) and before `/draft-spec` — all four require the initiative folder to exist.
- When HANDOVERS-5's `delivery/initiatives/<slug>/` is the missing artifact in the Phase-4 chain.

## Inputs

1. The positional arg — `<slug>` (the new Initiative's slug). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars.
2. `templates/initiative/` — the F3.7 folder template this command copies (`cp -r`).
3. Parent artifact: a Vision at `delivery/visions/<vision-slug>.md` whose `status:` is not `Deprecated`. Resolution rule below; `--from <vision-slug>` for explicit selection.
4. Optional flag `--force` — permits overwriting an existing `delivery/initiatives/<slug>/`.

## Procedure

### Step 1 — resolve the parent Vision

If `--from <vision-slug>` is given, verify `delivery/visions/<vision-slug>.md` exists and its `status:` is not `Deprecated`. If either fails, exit code 2 with a remediation message naming the malformed/deprecated slug.

Otherwise list candidate Visions in `delivery/visions/` whose `status:` is not in the terminal-or-killed set `{Deprecated}`. Sort by `last_updated:` descending; cap at 10. Present as a numbered list; ask the human to pick one (or specify `--from` for an older candidate). Never silently pick — always confirm, even when only one candidate exists.

If the candidate list is empty, exit code 2 with: `"no Vision found in delivery/visions/ with status != Deprecated. Run /draft-vision first, then re-run /draft-initiative <slug>."`

### Step 2 — instantiate the folder template

`cp -r templates/initiative/` to `delivery/initiatives/<slug>/`. If the destination already exists and `--force` is not set, exit code 2 with: `"delivery/initiatives/<slug>/ already exists — re-run with --force to overwrite, or pick a different slug."`

The five child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) are copied verbatim and left in placeholder state. They are NOT walked, NOT pre-filled, and NOT modified by this command beyond the `cp -r` itself.

Pre-fill the README's mechanical frontmatter (the human is never asked for these):

- `id: INIT-<NNN>` — scan `delivery/initiatives/*/README.md` for `^id: INIT-(\d+)$`, take max + 1, zero-pad to three digits (or `001` if none exist).
- `slug:` — the positional argument.
- `object_type: Initiative` — re-assert (template already pre-fills; defensive check).
- `created:` — today's date (ISO-8601, system clock at command start).
- `last_updated:` — same as `created`.
- `parent_vision:` — the resolved Vision slug from Step 1.
- `parent_intent:` — read from the parent Vision's `parent_intent:` field (transitive carry-through).
- `capabilities:` — empty list `[]`. **Not pre-filled with concrete ids.** The list is populated incidentally during the Section-2 walk; if the human supplies no concrete ids, the list stays empty and the README body carries the names as a TODO comment.

### Step 3 — walk the README's H2 sections one at a time

Walk these prompts in source order. One question per turn. Never batch. Confirm the section's filled content before advancing.

**Section 1 — `## What this initiative is`.** _"Restate the parent Vision (`<parent_vision-slug>`)'s `change:` field in one paragraph, scoped to what this Initiative delivers. Cite the parent Vision's slug inline. What does this Initiative deliver that the Vision promised? (One paragraph; do not list scope or sequencing — those come later.)"_

**Section 2 — `## Scope and bounded contexts`.** First, the prose prompt: _"Name the bounded contexts this Initiative crosses, in one paragraph. The full per-context detail (owner, public contract, Wardley evaluation, evolution stage) will be filled by `/context-map <slug>` later — for this paragraph, name only the contexts and their roles."_

Then the incidental Capability-list walk: _"List the Capability ids (`CAP-NNN`) this Initiative requires. If you don't yet have Capability ids assigned, give the human-readable names — the command will leave the `capabilities:` frontmatter list empty and add a `TODO` comment naming the capabilities you listed, for the Capability-registry assignment to happen separately. (The Capability rows themselves go into `capabilities.md` later; this prompt only fills the README's machine-readable list.)"_

**Section 3 — `## Delivery sequencing`.** _"Name the first-shippable subset and the dependency-driving spec in one paragraph. The full child-spec manifest goes into `child-specs.md` (populated by `/draft-spec` later); the dependency DAG goes into `sequence.md` (populated by `/sequence-initiative` later). For this paragraph, name only the headline subset and the spec that must ship first."_

**Section 4 — `## Optional sections` / `### Cross-team risk register`.** Gating question: _"Does this Initiative carry cross-team risks worth registering up-front? (yes / no — if no, the `## Optional sections` H2 and its `### Cross-team risk register` H3 will be deleted from the README per the template's deletion instruction.)"_

If `yes`: _"Name each cross-team risk in one line: who owns it, what would trigger it, what the mitigation is. One bullet per risk. The full risk register may live elsewhere (e.g., a Domain F Risk artifact); for the README this is a short call-out so reviewers know the risk is on the radar."_

If `no`, delete the `## Optional sections` H2 and the entire `### Cross-team risk register` subtree from the written README.

### Step 4 — surface human-owned decisions

For each of the three HANDOVERS-5 strings — `Bounded-context ownership assignment`, `Build vs buy decisions in the evolution check`, `Delivery sequencing` — ask sequentially (never batched):

_"Confirm: do you accept ownership of the decision **`<decision-string>`** for this Initiative? (yes / no — if no, name who owns it instead; the answer is recorded in `approvals_obtained:`.)"_

Write the result into `approvals_obtained:` in the universal-schema inline-list form: `approvals_obtained: ["<role-or-name>: <YYYY-MM-DD>", ...]`.

### Step 5 — lint the written README

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py` (do not assume cwd). Run `python3 <repo-root>/tools/lint-frontmatter.py delivery/initiatives/<slug>/README.md` (default mode).

**The lint covers `README.md` only.** The five placeholder child files carry no frontmatter (per F3.7 OQ4) and are treated as prose-only by the default-mode linter; they are not separately linted here — their respective augmenting commands lint them after they fill them.

- Exit 0: proceed to Step 6.
- Non-zero: surface the linter output; offer to re-open the relevant README sections for correction. If the human accepts and re-lint exits 0, proceed normally. If the human declines (or re-lint still fails), exit code 3 with the folder left on disk.

### Step 6 — emit the next-command hint

Last line of output, formatted exactly:

```
NEXT: /context-map <slug>
```

`<slug>` is the Initiative slug just created. No `REVIEW:` line is emitted (only `/sequence-initiative` emits a REVIEW interstitial, per the convention).

## Exit codes

- `0` — initiative folder instantiated, README walked and filled, linter passed, NEXT emitted.
- `1` — human aborted the Step-3 walk before completion. Folder left on disk (the five placeholder children are present from Step 2; the README is partially filled). Resume by re-running with the same `<slug>` and `--force`.
- `2` — pre-conditions failed (no candidate parent Vision; `--from` resolves to a non-existent or `Deprecated` Vision; destination exists without `--force`; slug malformed).
- `3` — folder written but post-fill README lint exited non-zero and human declined re-open. Folder persists in a known-imperfect state.

## What this command will not do

- Not overwrite an existing `delivery/initiatives/<slug>/` folder without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the parent Vision lacks a referenced field, ask the human; do not invent.
- Not batch placeholder questions — one at a time, sequentially.
- Not silently pick a parent Vision when multiple candidates exist (or when only one exists — always confirm).
- Not assume the current working directory is the repo root when invoking the linter.
- Not write an Initiative when the chosen parent Vision's `status:` is `Deprecated`. Refuse via exit code 2.
- Not pre-fill the `capabilities:` list with concrete `CAP-NNN` ids. Populate incidentally during the Section-2 walk; if the human supplies names but no ids, leave the list empty and capture the names as a TODO comment in the README body.
- Not modify, walk, lint, or pre-fill any of the five child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) beyond the `cp -r` itself. They are left in placeholder state for the augmenting commands.
- Not run `lint-frontmatter.py` against any of the five child files — they are intentionally in placeholder state until their augmenting commands fill them.
- Not auto-invoke `/context-map`, `/end-to-end-flow`, `/sequence-initiative`, or any other downstream command. The chain is human-driven; the NEXT line is a hint, not a dispatch.
- Not modify `templates/initiative/` or any of its child files. The template is frozen by F3.7.

$ARGUMENTS
