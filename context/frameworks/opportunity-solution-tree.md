# Opportunity Solution Tree

> A visual artifact for connecting a desired Outcome to the Opportunities, Solutions, and Assumption Tests that pursue it. Defined by Teresa Torres in *Continuous Discovery Habits* (2021), ch. 6–7. The OST is the kit's Discovery-phase handover artifact: every OST has one Outcome at its root and (when ready to hand off to Validation) one Opportunity named in the OST's `chosen_opportunity:` field (with `id:` and `rationale:` sub-fields), per `docs/HANDOVERS.md` §"Handover 2". The validator skill at `.claude/skills/ost-validator/SKILL.md` enforces the tree's structural rules; the template at `templates/ost.md` provides the empty shape.

## The four node types

Every OST is built from exactly four node types. Mixing them up — or skipping a layer — is the most common failure mode.

- **Outcome** — the root. The single business or customer metric this tree is moving (e.g., "weekly active analysts producing a saved query"). Maps to the kit's ontology Domain D type *Outcome*. There is exactly one Outcome per tree. Torres (2021, ch. 4) is explicit that the Outcome must be a *product* outcome the team can directly influence, not a business outcome two layers removed.

- **Opportunity** — a customer pain, desire, or aspiration sourced from a specific research moment. Example: "analysts redo the same join logic across notebooks because they can't share saved fragments." Maps to ontology Domain C types *Problem*, *Pain Point*, *Need*, or *Job to be Done*. Opportunities are stated in the customer's voice; if the wording reads like a feature request, you have a Solution masquerading as an Opportunity.

- **Solution** — a specific intervention proposed to address one Opportunity. Example: "saved-query snippets pinned to the workspace sidebar." Maps to ontology Domain E type *Feature* or *Capability*. Multiple Solutions per Opportunity is expected and healthy — the OST is the place where divergent thinking lives before convergent commitment.

- **Assumption Test** — the cheapest test that could falsify a specific assumption underlying one Solution. Example, tied to the Solution above: "do analysts adopt the saved-query snippet feature in their first session? Threshold: ≥40% of new analysts open the snippet panel within 7 days of first login." Maps to ontology Domain C type *Experiment*. Lives at the leaves; never at intermediate layers. The pre-declared threshold is the discipline that distinguishes a real test from a vibe-check.

Each node-type names a different thing. Treating an Opportunity as a Solution (or vice versa) collapses the tree. The four examples above — "weekly active analysts producing a saved query" → "analysts redo the same join logic across notebooks" → "saved-query snippets pinned to the workspace sidebar" → "≥40% open the snippet panel within 7 days" — form one end-to-end chain at each layer, and the chain is what makes the tree falsifiable rather than aspirational.

A Solution with no Assumption Test beneath it is a commitment without a falsifier; an Assumption Test without a named threshold (as Torres argues in ch. 7) is not a test, it is an observation. The kit's `assumption-threshold-lock` hook enforces the threshold rule at write time so the discipline doesn't depend on memory.

## Source opportunities

Every Opportunity must trace to a specific customer research moment — an interview snapshot, a quote, an observed behavior, or a support thread linked by ID. Opportunities without a named source are **conjecture** and the validator skill flags them.

The snapshot is the bridge: `context/frameworks/interview-snapshot.md` defines the artifact that captures one interview; the OST consumes snapshots and aggregates their pain points into Opportunities. The validator skill flags Opportunities with zero `evidence_basis:` entries as conjecture; one entry is the minimum; the richer the evidence chain, the more defensible the prioritization decision downstream — both for the team picking which Opportunity to pursue and for the reviewer auditing the choice later.

The `evidence_basis:` field on each Opportunity in the kit's ontology (see `docs/CONVENTIONS.md`) is where the source-trace lives in machine-readable form. Each entry is an ID — interview snapshot, support thread, analytics cohort, or observed-behavior log — that a human can open and read. The IDs let `/audit-discovery-coherence` and the `ost-validator` skill traverse from Opportunity back to raw evidence without re-interviewing the team.

Sourcing applies one direction only: every Opportunity must trace back to evidence, but not every interview snapshot needs to surface as an Opportunity. Most snapshots produce signal that confirms existing nodes; only the snapshots that introduce a *new* customer pain become new Opportunity nodes. Torres (2021, ch. 7) calls this aggregation — the tree is the team's running synthesis of what they've heard, not a transcript log.

## Tree-shape rules

The OST is a directed acyclic graph with strict layering. The validator at `.claude/skills/ost-validator/SKILL.md` checks all of these mechanically:

- **One Outcome at the root.** A tree with two Outcomes is two trees. If the team finds itself wanting two roots, the right move is to split the artifact into two OSTs and let each have its own `chosen_opportunity:` downstream.

