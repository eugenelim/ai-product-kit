---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: Assumption Map
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
parent_opportunity: <OPP-NNN>
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
  - Selection of the riskiest assumption to test next
  - Acceptance of assumptions marked "accept-as-bet"
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: <true | false>
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per docs/HANDOVERS.md §"Handover 2.5: Discovery → Assumption Map")
assumptions:
  - id: <ASM-NNN>
    statement: <one sentence>
    lens: <desirability | viability | feasibility | usability | ethical>
    risk_if_wrong: <Low | Medium | High | Critical>
    evidence_today: <Strong | Moderate | Weak | None>
    test_priority: <1 | 2 | 3 | ...>
riskiest_assumption: <ASM-NNN>             # the one Validation will test next
---

# Assumption Map

> Assumption Map for the chosen Opportunity. Gates Handover 2.5 (Discovery → Assumption Map) per docs/HANDOVERS.md.

## The chosen opportunity

<One-paragraph restatement of the chosen Opportunity from Handover 2; link to the OST node at `discovery/trees/<slug>.md#<OPP-NNN>`.>

## Assumptions, by lens

<Every assumption underneath the opportunity, classified into the five-lens taxonomy (desirability / viability / feasibility / usability / ethical). Cite `context/frameworks/assumption-tests.md` *(planned — ROADMAP F4.4)* for definitions; until that framework ships, link to ontology Domain C entries for the named lenses.>

## Risk-vs-evidence ranking

<Each assumption plotted on (risk_if_wrong × evidence_today). The riskiest under-evidenced assumption is the next test target.>

## The riskiest assumption

<Restated; why it earned the rank; what we'd lose if it's wrong.>

## Accepted bets

<Assumptions the team explicitly chooses not to test (with rationale). These propagate to the Vision artifact's `open_assumptions:` block as tier `accept-as-bet`.>

## Optional sections

Delete the heading and all unused sections below if none apply.
