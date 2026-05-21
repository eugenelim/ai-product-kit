# Conventions

How work happens in this kit. The Charter is the constitution; this is the operating manual.

## File conventions

- Markdown with YAML frontmatter for everything that isn't code.
- Kebab-case filenames. ISO dates (`YYYY-MM-DD`) when temporal: `2026-05-20-stakeholder-update.md`.
- Slugs in frontmatter match the filename stem (without extension and date prefix).
- Cross-links use kit-relative paths: `parent_intent: ../intents/north-star-retention.md`.

## Universal metadata schema

Every kit artifact carries the frontmatter block below. **Universally required fields** (enforced by `tools/lint-frontmatter.py`): `object_type`, `status`, `last_updated`. All other fields are **required where applicable** per the artifact's phase-specific handover contract in `docs/HANDOVERS.md` and are checked by `/audit-completeness`, not by the linter. A reader producing a compliant artifact needs both this schema AND the relevant handover contract.

```yaml
---
id: <type-prefix>-<sequence>           # e.g. CAP-014, REQ-073, OBJ-002
slug: <kebab-case>
object_type: <one of the 80 ontology types>
name: <human-readable name>
description: <one to three sentences>
owner: <named human or role>
status: <one of the canonical lifecycle states — see "Lifecycle states" below for the per-track vocabularies>
priority: Low | Medium | High | Critical
risk_level: Low | Medium | High | Critical
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

# Traceability (required where applicable — see HANDOVERS.md)
parent_intent: <strategy intent slug>
parent_opportunity: <discovery opportunity id>
parent_learning: <validation learning slug>
parent_vision: <delivery vision slug>
parent_initiative: <delivery initiative slug>
related_problems: [<id>, ...]
related_personas: [<id>, ...]
related_kpis: [<id>, ...]

# Evidence vs assumption
evidence_basis:
  - source: <interview / ticket / metric / market signal>
    strength: Strong | Moderate | Weak
    link: <path or url>
open_assumptions: [<text>, ...]

# Human-vs-AI ownership (every artifact must declare this)
human_owned_decisions:
  - <decision a human must make personally>
ai_assistance_used:
  - <what AI drafted, summarized, or checked in producing this artifact>
ai_assistance_allowed: true | restricted | not-allowed
human_approval_required: true | false
approvals_obtained:
  - <role>: <YYYY-MM-DD>

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
---
```

Not every field applies to every type. The phase-specific handover contracts in `docs/HANDOVERS.md` declare which fields are *required* per artifact. The `/audit-completeness` command checks them.

## Object types — the eight ontology domains

All artifacts classify into one of the eight domains from `context/frameworks/ontology.md`:

1. **Market and Business Context** — Market, Market Segment, Industry Vertical, Competitor, Trend, Regulation, Business Objective
2. **Customer and User Understanding** — Customer, Buyer, User, Admin, Persona, Stakeholder, Customer Segment
3. **Problems, Needs, Jobs** — Problem, Pain Point, Need, Job to Be Done, Use Case, Trigger, Current Workaround, Evidence, Assumption, Insight, Experiment
4. **Product Strategy and Value Proposition** — Product Vision, Product Principle, Value Proposition, Differentiator, Product Objective, Outcome, KPI, Initiative, Theme
5. **Capabilities, Features, Requirements** — Capability, Feature, Requirement, User Story, Acceptance Criteria, Business Rule, Policy Rule, Non-Functional Requirement, Dependency, Edge Case, Open Question
6. **Commercial Model** — Business Model, Revenue Stream, Pricing Model, Package/Tier, Entitlement, Cost Driver, Unit Economics Assumption, Sales Motion, Adoption Funnel Stage
7. **Operational Readiness** — Business Workflow, User Workflow, Internal Workflow, Support Scenario, SLA, Training Need, Launch Plan, Rollout Strategy, Customer Communication, Risk, Control/Mitigation
8. **Governance, Decisions, Handoff** — Decision, Decision Owner, Decision Rationale, Approval, Change Request, Requirement Owner, Handoff Packet, Traceability Link *(`Status` is a property of artifacts — the `status:` frontmatter field — not an `object_type:` value)*

Plus the kit's Domain I composite handover artifact types (Strategic Intent, Opportunity Solution Tree, Opportunity, Assumption Map, Validation Learning Memo, Vision, Landing Report, Audit Report) — see [`context/frameworks/ontology.md`](../context/frameworks/ontology.md) Domain I.

When in doubt, run the `ontology-classifier` skill — it will classify input into the right type and surface missing fields.

## Lifecycle states

Two parallel tracks. The linter (`tools/lint-frontmatter.py`) accepts all of these.

**Product-artifact track** (for PM-work artifacts under `strategy/`, `discovery/`, `validation/`, `delivery/`, `market/`):

