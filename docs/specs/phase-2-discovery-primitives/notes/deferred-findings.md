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

## D-QE-O2 — `validate_ost.py` `--verbose` mode

- **Source:** quality-engineer review iter-1 (O2).
- **Finding.** When Rule 1 (`change-set-determinism`) fires, the consumer sees the directional diff (added per iter-1 fix to remediation), but cannot inspect the intermediate `applied` tree without instrumenting the script. For a hook-fired invocation, a user with a confusing failure has no recourse short of reading the source.
- **When to address.** When the F2.7 (`hook-validate-ost`) PostToolUse hook starts producing real Rule 1 failures in the wild and the directional-diff remediation isn't enough. Sub-task of F2.7.

## D-QE-R2 — defensive `outcome.id` access in `_check_change_set_consistency`

- **Source:** quality-engineer review iter-1 (R2).
- **Finding.** Line 178 of `validate_ost.py` (pre-fix; line numbers shifted after iter-1 fixes) builds `known_ids` from `input_tree["outcome"]["id"]` with a direct subscript. If schema validation silently passed an `outcome` without an `id` (shouldn't happen, but the in-line schema validator returns on the first error and is not exhaustive), this subscript crashes. Iter-1 partially mitigated by making `outcome` optional and gating the `known_ids` build with `.get`.
- **When to address.** When the schema validator is made exhaustive, OR when a real malformed-input case slips past schema validation in production. Sub-task of the schema-validator refactor (no current ROADMAP item).

## D-QE-R3 — `_FORMAT` module-level global

- **Source:** quality-engineer review iter-1 (R3).
- **Finding.** `_FORMAT` is mutated by `main()`. If `main()` is ever called more than once in the same Python process (e.g., via `importlib`), the first call's format persists. All 20+ tests use `subprocess.run`, so this is not a live bug — it becomes one only if tests are refactored for speed.
- **When to address.** If/when the validator becomes invocable as an in-process library (the F2.7 hook could conceivably import-and-call instead of shell-out). Sub-task of F2.7.

## D-QE-T4 — `no-data-loss` fixture conflates two sub-rules

- **Source:** quality-engineer review iter-1 (T4).
- **Finding.** The current `invalid/no-data-loss/` fixture deletes an Opportunity that has both IS-ref evidence AND child nodes (well, no — the current fixture only has evidence, no child node; the children case is in `no-data-loss-delete-with-children/`). The QE finding noted ambiguity; reviewing the fixture confirms it tests only the IS-ref-loss sub-rule. Diagnostic value is fine; the finding may have been mistaken about scope.
- **When to address.** When adding additional fixture coverage; not blocking.

## D-QE-F2 — concurrent F2.7 hook invocation semantics

- **Source:** quality-engineer review iter-1 (F2).
- **Finding.** When the F2.7 PostToolUse hook fires twice concurrently on the same `discovery/trees/` file (two agent threads writing in parallel), both validators see the same on-disk state but may have stale `--input` files prepared by their respective callers. The validator is read-only and pure-functional; the concern is a deployment-side ambiguity, not a script bug. The spec doesn't explicitly require call-side stability of the three JSON files at invocation time, though it's implicit in the script's "three JSON files, all required" contract.
- **When to address.** When F2.7 ships — the hook's spec should document that input stability is the caller's responsibility. Sub-task of F2.7.

## D-E6 — `merge` with non-existent source id

- **Source:** adversarial-review iter-1 (E6).
- **Finding.** Test 17 (`test_merge_with_nonexistent_id_exits_2`) is now in the contract, addressing the spec-side gap. What remains deferred: the `references/action-vocabulary.md` should explicitly note the "internally-inconsistent change set ⇒ exit 2, not 1" rule for **every** action verb that takes an id reference (not just `merge`). The convention applies to `delete`, `reparent`, `reframe`, `split`, `add-source-opportunity` (target reference) as well. The spec covers `merge` by example; the vocabulary doc should generalize.
- **When to address.** During T1 (the action-vocabulary.md authoring) — call this out in each verb's entry. If T1 ships without this, log as a follow-up sub-task of D4.
