# Product and Business Knowledge Ontology Before Engineering Handoff

## Agent Handoff Artifact

**Purpose:** This document defines a product and business knowledge ontology for work that happens before engineering implementation. It is intended to help a product, strategy, operations, or AI agent structure product discovery, business context, requirements, workflow ownership, and engineering handoff materials.

**Primary goal:** Define the business truth of the product before it becomes an engineering design.

**Core question:** What are we building, for whom, why does it matter, how does it create value, how will success be measured, and what constraints must engineering respect?

---

# 1. Executive Summary

A strong product-to-engineering handoff should not begin with a feature request. It should begin with a structured understanding of the market, customer, problem, business objective, product capability, workflow, risks, requirements, metrics, and decisions already made.

The product/business ontology creates traceability across the full chain:

```text
Market -> Customer -> Problem -> Opportunity -> Product Capability -> Requirement -> Business Outcome -> Launch -> Measurement
```

This prevents handoffs that sound like:

```text
Build this feature.
```

And replaces them with:

```text
This capability serves this customer segment, addresses this validated problem, supports this business objective, must satisfy these constraints, will be measured by these KPIs, and is prioritized for these reasons.
```

This ontology is not an engineering architecture. It is the structured product and business layer that engineering can later translate into systems, APIs, data models, services, infrastructure, and implementation plans.

---

# 2. How An Agent Should Use This Document

An agent using this document should:

1. Classify product/business information into the ontology domains defined below.
2. Identify missing information before engineering handoff.
3. Preserve traceability between strategy, customer problems, evidence, capabilities, requirements, and metrics.
4. Distinguish assumptions from validated facts.
5. Flag human-owned decisions, especially those involving customer commitments, legal/compliance concerns, pricing, ethics, safety, or roadmap priority.
6. Generate structured artifacts such as opportunity briefs, PRDs, workflow maps, business rules, acceptance criteria, launch plans, and engineering handoff packets.
7. Never treat AI-generated output as final approval for strategy, scope, compliance, pricing, or launch decisions.

Recommended agent behavior:

```text
When receiving unstructured product information:
1. Extract ontology objects.
2. Assign object types.
3. Link related objects.
4. Identify evidence and assumptions.
5. Identify missing fields.
6. Flag risks and human-owned decisions.
7. Produce an engineering-ready handoff summary only after core product/business fields are complete.
```

---

# 3. Core Ontology Domains

The ontology is organized into eight product/business domains:

1. Market and Business Context
2. Customer and User Understanding
3. Problems, Needs, and Jobs
4. Product Strategy and Value Proposition
5. Capabilities, Features, and Requirements
6. Commercial Model
7. Operational Readiness
8. Governance, Decisions, and Handoff

Each domain contains business objects, relationships, ownership expectations, and evidence requirements.

---

# 4. Domain A: Market and Business Context

This domain explains the business environment in which the product exists.

## Core Objects

| Object | Definition | Example |
|---|---|---|
| Market | The broader category where the product competes or operates. | Mid-market HR software |
| Market Segment | A meaningful subdivision of the market. | Companies with 250-1,000 employees |
| Industry Vertical | A sector with specific needs, workflows, or regulations. | Healthcare, logistics, fintech |
| Competitor | An alternative solution, including direct and indirect competitors. | Workday, spreadsheets, internal tools |
| Trend | External shift affecting demand, behavior, regulation, or technology. | AI adoption in HR operations |
| Regulation or Policy Constraint | Legal, compliance, or policy requirement affecting the product. | GDPR, HIPAA, SOC 2, internal risk policy |
| Business Objective | Company-level goal the product supports. | Increase enterprise retention by 10 percent |

## Key Relationships

```text
Market contains Market Segments.
Market Segment contains Personas and Use Cases.
Business Objective is supported by Product Initiatives.
Regulation constrains Capabilities, Workflows, Data Uses, or Requirements.
Competitor influences Positioning, Pricing, Packaging, and Differentiation.
Trend influences Strategy, Timing, and Prioritization.
```

## Agent Guidance

An agent should identify whether the product request is connected to a clear business objective. If not, the agent should flag the missing business objective before engineering handoff.

Required questions:

```text
What market does this product operate in?
Which segment is being targeted first?
What business objective does this support?
What external trends or regulations affect this product?
What alternatives does the customer use today?
```

---

# 5. Domain B: Customer and User Understanding

This domain defines who the product serves, who buys it, who uses it, who configures it, and who is affected by it.

## Core Objects

| Object | Definition | Example |
|---|---|---|
| Customer | Organization or individual that buys, adopts, or benefits from the product. | Acme Health Systems |
| Buyer | Person or role responsible for purchasing. | VP of Operations |
| User | Person who directly uses the product. | HR operations analyst |
| Admin | Person who configures, controls, or manages the product. | HR systems administrator |
| Persona | A modeled role with goals, pains, behaviors, and decision criteria. | Compliance-conscious HR director |
| Stakeholder | Anyone affected by the product or decision. | Legal, finance, sales, support |
| Customer Segment | Group of customers with similar needs, constraints, or value potential. | Regulated mid-market healthcare companies |

## Key Relationships

```text
Customer Segment has Personas.
Persona performs Jobs to Be Done.
Persona experiences Pain Points and seeks Outcomes.
Buyer may differ from User.
Admin may control access but not receive primary value.
Stakeholder may influence adoption even without directly using the product.
```

## Agent Guidance

An agent should not assume the buyer and user are the same. It should identify all relevant roles and flag conflicts between buyer value, user value, admin burden, and stakeholder risk.

Required questions:

