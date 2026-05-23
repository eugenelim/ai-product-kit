---
description: Draft a PM Spec under an existing Initiative — copy templates/pm-spec.md, walk it interactively, append a row to the parent's child-specs.md, lint the written file, and chain to /handoff-packet.
argument-hint: <slug> [--from <initiative-slug>] [--force]
---

# /draft-spec

> Artifact-creating Phase-4 template-fill command. Reads an active Initiative folder; copies `templates/pm-spec.md` to `delivery/initiatives/<initiative-slug>/specs/<slug>.md`; walks the template's ten H2 sections one at a time interactively; appends a row to the parent Initiative's `child-specs.md` manifest (the load-bearing side-effect that gates Handover 5 → Handover 6 traceability); runs `tools/lint-frontmatter.py` against the written file; emits `NEXT: /handoff-packet <handoff-packet-slug>`. Deviates from the convention's six-step Procedure with a seventh step that separates the `child-specs.md` append from the chaining-hint emit.

## When to run

- After a parent Initiative folder exists at `delivery/initiatives/<initiative-slug>/` with `child-specs.md` declaring at least one expected per-feature spec slug.
- When a single Feature within that Initiative is ready to gain its own per-feature PM-side contract (per-Feature granularity, not per-Capability).
- Before `/handoff-packet` runs against the Initiative — the Handoff Packet reads each PM Spec as its primary per-feature input.

## Inputs

