# Spec: cmd-audit-spec-linkage

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command + script (bundled — mirrors `docs/specs/audit-traceability-script/spec.md`)
- **Serves kit phase:** Meta + Phase-4 Delivery (Handover-5 enforcement)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md`; `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec"; `scripts/lib/graph.py` (F1.1 — consumed; do not reimplement); `scripts/lib/frontmatter.py` (F1.2); `.claude/commands/audit-traceability.md` and `scripts/audit-traceability.py` (F1.4 — structural precedent for bundled command + script); `tools/lint-command.sh`; `.claude/commands/_meta/command-skeleton.md` (NOTE: skeleton authored for template-fill commands; this command intentionally deviates); `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands" (does NOT apply; explicit).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Bundled component: a runnable script `scripts/audit-spec-linkage.py` and a slash-command wrapper `.claude/commands/audit-spec-linkage.md`. The script enforces one Handover-5 rule — every PM Spec under an Initiative declares a resolving `parent_initiative:` — and the wrapper documents how to invoke it. Mirrors the bundling shape of `docs/specs/audit-traceability-script/spec.md` (F1.4).

## Objective

Build `scripts/audit-spec-linkage.py` and its `.claude/commands/audit-spec-linkage.md` wrapper. The script walks the typed-object graph (via `scripts.lib.graph`) and enforces one rule: every PM Spec under `delivery/initiatives/*/specs/*.md` must declare a `parent_initiative:` frontmatter value that resolves to an existing initiative folder (`delivery/initiatives/<value>/README.md` exists). The script emits a markdown or JSON report and an exit code. The wrapper documents the canonical script path, exit codes, flags, the three-line stdout header, and verdict thresholds — and keeps a prose procedure as fallback. ROADMAP P4.10 stub is `.claude/commands/audit-spec-linkage.md` (currently absent — to be created in this work). Handover-5 names this exact detector at `docs/HANDOVERS.md:258`.

## Why now

Handover 5 ships the contract that every PM Spec must live under an Initiative and declare `parent_initiative:`. Today no machine check enforces this; specs can drift away from their parent initiative silently. The check-handover-link hook (F2.5) explicitly defers child-spec coverage to this audit (`.claude/hooks/check-handover-link.md:79,98`). Phase 4 Wave-3 lands the three audit/diagnostic commands (P4.2, P4.9, P4.10); P4.10 closes the Handover-5 enforcement gap, unblocking the `delivery-manager` scheduled-agent rhythms and unblocking honest reporting from `/audit-traceability` (which assumes Handover-5 is sound).

## Inputs and outputs

**Inputs (script).**
- `--root <path>` — kit root path (default `.`).
- `--scope all | <initiative-slug>` — restrict audit to one initiative subtree (default `all`).
- `--format markdown | json` — report shape (default `markdown`).
- `--write` — when set, persist the markdown report to `docs/audits/spec-linkage-<YYYY-MM-DD>.md` AND append a log entry to `docs/audits/SPEC-LINKAGE-LOG.md` (default false: report streams to stdout).
- Reads every `*.md` and `*.yaml` under the kit-default include globs in `scripts.lib.graph.build`. The audit set is filtered to nodes whose path matches `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` (flat-file layout per `templates/initiative/child-specs.md` and `.claude/commands/draft-spec.md:36`).

**Inputs (wrapper).**
- `$ARGUMENTS` — optional `<initiative-slug>` to pass as `--scope` (default behavior: `--scope all`).

**Outputs (script).**
- Markdown report with frontmatter (when `--format markdown`):

  ```yaml
  ---
  date: <YYYY-MM-DD>
  scope: <all | initiative-slug>
  specs_audited: <int>
  broken_links: <int>
  verdict: clean | drift | broken | insufficient-data
  object_type: Audit Report
  status: Draft
  last_updated: <YYYY-MM-DD>
  ---
  ```

- Markdown body sections:
  1. `# Spec linkage audit — <scope>`
  2. `**Verdict:** <verdict>`
  3. `## Rule 1 violations` — table or list, columns: `spec_slug | path | violation_type | remediation`. Violation types: `missing-parent-initiative` (field absent or empty), `dangling-parent-initiative` (field present but target initiative folder / README missing).
  4. `## Orphans` — specs at the top of their subtree with no parent (may be roots or symptoms of missing initiatives).
  5. `## Recommended remediations` — one named next action per violation.