```text
Who pays for this?
Who uses this?
Who configures this?
Who approves this?
Who may object to this?
Who benefits most?
Who carries the risk if it fails?
```

---

# 6. Domain C: Problems, Needs, and Jobs

This domain prevents teams from jumping directly to features. It defines the underlying customer and business problem.

## Core Objects

| Object | Definition | Example |
|---|---|---|
| Problem | A customer or business issue worth solving. | HR teams cannot easily audit approval history |
| Pain Point | A specific friction or negative experience. | Manual audit prep takes several days |
| Need | A desired capability or condition. | Need fast access to historical approvals |
| Job to Be Done | The task or progress the user is trying to make. | Prepare for a compliance audit |
| Use Case | A concrete situation where the product is used. | Export approval logs before quarterly audit |
| Trigger | Event that causes the need or workflow to begin. | Regulator requests documentation |
| Current Workaround | How users solve the problem today. | Screenshots, spreadsheets, Slack searches |
| Evidence | Proof that the problem exists or matters. | Interviews, support tickets, usage data |
| Assumption | Belief that has not yet been proven. | Admins will trust AI-generated audit summaries |
| Insight | Interpreted learning from evidence. | Audit prep is painful because data is fragmented |
| Experiment | Test designed to validate or invalidate an assumption. | Prototype test with five compliance managers |

## Key Relationships

```text
Problem is supported by Evidence.
Problem affects Personas.
Job to Be Done creates Use Cases.
Use Case has Triggers, Inputs, Steps, and Desired Outcomes.
Current Workaround indicates pain severity and switching cost.
Assumption should be tested by an Experiment.
Insight informs Product Strategy or Capability Design.
```

## Agent Guidance

An agent should distinguish between a customer request and an underlying problem.

Example:

```text
Customer request: Add CSV export.
Underlying problem: Compliance teams cannot quickly assemble approval evidence for audits.
Potential capability: Generate audit-ready approval history.
```

Required questions:

```text
What problem is being solved?
Who experiences the problem?
How do they solve it today?
How often does it happen?
How painful is it?
What evidence supports it?
What assumptions are still unvalidated?
```

---

# 7. Domain D: Product Strategy and Value Proposition

This domain defines why the product should exist and how it wins.

## Core Objects

| Object | Definition | Example |
|---|---|---|
| Product Vision | Long-term aspiration for the product. | Become the system of record for HR compliance workflows |
| Product Principle | Decision rule that guides tradeoffs. | Human approval is required for compliance-sensitive actions |
| Value Proposition | Promise of value to a customer or segment. | Reduce audit preparation from days to minutes |
| Differentiator | Why this product is better or distinct. | AI-assisted evidence compilation with human review |
| Product Objective | Specific product-level goal. | Increase admin weekly active usage |
| Outcome | Measurable change in customer or business behavior. | Faster audit completion |
| KPI or Metric | Quantitative measure of progress. | Audit export completion time |
| Initiative | Strategic body of work. | Compliance workflow automation |
| Theme | Grouping of related opportunities or capabilities. | Trust, auditability, workflow speed |

## Key Relationships

```text
Product Vision informs Product Principles.
Product Principle constrains Product Decisions.
Value Proposition addresses Problems.
Product Objective supports Business Objective.
Initiative contains Capabilities.
KPI measures progress toward Outcome.
Differentiator is supported by Capabilities.
```

## Agent Guidance

An agent should check whether proposed capabilities are connected to a product objective and value proposition. If the connection is weak, the agent should flag the issue.

Required questions:

```text
What value is promised?
Why is this valuable now?
What outcome should change?
What metric will prove success?
What principles guide tradeoffs?
How is this differentiated from alternatives?
```

---

# 8. Domain E: Capabilities, Features, and Requirements

This domain converts product/business intent into clear, implementation-neutral definitions.

## Core Objects

| Object | Definition | Example |
|---|---|---|
| Capability | What the product must enable users or the business to do. | Generate an audit-ready approval history |
| Feature | A concrete product function that delivers a capability. | Audit log export |
| Requirement | A specific condition the product must satisfy. | Export must include approver, timestamp, decision, and comment |
| User Story | User-centered expression of a requirement. | As an admin, I want to export approval history so I can respond to audits |
| Acceptance Criteria | Conditions that determine whether the requirement is met. | Export includes all approval events for selected date range |
| Business Rule | Product behavior driven by business logic. | Only admins may export audit logs |
| Policy Rule | Requirement based on legal, compliance, risk, or internal policy. | Data exports must be logged |
| Non-Functional Requirement | Quality or constraint requirement. | Export completes within 60 seconds for 10,000 records |
| Dependency | Something required before this can succeed. | Approval events must already be captured |
| Edge Case | Unusual but important scenario. | User was deleted after approving request |
| Open Question | Unresolved issue needing decision. | Should deleted users appear by name or anonymized ID? |

## Key Relationships

```text
Capability addresses Problems.
Feature implements part of a Capability.
Requirement specifies a Feature.
Acceptance Criteria validate a Requirement.
Business Rule governs a Workflow or Feature.
Policy Rule constrains a Requirement.
Dependency links one Capability, Requirement, or Team to another.
Edge Case may create additional Requirements or Business Rules.
Open Question must be resolved or explicitly deferred before build.
```

## Important Distinctions

```text
Capability: What the product must enable.
Feature: How the product experience may expose it.
Requirement: What must be true.
Acceptance Criteria: How completion is evaluated.
Engineering Design: How it will be implemented.
```

## Agent Guidance

An agent should avoid jumping from problem directly to engineering design. It should first translate problems into capabilities and then requirements.

Required questions:

