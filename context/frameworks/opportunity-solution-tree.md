# Opportunity Solution Tree

> A visual artifact for connecting a desired Outcome to the Opportunities, Solutions, and Assumption Tests that pursue it. Defined by Teresa Torres in *Continuous Discovery Habits* (2021), ch. 6–7. The OST is the kit's Discovery-phase handover artifact: every OST has one Outcome at its root and (when ready to hand off to Validation) one Opportunity named in the OST's `chosen_opportunity:` field (with `id:` and `rationale:` sub-fields), per `docs/HANDOVERS.md` §"Handover 2". The validator skill at `.claude/skills/ost-validator/SKILL.md` enforces the tree's structural rules; the template at `templates/ost.md` provides the empty shape.

The OST exists because teams default to two failure modes when planning what to build: (a) jumping from a business goal straight to a feature list, skipping the customer-pain layer entirely; and (b) treating "we should do X" as if X were already validated when no test has been run. The tree resists both. The Opportunity layer forces a customer-pain bridge between the Outcome and any proposed Solution; the Assumption Test layer forces a falsifier under every Solution before it becomes a commitment.

This document is the framework reference — the *what* and *why*. Operational mechanics (how the kit generates, updates, and audits OSTs) live in the linked skills and commands; the structural validator is the single source of truth for the tree-shape rules.

## The four node types

Every OST is built from exactly four node types. Mixing them up — or skipping a layer — is the most common failure mode.

- **Outcome** — the root. The single business or customer metric this tree is moving (e.g., "weekly active analysts producing a saved query"). Maps to the kit's ontology Domain D type *Outcome*. There is exactly one Outcome per tree. Torres (2021, ch. 4) is explicit that the Outcome must be a *product* outcome the team can directly influence, not a business outcome two layers removed.

- **Opportunity** — a customer pain, desire, or aspiration sourced from a specific research moment. Example: "analysts redo the same join logic across notebooks because they can't share saved fragments." Maps to ontology Domain C types *Problem*, *Pain Point*, *Need*, or *Job to be Done*. Opportunities are stated in the customer's voice; if the wording reads like a feature request, you have a Solution masquerading as an Opportunity.

- **Solution** — a specific intervention proposed to address one Opportunity. Example: "saved-query snippets pinned to the workspace sidebar." Maps to ontology Domain E type *Feature* or *Capability*. Multiple Solutions per Opportunity is expected and healthy — the OST is the place where divergent thinking lives before convergent commitment.

- **Assumption Test** — the cheapest test that could falsify a specific assumption underlying one Solution. Example, tied to the Solution above: "do analysts adopt the saved-query snippet feature in their first session? Threshold: ≥40% of new analysts open the snippet panel within 7 days of first login." Maps to ontology Domain C type *Experiment*. Lives at the leaves; never at intermediate layers. The pre-declared threshold is the discipline that distinguishes a real test from a vibe-check.

Each node-type names a different thing. Treating an Opportunity as a Solution (or vice versa) collapses the tree. The four examples above — "weekly active analysts producing a saved query" → "analysts redo the same join logic across notebooks" → "saved-query snippets pinned to the workspace sidebar" → "≥40% open the snippet panel within 7 days" — form one end-to-end chain at each layer, and the chain is what makes the tree falsifiable rather than aspirational.

A Solution with no Assumption Test beneath it is a commitment without a falsifier; an Assumption Test without a named threshold (as Torres argues in ch. 7) is not a test, it is an observation. The kit's `assumption-threshold-lock` hook enforces the threshold rule at write time so the discipline doesn't depend on memory.

Two finer distinctions worth naming up front:

- An Opportunity is **not** the inverse of a Solution. "Users can't share snippets" is a Solution-shaped negation; "analysts redo the same join logic across notebooks because they have no way to share saved fragments" names the customer behavior and consequence. The latter survives the validator; the former gets flagged as Solution-leakage into the Opportunity layer.

- An Assumption Test is **not** a usability test or a discovery interview. Usability tests answer "can users find/use this?"; discovery interviews answer "what do users do today?". An Assumption Test answers "if we ship this Solution, will the metric the Outcome names move past threshold T by date D?" — the falsification criterion is pre-declared and binary.

## Source opportunities

Every Opportunity must trace to a specific customer research moment — an interview snapshot, a quote, an observed behavior, or a support thread linked by ID. Opportunities without a named source are **conjecture** and the validator skill flags them. This is the rule that prevents the OST from becoming a planning document instead of a research artifact.

The snapshot is the bridge: `context/frameworks/interview-snapshot.md` defines the artifact that captures one interview; the OST consumes snapshots and aggregates their pain points into Opportunities. The validator skill flags Opportunities with zero `evidence_basis:` entries as conjecture; one entry is the minimum; the richer the evidence chain, the more defensible the prioritization decision downstream — both for the team picking which Opportunity to pursue and for the reviewer auditing the choice later.

