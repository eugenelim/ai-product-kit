# Spec: audit-portfolio-coherence-script

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored)
- **Component type:** script
- **Serves kit phase:** Phase 1 (Strategy)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md`; the existing `.claude/commands/audit-portfolio-coherence.md`; `.claude/skills/strategy-coherence/SKILL.md` (the three-axis rule library)

> **Spec contract.** Promote the prose `/audit-portfolio-coherence` to a runnable `scripts/audit-portfolio-coherence.py`.

## Objective

Build `scripts/audit-portfolio-coherence.py`: pairwise Rumelt coherence check across all active strategic intents and initiatives. Classifies each pair on three axes (resources / capabilities / market posture) and labels the pair `coherent | adjacent | drifting | incoherent | sequenced | unknown`. Outputs a coherence report and exits with a verdict-encoded code.

## Why now

The prose command exists; the script makes the analysis deterministic and CI-runnable. Also exercises the F1.1 graph walker against the Strategy phase.

## Inputs and outputs

**Inputs.**
- `--root`: kit root (default: cwd).
- `--format`: `markdown` | `json`.
- `--write`: write to `strategy/diagnoses/<YYYY-MM-DD>-coherence-audit.md`; also append a line to `strategy/diagnoses/COHERENCE-LOG.md`.

**Outputs.**
- Markdown report with frontmatter: `date`, `artifacts_audited`, `pairs_checked`, `contradictions_flagged`, `verdict`, `object_type: Audit Report`, `last_updated`, `status: Draft`, `human_owned_decisions: [Remediation choice per contradiction]`. Field name `verdict` is the canonical name; the prose command's Step 3 currently uses `status:` and will be updated in Task 3 to match.
- Sections: Verdict; Active portfolio (artifacts in scope); Pairwise findings table; Remediation recommendations (one per contradiction); Open assumptions.
- Exit code: `0` clean (no contradictions), `1` drift (1-2 contradictions or any drifting pair), `2` incoherent (≥3 contradictions or any unmitigated incoherent pair), `3` no-portfolio (zero artifacts — the in-pass false-pass fix).

## Boundaries

### Always do
- Use `scripts.lib.graph` to discover active artifacts. "Active" = `status not in {Deprecated, killed, done}` AND artifact is a Strategic Intent OR Initiative OR Vision (visions ARE in scope; the prose command includes them).
- Apply the three-axis classification from `.claude/skills/strategy-coherence/SKILL.md` AS WRITTEN (today: `coherent` = ≥2 reinforces, neutral on third). The "tightened coherent" rule discussed in deferred-findings D11 is NOT applied here — until D11 ships and amends the skill, the script implements the current skill text verbatim.
- Where artifacts don't declare axis claims (`resource_claims:` / `capability_focus:` / `market_posture:`), emit `axis: unknown` for that pair on that axis. A pair with all `unknown` axes is labeled `unknown` and reported as a "needs frontmatter improvement" item, not a contradiction.
- Handle the empty / single-artifact portfolio cases: exit 3 with `no-portfolio`; on single-artifact emit a one-line report ("portfolio has 1 artifact; pairwise check requires ≥2") rather than a full audit.
- Detect `sequencing_after:` / `status: planned` frontmatter. **When `sequencing_after:` is set on either artifact in a pair, sequencing detection runs first and short-circuits axis classification for that pair: the pair is labeled `sequenced`, axes are not classified.** This is the simplest disambiguation rule until D11 ships richer ordering.
- Mark every unresolved contradiction in `human_owned_decisions:` — never auto-resolve.
- Emit `object_type: Audit Report` in report frontmatter (NOT `Coherence Audit`, which is not an ontology type — see open question 2).

### Ask first
- Adding axes beyond the three (resources / capabilities / market posture). Default: don't; RFC for changes.
- Changing classification thresholds. Default: match the skill.

### Never do
- Mutate kit artifacts.
- Auto-resolve contradictions.
- Treat a missing axis claim as a contradiction (it's `unknown`, which prompts a frontmatter improvement recommendation, not a coherence remediation).

## Verification mode

- **TDD.** Unit tests against fixture portfolios.
- **Goal-based check.** Run against fixture: 3-intent coherent portfolio → exit 0; 2-intent incoherent portfolio → exit 2; empty portfolio → exit 3.

## Contract tests

- `test_clean_verdict_on_coherent_portfolio`
- `test_incoherent_verdict_on_contradicting_portfolio`
- `test_no_portfolio_verdict_on_empty_repo`
- `test_single_artifact_emits_one_line_report`
- `test_sequenced_pair_does_not_flag_as_incoherent`
- `test_unknown_axis_does_not_flag_as_incoherent`
- `test_remediation_appears_in_human_owned_decisions`
- `test_json_output_shape`
- `test_write_creates_dated_diagnosis_and_appends_log`

## Non-goals

- Resolving contradictions (human's job).
- Inferring axis claims when frontmatter doesn't declare them.
- Cross-quarter / temporal analysis.
- Wardley-mapping (separate spec).
- **Tightened-coherent / richer sequencing rules.** Deferred to D11 (`skill-strategy-coherence-hardening`). This script implements the skill as-currently-written; the tightened definition is a follow-up.
- **Fan-out for portfolios > 10 artifacts.** Deferred to D13. This script runs all pairs in-process; for >10 artifacts it emits a stderr warning ("portfolio size N; consider fan-out per D13") and continues sequentially.

## Open questions

1. **Where to recognize the three axes:** lean — read explicit frontmatter fields `resource_claims:`, `capability_focus:`, `market_posture:`. The skill update will recommend these fields; until artifacts declare them, audits return `unknown` for most pairs.
2. **Object_type for the report:** lean — `Audit Report` (Domain H atomic), not `Coherence Audit` (which isn't an ontology type).
3. **Numeric thresholds for `1-2 contradictions = exit 1` / `≥3 = exit 2`.** Rationale: 1-2 contradictions in a small portfolio = manageable (the human can resolve them in one cadence cycle); ≥3 indicates systemic incoherence (the portfolio as a whole is off-track, not just one pair). Acknowledged as a kit convention, not a derived rule; review if cadence data suggests otherwise. Documented in `open_assumptions:` of the report.

## Acceptance criteria

- [ ] `scripts/audit-portfolio-coherence.py` exists, stdlib + `scripts.lib.*` only, ≤ ~350 LOC.
- [ ] `scripts/tests/test_audit_portfolio_coherence.py` exists; all 9 contract tests pass.
- [ ] `python3 -m unittest scripts.tests.test_audit_portfolio_coherence` exits 0.
- [ ] End-to-end smoke commands: coherent fixture exits 0; incoherent fixture exits 2; empty repo exits 3.
- [ ] `.claude/commands/audit-portfolio-coherence.md` updated: shell-out subsection; prose retained.
- [ ] INVENTORY: `/audit-portfolio-coherence` row Status: `shipped (script + prose fallback)`.
- [ ] ROADMAP.md: F1.6 checked off.
- [ ] PLAN/VERIFY/REVIEW gates exit 0.

## Cross-references

- **Consumed by:** `/audit-portfolio-coherence` command; `/audit-all` (P6.3); `cadence-manager` scheduled agent (P7.6).
- **Consumes:** `scripts.lib.graph`, `scripts.lib.frontmatter`. Uses the `strategy-coherence` skill as the rule library (referenced, not imported).
- **Frontmatter fields owned:** writes its own report frontmatter.
- **Ontology object types touched:** Strategic Intent (Domain I), Initiative (Domain D), Audit Report (Domain H).
