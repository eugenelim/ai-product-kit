# Plan: audit-traceability-script

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

## Approach

The script is thin: parse CLI args → call `scripts.lib.graph.build(root, scope=...)` → walk the seven rules → format the report → exit with the verdict-encoded code.

Each rule is a function `check_rule_N(graph: Graph) -> list[Violation]`. The seven functions are independent; iterating over them is the main loop. Output formatting (markdown vs json) is a renderer applied to the `[Violation]` collection.

## Constraints

- Stdlib + `scripts.lib.{graph,frontmatter}` only.
- ≤ ~300 LOC.
- Exit codes: 0 clean, 1 drift, 2 broken, 3 insufficient-data.
- The seven rules must be **semantically equivalent** to the rule descriptions in `.claude/commands/audit-traceability.md` §"The seven traceability rules" and §"Procedure", with Rule 6's parenthetical (distinction from completeness audit) reproduced verbatim in the script docstring.

## Tasks

### Task 1: Write `scripts/tests/test_audit_traceability.py` (red)

- **Depends on:** F1.1 + F1.2 shipped.
- **Tests:** all 14 contract tests from spec §Contract tests.
- **Approach:** Use the fixture trees from F1.1. Add per-rule fixtures under `scripts/tests/fixtures/traceability/` for the rules not exercised by the main sample-kit fixture (e.g., a Requirement without a Capability for Rule 1, a Decision without an ADR for Rule 6).
- **Done when:** suite runs and all tests fail.

### Task 2: Implement `scripts/audit-traceability.py` (green)

- **Depends on:** Task 1.
- **Tests:** Task 1's tests pass.
- **Approach:**
  - `argparse` CLI with `--scope`, `--root`, `--format`, `--write`.
  - Seven `check_rule_N` functions.
  - `@dataclass Violation`: `rule`, `node`, `description`, `remediation`.
  - `verdict_for(violations)`: applies the thresholds.
  - `render_markdown(report)`, `render_json(report)`.
  - If `--write`: ensure `docs/audits/` exists, write `traceability-<YYYY-MM-DD>.md`.
- **Done when:** unit tests pass; the two end-to-end smoke commands (clean fixture exits 0; broken fixture exits 2) work.

### Task 3: Update `.claude/commands/audit-traceability.md`

- **Depends on:** Task 2.
- **Tests:** the command file documents the shell-out + retains the prose procedure as fallback.
- **Approach:**
  - Add a "Shell-out" subsection at the top of Procedure: "When the script is available, the canonical implementation is `scripts/audit-traceability.py`. Run `python3 scripts/audit-traceability.py --scope <slug>`. The procedure below is the fallback when the script is unavailable or when reviewing the prose contract."
  - Don't change the seven-rules text (it must stay in sync with the script).
- **Done when:** command file updated; lint-command.sh exits 0.

### Task 4: Register

- **Depends on:** Tasks 1-3.
- **Tests:** grep checks below pass.
- **Approach:**
  - INVENTORY.md: refine `/audit-traceability` row Status to `shipped (script + prose fallback)`.
  - ROADMAP.md: check off F1.4.
  - AGENTS.md: no change required (already lists `/audit-traceability` in the commands block).
- **Done when:** ROADMAP shows F1.4 checked; INVENTORY shows the script row.

## Rollout

- CI can now `python3 scripts/audit-traceability.py --root . --scope all` as a pre-PR gate (out of scope for this spec; future RFC).
- `/audit-all` aggregator (P6.3) gets one of its building blocks.

## Risks

- **Rule-text drift between script and prose.** Mitigation: **the command file is the single source of truth.** The script docstring carries a verbatim copy of the rule text from the command file. Any edit to rule text starts in the command file and propagates to the script docstring. Task 3 enforces this by having lint-command.sh (or a manual review) compare the two.
- **Empty-repo false-pass.** Mitigated by the explicit insufficient-data verdict (exit 3) and a dedicated test.
- **TRACEABILITY-LOG.md append responsibility.** The script owns it: when `--write` is set, the script also appends a one-line summary to `docs/audits/TRACEABILITY-LOG.md` (creating the file with a header if absent).

## Changelog

- 2026-05-21: Initial plan.
