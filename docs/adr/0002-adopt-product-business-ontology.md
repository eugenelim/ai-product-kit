# 0002 — Adopt the product/business knowledge ontology as the kit's type system

* Status: accepted
* Deciders: kit author
* Date: 2026-05-20
* Supersedes: none

## Context and Problem Statement

v2 of the kit organized artifacts by phase but used loose, ad-hoc terminology within phases. The same concept appeared under different names in different files — "the chosen opportunity" in one place, "the bet" in another, "the validated learning" in a third. There was no shared type vocabulary across discovery, validation, and delivery, so:

1. **Traceability was implicit.** Requirements traced upward via prose, not typed links. A requirement could silently lose its connection to the problem that justified it.
2. **Object identity was vague.** "Capability" and "Feature" and "Requirement" were used interchangeably in different artifacts.
3. **The Human-vs-AI ownership model was missing entirely.** v2 had hooks that enforced phase-handover integrity but didn't capture the orthogonal question of *which decisions a human must own personally*.
4. **The engineering handoff was a folder, not an artifact.** v2's `delivery/specs/` produced specs but didn't bundle the surrounding business context engineering needs (workflows, business rules, compliance constraints, success metrics, open questions, decision log).

The [product and business knowledge ontology](../inspiration/product_business_knowledge_ontology_agent_handoff.md) provides a canonical type system that solves all four problems.

## Decision Drivers

- **Shared vocabulary across all phases.** Discovery, Validation, and Delivery need to refer to the same object by the same name.
- **Mechanical traceability.** Audits should be able to walk the chain Requirement → Capability → Problem → Evidence → KPI → Outcome and flag breaks.
- **Human-vs-AI accountability.** Every artifact should declare what decisions a human must own personally, and what AI was used for.
- **Engineering handoff as a first-class artifact.** The kit should produce a complete, validated handoff packet — not a folder of specs that engineering must re-assemble.

## Considered Options

### Option A — Build a kit-specific minimal type system

A short list (~15 types) covering the kit's core artifacts. Pro: low overhead, matches existing folders. Con: doesn't solve the cross-phase consistency problem; doesn't cover the Commercial Model or Operational Readiness domains that the kit's downstream consumers (sales, support, legal) need.

### Option B — Adopt the eight-domain ontology wholesale

