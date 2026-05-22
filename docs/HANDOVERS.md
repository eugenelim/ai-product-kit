# Handover contracts

The single load-bearing rule: **each handover must travel as an artifact, not as a conversation.** This document specifies every handover artifact's contract: required frontmatter, ontology object types it represents, required sections, and how the next phase consumes it.

If a handover artifact doesn't meet its contract, the next phase has insufficient gating. The audit commands and phase-guard hooks enforce these contracts mechanically.

The universal metadata schema (in `docs/CONVENTIONS.md`) applies to every artifact. The contracts below add **type-specific required fields** on top of the universal schema.

---

## Handover 1: Strategy → Discovery

**Artifact:** `strategy/intents/<slug>.md`
**Object type (ontology):** Strategic Intent / Business Objective composite (Domain A + Domain D)

**Required frontmatter (additions on top of the universal schema):**

```yaml
object_type: Strategic Intent
mode: greenfield | enterprise
central_challenge: <one sentence>
guiding_policy: <one paragraph>
coherent_actions:
  - <action 1>
  - <action 2>
  - <action 3>
  # 3-5 items, no more
horizon: <quarters>
business_objective: <linked Business Objective id>
parent_diagnosis: <path to diagnosis>
human_owned_decisions:
  - Whether to pursue this central challenge
  - Resource commitment behind coherent actions
human_approval_required: true
```

**Required sections:**

1. **The challenge** — what specifically must be addressed; cite evidence (numbers, quotes, market signal)
2. **The guiding policy** — what *kind* of response we commit to; what we are *not* responding with
3. **Coherent actions** — 3-5 actions that reinforce each other; for each, name what it commits and what it forecloses
4. **Coherence check** — explicitly check pairs and confirm they don't cancel out
5. **Open questions for discovery** — what we don't know that discovery will address

**Failure if missing:** Operating-model failure mode #3 (discovery without a strategic frame).

**Detector:** `/audit-discovery-coherence` flags OSTs with no `parent_intent`; intents with no downstream OST after >30 days. *(planned — ROADMAP P2.11; until shipped, this check is manual: confirm `parent_intent:` is populated before treating the OST as the Discovery → Validation handover.)*

---

## Handover 2: Discovery → Validation

**Artifact:** `discovery/trees/<slug>.md` (plus structured `discovery/trees/<slug>.json` for the OST validator)
**Object types:** Outcome (Domain D), Opportunity (Domain C), Job to Be Done (Domain C), Problem (Domain C), Evidence (Domain C), Insight (Domain C)

**Required frontmatter:**

```yaml
object_type: Opportunity Solution Tree
parent_intent: <strategic intent slug>
outcome:
  id: <OUT-NNN>
  metric: <name>
  current: <value>
  target: <value>
  measurement: <how, where, by when>
opportunity_count: <total nodes>
chosen_opportunity:
  id: <OPP-NNN>
  rationale: <one paragraph>
related_personas: [<persona ids>]
related_problems: [<problem ids>]
human_owned_decisions:
  - Selection of the chosen opportunity
  - What opportunities to explicitly exclude from the tree
```

**Required sections:**

1. **The outcome** — measurable, tied to the parent intent's coherent action
2. **Opportunity space** — all opportunities surfaced, as a tree
3. **The chosen one** — why this, why now, what we'd give up by choosing it
4. **Source opportunities** — interview-level evidence under each tree node
5. **Excluded** — opportunities considered and explicitly excluded (and why)

**Failure if missing:** Operating-model failure mode #4 (jumping from interviews to "let's build it").

**Detector:** `/audit-discovery-coherence` flags OSTs with no `parent_intent`; intents with no downstream OST after >30 days. *(planned — ROADMAP P2.11; until shipped, this check is manual.)*

---

## Handover 2.5: Discovery → Assumption Map

**Artifact:** `validation/assumption-maps/<slug>.md`
**Object types:** Assumption (Domain C), Opportunity (Domain C, by reference)

The chosen Opportunity from Handover 2 lists its assumptions; the Assumption Map is where those assumptions get *typed*, *ranked*, and *prioritized for testing*. Without this artifact, Validation jumps straight from "we picked an opportunity" to "we ran an experiment" — skipping the step where the team agrees on *which* assumption is the riskiest. That's the failure that produces validation theatre: testing the easy assumption because the riskiest one is uncomfortable.