The `evidence_basis:` field on each Opportunity in the kit's ontology (see `docs/CONVENTIONS.md`) is where the source-trace lives in machine-readable form. Each entry is an ID — interview snapshot, support thread, analytics cohort, or observed-behavior log — that a human can open and read. The IDs let `/audit-discovery-coherence` and the `ost-validator` skill traverse from Opportunity back to raw evidence without re-interviewing the team.

Sourcing applies one direction only: every Opportunity must trace back to evidence, but not every interview snapshot needs to surface as an Opportunity. Most snapshots produce signal that confirms existing nodes; only the snapshots that introduce a *new* customer pain become new Opportunity nodes. Torres (2021, ch. 7) calls this aggregation — the tree is the team's running synthesis of what they've heard, not a transcript log.

Evidence quality is a spectrum, and the validator does not yet distinguish strong from weak evidence — it only counts entries. Reviewers should still apply judgment:

- A single observed behavior from a paid customer in the target segment outweighs three secondhand quotes relayed by sales.
- Analytics cohorts grounded in product instrumentation outweigh inferred patterns from support-ticket text alone.
- Quotes from non-target users are noise; if an Opportunity's `evidence_basis:` consists entirely of off-segment quotes, the validator passes but the human reviewer should reject.

## Tree-shape rules

The OST is a directed acyclic graph with strict layering. The validator at `.claude/skills/ost-validator/SKILL.md` checks all of these mechanically:

- **One Outcome at the root.** A tree with two Outcomes is two trees. If the team finds itself wanting two roots, the right move is to split the artifact into two OSTs and let each have its own `chosen_opportunity:` downstream.

- **Opportunities are additive children.** As you learn, the tree branches **widen**, not narrow. The wrong instinct ("we have too many opportunities — let's prune") usually means: the tree is doing its job; pick one Opportunity to pursue, leave the others as inventory.

- **Solutions are children of one Opportunity each.** A Solution sitting under two Opportunities is a smell — either the two Opportunities are actually one (rebracket), or the Solution is really two Solutions (split). The validator surfaces this as a structural error and refuses to persist the tree until it's resolved.

- **An Assumption Test is a child of one Solution.** Tests at intermediate layers indicate you're trying to validate an Opportunity directly; that's a category error — Opportunities are evidence-grounded, not test-grounded. You can't "test" whether a pain is real; you can only test whether a proposed Solution moves the metric the Outcome names.

- **Opportunities may decompose into sub-Opportunities.** The four-level skeleton (Outcome → Opportunity → Solution → Assumption Test) is the *minimum* depth; useful trees often have Opportunity → sub-Opportunity → … chains before reaching Solutions. Decomposition is the mechanism that produces the varying-depth trees called out in `## Common failure modes` (a flat tree has no sub-Opportunities; that's the smell). Decompose an Opportunity into sub-Opportunities when the parent Opportunity contains internally-distinct customer pains that warrant different Solutions; branch sideways (more sibling Opportunities under the same Outcome) when the team is broadening exploration of what could move the Outcome. Decomposition narrows the question; sideways branching widens it. Both are legitimate moves; mixing them up produces trees that feel busy but aren't actually informative.

- **The chosen Opportunity is named, not implied.** When the OST is ready to hand off to Validation, exactly one Opportunity is recorded in the `chosen_opportunity:` field of the OST's frontmatter, with `id:` (the Opportunity's stable identifier) and `rationale:` (one paragraph naming why this one, not the others). Implicit choice — "obviously we'll pursue this one" — is how teams skip the Validation phase by accident.

## Common failure modes

The failure modes below are listed in roughly the order teams encounter them. Each names the recovery move the team should make when the validator (or a human reviewer) catches it. None are catastrophic on their own; what's catastrophic is letting them accumulate silently until the OST no longer reflects what the team has actually learned.

- **The "solution tree" anti-pattern** — skipping the Opportunity layer entirely and jumping from Outcome straight to Solution. Without the Opportunity, the Solution has no customer source and the Assumption Test underneath has no hypothesis to falsify. Recovery: for each orphan Solution, ask "what customer evidence motivated this?" and either insert the Opportunity or delete the Solution.

- **The "everything is an opportunity" tree** — every PM hunch gets a node; no real customer source backs any of them. The tree looks rich; the evidence is aspirational. Recovery: run the validator's `evidence_basis:` check; demote unsourced nodes to a `parking-lot.md` until evidence appears.

- **The "single-path" tree** — only one Opportunity per Outcome. Convergent thinking too early; the tree never had a chance to surface alternatives. Recovery: before naming `chosen_opportunity:`, require the tree to surface at least three sibling Opportunities so the choice is a *comparison*, not a default.