```text
What capability is required?
What features expose the capability?
What requirements define correct behavior?
What business rules apply?
What policy constraints apply?
What edge cases matter?
What is out of scope?
```

---

# 9. Domain F: Commercial Model

This domain connects product definition to business viability.

## Core Objects

| Object | Definition | Example |
|---|---|---|
| Business Model | How the product creates and captures value. | SaaS subscription |
| Revenue Stream | Source of revenue. | Monthly platform fee |
| Pricing Model | Pricing logic. | Per seat, per workflow, usage-based |
| Package or Tier | Commercial bundle. | Pro, Enterprise, Compliance Plus |
| Entitlement | Capability included or excluded by package. | Audit exports available only in Enterprise |
| Cost Driver | Business or technical factor that affects cost. | AI processing volume |
| Unit Economics Assumption | Belief about revenue, margin, or cost behavior. | AI summary cost stays below $0.05 per audit |
| Sales Motion | How the product is sold. | Product-led, sales-led, partner-led |
| Adoption Funnel Stage | Step in customer adoption. | Trial, activation, retained, expanded |

## Key Relationships

```text
Package includes Entitlements.
Capability may be tied to Pricing Tier.
Cost Driver affects Gross Margin or Pricing.
Sales Motion influences onboarding, packaging, and demo needs.
Business Model constrains product and operational design.
Revenue Stream must connect to customer value.
```

## Agent Guidance

An agent should flag product requirements that may affect pricing, packaging, entitlement logic, margins, or sales motion.

Required questions:

```text
Is this capability free, paid, or tier-specific?
Does it affect usage costs?
Does it change customer willingness to pay?
Does it require sales enablement?
Does it create a new revenue stream?
Does it increase support or operating costs?
```

---

# 10. Domain G: Operational Readiness

This domain defines whether the business can support, sell, launch, and govern the product once released.

## Core Objects

| Object | Definition | Example |
|---|---|---|
| Business Workflow | Human or organizational process surrounding the product. | Compliance audit preparation |
| User Workflow | Steps a user takes inside or around the product. | Select date range, review results, export |
| Internal Workflow | Process performed by company teams. | Support escalation for failed export |
| Support Scenario | Situation requiring customer support. | Customer cannot find historical approval |
| SLA or Service Expectation | Expected response, resolution, or system behavior. | Enterprise support responds within 4 hours |
| Training Need | Enablement required for users or internal teams. | Admin guide for audit exports |
| Launch Plan | Activities required to release and promote the product. | Beta, GA, sales enablement |
| Rollout Strategy | How access is introduced. | Internal dogfood, design partners, staged rollout |
| Customer Communication | External messaging about value, limits, and usage. | Release notes, help docs, sales deck |
| Risk | Potential harm, failure, or negative business impact. | Incorrect audit export could create compliance risk |
| Control or Mitigation | Action to reduce risk. | Human review before final export |

## Key Relationships

```text
Capability is used within User Workflows.
User Workflow may trigger Support Scenarios.
Launch Plan depends on Training, Support, Sales, Legal, Compliance, and Documentation.
Risk must have an Owner and, where needed, a Control.
Rollout Strategy should reflect customer value, product risk, and operational readiness.
Customer Communication must align with approved product behavior and legal/compliance constraints.
```

## Agent Guidance

An agent should identify operational implications before engineering handoff. A product may be technically feasible but operationally unready.

Required questions:

```text
Who supports this after launch?
What can go wrong?
What customer questions will arise?
What internal teams need training?
What launch sequence reduces risk?
What claims can we safely make?
What controls must be in place?
```

---

# 11. Domain H: Governance, Decisions, and Handoff

This domain preserves accountability and decision history.

## Core Objects

| Object | Definition | Example |
|---|---|---|
| Decision | Explicit choice made by accountable humans. | Audit export will require admin permission |
| Decision Owner | Person accountable for the decision. | Head of Product |
| Decision Rationale | Why the decision was made. | Reduces compliance and data exposure risk |
| Approval | Formal signoff from required stakeholder. | Legal approval on export behavior |
| Status | Lifecycle state of an object. | Draft, validated, approved, deprecated |
| Change Request | Proposed modification after approval. | Add CSV export in addition to PDF |
| Requirement Owner | Person responsible for requirement clarity. | Product manager |
| Handoff Packet | Final bundle passed to engineering. | PRD, workflow map, acceptance criteria, risks |
| Traceability Link | Connection between objects across the ontology. | Requirement -> Problem -> Evidence -> KPI |

## Key Relationships

```text
Decision affects Requirements, Capabilities, Policies, Pricing, or Launch Plans.
Approval is required for high-risk Decisions.
Change Request modifies an approved object.
Handoff Packet contains approved business and product artifacts.
Requirement must have an Owner.
Major Requirement should trace back to a Problem, Customer Segment, Business Objective, or Policy Constraint.
```

## Agent Guidance

An agent should maintain a decision log and should not treat unresolved decisions as complete requirements.

Required questions:

```text
Who owns this decision?
What was decided?
Why was it decided?
What alternatives were rejected?
What does this decision affect?
What approvals are required?
What remains unresolved?
```

---

# 12. Simplified Ontology Graph

```text
Business Objective
  -> Product Objective
      -> Initiative
          -> Capability
              -> Feature
                  -> Requirement
                      -> Acceptance Criteria
              -> User Workflow
              -> Business Rule
              -> Policy Constraint
              -> KPI

Customer Segment
  -> Persona
      -> Job to Be Done
          -> Use Case
              -> Problem
                  -> Evidence
                  -> Assumption
                  -> Insight
                      -> Opportunity
                          -> Capability

Package or Pricing Tier
  -> Entitlement
      -> Capability

Risk
  -> Mitigation or Control
      -> Requirement or Workflow Step

Decision
  -> Owner
  -> Rationale
  -> Approval
  -> Affected Capability, Requirement, Pricing Decision, or Launch Plan
```