**Required frontmatter (additions on top of the universal schema):**

```yaml
object_type: Assumption Map
parent_opportunity: <OPP-NNN>
parent_intent: <strategic intent slug>     # restated for traceability
assumptions:
  - id: <ASM-NNN>
    statement: <one sentence>
    lens: desirability | viability | feasibility | usability | ethical
    risk_if_wrong: Low | Medium | High | Critical
    evidence_today: Strong | Moderate | Weak | None
    test_priority: 1 | 2 | 3 | …          # 1 = test first
riskiest_assumption: <ASM-NNN>             # the one Validation will test next
human_owned_decisions:
  - Selection of the riskiest assumption to test next
  - Acceptance of assumptions marked "accept-as-bet"
```

**Required sections:**

1. **The chosen opportunity** — one-paragraph restatement; link to the OST node.
2. **Assumptions, by lens** — every assumption underneath the opportunity, classified into the five-lens taxonomy (desirability / viability / feasibility / usability / ethical). Cite `context/frameworks/assumption-tests.md` *(planned — ROADMAP F4.4)* for definitions; until that framework ships, link to ontology Domain C entries for the named lenses.
3. **Risk-vs-evidence ranking** — each assumption plotted on (risk_if_wrong × evidence_today). The riskiest under-evidenced assumption is the next test target.
4. **The riskiest assumption** — restated; why it earned the rank; what we'd lose if it's wrong.
5. **Accepted bets** — assumptions the team explicitly chooses not to test (with rationale). These propagate to the Vision artifact's `open_assumptions:` block as tier `accept-as-bet`.

**Failure if missing:** Validation theatre. Teams test the cheapest assumption rather than the riskiest, then declare "validated" on a test that wouldn't have changed the decision.

**Detector:** `/audit-assumption-coverage` *(planned — ROADMAP P3.11)* flags chosen opportunities with no assumption map after >7 days. Until shipped, audit manually.

---

## Handover 3: Validation → Vision

**Artifact:** `validation/learnings/<slug>.md`
**Object types:** Insight (Domain C), Experiment (Domain C), Assumption (Domain C), Decision (Domain H)

**Required frontmatter:**

```yaml
object_type: Validation Learning Memo
parent_opportunity: <opportunity id>
riskiest_assumption: <one sentence>
test:
  type: desirability | viability | feasibility | usability | ethical
  experiment: <link to validation/experiments/<id>/>
  predeclared_threshold:
    success: <quantitative criterion>
    falsification: <quantitative criterion>
  predeclared_at: <YYYY-MM-DD>     # MUST be before experiment ran
result:
  actual: <value>
  status: survived | killed
  decided: <YYYY-MM-DD>
  decided_by: <names>
human_owned_decisions:
  - Whether to survive or kill on ambiguous results
  - Whether to proceed to delivery given remaining open assumptions
human_approval_required: true
```

**Required sections:**

1. **The assumption tested** — restated; why it was the riskiest
2. **The test** — design, threshold, predeclared falsification with timestamp showing it was declared *before* results
3. **The result** — actual measurement vs predeclared thresholds
4. **What we learned** — separate from whether we proceed
5. **The disposition** — survived → proceed to vision; killed → opportunity returned to OST or pruned

**Hard rule:** `predeclared_at` must be before the experiment-results file's earliest timestamp. The `assumption-threshold-lock` hook enforces this. **The single most important guard in the kit** — it's what separates real validation from theatre.

