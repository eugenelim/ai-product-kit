# Spec: hook-ontology-type-check

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** hook (PreToolUse — Write, Edit, MultiEdit)
- **Serves kit phase:** Cross-cutting (consistency between filesystem layout and ontology declaration)
- **Constrained by:** `context/frameworks/ontology.md` (canonical 74-atomic + 8-composite type set); `docs/CONVENTIONS.md` (universal-metadata schema, including `object_type:`); `docs/HANDOVERS.md` (path-to-Domain-I-type mapping); F1.2; F0.10

> **Spec contract.** Defines `scripts/check-ontology-type.py` and `.claude/hooks/ontology-type-check.md`. **Warns** (does not block) when an artifact path implies an ontology type but the frontmatter `object_type:` is missing or mismatched.

## Objective

Build a non-blocking PreToolUse hook that surfaces a stderr nudge when a file is being written under a path that the ontology associates with a specific `object_type`, but the artifact's frontmatter either lacks `object_type:` or sets it to a value that doesn't match the path-implied type. The hook is intentionally soft — it nudges; it never blocks. The intent is to catch the most common ontology-drift case (creating a Vision file at `delivery/visions/foo.md` without declaring `object_type: Vision`) without rejecting writes the model is otherwise ready to make.

## Why now

The kit's traceability audits (`/audit-traceability`, `/audit-completeness`) depend on every typed artifact declaring `object_type:`. Missing-or-wrong-type is the highest-frequency drift mode AGENTS.md and CONVENTIONS.md cite. A warn-only PreToolUse hook is the right enforcement level — strong enough to catch the omission in the moment, weak enough to never bork a session.

F1.2 (parser) is shipped; F0.10 ships in the same batch. No other blockers.

## Inputs and outputs

**Inputs.**
- Stdin: PreToolUse JSON; `tool_name in {"Write", "Edit"}`.
- The proposed new-content frontmatter (parsed via `scripts.lib.frontmatter.parse`); for Edit-without-frontmatter, the disk file is read.

**Outputs.**
- Exit 0 always. Never blocks.
- Stderr (when applicable): a one-line nudge like `ontology-type-check: path <foo> implies object_type: Vision but frontmatter declares Initiative` or `... but frontmatter is missing object_type`.

**Path → implied object_type map (load-bearing):**

| Path glob | Implied `object_type:` |
|---|---|
| `strategy/intents/*.md` | `Strategic Intent` |
| `discovery/trees/*.md` | `Opportunity Solution Tree` |
| `discovery/opportunities/*.md` | `Opportunity` |
| `validation/assumption-maps/*.md` | `Assumption Map` |
| `validation/experiments/*/experiment.md` | `Experiment` |
| `validation/learnings/*.md` | `Validation Learning Memo` |
| `delivery/visions/*.md` | `Vision` |
| `delivery/initiatives/<slug>/README.md` | `Initiative` |
| `delivery/handoff-packets/<slug>/README.md` | `Handoff Packet` |
| `delivery/landings/*.md` | `Landing Report` |

**Path notes:**

- `validation/experiments/*/results.md` is **not in the table** because `Experiment Result` is not a canonical ontology type (it does not appear in `context/frameworks/ontology.md`). If/when a Domain B Experiment Result type is added via RFC, append the row.
- Initiative and Handoff Packet globs match only `README.md` because that's the canonical typed artifact for those folder artifacts. Other files in those folders (`specs/foo.md`, `context-map.md`) are sub-artifacts with their own types and varied paths — out of scope for this soft-nudge hook by design.
- Sub-artifacts more broadly (`delivery/initiatives/<slug>/specs/foo.md`, etc.) are not in scope. Sub-artifacts have their own object types but the path patterns are too varied to enumerate exhaustively in a soft-hook table.

## Boundaries

### Always do
- Operate as PreToolUse on `Write|Edit|MultiEdit`.
- Exit 0 in every branch (never block).
- Use stderr for warnings; nothing on stdout.
- Match paths case-sensitively, lowercase. Strip trailing slashes before matching.
- Suppress the warning if `object_type:` is declared and matches the implied value **exactly**, including case (e.g., `Vision` matches; `vision` warns).
- For Edit/MultiEdit: use the same body-only vs frontmatter-touching classification as F2.1 — body-only edits use the on-disk frontmatter; frontmatter-touching edits use the post-edit reconstruction.

### Ask first
- Adding new path globs beyond the ten in the table. The map is intentionally narrow — sub-artifact path patterns vary too much for a soft hook. Default: only the ten.
- **Do not broaden the Initiative or Handoff Packet globs beyond `README.md`.** The README is the canonical typed artifact for those directories; other files are sub-artifacts with distinct types.
- Changing the warning suppression to "any object_type declared, even mismatched" → "exact match." Default: exact match.
- **When HANDOVERS.md gains or renames an artifact path, review this table before merging.** This hook's table is HANDOVERS-derived; drift creates silent miss-fires.

