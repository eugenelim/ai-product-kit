# Assumption Tests

> The five-lens taxonomy for assumption testing, defined by David J. Bland and Alex Osterwalder in *Testing Business Ideas: A Field Guide for Rapid Experimentation* (Wiley, 2019). Every chosen Opportunity carries an Assumption Map of its riskiest assumptions; every riskiest assumption gets a test designed under one of the five lenses (Desirability, Viability, Feasibility, Usability, Ethical). This kit's Validation phase is structured around this taxonomy; the consuming surface is the Assumption Map template (F3.3), the experiment template (F3.4), and the `hook-assumption-threshold-lock` (F2.2) that enforces the predeclared-threshold rule.

## The five lenses

Each lens names a distinct kind of risk. An assumption is **riskiest** when it sits at the intersection of "if this is wrong, we stop" and "we don't yet have evidence." The lenses help name *what kind* of evidence the test will produce.

- **Desirability** — *do customers actually want this?* The classic lens; most over-used. Example: "small-business owners will pay to schedule social posts in advance" (test: landing page + waitlist with payment intent).
- **Viability** — *does the business model work?* Pricing, costs, distribution, lifecycle, unit economics. Example: "support cost per customer stays below $4 at our pricing" (test: 90-day proxy with the support team logging time per ticket against a synthetic billing model).
- **Feasibility** — *can we build this with current technology, team, and time?* Example: "we can deliver sub-200ms response time at 10k concurrent users on our current stack" (test: spike + load test against a representative workload).
- **Usability** — *can customers use what we build without intolerable friction?* Example: "first-time users find the dashboard's saved-view list within two clicks" (test: 5-user moderated usability with task success metric).
- **Ethical** — *should we build this?* What does it do to vulnerable users; second-order effects; externalities; consent. Example: "the recommendation engine doesn't disproportionately demote content from minority creators" (test: bias audit on a stratified sample). **The ethical lens is a kit addition** — Bland & Osterwalder (2019) name four lenses (Desirability, Viability, Feasibility, Usability); the kit treats Ethical as a co-equal fifth lens because every shipped feature carries ethical surface and the cheapest place to surface it is during test design.

## The test card schema

Every assumption test carries five fields, declared **before** the test runs:

1. **Hypothesis** — one falsifiable statement. Not "users will like it"; rather "≥40% of first-time users will create a saved view within their first 10-minute session."
2. **Test** — the cheapest method that could falsify the hypothesis. Cheap-and-fast beats elaborate-and-slow.
3. **Metric** — what we measure. Must be the same metric named in the hypothesis.
4. **Threshold** — the bar that decides survive-or-kill, **declared before the test runs**. The kit's `hook-assumption-threshold-lock` (F2.2, shipped at `scripts/check-assumption-threshold.py`) refuses to write `validation/experiments/**/results.md` unless a threshold was filed first. This is load-bearing.
5. **Outcome** — what actually happened, recorded **after**. Includes the raw number and the verdict (survived | killed) against the predeclared threshold.

The card is the artifact; the discipline is the predeclared-threshold rule. See `context/frameworks/falsification.md` for the epistemological grounding.

## Common failure modes

- **Desirability-only testing** — running only desirability tests and treating "they say they want it" as validation. Viability, feasibility, usability, and ethical risks remain untested. Most common in early-stage product work.
- **Confirmation-biased threshold setting** — setting the threshold low enough that the assumption can't fail. A 5% conversion target on a landing page is below baseline; "surviving" means nothing. The threshold is the falsification bar, not the hope.
- **"We'll know it when we see it" non-threshold** — no pre-declared metric; the test runs, a number appears, and the team retrofits a story. This is the failure mode the F2.2 hook exists to prevent.
- **Run-and-don't-pull** — running the test but having no intention of pulling the work on failure. The "would you pull the work?" test (see `context/frameworks/validation-theatre.md`) is the discriminator: if the answer is no, the test is theatre.
- **Single-test validation** — treating one survived test as validation. Validation requires many surviving attempts at increasing thresholds across distinct conditions; one survival just postpones the decision. See `context/frameworks/falsification.md` §"What 'survived' means."

## How the kit uses this framework

- **Assumption Map template** (`templates/assumption-map.md`, F3.3, shipped) — the artifact that holds the chosen Opportunity's riskiest assumptions, classified by lens.
- **Experiment template** (F3.4, shipped) — the test-card-shaped artifact for a single experiment, including the Threshold field.
- **`hook-assumption-threshold-lock`** (F2.2, shipped at `scripts/check-assumption-threshold.py`; documented at `.claude/hooks/assumption-threshold-lock.md`) — the kit's mechanical enforcement of the predeclared-threshold rule. Refuses to write `validation/experiments/**/results.md` unless a threshold was filed before the experiment ran.
- **Commands** (all planned — ROADMAP): `/assumption-test` (P3.1) designs a test under the five lenses; `/design-experiment` (P3.4) turns the design into a runnable experiment with predeclared threshold; `/run-assumption-test` (P3.7) captures results and computes pass/fail; `/falsify-or-confirm` (P3.8) writes the Learning Memo and flips status.
- **`assumption-skeptic` agent** (planned — ROADMAP P3.2) — dispatches the "would you pull the work?" question against any proposed test (see `context/frameworks/validation-theatre.md`).

Frame: this framework is the rule library the Validation phase consumes; the consumers above produce the artifacts the kit's Discovery → Validation → Delivery pipeline depends on.

## References

- Bland, D. J. & Osterwalder, A. (2019). *Testing Business Ideas: A Field Guide for Rapid Experimentation*. Wiley. The canonical source for the five-lens taxonomy (Desirability / Viability / Feasibility / Usability) and the test-card schema. Bland's subsequent public work adds the Ethical lens; the kit treats all five as canonical.
- `context/frameworks/falsification.md` — the epistemological grounding for the predeclared-threshold discipline.
- `context/frameworks/validation-theatre.md` — the "would you pull the work?" anti-theatre check that gates every test.
- `templates/assumption-map.md` — the kit's Assumption Map template.
- `.claude/hooks/assumption-threshold-lock.md` — the threshold-lock hook contract.
