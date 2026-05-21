---
object_type: Spec
status: Draft
last_updated: 2026-05-21
---

# Spec: agent-traceability-walker

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored)
- **Component type:** agent (fan-out worker)
- **Serves kit phase:** Meta + Phase 4D (Engineering Handoff)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md`; `.claude/agents/adversarial-reviewer.md` (the canonical agent shape); `scripts/audit-traceability.py` (F1.4 — the agent dispatches the script per subtree)

> **Spec contract.** Defines the `traceability-walker` agent: fan-out worker that runs `scripts/audit-traceability.py` against one upstream subtree at a time and returns a structured per-subtree report.

## Objective

Build `.claude/agents/traceability-walker.md`: a fan-out worker invoked by `/audit-traceability` when scope contains more than ~50 typed objects. The orchestrator splits the graph into N subtrees and dispatches one agent per subtree. Each agent runs `python3 scripts/audit-traceability.py --scope <subtree-root-slug>`, parses the output, returns a structured findings summary.

## Why now

F1.4's script can walk a whole kit in one process. For large portfolios (or CI runs across many initiatives) parallelism helps. The agent is a thin wrapper that lets `/audit-traceability` fan out cleanly.

## Inputs and outputs

**Inputs from the orchestrator.**
- `subtree_root_slug`: the artifact slug at the root of the subtree to walk. If ambiguous (resolves to multiple files), the agent returns a structured error requesting disambiguation — does NOT pick arbitrarily.
- `repo_root`: path to the kit root.
- Optional: `--format json` flag for machine-readable output back to the orchestrator.

**Outputs to the orchestrator.**
- A structured findings block matching F1.4's JSON output shape verbatim, plus a `subtree_root` field identifying which subtree this report covers:
  - `subtree_root: <slug>`
  - `objects_audited: <int>`
  - `rules_violated: <int>`
  - `broken_links: <int>`
  - `weak_chains: <int>`
  - `verdict: clean | drift | broken | insufficient-data | error`
  - `violations: [{rule: <1-7>, artifact_id, artifact_path, violation_type}]` — typed list so the orchestrator can aggregate by rule across subtrees. (NOT a `top_3_violations` summary string.)
- The full report file path (when `--write` is used by the orchestrator).
- **Error path:** if F1.4's script is missing, errors, or times out (Bash default), the agent returns `{verdict: error, reason: <"script-missing" | "script-timeout" | "script-error">, subtree_root, stderr_excerpt: <first 500 chars>}` and exits cleanly so the orchestrator can continue with other subtrees.

## Boundaries

### Always do
- Shell out to `scripts/audit-traceability.py`; never reimplement rules in agent prose.
- Return findings via the structured block; let the orchestrator aggregate.
- Confine analysis to the specified subtree.
- Apply a Bash timeout (default 300s) to the script invocation; on timeout return the structured `script-timeout` error response per spec Outputs.

### Ask first
- Persisting the per-subtree report. Default: only when the orchestrator says `--write`.
- Disambiguating an ambiguous `subtree_root_slug`: if it resolves to more than one artifact path, return a structured error (`{verdict: error, reason: "ambiguous-slug", candidates: [<paths>]}`) requesting disambiguation. Do not pick arbitrarily.

### Never do
- Modify any artifact.
- Skip the script and improvise.
- Take an external tool (this is a CLI-shell-out agent; tools list is `[Bash, Read]`).

## Verification mode

- **Manual gesture.** Dispatch the agent from a fresh Claude Code session against the F1.1 fixture sample-kit; verify the structured block is well-formed and the verdict matches what the script returns directly.
- **Goal-based check.** `tools/lint-agent.sh .claude/agents/traceability-walker.md` exits 0.

## Contract tests (manual-gesture form)

- The agent dispatches correctly on a single-subtree input.
- The structured findings block matches the script's JSON output shape.
- On an empty subtree, the agent surfaces `verdict: insufficient-data` cleanly rather than failing.
- The agent refuses (returns a structured error) if `scripts/audit-traceability.py` is missing — surfaces "F1.4 not yet shipped" message.

## Non-goals

- Aggregating across subtrees (the orchestrator does that).
- Running other audits (this agent is traceability-specific).
- Auto-fixing violations.

## Open questions

1. **Tool list:** lean — `[Bash, Read]`. Bash to invoke the script; Read for the report file when `--write` is used.
2. **Model:** lean — `haiku` (this is a thin wrapper; no synthesis).

## Acceptance criteria

- [ ] `.claude/agents/traceability-walker.md` exists.
- [ ] `tools/lint-agent.sh` exits 0.
- [ ] Manual-gesture verification recorded in `notes/manual-verification-2026-05-21.md`.
- [ ] `.claude/agents/README.md`: agent moved from Planned to Shipped.
- [ ] `.claude/commands/audit-traceability.md` Step 2 fan-out paragraph updated: references this agent by name rather than the previous "(planned)" annotation.
- [ ] INVENTORY.md: new row under Phase 4D's agent listing.
- [ ] ROADMAP.md: F1.7 checked off.
- [ ] PLAN/VERIFY/REVIEW gates exit 0.

## Cross-references

- **Consumed by:** `/audit-traceability` slash command (fan-out path).
- **Consumes:** `scripts/audit-traceability.py` (F1.4) via Bash shell-out.
- **Frontmatter fields owned:** none.
- **Ontology object types touched:** none directly (delegates).
