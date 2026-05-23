# Inventory at a glance

Every artifact in the kit, classified by **phase** (rows) and **practice area** (columns), with its primary output (ontology object type where applicable) and which agent invokes it.

## Legend

- **Block:** SC = slash command, AG = agent, SK = skill, HK = hook, SCH = scheduled agent, REF = reference context, IDX = index README
- **Invocation:** YOU = you type it, CLAUDE = Claude auto-invokes, EVENT = triggered by hook, CRON = OS scheduler
- **Output:** the artifact's primary output — an ontology object type when the artifact produces a Domain A–I type, otherwise a short label naming what the artifact emits (the ontology canon lives in `context/frameworks/ontology.md`)
- **Status:** `shipped` (built and usable today) or `planned (Fx.y)` / `planned (Px.y)` (forward-looking design intent; build queue row in [`ROADMAP.md`](../ROADMAP.md))

## Indexes (kit-meta)

| Artifact | Block | Inv | Purpose | Status |
|---|---|---|---|---|
| `.claude/skills/README.md` | IDX | (pulled) | On-disk index of skills (shipped + planned) — discharges AGENTS.md "full index" reference | shipped (created 2026-05-21) |
| `.claude/agents/README.md` | IDX | (pulled) | On-disk index of agents (shipped + planned + scheduled) — discharges AGENTS.md "full catalog" reference | shipped (created 2026-05-21) |

> **Reading this inventory:** rows marked `planned` are NOT currently shippable. Their presence here documents the kit's design surface, not its current capability. Use the `Status` column to filter to what works today.

## Linters (kit-meta)

Shape linters used by `tools/pre-pr.sh` and `.github/workflows/lint.yml` to keep kit components on contract. One linter per component type, plus a cross-cutting frontmatter checker. The work-loop SKILL §3.2 names them as the per-component-type verify gate.

| Linter | Lints | Rules | Status |
|---|---|---|---|
| `tools/lint-skill.sh` | `.claude/skills/*/SKILL.md` | YAML frontmatter (`name`, `description` ≤1024, `license`); H1; `## When to use this skill`; soft cap 400 lines | shipped (F0.4) |
| `tools/lint-agent.sh` | `.claude/agents/*.md` (excluding `README.md`) | YAML frontmatter (`name`, `description`, `tools`, `model`); H1; required body sections | shipped (F0.4) |
| `tools/lint-command.sh` | `.claude/commands/*.md` | YAML frontmatter; required body sections | shipped (F0.4) |
| `tools/lint-hook.sh` | `.claude/hooks/*.md` (excluding `README.md`) | H1 `^# <slug> hook$`; sections `## What it does`, `## Why this matters`, `## Configuration`; soft cap 250 lines | shipped 2026-05-21 (F0.10) |
| `tools/lint-frontmatter.py` | every kit artifact with frontmatter | universal-metadata schema (`object_type`, `status`, `last_updated`, parent-link validity, ontology type-set membership); `human_approval_required: true` ⇒ non-empty `human_owned_decisions`; `ai_assistance_allowed: restricted` ⇒ non-empty `ai_assistance_used` (list) | shipped (F0.5; F0.12 added `ai_assistance_allowed` check, 2026-05-21) |

## Authoring conventions (kit-meta)

Parent-convention specs that lock the shape of a fan-out before its workers run. Each ships a convention text inside `docs/CONVENTIONS.md`, a literal copyable skeleton under a `_meta/` directory, and a pytest contract test that auto-tightens as each fan-out worker ships its artifact.

| Convention | Skeleton | Contract test | Constrains | Status |
|---|---|---|---|---|
| `docs/specs/template-authoring-convention/` | `templates/_meta/template-skeleton.md` | `scripts/tests/test_templates_instantiate.py` (`--check-template` mode) | F3.1–F3.10 (ten kit-provided product-artifact templates under `templates/`) | shipped 2026-05-22 |
| `docs/specs/phase-4-command-convention/` | `.claude/commands/_meta/command-skeleton.md` | `scripts/tests/test_phase4_command_shape.py` | P4.1, P4.3, P4.4, P4.5, P4.6, P4.8, P4.11 (seven Phase-4 template-fill slash commands) | shipped 2026-05-23 |

