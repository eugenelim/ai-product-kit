---
description: Themes the candidate Opportunities in a `/extract-opportunities` batch file into clusters by dispatching the `opportunity-clustering` skill. The skill returns proposed clusters (each anchored by one of three named rules — shared customer behavior, shared workflow step, shared workaround pattern) plus an `unclustered:` bucket; this command walks each proposed cluster one at a time and asks the human to accept / revise / reject. Rejected clusters' members move to `unclustered:`. Writes the clustering proposal at `discovery/opportunities/clusters/<slug>.md`. Exits 2 with a NEXT remediation hint when the parent batch is empty. Never auto-promotes a cluster to an OST Opportunity (that's `/generate-ost`'s job, gated by human acceptance). Phase 2 (Discovery).
argument-hint: <slug> [--from <batch-slug>] [--force]
---

# /cluster-opportunities

> Artifact-creating Phase-2 command. Reads a candidate-Opportunity batch from `/extract-opportunities` and produces a thematic clustering proposal at `discovery/opportunities/clusters/<slug>.md`. The clustering is doctrine-driven — dispatches the `opportunity-clustering` skill, then walks each proposed cluster interactively with the human. Feeds `/generate-ost` (P2.7): each accepted cluster becomes one OST Opportunity node downstream, with the cluster's member candidates' `evidence_basis:` rolling up to that Opportunity.

## When to run

- After `/extract-opportunities` has produced a batch with ≥ 6 candidates (clustering small lists isn't synthesis; the P2.5 skill surfaces this as a "When this skill is wrong" condition).
- When a parking-lot file of Opportunity candidates has accumulated over weeks and the team wants to see what themes have built up.
- Before `/generate-ost` — the OST's "Opportunity space" is populated by promoting accepted clusters.

## Inputs

1. The positional arg — `<slug>` (the clustering proposal's slug). Kebab-case; default convention: today's date.
2. `<repo-root>/.claude/skills/opportunity-clustering/SKILL.md` (P2.5) — the canonical rule library the command dispatches.
3. Optional `--from <batch-slug>` — explicit parent batch (a file at `<repo-root>/discovery/opportunities/<batch-slug>.md`). If absent, resolves the most recent batch via the F4 candidate-listing rule.
4. Optional `--force` flag — permits overwriting an existing clustering proposal.

## Procedure

### Step 1 — resolve the parent candidate batch

Resolve `<repo-root>` as the nearest ancestor containing `tools/lint-frontmatter.py`.

If `--from <batch-slug>` is given, verify `<repo-root>/discovery/opportunities/<batch-slug>.md` exists. If missing, exit code 2 with: `"opportunity batch '<batch-slug>' not found — run /extract-opportunities first or pick an existing batch."`

Otherwise list candidate batches under `<repo-root>/discovery/opportunities/*.md` whose `status:` is not in the terminal-or-killed set, sorted by `last_updated:` descending, capped at 10. Present as a numbered list; ask the human to pick (or specify `--from` for an older candidate). Never silently pick — always confirm.

**Empty-batch case (the F4 skeleton's Step 1 empty-list contract):** if the candidate-batch list is empty, exit code 2 with: `"no candidate batch found under discovery/opportunities/ — run /extract-opportunities first."` Emit `NEXT: /extract-opportunities` as the remediation hint on the last line of stderr.

**Few-candidates case:** read the chosen batch's candidate count. If < 6 (matching the `## When to run` trigger above), exit code 2 with: `"batch <slug> has only N candidates — clustering fewer than 6 is rarely meaningful synthesis (per the opportunity-clustering skill's 'When this skill is wrong' condition AND the `## When to run` ≥ 6 trigger). Interview more, wait for more snapshots, or re-run with --force to override."` The `--force` flag overrides this guard in addition to its file-overwrite role.

### Step 2 — instantiate the proposal file

The destination is `<repo-root>/discovery/opportunities/clusters/<slug>.md`. If it exists and `--force` is not set, exit code 2 with the standard remediation hint.

Pre-fill frontmatter:

- `id: OPCL-<NNN>` — scan existing proposals for `id: OPCL-`; max + 1, zero-padded.
- `slug:` — the positional argument.
- `object_type: Opportunity | Adapted` — kit-composite escape hatch (H1 names it "Opportunity Clusters").
- `parent_batch: <batch-slug>` — the resolved batch.
- `created:`, `last_updated:` — today's ISO date.
- `status: Draft`.

### Step 3 — dispatch the `opportunity-clustering` skill against the candidate list

Load the P2.5 skill (`.claude/skills/opportunity-clustering/SKILL.md`). Construct the input block from the resolved batch's candidates:

```yaml
candidates:
  - id: OPP-CAND-<NNN>
    statement: "<from the candidate's H3 heading>"
    evidence_basis: [IS-<NNN>, IS-<NNN>, ...]
  # ...
```

Pass to the skill. Receive the proposal block: a list of clusters (each with `name`, `rule`, `members`, `rationale`) plus an `unclustered:` bucket.

### Step 4 — walk each proposed cluster one at a time

For each cluster in the skill's proposal, ask the human one question per cluster (never batch):

_"Cluster `<name>` (rule: `<rule>`) contains members `<member-id-list>`. Rationale: `<rationale>`. Accept / revise / reject?"_

- **Accept:** the cluster as proposed enters the proposal file's `clusters:` list.
- **Revise:** ask follow-up questions to refine — rename, change rule, move members in/out. The revised cluster enters the proposal.
- **Reject:** the cluster's members move to the `unclustered:` list with `reason: <human's stated reason>`.

After all clusters are walked, surface the `unclustered:` bucket (carrying both the skill's original unclustered candidates AND the rejected clusters' members). Ask: _"Review the unclustered list — any candidates here that should be Solutions, not Opportunities? Any that should be parked for follow-up interviews?"_ Record dispositions inline as `reason:` per item.

### Step 5 — surface human-owned decisions

Present the proposal's `human_owned_decisions:`:

- Accept clusters or revise them.
- Decide whether unclustered candidates are real Opportunities or should be parked.
- Decide which clusters to promote into the OST downstream (`/generate-ost`'s job; the human will name them again there).

Ask for explicit acknowledgement.

### Step 6 — lint the written artifact

Run `python3 <repo-root>/tools/lint-frontmatter.py <repo-root>/discovery/opportunities/clusters/<slug>.md`.

- Exit 0: proceed.
- Non-zero: offer to re-open relevant sections; exit code 3 if the human declines or re-runs still fail.

### Step 7 — emit the next-command hint

Last line of output: `NEXT: /generate-ost <slug-or-intent>`.

## What this command will not do

- Not auto-promote a cluster to an OST Opportunity. The P2.5 skill's no-auto-promote rule is doctrine; the human accepts each cluster, and even then the promotion to OST nodes is `/generate-ost`'s explicit job, gated by another human-acceptance step.
- Not force-cluster candidates with no shared anchor. Per the P2.5 skill's `unclustered:` bucket — candidates without a shared anchor stay unclustered; do not invent a cluster to make the output tidier.
- Not edit candidate text. Clusters group; they do not rewrite the underlying candidates.
- Not redefine what an Opportunity is. The framework owns that.
- Not invent a fourth grouping rule beyond the three the skill names (shared customer behavior, shared workflow step, shared workaround pattern).
- Not run when fewer than 3 candidates are in the parent batch.
- Not overwrite an existing proposal without `--force`.
- Not batch placeholder questions — one cluster at a time.
- Not assume the working directory is the repo root when invoking the linter.
