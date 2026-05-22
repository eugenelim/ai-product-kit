# Spec: template-experiment

- **Status:** Shipped (2026-05-22)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template
- **Serves kit phase:** Validation
- **Constrained by:** [`docs/specs/template-authoring-convention/spec.md`](../template-authoring-convention/spec.md) (parent contract — placeholder syntax, frontmatter ordering, pre-fill rules, linter contract, skeleton-as-copy-source, folder-template layout rule); `docs/HANDOVERS.md` §"Handover 3: Validation → Vision" (source-of-truth for the `test:` block the Learning Memo cites against `validation/experiments/<id>/`, quoted verbatim below); `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" and §"Universal metadata schema" (frontmatter superset, ordering, folder-template layout); `context/frameworks/ontology.md` Domain C row "Experiment" (the ontology type this template instantiates); `.claude/hooks/assumption-threshold-lock.md` + `scripts/check-assumption-threshold.py` (the hook contract that pins the two-file `validation/experiments/<id>/experiment.md` + `results.md` layout, the required `predeclared_threshold:` map shape, and the design-mtime-predates-results rule); ROADMAP F3.4.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `templates/experiment/` — a folder template with `README.md` (folder index, universal-schema frontmatter), `experiment.md` (design skeleton, carries `predeclared_threshold:` + `predeclared_at:` per the hook contract), and `results.md` (results skeleton, carries `result:` block). The two child files are the kit-user-instantiated artifacts at `validation/experiments/<id>/experiment.md` and `validation/experiments/<id>/results.md` — the exact file names the `assumption-threshold-lock` hook enforces. A kit user copies the folder, fills the design, runs the experiment, then fills the results — producing the artifact pair that the Learning Memo's `test:` block (Handover 3) cites via `experiment: <link to validation/experiments/<id>/>`.

## Objective

`templates/experiment/` is the folder skeleton for the Experiment artifact pair — the load-bearing scaffold underneath HANDOVERS Handover 3 (Validation → Vision). Today, a kit user wanting to draft an experiment has no copyable starting point: they would have to read HANDOVERS Handover 3 (which contracts the Learning Memo, not the experiment files), the `assumption-threshold-lock` hook documentation, the hook's source (to learn the exact frontmatter keys the hook parses — `predeclared_threshold.success`, `predeclared_threshold.falsification`, `predeclared_at`, plus the override-quad), the universal-metadata schema, the ontology Domain C row, and `templates/_meta/template-skeleton.md`, and stitch them together themselves — and they'd very likely get the file names wrong, the hook would then silently treat the artifact as out-of-glob, and validation theatre would slip through. This template collapses that into one `cp -r templates/experiment/ validation/experiments/<id>/` followed by placeholder replacement. The folder's shape — README.md plus exactly the two child file names `experiment.md` and `results.md` — IS the contract: the child file names match the hook's regex (`validation/experiments/.+/results\.md$`) and its sibling-design-file lookup (`exp_dir / "experiment.md"`). Pre-filled fields are identity-only: `object_type: Experiment` and `status: Draft` on the README and on `experiment.md`; everything else is an angle-bracket placeholder. The closest prior context in the repo is `templates/_meta/template-skeleton.md` (the shape contract this template copies for its README and adapts for its children), `.claude/hooks/assumption-threshold-lock.md` (the contract this template encodes), and `scripts/check-assumption-threshold.py` (the implementation that parses what the template lays down).

## Why now

ROADMAP F3.4 sits in the F3 block — the ten templates that the parent `template-authoring-convention` spec made parallelizable. P3.3 (`experiment-template` skill) explicitly depends on F3.4: its `Depends on:` line in ROADMAP names this row. Until F3.4 ships, P3.3 is blocked, `/design-experiment` (P3.4, depends on P3.3) is blocked, and the Validation phase has no canonical authoring path for experiments — leaving the `assumption-threshold-lock` hook as the only line of defence against validation theatre, with no upstream scaffold guiding kit users into the layout the hook expects. Shipping F3.4 closes the gap on the design side: when a kit user copies the template, they land in the layout the hook already polices. The parent convention shipped 2026-05-22, so the contract surface F3.4 consumes is stable. The hook (F2.2) shipped earlier; its source is the load-bearing constraint this template encodes.

## Inputs and outputs

**Inputs.**

- `templates/_meta/template-skeleton.md` — the canonical skeleton this template copies for its `README.md` (read-only; not edited by this spec).
- `docs/HANDOVERS.md` §"Handover 3: Validation → Vision" — source-of-truth for the `test:` frontmatter block that the Learning Memo cites against the experiment. Quoted verbatim below.
- `.claude/hooks/assumption-threshold-lock.md` — contract for the experiment-design frontmatter (`object_type: Experiment`, `predeclared_threshold:` with `success:` + `falsification:`, `predeclared_at:`, plus the override-quad `override_threshold_lock`, `override_reason`, `override_authorized_by`, `override_authorized_at`). The hook's documentation block is the canonical experiment-design frontmatter shape.
- `scripts/check-assumption-threshold.py` — the implementation. Read for: the exact regex enforcing `validation/experiments/.+/results\.md$` (pins the child file name `results.md`); the sibling lookup `exp_dir / "experiment.md"` (pins the child file name `experiment.md`); the required map shape of `predeclared_threshold` (must be a dict with `success` and `falsification` keys, both non-empty); the future-date rejection on `predeclared_at`; the design-mtime-predates-results-write-by->=1s rule.
- `docs/CONVENTIONS.md` §"Universal metadata schema" — universal frontmatter superset (inherited by the README).
- `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" — authoring convention. Specifically the "File layout" sub-section, which permits folder templates `templates/<slug>/` containing a `README.md` plus per-child-file templates where children carry their own frontmatter iff they instantiate a distinct ontology object.
- `context/frameworks/ontology.md` Domain C row "Experiment" (line 64: "Test designed to validate / invalidate an assumption") — confirms the `object_type:` pre-fill value as the single token `Experiment`.
- `tools/lint-frontmatter.py --check-template` — the linter gate every file in the template must pass.