---

# 13. Universal Metadata Schema

Every ontology object should use a consistent metadata structure.

```yaml
id: ""
name: ""
object_type: ""
description: ""
owner: ""
status: "Draft | In Review | Validated | Approved | Ready for Engineering | In Build | Launched | Measured | Deprecated"
priority: "Low | Medium | High | Critical"
source_or_evidence: []
related_objects: []
business_rationale: ""
customer_impact: ""
risk_level: "Low | Medium | High | Critical"
decision_history: []
last_updated: ""
open_questions: []
```

## Example Capability Record

```yaml
id: "CAP-014"
object_type: "Capability"
name: "Audit-ready approval history export"
description: "Enables admins to generate a complete export of historical approval events."
owner: "Product Manager"
status: "Approved for Engineering Discovery"
related_problems:
  - "PROB-006"
  - "PROB-011"
related_personas:
  - "HR Admin"
  - "Compliance Manager"
related_kpis:
  - "Time to complete audit preparation"
priority: "High"
risk_level: "High"
policy_constraints:
  - "Export access restricted to admins"
open_questions:
  - "Should deleted users appear by name or anonymized ID?"
```

---

# 14. Product Workflow Before Engineering Handoff

The pre-engineering product workflow should move through clear stages:

1. Strategic Intake
2. Customer and Market Discovery
3. Problem Validation
4. Opportunity and Solution Framing
5. Business Case and Prioritization
6. Product Definition
7. Cross-Functional Readiness
8. Engineering Handoff

Each stage should identify what humans lead, what AI can assist with, and what humans must completely own.

---

# 15. Stage 1: Strategic Intake

## Goal

Decide whether the opportunity is worth exploring.

## Human-Led Activities

Humans should lead:

- Business goal definition
- Strategic fit assessment
- Market prioritization
- Customer segment selection
- Initial opportunity framing
- Executive alignment

## AI-Assisted Activities

AI can assist with:

- Summarizing market signals
- Clustering feedback themes
- Drafting opportunity briefs
- Comparing competitor positioning
- Generating strategic questions
- Identifying missing assumptions

## Human-Owned Decisions

Humans should completely own:

- Strategic direction
- Company priorities
- Market selection
- Final investment decisions
- Any commitment to customers, partners, or investors

## Output

```text
Opportunity Brief
Business Objective
Target Segment
Initial Problem Hypothesis
Known Risks
Decision to Explore, Defer, or Reject
```

---

# 16. Stage 2: Customer and Market Discovery

## Goal

Understand the customer, problem, workflow, and evidence.

## Human-Led Activities

Humans should lead:

- Customer interviews
- Field observation
- Relationship-sensitive conversations
- Interpretation of emotional, political, or organizational nuance
- Discovery strategy
- Deciding which evidence matters

## AI-Assisted Activities

AI can assist with:

- Drafting interview guides
- Summarizing interview notes
- Extracting recurring pains
- Clustering qualitative feedback
- Identifying contradictions
- Generating follow-up questions
- Mapping workflows from transcripts
- Comparing customer segments

## Human-Owned Decisions

Humans should completely own:

- Customer trust
- Consent and privacy boundaries
- Final interpretation of customer needs
- Ethical handling of sensitive information
- Decisions based on ambiguous or conflicting evidence

## Output

```text
Persona Definitions
Customer Segment Definition
Jobs to Be Done
Problem Statements
Evidence Repository
Current Workflow Map
Assumptions List
```

---

# 17. Stage 3: Problem Validation

## Goal

Confirm the problem is real, important, frequent, and valuable enough to solve.

## Human-Led Activities

Humans should lead:

- Problem prioritization
- Severity assessment
- Willingness-to-pay conversations
- Segmentation decisions
- Tradeoff decisions
- Validation design

## AI-Assisted Activities

AI can assist with:

- Scoring evidence quality
- Detecting weak assumptions
- Summarizing validation findings
- Creating problem-ranking matrices
- Identifying segments where the pain appears strongest
- Drafting survey questions or experiment plans

## Human-Owned Decisions

Humans should completely own:

- Whether the problem is worth solving
- Whether the evidence is sufficient
- Whether the team should proceed
- Whether the problem aligns with company strategy

## Output

```text
Validated Problem Statement
Evidence Summary
Problem Priority
Affected Personas
Business Impact
Customer Impact
Decision to Proceed, Reframe, or Stop
```

---

# 18. Stage 4: Opportunity and Solution Framing

## Goal

Translate the validated problem into possible product opportunities without prematurely committing to implementation.

## Human-Led Activities

Humans should lead:

- Opportunity framing
- Product judgment
- Experience direction
- Scope boundaries
- Tradeoffs between customer value and business value
- Differentiation strategy

## AI-Assisted Activities

AI can assist with:

- Generating solution alternatives
- Drafting value propositions
- Identifying adjacent use cases
- Surfacing risks and edge cases
- Creating first-pass workflow maps
- Comparing possible feature bundles
- Suggesting acceptance criteria candidates

## Human-Owned Decisions

Humans should completely own:

- Product taste and judgment
- Final solution direction
- What not to build
- Customer experience principles
- Differentiation choices

## Output

```text
Opportunity Solution Brief
Candidate Capabilities
Workflow Concepts
Value Proposition
Risks and Constraints
Prioritization Rationale
```

