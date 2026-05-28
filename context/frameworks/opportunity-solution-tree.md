# Opportunity Solution Tree

> A visual artifact for connecting a desired Outcome to the Opportunities, Solutions, and Assumption Tests that pursue it. Defined by Teresa Torres in *Continuous Discovery Habits* (2021), ch. 6–7. The OST is the kit's Discovery-phase handover artifact: every OST has one Outcome at its root and (when ready to hand off to Validation) one Opportunity flagged `chosen: true`. The validator skill at `.claude/skills/ost-validator/SKILL.md` enforces the tree's structural rules; the template at `templates/ost.md` provides the empty shape.

## The four node types

Every OST is built from exactly four node types. Mixing them up — or skipping a layer — is the most common failure mode.

- **Outcome** — the root. The single business or customer metric this tree is moving (e.g., "weekly active analysts producing a saved query"). Maps to the kit's ontology Domain D type *Outcome*. There is exactly one Outcome per tree.
- **Opportunity** — a customer pain, desire, or aspiration sourced from a specific research moment. Example: "analysts redo the same join logic across notebooks because they can't share saved fragments." Maps to ontology Domain C types *Problem*, *Pain Point*, *Need*, or *Job to be Done*.
- **Solution** — a specific intervention proposed to address one Opportunity. Example: "saved-query snippets pinned to the workspace sidebar." Maps to ontology Domain E type *Feature* or *Capability*.
- **Assumption Test** — the cheapest test that could falsify a specific assumption underlying one Solution. Maps to ontology Domain C type *Experiment*. Lives at the leaves; never at intermediate layers.

Each node-type names a different thing. Treating an Opportunity as a Solution (or vice versa) collapses the tree.

## Source opportunities

Every Opportunity must trace to a specific customer research moment — an interview snapshot, a quote, an observed behavior, or a support thread linked by ID. Opportunities without a named source are **conjecture** and the validator skill flags them.

The snapshot is the bridge: `context/frameworks/interview-snapshot.md` defines the artifact that captures one interview; the OST consumes snapshots and aggregates their pain points into Opportunities. An Opportunity citing three snapshots is stronger than one citing one; an Opportunity citing zero snapshots is filler.

The `evidence_basis:` field on each Opportunity in the kit's ontology (see `docs/CONVENTIONS.md`) is where the source-trace lives in machine-readable form.

## Tree-shape rules

The OST is a directed acyclic graph with strict layering. The validator at `.claude/skills/ost-validator/SKILL.md` checks all of these mechanically:

- **One Outcome at the root.** A tree with two Outcomes is two trees.
- **Opportunities are additive children.** As you learn, the tree branches **widen**, not narrow. The wrong instinct ("we have too many opportunities — let's prune") usually means: the tree is doing its job; pick one Opportunity to pursue, leave the others as inventory.
- **Solutions are children of one Opportunity each.** A Solution sitting under two Opportunities is a smell — either the two Opportunities are actually one (rebracket), or the Solution is really two Solutions (split).
- **An Assumption Test is a child of one Solution.** Tests at intermediate layers indicate you're trying to validate an Opportunity directly; that's a category error — Opportunities are evidence-grounded, not test-grounded.

## Common failure modes

- **The "solution tree" anti-pattern** — skipping the Opportunity layer entirely and jumping from Outcome straight to Solution. Without the Opportunity, the Solution has no customer source and the Assumption Test underneath has no hypothesis to falsify.
- **The "everything is an opportunity" tree** — every PM hunch gets a node; no real customer source backs any of them. The tree looks rich; the evidence is aspirational.
- **The "single-path" tree** — only one Opportunity per Outcome. Convergent thinking too early; the tree never had a chance to surface alternatives.
- **The "flat tree"** — all Opportunities at the same depth, no sub-Opportunities. Makes prioritization impossible because every node looks comparable; useful trees have varying depth as some Opportunities decompose further than others.

## How the kit uses this framework

- `.claude/skills/ost-validator/SKILL.md` (shipped) — the validator that enforces the tree-shape rules above; runs in a validate-then-repair loop on every OST change set before the artifact is persisted.
- `templates/ost.md` (F3.2, shipped) — the empty-tree template the validator expects.
- `/generate-ost` (planned — ROADMAP P2.7) and `/update-ost` (planned — ROADMAP P2.9) — generate the first-pass tree from snapshots and integrate new interview content, respectively.
- `/audit-discovery-coherence` (planned — ROADMAP P2.11) — flags OSTs without parent intents.
- `discovery-coach` agent (planned — ROADMAP P2.13) — auto-invokes when the team is stuck on an Opportunity.
- The Discovery → Validation handover contract in `docs/HANDOVERS.md` §"Handover 2": the OST with `chosen: true` on one Opportunity is the artifact that crosses the phase boundary.

## References

- Torres, T. (2021). *Continuous Discovery Habits: Discover Products that Create Customer Value and Business Value*. Product Talk LLC. Chapters 6 ("The Opportunity Space") and 7 ("Mapping the Opportunity Space"). The canonical source for the four node types and the tree-shape rules.
- `context/frameworks/continuous-discovery.md` — the weekly habit that produces the snapshots the OST consumes.
- `context/frameworks/interview-snapshot.md` — the per-interview artifact that sources each Opportunity.
- `templates/ost.md` — the kit's OST template.
- `.claude/skills/ost-validator/SKILL.md` — the kit's mechanical validator.
