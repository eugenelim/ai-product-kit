# Plan: audit-portfolio-coherence-script

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

## Approach

The script: discover active artifacts via the graph → for each pair (N²/2), classify on three axes → label the pair → aggregate to verdict → render.

The classification is the load-bearing logic. It reads three frontmatter fields per artifact (`resource_claims:`, `capability_focus:`, `market_posture:`); if any field is empty, that axis is `unknown` for the pair. The classification function reads only frontmatter — no NLP, no inference from prose.

## Constraints

- Stdlib + `scripts.lib.*` only.
- ≤ ~350 LOC.
- No external NLP / no LLM call from inside the script. Audit is deterministic.

## Tasks

### Task 1: Write `scripts/tests/test_audit_portfolio_coherence.py` (red)

- **Depends on:** F1.1 + F1.2 shipped.
- **Tests:** all 9 contract tests.
- **Approach:** add `scripts/tests/fixtures/coherence/` with: coherent 3-intent portfolio, incoherent 2-intent portfolio (one pair contradicts on 2+ axes), sequenced pair, single-artifact, empty.
- **Done when:** suite fails as expected.

### Task 2: Implement `scripts/audit-portfolio-coherence.py` (green)

- **Depends on:** Task 1.
- **Approach:**
  - CLI per spec.
  - `discover_active(graph) -> list[Node]` — Strategic Intent + active Initiative artifacts.
  - `classify_pair(a, b) -> dict[str, str]` — returns `{resources, capabilities, market_posture}` each ∈ `reinforces | neutral | contradicts | unknown`.
  - `label_pair(classification) -> str` — `coherent | adjacent | drifting | incoherent | sequenced | unknown` per the skill rules AS WRITTEN (the tightened-coherent variant is deferred to D11 — see spec Non-goals).
  - `verdict_for(labels) -> tuple[verdict, exit_code]`.
  - `render_*`, `--write` machinery.
- **Done when:** unit tests pass; smoke commands work.

### Task 3: Update `.claude/commands/audit-portfolio-coherence.md`

- **Depends on:** Task 2.
- **Approach:**
  - Shell-out subsection at top of Procedure; keep prose as fallback.
  - Remove the now-defunct reference to `context/frameworks/strategic-coherence.md` as a hard input.
  - Update Step 3 frontmatter template: rename `status:` to `verdict:` (script's canonical field name) and change `object_type: Coherence Audit` to `object_type: Audit Report` (Coherence Audit is not in the ontology).
- **Done when:** lint-command.sh exits 0; the prose command's Step 3 frontmatter matches the script's output frontmatter (field names, object_type value).

### Task 4: Register

- **Depends on:** Tasks 1-3.
- **Approach:** INVENTORY status update; ROADMAP F1.6 check.
- **Done when:** ROADMAP F1.6 checked off.

## Rollout

- `/audit-portfolio-coherence` becomes deterministically runnable on a portfolio.
- Sets up `cadence-manager` (P7.6) to call it on a monthly cron.

## Risks

- **Frontmatter axis-claim fields not adopted.** Most existing artifacts won't have `resource_claims:` / `capability_focus:` / `market_posture:` yet. The audit will return mostly-`unknown` until those fields land. Mitigation: report explicitly recommends adding the fields; doesn't fail on absence.
- **Single-axis contradictions inflate to "incoherent".** Mitigation: per the tightened `coherent` rule, single contradictions on one axis with reinforces on others is `drifting`, not `incoherent`.

## Changelog

- 2026-05-21: Initial plan.
