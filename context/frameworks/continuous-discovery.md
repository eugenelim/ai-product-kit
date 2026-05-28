# Continuous Discovery

> A weekly habit framework for product discovery, defined by Teresa Torres in *Continuous Discovery Habits* (2021). Continuous discovery means staying in regular, structured contact with customers — at a cadence the team sets — so that opportunities and assumptions surface continuously rather than as a quarterly research project. This kit's Discovery phase is structured around this habit; the consumers are the interview-and-OST commands (`/interview-snapshot`, `/extract-opportunities`, `/cluster-opportunities`, `/generate-ost`) and the `cadence-nudge` SessionStart hook that surfaces drift on the habit.

## The weekly habit

Torres names **weekly customer contact** as the discipline; the kit's practical target is **≥3 customer interviews + ≥1 assumption test + ≥1 falsified-or-survived assumption per week** (three interviews is not Torres's published number — it is the kit's practical minimum for trio coverage across PM, designer, and tech lead). Frame it as a discipline, not a quota: the point is sustained contact, not the specific numbers. A team that hits 2-2-2 on a regular cadence is in better shape than one that hits 3-1-1 once and then nothing for two months.

The kit operationalizes the cadence through `scripts/cadence-nudge.py` (F2.5, shipped) — a SessionStart hook that surfaces drift when a team has gone too long without an interview, an OST update, or a killed assumption. The hook is a nudge, not a gate; it reads the timestamps on the most recent artifacts in `discovery/`, `validation/learnings/`, and `discovery/trees/` and reports drift in the session's opening message.

Cadence is the carrier wave. The signal — what you learn — only accumulates if the carrier is continuous.

## The product trio

Discovery is done by a cross-functional **trio**: PM, designer, tech lead. They interview together, build OSTs together, decide together. The trio is not a relay (designer hands research to PM, PM hands strategy to tech lead); it is a single decision-making body.

Why a trio matters in practice: different roles surface different opportunities from the same conversation. The designer hears interaction friction; the tech lead hears feasibility constraints; the PM hears business viability. Discovery done by a single role is systematically blind to two of the three lenses — which then surface late in delivery as rework, post-launch friction, or feasibility surprises.

The kit's Engineering Handoff Packet (F3.9 template) is designed to reflect the trio's shared ownership — the `human_owned_decisions:` and `approvals_obtained:` fields can carry approvals from any of the three roles, not just the PM.

## Outcome vs output orientation

Continuous discovery works backwards from a **single outcome metric** rather than forwards from a feature list. The Outcome at the root of an OST (see `context/frameworks/opportunity-solution-tree.md`) is the metric; the Opportunities below it are paths to that metric; the Solutions are specific moves; the Assumption Tests are the falsification gates.

The same outcome-vs-output discipline shows up again at the post-ship boundary in `context/frameworks/landings-not-launches.md`. Discovery starts the work outcome-first; landings end the work outcome-first; output is the middle, not the goal.

## Common failure modes

- **Discovery theatre** — the team interviews regularly but the interviews don't change what gets built. The cadence is intact; the decision-utility is missing. This is the analogue of validation theatre in the Discovery phase.
- **Slack/Discord-only research substitute** — proxy research (community channels, support tickets, sales calls relayed second-hand) replaces direct customer contact. Proxy data is biased toward complainers and toward whoever the team already talks to; the missing voices stay missing.
- **The "I'll discover next quarter" trap** — treating discovery as project-bound rather than habit-bound. Discovery that goes dormant between quarters loses the relationship continuity that makes interviews productive in the first place. Customers who agree to a one-off interview are different (and less useful) than customers who agree to a recurring conversation.
- **Cadence-as-theatre** — treating the weekly cadence as the discovery work itself rather than a habit that produces data. The team hits 3-1-1 every week but the OST never changes and no opportunity is ever killed. The cadence is real; the discovery is fake.

## How the kit uses this framework

The kit's Discovery phase is structured around the habit Torres describes. Consumers:

- `/interview-snapshot` (planned — ROADMAP P2.1) — turns a raw transcript into a structured snapshot (see `context/frameworks/interview-snapshot.md`).
- `interview-snapshot` skill (planned — ROADMAP P2.2) and `interview-coder` agent (planned — ROADMAP P2.3) — the fan-out workers behind the command.
- `/extract-opportunities` (planned — ROADMAP P2.4) — snapshots → opportunity candidates feeding the OST.
- `/cluster-opportunities` (planned — ROADMAP P2.6) — themes raw opportunities into clusters.
- `/generate-ost` and `/update-ost` (planned — ROADMAP P2.7, P2.9) — produce and integrate the OST.
- `discovery-coach` agent (planned — ROADMAP P2.13) — auto-invoked when the team is stuck on an opportunity.
- `cadence-nudge` hook (F2.5, shipped) — the only currently-running discipline guard.
- `/discovery-update` (planned — ROADMAP P2.14) — weekly stakeholder digest.

The Discovery → Validation handover contract in `docs/HANDOVERS.md` (Handover 2) requires an OST with one Opportunity flagged `chosen: true`; the continuous habit is what makes that handover non-aspirational.

## References

- Torres, T. (2021). *Continuous Discovery Habits: Discover Products that Create Customer Value and Business Value*. Product Talk LLC. The canonical source — defines the weekly habit, the product trio, and the outcome-orientation that the kit's Discovery phase implements.
- `context/frameworks/opportunity-solution-tree.md` — the artifact the habit produces and continuously updates; companion framework.
- `context/frameworks/interview-snapshot.md` — the per-interview output that feeds the OST.
- `context/frameworks/landings-not-launches.md` — the same outcome-vs-output discipline, applied at the post-ship boundary.
- `docs/PHASE-GUIDE.md` §"Discovery" — the kit's phase-level handover contract.
