---
name: ears-lint
description: Classifies a candidate requirement sentence (or a list of them) into one of the five EARS patterns (Ubiquitous, Event-driven, State-driven, Optional-feature, Unwanted-behavior), the Complex combination form, or Non-conformant. Returns a per-sentence verdict with pattern label, one-line rationale, and a suggested EARS-conformant rewrite when the sentence is non-conformant. Rule source is `context/frameworks/ears.md`; the skill cites the framework and does not restate the pattern templates. Typical dispatch is per Requirement or Acceptance-Criterion sentence inside `/draft-spec` (P4.8) and `/handoff-packet` (P4.11), or as a fan-out target when auditing existing PM Spec sections. Load whenever the orchestrator needs to verify that a candidate requirement sentence conforms to EARS — input is either inline sentences or a path to a file the orchestrator names.
license: MIT
---

# ears-lint

This skill classifies a candidate requirement sentence into one of the five EARS patterns (Ubiquitous, Event-driven, State-driven, Optional-feature, Unwanted-behavior), the Complex combination form, or Non-conformant. It consumes `context/frameworks/ears.md` as the rule library and returns a per-sentence verdict that downstream commands (`/draft-spec`, `/handoff-packet`) can act on.

## When to use this skill

- Right after a Requirement or Acceptance-Criterion sentence is drafted — typically inside `/draft-spec`'s Step 3 (Functional requirements collection) or `/handoff-packet`'s `acceptance-criteria.md` aggregation.
- When auditing an existing PM Spec's `## Functional requirements` or `## Acceptance criteria` section for syntax conformance.
- As a fan-out target when reviewing many sentences at once — each invocation handles one or more sentences; the orchestrator batches across a file.

## Invocation contract

**Input.** Either form is accepted:

- **(a) Inline.** One or more candidate sentences passed as text. Each sentence is one input slot.
- **(b) Path.** A path to a file the orchestrator names. The skill reads the file and treats each non-empty line as one candidate sentence.

The orchestrator is responsible for stripping bullet markup (`- `, `* `, leading numbers like `1.`) and the `REQ-NNN:` id prefix before passing sentences. Multi-sentence acceptance criteria are split by the orchestrator (one EARS sentence per invocation slot), not by the skill.

Known orchestrator-side splitter failure modes the orchestrator must handle (the skill does not): sentence-final periods inside abbreviations (`Req.`, `Fig.`, `e.g.`), decimal numbers (`$1.00`, `99.9% uptime`), embedded URLs (`https://example.com`), and quoted strings that themselves contain `;` or `.`. When the orchestrator cannot split unambiguously, it surfaces the bullet to the human rather than guessing.

**Output.** A structured verdict per input sentence, in this exact shape:

```
sentence: "<the input sentence, verbatim>"
pattern: ubiquitous | event-driven | state-driven | optional-feature | unwanted-behavior | complex | non-conformant
rationale: "<one short sentence — what keyword(s) or sentence shape triggered the classification, or what is missing>"
suggested_rewrite: "<an EARS-conformant rewrite if pattern == non-conformant; null otherwise>"
```

**Exit conditions.** The skill always emits a verdict for each input sentence — there is no "skip" or "abort" state. If the orchestrator passed zero sentences, the skill returns an empty verdict list (no error).

## Classification procedure

The rule library is `context/frameworks/ears.md` — read that file for the canonical pattern templates and the "common confusion" entries. Do not restate the pattern templates here.

The procedure is a Complex pre-filter followed by a single-keyword priority cascade. The pre-filter runs first because Complex requires inspecting the whole sentence, not the first matching keyword — a sequential cascade that returned on first match would make Complex unreachable for any sentence that leads with `When`, `While`, `Where`, or `If`.

0. **Complex pre-filter.** Count distinct leading-pattern keywords (`If`, `When`, `While`, `Where`) attached to distinct top-level clauses of the sentence. Two clauses from the same pattern family (e.g., two `If` preconditions joined by `and`) do not count as Complex — they are either a malformed compound Unwanted-behavior to be split, or a multi-requirement Non-conformant case. If two or more keywords from **distinct** pattern families are found, classify Complex and return.
1. **Unwanted-behavior.** Sentence begins with `If` followed by a precondition clause; the consequence clause uses `shall` and names the system actor. Both the canonical `If <precondition>, then the <system> shall <response>` and the comma-only `If <precondition>, the <system> shall <response>` forms classify as Unwanted-behavior — see `context/frameworks/ears.md` §"Unwanted-behavior" for why the comma-only form is kit-accepted.
2. **Event-driven.** Sentence begins with `When` followed by a discrete-event trigger; the consequence clause uses `shall` and names the system actor.
3. **State-driven.** Sentence begins with `While` followed by a sustained-state condition; the consequence clause uses `shall` and names the system actor.
4. **Optional-feature.** Sentence begins with `Where` followed by an opt-in feature condition; the consequence clause uses `shall` and names the system actor.
5. **Ubiquitous.** No leading EARS keyword; sentence starts with `The <system>` (the named system actor) and uses `shall` in the consequence clause.
6. **Non-conformant.** Sentence fails every above pattern. The canonical list of failure-mode shapes lives in `context/frameworks/ears.md` §"Failure modes — how the pattern can be misused"; this skill cites that list rather than restating it.