**Outputs.**

1. `templates/experiment/README.md` — new file. Folder index. Universal-schema frontmatter (per skeleton) plus a brief Handover-3 cross-reference block. Pre-filled: `object_type: Experiment`, `status: Draft`. Body is a one-paragraph orientation that names the two child files, names the hook that polices them, and tells the kit user the copy-and-fill sequence (design first, run experiment, then results). Auto-discovered by `scripts/tests/test_templates_instantiate.py` via the `*/README.md` glob.
2. `templates/experiment/experiment.md` — new file. The **design** skeleton. Carries its own frontmatter (distinct ontology object — same `Experiment` type, design phase). Frontmatter fields pinned by the hook contract: `object_type: Experiment` (pre-filled), `slug: <experiment-id>` (placeholder), `status: Draft` (pre-filled — required by linter), `last_updated: <YYYY-MM-DD>` (placeholder — required by linter), `created: <YYYY-MM-DD>` (placeholder), `parent_assumption: <ASM-NNN from the map>` (placeholder, traceability to Assumption Map), `predeclared_threshold:` (nested map with `success:` and `falsification:` placeholders), `predeclared_at: <YYYY-MM-DD>` (placeholder; hook rejects future-dated values), `sample_target: <n>` (placeholder), `duration: <days>` (placeholder), plus the override-quad as commented-out optional fields with one-line explanations. Body sections per §"Required sections" below.
3. `templates/experiment/results.md` — new file. The **results** skeleton. Carries its own frontmatter (distinct ontology object — same `Experiment` type, post-run phase; see Open Question 2 for ontology-naming rationale). Frontmatter fields: `object_type: Experiment` (pre-filled), `slug: <same as experiment.md slug>` (placeholder), `status: Draft` (pre-filled — required by linter; kit user updates to a post-run state when filling), `last_updated: <YYYY-MM-DD>` (placeholder — required by linter), `result:` block per HANDOVERS Handover 3 (`actual: <value>`, `status: <survived | killed>`, `decided: <YYYY-MM-DD>`, `decided_by: <names>` — note: `result.status` is the experiment-disposition enum and is distinct from the top-level `status:` lifecycle field). Body sections per §"Required sections" below.
4. `templates/_meta/README.md` — one-line append under "Shipped templates": `experiment/` (folder template). CAPTURE-phase only; tiny dedicated commit per parent plan §Rollout to avoid races with other F3.x workers.
5. `ROADMAP.md` — F3.4 checkbox marked. CAPTURE-phase only.
6. `docs/specs/template-experiment/spec.md` and `plan.md` frozen to `Status: Shipped (<date>)` / `Status: Done (<date>)` (CAPTURE phase only).

**Required Handover-3 `test:` frontmatter block (quoted verbatim from `docs/HANDOVERS.md` §"Handover 3: Validation → Vision").** This is the contract surface the Experiment artifact must shape so the Learning Memo (the actual Handover-3 artifact, owned by F3.5) can cite it cleanly:

