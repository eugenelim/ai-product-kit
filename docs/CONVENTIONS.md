# Conventions

How work happens in this kit. The Charter is the constitution; this is the operating manual.

## File conventions

- Markdown with YAML frontmatter for every product artifact that isn't code (kit-meta scaffolding — specs, plans, state — is exempt; see §"Specs and Plans").
- Kebab-case filenames. ISO dates (`YYYY-MM-DD`) when temporal: `2026-05-20-stakeholder-update.md`.
- Slugs in frontmatter match the filename stem (without extension and date prefix).
- Cross-links use kit-relative paths: `parent_intent: ../intents/north-star-retention.md`.

## Universal metadata schema

Every product artifact carries the frontmatter block below (kit-meta scaffolding — specs, plans, state — is exempt; see [§"Exempt from the universal metadata schema"](#exempt-from-the-universal-metadata-schema) below). **Universally required fields** (enforced by `tools/lint-frontmatter.py`): `object_type`, `status`, `last_updated`. All other fields are **required where applicable** per the artifact's phase-specific handover contract in `docs/HANDOVERS.md` and are checked by `/audit-completeness`, not by the linter. A reader producing a compliant artifact needs both this schema AND the relevant handover contract.

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

# Human-vs-AI ownership (every product artifact must declare this)
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

### Exempt from the universal metadata schema

Specs (`docs/specs/<feature>/spec.md`), plans (`plan.md`), and state files (`state.json`) do not carry the universal-metadata YAML frontmatter. The exemption rests on three facts:

- Specs use the **kit-build lifecycle track** (`Draft → In Review → Approved → Implementing → Shipped → Frozen`), which is separate from the product-artifact track and has different downstream consumers.
- The **markdown bullet block under the spec's H1** (Status, Plan, State, Component type, Serves kit phase, Constrained by) IS the spec's metadata surface. It carries the same information the universal schema does for product artifacts.
- `tools/lint-frontmatter.py` walks only `PHASE_DIRS = ["strategy", "discovery", "validation", "delivery", "market"]`. Universal-schema frontmatter on a spec under `docs/specs/` would never be enforced.

Adding `kit-spec` as an ontology type was considered and rejected: `context/frameworks/ontology.md` §"When the ontology is wrong" warns against ad-hoc additions, and Domain I composites are explicitly phase-boundary handovers — not kit-build scaffolding.

### Templates — `templates/<slug>.md`

The kit ships per-ontology-type templates under `templates/`. Each template is a literal skeleton a kit user copies and fills to produce a real product artifact under `strategy/`, `discovery/`, `validation/`, `delivery/`, or `market/`. Templates are *not* product artifacts themselves — they live outside `PHASE_DIRS` and are not linted in default mode.

**File layout.**
- Single-file template: `templates/<slug>.md` (slug matches the ontology-type kebab-case name, e.g., `strategic-intent`, `vision`, `landing-report`).
- Multi-file template (folders such as Initiative, Handoff Packet): `templates/<slug>/` containing a `README.md` plus the per-child-file templates. The folder's `README.md` carries the universal-schema frontmatter; child files carry their own type-specific frontmatter if and only if they instantiate distinct ontology objects.

**Placeholder syntax.** Use angle-bracket placeholders exactly as in `docs/HANDOVERS.md`: angle brackets wrap a descriptor with no whitespace between bracket and content, e.g. `<one sentence>`, `<YYYY-MM-DD>`, `<OPP-NNN>`. The linter requires at least one non-whitespace character inside the brackets — `<>` and `< >` are rejected. Curly-brace and double-underscore styles are not used.

**Frontmatter ordering.** Universal-metadata schema fields (per §"Universal metadata schema") appear first, in the order shown there. Handover-specific fields (per `docs/HANDOVERS.md`) appear in a second block under a `# Handover-specific fields` YAML comment. This makes diffs across templates trivial to read.

**Pre-fill vs placeholder.** A field whose value is the *template's identity* is pre-filled (e.g., `object_type: Strategic Intent` in `templates/strategic-intent.md` — the type is known, not a user choice). Every other field is a placeholder. The `status:` field is pre-filled to `Draft` — this is the entry state of the **product-artifact lifecycle track** (per CONVENTIONS.md §"Lifecycle states"), which is what the instantiated artifact (not the template file itself) will inherit when a kit user copies the template. The template file as a kit-build component lives on a separate lifecycle track that is managed via its companion spec under `docs/specs/template-<slug>/`, not via the template's YAML body.

**Required vs optional sections.** Required sections (per the relevant `HANDOVERS.md` row) appear in the template body verbatim. Optional sections appear under a single `## Optional sections` heading at the bottom of the template, each with a one-line description of when to use it. Authors of derived artifacts delete unused optional sections; required sections must remain.

**Linter contract.** Templates pass `tools/lint-frontmatter.py --check-template <path>`, which accepts angle-bracket placeholders where concrete values would otherwise be required. Default mode (which walks `PHASE_DIRS`) does not walk `templates/` and is unchanged. The contract test at `scripts/tests/test_templates_instantiate.py` runs `--check-template` against every template in CI.

**Authoring a new template.** Copy `templates/_meta/template-skeleton.md`. Read the relevant `docs/HANDOVERS.md` row for the handover this template gates. Fill the spec under `docs/specs/template-<slug>/` first (the F3 block in `ROADMAP.md` lists ten such specs as worked examples).

### Phase-4 Template-Fill Commands — `.claude/commands/draft-*.md` and siblings

Seven slash commands in Phase 4 (Delivery) share a single behavioral shape: read a parent product artifact → consume a kit-provided F3.x template (single file or folder) → walk the template's placeholders interactively with a single human → write the filled artifact under `delivery/` → run `tools/lint-frontmatter.py` (default mode) against the written file → emit a "next command in the chain" hint. The seven split into two sub-classes:

- **Artifact-creating commands** (4): `/draft-vision` (P4.1), `/draft-initiative` (P4.3), `/draft-spec` (P4.8), `/handoff-packet` (P4.11). These take a new-artifact slug as their positional argument and write to a *new* destination path (`delivery/visions/<slug>.md`, `delivery/initiatives/<slug>/`, `delivery/initiatives/<initiative-slug>/specs/<spec-slug>/`, `delivery/handoff-packets/<slug>/`). They pre-fill an `id:` derived from the slug.
- **Artifact-augmenting commands** (3): `/context-map` (P4.4), `/end-to-end-flow` (P4.5), `/sequence-initiative` (P4.6). These take an *existing* initiative slug as their positional argument and write (or replace) a specific child file within `delivery/initiatives/<initiative-slug>/` (`context-map.md`, `flow.md`, `sequence.md` respectively). They do **not** create a new artifact; they fill a placeholder child within an existing folder. They do not pre-fill `id:` (no new artifact).

The other nine ROADMAP P4.x items (analytical commands, audits, comms commands, the retro facilitator, the EARS-lint skill, the roadmap-skeptic agent) are out of scope; they ship under their own per-item specs.

**Body structure.** Every in-scope command's body has these H2 sections, in this order:
1. `## When to run` — bulleted list of triggers.
2. `## Inputs` — numbered list. First item is always "the slug (positional arg)"; second is always the template-path the command consumes; subsequent items name parent-artifact-resolution rules and any other input.
3. `## Procedure` — numbered Step-N sub-sections. Procedure must include, at minimum: Step 1 — resolve parent artifact; Step 2 — instantiate template at destination; Step 3 — walk placeholders one section at a time (NEVER batch — restates the kit's interactivity contract from `.claude/CLAUDE.md`); Step 4 — surface `human_owned_decisions:` for explicit human confirmation; Step 5 — run `tools/lint-frontmatter.py <written-path>` and report the result; Step 6 — emit the "next command in the chain" hint.
4. `## What this command will not do` — bulleted list of explicit non-behaviors. At minimum: "Not overwrite an existing artifact at the destination without `--force`"; "Not skip the `human_owned_decisions:` confirmation step"; "Not fabricate evidence — if the parent artifact lacks a referenced field, ask, do not invent"; "Not batch placeholder questions — one at a time".

**Frontmatter.** Required keys: `description:` (≤ 1024 chars; one-sentence purpose; the slash-command palette renders this) and `argument-hint:` (string, see Argv contract below). No other frontmatter keys.

**Argv contract.** First positional argument is a kebab-case identifier matching `^[a-z0-9-]+$` and ≤ 80 chars, naming the *operated-upon* artifact:
- For **artifact-creating commands**, the positional is `<slug>` — the slug of the new artifact to be created.
- For **artifact-augmenting commands**, the positional is `<initiative-slug>` — the slug of the existing initiative folder whose child file the command fills.

The `argument-hint:` frontmatter value names the positional explicitly using one of those two tokens (literal `<slug>` or literal `<initiative-slug>`) so the contract test can distinguish the two sub-classes. Optional flags follow:
- `--from <parent-slug>` — explicit parent-artifact selection; overrides auto-detection.
- `--force` — permit overwriting an existing artifact at the destination (creating commands) or an already-filled child file (augmenting commands).
- `--dry-run` is **not** part of the convention (deferred per Open Question 3).

Example `argument-hint:` values: `<slug> [--from <parent-slug>] [--force]` (creating); `<initiative-slug> [--force]` (augmenting — `--from` is not applicable because the parent is the initiative itself, named by the positional).

**Parent-artifact resolution.** Applies to artifact-creating commands; augmenting commands skip this step (the parent — the initiative folder named by the positional `<initiative-slug>` — is already named explicitly). If `--from <parent-slug>` is given, use it. Otherwise, list the candidate parent artifacts (the family directory's contents) filtered by `status:` not in the **terminal-or-killed set**: `Deprecated` (product-artifact track per `docs/CONVENTIONS.md` §"Lifecycle states"), plus `killed` for Learning Memos (per `docs/HANDOVERS.md` Handover 3, where Learning-Memo `status:` is `survived | killed`). If the candidate list exceeds 10, present the 10 most recently updated (sorted by `last_updated:` descending) and suggest `--from <parent-slug>` for explicit selection of an older candidate. If the candidate list is empty, exit with code 2 and a remediation suggestion naming the prerequisite command. Always confirm even when only one candidate exists (per Open Question 7). **Never silently pick** — the auto-pick failure mode is the silent failure HANDOVERS-4/5/6 are designed to prevent (a vision draft attached to the wrong learning memo, an initiative attached to the wrong vision).

**Interactive fill.** Walk the template's placeholders **one H2 section at a time**. If an H2 contains H3 sub-sections, treat each H3 as a separate fill unit; do not advance to the next H2 until every H3 within the current H2 is confirmed. Within a section: ask the human one question per placeholder, sequentially. **Never batch.** Confirm the section's filled content before advancing. The kit's "one clarifying question at a time" rule from `.claude/CLAUDE.md` is load-bearing here.

**Pre-fill rules.** Before asking the human anything, the command pre-fills the mechanical fields the template's frontmatter declares as placeholders:
- `id:` — derived from slug per the ontology type prefix (e.g., a Vision is `VIS-<NNN>` where `<NNN>` is the next unused integer in `delivery/visions/`).
- `slug:` — the positional argument.
- `created:` — today's date, ISO-8601, resolved from the system clock at command-start.
- `last_updated:` — same as `created` on first instantiation.
- `parent_*:` fields — resolved parent slug from the resolution step above.
- `object_type:` — already pre-filled in the template per the F3 authoring convention; the command re-asserts it (a defensive check).

The human is never asked to type a mechanical field. If a mechanical field cannot be resolved (e.g., no parent artifact exists), the command stops and reports the missing pre-condition with a remediation suggestion (e.g., "no learning memo found in `validation/learnings/` — run `/learning-memo` first").

**Linter integration.** After the interactive fill completes, the command resolves the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py` (do not assume the working directory is the repo root), then runs `python3 tools/lint-frontmatter.py <written-artifact-path>` (default mode, NOT `--check-template` — the artifact is now a real product artifact, not a template) and surfaces the linter's exit code and any errors to the human. If the linter exits non-zero, the command does not declare success; it offers to re-open the relevant sections for correction.

**Exit codes.**
> - `0` — artifact written, linter passed, next-command hint emitted.
> - `1` — human aborted the interactive walk before completion (artifact left at its partial state on disk; the command emits a "resume by re-running with the same slug" hint).
> - `2` — pre-conditions failed (no parent artifact, slug malformed, destination already exists without `--force`, template path missing, candidate parent list empty). Artifact not written.
> - `3` — artifact was written but the post-fill linter exited non-zero; the command offered to re-open relevant sections for correction and the human declined (or accepted but did not re-run the lint). Artifact persists on disk in a known-imperfect state. Automation consumers MUST treat exit 3 as distinct from exit 0 (the file exists but its frontmatter does not pass the kit's default-mode linter).

**Chaining hint.** The command's last output line names the next command in the Phase 4 chain, formatted exactly: `NEXT: /<command-name> <slug>`. The chain is `/draft-vision` → `/draft-initiative` → (`/context-map`, `/end-to-end-flow`, `/sequence-initiative` in any order) → `/draft-spec` (per child spec) → `/handoff-packet`. `/handoff-packet`'s NEXT line names `/audit-completeness <slug>` (Phase 5 entry, the existing command). If a chain successor is not yet shipped, the NEXT line uses the canonical name plus `(planned — ROADMAP P<row>)` per the kit-drift policy.

**Capabilities-file interstitial.** `delivery/initiatives/<slug>/capabilities.md` is HANDOVERS-5 required content but has no dedicated Phase-4 command (capabilities are typically populated incidentally during `/draft-initiative`'s Step-3 walk). `/sequence-initiative`'s NEXT line MUST therefore include a reviewer-prompt second line: `REVIEW: delivery/initiatives/<slug>/capabilities.md — verify the Capability list is filled and each row traces to a parent Problem before running /draft-spec.` This is a NEXT-output additional line, not an automated check; the human is responsible for the review. Other commands in the chain do not emit a REVIEW line.

**Authoring a new in-scope command.** Copy `.claude/commands/_meta/command-skeleton.md`. Read the relevant `docs/HANDOVERS.md` row (4, 5, or 6) for the artifact this command produces. Read the F3.x template the command will consume. Fill the per-command spec under `docs/specs/cmd-<verb>/` first; the `per-command-spec-checklist.md` in this convention's `notes/` enumerates what that spec must include.

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
