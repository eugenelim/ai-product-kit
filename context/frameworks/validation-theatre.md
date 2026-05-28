# Validation Theatre

> The failure mode where validation rituals happen but the result has no decision-power — the team feels rigorous but the work proceeds regardless of what was learned. This framework is kit synthesis grounded in Marty Cagan's "feature factory" framing (*Inspired*, 2017) and Teresa Torres's discipline distinguishing genuine discovery from ritual (*Continuous Discovery Habits*, 2021). The kit's frontline anti-theatre check is the "would you pull the work?" question; the consuming agent is `assumption-skeptic` (planned — ROADMAP P3.2).

## The four signature failure modes

Validation theatre takes four recognizable shapes. They are not mutually exclusive — a single test can manifest all four.

- **The predetermined-outcome theatre.** "We already decided to ship; the test is just to make ourselves feel better." The decision was made in a meeting last week; the test is ritual cover. The threshold can be hit or missed; the work proceeds either way. This is Cagan's "feature factory" pattern at the test-design layer.
- **The floor-it threshold theatre.** "We set the bar low enough that everything passes." A 5% conversion target on a landing page is below baseline; a "≥1 enthusiastic user out of 5" usability target is not falsifiable. The threshold exists; the falsification is impossible.
- **The no-consequences theatre.** "We ran the test but won't actually pull the work if it fails." The threshold is real; the will to act on a fail is absent. This is the failure mode the "would you pull the work?" test exposes.
- **The undersized-power theatre.** "The test is too small or too short to discriminate, but we're calling it done anyway." A 5-user usability test against a feature with 10,000 users; a 48-hour A/B test on a metric that takes weeks to materialize. The methodology can't separate signal from noise, so the result is whatever the team wants it to be.
- **The wrong-population theatre.** The test runs with the right methodology and the right sample size, but with the wrong population — existing power users instead of the target segment, internal stakeholders instead of customers, or one cohort treated as representative of all. The test can "pass" while the assumption about the target population remains untested. Population validity is a separate dimension from statistical power; both can fail independently.

## The "would you pull the work?" test

The single most discriminating question for any proposed validation. Ask the team **before** the test runs:

> "If this test fails the predeclared threshold, will we actually stop / kill / re-scope the work?"

If the answer is "no, regardless of the result," the test is theatre — kill the test, save the cost. The phrase **pull the work** is the kit's anti-theatre shibboleth; it is shorter than "stop, kill, or re-scope the work" and forces the team to name the consequence in concrete terms.

This question is the kit's frontline anti-theatre check. The `assumption-skeptic` agent (planned — ROADMAP P3.2) will dispatch it against every proposed test in the assumption-map. A test that does not survive the question should not be run; the cost of the test is wasted.

The question's force is in the timing: asked **before** the test, it surfaces the predetermined-outcome theatre; asked **after** a failed test, it becomes a post-hoc rationalization debate. Ask before.

## How the kit guards against theatre

The kit has four mechanical guards plus one human discipline:

- **Predeclared thresholds.** The `hook-assumption-threshold-lock` hook (F2.2, shipped at `scripts/check-assumption-threshold.py`) refuses to write `validation/experiments/**/results.md` unless a threshold was filed first. Catches the floor-it and absent-threshold modes.
- **Falsification framing.** `context/frameworks/falsification.md` is the rule library; the kit's vocabulary distinguishes `survived` from `validated` and reserves `killed` as a first-class status. Catches the soft-confirm mode.
- **Explicit `status: killed` in Learning Memos.** F3.5 template requires a status field with `survived | killed | pending` values. A team whose kill-rate is zero across many tests is running theatre by aggregate signal even if each individual test looks rigorous.
- **The "would you pull the work?" test.** Dispatched by `assumption-skeptic` (planned — ROADMAP P3.2) against each proposed test before it runs.
- **The Discovery → Validation handover contract** in `docs/HANDOVERS.md`. An Opportunity cannot cross into Validation as `chosen: true` until its riskiest assumption is named **and** the test design includes a predeclared threshold. The handover is the discipline-gate.

## How the kit uses this framework

- **`assumption-skeptic` agent** (planned — ROADMAP P3.2) — the consumer of the "would you pull the work?" test.
- **`hook-assumption-threshold-lock`** (F2.2, shipped) — the mechanical guard against absent and floor-it thresholds.
- **Experiment template** (F3.4, shipped) — the Threshold field carries the predeclared bar.
- **Learning Memo template** (F3.5, shipped) — the `status: killed` vocabulary that makes kill-rate visible.
- **The Validation phase commands** (planned — ROADMAP): `/assumption-test` (P3.1), `/design-experiment` (P3.4), `/run-assumption-test` (P3.7), `/falsify-or-confirm` (P3.8), `/kill-or-survive` (P3.9), `/learning-memo` (P3.10).

Frame: this framework is the anti-theatre rubric; the consumers above mechanically enforce parts of it. The rest is human discipline — the rubric makes the discipline nameable.

## References

- Cagan, M. (2017). *Inspired: How to Create Tech Products Customers Love* (2nd ed.). Wiley. The canonical source for the "feature factory" framing — organizations that ship without learning.
- Torres, T. (2021). *Continuous Discovery Habits*. Product Talk LLC. The canonical source for the discipline distinguishing genuine discovery from ritual.

Note: **"Validation Theatre" as a named framework is kit synthesis grounded in Cagan and Torres** — neither author publishes a framework under that name. Cagan supplies the feature-factory diagnosis; Torres supplies the continuous-discovery discipline; this framework names the failure mode that lives in the gap between them.

- `context/frameworks/falsification.md` — the epistemological grounding.
- `context/frameworks/assumption-tests.md` — the test-card schema this framework gates.
- `.claude/hooks/assumption-threshold-lock.md` — the threshold-lock hook contract.