```yaml
test:
  type: desirability | viability | feasibility | usability | ethical
  experiment: <link to validation/experiments/<id>/>
  predeclared_threshold:
    success: <quantitative criterion>
    falsification: <quantitative criterion>
  predeclared_at: <YYYY-MM-DD>     # MUST be before experiment ran
```

Plus the results block, also quoted from HANDOVERS:

```yaml
result:
  actual: <value>
  status: survived | killed
  decided: <YYYY-MM-DD>
  decided_by: <names>
```

Note on layering: HANDOVERS Handover 3 is the **Learning Memo** contract; the `test:` and `result:` blocks live on the Learning Memo's frontmatter and reference the experiment via `test.experiment: <link to validation/experiments/<id>/>`. The Experiment artifact (the thing this template scaffolds) is what that link points at. The experiment design file (`experiment.md`) carries the predeclared-threshold contract directly (per the `assumption-threshold-lock` hook source); the results file (`results.md`) carries the actual measurement. The Learning Memo (F3.5) re-encodes both blocks on its own frontmatter, citing the experiment by link — the template here makes that round-trip mechanical: a Learning Memo author copies the `predeclared_threshold:` block off the experiment and the `result:` block off the results file.

**Single-file vs two-file resolution.** Resolved: **two child files** (`experiment.md` + `results.md`) inside a folder template `templates/experiment/`. Rationale: the `assumption-threshold-lock` hook (`scripts/check-assumption-threshold.py`) hard-codes the file names. Its regex `validation/experiments/.+/results\.md$` pins `results.md`, and its sibling lookup `exp_dir / "experiment.md"` pins `experiment.md`. Its design-predates-results check uses `os.path.getmtime` on `experiment.md` vs the results-write event — which **requires two physical files with distinct mtimes**. A single-file template merging design and results into one document would either (a) collapse the two writes into one mtime, killing the predeclared-threshold guard; or (b) require the kit user to manually split the single file into two at instantiation time, undoing the whole "copy and fill" affordance and creating a silent class of kit-user error in which the hook treats the artifact as out-of-glob and lets the write through. Two child files preserve the hook's contract by construction. The cost — kit user copies a folder rather than a file — is trivial; the folder layout is already a supported pattern in the parent convention (per `docs/CONVENTIONS.md` §"Templates" → "File layout"). See §"Open questions" Q1 for the explicit comparison.

**Required sections (sourced explicitly; HANDOVERS does NOT enumerate per-experiment internal sections — the experiment's required-section taxonomy is inferred here from validation-design practice and from what the hook plus the Learning Memo's downstream `test:` block need).**

For `experiment.md` (design phase — six H2 sections, ordered):

