---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: Vision
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
parent_learning: <validation learning slug>
related_problems: [<id>, ...]
related_personas: [<id>, ...]
related_kpis: [<id>, ...]

# Evidence vs assumption
evidence_basis:
  - source: <interview | ticket | metric | market-signal>
    strength: <Strong | Moderate | Weak>
    link: <path or url>
open_assumptions:
  - assumption: <text>
    tier: <must-test-before-shipping | accept-as-bet | will-monitor-post-ship>

# Human-vs-AI ownership
human_owned_decisions:
  - Customer-shaped framing of the value proposition
  - Differentiator selection
  - Predicted outcome thresholds
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: <true | false>   # HANDOVERS-4 requires `true` on instantiated Visions; the wrapper here is for --check-template compliance
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per docs/HANDOVERS.md §"Handover 4: Vision → Initiative")
crosses_teams: <true | false>
predicted_outcomes:
  - kpi_id: <KPI-NNN>
    threshold: <value>
    measure_at: <weeks-after-launch>
counter_metrics:
  - kpi_id: <KPI-NNN>
---

# Vision

> <One-paragraph customer-shaped description of the Vision this instance carries. Gates Handover 4 (Vision → Initiative); cite docs/HANDOVERS.md §"Handover 4: Vision → Initiative".>

## The customer-shaped pitch

<One paragraph in narrative voice, persona-aware, drawing on the surviving learning memo.>

## The change

<One paragraph: what's different for the customer.>

## What we believe and why

<One paragraph: cite the learning memos that anchor each belief.>

## What we're still betting on

<One paragraph: open assumptions tiered as must-test-before-shipping, accept-as-bet, or will-monitor-post-ship.>

## Counter-metrics

<One paragraph: what we'd watch to know we made it worse.>

## Predicted outcomes

<One paragraph: what success looks like; measurement plan.>

## Optional sections

Delete the heading and all unused sections below if none apply.
