---
description: Walk the change-type-aware launch checklist for an existing Handoff Packet — pick one of {new-feature, breaking-change, pricing, regulated}, copy the matching per-change-type template into the packet folder, walk the 10–13 items one at a time recording confirm/note/n-a per item, surface the human_owned_decisions, lint the written artifact, bump the packet README's last_updated, and chain to /landing-report.
argument-hint: <handoff-packet-slug> [--change-type new-feature|breaking-change|pricing|regulated] [--force]
---

# /launch-checklist

> Phase-4 post-ship operational-artifact command (Wave-4, P4.14). Reads an existing Handoff Packet (HANDOVERS-6); picks one of four change-type lenses (`new-feature` / `breaking-change` / `pricing` / `regulated`); copies the matching per-change-type template from `templates/launch-checklist/<change-type>.md` to `delivery/handoff-packets/<slug>/launch-checklist.md` as a sibling of the packet's `launch-considerations.md` narrative summary (the checklist **extends** the narrative — it does not duplicate or replace it). Walks the 10–13 items one at a time, recording per-item confirm / note / not-applicable with a free-text note. Lints the written artifact; bumps the parent packet README's `last_updated:`; emits `NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5.x)` followed by a one-line commentary surfacing `/retro` as the cadence-level successor after the landing report. Deviates from the F4 template-fill convention on four declared points (positional names the parent Handoff Packet not a new artifact; Step 3 walks per-item not per-H2; argv carries `--change-type` absent from the convention; no `id:` pre-fill).

## When to run

- After the parent Handoff Packet's four `*_review_passed:` audit-gate fields are filled (i.e., the packet is sealed for engineering); running on an unsealed packet is non-standard and surfaces a non-blocking warning.
- After engineering has named the launch window and the change-type for the release.
- Before the launch lever is pulled — the checklist is the operational gate that says "we have actually cleared the change-type-specific risks." The Landing Report (P5.x) is the post-launch verdict; the checklist is its pre-launch counterpart.

## Inputs

1. The positional arg — `<handoff-packet-slug>`. Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. Names an existing Handoff Packet folder at `delivery/handoff-packets/<handoff-packet-slug>/`. **The positional names the parent (the Handoff Packet), not a new artifact** — this deviates from the F4 template-fill convention's positional rule.
2. Optional flag `--change-type new-feature|breaking-change|pricing|regulated` — selects the per-change-type template. If absent, Step 2 asks the human interactively (one prompt, the four options listed verbatim).
3. Optional flag `--force` — permits overwriting an existing `delivery/handoff-packets/<slug>/launch-checklist.md`. Before overwriting, Step 2 surfaces the existing file's `[x]`-confirmed items and `approvals_obtained:` and asks the human to confirm the overwrite is intentional — silent destruction of prior confirmations is forbidden.
4. `templates/launch-checklist/<change-type>.md` — the per-change-type single-file template the command copies. Four files: `new-feature.md` (10 items), `breaking-change.md` (12 items), `pricing.md` (11 items), `regulated.md` (13 items).
5. `delivery/handoff-packets/<slug>/README.md` — the parent Handoff Packet's frontmatter. Read for `parent_initiative:`, `parent_vision:`, `status:`. Refuse if `status:` is `Deprecated`.
6. `delivery/handoff-packets/<slug>/launch-considerations.md` — the narrative one-pager the checklist extends. Read for citation context during the walk; checklist item prompts reference its three sections by name where applicable. **Change-type-conditional placeholder behaviour:** for `new-feature` / `pricing`, a placeholder-shaped `launch-considerations.md` is surfaced as a non-blocking warning. For `breaking-change` / `regulated`, it is a blocking prompt — these change types' items cite `launch-considerations.md` materially (deprecation timing, rollout cadence, customer-disclosure routing), and running the checklist against placeholders produces unconfirmable items at scale (checklist-theatre).
7. `delivery/handoff-packets/<slug>/risks.md` — read for risk-driven items (especially `breaking-change` and `regulated`).
8. `delivery/handoff-packets/<slug>/requirements.yaml` — read for REQ-NNN citation context (especially `regulated` policy-compliance items).
9. `tools/lint-frontmatter.py` — default-mode linter run against the written checklist artifact.