1. **The assumption tested** — restate the assumption from the Assumption Map (Handover 2.5); name its lens (desirability / viability / feasibility / usability / ethical) and its risk-if-wrong rank. *(Inferred — standard validation-design taxonomy; also the upstream link to the Assumption Map artifact.)*
2. **The method** — what the experiment does mechanically; how subjects encounter the stimulus; what data is captured. One paragraph plus a short bullet list. *(Inferred — standard validation-design taxonomy.)*
3. **Predeclared thresholds** — the `success:` and `falsification:` criteria, in prose, mirroring the frontmatter. The body restates the frontmatter values so a reader scanning the markdown sees the threshold without parsing YAML; the frontmatter is the machine-readable contract. **This section is non-negotiable** — it's the kit's anti-theatre guard. *(Sourced from the `assumption-threshold-lock` hook contract — the `predeclared_threshold:` block and `predeclared_at:` timestamp are pinned by the hook.)*
4. **Sample and duration** — `sample_target:` rationale (why N is enough); `duration:` window; stopping rule (do we stop early if the falsification threshold is hit, or run the full window?). *(Inferred — standard validation-design taxonomy.)*
5. **Risks and ethical considerations** — what could go wrong with running this experiment (not with the outcome — with the act of running it). Cite ethics if the experiment involves users / real data / customer exposure. *(Inferred — required by the kit's `human_owned_decisions:` and the ontology Domain C "Experiment" obligation to surface harm before running.)*
6. **Disposition plan** — what we'll do on `survived` vs `killed`. Predeclared so the result doesn't get re-interpreted post-hoc. *(Inferred — the kit's "would we actually pull the work?" test, the assumption-skeptic's central question.)*

For `results.md` (post-run — three H2 sections, ordered):

1. **The result** — the measured value vs the predeclared threshold. Cite the experiment.md file. *(Sourced from HANDOVERS Handover 3 §"Required sections" item 3 verbatim: "The result — actual measurement vs predeclared thresholds.")*
2. **What we learned** — separate from whether we proceed. *(Sourced from HANDOVERS Handover 3 §"Required sections" item 4 verbatim.)*
3. **The disposition** — `survived` or `killed`; the human decision-maker named; what changes next. *(Sourced from HANDOVERS Handover 3 §"Required sections" item 5 verbatim.)*

For `README.md` (folder index — two H2 sections, ordered):

1. **What this folder is** — one-paragraph orientation: this is an Experiment artifact (per ontology Domain C); it pairs with an Assumption Map (Handover 2.5) and feeds a Learning Memo (Handover 3); the `assumption-threshold-lock` hook polices the design-predates-results rule. *(Inferred — folder index orientation.)*
2. **How to use this template** — step list: copy the folder to `validation/experiments/<id>/`; fill `experiment.md` (design); commit; run the experiment; only then fill `results.md`. Name the hook that enforces this and what happens on override. *(Inferred — folder index orientation.)*

**Downstream consumers.** ROADMAP P3.3 (`experiment-template` skill) reads `templates/experiment/` as its scaffolding source. F3.5 (Learning Memo template, in the same F3 fan-out) cites the experiment via `test.experiment:` link — F3.5 does not consume this template's file *content* but consumes its *layout contract* (so the link target resolves to a folder containing both `experiment.md` and `results.md`). No other shipped or planned ROADMAP row consumes the template directly.

## Boundaries

### Always do

- Use the folder layout `templates/experiment/` with the three files `README.md`, `experiment.md`, `results.md` — file names pinned by the `assumption-threshold-lock` hook contract (`results.md` regex + `experiment.md` sibling lookup). `experiment/` is the first non-listed folder template in the kit; authorized by the parent convention spec's enumeration "Multi-file template (folders such as Initiative, Handoff Packet)" (`docs/specs/template-authoring-convention/spec.md`, the "such as" language being non-exhaustive).
- Use angle-bracket placeholder syntax exclusively (`<descriptor>`); inherit the skeleton's placeholder discipline. Nested-container placeholders (`predeclared_threshold: {success: <…>, falsification: <…>}`) are accepted by the parent linter's recursive rule (per parent spec T8f / T8h).
- Quote the Handover-3 `test:` and `result:` frontmatter blocks verbatim where they appear. On `experiment.md`, `predeclared_threshold` and `predeclared_at` are carried as **flat top-level frontmatter keys** (per the hook source `scripts/check-assumption-threshold.py` — distinct from the `test.` nesting on the Learning Memo). On `results.md`, the `result:` block is carried as a nested map mirroring the `result.*` keys on the Learning Memo.
- Pre-fill the template's identity fields and only those: `object_type: Experiment` on all three files where applicable; `status: Draft` on README and `experiment.md`. Every other field is a placeholder.
- Keep the README's universal-schema frontmatter block ordering identical to `templates/_meta/template-skeleton.md` (the parent convention pins ordering).
- On `experiment.md`, append the design-specific fields (`parent_assumption`, `predeclared_threshold`, `predeclared_at`, `sample_target`, `duration`, and the optional override-quad as commented-out placeholders) under a `# Handover-specific fields (per assumption-threshold-lock hook contract)` YAML comment as a second block.
- Visually separate the **pre-run design block** (everything in `experiment.md`) from the **post-run results block** (everything in `results.md`) by the file boundary itself — this is the load-bearing property that lets the hook compare mtimes.
- Pass `tools/lint-frontmatter.py --check-template <path>` against all three files (README.md, experiment.md, results.md) and pass `python3 -m pytest scripts/tests/test_templates_instantiate.py` cleanly before CAPTURE.
- **Cross-cutting dedup convention.** When HANDOVERS-3-derived fields overlap with the universal-metadata schema (e.g., `human_owned_decisions:` on `experiment.md`), the field appears once — in its universal-schema position on the relevant child file — carrying the HANDOVERS-3-mandated value. The universal-schema placeholder is deleted in the same edit. The handover-specific block on each child carries only fields not present in the universal schema.

### Ask first

- Adding a frontmatter field to `experiment.md` not present in `.claude/hooks/assumption-threshold-lock.md`'s documented frontmatter block. The hook's documentation block is the canonical source; the template is downstream.
- Adding a seventh required H2 section to `experiment.md` or a fourth to `results.md`. The taxonomies above are deliberate; expanding either requires the surrounding-docs-update justification.
- Pre-filling `type: <lens>` on the Learning Memo's `test:` block from inside this template. The `type:` field lives on the Learning Memo (F3.5), not on the experiment artifact; this template stays on its side of the line.

### Never do

- Invent domain content. The template body is shape-only: H2 headings plus one-line `<placeholder>` bodies. No example experiments, no real assumptions, no real thresholds.
- Use `{{...}}` or `__FILL__` placeholder syntax anywhere. The parent convention permits angle-bracket only; T16 in the parent spec greps these from any template.
- Rename either child file. The hook's regex and sibling lookup pin `experiment.md` and `results.md` — any other name silently bypasses the guard.
- Pre-fill `predeclared_at:` to today's date (or any date). The hook rejects future-dated values; a date pre-fill would also encourage retroactive editing — the opposite of the predeclared-threshold contract. Leave it as the angle-bracket placeholder.
- Loosen the threshold contract by making `predeclared_threshold` a single string instead of the `{success, falsification}` map. The hook parses the map shape; collapsing it would break the hook.
- Add `Experiment Design` or `Experiment Results` as new ontology types. Templates are kit-build scaffolding; the ontology only carries instantiated-artifact types and the single `Experiment` row already covers both design and results phases.
- Modify `.claude/hooks/assumption-threshold-lock.md`, `scripts/check-assumption-threshold.py`, `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, or `scripts/tests/test_templates_instantiate.py`. If reality demands a contract edit during EXECUTE, surface as an adversarial-review finding and resolve in a separate spec; do not silently rewrite source-of-truth inside the F3.4 loop.
- Walk `templates/experiment/` from the default-mode linter. The linter contract (parent spec) keeps `templates/` outside `PHASE_DIRS`; only `--check-template` runs against it.

## Verification mode

- **Goal-based check** for the template's shape — required headings present in order, required frontmatter keys present (incl. nested `predeclared_threshold.success` and `predeclared_threshold.falsification`), placeholder-syntax purity. Each check is a one-line shell or python predicate.
- **Audit-driven** for the linter and pytest gates: `python3 tools/lint-frontmatter.py --check-template templates/experiment/README.md`, `… --check-template templates/experiment/experiment.md`, `… --check-template templates/experiment/results.md` each exit 0; `python3 -m pytest scripts/tests/test_templates_instantiate.py` (which auto-discovers `templates/experiment/README.md` via the `*/README.md` glob) exits 0; `bash tools/pre-pr.sh` exits 0.
- **Manual gesture** for the hook contract — verify by inspection (no need to actually run the hook) that the experiment.md frontmatter, when copied to `validation/experiments/<id>/experiment.md`, would pass `scripts/check-assumption-threshold.py`'s `check_threshold_fields` (the `predeclared_threshold:` block has both `success` and `falsification` keys; the `predeclared_at:` placeholder is positioned at top-level frontmatter; the override-quad is present-but-commented). The manual gesture records: "If a kit user backdates `predeclared_at:` to a future value or writes `results.md` without the design file existing first, the hook blocks the write. If the placeholder `<YYYY-MM-DD>` is left unfilled when results are written, the hook blocks with a parse-error on the date (`datetime.date.fromisoformat()` raises), not a future-date error." This is the kit's most important guard.
- **Adversarial review** (manual gesture against the shipped template files) — dispatch the `adversarial-reviewer` subagent against the three template files versus HANDOVERS §"Handover 3", the hook contract, and ontology Domain C. Iterate fixes inline; max 3 review passes per the work-loop default.

The template is done when T1–T12 all pass and the adversarial review returns 0 blocking findings.

## Contract tests

Each test is one shell line or one pytest case.

- `T1` — `test -d templates/experiment && test -f templates/experiment/README.md && test -f templates/experiment/experiment.md && test -f templates/experiment/results.md` exits 0 (target folder + three child files exist).
- `T2a` — `python3 tools/lint-frontmatter.py --check-template templates/experiment/README.md` exits 0.
- `T2b` — `python3 tools/lint-frontmatter.py --check-template templates/experiment/experiment.md` exits 0.
- `T2c` — `python3 tools/lint-frontmatter.py --check-template templates/experiment/results.md` exits 0.
- `T3a` — README frontmatter contains the full universal-schema key set inherited from the skeleton (asserted by a python one-liner that parses YAML and checks every skeleton key is present at top level).
- `T3b` — `experiment.md` frontmatter contains the linter-required keys plus the design-specific keys pinned by the hook: `object_type`, `status`, `last_updated` (linter requires these three on any artifact), `slug`, `created`, `parent_assumption`, `predeclared_threshold` (a map with `success` and `falsification` sub-keys), `predeclared_at`, `sample_target`, `duration`. Asserted by a python one-liner that parses YAML and walks the keys, including the nested `predeclared_threshold.success` and `predeclared_threshold.falsification`.
- `T3c` — `results.md` frontmatter contains the linter-required keys plus the results-specific keys pinned by HANDOVERS Handover 3 `result:` block: `object_type`, `status`, `last_updated`, `slug`, `result` (a map with `actual`, `status`, `decided`, `decided_by` sub-keys — `result.status` is the experiment-disposition enum, distinct from the top-level `status:` lifecycle field). Asserted by a python one-liner.
- `T4a` — `experiment.md` required H2 headings present in order: `## The assumption tested`, `## The method`, `## Predeclared thresholds`, `## Sample and duration`, `## Risks and ethical considerations`, `## Disposition plan`. Asserted by `grep -n` recording line numbers and checking monotonicity.
- `T4b` — `results.md` required H2 headings present in order: `## The result`, `## What we learned`, `## The disposition`. Asserted by `grep -n`.
- `T4c` — `README.md` required H2 headings present in order: `## What this folder is`, `## How to use this template`. Asserted by `grep -n`.
- `T5` — Angle-bracket-only placeholder syntax across all three files: `grep -rc '{{' templates/experiment/` returns 0 and `grep -rc '__FILL__' templates/experiment/` returns 0.
- `T6` — Pytest harness picks the README up and passes: `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (the parametrized `test_template_passes_check_template_mode` test will include `templates/experiment/README.md` via the `*/README.md` glob).
- `T7` — `bash tools/pre-pr.sh` exits 0 (kit-wide health check after the template lands).
- `T8` — ROADMAP F3.4 checkbox flipped: `grep -c '^- \[x\] \*\*F3\.4\*\*' ROADMAP.md` returns 1 (CAPTURE-phase predicate).
- `T9` — `templates/_meta/README.md` lists the template: `grep -c 'experiment/' templates/_meta/README.md` returns >= 1 (CAPTURE-phase predicate).
- `T10` — Pre-filled identity fields are exact: `grep -E '^object_type: Experiment$' templates/experiment/README.md` returns 1; same on `experiment.md`; same on `results.md`. `grep -E '^status: Draft' templates/experiment/README.md` returns 1; same on `experiment.md`.
- `T11` — Default-mode linter does NOT walk `templates/` (mode-separation safety): `python3 tools/lint-frontmatter.py --all` exits 0 (no errors reported against `templates/experiment/**`). This pins the load-bearing property the parent convention asserts: `--all` enumerates only `PHASE_DIRS` (`strategy`, `discovery`, `validation`, `delivery`, `market`); if a future linter change ever started walking `templates/` from `--all`, T11 would catch it by failing on the template's placeholder content. **Note:** an earlier draft of this test framed it as "default mode positionally invoked on a template file exits non-zero" — that framing does not hold because once identity fields (`object_type: Experiment`, `status: Draft`, `last_updated: <YYYY-MM-DD>`) are pre-filled with valid values, the linter's default mode (which only checks the universal-schema enums on `object_type`/`status` plus presence of `last_updated`) accepts the template. The real mode-separation guard is that default mode never visits templates automatically, which is what T11 now asserts. Surface to F3 fan-out aggregate: the precedent F3.1 (`template-strategic-intent`) spec's T11 carries the same incorrect framing and should be reconciled.
- `T12` — Hook-contract preservation by construction. Three sub-assertions:
  - `T12a` — `experiment.md`'s frontmatter, when parsed, has `predeclared_threshold` as a dict whose `success` and `falsification` values are placeholder strings (matching the parent linter's `AUGMENTED_PLACEHOLDER` rule) and not empty. This proves the template's predeclared-threshold block has the **shape** the hook's `check_threshold_fields` function inspects (per `scripts/check-assumption-threshold.py` lines 66-83).
  - `T12b` — `experiment.md`'s frontmatter contains `predeclared_at:` as a placeholder string (not a literal date), so the hook's future-date check would not fire on the template itself but would fire on any backdated edit at instantiation time. Asserted by a python one-liner that confirms the value matches the angle-bracket-placeholder rule and does NOT parse as an ISO date.
  - `T12c` — File names are exact: `templates/experiment/experiment.md` and `templates/experiment/results.md` (no `-design.md` / `-results.md` suffix), so the hook's regex `validation/experiments/.+/results\.md$` and sibling lookup `exp_dir / "experiment.md"` resolve cleanly when a kit user copies the folder. Asserted by `test -f` on the exact paths (already covered by T1; T12c restates it under the hook-preservation contract for traceability).
- `T13` — Adversarial-reviewer subagent returns no Blocking findings against the three shipped files versus HANDOVERS §"Handover 3", the hook contract, and ontology Domain C.

## Non-goals

- Authoring an instantiated experiment under `validation/experiments/<id>/`. F3.4 ships the skeleton; the kit user (or P3.3, when shipped) instantiates the artifact.
- Building P3.3 (`experiment-template` skill). Separate ROADMAP row; F3.4 unblocks it but does not implement it.
- Modifying `.claude/hooks/assumption-threshold-lock.md` or `scripts/check-assumption-threshold.py`. The hook contract is the load-bearing constraint; this template is a downstream re-projection. If adversarial review surfaces an actual gap, that becomes a separate spec, not an in-session hook edit.
- Editing `docs/HANDOVERS.md`. The Handover-3 contract is stable; F3.4 is a downstream re-projection only.
- Editing `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, or `scripts/tests/test_templates_instantiate.py`. The pytest harness auto-discovers `templates/experiment/README.md` via the `*/README.md` glob; F3.4 needs no test-harness wiring. The two child files (`experiment.md`, `results.md`) are covered by spec-local T2b and T2c invocations against `--check-template`; their coverage is asserted at acceptance-criteria time, not by amending shared infrastructure.
- Adding a `templates/experiment/CLAUDE.md`-style per-template guidance file. README.md plus the spec are sufficient.
- Authoring F3.5 (Learning Memo template, which is what actually instantiates the Handover-3 `test:` block at its full reach). Separate parallel F3 row.
- Shipping `tools/new-template.sh`. Out of scope per parent spec's §Non-goals.

## Open questions

1. **Single-file vs two-file resolution.** Resolved here: **two child files inside a folder template**, for the reasons in §"Inputs and outputs" ("Single-file vs two-file resolution"). The hook's file-name regex and sibling-lookup behaviour pin the layout; a single file would either kill the predeclared-threshold guard or push the burden of splitting onto every kit user. Two child files preserve the hook contract by construction and only cost the kit user a folder copy instead of a file copy.
2. **Ontology object_type for the results file.** Domain C lists `Experiment` as a single ontology type (`context/frameworks/ontology.md` line 64). Both the design file and the results file carry `object_type: Experiment` — the results file is the same ontological object in its post-run phase, not a separate type. Resolved here: do not invent `Experiment Result` or `Experiment Results` as a new ontology type (per the parent convention's "Never do — Add … as a new ontology type" rule). Both files share `object_type: Experiment`; the lifecycle distinction lives on the `status:` field (`Draft` on design before-run; the kit's broader lifecycle states track the post-run progression). If F3.5's adversarial review surfaces a contradiction (e.g., the Learning Memo's `test.experiment:` link semantically needs a typed-distinct results object), reconcile by editing the ontology in a separate spec — not here.
3. **Should `experiment.md` pre-fill `human_owned_decisions:` and `human_approval_required: true` to match the hook documentation's example block?** Resolved here: yes for the **value pattern** named by the hook docs (`Threshold selection`, `Survived/killed call on ambiguous results`, `human_approval_required: true`), no for any specific decision text. Pre-fill the two-item list with those two strings verbatim (they're already in the hook's documented frontmatter block) and `human_approval_required: true`. Justification: the hook contract documents these as standard; pre-filling reduces the chance a kit user drafts an experiment without flagging the survived/killed judgment as human-owned, which is the second half of the anti-theatre guard.
4. **Should `disposition_plan:` be a frontmatter field or only a body section?** Resolved here: body section only. The hook does not parse a disposition-plan field, and HANDOVERS Handover 3's `result:` block already encodes the post-run disposition via `status: survived | killed`. Adding a `disposition_plan:` field would duplicate the body section and confuse the linter on whether it's free-text or enumerated.
5. **Should the README also enumerate the override-quad fields?** Resolved here: no. The override-quad lives only on `experiment.md` as commented-out optional placeholders with a one-line explanation of when to set them. The README points kit users at the hook documentation for the override path; duplicating it in the README would drift.
6. **OQ-Z: `experiment.md` and `results.md` are not auto-discovered by `scripts/tests/test_templates_instantiate.py`** (its globs cover `templates/*.md` and `templates/*/README.md`); coverage is asserted via spec-local T2b/T2c shell invocations only. _Resolved: known CI coverage gap; closing it would require either (a) expanding the pytest harness glob OR (b) promoting T2b/T2c to a spec-local pytest case in `scripts/tests/`. Track as a follow-up ROADMAP candidate; not in F3.4 scope._

## Acceptance criteria

- [ ] `templates/experiment/` folder exists with three child files: `README.md`, `experiment.md`, `results.md` (asserted by T1).
- [ ] All three files pass `python3 tools/lint-frontmatter.py --check-template <path>` (asserted by T2a, T2b, T2c).
- [ ] README frontmatter contains every key in the universal-schema set (asserted by T3a).
- [ ] `experiment.md` frontmatter contains the design-specific keys including the nested `predeclared_threshold.success` and `predeclared_threshold.falsification` (asserted by T3b).
- [ ] `results.md` frontmatter contains the results-specific keys including the nested `result.actual`, `result.status`, `result.decided`, `result.decided_by` (asserted by T3c).
- [ ] `experiment.md` H2 headings appear in order: `## The assumption tested`, `## The method`, `## Predeclared thresholds`, `## Sample and duration`, `## Risks and ethical considerations`, `## Disposition plan` (asserted by T4a).
- [ ] `results.md` H2 headings appear in order: `## The result`, `## What we learned`, `## The disposition` (asserted by T4b).
- [ ] `README.md` H2 headings appear in order: `## What this folder is`, `## How to use this template` (asserted by T4c).
- [ ] No `{{` or `__FILL__` placeholders across the folder (asserted by T5).
- [ ] `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (asserted by T6).
- [ ] `bash tools/pre-pr.sh` exits 0 (asserted by T7).
- [ ] ROADMAP.md F3.4 row is checked off (asserted by T8).
- [ ] `templates/_meta/README.md` "Shipped templates" list includes `experiment/` (asserted by T9).
- [ ] Pre-filled identity fields are exact across all three files (asserted by T10).
- [ ] Default-mode `--all` linter does NOT visit `templates/experiment/**` (asserted by T11 — mode-separation by non-traversal, not by per-file rejection).
- [ ] `predeclared_threshold:` is a dict with non-empty `success:` and `falsification:` placeholder values, `predeclared_at:` is a placeholder (not a literal date), and the child file names match the hook's regex and sibling lookup exactly (asserted by T12a, T12b, T12c — hook-contract preservation by construction).
- [ ] `adversarial-reviewer` subagent returns no Blocking findings (asserted by T13).

## Cross-references

- **Consumed by:** ROADMAP P3.3 `experiment-template` skill (depends on F3.4 per its `Depends on:` line). ROADMAP F3.5 (Learning Memo template) consumes the layout contract — its `test.experiment:` link resolves to a folder containing both `experiment.md` and `results.md`. Any future kit user authoring an experiment by hand.
- **Consumes:** `templates/_meta/template-skeleton.md` (copied for README); `docs/HANDOVERS.md` §"Handover 3: Validation → Vision" (quoted `test:` and `result:` blocks); `docs/CONVENTIONS.md` §"Templates" (folder-layout rule) and §"Universal metadata schema"; `context/frameworks/ontology.md` Domain C row "Experiment"; `.claude/hooks/assumption-threshold-lock.md` + `scripts/check-assumption-threshold.py` (the canonical experiment-design frontmatter shape and file-name pins); `tools/lint-frontmatter.py --check-template`; `scripts/tests/test_templates_instantiate.py`.
- **Frontmatter fields owned:** the template encodes (at the template level — canonical source remains the hook contract for design and HANDOVERS for results) the design-specific keys `parent_assumption`, `predeclared_threshold` (with nested `success`, `falsification`), `predeclared_at`, `sample_target`, `duration`, plus the optional override-quad `override_threshold_lock`, `override_reason`, `override_authorized_by`, `override_authorized_at`; and the results-specific keys `result` (with nested `actual`, `status`, `decided`, `decided_by`). Inherits the full universal-schema key set from the skeleton on the README.
- **Ontology object types touched:** Experiment (Domain C; the single ontology type instantiated by both `experiment.md` and `results.md`). Assumption (Domain C; referenced via the `parent_assumption:` frontmatter field on `experiment.md` — by id, not instantiated here).
