# Jobs to Be Done

> Two distinct canonical formulations of the same insight — customers do not buy products; they hire products to make progress on a job. Clayton Christensen's "jobs hired to do" framing (*Competing Against Luck*, 2016; HBR, Sept 2016) supplies the struggle-moment lens for early discovery. Tony Ulwick's outcome-driven innovation (*What Customers Want*, 2005) supplies the four-part outcome-statement shape for late-stage prioritization. The two are complementary, not competing — this kit uses both, in different phases. Consumers are `/internal-jtbd-interview` (planned — P7.9, enterprise) and `/jtbd-analogues` (planned — P7.12, greenfield).

## The Christensen formulation — "jobs hired to do"

Clayton Christensen's framing: customers "hire" products to make progress on a job they are trying to do in their lives. The job is the customer's progress, not the product's feature.

The canonical illustration is the milkshake example: a fast-food chain wanted to grow milkshake sales; demographic segmentation suggested obvious moves. Investigation showed half of milkshakes were sold to commuters in the morning who "hired" the shake to make the drive less boring and keep them full until lunch. Competitors for the morning hire were not other milkshakes — they were bananas, bagels, and boredom. The afternoon hire (parents buying a treat for kids) had different competitors and different success criteria.

The lens directs attention to **struggle moments** in the customer's day — the points where the customer is trying to make progress and is hindered. Demographic segmentation describes who the customer is; the job describes what the customer is trying to do. The two often cross-cut: the same person hires different products for different jobs across the day.

Three diagnostic questions test whether a candidate job statement is well-formed in the Christensen sense:

1. **Is it stable across time and technology?** A real job ("get to work without being stressed") persists across decades; a feature ("ride-hail an SUV") is one of many current implementations. If the candidate job evaporates when you change the product, it is a feature in disguise.
2. **Does it admit non-obvious competitors?** The milkshake's morning competitors were bananas, bagels, and boredom — not other milkshakes. If your job statement only competes against products in your own category, it is too narrow.
3. **Does it surface a struggle moment, not a preference?** "I prefer faster cars" is a preference; "I am late and the kids' school bell rings in twelve minutes" is a struggle moment. Struggle moments have time, context, and stakes; preferences do not.

## The Ulwick formulation — outcome statements

Tony Ulwick's "Outcome-Driven Innovation" (*What Customers Want*, 2005) decomposes a job into **measurable desired outcomes**. Outcome statements have a canonical **four-part shape**:

> *Direction of improvement* + *Performance metric* + *Object of control* + *Context*

Worked example: "**Minimize** the **time it takes** to **find a missing document** when **preparing for a client meeting**." The four parts:

- **Direction:** *Minimize* (or *Maximize* / *Reduce* / *Increase* / *Stabilize*).
- **Performance metric:** *the time it takes* (or *the likelihood of* / *the number of* / *the cost of*).
- **Object of control:** *to find a missing document* — the specific thing the customer is acting on.
- **Context:** *when preparing for a client meeting* — the moment of use.

Statements in this shape are **testable**: Ulwick surveys customers on two dimensions per outcome — **importance** ("how much does this matter to you?") and **current satisfaction** ("how well is it currently served?"). Plotting outcomes on a two-axis grid surfaces the **high-importance / low-satisfaction quadrant** — the underserved outcomes where new product investment pays back. Outcomes in other quadrants either don't matter, are already well-served, or are over-served (where competitors invest disproportionately for diminishing return).

The four quadrants of the importance × satisfaction grid each carry a different strategic implication:

- **High importance, low satisfaction** — **underserved**. Investment pays back. These are the outcomes the team should target.
- **High importance, high satisfaction** — **well-served**. Investment here is table-stakes maintenance, not differentiation.
- **Low importance, low satisfaction** — **noise**. The customer does not care that it is unsolved.
- **Low importance, high satisfaction** — **over-served**. Competitors are over-investing; this is the segment ripe for low-end disruption (a cheaper, simpler product that drops the over-served outcome).

A typical Ulwick survey enumerates 50–150 outcome statements for a single job and asks each respondent to score every statement on a 1–5 importance and 1–5 satisfaction scale. Aggregated, the **opportunity score** is `importance + max(importance − satisfaction, 0)` — the formula deliberately weights importance, so a high-importance / high-satisfaction outcome still ranks above a low-importance / low-satisfaction one even though both have the same raw gap. Ulwick (*What Customers Want*, 2005, ch. 6) is the canonical source for the formula; Ulwick & Bettencourt (2008, *MIT Sloan Management Review*) covers the survey mechanics in practitioner-friendly form. The hard work is writing the outcome statements correctly; the scoring math is mechanical once the statements are in shape.

## When to use which

The two formulations are not competing; they sit at different stages of the workflow and answer different questions with different data.

- **Christensen for early-stage discovery.** *What job is the customer trying to do? Who are the unobvious competitors?* The framing is qualitative, struggle-moment-driven, and the data input is interview transcripts and field observation — what the customer said, what they were trying to do, what they hired or fired. Best used when the team does not yet know what to build. Used in interviews and snapshot extraction (see `context/frameworks/interview-snapshot.md`).
- **Ulwick for late-stage prioritization.** *Among the named outcomes for this job, which are most underserved relative to their importance?* The framing is quantitative, survey-driven, and the data input is a structured survey scoring each outcome on importance and current satisfaction (the two-axis grid in the section above). Best used when the team has a job statement and needs to choose which outcome to chase.

