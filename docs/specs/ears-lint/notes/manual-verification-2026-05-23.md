# Manual-gesture verification — ears-lint — 2026-05-23

Records the in-session execution of the `ears-lint` classification procedure against each row in `.claude/skills/ears-lint/references/fixture-sentences.md`. Per the spec's Verification mode (and the iter-1 acknowledgement of self-marking risk), classifications were written **before** reading the expected-pattern column of each fixture row.

## Protocol

1. For each fixture row, the sentence was read in isolation.
2. The classification procedure from `.claude/skills/ears-lint/SKILL.md` §"Classification procedure" was applied — the six-step keyword-priority cascade plus the final fall-through to Non-conformant.
3. Actual pattern + rationale + suggested_rewrite recorded below.
4. **Only then** the expected-pattern column was read and compared.
5. Self-consistency caveat from the spec applies — the same model instance authored the fixture, the framework, and the skill, then executed this gesture. The gesture verifies that the three artifacts agree (self-consistency), not that the procedure is independently correct on unseen inputs. The deferred fresh-session re-verification remains the canonical independent test.

## Actual classifications

| # | Sentence (abbreviated) | Actual pattern | Rationale (one line) | Suggested rewrite |
|---|---|---|---|---|
| 1 | The system shall log every API request. | ubiquitous | No leading EARS keyword; system actor first; `shall` present. Fall-through Ubiquitous. | null |
| 2 | When a user submits the checkout form, the system shall validate… | event-driven | Single leading `When` (discrete event); consequence uses `shall` and names the system. | null |
| 3 | While the user is authenticated, the system shall display… | state-driven | Single leading `While` (sustained state); consequence uses `shall` and names the system. | null |
| 4 | Where multi-factor authentication is enabled, the system shall require… | optional-feature | Single leading `Where` (opt-in feature); consequence uses `shall` and names the system. | null |
| 5 | If the payment gateway returns an error, then the system shall display… | unwanted-behavior | Leading `If` + explicit `then`; consequence uses `shall` and names the system. Canonical form. | null |
| 6 | If the user's session expires, the system shall redirect… | unwanted-behavior | Leading `If` + comma-only (no `then`); kit-accepted per framework Unwanted-behavior H3. | null |
| 7 | When a user submits the checkout form, while the cart total exceeds $1000, the system shall require manager approval. | complex | Two leading EARS keywords (`When` + `While`) on distinct clauses. Complex combination. | null |
| 8 | Should the system support guest checkout? | non-conformant | Question (ends with `?`); not a requirement. | (orchestrator should move this bullet to `## Open questions`, not rewrite as EARS.) |
| 9 | The system must validate the email field. | non-conformant | Modal verb `must` instead of `shall`. | The system shall validate the email field. |
| 10 | The user should be able to log in via SSO. | non-conformant | Subject is `The user`, not the named system; modal is `should`, not `shall`. | When a user initiates SSO sign-in, the system shall delegate authentication to the configured identity provider. |
| 11 | An email shall be sent to the user on checkout completion. | non-conformant | Passive voice — `shall` present but the system is not the grammatical subject of the consequence clause. | When checkout completes, the system shall send a confirmation email to the user. |
| 12 | The system shall validate the email and the system shall send a confirmation message. | non-conformant | Two `shall` clauses joined by `and` without Complex keywords — packs two requirements into one sentence. | Split into two requirements: `The system shall validate the email.` and `When email validation succeeds, the system shall send a confirmation message.` |

## Compare against expected

Reading the Expected-pattern column of each fixture row and comparing to the Actual column above:

| # | Expected | Actual | Match? |
|---|---|---|---|
| 1 | ubiquitous | ubiquitous | ✓ |
| 2 | event-driven | event-driven | ✓ |
| 3 | state-driven | state-driven | ✓ |
| 4 | optional-feature | optional-feature | ✓ |
| 5 | unwanted-behavior | unwanted-behavior | ✓ |
| 6 | unwanted-behavior | unwanted-behavior | ✓ |
| 7 | complex | complex | ✓ |
| 8 | non-conformant | non-conformant | ✓ |
| 9 | non-conformant | non-conformant | ✓ |
| 10 | non-conformant | non-conformant | ✓ |
| 11 | non-conformant | non-conformant | ✓ |
| 12 | non-conformant | non-conformant | ✓ |

**Result:** 12 of 12 rows match. T11 passes.

## Verdict-label coverage

Per T10, at least one row per verdict label must appear in the actual classifications:

- ubiquitous: row 1 ✓
- event-driven: row 2 ✓
- state-driven: row 3 ✓
- optional-feature: row 4 ✓
- unwanted-behavior: rows 5, 6 ✓
- complex: row 7 ✓
- non-conformant: rows 8, 9, 10, 11, 12 ✓

All seven verdict labels exercised.

## Notes

- The classification procedure converged in one pass for every sentence — no row required an iteration or a framework-text re-edit. Sentence 6 (the `If`-without-`then` edge case) and sentence 11 (the passive-voice-no-actor edge case) were the rows that adversarial-review iter-1 specifically added; both classified as expected.
- No discrepancies surfaced; `notes/deferred-findings.md` was not amended.
- Self-consistency caveat re-affirmed: the next independent verification of this skill should be a fresh-session re-execution of this fixture against the SKILL.md by a model instance that did not author either file. Tracked as a future follow-up alongside the runnable Python form (`script-ears-lint`).

## Iter-2 re-run (after Complex pre-filter restructure)

Post-EXECUTE adversarial-reviewer iter-2 added Step 0 (Complex pre-filter) to the classification procedure. Re-walking each fixture row under the updated procedure:

- Rows 1–6, 8–12: Step 0 finds zero or one leading-pattern keyword (pre-filter does not match); the cascade then resolves to the same pattern as iter-1 (Ubiquitous / Event-driven / State-driven / Optional-feature / Unwanted-behavior / Non-conformant respectively).
- Row 7: Step 0 finds two leading-pattern keywords from distinct families (`When` Event-driven + `while` State-driven), returns Complex immediately. Same outcome as iter-1.

All 12 rows still match expected. The pre-filter restructure is procedurally cleaner without changing any classification in the existing fixture; its load-bearing role is unreached by the current fixture rows beyond row 7. A future fixture extension should add a non-leading `where` row and a same-family `If … and if …` row to exercise the pre-filter's distinct-family rule (deferred per `notes/deferred-findings.md`).