---

## Phase 1 — Strategy

| Artifact | Block | Mode | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|---|
| `/market-scan` | SC | greenfield | YOU | Market, Market Segment | Analogical industry scan | planned (P7.11) |
| `/competitive-research` | SC | greenfield | YOU | Competitor, Differentiator | Parallel fan-out across competitors | shipped |
| `/jtbd-analogues` | SC | greenfield | YOU | Job to Be Done | Jobs from adjacent markets | planned (P7.12) |
| `/wardley-map` | SC | enterprise | YOU | Value chain, Evolution stage | Map current value chain | planned (P7.7) |
| `/internal-jtbd-interview` | SC | enterprise | YOU | Job to Be Done, Insight | Captive user-base interview | planned (P7.9) |
| `/value-chain-evolution` | SC | enterprise | YOU | Trend | Quarter-over-quarter diff | planned (P7.10) |
| `/strategy-refresh` | SC | both | YOU (quarterly) | Strategic Diagnosis | Rumelt-style one-page diagnosis | planned (P7.1) |
| `/strategic-intent` | SC | both | YOU | Strategic Intent | One-pager: central challenge + policy + actions | planned (P7.2) |
| `/audit-portfolio-coherence` | SC | both | YOU (weekly) | Audit Report | Rumelt coherence across portfolio | shipped (script + prose fallback) |
| `/cadence-check` | SC | both | YOU (monthly) | Cadence Drift Report | Detect rhythm decay | planned (P7.5) |
| `/exec-strategy-narrative` | SC | both | YOU | Exec Narrative | 6-pager for leadership | planned (P7.4) |
| `competitor-research` | AG | greenfield | CLAUDE (fan-out) | Competitor record | One competitor end to end | shipped |
| `strategy-skeptic` | AG | both | CLAUDE (dispatch) | Review | Rumelt's failure modes | planned (P7.3) |
| `strategy-coherence` | SK | both | CLAUDE | Coherence rule library | Pairwise audit rules | shipped |
| `wardley-evolution` | SK | enterprise | CLAUDE | Evolution placement | Place components on the axis | planned (P7.8) |
| Rumelt failure modes | REF | both | (pulled) | — | `context/frameworks/rumelt.md` | planned (F4.7) |
| Wardley primer | REF | enterprise | (pulled) | — | `context/frameworks/wardley.md` | planned (F4.8) |
| Strategic coherence | REF | both | (pulled) | — | `context/frameworks/strategic-coherence.md` | planned (F4.10) |

## Phase 2 — Discovery

| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/interview-snapshot` | SC | YOU | Insight, Pain Point, Use Case | Transcript → snapshot | planned (P2.1) |
| `/extract-opportunities` | SC | YOU | Opportunity | Snapshots → candidates | planned (P2.4) |
| `/cluster-opportunities` | SC | YOU | Theme | Theme raw opportunities | planned (P2.6) |
| `/generate-ost` | SC | YOU | OST, Outcome, Opportunity | First-pass tree | planned (P2.7) |
| `/update-ost` | SC | YOU | OST change set | Integrate new interviews; emits change set + tree | planned (P2.9) |
| `/opportunity-narrative` | SC | YOU | Opportunity narrative | Write up chosen opp for validation | planned (P2.12) |
| `/discovery-update` | SC | YOU (weekly) | Stakeholder Update | Weekly digest | planned (P2.14) |
| `/audit-discovery-coherence` | SC | YOU | Audit Report | Flag OSTs without parent intent | planned (P2.11) |
| `interview-coder` | AG | CLAUDE (fan-out) | Insight set | One transcript | planned (P2.3) |
| `opportunity-merger` | AG | CLAUDE (fan-out) | Merge decision | One OST node on `/update-ost` | planned (P2.10) |
| `discovery-coach` | AG | CLAUDE (dispatch) | Coaching | Continuous Discovery coaching | planned (P2.13) |
| `interview-snapshot` | SK | CLAUDE | Speakers + quotes | Speaker detection + time alignment | planned (P2.2) |
| `opportunity-clustering` | SK | CLAUDE | Cluster set | Theme raw opportunities | planned (P2.5) |
| `ost-validator` | SK | CLAUDE | Validation verdict | Validate-then-repair loop (prose procedure shipped; runnable script + reference files planned P2.8) | shipped (prose) |
| Continuous Discovery | REF | (pulled) | — | `context/frameworks/continuous-discovery.md` | planned (F4.1) |
| OST schema | REF | (pulled) | — | `context/frameworks/opportunity-solution-tree.md` | planned (F4.2) |

## Phase 3 — Validation

| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/assumption-test` (design) | SC | YOU | Assumption Map | Five-lens design | planned (P3.1) |
| `/design-experiment` | SC | YOU | Experiment | Runnable experiment with predeclared threshold | planned (P3.4) |
| `/test-cost-vs-evidence` | SC | YOU | Test Prioritization | Cost vs evidence-needed | planned (P3.6) |
| `/run-assumption-test` | SC | YOU | Experiment Result | Capture results; computes pass/fail | planned (P3.7) |
| `/falsify-or-confirm` | SC | YOU | Learning Memo | Write memo; flip status; propagate | planned (P3.8) |
| `/kill-or-survive` | SC | YOU | Opportunity Disposition | Formal disposition | planned (P3.9) |
| `/learning-memo` | SC | YOU | Learning Memo | Synthesize learning | planned (P3.10) |
| `/validation-update` | SC | YOU (weekly) | Stakeholder Update | Weekly digest | planned (P3.13) |
| `/audit-assumption-coverage` | SC | YOU | Audit Report | Flag chosen opps without assumption map | planned (P3.11) |
| `/audit-vision-evidence` | SC | YOU | Audit Report | Flag visions citing untested assumptions | planned (P3.12) |
| `assumption-skeptic` | AG | CLAUDE (dispatch) | Review | "Would you pull the work?" check | planned (P3.2) |
| `experiment-designer` | AG | CLAUDE (dispatch) | Test proposal | Cheapest valid test | planned (P3.5) |
| `experiment-template` | SK | CLAUDE | Scaffold | Experiment folder structure | planned (P3.3) |
| Assumption taxonomy | REF | (pulled) | — | `context/frameworks/assumption-tests.md` | planned (F4.4) |
| Falsification | REF | (pulled) | — | `context/frameworks/falsification.md` | planned (F4.5) |
| Validation theatre | REF | (pulled) | — | `context/frameworks/validation-theatre.md` | planned (F4.6) |

## Phase 4 — Delivery (Vision → Initiative → Spec → Handoff Packet)

### Vision (4A)
| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/draft-vision` | SC | YOU | Vision, Value Prop, Differentiator | From learning + persona + product | shipped (2026-05-23) |
| `/vision-shape-check` | SC | YOU | Shape Decision | Crosses teams? Initiative or single spec? | planned (P4.2) |

### Initiative (4B)
| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/draft-initiative` | SC | YOU | Initiative, Capability list | Build initiative folder | shipped (2026-05-23) |
| `/context-map` | SC | YOU | Bounded Contexts, Evolution Check | Interactive context map | shipped (2026-05-23) |
| `/end-to-end-flow` | SC | YOU | Business Workflow | Cross-team flow (Mermaid) | shipped (2026-05-23) |
| `/sequence-initiative` | SC | YOU | Dependency Sequence | Delivery sequence | shipped (2026-05-23) |