## Procedure

### Step 1 — resolve parent Handoff Packet

The positional argument names the packet directly; validate `delivery/handoff-packets/<handoff-packet-slug>/` exists. If not, exit code 2: `"no Handoff Packet found at delivery/handoff-packets/<handoff-packet-slug>/ — run /handoff-packet <slug> first."`

Read `delivery/handoff-packets/<handoff-packet-slug>/README.md`. If `status:` is `Deprecated`, exit code 2 with the missing pre-condition surfaced. If the four `*_review_passed:` audit-gate fields are placeholder-shaped, surface a non-blocking warning ("the parent Handoff Packet's audit gates are not all passed — running the launch checklist on an unsealed packet may be premature; continue?") and ask the human; proceed if yes.

Confirm the packet choice with the human even when the positional is explicit.

### Step 2 — pick the change-type and instantiate the template

If `--change-type` is absent, ask: _"Which change type is this launch? Choose one: `new-feature`, `breaking-change`, `pricing`, `regulated`. (Pick the lens most applicable; multi-type launches run the command once per type.)"_ The chosen value pins the template file.

For `--change-type breaking-change` or `--change-type regulated`: read `delivery/handoff-packets/<slug>/launch-considerations.md`. If the three H2 sections still hold angle-bracket placeholders, surface a **blocking prompt**: _"The parent packet's `launch-considerations.md` still holds placeholders. For a breaking-change/regulated launch, checklist items that cite it may be impossible to confirm accurately. Continue anyway? (yes/no)."_ Refuse if `no`.

For `--change-type new-feature` or `--change-type pricing`: a placeholder-shaped `launch-considerations.md` is a non-blocking warning only — log the warning and proceed.

If `delivery/handoff-packets/<slug>/launch-checklist.md` already exists and `--force` is set, **first** echo the existing file's `change_type:`, the list of `[x]`-confirmed items (with their indices), and the existing `approvals_obtained:` list. Ask: _"Confirm overwrite? The above per-item confirmations and approvals will be lost."_ Refuse on `no`. On `yes`, proceed.

If the destination exists and `--force` is **not** set, exit code 2: `"delivery/handoff-packets/<slug>/launch-checklist.md already exists — re-run with --force or pick a different slug."`

Copy `templates/launch-checklist/<change-type>.md` to `delivery/handoff-packets/<slug>/launch-checklist.md`. Pre-fill mechanical frontmatter (no `id:` — operational sibling artifact, identified by its containing folder, not by a typed id form):

- `slug:` — the parent packet's slug.
- `change_type:` — the resolved value.
- `created:`, `last_updated:` — today's date (ISO-8601, system clock at command start).
- `parent_handoff_packet:` — the resolved packet slug.
- `parent_initiative:`, `parent_vision:` — transitive carry-through from the packet README.
- `object_type: Launch Checklist` — re-assert (template pre-fills).
- `status: Draft` — re-assert.

### Step 3 — walk the checklist items, one at a time, never batched

For each numbered item in the chosen template's `## Checklist` H2, in source order:

1. Echo the item text verbatim.
2. Ask: _"Confirm, note, or mark not-applicable? Reply `confirm` to mark `[x]`; `note: <text>` to mark `[ ]` with an inline note explaining what's blocking; `n/a: <rationale>` to mark `[~]` with the rationale."_
3. Record the response inline in the written file: `[x]` for confirm, `[ ]` for note (with the note text indented two spaces under the item), `[~]` for not-applicable (with the rationale indented two spaces).
4. Echo the recorded line back to the human; advance to the next item only after confirmation.

Per-change-type item content is pinned by `templates/launch-checklist/<change-type>.md`; the command does not re-state items inline. Items that cite `launch-considerations.md` §sections include the citation in the echoed text.

### Step 4 — surface `human_owned_decisions:`