- **Opportunities are additive children.** As you learn, the tree branches **widen**, not narrow. The wrong instinct ("we have too many opportunities — let's prune") usually means: the tree is doing its job; pick one Opportunity to pursue, leave the others as inventory.

- **Solutions are children of one Opportunity each.** A Solution sitting under two Opportunities is a smell — either the two Opportunities are actually one (rebracket), or the Solution is really two Solutions (split). The validator surfaces this as a structural error and refuses to persist the tree until it's resolved.

- **An Assumption Test is a child of one Solution.** Tests at intermediate layers indicate you're trying to validate an Opportunity directly; that's a category error — Opportunities are evidence-grounded, not test-grounded. You can't "test" whether a pain is real; you can only test whether a proposed Solution moves the metric the Outcome names.

- **Opportunities may decompose into sub-Opportunities.** The four-level skeleton (Outcome → Opportunity → Solution → Assumption Test) is the *minimum* depth; useful trees often have Opportunity → sub-Opportunity → … chains before reaching Solutions. Decomposition is the mechanism that produces the varying-depth trees called out in `## Common failure modes` (a flat tree has no sub-Opportunities; that's the smell). Decompose an Opportunity into sub-Opportunities when the parent Opportunity contains internally-distinct customer pains that warrant different Solutions; branch sideways (more sibling Opportunities under the same Outcome) when the team is broadening exploration of what could move the Outcome. Decomposition narrows the question; sideways branching widens it. Both are legitimate moves; mixing them up produces trees that feel busy but aren't actually informative.

- **The chosen Opportunity is named, not implied.** When the OST is ready to hand off to Validation, exactly one Opportunity is recorded in the `chosen_opportunity:` field of the OST's frontmatter, with `id:` (the Opportunity's stable identifier) and `rationale:` (one paragraph naming why this one, not the others). Implicit choice — "obviously we'll pursue this one" — is how teams skip the Validation phase by accident.

## Common failure modes

- **The "solution tree" anti-pattern** — skipping the Opportunity layer entirely and jumping from Outcome straight to Solution. Without the Opportunity, the Solution has no customer source and the Assumption Test underneath has no hypothesis to falsify.
- **The "everything is an opportunity" tree** — every PM hunch gets a node; no real customer source backs any of them. The tree looks rich; the evidence is aspirational.
- **The "single-path" tree** — only one Opportunity per Outcome. Convergent thinking too early; the tree never had a chance to surface alternatives.
- **The "flat tree"** — all Opportunities at the same depth, no sub-Opportunities. Makes prioritization impossible because every node looks comparable; useful trees have varying depth as some Opportunities decompose further than others.
- **The "frozen tree"** — an OST that has not been updated in weeks or months while the team continues interviewing. Continuous discovery's whole premise is that the tree moves; a frozen tree means either the discovery work stopped or the integration into the tree stopped. The kit's `cadence-nudge` hook (F2.5, shipped) surfaces this drift at session start; see also `context/frameworks/continuous-discovery.md`.

## How the kit uses this framework

- `.claude/skills/ost-validator/SKILL.md` (shipped) — the validator that enforces the tree-shape rules above; runs in a validate-then-repair loop on every OST change set before the artifact is persisted.
- `templates/ost.md` (F3.2, shipped) — the empty-tree template the validator expects.
- `/generate-ost` (planned — ROADMAP P2.7) and `/update-ost` (planned — ROADMAP P2.9) — generate the first-pass tree from snapshots and integrate new interview content, respectively.
- `/audit-discovery-coherence` (planned — ROADMAP P2.11) — flags OSTs without parent intents.
- `discovery-coach` agent (planned — ROADMAP P2.13) — auto-invokes when the team is stuck on an Opportunity.
- The Discovery → Validation handover contract in `docs/HANDOVERS.md` §"Handover 2": the OST with a `chosen_opportunity:` (carrying `id:` and `rationale:`) is the artifact that crosses the phase boundary.

## References

- Torres, T. (2021). *Continuous Discovery Habits: Discover Products that Create Customer Value and Business Value*. Product Talk LLC. Chapters 6 ("The Opportunity Space") and 7 ("Mapping the Opportunity Space"). The canonical source for the four node types and the tree-shape rules.
- `context/frameworks/continuous-discovery.md` — the weekly habit that produces the snapshots the OST consumes.
- `context/frameworks/interview-snapshot.md` — the per-interview artifact that sources each Opportunity.
- `templates/ost.md` — the kit's OST template.
- `.claude/skills/ost-validator/SKILL.md` — the kit's mechanical validator.