- JSON report (when `--format json`): top-level keys `frontmatter`, `violations`, `orphans`; `violations` entries are dicts with keys `spec_slug`, `path`, `violation_type`, `remediation`.

- **Three-line stdout header (prefixed BEFORE the markdown payload on stdout — shared Wave-3 verdict-header shape with P4.2 and P4.10):**

  ```
  PHASE: Delivery → Spec linkage audit (scope=<scope>)
  VERDICT: clean | drift | broken | insufficient-data
  NEXT: <one-line recommended human action — e.g., "fix the listed broken parent_initiative links" or "no action; the audit log was appended">
  ```

  The header prints to stdout (for the human reading the terminal). The `--write` path persists ONLY the markdown payload (frontmatter + body); the three-line header is NOT included in the written file or the appended log entry.

- **Side effects on `--write`:**
  - Create `docs/audits/` if missing.
  - Write `docs/audits/spec-linkage-<YYYY-MM-DD>.md` (the markdown payload).
  - Append a log line to `docs/audits/SPEC-LINKAGE-LOG.md` (create with `# Spec linkage audit log\n\n` header if missing). Log line format: `- <date> scope=<scope> verdict=<verdict> specs=<count> broken=<count>`.

- **Exit codes (verbatim from F1.4 / `.claude/commands/audit-traceability.md`):**
  - `0` clean — no violations.
  - `1` drift — 1–3 broken links (recoverable in a single session).
  - `2` broken — >3 broken links OR systemic (>25% of audited specs broken).
  - `3` insufficient-data — fewer than 3 specs in scope.

**Outputs (wrapper).** The `.claude/commands/audit-spec-linkage.md` file. Lints clean against `tools/lint-command.sh`. Body documents the canonical script path, the four exit codes, the three flags (`--scope`, `--format`, `--write`), verdict thresholds, the three-line stdout header verbatim, the F4 template-fill convention deviation, and a prose-fallback procedure (rule statement, scoping, violation taxonomy, verdict-threshold table).

## Boundaries

### Always do

- Consume `scripts.lib.graph` (F1.1) and `scripts.lib.frontmatter` (F1.2). Reuse `PARENT_FIELDS` (which already includes `parent_initiative`) and `Graph.dangling_edges()`. Do not reimplement graph traversal or frontmatter parsing.
- Filter the audited set to PM Specs by path-shape: nodes whose path matches `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` (the flat-file layout this kit uses per `templates/initiative/child-specs.md` and `.claude/commands/draft-spec.md`). Cross-check `object_type` if present (Feature, or any documented spec object_type), but path-shape is the primary discriminator because Handover-5 binds layout to contract.
- For the wrapper file, declare the F4 template-fill convention deviation in §`Boundaries → Always do` (verbatim phrase per orchestrator instruction): "This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply."
- Mirror `.claude/commands/audit-traceability.md`'s body shape: state canonical script path; document the four exit codes; document `--scope` / `--format` / `--write`; describe verdict thresholds; carry a prose-fallback procedure.
- Print the three-line stdout header before the markdown payload, verbatim. Persist only the payload (not the header) under `--write`.
- Exit 3 (`insufficient-data`) when fewer than 3 specs are in scope. Do not invent a misleading "clean" verdict on a small or empty scope.

### Ask first

- Adding additional rules beyond Rule 1. Default: don't. Linkage rules other than Handover-5 belong to F1.4 (`/audit-traceability`) and F1.5 (`/audit-completeness`). New rules in this audit go through RFC.
- Changing the verdict thresholds. Default: match F1.4 verbatim.
- Auto-fixing violations. Default: don't — this audit reports; the human (or a sibling skill) decides remediation.

### Never do

