# Agents

Specialist subagents with sharp, differentiable lenses. The orchestrator dispatches one (or a small set) per artifact; do NOT run every agent on every artifact.

For the canonical narrative referenced from `AGENTS.md`, see the [Specialist subagents](../../AGENTS.md#specialist-subagents) section. This file is the on-disk index — what's actually shippable today vs. what's planned.

## Shipped

- **[`adversarial-reviewer`](adversarial-reviewer.md)** — the default reviewer for any non-trivial kit artifact. Looks for drift between the artifact and its handover contract, missing edge cases, scope creep, hidden assumptions, vague language, and fluff. Runs after audit gates pass and before declaring an artifact complete. Verdicts: `pass` / `needs-fixes` / `block`.
- **[`competitor-research`](competitor-research.md)** — fan-out worker that researches one named competitor end-to-end (positioning, features, pricing, recent moves). Writes findings to `market/competitors/<slug>.md`. Greenfield mode only; consumed by `/competitive-research`.
- **[`quality-engineer`](quality-engineer.md)** — testability, observability, reliability, maintainability lens for specs and handoff packets. Asks whether engineering could operationalize the artifact without re-deriving the test plan, observability requirements, SLA, failure-mode coverage, or rollback. Runs after `/audit-completeness` and `adversarial-reviewer`; complements both, replaces neither.
- **[`traceability-walker`](traceability-walker.md)** — fan-out worker dispatched by `/audit-traceability` on large scopes. Runs `scripts/audit-traceability.py` against one upstream subtree at a time and returns a structured per-subtree findings block the orchestrator can aggregate. Never reimplements rules — always shells out to F1.4.

## Planned — reviewers

Listed for completeness; not currently shippable. Build queue in [`ROADMAP.md`](../../ROADMAP.md).

- `compliance-reviewer` *(planned — [ROADMAP P6.1](../../ROADMAP.md#phase-6--reviewer-agents-and-the-work-loop-closure))* — regulatory, legal, privacy, ethics lens. Use when an artifact touches user data, claims, pricing, safety, or regulated workflows. Complements human legal/compliance review; does not replace it.

## Planned — phase skeptics

Phase-specific challengers, invoked when a phase's signature artifact is being drafted or reviewed.

- `strategy-skeptic` *(planned — [ROADMAP P7.3](../../ROADMAP.md#phase-7--phase-1-strategy-commands-the-missing-ones))* — challenges strategy drafts with Rumelt's failure modes (list-of-goals, no diagnosis, incoherent actions).
- `discovery-coach` *(planned — [ROADMAP P2.13](../../ROADMAP.md#phase-2--discovery-commands))* — Continuous Discovery coaching; auto-invoke when stuck on an opportunity.
- `assumption-skeptic` *(planned — [ROADMAP P3.2](../../ROADMAP.md#phase-3--validation-commands))* — "would you actually pull the work?" theatre detector for validation artifacts.
- `roadmap-skeptic` *(planned — [ROADMAP P4.16](../../ROADMAP.md#phase-4--delivery-and-engineering-handoff))* — bets-vs-commitments lens on the roadmap.
- `landing-skeptic` *(planned — [ROADMAP P5.7](../../ROADMAP.md#phase-5--landings))* — "what would have to be true for us to revert?" lens for landing reports.

## Planned — fan-out workers

Parallel-dispatch agents that handle one unit of work at a time.

- `interview-coder` *(planned — [ROADMAP P2.3](../../ROADMAP.md#phase-2--discovery-commands))* — one transcript at a time.
- `opportunity-merger` *(planned — [ROADMAP P2.10](../../ROADMAP.md#phase-2--discovery-commands))* — one OST node on `/update-ost`.
- `experiment-designer` *(planned — [ROADMAP P3.5](../../ROADMAP.md#phase-3--validation-commands))* — proposes the cheapest valid test.
- `cohort-analyst` *(planned — [ROADMAP P5.5](../../ROADMAP.md#phase-5--landings))* — one cohort at a time.
- `writing-critic` *(planned — [ROADMAP P8.8](../../ROADMAP.md#phase-8--communication-and-research))* — voice-aware review dispatched by `/critique`.
- `section-fact-checker` *(planned — [ROADMAP P8.9](../../ROADMAP.md#phase-8--communication-and-research))* — one section at a time.
- `paper-summarizer` *(planned — [ROADMAP P8.12](../../ROADMAP.md#phase-8--communication-and-research))* — one paper at a time.

## Planned — scheduled agents

Long-lived, headless. Run on a cron schedule against their identity file in `personal-os/agents/` *(directory ships empty until scheduled agents land)*. Each runs the `work-loop` headless against its own brief.

- `landings-manager` *(planned — [ROADMAP P5.10](../../ROADMAP.md#phase-5--landings) `sched-landings-manager`)* — Wed 7am — mid-week landings-debt scan.
- `cadence-manager` *(planned — [ROADMAP P7.6](../../ROADMAP.md#phase-7--phase-1-strategy-commands-the-missing-ones) `sched-cadence-manager`)* — first Monday monthly — cadence-drift report.
- `sched-personal-os-agents` *(planned — [ROADMAP P9.6](../../ROADMAP.md#phase-9--personal-os))* — bundle covering `podcast-manager`, `sales-admin`, `coding-manager`, `discovery-manager`, `validation-manager`.

## How agents are built

Per the kit's `work-loop` doctrine. Every new agent:

1. Has a spec under `docs/specs/<slug>/spec.md` and a plan under `docs/specs/<slug>/plan.md`.
2. Passes pre-EXECUTE adversarial review on its spec + plan.
3. Implements per the agent definition shape — frontmatter with `name`, `description`, `tools`, `model`; body that declares when invoked, inputs, outputs, hard rules.
4. Passes `tools/lint-agent.sh` on its `.md` file.
5. Passes post-EXECUTE adversarial review on the implementation.
6. Gets a row added to `docs/INVENTORY.md` and a check-mark on its ROADMAP item.

See [`../skills/work-loop/SKILL.md`](../skills/work-loop/SKILL.md) for the full mechanics. See [`adversarial-reviewer.md`](adversarial-reviewer.md) for the canonical reviewer-agent shape.
