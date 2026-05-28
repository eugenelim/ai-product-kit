# Strategic Coherence

> Kit synthesis grounded in Richard Rumelt's coherent-actions kernel-leg (*Good Strategy, Bad Strategy*, Crown Business, 2011, ch. 5), operationalized as a three-axis audit lens for pairs of strategic bets. The three axes — resources, capabilities, market posture — are kit-original decompositions of Rumelt's "coordinated, mutually reinforcing, resource-feasible" criteria; they are not attributed to Rumelt as an axis framework. The kit's `/audit-portfolio-coherence` command (F1.6, shipped) walks pairs of Strategic Intents and Initiatives flagging axis violations; the runnable script is `scripts/audit-portfolio-coherence.py` (confirmed to exist at spec-time, 2026-05-28); the consuming skill is `.claude/skills/strategy-coherence/SKILL.md` (shipped).

## The three axes

Coherence is checked along three axes. A pair of bets is **incoherent** if it conflicts on at least one axis.

- **Resource coherence.** Do the actions share a budget (people, time, capital) that won't starve any one of them? Two big bets fighting for the same engineering team this quarter is a resource conflict — even if each bet is individually sound. The audit asks: if both bets are funded, can the team execute both within the declared resource envelope?
- **Capability coherence.** Do the actions need the same capabilities the team has, or do they require contradictory capabilities? "Move fast" and "be precise" both promoted to primary capability is a capability conflict unless one is named as dominant. The audit asks: do the bets require the team to be simultaneously good at things that are usually traded-off against each other?
- **Market posture coherence.** Do the actions present a consistent posture to the market — premium vs price-leader, depth vs breadth, enterprise vs consumer, premium vs freemium? Saying enterprise to one customer and self-serve-consumer to another in the same quarter is a posture conflict. The market will read the posture as one thing; whichever one is correct, the other will fail.

A fourth implicit axis surfaces in practice: **shared-audience coherence**. Bets that look independent but consume the same scarce attention surface (a single customer can only adopt so many things in a quarter) are coherent on resources and capabilities but incoherent on audience capacity. The audit treats this as a sub-case of market posture.

## The audit lens — Rumelt's coherent-actions leg, operationalized

Rumelt's third kernel-leg (see `context/frameworks/rumelt.md`) says coherent actions are coordinated, mutually reinforcing, and resource-feasible. The kit's audit decomposes those three criteria into the three axes above:

- **Resource coherence** operationalizes Rumelt's *resource-feasible* criterion — the bets must fit inside the team's actual resource envelope, not the wishful one.
- **Capability coherence** operationalizes the *mutually reinforcing* criterion — two bets that demand contradictory capabilities cannot strengthen each other.
- **Market posture coherence** operationalizes the *coordinated* criterion — actions that read as contradictory postures to the market are not externally coordinated even when internally aligned.

The audit runs pairwise checks across the active portfolio:

- The shipped command is `/audit-portfolio-coherence` (F1.6).
- The script is `scripts/audit-portfolio-coherence.py` (confirmed to exist at spec-time).
- The skill is `.claude/skills/strategy-coherence/SKILL.md` (shipped).

