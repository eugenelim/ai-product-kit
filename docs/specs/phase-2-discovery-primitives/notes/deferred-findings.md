# Deferred findings — phase-2-discovery-primitives

Items the adversarial review on 2026-05-28 surfaced that this batch does not address. Each row carries an explicit **when to address** trigger so the next loop knows what to wait for.

## D-H3 — discovery-coach visibility surface for PMs

- **Source:** adversarial-review iter-1 (H3).
- **Finding.** The `discovery-coach` agent is manually invocable, but a PM hitting the stuck condition has no PM-facing surface that points them at the agent. AGENTS.md is not edited by this batch; the agent README will get a row, but a PM in flow does not check `.claude/agents/README.md`.
- **When to address.** When `context/frameworks/opportunity-solution-tree.md` is next edited (e.g., during P2.7 / P2.9 work-loop or the next reconcile-and-harden pass), add a one-sentence pointer to the agent in §"Common failure modes" under a new "The 'stuck Opportunity' failure" entry. No spec required for that edit; sub-task of P2.11 or P2.7 work-loop's capture phase.

## D-V3 — `.claude/skills/ost-validator/SKILL.md` "typically converges in 1-2 turns"

- **Source:** adversarial-review iter-1 (V3).
- **Finding.** The repair-loop protocol in the existing skill says "typically converges in 1–2 turns. If 5 turns without convergence, abort." The "typically" is vague; the abort threshold is named but the audit of in-the-wild convergence rates has never been performed.
- **When to address.** When the validator script ships and `/generate-ost` (P2.7) or `/update-ost` (P2.9) produces real change sets, log per-invocation turn counts. Reconcile the published "typically 1–2 turns" against observed data. Sub-task of P2.9.

## D-E6 — `merge` with non-existent source id

- **Source:** adversarial-review iter-1 (E6).
- **Finding.** Test 17 (`test_merge_with_nonexistent_id_exits_2`) is now in the contract, addressing the spec-side gap. What remains deferred: the `references/action-vocabulary.md` should explicitly note the "internally-inconsistent change set ⇒ exit 2, not 1" rule for **every** action verb that takes an id reference (not just `merge`). The convention applies to `delete`, `reparent`, `reframe`, `split`, `add-source-opportunity` (target reference) as well. The spec covers `merge` by example; the vocabulary doc should generalize.
- **When to address.** During T1 (the action-vocabulary.md authoring) — call this out in each verb's entry. If T1 ships without this, log as a follow-up sub-task of D4.
