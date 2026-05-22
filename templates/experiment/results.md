---
# Experiment results phase. Frontmatter is the subset of the universal schema required by
# the linter (`object_type`, `status`, `last_updated`) plus the HANDOVERS-3 `result:` block.
# Companion to `experiment.md` in this folder; the assumption-threshold-lock hook reads
# both files when validating a write to this path.
object_type: Experiment
slug: <same as experiment.md slug>
name: <one-line experiment name — match experiment.md>
status: Draft
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

# Sibling-file pointer (editorial; the hook discovers `experiment.md` via filesystem sibling lookup, not this field).
parent_experiment: experiment.md

# Human-vs-AI ownership
human_owned_decisions:
  - Whether to survive or kill on ambiguous results
  - Whether to proceed to delivery given remaining open assumptions
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: true

# Handover-specific fields (per docs/HANDOVERS.md §"Handover 3: Validation → Vision" — `result:` block verbatim)
# Note: `result.decided_by` serves as the approval record for this results file; `approvals_obtained:` is therefore omitted here (its role is taken by `decided_by` per HANDOVERS-3).
result:
  actual: <value>
  status: <survived | killed>
  decided: <YYYY-MM-DD>
  decided_by: <names>
---

# Experiment results: <one-line name>

> Results phase for the Experiment whose design lives in `experiment.md` in this same folder. The `result:` block above must be filled after the experiment runs. The `assumption-threshold-lock` hook rejects writes here whose `decided` timestamp predates the sibling `experiment.md` `predeclared_at:` value. Cite docs/HANDOVERS.md §"Handover 3: Validation → Vision".

## The result

<One paragraph: actual measurement vs predeclared thresholds. Did the success criterion fire? Did the falsification criterion fire?>

## What we learned

<One paragraph: what we now know as a result of this experiment, separate from the survived-or-killed decision. Learning can be real even when the assumption is killed.>

## The disposition

<One paragraph: survived → proceed to vision; killed → opportunity returned to OST or pruned. Cite the Validation Learning Memo this Experiment feeds.>

## Optional sections

Delete the heading and all unused sections below if none apply.