```
Draft → In Review → Validated → Approved → Ready for Engineering → In Build → Launched → Measured → Deprecated
```

**Kit-build-component track** (for kit-internal artifacts: specs, plans, skills, agents, commands, hooks, scripts, framework refs, templates, ADRs, RFCs):

```
Draft → In Review → Approved → Implementing → Shipped → Frozen
```

The two tracks share `Draft`, `In Review`, and `Approved` but diverge after. `Implementing`, `Shipped`, and `Frozen` are kit-build-only and are documented here as part of the linter's accepted set.

State transitions are checked by the linter (only that the value is in the accepted set). Cross-object state consistency (e.g., a Capability at `Approved` whose underlying Problem is still `Draft`) is checked by `/audit-traceability` when it ships in full (currently the audit is a prose procedure; ROADMAP F1.4 plans the runnable script).

## Traceability rules

Enforced by `/audit-traceability`:

1. Every Requirement must trace to a Capability.
2. Every Capability must trace to a Problem, Business Objective, or Policy Rule (Domain E).
3. Every Problem must trace to Evidence (or be marked `Assumption` until evidence exists).
4. Every KPI must trace to an Outcome.
5. Every high-risk Requirement must have a named Owner and a Mitigation.
6. Every major Decision must have a Decision Owner and Rationale recorded in `docs/adr/`.
7. Every engineering Handoff Packet must identify what is fixed, flexible, and unknown.

The canonical chain:

```
Business Objective → Product Objective → Customer Segment → Persona → Problem → Evidence → Capability → Requirement → Acceptance Criteria → KPI
```

## ADRs — Architecture Decision Records (frozen)

ADRs record **why a particular decision was made**, frozen at the time it was made. We use ADRs not just for technical architecture but for *product architecture* decisions: "Why did we choose to serve segment X over Y?", "Why did we kill opportunity Z?", "Why did we set the threshold for assumption A at 40%?".

Filename: `docs/adr/<NNNN>-<kebab-slug>.md`. Sequential numbering, no gaps.

