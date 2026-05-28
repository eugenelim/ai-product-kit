---
description: Generates the first-pass Opportunity Solution Tree from a strategic intent and a cluster proposal. Writes BOTH `discovery/trees/<slug>.md` (human-readable, from `templates/ost.md`) AND `discovery/trees/<slug>.json` (the validator's projection) — the JSON is the source of truth for `scripts/validate_ost.py`, the markdown is the human surface. Builds the change set node-by-node from accepted clusters (each cluster → one Opportunity node, each member candidate's `IS-NNN` → an `add-source-opportunity` action), shells out to the validator against an empty `{"nodes": []}` seed, refuses to persist on validator non-clean, offers up to 5 repair rounds unconditionally. Emits `NEXT: /update-ost`. Phase 2 (Discovery), Handover-2 step 1 of 2 (`/update-ost` step 2 lets the human name `chosen_opportunity:`).
argument-hint: <slug> --from <intent-slug> [--from-clusters <clusters-slug>] [--force]
---

# /generate-ost

> Artifact-creating Phase-2 command. Produces the first-pass OST from a strategic intent and a clusters proposal. Dual-write: markdown (human-readable, per `templates/ost.md`) plus JSON projection (the validator's source of truth). Validator-gated — refuses to persist on `scripts/validate_ost.py` non-clean. The OST emitted here will typically NOT carry `chosen_opportunity:` yet — that's `/update-ost`'s job. Gates Handover 2 (Discovery → Validation) — the OST is the handover artifact.

## When to run

- After `/cluster-opportunities` has produced an accepted clustering proposal AND a parent strategic intent exists under `strategy/intents/`.
- When the team is ready to convert clustered candidates into a structured tree before the Validation phase.
- Once per strategic intent per cycle — subsequent updates use `/update-ost`, not re-generation.

## Inputs

1. The positional arg — `<slug>` (the OST's slug). Kebab-case, ≤ 80 chars.
2. `--from <intent-slug>` — required parent strategic intent. Resolves to `<repo-root>/strategy/intents/<intent-slug>.md`.
3. Optional `--from-clusters <clusters-slug>` — explicit clusters proposal at `<repo-root>/discovery/opportunities/clusters/<clusters-slug>.md`. If absent, resolves the most recent clusters file.
4. `<repo-root>/templates/ost.md` (F3.2) — the markdown OST template.
5. `<repo-root>/scripts/validate_ost.py` (P2.8) — the validator the command shells out to.
6. `<repo-root>/.claude/skills/ost-validator/references/ost-schema.json` — the JSON schema the validator enforces.
7. Optional `--force` flag — permits overwriting an existing `discovery/trees/<slug>.{md,json}`. Has NO effect on the repair loop (the loop is unconditional).

## Procedure

### Step 1 — resolve the parent strategic intent

Resolve `<repo-root>` as the nearest ancestor containing `tools/lint-frontmatter.py`.

`--from <intent-slug>` is required. Verify `<repo-root>/strategy/intents/<intent-slug>.md` exists and `status:` is not in `{killed, abandoned}`. If missing or terminal, exit code 2 with: `"strategic intent '<intent-slug>' not found or terminal — pick an active intent or run /strategic-intent first."`

If `--from` is absent (the human invoked the command without it), exit code 2 with: `"--from <intent-slug> is required — pick the strategic intent the OST will pursue."` (do NOT silently pick the most recent intent — strategy ownership is human-owned).

### Step 2 — resolve the clusters proposal

If `--from-clusters <clusters-slug>` is given, verify `<repo-root>/discovery/opportunities/clusters/<clusters-slug>.md` exists. Otherwise list active proposals under that directory, sorted by `last_updated:` descending, capped at 10; present numbered; ask the human to pick. Never silently pick.

**Zero-clusters case:** if `--from-clusters` is absent AND no clusters file exists, exit code 2 with: `"no clusters proposal found under discovery/opportunities/clusters/ — run /cluster-opportunities first."` Emit `NEXT: /cluster-opportunities` as the remediation hint on the last line of stderr. (The continuous-discovery framework permits generating an OST from raw snapshots without a clustering pass, but this command treats clusters as a soft prerequisite for predictability; a future flag — `--from-clusters none --from-snapshots ...` — can open the raw-snapshots path. Not in this batch.)

### Step 3 — instantiate the markdown OST from the template

The markdown destination is `<repo-root>/discovery/trees/<slug>.md`. The JSON destination is `<repo-root>/discovery/trees/<slug>.json`. If either exists and `--force` is not set, exit code 2 with the standard remediation hint.

Copy `<repo-root>/templates/ost.md` to the markdown destination. Pre-fill mechanical frontmatter:

- `id: OST-<NNN>` — scan `<repo-root>/discovery/trees/*.md` for `id: OST-`; max + 1, zero-padded.
- `slug:` — positional.
- `object_type: Opportunity Solution Tree` — re-assert (already in template).
- `parent_intent:` — the resolved intent slug.
- `created:`, `last_updated:` — today's ISO date.
- `status: Draft`.
- `outcome.id:` — pre-fill `OUT-001` (or scan existing OSTs and pick a unique id if there's a numbering convention; ask the human to confirm the id and the outcome's metric and target in Step 4).

### Step 4 — walk the OST H2 sections one at a time

Walk per `templates/ost.md` — outcome first, then opportunity space, then chosen one (typically deferred to `/update-ost`), then source opportunities, then excluded.

**H2 — The outcome.** Ask: _"What is the single product outcome this tree pursues? State as a measurable metric tied to the parent intent's coherent action. Cite `context/frameworks/opportunity-solution-tree.md` §'The four node types' — Outcome must be a product outcome the team can directly influence, not a business outcome two layers removed."_ Record outcome `id`, `name`, `metric`, `current`, `target`, `measurement`.

**H2 — Opportunity space.** **Promote each accepted cluster from the parent clusters file to one OST Opportunity node.** For each cluster:

1. Ask: _"Cluster `<cluster-name>` (rule: `<rule>`) — promote as Opportunity? If yes, restate the Opportunity in the customer's voice (one line)."_
2. The new Opportunity gets a fresh id `OPP-<NNN>` (scan within this in-progress tree for max + 1).
3. The cluster's member candidates' `evidence_basis:` references roll up — every member candidate's `IS-<NNN>` becomes a source for this Opportunity.
4. Solutions and Assumption Tests are NOT named at this step — they come later via `/update-ost`.

After all accepted clusters are promoted, ask: _"Any clusters from the unclustered bucket that warrant a standalone Opportunity in the tree? List one at a time."_

**H2 — The chosen one.** Ask: _"Is the team ready to name `chosen_opportunity:` now, or defer to `/update-ost`? The framework's `## Common failure modes` warns against premature commitment — surface ≥ 3 sibling Opportunities first."_ If deferred (the default), leave `chosen_opportunity:` empty. If named now, capture id + one-paragraph rationale.

**H2 — Source opportunities.** Already populated via Step 3's evidence_basis rollup. Render as a table under this H2 mapping each `IS-<NNN>` to the Opportunity it sources.

**H2 — Excluded.** Ask: _"Were any cluster's members explicitly rejected as Opportunities (Solutions masquerading; off-strategy; etc.)? List them with reason."_

### Step 5 — build the JSON projection and the change set; shell out to the validator

Build the JSON projection node-by-node from the walked H2 sections:

```json
{
  "outcome": {"id": "<OUT-NNN>", "name": "<name>", "metric": "<metric>"},
  "nodes": [
    {"id": "<OPP-NNN>", "type": "Opportunity", "name": "<name>", "parent": "<OUT-NNN>", "evidence_basis": ["<IS-NNN>", ...]},
    ...
  ]
}
```

If `chosen_opportunity:` was set in Step 4, add it to the JSON.

Build the change set — the action sequence that produced this tree from an empty seed. Order matters (the validator's consistency check walks actions in order):

```json
{
  "actions": [
    {"op": "add-outcome", "id": "<OUT-NNN>", "name": "<name>"},
    {"op": "add-opportunity", "id": "<OPP-001>", "name": "<name>", "parent": "<OUT-NNN>"},
    {"op": "add-source-opportunity", "id": "<IS-NNN>", "target": "<OPP-001>"},
    ...
  ]
}
```

Write the canonical empty seed `{"nodes": []}` to a `$(mktemp)`-created temp file. Write the projection JSON and the change-set JSON to temp files as well. Shell out:

```bash
python3 <repo-root>/scripts/validate_ost.py \
  --input <empty-seed-tmp-path> \
  --output <projection-tmp-path> \
  --change-set <change-set-tmp-path> \
  --format json
```

Clean up the empty-seed temp file regardless of validator outcome.

**Validator interpretation:**

- **Exit 0 (pass):** proceed to Step 6.
- **Exit 1 (rule violation):** parse the validator's JSON failure report from stderr. Present the violations to the human. **The repair loop is unconditional** — offer up to 5 repair rounds. Each round: ask the human to revise the walked H2 content based on the validator's remediation; rebuild the projection + change set; re-invoke the validator. If 5 rounds elapse without convergence, exit code 3 with the cumulative validator output; the markdown OST is NOT persisted to disk (rollback all temp files).
- **Exit 2 (input error):** the validator surfaces `reason: <malformed-json | schema-violation | change-set-inconsistent | ...>`. This is a bug in the projection or change-set construction. Exit code 3 with the validator's report; the command refuses to retry (the bug is on the command's side, not the human's).

### Step 6 — persist markdown + JSON

On validator pass, write:

- `<repo-root>/discovery/trees/<slug>.md` — the walked markdown (atomic write via `tmp + os.replace`-equivalent shell pattern).
- `<repo-root>/discovery/trees/<slug>.json` — the validated projection (atomic write).

Bump `last_updated:` on the markdown.

### Step 7 — lint the markdown OST + emit the next-command hint

Run `python3 <repo-root>/tools/lint-frontmatter.py <repo-root>/discovery/trees/<slug>.md`.

- Exit 0: proceed.
- Non-zero: offer to re-open relevant sections; exit code 3 if the human declines or re-runs still fail.

Last line of output: `NEXT: /update-ost <slug>`.

If the team set `chosen_opportunity:` in Step 4 (rare for first-pass generation, but allowed), alternatively emit `NEXT: /audit-discovery-coherence <slug>` (planned — P2.11) per the F4 chain convention.

## What this command will not do

- Not persist the OST if `scripts/validate_ost.py` returns non-clean after 5 repair rounds. The validator is the gate; bypassing it produces silent structural drift.
- Not auto-promote a cluster to an Opportunity. The human accepts each cluster explicitly in Step 4 — even though the cluster proposal was already accepted by `/cluster-opportunities`, the promotion to OST node is a second human acceptance.
- Not name `chosen_opportunity:` automatically. That is human-owned (per the OST framework's `## Common failure modes` warning against premature commitment).
- Not fabricate Opportunities not present in the parent clusters file. New Opportunities surface from unclustered candidates only via explicit human input in Step 4.
- Not assume the working directory is the repo root when invoking the linter or the validator.
- Not overwrite an existing OST without `--force` (and `--force` does NOT bypass the repair loop).
- Not chain a wedge skip — `/generate-ost` always emits NEXT to either `/update-ost` or `/audit-discovery-coherence`; the Validation phase is downstream of those, never skipped from here.