74 atomic object types across the eight domains (an earlier count of "~80" was an approximation; the actual count after carefully reading the source is 74; the kit's Domain I extension adds 8 composite types for a documented total of 82). Plus the universal metadata schema, the traceability rules, the lifecycle states, and the human-vs-AI ownership model. Pro: complete; the source artifact is the most thoroughly structured PM-side ontology the author has found, though it is a structured reference document rather than empirically validated across organizations — "battle-tested" is therefore the wrong claim; "thorough" is the right one. Covers domains the kit was previously silent on (Commercial Model, Operational Readiness). Con: meaningful upfront overhead — populating the required frontmatter adds the 3 universally-required fields plus a per-artifact set of conditionally-required fields (see CONVENTIONS.md universal schema for the exact list). Some types (Cost Driver, Unit Economics Assumption, SLA) are unfamiliar in PM-centric vocabularies; risk of "type proliferation" if used dogmatically.

### Option C — Adopt the ontology's structure but a curated subset of types

The eight domains stay; only the most-used types in each domain are first-class. Add types on demand via RFC. Pro: balances completeness against overhead. Con: requires drawing an arbitrary line; defeats the value of having a *complete* type system.

### Option D — Reference the ontology as a framework but don't enforce it

Add `context/frameworks/ontology.md` for reference; let Claude use it when relevant; don't require artifacts to declare `object_type:`. Pro: minimal disruption. Con: gives up the audit-chain benefits.

## Decision Outcome

**Option B — adopt the ontology wholesale, with two named extensions.**

The eight domains, all atomic object types from the source ontology, the universal metadata schema, the traceability rules, the lifecycle states, and the Human-vs-AI ownership model are all adopted as canonical. The kit additionally introduces two named extensions to make the adoption work in practice:

- **Domain I (kit-composite handover artifacts).** The source ontology defines 74 atomic types across Domains A–H. The kit's phase model requires composite types that wrap and reference those atomics (Strategic Intent, Opportunity Solution Tree, Validation Learning Memo, Vision, Landing Report, Assumption Map, Audit Report, plus `Opportunity` as a Domain C-style node used inside OSTs). These eight composite types are documented as Domain I in `context/frameworks/ontology.md` and are accepted by `tools/lint-frontmatter.py` once added to the type-table parser's scan.
- **Kit-build lifecycle states.** The source ontology's product-artifact lifecycle (`Draft → ... → Deprecated`) does not cover kit-internal components (specs, plans, skills, agents). The kit adds `Implementing`, `Shipped`, `Frozen` to `LIFECYCLE_STATES` in the linter and documents the two parallel tracks in `docs/CONVENTIONS.md` §"Lifecycle states."

### What gets adopted

1. **`context/frameworks/ontology.md`** — the canonical working summary (74 atomic + 8 composite = 82 documented types), pulled into context on demand
2. **`docs/CONVENTIONS.md`** — the universal metadata schema as the kit-wide standard for every artifact's frontmatter
3. **`docs/HUMAN-AI-OWNERSHIP.md`** — the Human-vs-AI responsibility model with per-phase ownership maps
4. **`docs/HANDOVERS.md`** — each handover artifact's required frontmatter declares which ontology types its content represents and which traceability links are required
5. **`delivery/handoff-packets/`** — new top-level folder for engineering-handoff packets; each is a folder of 23 files mapping to the ontology's §28 content. The §41 25-item checklist runs against that content (the file-vs-item count distinction is documented in `docs/HANDOVERS.md` Handover 6)
6. **`/audit-completeness`** — runs the ontology's 25-item pre-engineering-handoff checklist (shipped as prose procedure; runnable script planned ROADMAP F1.5)
7. **`/audit-traceability`** — enforces the seven traceability rules (shipped as prose; runnable script planned ROADMAP F1.4)
8. **`ontology-classifier` skill** *(planned — ROADMAP F1.3)* — extracts typed objects from unstructured input and surfaces missing fields. Until shipped, classification is done by hand against `context/frameworks/ontology.md`.

### What's explicitly not adopted

- The source ontology's §30 ("Recommended Governance Roles") taxonomy — not applicable; the kit defers role assignments to the human-vs-AI ownership model (Domain I composite types declare `human_owned_decisions:` per artifact, no separate role hierarchy).
- The source ontology's §34 ("Practical Operating Model") narrative — overlaps and lightly conflicts with the kit's own four-phase operating model in `docs/PHASE-GUIDE.md`. The kit's phases win.
- The source ontology's §35 ("Recommended Final Artifact Structure") template — the kit's per-phase handover-artifact contracts in `docs/HANDOVERS.md` are the operative structure, not the source's recommended template.
- The source's agent-guidance prose (the source itself was written as an LLM context document; the kit's AGENTS.md and skills supersede it for agent guidance).
- Type-extension via inline declaration. The kit requires an RFC for new types (with the `<type> | Adapted` linter escape hatch for one-off cases — see `context/frameworks/ontology.md` "When the ontology is wrong" section).

### Consequences

**Positive:**
- Shared vocabulary across all phases — Capability means the same thing in Discovery, Validation, and Delivery
- Audit chains are mechanical — `/audit-traceability` and `/audit-completeness` can walk the typed graph
- Human-vs-AI accountability is structural — every artifact declares it in frontmatter
- Engineering handoff is a real, validated deliverable — engineering inherits structure, not prose
- Cross-domain coverage — the kit now has first-class types for Commercial Model and Operational Readiness, not just discovery/delivery

**Negative / accepted tradeoffs:**
- Upfront overhead — populating ontology fields requires more frontmatter
- Type rigidity — some judgment calls fit awkwardly into the 80 types (the kit handles this via `object_type: <type> | Adapted` and an RFC for new types)
- Risk of type theater — if adopters fill in `object_type:` without classifying carefully, the chain looks valid but isn't. Mitigated by `ontology-classifier` skill and the `/audit-traceability` "weak chain" detection