---

# 19. Stage 5: Business Case and Prioritization

## Goal

Decide whether the opportunity deserves product and engineering investment.

## Human-Led Activities

Humans should lead:

- ROI assessment
- Strategic prioritization
- Roadmap tradeoffs
- Revenue impact analysis
- Risk-reward analysis
- Resource allocation

## AI-Assisted Activities

AI can assist with:

- Building draft business cases
- Summarizing revenue assumptions
- Comparing prioritization frameworks
- Identifying missing cost drivers
- Generating scenario models
- Drafting roadmap narratives
- Highlighting inconsistencies between strategy and scope

## Human-Owned Decisions

Humans should completely own:

- Roadmap commitments
- Budget allocation
- Pricing decisions
- Revenue forecasts used externally
- Customer commitments
- Final prioritization

## Output

```text
Business Case
Prioritization Score
Investment Rationale
Commercial Assumptions
Roadmap Recommendation
Decision Log
```

---

# 20. Stage 6: Product Definition

## Goal

Convert the opportunity into clear product artifacts that engineering can evaluate.

## Human-Led Activities

Humans should lead:

- PRD ownership
- Requirement prioritization
- Defining user workflows
- Defining success metrics
- Resolving cross-functional ambiguity
- Aligning stakeholders

## AI-Assisted Activities

AI can assist with:

- Drafting PRDs
- Converting notes into structured requirements
- Generating user stories
- Suggesting acceptance criteria
- Identifying missing edge cases
- Checking for vague language
- Detecting conflicting requirements
- Creating glossary drafts
- Creating traceability maps

## Human-Owned Decisions

Humans should completely own:

- Final requirement approval
- Final scope
- Product priority
- Acceptance criteria approval
- Definition of success
- Any requirement that affects safety, privacy, compliance, pricing, or customer obligations

## Output

```text
Product Requirements Document
Capability Map
User Workflow Map
Business Rules
Acceptance Criteria
Success Metrics
Risks
Open Questions
Out-of-Scope List
```

---

# 21. Stage 7: Cross-Functional Readiness

## Goal

Ensure the business can sell, support, launch, and govern the product.

## Human-Led Activities

Humans should lead:

- Sales alignment
- Support readiness
- Legal and compliance review
- Pricing and packaging alignment
- Customer communication planning
- Launch sequencing
- Operational risk review

## AI-Assisted Activities

AI can assist with:

- Drafting release notes
- Drafting help center articles
- Creating sales enablement drafts
- Generating FAQ candidates
- Summarizing legal/compliance questions
- Identifying support scenarios
- Drafting training materials
- Creating launch checklists

## Human-Owned Decisions

Humans should completely own:

- Legal approval
- Compliance approval
- Pricing and packaging approval
- External messaging approval
- Customer-facing claims
- Launch readiness decision
- Incident and escalation policy

## Output

```text
Launch Plan
Sales Enablement Brief
Support Readiness Plan
Legal and Compliance Signoff
Pricing and Packaging Decision
Customer Communication Plan
Operational Risk Register
```

---

# 22. Stage 8: Engineering Handoff

## Goal

Transfer clear, validated, decision-backed product knowledge to engineering.

## Human-Led Activities

Humans should lead:

- Handoff narrative
- Requirement walkthrough
- Priority explanation
- Decision context
- Risk explanation
- Scope negotiation
- Tradeoff discussion with engineering

## AI-Assisted Activities

AI can assist with:

- Creating handoff summaries
- Generating traceability matrices
- Turning PRDs into engineering discovery questions
- Identifying undefined terms
- Highlighting missing dependencies
- Summarizing open questions
- Generating test scenario candidates

## Human-Owned Decisions

Humans should completely own:

- Final handoff approval
- Scope authority
- Business context
- Priority calls
- Requirement interpretation
- Tradeoff decisions
- Customer or business commitments

## Output

```text
Engineering Handoff Packet
Approved PRD
Capability-to-Requirement Traceability
Workflow Diagrams
Business Rules
Acceptance Criteria
Non-Functional Requirements
Risk Register
Decision Log
Open Questions
Launch Dependencies
```

---

# 23. Human vs AI Responsibility Model

## Core Rule

```text
AI may assist with analysis, synthesis, drafting, comparison, and consistency checking.
Humans must own judgment, accountability, commitments, ethics, prioritization, and final decisions.
```

---

# 24. Where AI Can Assist

AI is useful for:

- Drafting
- Summarizing
- Pattern detection
- Feedback clustering
- Requirements cleanup
- Persona draft creation
- Workflow extraction
- Competitive summaries
- Assumption generation
- Risk identification
- Scenario exploration
- Test case suggestions
- Acceptance criteria suggestions
- Documentation drafts
- Handoff summaries

AI is especially helpful when the work involves transforming messy information into structured artifacts.

Example:

```text
Input:
20 customer interview notes, 50 support tickets, 3 sales call summaries.

AI-assisted output:
- Top 7 pain points
- Frequency by segment
- Draft problem statements
- Suggested personas
- Contradictions in evidence
- Open questions for follow-up
```

Human review is required before treating these outputs as valid.

---

# 25. Where Humans Should Lead

Humans should lead work that requires context, judgment, trust, and accountability:

- Strategy
- Discovery
- Customer relationships
- Product vision
- Opportunity selection
- Prioritization
- Stakeholder alignment
- Tradeoff decisions
- Roadmap shaping
- Business model design
- Risk interpretation
- Launch readiness
- Cross-functional negotiation

Human-led does not mean AI is absent. It means AI supports the human, while the human directs the work and owns the interpretation.

