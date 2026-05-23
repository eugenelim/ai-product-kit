# EARS — Easy Approach to Requirements Syntax

> A constrained natural-language pattern for requirement sentences, defined by Mavin, Wilkinson, Harwood & Novak (2009). EARS reduces ambiguity by forcing every requirement to one of five sentence templates — Ubiquitous, Event-driven, State-driven, Optional-feature, Unwanted-behavior — or a Complex combination of them. This kit uses EARS to govern the syntax of Requirement and Acceptance-Criterion sentences inside PM Specs (`docs/HANDOVERS.md` §"Handover 5") and Engineering Handoff Packets (`docs/HANDOVERS.md` §"Handover 6"). The classification skill that consumes this framework is `.claude/skills/ears-lint/SKILL.md`.

## The five canonical patterns

Each pattern names the kind of requirement, the canonical sentence template (verbatim from Mavin et al.), one canonical example, when the pattern applies, and the most common authoring confusion.

### Ubiquitous

- **Template:** `The <system name> shall <system response>.`
- **Example:** `The system shall log every API request.`
- **When to use:** the requirement holds at all times, with no triggering condition, optional feature, or unwanted-behavior precondition.
- **Common confusion:** Ubiquitous is the fall-through pattern — if a sentence has no leading EARS keyword and the consequence uses `shall`, it is Ubiquitous. A sentence that *looks* unconditional but actually depends on a sustained state ("the user is authenticated") is State-driven, not Ubiquitous.

### Event-driven

- **Template:** `When <trigger>, the <system name> shall <system response>.`
- **Example:** `When a user submits the checkout form, the system shall validate the card details.`
- **When to use:** the requirement fires in response to a discrete event — a click, a form submission, a message arrival, a timer tick.
- **Common confusion:** if the trigger is a sustained condition rather than a discrete event ("while the user is editing"), the sentence is State-driven, not Event-driven. "When the user is logged in" is borderline — prefer "While the user is logged in" if the requirement holds for the duration of the session.

### State-driven

- **Template:** `While <state>, the <system name> shall <system response>.`
- **Example:** `While the user is authenticated, the system shall display the dashboard.`
- **When to use:** the requirement holds for the duration of a named system or user state.
- **Common confusion:** State-driven and Event-driven both look like preconditions in English. Use `When` for instantaneous triggers and `While` for sustained conditions. If both apply (an event during a state), use the Complex form.

### Optional-feature

- **Template:** `Where <feature is included>, the <system name> shall <system response>.`
- **Example:** `Where multi-factor authentication is enabled, the system shall require a second factor.`
- **When to use:** the requirement applies only when an opt-in capability is configured or licensed. Distinguishes "feature is built but not turned on" from "feature is always on."
- **Common confusion:** Optional-feature is for kit configuration (a flag, a license, a tenant setting). It is not for user-driven preferences within a feature — those are typically State-driven or Event-driven.

### Unwanted-behavior

- **Template (canonical):** `If <precondition>, then the <system name> shall <system response>.`
- **Template (comma-only equivalent, kit-accepted):** `If <precondition>, the <system name> shall <system response>.`
- **Example:** `If the payment gateway returns an error, then the system shall display a retry prompt.`
- **When to use:** the precondition is an unwanted, exceptional, or error condition, and the response is the recovery or guard behavior.
- **Common confusion:** the literal `then` keyword is part of Mavin et al.'s canonical form. The kit accepts the comma-only form because PM-authored sentences commonly omit `then` for prose readability; the leading `If` keyword is sufficient to anchor the pattern. A sentence whose `If` clause is *not* an unwanted condition (e.g., `If the user opts in, the system shall send notifications`) is still classified Unwanted-behavior by EARS — the pattern is keyword-driven, not semantic-driven; the author's job is to phrase opt-in flows as Optional-feature with `Where`, not as Unwanted-behavior with `If`.

## The Complex combination form

A Complex requirement combines two or more EARS keywords from distinct pattern families into one sentence.

- **Example:** `When a user submits the checkout form, while the cart total exceeds $1000, the system shall require manager approval.`
- **Classification rule:** a sentence is Complex if it contains two or more leading-pattern keywords (`When`, `While`, `Where`, `If`) from **distinct** pattern families attached to distinct clauses; a sentence that contains a keyword in a non-leading position (e.g., an adverbial `while` deep inside a clause like "the page where the flag is visible") is not Complex by that fact alone. Two clauses from the same pattern family (e.g., two `If` preconditions joined by `and`) are not Complex either — split them into separate Unwanted-behavior requirements, or reclassify as Non-conformant multi-requirement.
- **Common combinations include** `When … while …`, `While … if …`, and `Where … when …`.
- **When to use:** a single requirement genuinely depends on both a state and an event, or both an event and an unwanted condition. If the sentence is becoming hard to parse, split it into two separate requirements rather than reaching for Complex.

## Failure modes — how the pattern can be misused

EARS exists to eliminate ambiguity. The most common ways PM-authored sentences fail conformance:

- **The sentence is a question.** "Should the system support guest checkout?" is not a requirement; it is an open question. Move to the `## Open questions` section of the artifact.
- **The sentence states a goal without naming the system actor and action.** "The user should be able to log in via SSO" is non-conformant — the system actor is implicit and the modal is `should`, not `shall`. Conformant rewrite: `When a user initiates SSO sign-in, the system shall delegate authentication to the configured identity provider.`
- **The modal verb is `must`, `will`, or `should` instead of `shall`.** EARS requires `shall`. The kit accepts `shall` only — any other modal verb makes the sentence non-conformant. Rationale: `shall` is the unambiguous deontic marker EARS adopted from formal-requirements practice precisely to avoid the ambiguity that `should` and `will` carry in natural English.
- **The sentence packs two requirements without the Complex form's keywords.** `The system shall validate the email and the system shall send a confirmation message` is two Ubiquitous sentences glued with `and` — split it, or use the Complex form if the two clauses genuinely depend on one trigger.
- **The sentence is in the passive voice with `shall` but no named system actor.** `An email shall be sent to the user on checkout completion` is non-conformant — the EARS templates require the named system as the grammatical subject of the consequence clause. Conformant rewrite: `When checkout completes, the system shall send a confirmation email to the user.`

## How the kit uses this framework

This framework is the source-of-truth for the five EARS patterns. The classification skill at `.claude/skills/ears-lint/SKILL.md` consumes it as the rule library and applies pattern-matching to candidate sentences in keyword-priority order. The skill cites this framework and does not restate the pattern definitions; the framework does not restate the skill's classification procedure. Downstream commands that consume the skill: `/draft-spec` (P4.8 — Step 3 collects each Requirement and currently emits an advisory EARS prompt; a future integration patch will dispatch the skill against each Requirement and Acceptance-Criterion sentence) and `/handoff-packet` (P4.11 — `acceptance-criteria.md` aggregates per-Requirement and is the natural consumer of mechanical EARS lint). Until the integration patches ship, this framework is documentary; the skill is invocable on demand against any candidate sentence or fixture file.

## References

- Mavin, A., Wilkinson, P., Harwood, A., & Novak, M. (2009). "Easy Approach to Requirements Syntax (EARS)." *17th IEEE International Requirements Engineering Conference*, pp. 317–322. The canonical academic source for the five patterns and the Complex combination form.
- `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" and §"Handover 6: Spec → Engineering Handoff Packet" — the kit's consuming surface for EARS-conformant Requirement and Acceptance-Criterion sentences.
- `.claude/skills/ears-lint/SKILL.md` — the rule consumer.
