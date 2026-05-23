# Plan: cmd-audit-spec-linkage

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

Build the bundled component in three stages, mirroring the F1.4 (`audit-traceability`) precedent. **Stage 1:** Python script `scripts/audit-spec-linkage.py` — Python 3, argparse entry-point, stdlib + `scripts.lib.{graph,frontmatter}` only, single `audit()` function returning a `(Report, exit_code)` tuple, two renderers (`render_markdown` / `render_json`), one `main()` that wires argv → audit → render → (optional `--write` side effect) → stdout three-line header + payload → exit. **Stage 2:** the slash-command wrapper `.claude/commands/audit-spec-linkage.md` — body modelled verbatim on `.claude/commands/audit-traceability.md`'s shape (state canonical script path; document `--scope` / `--format` / `--write`; describe the four exit codes; carry a prose-fallback procedure) plus the explicit F4 deviation declaration and the three-line stdout header documentation. **Stage 3:** verification — `python3 -m pytest scripts/tests/test_audit_spec_linkage.py -v` exits 0, full suite exits 0, `tools/lint-command.sh` exits 0.

Load-bearing sequencing: the script is built TDD-style (Task 1 = tests, Task 2 = implementation to make tests pass). The wrapper file (Task 3) can be drafted in parallel with Task 2 because the script's argv and exit codes are fully specified in the spec and do not depend on the implementation. Final regression (Task 4) is the gate.

The script reuses `scripts.lib.graph.build()` (which already scans the kit-default include globs and parses every typed-object frontmatter, including `parent_initiative:` in `PARENT_FIELDS`) and filters the audited set to PM Specs by path-shape `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`. The two violation kinds — `missing-parent-initiative` and `dangling-parent-initiative` — fall out of inspecting `node.frontmatter.get("parent_initiative")` and the corresponding edge's `target_exists` (the graph already records dangling edges for us; see `Graph.dangling_edges()`).

## Constraints

- Stdlib only on the script, except for `scripts.lib.graph` and `scripts.lib.frontmatter` imports. No new top-level dependencies.
- Script ≤ ~250 LOC (the F1.4 sibling is ~367 LOC and handles seven rules; this audit handles one rule and should land smaller).
- Atomic-write the dated report file (`tmp + os.replace`) so a partial write never corrupts `docs/audits/`. Append to `SPEC-LINKAGE-LOG.md` uses standard append-open; lines are single-line and crash-safe.
- Wrapper file `description:` frontmatter ≤ 1024 characters (palette-render limit; T_cmd3).
- The three-line stdout header must print BEFORE the markdown payload on stdout, regardless of `--format`. On `--format json`, the header still prints (header is stdout-facing; payload is the JSON body). The `--write` path persists only the markdown payload (not the header).
- Wrapper file must declare verbatim: "This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply." (T_cmd6).
- Do not introduce a new top-level folder. Outputs land under `docs/audits/` (already exists per F1.4).
- Read-only on every spec / initiative artifact. The audit never mutates the kit.

## Construction tests

The eight script contract tests (per spec §"Contract tests") drive Task 2. The seven wrapper-shape tests (T_cmd1–T_cmd7) drive Task 3. No cross-cutting tests beyond the per-task `Tests:` subsections below.

## Tasks

### Task 1: Author `scripts/tests/test_audit_spec_linkage.py` with the 8 fixture-based tests

- **Depends on:** none
- **Tests (this task IS the tests):**
  - `test_clean_verdict_on_well_linked_fixture` — well-linked fixture → exit 0, verdict `clean`.
  - `test_missing_parent_initiative_flags_violation` — spec without `parent_initiative:` → violation_type `missing-parent-initiative`.
  - `test_dangling_parent_initiative_flags_violation` — spec with `parent_initiative:` pointing at non-existent initiative → violation_type `dangling-parent-initiative`.
  - `test_scope_subtree_limits_audited_set` — `--scope initiative-A` excludes specs under initiative-B.
  - `test_write_flag_creates_dated_report_file_and_appends_log` — `--write` creates dated report + appends to log.
  - `test_json_output_shape` — `--format json` returns the four required top-level keys + frontmatter required fields.
  - `test_insufficient_data_verdict_on_small_scope` — 0–2 specs → exit 3, verdict `insufficient-data`.
  - `test_clean_verdict_when_no_specs_in_scope_is_insufficient_data_not_clean` — 0 specs in scope (even if initiatives present) → exit 3, NOT exit 0.
- **Approach:**
  - Mirror `scripts/tests/test_audit_traceability.py` structure: `subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, cwd=str(REPO_ROOT))`.
  - Build fixtures either inline (`tempfile.TemporaryDirectory`) or under `scripts/tests/fixtures/spec-linkage-clean/` and `scripts/tests/fixtures/spec-linkage-broken/` (see Task 5).
  - For each test, run the script and assert on `returncode`, parsed JSON, or persisted file contents.
  - Tests fail initially (script does not yet exist or rules not yet implemented). This is intentional — they drive Task 2.
