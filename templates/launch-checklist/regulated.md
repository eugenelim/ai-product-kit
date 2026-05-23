---
slug: <kebab-case>
object_type: Launch Checklist
name: <human-readable name>
description: <one to three sentences>
owner: <named human or role>
status: Draft
priority: <Low | Medium | High | Critical>
risk_level: <Low | Medium | High | Critical>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

parent_handoff_packet: <handoff packet slug>
parent_initiative: <delivery initiative slug>
parent_vision: <delivery vision slug>
change_type: regulated

human_owned_decisions:
  - Legal / compliance sign-off (named human, not AI per docs/HUMAN-AI-OWNERSHIP.md; specifies the regulatory regime(s) the change interacts with)
  - Named compliance-officer accountability (a specific named compliance officer is on the hook for the first 90 days post-launch)
ai_assistance_used:
  - Walked the per-item checklist confirmations
ai_assistance_allowed: restricted
human_approval_required: true
approvals_obtained: ["<role>: <YYYY-MM-DD>"]
---

# Launch checklist: regulated

> Change-type-keyed operational gate (`Launch Checklist`, Domain H — added 2026-05-23). Sibling of the Handoff Packet's `launch-considerations.md` narrative one-pager; this file extends the narrative with actionable per-item confirmations specific to a launch that touches a regulated workflow (GDPR, HIPAA, SOC 2, PCI-DSS, financial-services, etc.). Legal / compliance sign-off is mandatory, not optional. Cite `/launch-checklist` (P4.14) for the per-item walk; items are pinned by `docs/specs/cmd-launch-checklist/spec.md` §"Per-change-type checklist items" and copied verbatim.

## Checklist

1. - [ ] Legal / compliance sign-off recorded (named human, not AI per `docs/HUMAN-AI-OWNERSHIP.md`); sign-off names the specific regulatory regime(s) the change interacts with. Recorded in `human-owned-decisions.md` and `approvals_obtained:`.
2. - [ ] Regulator notification timing confirmed if the regime requires advance notification (e.g., financial-services pre-launch filings); filing reference number recorded.
3. - [ ] Audit-log instrumentation: the regulated workflow's user-facing actions emit audit events with the regulator-required fields (actor, action, timestamp, affected record id, before/after state where applicable); a test event is verified end-to-end in staging.
4. - [ ] Evidence-of-controls documentation: the change's control-design rationale is documented under `policy-constraints.md` or a linked controls-evidence file; the documentation is in the format the org's compliance team will surface in the next audit cycle.
5. - [ ] Data-handling compliance: PII / PHI / cardholder data classifications confirmed; the change does not expand the data-classification scope without compensating controls; classification recorded in `non-functional-requirements.md` §Data.
6. - [ ] Retention-policy review: data the change creates is subject to the named retention policy (e.g., 7-year retention for financial records); retention configuration verified in staging.
7. - [ ] Breach-notification runbook updated: in the event of a breach involving the change's data surface, the named runbook step ("who to call, what to say, in what timeframe per the regulation's notification deadline") is current.
8. - [ ] Third-party processor list updated if the change introduces a new sub-processor; customer-facing sub-processor list and any DPAs (Data Processing Agreements) updated.
9. - [ ] Customer-disclosure language reviewed by legal: privacy notice, terms-of-service, in-product disclosures all reflect the change; review record cited under `approvals_obtained:`.
10. - [ ] Internal-audit pre-review completed: the org's internal-audit function has reviewed the change (or has explicitly waived the review with rationale); waiver, if used, is recorded.
11. - [ ] Regulatory-change-log entry filed: the org's internal regulatory-change tracker has an entry for this launch with the named regime(s) and effective date.
12. - [ ] Sunset of any non-compliant prior behavior: if the change brings something into compliance, the non-compliant behavior is removed (not just supplemented); removal verified.
13. - [ ] Named compliance-officer accountability: a specific named compliance officer (not "the compliance team") is on the hook for the change's regulatory posture for the first 90 days post-launch; name recorded in `human-owned-decisions.md`.
