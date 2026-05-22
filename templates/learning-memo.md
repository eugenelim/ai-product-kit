---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: Validation Learning Memo
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
parent_opportunity: <opportunity id>
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
  - Whether to survive or kill on ambiguous results
  - Whether to proceed to delivery given remaining open assumptions
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: true
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per docs/HANDOVERS.md §"Handover 3: Validation → Vision")
riskiest_assumption: <one sentence>
test:
  type: <desirability | viability | feasibility | usability | ethical>
  experiment: <path to validation/experiments folder>
  predeclared_threshold: <success criterion AND falsification criterion — restate verbatim from linked experiment.md>
  predeclared_at: <YYYY-MM-DD>
result:
  actual: <value>
  status: <survived | killed>
  decided: <YYYY-MM-DD>
  decided_by: <names>
---

# Validation Learning Memo

> This artifact records the outcome of testing a riskiest assumption — predeclared threshold, actual result, and survived-or-killed disposition. It is the load-bearing Validation → Vision handover (Handover 3 per `docs/HANDOVERS.md`). Copy to `validation/learnings/<slug>.md` to instantiate.

## The assumption tested

<One paragraph: restate the assumption under test; explain why it was selected as the riskiest — what the team would lose if it were wrong.>

## The test

<One paragraph: describe the experiment design, the predeclared success threshold, and the predeclared falsification criterion with the timestamp showing it was declared before results were collected.>

## The result

<One paragraph: state the actual measurement and compare it against both predeclared thresholds.>

## What we learned

<One paragraph: articulate what the team now knows as a result of the test, kept separate from the go/no-go disposition. Learning can be real even when the assumption is killed.>

## The disposition

<One paragraph: state whether the assumption survived or was killed. If survived, confirm the path forward to producing a Vision artifact. If killed, state whether the opportunity is returned to the OST or pruned.>

## Optional sections

Delete this heading if no optional sections apply. Add optional sections above this line if needed.
