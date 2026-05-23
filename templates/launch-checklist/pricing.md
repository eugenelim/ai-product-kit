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
change_type: pricing

human_owned_decisions:
  - Pricing model sign-off (named human, never AI per docs/HUMAN-AI-OWNERSHIP.md)
  - Grandfathering policy approval (which existing customers keep the old pricing, for how long, under what conditions)
ai_assistance_used:
  - Walked the per-item checklist confirmations
ai_assistance_allowed: restricted
human_approval_required: true
approvals_obtained: ["<role>: <YYYY-MM-DD>"]
---

# Launch checklist: pricing

> Change-type-keyed operational gate (`Launch Checklist`, Domain H — added 2026-05-23). Sibling of the Handoff Packet's `launch-considerations.md` narrative one-pager; this file extends the narrative with actionable per-item confirmations specific to a pricing change. Pricing is an area where AI must never be the final owner (per `docs/HUMAN-AI-OWNERSHIP.md`). Cite `/launch-checklist` (P4.14) for the per-item walk; items are pinned by `docs/specs/cmd-launch-checklist/spec.md` §"Per-change-type checklist items" and copied verbatim.

## Checklist

1. - [ ] Pricing decision owner (a named human, never AI per `docs/HUMAN-AI-OWNERSHIP.md`) has signed off on the new pricing model; signature recorded in `human-owned-decisions.md` and mirrored in `approvals_obtained:`.
2. - [ ] Grandfathering policy explicit: which existing customers (by segment, contract type, or join-date) keep the old pricing, for how long, under what conditions; policy recorded in `launch-considerations.md` §Pricing and packaging.
3. - [ ] Billing-system change validated end-to-end: a test transaction at the new price succeeds; a test transaction for a grandfathered customer succeeds at the old price.
4. - [ ] Finance team sign-off on revenue-impact forecast and on the accounting treatment of the change; sign-off recorded under `approvals_obtained:`.
5. - [ ] Customer comms timeline: existing customers notified ≥ 30 days before change (or contractual notice window, whichever is longer); new customers see the new price from day one. Both sets of copy drafted and routed.
6. - [ ] Sales-team enablement: pricing FAQ, objection-handling guide, and updated quote templates distributed; sales lead has confirmed receipt.
7. - [ ] Support ticket triage policy for pricing complaints: stock answer, escalation path (named person), discount-authority limits (do front-line reps have a "save the customer" lever, and what is its dollar ceiling).
8. - [ ] Revenue-impact forecast reviewed against a sensitivity range (best / base / worst); the worst-case impact is acceptable per the named decision owner.
9. - [ ] Investor-relations comms drafted if the pricing change is **material** (per the org's definition of materiality, not the kit's); IR sign-off recorded if applicable, or "not material" recorded with rationale.
10. - [ ] A/B test gate: if the change is being tested rather than launched in full, the test's success/falsification thresholds are predeclared (per the kit's `assumption-threshold-lock` discipline) and recorded in the linked experiment artifact.
11. - [ ] Contract-customer renegotiation list: every customer with a contract that names a specific price has a renegotiation owner and target close date; the list is closed (no "TBD" customers) before launch.
