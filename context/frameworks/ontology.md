# Product and business knowledge ontology

> The kit's canonical type system. Pulled into context whenever Claude is classifying, linking, or validating product/business artifacts.
>
> Full source: [`docs/inspiration/product_business_knowledge_ontology_agent_handoff.md`](../../docs/inspiration/product_business_knowledge_ontology_agent_handoff.md). This file is the working summary.

## Core question

> What are we building, for whom, why does it matter, how does it create value, how will success be measured, and what constraints must engineering respect?

## The canonical traceability chain

```
Market → Customer → Problem → Opportunity → Capability → Requirement → Outcome → Launch → Measurement
```

This is the chain every requirement must trace back through. The audit chain (`/audit-traceability`) enforces it.

## The eight domains

### A. Market and Business Context
Where the product operates and why now.

| Object | Definition |
|---|---|
| Market | Broader category where the product competes |
| Market Segment | Meaningful subdivision of the market |
| Industry Vertical | Sector with specific needs, workflows, regulations |
| Competitor | Alternative solution, direct or indirect |
| Trend | External shift affecting demand, behavior, regulation, technology |
| Regulation / Policy Constraint | Legal, compliance, or policy requirement |
| Business Objective | Company-level goal the product supports |

### B. Customer and User Understanding
Who buys, who uses, who configures, who is affected.

| Object | Definition |
|---|---|
| Customer | Organization or person who buys, adopts, benefits |
| Buyer | Person or role responsible for purchase |
| User | Person who uses the product |
| Admin | Person who configures or manages |
| Persona | Modeled role with goals, pains, behaviors, criteria |
| Stakeholder | Anyone affected by the product or decision |
| Customer Segment | Group of customers with similar needs / constraints / value |

**Critical distinction:** buyer ≠ user ≠ admin ≠ stakeholder. AI should never assume they're the same.

### C. Problems, Needs, Jobs
The underlying customer and business problem — before we jump to features.

| Object | Definition |
|---|---|
| Problem | A customer or business issue worth solving |
| Pain Point | Specific friction or negative experience |
| Need | Desired capability or condition |
| Job to Be Done | The progress the user is trying to make |
| Use Case | Concrete situation where the product is used |
| Trigger | Event that causes the workflow to begin |
| Current Workaround | How users solve it today (indicates pain severity and switching cost) |
| Evidence | Proof the problem exists or matters |
| Assumption | Belief not yet proven |
| Insight | Interpreted learning from evidence |
| Experiment | Test designed to validate / invalidate an assumption |

**Critical distinction:** customer requests are not problems. "Add CSV export" is a request; "compliance teams cannot quickly assemble approval evidence for audits" is the underlying problem; "generate audit-ready approval history" is the capability.

### D. Product Strategy and Value Proposition
Why the product should exist and how it wins.

| Object | Definition |
|---|---|
| Product Vision | Long-term aspiration |
| Product Principle | Decision rule for tradeoffs |
| Value Proposition | Promise of value to a segment |
| Differentiator | Why this product is better or distinct |
| Product Objective | Specific product-level goal |
| Outcome | Measurable change in customer or business behavior |
| KPI / Metric | Quantitative measure of progress |
| Initiative | Strategic body of work |
| Theme | Grouping of related opportunities or capabilities |

### E. Capabilities, Features, and Requirements
Translating intent into implementation-neutral definitions.

| Object | Definition |
|---|---|
| Capability | What the product must enable users or the business to do |
| Feature | A concrete product function that delivers a capability |
| Requirement | A specific condition the product must satisfy |
| User Story | User-centered expression of a requirement |
| Acceptance Criteria | Conditions that determine whether the requirement is met |
| Business Rule | Behavior driven by business logic |
| Policy Rule | Requirement based on legal/compliance/risk/policy |
| Non-Functional Requirement | Quality or constraint requirement |
| Dependency | Something required first |
| Edge Case | Unusual but important scenario |
| Open Question | Unresolved issue needing decision |

**Critical distinctions:**
- *Capability* = what must be enabled
- *Feature* = how the product surface exposes it
- *Requirement* = what must be true
- *Acceptance Criteria* = how completion is judged
- *Engineering Design* = how it will be implemented (NOT in this ontology — that's engineering's domain)

### F. Commercial Model
Connecting product to business viability.

| Object | Definition |
|---|---|
| Business Model | How the product creates and captures value |
| Revenue Stream | Source of revenue |
| Pricing Model | Pricing logic (per-seat, per-workflow, usage) |
| Package / Tier | Commercial bundle |
| Entitlement | Capability included or excluded by package |
| Cost Driver | Factor affecting cost |
| Unit Economics Assumption | Belief about revenue/margin/cost behavior |
| Sales Motion | Product-led, sales-led, partner-led |
| Adoption Funnel Stage | Trial, activation, retained, expanded |

### G. Operational Readiness
Whether the business can support, sell, launch, govern.

| Object | Definition |
|---|---|
| Business Workflow | Human / organizational process around the product |
| User Workflow | Steps a user takes |
| Internal Workflow | Process performed by company teams |
| Support Scenario | Situation requiring customer support |
| SLA / Service Expectation | Expected response / resolution |
| Training Need | Enablement required |
| Launch Plan | Activities to release and promote |
| Rollout Strategy | How access is introduced |
| Customer Communication | External messaging |
| Risk | Potential harm, failure, negative impact |
| Control / Mitigation | Action to reduce risk |