1. The positional arg — `<slug>` (the new PM Spec's slug). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars.
2. `templates/pm-spec.md` — the F3.8 single-file template this command copies.
3. Parent artifact: an Initiative folder at `delivery/initiatives/<initiative-slug>/` whose `status:` is not `Deprecated`. Resolution rule below; `--from <initiative-slug>` for explicit selection (effectively required because the destination is initiative-nested).
4. `delivery/initiatives/<initiative-slug>/child-specs.md` — the manifest table this command appends to as a Step-6 side-effect.
5. Optional flag `--force` — permits overwriting an existing PM Spec at the destination.

## Procedure

### Step 1 — resolve parent Initiative

If `--from <initiative-slug>` is given, validate `delivery/initiatives/<initiative-slug>/` exists. If not, exit code 2 with: `"no Initiative folder found at delivery/initiatives/<initiative-slug>/ — run /draft-initiative <initiative-slug> first."`

Otherwise list candidates from `delivery/initiatives/` filtered by `status:` not in `{Deprecated}`, sorted by `last_updated:` descending, capped at 10. Present as a numbered list; ask the human to pick one (or re-run with `--from` for an older candidate). Never silently pick — always confirm, even when only one candidate exists.

If the candidate list is empty, exit code 2 with: `"no Initiative found in delivery/initiatives/ — run /draft-initiative <slug> first."`

### Step 2 — instantiate the template at the destination

Copy `templates/pm-spec.md` to `delivery/initiatives/<initiative-slug>/specs/<slug>.md`. If the destination file exists and `--force` is not set, exit code 2 with: `"delivery/initiatives/<initiative-slug>/specs/<slug>.md already exists — re-run with --force or pick a different slug."` If the `specs/` directory does not exist, create it (`mkdir -p`).

Pre-fill the mechanical frontmatter (the human is never asked for these):

- `id: FEAT-<NNN>` — scan `delivery/initiatives/*/specs/*.md` for Feature ids, take max + 1, zero-pad to three digits (or `001` if none exist).
- `slug:` — the positional argument.
- `created:` — today's date (ISO-8601, system clock at command start).
- `last_updated:` — same as `created`.
- `parent_initiative:` — the resolved Initiative slug from Step 1.
- `object_type: Feature` — re-assert (template already pre-fills; defensive check).
- `status: Draft` — re-assert.

If any mechanical field cannot be resolved, exit code 2 with the missing pre-condition surfaced.

### Step 3 — walk the PM Spec's H2 sections one at a time

Before walking the template body, ask the two `child-specs.md` row fields (these become side-effect inputs for Step 6, not PM Spec body content):

_"Which bounded context owns this spec? (See the parent Initiative's `context-map.md` for the candidate list.)"_

_"Which team owns this spec? (Free-text; e.g., 'Pricing', 'Checkout', 'Platform'.)"_

Then walk the template body in source order. One question per turn. Never batch. Confirm per-H2 before advancing.

- **Feature name (H1):** _"What is the human-readable name of this Feature? (One short phrase; will become the H1 of the PM Spec.)"_
- **Intro blockquote:** _"Write one paragraph: what this Feature is, which parent Initiative it sits under, and which Capability id(s) from the parent Initiative's `capabilities.md` it contributes to. I'll cite HANDOVERS §'Handover 5' and §'Handover 6' automatically."_
- **`## Problem this spec addresses`:** _"What is the specific customer or business issue this Feature addresses? Keep it scoped to this Feature only — the parent Initiative already holds the broader problem statement. Cite the linked Problem id from the parent Initiative's `capabilities.md`."_
- **`## Capabilities contributed to`:** _"Which Capability id(s) from the parent Initiative's `capabilities.md` does this Feature contribute to? (Ontology direction: Capability → Feature is decomposition; one Feature can contribute to one or more Capabilities.)"_
- **`## User behaviour — current vs future`:** Two prompts asked in sequence: _"Describe how the user behaves today, in one paragraph."_ then _"Describe how the user will behave after this Feature ships, in one paragraph."_
- **`## Functional requirements`:** Loop per Requirement until the human says `done`:
  - _"What is the next Functional Requirement this Feature must support? (One predicate per Requirement. Reply 'done' when no more remain.)"_
  - _"Assign this Requirement an id (REQ-NNN). The next unused id in this Initiative is REQ-<next-int>; press Enter to accept or type a different id."_
  - _"Which EARS pattern does this Requirement follow — Ubiquitous, Event-driven, State-driven, Optional, or Unwanted-behavior? (For reference; not linted in this command. The /ears-lint skill is planned per ROADMAP P4.7.)"_
- **`## Acceptance criteria`:** Per Requirement collected above: _"For REQ-<id>, write the observable predicate that confirms the Requirement is met. Format: 'REQ-NNN: <predicate>' — the downstream Handoff Packet's `acceptance-criteria.md` aggregates per-Requirement without re-mapping."_
- **`## Non-functional requirements`:** _"What non-functional requirements apply to this Feature? (Performance, reliability, security, accessibility, observability — one per line. Reply 'none' if no NFRs apply at per-Feature scope.)"_
- **`## Dependencies`:** _"What upstream Features (FEAT-NNN), Capabilities (CAP-NNN), or external systems does this Feature depend on? Use typed ids so the downstream Handoff Packet's `dependencies.md` can cross-reference without re-triage."_
- **`## Out of scope`:** _"What does this Feature explicitly NOT do? (Surface the dog that doesn't bark — it's often more informative than the in-scope list.)"_
- **`## Open questions`:** _"What questions remain for engineering, design, legal, compliance, or human stakeholders to resolve before this Feature can ship?"_
- **`## Optional sections` → `### Business rules`:** _"Are there business-logic rules beyond the Acceptance Criteria that this Feature must enforce? (Reply 'skip' to remove this optional section from the written file. Otherwise: one rule per line.)"_

### Step 4 — surface human-owned decisions

Read the written file's `human_owned_decisions:` list (pre-filled by F3.8). For each entry, ask the human for explicit confirmation. Record confirmations under `approvals_obtained:` in `<role>: <YYYY-MM-DD>` form.

### Step 5 — lint the written artifact

Resolve repo root as nearest ancestor of CWD containing `tools/lint-frontmatter.py`. Run `python3 <repo-root>/tools/lint-frontmatter.py delivery/initiatives/<initiative-slug>/specs/<slug>.md` (default mode).

- Exit 0: proceed to Step 6.
- Non-zero: surface the linter output; offer to re-open the relevant sections for correction. If the human accepts and re-lint exits 0, proceed normally. If the human declines (or re-lint still fails), exit code 3. **`child-specs.md` is NOT appended on exit 3** — the spec did not pass quality bar; do not pollute the manifest.

### Step 6 — append the row to `child-specs.md`

Read `delivery/initiatives/<initiative-slug>/child-specs.md`. Locate the manifest table (the first markdown table with header columns `spec slug | owning context | owning team | status | link`). If `<slug>` is already a row, do not duplicate — surface a warning and skip the append. Otherwise append: `<slug> | <owning-context> | <owning-team> | Draft | specs/<slug>.md`, using the values collected during the Step-3 pre-walk.

Update the parent Initiative `README.md`'s `last_updated:` to today's date.

### Step 7 — emit the next-command hint

Last line of output, formatted exactly:

```
NEXT: /handoff-packet <handoff-packet-slug>
```

`<handoff-packet-slug>` is a literal angle-bracket placeholder — the human supplies the packet slug when they invoke `/handoff-packet`. Append the prose annotation on the next line:

_"(If more PM Specs remain in this Initiative's child-specs.md, run `/draft-spec <next-slug> --from <initiative-slug>` first. `/handoff-packet` should only run when every row in `child-specs.md` has an instantiated PM Spec file. The handoff-packet slug is typically the same as the initiative slug for clarity, but the human chooses it.)"_

No `REVIEW:` line is emitted (only `/sequence-initiative` emits a REVIEW interstitial).

## Exit codes

- `0` — PM Spec written, linter passed, `child-specs.md` row appended (or skipped because the row already existed), parent Initiative README `last_updated:` bumped, NEXT hint emitted.
- `1` — human aborted the interactive walk before Step 5 completed. Partial PM Spec left on disk; `child-specs.md` NOT updated; README NOT bumped. Resume by re-running with the same `<slug>` and `--from <initiative-slug>`.
- `2` — pre-conditions failed (parent Initiative not found or `Deprecated`; `--from <initiative-slug>` resolves to a non-existent folder; candidate list empty; destination exists without `--force`; `child-specs.md` missing from parent; slug malformed).
- `3` — artifact written but post-fill linter exited non-zero, and the human declined or re-run failed. `child-specs.md` NOT appended (do not pollute the manifest with an unverified row). Artifact persists on disk in a known-imperfect state.

## What this command will not do

- Not write a PM Spec when the chosen parent Initiative's `status:` is `Deprecated`. Refuse via exit code 2 — writing a child to a deprecated parent is silent ontology drift.
- Not write a Functional-requirements row without an `id:` (REQ-NNN). The downstream Handoff Packet's `requirements.yaml` aggregates by `id:`; un-ided rows break the aggregation contract.
- Not skip the EARS-pattern fill prompt within Functional-requirements. The command does not lint the answer mechanically (`ears-lint` skill is planned per ROADMAP P4.7), but it surfaces the prompt so the eventual lint pass has well-formed input.
- Not overwrite an existing PM Spec at the destination without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the parent Initiative lacks a referenced Capability id, ask the human; do not invent.
- Not batch placeholder questions — one at a time, sequentially.
- Not silently pick a parent Initiative when multiple candidates exist (or when only one exists — always confirm).
- Not assume the working directory is the repo root when invoking the linter.
- Not run `/audit-spec-linkage` automatically (HANDOVERS-5's detector). The human runs it later, against the whole Initiative, after all PM Specs have been drafted.
- Not append to `child-specs.md` on exit 3 — the lint failed; do not pollute the manifest with an unverified row.
- Not bump the parent Initiative `README.md`'s `status:`. Only `last_updated:` is mutated; the Initiative's lifecycle is managed elsewhere.
- Not modify `templates/pm-spec.md`. The template is frozen by F3.8.

$ARGUMENTS
