---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
id: RN-<NNN>
slug: <kebab-case>
object_type: Customer Communication
name: <human-readable name>
description: <one to three sentences>
owner: <named human or role>
status: Draft
priority: <Low | Medium | High | Critical>
risk_level: <Low | Medium | High | Critical>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

# Traceability (one of parent_handoff_packet OR parent_landing — the command
# writes whichever the `--from-landing` flag selects; the other is omitted).
parent_handoff_packet: <handoff packet slug>
parent_landing: <landing report slug>
parent_initiative: <delivery initiative slug>
parent_vision: <delivery vision slug>
related_personas: [<id>, ...]
related_kpis: [<id>, ...]

# Human-vs-AI ownership
human_owned_decisions:
  - Approval of customer-facing claims in the draft body before publication
ai_assistance_used:
  - Draft of customer-facing what's-new and feature-list copy
ai_assistance_allowed: restricted
human_approval_required: true
approvals_obtained: ["<role>: <YYYY-MM-DD>"]

# Open items
open_questions: [<text>, ...]
---

# Release notes

> Customer Communication (Domain G) drafted post-ship from a Handoff Packet (default) or a Landing Report (`--from-landing`). Cite docs/HANDOVERS.md §"Handover 6" / §"Handover 7" for parent contracts and docs/HUMAN-AI-OWNERSHIP.md (release-notes drafting is zone-1 AI-assisted; the customer-facing claims they make are zone-3 human-only). The command writes this draft; the human approves the claims via the `human_owned_decisions:` entry above before publication.

## What's new

<One paragraph in customer voice. Name what they can now do that they couldn't before. Voice: second-person; avoid internal jargon (kubernetes, microservice, feature-flag, rollout %, canary, dogfood, internal-only, eng-only, mvp, etc.).>

## Features in this release

- <User-visible feature 1 — one short line in customer voice.>
- <User-visible feature 2.>
- <User-visible feature 3. (3–7 bullets total; refuse to publish below 3.)>

## Optional sections

Delete the heading and all unused sections below if none apply.

### Known limitations

- <Limitation 1 the customer should be told about up front, in customer voice.>