### Spec (4C)
| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/draft-spec` | SC | YOU | Requirement, Acceptance Criteria, Business Rule | From initiative + context-map row + EARS | shipped (2026-05-23) |
| `/spec-impact-analysis` | SC | YOU | Impact Report | What changes if this spec changes? | planned (P4.9) |
| `/audit-spec-linkage` | SC | YOU | Audit Report | Every spec needs `parent_initiative:` | planned (P4.10) |

### Engineering handoff (4D — NEW in v3)
| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/handoff-packet` | SC | YOU | Handoff Packet | Assemble the ontology-defined 23-section deliverable | shipped (2026-05-23) |
| `/audit-completeness` | SC | YOU | Audit Report | 25-item pre-handoff checklist | shipped (script + prose fallback) |
| `/audit-traceability` | SC | YOU | Audit Report | Walk the seven traceability rules | shipped (script + prose fallback) |
| `adversarial-reviewer` | AG | CLAUDE (dispatch) | Review | Default reviewer; artifact-vs-contract drift | shipped |
| `compliance-reviewer` | AG | CLAUDE (dispatch) | Review | Regulatory / legal / privacy / ethics lens | planned (P6.1) |
| `quality-engineer` | AG | CLAUDE (dispatch) | Review | Testability / observability / reliability lens | shipped |
| `traceability-walker` | AG | CLAUDE (fan-out) | Audit Report | Per-subtree traceability shell-out (wraps F1.4) | shipped |
| `voice-check` | SK | CLAUDE | Voice rubric | For customer-facing drafts | planned (P8.4) |
| `ears-lint` | SK | CLAUDE | EARS check | Spec sentence pattern | planned (P4.7) |
| `ontology-classifier` | SK | CLAUDE | Object types + links | Extract typed objects from input | shipped |
| `work-loop` | SK | CLAUDE | Standard pattern | Plan → execute → verify → review | shipped |

### Across delivery
| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/release-notes` | SC | YOU | Customer Communication | Customer-facing notes | planned (P4.12) |
| `/launch-comms` | SC | YOU | Customer Communication | Internal + external launch messaging | planned (P4.13) |
| `/launch-checklist` | SC | YOU | Launch Plan | Change-type checklist | planned (P4.14) |
| `/retro` | SC | YOU | Retro | Facilitated retro | planned (P4.15) |
| `roadmap-skeptic` | AG | CLAUDE (dispatch) | Review | Bets vs commitments lens | planned (P4.16) |
| `section-fact-checker` | AG | CLAUDE (fan-out) | Fact check | One section at a time | planned (P8.9) |

## Phase 5 — Landings

| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/landing-report` | SC | YOU | Landing Report | Actuals vs predictions vs counter-metrics | planned (P5.1) |
| `/adoption-readout` | SC | YOU | Adoption Curve | Adoption only | planned (P5.2) |
| `/outcome-vs-prediction` | SC | YOU | KPI Diff | Mechanical comparison | planned (P5.3) |
| `/cohort-analysis` | SC | YOU | Cohort breakdown | Slice by segment / surface / cohort | planned (P5.4) |
| `/landing-interview` | SC | YOU | Insight | Qualitative follow-up | planned (P5.6) |
| `/landings-update` | SC | YOU | Stakeholder Update | Stakeholder digest | planned (P5.8) |
| `/audit-landings-debt` | SC | YOU | Audit Report | Flag shipped initiatives without landing report after 30 days | planned (P5.9) |
| `cohort-analyst` | AG | CLAUDE (fan-out) | Cohort report | One cohort at a time | planned (P5.5) |
| `landing-skeptic` | AG | CLAUDE (dispatch) | Review | "What would have to be true to revert?" | planned (P5.7) |
| `landings-manager` | SCH | CRON (Wed 7am) | Debt scan | Mid-week landings-debt scan | planned (P5.10) |

## Cross-cutting

