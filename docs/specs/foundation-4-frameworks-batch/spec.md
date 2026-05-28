# Spec: foundation-4-frameworks-batch

- **Status:** Drafting
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** framework-ref (12 deliverables under one spec — mirrors the F3 `template-authoring-convention` and F4.12 `ears-lint` precedents of shipping a coupled batch under one work-loop when artifacts share contract surface)
- **Serves kit phase:** Cross-cutting (Strategy, Discovery, Validation, Delivery, Landings — each framework serves the phase named in its row below)
- **Constrained by:** ROADMAP F4.1, F4.2, F4.3, F4.4, F4.5, F4.6, F4.7, F4.8, F4.9, F4.10, F4.11, F4.13 (F4.12 shipped 2026-05-23 and is the shape precedent); `context/frameworks/ears.md` and `context/frameworks/ontology.md` (the two shape precedents — un-frontmatter-ed prose-only docs sitting outside `PHASE_DIRS`); `context/README.md` "Catalog" section (every shipped framework must flip from `*(planned — F4.x)*` to `*(shipped)*` and update the catalog line); `docs/CONVENTIONS.md` §"Specs and Plans" (kit-meta exemption); `tools/lint-frontmatter.py` (default mode does not walk `context/frameworks/` — the framework docs are exempt from default-mode linting); `.claude/skills/work-loop/SKILL.md` (loop doctrine); Mavin et al. (2009) — precedent for the citation-and-paraphrase discipline that every framework doc in this batch must follow.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships 12 canonical framework reference docs under `context/frameworks/` — one per ROADMAP F4 item except F4.12 (already shipped). Each doc is a prose-only reference (no YAML frontmatter, ≤ 150 body lines target, ≤ 200 hard cap), modeled on `context/frameworks/ears.md`. Each doc cites its canonical author(s) verbatim and names the kit consumers (commands, skills, templates) that pull it. Together they close every dangling `*(planned — F4.x)*` reference in `context/README.md` and unblock every downstream command/skill/template whose contract names a framework that did not yet exist.

## Objective

Author 12 prose reference docs under `context/frameworks/`, completing Foundation 4. Each doc serves as the single canonical source-of-truth for one named framework, so that on-demand pulls from skills, commands, and templates resolve to a real file rather than a broken link or the silent ontology-fallback declared in `context/README.md` line 7.

The 12 deliverables, in ROADMAP order:

| # | File | ROADMAP slug | Phase served | Canonical author(s) / source |
|---|---|---|---|---|
| 1 | `continuous-discovery.md` | F4.1 `framework-continuous-discovery` | Discovery | Teresa Torres, *Continuous Discovery Habits* (2021) — the weekly habit loop (3 interviews / 1 experiment / 1 falsification per week) |
| 2 | `opportunity-solution-tree.md` | F4.2 `framework-ost` | Discovery | Teresa Torres, *Continuous Discovery Habits* (2021) ch. 6–7 — node types (Outcome, Opportunity, Solution, Assumption Test), source opportunities, tree-shape rules |
| 3 | `interview-snapshot.md` | F4.3 `framework-interview-snapshot` | Discovery | Teresa Torres, *Continuous Discovery Habits* (2021) ch. 5 — the snapshot schema (Goal, Workflow, Pain Points, Workarounds, Tools, Direct quote, Date) and transcript-extraction rules |
| 4 | `assumption-tests.md` | F4.4 `framework-assumption-tests` | Validation | David Bland & Alex Osterwalder, *Testing Business Ideas* (2019) — the five-lens taxonomy (desirability / viability / feasibility / usability / ethical) plus test-card-style framing |
| 5 | `falsification.md` | F4.5 `framework-falsification` | Validation | Karl Popper (epistemological foundation: *The Logic of Scientific Discovery*, 1934) + kit synthesis on the predeclared-threshold pattern that this kit's `hook-assumption-threshold-lock` (F2.2) enforces |
| 6 | `validation-theatre.md` | F4.6 `framework-validation-theatre` | Validation | Kit synthesis. Names the failure modes ("we already decided to ship; the test is just to make ourselves feel better"; "we set the bar low enough that everything passes"; "we ran the test but won't actually pull the work if it fails"); the "would you pull the work?" test; cites Marty Cagan (*Inspired*, 2017) on "feature factory" anti-patterns and Teresa Torres on the role of falsification in genuine discovery |
| 7 | `rumelt.md` | F4.7 `framework-rumelt` | Strategy | Richard Rumelt, *Good Strategy, Bad Strategy* (2011) — the kernel (Diagnosis, Guiding Policy, Coherent Action) and the four failure modes (fluff, failure to face the challenge, mistaking goals for strategy, bad strategic objectives) |
| 8 | `wardley.md` | F4.8 `framework-wardley` | Strategy (enterprise mode) | Simon Wardley, *Wardley Maps* (CC-BY-SA online book, 2018+) — value chain anchored on user need, the evolution axis (Genesis → Custom → Product → Commodity), climatic patterns, doctrine, and gameplay |
| 9 | `jtbd.md` | F4.9 `framework-jtbd` | Discovery / Strategy | Clayton Christensen (HBR "Know Your Customers' Jobs to Be Done", 2016; *Competing Against Luck*, 2016) for the milkshake-style "jobs" formulation; Tony Ulwick (*What Customers Want*, 2005; "Outcome-Driven Innovation") for the desired-outcome / outcome-statement formulation. Both are canonical; the doc names the difference. |
| 10 | `strategic-coherence.md` | F4.10 `framework-strategic-coherence` | Strategy | Kit synthesis, citing Rumelt (*Good Strategy, Bad Strategy* ch. 5 on the coherent-actions kernel-leg) — the three axes (resources / capabilities / market posture) and the incoherence patterns (resource conflict, capability conflict, market-posture conflict). The companion to `rumelt.md`; the audit `/audit-portfolio-coherence` consumes it. |
| 11 | `landings-not-launches.md` | F4.11 `framework-landings-not-launches` | Landings | Kit synthesis, citing Marty Cagan (*Inspired*, *Empowered*) on outcome-vs-output discipline and the kit's own ROADMAP Phase-5 ontology (Landing Report → Adoption / Outcome / Counter-metric). "Launching is the start of the work, not the end" — the adoption curve is part of the work, not a marketing follow-on. |
| 12 | `competitive-analysis.md` | F4.13 `framework-competitive-analysis` | Strategy (greenfield mode) | Kit synthesis, citing Michael Porter (*Competitive Strategy*, 1980) for the five-forces lens, Simon Wardley for the evolution-axis lens (cross-link to `wardley.md`), and Christensen/Ulwick for the JTBD lens (cross-link to `jtbd.md`). What a thorough competitive analysis contains; what makes the difference between table-stakes scanning and decision-useful analysis. |

