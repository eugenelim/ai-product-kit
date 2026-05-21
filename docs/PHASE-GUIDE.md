# Phase guide — where am I, what's next?

When something feels stuck, the answer is almost always *go back one phase*.

The single load-bearing diagnostic question: **what artifact do I currently have that's signed off?**

If your most-recent signed-off artifact is...

| ...this | ...you're at | ...your next artifact | ...command to start |
|---|---|---|---|
| Nothing — vague sense the org "should do something about X" | Pre-strategy | Rumelt diagnosis: name the central challenge in one sentence | `/strategy-refresh` |
| A diagnosed challenge + guiding policy | Strategy → Discovery handover | OST rooted in a measurable outcome that ties to the intent | `/generate-ost` |
| An OST with several opportunities, one flagged `chosen: true` AND a named `riskiest_assumption:` | Discovery → Validation handover | Assumption map for the chosen opportunity (`validation/assumption-maps/<slug>.md`); the riskiest assumption gets a falsifiable framing | `/assumption-test` |
| Assumption map with riskiest assumption named | Validation (mid-phase) | Designed experiment with predeclared falsification threshold | `/design-experiment` |
| Learning memo with `status: killed` | Validation (re-enter Discovery) | Update the OST: mark the opportunity `killed: true`; pick the next opportunity or reframe the tree | `/update-ost` |
| Experiment with results vs threshold | Validation → Delivery handover | Learning memo with `status: survived` or `status: killed` | `/falsify-or-confirm` |
| Learning memo with `status: survived` | Delivery / Vision sub-phase | The vision document | `/draft-vision` |
| A vision but unsure if work crosses teams | Vision shape check | Either expand to initiative, or fold onto a single spec | `/vision-shape-check` |
| Vision + at least two affected services/repos | Delivery / Initiative sub-phase | Initiative folder with context map + flow + child-spec manifest | `/draft-initiative` |
| Initiative with child-spec pointers | Delivery / Spec sub-phase | Spec(s) + plan(s) in each affected repo | `/draft-spec` |
| Specs + a complete handoff packet | Engineering handoff | Send to engineering; the engineering work begins | `/audit-completeness` (final check) |
| Code in production | Delivery → Landings handover | Landing report (actuals vs predictions) | `/landing-report` |
| Landing report with `verdict: adopt | fix | kill` | Cycle complete | Feed into next quarterly strategy refresh | `/strategy-refresh` |

---

## The "I'm stuck" diagnostic — extended

If you're stuck, run these in order until something clicks:

1. **`/phase-guide`** — interactive: what artifact do you have, what's missing
2. **`/cadence-check`** — maybe a higher-rhythm phase has decayed (strategy stale, OST not updated, no kills lately) and the immediate stuckness is a downstream symptom
3. **`/audit-traceability`** — maybe the chain is broken upstream and the artifact you're trying to draft is structurally unsupported
4. **`/audit-completeness <slug>`** — maybe the artifact looks done but is missing required handoff fields
5. **The relevant phase-specific audit:**
   - Specs feel wrong: `/audit-spec-linkage`
   - Initiatives feel contradictory: `/audit-portfolio-coherence`
   - Vision feels like wishful thinking: `/audit-vision-evidence`
   - OST feels disconnected from strategy: `/audit-discovery-coherence`
   - Validation feels like theatre: the `assumption-threshold-lock` hook + `/audit-vision-evidence`
6. **Go back one phase.** If a phase keeps re-deriving the prior phase's output, the prior phase didn't finish.

---

## The seven failure modes, with detection commands

| Failure | Detection |
|---|---|
| 1. Operating at the wrong phase | `/phase-guide` |
| 2. Strategy = list of goals | `strategy-skeptic` agent + `/audit-portfolio-coherence` |
| 3. Discovery without strategic frame | `/audit-discovery-coherence` |
| 4. Validation theatre | `assumption-threshold-lock` hook + `/audit-vision-evidence` |
| 5. Vision before validation | `/audit-vision-evidence` |
| 6. Specs without initiatives | `/audit-spec-linkage` |
| 7. Cadence collapse | `/cadence-check` + `cadence-manager` scheduled agent |

Plus the v3 additions:

| Failure | Detection |
|---|---|
| 8. Untraceable requirement | `/audit-traceability` |
| 9. Incomplete engineering handoff | `/audit-completeness` |
| 10. Missing human approval | `/audit-completeness` flags `approvals_obtained:` gaps |
| 11. Untyped or wrongly-typed object | `ontology-classifier` skill |
| 12. Stale ontology drift | An RFC proposing a new type without it living anywhere is the symptom; `docs/rfc/` should be checked for stalled proposals |

If any audit comes back with hits, that's where to spend your next session — not on the new work, on the missing artifact.

---

## What this guide is NOT

- **Not a flowchart.** Phases overlap and run on different rhythms. You'll often be in Discovery for one intent and Delivery for another simultaneously.
- **Not a gate.** Hooks allow override with explicit opt-in. But override goes in frontmatter and audits keep flagging it.
- **Not a substitute for judgment.** The kit can tell you when an artifact is missing. It can't tell you whether to invest in producing it. That's still your call.
