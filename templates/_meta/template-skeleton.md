---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: <pre-filled per template — e.g., Strategic Intent>
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
  - <decision a human must make personally>
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: <true | false>
approvals_obtained:
  - <role>: <YYYY-MM-DD>

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per docs/HANDOVERS.md row for this handover)
# Add fields from HANDOVERS.md that are required for this artifact type.
# Example for Strategic Intent: central_challenge, guiding_policy, coherent_actions, horizon.
---

<!-- Single-file template skeleton. For folder-based templates (Initiative,
Handoff Packet), the README.md carries this frontmatter; child files carry
their own frontmatter only when they instantiate a distinct ontology object.
See CONVENTIONS.md §"Templates" → "File layout"; F3.7 and F3.9 specs encode
the per-child decision. -->

# <Artifact name>

> One-paragraph description of what this artifact is and what handover it gates. Cite the HANDOVERS.md section.

## <Required section 1 from HANDOVERS.md>

<Placeholder body. One paragraph or list. The required sections are quoted verbatim from HANDOVERS.md for this handover.>

## <Required section 2 from HANDOVERS.md>

<...>

## <Required section N from HANDOVERS.md>

<...>

## Optional sections

Delete the heading and all unused sections below if none apply.

### <Optional section A>

<When to use this section; what it contains.>