- **Done when:** `python3 -m pytest scripts/tests/test_audit_spec_linkage.py -v` runs all 8 tests; they fail (script missing). Each test name is enumerated in the spec's §"Contract tests".

### Task 2: Author `scripts/audit-spec-linkage.py` to make Task-1 tests pass

- **Depends on:** Task 1
- **Tests:**
  - All 8 tests from Task 1 pass.
  - `python3 -m pytest scripts/tests/` exits 0 (no regression on F1.1 / F1.2 / F1.4 / F1.5 / F1.6 / F2.x tests).
- **Approach:**
  - Mirror `scripts/audit-traceability.py` structure verbatim where possible:
    - Module docstring describes the one rule and its violation taxonomy.
    - `REPO_ROOT = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(REPO_ROOT))` then `from scripts.lib.graph import Graph, Node, build`.
    - Dataclasses: `Violation(spec_slug, path, violation_type, remediation)`, `Report(date, scope, specs_audited, broken_links, verdict, violations, orphans)`.
    - `audit(root: Path, scope: Optional[str]) -> tuple[Report, int]` — build graph (with optional scope); filter nodes to PM Specs by path-shape `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`; for each, check `parent_initiative:` is present (else `missing-parent-initiative`) AND the target initiative folder `delivery/initiatives/<value>/README.md` exists OR an edge resolves (else `dangling-parent-initiative`); apply `verdict_for(specs_audited, broken_links)`; return `(report, exit_code)`.
    - `verdict_for(specs_audited, broken_links)` — verbatim threshold logic: `< 3` → `insufficient-data`/3; `broken_links == 0` → `clean`/0; `1 <= broken_links <= 3 AND broken_links / specs_audited <= 0.25` → `drift`/1; else `broken`/2.
    - `render_markdown(report)` — emit frontmatter block; H1; verdict line; Rule-1 violations section; Orphans section; Recommended remediations section.
    - `render_json(report)` — `json.dumps({frontmatter, violations, orphans})`.
    - `main()` — argparse; resolve root; call `audit`; print three-line stdout header (`PHASE: Delivery → Spec linkage audit (scope=<scope>)`, `VERDICT: <verdict>`, `NEXT: <action>`) where `<action>` is computed from verdict (`clean` → "no action needed"; `drift` / `broken` → "fix the listed broken parent_initiative links"; `insufficient-data` → "expand scope or add specs"); then print payload; on `--write`, write dated report + append log line; return exit code.
  - The script must NOT include the three-line header in the persisted markdown file or the appended log line.
- **Done when:** `python3 -m pytest scripts/tests/test_audit_spec_linkage.py -v` exits 0 with all 8 tests green; script LOC ≤ ~250.

### Task 3: Author `.claude/commands/audit-spec-linkage.md` (the slash-command wrapper)

- **Depends on:** none (can run in parallel with Task 2; the script's argv contract is fully spec'd)
- **Tests:**
  - T_cmd1: `tools/lint-command.sh .claude/commands/audit-spec-linkage.md` exits 0.
  - T_cmd2: file contains H1 `# /audit-spec-linkage`.
  - T_cmd3: frontmatter `description:` ≤ 1024 chars.
  - T_cmd4: body cites canonical script path `scripts/audit-spec-linkage.py` (verbatim string `python3 scripts/audit-spec-linkage.py` present).
  - T_cmd5: body documents the four exit codes (`0 clean`, `1 drift`, `2 broken`, `3 insufficient-data`).
  - T_cmd6: body contains the verbatim F4 deviation phrase: "This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply."
  - T_cmd7: body documents the three-line stdout header verbatim (`PHASE:`, `VERDICT:`, `NEXT:` in order, in a fenced block).
- **Approach:**
  - Mirror `.claude/commands/audit-traceability.md`'s body shape: frontmatter (`description`, `argument-hint`); H1; opening paragraph; "Canonical implementation" callout with the script invocation; "When to run"; "Inputs"; "The rule" (one rule, not seven); "Procedure" (prose fallback for the contract review); "Verdict thresholds"; "Why this matters"; trailing `$ARGUMENTS`.
  - Add a §"Boundaries → Always do" block (in the prose-fallback Procedure or a dedicated section near the top) containing the verbatim F4 deviation phrase.
  - Document the three-line stdout header in a fenced block titled (e.g.) "Stdout header (printed before the markdown payload)".
- **Done when:** all seven T_cmd assertions pass; the file reads coherently as a sibling to `.claude/commands/audit-traceability.md`.

### Task 4: Verification gate — full suite + linter green

- **Depends on:** Task 2, Task 3
- **Tests:**
  - `tools/lint-command.sh .claude/commands/audit-spec-linkage.md` exits 0.
  - `python3 -m pytest scripts/tests/test_audit_spec_linkage.py -v` exits 0.
  - `python3 -m pytest scripts/tests/` exits 0 (regression: F1.1, F1.2, F1.4, F1.5, F1.6, F2.x suites still pass).