Pairwise is load-bearing: the audit does not check whether each bet is *individually* sound (that is the Strategic Intent template's job); it checks whether *every pair* of active bets is coherent on all three axes. The output is a list of pairs with the axis on which they conflict.

## Incoherence patterns

The audit emits findings in named pattern shapes. Each pattern has a definition (what the conflict *is*) and a worked example (so a consumer can recognize the shape in their own portfolio):

- **Resource conflict.**
  - *Definition:* two bets compete for the same finite pool of people, time, or capital within the same window, such that funding both implies starving one. The audit flags the pair and names the contested resource (team, budget line, or calendar slot).
  - *Worked example:* Bet A — re-platform onto Postgres in Q3 — and Bet B — ship the new billing engine in Q3 — both require the four senior platform engineers; one must yield or the quarter slips on both.

- **Capability conflict.**
  - *Definition:* two bets each claim a different primary differentiating capability, without naming which dominates, so the organization cannot concentrate the focus and tradeoffs needed to make either one excellent.
  - *Worked example:* Bet A claims "fastest time-to-market in the segment" as the differentiator; Bet B claims "regulatory-grade audit completeness" as the differentiator. Without naming which capability is dominant, neither bet gets the org's focus and both ship mediocre on their respective claims.

- **Market-posture conflict.**
  - *Definition:* two bets present contradictory postures to the market — pricing surface, sales motion, brand voice, or target segment — such that the external read of the company drifts incoherent regardless of internal alignment.
  - *Worked example:* Bet A: high-touch enterprise sales with $50k+ ACV pricing; Bet B: self-serve freemium with viral growth via product-led signups. The sales motion, pricing surface, and brand voice will drift incoherent within two quarters.

- **Implicit-shared-audience conflict.**
  - *Definition:* two bets look independent on the org chart but share the same scarce attention surface — the same customer segment, the same product area, or the same learning-and-adoption bandwidth — within the same window.
  - *Worked example:* Bet A: launch a power-user feature for senior analysts in Q4; Bet B: launch a new onboarding for junior analysts in Q4. The bets look independent but compete for engineering attention on the same product surface and for the same customers' learning bandwidth.

## Common failure modes

Each failure mode has a definition (what the team did wrong) and a worked example or signal (how it shows up in practice):

- **Single-axis review.**
  - *Definition:* the audit only checks the most visible axis — usually resources, because resources are line items in the budget — and treats the other two as out of scope.
  - *Signal:* the audit only checks resources because resources are visible in the budget — capability and posture conflicts surface only when the team starts shipping, by which point the conflict has compounded into delivery friction or sales-motion drift.

- **"They're independent" rationalization.**
  - *Definition:* two bets are declared parallel because they live in different teams' roadmaps with different OKRs, and the org-chart separation is mistaken for a real absence of contention.
  - *Signal:* two bets are framed as parallel because they sit in different teams' roadmaps with different OKRs — but they share the same scarce platform capacity, or the same customer's attention, or the same go-to-market motion.

- **Shared-outcome trap.**
  - *Definition:* the team concludes that two bets must be coherent because both serve the same outcome metric — but a shared destination says nothing about whether the paths conflict on resources, capabilities, or posture.
  - *Signal:* both bets aim at the same outcome metric (e.g., ARR growth), so the team concludes the actions must be coherent. They might be — but a shared destination does not imply non-conflicting paths.

## How the kit uses this framework

- **`/audit-portfolio-coherence`** (F1.6, shipped) — consumes this framework as its rule library; emits per-pair findings labeled by axis.
- **`scripts/audit-portfolio-coherence.py`** (shipped) — the runnable script.
- **`.claude/skills/strategy-coherence/SKILL.md`** (shipped) — the skill the command dispatches; bundles the coherence-audit rule library.
- **Strategic Intent template** (F3.1, shipped at `templates/strategic-intent.md`) — the artifact whose pairs the audit walks.
- **`strategy-skeptic` agent** (planned — ROADMAP P7.3) — uses this framework alongside `context/frameworks/rumelt.md` when challenging drafts.

Frame: this framework is the companion to `context/frameworks/rumelt.md`. Rumelt names the third kernel-leg (coherent actions); this doc operationalizes it as an audit lens the kit can run automatically.

## References

- Rumelt, R. P. (2011). *Good Strategy, Bad Strategy: The Difference and Why It Matters*. Crown Business. Chapter 5, "The Kernel of Good Strategy" — the canonical source for the coherent-actions kernel-leg.

Note: **the three-axis decomposition is kit synthesis grounded in Rumelt** — Rumelt names the criteria (coordinated, mutually reinforcing, resource-feasible); the kit's resource / capability / market-posture axes are a derived decomposition, not a Rumelt-published framework.

- `context/frameworks/rumelt.md` — the companion framework covering the full kernel (diagnosis / guiding policy / coherent action).
- `.claude/commands/audit-portfolio-coherence.md` — the audit command's contract.
- `.claude/skills/strategy-coherence/SKILL.md` — the consuming skill.
- `templates/strategic-intent.md` — the artifact the audit walks.