- Mutate any spec file or initiative artifact.
- Write outside `docs/audits/` on `--write`.
- Pull network dependencies. Stdlib + `scripts.lib.{graph,frontmatter}` only.
- Reimplement graph walking or frontmatter parsing.
- Cite or apply the `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands" body section convention for the wrapper file — it does not apply to audit-shell commands.

## Verification mode

- **TDD** for the script — eight black-box tests under `scripts/tests/test_audit_spec_linkage.py` exercise rule logic, scoping, JSON shape, write side-effects, and edge cases. The script's audit logic has compressible invariants and is well-suited to fixture-based testing (the F1.4 precedent).
- **Goal-based check** for the wrapper file — `tools/lint-command.sh .claude/commands/audit-spec-linkage.md` exits 0, plus seven content assertions (H1, description-length, canonical script path citation, four exit codes documented, F4 deviation declared, three-line header documented).
- **Integration check** — `python3 -m pytest scripts/tests/` exits 0 (regression). The wrapper-via-Claude-Code path returns the same exit code and markdown payload as direct script invocation (the three-line header is added regardless of invocation path).

## Contract tests

**Script tests (TDD; place under `scripts/tests/test_audit_spec_linkage.py`):**

1. `test_clean_verdict_on_well_linked_fixture` — given a fixture with ≥3 PM Specs, each declaring `parent_initiative:` resolving to an existing initiative folder, the script exits 0 and the report verdict is `clean`.
2. `test_missing_parent_initiative_flags_violation` — given a PM Spec whose frontmatter omits `parent_initiative:`, the violation type is `missing-parent-initiative`, the spec appears in the Rule-1 violations list, and the exit code is non-zero (drift or broken).
3. `test_dangling_parent_initiative_flags_violation` — given a PM Spec whose `parent_initiative:` value names a non-existent initiative slug (no `delivery/initiatives/<value>/README.md`), the violation type is `dangling-parent-initiative` and it appears in the Rule-1 violations list.
4. `test_scope_subtree_limits_audited_set` — given two initiative subtrees, invoking with `--scope <initiative-A-slug>` audits only specs under that initiative; specs under initiative-B are excluded from the count and violations list.
5. `test_write_flag_creates_dated_report_file_and_appends_log` — `--write` creates `docs/audits/spec-linkage-<YYYY-MM-DD>.md` and `docs/audits/SPEC-LINKAGE-LOG.md` (the latter with at least one new log line whose format matches `- <date> scope=<scope> verdict=<verdict> specs=<n> broken=<n>`).
6. `test_json_output_shape` — `--format json` returns valid JSON with top-level keys `frontmatter`, `violations`, `orphans`; `frontmatter` includes `date`, `scope`, `specs_audited`, `broken_links`, `verdict`.
7. `test_insufficient_data_verdict_on_small_scope` — given a fixture with 0–2 PM Specs in scope, the exit code is 3 and the verdict is `insufficient-data`.
8. `test_clean_verdict_when_no_specs_in_scope_is_insufficient_data_not_clean` — given a fixture containing initiatives but zero PM Specs, the verdict is `insufficient-data` (exit 3), NOT `clean` (exit 0). Guards against the false-confidence failure mode.

**Wrapper / command-shape tests (goal-based; assert on the rendered file):**

- `T_cmd1` — `tools/lint-command.sh .claude/commands/audit-spec-linkage.md` exits 0.
- `T_cmd2` — file contains an H1 header `# /audit-spec-linkage`.
- `T_cmd3` — frontmatter `description:` is ≤ 1024 characters.
- `T_cmd4` — body contains the verbatim canonical script invocation `python3 scripts/audit-spec-linkage.py` and names the canonical script path `scripts/audit-spec-linkage.py`.
- `T_cmd5` — body documents all four exit codes verbatim: `0 clean`, `1 drift`, `2 broken`, `3 insufficient-data`.
- `T_cmd6` — body contains the verbatim F4 deviation phrase: "This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply."
- `T_cmd7` — body documents the three-line stdout header verbatim (the literal `PHASE:`, `VERDICT:`, `NEXT:` lines, in that order, in a fenced block).

## Non-goals

- **Does NOT audit traceability** — that is F1.4 (`/audit-traceability`). Rule 1 here is Handover-5 specifically (parent_initiative linkage); the seven traceability rules remain F1.4's territory.
- **Does NOT audit completeness** — the 25-item pre-engineering-handoff checklist is F1.5 (`/audit-completeness`).
- **Does NOT audit portfolio coherence** — strategic-intent-vs-initiative coherence is F1.6 (`/audit-portfolio-coherence`).
- **Does NOT modify any spec file** — the audit reports; remediation is human-led (or sibling-skill-led).
- **Does NOT auto-fix violations** — even mechanical fixes (e.g., `sed`-ing in a `parent_initiative:` value) are out of scope.
- **Does NOT walk the graph itself** — that is `scripts.lib.graph` (F1.1).
- **Does NOT enforce the directory layout** (file-system shape of `delivery/initiatives/<slug>/specs/`) — that is the writer's command (`/draft-spec`, F3.8). This audit reads the layout that exists.

