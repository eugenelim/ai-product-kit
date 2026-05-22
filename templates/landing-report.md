---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: Landing Report
name: <human-readable name>
description: <one to three sentences>
owner: <named human or role>
status: Draft   # product-artifact track entry state; see CONVENTIONS.md §"Lifecycle states"
priority: <Low | Medium | High | Critical>
risk_level: <Low | Medium | High | Critical>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

# Traceability (per HANDOVERS.md row for this handover; delete fields that don't apply)
parent_vision: <delivery vision slug>
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
  - Verdict
  - Decision to revert, double-down, or fix
  - <decision a human must make personally>
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: <true | false>
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per docs/HANDOVERS.md §"Handover 7: Engineering → Landings")
# object_type, human_owned_decisions, human_approval_required: set in universal block above.
parent_handoff_packet: <handoff packet slug>
shipped: <YYYY-MM-DD>
measured_at: <YYYY-MM-DD>     # at least 30 days post-ship
verdict: <adopt | fix | kill>
verdict_at: <YYYY-MM-DD>
verdict_by: ["<name>: <YYYY-MM-DD>"]
---

# Landing Report

> This artifact is the Engineering → Landings handover; cite docs/HANDOVERS.md §"Handover 7: Engineering → Landings". The "measured_at" date must be at least 30 days after "shipped"; otherwise the report is premature.

## The shipped change

<One-paragraph recap of the shipped change. Cite the parent handoff packet and the shipped commit/PR.>

## Predicted outcomes vs actuals

<Table: KPI id, predicted threshold (from the parent Vision's predicted_outcomes), measured actual, delta, met-yes-no. Cite the Vision's predicted thresholds verbatim.>

## Adoption curve

<Visualization or table of adoption by cohort or surface, from shipped through measured_at. Note where the curve plateaus or rolls back.>

## Counter-metrics

<For each counter-metric KPI declared in the Vision, the measured value at measured_at. Did we break anything we said we were watching?>

## What landed and what didn't

<Surviving assumptions that did NOT hold up in production; then the ones that did. Tie each to a learning memo if available.>

## Verdict

<One of: adopt (move on), fix (named change), kill (rollback). Justify in one paragraph.>

## Feedback to strategy

<What this teaches for the next quarterly /strategy-refresh. Surface any contradictions with the parent intent's guiding policy.>

## Optional sections

Delete the heading and all unused sections below if none apply.
