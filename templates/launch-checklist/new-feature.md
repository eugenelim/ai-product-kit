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
change_type: new-feature

human_owned_decisions:
  - Beta cohort selection (named cohort + selection criteria recorded in launch-considerations.md §Communications and rollout)
  - Customer comms approval (the light-touch blog or in-product banner draft is routed to a named approver before publication)
ai_assistance_used:
  - Walked the per-item checklist confirmations
ai_assistance_allowed: restricted
human_approval_required: true
approvals_obtained: ["<role>: <YYYY-MM-DD>"]
---

# Launch checklist: new-feature

> Change-type-keyed operational gate (`Launch Checklist`, Domain H — added 2026-05-23). Sibling of the Handoff Packet's `launch-considerations.md` narrative one-pager; this file extends the narrative with actionable per-item confirmations. Cite `/launch-checklist` (P4.14) for the per-item walk; items are pinned by `docs/specs/cmd-launch-checklist/spec.md` §"Per-change-type checklist items" and copied verbatim.

## Checklist

1. - [ ] Feature-flag wired and tested in staging; flag default is OFF for non-beta cohort.
2. - [ ] User-facing docs published (help center / in-product) and discoverable from the feature surface.
3. - [ ] Success-metric instrumentation (per `success-metrics.md`) is live and validated against a known event in staging.
4. - [ ] Observability dashboard names the feature and its key counters / SLO targets; alert thresholds are committed.
5. - [ ] Support team briefed; FAQ + escalation path documented; on-call coverage confirmed for first 72h.
6. - [ ] Beta cohort (≤ 5% rollout) selected and named; cohort selection criteria recorded in `launch-considerations.md` §Communications and rollout.
7. - [ ] Rollback plan: feature flag is the kill switch; named owner for the rollback decision; rollback drill performed in staging.
8. - [ ] Internal comms (engineering + customer-facing teams) scheduled at T-3 days with the named copy.
9. - [ ] Customer comms (light-touch — blog or in-product banner) drafted and routed to the named approver per `human-owned-decisions.md`.
10. - [ ] Post-launch retro scheduled at T+14 days with named facilitator; metric-review meeting separately scheduled at T+30 days.
