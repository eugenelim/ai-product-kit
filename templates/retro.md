---
id: RETRO-<NNN>
slug: <kebab-case>
object_type: Decision
name: <human-readable name>
description: <one to three sentences>
owner: <named human or role>
status: Draft
priority: <Low | Medium | High | Critical>
risk_level: <Low | Medium | High | Critical>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

parent_landing: <landing report slug>
parent_handoff_packet: <handoff packet slug>
parent_vision: <delivery vision slug>
parent_initiative: <delivery initiative slug>

human_owned_decisions:
  - <Explicit decisions the retro surfaces — e.g., "stop doing X" or "double down on Y" — one per line>
ai_assistance_used:
  - Captured the five-question retro answers verbatim
ai_assistance_allowed: restricted
human_approval_required: false
approvals_obtained: ["<role>: <YYYY-MM-DD>"]

retro_scope: <landing | handoff>
retro_facilitator: <name>
---

# Retrospective: <slug>

> Domain H `Decision`-class artifact (per `context/frameworks/ontology.md`). Adjacent to — not inside — the upstream Landing Report (when `retro_scope: landing`) or Handoff Packet (when `retro_scope: handoff`). Captures the team's verbatim answers to five fixed questions in fixed order, asked one at a time and never batched. Cite `docs/HANDOVERS.md` §"Handover 7: Engineering → Landings" for the upstream Landing Report contract; the retro complements the report (process reflection vs. metric verdict).

## What worked?

_<Human's verbatim answer to "What worked?". The command captures the answer as the human types it — no paraphrase, no summary, no bullet-ification.>_

## What didn't?

_<Human's verbatim answer to "What didn't?".>_

## What surprised us?

_<Human's verbatim answer to "What surprised us?".>_

## What would we repeat?

_<Human's verbatim answer to "What would we repeat?".>_

## What would we change?

_<Human's verbatim answer to "What would we change?".>_

## Cross-references

- Upstream artifact: `delivery/landings/<slug>.md` (when `retro_scope: landing`) or `delivery/handoff-packets/<slug>/` (when `retro_scope: handoff`).
- Related: parent Vision, parent Initiative (transitive frontmatter carry-through).
