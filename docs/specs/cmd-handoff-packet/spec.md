# Spec: cmd-handoff-packet

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command (Phase-4 template-fill, artifact-creating sub-class — folder template, 23 children)
- **Serves kit phase:** Delivery (gates Handover 6 — Spec → Engineering Handoff Packet)
- **Constrained by:** [`docs/specs/phase-4-command-convention/spec.md`](../phase-4-command-convention/spec.md) (parent convention — body structure, argv contract, parent-resolution rule, interactive-fill behavior, pre-fill rules, linter integration, exit codes, chaining hint); [`docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md`](../phase-4-command-convention/notes/per-command-spec-checklist.md) (the five-row checklist this spec satisfies); `docs/HANDOVERS.md` §"Handover 6: Spec → Engineering Handoff Packet" (the contract the written packet must shape — 23-file folder layout, README frontmatter superset, "ready for engineering" semantic test); `templates/handoff-packet/` (F3.9 — shipped 2026-05-22 — the folder template this command consumes); [`docs/specs/template-handoff-packet/spec.md`](../template-handoff-packet/spec.md) (sibling F3.9 spec — pins the README's three H2s, per-child frontmatter decisions, and the `requirements.yaml`-as-data-file shape); `.claude/commands/audit-completeness.md` and `scripts/audit-completeness.py` (F1.5 — shipped 2026-05-21 — the NEXT-line target); `tools/lint-command.sh` (existing per-command shape linter — gates the command file itself); `tools/lint-frontmatter.py` (default mode — runs against the written README only; the 22 placeholder children are excluded); `.claude/skills/work-loop/SKILL.md` (the build pattern this spec follows); `.claude/CLAUDE.md` "one clarifying question at a time. Never batch." (the interactivity contract); `.claude/commands/_meta/command-skeleton.md` (the skeleton this command file copies).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `.claude/commands/handoff-packet.md` — the Phase-4 template-fill slash command (P4.11) that instantiates `templates/handoff-packet/` at `delivery/handoff-packets/<slug>/`, walks the README's three H2 sections interactively with one human (one question at a time, never batched), copies the 22 child files as placeholder-shaped stubs, runs `tools/lint-frontmatter.py` (default mode) against the written README, and emits `NEXT: /audit-completeness <slug>` as its chain hint. The command is the natural Phase-4 → Phase-5 boundary: it produces the folder skeleton; `/audit-completeness` (already shipped) is what flips the packet from "drafted" to "ready for engineering."

## Objective

`/handoff-packet <slug>` is the slash command that turns the F3.9 folder template into an instantiated `delivery/handoff-packets/<slug>/` folder owned by a kit user. Today, a kit user wanting to assemble a packet must (a) read HANDOVERS-6, (b) `cp -r templates/handoff-packet/ delivery/handoff-packets/<my-slug>/` manually, (c) figure out which initiative under `delivery/initiatives/` to resolve as `parent_initiative:`, (d) re-derive the README's frontmatter pre-fill rules, and (e) remember to run `/audit-completeness <my-slug>` afterwards to gate the `status: Ready for Engineering` value the template ships pre-filled. This command collapses all of that into one interactive walk. The interactive walk is **README-only** — the command asks the human three sets of questions (one per H2 in `templates/handoff-packet/README.md`: Product brief, Folder index, Ready-for-engineering test) and writes the filled README. The other 22 child files (the 21 narrative children plus `requirements.yaml`) are copied verbatim as placeholder stubs; their per-section filling is the kit user's job, performed outside this command's interactive walk, gated by `/audit-completeness <slug>` (the NEXT-line target). The 22-child-placeholder decision is load-bearing — surfaced explicitly in §"Boundaries" and §"Non-goals" — because pre-filling the 22 children from the parent spec(s) would (a) require fan-out logic this command's contract does not authorize, (b) shadow the kit-user's owner-of-record on the narrative content, and (c) violate the parent convention's "Not fabricate evidence" rule.

The closest prior context is `docs/specs/template-handoff-packet/spec.md` (the F3.9 sibling — pins the layout the command instantiates), `docs/specs/phase-4-command-convention/spec.md` (the parent convention — pins the command's shape), and the four other in-scope creating commands' specs (`cmd-draft-vision`, `cmd-draft-initiative`, `cmd-draft-spec` — fan-out siblings authored in parallel). `/handoff-packet` is the largest of the seven F4 template-fill commands by destination file count (23 vs 1 for `/draft-vision`, 6 for `/draft-initiative`, 1 for `/draft-spec`), but its interactive surface is the smallest by H2 count (3 vs 5–10 across the others) because the README is a structured Product Brief + folder index, not a freeform artifact.

## Why now

ROADMAP P4.11 sits in the Phase-4 block alongside the six other template-fill commands the parent convention made parallelizable. F3.9 (the folder template P4.11 consumes) shipped 2026-05-22, so the template surface is stable. The parent convention (`phase-4-command-convention`) shipped 2026-05-23, so the body-shape contract is locked. F1.5 (`scripts/audit-completeness.py` — the NEXT-line target) shipped 2026-05-21, so the chain successor exists and is runnable. The three upstream dependencies are all met; P4.11 is unblocked. Until this command ships, kit users have a copyable template but no interactive command, and the Delivery → Engineering boundary remains a manual `cp -r` plus hand-frontmatter-fill exercise — which is precisely the friction the parent convention's "interactive walk" pattern is designed to remove.

P4.11 also closes the Phase-4 chain: `/draft-vision` → `/draft-initiative` → (`/context-map`, `/end-to-end-flow`, `/sequence-initiative`) → `/draft-spec` → **`/handoff-packet`** → `/audit-completeness` (Phase-5 entry). Until P4.11 ships, the chain's last creating command is missing; once it ships, the seven-command chain is complete and the kit's Delivery-phase workflow is end-to-end interactive.

## Inputs and outputs

**Inputs.**

1. Positional argument `<slug>` — kebab-case identifier matching `^[a-z0-9-]+$`, ≤ 80 chars, naming the new Handoff Packet. Becomes the folder name under `delivery/handoff-packets/`.
2. Optional flag `--from <initiative-slug>` — explicit selection of the parent initiative. Overrides the auto-detect step. Per parent convention OQ6, the parent is named via a flag, not a second positional.
3. Optional flag `--force` — permits overwriting an existing `delivery/handoff-packets/<slug>/` folder. Without `--force`, an existing destination causes exit 2.
4. `templates/handoff-packet/` — the F3.9 folder template the command copies. The template contains `README.md` (carries universal-schema + HANDOVERS-6 frontmatter superset), `requirements.yaml` (YAML data file, no markdown frontmatter), and 21 narrative child files (no frontmatter, H1 + orientation + sub-templates).
5. `delivery/initiatives/` — the family directory holding candidate parent Initiative artifacts. Each candidate is a folder `delivery/initiatives/<initiative-slug>/` with a `README.md` carrying universal-schema frontmatter including `status:`. The candidate list filters on `status:` not equal to `Deprecated` (the product-artifact-track terminal-or-killed value per `docs/CONVENTIONS.md` §"Lifecycle states"; per the parent convention's "Parent-artifact resolution" sub-section).
6. `tools/lint-frontmatter.py` — default-mode linter the command runs against the written README. Default mode walks `PHASE_DIRS = ["strategy", "discovery", "validation", "delivery", "market"]` so `delivery/handoff-packets/<slug>/README.md` is in scope.

**Outputs.**

1. `.claude/commands/handoff-packet.md` — the new slash-command file. Body follows `.claude/commands/_meta/command-skeleton.md` and the parent convention's body-structure contract (H2 sections: `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`). Frontmatter declares `description:` (one sentence ≤ 1024 chars; the slash-command palette renders this) and `argument-hint:` set to the literal string `<slug> [--from <initiative-slug>] [--force]` per the artifact-creating sub-class's argv contract (parent named specifically as `<initiative-slug>`, consistent with `/draft-spec`'s `<initiative-slug>` and `/draft-initiative`'s `<vision-slug>`).
2. `delivery/handoff-packets/<slug>/` — the instantiated folder at command-runtime. The folder layout matches `templates/handoff-packet/` exactly: `README.md` (filled by the interactive walk; frontmatter pre-fills resolved; placeholder body replaced with human-confirmed content) plus 22 child files copied verbatim from the template as placeholder stubs (21 narrative children retain their `<placeholder>` body markers; `requirements.yaml` retains its single placeholder Requirement entry). The folder is the load-bearing artifact for HANDOVERS-6; the README's `status:` field is pre-filled to `Ready for Engineering` per the F3.9 template (with the inline HTML warning the template ships intact), but the four `*_review_passed:` audit-gate fields remain at their `<YYYY-MM-DD>` and `<passed | not-required | <YYYY-MM-DD>>` augmented-placeholder values — they flip to concrete values only after `/audit-completeness <slug>` and the named reviewer subagents pass, which is human-orchestrated post-`/handoff-packet`.
3. Stdout — the interactive walk's prompts and confirmations, plus the linter's report, plus the chain hint. Last line is exactly `NEXT: /audit-completeness <slug>` (matches the parent convention's chaining-hint contract; resolves the convention's OQ3).
4. Exit code — one of `0` (success), `1` (human aborted), `2` (pre-conditions failed), `3` (lint failed post-write and human declined to re-open). See §"Exit codes" below.

A reader of this section can construct the command's interface signature without reading anything else.

## Body-shape contract

The command file body matches the parent convention's skeleton verbatim where the skeleton's placeholder text applies; per-section refinements below specialize the skeleton for `/handoff-packet`.

```markdown
---
description: Instantiate the Handoff Packet folder template at delivery/handoff-packets/<slug>/, walk the README's three H2 sections interactively with the human, copy the 22 child files as placeholders, lint the written README, and chain to /audit-completeness <slug>.
argument-hint: <slug> [--from <parent-slug>] [--force]
---

# /handoff-packet

> Phase-4 template-fill command (artifact-creating sub-class). Instantiates the F3.9 folder template at `delivery/handoff-packets/<slug>/`. Walks the README's three H2 sections interactively (Product brief, Folder index, Ready-for-engineering test). Copies the 22 child files as placeholder stubs; the human fills them after this command exits, gated by `/audit-completeness <slug>`. Gates HANDOVERS-6 (Spec → Engineering Handoff Packet).

## When to run

- After a `delivery/initiatives/<slug>/specs/` folder has one or more PM Specs ready for engineering consolidation.
- After `/draft-spec` has emitted `NEXT: /handoff-packet <slug>` (the Phase-4 chain's penultimate step).
- When assembling the structured pre-engineering deliverable engineering will actually consume.

## Inputs

1. The positional arg — `<slug>` (the new Handoff Packet's slug). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars.
2. `templates/handoff-packet/` — the F3.9 folder template this command consumes (README + `requirements.yaml` + 21 narrative children).
3. Parent artifact: an Initiative under `delivery/initiatives/<initiative-slug>/` (resolution rule below).
4. Optional flag `--from <initiative-slug>` overrides auto-detection.
5. Optional flag `--force` permits overwriting an existing destination.

## Procedure

### Step 1 — resolve parent Initiative

If `--from <initiative-slug>` is given, use it. Otherwise list candidate parents from `delivery/initiatives/` whose `status:` is not `Deprecated` (the product-artifact-track terminal-or-killed value per CONVENTIONS §"Lifecycle states"), sorted by `last_updated:` descending and capped at 10. Present as a numbered list; ask the human to pick one (or to specify `--from` for an older candidate). Never silently pick — always confirm, even when only one candidate exists (per parent convention OQ7). If the candidate list is empty, exit with code 2 and surface the remediation message: `no Initiative found in delivery/initiatives/ with status != Deprecated — run /draft-initiative first, then /draft-spec, then re-run /handoff-packet <slug>`.

After resolving the parent Initiative, check whether the Initiative has any PM Specs: if `delivery/initiatives/<initiative-slug>/specs/` does not exist OR exists but is empty, emit a **non-blocking warning** to stdout: `"warning: parent Initiative '<initiative-slug>' has no PM Specs under specs/ — the Handoff Packet will be authored against an Initiative with no per-feature contract. Run /draft-spec --from <initiative-slug> before continuing if a PM Spec is expected. Continuing as-is is supported (the convention's OQ3 allows it) but /audit-completeness will likely flag missing per-feature content."` Proceed to Step 2 regardless of the human's response — the warning is informational, not gating (this honors OQ3's no-hard-precondition resolution).

### Step 2 — instantiate the folder template

Copy `templates/handoff-packet/` (folder, `cp -r`) to `delivery/handoff-packets/<slug>/`. If the destination exists and `--force` is not set, exit code 2 with: `delivery/handoff-packets/<slug>/ already exists — re-run with --force to overwrite, or pick a different slug`. Pre-fill the README's mechanical frontmatter fields (see §"Pre-fill rules" below). The 22 child files are NOT modified — they are copied verbatim from the template as placeholder stubs.

### Step 3 — walk the README's three H2 sections one section at a time

For each H2 in `templates/handoff-packet/README.md` (Product brief, Folder index, Ready-for-engineering test), ask one question per placeholder, sequentially. Never batch. Confirm the section's filled content before advancing. See §"Per-section interactive prompts" below for the verbatim prompts. The 22 child files are NOT walked here — they are filled by the human after this command exits, with `/audit-completeness <slug>` reporting which child files still hold placeholders.

### Step 4 — surface human-owned decisions

Read the README's `human_owned_decisions:` frontmatter list (pre-filled by the F3.9 template with the three HANDOVERS-6-canonical decisions: "Final fixed_vs_flexible classification", "Compliance review acceptance", "Engineering partner sign-off"). Ask the human to confirm each is owned by a named human. Update `approvals_obtained:` inline-list entries as the human dictates.

### Step 5 — lint the written README

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`. Run `python3 <repo-root>/tools/lint-frontmatter.py delivery/handoff-packets/<slug>/README.md` (default mode). The 22 child files are NOT linted — `requirements.yaml` is not markdown (the linter's discovery skips it by extension), and the 21 narrative children carry no frontmatter and retain `<placeholder>` body markers (because they are copied verbatim from the F3.9 template). Default-mode lint would reject those — the same exclusion pattern `/draft-initiative` uses for its five placeholder children. Report the linter result.

- If exit 0: proceed to Step 6.
- If exit non-zero: offer to re-open the relevant README sections for correction. If the human accepts and the corrections lint clean on re-run, proceed to Step 6. If the human declines (or re-runs but lint still fails), exit code 3 with the linter output surfaced and the artifact left on disk.

### Step 6 — emit the next-command hint

Last line of output, formatted exactly: `NEXT: /audit-completeness <slug>`. No `REVIEW:` line is emitted (that affordance is unique to `/sequence-initiative` per the parent convention's "Capabilities-file interstitial" sub-section).

## What this command will not do

- Not overwrite an existing `delivery/handoff-packets/<slug>/` without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the parent Initiative lacks a referenced field, ask, do not invent.
- Not batch placeholder questions — one at a time, even within an H2.
- Not silently pick a parent Initiative when multiple candidates exist.
- Not assume the working directory is the repo root when invoking the linter.
- Not pre-fill the 22 child files with content extracted from the parent spec(s) — filling the children is the human's job, performed outside this command's interactive walk; `/audit-completeness <slug>` is the gate that reports which children still hold placeholders.
- Not declare the packet `Ready for Engineering` — that lifecycle transition flips only after `/audit-completeness` plus the named reviewer subagents pass, which is human-orchestrated post-`/handoff-packet`. The README's `status:` value remains the template-pre-filled `Ready for Engineering` string, but the four `*_review_passed:` audit-gate fields remain placeholders until the audits actually pass (per the F3.9 template's inline HTML warning, which this command leaves intact).
- Not run `/audit-completeness` itself. The chain hint names it; the human runs it next.
- Not run the `adversarial-reviewer` or `quality-engineer` subagents. The chain hint names `/audit-completeness` as the immediate next step; the reviewer subagents are invoked separately by the human as part of the README's four `*_review_passed:` gate-fill workflow.
```

## Per-section interactive prompts

The interactive walk covers **only** the three H2s in `templates/handoff-packet/README.md`. Per parent convention §"Interactive fill," the command walks one H2 at a time and asks one question per placeholder, sequentially, within each H2.

### H2 #1 — `## Product brief`

The README's Product brief section is a single-paragraph orientation citing the parent strategic intent and pointing to `business-objective.md` and `customer-segment.md` for full elaboration. The command emits these prompts in order:

1. "What is being shipped, in one sentence? (This is the load-bearing claim engineering will read first — name the product behavior, not the strategy.)"
2. "Which customer segment does it serve? (One short noun phrase; full segment definition belongs in `customer-segment.md`, which is a placeholder for now.)"
3. "Which strategic intent does it advance? (Provide the intent slug; this must match the `parent_intent:` value in the README's frontmatter — already pre-filled from the parent Initiative's `parent_intent:` if present.)"

After all three are answered, the command echoes the assembled Product Brief paragraph and asks: "Does this Product Brief read as engineering's first paragraph of context? Confirm or revise."

### H2 #2 — `## Folder index`

The Folder index is a 22-row markdown table the F3.9 template ships pre-filled (file name + one-line purpose for each sibling child). The table content is not edited interactively — it is the kit's canonical folder layout per HANDOVERS-6 — but the command asks one confirmation question:

1. "The folder index table lists 22 sibling files in the HANDOVERS-6 canonical order. The 22 children are copied as placeholders; you will fill them outside this command, with `/audit-completeness <slug>` reporting which still hold placeholders. Confirm you understand the 22-child fill is your next workflow step."

A `yes` advances; any other response surfaces a remediation message naming `/audit-completeness <slug>` and the parent convention §"Phase-4 Template-Fill Commands" sub-section.

### H2 #3 — `## Ready-for-engineering test`

The Ready-for-engineering test restates HANDOVERS-6's seven-clause semantic test (we understand the customer problem / business objective / required product behavior / what is fixed and flexible / risks / how success is measured / which questions remain). The F3.9 template ships the seven clauses pre-filled as a bulleted list. The command asks one question:

1. "The seven-clause ready-for-engineering test is HANDOVERS-6's semantic gate. It is restated verbatim in the README so a reader of the folder can apply the test directly. Confirm the seven clauses are present and that you understand the packet is not actually ready for engineering until `/audit-completeness <slug>` and the named reviewer subagents pass."

A `yes` advances to Step 4; any other response surfaces a remediation message naming the four `*_review_passed:` audit-gate frontmatter fields and the `/audit-completeness` chain step.

**Note on the 22 child files.** None of the 22 child files (the 21 narrative children plus `requirements.yaml`) are walked interactively by this command. They are copied verbatim from the F3.9 template as placeholder stubs. The human fills them after this command exits, by reading the parent Initiative's spec(s) at `delivery/initiatives/<initiative-slug>/specs/` and the parent strategic intent / Validation Learning Memo upstream; `/audit-completeness <slug>` is the gate that reports which children still hold `<placeholder>` markers and which checklist items are unsatisfied. This is the same pattern `/draft-initiative` uses for its five placeholder children (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) — those are filled by the three augmenting commands (`/context-map`, `/end-to-end-flow`, `/sequence-initiative`) and by `/draft-spec` accumulations, not by `/draft-initiative` itself. `/handoff-packet`'s out-of-band fill is symmetric.

## Pre-fill rules

Before asking the human anything in Step 3, the command pre-fills the README's mechanical frontmatter fields:

- `id:` — derived as `HP-<NNN>` where `<NNN>` is the next unused integer across existing `delivery/handoff-packets/*/README.md` files' `id:` values (zero-padded to three digits, e.g., `HP-001`, `HP-002`). The `HP-` prefix matches the ontology Domain H "Handoff Packet" object_type's conventional id form (consistent with the kit's other typed prefixes: `VIS-` for Vision, `INIT-` for Initiative, etc., per the F3.9 template's pre-filled `id: <type-prefix>-<NNN>` placeholder).
- `slug:` — the positional argument verbatim.
- `created:` — today's date, ISO-8601 (YYYY-MM-DD), resolved from the system clock at command-start.
- `last_updated:` — same as `created` on first instantiation.
- `parent_initiative:` — the resolved parent Initiative slug from Step 1.
- `parent_intent:` and `parent_vision:` — restated for upstream traceability per the F3.9 template's traceability-field retention rule (the template ships these as placeholders); pre-fill by reading the parent Initiative's `README.md` frontmatter (`parent_intent:` and `parent_vision:` fields). If the parent Initiative is missing either field, the command leaves the corresponding pre-fill at its `<placeholder>` value and surfaces a one-line warning ("parent Initiative `<slug>` does not declare `parent_intent:` — the Handoff Packet README will inherit a `<placeholder>` value for that field; resolve upstream by editing the parent Initiative's frontmatter").
- `object_type: Handoff Packet` — the F3.9 template ships this pre-filled; the command re-asserts it as a defensive check.
- `status: Ready for Engineering` — the F3.9 template ships this pre-filled (the value is in `LIFECYCLE_STATES`, so the linter accepts it). The command does NOT change this value. The inline HTML warning the template ships intact ("WARNING: pre-filled to satisfy LIFECYCLE_STATES; the four audit-gate date fields above MUST be completed with concrete values before this packet is handed to engineering.") is preserved verbatim by the `cp -r`.

The command never asks the human to type a mechanical field. The four `*_review_passed:` audit-gate fields (`completeness_audit_passed`, `adversarial_review_passed`, `quality_engineer_review_passed`, `compliance_review_status`) and `engineering_partner:` and the `fixed_vs_flexible:` nested map are NOT pre-filled by the command — they remain at their F3.9-template-shipped augmented-placeholder values, to be filled by the human after the corresponding audits and reviews actually pass.

## Linter integration

After Step 3–4 complete, Step 5 runs `python3 <repo-root>/tools/lint-frontmatter.py delivery/handoff-packets/<slug>/README.md` (default mode, NOT `--check-template` — the artifact is now a real product artifact, not a template). The linter is run **only against the README**. The 22 child files are excluded for two reasons:

1. `requirements.yaml` is a YAML data file, not markdown; the linter's discovery skips it by extension.
2. The 21 narrative child files carry no frontmatter and retain `<placeholder>` body markers (because they are copied verbatim from the F3.9 template). Default-mode `tools/lint-frontmatter.py` requires the universal-schema frontmatter superset on markdown files in `PHASE_DIRS`; a placeholder-shaped narrative file would fail that check. Excluding the 22 children from this command's lint step mirrors the same exclusion pattern `/draft-initiative` uses for its five placeholder children: the command lints only the README it actually fills; the rest are linted (or not) by later commands or by `/audit-completeness`.

If the linter exits 0, the command proceeds to Step 6. If non-zero, the command offers to re-open the relevant README sections for correction; per the parent convention, exit code 3 fires if the human declines or re-runs but lint still fails.

## Exit codes

Per the parent convention's "Exit codes" sub-section, exactly four codes:

- `0` — folder instantiated at `delivery/handoff-packets/<slug>/`, README walked and filled, linter passed, `NEXT: /audit-completeness <slug>` emitted.
- `1` — human aborted the interactive walk before Step 5 completed. The folder is left at its partial state on disk (the `cp -r` happened in Step 2, so the 22 children are present as placeholders; the README is partially filled). Command emits a "resume by re-running with the same slug" hint. No NEXT line.
- `2` — pre-conditions failed: positional `<slug>` malformed; `delivery/handoff-packets/<slug>/` already exists without `--force`; `templates/handoff-packet/` missing; candidate parent Initiative list empty; `--from <initiative-slug>` named but `delivery/initiatives/<initiative-slug>/` does not exist. Folder not written. Command surfaces the specific failed pre-condition and the corresponding remediation suggestion.
- `3` — folder was written and README walked, but `tools/lint-frontmatter.py` exited non-zero on the README and the human declined to re-open the relevant sections (or re-opened, but lint still failed). Artifact persists on disk in a known-imperfect state. Automation consumers MUST treat exit 3 as distinct from exit 0.

No fifth code is added. The parent convention's four-code contract is honored verbatim.

## Chaining hint

Last line of output, formatted exactly: `NEXT: /audit-completeness <slug>`. This resolves the parent convention's OQ3 ("Should `/handoff-packet` chain into `/audit-completeness <slug>` or into a TBD `/handoff-packet-finalize` command?") — the parent convention resolves to `/audit-completeness <slug>` because `/audit-completeness` is shipped (prose-procedure plus F1.5 script) and is the natural Phase-4 exit and Phase-5 entry.

No `REVIEW:` line is emitted. That affordance is unique to `/sequence-initiative` per the parent convention's "Capabilities-file interstitial" sub-section.

## Boundaries

### Always do

- Quote the parent convention's body-structure contract verbatim where the command's H2 sections match. Any deviation surfaces as a "deviates from §X for reason Y" note in this spec's `Constrained by:` line (none currently — `/handoff-packet` conforms to the convention exactly).
- Walk the README's three H2 sections one at a time. Never batch placeholder questions within an H2. Restates the kit's `.claude/CLAUDE.md` "one clarifying question at a time" rule mechanically.
- Copy `templates/handoff-packet/` recursively (`cp -r`) so the 22 child files arrive at the destination with their `<placeholder>` markers intact. The F3.9 template's inline HTML warning on the README (re: audit-gate fields) is preserved verbatim.
- Confirm the parent Initiative choice with the human even when only one candidate exists (per parent convention OQ7 — auto-pick is forbidden).
- Resolve the repo root as the nearest ancestor of the working directory containing `tools/lint-frontmatter.py`; do not assume the working directory is the repo root.
- Emit the `NEXT: /audit-completeness <slug>` hint on success (exit 0). On exit 1, emit a "resume by re-running with the same slug" hint. On exit 2 and 3, emit the specific remediation messages defined in §"Exit codes."

### Ask first

- Adding any pre-fill for the 22 child files beyond the verbatim `cp -r`. Any such pre-fill would extract content from the parent spec(s), shadow the kit-user's owner-of-record, and risk fabricating evidence — surfaces as a per-command-spec deviation per the parent convention.
- Adding any pre-fill for the four `*_review_passed:` audit-gate fields, `engineering_partner:`, or `fixed_vs_flexible:`. These are audit-outcome / human-decision fields whose values must be set by the human after the corresponding audits / decisions actually happen, not by the command's pre-fill logic.
- Expanding the interactive walk beyond the README's three H2s. The 22 child files are explicitly out of the interactive walk's scope; expanding that scope changes the command's contract substantially and would require a per-command-spec deviation note.
- Adding a `--non-interactive` mode that fills the README from the parent Initiative's frontmatter without prompting. The parent convention's "one question at a time" rule is load-bearing; a non-interactive mode silently fabricates the human-confirmation step.

### Never do

- Pre-fill the 22 child files with content extracted from the parent spec(s). Per §"Always do" rationale and parent convention "Not fabricate evidence" rule. **This is the load-bearing design decision of this spec.** The 22 children are placeholders; the human fills them; `/audit-completeness <slug>` is the gate.
- Declare the packet `Ready for Engineering` as a behavioral consequence of this command. The README's `status:` value remains the template-pre-filled `Ready for Engineering` string, but the four `*_review_passed:` audit-gate fields remain placeholders until the audits actually pass. The semantic "ready for engineering" gate is `/audit-completeness <slug>` plus the named reviewer subagents, all of which are human-orchestrated post-`/handoff-packet`.
- Run `/audit-completeness` automatically as part of this command's Step 5 or Step 6. The chain hint names it; the human runs it next.
- Run the `adversarial-reviewer` or `quality-engineer` subagents automatically. Those are invoked separately by the human as part of the README's `adversarial_review_passed:` / `quality_engineer_review_passed:` gate-fill workflow.
- Modify `templates/handoff-packet/` from inside the command. The template is the kit's source of truth; modifying it here would silently drift the contract.
- Add a new ontology type. `/handoff-packet` instantiates the Handoff Packet type that already exists in ontology Domain H. Same rule as the parent convention's "Never do" sub-section.
- Walk the 22 child files interactively. Out of scope by design. Any expansion of the interactive walk to children requires a per-command-spec deviation note per parent convention OQ8.
- Silently pick a parent Initiative when multiple candidates exist. Per parent convention "Parent-artifact resolution."

## Verification mode

- **Goal-based check** — the command file at `.claude/commands/handoff-packet.md` passes `bash tools/lint-command.sh`; the file's H2 section list matches the parent convention's required-H2 superset (`## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`); the `argument-hint:` frontmatter starts with the literal `<slug>` token per the artifact-creating sub-class's argv contract; the body cites `templates/handoff-packet/` and the path exists in the repo; the body cites `delivery/handoff-packets/` and the parent directory exists in the repo.
- **Audit-driven** — `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 with the `handoff-packet` row no longer auto-skipped (the parent convention's contract test auto-detects the file's existence and runs the seven assertions against it).
- **Manual gesture** — one recorded reproduction: from a fixture initiative (with at least one PM Spec), invoke `/handoff-packet my-test-packet --from <fixture-initiative-slug>` in a Claude Code session; verify the destination folder is created with 23 files; verify the README's three H2s were walked one question at a time; verify the linter ran in default mode against the README only; verify the NEXT line is exactly `NEXT: /audit-completeness my-test-packet`. Recorded in this spec's `notes/manual-gesture.md` at CAPTURE phase.

The command is **not** verified by a runtime-behavior simulation in pytest — the command's body is a prose procedure for Claude Code to follow interactively, not a runnable Python entry-point. The contract test (`test_phase4_command_shape.py`) gates the file's *shape*; the manual gesture gates the file's *behavior*. This is the same verification split the parent convention's spec uses for the skeleton.

## Contract tests

Each test is one shell line or one pytest case. They are the gate.

- `T1` — `test -f .claude/commands/handoff-packet.md` (the command file exists).
- `T2` — `bash tools/lint-command.sh .claude/commands/handoff-packet.md` exits 0 (passes the generic command-shape linter).
- `T3` — `python3 -m pytest scripts/tests/test_phase4_command_shape.py -k handoff_packet` exits 0 (passes all parent-convention contract assertions for the `handoff-packet` row of the `INSCOPE` constant).
- `T4` — `grep -cE "^## (When to run|Inputs|Procedure|What this command will not do)" .claude/commands/handoff-packet.md` returns 4 (the four required H2s are present).
- `T5` — `grep -cE "^argument-hint: <slug>" .claude/commands/handoff-packet.md` returns 1 (the artifact-creating sub-class positional is declared).
- `T6` — `grep -c "templates/handoff-packet/" .claude/commands/handoff-packet.md` returns ≥ 1 AND `test -d templates/handoff-packet` (the cited template path exists).
- `T7` — `grep -c "delivery/handoff-packets/" .claude/commands/handoff-packet.md` returns ≥ 1 AND `test -d delivery/handoff-packets` (the destination family directory exists in the repo).
- `T8` — `grep -c "^NEXT: /audit-completeness <slug>$" .claude/commands/handoff-packet.md` returns ≥ 1 (the chain hint is present in the documented exact form). The `^` and `$` anchors guard against drift to a non-canonical chain successor.
- `T9` — `grep -c "_meta/command-skeleton.md" .claude/commands/handoff-packet.md` returns 0 (the command file does NOT reference the skeleton path inside its own body — the skeleton is a copy-source, not a runtime reference).
- `T10` — `bash tools/pre-pr.sh` exits 0 (no regression on kit-wide health).
- `T11` — `grep -cE "^- \[ \] \*\*P4\.11\*\*" ROADMAP.md` returns 1 at PLAN-phase time (the P4.11 row is still unchecked; flips to `[x]` at CAPTURE phase only).

## Non-goals

- Running `/audit-completeness` as part of this command. Out of scope. The chain hint names it; the human runs it next.
- Running the `adversarial-reviewer` or `quality-engineer` subagents. Out of scope. Same rationale.
- Pre-filling the 22 child files. Out of scope by design. The human fills them out-of-band, with `/audit-completeness` as the gate. **This is the load-bearing non-goal.**
- Flipping the README's four `*_review_passed:` audit-gate fields to concrete values. Out of scope. The fields flip only after the corresponding audits actually run and pass; this command does not run them.
- Modifying `templates/handoff-packet/`. Out of scope. The template is frozen by F3.9.
- Modifying `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, or any of the parent-convention surface. Out of scope.
- Adding a runnable Python entry-point for this command. The command file is a prose procedure for Claude Code to follow interactively; no Python script ships with this spec.
- Authoring a `/handoff-packet-finalize` command. The parent convention OQ3 resolves explicitly to chaining into `/audit-completeness`, not into a TBD finalizer.
- Adding `--dry-run` to the argv contract. Per parent convention OQ1, deferred.
- Adding a `--non-interactive` mode. Out of scope; the interactivity contract is load-bearing.

## Open questions

1. **Should the command read the parent Initiative's `parent_intent:` and `parent_vision:` and pre-fill them on the Handoff Packet README, or should it leave them as placeholders for the human to confirm during the interactive walk?** _Resolved here: pre-fill from the parent Initiative's frontmatter; if the parent Initiative is missing either field, leave the corresponding pre-fill at its `<placeholder>` value and surface a one-line warning naming the upstream fix. Rationale: the mechanical-field-pre-fill rule (parent convention §"Pre-fill rules") includes traceability `parent_*:` fields; not pre-filling them would force the human to re-type values that are already canonically stored in the parent Initiative. The warning preserves the kit's "don't fabricate" discipline when the parent itself is incomplete._
2. **Should the command emit a one-line summary of which of the 22 child files still hold placeholders, as part of its exit-0 stdout?** _Deferred. The `/audit-completeness` chain step already produces this report (it walks the 23 files and maps placeholders to the 25-item checklist); duplicating it inside `/handoff-packet`'s exit-0 stdout would be redundant. Surface as a future polish item if adopters request it._
3. **Should the command refuse to instantiate when the parent Initiative has zero PM Specs under `delivery/initiatives/<initiative-slug>/specs/`?** _Resolved here: no. The Handoff Packet's parent is the Initiative, not the specs; the specs are the upstream content the human will reference when filling the 22 children, but their existence is not a hard pre-condition for `/handoff-packet`. Surfacing the "no specs found" case as a one-line warning is acceptable but not required; the human is responsible for knowing what they're doing._
4. **Should the command verify the parent Initiative's `status:` against a more restrictive set than just "not `Deprecated`" (e.g., require `Approved` or `Ready for Engineering`)?** _Resolved here: no. Per parent convention, the candidate filter is "`status:` not in the terminal-or-killed set" — `Deprecated` is the only product-artifact-track terminal value; further narrowing would diverge from the convention and require a per-command-spec deviation note. The human's confirmation step in Step 1 catches "wrong Initiative" failures._

## Acceptance criteria

- [ ] `.claude/commands/handoff-packet.md` exists with the body shape specified in §"Body-shape contract" (the four required H2s plus the per-section prompts derived from `templates/handoff-packet/README.md`'s three H2s).
- [ ] `argument-hint:` frontmatter is exactly `<slug> [--from <parent-slug>] [--force]` (artifact-creating sub-class).
- [ ] `description:` frontmatter is one sentence, ≤ 1024 chars, and accurately summarizes the command's behavior.
- [ ] The body cites `templates/handoff-packet/` as the consumed template and `delivery/handoff-packets/` as the destination family.
- [ ] The body declares the parent-artifact-resolution rule: candidates from `delivery/initiatives/` filtered by `status:` not equal to `Deprecated`; empty list → exit 2 with the documented remediation message.
- [ ] The body documents the 22-child-placeholder choice explicitly, including the rationale and the `/audit-completeness` gate.
- [ ] The body documents the four-code exit-code contract verbatim per the parent convention.
- [ ] The body's last documented output line is exactly `NEXT: /audit-completeness <slug>`.
- [ ] All contract tests pass: T1–T11.
- [ ] No new ontology type added; no F3.9 template modified; no `tools/` script modified; no `docs/HANDOVERS.md` or `docs/CONVENTIONS.md` modified.

## Cross-references

- **Consumed by:** kit users running `/handoff-packet <slug>` interactively in Claude Code. Downstream chain: `/audit-completeness <slug>` (Phase-5 entry — shipped F1.5).
- **Consumes:** `templates/handoff-packet/` (F3.9), `delivery/initiatives/` (family directory for parent resolution), `tools/lint-frontmatter.py` (default mode), `.claude/commands/_meta/command-skeleton.md` (copy-source).
- **Frontmatter fields owned:** none directly; the command pre-fills the README's mechanical universal-schema and HANDOVERS-6 fields per §"Pre-fill rules."
- **Ontology object types touched:** Handoff Packet (Domain H, instantiated). Initiative (Domain D, read for parent resolution). Requirement, Feature, Capability, Acceptance Criteria, Business Rule, Non-Functional Requirement (Domain E — referenced by the 22 placeholder children but not instantiated by this command). Risk, Mitigation (Domain G — same).
