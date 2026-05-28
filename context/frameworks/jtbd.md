# Jobs to Be Done

> Two distinct canonical formulations of the same insight — customers do not buy products; they hire products to make progress on a job. Clayton Christensen's "jobs hired to do" framing (*Competing Against Luck*, 2016; HBR, Sept 2016) supplies the struggle-moment lens for early discovery. Tony Ulwick's outcome-driven innovation (*What Customers Want*, 2005) supplies the four-part outcome-statement shape for late-stage prioritization. The two are complementary, not competing — this kit uses both, in different phases. Consumers are `/internal-jtbd-interview` (planned — P7.9, enterprise) and `/jtbd-analogues` (planned — P7.12, greenfield).

## The Christensen formulation — "jobs hired to do"

Clayton Christensen's framing: customers "hire" products to make progress on a job they are trying to do in their lives. The job is the customer's progress, not the product's feature.

The canonical illustration is the milkshake example: a fast-food chain wanted to grow milkshake sales; demographic segmentation suggested obvious moves. Investigation showed half of milkshakes were sold to commuters in the morning who "hired" the shake to make the drive less boring and keep them full until lunch. Competitors for the morning hire were not other milkshakes — they were bananas, bagels, and boredom. The afternoon hire (parents buying a treat for kids) had different competitors and different success criteria.

The lens directs attention to **struggle moments** in the customer's day — the points where the customer is trying to make progress and is hindered. Demographic segmentation describes who the customer is; the job describes what the customer is trying to do. The two often cross-cut: the same person hires different products for different jobs across the day.

## The Ulwick formulation — outcome statements

Tony Ulwick's "Outcome-Driven Innovation" (*What Customers Want*, 2005) decomposes a job into **measurable desired outcomes**. Outcome statements have a canonical **four-part shape**:

> *Direction of improvement* + *Performance metric* + *Object of control* + *Context*

Worked example: "**Minimize** the **time it takes** to **find a missing document** when **preparing for a client meeting**." The four parts:

- **Direction:** *Minimize* (or *Maximize* / *Reduce* / *Increase* / *Stabilize*).
- **Performance metric:** *the time it takes* (or *the likelihood of* / *the number of* / *the cost of*).
- **Object of control:** *to find a missing document* — the specific thing the customer is acting on.
- **Context:** *when preparing for a client meeting* — the moment of use.

Statements in this shape are **testable**: Ulwick surveys customers on two dimensions per outcome — **importance** ("how much does this matter to you?") and **current satisfaction** ("how well is it currently served?"). Plotting outcomes on a two-axis grid surfaces the **high-importance / low-satisfaction quadrant** — the underserved outcomes where new product investment pays back. Outcomes in other quadrants either don't matter, are already well-served, or are over-served (where competitors invest disproportionately for diminishing return).

## When to use which

The two formulations are not competing; they sit at different stages of the workflow.

- **Christensen for early-stage discovery.** *What job is the customer trying to do? Who are the unobvious competitors?* The framing is qualitative, struggle-moment-driven, and best used when the team does not yet know what to build. Used in interviews and snapshot extraction (see `context/frameworks/interview-snapshot.md`).
- **Ulwick for late-stage prioritization.** *Among the named outcomes for this job, which are most underserved relative to their importance?* The framing is quantitative, survey-driven, and best used when the team has a job statement and needs to choose which outcome to chase. Used downstream of the OST when the chosen Opportunity has many candidate Solutions.

Christensen surfaces the job; Ulwick decomposes the job into outcomes the team can rank.

## Common failure modes

- **Confusing a job with a feature.** "They want a faster checkout" is a feature request; the job is "complete the purchase quickly enough to finish before my kid wakes up." Features describe the product; jobs describe the customer's progress.
- **Confusing a job with a persona.** Personas are about who the customer is (demographics, role, segment); jobs are about what the customer is trying to do. The same person hires different products for different jobs across the day.
- **The "everyone's job" trap.** Job statements so abstract they describe every human — "the customer wants to feel productive," "the customer wants peace of mind." If the job describes everyone, it discriminates nothing.
- **The "solution-as-job" trap** — defining the job as "use our product" rather than the underlying progress the customer seeks. This is the single most common JTBD mis-application: the company restates its own product as a job, then mistakes feature usage for progress.

## How the kit uses this framework

- **`/internal-jtbd-interview`** (planned — ROADMAP P7.9, enterprise mode only) — interview prep and analysis for the captive user base; uses both formulations (Christensen for the interview; Ulwick for the post-interview prioritization).
- **`/jtbd-analogues`** (planned — ROADMAP P7.12, greenfield mode only) — surfaces jobs being hired-for in adjacent markets; uses primarily the Christensen formulation.
- **`context/frameworks/competitive-analysis.md`** uses JTBD as one of three lenses (with Porter's five forces and Wardley's evolution axis).
- **`context/frameworks/opportunity-solution-tree.md`** — Opportunities in an OST are often expressed as jobs or job-fragments; the Christensen formulation is the natural language.
- **`mode-guard` hook** (F2.4, shipped) — enforces mode-gated access to the JTBD commands.

## References

- Christensen, C. M. (2016). *Competing Against Luck: The Story of Innovation and Customer Choice*. HarperBusiness. The canonical source for the "jobs hired to do" framing and the milkshake example.
- Christensen, C. M., et al. (2016, September). "Know Your Customers' Jobs to Be Done." *Harvard Business Review*. The HBR article version of the same framework.
- Ulwick, A. W. (2005). *What Customers Want: Using Outcome-Driven Innovation to Create Breakthrough Products and Services*. McGraw-Hill. The canonical source for the four-part outcome-statement shape and the importance × satisfaction prioritization.
- `context/frameworks/competitive-analysis.md` — consumer of the JTBD lens.
- `context/frameworks/opportunity-solution-tree.md` — consumer of the job framing for Opportunity sourcing.
