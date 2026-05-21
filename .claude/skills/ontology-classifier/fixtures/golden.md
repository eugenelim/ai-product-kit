# Golden fixtures for ontology-classifier

Five inputs with expected classifications. Use these to verify the skill in a fresh Claude Code session.

## How to run a verification

1. Open a fresh Claude Code session (one not used to author the skill).
2. Load this skill via `Skill ontology-classifier`.
3. Feed each fixture's Input block, one at a time.
4. Compare the skill's output to the Expected block.
5. Record pass/fail per fixture in `docs/specs/ontology-classifier-skill/notes/manual-verification-<YYYY-MM-DD>.md`.

**Pass threshold:** 5 of 5 fixtures produce a top-level classification block; ≥4 of 5 proposed `object_type` values match the expected type exactly. A skill-flagged "Candidates" block counts as a miss for verification purposes.

---

### Fixture 1 — interview snippet (Problem + Pain Point + Use Case)

**Input:**

> "When I'm onboarding a new analyst, the worst part is the first dashboard setup. They have to click through six different settings panels just to get the default views right, and then half the time the saved-view button doesn't actually save anything — they have to redo it the next session. We end up shadowing them for the first week just to keep them unstuck."

**Expected (multi-chunk):**

- **Chunk 1** — `proposed_object_type: Problem` (Domain C). Slug: `analyst-onboarding-dashboard-setup`. Required fields: status (Inferred: Draft), description from chunk. open_assumptions notes: "Severity not stated; the 'shadowing for first week' is a workaround signal."
- **Chunk 2** — `proposed_object_type: Pain Point` (Domain C). Slug: `saved-view-button-broken`. Confidence Confirmed on description. proposed_links: `related_problems: [<chunk-1-id>]` (Confidence: Inferred).
- **Chunk 3** — `proposed_object_type: Use Case` (Domain C). Slug: `first-dashboard-setup`. Confidence Inferred on persona ("new analyst" — Persona Inferred, not Confirmed).

Summary line: `Classified: 3 chunks. By type: Problem: 1, Pain Point: 1, Use Case: 1. Needs human review: 1 (link confirmation on chunk 2 + 3).`

---

### Fixture 2 — Slack thread (Assumption + Experiment idea)

**Input:**

> "@channel quick question — do we actually know that customers want self-serve seat reassignment, or are we assuming because two enterprise reps asked? Could we ship a tiny prompt in the admin panel asking 'would you self-serve this?' for two weeks and see the click rate before building it?"

**Expected (multi-chunk):**

- **Chunk 1** — `proposed_object_type: Assumption` (Domain C). Slug: `customers-want-self-serve-seat-reassignment`. Confidence Confirmed (the chunk explicitly questions the assumption). open_assumptions: "Tier (must-test-before-shipping vs accept-as-bet) not stated."
- **Chunk 2** — `proposed_object_type: Experiment` (Domain C). Slug: `admin-panel-self-serve-prompt-test`. Confidence Inferred on details (duration "two weeks" stated, but predeclared_threshold absent — must be added before the experiment runs per the assumption-threshold-lock hook).

---

### Fixture 3 — Customer email (Feature Request + Job to Be Done)

**Input:**

> "Hi team — we'd love to be able to schedule the weekly export to land in our Snowflake instance every Monday at 6am UTC. Right now my analyst spends an hour every Monday morning kicking off the export and validating it before the leadership review at 9am."

**Expected (multi-chunk):**

- **Chunk 1** — `proposed_object_type: Job to Be Done` (Domain C). Slug: `monday-leadership-review-prep`. Confidence Confirmed on "I want to have validated weekly data ready for leadership review at 9am Monday." The Feature Request ("scheduled export to Snowflake at 6am Monday UTC") is captured under `open_assumptions` as the customer's *proposed solution*, with a recommendation to surface as a Capability candidate during discovery, not a Feature directly. (Honest classification: the customer's stated solution is a means; the JTBD is the end.)

---

### Fixture 4 — Meeting note (Decision + Risk)

**Input:**

> "We decided in today's roadmap review to deprioritize the SAML rewrite for Q3. Main risk: two enterprise prospects in the pipeline have flagged SAML as a must-have; if we don't move it back into Q3 by mid-quarter, we lose at least one of those deals."

**Expected (multi-chunk):**

- **Chunk 1** — `proposed_object_type: Decision` (Domain H). Slug: `deprioritize-saml-q3`. Confidence Confirmed on decision text. Required fields: decision_owner (Unknown — chunk says "we decided," doesn't name an owner), decision_rationale (Inferred from Q3 context). `proposed_links: related_initiatives: <saml-rewrite-id>` (Inferred).
- **Chunk 2** — `proposed_object_type: Risk` (Domain G). Slug: `saml-deprioritization-pipeline-loss`. Confidence Confirmed. Required fields: severity (Inferred: High — "lose at least one deal"), mitigation (Inferred from "move back into Q3 by mid-quarter").

---

### Fixture 5 — Competitor announcement (Trend + Differentiator gap)

**Input:**

> "Acme just announced their AI co-pilot for analysts. Public pricing matches ours but they're throwing in 1000 free LLM credits per seat per month. If this becomes table stakes by EOY, our 'no AI features' position becomes a sales objection rather than a deliberate choice."

**Expected (multi-chunk):**

- **Chunk 1** — `proposed_object_type: Trend` (Domain A). Slug: `analyst-ai-copilot-becoming-table-stakes`. Confidence Confirmed. Required: source link (Unknown — chunk doesn't link the announcement; surface as a gap).
- **Chunk 2** — `proposed_object_type: Differentiator` (Domain D) `| Adapted` because the chunk describes the *absence* of a differentiator (the kit's "no AI features" position). Confidence Inferred. open_assumptions: "Whether 'no AI features' is a deliberate position or just an unbuilt feature isn't stated; needs strategy input." Recommend escalation to `/audit-portfolio-coherence`.

---

## Pass criteria summary

| Fixture | Expected primary type | Min. fields to surface | Confidence calibration |
|---|---|---|---|
| 1 | Problem + Pain Point + Use Case (split into 3 chunks) | severity, persona, evidence_basis | Mostly Inferred/Unknown; not Confirmed |
| 2 | Assumption + Experiment (split into 2 chunks) | predeclared_threshold (Unknown), tier (Unknown) | High on Assumption, Inferred on Experiment |
| 3 | Job to Be Done (primary); Feature-request flagged as proposed solution under open_assumptions | persona, job statement | Confirmed on JTBD; the Feature is NOT mis-classified |
| 4 | Decision + Risk (split into 2 chunks) | decision_owner (Unknown), severity, mitigation | Confirmed on Decision/Risk text; Unknown on owners |
| 5 | Trend (Confirmed) + Differentiator \| Adapted (Inferred) | source link (Unknown), competitor link | Honest about "no AI features" being unclassifiable as straightforward Differentiator |

**Borderline cases that count as miss but are forgivable** (one allowed): the Feature Request in Fixture 3 if the skill classifies it as a Feature directly rather than surfacing under the JTBD's open_assumptions.
