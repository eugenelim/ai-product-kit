---
description: Draft a Vision artifact under delivery/visions/ from a surviving learning memo — walk the six HANDOVERS-4 sections interactively one at a time, pre-fill mechanical metadata, lint the result, and chain to /draft-initiative.
argument-hint: <slug> [--from <learning-slug>] [--force]
---

# /draft-vision

> Artifact-creating Phase-4 template-fill command. Reads a surviving learning memo from `validation/learnings/`; copies `templates/vision.md` to `delivery/visions/<slug>.md`; walks the six HANDOVERS-4 H2 sections (and the three H3 tier sub-units under "What we're still betting on") one at a time interactively; pre-fills mechanical frontmatter (`id: VIS-<NNN>`, slug, created, last_updated, parent_learning, parent_intent, object_type, status); runs `tools/lint-frontmatter.py` against the written file; emits `NEXT: /draft-initiative <initiative-slug>`. Gates Handover 4 (Vision → Initiative).

## When to run

- After a learning memo's `status:` flips to `survived` and the team is ready to translate the surviving learning into a customer-shaped Vision.
- Before `/draft-initiative` — HANDOVERS-4's `parent_vision:` field on every Initiative depends on this artifact existing.
- When a new strategic intent has been refreshed and the Validation→Delivery handover artifact is missing.

## Inputs

