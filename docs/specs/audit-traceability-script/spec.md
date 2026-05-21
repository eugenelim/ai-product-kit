# Spec: audit-traceability-script

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored)
- **Component type:** script
- **Serves kit phase:** Meta + Phase 4D (Engineering Handoff)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md`; `context/frameworks/ontology.md` §"Traceability rules"; `docs/HANDOVERS.md`; the existing prose procedure in `.claude/commands/audit-traceability.md`

> **Spec contract.** Promote the prose procedure in `.claude/commands/audit-traceability.md` to a runnable `scripts/audit-traceability.py` the slash command shells out to.

## Objective

Build `scripts/audit-traceability.py`: a CLI script that walks the typed-object graph (via `scripts.lib.graph`) and enforces the seven traceability rules from the ontology. Outputs a structured audit report and an exit code (`0` clean, `1` drift, `2` broken). Updates `.claude/commands/audit-traceability.md` to call the script (keeping the prose as the procedural fallback).

## Why now

The slash command is shipped today as a prose procedure. Promoting it to a script makes the seven rules deterministically enforceable, testable against fixtures, and CI-runnable.

## Inputs and outputs

**Inputs.**
- `--scope`: `all` | `<intent-slug>` | `<initiative-slug>` (default: `all`).
- `--root`: kit root path (default: current working dir).
- `--format`: `markdown` | `json` (default: `markdown`).
- `--write`: write the audit report to `docs/audits/traceability-<YYYY-MM-DD>.md` (default: false; prints to stdout otherwise).

**Outputs.**
- A markdown report with frontmatter: `date`, `scope`, `objects_audited`, `rules_violated`, `broken_links`, `weak_chains`, `verdict`.
- Sections: Verdict; Rule violations (one per violated rule); Weak chains; Orphans; Recommended remediations.
- Exit code per the command-file thresholds (single source of truth: `.claude/commands/audit-traceability.md` §Verdict thresholds):
  - `0` clean: 0 broken links AND ≤10% weak chains.
  - `1` drift: 1-3 broken links AND ≤25% weak chains. (BOTH must hold.) Pure-weak case (0 broken, 11-25% weak) is also `drift`.
  - `2` broken: >3 broken links OR >25% weak chains.
  - `3` insufficient-data: <3 typed nodes in scope.

## Boundaries

### Always do
- Use `scripts.lib.graph` and `scripts.lib.frontmatter`. No reinvention.
- Enforce the seven rules exactly as documented in `.claude/commands/audit-traceability.md` (which itself reflects ontology §32, post-reconcile-pass corrections for Policy Rule and Decision-type Rule 6).
- Handle the empty-repo / insufficient-data case (exit 3 with `verdict: insufficient-data`, do not write a misleading "clean" report).
- Surface dangling edges as Rule violations under Rule 1 or 2 depending on the target type.

### Ask first
- Adding additional rules beyond the seven. Default: don't; new rules go through RFC.
- Changing the verdict thresholds (`drift` vs `broken`). Default: match the prose procedure.

### Never do
- Write to anything outside `docs/audits/` (when `--write`).
- Mutate kit artifacts.
- Pull in network dependencies.

## Verification mode

- **TDD.** Unit tests under `scripts/tests/test_audit_traceability.py` against the F1.1 fixture tree.
- **Goal-based check.** Run the script against the sample-kit fixture and assert the verdict is `clean`; run against `fixtures/broken/` and assert `broken` with the specific rule violations enumerated.
- **Integration check.** `.claude/commands/audit-traceability.md` updated so the procedure shells out to the script; the slash-command-via-Claude-Code path returns the same result as direct invocation.

## Contract tests

- `test_clean_verdict_on_sample_kit_fixture`
- `test_broken_verdict_on_broken_fixtures`
- `test_dangling_parent_edge_flags_rule_1_or_2`
- `test_cycle_flags_as_broken`
- `test_requirement_without_capability_flags_rule_1`
- `test_capability_without_problem_flags_rule_2`
- `test_problem_without_evidence_flags_rule_3`
- `test_kpi_without_outcome_flags_rule_4`
- `test_high_risk_requirement_without_owner_flags_rule_5`
- `test_decision_without_adr_flags_rule_6`
- `test_handoff_packet_without_fixed_flexible_unknown_flags_rule_7`
- `test_insufficient_data_verdict_on_empty_repo`
- `test_json_output_shape`
- `test_write_flag_creates_dated_report_file`
- `test_weak_chains_only_above_10pct_yields_drift`
- `test_rule_7_vacuously_passes_when_no_handoff_packets_exist`
- `test_scope_subtree_evaluates_insufficient_data_threshold_on_subtree_not_global`

## Non-goals

- Walking the graph itself (that's `scripts.lib.graph`).
- Auditing handoff-packet completeness (that's F1.5).
- Cross-portfolio coherence (that's F1.6).
- A graphical / web UI.

## Open questions

1. **Where the report lands when `--write` is set.** Lean: `docs/audits/traceability-<YYYY-MM-DD>.md`. Create `docs/audits/` if missing.
2. **Logging:** print to stderr only on failures; stdout is the report payload.
3. **Cycle scope.** Cycles detected by `scripts.lib.graph.cycles()` are reported under Rule 1 (a node in a cycle cannot have a valid parent chain). They increment `broken_links` and appear in the Rule-1 violations section with `violation_type: cycle`.

## JSON output schema (when `--format json`)

```json
{
  "frontmatter": {
    "date": "YYYY-MM-DD",
    "scope": "all | <slug>",
    "objects_audited": <int>,
    "rules_violated": <int>,
    "broken_links": <int>,
    "weak_chains": <int>,
    "verdict": "clean | drift | broken | insufficient-data"
  },
  "violations": [
    {
      "rule": <1-7>,
      "artifact_id": "<id-or-path>",
      "artifact_path": "<path>",
      "violation_type": "missing-link | cycle | missing-owner | missing-adr | missing-fixed-flexible-unknown",
      "description": "<one-line>",
      "remediation": "<one-line>"
    }
  ],
  "weak_chains": [
    {"chain": ["<id>", "<id>", ...], "weak_link": "<id>", "weakness": "evidence_basis: Weak"}
  ],
  "orphans": ["<id>", ...]
}
```

## Acceptance criteria

- [ ] `scripts/audit-traceability.py` exists, stdlib + `scripts.lib.{graph,frontmatter}` only, ≤ ~300 LOC.
- [ ] `scripts/tests/test_audit_traceability.py` exists; all 14 contract tests pass.
- [ ] `python3 -m unittest scripts.tests.test_audit_traceability` exits 0.
- [ ] `python3 scripts/audit-traceability.py --root scripts/tests/fixtures/sample-kit` exits 0 with `verdict: clean`.
- [ ] `python3 scripts/audit-traceability.py --root scripts/tests/fixtures/broken` exits 2 with `verdict: broken`.
- [ ] `.claude/commands/audit-traceability.md` updated: the Procedure section says the slash command shells out to the script; the prose procedure remains as fallback.
- [ ] INVENTORY.md `Status` for `/audit-traceability` updated to clarify "script + prose fallback".
- [ ] ROADMAP.md: F1.4 checked off.
- [ ] PLAN/VERIFY/REVIEW gates exit 0.
- [ ] F1.1 and F1.2 are shipped before this spec's EXECUTE begins: `scripts/lib/graph.py` and `scripts/lib/frontmatter.py` both exist and their unit test suites pass.

## Cross-references

- **Consumed by:** `/audit-traceability` slash command; `/audit-all` aggregator (planned P6.3); CI workflow.
- **Consumes:** `scripts.lib.graph` (F1.1), `scripts.lib.frontmatter` (F1.2).
- **Frontmatter fields owned:** none on kit artifacts; the script writes its own report frontmatter.
- **Ontology object types touched:** all (the rules cover every Domain).