### Never do
- Block any write.
- Treat the table as authoritative for the audit pipeline — this is a nudge, not a rule. `/audit-traceability` and `lint-frontmatter.py` are authoritative.
- Read or modify any file other than the proposed tool target.

## Verification mode

- **TDD.** Unit tests under `scripts/tests/test_check_ontology_type.py`.
- **Goal-based check.** `tools/lint-hook.sh .claude/hooks/ontology-type-check.md` exits 0.
- **Manual gesture.** Write a `delivery/visions/foo.md` with no `object_type:` in a fresh session; observe the stderr nudge appears but the write proceeds.

## Contract tests

- `test_warns_when_object_type_missing_on_implied_path` — `delivery/visions/foo.md` no `object_type:` → exit 0, stderr nudge mentioning "Vision".
- `test_warns_when_object_type_mismatched` — `delivery/visions/foo.md` with `object_type: Initiative` → exit 0, stderr nudge naming both.
- `test_warns_on_case_mismatch` — `delivery/visions/foo.md` with `object_type: vision` (lowercase) → exit 0, stderr nudge (closes Open Q on case-sensitivity).
- `test_silent_when_object_type_matches_exactly` — `delivery/visions/foo.md` with `object_type: Vision` → exit 0, empty stderr.
- `test_silent_for_path_outside_table` — `delivery/initiatives/auth/specs/foo.md` → exit 0, no stderr.
- `test_handles_experiment_design_path` — `validation/experiments/exp-001/experiment.md` produces implied type `Experiment`.
- `test_silent_for_experiment_results_path` — `validation/experiments/exp-001/results.md` is NOT in the table → exit 0, no stderr (Experiment Result is not a canonical ontology type yet).
- `test_landing_path_implies_landing_report` — `delivery/landings/foo.md` no object_type → nudge naming "Landing Report".
- `test_edit_body_only_uses_on_disk_frontmatter` — Edit operation, body-only, disk file has correct object_type → silent.
- `test_edit_that_changes_object_type_to_mismatch_warns` — Edit whose frontmatter-touching change sets `object_type: Vision` for a file at `delivery/initiatives/foo/README.md` → nudge.
- `test_edit_that_does_not_change_frontmatter_stays_silent` — Edit whose `old_string` contains `---` but the replacement keeps the matching object_type identical → silent.
- `test_multiedit_evaluated_against_final_state` — MultiEdit sequence ending in correct object_type → silent regardless of intermediate states.
- `test_trailing_slash_in_path_handled` — `delivery/visions/foo.md/` (trailing slash) matches the same glob as without.
- `test_malformed_frontmatter_silent_not_crash` — unclosed `---` block → exit 0, no nudge (degrade silently; this hook isn't responsible for shape errors).
- `test_warning_format_includes_path_and_implied_type` — the nudge string is one line, in format `ontology-type-check: <path-as-received> implies object_type: <Implied> but <details>`. Path is emitted verbatim from the tool payload (no normalization).

## Non-goals

- Validating `object_type:` is in the canonical type set (that's `lint-frontmatter.py`).
- Enforcing universal-metadata fields beyond `object_type:` (that's `lint-frontmatter.py`).
- Inferring `object_type:` from file content. Only path → implied type. No body parsing.
- Mapping every ontology type to a path. Sub-artifacts and inline-defined types (KPIs inside a Vision's frontmatter, for example) are out of scope.

## Open questions

(None remain blocking. Both prior questions resolved: case-sensitivity warns on mismatch (now in Boundaries + contract test); Edit-that-doesn't-change-frontmatter is silent (now in contract test).)

## Acceptance criteria

- [ ] `scripts/check-ontology-type.py` exists, stdlib + `scripts.lib.frontmatter` only, ≤ 200 LOC.
- [ ] `scripts/tests/test_check_ontology_type.py` exists; all 14 contract tests pass.
- [ ] `.claude/hooks/ontology-type-check.md` exists; `tools/lint-hook.sh` exits 0 against it.
- [ ] `python3 -m unittest scripts.tests.test_check_ontology_type` exits 0.
- [ ] PLAN / VERIFY / REVIEW gates exit 0.
- [ ] **Depends on:** F0.10 (`tools/lint-hook.sh`) and F2.1 (shared Edit-fallback logic). The Edit-fallback module from F2.1 is reused — either via import from `scripts.lib` (if F2.1 extracts it) or by inlining a small helper.

## Cross-references

- **Consumed by:** F2.6.
- **Consumes:** `scripts.lib.frontmatter` (F1.2).
- **Frontmatter fields owned:** reads `object_type:`. Does not write.
- **Ontology object types touched:** the eleven types listed in the path table.
