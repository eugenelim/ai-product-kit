# Product operating model

How product work flows from strategy through delivery, in one file. Personal
point of view, not a corporate methodology. Opinionated. If you disagree with
a specific call, change it locally and move on.

The model has four phases. Each phase has an **entry condition** you must
meet before starting it and an **exit condition** that triggers the handover
to the next phase. The most common failure in product orgs isn't picking the
wrong framework inside a phase — it's operating at the wrong phase entirely.
Strategy without discovery picks the wrong problem; discovery without strategy
surfaces dozens of unrelated opportunities; validation without an opportunity
is theatre; delivery without validation builds confidently in the wrong
direction.

## The four phases

| Phase | Entry condition | Exit condition (handover) | Canonical references |
|---|---|---|---|
| **Strategy** | The org has a decision to make about where to invest | A named central challenge + guiding policy + 3–5 coherent actions | Rumelt, *Good Strategy / Bad Strategy*; Perri, *Escaping the Build Trap*; Wardley, *Wardley Maps* (free online) |
| **Discovery** | A strategic intent exists, in one sentence | A chosen opportunity, tied to a measurable outcome | Torres, *Continuous Discovery Habits* (Opportunity Solution Tree); Christensen / Ulwick, Jobs-to-be-Done |
| **Validation** | An opportunity is chosen and its riskiest assumption is named | The riskiest assumption has survived a falsification test, or been killed and the opportunity dropped | Ries, *Lean Startup*; Bland & Osterwalder, *Testing Business Ideas* |
| **Delivery** | A validated solution sketch exists and the team has enough confidence to invest | Code in production; success and falsification metrics tracked | [`initiative-kit/`](./initiative-kit/) (Cagan, *Inspired* / *Empowered* for the team shape) |

Each phase points at canonical references for working *inside* it. This
document does not re-explain them. Read the books; this doc is the wiring
diagram.

## Cadence

The phases don't sit in a waterfall. They run on different rhythms
simultaneously.

- **Quarterly** — strategy refresh. Rumelt-style diagnosis. One page. If
  you can't name *the* central challenge in one sentence, you don't have a
  strategy yet.
- **Monthly** — update the Opportunity Solution Tree. Outcome at the root
  tied to the strategic intent, opportunities below, solutions and
  assumption tests at the leaves.
- **Weekly** — three customer touches (Torres's minimum-viable rhythm),
  one experiment shipped, one assumption falsified. Cross-functional trio
  (PM + design + eng) reviews the tree.
- **Per-feature** — discovery and delivery run as parallel tracks (Cagan's
  dual-track). Discovery's output is a validated opportunity with a tested
  solution sketch, not a spec. The spec follows once the riskiest assumption
  is dead.

The discipline is keeping all four rhythms alive at once. Most orgs run the
per-feature rhythm and drop the others; that's how strategy decays from
"where we play" into "what we built last sprint."

## Handovers — what crosses each boundary

```
Strategy
   ↓  strategic intent (one sentence, from the strategy doc)
Discovery
   ↓  chosen opportunity, tied to a measurable outcome
Validation
   ↓  validated solution sketch (riskiest assumption survived a test)
Delivery — Vision
   ↓  customer-shaped pitch + assumption tests still owed
Delivery — Initiative
   ↓  context map + end-to-end flow + child-spec pointers
Delivery — Per-context Spec
   ↓  plan
Code
```

The load-bearing fact: **each handover must travel as an artifact, not as a
conversation**. If the strategic intent is "what we discussed at the offsite,"
every downstream phase drifts. If the validated solution sketch is "what the
PM has in their head," the vision starts re-litigating discovery decisions.

For each handover, the missing-handover pattern to watch for:

**Strategy → Discovery.** *Missing*: discovery interviews running against no
strategic frame. *Symptom*: dozens of opportunities surface, none converge on
a meaningful bet.

**Discovery → Validation.** *Missing*: jumping from "we interviewed users"
straight to "let's build it." *Symptom*: the riskiest assumption is never
isolated, the team spends six weeks building before learning anything could
be wrong.

**Validation → Vision.** *Missing*: a vision that reads confident but rests
on unfalsified hopes ("customers will love this"). *Symptom*: a year later,
the feature shipped but adoption is below threshold and nobody can say
*which* assumption was wrong.

**Vision → Initiative.** *Missing*: a vision filed with no
`strategic_intent:` reference. *Symptom*: three concurrent initiatives that
each look reasonable in isolation but contradict each other in aggregate —
Rumelt's "list of wishes" failure at the portfolio level.

**Initiative → Spec.** *Missing*: a spec filed with no context-map row or
`parent_initiative:` link. *Symptom*: cross-team handoffs get re-litigated
inside individual specs, each team assuming a different shape for the
shared contract.

## Phase guide — where am I, what's next?

When something feels stuck, the answer is almost always *go back one phase*.
Use this table to find where you are.

| You currently have | You're at | Your next artifact | Where it lives |
|---|---|---|---|
| A vague sense the org "should do something about X" | Pre-strategy | A Rumelt diagnosis: name the central challenge in one sentence | Strategy doc (separate from the kit) |
| A diagnosed challenge and a guiding policy | Strategy → Discovery handover | An Opportunity Solution Tree rooted in a measurable outcome | Discovery space (separate from the kit) |
| An OST with several opportunities | Discovery → Validation handover | Assumption map on the top two or three; pick one to test first | Discovery space (separate from the kit) |
| A tested opportunity that survived its riskiest assumption | Validation → Delivery handover | The vision document | [`initiative-kit/vision-TEMPLATE.md`](./initiative-kit/vision-TEMPLATE.md) |
| A vision but unsure if the work crosses teams | Vision shape check | Either expand into an initiative or fold the vision onto the lead spec | The kit, or skip if it's truly single-repo |
| A vision and at least two affected services / repos | Initiative | Initiative folder with context map, end-to-end flow, child-spec manifest | [`initiative-kit/initiative-TEMPLATE.md`](./initiative-kit/initiative-TEMPLATE.md) |
| An initiative with child-spec pointers | Per-context spec drafting | Spec + plan in each affected repo | Each repo's `docs/specs/` |

If a phase keeps re-deriving the prior phase's output, the prior phase didn't
finish. If the spec keeps re-litigating bounded-context ownership, the
context map isn't done. If the vision keeps changing scope, discovery didn't
surface a validated opportunity.

## Greenfield vs enterprise

Prior-art research — scanning how the industry has solved adjacent problems —
is a strategy-phase move that works well in greenfield and badly in
enterprise. In greenfield, you have no internal data and no installed base,
so the cheapest situational awareness comes from analogical reasoning across
the wider industry. In enterprise / brownfield, the constraints aren't
"what's possible" but "what's compatible"; differentiation comes from
integration depth and switching costs; and the customer is partly captive, so
revealed-preference data already exists internally and beats analogical
reasoning from external products.

For enterprise, swap external prior-art research for two different inputs in
the strategy phase:

1. **Wardley Map of the current value chain.** What's evolved to commodity,
   what's still custom, where the inertia lives. This tells you where to
   invest versus where to consume.
2. **Internal JTBD interviews with the existing user base.** What jobs are
   currently being hired-for that your product underserves. The brownfield
   equivalent of greenfield's "scan the market."

The kit's `initiative-TEMPLATE.md` carries a Wardley-lite *Evolution check*
in the context map for the same reason, one phase down: in enterprise,
naming what's commodity vs. custom in the architecture map is load-bearing
for build-vs-buy decisions.

## Failure modes

The seven most common ways product work goes sideways, each pinned to its
phase:

1. **Operating at the wrong phase** (universal). Lean Startup applied without
   strategy → a portfolio of validated-but-unrelated bets. Strategy without
   discovery → a beautifully argued plan to build the wrong thing.
2. **Strategy that's just a list of goals** (Rumelt's primary failure mode).
   "Grow revenue, improve retention, expand into Europe, and become
   customer-obsessed" is not a strategy. A strategy names *the central
   challenge* and *the guiding policy that responds to it*.