- **Approach:**
  - Run all three commands in sequence; on any failure, return to the upstream task.
- **Done when:** all three commands exit 0.

### Task 5 (optional): Author `scripts/tests/fixtures/spec-linkage-clean/` and `scripts/tests/fixtures/spec-linkage-broken/`

- **Depends on:** none (informs Task 1)
- **Tests:**
  - `scripts/tests/fixtures/spec-linkage-clean/` contains ≥ 3 PM Spec stubs at `delivery/initiatives/<slug>/specs/<spec-slug>.md`, each declaring `parent_initiative:` resolving to an existing `delivery/initiatives/<slug>/README.md`.
  - `scripts/tests/fixtures/spec-linkage-broken/` contains at least one PM Spec with missing `parent_initiative:` and one with dangling `parent_initiative:`.
- **Approach:**
  - Create minimal fixture trees — only the directories and frontmatter blocks the audit reads. No spec body content beyond a placeholder. Mirror the sparse style of `scripts/tests/fixtures/broken/`.
  - Skip this task if Task 1 chooses to build fixtures inline with `tempfile.TemporaryDirectory` (the F1.4 precedent uses inline fixtures for per-rule tests and only an on-disk fixture for the "clean" and "broken" headline cases).
- **Done when:** either fixtures exist on disk and Task 1 tests reference them, OR Task 1 tests build fixtures inline and this task is skipped (note in the changelog).

## Rollout

- **INVENTORY.md** — add a row for `/audit-spec-linkage` under the "Audits & guards" section and a row for `scripts/audit-spec-linkage.py` under the scripts section. (Supervisor / CAPTURE phase.)
- **ROADMAP.md** — check off P4.10 (`[x] P4.10 /audit-spec-linkage ...`). (Supervisor / CAPTURE phase.)
- **`.claude/hooks/check-handover-link.md`** — the lines 79 and 98 footnotes that say "follow-up hook will, once `/audit-spec-linkage` firms up" remain accurate; no edit needed in this work. A follow-up hook may be RFC'd separately.
- **AGENTS.md** — no edit required; the "audit-spec-linkage" detector reference already exists in `docs/HANDOVERS.md:258`.
- **No existing audit/command needs to call this script** — it is invoked directly (CLI or via the slash command). Future consumers: `delivery-manager` scheduled agent (P9.6), `/audit-all` aggregator (P6.3).

## Risks

- **Risk 1: spec-folder layout convention drift.** The spec assumes flat-file `delivery/initiatives/<slug>/specs/<slug>.md`. If a subfolder layout `delivery/initiatives/<slug>/specs/<slug>/spec.md` also exists in the wild, the path filter must accept both. **Mitigation:** at Task 1 fixture authoring, grep the repo for any existing spec to confirm; if ambiguous, accept BOTH path-shapes in the filter and note in the script docstring. Flagged as Open Question #1 on the spec.
- **Risk 2: `object_type:` filter false-negatives.** The path-shape filter alone may catch markdown files that are accidentally placed under `specs/` but are not actually PM Specs (e.g., a stray notes file). **Mitigation:** acceptable initial cost — the audit's `Recommended remediations` section names them, the human filters. Revisit if false-positive rate is non-trivial in first usage.
- **Risk 3: stdout-header coupling to `--format json`.** A consumer piping `--format json` into `jq` will choke on the three preceding non-JSON lines. **Mitigation:** the wrapper file documents the header explicitly; downstream pipeline consumers either parse from line 4 onward or use the `--write` path (which omits the header). If this becomes a real pain, a `--no-header` flag can be added — but defer until needed.
- **Risk 4: log file race on concurrent invocation.** Two parallel `--write` invocations can interleave log appends. **Mitigation:** acceptable for a human-driven audit; log lines are single-line and crash-safe. Production-grade locking is out of scope.
- **Risk 5: F1.1 (`scripts/lib/graph.py`) behavior change.** If F1.1 evolves and `PARENT_FIELDS` or `Graph.dangling_edges()` semantics shift, this script's tests catch it. **Mitigation:** none needed — tests are the guard.

## Changelog

- 2026-05-23: PLAN → EXECUTE → VERIFY → REVIEW → CAPTURE in one session as part of Wave 3 (P4.2 + P4.9 + P4.10). TDD-built: 9 fixture-based script tests went red, script written, all green. Cross-cutting impl review + quality-engineer surfaced four fixes applied in-session: (1) wrapper documents `--write` always persists markdown regardless of `--format`; (2) script coerces list-valued `parent_initiative` to its first element (correctness — list value was silently misclassified as dangling); (3) script treats whitespace-only `parent_initiative` as missing not dangling; (4) script emits a stderr warning when `graph.parse_errors` is non-empty (observability — silent parse-skips inflated the clean count). Two regression tests added: list-coercion + whitespace-handling. Deferred: log-append race (already accepted in §Risks Risk-4); scope-not-found stderr diagnostic; missing `delivery/initiatives/` warning; threshold-boundary tests; `--write --format json` test.
