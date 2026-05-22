# Plan: template-authoring-convention

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for the spec. Allowed to change as we learn; changelog at the bottom.

## Approach

Five independent task families (Tasks 1–5 below), each landing on its own commit. Task ordering is `1 → 2 → (3 ∥ 4) → 5`: the convention text (Task 1) and the skeleton file (Task 2) ship first because every other task references them or asserts about them. The `--check-template` linter mode (Task 3) and the Handover-2.5 contract (Task 4) are independent and can run in parallel after Tasks 1–2 land. Task 5 (the contract test + fixtures + kit-wide health) is the integration gate and must be last.

Why this sequencing: Task 3 (the linter mode) depends on Task 2's skeleton existing as a real file so test T5 can pass. Task 4 (HANDOVERS Handover 2.5) doesn't depend on the others mechanically but is read by every F3 spec, so it must be in place when F3 fans out. Task 5 verifies the whole convention round-trips and is the gate the spec's Acceptance criteria walk.

No new top-level dependencies. Python stdlib + the existing yaml import in `lint-frontmatter.py`. No shell tooling beyond what already ships.

## Constraints

- Must not change `tools/lint-frontmatter.py`'s default-mode behavior. Test T12 enforces this.
- Must not walk `templates/` from default mode. The mode separation is the load-bearing safety property.
- Skeleton ≤ 80 body lines (T3). If it grows, the convention has drifted into being a parallel source of truth.
- All edits to `docs/HANDOVERS.md` and `docs/CONVENTIONS.md` are additive plus *one* relocation (the Handover 2 detector). No content removed; no pre-existing claim contradicted.
- Atomic writes for any file produced (Python `tempfile` + `os.replace`); the linter already does this and we extend the same pattern in tests.
- Stdlib + pyyaml only (pyyaml is already a kit dependency via `tools/lint-frontmatter.py`).

## Construction tests

Cross-cutting only. Per-task tests are inline under each task.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 after every committed task. Run before each commit, not just at the end.

## Tasks

### Task 1: §"Templates — `templates/<slug>.md`" sub-section lands in `docs/CONVENTIONS.md`

