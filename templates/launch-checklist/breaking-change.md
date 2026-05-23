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
change_type: breaking-change

human_owned_decisions:
  - Sunset date commitment (named sunset date ≥ 90 days from notice, or shorter window with documented rationale)
  - Rollback-or-stop-the-bleeding owner with paging contract (named human; full revert often infeasible mid-window)
ai_assistance_used:
  - Walked the per-item checklist confirmations
ai_assistance_allowed: restricted
human_approval_required: true
approvals_obtained: ["<role>: <YYYY-MM-DD>"]
---

# Launch checklist: breaking-change

> Change-type-keyed operational gate (`Launch Checklist`, Domain H — added 2026-05-23). Sibling of the Handoff Packet's `launch-considerations.md` narrative one-pager; this file extends the narrative with actionable per-item confirmations specific to a breaking change (something existing customers depend on is intentionally being changed). Cite `/launch-checklist` (P4.14) for the per-item walk; items are pinned by `docs/specs/cmd-launch-checklist/spec.md` §"Per-change-type checklist items" and copied verbatim.

## Checklist

1. - [ ] Deprecation notice published with named sunset date; sunset date is ≥ 90 days from notice (or rationale for shorter window recorded in `decision-log.md`).
2. - [ ] Customer migration tooling published (script, codemod, in-product wizard, or guided runbook); the tooling is tested against a representative sample of customer data.
3. - [ ] Per-segment customer outreach completed for the high-impact accounts named in `customer-segment.md`; outreach record (date + customer-side acknowledgment) logged in the Handoff Packet folder (free-text appendix or linked CRM record).
4. - [ ] Communications cadence committed: T-90 announcement, T-30 reminder, T-7 final notice. Copy drafted and routed for all three; first send-date recorded.
5. - [ ] Version-skew compatibility window confirmed: the old and new behaviors coexist for the full deprecation window (or a documented exception with risk-acceptance signature in `human-owned-decisions.md`).
6. - [ ] Dependency-team coordination completed: every team consuming the deprecated surface (SDK clients, mobile apps, partner integrations per `dependencies.md`) has a named contact who has acknowledged the deprecation timeline.
7. - [ ] API change-log entry (or equivalent versioned-contract entry) published; the entry cites the deprecation rationale and the named sunset date.
8. - [ ] Customer-success ticket tagging strategy in place: tickets mentioning the deprecated behavior auto-tag with `<feature>-deprecation-2026` (or equivalent) so support sees aggregate volume.
9. - [ ] Support runbook for the deprecation window: stock answers for "why is this changing," "what do I do," "can I get an extension"; named on-call coverage for the deprecation window.
10. - [ ] Rollback-or-stop-the-bleeding owner named with paging contract; rollback is realistically scoped (full revert is often infeasible mid-window — name the actual recovery path).
11. - [ ] Post-deprecation cleanup audit scheduled: at T+30-post-sunset, confirm the deprecated surface is actually removed (not just hidden) and that no customers still depend on it.
12. - [ ] Legal / compliance review confirmed if the deprecated behavior was part of a contractual commitment to specific customers; sign-off recorded under `approvals_obtained:`.
