# Validation Theatre

> The failure mode where validation rituals happen but the result has no decision-power — the team feels rigorous but the work proceeds regardless of what was learned. This framework is kit synthesis grounded in Marty Cagan's "feature factory" framing (*Inspired*, 2017) and Teresa Torres's discipline distinguishing genuine discovery from ritual (*Continuous Discovery Habits*, 2021). The kit's frontline anti-theatre check is the "would you pull the work?" question; the consuming agent is `assumption-skeptic` (planned — ROADMAP P3.2).

## The four signature failure modes

Validation theatre takes four recognizable shapes. They are not mutually exclusive — a single test can manifest all four.

- **The predetermined-outcome theatre.** "We already decided to ship; the test is just to make ourselves feel better." The decision was made in a meeting last week; the test is ritual cover. The threshold can be hit or missed; the work proceeds either way. This is Cagan's "feature factory" pattern at the test-design layer — the organization performs validation as ceremony around a commitment that has already calcified. The tell is sequencing: in genuine discovery the test precedes the commitment; in theatre the commitment precedes the test and the test is scoped to fit it.
  - *Recognition signal:* the test was scoped **after** the launch date was set, and the team cannot articulate a single concrete thing that would change about the launch if the test failed. Common example: a "concept validation" survey designed in the same sprint as the eng team starts the build.
- **The floor-it threshold theatre.** "We set the bar low enough that everything passes." A 5% conversion target on a landing page is below baseline; a "≥1 enthusiastic user out of 5" usability target is not falsifiable. The threshold exists; the falsification is impossible. The threshold-lock hook catches the absence of a threshold, but it cannot judge whether a written threshold is meaningful — that requires either a baseline comparison or `assumption-skeptic` review.
  - *Recognition signal:* the predeclared threshold sits at or below the test's known baseline (current conversion, historical retention, prior survey score) — "surviving" is mathematically necessary rather than evidentially informative. Common example: "at least one user says they would use this" against an audience pre-recruited for interest.
- **The no-consequences theatre.** "We ran the test but won't actually pull the work if it fails." The threshold is real; the will to act on a fail is absent. This is the failure mode the "would you pull the work?" test exposes. **This is the most prevalent mode in product practice** — most teams know how to set a threshold and size a sample; far fewer have pre-committed to the consequence of a fail. When in doubt, assume this is the mode you are in and check first. The theatre is socially comfortable because nobody loses face from a failed test that has no consequence; the cost is that the org learns nothing it acts on.
  - *Recognition signal:* the test outcome shows up as a status update in a weekly review ("we ran the test, here are the numbers") and never as a decision input ("the test failed, therefore we are pulling X") — the result is reported, not acted upon. Common example: a Learning Memo with `status: killed` filed against an initiative that nevertheless ships on its original date.
- **The undersized-power theatre.** "The test is too small or too short to discriminate, but we're calling it done anyway." A 5-user usability test against a feature with 10,000 users; a 48-hour A/B test on a retention metric that requires 14–28 days of post-event observation to stabilize. The methodology can't separate signal from noise, so the result is whatever the team wants it to be. Torres's continuous-discovery discipline addresses the qualitative version of this mode (under-sampled interview rounds); the quantitative version requires a pre-test power calculation and is usually skipped.
  - *Recognition signal:* the confidence interval on the result spans both the success and the failure region — the same data is consistent with the assumption surviving **and** with it being killed, so the test discriminates nothing. Common example: declaring a retention experiment "successful" at day 3 because early-window engagement looks fine.
- **The wrong-population theatre.** The test runs with the right methodology and the right sample size, but with the wrong population — existing power users instead of the target segment, internal stakeholders instead of customers, or one cohort treated as representative of all. The test can "pass" while the assumption about the target population remains untested. Population validity is a separate dimension from statistical power; both can fail independently — and population error is the harder failure to detect from the result alone, because the numbers look clean.
  - *Recognition signal:* the test's sample frame (who actually got the survey, prototype, or experiment) and the assumption's target population (the segment the strategic bet is about) are not the same set — and no one on the team has written down the gap. Common example: a willingness-to-pay test run against existing free-tier users to validate a new top-tier price point.

## The "would you pull the work?" test

The single most discriminating question for any proposed validation. Ask the team **before** the test runs:

> "If this test fails the predeclared threshold, will we actually stop / kill / re-scope the work?"

If the answer is "no, regardless of the result," the test is theatre — kill the test, save the cost. The phrase **pull the work** is the kit's anti-theatre shibboleth; it is shorter than "stop, kill, or re-scope the work" and forces the team to name the consequence in concrete terms.

This question is the kit's frontline anti-theatre check. The `assumption-skeptic` agent (planned — ROADMAP P3.2) will dispatch it against every proposed test in the assumption-map. A test that does not survive the question should not be run; the cost of the test is wasted.

The question's force is in the timing: asked **before** the test, it surfaces the predetermined-outcome theatre; asked **after** a failed test, it becomes a post-hoc rationalization debate. Ask before.

## How the kit guards against theatre

The kit has four mechanical guards plus one human discipline:

- **Predeclared thresholds.** The `hook-assumption-threshold-lock` PreToolUse hook (F2.2, shipped — registered in `.claude/settings.json`; implementation at `scripts/check-assumption-threshold.py`; contract at `.claude/hooks/assumption-threshold-lock.md`) refuses to write `validation/experiments/**/results.md` unless a threshold was filed first. Catches the floor-it and absent-threshold modes.
- **Falsification framing.** `context/frameworks/falsification.md` is the rule library; the kit's vocabulary distinguishes `survived` from `validated` and reserves `killed` as a first-class status. Catches the soft-confirm mode.
- **Explicit `status: killed` in Learning Memos.** F3.5 template requires a status field with `survived | killed | pending` values. A team whose kill-rate is zero across many tests is running theatre by aggregate signal even if each individual test looks rigorous.
- **The "would you pull the work?" test.** Dispatched by `assumption-skeptic` (planned — ROADMAP P3.2) against each proposed test before it runs.
- **The Discovery → Validation handover contract** in `docs/HANDOVERS.md` §"Handover 2". An Opportunity cannot cross into Validation as the `chosen_opportunity:` until its riskiest assumption is named **and** the test design includes a predeclared threshold. The handover is the discipline-gate.

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
