---
description: Instantiate the F3.9 Handoff Packet folder template at delivery/handoff-packets/<slug>/ — copy README plus 22 placeholder children, walk the README's three H2 sections interactively, pre-fill mechanical metadata, lint the README, and chain to /audit-completeness.
argument-hint: <slug> [--from <initiative-slug>] [--force]
---

# /handoff-packet

> Artifact-creating Phase-4 template-fill command (folder-template sub-case). Reads an active parent Initiative; `cp -r` the `templates/handoff-packet/` folder to `delivery/handoff-packets/<slug>/`; walks the README's three H2 sections (`## Product brief`, `## Folder index`, `## Ready-for-engineering test`) one at a time interactively; leaves the 22 child files (`business-objective.md`, `customer-segment.md`, `personas.md`, `problem.md`, `jobs-to-be-done.md`, `current-workflow.md`, `future-workflow.md`, `capabilities.md`, `features.md`, `requirements.yaml`, `business-rules.md`, `policy-constraints.md`, `acceptance-criteria.md`, `non-functional-requirements.md`, `risks.md`, `dependencies.md`, `open-questions.md`, `out-of-scope.md`, `decision-log.md`, `launch-considerations.md`, `success-metrics.md`, `human-owned-decisions.md`) as placeholder stubs — the human fills them after this command exits, gated by `/audit-completeness <slug>`. Gates Handover 6 (Spec → Engineering Handoff Packet).

## When to run

- After all PM Specs under a parent Initiative have been drafted (`/draft-spec` has run for every row in `delivery/initiatives/<initiative-slug>/child-specs.md`).
- When the Initiative is ready to be consolidated into the kit's structured pre-engineering deliverable engineering will actually consume.
- Before `/audit-completeness <slug>` — the audit reports which of the 22 children still hold placeholders and which checklist items are unsatisfied.

## Inputs

