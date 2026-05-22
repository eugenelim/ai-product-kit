# Plan: template-pm-spec

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for the spec. Allowed to change as we learn; changelog at the bottom.

## Approach

Single-file template at `templates/pm-spec.md`, built by copying `templates/_meta/template-skeleton.md`, deleting the placeholder lines for parent-types that don't apply to a PM Spec (`parent_intent`, `parent_opportunity`, `parent_learning`, `parent_vision`), pre-filling the template's identity (`object_type: Feature`, `status: Draft`), and authoring the nine required-section headings in the load-bearing order pinned in the spec's §"Inputs and outputs" output 1 (and provenance-marked in spec §"Required-section provenance"). Per the cross-cutting dedup convention (spec §"Boundaries → Always do"), `parent_initiative`, `capabilities`, and `related_kpis` are carried once in their universal-schema positions; the `# Handover-specific fields` YAML comment introduces no fields not already in the universal schema (per Decision B, `owning_context` and `owning_team` are NOT introduced; they remain in the parent Initiative's `child-specs.md` manifest columns). Verify against `--check-template` and the existing `scripts/tests/test_templates_instantiate.py` (no test-file modification needed; the parametrized auto-discovery picks the new template up). Append the template's row to `templates/_meta/README.md` `## Shipped templates`. Run adversarial-reviewer. Mark F3.8 shipped in `ROADMAP.md` in the final task. Capture any learnings into the parent spec's changelog (if a finding generalises across F3.x workers) or into this plan's changelog (if it's local to F3.8).

Why this sequencing: every task is small and the dependency graph is mostly linear (`1 → 2 → 3 → 4 → 5 → 6 → 7`). Task 1 (skeleton-copy + identity pre-fill) ships the template-file skeleton; Task 2 encodes the nine required-section headings; Task 3 appends the Handover-specific frontmatter fields; Task 4 runs the VERIFY gate (`--check-template`, contract test, `pre-pr.sh`); Task 5 runs the REVIEW gate (adversarial-reviewer); Task 6 captures the README.md index update and ROADMAP F3.8 check; Task 7 is the CAPTURE phase (parent-spec changelog cross-link if needed). Tasks 1-3 could be interleaved into one edit, but separating them keeps the VERIFY gate's output diagnosable (a failure in T3 versus T4 versus T10 points to the right edit).

No new top-level dependencies. The template is angle-bracket-text only, the linter mode already exists, and the contract test already auto-discovers `templates/*.md`.

## Constraints

- Angle-bracket placeholder syntax exclusively. No `{{...}}`, no `__FILL__`. Pre-fill only `object_type: Feature` and `status: Draft`; every other field is a placeholder. (Per parent spec §"Convention-text contract" → "Placeholder syntax" and "Pre-fill vs placeholder".)
- Frontmatter ordering: universal-schema block first (matching CONVENTIONS.md §"Universal metadata schema" field order verbatim), then a `# Handover-specific fields` YAML-comment marker line. Per Decision B, no fields are appended under the comment (`owning_context` and `owning_team` are NOT introduced). The comment line is retained as a placeholder marker for downstream extension. (Per CONVENTIONS.md §"Templates" → "Frontmatter ordering".)
- **Cross-cutting dedup convention.** `parent_initiative`, `capabilities`, and `related_kpis` are already universal-schema fields per CONVENTIONS.md and are carried once in their universal-schema positions. Do NOT duplicate them under the `# Handover-specific fields` comment. Per the spec §"Boundaries → Always do" dedup convention.
- Section-source provenance must be documented inside the spec's §"Required-section provenance" sub-section (already authored); do not duplicate the provenance markers inside the template body itself.
- Required-section headings appear verbatim where they map from a Handover 6 file (e.g., `## Non-functional requirements` ↔ `non-functional-requirements.md`); inferred sections cite their inference target in the spec, not in the template body.
- File length ≤ 120 body lines (skeleton is ≤ 80; this template adds ~30-40 lines for handover-specific frontmatter + nine sections + optional-block). If we exceed 120 lines, the template has drifted into authoring example content — surface as a plan changelog entry.
- `templates/_meta/README.md` append is sequential across F3 fan-out workers. Per the parent spec's "Sequential README.md appends" rollout note, this worker writes its README.md update inside a tiny dedicated commit at the end of its own loop; the F3 plan's Stage 2 CAPTURE merge resolves any append-only merge conflicts.
- No edit to `docs/HANDOVERS.md` or `docs/CONVENTIONS.md`. No edit to `context/frameworks/ontology.md`.
- Atomic writes (the existing `templates/_meta/template-skeleton.md` and the new `templates/pm-spec.md` are both small markdown files; standard editor writes are atomic enough — no Python `tempfile + os.replace` ceremony needed for a one-shot template file).