---

# 26. Where Humans Should Completely Own

Humans should completely own any decision or action that:

- Commits the company externally
- Affects customer trust
- Has legal, privacy, financial, ethical, or safety implications
- Determines roadmap priority
- Defines pricing or packaging
- Approves product scope
- Approves requirements
- Approves launch
- Interprets customer evidence
- Resolves conflicting stakeholder interests
- Defines what the company will or will not do

Examples of human-owned decisions:

```text
Should we enter this market?
Should we serve this customer segment?
Is this problem important enough to solve?
Should this be on the roadmap?
What are we willing not to build?
Can we make this claim publicly?
Is this compliant?
Is this ethical?
Is this safe enough to launch?
Are we comfortable charging for this?
Should we override AI-generated recommendations?
```

AI should not be the accountable owner of these decisions.

---

# 27. Product Workflow and Ownership Maps

## Workflow 1: Opportunity Intake

| Step | Human Role | AI Role | Human-Owned Decision |
|---|---|---|---|
| Capture idea | Lead | Organize and summarize | Whether idea deserves review |
| Link to business objective | Lead | Suggest possible links | Whether alignment is real |
| Identify target customer | Lead | Draft candidate segments | Segment selection |
| Initial scoring | Lead | Pre-fill scoring matrix | Proceed, reject, or defer |

## Workflow 2: Customer Discovery

| Step | Human Role | AI Role | Human-Owned Decision |
|---|---|---|---|
| Define research goals | Lead | Draft research plan | What must be learned |
| Conduct interviews | Lead | Suggest questions | Customer relationship and consent |
| Analyze notes | Lead | Summarize and cluster themes | What insights are valid |
| Identify problems | Lead | Draft problem statements | Which problems matter |

## Workflow 3: Problem Validation

| Step | Human Role | AI Role | Human-Owned Decision |
|---|---|---|---|
| Gather evidence | Lead | Organize evidence | Evidence quality threshold |
| Assess severity | Lead | Compare signals | Severity rating |
| Assess frequency | Lead | Analyze available data | Whether problem is widespread |
| Validate willingness to pay | Lead | Draft questions and summarize | Commercial viability |

## Workflow 4: Solution Framing

| Step | Human Role | AI Role | Human-Owned Decision |
|---|---|---|---|
| Define desired outcome | Lead | Draft outcome options | Final outcome definition |
| Generate solution options | Lead | Brainstorm alternatives | Which direction to pursue |
| Map workflows | Lead | Create first-pass maps | Final workflow design |
| Identify risks | Lead | Suggest risks and edge cases | Risk tolerance |

## Workflow 5: Product Definition

| Step | Human Role | AI Role | Human-Owned Decision |
|---|---|---|---|
| Define capabilities | Lead | Suggest capability taxonomy | Capability scope |
| Write requirements | Lead | Draft, clarify, and standardize | Requirement approval |
| Define acceptance criteria | Lead | Suggest criteria | Final acceptance standard |
| Define out-of-scope items | Lead | Identify scope creep | Final scope boundary |

## Workflow 6: Commercial Readiness

| Step | Human Role | AI Role | Human-Owned Decision |
|---|---|---|---|
| Define packaging | Lead | Compare options | Final package structure |
| Assess pricing | Lead | Model scenarios | Final pricing decision |
| Prepare sales materials | Lead | Draft content | Approved external claims |
| Prepare support materials | Lead | Draft FAQs | Approved customer guidance |

## Workflow 7: Engineering Handoff

| Step | Human Role | AI Role | Human-Owned Decision |
|---|---|---|---|
| Prepare handoff packet | Lead | Summarize and format | Handoff completeness |
| Walk through requirements | Lead | Generate talking points | Requirement interpretation |
| Resolve questions | Lead | Track unresolved items | Final product decision |
| Negotiate scope | Lead | Model tradeoffs | Priority and scope calls |

---

# 28. Engineering Handoff Packet

The final handoff should include:

```text
1. Product Brief
2. Business Objective
3. Customer Segment
4. Personas
5. Validated Problem Statement
6. Evidence Summary
7. Jobs to Be Done
8. Use Cases
9. Current Workflow
10. Desired Future Workflow
11. Product Capabilities
12. Features
13. Requirements
14. Business Rules
15. Policy and Compliance Constraints
16. Acceptance Criteria
17. Success Metrics
18. Risks and Mitigations
19. Dependencies
20. Open Questions
21. Out-of-Scope Items
22. Decision Log
23. Launch and Operational Considerations
```

A good engineering handoff should make it easy for engineering to say:

```text
We understand the customer problem.
We understand the business objective.
We understand the required product behavior.
We understand what is flexible and what is not.
We understand the risks.
We understand how success will be measured.
We know which questions remain unresolved.
```

---

# 29. Example Ontology Application

## Business Objective

```text
Increase retention among enterprise customers by improving compliance workflow support.
```

## Customer Segment

```text
Regulated mid-market companies with recurring audit obligations.
```

## Persona

```text
Compliance Manager
```

## Job to Be Done

```text
When an audit request arrives, I need to quickly gather proof of approvals so that I can respond accurately and on time.
```

## Problem

```text
Approval history is fragmented across tools, making audit preparation slow and error-prone.
```

## Evidence

```text
- 8 of 12 interviewed compliance managers reported manual audit preparation.
- Support tickets show repeated requests for historical approval data.
- Sales reports indicate auditability is a recurring enterprise blocker.
```

## Capability

```text
Generate audit-ready approval history.
```

## Feature

```text
Audit log export.
```

## Requirement

```text
Admins must be able to export approval events for a selected date range.
```

