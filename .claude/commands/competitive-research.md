---
description: Research every competitor in market/competitors.md in parallel, then generate price and feature comparison tables. Phase 1 (Strategy), greenfield mode only.
argument-hint: "[optional: additional context, e.g. 'focus on enterprise tier']"
---

# /competitive-research

**Phase:** Strategy (1)
**Mode:** greenfield only — the `mode-guard` hook *(planned — ROADMAP F2.4; not yet enforced)* will block this in enterprise mode and direct you to `/wardley-map` + `/internal-jtbd-interview` instead. Until the hook ships, mode enforcement is documentary: confirm `.claude/CLAUDE.md` shows `mode: greenfield` before proceeding.
**Ontology types produced:** Competitor (Domain A). Per-competitor files only. (Differentiator-flavored content appears inside the aggregate tables as prose; the kit does not yet produce a typed Differentiator artifact — flag as a ROADMAP item if you want one.)

Run a full competitive landscape analysis using the canonical files in `market/`. The kit's exemplar parallel-fan-out workflow.

## Why this is greenfield-only

In greenfield, you have no internal data and no installed base; analogical reasoning from the wider industry is the cheapest situational awareness available. In enterprise/brownfield, the constraints aren't "what's possible" but "what's compatible," and revealed-preference data already exists internally. Running `/competitive-research` in enterprise mode produces a polished artifact pointing at the wrong landscape.

## Inputs

1. `market/competitors.md` — list of competitors to analyze
2. `market/product-info.md` — our product's positioning, features, pricing
3. `context/frameworks/competitive-analysis.md` *(planned — ROADMAP F4.13)* — what a thorough analysis should contain. Until shipped, the agent uses its own inline structure (see `.claude/agents/competitor-research.md` §Output).
4. `context/business/profile.md` — who we are, our target segment

If `product-info.md` is missing or older than 30 days — stop and tell me before proceeding. If `competitors.md` is missing or empty, see Step 0 below for bootstrap. If `business/profile.md` is missing, proceed but mark all "overlap with our segment" cells `Inferred` in the per-competitor files. The 30-day staleness threshold is a kit convention — review if your strategy cadence changes.

## Procedure

### Step 0 — bootstrap (only if needed)
If `market/competitors.md` does not exist or is empty: prompt the user for an initial competitor list (3-8 names is a reasonable starter), write `market/competitors.md` with one competitor per line as a markdown list, then continue to Step 1. Do NOT proceed silently with an empty list.

### Step 1 — confirm scope
List the competitors from `market/competitors.md`. Record the set of slugs being processed (used in Step 3 for stale-file detection). Confirm before kicking off if there are more than 8 (parallel runs are token-expensive).

### Step 2 — fan out
For each competitor, launch the `competitor-research` sub-agent in parallel. Each sub-agent:
- Researches one competitor end to end (positioning, features, pricing, recent moves)
- Writes findings to `market/competitors/<competitor-slug>.md` with `object_type: Competitor` frontmatter
- Reports back a one-paragraph summary

Each gets its own context window — the main thread stays clean.

**Partial-failure policy:** if a sub-agent returns a structured failure (e.g., empty WebSearch result, missing product-info), do NOT abort the whole run. Record the failure in `market/CHANGELOG.md` under this run and continue Step 3 with the competitors that succeeded; the aggregate tables will note which competitors are missing from the comparison.

### Step 3 — synthesize
After every sub-agent completes:
1. Read every file in `market/competitors/*.md`. Compare on-disk slugs against this run's slug set. If any on-disk file is for a competitor not in the current `competitors.md`, FLAG IT (do not silently include) — it's stale from a prior run after the source list changed. Move stale files to `market/competitors/_archive/<slug>-<date>.md` or note them in CHANGELOG; do not let them pollute the comparison tables.
2. Generate `market/price-comparison.md` — pricing across all tiers.
3. Generate `market/feature-comparison.md` — feature matrix grouped by capability area.
4. Our product is the first column in both tables.

### Step 4 — show me what changed
If `price-comparison.md` or `feature-comparison.md` already exists, diff before overwriting. Flag:
- New competitors entering the market
- Pricing changes since last run
- Feature gaps that opened or closed
- Stale-file removals from Step 3.1

### Step 5 — feed forward
If triggered by `/strategy-refresh`, write a summary to `strategy/diagnoses/<YYYY-MM-DD>-competitive-input.md` so the diagnosis can cite it.

### Step 6 — log
Append a line to `market/CHANGELOG.md` with the date, competitor count, a one-sentence summary of what shifted, and a count of any sub-agent failures from Step 2. If `market/CHANGELOG.md` does not exist, create it with a header and append the first entry.

$ARGUMENTS