## Construction tests

Cross-cutting only. Per-task tests are inline under each task.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 after every task that touches a committed file. Run before each commit, not just at the end.
- `contract-test-clean` — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 after Task 4 lands.

## Tasks

### Task 1: `templates/pm-spec.md` exists with identity pre-filled (skeleton copy + delete-inapplicable + pre-fill)

- **Depends on:** none
- **Tests:**
  - T1 (spec) — `test -f templates/pm-spec.md` exits 0.
  - T10 (spec) — `awk '/^object_type:/{print $2; exit}' templates/pm-spec.md` prints `Feature`.
  - T11 (spec) — `awk '/^status:/{print $2; exit}' templates/pm-spec.md` prints `Draft`.
- **Approach:**
  - Copy `templates/_meta/template-skeleton.md` to `templates/pm-spec.md` verbatim.
  - In the universal-schema frontmatter block: replace the line `object_type: <pre-filled per template — e.g., Strategic Intent>` with `object_type: Feature`. Leave `status: Draft   # product-artifact track entry state; see CONVENTIONS.md §"Lifecycle states"` as-is (the skeleton's pre-fill is already correct for this template's product-artifact track).
  - Delete the four parent-type lines that don't apply to a PM Spec (per skeleton's "delete fields that don't apply" guidance): `parent_intent:`, `parent_opportunity:`, `parent_learning:`, `parent_vision:`. Keep `parent_initiative:` as the load-bearing parent placeholder.
  - Do not yet touch the `# Handover-specific fields` block contents — that's Task 3.
- **Done when:** T1, T10, T11 pass. No need to run `pre-pr-clean` yet — Task 1 leaves the template's body sections still as the skeleton's placeholder shape; the linter will pass `--check-template` only after Task 2 + 3 land, but Task 1's file is syntactically valid markdown and is committable as a partial step. (If the fan-out worker prefers a single commit, fold Tasks 1-3 into one edit and commit only after Task 4 — see Changelog if that choice is made.)

### Task 2: Required-section headings present in load-bearing order

- **Depends on:** Task 1
- **Tests:**
  - T4 (spec) — `awk '/^## /' templates/pm-spec.md` returns the ten `## ` headings in this order: Problem this spec addresses, Capabilities contributed to, User behaviour — current vs future, Functional requirements, Acceptance criteria, Non-functional requirements, Dependencies, Out of scope, Open questions, Optional sections.
