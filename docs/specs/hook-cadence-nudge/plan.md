# Plan: hook-cadence-nudge

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

## Approach

Single-file Python entry point at `scripts/cadence-nudge.py`. The script builds the graph (`scripts.lib.graph.build`), then runs three independent signal functions:

```python
def stale_strategy(graph, today) -> list[Finding]
def orphan_ost(graph, today) -> list[Finding]
def kill_drought(graph, today) -> list[Finding]
```

Each returns a list of findings (most often 0 or 1). Findings are formatted into one bullet line each, capped at ~600 chars total, and surfaced via `hookSpecificOutput.additionalContext`.

`today` is parameterized so tests can pin it deterministically; production reads `date.today()`.

Tests build small fixture trees per signal under `scripts/tests/fixtures/cadence/<signal>/` and assert exact finding lists.

## Constraints

- Python stdlib + `scripts.lib.graph` + `scripts.lib.frontmatter` only.
- ≤ 250 LOC.
- ≤ 200ms wall time on the kit's own repo (SessionStart is on the user's interactive critical path).
- Degrade safely: any exception → exit 0 + stderr trace.

## Tasks

### Task 1: Fixture trees

- **Depends on:** F1.1 (shipped).
- **Tests:** fixtures parse cleanly via `scripts.lib.graph.build`.
- **Approach:**
  - `scripts/tests/fixtures/cadence/empty/` — graph has zero typed nodes of the three target types.
  - `scripts/tests/fixtures/cadence/all-fresh/` — one intent (`last_updated: 2026-05-15`), one OST with `chosen_opportunity: OPP-001` set on the OST frontmatter, one recent killed learning (`status: killed`, `last_updated: 2026-04-22`).
  - `scripts/tests/fixtures/cadence/stale-strategy/` — intent with `last_updated: 2026-02-18` (92 days before pinned 2026-05-21).
  - `scripts/tests/fixtures/cadence/boundary-strategy/` — intent with `last_updated: 2026-02-20` (exactly 90 days before pinned 2026-05-21; must NOT fire).
  - `scripts/tests/fixtures/cadence/orphan-ost/` — OST with no `chosen_opportunity:` field, OST `last_updated: 2026-04-15` (≥31 days ago).
  - `scripts/tests/fixtures/cadence/kill-drought/` — only `status: survived` learnings, all >60 days old; one OST with `chosen_opportunity:` set pointing at a non-killed opportunity.
  - `scripts/tests/fixtures/cadence/chosen-already-killed/` — OST has `chosen_opportunity: OPP-002`; opportunity OPP-002.md has `status: killed`. No learnings. Hook should NOT fire kill-drought (kit is mid-transition).
  - `scripts/tests/fixtures/cadence/all-three-fire/` — composite fixture with intentionally long slugs to force truncation in the under-600-chars test.
- **Done when:** all fixtures parse via `scripts.lib.graph.build`; `fixtures/README.md` documents which test each backs.

### Task 2: `stale_strategy()` signal

- **Depends on:** Task 1.
- **Tests:**
  - `test_silent_when_all_within_thresholds` (the all-fresh fixture)
  - `test_fires_stale_strategy_on_92_day_old_intent`
  - `test_does_not_fire_stale_strategy_on_90_day_old_intent`
- **Approach:** iterate `graph.by_type("Strategic Intent")`; for each, parse `last_updated`; if `(today - last_updated).days > 90`, emit a finding with the slug.
- **Done when:** 3 tests pass.

### Task 3: `orphan_ost()` signal

- **Depends on:** Task 1.
- **Tests:**
  - `test_fires_orphan_ost_when_chosen_opportunity_unset_and_ost_31d_old`
  - `test_does_not_fire_orphan_ost_when_chosen_opportunity_set`
- **Approach:** iterate `graph.by_type("Opportunity Solution Tree")`; read `chosen_opportunity:` directly off the OST node's `frontmatter` dict. If the field is absent or empty AND OST `last_updated` is >30 days ago, emit finding.
- **Done when:** 2 tests pass.

### Task 4: `kill_drought()` signal

- **Depends on:** Task 1.
- **Tests:**
  - `test_fires_kill_drought_when_no_killed_learning_in_60_days`
  - `test_does_not_fire_kill_drought_when_recent_killed_learning_exists`
  - `test_fires_kill_drought_when_no_learnings_exist_and_chosen_opportunity_alive`
  - `test_does_not_fire_kill_drought_when_chosen_opportunity_already_killed`