## Open questions

1. **Spec-file layout shape.** This spec assumes the flat-file layout `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` (per `templates/initiative/child-specs.md` and `.claude/commands/draft-spec.md:36`). If the kit also ships a subfolder layout `delivery/initiatives/<initiative-slug>/specs/<spec-slug>/spec.md`, the path filter and the fixture layout need a small union — resolve before EXECUTE-phase fixture construction. Answer: supervisor (or path-shape detection at EXECUTE-phase Task 1 fixture authoring).
2. **`object_type:` filter.** The path-shape filter is primary; should the script ALSO require `object_type: Feature` (or any Domain-E spec-typed value) before flagging a missing `parent_initiative:`? Default: no — path-shape is sufficient and avoids false negatives on specs whose `object_type` is mis-declared. Answer: revisit on first usage if false positives appear.
3. **`SPEC-LINKAGE-LOG.md` header text.** First-write creates the log with header `# Spec linkage audit log\n\n`. If a stricter naming convention exists for audit-log headers across the kit, align — resolve before EXECUTE.

## Acceptance criteria

- [ ] `scripts/audit-spec-linkage.py` exists; stdlib + `scripts.lib.{graph,frontmatter}` only; ≤ ~250 LOC.
- [ ] `scripts/tests/test_audit_spec_linkage.py` exists; all 8 script contract tests pass.
- [ ] `python3 -m pytest scripts/tests/test_audit_spec_linkage.py -v` exits 0.
- [ ] `python3 -m pytest scripts/tests/` exits 0 (regression — sibling test suites still pass).
- [ ] `.claude/commands/audit-spec-linkage.md` exists.
- [ ] `tools/lint-command.sh .claude/commands/audit-spec-linkage.md` exits 0 (T_cmd1).
- [ ] Wrapper file passes T_cmd2 (H1), T_cmd3 (description length), T_cmd4 (canonical script path), T_cmd5 (four exit codes), T_cmd6 (F4 deviation phrase), T_cmd7 (three-line stdout header documented).
- [ ] Script, when invoked through the wrapper or directly, prints the three-line `PHASE / VERDICT / NEXT` header to stdout BEFORE the markdown payload.
- [ ] `python3 scripts/audit-spec-linkage.py --root scripts/tests/fixtures/spec-linkage-clean` (or an existing fixture demonstrating the clean case) exits 0 with `verdict: clean`.
- [ ] `python3 scripts/audit-spec-linkage.py --root scripts/tests/fixtures/spec-linkage-broken` (or an existing fixture demonstrating the broken case) exits 1 or 2 with violations enumerated.
- [ ] On `--write`, the dated report appears at `docs/audits/spec-linkage-<YYYY-MM-DD>.md` and a log line is appended to `docs/audits/SPEC-LINKAGE-LOG.md`; neither file contains the three-line stdout header.
- [ ] F1.1 (`scripts/lib/graph.py`) and F1.2 (`scripts/lib/frontmatter.py`) are shipped before this spec's EXECUTE begins.
- [ ] PLAN / VERIFY / REVIEW gates exit 0.

## Cross-references

- **Consumed by:** the `delivery-manager` scheduled agent (planned — ROADMAP P9.6); CI workflow (planned — ROADMAP P6.3 `/audit-all` aggregator); humans running `/audit-spec-linkage <slug>` manually before declaring Handover-5 sound.
- **Consumes:** `scripts.lib.graph` (F1.1), `scripts.lib.frontmatter` (F1.2), `tools/lint-command.sh` (for the wrapper's lint gate).
- **Frontmatter fields owned (read):** `parent_initiative:` on PM Spec frontmatter; `object_type:` (read but not required).
- **Frontmatter fields owned (written):** the audit report's own frontmatter (`date`, `scope`, `specs_audited`, `broken_links`, `verdict`, `object_type: Audit Report`, `status: Draft`, `last_updated`).
- **Ontology object types touched:** Feature / PM Spec (Domain E); Initiative (Domain D); Audit Report (Domain I composite — written).
- **Related Handover:** Handover 5 (`docs/HANDOVERS.md:218`).
- **Related hooks:** `check-handover-link` (F2.5) — explicitly defers child-spec coverage to this audit (`.claude/hooks/check-handover-link.md:79,98`).
