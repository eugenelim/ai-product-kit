# Spec: inventory-produces-column-refactor

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** docs reconciliation (single-file edit)
- **Serves kit phase:** Meta (kit infrastructure — INVENTORY honesty)
- **Constrained by:** ROADMAP F0.13; D10 (reconcile-existing-components reviewer finding — INVENTORY's "Produces (ontology)" column contains ~40% non-ontology prose labels); `context/frameworks/ontology.md` (the source of truth for what IS an ontology type); `docs/CONVENTIONS.md` §"Universal metadata schema" (ontology-type-set claim).

> **Spec contract.** Edits `docs/INVENTORY.md` only. Resolves the column-contract violation by **renaming the column** from "Produces (ontology)" to "Produces (output)" across all tables, and updating the legend block to match. Existing values stay — the column header is the lie, not most of the rows.

## Objective

Reconcile `docs/INVENTORY.md` so its tables stop claiming every cell is an ontology type. The minimum-honest fix is renaming the column header to "Produces (output)" (which accepts both ontology types and internal-process outputs), updating the legend definition, and leaving cell values untouched.

## Why now

D10 surfaced this in the reconcile-and-harden pass and committed it to ROADMAP F0.13. As ROADMAP downstream items ship — every new command and agent adds a row — the contradiction grows. Renaming the column once now is a single textual diff. Renaming after 30+ more rows ship will be a much larger diff and a much higher chance of contributors fighting the type-set constraint by inventing types.

## Inputs and outputs

**Inputs.** Current `docs/INVENTORY.md`:
- Top-of-file prose at line 3 ("with the ontology object types it produces") — repeats the column-contract claim.
- Legend bullet at line 9 (`- **Type:** the primary ontology object type the artifact produces …`) — defines the column.
- Legend bullet label `- **Type:**` itself (becomes `- **Output:**` after rename).
- Table headers using `Produces (ontology)` in twelve tables.

**Outputs.** Single edited file with:
- Line 3 prose rewritten so it does not claim every artifact produces an ontology type.
- Legend bullet at line 9 rewritten to describe the new column accurately ("the artifact's primary output — an ontology object type when the artifact produces a Domain A–I type, otherwise a short label naming what the artifact emits").
- Legend bullet label `- **Type:**` renamed to `- **Output:**` so the legend key matches the new column header.
- All table headers using `Produces (ontology)` renamed to `Produces (output)`. Affected tables (count = 12):
  - Phase 1 — Strategy (note: this table has an extra `Mode` column the others lack — Block | Mode | Inv | Produces … | Purpose | Status. The literal-substring rename handles it correctly.)
  - Phase 2 — Discovery
  - Phase 3 — Validation
  - Phase 4 sub-tables: Vision (4A), Initiative (4B), Spec (4C), Engineering handoff (4D), Across delivery
  - Phase 5 — Landings
  - Cross-cutting: Communication, Research, Personal OS
- Row cell values: **unchanged**.

## Boundaries

### Always do
- Rename the column header in **every** table that currently uses `Produces (ontology)`. If even one table is missed, the column-contract violation persists.
- Update the legend's `**Type:**` definition to match the new column name AND rename the bullet label from `**Type:**` to `**Output:**`.
- Update the top-of-file prose at line 3 to drop the unqualified ontology-type claim.
- Keep the column position the same — don't reorder columns.

### Ask first
- Editing any individual cell value. Out of scope; defer to a follow-up if a contributor flags a specific cell.
- Adding a parallel column "Ontology type (where applicable)" to preserve the original semantic. Lean: no, that's clutter. If the user asks for it, surface as a follow-up.

### Never do
- Add a new ontology type to accommodate a cell value (e.g., adding "Coaching" or "Voice rubric" to Domain I).
- Reorder columns or rows.
- Remove rows.
- Touch the "Linters (kit-meta)" table or the "Read-the-source map" — they don't use the affected column.

## Verification mode

- **Goal-based check.** Greps and a kit-wide gate.

## Contract tests

- `T1` — `grep -c "Produces (ontology)" docs/INVENTORY.md` returns `0`. Every instance of the old column name is gone.
- `T2` — `grep -c "Produces (output)" docs/INVENTORY.md` returns exactly `12`. Counts the new column header across all twelve affected tables. (Exact rather than ≥12 so a missed table fails the test, rather than passing on a padded count.)
- `T3` — `grep -nE "ontology object type when the artifact produces" docs/INVENTORY.md` returns ≥ 1 hit. Confirms the legend body was updated.
- `T4` — `grep -nE "^\s*-\s+\*\*Output:\*\*" docs/INVENTORY.md` returns ≥ 1 hit. Confirms the legend bullet label was renamed from `**Type:**` to `**Output:**`.
- `T5` — `grep -c "the ontology object types it produces" docs/INVENTORY.md` returns 0. Confirms line 3 prose narrowed.
- `T6` — `bash tools/pre-pr.sh` exits 0.
- `T7` — `grep -ncE '^\|\s*([Kk]it[ -][Ss]pec|Coaching|Voice rubric)\s*\|' context/frameworks/ontology.md` returns 0 hits. Precise table-row anchored check (avoids false positive against the pre-existing prose "kit-specific" in §I's heading).

## Non-goals

- Editing individual cell values to better match ontology types.
- Adding a new column (e.g., "Ontology type if applicable").
- Reconciling INVENTORY against the actual ontology type set programmatically (would require a script — out of scope).
- Touching `docs/CONVENTIONS.md`, AGENTS.md, or any other file.

## Open questions

1. **Should we drop the column entirely instead of renaming it?** Lean: no. The column carries useful information — what an artifact emits — regardless of whether that's an ontology type. Renaming preserves the information while honestly labeling the surface. _Resolved here: rename._

2. **Should the legend definition mention which Domain (I, A, etc.) each value belongs to where it IS an ontology type?** Lean: no. That's auditing, not legend. _Resolved here: keep the legend short._

## Acceptance criteria

- [ ] Every `Produces (ontology)` header in `docs/INVENTORY.md` renamed to `Produces (output)`.
- [ ] Legend bullet label renamed from `**Type:**` to `**Output:**`; legend body rewritten to describe the new column accurately.
- [ ] Line 3 prose narrowed so it does not claim every artifact produces an ontology type.
- [ ] Cell values unchanged.
- [ ] Contract tests T1–T7 all pass.
- [ ] No new ontology types invented.
- [ ] ROADMAP.md F0.13 marked checked with `Shipped: 2026-05-21` in the CAPTURE phase (per work-loop SKILL §5.4).

## Cross-references

- **Consumed by:** humans reading INVENTORY; the work-loop SKILL §5.2 (which references INVENTORY).
- **Consumes:** nothing.
- **Frontmatter fields owned:** none.
- **Ontology object types touched:** none structurally; the cells reference Domain A–I types, but the spec doesn't add or modify those types.
