# Product research → development → strategy: a practitioner's map

There's no single canonical playbook, but the field has converged on a fairly stable stack. The trick is knowing which layer you're operating at, because the frameworks are not interchangeable — they answer different questions.

## The four layers

| Layer | Question it answers | Canonical references |
|---|---|---|
| **Strategy** | Where are we playing, and why will we win? | Rumelt's *Good Strategy/Bad Strategy* (diagnose → guiding policy → coherent actions); Perri's strategy stack (vision → strategic intent → product initiatives → options); Wardley Mapping for situational awareness |
| **Discovery (problem-finding)** | What problem is worth solving, for whom? | Torres's Continuous Discovery + Opportunity Solution Tree; Christensen/Ulwick Jobs-to-be-Done; IDEO/Stanford Design Thinking |
| **Validation (problem→solution)** | Will the thing we have in mind actually work? | Ries's Lean Startup (build–measure–learn); David Bland's *Testing Business Ideas* (assumption mapping + experiment selection); design sprints |
| **Delivery** | How do we build and ship it well? | Cagan's *Inspired*/*Empowered* (product trio, outcomes over output, dual-track discovery+delivery) |

Most teams fail not because they pick the "wrong" framework but because they're operating at the wrong layer. Lean Startup applied without a strategy gives you a portfolio of validated-but-unrelated bets. Strategy without discovery gives you a beautifully argued plan to build the wrong thing.

## How the layers compose

Read top-down and bottom-up:

- **Top-down**: Rumelt forces you to name the *one* central challenge, not the eight things you wish were different. Perri's stack then cascades that diagnosis into product-level problems with measurable outcomes. OKRs are the cadence layer underneath.
- **Bottom-up**: Torres's Opportunity Solution Tree is the bridge — it ties weekly customer interviews to a desired business outcome, surfaces an opportunity space, and tests solutions against it. Cagan's discovery practices (15 experiments/week is the high-water mark, not the median) sit underneath that as daily craft.

JTBD, Design Thinking, and Lean Startup are best understood as **different lenses on the discovery/validation seam**, not competitors:

- **JTBD** is sharpest when you need a *market-side definition of the problem* that doesn't drift with personas or solutions ("when X happens, I want to Y, so I can Z"). Strong for choosing where to play.
- **Design Thinking** is sharpest in the *empathy + ideation* phase when the problem space is fuzzy and you need divergent options before convergent choice.
- **Lean Startup** is sharpest *after* you have a hypothesis and a candidate solution — it's a validation discipline, not a discovery one.

A common synthesis: JTBD to frame the market, Design Thinking to explore the solution space, Lean Startup / Testing Business Ideas to validate, Cagan-style continuous discovery to keep it all running weekly.

## Greenfield vs enterprise — where prior-art research fits

Researching prior art online — scanning how the industry has solved adjacent problems — is essentially a **strategy-layer move dressed as a discovery-layer one**. In greenfield, you have no internal data and no installed base, so the cheapest situational awareness comes from analogical reasoning across the wider industry. That's why it works there.

In enterprise / brownfield it's the wrong tool because:

- The constraints are not "what's possible" but "what's compatible" — installed systems, contracts, regulatory posture, internal political topology.
- The customer is partly captive, so revealed-preference data already exists internally and beats analogical reasoning from external products.
- Differentiation rarely comes from architectural novelty; it comes from integration depth and switching costs.

For enterprise, **swap prior-art research for two different inputs**:

1. **Wardley Map of the current value chain** — what's evolved to commodity, what's still custom, where the inertia is. This tells you where to invest vs where to consume.
2. **Internal JTBD interviews with the existing user base** — what jobs are currently being hired-for that your product underserves. This is the brownfield equivalent of greenfield's "scan the market."

Same impulse — *understand the landscape before committing* — but the landscape is internal-and-political rather than external-and-technical.

## A weekly operating cadence that holds it together

End-to-end operating model:

- **Quarterly**: Rumelt-style strategy refresh. One-page diagnosis, guiding policy, three to five coherent actions. Refuse fluff. If you can't name *the* central challenge in one sentence, you don't have a strategy yet.
- **Monthly**: Update the Opportunity Solution Tree. Outcome at the root tied to strategic intent, opportunities below, solutions and assumption tests at the leaves.
- **Weekly**: Three customer touches (Torres's minimum-viable rhythm), one experiment shipped, one assumption falsified. Cross-functional trio (PM + design + eng) reviews the tree.
- **Per-feature**: Run discovery and delivery as parallel tracks (Cagan dual-track). Discovery output is a *validated opportunity with a tested solution sketch*, not a spec. Spec follows once the riskiest assumption is dead.

## What to actually read (in order)

If you only read four, in this order:

1. **Rumelt — *Good Strategy/Bad Strategy*** — fixes the most common error: confusing goals for strategy.
2. **Perri — *Escaping the Build Trap*** — wires Rumelt into a product org's operating model.
3. **Torres — *Continuous Discovery Habits*** — the weekly discipline that makes the strategy real.
4. **Cagan — *Inspired*** (then *Empowered*) — the team-shape and culture that supports it.

Add Wardley's online book (*Wardley Maps*, free) when you want situational awareness for an enterprise landscape, and Bland & Osterwalder's *Testing Business Ideas* as the practical assumption-testing reference.

## Sources

- [Opportunity Solution Trees — Product Talk](https://www.producttalk.org/opportunity-solution-trees/)
- [Opportunity Solution Tree definition — Product Talk glossary](https://www.producttalk.org/glossary-discovery-opportunity-solution-tree/)
- [Empowered Product Teams — SVPG (Marty Cagan)](https://www.svpg.com/empowered-product-teams/)
- [Discovery vs Delivery — SVPG](https://www.svpg.com/discovery-delivery/)
- [The Product Operating Model — SVPG](https://www.svpg.com/the-product-operating-model-an-introduction/)
- [Rumelt's Good Strategy Bad Strategy + Wardley Mapping](https://learnwardleymapping.com/2022/03/27/rumelts-good-strategy-bad-strategy-and-wardley-mapping/)
- [Introduction to Wardley Maps](https://aktiasolutions.com/introduction-to-wardley-maps/)
- [Summary — Escaping the Build Trap (Melissa Perri)](https://t-ziegelbecker.medium.com/a-summary-of-escaping-the-build-trap-by-melissa-perri-d247f943a7b3)
- [Product Strategy vs North Star Framework — Paweł Huryn](https://huryn.medium.com/product-strategy-vs-north-star-framework-adaa06397371)
- [JTBD — Strategyn (Tony Ulwick)](https://strategyn.com/jobs-to-be-done/)
- [Zig Then Zag: Design Thinking vs Lean Startup — IDEO](https://www.ideo.com/journal/zig-then-zag-when-to-use-design-thinking-vs-the-lean-startup-approach)
- [Agile / Design Sprints / Lean Startup / Design Thinking comparison — Appcues](https://www.appcues.com/blog/product-development-innovation-methodology)
- [Greenfield Product Management: Fantasy vs Reality — Stryber](https://medium.com/stryber-strategic-venture-builder/greenfield-product-management-fantasy-vs-reality-9499a9ab2fe)
- [Greenfield vs Brownfield IT Projects — Naturaily](https://naturaily.com/blog/greenfield-vs-brownfield-projects-in-it-differences-pros-cons-and-how-to-lead)
