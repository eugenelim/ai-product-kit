# AGENTS.md

> **This is the canonical agent context file.** `CLAUDE.md` is a symlink to this file (where the filesystem supports it; otherwise treat the two as identical).
> Cursor, Codex, Gemini CLI, and Copilot also read it via their own discovery rules.
>
> Keep this file under ~250 lines. If you're tempted to add more, the content probably belongs in `docs/`, `context/`, `.claude/skills/`, or a domain-specific `AGENTS.md` under one of the phase folders.

## What this repo is

A product manager's operating system, built on two foundations:

- A **four-phase operating model** (Strategy → Discovery → Validation → Delivery → Landings) with each phase gated by a load-bearing handover artifact.
- A **canonical product/business ontology** (eight domains, ~82 documented object types (74 atomic across Domains A–H + 8 composite in Domain I), traceability rules, lifecycle states, and a Human-vs-AI responsibility model).

The detailed map of what lives where is in [`docs/architecture/overview.md`](docs/architecture/overview.md). The phase-by-phase guide is in [`docs/PHASE-GUIDE.md`](docs/PHASE-GUIDE.md). The artifact contracts at every phase boundary are in [`docs/HANDOVERS.md`](docs/HANDOVERS.md). Read those before exploring — they'll save you 20 minutes of grep.

## Source of truth

For each kind of decision or knowledge, there is exactly one place it lives.

| Question | Where it lives |
|---|---|
| What is this kit, and what's in/out of scope? | [`docs/CHARTER.md`](docs/CHARTER.md) |
| What phase am I at right now? | [`docs/PHASE-GUIDE.md`](docs/PHASE-GUIDE.md) — or run `/phase-guide` |
| What artifact closes the phase I'm at? | [`docs/HANDOVERS.md`](docs/HANDOVERS.md) |
| What types of objects can exist, and how do they link? | [`context/frameworks/ontology.md`](context/frameworks/ontology.md) (eight domains + kit-composite Domain I, 82 documented types) |
| Required metadata for any artifact? | [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) — universal metadata schema |
| Who owns decisions — human vs AI? | [`docs/HUMAN-AI-OWNERSHIP.md`](docs/HUMAN-AI-OWNERSHIP.md) |
| Why did we choose X over Y? | [`docs/adr/`](docs/adr/) (Architecture Decision Records — frozen) |
| What should change in the kit, and how? | [`docs/rfc/`](docs/rfc/) (proposals — governance) |
| What exactly does this kit component do? | `docs/specs/<feature>/spec.md` |
| How will we build it, step by step? | `docs/specs/<feature>/plan.md` |
| What's the ordered build queue for the kit? | [`ROADMAP.md`](ROADMAP.md) |
| What's the current strategic bet? | `strategy/intents/<slug>.md` (the canonical handover artifact) |
| What problems are we tracking? | `discovery/opportunities/` + the OSTs in `discovery/trees/` |
| What assumptions are live? | `validation/assumption-maps/<slug>.md` |
| What did we learn from each test? | `validation/learnings/<slug>.md` |
| What are we shipping or have shipped? | `delivery/visions/`, `delivery/initiatives/`, `delivery/specs/` |
| Was it adopted? | `delivery/landings/<slug>.md` |
| How do users use this kit? | [`docs/guides/`](docs/guides/) — Diátaxis: tutorials / how-to / reference / explanation |
| How does Claude do `<repeating task>`? | `.claude/skills/<task>/SKILL.md` |

**If you can't find the answer in one of these places, the answer doesn't exist yet.** Ask, or open an RFC. Don't guess. Guessing creates ontology drift.

## Phase-aware behavior

Before any non-trivial work, identify what **phase** you're at:

1. **Strategy** — entry: org has a decision to make about where to invest; exit: a `strategy/intents/<slug>.md` with central challenge + guiding policy + 3–5 coherent actions
2. **Discovery** — entry: a strategic intent exists; exit: an OST with one opportunity flagged `chosen: true`
3. **Validation** — entry: a chosen opportunity with its riskiest assumption named; exit: a `validation/learnings/<slug>.md` with `status: survived | killed`
4. **Delivery** (Vision → Initiative → Spec → Handoff) — entry: a surviving learning; exit: code in production
5. **Landings** — entry: code in production; exit: a `delivery/landings/<slug>.md` with `verdict: adopt | fix | kill`

If a prior phase's handover artifact is missing, **surface that before doing the work**. The right next step is almost always producing the missing artifact, not skipping ahead.

