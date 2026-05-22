---
# Experiment design phase. Frontmatter is the subset of the universal schema required by
# the linter (`object_type`, `status`, `last_updated`) plus the assumption-threshold-lock
# hook contract (predeclared_threshold, predeclared_at). The full universal schema lives
# on this folder's README.md.
object_type: Experiment
slug: <experiment-id>
name: <one-line experiment name>
description: <one to three sentences>
owner: <named human>
status: Draft
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

# Traceability
parent_opportunity: <discovery opportunity id>
parent_intent: <strategy intent slug>

# Human-vs-AI ownership
human_owned_decisions:
  - Threshold selection
  - Survived/killed call on ambiguous results
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: true
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Handover-specific fields (per assumption-threshold-lock hook contract)
parent_assumption: <ASM-NNN from the assumption map>
predeclared_threshold:
  success: <quantitative criterion>
  falsification: <quantitative criterion>
predeclared_at: <YYYY-MM-DD>
sample_target: <n>
duration: <days>
# Override-quad (uncomment ONLY when capturing results from a non-predeclared test — rare):
# override_threshold_lock: true
# override_reason: <one-paragraph explanation>
# override_authorized_by: <name>
# override_authorized_at: <YYYY-MM-DD>
---

# Experiment: <one-line name>

> Design phase for one Experiment instance. The `predeclared_threshold` and `predeclared_at` fields above are the load-bearing contract the `assumption-threshold-lock` hook polices against the sibling `results.md`. Cite docs/HANDOVERS.md §"Handover 3: Validation → Vision" for the upstream Validation Learning Memo that consumes this Experiment.

## The assumption tested

<One paragraph: restate the assumption from the parent Assumption Map; explain why it earned the riskiest rank.>

## The method

<One paragraph: how the experiment will be run — population, intervention, measurement, instrumentation.>

## Predeclared thresholds

<One paragraph: success criterion and falsification criterion in prose. Both must match the YAML `predeclared_threshold` block above.>

## Sample and duration

<One paragraph: target sample size, expected duration, statistical power if relevant.>

## Risks and ethical considerations

<One paragraph: what could go wrong; what user/legal/compliance risks need acknowledgement before running.>

## Disposition plan

<One paragraph: if the success criterion is met, what's the next step; if the falsification criterion is met, same.>

## Optional sections

Delete the heading and all unused sections below if none apply.
