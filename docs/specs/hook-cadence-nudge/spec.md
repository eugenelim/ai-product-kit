# Spec: hook-cadence-nudge

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** hook (SessionStart)
- **Serves kit phase:** Cross-cutting (drift detection across the portfolio's rhythms)
- **Constrained by:** `docs/PHASE-GUIDE.md` (operating-model failure modes and cadence rhythms); F1.1 (`scripts/lib/graph`); F1.2; F0.10

> **Spec contract.** Defines `scripts/cadence-nudge.py` and `.claude/hooks/cadence-nudge.md`. On every SessionStart, scans the typed-object graph and emits a one-block context reminder when any of three drift signals fire: stale strategy, orphaned OST, kill-drought.

## Objective

Build a SessionStart hook that surfaces three categorical drift signals as injected session context — never blocking, never demanding action, just visible. The signals:

1. **Stale Strategic Intent.** Any `strategy/intents/*.md` with `last_updated` more than 90 days ago (90 = ~quarterly per the operating model's three-tier cadence).
2. **Orphan OST.** Any `discovery/trees/*.md` whose frontmatter has no `chosen_opportunity:` set AND whose `last_updated` is more than 30 days ago (30 = ~monthly per the operating model). The OST's `chosen_opportunity:` field is the canonical signal — derived from the F1.1 sample-kit schema (`discovery/trees/onboarding-funnel.md` carries `chosen_opportunity: OPP-001`); Opportunity child files do NOT carry a `chosen: true` flag.
3. **Kill-drought.** No `validation/learnings/*.md` with `status: killed` in the last 60 days across the portfolio (60 = ~bimonthly; covers two monthly Discovery cycles). Fires also when zero killed learnings exist AND at least one OST has a `chosen_opportunity:` pointing at a node with `status != killed` (kit is doing Validation but has produced no kill verdicts).

If any signal fires, emit a one-block additionalContext reminder naming the specific files / counts and a one-line "what to consider next." If no signals fire, exit 0 silently — sessions stay quiet by default.

## Why now

Cadence drift is silent. The kit declares quarterly, monthly, weekly rhythms in PHASE-GUIDE.md but nothing surfaces missed beats. P7.5 (`/cadence-check`) will be the human-driven audit; this hook is the ambient nudge between audits. Both can exist; the audit goes deep, the nudge stays light.

F1.1 (graph walker) shipped on 2026-05-21 — dependency satisfied. F0.10 ships in batch.

## Inputs and outputs

**Inputs.**
- Stdin: SessionStart JSON (typically `{}`).
- Disk: the repo root, scanned by `scripts.lib.graph.build` for typed artifacts.
- "Today" is `datetime.date.today()`.

**Outputs.**
- Exit 0 always.
- If any signal fires: stdout JSON with `hookSpecificOutput.additionalContext` containing a one-block reminder. Format:
  ```
  Cadence drift detected:
  - Stale strategy: <slug> last updated <YYYY-MM-DD> (>90 days)
  - Orphan OST: <slug> no chosen opportunity for <N> days
  - Kill drought: <N> days since last killed learning
  Consider: /cadence-check, /strategy-refresh, /kill-or-survive
  ```
- If no signals fire: empty stdout, exit 0.
- If the graph build errors: exit 0, stderr trace summary (degrade safely; never block a session).

## Boundaries

### Always do
- Run on SessionStart only.
- Use `scripts.lib.graph.build` for typed-object enumeration.
- Compare dates against `date.today()`. Boundary: `(today - last_updated).days > N` (strict; day N exactly does not fire).
- Read `chosen_opportunity:` off the OST node's own frontmatter (never via `children_of(ost)`).
- Skip when the **graph has zero typed nodes** of Strategic Intent / OST / Validation Learning Memo types — concrete predicate, not "phase folders missing on disk."
- Cap message length at 600 chars deterministically: render findings in order (stale-strategy, orphan-ost, kill-drought); within each finding, truncate the value list to first 2 items + `…` when total would exceed 500 chars before header/footer.

### Ask first
- Adding new drift signals beyond the three named. Default: only the three.
- Changing the thresholds (90 / 30 / 60 days). Default: doc-cited.

### Never do
- Block or warn loudly. SessionStart is informational only.
- Persist nudge state across sessions (no de-duplication; the user sees the same nudge each session until they act).
- Modify any artifact.
- Read or write outside the scanned phase folders + `scripts/lib`.

## Verification mode

- **TDD.** Unit tests under `scripts/tests/test_cadence_nudge.py` using small fixture trees.
- **Goal-based check.** `tools/lint-hook.sh .claude/hooks/cadence-nudge.md` exits 0.
- **Manual gesture.** With a fixture kit producing one stale intent, fresh SessionStart shows the nudge; advance the intent's `last_updated:`, SessionStart goes silent.

## Contract tests

- `test_silent_on_empty_kit` — graph has zero typed nodes of the three relevant types → no stdout.
- `test_silent_when_all_within_thresholds` — every artifact is recent → no stdout.
- `test_fires_stale_strategy_on_92_day_old_intent` — `last_updated: 2026-02-18` (92 days before pinned today=2026-05-21) → nudge mentions the intent slug and "Stale strategy".
- `test_does_not_fire_stale_strategy_on_90_day_old_intent` — `last_updated: 2026-02-20` (exactly 90 days before today=2026-05-21) → no nudge (boundary day, strict `>` does not fire).
- `test_fires_orphan_ost_when_chosen_opportunity_unset_and_ost_31d_old` — OST frontmatter has no `chosen_opportunity:` field AND OST `last_updated` ≥31 days ago.
- `test_does_not_fire_orphan_ost_when_chosen_opportunity_set` — OST has `chosen_opportunity: OPP-001` set, regardless of OST age.
- `test_fires_kill_drought_when_no_killed_learning_in_60_days` — `validation/learnings/*.md` exist but none with `status: killed` newer than 60 days.
- `test_does_not_fire_kill_drought_when_recent_killed_learning_exists` — at least one `status: killed` learning newer than 60 days.
- `test_fires_kill_drought_when_no_learnings_exist_and_chosen_opportunity_alive` — no learnings AND ≥1 OST has `chosen_opportunity:` pointing at a node whose status is not `killed`.
- `test_does_not_fire_kill_drought_when_chosen_opportunity_already_killed` — only OSTs are ones whose `chosen_opportunity:` target has `status: killed` (kit is mid-transition; this is not drift).
- `test_message_lists_all_firing_signals_in_one_block` — fixture firing 2/3 signals → message contains both bullet lines.
- `test_message_under_600_chars` — fixture with all three signals AND long slug names → message length < 600; truncation rule deterministic.
- `test_truncation_uses_ellipsis_when_value_list_exceeds_500` — explicit test that the ≥3rd item in any value list is replaced with `…`.
- `test_graph_build_error_degrades_to_stderr_not_crash` — fixture with malformed frontmatter → exit 0, stderr trace, no stdout JSON.

## Non-goals

- Distinguishing "no validation activity yet" from "validation has gone cold" (the kit's freshness is the proxy; perfect distinction is overkill).
- Tracking individual cadence rhythms (weekly/monthly/quarterly per role). That's `/cadence-check`.
- Emitting per-artifact warnings (only roll-ups).
- Persisting last-nudged state so the same nudge isn't shown across sessions. Repetition is the feature — the user is supposed to act on it.

## Open questions

(Both prior questions closed. Q1: kill-drought fires when zero learnings exist AND ≥1 chosen opportunity with `status != killed` (now in Always do + contract test). Q2: day-boundary is strict `>` (now in Always do + contract test).)

1. **Threshold tuning.** The 90/30/60-day values are anchored to the operating model's three-tier cadence (quarterly/monthly/bimonthly). If real usage shows they fire too often or too rarely, surface via a single follow-up spec; do not tune them in-session without an RFC. Listed as a defer, not a question.

## Acceptance criteria

- [ ] `scripts/cadence-nudge.py` exists, stdlib + `scripts.lib.graph` + `scripts.lib.frontmatter` only, ≤ 250 LOC.
- [ ] `scripts/tests/test_cadence_nudge.py` exists; all 14 contract tests pass.
- [ ] `.claude/hooks/cadence-nudge.md` exists; `tools/lint-hook.sh` exits 0 against it.
- [ ] `python3 -m unittest scripts.tests.test_cadence_nudge` exits 0.
- [ ] PLAN / VERIFY / REVIEW gates exit 0.
- [ ] **Depends on:** F0.10 (`tools/lint-hook.sh`) must ship before VERIFY can run.

## Cross-references

- **Consumed by:** F2.6; the eventual P7.5 `/cadence-check` command (which goes deeper, but this hook is its ambient counterpart).
- **Consumes:** `scripts.lib.graph` (F1.1), `scripts.lib.frontmatter` (F1.2).
- **Frontmatter fields owned:** reads `last_updated`, `status`, and `chosen_opportunity:` (on OST node frontmatter).
- **Ontology object types touched:** Strategic Intent, Opportunity Solution Tree, Opportunity (as OST nodes), Validation Learning Memo.
