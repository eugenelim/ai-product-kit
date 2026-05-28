# Rumelt's strategy kernel

> Strategy as a three-leg kernel — Diagnosis, Guiding Policy, Coherent Action — defined by Richard P. Rumelt in *Good Strategy, Bad Strategy: The Difference and Why It Matters* (Crown Business, 2011). All three legs are required for a strategy to exist; missing any one produces what Rumelt calls "bad strategy." This kit's Strategy phase is structured around the kernel: every Strategic Intent in `strategy/intents/<slug>.md` is a Rumelt kernel. The consumers are the Strategic Intent template (F3.1, shipped at `templates/strategic-intent.md`), `/strategy-refresh` (planned — ROADMAP P7.1), and the `strategy-skeptic` agent (planned — ROADMAP P7.3).

## The kernel — Diagnosis, Guiding Policy, Coherent Action

Rumelt's central insight (ch. 5): a strategy is not a goal, a vision, or a set of OKRs. It is the triad that connects a diagnosed challenge to coordinated action.

- **Diagnosis.** Identify the central challenge and what makes it hard. The diagnosis names the constraint, not just the symptom. "Revenue is flat" is a symptom; "the cost of customer acquisition now exceeds first-year revenue per customer because incumbent X bundled our differentiator into their free tier" is a diagnosis. A good diagnosis is testable, specific, and implies what kinds of action would and would not move the constraint.
- **Guiding Policy.** An overall approach to navigate the diagnosed challenge — a directional posture, not a target. "Become the lowest-cost option for the SMB segment by collapsing our distribution layer onto self-serve channels" is a guiding policy. It rules in some actions and rules out others; it does not name the specific moves.
- **Coherent Action.** A set of mutually reinforcing moves that the guiding policy authorizes. This is the leg most often skipped or hand-waved. Coherent actions are coordinated (they share a thread), mutually reinforcing (each makes the others stronger or cheaper), and resource-feasible (the team can actually execute them all).

Rumelt's canonical example is the IBM-PC strategy or the Wal-Mart small-town strategy: in each, the diagnosis names a specific constraint, the guiding policy provides a directional answer, and the coherent actions reinforce each other.

## What good strategy is not — the four hallmarks of bad strategy

From Rumelt (ch. 2), the four shapes of bad strategy.

- **Fluff.** Vague aspirational language disguising an empty kernel. "Synergy," "leverage our platform," "be the leader in our space." Fluff fails the test "what specifically would we do (or not do) differently after reading this?"
- **Failure to face the challenge.** No real diagnosis. The strategy doc names what we want without naming what's stopping us. A team that can articulate the goal but not the constraint hasn't done the diagnostic work.
- **Mistaking goals for strategy.** A goal is not a path to a goal. "Grow ARR 30% YoY" is a target, not a strategy. OKRs and ARR targets describe destinations; strategy describes how the destination becomes reachable given the constraint.
- **Bad strategic objectives.** Objectives that look like strategy because they use action language and carry target metrics, but they connect to no diagnosed constraint and reinforce no guiding policy. The single most common shape: a list of 12 priorities, none of which interlocks with the others, all of which compete for the same budget. Distinguishable from "failure to face the challenge" because the bad-objectives doc *does* name action items — they are just disconnected from any constraint the actions would resolve.

## The coherent-actions leg

The kernel's third leg is the one this kit operationalizes most heavily. Coherent actions are checked along three axes (the companion framework `context/frameworks/strategic-coherence.md` covers this in detail): **resource coherence** (do the actions share a budget that won't starve any one of them?), **capability coherence** (do the actions need the same capabilities the team has?), **market posture coherence** (do the actions present a consistent posture — premium vs price-leader, depth vs breadth, enterprise vs consumer?).

The kit's `/audit-portfolio-coherence` command (F1.6, shipped) walks pairs of Strategic Intents and Initiatives and flags axis violations. The script is `scripts/audit-portfolio-coherence.py`; the skill is `.claude/skills/strategy-coherence/SKILL.md`.

## Common failure modes

- **The strategy-as-vision-statement substitution** — "our vision is..." replaces the kernel. Vision statements describe a future state; they do not name the constraint or the path.
- **The strategy-as-OKRs substitution** — OKRs are targets, not strategy. A team that says "we have OKRs; we have a strategy" has confused destinations with paths.
- **The missing-diagnosis pattern** — the doc opens with the guiding policy ("we will become the platform of choice for...") without naming what made the challenge hard. The guiding policy without the diagnosis is just a slogan.
- **The "diagnosis-as-complaint" pattern** — the diagnosis describes the symptom without naming the constraint. "We're losing market share" is a complaint, not a diagnosis. "Our customer acquisition cost has exceeded first-year revenue because incumbent X bundled our differentiator into their free tier" is a diagnosis: it names what's changed, why, and what kinds of response would and would not work.

## How the kit uses this framework

- **Strategic Intent template** (F3.1, shipped at `templates/strategic-intent.md`) — its three required sections mirror the kernel (diagnosis / guiding policy / 3-5 coherent actions). The template is the single canonical artifact for the Strategy → Discovery handover.
- **`/strategy-refresh`** (planned — ROADMAP P7.1) — drafts a Rumelt-style diagnosis from current state.
- **`/strategic-intent`** (planned — ROADMAP P7.2) — synthesizes the one-pager.
- **`strategy-skeptic` agent** (planned — ROADMAP P7.3) — challenges drafts with Rumelt's four hallmarks of bad strategy.
- **`/audit-portfolio-coherence`** (F1.6, shipped) — audits the coherent-actions leg across the portfolio. See companion framework `context/frameworks/strategic-coherence.md`.
- **`/exec-strategy-narrative`** (planned — ROADMAP P7.4) — turns the intent into a 6-pager.

Frame: every Strategic Intent in the kit is a Rumelt kernel. The kit's Strategy phase is not a vision-and-OKRs phase; it is a diagnose-and-act phase.

## References

- Rumelt, R. P. (2011). *Good Strategy, Bad Strategy: The Difference and Why It Matters*. Crown Business. The canonical source. Chapter 2 ("Bad Strategy") for the four hallmarks; chapter 5 ("The Kernel of Good Strategy") for diagnosis / guiding policy / coherent action.
- `context/frameworks/strategic-coherence.md` — the companion framework operationalizing the coherent-actions leg as a three-axis audit.
- `templates/strategic-intent.md` — the kit's Strategic Intent template.
- `.claude/commands/audit-portfolio-coherence.md` — the audit command's contract.