1. The positional arg — `<slug>` (the new Handoff Packet's slug). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars.
2. `templates/handoff-packet/` — the F3.9 folder template this command consumes (README + `requirements.yaml` + 21 narrative children).
3. Parent artifact: an Initiative at `delivery/initiatives/<initiative-slug>/` whose `status:` is not `Deprecated`. Resolution rule below; `--from <initiative-slug>` for explicit selection.
4. Optional flag `--force` — permits overwriting an existing `delivery/handoff-packets/<slug>/`.

## Procedure

### Step 1 — resolve parent Initiative

If `--from <initiative-slug>` is given, use it. Otherwise list candidate parents from `delivery/initiatives/` whose `status:` is not `Deprecated`, sorted by `last_updated:` descending, capped at 10. Present as a numbered list; ask the human to pick one (or specify `--from` for an older candidate). Never silently pick — always confirm, even when only one candidate exists.

If the candidate list is empty, exit code 2 with: `"no Initiative found in delivery/initiatives/ with status != Deprecated — run /draft-initiative first, then /draft-spec, then re-run /handoff-packet <slug>."`

After resolving the parent Initiative, check whether the Initiative has any PM Specs. If `delivery/initiatives/<initiative-slug>/specs/` does not exist OR exists but is empty, emit a **non-blocking warning**: _"warning: parent Initiative '<initiative-slug>' has no PM Specs under specs/ — the Handoff Packet will be authored against an Initiative with no per-feature contract. Run `/draft-spec --from <initiative-slug>` before continuing if a PM Spec is expected. Continuing as-is is supported, but `/audit-completeness` will likely flag missing per-feature content."_ Proceed to Step 2 regardless of the human's response — the warning is informational, not gating.

### Step 2 — instantiate the folder template

`cp -r templates/handoff-packet/` to `delivery/handoff-packets/<slug>/`. If the destination exists and `--force` is not set, exit code 2 with: `"delivery/handoff-packets/<slug>/ already exists — re-run with --force to overwrite, or pick a different slug."`

The 22 child files (`business-objective.md`, …, `human-owned-decisions.md`, plus `requirements.yaml`) are copied verbatim and left in placeholder state. They are NOT modified by this command beyond the `cp -r` itself.

Pre-fill the README's mechanical frontmatter (the human is never asked for these):

- `id: HP-<NNN>` — scan `delivery/handoff-packets/*/README.md` for `id: HP-` lines, take max + 1, zero-pad to three digits (or `001` if none exist).
- `slug:` — the positional argument.
- `created:` — today's date (ISO-8601, system clock at command start).
- `last_updated:` — same as `created`.
- `parent_initiative:` — the resolved Initiative slug from Step 1.
- `parent_vision:` and `parent_intent:` — read from the parent Initiative's README frontmatter (transitive carry-through). If either is missing, leave the corresponding field at its `<placeholder>` value and surface a one-line warning naming the unresolved upstream link.
- `object_type: Handoff Packet` — re-assert (template already pre-fills; defensive check).
- `status: Ready for Engineering` — left at the template's pre-filled value. The inline HTML warning the template ships intact ("WARNING: pre-filled to satisfy LIFECYCLE_STATES; the four audit-gate date fields above MUST be completed with concrete values before this packet is handed to engineering.") is preserved verbatim. The four `*_review_passed:` audit-gate fields (`completeness_audit_passed`, `adversarial_review_passed`, `quality_engineer_review_passed`, `compliance_review_status`), `engineering_partner:`, and `fixed_vs_flexible:` are NOT pre-filled — they remain at their template-shipped placeholder values for the human to set after the audits actually pass.

### Step 3 — walk the README's three H2 sections one at a time

Walk these prompts in order. One question per turn. Never batch. Confirm per-H2 before advancing.

**H2 #1 — `## Product brief`** (three prompts, then a confirmation echo):

- _"What is being shipped, in one sentence? (This is the load-bearing claim engineering will read first — name the product behavior, not the strategy.)"_
- _"Which customer segment does it serve? (One short noun phrase; full segment definition belongs in `customer-segment.md`, which is a placeholder for now.)"_
- _"Which strategic intent does it advance? (Provide the intent slug; this must match the `parent_intent:` value in the README's frontmatter — already pre-filled from the parent Initiative's `parent_intent:` if present.)"_

After all three are answered, echo the assembled Product Brief paragraph and ask: _"Does this Product Brief read as engineering's first paragraph of context? Confirm or revise."_

**H2 #2 — `## Folder index`** (one confirmation prompt):

- _"The folder index table lists 22 sibling files in the HANDOVERS-6 canonical order. The 22 children are copied as placeholders; you will fill them outside this command, with `/audit-completeness <slug>` reporting which still hold placeholders. Confirm you understand the 22-child fill is your next workflow step."_

A `yes` advances; any other response surfaces a remediation message naming `/audit-completeness <slug>` and the parent convention §"Phase-4 Template-Fill Commands" sub-section.

**H2 #3 — `## Ready-for-engineering test`** (one confirmation prompt):

- _"The seven-clause ready-for-engineering test is HANDOVERS-6's semantic gate. It is restated verbatim in the README so a reader of the folder can apply the test directly. Confirm the seven clauses are present and that you understand the packet is not actually ready for engineering until `/audit-completeness <slug>` and the named reviewer subagents pass."_

### Step 4 — surface human-owned decisions

Read the README's `human_owned_decisions:` list (pre-filled by F3.9 with the three HANDOVERS-6 canonical decisions: "Final fixed_vs_flexible classification", "Compliance review acceptance", "Engineering partner sign-off"). For each, ask the human to confirm the decision is owned by a named human. Update `approvals_obtained:` inline-list entries as the human dictates.

### Step 5 — lint the written README

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py` (do not assume cwd). Run `python3 <repo-root>/tools/lint-frontmatter.py delivery/handoff-packets/<slug>/README.md` (default mode).

**The lint covers `README.md` only.** The 22 child files are excluded: `requirements.yaml` is YAML (linter discovery skips it by extension); the 21 narrative children carry no frontmatter and retain placeholder body markers (the same exclusion pattern `/draft-initiative` uses for its five placeholder children).

- Exit 0: proceed to Step 6.
- Non-zero: surface the linter output; offer to re-open the relevant README sections for correction. If the human accepts and re-lint exits 0, proceed normally. If the human declines (or re-lint still fails), exit code 3 with the folder left on disk.

### Step 6 — emit the next-command hint

Last line of output, formatted exactly:

```
NEXT: /audit-completeness <slug>
```

`<slug>` is the Handoff Packet slug just created. No `REVIEW:` line is emitted (only `/sequence-initiative` emits a REVIEW interstitial).

## Exit codes

- `0` — folder instantiated, README walked and filled, linter passed, NEXT emitted.
- `1` — human aborted the interactive walk before Step 5 completed. The folder is left on disk in its partial state (the 22 children are present as placeholders from Step 2; the README is partially filled). Resume by re-running with the same slug and `--force`. No NEXT line.
- `2` — pre-conditions failed (malformed slug; destination exists without `--force`; template missing; candidate parent Initiative list empty; `--from` named a non-existent Initiative). Folder not written.
- `3` — folder written but post-fill linter exited non-zero on README and the human declined re-open (or re-open failed). Folder persists on disk in a known-imperfect state. Automation consumers MUST treat exit 3 as distinct from exit 0.

## What this command will not do

- Not overwrite an existing `delivery/handoff-packets/<slug>/` without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the parent Initiative lacks a referenced field, ask the human; do not invent.
- Not batch placeholder questions — one at a time, even within an H2.
- Not silently pick a parent Initiative when multiple candidates exist (or when only one exists — always confirm).
- Not assume the working directory is the repo root when invoking the linter.
- Not pre-fill the 22 child files with content extracted from the parent spec(s). Filling the children is the human's job, performed outside this command's interactive walk; `/audit-completeness <slug>` is the gate that reports which children still hold placeholders. **This is the load-bearing design decision.**
- Not declare the packet `Ready for Engineering` as a behavioral consequence of this command. The README's `status:` value remains the template-pre-filled string, but the four `*_review_passed:` audit-gate fields remain placeholders until the audits actually pass.
- Not pre-fill the four `*_review_passed:` audit-gate fields, `engineering_partner:`, or `fixed_vs_flexible:`. Those are audit-outcome / human-decision fields whose values must be set after the corresponding audits / decisions actually happen.
- Not run `/audit-completeness` itself. The chain hint names it; the human runs it next.
- Not run the `adversarial-reviewer` or `quality-engineer` subagents. The chain hint names `/audit-completeness` as the immediate next step; reviewer subagents are invoked separately by the human as part of the README's four `*_review_passed:` gate-fill workflow.
- Not walk the 22 child files interactively. Out of scope by design.
- Not modify `templates/handoff-packet/` from inside the command. The template is frozen by F3.9.

$ARGUMENTS
