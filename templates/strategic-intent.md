---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: Strategic Intent
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
parent_learning: <validation learning slug>
parent_vision: <delivery vision slug>
parent_initiative: <delivery initiative slug>
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
  - Whether to pursue this central challenge
  - Resource commitment behind coherent actions
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: true
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per docs/HANDOVERS.md row for this handover)
# Add fields from HANDOVERS.md that are required for this artifact type.
mode: <greenfield | enterprise>
central_challenge: <one sentence>
guiding_policy: <one paragraph>
coherent_actions:
  - <action 1>
  - <action 2>
  - <action 3>
  # 3-5 items, no more
horizon: <quarters>
business_objective: <linked Business Objective id>
parent_diagnosis: <path to diagnosis>
---

# Strategic Intent

> <One-paragraph description of the Strategic Intent this instance carries. This artifact is the Strategy → Discovery handover; cite docs/HANDOVERS.md §"Handover 1: Strategy → Discovery".>

## The challenge

<What specifically must be addressed; cite evidence — numbers, quotes, market signal.>

## The guiding policy

<What kind of response we commit to; what we are not responding with.>

## Coherent actions

<3-5 actions that reinforce each other; for each, name what it commits and what it forecloses.>

## Coherence check

<Explicitly check pairs of actions and confirm they don't cancel out.>

## Open questions for discovery

<What we don't know that discovery will address.>

## Optional sections

Delete the heading and all unused sections below if none apply.