### Communication
| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/stakeholder-update` | SC | YOU (weekly/monthly) | Stakeholder Update | Auto-compose from current state | planned (P8.1) |
| `/exec-narrative` | SC | YOU | Exec Narrative | 6-pager on a strategic question | planned (P8.2) |
| `/battlecard` | SC | YOU | Sales Enablement | One-competitor battlecard | planned (P8.3) |
| `/headlines` | SC | YOU | Headline candidates | 3–5 × 7 categories | planned (P8.5) |
| `/seo` | SC | YOU | SEO Analysis | Content + keyword + volume | planned (P8.6) |
| `/critique` | SC | YOU | Review | Direct feedback on a draft | planned (P8.7) |
| `writing-critic` | AG | CLAUDE (dispatch) | Voice-aware review | (in writing surfaces) | planned (P8.8) |

### Research
| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/research-digest` | SC | YOU (daily) | Research Digest | Academic + industry | planned (P8.10) |
| `/summarize-paper` | SC | YOU | Paper Summary | Structured summary of one PDF | planned (P8.11) |
| `paper-summarizer` | AG | CLAUDE (fan-out) | Summary | One paper in parallel | planned (P8.12) |

### Personal OS
| Artifact | Block | Inv | Produces (output) | Purpose | Status |
|---|---|---|---|---|---|
| `/today` | SC | YOU (morning) | Daily Plan | Tasks + AI-helpable surfacing | planned (P9.2) |
| `/inbox` | SC | YOU | Triage | Triage and file inbox | planned (P9.3) |
| `/meeting-prep` | SC | YOU | Meeting Brief | Prep for next event | planned (P9.4) |
| `/weekly-retro` | SC | YOU (Friday) | Retro | Session patterns | planned (P9.5) |
| `/phase-guide` | SC | YOU (when stuck) | Phase Diagnosis | "What do you have right now?" | shipped |
| `dates` | SK | CLAUDE | Date facts | today/tomorrow/this-week/next-week | planned (P9.1) |
| Personal OS scheduled agents (`podcast-manager`, `sales-admin`, `coding-manager`, `discovery-manager`, `validation-manager`) | SCH | CRON (various) | Tasks / Retro | Daily 6am + Mon 7-8am rhythm agents; depend on `personal-os/agents/` runtime dir (also planned) | planned (P9.6 — `sched-personal-os-agents`, single atomic ROADMAP item covering all five) |
| `cadence-manager` | SCH | CRON (1st Mon monthly) | Cadence Report | Monthly cadence-drift report | planned (P7.6) |

---

## Global hooks (phase guards)

> All SCH (scheduled agent) entries depend on the `personal-os/agents/` runtime directory, which ships empty. The directory must be populated before any scheduled agent can run. See ROADMAP P9.6.
>
> Six hook scripts ship as of 2026-05-21 and are wired in `.claude/settings.json` (F2.6, 2026-05-21). Every new session in this repo registers them with Claude Code's tool-use lifecycle.

