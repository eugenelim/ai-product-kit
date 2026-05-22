---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: Experiment
name: <human-readable name>
description: <one to three sentences>
owner: <named human or role>
status: Draft   # product-artifact track entry state; see CONVENTIONS.md §"Lifecycle states"
priority: <Low | Medium | High | Critical>
risk_level: <Low | Medium | High | Critical>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

# Traceability (per HANDOVERS.md row for this handover; delete fields that don't apply)
parent_intent: <strategy intent slug>
parent_opportunity: <discovery opportunity id>
related_problems: [<id>, ...]
related_personas: [<id>, ...]
related_kpis: [<id>, ...]

# Evidence vs assumption
evidence_basis:
  - source: <interview | ticket | metric | market-signal>
    strength: <Strong | Moderate | Weak>
    link: <path or url>
open_assumptions: [<text>, ...]

# Human-vs-AI ownership
human_owned_decisions:
  - Threshold selection
  - Survived/killed call on ambiguous results
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: true   # pre-filled: experiments always require human approval (the survived/killed call is a human_owned_decisions item — see above)
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per docs/HANDOVERS.md §"Handover 3: Validation → Vision")
# This folder scaffolds the Experiment artifact pair that the Validation Learning Memo's `test.experiment:` link resolves to.
# Child files: experiment.md (design phase), results.md (results phase). Names are pinned by the assumption-threshold-lock hook regex.
---

# Experiment

> This folder is the Experiment artifact for a single Validation test. It contains `experiment.md` (the design — predeclared thresholds, sample, duration) and `results.md` (the result — actual value, survived/killed disposition). The Validation Learning Memo (Handover 3 per `docs/HANDOVERS.md`) links here via its `test.experiment:` field. The `assumption-threshold-lock` hook (see `.claude/hooks/assumption-threshold-lock.md`) enforces two checks on writes to `results.md`: (a) `experiment.md` exists with a non-empty `predeclared_threshold:` map and a `predeclared_at:` value that parses as a valid YYYY-MM-DD date and is not in the future; and (b) the `experiment.md` file's filesystem mtime predates the `results.md` write event by ≥ 1 second. The hook does NOT read any in-file timestamp from `results.md` — the predeclaration ordering is enforced via OS mtime, not via a timestamp field in `results.md`.

## What this folder is

<One paragraph: the Experiment instance this folder represents — the assumption tested, who owns it, and the Validation Learning Memo it feeds. The folder name is the experiment id; the two child files together form one Experiment artifact.>

## How to use this template

<Copy the folder to `validation/experiments/<id>/` (the path the `assumption-threshold-lock` hook scans). Fill `experiment.md` before running the experiment; the hook records `predeclared_at:` as the lock. Fill `results.md` after the experiment runs; the hook rejects writes whose `decided` timestamp predates `predeclared_at:`.>

## Optional sections

Delete the heading and all unused sections below if none apply.
