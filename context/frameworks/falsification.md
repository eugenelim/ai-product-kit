# Falsification

> The epistemological asymmetry between confirmation and refutation, from Karl Popper's *The Logic of Scientific Discovery* (Logik der Forschung, 1934; English ed. 1959, Hutchinson). A single counter-example can refute a universal claim; no number of confirming observations can prove one. The kit operationalizes this insight as the predeclared-threshold pattern enforced by `hook-assumption-threshold-lock` (F2.2, shipped) and as the `status: survived | killed` vocabulary in Learning Memos (F3.5).

## What "survived" means

**Survived ≠ confirmed.** An assumption survives one falsification attempt at one predeclared threshold; the bar to convert "survived" into "validated" is many surviving attempts at increasing thresholds across distinct conditions. This is Popper's logic applied to product work: positive results are weaker evidence than negative results, because positive results can come from confounds, biased sampling, or insufficient power.

The kit's Learning Memo template (F3.5, shipped at `templates/learning-memo.md`) carries a `status:` field with exactly three values: `survived`, `killed`, or `pending`. The vocabulary is deliberate — `survived` does not mean "the assumption is now true," it means "this one test did not kill it at this one threshold." A team that treats a single survival as confirmation is committing the soft-confirm failure mode named below.

## The predeclared-threshold pattern

**What counts as falsified must be declared before the test runs.** Without a predeclared threshold, every result can be post-hoc rationalized into a survival ("the conversion rate was lower than we hoped but the segment was unrepresentative"; "the latency missed the SLA but the test load was unrealistic"). The threshold itself lives in the test-card schema defined in `context/frameworks/assumption-tests.md` (the Threshold field). The kit's `hook-assumption-threshold-lock` (F2.2, shipped — registered in `.claude/settings.json`; implementation at `scripts/check-assumption-threshold.py`; contract at `.claude/hooks/assumption-threshold-lock.md`) is the mechanical guard: it refuses to write `validation/experiments/**/results.md` unless a falsification threshold was filed before the experiment ran.

The threshold declaration must name the **statistical shape** of the metric explicitly — point estimate (e.g., "conversion rate ≥ 12%"), interval (e.g., "p-value ≤ 0.05 on a two-tailed test"), or categorical (e.g., "≥4 of 5 users complete the task unaided"). The shape must match the test's actual output; declaring a point-estimate threshold and then reporting a p-value (or vice versa) lets the team interpret the result either way after the fact. This is the prescriptive fix for the confidence-interval-confusion failure mode named below.

This is the kit's signature guard — the one PreToolUse hook that protects the falsification discipline at write-time, not at review-time. Post-hoc rationalization is the dominant failure mode in product validation; the hook makes the rationalization mechanically visible by refusing the write that would conceal it.

## Why the kit is asymmetric

Falsification kills cheaply; survival only postpones. The asymmetry is Popper's logical insight: under uncertainty, the cheapest way to make decisions is to **try to kill ideas**, not to defend them.

The kit's pipeline (Discovery → Validation → Delivery → Landings) is structured to maximize kill-rate, not survival-rate. A chosen Opportunity should aim to be killed before delivery, because killing in Validation is orders of magnitude cheaper than killing in Delivery (or worse, in Landings after launch). A team whose kill-rate is zero is either working on trivially-correct assumptions or running validation theatre — both diagnoses are bad.

The asymmetry shows up in the kit's downstream vocabulary too: `discovery-coach` (P2.13) and `assumption-skeptic` (P3.2) are agents designed to *find ways to kill* the current bet, not to defend it.

## Common failure modes

- **The "moving threshold"** — the threshold gets relaxed after a borderline result so the assumption survives. Defeats the entire mechanism; the hook can't catch this because the rationalization happens in commit messages and Slack threads, not in the threshold file. The mitigation is review-pass discipline (convention, not mechanically enforced): a threshold edit that lands after the experiment's result is recorded must carry a documented rationale in the threshold file itself before any reviewer accepts it.
- **The "soft confirm"** — a survived assumption is treated as validated and goes unchallenged thereafter. Subsequent decisions cite "we validated this" when the actual record reads `status: survived` on one test. The mitigation is vocabulary discipline: `survived` and `validated` are not synonyms.
- **The "absent threshold"** — the test produces a number but there's no pre-declared meaning of it, so any number is reported as "evidence." The F2.2 hook blocks this at write-time.
- **The "confidence-interval confusion"** — the experiment produces a p-value but the threshold was declared in absolute terms (or vice versa). Mismatched metric types let the team interpret the result either way. Mitigation: threshold and metric must declare the same statistical shape (point estimate vs interval vs categorical) in the experiment template.

## How the kit uses this framework

- **`hook-assumption-threshold-lock`** (F2.2, shipped — registered in `.claude/settings.json`; implementation at `scripts/check-assumption-threshold.py`; contract at `.claude/hooks/assumption-threshold-lock.md`) — the mechanical enforcer; the kit's most important PreToolUse hook.
- **Learning Memo template** (F3.5, shipped at `templates/learning-memo.md`) with its `status: survived | killed | pending` field.
- **Experiment template** (F3.4, shipped) with its predeclared Threshold field.
- **Commands** (all planned — ROADMAP): `/run-assumption-test` (P3.7) captures results and computes survive-or-kill against the predeclared threshold; `/falsify-or-confirm` (P3.8) writes the Learning Memo and flips status; `/kill-or-survive` (P3.9) formal opportunity disposition; `/learning-memo` (P3.10) synthesizes learning separately from the proceed decision.
- **`assumption-skeptic` agent** (planned — ROADMAP P3.2) — dispatches the "would you pull the work?" check from `context/frameworks/validation-theatre.md` against every proposed test.

## References

- Popper, K. R. (1934/1959). *The Logic of Scientific Discovery* [Logik der Forschung]. London: Hutchinson. The canonical source for the asymmetry between confirmation and refutation — the philosophical grounding for everything in this doc.
- `context/frameworks/assumption-tests.md` — the test-card schema that the predeclared-threshold rule applies to.
- `context/frameworks/validation-theatre.md` — the failure modes that arise when the asymmetry is ignored.
- `.claude/hooks/assumption-threshold-lock.md` — the threshold-lock hook contract.
- `templates/learning-memo.md` — the kit's Learning Memo template.
