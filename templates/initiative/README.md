---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: Initiative
name: <human-readable name>
description: <one to three sentences>
owner: <named human or role>
status: <active | paused | done>   # HANDOVERS §"Handover 5" enum, overriding the universal CONVENTIONS.md §"Lifecycle states" set; see body callout + spec OQ1
priority: <Low | Medium | High | Critical>
risk_level: <Low | Medium | High | Critical>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

# Traceability (per HANDOVERS.md row for this handover; delete fields that don't apply)
parent_intent: <strategy intent slug>
parent_vision: <vision slug>
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
  - Bounded-context ownership assignment
  - Build vs buy decisions in the evolution check
  - Delivery sequencing
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: <true | false>
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per HANDOVERS.md Handover 5)
crosses_repos: [<repo>, <repo>]
crosses_teams: [<team>, <team>]
capabilities: [<CAP-NNN>, ...]
context_map_signed_off: <YYYY-MM-DD>
sign_off_by: [<names>]
---

# Initiative

> This is an Initiative — a Strategic body of work per `context/frameworks/ontology.md` Domain D. The folder is the load-bearing artifact for Handover 5 (Initiative → Spec); see `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" for the canonical contract this README and its five sibling child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) implement. **Known issue:** `status:` above uses HANDOVERS-5's `active | paused | done` enum, which is not in `docs/CONVENTIONS.md` §"Lifecycle states" — concrete values fail the default-mode linter on instantiation. Tracked under `docs/specs/template-initiative/spec.md` §"Open questions" Q1.

## What this initiative is <!-- source: inferred (folder-index orientation) -->

<One paragraph restating the parent Vision's `change` field, scoped to what this Initiative delivers. Cite the parent Vision by slug (matches `parent_vision:` in the frontmatter above).>

## Scope and bounded contexts <!-- source: inferred (folder-index orientation) -->

<One paragraph naming the bounded contexts this Initiative crosses. Defer the full per-context detail (owner, public contract, Wardley evaluation, evolution stage) to [`context-map.md`](./context-map.md).>

## Delivery sequencing <!-- source: inferred (folder-index orientation) -->

<One paragraph naming the first-shippable subset and the dependency-driving spec. Defer the full spec manifest to [`child-specs.md`](./child-specs.md) and the dependency DAG to [`sequence.md`](./sequence.md).>

## Optional sections

Delete the heading and all unused sections below if none apply.

### Cross-team risk register

<When to use this section; what it contains.>
