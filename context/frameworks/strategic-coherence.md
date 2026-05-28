# Strategic Coherence

> Kit synthesis grounded in Richard Rumelt's coherent-actions kernel-leg (*Good Strategy, Bad Strategy*, Crown Business, 2011, ch. 5), operationalized as a three-axis audit lens for pairs of strategic bets. The three axes — resources, capabilities, market posture — are kit-original decompositions of Rumelt's "coordinated, mutually reinforcing, resource-feasible" criteria; they are not attributed to Rumelt as an axis framework. The kit's `/audit-portfolio-coherence` command (F1.6, shipped) walks pairs of Strategic Intents and Initiatives flagging axis violations; the runnable script is `scripts/audit-portfolio-coherence.py` (confirmed to exist at spec-time, 2026-05-28); the consuming skill is `.claude/skills/strategy-coherence/SKILL.md` (shipped).

## The three axes

Coherence is checked along three axes. A pair of bets is **incoherent** if it conflicts on at least one axis.

- **Resource coherence.** Do the actions share a budget (people, time, capital) that won't starve any one of them? Two big bets fighting for the same engineering team this quarter is a resource conflict — even if each bet is individually sound. The audit asks: if both bets are funded, can the team execute both within the declared resource envelope?
- **Capability coherence.** Do the actions need the same capabilities the team has, or do they require contradictory capabilities? "Move fast" and "be precise" both promoted to primary capability is a capability conflict unless one is named as dominant. The audit asks: do the bets require the team to be simultaneously good at things that are usually traded-off against each other?
- **Market posture coherence.** Do the actions present a consistent posture to the market — premium vs price-leader, depth vs breadth, enterprise vs consumer, premium vs freemium? Saying enterprise to one customer and self-serve-consumer to another in the same quarter is a posture conflict. The market will read the posture as one thing; whichever one is correct, the other will fail.

A fourth implicit axis surfaces in practice: **shared-audience coherence**. Bets that look independent but consume the same scarce attention surface (a single customer can only adopt so many things in a quarter) are coherent on resources and capabilities but incoherent on audience capacity. The audit treats this as a sub-case of market posture.

## The audit lens — Rumelt's coherent-actions leg, operationalized

Rumelt's third kernel-leg (see `context/frameworks/rumelt.md`) says coherent actions are coordinated, mutually reinforcing, and resource-feasible. The kit's audit decomposes those three criteria into the three axes above and runs pairwise checks across the active portfolio:

- The shipped command is `/audit-portfolio-coherence` (F1.6).
- The script is `scripts/audit-portfolio-coherence.py` (confirmed to exist at spec-time).
- The skill is `.claude/skills/strategy-coherence/SKILL.md` (shipped).

Pairwise is load-bearing: the audit does not check whether each bet is *individually* sound (that is the Strategic Intent template's job); it checks whether *every pair* of active bets is coherent on all three axes. The output is a list of pairs with the axis on which they conflict.

## Incoherence patterns

The audit emits findings in named pattern shapes:

- **Resource conflict.** Two strategic bets both require the senior platform team this quarter; one must yield. The audit flags the pair and the resource (the named team or budget).
- **Capability conflict.** The bet on "speed-to-market" and the bet on "regulatory-grade accuracy" both claim primary capability priority; neither will get it. The audit asks the team to name which dominates.
- **Market-posture conflict.** Bet A says we're a high-touch enterprise product; Bet B says we're self-serve and freemium; sales motion drift is inevitable. The audit asks the team to resolve the posture conflict before either bet ships customer-facing surface.
- **Implicit-shared-audience conflict.** Bets that look independent but consume the same scarce attention surface. The audit surfaces this when two bets target the same persona segment with launch windows in the same quarter.

## Common failure modes

- **Single-axis review.** The team checks resources (the most visible axis) and stops there. Capability and posture conflicts go un-flagged until they manifest in delivery friction or sales-motion drift.
- **"They're independent" rationalization.** Two bets are framed as parallel because that's organizationally convenient — different teams, different roadmaps, different OKRs. The shared scarce capability or audience is invisible to the framing but real to the constraint.
- **"All our bets are coherent because they share an outcome."** Sharing an outcome metric (e.g., ARR growth) doesn't mean the actions don't conflict on resources, capabilities, or posture. The shared outcome is a destination; coherence is about the paths.

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