- **The "flat tree"** — all Opportunities at the same depth, no sub-Opportunities. Makes prioritization impossible because every node looks comparable; useful trees have varying depth as some Opportunities decompose further than others.

- **The "frozen tree"** — an OST that has not been updated in weeks or months while the team continues interviewing. Continuous discovery's whole premise is that the tree moves; a frozen tree means either the discovery work stopped or the integration into the tree stopped. The kit's `cadence-nudge` hook (F2.5, shipped) surfaces this drift at session start; see also `context/frameworks/continuous-discovery.md`.

- **The "test-as-launch" failure** — running the Assumption Test by shipping the full Solution to all users and watching what happens. The Assumption Test is meant to falsify cheaply, *before* the build commitment; using production launch as the test conflates discovery with delivery and means a falsified assumption costs a quarter of engineering, not a week of prototype. Recovery: for each Solution at risk, name the cheapest test that could plausibly falsify the underlying assumption — paper prototype, concierge experiment, smoke test, fake-door — and run that before any code is written.

- **The "premature commitment" failure** — naming `chosen_opportunity:` before the tree has surfaced sibling Opportunities to compare against. The OST is supposed to make the *choice* legible, not rubber-stamp a prior commitment. Recovery: leave `chosen_opportunity:` unset until at least three sibling Opportunities are present and the team has explicitly considered each.

## How the kit uses this framework

The OST sits at the center of the Discovery phase. Every component below is built around the assumption that an OST exists, is current, and obeys the tree-shape rules above. If any of those preconditions fail, the corresponding downstream artifact (assumption map, learning, vision) cannot be produced — the phase guards in `scripts/` enforce the precedence at write time, so the framework's rules cash out as filesystem-level checks rather than aspirational discipline.

- `.claude/skills/ost-validator/SKILL.md` (shipped) — the validator that enforces the tree-shape rules above; runs in a validate-then-repair loop on every OST change set before the artifact is persisted. The validator emits a structured diff (added/modified/removed nodes) so changes are auditable instead of silent overwrites.

- `templates/ost.md` (F3.2, shipped) — the empty-tree template the validator expects. The template declares the universal-metadata frontmatter and the four-section body skeleton (one H2 per node type); deviating from this shape makes the validator fail closed.

- `/generate-ost` (planned — ROADMAP P2.7) and `/update-ost` (planned — ROADMAP P2.9) — generate the first-pass tree from snapshots and integrate new interview content, respectively. Both are change-set producers; both go through the validator before persistence.

- `/audit-discovery-coherence` (planned — ROADMAP P2.11) — flags OSTs without parent intents, OSTs whose `chosen_opportunity:` does not match any Opportunity node in the tree body, and OSTs whose Outcome does not align with the parent strategic intent's guiding policy.

- `discovery-coach` agent (planned — ROADMAP P2.13) — auto-invokes when the team is stuck on an Opportunity (no Solutions named, or no Assumption Tests under the named Solutions) and prompts the team toward divergent generation rather than convergent commitment.

- The Discovery → Validation handover contract in `docs/HANDOVERS.md` §"Handover 2": the OST with a `chosen_opportunity:` (carrying `id:` and `rationale:`) is the artifact that crosses the phase boundary. Without that field, the phase-guard hook blocks creation of a downstream `validation/assumption-maps/<slug>.md` — the kit refuses to start Validation without an explicit choice.

- `cadence-nudge` hook (F2.5, shipped) — surfaces a frozen-tree warning at session start when the OST has not been updated for longer than the configured cadence interval (default: 14 days). The nudge is informational; it never blocks. The signal exists because frozen trees fail silently — the team keeps working, but the artifact no longer reflects reality, and the next handover to Validation will be based on stale evidence.

## References

- Torres, T. (2021). *Continuous Discovery Habits: Discover Products that Create Customer Value and Business Value*. Product Talk LLC. Chapters 6 ("The Opportunity Space") and 7 ("Mapping the Opportunity Space"). The canonical source for the four node types and the tree-shape rules. Chapter 4 ("The Outcome Mindset") underwrites the rule that the root must be a product outcome the team can influence directly.

- `context/frameworks/continuous-discovery.md` — the weekly habit that produces the snapshots the OST consumes. Without the weekly cadence, the OST drifts into the frozen-tree failure mode within a quarter.

- `context/frameworks/interview-snapshot.md` — the per-interview artifact that sources each Opportunity. The `evidence_basis:` IDs on Opportunity nodes point to snapshot files of this shape.

- `templates/ost.md` — the kit's OST template. Empty-tree shape the `/generate-ost` and `/update-ost` commands populate.

- `.claude/skills/ost-validator/SKILL.md` — the kit's mechanical validator. Enforces tree-shape rules and emits structured change-set diffs.

- `docs/HANDOVERS.md` §"Handover 2" — the Discovery → Validation handover contract that names the OST + `chosen_opportunity:` as the boundary artifact.
