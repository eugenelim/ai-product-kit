# Skills

Workflows used enough to deserve a name. Skills encode constraints you would otherwise re-derive. Load with `Skill <name>` (or `/<name>` when invoked as a command).

For the canonical list referenced from `AGENTS.md`, see the [Skills available to you](../../AGENTS.md#skills-available-to-you) section. This file is the on-disk index — what's actually shippable today vs. what's planned.

## Shipped

- **[`work-loop`](work-loop/SKILL.md)** — the kit's standard pattern: plan → execute → verify → review → capture. Start here for any non-trivial kit component (skill, agent, command, hook, script, framework ref, template).
- **[`ost-validator`](ost-validator/SKILL.md)** — validate-then-repair loop on Opportunity Solution Tree change sets. Detects orphans, double-deletes, data loss; returns structured pass/fail with specific repair instructions.
- **[`strategy-coherence`](strategy-coherence/SKILL.md)** — bundles the Rumelt-style coherence-audit rule library. Used by `/audit-portfolio-coherence` and when reviewing a proposed initiative against the existing portfolio.
- **[`ontology-classifier`](ontology-classifier/SKILL.md)** — extracts typed objects from unstructured input (transcripts, threads, emails, notes) and proposes classifications against the 76 atomic + 8 composite ontology types. Surfaces missing required fields and confidence labels; never persists.
- **[`ears-lint`](ears-lint/SKILL.md)** — EARS pattern checker for Requirement and Acceptance-Criterion sentences. Classifies each candidate sentence into one of {Ubiquitous, Event-driven, State-driven, Optional-feature, Unwanted-behavior, Complex, Non-conformant} with rationale and suggested rewrite. Consumes `context/frameworks/ears.md` as the rule source.
- **[`interview-snapshot`](interview-snapshot/SKILL.md)** — transforms a raw customer-interview transcript into a proposal block matching the eight-field Interview Snapshot schema from `context/frameworks/interview-snapshot.md`. Adds four operational rules the framework does not specify mechanically: speaker detection, time-aligned quote extraction, paraphrase enforcement, no-recording fallback. Dispatched per transcript by `/interview-snapshot` (planned — P2.1) or the `interview-coder` agent (planned — P2.3). Never persists.
- **[`opportunity-clustering`](opportunity-clustering/SKILL.md)** — themes a list of raw opportunity candidates into clusters by one of three named rules (shared customer behavior / shared workflow step / shared workaround pattern). Candidates without a shared anchor land in an `unclustered:` bucket. Output is a proposal; the skill never persists and never auto-promotes a cluster to an OST Opportunity (downstream `/cluster-opportunities` — planned P2.6 — owns promotion, gated by human acceptance).

## Planned

Listed for completeness; not currently shippable. Build queue in [`ROADMAP.md`](../../ROADMAP.md).

- `experiment-template` *(planned — [ROADMAP P3.3](../../ROADMAP.md#phase-3--validation-commands))* — scaffold the experiment folder per the assumption-test contract.
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