1. The positional arg — `<slug>` (the new Vision's slug). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars.
2. `templates/vision.md` — the F3.6 single-file template this command copies.
3. Parent artifact: a learning memo at `validation/learnings/<learning-slug>.md` with `status: survived`. Resolution rule below; `--from <learning-slug>` for explicit selection.
4. Optional flag `--force` — permits overwriting an existing `delivery/visions/<slug>.md`.

## Procedure

### Step 1 — resolve the parent learning memo

If `--from <learning-slug>` is given, verify `validation/learnings/<learning-slug>.md` exists and its `status:` is not `killed`. If the file is missing OR the status is `killed`, exit code 2 with the message: `"learning memo '<slug>' has status: killed; a Vision cannot be drafted from a killed learning. Pick a memo with status: survived or re-run /learning-memo to capture a new learning."`

Otherwise list candidate memos in `validation/learnings/` whose `status:` is not in the terminal-or-killed set `{killed}`. Sort by `last_updated:` descending; cap at 10. Present as a numbered list; ask the human to pick one (or specify `--from` for an older candidate). Never silently pick — always confirm, even when only one candidate exists.

If the candidate list is empty, exit code 2 with: `"no learning memo found in validation/learnings/ with status: survived. Run /learning-memo first, then re-run /draft-vision <slug>."`

### Step 2 — instantiate the template at the destination

Copy `templates/vision.md` to `delivery/visions/<slug>.md`. If the destination already exists and `--force` is not set, exit code 2 with: `"delivery/visions/<slug>.md already exists — re-run with --force to overwrite, or pick a different slug."`

Pre-fill the mechanical frontmatter (the human is never asked for these):

- `id: VIS-<NNN>` — scan existing files for `id: VIS-` lines, take max + 1, zero-pad to three digits.
- `slug:` — the positional argument.
- `created:` — today's date (ISO-8601, system clock at command start).
- `last_updated:` — same as `created`.
- `parent_learning:` — the resolved learning slug from Step 1.
- `parent_intent:` — read from the chosen learning memo's `parent_intent:` field. If empty, ask the human for the slug and surface the missing link as an open question on the Vision.
- `object_type: Vision` — re-assert (already in template; defensive check).
- `status: Draft` — re-assert.

### Step 3 — walk the six H2 sections one at a time

Walk these prompts in order. One question per turn. Never batch. Confirm the section's filled content before advancing.

**H2 1 — The customer-shaped pitch.** _"In one paragraph, narrative voice: who is the customer, what problem are they hitting, and how does this change land in their words? Draw on the surviving learning memo `<parent-learning-slug>` — paraphrase the customer language verbatim where you can."_

**H2 2 — The change.** _"In one paragraph: what is different for the customer when this ships? Name the before-state and the after-state in the customer's own frame — not in feature language."_

**H2 3 — What we believe and why.** _"In one paragraph: which beliefs anchor this Vision, and which learning memos anchor each belief? Cite the memo slugs inline (e.g., `validation/learnings/<slug>.md`). Beliefs without a cited memo are surfaced as Open Assumptions in the next section, not here."_

**H2 4 — What we're still betting on.** Three H3 tier sub-units, walked in order. Each H3 is its own fill unit; confirm each before advancing. Do not advance to H2 5 until all three H3s are confirmed.

- *H3 4a — must-test-before-shipping:* _"What's the riskiest assumption that, if wrong, kills the Vision and must be tested before any shipping? One assumption per line. Each one becomes a `tier: must-test-before-shipping` entry in `open_assumptions:`. If there are none, say 'none' — I'll record an empty list and we move on."_
- *H3 4b — accept-as-bet:* _"What assumptions are you accepting as bets — explicitly known-uncertain, but you're choosing to commit and learn on the way? One per line. Each one becomes a `tier: accept-as-bet` entry."_
- *H3 4c — will-monitor-post-ship:* _"What assumptions will you watch in production but not test pre-ship? One per line. Each one becomes a `tier: will-monitor-post-ship` entry."_

**H2 5 — Counter-metrics.** _"In one paragraph: which metrics would tell us we made the product worse, not better? For each counter-metric, give me the KPI id (format `KPI-NNN` per the ontology). If the KPI doesn't yet have an id, say so — I won't fabricate one; you create the KPI separately and we link it back."_

**H2 6 — Predicted outcomes.** _"In one paragraph: what does success look like, and how will you measure it? For each predicted outcome, give me three values: the KPI id (`KPI-NNN`), the threshold (the numeric or qualitative bar that counts as success), and the measure-at horizon (weeks-after-launch). If you don't have the KPI ids yet, name the metric in prose and I'll surface 'KPI id needed' as an open item — I won't invent ids."_

### Step 4 — surface human-owned decisions

Read the written file's `human_owned_decisions:` list (pre-filled by F3.6 with the three HANDOVERS-4 entries verbatim: "Customer-shaped framing of the value proposition", "Differentiator selection", "Predicted outcome thresholds"). For each entry, ask the human for explicit confirmation that the decision is owned and named. Record the confirmations under `approvals_obtained:` in `<role>: <YYYY-MM-DD>` form.

### Step 5 — lint the written artifact

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py` (do not assume cwd is the repo root). Run `python3 <repo-root>/tools/lint-frontmatter.py delivery/visions/<slug>.md` (default mode, NOT `--check-template`). Report the result.

- Exit 0: proceed to Step 6.
- Non-zero: surface the linter output; offer to re-open the relevant sections for correction. If the human accepts and re-lint exits 0, proceed normally. If the human declines (or re-lint still fails), exit code 3 with the artifact left on disk.

### Step 6 — emit the next-command hint

Last line of output, formatted exactly:

```
NEXT: /draft-initiative <initiative-slug>
```

`<initiative-slug>` is a literal angle-bracket placeholder — the Vision draft does not pre-determine the Initiative slug. No `REVIEW:` line is emitted (only `/sequence-initiative` emits a REVIEW interstitial, per the convention).

## Exit codes

- `0` — Vision written, linter passed, NEXT emitted.
- `1` — human aborted the Step-3 walk before completion. Partial artifact left at `delivery/visions/<slug>.md`; resume by re-running `/draft-vision <slug>`.
- `2` — pre-conditions failed (no candidate learning memo, malformed slug, destination exists without `--force`, `--from` names a `killed` or non-existent memo, mechanical pre-fill cannot be resolved).
- `3` — Vision written but post-fill linter exited non-zero and human declined re-open (or re-open failed). Artifact persists in a known-imperfect state.

## What this command will not do

- Not overwrite an existing `delivery/visions/<slug>.md` without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the chosen learning memo lacks a referenced field, ask the human; do not invent.
- Not batch placeholder questions — one at a time, sequentially.
- Not silently pick a parent learning memo when multiple candidates exist (and not silently pick when only one exists either — always confirm).
- Not assume the current working directory is the repo root when invoking the linter.
- Not write a Vision when the chosen learning memo's `status:` is `killed`. Refuse via exit code 2; the Validation→Vision causal chain requires a surviving learning.
- Not fabricate `predicted_outcomes[*].kpi_id` or `counter_metrics[*].kpi_id` values. KPI ids are human-owned per HANDOVERS-4; if the human doesn't have the id, record "KPI id needed" as an open item, not a synthesized `KPI-001`.
- Not auto-invoke `/draft-initiative` after writing the Vision. The chain is human-driven; the NEXT line is a hint, not a dispatch.
- Not modify `templates/vision.md`. The template is frozen by F3.6.

$ARGUMENTS