## Why now

`context/README.md` lines 6–8 declare that when a planned framework is needed but absent, the consumer falls back to `context/frameworks/ontology.md` and surfaces the gap. That fallback was a stopgap, not a permanent posture. Every shipped Phase-4 command, the audit pipeline in Foundation 1, and the templates in Foundation 3 carry citations to one or more of these frameworks. Until they exist, those citations are documentary IOUs.

F4.12 (`ears.md`) shipped 2026-05-23 alongside its consuming skill (P4.7 `ears-lint`) under a coupled work-loop because the two artifacts share a contract surface. The remaining 12 frameworks are pure reference docs with no coupled skill — they consume nothing and are consumed by many. The cheapest path is one umbrella spec, parallel research-and-author, single verify and review pass. The F3 `template-authoring-convention` spec (ten templates under one work-loop) is the direct precedent for batch-shipping reference artifacts that share a shape contract.

Shipping all 12 in one session closes Foundation 4 entirely, removing the largest single block of `*(planned — F4.x)*` annotations across the kit and unblocking every Phase-2 / Phase-3 / Phase-5 command that names a framework in its contract.

## Inputs and outputs

**Inputs (shared across all 12 docs).**

- `context/frameworks/ears.md` — the shape precedent. Body outline: H1 + intro blockquote + `## <topic>` H2 sections + `## How the kit uses this framework` + `## References`. No YAML frontmatter.
- `context/frameworks/ontology.md` — the other shape precedent (same prose-only posture, no frontmatter; the precedent that `context/frameworks/` sits outside `PHASE_DIRS`).
- `context/README.md` — the on-demand-pull catalog. Each shipped framework's line under the catalog must flip from `*(planned — F4.x)*` to `*(shipped)*`. The "Fallback when a planned framework is needed but absent" note (lines 6–8) stays in place because some F4-adjacent frameworks (e.g., `perri-strategy-stack`, `bland-testing-business-ideas`) remain planned outside this batch.
- `ROADMAP.md` lines 175–187 — the Foundation 4 row block. Each shipped row flips from `[ ]` to `[x]` with `**Shipped:** 2026-05-28`.
- `docs/INVENTORY.md` lines 138–146 (the Phase 4-D "Engineering handoff" sub-section that holds the existing `EARS framework` REF row) — pattern for inserting REF rows for the new frameworks. (Most of the new frameworks land under their phase's table, not the Phase-4-D one — see Boundaries §"Always do".)
- The canonical sources named in each row of the §"Objective" table. Where the source is online and CC-licensed (Wardley Maps book), agents may WebFetch; where the source is behind a paywall or copyright (Torres, Christensen, Rumelt, Cagan, Bland, Ulwick, Porter), agents must paraphrase from public summaries and cite the book by title + year — no verbatim copying beyond short attributed quotes (per AGENTS.md "Don't reproduce competitor copy verbatim" rule, extended to all third-party sources in this batch).

**Outputs (12 files; each follows the same shape contract).**

Each `context/frameworks/<slug>.md` file has this body outline, in order, no YAML frontmatter:

1. **H1** — `# <Framework name>` (sentence-case; matches the canonical name used by its author; e.g., `# Continuous Discovery`, `# Opportunity Solution Tree`, `# Rumelt's strategy kernel`, `# Wardley mapping`).
2. **Intro blockquote** — one paragraph: what the framework is (1 sentence with author + year), why this kit uses it (1 sentence naming the consuming surface — phase, command, skill, or audit), and a pointer to the kit consumer(s) for further context.
3. **2 to 5 H2 sections** describing the framework's substance. Each H2 names a canonical concept from the source. The per-framework required H2 list is named below under §"Per-framework required content".
4. **H2** `## How the kit uses this framework` — names the consuming surface explicitly (commands, skills, audits, hooks, templates) and how each one pulls the framework. If a consumer is *planned* (not yet shipped), name the ROADMAP item.
5. **H2** `## References` — the canonical source(s) verbatim citation (author, year, title, edition or chapter where load-bearing), plus 0–3 secondary kit cross-links (e.g., `docs/HANDOVERS.md` §X, `context/frameworks/<other-slug>.md`).

**Body cap.** Target ≤ 150 lines; hard cap 200 (matches the F4.12 precedent — T2 of the ears-lint spec). The cap exists to keep these as reference docs, not tutorials.

### Per-framework required content

The H2 section list below names the *minimum* required content. Each framework may add 1 H2 beyond the minimum if its source material requires it; adding more than 1 must surface in the Plan's Changelog. Authoring agents must paraphrase, not copy; short attributed quotes (≤ 25 words) are acceptable.

**F4.1 — `continuous-discovery.md`** (target ~120 lines)
- `## The weekly habit` — the cadence (3 customer interviews + 1 experiment + 1 falsified assumption per week as Torres's target; the kit may relax to ≥1 per discipline per week, but the asymmetric target is the canonical anchor).
- `## The product trio` — the cross-functional pair (PM + designer + tech lead) that does discovery together, not as a relay.
- `## Outcome vs output orientation` — the discipline of working backwards from a single outcome metric rather than forwards from a feature list.
- `## Common failure modes` — drift to discovery theatre (we interview but don't act), the "Slack/Discord-only" research substitute, the "I'll discover next quarter" trap.

**F4.2 — `opportunity-solution-tree.md`** (target ~130 lines)
- `## The four node types` — Outcome (root), Opportunity (a customer pain/desire/aspiration), Solution (a specific intervention to address an opportunity), Assumption Test (how we'll learn whether a solution is viable). Each named with one sentence and one canonical example.
- `## Source opportunities` — every Opportunity must trace to a specific customer-research moment (interview snapshot, quote, observed behavior). Opportunities without source are conjecture.
- `## Tree-shape rules` — Outcome at the root (one per tree); Opportunities are *additive children* (the tree branches widen as you learn, not narrow); Solutions are children of one Opportunity; an Assumption Test is a child of one Solution. A Solution under two Opportunities is a smell — split or rebracket.
- `## Common failure modes` — the "solution tree" anti-pattern (skipping the Opportunity layer); the "everything is an opportunity" tree (no real customer source); the "single-path" tree (only one Opportunity per Outcome).

**F4.3 — `interview-snapshot.md`** (target ~110 lines)
- `## The snapshot schema` — Goal / Workflow / Pain Points / Workarounds / Tools / one Direct Quote / Date / Interviewer. Each field with a one-sentence definition.
- `## Transcript extraction rules` — paraphrase, do not invent; one snapshot per interviewee per session; quotes verbatim with attribution; ambiguous statements get flagged not resolved.
- `## What a good snapshot is *not*`— a summary of what the PM thinks; a synthesized persona; a sales-style needs assessment; an opportunity list (those derive from the snapshot, downstream).

**F4.4 — `assumption-tests.md`** (target ~130 lines)
- `## The five lenses` — Desirability (do customers want this?), Viability (does the business want this?), Feasibility (can we build this?), Usability (can customers use what we build?), Ethical (should we build this?). One sentence + one canonical example per lens.
- `## The test card schema` — Hypothesis / Test (cheapest method) / Metric / Threshold (declared *before* the test runs) / Outcome. Names this kit's `hook-assumption-threshold-lock` (F2.2) as the enforcement of the predeclared-threshold rule.
- `## Common failure modes` — running only desirability tests (most common; misses viability); confirmation-biased threshold setting; "we'll know it when we see it" non-threshold; running the test but not pulling the work on failure (cross-link to `validation-theatre.md`).

**F4.5 — `falsification.md`** (target ~120 lines)
- `## What "survived" means` — survived ≠ confirmed; an assumption survives one falsification attempt at one threshold; the bar to convert to "validated" is many surviving attempts at increasing thresholds. Names the kit's `validation/learnings/<slug>.md` `status: survived | killed` vocabulary.
- `## The predeclared-threshold pattern` — what counts as falsified must be declared *before* the test runs. Names the kit's `hook-assumption-threshold-lock` (F2.2) and the rationale (post-hoc rationalization is the dominant failure mode).
- `## Why the kit is asymmetric` — falsification kills; survival only postpones. The asymmetry is on purpose (Popper's logical insight) — the cheapest way to make decisions is to try to kill ideas, not to defend them.
- `## Common failure modes` — the "moving threshold" (threshold gets relaxed after a borderline result); the "soft confirm" (a survived assumption is treated as validated); the "absent threshold" (the test produces a number but there's no pre-declared meaning of it).

**F4.6 — `validation-theatre.md`** (target ~110 lines)
- `## The four signature failure modes` — (a) "we already decided to ship; the test is just to make ourselves feel better"; (b) "we set the bar low enough that everything passes"; (c) "we ran the test but won't actually pull the work if it fails"; (d) "the test is too small/short to discriminate, but we're calling it done anyway".
- `## The "would you pull the work?" test` — the single most discriminating question. If the answer is "no, regardless of the result," the test is theatre. Names this question as the kit's frontline anti-theatre check.
- `## How the kit guards against theatre` — predeclared thresholds (F2.2 hook); falsification-not-confirmation framing (`falsification.md`); explicit `status: killed` vocabulary; the assumption-skeptic agent (planned — ROADMAP P3.2).

**F4.7 — `rumelt.md`** (target ~140 lines)
- `## The kernel — Diagnosis, Guiding Policy, Coherent Action` — three legs; all three required. One sentence per leg, one canonical example (Rumelt's own — the IBM-PC kernel or the Wal-Mart kernel).
- `## What good strategy is not — the four hallmarks of bad strategy` — Fluff (vague aspirational language disguising an empty kernel); Failure to face the challenge (no real diagnosis); Mistaking goals for strategy (a goal is not a path to a goal); Bad strategic objectives (objectives that are unfocused, mutually conflicting, or unconnected to a diagnosis).
- `## The coherent-actions leg` — the leg most often skipped. Coherent actions are *coordinated, mutually reinforcing*, and *resource-feasible*. The companion framework `strategic-coherence.md` is the audit lens.
- `## Common failure modes` — the strategy-as-vision-statement substitution; the strategy-as-OKRs substitution; the missing-diagnosis pattern; the "diagnosis-as-complaint" pattern (a diagnosis that describes the symptom without naming the constraint — e.g., "we're losing market share" is a complaint; "the cost of customer acquisition is now higher than first-year revenue per customer because incumbent X bundled our differentiator" is a diagnosis).

**F4.8 — `wardley.md`** (target ~150 lines — the longest in this batch; Wardley has more named primitives)
- `## The map — value chain anchored on user need` — every map starts with a user need; the value chain hangs from that need; "if you can't tell me who the user is and what they need, you don't have a map."
- `## The evolution axis — Genesis → Custom → Product (incl. rental) → Commodity (incl. utility)` — the four stages; the implication that components move rightward over time, dragged by competition.
- `## Climatic patterns` — short list (≤5): "Everything evolves," "No two things are the same," "Inertia increases with scale," "Componentization enables higher-order systems," "Efficiency enables innovation."
- `## Doctrine and gameplay` — doctrine is universal (e.g., "Use a common language," "Focus on user needs"); gameplay is contextual (e.g., "Open-source the commodity layer to drive a competitor's investment to zero").
- `## Common failure modes` — mapping without a user need (it's a diagram, not a map); placing components on the evolution axis by feel instead of by characteristics; using the map as a static artifact instead of revising on a cadence.
- **Authoring fallback (if WebFetch against Wardley Maps online fails — rate limit, network, URL drift):** the four stage names and the five climatic patterns above are inlined in this spec section precisely so a sub-agent can author `wardley.md` from this spec without re-fetching the source. Cite the book by title (`Simon Wardley, Wardley Maps`, CC-BY-SA, ongoing online edition) and the URL (`https://list.wardleymaps.com/`) without quoting from it.

**F4.9 — `jtbd.md`** (target ~130 lines)
- `## The Christensen formulation — "jobs hired to do"` — customers "hire" products to make progress on a job; the milkshake example; the focus on *struggle moments* not demographic segmentation.
- `## The Ulwick formulation — outcome statements` — a job has measurable desired outcomes; outcome statements have a canonical four-part shape (Direction of improvement + Performance metric + Object of control + Context); these are testable. **Authoring fallback (if the Ulwick public-summary quality is sparse — public summaries frequently conflate Ulwick with Christensen):** the four-part shape is canonical Ulwick (*What Customers Want*, 2005; the "outcome-driven innovation" framing); a worked example is "minimize the time it takes (Direction + Performance metric) to find a missing document (Object of control) when preparing for a client meeting (Context)." Inline this example in the doc rather than reproducing from a secondary source.
- `## When to use which` — Christensen for early-stage discovery (what job?); Ulwick for late-stage prioritization (which outcome is underserved?). They are complementary, not competing.
- `## Common failure modes` — confusing a job with a feature; confusing a job with a persona; the "everyone's job" trap (job statements so abstract they describe everyone); the "solution-as-job" trap (defining the job as "use our product" rather than the underlying progress the customer seeks — the single most common JTBD mis-application).

**F4.10 — `strategic-coherence.md`** (target ~120 lines)
- `## The three axes` — Resource coherence (do the actions share a budget that won't starve any of them?), Capability coherence (do the actions need the same capabilities the team has?), Market posture coherence (do the actions present a consistent posture to the market — premium vs price-leader, depth vs breadth, enterprise vs consumer?).
- `## The audit lens — Rumelt's coherent-actions leg, operationalized` — the kit's `/audit-portfolio-coherence` command (F1.6) walks pairs of strategic intents and initiatives and flags axis violations. Names the audit and the script (`scripts/audit-portfolio-coherence.py` — confirmed to exist at spec-time, 2026-05-28).
- `## Incoherence patterns` — Resource conflict (two big bets fighting for the same engineers); Capability conflict (we're betting on speed and accuracy at the same time without naming which dominates); Market-posture conflict (we say enterprise to one customer, consumer to another; we say premium and freemium in the same quarter).
- `## Common failure modes` — single-axis review (only checking resources; missing capability or posture); "they're independent" rationalization (when they share scarce capability or audience).

**F4.11 — `landings-not-launches.md`** (target ~110 lines)
- `## "Launches are starts, not ends"` — the framing: shipping code is the start of adoption work, not the conclusion of build work.
- `## The adoption curve` — the work between code-in-prod and outcome-realized. Adoption is the bridge; without it, shipped output ≠ realized outcome.
- `## What a landing report contains` — names the kit's Landing Report (F3.10 template + P5.1 `/landing-report` command) — Adoption / Outcome / Counter-metric, all measured against predeclared thresholds from the parent Vision.
- `## Common failure modes` — declaring victory at code-in-prod (the most common); measuring adoption without a counter-metric (don't see the regressions you caused); shipping without a predeclared outcome target (no way to know whether it worked).

**F4.13 — `competitive-analysis.md`** (target ~140 lines)
- `## What thorough analysis contains` — a named-competitor scan (positioning, features, pricing, recent moves), the cross-competitor synthesis (gaps, parity, differentiators), and a decision-useful conclusion (what this changes about our strategy).
- `## Three lenses — Porter, Wardley, JTBD` — Porter's five forces (industry-structural lens; cross-link to no kit file — Porter is reference-only); Wardley's evolution axis (where does each competitor sit on each component? cross-link to `wardley.md`); JTBD (what job is each competitor being hired for? cross-link to `jtbd.md`). Use ≥2 lenses; one is rarely enough.
- `## What this kit asks for` — the kit's `/competitive-research` command (greenfield mode) and `competitor-research` agent each produce a one-competitor analysis; `/market-scan` (planned — P7.11) aggregates them; this framework defines the per-competitor and the cross-competitor expectations.
- `## Common failure modes` — table-stakes feature comparison without positioning (a feature matrix is not analysis); the "everyone's a competitor" trap (no prioritization); copying competitor copy (don't — short attributed quotes only per AGENTS.md).

A reader of this section should be able to write any one of the 12 framework bodies without reading anything else — the canonical author, the required H2s, the line budget, the cross-references, and the failure-mode-tax are all here.

## Boundaries

### Always do

- Write **prose only**. No YAML frontmatter at the top of any framework doc (matches `ears.md` and `ontology.md` precedents).
- Keep each framework body ≤ 200 lines (hard cap; per-framework target lines listed in §"Per-framework required content").
- Cite the canonical author(s) by full reference (author, year, title) in the `## References` section. Where the canonical source is online and openly licensed (e.g., Wardley Maps CC-BY-SA), include the URL; where it is copyright/paywalled, name the book and year, do not paste excerpts.
- Paraphrase. Short attributed quotes (≤ 25 words) only — extends the AGENTS.md "Don't reproduce competitor copy verbatim" rule to all third-party sources.
- Name the kit consumer(s) — every framework has at least one consumer (command, skill, audit, hook, template). Find the consumer in `ROADMAP.md`, `.claude/commands/`, `.claude/skills/`, `.claude/agents/`, `scripts/`, or `templates/`. If a consumer is planned (not shipped), say so and name the ROADMAP slug.
- Cross-link companion frameworks in the same batch by relative path (`context/frameworks/<other-slug>.md`). Only frameworks that genuinely depend on or extend a sibling get a cross-link — do not stuff every doc with twelve sideways links.
- Insert one INVENTORY row per framework. INVENTORY's strategy content lives under the `## Phase 7 — Phase 1 strategy commands` section in `docs/INVENTORY.md` (there is no separate "Phase 1" strategy table — the v3 INVENTORY consolidates strategy under Phase 7 with `### Enterprise-mode strategy` and `### Greenfield-mode strategy` sub-sections). Placement: `continuous-discovery`, `opportunity-solution-tree`, `interview-snapshot` → Phase 2 (Discovery) table; `assumption-tests`, `falsification`, `validation-theatre` → Phase 3 (Validation) table; `rumelt`, `strategic-coherence`, `jtbd` → in the main `## Phase 7 — Phase 1 strategy commands` table (above the enterprise/greenfield sub-sections); `wardley` → `### Enterprise-mode strategy` sub-section; `competitive-analysis` → `### Greenfield-mode strategy` sub-section; `landings-not-launches` → Phase 5 (Landings) table.
- Update `context/README.md` — flip each shipped framework's catalog line from `*(planned — F4.x)*` to `*(shipped)*`. Also flip the stale `ears.md *(planned — F4.12)*` line (line 77 region) to `ears.md *(shipped)*` — this is a pre-existing drift unrelated to this batch but is the cheapest place to fix it. (The existing `ontology.md *(shipped)*` entry on line 54 is the style precedent: dateless. The ship-date is recorded in `ROADMAP.md` and `docs/INVENTORY.md`; `context/README.md` does not duplicate it.)
- Update `ROADMAP.md` — flip each F4.x row from `[ ]` to `[x]` with `**Shipped:** 2026-05-28`.
- Check `AGENTS.md` — walk the `## Skills available to you` and `## Specialist subagents` sections; if any row references a now-shipped framework as `*(planned — ROADMAP F4.x)*`, flip the annotation to remove the planned marker. (Verified at spec-time: no F4.x planned markers currently in AGENTS.md, so this is a defensive check; a regression in the regression-window is the only failure mode.)
- Record manual-gesture verification (where applicable) and any per-framework deferred findings under `docs/specs/foundation-4-frameworks-batch/notes/`.
- Leave the `context/README.md` section-level subheadings (`### Strategy phase *(all planned)*`, `### Discovery phase *(all planned)*`, `### Validation phase *(all planned)*`, `### Delivery phase *(all planned)*`, `### Landings phase *(all planned)*`) in place. After this batch ships, those headers will be cosmetically wrong (most subsections will be "all shipped" or "mostly shipped"); fixing them is a cosmetic follow-up tracked alongside the D18 batch and explicitly out of scope here. The per-line `*(planned — F4.x)*` annotations under each header are in scope; the header itself is not.

### Ask first

- Adding a *13th* framework doc to the batch (e.g., one of the D18 `framework-additions-batch` items — `perri-strategy-stack`, `bland-testing-business-ideas`, `roadmap-as-bets`, `cagan-dual-track`, `context-map`, `outcome-vs-prediction`). These are tracked in ROADMAP §"Component-hardening defers" D18 and explicitly out of this batch's scope. Surface the question; do not silently expand the batch.
- Authoring a coupled skill or command on the basis of any framework in this batch (e.g., a `rumelt-lint` skill that mirrors `ears-lint`). Out of scope; surface as a follow-up spec.
- Modifying any consumer (command, skill, audit, hook, template) to *dispatch* this batch's framework reference, beyond the mechanical text-citation update in `context/README.md` and INVENTORY. The integration is a separate spec per consumer (mirrors the F4.12 / P4.7 split where the framework shipped without the `/draft-spec` dispatch patch).
- Extending the `tools/lint-frontmatter.py` walker to cover `context/frameworks/`. The existing posture is intentional; if you think it should change, surface as an RFC.

### Never do

- Do not invent framework variants. Each framework's canonical author defined its primitives; the kit's job is to re-project them faithfully and name the kit's consuming surface. If a primitive does not appear in the canonical source, do not add it under the canonical author's name. Kit-original concepts (e.g., the predeclared-threshold pattern in `falsification.md`, the "would you pull the work?" test in `validation-theatre.md`) are explicitly labelled as kit synthesis, not attributed to the canonical author.
- Do not copy paragraphs from the canonical source. Short attributed quotes only; everything else paraphrased.
- Do not add a YAML frontmatter block to any framework doc.
- Do not exceed the 200-line hard cap on any doc.
- Do not modify `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `context/frameworks/ears.md`, or `tools/lint-frontmatter.py`.
- Do not introduce a new ontology object_type for "Framework Reference" (existing posture: framework references are kit-meta scaffolding, not Domain A-I types; same posture as `ontology.md` and `ears.md`).
- Do not create a new top-level folder. Everything lands under existing folders.
- Do not push a commit that mentions Claude / Anthropic / AI in the message (per the user's auto-memory `feedback_no_claude_coauthor`).

## Verification mode

- **Goal-based check** for every framework doc — per-file grep predicates (file exists; ≤ 200 lines; H1 present; required H2 sections present; canonical-author last-name present in `## References`).
- **Audit-driven** for kit-wide health — `python3 tools/lint-frontmatter.py --all` exits 0 (no product-artifact regression; framework docs are not walked by default mode); `bash tools/pre-pr.sh` exits 0.
- **Adversarial-reviewer** (post-EXECUTE) — one dispatch per framework doc, each comparing the produced doc to its slice of this spec (§"Per-framework required content"). Findings triaged per the standard work-loop rules (block / needs-fix / defer).

The 12 framework docs are pure reference content with no runnable interface, so there is no manual-gesture verification mode (no in-session classification, no fresh-session reproduction). The goal-based + adversarial-reviewer combination is the equivalent gate for prose-reference artifacts.

## Contract tests

Each test is one shell line or one verifiable predicate. They are the gate. Tests are grouped by deliverable; the kit-wide row at the bottom runs once across all 12 outputs.

For each `<slug>` in {`continuous-discovery`, `opportunity-solution-tree`, `interview-snapshot`, `assumption-tests`, `falsification`, `validation-theatre`, `rumelt`, `wardley`, `jtbd`, `strategic-coherence`, `landings-not-launches`, `competitive-analysis`}:

- `T-<slug>-1` — `test -f context/frameworks/<slug>.md` (the file exists).
- `T-<slug>-2` — `[[ $(wc -l < context/frameworks/<slug>.md) -le 200 ]]` (hard cap 200 — this is the mechanical gate). The per-framework target line count under §"Per-framework required content" is **advisory only**, checked by the post-EXECUTE adversarial-reviewer, not by any contract test. A 180-line doc passes T-<slug>-2; the reviewer flags it as over-target.
- `T-<slug>-3` — `[[ $(grep -c "^# " context/frameworks/<slug>.md) -ge 1 ]]` (H1 present).
- `T-<slug>-4` — `[[ $(grep -c "^## How the kit uses this framework$" context/frameworks/<slug>.md) -eq 1 ]]` (consuming-surface section present).
- `T-<slug>-5` — `[[ $(grep -c "^## References$" context/frameworks/<slug>.md) -eq 1 ]]` (references section present).
- `T-<slug>-6` — `! head -1 context/frameworks/<slug>.md | grep -q "^---$"` (no YAML frontmatter — first line is not a frontmatter delimiter).
- `T-<slug>-7` — per-framework canonical-author grep (one author last-name per row below must appear in the file, case-insensitive):

| Slug | Required author name(s) — any one suffices |
|---|---|
| `continuous-discovery` | `Torres` |
| `opportunity-solution-tree` | `Torres` |
| `interview-snapshot` | `Torres` |
| `assumption-tests` | `Bland` or `Osterwalder` |
| `falsification` | `Popper` |
| `validation-theatre` | `Torres` **and** `Cagan` (the spec's §"Per-framework required content" requires citing both — Cagan for "feature factory" framing, Torres for the falsification frame; both must appear in the file) |
| `rumelt` | `Rumelt` |
| `wardley` | `Wardley` |
| `jtbd` | `Christensen` or `Ulwick` |
| `strategic-coherence` | `Rumelt` |
| `landings-not-launches` | `Cagan` |
| `competitive-analysis` | `Porter` or `Wardley` or `Christensen` |

- `T-<slug>-8` — per-framework H2 content keyword grep (one keyword per file must appear case-insensitively in the body, catching sub-agents that re-label required H2s):

| Slug | Required content keyword (case-insensitive `grep -qi`) |
|---|---|
| `continuous-discovery` | `weekly` |
| `opportunity-solution-tree` | `outcome` |
| `interview-snapshot` | `workflow` |
| `assumption-tests` | `desirability` |
| `falsification` | `threshold` |
| `validation-theatre` | `pull the work` |
| `rumelt` | `diagnosis` |
| `wardley` | `evolution` |
| `jtbd` | `job` |
| `strategic-coherence` | `coherence` (in body, not just H1) |
| `landings-not-launches` | `adoption` |
| `competitive-analysis` | `positioning` |

Kit-wide:

- `T-K1` — `python3 tools/lint-frontmatter.py --all` exits 0 (no product-artifact regression; framework docs sit outside `PHASE_DIRS` so they are not walked).
- `T-K2` — `bash tools/pre-pr.sh` exits 0.
- `T-K3` — `ROADMAP.md` shows `[x]` for F4.1, F4.2, F4.3, F4.4, F4.5, F4.6, F4.7, F4.8, F4.9, F4.10, F4.11, F4.13, each with `**Shipped:** 2026-05-28`.
- `T-K4` — `context/README.md` has zero remaining `*(planned — F4.x)*` annotations for any of the 12 shipped slugs (one grep per slug) **and** zero remaining `*(planned — F4.12)*` (the stale ears.md catalog line). The note line about fallback (lines 6–8) and other non-F4 planned framework lines stay in place.
- `T-K5` — `docs/INVENTORY.md` contains one REF row per shipped framework. The row format matches the existing `EARS framework | REF | (pulled) | — | context/frameworks/ears.md | shipped (2026-05-23)` template (with the new date).
- `T-K6` — Spec/plan cleanup: spec.md status = `Shipped (2026-05-28)`; plan.md status = `Done (2026-05-28)`; state.json gitignored, not staged.
- `T-K7` — Two commits on the current branch, both present in the last two HEAD commits at SHIP-time: `git log --oneline -2` contains a line matching `docs(foundation-4-frameworks-batch): F4.1–F4.13 spec + plan — PLAN-phase` (the PLAN commit) AND a line matching `feat(foundation-4-frameworks-batch): ship F4.1–F4.13 (12 reference frameworks)` (the SHIP commit). No Claude/Anthropic/AI mention in either message.

## Non-goals

- Authoring a runnable skill or command coupled to any framework in this batch. Coupled skills (like `ears-lint` for `ears.md`) are separate specs.
- Modifying `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, or `context/frameworks/ears.md`.
- Extending `tools/lint-frontmatter.py` to walk `context/frameworks/`. Default-mode exclusion is intentional.
- Shipping the other six "framework-additions-batch" items (D18 in ROADMAP) — they are out of this batch's scope and tracked separately.
- Producing per-framework specs under `docs/specs/framework-<slug>/`. The umbrella spec is the per-framework spec; the F3 `template-authoring-convention` precedent applies.
- Writing tutorials. These are reference docs, not how-tos (Diátaxis "reference" quadrant).
- Adding any ontology object_type. Framework references are kit-meta scaffolding.

## Open questions

1. **Date discipline if the batch slips past 2026-05-28.** _Resolved here: all `Shipped:` annotations and INVENTORY rows use the date the second commit lands. If the work slips one calendar day, the spec/plan/state files and the ROADMAP rows all use the new date — there is no carrying of the originally-planned date. The user's auto-memory `currentDate` confirms 2026-05-28; if the second commit lands on 2026-05-29, find-replace `2026-05-28` → `<actual-date>` across exactly four targets before the second commit: (a) `ROADMAP.md` (the 12 newly-flipped F4 rows); (b) `docs/INVENTORY.md` (the 12 newly-inserted REF rows); (c) `docs/specs/foundation-4-frameworks-batch/spec.md` (the Status line and any §"Why now" / §"Open questions" references); (d) `docs/specs/foundation-4-frameworks-batch/plan.md` (the Status line and the Changelog entry). The `context/README.md` catalog lines do not carry a date — they flip to `*(shipped)*` without a date suffix, matching the existing in-repo `*(shipped)*` style._
2. **What if a canonical source is genuinely unfindable for one framework?** (e.g., the secondary literature on `validation-theatre.md` is patchy because the framework is mostly kit synthesis.) _Resolved here: kit-synthesis frameworks (specifically `validation-theatre.md`, `strategic-coherence.md`, `landings-not-launches.md`, `competitive-analysis.md`) cite at least one named author whose work *grounds* the synthesis (the §"Objective" table names them) plus the kit's own consuming surface; they do not invent precursor sources. The `## References` section labels these as "synthesis grounded in <author>, <year>" rather than "framework by <author>."_
3. **Should the batch include the six D18 frameworks?** _Resolved here: no. Each is a separate ROADMAP item that has not earned an F4.x slot. Adding them silently expands scope; the Boundaries §"Ask first" rule requires surfacing the question first. The user can approve a follow-up spec to ship D18 in a separate wave._
4. **Branch naming.** _Resolved here: per the user's auto-memory `feedback_branch_prefix`, branches must use `eugenelim/` prefix. Current branch is `eugeneacn/nicosia` (Conductor's default). The user explicitly framed this work as "complete in this session" without asking for a branch rename, so the work proceeds on the current branch. A rename is a separate action; this spec does not block on it._
5. **Fan-out failure handling.** _Resolved here: per the user's global `~/.claude/CLAUDE.md` note on Claude Code bug #57037, parallel dispatch is preferred but may cascade-fail. On failure, fall back to single-agent dispatch one framework at a time. The fallback retry does not count against the work-loop iteration cap (it's a tool-availability fallback, not a content-quality iteration)._
6. **Self-consistency limitation acknowledgment.** _Resolved here: same model instance authors this spec, dispatches the 12 sub-agents, and runs the adversarial-reviewer. Mitigation: each sub-agent is given the canonical-author citation as a hard requirement (T-<slug>-7), so the agent must surface the canonical source to its working context to pass. The post-EXECUTE adversarial-reviewer is dispatched fresh per-framework, which dilutes (does not eliminate) the self-marking effect. **Stronger limitation acknowledgment:** the reviewer checks the produced doc against this spec's §"Per-framework required content" — it does not independently verify the canonical source material. Factual fidelity to the canonical source (e.g., did the agent paraphrase Torres's weekly habit numbers correctly?) is not mechanically gated; it depends on the author's paraphrase quality and any reviewer's prior domain knowledge. A fresh-session human review by someone with canonical-source fluency is the missing independent gate; it is a deferred follow-up._

## Acceptance criteria

- [ ] All 12 framework docs exist at `context/frameworks/<slug>.md` and match the §"Per-framework required content" outline.
- [ ] All `T-<slug>-1` through `T-<slug>-7` predicates pass for each of the 12 slugs.
- [ ] `T-K1` through `T-K7` pass.
- [ ] ROADMAP F4.1, F4.2, F4.3, F4.4, F4.5, F4.6, F4.7, F4.8, F4.9, F4.10, F4.11, F4.13 flipped to `[x]` with `**Shipped:** 2026-05-28` (or the actual ship date).
- [ ] `context/README.md` catalog flipped for all 12 shipped slugs.
- [ ] `docs/INVENTORY.md` has one new REF row per framework.
- [ ] No new ontology object_type; no new top-level folder; no modification of `HANDOVERS.md`, `CONVENTIONS.md`, `ontology.md`, or `ears.md`.
- [ ] No Claude/Anthropic/AI mention in commit messages.

## Cross-references

- **Consumed by:** every command, skill, audit, hook, and template named in each framework's `## How the kit uses this framework` section. Most consumers are listed in `ROADMAP.md` Phases 2, 3, 5, 7, 8; the audits in Foundation 1; the templates in Foundation 3; the hooks in Foundation 2.
- **Consumes:** the canonical sources named in §"Objective"; `context/frameworks/ears.md` and `context/frameworks/ontology.md` as shape precedents; `context/README.md` for the catalog format; `docs/INVENTORY.md` for the REF-row format; `ROADMAP.md` for the row format.
- **Frontmatter fields owned:** none. Framework docs are un-frontmatter-ed.
- **Ontology object types touched:** none directly. Frameworks are kit-meta scaffolding (same posture as `ears.md` and `ontology.md`). The frameworks *describe* domains (Discovery, Validation, Strategy, Landings) whose ontology types they support, but they do not instantiate or modify Domain A-I types.