## Acceptance Criteria

```text
- Export includes approver, requester, timestamp, decision, workflow name, and comments.
- Export can be filtered by date range.
- Export is available only to users with admin permissions.
- Export event is itself logged.
```

## Business Rule

```text
Only admins may export audit logs.
```

## Risk

```text
Sensitive employee data may be exposed through exports.
```

## Mitigation

```text
Restrict access, log export activity, include permission checks, and require compliance review before launch.
```

## KPI

```text
Median time to prepare audit documentation.
```

## Human-Owned Decision

```text
Whether export access should be limited to admins only.
```

## AI-Assisted Work

```text
Draft export requirements, identify edge cases, suggest acceptance criteria, and summarize audit-related customer feedback.
```

---

# 30. Governance Model

The ontology needs governance so it does not become a messy repository.

## Recommended Governance Roles

| Role | Responsibility |
|---|---|
| Product Owner | Owns product definitions, capabilities, requirements, and priorities |
| Business Owner | Owns business objectives, market priorities, and commercial rationale |
| Design Owner | Owns user workflows, experience principles, and usability requirements |
| Data or Analytics Owner | Owns KPI definitions and measurement plans |
| Legal or Compliance Owner | Owns regulatory interpretation and approval |
| Sales or GTM Owner | Owns packaging, messaging, and sales readiness |
| Support or Ops Owner | Owns support readiness and operational workflows |
| Engineering Partner | Reviews feasibility, dependencies, and implementation implications |

---

# 31. Lifecycle States

Each ontology object should have a status.

```text
Draft
In Review
Validated
Approved
Ready for Engineering
In Build
Launched
Measured
Deprecated
```

Example:

```text
Problem: Validated
Capability: Approved
Requirement: Ready for Engineering
KPI: Approved
Launch Plan: In Review
Pricing: Draft
```

This prevents teams from treating early assumptions as approved facts.

---

# 32. Traceability Rules

To keep the ontology useful, enforce these rules:

1. Every requirement must trace to a capability.
2. Every capability must trace to a problem, business objective, or policy need.
3. Every problem must trace to evidence.
4. Every KPI must trace to an outcome.
5. Every high-risk requirement must have an owner and mitigation.
6. Every major decision must have a decision owner and rationale.
7. Every engineering handoff must identify what is fixed, flexible, and unknown.

Simple traceability chain:

```text
Business Objective
-> Product Objective
-> Customer Segment
-> Persona
-> Problem
-> Evidence
-> Capability
-> Requirement
-> Acceptance Criteria
-> KPI
```

---

# 33. Where AI Should Not Be The Owner

AI should not fully own:

```text
Product strategy
Customer commitments
Legal interpretation
Compliance approval
Pricing approval
Roadmap priority
Final requirement approval
Launch approval
Ethical risk decisions
Customer-facing claims
Data access policy
Permission design decisions
Market entry decisions
High-stakes user-impacting decisions
```

AI may generate useful input for these areas, but a human must remain accountable.

---

# 34. Practical Operating Model

A healthy operating model looks like this:

```text
Humans decide what matters.
AI helps organize what is known.

Humans interpret customer reality.
AI helps summarize and compare evidence.

Humans define product judgment.
AI helps generate options and expose gaps.

Humans own accountability.
AI supports speed, consistency, and completeness.

Humans approve.
AI assists.
```

---

# 35. Recommended Final Artifact Structure

A repeatable product/business template should include:

```text
Product Knowledge Ontology

1. Business Context
   - Business objectives
   - Market
   - Segment
   - Competitors
   - Trends
   - Constraints

2. Customer Context
   - Customers
   - Buyers
   - Users
   - Personas
   - Stakeholders

3. Problem Space
   - Jobs to be done
   - Problems
   - Pain points
   - Use cases
   - Evidence
   - Assumptions
   - Insights

4. Strategy
   - Vision
   - Product principles
   - Value proposition
   - Differentiators
   - Outcomes
   - KPIs

5. Product Definition
   - Initiatives
   - Capabilities
   - Features
   - Requirements
   - Business rules
   - Acceptance criteria
   - Dependencies
   - Out-of-scope items

6. Commercial Model
   - Pricing
   - Packaging
   - Entitlements
   - Revenue assumptions
   - Sales motion
   - Cost drivers

7. Operational Model
   - User workflows
   - Internal workflows
   - Support scenarios
   - Training needs
   - Launch plan
   - Rollout strategy
   - Risks and mitigations

8. Governance
   - Owners
   - Decisions
   - Approvals
   - Change requests
   - Status
   - Handoff packet
```

---

# 36. Product Brief Template

```markdown
# Product Brief

## Product / Initiative Name

## Business Objective

## Target Customer Segment

## Primary Personas

## Problem Statement

## Evidence Summary

## Jobs to Be Done

## Current Workflow

## Desired Future Workflow

## Value Proposition

## Product Capabilities

## Scope

### In Scope

### Out of Scope

## Success Metrics

## Business Rules

## Risks and Mitigations

## Open Questions

## Human-Owned Decisions Required

## AI-Assisted Outputs Used

## Engineering Handoff Readiness
```

---

# 37. Requirement Template

```yaml
id: "REQ-001"
name: ""
capability_id: ""
feature_id: ""
requirement_type: "Functional | Non-Functional | Business Rule | Policy Rule"
description: ""
user_story: ""
acceptance_criteria:
  - ""
priority: "Must Have | Should Have | Could Have | Will Not Have"
owner: ""
status: "Draft | In Review | Approved | Ready for Engineering"
related_problem_ids: []
related_personas: []
related_kpis: []
dependencies: []
edge_cases: []
risks: []
open_questions: []
human_approval_required: true
```

