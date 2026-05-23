---
id: LC-<NNN>
slug: <kebab-case-internal>
object_type: Launch Communication
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
audience: internal-team

human_owned_decisions:
  - Runbook accuracy (the on-call rotation and runbook link are verified by the named engineering owner)
  - Kill-switch / rollback plan accuracy (verbatim copy through from the parent packet, or a named owner has approved a divergence)
ai_assistance_used:
  - Draft of internal-team launch announcement
ai_assistance_allowed: restricted
human_approval_required: true
approvals_obtained: ["<role>: <YYYY-MM-DD>"]
---

# Internal-team announcement

> Launch Communication (proposed Domain G/H — see cmd-launch-comms spec OQ2 / RFC) drafted post-ship from a Handoff Packet's `launch-considerations.md` §"Communications and rollout" sub-section. Internal-team voice: direct, operational, runbook-aware.

## What shipped

<One paragraph naming the product behaviour and the rollout phase (e.g., "10% rollout to US-only at T+0; 100% at T+14d").>

## Who owns what at launch

<Explicit table: on-call rotation, runbook link, escalation paths. Copy through from the parent packet's `launch-considerations.md` §"Communications and rollout" if it already names these.>

## Kill-switch and rollback plan

<Verbatim text the engineer-on-call can read and act on. Pulled from the parent packet's `launch-considerations.md` §"Communications and rollout". The command refuses to advance for the internal draft if no kill-switch plan exists.>

## Internal FAQ

- **Q:** <Anticipated internal question — operational concern, load, dependencies, on-call burden.>
  **A:** <Short answer.>
- **Q:** <...>
  **A:** <...>

## Talking points for customer-facing teams

- <Short bullet sales / support / CSM can use internally. The customer-facing version lives in blog.md and email.md.>
- <...>
