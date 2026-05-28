# Wardley mapping

> A strategic mapping technique that anchors a value chain on a named user need and positions each component along an evolution axis. Defined by Simon Wardley in his CC-BY-SA online book *Wardley Maps* (https://list.wardleymaps.com/, ongoing). A Wardley map is a *map* (not a diagram) because the spatial position of every component carries meaning: the y-axis is the value chain from user-facing to invisible-infrastructure; the x-axis is the evolution stage from Genesis to Commodity. This kit consumes Wardley in enterprise mode only — the `mode-guard` hook (F2.4, shipped) blocks `/wardley-map` outside enterprise mode. Downstream consumers are the `/wardley-map` command (planned — P7.7) and the `wardley-evolution` skill (planned — P7.8).

## The map — value chain anchored on user need

Every Wardley map starts with a named **user need**. The value chain hangs from that need: each component above another is something that the lower one supports. If you cannot name who the user is and what they need, you do not have a map — you have a diagram of components.

The anchor matters because strategic decisions are valid only relative to a user. A component that is critical for one user need may be irrelevant for another. The discipline of forcing the map to declare its anchor user is the single most useful rule Wardley imposes; teams that skip it end up with diagrams that suggest moves that don't actually serve any specific customer.

## The evolution axis — Genesis → Custom → Product (incl. rental) → Commodity (incl. utility)

Every component on a map sits at one of four evolution stages on the x-axis:

- **Genesis** — novel, unique, poorly understood. The component exists but its shape, value, and even necessity are unclear. R&D-ish.
- **Custom** — the component is built specifically each time it appears; no two implementations look the same. Bespoke; expensive; relies on specialists.
- **Product (including rental)** — the component is standardized and packaged. Available as a product or as a rental/SaaS offering. Multiple vendors; meaningful differentiation between them.
- **Commodity (including utility)** — well-understood, undifferentiated, often metered. Component X is functionally equivalent across vendors; price and reliability dominate. Utility-scale components (electricity, AWS S3) sit at the right end.

Components move rightward over time, dragged by competition. The strategic implication: where each component sits on the axis determines what you should *do* with it. Genesis components warrant exploration and patience; custom components warrant standardization investment; product components warrant differentiation or partnership; commodity components warrant outsourcing or utility consumption. Treating a commodity as a differentiator (building your own database when a managed one exists) is a category error the map exposes.

## Climatic patterns

Wardley names many climatic patterns; the kit references five canonical ones:

- **"Everything evolves"** — components shift rightward over time. Static maps decay; revisit on a cadence.
- **"No two things are the same"** — two superficially-identical components (two databases, two queues) can sit at different evolution stages depending on context. Place by characteristics, not by name.
- **"Inertia increases with scale"** — large established players resist the evolution of components they have invested in. The incumbent's reluctance to commoditize their differentiator is gameplay-relevant.
- **"Componentization enables higher-order systems"** — commoditization of layer N unlocks new genesis at layer N+1. The commoditization of compute enabled the genesis of cloud-native databases; the commoditization of those is enabling new genesis above them.
- **"Efficiency enables innovation"** — utility-scale components free up resources for genesis-stage bets. Outsourcing what's commodity frees the team to invest in what's not.

## Doctrine and gameplay

Wardley separates universal advice from contextual moves.

- **Doctrine** is universal — it applies regardless of map shape. Examples: "Focus on user needs," "Use a common language," "Know your users," "Think small (as in teams)," "Be transparent." Doctrine doesn't change with the map; it is the discipline that lets the map be honest in the first place.
- **Gameplay** is contextual — moves you make based on the map's current shape. Examples: "Open-source the commodity layer to drive a competitor's investment to zero," "Embrace the evolution of a layer to force consolidation," "Acquire to accelerate a genesis-stage component you cannot build internally." Gameplay shifts as the map shifts; doctrine does not.

A team using gameplay without doctrine plays clever but inconsistent moves. A team using doctrine without gameplay is rigorous but does not act.

## Common failure modes

- **Mapping without a user need.** Without the anchor, the artifact is a diagram of components, not a map of strategy. Every move suggested by the diagram is unrooted; the team will argue past each other about which moves to make.
- **Placing components on the evolution axis by feel.** Wardley provides characteristics tables (genesis is uncertain, expensive, novel; commodity is metered, undifferentiated, well-understood). Use the characteristics; do not place by intuition.
- **Using the map as a static artifact.** The "everything evolves" climatic pattern means a stale map misleads more than no map. Revisit on a cadence — at minimum, per strategy refresh.

## How the kit uses this framework

- **`/wardley-map`** (planned — ROADMAP P7.7) — interactive value-chain mapping with evolution axis. Enterprise mode only — the `mode-guard` hook (F2.4, shipped) blocks this command in greenfield mode.
- **`wardley-evolution` skill** (planned — ROADMAP P7.8) — places components on the evolution axis using Wardley's characteristics tables.
- **`/value-chain-evolution`** (planned — ROADMAP P7.10) — diffs the value chain across quarters; consumes the climatic pattern "everything evolves" as its core assumption.
- **`context/frameworks/competitive-analysis.md`** uses the evolution-axis lens as one of three lenses in a thorough competitive analysis.
- **`mode-guard` hook** (F2.4, shipped at `scripts/mode-guard.py`; documented at `.claude/hooks/mode-guard.md`) — enforces enterprise-mode-only access to the Wardley commands.

## References

- Wardley, S. (ongoing). *Wardley Maps*. CC-BY-SA, https://list.wardleymaps.com/. The canonical source — the book is published openly under CC-BY-SA and is the single reference for all of Wardley's primitives.
- `context/frameworks/competitive-analysis.md` — consumer of the evolution-axis lens.
- `.claude/hooks/mode-guard.md` — the kit's mode-gated access hook.
