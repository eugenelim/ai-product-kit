# Assumption Tests

> The five-lens taxonomy for assumption testing, defined by David J. Bland and Alex Osterwalder in *Testing Business Ideas: A Field Guide for Rapid Experimentation* (Wiley, 2019). Every chosen Opportunity carries an Assumption Map of its riskiest assumptions; every riskiest assumption gets a test designed under one of the five lenses (Desirability, Viability, Feasibility, Usability, Ethical). This kit's Validation phase is structured around this taxonomy; the consuming surface is the Assumption Map template (F3.3), the experiment template (F3.4), and the `hook-assumption-threshold-lock` (F2.2) that enforces the predeclared-threshold rule.

## The five lenses

Each lens names a distinct kind of risk. An assumption is **riskiest** when it sits at the intersection of "if this is wrong, we stop" and "we don't yet have evidence." The lenses help name *what kind* of evidence the test will produce.

- **Desirability** — *do customers actually want this?* The classic lens; most over-used.
  - *Worked example.* "Small-business owners will pay to schedule social posts in advance." Test: landing page + waitlist with payment intent. Threshold: ≥8% of qualified visitors leave a card.
  - *Signature failure mode — stated-preference over revealed-behavior.* Teams accept "I would definitely use this" survey answers as desirability evidence. The gap between what users say in an interview and what they do when their credit card is on the table is the entire reason landing-page-with-payment-intent exists. If the test asks but does not cost the user something (time, money, reputation, attention), the result is opinion, not desirability.
- **Viability** — *does the business model work?* Pricing, costs, distribution, lifecycle, unit economics.
  - *Worked example.* "Support cost per customer stays below $4 at our pricing." Test: 90-day proxy with the support team logging time per ticket against a synthetic billing model. Threshold: median fully-loaded ticket cost <$4 across a representative cohort.
  - *Second worked example.* "Self-serve sign-ups convert at a CAC under one month of revenue." Test: run a $5k paid-acquisition spike against the real funnel and divide spend by activated paying accounts. Threshold: CAC < first-month ARPU at a 30-day lag.
  - *Signature failure mode — support-and-success cost forgotten.* Viability tests routinely model direct cost of goods (hosting, third-party APIs, payment fees) and forget the cost of humans answering tickets, running onboarding calls, and writing custom integrations for the long tail. A feature that looks viable at $4/seat at 100 customers becomes a loss-maker at 10,000 because the per-ticket cost did not decline the way the spreadsheet assumed. Always model fully-loaded service cost, not just infrastructure cost.
- **Feasibility** — *can we build this with current technology, team, and time?*
  - *Worked example.* "We can deliver sub-200ms p99 response time at 10k concurrent users on our current stack." Test: spike + load test against a representative workload, including the slowest 1% of tenants' data shapes. Threshold: p99 < 200ms sustained over a 30-minute soak.
  - *Signature failure mode — passes in a controlled environment, breaks at production scale.* Feasibility tests are usually run on clean fixtures with a single tenant, no noisy neighbours, and no real-world data skew. Production has cold caches, lock contention on hot rows, retry storms, and the one customer whose dataset is 200x the median. A feasibility test that does not exercise multi-tenant interaction, cache-cold paths, and the 99th-percentile data shape will pass at design time and fail the week after launch.
- **Usability** — *can customers use what we build without intolerable friction?*
  - *Worked example.* "First-time users find the dashboard's saved-view list within two clicks." Test: 5-user moderated usability with task success metric. Threshold: ≥4/5 complete the task unaided in under 90 seconds.
  - *Signature failure mode — 5-user studies miss the long tail.* The Nielsen "5 users find 85% of usability issues" rule applies to *catastrophic* issues in a *homogeneous* user pool. It does not apply to issues affecting users with disabilities, users on low-bandwidth connections, users on the smallest supported screen, users on the oldest supported browser, or non-native speakers of the interface language. Usability tests that sample only the modal user systematically ship working software that excludes the tail — and the tail is where compliance, accessibility, and brand-damage risk live. Sample for the edges deliberately.
- **Ethical** — *should we build this?* What does it do to vulnerable users; second-order effects; externalities; consent.
  - *Worked example.* "The recommendation engine doesn't disproportionately demote content from minority creators." Test: bias audit on a stratified sample. Threshold: <5% relative-rate gap between strata on the impression-share metric.
  - *Second worked example.* "The new pricing tier does not push existing free-tier users with no upgrade path into churn." Test: segment the free-tier cohort against the proposed paywall, model the cohort whose use case is now unsupported, and confirm with five qualitative interviews from that cohort. Threshold: <10% of the affected cohort has no acceptable upgrade or alternative.
  - *Signature failure mode — the affected populations are not in the sample.* Ethical tests are most often run by the team that built the feature, on data the team already has, using metrics the team chose. The population most exposed to the externality — minority creators, low-income users, users in adversarial jurisdictions, children, users with disabilities — is rarely overrepresented in the test set and is often absent entirely. An ethical test whose sample does not deliberately oversample the at-risk population is not an ethical test; it is a comfort test.
  - *Kit framing.* **The ethical lens is a kit addition** — Bland & Osterwalder (2019) name four lenses (Desirability, Viability, Feasibility, Usability); the kit treats Ethical as a co-equal fifth lens because every shipped feature carries ethical surface and the cheapest place to surface it is during test design.

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