- **Approach:**
  - In the template body (under the H1 + intro blockquote), replace the skeleton's three `## <Required section N from HANDOVERS.md>` placeholder headings with the nine required-section headings authored in the spec's §"Inputs and outputs" output 1 sub-list of required sections.
  - Under each heading, leave a one-line angle-bracket placeholder body (e.g., `## Problem this spec addresses\n\n<One paragraph: the specific customer or business issue this Feature addresses, scoped to this Feature only — not the parent Initiative's full problem statement. Cite the linked Problem id from the parent Initiative's capabilities.md.>`). The `## Capabilities contributed to` section's placeholder names that the Feature contributes to one or more Capabilities (ontology direction: `Capability → Feature`).
  - Keep the `## Optional sections` heading from the skeleton; add one example optional sub-section `### Business rules` with a one-line "when to use" description.
  - Update the H1 to `# <Feature name>` (per spec's output 1).
  - Update the intro blockquote to: `> <One-paragraph description: what this Feature is, which Capability it delivers, which parent Initiative it sits under. Cite docs/HANDOVERS.md §"Handover 5" (parent manifest source) and §"Handover 6" (downstream Engineering Handoff Packet consumer).>`
- **Done when:** T4 passes.

### Task 3: Handover-specific frontmatter dedup convention applied

- **Depends on:** Task 2 (or Task 1 if folded into one edit)
- **Tests:**
  - T3 (spec) — required universal-schema frontmatter keys all present (`parent_initiative`, `capabilities`, `related_kpis` carried once each in their universal-schema positions).
- **Approach:**
  - Per the cross-cutting dedup convention (spec §"Boundaries → Always do") and Decision B: the `# Handover-specific fields (per docs/HANDOVERS.md row for this handover)` YAML comment is retained as a placeholder marker, but NO fields are appended under it. `parent_initiative`, `capabilities`, and `related_kpis` live in their universal-schema positions in the block above the comment line; their universal-schema placeholders carry the HANDOVERS-mandated values (e.g., `capabilities: [<CAP-NNN>, ...]` describes the Capability id(s) this Feature contributes to). `owning_context` and `owning_team` are NOT introduced — they remain in the parent Initiative's `child-specs.md` manifest columns per Handover 5.
- **Done when:** T3 passes.

### Task 4: VERIFY — `--check-template` passes; contract test passes; pre-pr clean

- **Depends on:** Tasks 1-3
- **Tests:**
  - T2 (spec) — `python3 tools/lint-frontmatter.py --check-template templates/pm-spec.md` exits 0.
  - T5 (spec) — `grep -nE '(\{\{|__FILL__)' templates/pm-spec.md` returns no matches.
  - T6 (spec) — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0.
  - T7 (spec) — `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Run `python3 tools/lint-frontmatter.py --check-template templates/pm-spec.md`. Fix any frontmatter shape issues (most likely: a placeholder that doesn't satisfy the atomic-or-augmented placeholder regex, e.g., a bare angle-bracket like `<>` or a stray non-placeholder concrete value that violates an enum).
  - Run `python3 -m pytest scripts/tests/test_templates_instantiate.py -v`. Confirm `test_template_passes_check_template_mode[templates/pm-spec.md]` shows up in the parametrize output and passes. This confirms auto-discovery is wired and the new template is in the production target set.
  - Run `bash tools/pre-pr.sh`. Address any unrelated linter complaints surfaced (none expected — this loop touches only template files and an index README).
- **Done when:** T2, T5, T6, T7 pass.

### Task 5: REVIEW — dispatch adversarial-reviewer; iterate any findings

- **Depends on:** Task 4
- **Tests:**
  - Adversarial-reviewer pass exits clean OR returns findings that converge in ≤ 3 iterations.
- **Approach:**
  - Dispatch `adversarial-reviewer` with the prompt named in the worker's PRE-EXECUTE adversarial review (artifact-vs-handover-contract drift; missing edge cases; scope creep).
  - For each finding, either fix the template/spec/plan in-session or mark `Open Questions` if the finding raises a question the worker can't resolve unilaterally.
  - Re-run T2 + T6 + T7 after any template-body change.
- **Done when:** adversarial-reviewer returns clean OR `state.json.iteration_count` < `max_iterations` AND the last review pass returned only deferrable findings (deferred to ROADMAP `F3-G*` rows per the parent spec's "fix small scope-adjacent diagnostic/coverage/cosmetic defers in-session" memory rule).

### Task 6: CAPTURE — `templates/_meta/README.md` index updated; ROADMAP F3.8 marked shipped

- **Depends on:** Task 5
- **Tests:**
  - T8 (spec) — `grep -nE "^- \[x\] \*\*F3\.8\*\*" ROADMAP.md` returns exactly 1 line.
  - T9 (spec) — `grep -nE 'pm-spec\.md' templates/_meta/README.md` returns ≥ 1 line.
- **Approach:**
  - Append under `templates/_meta/README.md` `## Shipped templates`: `- [\`pm-spec.md\`](../pm-spec.md) — PM-side spec for one Feature listed in an Initiative's child-specs manifest. Instantiates as \`delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md\`. Pre-filled \`object_type: Feature\`.`
  - In `ROADMAP.md`, change the F3.8 line from `- [ ] **F3.8** Spec template (PM-side — distinct from the kit's spec template). **Slug:** \`template-pm-spec\`.` to `- [x] **F3.8** Spec template (PM-side — distinct from the kit's spec template). **Slug:** \`template-pm-spec\`. **Shipped:** <YYYY-MM-DD>.`
  - Re-run `pre-pr-clean`.
- **Done when:** T8, T9 pass; `pre-pr-clean` exits 0.

### Task 7: CAPTURE — learnings folded back

- **Depends on:** Task 6
- **Tests:** none mechanical — this is the "what did we learn" task.
- **Approach:**
  - If the F3.8 loop surfaced a generalisable finding that should be captured back into the parent spec (e.g., a section-provenance pattern that all F3.x workers should follow), append a one-line entry to `docs/specs/template-authoring-convention/plan.md` `## Changelog` block.
  - If the finding is local to F3.8 (e.g., a specific edge case in this template's placeholder shape), append to this plan's `## Changelog`.
  - If the finding is a deferred item (cosmetic, coverage gap, diagnostic improvement), add a row to `ROADMAP.md` under the existing `F3-G*` gaps section.
- **Done when:** any learning either lands in a doc or is explicitly noted as "no generalisable learning."

## Rollout

- **Downstream consumers.** Future `/draft-pm-spec` command (anticipated under ROADMAP P4.x, not yet rowed) will copy this template and pre-fill from a parent Initiative's `child-specs.md` row. The `/handoff-packet` command (P4.11) will walk `child-specs.md` and read each PM Spec to assemble the 23-file packet — F3.8's template is what makes that walk's input shape predictable.
- **No INVENTORY.md row.** Per the parent spec's rollout note: templates are infrastructure, not INVENTORY-tracked (the existing `docs/_templates/spec.md` precedent applies).
- **No AGENTS.md edit.** The source-of-truth table already points at `docs/HANDOVERS.md` for the per-handover contract, which is where the PM Spec's shape ultimately derives from.
- **`templates/_meta/README.md` sequential-append concurrency.** This worker writes its README.md update inside Task 6, after VERIFY + REVIEW have cleared. The F3 plan's Stage 2 CAPTURE merge resolves any conflicts with parallel F3.x workers' appends (append-only conflicts are trivially mergeable). Per parent spec's "Sequential README.md appends" rollout note.

## Risks

- **Object_type choice (`Feature`) gets contested by a downstream F3.x worker.** Mitigation: ratified per Decision C; the spec's Open Question 1 documents the candidates considered (`Feature`, `Capability`, Domain I composite) and the rationale. Per ontology Domain E direction (`Capability → Feature` is decomposition), a Feature contributes to one or more Capabilities. If a downstream worker disagrees, the fix is a one-line frontmatter change plus a `capabilities:` field semantic flip — small surface area, recoverable in one iteration.
- **Single-file-vs-folder choice gets contested.** Mitigation: ratified per Decision A; the spec's Open Question 2 documents the strengthened rationale (reduced-ceremony argument plus `link`-column compatibility with either form) and the override clause invoking the parent spec's escape clause. If a downstream worker disagrees, the fix is to convert `templates/pm-spec.md` to `templates/pm-spec/README.md` plus per-child files — but this would explode scope into "design the PM Spec folder structure," which is a separate spec.
- **Handover 6 file-list is per-packet, not per-feature; the section-list might be wrong-shaped at per-feature scope.** Mitigation: the spec's §"Required-section provenance" explicitly marks which sections are HANDOVERS-verbatim (mapping packet files to per-feature scope) and which are inferred (envelope + optional block). If reviewer challenges a specific mapping, fix is to rename or drop one heading — small edit.
- **The parent spec's Open Question 2 resolution (`delivery/initiatives/<initiative-slug>/specs/<spec-slug>/` folder) conflicts with this worker's single-file decision.** Mitigation: ratified per Decision A as an override; spec §"Open questions" Q2 contains the override clause and Q5 documents that the parent's directory-level resolution stands while the per-spec form is now single-file. The parent spec is frozen (Shipped) and is not amended; the override is authoritative for future F3.x worker authors.
- **`scripts/tests/test_templates_instantiate.py`'s parametrize evaluates `_discover_template_targets()` at module-import time.** If pytest's discovery doesn't re-collect after the new template lands, the new template might not appear in the parametrized test cases. Mitigation: T6 is `python3 -m pytest scripts/tests/test_templates_instantiate.py`, run from a fresh invocation; pytest re-imports the test module each invocation, so re-collection happens automatically. If a CI cache somehow holds an old collection, the fix is to invalidate the cache; surface in plan changelog if encountered.
- **`pre-pr.sh` runs the default-mode linter against the kit and could flag the new `templates/pm-spec.md` if it walks `templates/` by accident.** Mitigation: per CONVENTIONS.md §"Templates" → "Linter contract" and per parent spec, default mode does NOT walk `templates/` — this is the load-bearing safety property the parent spec's test T12 enforces. If `pre-pr.sh` does flag `templates/pm-spec.md`, the bug is in `pre-pr.sh`'s glob, not in this template; surface as a parent-spec regression.
- **Risk retired per Decision B.** Earlier draft considered adding `owning_context` / `owning_team` as Handover-specific frontmatter fields. Per Decision B, those fields are NOT introduced in F3.8 — `child-specs.md` manifest columns already carry them at parent-Initiative scope (Handover 5). If a future consuming command needs them per-spec, that command's spec amends F3.8.

## Changelog

Append entries when the plan changes substantially during execution. Format: `<YYYY-MM-DD>: <one-line description of the change and why>`.

- 2026-05-22 (review-iter-1): Applied human-decisions (A: single-file ratified with strengthened rationale; B: owning_context/owning_team dropped; C: object_type Feature retained, terminology corrected to 'contributes to'). Reviewer findings D1/D2/H1/E1/E2/E3/E4/V1-V3 applied. Cross-cutting dedup convention added.