**Neutral:**
- v2-era artifacts can be migrated incrementally; old artifacts default to `object_type: Initiative | Adapted` (using the canonical `| Adapted` suffix the linter recognizes) until reclassified. An earlier draft of this ADR used `| Legacy` — the canonical suffix is `| Adapted` per `lint-frontmatter.py` and `context/frameworks/ontology.md`.

### Process for adding a new type

When a new type is needed (the linter rejects an `object_type:` and the `| Adapted` escape doesn't fit):

1. Open an RFC in `docs/rfc/` proposing the new type. Specify which Domain (A–I) it belongs to, its definition, and the artifacts that will use it.
2. If accepted, the RFC produces an edit to `context/frameworks/ontology.md` adding the type to the appropriate Domain table. The linter's `load_ontology_types()` will then accept it on next run.
3. Document the addition in the next ADR (this one's supersessor) so the type vocabulary's growth is traceable.

`context/frameworks/ontology.md` is the canonical type registry; the inspiration source doc (`docs/inspiration/product_business_knowledge_ontology_agent_handoff.md`) is reference material that does not change. Once an RFC adds a type, the working summary is authoritative and the inspiration doc is historical.

## Alternatives Considered (in detail)

### Option A — Build a kit-specific minimal type system (~15 types) (rejected)

**Failure on cross-phase consistency:** the kit's primary value claim is that an artifact in Discovery refers to the same object the Validation team will pick up. A 15-type system would force one of two failures: (1) cover only the highest-frequency types and leave Discovery↔Validation handoffs to invent names for the un-covered objects (re-creating the v2 problem), or (2) collapse fine distinctions (Capability vs Feature vs Requirement) into single types, which destroys the audit chain's ability to walk traceability.

**Failure on commercial / operational coverage:** the kit's downstream consumers include sales (battlecards), support (training-need detection), and legal/compliance (policy-rule enforcement). A 15-type minimum cannot cover those domains without re-inventing them. Better to adopt the ontology that already covers them.

### Option C — Adopt the ontology's structure but a curated subset of types (rejected)

**Failure on completeness:** the choice of which types are "core" vs "exotic" is the kit's most consequential type-system decision. Drawing it as a curation removes the option of using the full vocabulary when the situation calls for it (Operational Readiness: which subset is core? Customer Communication is exotic until a kit user needs to track marketing artifacts).

**Failure on extension protocol:** if some types are first-class and others require RFCs, the line is arbitrary and litigates. Either all 74 atomic types are first-class (Option B) or none are (Option D).

### Option D — Reference the ontology as a framework but don't enforce it (rejected)

**Failure on audit chain:** the whole point of `/audit-traceability` and `/audit-completeness` is to walk a typed graph. Without enforced `object_type:` declarations, the audits can't function — they degrade to prose review. Drift between the framework reference and actual artifacts becomes invisible.

**Failure on agent classification:** the `ontology-classifier` skill (planned F1.3) extracts typed objects from unstructured input. Without enforced types, there's nothing for it to classify against — the skill's output becomes "here's what this looks like to me," not "here is the classification per the kit's type system." That's a meaningful loss.

### Option B wins because

Cross-phase consistency, mechanical audit, human-vs-AI accountability, and engineering-handoff-as-artifact are all second-order benefits of having a *complete and enforced* type system. Options A, C, and D each sacrifice one or more of these. The upfront overhead of adopting 74 + 8 = 82 types is real but bounded — and the kit's `ontology-classifier` skill (when it ships) is designed to discharge that overhead at usage time.

## Links

* parent_intent: — (kit-architecture decision)
* affected_artifacts: docs/CONVENTIONS.md, docs/HUMAN-AI-OWNERSHIP.md, docs/HANDOVERS.md, docs/INVENTORY.md, context/frameworks/ontology.md, delivery/handoff-packets/, .claude/commands/audit-completeness.md, .claude/commands/audit-traceability.md
* related_to: ADR 0001 (the agent-ready-repo adoption — these two decisions reinforce each other)
* references:
  * [`docs/inspiration/product_business_knowledge_ontology_agent_handoff.md`](../inspiration/product_business_knowledge_ontology_agent_handoff.md) — the source ontology