Read the written file's `human_owned_decisions:` list (pre-populated by the template — `pricing` lists "Pricing model sign-off" and "Grandfathering policy approval"; `regulated` lists "Legal/compliance sign-off" and "Named compliance-officer accountability"; `breaking-change` lists "Sunset date commitment" and "Rollback-or-stop-the-bleeding owner with paging contract"; `new-feature` lists "Beta cohort selection" and "Customer comms approval"). For each entry, ask the human to confirm the decision is owned by a named human and (where applicable) signed off. Record confirmations under `approvals_obtained:` in `<role>: <YYYY-MM-DD>` form.

### Step 5 — lint the written artifact

Resolve repo root as nearest ancestor of CWD containing `tools/lint-frontmatter.py`. Run `python3 <repo-root>/tools/lint-frontmatter.py delivery/handoff-packets/<slug>/launch-checklist.md` (default mode).

- Exit 0: proceed to Step 6.
- Non-zero: surface the linter output; offer to re-open. If re-lint exits 0, proceed normally. If the human declines (or re-lint still fails), exit code 3 — the parent packet README's `last_updated:` is **not** bumped on exit 3 (command success is a precondition for the bump).

### Step 6 — bump the parent packet README and emit the next-command hint

Bump `delivery/handoff-packets/<slug>/README.md`'s `last_updated:` field to today's date (ISO-8601). No other field on the packet README is touched; the parent Initiative `README.md` is **not** touched.

Last line of output, formatted exactly:

```
NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5.x)
```

Follow with a one-line commentary on a separate line: _"After the landing report is filed (measured at T+30d), run `/retro <slug>` for the team-process retrospective."_ This makes `/retro` (P4.15) discoverable as the cadence-level successor; the chain does not auto-invoke either command.

No `REVIEW:` line is emitted.

## Exit codes

- `0` — checklist written, all items walked and recorded, linter passed, packet README `last_updated:` bumped, NEXT emitted.
- `1` — human aborted mid-walk before Step 5 completed. Partial checklist file left on disk; packet README `last_updated:` **not** bumped. Resume by re-running with the same positional and `--change-type` plus `--force`.
- `2` — pre-conditions failed: slug malformed; packet not found; packet `status:` is `Deprecated`; destination exists without `--force`; `templates/launch-checklist/<change-type>.md` missing; `--change-type` flag had an invalid value; human refused the `breaking-change`/`regulated` placeholder-blocking prompt; human refused the `--force` overwrite-loses-confirmations prompt.
- `3` — file written but post-fill linter exited non-zero and human declined re-open. File persists on disk in known-imperfect state; packet README `last_updated:` **not** bumped.

## What this command will not do

- Not pre-fill checklist items with `[x]` confirmations from the packet's frontmatter. **Load-bearing design decision** — the artifact's value is the per-item human walk; pre-filled confirmations destroy the artifact's purpose.
- Not touch `launch-considerations.md` from inside this command. The narrative one-pager is owned by F3.9; the checklist extends it but does not write to it.
- Not run `/landing-report` automatically as part of this command's success path. The chain hint names it; the human runs it next.
- Not modify `templates/launch-checklist/` at runtime. The four per-change-type templates are frozen by this command's spec (Task 0).
- Not add a new ontology type at runtime. `Launch Checklist` is added by the spec's ontology extension (P4.14 EXECUTE phase); ad-hoc additions are forbidden.
- Not silently pick a change-type when `--change-type` is absent. Always ask.
- Not silently overwrite an existing `launch-checklist.md` with `--force` — first surface the existing confirmations and approvals and ask the human to confirm the overwrite.
- Not silently overwrite without `--force` at all.
- Not skip the `human_owned_decisions:` confirmation step.
- Not batch placeholder questions — one item at a time, sequentially.
- Not assume the working directory is the repo root when invoking the linter.
- Not bump the parent Initiative `README.md`. Only the packet's `README.md` `last_updated:` is bumped.
- Not bump the packet README on exit 1, 2, or 3.
- Not add a fifth change-type lens beyond the four pinned without an explicit spec amendment.

$ARGUMENTS