| Hook | Event(s) | Script | Action | Status |
|---|---|---|---|---|
| `check-handover-link` | PreToolUse(Write, Edit, MultiEdit) | `scripts/check-handover-link.py` | Refuse writes to phase artifacts without a required `parent_*` frontmatter link (per HANDOVERS.md) | shipped 2026-05-21 (F2.1) — wired (F2.6, 2026-05-21) |
| `assumption-threshold-lock` | PreToolUse(Write on `validation/experiments/**/results.md`) | `scripts/check-assumption-threshold.py` | Refuse experiment-results writes unless a sibling `experiment.md` with `predeclared_threshold` predates the write | shipped 2026-05-21 (F2.2) — wired (F2.6, 2026-05-21) |
| `ontology-type-check` | PreToolUse(Write, Edit, MultiEdit) | `scripts/check-ontology-type.py` | Warn (never block) when an artifact path implies an `object_type:` but frontmatter omits or mismatches it | shipped 2026-05-21 (F2.3) — wired (F2.6, 2026-05-21) |
| `mode-guard` | SessionStart + UserPromptExpansion + PreToolUse(Skill) | `scripts/mode-guard.py` | Block wrong-mode slash-command invocations; surface active mode at session start | shipped 2026-05-21 (F2.4) — wired (F2.6, 2026-05-21) |
| `cadence-nudge` | SessionStart | `scripts/cadence-nudge.py` | Surface drift signals (stale strategy >90d, orphan OST >30d, kill-drought >60d) as session context | shipped 2026-05-21 (F2.5) — wired (F2.6, 2026-05-21) |
| `guard-credentials` | PreToolUse(Bash, Write, Edit, MultiEdit, Read) | `scripts/guard-credentials.py` | Hard-block tool calls touching `~/.ssh`, `.env*`, `~/.kube/config`, `~/.npmrc`, `~/.pypirc`, `~/.netrc`, `.pem`/`.key`, credential dirs | shipped 2026-05-21 (F2.8) — wired (F2.6, 2026-05-21) |
| `pin-date` | SessionStart | (planned) | Run dates script | planned (F2.9; depends on P9.1 skill-dates) |
| `validate-ost` | PostToolUse(Write on `discovery/trees/**`) | (planned) | Run OST validator; abort on failure | planned (F2.7; depends on P2.8 script-ost-validator) |

---

## Read-the-source map

| Kit concept | Source |
|---|---|
| Four-phase operating model (Strategy / Discovery / Validation / Delivery) | `product-operating-model.md` + Rumelt/Perri/Torres/Cagan |
| Five-phase model (kit adds Landings) | Operating model + 2026 industry consensus "landings not launches" |
| Handovers as artifacts | `product-operating-model.md` |
| Phase-guard hooks | Operating model made mechanical |
| Greenfield vs enterprise mode | Both source docs |
| Cadence rhythms + drift detector | Operating model's "cadence collapse" failure mode |
| Strategic coherence audit | Rumelt + 2025/26 incoherence research |
| Validation theatre detector | Operating model failure #4 + Bland & Osterwalder |
| Landings phase + audit-landings-debt | Google's "landings not launches" reframe |
| **Product/business ontology (8 domains + kit-composite Domain I, 82 documented types)** | **`product_business_knowledge_ontology_agent_handoff.md`** (source: 74 atomic; kit-composite Domain I adds 8 — see `context/frameworks/ontology.md`) |
| **Universal metadata schema** | **Ontology section 13** |
| **Traceability rules + `/audit-traceability`** | **Ontology section 32** |
| **`/audit-completeness` (25-item checklist)** | **Ontology section 41** |
| **Engineering Handoff Packet (Domain H)** | **Ontology section 28** |
| **Human-vs-AI ownership model** | **Ontology sections 23–26** |
| **`ontology-classifier` skill** | **Ontology section 2 (agent guidance)** |
| **`AGENTS.md` as canonical context** | **agent-ready-repo template** |
| **Source-of-truth table** | **agent-ready-repo AGENTS.md** |
| **Charter / ADR / RFC structure** | **agent-ready-repo docs/ layout** |
| **`work-loop` skill (plan→execute→verify→review)** | **agent-ready-repo work-loop, reshaped for PM work** |
| **`adversarial-reviewer` / `compliance-reviewer` / `quality-engineer`** | **agent-ready-repo specialist subagents, reshaped** |
| **"When this file is wrong, flag drift" discipline** | **agent-ready-repo AGENTS.md** |
| Files-as-memory; markdown over uploads | Torres, *Claude Code: What It Is* |
| /competitive-research parallel fan-out | Torres, same article |
| Three-layer memory (Global / Project / Reference) | Torres, *Stop Repeating Yourself* |
| Slash commands vs agents vs skills vs hooks vs plug-ins | Torres, *How to Use Claude Code (Features)* |
| Context-rot meter + /compact + /clear | Torres, *Context Rot* |
| Scheduled team-of-agents | Torres, *My Team of Agents* |
| Show-the-model's-work + agent repair loop | Torres, *Behind the Scenes: AI-OSTs* |