**The handoff between the two.** A team transitions from Christensen-style discovery to Ulwick-style prioritization at a specific point in the OST workflow: **after** an OST has surfaced a chosen Opportunity (the job is named and the rough struggle-moment is understood), but **before** the team commits to a Solution. At that boundary, the chosen Opportunity is decomposed into a list of candidate desired outcomes in Ulwick's four-part shape, surveyed for importance × satisfaction, and the underserved outcomes become the targets for Solution exploration. Skipping the Ulwick step is how teams ship Solutions targeting outcomes that are already well-served — losing the work to a stronger incumbent.

**Why the two are complementary, not redundant.** Christensen reveals the **wrong-segmentation error**: we thought we were selling to teenagers, but the morning milkshake job is hired by commuters. Ulwick reveals the **wrong-investment error**: we thought speed-of-checkout mattered most, but the survey shows speed is already well-served and the underserved outcome is recovering from a checkout error. They are different failure modes; a team using only one lens systematically misses the other.

Christensen surfaces the job; Ulwick decomposes the job into outcomes the team can rank.

## Common failure modes

- **Confusing a job with a feature.** "They want a faster checkout" is a feature request; the job is "complete the purchase quickly enough to finish before my kid wakes up." Features describe the product; jobs describe the customer's progress.
- **Confusing a job with a persona.** Personas are about who the customer is (demographics, role, segment); jobs are about what the customer is trying to do. The same person hires different products for different jobs across the day.
- **The "everyone's job" trap.** Job statements so abstract they describe every human — "the customer wants to feel productive," "the customer wants peace of mind." If the job describes everyone, it discriminates nothing.
- **The "solution-as-job" trap** — defining the job as "use our product" rather than the underlying progress the customer seeks. This is the single most common JTBD mis-application: the company restates its own product as a job, then mistakes feature usage for progress.
- **Skipping Ulwick after naming the job.** Teams sometimes stop at the Christensen step — "we know the job, let's build" — and ship Solutions targeting outcomes that turn out to be either unimportant or already well-served. The Ulwick decomposition is the cheap insurance against this; the survey is faster than the build.
- **Treating the survey as a vote on solutions.** The Ulwick survey scores **outcomes**, not features or solution concepts. Asking respondents to rate "an AI-powered document finder" mixes solution preference with outcome importance and destroys the signal. Keep the survey on outcomes; let the team generate solutions afterward.

## How the kit uses this framework

The JTBD framework itself is **mode-agnostic** — both the Christensen and Ulwick formulations are usable across greenfield and enterprise modes, and the cross-link from `context/frameworks/opportunity-solution-tree.md` (Opportunities expressed as job-fragments) applies in both. Only the specific named JTBD slash-commands below are mode-gated, because the data-gathering mechanic differs by mode (cold outreach to analogues vs. interviews with a captive user base).

- **`/internal-jtbd-interview`** (planned — ROADMAP P7.9, enterprise mode only) — interview prep and analysis for the captive user base; uses both formulations (Christensen for the interview; Ulwick for the post-interview prioritization).
- **`/jtbd-analogues`** (planned — ROADMAP P7.12, greenfield mode only) — surfaces jobs being hired-for in adjacent markets; uses primarily the Christensen formulation.
- **`context/frameworks/competitive-analysis.md`** uses JTBD as one of three lenses (with Porter's five forces and Wardley's evolution axis).
- **`context/frameworks/opportunity-solution-tree.md`** — Opportunities in an OST are often expressed as jobs or job-fragments; the Christensen formulation is the natural language.
- **`mode-guard` hook** (F2.4, shipped) — enforces mode-gated access to the JTBD commands.

The typical kit workflow that uses JTBD end-to-end:

1. **Discovery phase** — early customer interviews use the Christensen lens to surface job statements and struggle moments; `ontology-classifier` extracts `Job` objects from transcripts; jobs feed into `discovery/opportunities/` as candidate Opportunities.
2. **OST construction** — chosen Opportunities are expressed as job-fragments (e.g., "shorten the time to find a missing document during meeting prep"); the OST captures multiple jobs and their candidate Solutions.
3. **Pre-Solution prioritization** — for the chosen Opportunity, decompose into Ulwick outcome statements; run an importance × satisfaction survey; rank by opportunity score.
4. **Validation phase** — the surviving underserved outcomes become assumption-map inputs: the team commits to a specific outcome target and falsifiable threshold before building.
5. **Delivery phase** — the Spec's success criteria reference the Ulwick outcome by name and threshold; the Landing report measures whether the outcome's satisfaction score moved.

## References

- Christensen, C. M. (2016). *Competing Against Luck: The Story of Innovation and Customer Choice*. HarperBusiness. The canonical source for the "jobs hired to do" framing and the milkshake example.
- Christensen, C. M., et al. (2016, September). "Know Your Customers' Jobs to Be Done." *Harvard Business Review*. The HBR article version of the same framework.
- Ulwick, A. W. (2005). *What Customers Want: Using Outcome-Driven Innovation to Create Breakthrough Products and Services*. McGraw-Hill. The canonical source for the four-part outcome-statement shape and the importance × satisfaction prioritization.
- Ulwick, A. W., & Bettencourt, L. A. (2008, Spring). "Giving Customers a Fair Hearing." *MIT Sloan Management Review*. Practitioner-oriented article on the outcome-survey mechanics and common pitfalls.
- `context/frameworks/competitive-analysis.md` — consumer of the JTBD lens (one of three lenses, alongside Porter and Wardley).
- `context/frameworks/opportunity-solution-tree.md` — consumer of the job framing for Opportunity sourcing; jobs are the natural language of OST Opportunities.
- `context/frameworks/interview-snapshot.md` — the per-interview extraction template; the Christensen lens shapes which sentences become `Job` objects.
