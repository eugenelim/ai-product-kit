# Deferred findings — phase-2-discovery-audits-and-comms

Items the REVIEW iter-1 adversarial review surfaced that this batch does not address. Each row carries an explicit "when to address" trigger.

## D-E1 — `/opportunity-narrative` doesn't gate on parent intent status

- **Source:** adversarial-reviewer post-EXECUTE review iter-1 (E-1).
- **Finding.** `/opportunity-narrative` Steps 1–2 verify the OST exists and enforce the anti-prematurity guard on `chosen_opportunity:`. Neither step checks whether the OST's `parent_intent:` resolves to an active intent (status not `killed`/`abandoned`). If the parent intent was terminated after the OST was written but before the narrative is drafted, the narrative crosses the Discovery → Validation boundary against a dead strategic direction.
- **Why deferred for this batch.** The spec's anti-prematurity guard specification names exactly two conditions (chosen_opportunity present AND chosen_opportunity.id resolves). The intent-status check is the audit's domain (`/audit-discovery-coherence` Rule 1 catches it). Adding a third gate to `/opportunity-narrative` would broaden the spec's contract beyond what iter-2 review approved, and the intent-killed-mid-discovery case is low-frequency.
- **When to address.** When `/audit-discovery-coherence` is wired as a precondition for `/opportunity-narrative` (a future ROADMAP item), OR when a real PM has the experience of drafting a narrative against a recently-killed intent. The recommended fix is to add to `/opportunity-narrative` Step 1: "Read `<repo-root>/strategy/intents/<parent_intent>.md`. If missing or if `status:` is `killed`/`abandoned`, exit code 2 with a remediation message pointing at `/audit-discovery-coherence` for diagnosis."
- **Workaround for users today.** Run `/audit-discovery-coherence <ost-slug>` before `/opportunity-narrative`. Rule 1 will surface the dead-intent issue with a `broken` verdict.

## Open question — `discovery-update` integration with `voice-check`

- **Source:** spec open question (carried over from PLAN-iter-1).
- **Finding.** `/discovery-update --for <role>` ships with role-mode mechanical anchors (exec / eng-lead / design-lead / support / all-hands). Each role has a grep-testable content rule. A future `voice-check` skill (planned — P8.4) would add stricter voice-guide enforcement on top of the mechanical anchors.
- **When to address.** When P8.4 (`skill-voice-check`) ships.

## Open question — Promote `/audit-discovery-coherence` prose to a runnable script

- **Source:** spec open question.
- **Finding.** Following F1.4's precedent (which promoted `/audit-traceability`'s prose to `scripts/audit-traceability.py`), a future ROADMAP item could promote `/audit-discovery-coherence` to `scripts/audit-discovery-coherence.py`. The command already documents the "script-when-available, prose-fallback when not" pattern in Step 2.
- **When to address.** When `/audit-discovery-coherence` is invoked enough in real workflows that automation pays off (loose heuristic: > 1 invocation per week).