3. **Discovery without a strategic frame.** Surfaces opportunities unrelated
   to where the org is investing. The OST root must trace to a strategic
   intent.
4. **Validation theatre.** Running experiments after the build decision has
   been made. Validation only counts if the team will *pull the work* when
   the assumption fails.
5. **Vision before validation.** Writing the customer-shaped pitch as if you
   already knew it would resonate. The vision should carry open assumption
   tests forward, not assert confidence.
6. **Specs without initiatives.** Per-service spec authors deriving
   cross-team contracts in prose, each making different assumptions about
   the shared shape. The context map lives at the initiative level for a
   reason.
7. **Cadence collapse.** Running the per-feature rhythm and dropping the
   quarterly / monthly / weekly. Strategy decays, the OST goes stale, the
   weekly customer touches stop happening, and within two quarters the org
   is shipping features against a strategy it can no longer recite.

## Read order — the four books

If you only read four, in this order:

1. **Rumelt, *Good Strategy / Bad Strategy*** — fixes the most common error:
   confusing goals for strategy.
2. **Perri, *Escaping the Build Trap*** — wires Rumelt into a product org's
   operating model.
3. **Torres, *Continuous Discovery Habits*** — the weekly discipline that
   makes the strategy real.
4. **Cagan, *Inspired*** (then *Empowered*) — the team shape and culture
   that supports it.

Add **Wardley's *Wardley Maps*** (free online) when you want situational
awareness for an enterprise landscape. Add **Bland & Osterwalder's *Testing
Business Ideas*** as the practical assumption-testing reference.

## The kit

For the delivery phase, this points at [`initiative-kit/`](./initiative-kit/).
The kit assumes the validation handover has been met: a tested solution
sketch exists, the riskiest assumption has survived (or been killed), and the
team has enough confidence to invest delivery time.

**Don't reach for the kit before the validation handover.** If you do, the
kit will let you — the vision template has slots that don't enforce the
prior phases — but you'll have built scaffolding around an unvalidated bet,
which is the most expensive way to learn the bet was wrong.

Inside the kit:

- [`vision-TEMPLATE.md`](./initiative-kit/vision-TEMPLATE.md) — customer-shaped pitch + assumption tests still owed
- [`initiative-TEMPLATE.md`](./initiative-kit/initiative-TEMPLATE.md) — context map, end-to-end flow, child specs, sequencing
- [`sample-vision-…`](./initiative-kit/sample-vision-subscription-pause.md) and [`sample-initiative-…`](./initiative-kit/sample-initiative-subscription-pause.md) — worked example
- [`pragmatic-core.md`](./initiative-kit/pragmatic-core.md) — the test that separates load-bearing artifacts from ceremony
- [`stack-map.md`](./initiative-kit/stack-map.md) — kit-local gaps (portfolio coherence, discovery evidence, cadence, continuous-discovery-on-delivery)

## What this isn't

- **Not a methodology rollout.** This is a personal POV on how the phases
  should sequence. Not corporate guidance, not something to mandate across
  a department.
- **Not a replacement for the books.** The wiring diagram doesn't substitute
  for the wires. Read Rumelt, Torres, Cagan, Bland.
- **Not enforced anywhere.** Rhythm comes from discipline, not tooling.
  This doc is a reminder, not a gate.
- **Not finished.** When a phase consistently fails in a way the doc
  doesn't predict, update the failure-modes section.