For Non-conformant sentences, populate `suggested_rewrite` with the most natural EARS-conformant rephrasing — usually a modal-verb swap to `shall`, an actor-naming rephrase from passive voice, or the addition of a leading EARS keyword. If the trigger condition cannot be inferred from the sentence alone, default to a Ubiquitous-shaped rewrite (`The <system> shall <action>`) and surface a note that the author should verify whether an `If`/`When`/`While`/`Where` keyword is more appropriate.

## Failure modes

The canonical list of non-conformant sentence shapes lives in `context/frameworks/ears.md` §"Failure modes — how the pattern can be misused" — read that section for the authoritative enumeration (question; goal-style with no named system actor; wrong modal verb; multi-requirement glued with `and`; passive voice with `shall` but no named system actor). This skill section adds the classifier-operational addenda — what to write in `suggested_rewrite` per shape, and one additional shape the framework omits.

- **Question (framework-cited).** `suggested_rewrite` is `null`; the verdict's rationale tells the orchestrator to move the bullet to the artifact's `## Open questions` section, not to invent an EARS sentence for it.
- **Goal-style with no named system actor (framework-cited).** `suggested_rewrite` is an Event-driven rephrase that adds the named system as the consequence-clause subject (the framework's §"Failure modes" entry gives the canonical example).
- **Wrong modal verb (framework-cited).** `suggested_rewrite` swaps the modal for `shall`; the surrounding pattern classification (Ubiquitous / Event-driven / …) is the same as it would have been with `shall` in place — the skill records the underlying pattern in the verdict rationale so the rewrite is one-keyword scoped.
- **Multi-requirement glued with `and` (framework-cited).** `suggested_rewrite` is two separate EARS sentences (the framework recommends splitting; the Complex form is only appropriate when the two clauses genuinely share a condition).
- **Passive voice with `shall` but no named system actor (framework-cited).** `suggested_rewrite` makes the named system the grammatical subject — typically by introducing a `When` keyword and the missing actor.
- **Multi-clause prose, not a single requirement (skill-specific addendum, not in the framework).** A paragraph describing behavior is not a requirement; `suggested_rewrite` is `null` and the rationale tells the orchestrator the bullet belongs in `## User behaviour — current vs future`, not in `## Functional requirements`.

## Examples

One passing example per pattern (canonical EARS forms; the rule source is `context/frameworks/ears.md`), the Complex form, and one non-conformant case with rewrite.

```
sentence: "The system shall log every API request."
pattern: ubiquitous
rationale: "No leading EARS keyword; named system actor; uses shall — classifies as the fall-through Ubiquitous pattern."
suggested_rewrite: null

sentence: "When a user submits the checkout form, the system shall validate the card details."
pattern: event-driven
rationale: "Leading `When` keyword with a discrete-event trigger; consequence uses shall and names the system."
suggested_rewrite: null

sentence: "While the user is authenticated, the system shall display the dashboard."
pattern: state-driven
rationale: "Leading `While` keyword with a sustained state; consequence uses shall and names the system."
suggested_rewrite: null

sentence: "Where multi-factor authentication is enabled, the system shall require a second factor."
pattern: optional-feature
rationale: "Leading `Where` keyword with an opt-in feature; consequence uses shall and names the system."
suggested_rewrite: null

sentence: "If the payment gateway returns an error, then the system shall display a retry prompt."
pattern: unwanted-behavior
rationale: "Leading `If` keyword with an exceptional precondition; consequence uses shall and names the system."
suggested_rewrite: null

sentence: "When a user submits the checkout form, while the cart total exceeds $1000, the system shall require manager approval."
pattern: complex
rationale: "Contains two leading EARS keywords (`When` and `While`) attached to distinct clauses — the Complex combination form."
suggested_rewrite: null

sentence: "An email shall be sent to the user on checkout completion."
pattern: non-conformant
rationale: "Passive voice with `shall` but no named system actor — fails the EARS requirement that the system be the grammatical subject of the consequence clause."
suggested_rewrite: "When checkout completes, the system shall send a confirmation email to the user."
```

## Files

- `references/fixture-sentences.md` — the manual-gesture verification fixture: ~11 candidate sentences with annotated expected classifications, covering all seven verdict labels including passive-voice-no-actor and `If`-without-`then` edge cases.

The skill is prose-procedure today. A runnable Python form (`scripts/ears_lint.py`) is a deferred follow-up tracked in `docs/specs/ears-lint/notes/deferred-findings.md` under the placeholder slug `script-ears-lint`. The runnable form would let CI run the lint without a model in the loop, on the `ost-validator → scripts/validate_ost.py` (P2.8) precedent.
