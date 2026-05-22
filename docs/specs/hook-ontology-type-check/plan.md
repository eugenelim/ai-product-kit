# Plan: hook-ontology-type-check

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

## Approach

Single-file Python entry point at `scripts/check-ontology-type.py`. The ten path globs from the spec compile once at module load into a `PATH_TYPE_MAP` list of `(regex, implied_type)`. The main flow: stdin → path normalize (strip trailing slash) → path match → frontmatter parse → compare → emit nudge or stay silent.

Edit/MultiEdit semantics mirror F2.1's exactly. The shared helper lives in `scripts/check-handover-link.py` first; F2.3 either imports it (preferred — extract to `scripts/lib/edits.py` as part of F2.1) or inlines a small copy. Decision deferred to EXECUTE — see Rollout.

Tests run in-memory wherever possible (compose a payload dict, feed `check()`); disk fixtures only where Edit-fallback testing requires it.

## Constraints

- Python stdlib + `scripts.lib.frontmatter` only.
- ≤ 200 LOC.
- Exit 0 unconditionally. The only output channel is stderr.
- Top-level try/except → exit 0, swallow trace to stderr without scaring the user.

## Tasks

### Task 1: Path-type table + matcher

- **Depends on:** none.
- **Tests:**
  - `test_silent_for_path_outside_table`
  - `test_handles_experiment_design_path`
  - `test_silent_for_experiment_results_path`
  - `test_trailing_slash_in_path_handled`
- **Approach:**
  - Module-level `PATH_TYPE_MAP: list[tuple[re.Pattern, str]]` — 10 entries, regexes compiled.
  - `imply_type(path: str) -> str | None`. Strips trailing `/` before matching.
- **Done when:** 4 tests pass.

### Task 2: Frontmatter compare + nudge formatting

- **Depends on:** Task 1.
- **Tests:**
  - `test_warns_when_object_type_missing_on_implied_path`
  - `test_warns_when_object_type_mismatched`
  - `test_warns_on_case_mismatch`
  - `test_silent_when_object_type_matches_exactly`
  - `test_landing_path_implies_landing_report`
  - `test_warning_format_includes_path_and_implied_type`
- **Approach:**
  - `compare(path: str, fm: dict, implied: str) -> str | None` returns the nudge string or None.
  - Exact-equality check (Python `==`) — case difference fires the nudge.
  - Nudge format: `ontology-type-check: <path-as-received> implies object_type: <Implied> but <frontmatter says X | object_type is missing>`. Path is emitted verbatim from the tool payload — no normalization.
- **Done when:** 6 tests pass.

### Task 3: Edit / MultiEdit semantics

- **Depends on:** Task 2.
- **Tests:**
  - `test_edit_body_only_uses_on_disk_frontmatter`
  - `test_edit_that_changes_object_type_to_mismatch_warns`
  - `test_edit_that_does_not_change_frontmatter_stays_silent`
  - `test_multiedit_evaluated_against_final_state`
- **Approach:**
  - Same classification as F2.1 (frontmatter-touching if `---` in `old_string`).
  - If F2.1 has extracted helpers to `scripts/lib/edits.py`, import them. Otherwise inline a small `reconstruct_frontmatter(file_path, edits) -> dict | None` function.
- **Done when:** 4 tests pass.

### Task 4: Degraded paths

- **Depends on:** Task 3.
- **Tests:**
  - `test_malformed_frontmatter_silent_not_crash`
- **Approach:** wrap `parse` in try/except; on failure, return None (no nudge).
- **Done when:** test passes.

### Task 5: Entry point

- **Depends on:** Tasks 1–4.
- **Tests:**
  - Subprocess test exercising one nudge case and one silent case.
- **Approach:**
  - `if __name__ == "__main__":` reads stdin, calls `check(payload)`, writes nudge to stderr if any, exits 0.
- **Done when:** subprocess test passes.

### Task 6: Author `.claude/hooks/ontology-type-check.md`

- **Depends on:** Tasks 1–5.
- **Tests:** `bash tools/lint-hook.sh .claude/hooks/ontology-type-check.md` exits 0.
- **Approach:** sections: What it does, Why this matters (the nudge philosophy — soft enforcement, no blocking), The eleven path globs (table verbatim from spec), Configuration, Related (links to `lint-frontmatter.py` and `/audit-traceability`).
- **Done when:** lint passes.

### Task 7: Update reference docs

- **Depends on:** Tasks 1–6.
- **Tests:** none.
- **Approach:**
  - `docs/INVENTORY.md` — new row for the hook.
  - `ROADMAP.md` — check off F2.3.
- **Done when:** edits land.

## Rollout

- F2.6 wires the hook in `.claude/settings.json` as PreToolUse on `Write|Edit`.
- No other consumer; the hook's value is the nudge surfacing in real sessions.

## Risks

- **Soft-hook fatigue.** A noisy nudge dilutes attention. Mitigation: the spec restricts the table to eleven high-signal paths, no body parsing, and exact-match suppression — keeps signal-to-noise high.
- **Path table drift.** If HANDOVERS.md adds new artifact paths and this table isn't updated, the hook stays silent on those new paths. Mitigation: the hook doc cross-references the table; HANDOVERS.md amendments should propagate here.

## Changelog

- 2026-05-21: Initial plan.
- 2026-05-21: Addressed adversarial review (9 findings). Replaced fictional `parse_text` with `parse`. Removed `Experiment Result` row (not a canonical ontology type). Closed Open Q2 (case-sensitivity): now warns on case mismatch with explicit contract test. Added MultiEdit support; Edit semantics now mirror F2.1's body-only vs frontmatter-touching classification. Added trailing-slash handling, Initiative/Handoff-Packet boundary, HANDOVERS-drift cross-reference. Added F0.10 + F2.1 dependencies.