---

# 38. Decision Log Template

```yaml
- decision_id: "DEC-001"
  decision: ""
  decision_owner: ""
  date: ""
  status: "Proposed | Approved | Rejected | Superseded"
  rationale: ""
  alternatives_considered:
    - ""
  affected_objects:
    - ""
  required_approvals:
    - ""
  risks:
    - ""
  notes: ""
```

---

# 39. Risk Register Template

```yaml
- risk_id: "RISK-001"
  name: ""
  description: ""
  risk_type: "Customer | Legal | Compliance | Privacy | Security | Financial | Operational | Reputational | Product"
  likelihood: "Low | Medium | High"
  impact: "Low | Medium | High | Critical"
  risk_level: "Low | Medium | High | Critical"
  owner: ""
  mitigation: ""
  control_required: true
  related_requirements: []
  related_workflows: []
  status: "Open | Mitigated | Accepted | Closed"
```

---

# 40. Workflow Template

```yaml
workflow_id: "WF-001"
name: ""
workflow_type: "User | Business | Internal | Support | Launch"
primary_persona: ""
trigger: ""
preconditions:
  - ""
steps:
  - step_number: 1
    actor: ""
    action: ""
    system_behavior: ""
    human_decision_required: false
    ai_assistance_allowed: true
    notes: ""
outputs:
  - ""
exceptions:
  - ""
risks:
  - ""
related_requirements:
  - ""
```

---

# 41. Agent Checklist Before Engineering Handoff

An agent should verify the following before labeling an initiative ready for engineering handoff:

```text
[ ] Business objective is defined.
[ ] Target customer segment is defined.
[ ] Primary personas are defined.
[ ] Problem statement is clear.
[ ] Evidence is attached to the problem.
[ ] Current workaround is understood.
[ ] Jobs to Be Done are documented.
[ ] Desired outcomes are defined.
[ ] KPIs are defined.
[ ] Capabilities are defined.
[ ] Features are mapped to capabilities.
[ ] Requirements are mapped to features and capabilities.
[ ] Acceptance criteria are defined.
[ ] Business rules are documented.
[ ] Policy or compliance constraints are documented.
[ ] Risks are documented.
[ ] Mitigations or controls are assigned.
[ ] Dependencies are identified.
[ ] Open questions are listed.
[ ] Out-of-scope items are listed.
[ ] Pricing or packaging implications are flagged.
[ ] Support and operational implications are flagged.
[ ] Human-owned decisions are explicitly marked.
[ ] Required approvals are identified.
[ ] Decision log is current.
[ ] Engineering handoff packet is complete.
```

---

# 42. The Most Important Distinction

Before engineering, the product/business side should not merely say:

```text
Feature: Add AI audit export.
```

It should say:

```text
Customer Segment:
Regulated mid-market companies.

Persona:
Compliance Manager.

Problem:
Audit evidence is hard to gather because approval history is fragmented.

Evidence:
Customer interviews, support tickets, sales objections.

Business Objective:
Improve enterprise retention and reduce audit-related churn risk.

Capability:
Generate audit-ready approval history.

Workflow:
Admin selects date range, reviews generated history, confirms export, and downloads audit package.

Human Ownership:
Compliance-sensitive outputs require human review before external use.

AI Assistance:
AI may summarize approval history, detect missing evidence, and draft export descriptions.

Human-Only Decisions:
Permission policy, compliance claims, final audit package approval, and customer-facing representations.

Engineering Handoff:
Build requirements, acceptance criteria, policy constraints, success metrics, risks, and open questions.
```

That is the level of definition that creates a strong product-to-engineering handoff.

---

# 43. Compact Agent Prompt

Use the following prompt to hand this ontology to an AI agent:

```text
You are a product/business ontology agent working before engineering handoff.
Your job is to structure product knowledge into a traceable ontology across business context, customer context, problem space, product strategy, capabilities, requirements, commercial model, operational readiness, governance, and handoff.

Do not jump directly to implementation.
Do not treat assumptions as facts.
Do not make final decisions on strategy, scope, pricing, compliance, legal risk, customer commitments, or launch approval.

For any product idea, extract and structure:
- Business objective
- Market and customer segment
- Personas and stakeholders
- Jobs to Be Done
- Problems and pain points
- Evidence and assumptions
- Current workaround
- Value proposition
- Capabilities
- Features
- Requirements
- Acceptance criteria
- Business rules
- Policy and compliance constraints
- Commercial implications
- Operational implications
- Risks and mitigations
- Human-owned decisions
- Open questions
- Engineering handoff packet

Flag missing information, unresolved decisions, weak evidence, unsupported requirements, ambiguous ownership, and risks that require human approval.

Use the principle:
AI assists with synthesis, drafting, comparison, and consistency checking.
Humans own judgment, accountability, commitments, ethics, prioritization, approvals, and final decisions.
```

---

# 44. Final Summary

The product/business ontology exists to ensure engineering receives more than a feature request. It gives engineering a structured, decision-backed, evidence-linked explanation of what matters and why.

The strongest handoff includes:

```text
Clear business objective.
Clear target customer.
Validated problem.
Evidence.
Capability map.
Requirements.
Acceptance criteria.
Business rules.
Policy constraints.
Risks.
Human-owned decisions.
Success metrics.
Operational readiness.
Decision log.
Open questions.
```

The operating model is simple:

```text
Humans lead and own judgment.
AI assists with structure, synthesis, and completeness.
Engineering receives a clear, traceable, accountable handoff.
```