- **Depends on:** none
- **Tests:**
  - `T1` from spec — sub-section heading present exactly once.
  - Markdown sanity — `python3 -c "open('docs/CONVENTIONS.md').read()"` succeeds. Cross-reference check: `grep -rn "CONVENTIONS.md#templates" --include='*.md' .` returns zero hits before the section lands and ≥0 hits after (the new anchor is `#templates--templatesslugmd` per GitHub's slugger; no callers yet, so zero hits is fine post-merge).
- **Approach:**
  - Read current end of §"Specs and Plans" in `docs/CONVENTIONS.md`. Confirm the new sub-section will sit between `### Exempt from the universal metadata schema` and §"How non-trivial work happens — the work-loop".
  - Append the convention body from spec's §"Convention-text contract" verbatim.
  - Confirm no other section in CONVENTIONS.md has a competing claim about templates.
- **Done when:** T1 passes; pre-pr-clean exits 0.

### Task 2: `templates/_meta/template-skeleton.md` and `templates/_meta/README.md` exist

- **Depends on:** Task 1 (so the convention is in place before the skeleton claims to instantiate it)
- **Tests:**
  - `T3` from spec — skeleton ≤ 80 body lines.
  - `T4` from spec — `templates/_meta/README.md` exists.
  - `T16` from spec — skeleton uses angle-bracket placeholders only.
  - Skeleton ↔ convention consistency: a one-shot grep asserting the skeleton's frontmatter field names are a subset of the union of (universal schema in CONVENTIONS.md) + (handover-specific fields in HANDOVERS.md). Implemented as a one-line shell test in Task 5's pytest file.
- **Approach:**
  - Create `templates/_meta/` directory.
  - Write `template-skeleton.md` exactly per spec's §"Skeleton-text contract."
  - Write `templates/_meta/README.md`: one paragraph naming what `_meta/` is for, listing the skeleton, and linking to the convention sub-section in CONVENTIONS.md.
- **Done when:** T3, T4, T16 pass; pre-pr-clean exits 0. (T5 — `--check-template` against the skeleton — is deferred to Task 3 since it requires the new linter mode.)

### Task 3: `--check-template` mode on `tools/lint-frontmatter.py`

- **Depends on:** Task 2 (the skeleton must exist so T5 has something to run against)
- **Tests:**
  - `T5` — `--check-template templates/_meta/template-skeleton.md` exits 0.
  - `T6` — `--check-template` on `valid-all-placeholders.md` exits 0.
  - `T7` — `--check-template` on `missing-object-type.md` exits non-zero.
  - `T8` — `--check-template` on `bogus-enum-value.md` exits non-zero (enum violations still rejected).
  - `T8b` — `--check-template` on `whitespace-only-placeholder.md` exits non-zero (`< >` rejected).
  - `T8c` — `--check-template` on `mixed-list-placeholders.md` exits 0 (mixed lists accepted).
  - `T8d` — `--check-template` on `mixed-list-invalid.md` exits non-zero (empty-string concrete element rejected).
  - `T8e` — `--check-template` on `augmented-placeholder.md` exits 0 (the `<role>: <YYYY-MM-DD>` form is accepted).
  - `T8f` — `--check-template` on `nested-container-placeholder.md` exits 0 (list-of-maps with all leaf placeholders accepted).
  - `T8g` — `--check-template` on `nested-container-invalid.md` exits non-zero (one nested leaf is enum-violating).
  - `T9` — `--check-template` on `placeholder-block-scalar.md` exits 0.
  - `T10` — default mode on `valid-all-placeholders.md` exits non-zero (mode separation).
  - `T12` — `python3 tools/lint-frontmatter.py --all` exits 0 (no regression on the existing kit).
- **Approach:**
  - **Red:** author the ten fixtures under `scripts/tests/fixtures/templates/` per the spec's §"Verification mode" fixture list (`valid-all-placeholders.md`, `missing-object-type.md`, `bogus-enum-value.md`, `placeholder-block-scalar.md`, `whitespace-only-placeholder.md`, `augmented-placeholder.md`, `nested-container-placeholder.md`, `nested-container-invalid.md`, `mixed-list-placeholders.md`, `mixed-list-invalid.md`) and write a pytest stub that runs the linter as a subprocess against each, asserting T5–T12 (including T8b–T8g). All assertions fail (linter has no `--check-template` flag yet).
  - **Green:** edit `tools/lint-frontmatter.py`:
    - Add `--check-template <path>` to the argparse surface. Mutually exclusive with `--all` and with positional paths.
    - Add two module-level regexes:
      - `ATOMIC_PLACEHOLDER = re.compile(r"^<\S(?:[^>]*\S)?>$")` — single token, ≥1 non-whitespace char.
      - `AUGMENTED_PLACEHOLDER = re.compile(r"^[^<>]*(<\S(?:[^>]*\S)?>[^<>]*)+$")` — one or more atomic placeholders interleaved with literal non-`<>` text; matches `<role>: <YYYY-MM-DD>` and `<NNN>-<kebab-case>`.
    - Add a recursive `_value_acceptable_as_template(value, expected_constraint)` helper:
      - If `value` is a string and `AUGMENTED_PLACEHOLDER.match(value)`: accept.
      - Else if `value` is a string with embedded newlines (block scalar): match the first non-empty line against `AUGMENTED_PLACEHOLDER`; accept iff matched.
      - Else if `value` is a string: apply the existing concrete-value validation for `expected_constraint` (enum membership, non-empty for untyped list elements, etc.).
      - Else if `value` is a `list`: accept iff every element is acceptable (recurse with the element's expected constraint, or `None` for untyped list-element fields).
      - Else if `value` is a `dict`: accept iff every value is acceptable (recurse).
    - In `--check-template` mode, route every scalar/list/dict validation through `_value_acceptable_as_template`. Required-key-present checks unchanged.
    - Exit 0 on clean; exit 1 on any violation; print the violating path and field per existing convention.
  - **Refactor:** if the recursion duplicates the default-mode validators, consolidate into a single `_validate(value, expected, allow_placeholder: bool)` so default mode and `--check-template` mode share one entry point.
- **Done when:** T5, T6, T7, T8, T8b, T8c, T8d, T8e, T8f, T8g, T9, T10, T12 pass; pre-pr-clean exits 0.

### Task 4: §"Handover 2.5: Discovery → Assumption Map" lands in `docs/HANDOVERS.md`; Handover 2 detector relocated

- **Depends on:** none (independent of Tasks 1–3; can land in parallel)
- **Tests:**
  - `T2` from spec — new section heading present exactly once.
  - `T14a`, `T14b`, `T14c`, `T14d` from spec — detector relocation (exactly one mention of `audit-assumption-coverage`, sitting under Handover 2.5) AND handover-heading count exactly 8 AND Handover 2.5 sequenced between Handover 2 and Handover 3.
  - Markdown sanity — `python3 -c "open('docs/HANDOVERS.md').read()"` succeeds.
- **Approach:**
  - Insert the §"Handover 2.5" body from spec's §"Handover-2.5 text contract" between current Handover 2's `---` separator and the `## Handover 3:` heading.
  - Delete the existing `**Detector:** /audit-assumption-coverage flags chosen opportunities with no assumption map.` line from Handover 2.
  - Confirm Handover 2's remaining detector reads `/audit-discovery-coherence` only.
- **Done when:** T2 and T14 pass; pre-pr-clean exits 0.

### Task 5: `scripts/tests/test_templates_instantiate.py` + ROADMAP cross-reference + D7 mark

- **Depends on:** Tasks 1, 2, 3, 4 (this is the integration commit)
- **Tests:**
  - `T11` — pytest walks `templates/*.md` (excluding `CLAUDE.global.md`) and `templates/*/README.md` and asserts `--check-template` exits 0 on each.
  - `T13` — `bash tools/pre-pr.sh` exits 0.
  - `T15` — no ad-hoc `Kit Template` ontology type added.
  - All previously-defined contract tests (T1–T16) pass when run together.
- **Approach:**
  - Write `scripts/tests/test_templates_instantiate.py`:
    - Discover targets via:
      - `pathlib.Path("templates").glob("*.md")` (top-level template files)
      - `pathlib.Path("templates").glob("*/README.md")` (folder-template READMEs)
      - The explicit path `pathlib.Path("templates/_meta/template-skeleton.md")` (the canonical skeleton — always tested even though it doesn't match either glob)
    - SKIP set: `{Path("templates/CLAUDE.global.md"), Path("templates/_meta/README.md")}` with a docstring naming why for each.
    - For each non-skipped target, run `subprocess.run(["python3", "tools/lint-frontmatter.py", "--check-template", str(path)], check=False)` and assert `returncode == 0`.
    - Add a separate test `test_target_count_nonzero` asserting the discovered-and-not-skipped target count is ≥ 1 (after Task 2, the skeleton guarantees this). Without this assertion the test would be a no-op until F3.1 lands.
    - Add a second test `test_skeleton_field_names_are_known` that parses the skeleton's frontmatter and asserts every key is a member of the **canonical key set** enumerated below. Drift in either direction (skeleton adds an unknown key, or canonical set drops a key the skeleton uses) fails the test.
  - **Canonical key set** (enumerated here so the test is self-contained and reviewable; if this list diverges from CONVENTIONS.md's universal-metadata schema example, fix CONVENTIONS.md or this list — whichever is wrong — in the same commit):
    - Universal schema: `id`, `slug`, `object_type`, `name`, `description`, `owner`, `status`, `priority`, `risk_level`, `created`, `last_updated`
    - Traceability: `parent_intent`, `parent_opportunity`, `parent_learning`, `parent_vision`, `parent_initiative`, `related_problems`, `related_personas`, `related_kpis`
    - Evidence: `evidence_basis`, `open_assumptions`
    - Human-vs-AI: `human_owned_decisions`, `ai_assistance_used`, `ai_assistance_allowed`, `human_approval_required`, `approvals_obtained`
    - Open items: `open_questions`, `risks`
    - **Deliberately excluded:** `related_capabilities` (used by `scripts/lib/graph.py`'s `RELATED_FIELDS` per F1.1, but not yet in CONVENTIONS.md per ROADMAP F1-G7). If the skeleton ever adds this key, the test fails and forces the F1-G7 reconciliation first.
  - Edit `ROADMAP.md`:
    - At the top of the Foundation 3 section (just above F3.1), insert: `> F3.x items consume the authoring convention from \`docs/specs/template-authoring-convention/\`. Read that spec first; copy \`templates/_meta/template-skeleton.md\` to start each F3.x template.`
    - Mark `D7` checked with `Shipped: <today>`.
    - Mark this spec's own ROADMAP entry (none currently — this spec is the *prerequisite* to F3.x, not its own ROADMAP row; surface in CAPTURE whether to add a row).
  - Run the full contract-test set; iterate any reds.
- **Done when:** T11, T13, T15 pass; the full contract test set passes; pre-pr-clean exits 0; ROADMAP shows D7 shipped and the F3-block cross-reference.

## Rollout

- F3.1–F3.10 specs will each copy `templates/_meta/template-skeleton.md`, cite this spec in their `Constrained by:` block, and add their template's entry to `templates/_meta/README.md`'s index list.
- **Sequential README.md appends.** `templates/_meta/README.md` is a shared write target across the ten F3.x workers. Concurrent appends would produce last-write-wins corruption. The F3 plan's Stage 1 must merge the ten parallel branches sequentially (one PR at a time) so each worker's README.md update lands on top of the previous merge — *or* every worker writes its README.md update inside a tiny dedicated commit at the end of its own loop, and Stage 2's CAPTURE merge resolves merge conflicts (acceptable because the conflicts will be append-only and trivially mergeable). The F3 plan's Stage 2 re-validates that the index matches the directory listing after all ten merge.
- `docs/CONVENTIONS.md` is already read by every author working in the kit; the new sub-section needs no separate announcement.
- `docs/HANDOVERS.md` Handover 2.5 will be referenced by F3.3's spec; F3.3 may want a forward-reference in its own `Constrained by:` block. Not a rollout step — normal cross-referencing.
- `INVENTORY.md`: skeleton and convention sub-section are infrastructure (similar to how the existing `docs/_templates/spec.md` isn't an INVENTORY row). No row added.
- `AGENTS.md`: the source-of-truth table already has a "Required metadata for any artifact?" row pointing at `docs/CONVENTIONS.md`. The new sub-section sits under that pointer. No edit required.

## Risks

- **The `--check-template` mode masks real bugs.** If the placeholder regex is too lax (e.g., a typo that produces `<>`empty) it could let broken templates through. Mitigation: T7 + T8 enforce that required-key-missing and enum-violation are still caught; the regex requires at least one non-`>` char inside the brackets.
- **HANDOVERS.md Handover-2.5 insertion breaks an existing internal cross-reference** that says "see Handover 3 below" or similar with numbering that shifted. Mitigation: Task 4 includes a grep for "Handover [3-7]" mentions and visual check that none are off-by-one against the new numbering. Handover 3 is still numbered 3; only the new 2.5 is inserted, so this risk is low.
- **F3.3 may discover the Handover 2.5 contract is insufficient** (missing a field, ambiguous required-section). Mitigation: F3.3's adversarial review against its own spec will surface drift; we treat that as a normal "spec is wrong" event per work-loop §2.2 and amend HANDOVERS.md in the F3.3 loop, not in this one.
- **The pyyaml block-scalar handling differs across pyyaml versions.** Mitigation: T9 fixture explicitly uses `description: |` with a leading newline; if it breaks on the CI pyyaml version, the fix is local to the linter's value-extraction, not to the convention.

- **Task 4 (Handover 2.5) commits independently of Tasks 1–3.** Confirmed: Task 4 has `Depends on: none` and touches only `docs/HANDOVERS.md`. If Tasks 1–3 are blocked mid-loop, Task 4 still ships, which unblocks F3.3. The executor SHOULD commit Task 4 early in the loop so D7's "Closes" guarantee lands first.

## Changelog

-

