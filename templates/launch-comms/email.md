---
id: LC-<NNN>
slug: <kebab-case-email>
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
audience: customer-email

human_owned_decisions:
  - Customer-facing copy approval (this draft will not be published without a named approver's sign-off)
  - Subject-line factual accuracy (no claim outside the parent Handoff Packet's verified content)
  - Marketing / Legal / Compliance review status (none of these reviews are run by this command; the human routes the draft to the named reviewer)
ai_assistance_used:
  - Draft of customer email copy
ai_assistance_allowed: restricted
human_approval_required: true
approvals_obtained: ["<role>: <YYYY-MM-DD>"]
---

# Customer email

> Launch Communication (proposed Domain G/H — see cmd-launch-comms spec OQ2 / RFC) drafted post-ship for a customer email send. Imperative, scannable, single-action voice. Customer-facing claims are HUMAN-AI-OWNERSHIP zone-3 — the human approves before sending.

## Subject line

<Single line, ≤ 60 chars. The email's load-bearing unit; everything else is downstream. Confirm character count before advancing.>

## Preview text

<≤ 90 chars. The snippet that appears in the inbox between subject and body in most clients.>

## Body

<Three short paragraphs maximum. One opening sentence ("here's what's new"); one middle paragraph naming the benefit and linking to the blog post; one closing sentence with the single CTA.>

## Call to action

<One line. Matches the `Get started` CTA in blog.md for cross-channel consistency — paste it through. The command does not auto-link; the human confirms the match.>