Each ADR follows the [MADR](https://adr.github.io/madr/) shape:

```markdown
# <Title>

* Status: proposed | accepted | superseded | deprecated
* Deciders: <names>
* Date: <YYYY-MM-DD>
* Supersedes: <ADR id or none>

## Context and Problem Statement

## Decision Drivers

## Considered Options

## Decision Outcome

### Consequences

## Alternatives Considered (in detail)

## Links

* parent_intent: <slug>
* affected_artifacts: <list>
```

ADRs are **append-only**. To change a decision, write a new ADR that supersedes the old one. Never edit accepted ADRs except for typos.

## RFCs — Requests for Comments (governance, living until accepted)

RFCs are for **proposed changes to the kit itself**: new audits, new phases, new ontology types, conventions changes, plugin design. They are living documents during review and become read-only when accepted.

Filename: `docs/rfc/<NNNN>-<kebab-slug>.md`.

```markdown
# RFC NNNN: <Title>

* Status: draft | in review | accepted | rejected | withdrawn
* Author: <name>
* Date: <YYYY-MM-DD>

## Summary

## Motivation

## Detailed design

## Drawbacks

## Alternatives

## Adoption strategy

## Unresolved questions
```

Accepted RFCs may produce one or more ADRs that record the decisions taken. Once accepted, the RFC is locked and the implementation lives in the kit.

## Specs and Plans — `docs/specs/<feature>/`

The kit itself is built feature-by-feature. Every non-trivial kit component — a new skill, agent, command, hook, script, framework reference, or template — gets a spec + plan before any implementation work happens.

```
docs/specs/<feature>/
├── spec.md       ← contract + acceptance criteria
├── plan.md       ← implementation strategy + tasks
├── state.json    ← session-scratch loop state (gitignored)
└── notes/        ← (optional) research, sketches, rejected approaches
```

### What lives where

**`spec.md` is the contract.** Defines what "done" means for the component: inputs, outputs, boundaries (Always do / Ask first / Never do), verification mode, contract tests, acceptance criteria, non-goals. Scoped to a single buildable unit — days, not months. Template at [`docs/_templates/spec.md`](_templates/spec.md).

**`plan.md` is the implementation strategy.** Enumerates the work as tasks with explicit `Depends on:` declarations. Within each task, `Tests:` comes before `Approach:` — tests drive implementation, not the other way around. Tasks phrase their success criterion as the task name itself ("All invalid-input tests pass", not "Add input validation"). Template at [`docs/_templates/plan.md`](_templates/plan.md).

**`state.json` is per-session scratch.** Holds the iteration counter, plan-review status, and finding fingerprints used by `tools/check-done.py` to gate phase transitions. Gitignored — a new session deserves a fresh budget. Template at [`docs/_templates/state.json`](_templates/state.json).

### Lifecycle

Specs are **living** during implementation. If the implementation diverges from the spec, the spec is wrong; update it in the same PR. After the component ships, the spec stays as documentation of the component's contract — but at that point the *code is the truth*, and the spec is reference material to be updated alongside behavior changes.

Plans are **revisable** as you learn. When the approach changes substantially, append a line to the plan's `## Changelog`.

### Scaffolding

Run `tools/new-spec.sh <feature-slug>` to scaffold a new spec directory from the templates. The script refuses to overwrite an existing spec.

### Cite upward, never downward

Specs link to the ADRs and RFCs that constrain them. ADRs do not link to specs (specs are too small and short-lived to be worth citing from an ADR). The roadmap in [`ROADMAP.md`](../ROADMAP.md) is the ordered list of specs to build.

## How non-trivial work happens — the work-loop

For anything beyond a one-line edit, follow the **plan → execute → verify → review → iterate** loop. The mechanics are in the [`work-loop` skill](../.claude/skills/work-loop/SKILL.md); this section is the why.

**Why a loop, not a single pass.** LLM self-assessment is unreliable — agents declare victory when they *feel* done. Mechanical gates (linters, type checks, audit passes) plus an adversarial review pass replace "feel" with verifiable termination. The loop keeps going until both kinds of check are satisfied or until it hits a hard cap.

**Why think before acting.** The cost of a wrong start is higher than the cost of thinking. For high-stakes changes (new top-level structure, new ontology types, multi-component refactors), think hard first. For routine work, skip the ceremony; the discipline is "match thinking depth to stakes," not "always think hardest."

**Why iterate, not retry-from-scratch.** Most loops converge: gates fail, the reviewer surfaces a finding, the next pass fixes it. Restart-from-scratch loses the planning context.

**Why a hard iteration cap.** Without one, you're hoping. The cap (`max_iterations`, default 5) lives in `state.json` and is enforced by `tools/check-done.py`. Hit it and the work is bigger than you thought — stop, re-plan, or split.

**Why capture learnings.** A loop that finishes without updating *some* doc, skill, or note has wasted what it learned. The next agent — Claude, you, or a teammate — will pay for it again. The work-loop SKILL's CAPTURE phase enumerates where each kind of learning belongs.

### Work-loop state

The phase gates read `state.json`. Fields:

| Field | Meaning |
|---|---|
| `feature` | spec slug (informational) |
| `iteration_count` / `max_iterations` | how many REVIEW passes have run / hard cap |
| `token_budget_used_pct` / `token_budget_cap_pct` | optional session token budget |
| `consecutive_same_error_count` / `consecutive_same_error_threshold` | gate-error stuck-loop counter |
| `plan_review_status` | `pending` until the spec-mode adversarial review clears, then `approved` |
| `last_commit_sha` | latest commit produced by the loop (informational) |
| `finding_fingerprints` / `previous_finding_fingerprints` | hashes of reviewer findings, rotated each REVIEW iteration; used to detect circling |

`check-done.py` exits 0 when the phase is satisfied and non-zero when it isn't, with a one-line reason on stderr. Treat non-zero as "stop and surface."

### Enforcement (the triplet)

Three layered mechanisms enforce the kit's discipline:

| Layer | Mechanism | What it gates |
|---|---|---|
| Caps | `tools/check-done.py` | Iteration cap, token budget, plan approval, fingerprint stasis |
| Artifacts | `tools/lint-skill.sh`, `tools/lint-agent.sh`, `tools/lint-command.sh`, `tools/lint-frontmatter.py` | Shape and content hygiene per component type |
| Aggregation | `tools/pre-pr.sh` | Runs caps + artifact linters together before opening a PR |

`pre-pr.sh` is the hook to wire into your tool's lifecycle (or your local pre-commit). CI mirrors it in `.github/workflows/lint.yml`.

## Commits and PRs

If the kit lives in git:

- Conventional commits: `<type>(<scope>): <subject>`
  - Types: `feat`, `fix`, `docs`, `refactor`, `chore`, `adr`, `rfc`, `audit`, `spec`, `test`
  - Scopes for kit-build work: `skills`, `agents`, `commands`, `hooks`, `tools`, `frameworks`, `templates`, `docs`
  - Scopes for product work inside the kit: `strategy`, `discovery`, `validation`, `delivery`, `landings`
- Commits that implement a spec end with `Spec: docs/specs/<feature>/spec.md`
- One artifact per commit where practical; ADRs and RFCs always in their own commit.
- If a PR changes an artifact whose handover contract requires re-approval, flag it in the PR description and request the named owner.

## When this file is wrong

Conventions drift faster than code. If you find yourself working around something in this file, flag it in the session — either open an RFC or fix the file in the same PR. Silent workarounds are how the convention layer rots.
