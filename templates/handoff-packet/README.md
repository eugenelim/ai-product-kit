---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: Handoff Packet
name: <human-readable name>
description: <one to three sentences>
owner: <named human or role>
status: Ready for Engineering
priority: <Low | Medium | High | Critical>
risk_level: <Low | Medium | High | Critical>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

# Traceability (per HANDOVERS.md row for this handover; delete fields that don't apply)
parent_intent: <strategy intent slug>
parent_vision: <vision slug>
parent_initiative: <slug>
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
  - Final fixed_vs_flexible classification
  - Compliance review acceptance
  - Engineering partner sign-off
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: <true | restricted | not-allowed>
human_approval_required: <true | false>
approvals_obtained: ["<role>: <YYYY-MM-DD>"]   # inline-list form: the kit's frontmatter parser cannot key-extract `<role>` in block-list form

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per HANDOVERS.md Handover 6)
completeness_audit_passed: <YYYY-MM-DD>
adversarial_review_passed: <YYYY-MM-DD>
quality_engineer_review_passed: <YYYY-MM-DD>
compliance_review_status: <passed | not-required | <YYYY-MM-DD>>
engineering_partner: <name>
fixed_vs_flexible:
  fixed: [<requirement ids that must not change>]
  flexible: [<requirement ids open to engineering tradeoffs>]
  unknown: [<questions for engineering to weigh in on>]
---

<!-- WARNING: pre-filled to satisfy LIFECYCLE_STATES; the four audit-gate date fields above (completeness_audit_passed / adversarial_review_passed / quality_engineer_review_passed / compliance_review_status) MUST be completed with concrete values before this packet is handed to engineering. -->

# Handoff Packet

> This is a Handoff Packet — the ontology's signature pre-engineering deliverable per Domain H. The folder is the load-bearing artifact for `docs/HANDOVERS.md` §"Handover 6: Spec → Engineering Handoff Packet"; this README plus 22 sibling children (21 narrative content files plus `requirements.yaml`) implement that contract. The packet's verification surface is `/audit-completeness`'s 25-item checklist; the packet is ready for engineering when the checklist runs clean against the kit user's filled-in content.

## Product brief <!-- source: inferred per HANDOVERS-6 gloss "README.md ← Product Brief" -->

<One paragraph restating what is being shipped, the customer segment it serves, and the strategic intent it advances. Cite the parent strategic intent slug (matches `parent_intent:` in the frontmatter above). Defer full elaboration of the business objective to [`business-objective.md`](./business-objective.md) and of the customer segment to [`customer-segment.md`](./customer-segment.md).>

## Folder index <!-- source: inferred (folder-template entry-point navigation) -->

| File | Purpose |
| --- | --- |
| [`business-objective.md`](./business-objective.md) | Cite the strategic intent. |
| [`customer-segment.md`](./customer-segment.md) | Cite the segment definition. |
| [`personas.md`](./personas.md) | Linked persona files from `context/personas/`. |
| [`problem.md`](./problem.md) | Validated problem statement + evidence. |
| [`jobs-to-be-done.md`](./jobs-to-be-done.md) | Documented JTBDs for the target customer. |
| [`current-workflow.md`](./current-workflow.md) | How it works today. |
| [`future-workflow.md`](./future-workflow.md) | How it'll work. |
| [`capabilities.md`](./capabilities.md) | From the parent initiative. |
| [`features.md`](./features.md) | Features mapped to parent capabilities. |
| [`requirements.yaml`](./requirements.yaml) | Requirement entries with full ontology metadata. |
| [`business-rules.md`](./business-rules.md) | Business rules in play. |
| [`policy-constraints.md`](./policy-constraints.md) | Policy / regulatory constraints. |
| [`acceptance-criteria.md`](./acceptance-criteria.md) | Per-requirement acceptance criteria. |
| [`non-functional-requirements.md`](./non-functional-requirements.md) | NFRs (performance, security, accessibility, etc.). |
| [`risks.md`](./risks.md) | Risks with mitigations. |
| [`dependencies.md`](./dependencies.md) | Internal-team, external-vendor, and upstream-system dependencies. |
| [`open-questions.md`](./open-questions.md) | Unresolved questions with owners and target resolution dates. |
| [`out-of-scope.md`](./out-of-scope.md) | Items deliberately excluded. |
| [`decision-log.md`](./decision-log.md) | Summary; full ADRs in `docs/adr/`. |
| [`launch-considerations.md`](./launch-considerations.md) | Pricing, support, operational, communications. |
| [`success-metrics.md`](./success-metrics.md) | KPIs with thresholds. |
| [`human-owned-decisions.md`](./human-owned-decisions.md) | Human-readable elaboration of the `human_owned_decisions:` frontmatter list. |

## Ready-for-engineering test <!-- source: HANDOVERS-6 "ready for engineering" seven-clause semantic test -->

The packet is ready when engineering can say, after reading the folder:

- We understand the customer problem.
- We understand the business objective.
- We understand the required product behavior.
- We understand what is fixed and what is flexible.
- We understand the risks.
- We understand how success will be measured.
- We understand which questions remain unresolved.
