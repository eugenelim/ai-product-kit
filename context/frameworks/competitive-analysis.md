# Competitive Analysis

> Kit synthesis of three named lenses for analyzing competitors: Michael Porter's five forces (*Competitive Strategy*, Free Press, 1980) for industry structure, Simon Wardley's evolution axis (`context/frameworks/wardley.md`) for component positioning, and Christensen/Ulwick's Jobs-to-be-Done (`context/frameworks/jtbd.md`) for hired-for-what comparison. The kit's `/competitive-research` command (shipped, greenfield mode) and `competitor-research` agent (shipped) both consume this framework; until this doc shipped, both fell back to the inline analysis structure declared in the agent's own contract (`context/README.md` line 9 special case). Note: this framework is kit synthesis of three lenses, not a published framework by any single author.

## What thorough analysis contains

A competitive analysis that earns its keep produces three distinct outputs. A scan without a synthesis is data; a synthesis without a conclusion is theatre.

- **A named-competitor scan.** For each in-scope competitor: positioning (the one-sentence claim they make to the market), features (what they actually ship — not what their landing page promises), pricing (tiers, anchors, packaging), recent moves (acquisitions, launches, hires, public statements), target customer (segments, ICP).
- **A cross-competitor synthesis.** Where do the competitors converge (parity), where do they diverge (differentiators), and where do they collectively leave gaps? The synthesis is where decision-utility comes from; the per-competitor scan in isolation is inventory, not insight.
- **A decision-useful conclusion.** What this changes about our strategy — what to defend, what to copy, what to ignore, what to bet on. If the analysis ends without naming a decision, it didn't earn the cost of the work.

A scan of 12 competitors with no synthesis and no conclusion is a worse outcome than a scan of 3 with both.

## Three lenses — Porter, Wardley, JTBD

Use **at least two** lenses. One lens is rarely enough — single-lens analysis is the most common failure mode, named below.

- **Porter's five forces.** The industry-structural lens; tells you whether the market itself is attractive, irrespective of any single competitor. Useful early when the team is asking "is this a market we should be in?" rather than "how do we beat competitor X?" Reference-only — the kit ships no Porter framework doc; cite the 1980 book. The five forces and their operative questions:
  - *Threat of new entrants* — what barriers would a new competitor face (capital, regulation, network effects, brand)?
  - *Bargaining power of suppliers* — how concentrated are upstream suppliers; can they raise prices or restrict supply?
  - *Bargaining power of buyers* — how easily can customers switch, push back on price, or aggregate demand?
  - *Threat of substitutes* — what alternative ways exist to do the same job (the JTBD lens overlaps here)?
  - *Industry rivalry* — how competitive is the existing market on price, feature parity, marketing intensity?
- **Wardley's evolution axis.** Where does each competitor sit on each component of the value chain (Genesis → Custom → Product → Commodity)? A competitor whose differentiator is at Commodity is on borrowed time; one whose differentiator is at Genesis is hard to copy. Cross-link to `context/frameworks/wardley.md`. Useful when the team is asking "where is the durable advantage?"
- **JTBD.** What job is each competitor being hired for? Two competitors with overlapping features can be hired for different jobs and not actually compete. Cross-link to `context/frameworks/jtbd.md`. Useful when the team is asking "are we even competing with this company, or are we adjacent?"

A competitor's **positioning** is the public claim; the lenses tell you whether the claim holds up structurally (Porter), durably (Wardley), and against the right customer-job (JTBD).

## Common failure modes

- **Table-stakes feature comparison without positioning.** A feature matrix is data, not analysis. Two competitors with the same features can occupy different positions (premium vs commodity; enterprise vs consumer); the matrix obscures the positioning the lenses surface.
- **The "everyone's a competitor" trap.** No prioritization; the scan is too thin everywhere. Three competitors analyzed deeply produces better decisions than twelve analyzed shallowly.
- **Copying competitor copy.** Don't. Short attributed quotes only — per the kit's AGENTS.md rule "Don't reproduce competitor copy verbatim." Paraphrase with sources; the analysis is the kit's voice, not the competitor's.
- **Single-lens analysis.** Using only the feature comparison; missing the industry-structural lens (Porter), the evolution-axis lens (Wardley), or the JTBD lens. This is the most common failure — the matrix is fast to build; the lens analysis is not.
- **Conclusion-by-omission.** The scan is detailed but the "what this changes about our strategy" section is missing. The work has no decision-utility — it informs no move.

## How the kit uses this framework

This framework defines both the **per-competitor expectations** (the scan; ≥2 lenses applied per competitor; positioning explicit) and the **cross-competitor expectations** (the synthesis; the decision-useful conclusion). Until this framework shipped, consumers fell back to the inline contract in `.claude/agents/competitor-research.md`; with the framework shipped, that contract is canonical.

- **`/competitive-research`** (shipped, greenfield mode only — the `mode-guard` hook (F2.4) blocks it in enterprise mode) — the command that produces per-competitor analyses; its contract names this framework as the rule library.
- **`competitor-research` agent** (shipped) — fan-out worker, one competitor at a time. Writes findings to `market/competitors/<slug>.md`.
- **`/market-scan`** (planned — ROADMAP P7.11) — aggregates per-competitor analyses into a cross-competitor synthesis with positioning and pricing comparison tables. **Interim posture (until P7.11 ships):** the cross-competitor synthesis is produced manually by the PM using the per-competitor files at `market/competitors/<slug>.md`; `market/comparison-tables/` is the home for those manual syntheses.
- **`mode-guard` hook** (F2.4, shipped) — enforces greenfield-mode-only access to the named commands.
- **The greenfield-mode strategy commands generally** consume the cross-competitor synthesis.

Frame: this framework defines what thoroughness means; the consumers above produce the deliverables that meet (or fail) the definition.

## References

- Porter, M. E. (1980). *Competitive Strategy: Techniques for Analyzing Industries and Competitors*. Free Press. The canonical source for the five-forces lens.
- Wardley, S. (ongoing). *Wardley Maps*. CC-BY-SA, https://list.wardleymaps.com/. The canonical source for the evolution-axis lens — see also `context/frameworks/wardley.md`.
- Christensen, C. M. (2016). *Competing Against Luck*. HarperBusiness, AND Ulwick, A. W. (2005). *What Customers Want*. McGraw-Hill. The two canonical formulations of JTBD — see also `context/frameworks/jtbd.md`.

Note: **this framework is kit synthesis of three lenses**, not a published framework by any of the four named authors. The lenses are canonical; the assembly into a single competitive-analysis discipline is kit-original.

- `context/frameworks/wardley.md` — evolution-axis lens.
- `context/frameworks/jtbd.md` — Jobs-to-be-Done lens.
- `.claude/commands/competitive-research.md` — the shipped consumer.
- `.claude/agents/competitor-research.md` — the fan-out worker.