Phase-skipping is the kit's #1 failure mode, and it's silent. The phase-guard hooks *(planned — see [ROADMAP F2](ROADMAP.md#foundation-2--hook-scripts); only `assumption-threshold-lock` ships today)* catch it at write time; phase-awareness in this file catches it at think time.

## Workflow: the PM work-loop

For anything beyond a one-line edit, follow the **plan → execute → verify → review** loop. The full mechanics are in the [`work-loop`](.claude/skills/work-loop/SKILL.md) skill — load it before non-trivial work. Summary:

1. **Plan before acting.** Identify the phase. Identify the artifact you're producing. Confirm the parent handover artifact exists. State the success criterion before touching the keyboard.

2. **Handover artifacts are validation gates, not write-once docs.** If reality diverges from the intent / OST / learning / vision, update the artifact in the same session. Drift is a bug.

3. **Verification before publication.** Every artifact declares *how* it'll be verified before it's considered complete. Verification modes:
    - **Audit-driven** — run the relevant `/audit-*` command; the artifact passes when the audit returns clean
    - **Human review** — the artifact is sent to its named decision owner for sign-off (see [`docs/HUMAN-AI-OWNERSHIP.md`](docs/HUMAN-AI-OWNERSHIP.md))
    - **Repair loop** — structural artifacts (OST change sets, context maps, coherence audits) run deterministic validation; the model fixes its own mistakes in 1–2 turns

4. **Run the audit gate** before declaring done. Audits are listed in [`docs/INVENTORY.md`](docs/INVENTORY.md) under "Audits & guards."

5. **Self-review against the spec.** After the audit passes, run a specialist-reviewer subagent if the artifact warrants it:
    - `adversarial-reviewer` — spec / plan / artifact drift; missing edge cases; scope creep (default for non-trivial artifacts)
    - `compliance-reviewer` *(planned — [ROADMAP P6.1](ROADMAP.md#phase-6--reviewer-agents-and-the-work-loop-closure))* — regulatory, legal, privacy, ethics (use when the artifact touches customer data, claims, pricing, safety, or regulated workflows)
    - `quality-engineer` — testability, observability, reliability, maintainability (use for specs and handoff packets)

6. **Iterate on findings, with a hard cap of five in-session iterations.** If you hit it, stop and re-plan — don't grind.

7. **Capture what you learned** before closing the session — into the right `AGENTS.md`, skill, ADR, or `context/` file.

For unattended work (the scheduled team-of-agents *(planned — [ROADMAP P9.6](ROADMAP.md#phase-9--personal-os) `sched-personal-os-agents`)*), each scheduled agent runs the loop headless against its identity file in `personal-os/agents/` *(directory ships empty; populated as scheduled agents land)*.

## Human-vs-AI responsibility

The kit's operating principle, from the product ontology:

> **AI may assist with analysis, synthesis, drafting, comparison, and consistency checking. Humans must own judgment, accountability, commitments, ethics, prioritization, and final decisions.**

Every artifact carries explicit frontmatter:

```yaml
human_owned_decisions:
  - <decision a human must make personally>
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: true | restricted | not-allowed
human_approval_required: true | false
approvals_obtained:
  - <role>: <YYYY-MM-DD>
```

Areas where AI must never be the final owner: strategic intent selection, customer commitments, legal/compliance approval, pricing decisions, roadmap priority, launch approval, ethical-risk decisions, customer-facing claims. Full catalog in [`docs/HUMAN-AI-OWNERSHIP.md`](docs/HUMAN-AI-OWNERSHIP.md).

## Commands you'll need

```bash
claude                                     # start Claude Code in this folder
/phase-guide                               # what phase am I at, what's next
/audit-portfolio-coherence                 # Rumelt-style coherence audit across the portfolio
/audit-traceability                        # every requirement traces to a problem and evidence?
/audit-completeness <slug>                 # ontology's pre-engineering-handoff checklist
/cadence-check                             # are we drifting on quarterly/monthly/weekly rhythms? (planned — ROADMAP P7.5)
```

Full catalog in [`docs/INVENTORY.md`](docs/INVENTORY.md).

## Skills available to you

`.claude/skills/` contains workflows used enough to deserve a name. Use them when relevant — they encode constraints you would otherwise re-derive.

> **Status note:** items marked *(planned — ROADMAP X)* are listed for completeness; they are forward-looking design intent, not currently shippable. See [`ROADMAP.md`](ROADMAP.md) for the build queue.

- `work-loop` — **start here for any non-trivial artifact** (plan → execute → verify → review)
- `ost-validator` — validate-then-repair loop on OST change sets
- `strategy-coherence` — bundles the coherence-audit rule library
- `voice-check` *(planned — [ROADMAP P8.4](ROADMAP.md#phase-8--communication-and-research))* — voice-guide rubric for customer-facing drafts
- `dates` *(planned — [ROADMAP P9.1](ROADMAP.md#phase-9--personal-os))* — today/tomorrow/this-week/next-week (eliminates the "Claude thinks it's 2024" failure)
- `ears-lint` *(planned — [ROADMAP P4.7](ROADMAP.md#phase-4--delivery-and-engineering-handoff))* — EARS pattern checker for spec sentences
- `ontology-classifier` — extract typed objects from unstructured input and link them per the ontology

Full index in [`.claude/skills/README.md`](.claude/skills/README.md).

## Specialist subagents

`.claude/agents/` contains reviewers with sharp, differentiable lenses. Pick the ones the artifact warrants; don't run all by default.

> **Status note:** items marked *(planned — ROADMAP X)* are listed for completeness; they are forward-looking design intent, not currently shippable. See [`ROADMAP.md`](ROADMAP.md) for the build queue.

- `adversarial-reviewer` — artifact vs. handover-contract drift; missing edge cases; scope creep. Default reviewer; runs after audits pass.
- `compliance-reviewer` *(planned — [ROADMAP P6.1](ROADMAP.md#phase-6--reviewer-agents-and-the-work-loop-closure))* — regulatory, legal, privacy, ethics lens. Use when the artifact touches user data, claims, pricing, safety, or regulated workflows. Complements human legal/compliance review; does not replace it.
- `quality-engineer` — testability, observability, reliability, maintainability lens for specs and handoff packets.

Plus the phase-skeptic agents (`strategy-skeptic` *(planned — ROADMAP P7.3)*, `discovery-coach` *(planned — ROADMAP P2.13)*, `assumption-skeptic` *(planned — ROADMAP P3.2)*, `roadmap-skeptic` *(planned — ROADMAP P4.16)*, `landing-skeptic` *(planned — ROADMAP P5.7)*) and fan-out workers (`competitor-research`, `interview-coder` *(planned — ROADMAP P2.3)*, `paper-summarizer` *(planned — ROADMAP P8.12)*, `cohort-analyst` *(planned — ROADMAP P5.5)*, etc.). Full catalog in [`.claude/agents/README.md`](.claude/agents/README.md).

## Things you should not do without asking

- **Don't skip a phase silently.** Phase guards will block; the right behavior is to surface the missing upstream artifact and recommend producing it first.
- **Don't write experiment results without a predeclared falsification threshold.** The `assumption-threshold-lock` hook will block. This is the kit's most important guard — it separates real validation from theatre.
- **Don't reproduce competitor copy verbatim.** Short attributed quotes only; everything else paraphrased with sources.
- **Don't make commitments on behalf of the human.** Pricing, roadmap, customer-facing claims, legal/compliance approvals — surface as a `human_owned_decisions` entry; do not resolve them yourself.
- **Don't fabricate evidence.** If a number, study, or customer quote isn't sourced, say so. Mark it `Assumption` until evidence exists.
- **Don't create new top-level folders.** The phase structure is intentional. If you think a new one is needed, open an RFC in `docs/rfc/`.
- **Don't touch** `~/.ssh`, credential stores, `.env*`, or push to protected branches. `scripts/guard-credentials.py` (the `guard-credentials` PreToolUse hook) blocks these on Bash, Write, Edit, MultiEdit, and Read with no model-side override; don't even propose them.

## When this file is wrong

Flag drift in your session — don't silently work around it. AGENTS.md-vs-reality drift is the biggest cause of agent-quality decay. Substantive changes to this file go through an RFC in `docs/rfc/`. Small fixes (typos, broken links, a newly added skill or audit) are normal edits.

---

*Synthesized from: the agent-ready-repo template (AGENTS.md pattern, source-of-truth table, lifecycle-aware doc taxonomy, plan→verify→review loop, specialist subagents, "when this file is wrong" discipline); the [product operating model](docs/inspiration/product-operating-model.md) (four phases, handovers as artifacts, cadence rhythms); the [product and business knowledge ontology](docs/inspiration/product_business_knowledge_ontology_agent_handoff.md) (eight domains, traceability rules, lifecycle states, human-vs-AI responsibility); and Teresa Torres's [Claude Code Recipes](https://www.producttalk.org/tag/claude-code-recipes/) series (markdown memory, slash commands, agents, skills, hooks, validate-then-repair, scheduled team-of-agents).*
