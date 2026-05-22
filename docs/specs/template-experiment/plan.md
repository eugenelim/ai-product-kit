# Plan: template-experiment

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-22)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

One single-commit task: scaffold `templates/experiment/` as a folder template with three child files (`README.md`, `experiment.md`, `results.md`), pre-fill identity, encode required sections per the spec's section taxonomy, append handover-derived and hook-derived frontmatter, then VERIFY → REVIEW → CAPTURE. The two child files (`experiment.md`, `results.md`) carry frontmatter independent of the README because they instantiate the load-bearing hook-contract surface (per parent convention §"File layout": child files carry their own frontmatter iff they instantiate a distinct ontology object — here the Experiment lifecycle's design phase and results phase). The folder layout is mechanical: a kit user `cp -r templates/experiment/ validation/experiments/<id>/` lands them in the exact layout the `assumption-threshold-lock` hook polices.

Sequencing inside the task: scaffold the folder; copy the skeleton to `templates/experiment/README.md` and adapt; author `templates/experiment/experiment.md` from scratch (smaller frontmatter superset — hook contract + traceability fields — and the six design H2 sections); author `templates/experiment/results.md` from scratch (smaller still — `result:` block + three H2 sections). VERIFY runs the contract tests T1–T12 plus the pytest harness. REVIEW dispatches `adversarial-reviewer`. CAPTURE updates `templates/_meta/README.md`, ROADMAP F3.4, and freezes spec.md / plan.md statuses.

Why one task rather than three: the three files are tightly coupled (same folder, same template identity, same VERIFY pass). Splitting into three tasks would multiply pre-pr.sh runs and adversarial-review hand-offs with no parallelism gain (all three files live in the same folder; no inter-task dependency to exploit). The parent convention's plan.md models its tasks at the "coherent commit" granularity — this template ships as one commit.

## Constraints

