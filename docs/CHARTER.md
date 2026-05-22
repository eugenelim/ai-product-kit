# Charter

This file is the kit's one-page constitution. It sets mission, scope, and principles. Substantive changes go through an RFC in `docs/rfc/`. Small edits (typos, broken links) are normal PRs.

## Mission

Give product managers a Claude Code-powered operating system that:

- Enforces **phase discipline** before activity, so the team operates at the right phase rather than skipping ahead.
- Maintains **ontology traceability** across the chain Market → Customer → Problem → Opportunity → Capability → Requirement → Outcome → Launch → Measurement, so engineering receives validated, decision-backed knowledge instead of feature requests.
- Preserves **human accountability** for judgment, ethics, commitments, prioritization, and final decisions, while using AI for synthesis, drafting, comparison, and completeness checking.
- Produces **landings, not launches** — the kit treats the post-release adoption curve as part of the work, not as someone else's problem.

## In scope

- Pre-engineering product work: strategy, discovery, validation, vision, initiative, spec definition through engineering handoff
- Post-launch measurement and the feedback loop into the next strategy cycle
- The mechanical artifacts that gate every phase handover
- The Claude Code primitives (markdown memory, slash commands, agents, skills, hooks, scheduled team-of-agents) that automate or assist the above
- Communication and personal-OS workflows that support PM craft
- Both greenfield and enterprise/brownfield modes

## Out of scope

- Engineering implementation itself (covered by the agent-ready-repo template and per-repo specs/plans)
- Detailed project management (Jira, Linear, Asana mechanics) beyond the personal-OS layer
- Replacing the canonical books and practitioner references
- Producing strategy *on behalf of* a human leader — the kit produces drafts, options, audits, and completeness checks; humans make the strategic calls

## Principles

1. **Phase before activity.** Identify the phase before reaching for a tool. Skipping a phase produces confident output against an unvalidated foundation.

2. **Handovers travel as artifacts, not conversations.** Every phase boundary is gated by a named file with required frontmatter. The phase-guard hooks enforce this mechanically *(today: `assumption-threshold-lock` ships; the remaining phase-guard hooks are planned — see [ROADMAP F2](../ROADMAP.md#foundation-2--hook-scripts))*.

3. **Ontology is the type system.** Every product artifact declares its `object_type:` and uses the universal metadata schema (kit-meta scaffolding is exempt; see [`docs/CONVENTIONS.md`](CONVENTIONS.md) §"Specs and Plans"). Traceability links are required, not optional.

4. **Outcomes over outputs.** Initiatives declare the outcome they serve, not the features they ship. A launch is the start of an adoption curve, not the finish line.

5. **Show the model's work; let it repair its own mistakes.** Structural artifacts (OST change sets, context maps, coherence audits) emit both result and steps. Validation runs. The model fixes its own mistakes in 1–2 turns.

6. **Files are memory.** Markdown on local disk is the canonical store. No vendor lock-in. Three layers: global preferences, project preferences, reference context.

7. **Humans own judgment; AI assists.** The Human-vs-AI ownership model is not aspirational — it lives in artifact frontmatter and the audit chain.

8. **Drift is a bug.** AGENTS.md, ADRs, the ontology, the handover contracts — when reality diverges, fix the doc in the same session. Reality-vs-doc drift is the biggest cause of agent-quality decay.

## Non-goals

- **Not a methodology rollout.** This is a personal POV on how the phases should sequence. Not corporate guidance, not something to mandate across a department.
- **Not a replacement for the books.** The kit is the wiring diagram; Rumelt, Perri, Torres, Cagan, Wardley, Bland are the wires.
- **Not enforced anywhere.** Rhythm comes from discipline; the kit's hooks are guards, not gates. Overrides are allowed but logged.
- **Not finished.** When a phase consistently fails in a way the doc doesn't predict, update the failure-modes section or open an ADR.

## What success looks like

A team using this kit should:

- Be able to name their current strategic intent in one sentence at any moment
- Have an OST less than 35 days old that ties to the intent
- Have at least one assumption killed or survived in the last 14 days
- Have a landing report for every shipped initiative within 30 days of release
- Never produce a spec without a parent initiative; never produce a vision without a parent learning

If any of these is consistently false, the kit isn't being used — or the work isn't being done — regardless of how many slash commands fire per week.

> **Note on enforcement.** Four of the five criteria above describe behaviour the kit will eventually enforce *mechanically* (via `/cadence-check` P7.5, the `cadence-nudge` hook F2.5, `/audit-landings-debt` P5.9, and `phase-link-check` F2.1 — all planned). Until those ship, these criteria are **manual discipline**, not automated guards. Track build progress in [`ROADMAP.md`](../ROADMAP.md).
