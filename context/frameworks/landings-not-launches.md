# Landings, not Launches

> Kit synthesis grounded in Marty Cagan's outcome-vs-output discipline (*Inspired*, Wiley, 2nd ed. 2017; *Empowered*, Wiley, 2020). The framing: shipping code is the **start of the adoption work**, not the end of the build work. The kit's Phase 5 is named "Landings" — not "Launches" — precisely because the work of adoption is part of the work, not a marketing follow-on. Consumers are the Landing Report template (F3.10, shipped) and `/landing-report` (planned — ROADMAP P5.1). Note: "Landings, not Launches" is kit synthesis grounded in Cagan; it is not a framework Cagan publishes under that name.

## "Launches are starts, not ends"

The traditional product calendar treats launch as the terminal event: build → test → launch → celebrate → move on. Reality treats launch as the inflection where adoption work begins. A product that ships but is not adopted has produced output without outcome — and Cagan's "feature factory" failure mode (`context/frameworks/validation-theatre.md`) lives in the gap.

The kit's Phase 5 makes adoption work an explicit phase with its own handover artifact (the Landing Report). Phase 4 (Delivery) ends at code-in-prod; Phase 5 (Landings) begins there and ends at outcome-realized-or-rejected. Skipping Phase 5 is the most common failure mode in product practice — and the most expensive, because the work that didn't land is rarely surfaced before the next quarter's commitments lock in.

The phrase "Landings, not Launches" names the discipline: launches are events; landings are work.

## The adoption curve

The adoption curve is the work between code-in-prod and outcome-realized. Adoption is the bridge; without it, **shipped output ≠ realized outcome**. Adoption work includes:

- **Targeted rollout** to first cohorts (not big-bang to everyone; segmented by readiness).
- **Enablement** — docs, training, in-product nudges, integration support.
- **Friction removal** as early adopters surface what the team missed.
- **Measurement against predeclared thresholds** — *not* retroactively-justified numbers. The thresholds come from the parent Vision (declared before code shipped), per the kit's predeclared-threshold discipline (`context/frameworks/falsification.md`).

A team that ships into a 100% rollout with no measurement plan has skipped every step. The Landing Report is the artifact that forces the team to write the adoption work down.

## What a landing report contains

The kit's Landing Report (F3.10 template at `templates/landing-report.md` + `/landing-report` command planned — ROADMAP P5.1) has three load-bearing sections:

- **Adoption** — who actually started using it, segmented by cohort / segment / surface. Not aggregate DAU; segmented adoption with the missing-cohort question explicit.
- **Outcome** — did the predeclared parent-Vision metric move, measured against the predeclared threshold? Verdict is `adopt | fix | kill`.
- **Counter-metric** — what regressed. Every win has a cost; the counter-metric is what you don't want to see degrade. If the team can't name a counter-metric, the report is incomplete — the team didn't know what cost they were willing to pay.

All three measured against thresholds declared **in the parent Vision before code shipped**, not numbers reverse-engineered from the result. This is the predeclared-threshold discipline applied at the post-ship boundary.

## Common failure modes

- **Declaring victory at code-in-prod.** The most common failure. Output is mistaken for outcome; the team moves to the next thing while the previous thing decays silently.
- **Measuring adoption without a counter-metric.** You don't see the regressions you caused. A feature can increase one metric and decrease another by more; without the counter-metric, the gain is uncosted.
- **Shipping without a predeclared outcome target.** No way to know whether it worked, so any number is reported as success. This is the predeclared-threshold failure mode (`context/frameworks/falsification.md`) at the post-ship layer.
- **Adoption theatre** — measuring *usage* but not asking whether the usage produced the *outcome*. DAU as a proxy for value-realized is a category error when the actual outcome metric is something else (retention, revenue, NPS, time-to-completion). Usage is necessary but not sufficient.

## How the kit uses this framework

- **Landing Report template** (F3.10, shipped at `templates/landing-report.md`) — the artifact that closes the loop.
- **`/landing-report`** (planned — ROADMAP P5.1) — drafts the report against the parent Vision's predeclared thresholds.
- **`/adoption-readout`** (planned — ROADMAP P5.2) — adoption curve only, faster cadence than the full Landing Report.
- **`/outcome-vs-prediction`** (planned — ROADMAP P5.3) — mechanical diff against predeclared thresholds; the verdict generator.
- **`/cohort-analysis`** (planned — ROADMAP P5.4) and `cohort-analyst` agent (planned — P5.5) — slice by segment / surface / cohort.
- **`/landing-interview`** (planned — ROADMAP P5.6) — qualitative follow-up with adopters AND non-adopters.
- **`landing-skeptic` agent** (planned — ROADMAP P5.7) — asks "what would have to be true for us to revert?" against every Landing Report.
- **`/audit-landings-debt`** (planned — ROADMAP P5.9) — flags shipped initiatives without a Landing Report after 30 days.
- **`landings-manager` scheduled agent** (planned — ROADMAP P5.10) — mid-week landings-debt scan.

Frame: Phase 5 is structured around this framework. The Landing Report is the Phase 5 handover artifact that feeds the next Strategy cycle.

## References

- Cagan, M. (2017). *Inspired: How to Create Tech Products Customers Love* (2nd ed.). Wiley. The canonical source for the outcome-vs-output discipline that grounds this framework.
- Cagan, M., & Jones, C. (2020). *Empowered: Ordinary People, Extraordinary Products*. Wiley. The companion source — names "missionaries, not mercenaries" and the discipline of teams that own outcomes, not output.

Note: **"Landings, not Launches" is kit synthesis grounded in Cagan's outcome-vs-output discipline** — it is not a phrase or framework Cagan publishes under that name. The phrase and the Phase-5 structure are kit-original.

- `context/frameworks/falsification.md` — the predeclared-threshold discipline applied at the post-ship layer.
- `context/frameworks/validation-theatre.md` — the feature-factory failure mode that this framework is structured to prevent.
- `context/frameworks/continuous-discovery.md` — the same outcome-vs-output discipline applied at the Discovery boundary.
- `templates/landing-report.md` — the kit's Landing Report template.
- `docs/PHASE-GUIDE.md` §"Landings" — the phase-level handover contract.
