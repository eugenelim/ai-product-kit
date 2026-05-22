---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: Opportunity Solution Tree
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
  - Selection of the chosen opportunity
  - What opportunities to explicitly exclude from the tree
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: <true | false>
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per docs/HANDOVERS.md §"Handover 2: Discovery → Validation")
outcome:
  id: <OUT-NNN>
  metric: <name>
  current: <value>
  target: <value>
  measurement: <how, where, by when>
opportunity_count: <total nodes>
chosen_opportunity:
  id: <OPP-NNN>
  rationale: <one paragraph>
---

# Opportunity Solution Tree

> <One-paragraph description of the OST artifact this instance represents. Cite docs/HANDOVERS.md §"Handover 2: Discovery → Validation".>

## The outcome

<The measurable outcome this tree pursues, tied to the parent intent's coherent action.>

## Opportunity space

<The tree of opportunities surfaced from discovery interviews.>

## The chosen one

<Why this opportunity, why now, and what we give up by choosing it.>

## Source opportunities

<Interview-level evidence under each tree node.>

## Excluded

<Opportunities considered and explicitly excluded, with reason.>

## Optional sections

Delete the heading and all unused sections below if none apply.