**Detector:** `/audit-vision-evidence` flags visions citing assumptions that never went through a test. *(planned — ROADMAP P3.12; until shipped, the human reviewer must confirm `predeclared_at:` precedes the experiment results file's earliest timestamp.)*

---

## Handover 4: Vision → Initiative

**Artifact:** `delivery/visions/<slug>.md`
**Object types:** Value Proposition (Domain D), Differentiator (Domain D), Product Objective (Domain D), Risk (Domain G), Open Assumption (Domain C)

**Required frontmatter:**

```yaml
object_type: Vision
parent_learning: <validation learning slug>
parent_intent: <strategic intent slug>    # restated for traceability
crosses_teams: true | false
predicted_outcomes:
  - kpi_id: <KPI-NNN>
    threshold: <value>
    measure_at: <weeks-after-launch>
open_assumptions:
  - assumption: <text>
    tier: must-test-before-shipping | accept-as-bet | will-monitor-post-ship
counter_metrics:
  - kpi_id: <KPI-NNN>
human_owned_decisions:
  - Customer-shaped framing of the value proposition
  - Differentiator selection
  - Predicted outcome thresholds
human_approval_required: true
```

**Required sections:**

1. **The customer-shaped pitch** — narrative voice, persona-aware, drawing on surviving learning
2. **The change** — what's different for the customer
3. **What we believe and why** — citing learning memos
4. **What we're still betting on** — open assumptions, tiered (must-test, accept-as-bet, monitor)
5. **Counter-metrics** — what we'd watch to know we made it worse
6. **Predicted outcomes** — what success looks like; measurement plan

**Failure if missing:** Three concurrent initiatives that look reasonable in isolation but contradict each other.

**Detector:** `/audit-portfolio-coherence` (Rumelt-style coherence audit across all active visions/initiatives).

---

## Handover 5: Initiative → Spec

**Artifact:** `delivery/initiatives/<slug>/` (folder)
**Object types:** Initiative (Domain D), Capability (Domain E), Feature (Domain E), Business Workflow (Domain G), Dependency (Domain E)

Folder contents:
- `README.md` — initiative overview
- `context-map.md` — bounded contexts, ownership, shared shapes, Wardley-lite evolution check
- `flow.md` — end-to-end flow (Mermaid)
- `child-specs.md` — manifest of spec files
- `sequence.md` — dependency-aware delivery sequence
- `capabilities.md` — Capability list with traceability to parent Problems

**Required frontmatter on `README.md`:**

```yaml
object_type: Initiative
parent_vision: <vision slug>
crosses_repos: [<repo>, <repo>]
crosses_teams: [<team>, <team>]
capabilities: [<CAP-NNN>, ...]
status: active | paused | done
context_map_signed_off: <YYYY-MM-DD>
sign_off_by: [<names>]
human_owned_decisions:
  - Bounded-context ownership assignment
  - Build vs buy decisions in the evolution check
  - Delivery sequencing
```

**Required content:**

1. `context-map.md` — per bounded context: owner, public contract, commodity-vs-custom (Wardley), evolution stage
2. `flow.md` — Mermaid sequence diagram of end-to-end customer flow across contexts
3. `child-specs.md` — table: spec slug, owning context, owning team, status, link
4. `sequence.md` — DAG of specs by dependency; first-shippable subset called out
5. `capabilities.md` — each Capability with linked Problem, evidence strength, related KPI

**Failure if missing:** Cross-team handoffs re-litigated inside individual specs.

**Detector:** `/audit-spec-linkage` flags specs without `parent_initiative:`; `/audit-traceability` flags Capabilities without traced Problems.

---

## Handover 6: Spec → Engineering Handoff Packet

**Artifact:** `delivery/handoff-packets/<slug>/`
**Object type:** Handoff Packet (Domain H) — the ontology's signature pre-engineering deliverable

This is a new handover in v3, added because v2's specs were a folder but the engineering team inherited prose, not a structured deliverable. The packet is what engineering actually consumes.

Folder contents (the ontology's section 28, 23 items, as files or as sections in a single brief):

```
README.md                       ← Product Brief (template in templates/handoff-brief.md)
business-objective.md           ← cite the strategic intent
customer-segment.md             ← cite the segment definition
personas.md                     ← linked persona files from context/personas/
problem.md                      ← validated problem statement + evidence
jobs-to-be-done.md
current-workflow.md             ← how it works today
future-workflow.md              ← how it'll work
capabilities.md                 ← from the parent initiative
features.md
requirements.yaml               ← REQ-NNN files with full ontology metadata
business-rules.md
policy-constraints.md
acceptance-criteria.md          ← per-requirement
non-functional-requirements.md
risks.md                        ← with mitigations
dependencies.md
open-questions.md
out-of-scope.md
decision-log.md                 ← summary; full ADRs in docs/adr/
launch-considerations.md
success-metrics.md              ← KPIs with thresholds
human-owned-decisions.md
```

**Required frontmatter on `README.md`:**

```yaml
object_type: Handoff Packet
parent_initiative: <slug>
status: Ready for Engineering
completeness_audit_passed: <YYYY-MM-DD>
adversarial_review_passed: <YYYY-MM-DD>
quality_engineer_review_passed: <YYYY-MM-DD>
compliance_review_status: passed | not-required | <YYYY-MM-DD>
engineering_partner: <name>
fixed_vs_flexible:
  fixed: [<requirement ids that must not change>]
  flexible: [<requirement ids open to engineering tradeoffs>]
  unknown: [<questions for engineering to weigh in on>]
```

**Required content:** the 23 files listed in the folder above. The `/audit-completeness` command runs the ontology §41 checklist (25 items) against the packet; the 23 files contain the content the checklist verifies — some §41 items map to single files (e.g., "business objective is named" → `business-objective.md`) and a few items are content checks within a file (e.g., "approvals identified" + "approvals obtained" both check `human-owned-decisions.md` + the packet's `approvals_obtained:` frontmatter). The count mismatch (23 files vs 25 checklist items) is intentional: files are the unit of authoring; checklist items are the unit of verification. See `/audit-completeness` command for the canonical 25-item list.

**The "ready for engineering" test:** engineering should be able to say, after reading the packet:

> We understand the customer problem. We understand the business objective. We understand the required product behavior. We understand what is fixed and what is flexible. We understand the risks. We understand how success will be measured. We know which questions remain unresolved.

If any of those is uncertain, the packet isn't ready. Run `/audit-completeness` and fix the flagged items.

**Detector:** `/audit-completeness` runs the ontology's 25-item checklist (shipped, prose-procedure form; runnable script planned — ROADMAP F1.5). The `adversarial-reviewer` (shipped), `compliance-reviewer` *(planned — ROADMAP P6.1)*, and `quality-engineer` *(planned — ROADMAP P6.2)* subagents add their lenses.

---

## Handover 7: Engineering → Landings

**Artifact:** `delivery/landings/<slug>.md`
**Object types:** Outcome (Domain D), KPI (Domain D), Decision (Domain H)

**Required frontmatter:**

```yaml
object_type: Landing Report
parent_vision: <vision slug>
parent_handoff_packet: <handoff packet slug>
shipped: <YYYY-MM-DD>
measured_at: <YYYY-MM-DD>     # at least 30 days post-ship
verdict: adopt | fix | kill
verdict_at: <YYYY-MM-DD>
verdict_by: [<names>]
human_owned_decisions:
  - Verdict
  - Decision to revert, double-down, or fix
human_approval_required: true
```

**Required sections:**

1. **The shipped change** — one-paragraph recap
2. **Predicted outcomes vs actuals** — table; cite the vision's predicted thresholds
3. **Adoption curve** — visualization or table by cohort / surface
4. **Counter-metrics** — did we break anything we said we were watching?
5. **What landed and what didn't** — surviving assumptions that didn't hold up in production; the ones that did
6. **Verdict** — adopt (move on), fix (named change), or kill (rollback)
7. **Feedback to strategy** — what this teaches us for the next quarterly refresh

**How the cycle consumes it:** landings feed directly into the next `/strategy-refresh`. Killed initiatives become input to coherence analysis ("we thought X; X was wrong; what does that say about our guiding policy?").

**Detector:** `/audit-landings-debt` lists every shipped initiative with no landing report after 30 days. *(planned — ROADMAP P5.9; until shipped, audit manually by listing `delivery/handoff-packets/` against `delivery/landings/`.)*

---

## The audit chain

The single command, `/audit-all` *(planned — ROADMAP P6.3)*, runs every handover audit in sequence and produces a one-page report listing every missing or weak handover across the active portfolio. Until shipped, run the individual `/audit-*` commands manually in order.

This is the report to bring to a quarterly review. If it's long, the conversation isn't about new bets; it's about closing open ones.

---

## What this document is NOT

- **Not a contract you sign with someone else.** It's the contract your future self signs with your past self. Most product orgs fail by re-litigating prior phases.
- **Not exhaustive frontmatter.** Add fields. Don't remove the required ones. The audits read them by name.
- **Not a substitute for judgment.** A handover artifact can meet its contract and still be wrong. The contract is a floor, not a ceiling.
