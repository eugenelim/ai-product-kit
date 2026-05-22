---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: Feature
name: <human-readable name>
description: <one to three sentences>
owner: <named human or role>
status: Draft   # product-artifact track entry state; see CONVENTIONS.md §"Lifecycle states"
priority: <Low | Medium | High | Critical>
risk_level: <Low | Medium | High | Critical>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

# Traceability (per HANDOVERS.md row for this handover; delete fields that don't apply)
parent_initiative: <delivery initiative slug>
capabilities: [<CAP-NNN>, ...]
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
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per docs/HANDOVERS.md §"Handover 5: Initiative → Spec" and §"Handover 6: Spec → Engineering Handoff Packet")
# Per cross-cutting dedup convention: `parent_initiative` and `related_kpis` live in the universal-schema block above (they are universal-schema fields per docs/CONVENTIONS.md). `capabilities:` is a Handover-5-specific field placed in the traceability block above (co-located with sibling parent/related fields), not a universal-schema field.
---

# <Feature name>

> <One-paragraph description: what this Feature is, which Capability it delivers, which parent Initiative it sits under. Cite docs/HANDOVERS.md §"Handover 5" (parent manifest source) and §"Handover 6" (downstream Engineering Handoff Packet consumer).>

## Problem this spec addresses

<One paragraph: the specific customer or business issue this Feature addresses, scoped to this Feature only — not the parent Initiative's full problem statement. Cite the linked Problem id from the parent Initiative's capabilities.md.>

## Capabilities contributed to

<One paragraph: name the Capability id(s) this Feature contributes to. Ontology direction: Capability → Feature (decomposition).>

## User behaviour — current vs future

<One paragraph: how the user behaves today; one paragraph: how the user behaves after this Feature ships.>

## Functional requirements

<List: the behaviours the Feature must support. Each item is a Domain E Requirement object — assign a typed id (REQ-NNN) so it can be referenced by the parent Capability's traceability chain and aggregated into the downstream Handoff Packet's requirements.yaml.>

## Acceptance criteria

<List: one item per REQ-NNN above. Format each item as "REQ-NNN: <observable predicate that confirms the requirement is met>" so the downstream Handoff Packet's acceptance-criteria.md can aggregate per-requirement without re-mapping.>

## Non-functional requirements

<List: performance, reliability, security, accessibility, observability constraints.>

## Dependencies

<List: upstream Features (FEAT-NNN), Capabilities (CAP-NNN), or external systems this Feature depends on. Use typed ids so the downstream Handoff Packet's dependencies.md can cross-reference without re-triage.>

## Out of scope

<List: things this Feature explicitly does not do.>

## Open questions

<List: questions for engineering, design, legal, compliance, or human stakeholders to resolve.>

## Optional sections

Delete the heading and all unused sections below if none apply.

### Business rules

<When to use this section; what it contains.>