### H. Governance, Decisions, and Handoff
Accountability and decision history.

| Object | Definition |
|---|---|
| Decision | Explicit choice made by accountable humans |
| Decision Owner | Person accountable |
| Decision Rationale | Why the decision was made |
| Approval | Formal signoff from required stakeholder |
| Change Request | Proposed modification after approval |
| Requirement Owner | Person responsible for clarity |
| Handoff Packet | Final bundle to engineering |
| Traceability Link | Connection between objects |

> Note: lifecycle state (the value of an artifact's `status:` frontmatter field) is a *property* of objects, not an object type itself. See "Lifecycle states" section below for the canonical state vocabulary.

### I. Kit composite handover artifacts (kit-specific)
Composite types the kit produces at phase boundaries. These wrap and reference the atomic types from Domains A–H above; the audits walk through them as units.

| Object | Definition |
|---|---|
| Strategic Intent | The Strategy → Discovery handover. Composite of Business Objective + diagnosis + guiding policy + 3-5 coherent actions. Lives at `strategy/intents/<slug>.md`. |
| Opportunity Solution Tree | The Discovery → Validation handover. Composite of Outcome + opportunity nodes (each containing Problem/Job/Evidence/Assumption/Insight) with one node flagged `chosen: true`. Lives at `discovery/trees/<slug>.md`. |
| Opportunity | A potential area of improvement identified from evidence and insight; not yet committed to. The chosen node in an OST. Used as a Domain C-style atomic node within an OST. |
| Assumption Map | The Chosen-Opportunity → Validation handover. Five-lens inventory of assumptions with a single named riskiest. Lives at `validation/assumption-maps/<slug>.md`. |
| Validation Learning Memo | The Validation → Vision handover. Composite of Experiment + predeclared threshold + actual result + Decision. Lives at `validation/learnings/<slug>.md`. |
| Vision | The Vision → Initiative handover. Composite of Value Proposition + Differentiator + predicted outcomes + open assumptions + counter-metrics. Lives at `delivery/visions/<slug>.md`. |
| Landing Report | The Engineering → Landings handover. Composite of predicted-vs-actual outcomes + adoption curve + counter-metrics + verdict. Lives at `delivery/landings/<slug>.md`. |
| Audit Report | Output of any `/audit-*` command. Lists findings with verdict (clean/needs-fixes/block). |

## Simplified ontology graph

```
Business Objective
  → Product Objective
      → Initiative
          → Capability
              → Feature
                  → Requirement
                      → Acceptance Criteria
              → User Workflow
              → Business Rule
              → Policy Constraint
              → KPI

Customer Segment
  → Persona
      → Job to Be Done
          → Use Case
              → Problem
                  → Evidence
                  → Assumption
                  → Insight
                      → Opportunity
                          → Capability

Package / Pricing Tier
  → Entitlement
      → Capability

Risk
  → Mitigation / Control
      → Requirement or Workflow Step

Decision
  → Owner
  → Rationale
  → Approval
  → Affected Capability / Requirement / Pricing / Launch Plan
```

## Mapping to kit phases

| Ontology domain | Lives primarily in |
|---|---|
| A. Market & Business Context | `strategy/` |
| B. Customer & User Understanding | `context/personas/` and `discovery/` |
| C. Problems, Needs, Jobs | `discovery/` |
| D. Product Strategy and Value Proposition | `strategy/intents/`, `discovery/outcomes/`, `delivery/visions/` |
| E. Capabilities, Features, Requirements | `delivery/visions/`, `delivery/initiatives/`, `delivery/specs/` |
| F. Commercial Model | `strategy/intents/` (high level), `delivery/visions/` (per-bet), `context/business/` |
| G. Operational Readiness | `delivery/initiatives/` and `delivery/launch-checklists/` |
| H. Governance, Decisions, Handoff | `docs/adr/`, `delivery/handoff-packets/`, every artifact's frontmatter |

## Traceability rules (enforced by `/audit-traceability`)

1. Every Requirement must trace to a Capability.
2. Every Capability must trace to a Problem, Business Objective, or Policy Rule (Domain E).
3. Every Problem must trace to Evidence (or be marked Assumption until evidence exists).
4. Every KPI must trace to an Outcome.
5. Every high-risk Requirement must have a named Owner and a Mitigation.
6. Every major Decision must have a Decision Owner and Rationale recorded in `docs/adr/`.
7. Every engineering Handoff Packet must identify what is fixed, flexible, and unknown.

## Lifecycle states

```
Draft → In Review → Validated → Approved → Ready for Engineering → In Build → Launched → Measured → Deprecated
```

State transitions are recorded in artifact frontmatter (`status:`) with `last_updated:`. The audit chain flags state mismatches (e.g. a Capability at `Approved` whose underlying Problem is still `Draft`).

## When the ontology is wrong

If an object appears in your work that doesn't fit any of the documented types (74 atomic types across Domains A–H plus 8 composite types in Domain I), open an RFC. Don't invent ad-hoc types — that's how ontology drift starts.

For "close but not quite" cases, the linter (`tools/lint-frontmatter.py`) accepts `object_type: <Base Type> | Adapted` as a documented escape hatch. Use it sparingly and follow up with an RFC if the adapted form recurs.
