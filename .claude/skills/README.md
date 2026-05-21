# Skills

Workflows used enough to deserve a name. Skills encode constraints you would otherwise re-derive. Load with `Skill <name>` (or `/<name>` when invoked as a command).

For the canonical list referenced from `AGENTS.md`, see the [Skills available to you](../../AGENTS.md#skills-available-to-you) section. This file is the on-disk index — what's actually shippable today vs. what's planned.

## Shipped

- **[`work-loop`](work-loop/SKILL.md)** — the kit's standard pattern: plan → execute → verify → review → capture. Start here for any non-trivial kit component (skill, agent, command, hook, script, framework ref, template).
- **[`ost-validator`](ost-validator/SKILL.md)** — validate-then-repair loop on Opportunity Solution Tree change sets. Detects orphans, double-deletes, data loss; returns structured pass/fail with specific repair instructions.
- **[`strategy-coherence`](strategy-coherence/SKILL.md)** — bundles the Rumelt-style coherence-audit rule library. Used by `/audit-portfolio-coherence` and when reviewing a proposed initiative against the existing portfolio.

## Planned

Listed for completeness; not currently shippable. Build queue in [`ROADMAP.md`](../../ROADMAP.md).

- `ontology-classifier` *(planned — [ROADMAP F1.3](../../ROADMAP.md#foundation-1--make-the-existing-audits-run))* — extract typed objects from unstructured input (transcripts, threads, emails) and surface missing required fields. Used by every audit and when classifying inbound material.
- `interview-snapshot` *(planned — [ROADMAP P2.2](../../ROADMAP.md#phase-2--discovery-commands))* — speaker detection + time-aligned quotes for `/interview-snapshot`.
- `opportunity-clustering` *(planned — [ROADMAP P2.5](../../ROADMAP.md#phase-2--discovery-commands))* — theme raw opportunities into clusters.
- `experiment-template` *(planned — [ROADMAP P3.3](../../ROADMAP.md#phase-3--validation-commands))* — scaffold the experiment folder per the assumption-test contract.
- `ears-lint` *(planned — [ROADMAP P4.7](../../ROADMAP.md#phase-4--delivery-and-engineering-handoff))* — EARS pattern checker for spec sentences.
- `wardley-evolution` *(planned — [ROADMAP P7.8](../../ROADMAP.md#enterprise-mode-strategy))* — place value-chain components on the evolution axis (enterprise mode).
- `voice-check` *(planned — [ROADMAP P8.4](../../ROADMAP.md#phase-8--communication-and-research))* — voice-guide rubric for customer-facing drafts.
- `dates` *(planned — [ROADMAP P9.1](../../ROADMAP.md#phase-9--personal-os))* — today/tomorrow/this-week/next-week; eliminates the "Claude thinks it's 2024" failure.

## How skills are built

Per the kit's `work-loop` doctrine. Every new skill:

1. Has a spec under `docs/specs/<slug>/spec.md` and a plan under `docs/specs/<slug>/plan.md`.
2. Passes pre-EXECUTE adversarial review on its spec + plan.
3. Implements with TDD where the contract is compressible, goal-based check otherwise.
4. Passes `tools/lint-skill.sh` on its `SKILL.md`.
5. Passes post-EXECUTE adversarial review on the implementation.
6. Gets a row added to `docs/INVENTORY.md` and a check-mark on its ROADMAP item.

See [`work-loop/SKILL.md`](work-loop/SKILL.md) for the full mechanics.
