---
object_type: Plan
status: Drafting
last_updated: 2026-05-21
---

# Plan: agent-traceability-walker

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

## Approach

Author a single `.claude/agents/traceability-walker.md` matching the shape of `adversarial-reviewer.md` (frontmatter + When invoked + Inputs + Output + How to work + Hard rules). The agent body is short — it's a shell-out wrapper.

## Constraints

- Single .md file, ≤ ~120 lines.
- No code dependencies (agent prose only).
- Tools list: `[Bash, Read]`. Model: `haiku`.

## Tasks

### Task 1: Author `.claude/agents/traceability-walker.md`

- **Depends on:** F1.4 shipped (the script and its CLI flags must exist). The agent's "How to work" must be finalized AGAINST the actual F1.4 CLI — do not draft hard-coded flag names before F1.4 publishes them.
- **Tests:** lint-agent.sh exits 0; the agent's instructions cite F1.4's actual CLI flags verbatim; the structured output shape matches F1.4's JSON output schema (the spec's Outputs field list is the orchestrator-facing schema, derived from F1.4's JSON).
- **Approach:**
  - Frontmatter: `name: traceability-walker`, `description`, `tools: [Bash, Read]`, `model: haiku` (acknowledged as an open assumption — see spec Open questions item 2; revisit if error-path handling proves unreliable).
  - Body sections matching adversarial-reviewer's shape, adapted to a fan-out worker.
  - "How to work" lays out: receive subtree_root_slug + repo_root → invoke the F1.4 CLI (flags-as-shipped) with `--format json` → parse the JSON → emit the structured block per spec Outputs.
  - Error paths: script-missing / script-timeout / script-error all produce the structured error response per spec, never raise unhandled.
- **Done when:** file exists, lint passes, the CLI invocation matches F1.4's shipped CLI exactly.

### Task 2: Manual-gesture verification

- **Depends on:** Task 1.
- **Tests:** dispatching the agent against the sample-kit fixture returns a structured block matching the direct script invocation.
- **Approach:** record in `notes/manual-verification-2026-05-21.md`.
- **Done when:** verification recorded; output matches.

### Task 3: Register

- **Depends on:** Tasks 1-2.
- **Approach:**
  - `.claude/agents/README.md`: ADD `traceability-walker` under Shipped (it isn't in the current Planned list — the entry is being created fresh, not moved).
  - `.claude/commands/audit-traceability.md`: update Step 2 to reference the agent by name (drop the prior "(planned)" annotation if present).
  - INVENTORY.md: add `traceability-walker` row to Phase 4D / agents.
  - ROADMAP.md: check off F1.7.
- **Done when:** ROADMAP F1.7 checked.

## Rollout

- `/audit-traceability` can now fan out cleanly on large portfolios.
- Sets up `/audit-all` (P6.3) to use the same pattern for the aggregate audit.

## Risks

- **Manual-gesture verification subjective.** Mitigation: the fixture sample-kit is small enough to verify the structured block byte-for-byte against the script's JSON output.

## Changelog

- 2026-05-21: Initial plan.