- Angle-bracket placeholder syntax only across all three files; no `{{...}}` or `__FILL__`.
- Nested-container placeholders honored: `predeclared_threshold: {success: <…>, falsification: <…>}` and `result: {actual: <…>, status: <…>, decided: <…>, decided_by: <…>}` rely on the parent linter's recursive rule (parent spec T8f / T8h). The nested values must be non-empty placeholder strings to pass the linter and to preserve the hook's `check_threshold_fields` shape.
- File names are pinned: `templates/experiment/experiment.md` and `templates/experiment/results.md` exactly. No `-design.md` / `-results.md` suffixes.
- Pre-declared-threshold lock contract preserved: `predeclared_at:` is an angle-bracket placeholder (never a literal date); `predeclared_threshold` is a YAML map (never a string).
- README's universal-schema frontmatter block ordering identical to `templates/_meta/template-skeleton.md`.
- Must not modify `.claude/hooks/assumption-threshold-lock.md`, `scripts/check-assumption-threshold.py`, `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, or `scripts/tests/test_templates_instantiate.py`. Surfacing a contract-gap finding is allowed in adversarial review; resolving it is a separate spec.
- Stdlib only for any one-liner test invocations (no new dependencies).
- Atomic writes (`tempfile` + `os.replace` if any python writer is used; otherwise plain `Write` tool with the spec's exact content).

## Construction tests

Cross-cutting only. Per-task tests are inline under the single task below.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 before the commit (run after VERIFY, before CAPTURE).

## Tasks

### Task 1: `templates/experiment/` folder template lands with three child files; pytest auto-discovery includes README; both child files pass `--check-template`; adversarial review clean

- **Depends on:** none (parent convention `template-authoring-convention` is already shipped 2026-05-22; the skeleton and `--check-template` mode are live).
- **Tests:** (every spec contract test)
  - `T1` — folder + three child files exist.
  - `T2a` — `--check-template templates/experiment/README.md` exits 0.
  - `T2b` — `--check-template templates/experiment/experiment.md` exits 0.
  - `T2c` — `--check-template templates/experiment/results.md` exits 0.
  - `T3a` — README frontmatter contains the universal-schema key set.
  - `T3b` — experiment.md frontmatter contains the design-specific keys including nested `predeclared_threshold.{success, falsification}`.
  - `T3c` — results.md frontmatter contains the results-specific keys including nested `result.{actual, status, decided, decided_by}`.
  - `T4a` — experiment.md H2 headings present in order.
  - `T4b` — results.md H2 headings present in order.
  - `T4c` — README.md H2 headings present in order.
  - `T5` — angle-bracket-only placeholders across the folder.
  - `T6` — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0.
  - `T7` — `bash tools/pre-pr.sh` exits 0.
  - `T8` — ROADMAP F3.4 checkbox flipped (CAPTURE-phase).
  - `T9` — `templates/_meta/README.md` lists `experiment/` (CAPTURE-phase).
  - `T10` — pre-filled identity fields exact across all three files.
  - `T11` — `python3 tools/lint-frontmatter.py --all` exits 0 (default mode does not traverse `templates/` — mode-separation by non-traversal, not per-file rejection).
  - `T12a/T12b/T12c` — hook-contract preservation (threshold shape, predeclared_at placeholder, exact file names).
  - `T13` — adversarial-reviewer Blocking-findings count is 0.
- **Approach:**
  1. **Scaffold.** `mkdir -p templates/experiment/`. No `tools/new-template.sh` exists (deferred per parent spec); use the kit's standard `mkdir` + `cp` pattern.
  2. **README.md — copy and adapt skeleton.** `cp templates/_meta/template-skeleton.md templates/experiment/README.md`. Edit:
     - Pre-fill `object_type: Experiment` (replace the `<pre-filled per template ...>` placeholder).
     - Pre-fill `status: Draft` (already pre-filled in skeleton; confirm preserved).
     - Replace the H1 `<Artifact name>` with `# Experiment`.
     - Replace the one-paragraph description below H1 with one paragraph naming the two child files, citing HANDOVERS Handover 3, naming the `assumption-threshold-lock` hook.
     - Replace the body section heading templates with the two README H2 sections from the spec (`## What this folder is`, `## How to use this template`).
     - Keep the universal-schema frontmatter block ordering identical to the skeleton.
     - Append a Handover-3 cross-reference one-liner under `# Handover-specific fields` comment (link to HANDOVERS Handover 3 anchor); the README itself does not encode the full `test:` block (that's on the Learning Memo per F3.5).
     - **Source marker:** the two H2 sections are inferred (folder-index orientation; no HANDOVERS verbatim source) — already documented in spec §"Required sections".
  3. **experiment.md — author from scratch.** Frontmatter (in two blocks):
     - Block 1 (subset of universal schema relevant to a design artifact — the file is a child of the folder template, not the README, so it does not need to mirror the full universal-schema superset; it carries the minimum the linter and the hook require — the linter requires `object_type`, `status`, `last_updated` on every artifact per `tools/lint-frontmatter.py` lines 169 / 227):
       - `object_type: Experiment` (pre-filled)
       - `slug: <experiment-id>` (placeholder)
       - `name: <one-line experiment name>` (placeholder)
       - `description: <one to three sentences>` (placeholder)
       - `owner: <named human>` (placeholder)
       - `status: Draft` (pre-filled — linter-required, identity-pinned)
       - `last_updated: <YYYY-MM-DD>` (placeholder — linter-required)
       - `created: <YYYY-MM-DD>` (placeholder; matches the hook's documented frontmatter block)
       - `parent_opportunity: <discovery opportunity id>` (placeholder; traceability)
       - `parent_intent: <strategy intent slug>` (placeholder; traceability)
       - `human_owned_decisions:` with the two values from the hook documentation block verbatim (`Threshold selection`, `Survived/killed call on ambiguous results`) — per spec Open Question 3 resolution.
       - `human_approval_required: true` (pre-filled per spec Open Question 3).
       - `ai_assistance_allowed: <true | restricted | not-allowed>` (placeholder)
     - Block 2 (under `# Handover-specific fields (per assumption-threshold-lock hook contract)` YAML comment):
       - `parent_assumption: <ASM-NNN from the assumption map>` (placeholder; traceability to Handover 2.5)
       - `predeclared_threshold:` as a nested map with `success: <quantitative criterion>` and `falsification: <quantitative criterion>` placeholders. **Quoted verbatim from HANDOVERS Handover 3 `test.predeclared_threshold:` and from the hook documentation.**
       - `predeclared_at: <YYYY-MM-DD>` (placeholder; **quoted verbatim from HANDOVERS Handover 3 `test.predeclared_at:`**)
       - `sample_target: <n>` (placeholder; per hook documentation)
       - `duration: <days>` (placeholder; per hook documentation)
       - Override-quad as commented-out optional fields with one-line explanations: `# override_threshold_lock: true   # set only when capturing results from a non-predeclared test (rare)`, `# override_reason: <one-paragraph explanation>`, `# override_authorized_by: <name>`, `# override_authorized_at: <YYYY-MM-DD>`. Sourced from `.claude/hooks/assumption-threshold-lock.md` override section.
     - Body: H1 `# Experiment: <one-line name>`. One-paragraph blockquote citing HANDOVERS Handover 3 and the hook contract. Then the six H2 sections in spec order, each with a one-line `<placeholder body>` paragraph:
       1. `## The assumption tested` — *(inferred section)*
       2. `## The method` — *(inferred section)*
       3. `## Predeclared thresholds` — *(sourced from hook contract; body mirrors the frontmatter values in prose)*
       4. `## Sample and duration` — *(inferred section)*
       5. `## Risks and ethical considerations` — *(inferred section)*
       6. `## Disposition plan` — *(inferred section)*
     - Optional sections heading at the bottom (per skeleton convention): `## Optional sections` with one example optional sub-section `### Notes`.
     - **Source markers** are added as inline HTML comments inside the body next to each H2 heading so an adversarial reviewer can see at a glance which sections derive from HANDOVERS verbatim and which are inferred from validation-design practice. Format: `<!-- source: inferred -->` or `<!-- source: assumption-threshold-lock hook contract -->`.
  4. **results.md — author from scratch.** Frontmatter:
     - `object_type: Experiment` (pre-filled — same ontological object as design file, per spec Open Question 2 resolution)
     - `slug: <same as experiment.md slug>` (placeholder)
     - `name: <one-line experiment name — match experiment.md>` (placeholder)
     - `status: Draft` (pre-filled — linter-required; kit user updates to a post-run lifecycle state when filling in results)
     - `last_updated: <YYYY-MM-DD>` (placeholder — linter-required)
     - `created: <YYYY-MM-DD>` (placeholder)
     - `parent_experiment: experiment.md` (literal sibling-file pointer; **editorial addition for kit-user navigation; not a hook-contract requirement.** This is the only concrete non-placeholder value besides identity fields, because the sibling file name is pinned by the hook contract — and the linter's `--check-template` mode allows concrete values that pass type/enum checks. Document this exception in the body comment.)
     - `result:` as a nested map with the four sub-keys: `actual: <value>`, `status: <survived | killed>`, `decided: <YYYY-MM-DD>`, `decided_by: <names>`. **Quoted verbatim from HANDOVERS Handover 3 `result:` block.** Note: `result.status` is the experiment-disposition enum (`survived | killed`) and is intentionally distinct from the top-level `status:` lifecycle field (`Draft`, etc.) — both are simultaneously present in the frontmatter at different YAML paths.
     - `human_owned_decisions:` with values from HANDOVERS Handover 3 verbatim (`Whether to survive or kill on ambiguous results`, `Whether to proceed to delivery given remaining open assumptions`).
     - `human_approval_required: true`
     - `ai_assistance_allowed: <true | restricted | not-allowed>` (placeholder)
     - Body: H1 `# Experiment results: <one-line name>`. One-paragraph blockquote citing HANDOVERS Handover 3 and the experiment.md sibling. Then the three H2 sections in spec order with `<placeholder body>`:
       1. `## The result` — *(sourced from HANDOVERS Handover 3 §"Required sections" item 3 verbatim)*
       2. `## What we learned` — *(sourced from HANDOVERS Handover 3 §"Required sections" item 4 verbatim)*
       3. `## The disposition` — *(sourced from HANDOVERS Handover 3 §"Required sections" item 5 verbatim)*
     - Source markers as inline HTML comments next to each H2.
  5. **VERIFY.** Run T1 through T12 in order:
     - `test -d` and `test -f` for T1.
     - Three `python3 tools/lint-frontmatter.py --check-template <path>` invocations for T2a/T2b/T2c.
     - Three python YAML-parse one-liners for T3a/T3b/T3c, walking the keys.
     - Three `grep -n` invocations checking H2 monotonicity for T4a/T4b/T4c.
     - One `grep -rc` invocation across the folder for T5.
     - `python3 -m pytest scripts/tests/test_templates_instantiate.py` for T6.
     - `bash tools/pre-pr.sh` for T7. Iterate any reds.
     - One `grep -E` invocation per file for T10.
     - One `python3 tools/lint-frontmatter.py --all` invocation for T11; assert exit 0 (default mode does not traverse `templates/` — the load-bearing mode-separation property).
     - One python one-liner for T12a (parse `experiment.md` frontmatter; assert `predeclared_threshold` is a dict with non-empty placeholder `success` and `falsification`).
     - One python one-liner for T12b (assert `predeclared_at` is a placeholder, not an ISO date).
     - `test -f` for T12c (restates T1 paths).
     - Defer T8 and T9 to CAPTURE.
  6. **REVIEW.** Dispatch `adversarial-reviewer` against all three files versus the constraint set (HANDOVERS §"Handover 3", `assumption-threshold-lock` hook contract, ontology Domain C). Max 3 iterations per work-loop default. Any Blocking finding fixed in-session; non-blocking findings tracked in spec's open-questions / risks as appropriate.
  7. **CAPTURE.** In a single small commit at the end of the loop (per parent plan §Rollout — sequential README appends across F3.x workers):
     - Append a one-line entry to `templates/_meta/README.md` under "Shipped templates": `- \`experiment/\` — Experiment design + results folder template (per HANDOVERS Handover 3 + assumption-threshold-lock hook).` (T9).
     - Flip ROADMAP F3.4 checkbox: `- [ ] **F3.4**` → `- [x] **F3.4**`. (T8).
     - Update `docs/specs/template-experiment/spec.md` Status: `Shipped (<YYYY-MM-DD>)`.
     - Update `docs/specs/template-experiment/plan.md` Status: `Done (<YYYY-MM-DD>)` and append a changelog entry.
- **Done when:** T1–T13 all pass; pre-pr-clean exits 0; adversarial review returns 0 Blocking findings.

## Rollout

- ROADMAP P3.3 (`experiment-template` skill) is unblocked once this template lands. P3.4 (`/design-experiment`) is unblocked by P3.3. The Validation phase gains a canonical authoring path that lands kit users directly in the layout the `assumption-threshold-lock` hook polices.
- `templates/_meta/README.md` gets a new "Shipped templates" entry. Per parent plan §Rollout, the F3.x workers' README appends are sequential — this F3.4 worker's append happens at CAPTURE time in its own commit.
- `docs/HANDOVERS.md` Handover 3 cross-references the experiment artifact via the Learning Memo's `test.experiment:` link; no edit to HANDOVERS is required (F3.4 is a downstream re-projection).
- AGENTS.md and INVENTORY.md: no row added. The template is infrastructure (same pattern as `templates/_meta/template-skeleton.md`); the parent convention spec already established that templates are not INVENTORY rows.
- F3.5 (Learning Memo template) consumes the layout contract (its `test.experiment:` link must resolve to a folder containing both `experiment.md` and `results.md`). F3.5's spec will cite F3.4 in its `Constrained by:` block; coordinated via the parent F3 fan-out aggregate step.

## Risks

- **Section taxonomy not directly from HANDOVERS.** HANDOVERS Handover 3 enumerates Learning Memo sections, not Experiment-internal sections. The six design-phase headings (`The assumption tested`, `The method`, `Predeclared thresholds`, `Sample and duration`, `Risks and ethical considerations`, `Disposition plan`) and the three results-phase headings are inferred from validation-design practice and the hook contract. **Mitigation:** each section heading is marked with a source comment (HANDOVERS-verbatim vs inferred) in the body; adversarial review explicitly checks the inferred set against predecessor validation frameworks (e.g., Teresa Torres's continuous-discovery experiment design pattern, the kit's own `context/frameworks/assumption-tests.md` *(planned — ROADMAP F4.4)*). If adversarial review rejects the taxonomy, iterate within the 3-pass limit; if no convergence, surface to parent fan-out aggregate and defer to a separate framework-authoring spec.
- **Ontology naming for `object_type:` on the results file.** Domain C lists only `Experiment`. Both design and results files share that type per spec Open Question 2. **Mitigation:** documented in the spec; if F3.5's adversarial review surfaces a contradiction, reconcile by editing the ontology in a separate spec (not in the F3.4 loop). If a contradiction surfaces in F3.4's own adversarial review, surface and defer.
- **Linter recursion on `predeclared_threshold` nested placeholders.** The parent spec asserts T8f (nested-container with all placeholders passes) and T8h (nested malformed placeholder rejects). This template depends on T8f's behaviour. **Mitigation:** T2b explicitly invokes the linter on `experiment.md`; if recursion fails, the failure is local to the linter (already shipped 2026-05-22 with T8f passing), not to this template. No mitigation owed at the F3.4 level.
- **`parent_experiment: experiment.md` on results.md is the only concrete non-placeholder value in the template body other than identity fields.** The linter's `--check-template` mode accepts concrete values that pass type/enum checks; `parent_experiment` has no enum (it's a free-form string field), so the concrete value `experiment.md` will pass. **Mitigation:** confirmed by inspecting `tools/lint-frontmatter.py` behavior for untyped fields. If the linter's concrete-value validation rejects this string in a future change, T2c catches it.
- **Pytest harness might not auto-discover `experiment.md` and `results.md`.** The harness globs `templates/*.md` and `templates/*/README.md` (per `scripts/tests/test_templates_instantiate.py`). Child files inside a folder template are NOT auto-discovered. **Mitigation:** the spec acknowledges this explicitly under §Non-goals — child file coverage is asserted via spec-local T2b and T2c shell invocations during VERIFY, not by amending shared infrastructure. The acceptance criteria treat T2b and T2c as first-class gates, so the children are covered.

## Changelog

Append entries when the plan changes substantially during execution. Format: `<YYYY-MM-DD>: <one-line description of the change and why>`.

- 2026-05-22 (review-iter-1): Applied adversarial-reviewer fixes — C1 (Always-do bullet layering correction), C2 (T11 description), D1 (folder-template authorization cite), H1 (unfilled-placeholder hook behavior), V1 (vague claim removed), SC1 (parent_experiment editorial label), E1 (OQ-Z CI coverage gap), cross-cutting dedup convention bullet added.
