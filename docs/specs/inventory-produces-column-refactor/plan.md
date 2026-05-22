# Plan: inventory-produces-column-refactor

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** approved

> **Plan contract.** Single-file edit. The work is finding every instance of the old column header and confirming the substitution is safe.

## Approach

Use `Edit` with `replace_all: true` for the column header substitution — this catches every table in one operation. Then a separate `Edit` for the legend's `**Type:**` line. Verify with the spec's contract tests.

## Constraints

- The column appears in many tables. `replace_all` is the only safe pattern; a manual edit-per-table would risk missing one.
- The exact substring `Produces (ontology)` must be unique to the column header — verify with a grep before replace_all (a body cell that happens to contain the literal phrase would also be replaced).

## Tasks

### Task 1: confirm the substitution is safe + note schema differences

- **Depends on:** none
- **Tests:**
  - `grep -c "Produces (ontology)" docs/INVENTORY.md` returns N (expected: exactly 12); record N for post-edit verification.
  - `grep -n "(ontology)" docs/INVENTORY.md` — every hit must be inside a column-header row; no body-cell hits.
- **Approach:**
  - Run both greps.
  - Note that the Phase 1 — Strategy table has one extra column (`Mode`) compared to all other tables. The literal-substring `replace_all` handles this correctly because the column header text is identical across all twelve tables.
  - If a body-cell hit appears, switch to per-table edits.
- **Done when:** safety scan confirms `replace_all` is safe; Phase 1 schema difference documented.

### Task 2: rename the column header globally

- **Depends on:** Task 1
- **Tests:**
  - T1 from spec passes (`grep -c "Produces (ontology)"` returns 0).
  - T2 from spec passes (`grep -c "Produces (output)"` returns exactly 12).
- **Approach:** `Edit docs/INVENTORY.md replace_all=true`: `"Produces (ontology)" → "Produces (output)"`.
- **Done when:** T1 and T2 pass.

### Task 3: update the legend bullet (label + body)

- **Depends on:** Task 2
- **Tests:**
  - T3 from spec passes (legend body grep).
  - T4 from spec passes (legend bullet label is `**Output:**`).
- **Approach:**
  - Locate the legend bullet beginning `- **Type:**` (line 9).
  - Replace with: `- **Output:** the artifact's primary output — an ontology object type when the artifact produces a Domain A–I type, otherwise a short label naming what the artifact emits`
- **Done when:** T3 and T4 pass.

### Task 4: narrow the line-3 prose

- **Depends on:** Task 2
- **Tests:** T5 from spec passes (the old prose phrase is gone).
- **Approach:**
  - Line 3 currently reads: `Every artifact in the kit, classified by **phase** (rows) and **practice area** (columns), with the ontology object types it produces and which agent invokes it.`
  - Rewrite to: `Every artifact in the kit, classified by **phase** (rows) and **practice area** (columns), with its primary output (ontology object type where applicable) and which agent invokes it.`
- **Done when:** T5 passes.

### Task 5: verify kit health

- **Depends on:** Tasks 2–4
- **Tests:**
  - T6 (`bash tools/pre-pr.sh` exits 0).
  - T7 (no invented ontology types).
- **Approach:**
  - Run the kit-wide gate.
- **Done when:** T6 and T7 pass.

## Rollout

- INVENTORY.md is the only file edited.
- No cross-references in other docs need updating (legend rename is internal to the file).
- ROADMAP.md F0.13 marked `Shipped: 2026-05-21` in the CAPTURE phase (work-loop SKILL §5.4).

## Risks

- **Reader-side confusion from bullet-label rename.** A contributor who reads the INVENTORY top-to-bottom encounters the new legend before the tables; that order is fine. A contributor who searches the file for "Type" (the old label) finds no result. Mitigation: the old word has no semantic anchor outside this one bullet; T1 + T5 confirm no stale references remain. Accepted.
- **Some PR readers may want to also fix the cell values.** Out of scope; surface as a separate spec if requested.

## Changelog

- 2026-05-21: T7 grep refined to a table-row anchored pattern after the original substring pattern produced a false-positive against the pre-existing prose "kit-specific" in ontology.md §I's heading. (Same fix pattern as F0.11 T11.)