- **Approach:**
  - Iterate `graph.by_type("Validation Learning Memo")` filtering `status == "killed"`; find max `last_updated`.
  - If max is >60 days ago, fire.
  - If no killed learnings exist, check OSTs: any OST with `chosen_opportunity:` set AND the target Opportunity node has `status != "killed"` → fire.
  - Else silent.
- **Done when:** 4 tests pass.

### Task 5: Compose + format + degrade

- **Depends on:** Tasks 2–4.
- **Tests:**
  - `test_silent_on_empty_kit`
  - `test_message_lists_all_firing_signals_in_one_block`
  - `test_message_under_600_chars`
  - `test_truncation_uses_ellipsis_when_value_list_exceeds_500`
  - `test_graph_build_error_degrades_to_stderr_not_crash`
- **Approach:**
  - `compose(findings: list[Finding]) -> str | None` returns the additionalContext block or None.
  - "Empty kit" predicate: `len(graph.by_type("Strategic Intent")) == 0 and len(graph.by_type("Opportunity Solution Tree")) == 0 and len(graph.by_type("Validation Learning Memo")) == 0` → return None.
  - Deterministic truncation: render findings in fixed order (stale-strategy → orphan-ost → kill-drought); within each finding, if its rendered value-list exceeds 500 chars, replace items beyond index 1 with `…`. Total length is capped at 600 by this rule.
  - Wrap the orchestrator in try/except → exit 0 + stderr on any unexpected failure.
- **Done when:** 5 tests pass.

### Task 6: Entry point

- **Depends on:** Task 5.
- **Tests:** (integration smoke; not part of the spec's 14 contract tests)
  - Subprocess test on `all-fresh` (silent) and `stale-strategy` (one nudge).
- **Approach:**
  - `if __name__ == "__main__":` reads stdin (ignored), runs `build()` on repo root, runs signals with `today=date.today()`, prints additionalContext JSON or nothing, exits 0.
  - `today` is a function parameter through the call chain so tests can pin to 2026-05-21.
- **Done when:** integration smoke tests pass.

### Task 7: Hook doc

- **Depends on:** Task 6.
- **Tests:** `bash tools/lint-hook.sh .claude/hooks/cadence-nudge.md` exits 0.
- **Approach:** sections: What it does, Why this matters (the three signals; ambient vs. audit), Configuration, Override (no override — silence drift by acting on it), Related (`/cadence-check` P7.5).
- **Done when:** lint passes.

### Task 8: CAPTURE

- **Depends on:** Task 7.
- **Approach:**
  - `docs/INVENTORY.md` — new row.
  - `ROADMAP.md` — check off F2.5.
  - `docs/PHASE-GUIDE.md` — add one sentence under cadence rhythms noting the SessionStart nudge.
- **Done when:** edits land.

## Rollout

- F2.6 wires SessionStart matcher.
- After ship, the hook fires for every new session in any kit with phase artifacts. Empty-kit cases stay silent.

## Risks

- **Performance.** SessionStart latency matters. Mitigation: the 200ms budget; if it slips, the spec requires hard-cap the scan or memoize.
- **Signal fatigue.** Persistent nudges become noise. Mitigation: the signals fire only on real drift; once the user acts (refresh the intent, choose an opportunity, kill a learning), the nudge stops naturally.
- **Today-handling in tests.** Production reads `date.today()` (non-deterministic). Mitigation: `today` is a function parameter; tests pin to 2026-05-21.

## Changelog

- 2026-05-21: Initial plan.
- 2026-05-21: Addressed adversarial review (10 findings). **Critical schema fix:** orphan-OST signal now reads `chosen_opportunity:` directly off the OST node frontmatter (matches F1.1 sample-kit schema), not `chosen: true` on child Opportunity files (which don't exist as edges). Fixture rewritten accordingly. Fixed 91→92 day arithmetic (2026-02-18 to 2026-05-21 is 92 days). Orphan-OST clock interpretation locked to "OST `last_updated` >30 days." Kill-drought guard tightened: don't fire if chosen opportunity already killed. Empty-kit predicate operationalized as "zero typed nodes of the three target types." Truncation rule made deterministic (in-order, replace items beyond index 1 with `…`). Thresholds cited (quarterly/monthly/bimonthly cadence). Integration smoke tests labeled distinct from contract tests. Added F0.10 dependency.
