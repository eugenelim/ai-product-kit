# Reference context (Layer 3)

Not loaded automatically. Claude pulls these only when relevant. Keeps the context window clean.

> **Status note:** the `personas/`, `products/`, `business/`, `voice/`, and `glossary/` subdirectories ship empty — they hold *user-supplied* content created as a project unfolds. The `frameworks/` subdirectory ships with only `ontology.md`; every other framework reference listed below is *(planned — see [ROADMAP F4](../ROADMAP.md#foundation-4--reference-frameworks))*.
>
> **Fallback when a planned framework is needed but absent:** use `context/frameworks/ontology.md` as the always-available substrate, note the gap explicitly in your output (e.g., "would have pulled `falsification.md` but it does not yet exist — proceeding with the ontology's `Assumption` and `Experiment` types as the closest available"), and surface the missing file as a ROADMAP-priority signal to the user. Do not invent the contents of a planned framework file.
>
> **Special case — `competitive-analysis.md`:** the shipped `/competitive-research` command and `competitor-research` agent both reference this framework, but the file does not yet exist (ROADMAP F4.13). Until it ships, both fall back to the inline analysis structure declared in the agent's own contract.

Catalog. Each entry says **when** to pull.

## `personas/`

Target customer profiles. One file per persona. Pull when:
- Drafting anything customer-facing (`/exec-narrative`, `/critique`, `/draft-vision`)
- Designing assumption tests (desirability lens needs the persona)
- Generating sales enablement (`/battlecard`)
- Running landing interviews

Files: `primary.md`, `secondary.md`, `non-target.md`

## `products/`

Your product surface — features, capabilities, pricing, integrations. Pull when:
- Running `/competitive-research` (greenfield) or `/wardley-map` (enterprise)
- Drafting a spec or release notes
- Generating a battlecard
- Producing landing reports (needs predicted thresholds)

Files: one per product / surface, plus `pricing.md`, `roadmap-bets.md`

**Discipline:** update on every release. Stale product context is the most common cause of bad output.

## `business/`

Pull for work requiring the business model. Pull when:
- Stakeholder updates, exec narratives, strategic intents
- Assessing viability (viability lens)
- Generating sales/marketing copy
- Running `/strategy-refresh` or `/audit-portfolio-coherence`

Files: `profile.md`, `revenue-model.md`, `channels.md`, `strategy.md`

## `voice/`

Pull when drafting customer-facing or in-your-name content. Files: `guide.md`, `samples/`, `anti-samples/`

## `frameworks/`

The PM-craft schemas the kit operates on. Pull when working with the corresponding artifact.

### Universal type system
- **`ontology.md`** *(shipped)* — the canonical product/business ontology: eight domains plus a kit-composite Domain I, 82 documented typed objects (74 atomic + 8 composite), traceability rules, lifecycle states. Pull for any work that produces a typed artifact (which is nearly everything). The `ontology-classifier` skill *(planned — [ROADMAP F1.3](../ROADMAP.md#foundation-1--make-the-existing-audits-run))* will load this.

### Strategy phase *(all planned)*
- `rumelt.md` *(planned — F4.7)* — diagnosis / guiding policy / coherent actions; failure modes
- `wardley.md` *(planned — F4.8)* — value chain, evolution axis, climatic patterns (enterprise mode)
- `strategic-coherence.md` *(planned — F4.10)* — three axes (resources / capabilities / posture); incoherence patterns
- `perri-strategy-stack.md` *(planned — not yet in ROADMAP)* — vision / intent / initiatives / options

### Discovery phase *(all planned)*
- `continuous-discovery.md` *(planned — F4.1)* — the weekly habit: 3 interviews, 1 experiment, 1 falsification
- `opportunity-solution-tree.md` *(planned — F4.2)* — node types, source opportunities, structure
- `interview-snapshot.md` *(planned — F4.3)* — snapshot contents, transcript extraction
- `jtbd.md` *(planned — F4.9)* — Christensen / Ulwick formulations

### Validation phase *(all planned)*
- `assumption-tests.md` *(planned — F4.4)* — five-lens taxonomy: desirability / viability / feasibility / usability / ethical
- `falsification.md` *(planned — F4.5)* — what "survived" actually means; predeclared threshold pattern
- `validation-theatre.md` *(planned — F4.6)* — failure modes; the "would you pull the work?" test
- `bland-testing-business-ideas.md` *(planned — not yet in ROADMAP)* — assumption-mapping + experiment-selection reference

### Delivery phase *(all planned)*
- `competitive-analysis.md` *(planned — F4.13)* — what a thorough analysis contains
- `roadmap-as-bets.md` *(planned — not yet in ROADMAP)* — "roadmaps as plans for uncertainty"
- `ears.md` *(planned — F4.12)* — EARS pattern for spec sentences
- `cagan-dual-track.md` *(planned — not yet in ROADMAP)* — discovery + delivery as parallel tracks
- `context-map.md` *(planned — not yet in ROADMAP)* — bounded contexts, ownership, shared shapes

### Landings phase *(all planned)*
- `landings-not-launches.md` *(planned — F4.11)* — adoption curve is part of the work
- `outcome-vs-prediction.md` *(planned — not yet in ROADMAP)* — measuring against predeclared thresholds

## `glossary/`

Short entries — one paragraph each, with synonyms and "not to be confused with."

- `discovery-terms.md`, `validation-terms.md`, `delivery-terms.md`, `business-terms.md`, `strategy-terms.md`
- `ontology-terms.md` (v3) — the eight domains plus Domain I and their 82 documented types, with cross-references *(planned — when this glossary file ships it must stay in sync with `context/frameworks/ontology.md`, which is the source of truth)*

## Discipline rules

1. **Keep files small and atomic.** One concept per file. Split at ~500 words.
2. **Cross-link sparingly.** Each file should be self-contained.
3. **Update the catalog when you add a file.** This README tells Claude when to pull it. Undocumented = invisible.
4. **The cardinal sin:** one giant `business.md`. Atomic files = surgical context loading = better output.
