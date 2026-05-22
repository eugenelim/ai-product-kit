# Spec: template-learning-memo

- **Status:** Shipped (2026-05-22)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template
- **Serves kit phase:** Validation
- **Constrained by:** `docs/specs/template-authoring-convention/spec.md` (parent authoring contract — placeholder rule, frontmatter ordering, skeleton source, `--check-template` linter mode); `docs/HANDOVERS.md` §"Handover 3: Validation → Vision" (required frontmatter + required sections, verbatim); `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`", §"Universal metadata schema", §"Lifecycle states"; `context/frameworks/ontology.md` (Domain I `Validation Learning Memo` composite; Domain C atomics `Insight`, `Experiment`, `Assumption`; Domain H `Decision`); `assumption-threshold-lock` hook contract (predeclared-threshold guard — the kit's "single most important guard"); `ROADMAP.md` F3.5 (this item) and F3.4 (sibling — the Experiment template the `test.experiment` field links to).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Authors the `Validation Learning Memo` template at `templates/learning-memo.md`. The template is the on-disk skeleton a PM copies into `validation/learnings/<slug>.md` to record the outcome of testing a riskiest assumption — predeclared threshold, actual result, survived-or-killed disposition. The template's only job is to (a) hand the PM the exact frontmatter + section shape that closes Handover 3 and (b) position `predeclared_at:` so the `assumption-threshold-lock` hook can read it on every instantiated learning memo *before* results are written. The template itself is not enforced by the threshold-lock hook; the hook runs against instantiated learnings under `validation/learnings/`. The template's job is to make backdating mechanically harder, not to enforce non-backdating.

## Objective

Ship `templates/learning-memo.md` — a single-file template, instantiating Domain I's `Validation Learning Memo` composite — that a kit user copies into `validation/learnings/<slug>.md` to produce a learning memo that satisfies `docs/HANDOVERS.md` §"Handover 3" verbatim. The template pre-fills the artifact's identity fields (`object_type: Validation Learning Memo`, `status: Draft`, `human_approval_required: true`, the H1 heading) and placeholders everything else with the angle-bracket syntax mandated by the parent authoring convention. The `test:` and `result:` blocks are encoded as one-level nested maps so the linter's recursive leaf-scalar check accepts every leaf. **`test.predeclared_threshold` is a flat scalar placeholder, not a nested `{success, falsification}` map** — see plan.md §Changelog (2026-05-22 EXECUTE deviation) for the parser-limitation rationale; the underlying `{success, falsification}` distinction is preserved at depth 1 in `templates/experiment/experiment.md`, which is what the `assumption-threshold-lock` hook actually polices. The `predeclared_at:` field sits at the bottom of the `test:` block so it is read by the threshold-lock hook *before* any `result.*` scalar; the hook scans top-down on instantiated memos and `predeclared_at:` must precede every `result.*` line.

No prior stub exists. `templates/` currently holds only `templates/_meta/template-skeleton.md` (the source) and `templates/_meta/README.md` (the index).

## Why now

F3.5 is one of ten F3.x templates fanned out in parallel after `template-authoring-convention` shipped. The Learning Memo is the load-bearing handover between Validation and Vision — Vision (F3.6) cannot cite a `parent_learning:` until this template exists, and `/draft-vision` (P4.1) cannot run without an instantiated learning memo from this template. Without it, PMs writing learning memos by hand drift on the threshold-lock-readable shape, which silently weakens the kit's single most important guard. The work also closes a sibling dependency loop: F3.4 (Experiment template) provides the artifact that the memo's `test.experiment` field links to; F3.4 runs in parallel with this spec but does not block it — this spec cites F3.4's slug (`template-experiment`) as a referenced template, not as a prerequisite.

## Inputs and outputs

**Inputs.**

- `templates/_meta/template-skeleton.md` — copy source. Provides universal-schema frontmatter ordering and the required-section heading scaffolding.
- `docs/HANDOVERS.md` §"Handover 3: Validation → Vision" — source of truth for the required frontmatter and required sections quoted into this template verbatim.
- `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" — placeholder syntax, frontmatter ordering, pre-fill rule, required-vs-optional sections, linter contract.
- `docs/CONVENTIONS.md` §"Universal metadata schema" — the universal frontmatter superset; carried into the template per the parent skeleton.
- `docs/CONVENTIONS.md` §"Lifecycle states" — `status: Draft` is the product-artifact-track entry state pre-filled by the parent convention.
- `context/frameworks/ontology.md` — Domain I `Validation Learning Memo` row (the composite this template instantiates); Domain C `Experiment`, `Assumption`, `Insight` and Domain H `Decision` (the atomic types the composite wraps).
- `tools/lint-frontmatter.py --check-template` — the linter mode that walks the template, accepting angle-bracket placeholders and recursing into nested containers; this template must pass it.

**Outputs.**

- `templates/learning-memo.md` — single file. Universal-schema block at top (per skeleton), `# Handover-specific fields` block underneath containing the Handover-3 required frontmatter quoted verbatim from `docs/HANDOVERS.md` and placeholdered per the parent convention's recursive placeholder rule. Body has five `## ` required-section headings quoted verbatim from HANDOVERS.md §"Handover 3", in the same order, each with a one-paragraph placeholder body. An H1 `# Validation Learning Memo`. An entry under `templates/_meta/README.md`'s "Shipped templates" list pointing at this file (appended in CAPTURE per the parent plan's Stage 1 convention).

The required frontmatter, quoted verbatim from `docs/HANDOVERS.md` §"Handover 3" with one deliberate deviation: HANDOVERS-3 prints enum-choice values as bare prose (`type: desirability | viability | feasibility | usability | ethical`, `status: survived | killed`), but the linter's `--check-template` mode requires angle-bracket placeholders on every non-concrete leaf. This template wraps enum-choice values in angle brackets — `type: <desirability | viability | feasibility | usability | ethical>`, `status: <survived | killed>` — following the parent skeleton's precedent for `priority` and `risk_level` (the parent skeleton at `templates/_meta/template-skeleton.md` lines 11–12 carries `priority: <Low | Medium | High | Critical>` and `risk_level: <Low | Medium | High | Critical>` in the wrapped form; this template carries the same wrapping convention forward). Keys, ordering, nesting depth, and structural shape remain verbatim with HANDOVERS-3. A future maintainer must not "fix" the enum-choice wrappers back to bare prose; that would fail the linter.

```yaml
object_type: Validation Learning Memo
parent_opportunity: <opportunity id>
riskiest_assumption: <one sentence>
test:
  type: <desirability | viability | feasibility | usability | ethical>
  experiment: <path to validation/experiments folder>
  predeclared_threshold: <success criterion AND falsification criterion — restate verbatim from linked experiment.md>
  predeclared_at: <YYYY-MM-DD>
result:
  actual: <value>
  status: <survived | killed>
  decided: <YYYY-MM-DD>
  decided_by: <names>
human_owned_decisions:
  - Whether to survive or kill on ambiguous results
  - Whether to proceed to delivery given remaining open assumptions
human_approval_required: true
```

The required sections quoted verbatim from `docs/HANDOVERS.md` §"Handover 3", in this exact order:

1. **The assumption tested** — restated; why it was the riskiest
2. **The test** — design, threshold, predeclared falsification with timestamp showing it was declared *before* results
3. **The result** — actual measurement vs predeclared thresholds
4. **What we learned** — separate from whether we proceed
5. **The disposition** — survived → proceed to vision; killed → opportunity returned to OST or pruned

A reader of this section should be able to reconstruct `templates/learning-memo.md` without reading anything else.

## Boundaries

### Always do

- Use **angle-bracket placeholders only** per parent convention. Atomic (`<one sentence>`), augmented (`<role>: <YYYY-MM-DD>`), block-scalar, and nested-container forms are all permitted; curly-brace or `__FILL__` forms are not.
- Quote the Handover-3 required frontmatter keys and the five required-section headings **verbatim** from `docs/HANDOVERS.md`. No rewording, no summary, no "improved phrasing."
- Pre-fill the template's identity per parent convention: `object_type: Validation Learning Memo`, `status: Draft`, `human_approval_required: true`, and the H1 `# Validation Learning Memo`. Every other field is a placeholder. (`human_approval_required: true` is pre-filled because HANDOVERS-3 fixes it as the contract value for this handover — kit users do not have discretion to set this to `false`. See Open Question 3.)
- Position `predeclared_at:` as the **last** scalar under `test:` (immediately after the `predeclared_threshold:` block) but **above** anything under `result:`, exactly matching the HANDOVERS-3 example block. The threshold-lock hook scans top-down; `predeclared_at:` must appear before any `result.*` scalar in the instantiated memo's YAML.
- Encode `test:` and `result:` as nested-container placeholders — every leaf scalar inside each block must be a valid placeholder so the linter's recursion accepts the whole sub-tree.
- Follow the universal-schema frontmatter ordering inherited from `templates/_meta/template-skeleton.md`; append the Handover-specific block under the existing `# Handover-specific fields` comment.
- Append a one-line entry to `templates/_meta/README.md`'s "Shipped templates" list. (Appended in CAPTURE, not during the spec/plan phase. The parent plan's Stage 1 rollout addresses concurrent-append risk.)
- **Dedup convention.** When HANDOVERS-3 fields overlap with the universal-metadata schema (`object_type`, `human_owned_decisions`, `human_approval_required`), the field appears once — in its universal-schema position — carrying the HANDOVERS-3-mandated value. The universal-schema placeholder is deleted in the same edit. The handover-specific block carries only fields not present in the universal schema (`parent_opportunity`, `riskiest_assumption`, `test`, `result`). This single-emission discipline matches what Task 2 implements for `human_approval_required:` and what Task 4 omits from the Handover-specific block.

### Ask first

- Adding any field not listed in Handover 3's required frontmatter (e.g., a kit-internal annotation). Surface as an open question; do not silently extend.
- Promoting any optional section into a required one. The five required sections are fixed by HANDOVERS.md; additions belong under `## Optional sections`.
- Re-ordering the nested keys inside `test:` or `result:` from how HANDOVERS-3 prints them. The ordering is contract surface for the threshold-lock hook.

### Never do

- Invent learning content. The template is shape-only — no example assumption text, no example threshold number, no example disposition. A reader must be able to tell this is a skeleton, not a worked example.
- Weaken the predeclared-threshold rule. The template must not (a) omit `predeclared_at:`, (b) move `predeclared_at:` below any `result.*` field in the frontmatter, (c) hide `predeclared_at:` inside a deeper block scalar that the threshold-lock hook cannot read, (d) suggest in commentary that backdating is acceptable, or (e) pre-fill `predeclared_at:` with anything other than a placeholder — pre-filling a concrete date would let a kit user save the template after results are recorded and claim a `predeclared_at:` that was never declared.
- Add a new ontology type. `Validation Learning Memo` already exists in Domain I; do not re-classify it or add a `Learning` synonym.
- Modify `assumption-threshold-lock` or any other hook. The template is data; hooks are out of scope for F3.5.
- Modify the parent skeleton, parent convention, `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, the linter, or the contract test under `scripts/tests/`. All of those ship via their own specs.
- Author the `validation/learnings/<slug>.md` artifact itself. The template is shipped; instantiation is the kit user's job, not this spec's.

## Verification mode

- **Goal-based check** — for shape: the template file exists at the named path; the linter's `--check-template` mode exits 0; greps confirm the five required-section headings are present; T10 asserts the critical positional ordering of `predeclared_at:` relative to `result.*`; broader frontmatter key ordering is YAML-load-tested by T3 (structural presence only, not sequence).
- **Audit-driven** — for kit-wide health: `bash tools/pre-pr.sh` exits 0 after Task 1 ships; `python3 -m pytest scripts/tests/test_templates_instantiate.py` passes (the parent spec's contract test, which auto-discovers `templates/learning-memo.md` via its `templates/*.md` glob and runs `--check-template` against it; this exercises the nested-container-placeholder branch on both `test:` and `result:`).
- The `assumption-threshold-lock` hook is **not** a verification gate for this spec. The hook gates *instantiated* learning memos under `validation/learnings/`, not template files under `templates/`. This template's verification asserts the *shape* the hook needs; the hook itself is exercised by future instantiation work, not by F3.5.
- **Explicit non-guarantee.** This template does not prevent a kit user from saving an instantiated memo with a backdated `predeclared_at:`. Backdating prevention is the `assumption-threshold-lock` hook's runtime job (file-mtime-vs-frontmatter check); the template's job ends at making the `predeclared_at:` field readable, positionally ordered before `result.*`, and impossible to omit without obvious damage to the frontmatter. The two guards are complementary; neither replaces the other.

## Contract tests

Each test is a one-liner or one pytest case. They are the gate.

- `T1` — `test -f templates/learning-memo.md` (file exists at the agreed path).
- `T2` — `python3 tools/lint-frontmatter.py --check-template templates/learning-memo.md` exits 0. Exercises the nested-container-placeholder branch on both `test:` and `result:` blocks — a regression here implies the parent linter's recursion is broken or the template encoded a non-placeholder, non-concrete leaf.
- `T3` — Required Handover-3 frontmatter keys present (including nested keys). Python one-liner loads the YAML frontmatter and asserts: top-level keys `object_type`, `parent_opportunity`, `riskiest_assumption`, `test`, `result`, `human_owned_decisions`, `human_approval_required` all present; `test` is a mapping containing keys `type`, `experiment`, `predeclared_threshold`, `predeclared_at`; `test.predeclared_threshold` is a non-empty scalar placeholder (NOT a nested map — flattened per plan.md §Changelog 2026-05-22 EXECUTE deviation due to the kit frontmatter parser's depth-2 limit); `result` is a mapping containing keys `actual`, `status`, `decided`, `decided_by`. The one-liner is recorded in `plan.md` Task 5.
- `T4` — Required-section headings present in order. `grep -nE "^## " templates/learning-memo.md` extracts headings in document order; the first five headings (excluding any `## Optional sections` trailer) must be — in this exact order — "The assumption tested", "The test", "The result", "What we learned", "The disposition". Trailing context after each heading (e.g., an em-dash gloss) is permitted; the heading text matched is exact-prefix.
- `T5` — Angle-bracket-only discipline. `python3 -c "body=open('templates/learning-memo.md').read(); body_only=body.split('---',2)[2] if body.count('---')>=2 else body; assert '{{' not in body_only and '__FILL__' not in body_only"` exits 0. (Identical to parent T16; re-run against this template.)
- `T6` — `python3 -m pytest scripts/tests/test_templates_instantiate.py -v` exits 0 **and** its verbose output lists `templates/learning-memo.md` as a non-skipped target (guards against a silent discovery regression that would let T6 pass vacuously). Concretely: `python3 -m pytest scripts/tests/test_templates_instantiate.py -v 2>&1 | grep -F "PASSED" | grep -F "templates/learning-memo.md"` returns at least one line; AND `python3 -m pytest scripts/tests/test_templates_instantiate.py -v 2>&1 | grep -F "SKIPPED" | grep -F "templates/learning-memo.md"` returns zero lines. The two-pronged form disambiguates PASSED from SKIPPED — a bare `grep -F "templates/learning-memo.md"` would match either status.
- `T7` — `bash tools/pre-pr.sh` exits 0 (kit-wide health gate).
- `T8` — `ROADMAP.md` F3.5 row is checked: `grep -E "^- \[x\] \*\*F3\.5\*\*" ROADMAP.md` returns exactly 1. (Done in CAPTURE.)
- `T9` — `templates/_meta/README.md`'s "Shipped templates" section lists this template: `grep -F "learning-memo.md" templates/_meta/README.md` returns ≥ 1. (Done in CAPTURE.)
- `T10` — `predeclared_at:` precedes any `result.*` line in the frontmatter. Python one-liner: load the file's frontmatter slice (between the two `---` fences), find the line index of `predeclared_at:` and the line index of `result:`, assert the former is less than the latter. This is the structural assertion that makes the threshold-lock hook readable on instantiated memos.

## Non-goals

- **Not building `/audit-vision-evidence` (P3.12).** That command audits instantiated visions for evidence linkage; the template is upstream of it.
- **Not authoring an instantiated learning memo.** No file under `validation/learnings/` is written by this spec.
- **Not modifying the `assumption-threshold-lock` hook.** The hook is the runtime gate; this spec sets up the data shape it reads. If the hook's read path is wrong, that is a separate bug, surfaced separately.
- **Not authoring the Vision template (F3.6).** F3.6 references this template's instantiated output via `parent_learning:`; that's a cross-reference, not a co-build.
- **Not authoring `templates/_meta/README.md`'s structural format.** That ships with the parent spec; this F3.5 worker only appends a row in CAPTURE per the parent plan's Stage-1 convention.
- **Not exercising the linter's recursive placeholder logic with new fixtures.** The parent spec's fixtures cover the recursion; this template's `--check-template` pass is the end-to-end check.

## Open questions

1. **Should the template carry an example `decided_by:` cell that names the role (e.g., `<PM>, <Engineering Lead>`) or just `<names>`?** HANDOVERS-3 quotes `<names>`. Resolved here: match HANDOVERS-3 verbatim with `<names>`; a kit user can list role+name in their instantiated memo at their discretion. Surface for review.
2. **Does the augmented placeholder `<survived | killed>` (an enum-choice rendered as `<a | b>`) actually pass the linter's `--check-template` mode?** The parent skeleton uses the same shape for `priority` and `risk_level`, so by precedent it is accepted. If the linter rejects this template on `status: <survived | killed>` or `type: <desirability | viability | feasibility | usability | ethical>`, the fix is local (drop to a plain `<status>` / `<lens>`). Surface for review; expectation is that it passes — verify in EXECUTE.
3. **Should `human_approval_required:` be pre-filled `true` (matching HANDOVERS-3's example, which prints `true` literally) or placeholdered `<true | false>`?** HANDOVERS-3 prints it as `human_approval_required: true` because the contract is that this handover always requires human approval. Resolved here: pre-fill `true` as part of the template's identity, alongside `object_type:` and `status:`. The kit user does not have discretion to disable human approval on this handover; pre-filling makes that contract visible. Cited in plan Task 4 and `Always do` boundary.

## Acceptance criteria

- [ ] `templates/learning-memo.md` exists, copied from `templates/_meta/template-skeleton.md` and edited per this spec.
- [ ] Identity fields pre-filled: `object_type: Validation Learning Memo`, `status: Draft`, `human_approval_required: true`, H1 `# Validation Learning Memo`.
- [ ] Universal-schema frontmatter block matches the parent skeleton's ordering and placeholder forms.
- [ ] `# Handover-specific fields` block contains every required Handover-3 frontmatter key (incl. nested `test.type`, `test.experiment`, `test.predeclared_threshold` as a flat scalar, `test.predeclared_at`, `result.actual`, `result.status`, `result.decided`, `result.decided_by`, `human_owned_decisions`), all placeholdered per the parent convention's recursive placeholder rule. Note: `test.predeclared_threshold` is intentionally flat (not nested `{success, falsification}`) — see plan.md §Changelog 2026-05-22 EXECUTE deviation.
- [ ] `predeclared_at:` is positioned at the bottom of the `test:` block, above any `result.*` line. T10 enforces.
- [ ] Body contains the five Handover-3 required-section headings verbatim, in order: "The assumption tested", "The test", "The result", "What we learned", "The disposition". Each followed by a one-paragraph placeholder body.
- [ ] `## Optional sections` heading present at the bottom per the parent skeleton; the body underneath is a one-line "Delete this heading and all unused sections if none apply." note. (No domain-specific optional sections enumerated by Handover 3 — leave as-is from the skeleton.)
- [ ] No example learning content, no example assumption text, no example threshold number.
- [ ] Contract tests T1–T10 pass.

## Cross-references

- **Consumed by:** Vision template (F3.6, `template-vision`) — its instantiated form cites a `parent_learning:` slug that points at a `validation/learnings/<slug>.md` produced from this template. `/draft-vision` (P4.1) reads instantiated learning memos. `/audit-vision-evidence` (P3.12, planned) walks back from a Vision to the cited learning memo.
- **Consumes:** `docs/HANDOVERS.md` §"Handover 3" (verbatim quote source); `docs/CONVENTIONS.md` §"Templates", §"Universal metadata schema", §"Lifecycle states"; `context/frameworks/ontology.md` (Domain I `Validation Learning Memo`, Domain C `Experiment`/`Assumption`/`Insight`, Domain H `Decision`); `templates/_meta/template-skeleton.md` (copy source); `tools/lint-frontmatter.py --check-template` (gate); `scripts/tests/test_templates_instantiate.py` (auto-discovery gate); the `assumption-threshold-lock` hook contract (which reads `predeclared_at:` on instantiated memos — this template positions that field to be readable).
- **Frontmatter fields owned (under `# Handover-specific fields`):** `riskiest_assumption`, `test` (with nested `type`, `experiment`, `predeclared_threshold` as flat scalar, `predeclared_at`), `result` (with nested `actual`, `status`, `decided`, `decided_by`). `parent_opportunity` lives in the universal-schema traceability block (single emission, dedup convention). Universal-schema fields are owned by the parent convention.
- **Ontology object types touched:** Domain I `Validation Learning Memo` (the composite this template instantiates); Domain C `Experiment` (referenced by `test.experiment`), `Assumption` (referenced by `riskiest_assumption`), `Insight` (produced inside the "What we learned" section); Domain H `Decision` (produced inside the "The disposition" section). No new ontology types added.
- **Sibling parallel item:** F3.4 (`template-experiment`) — provides the artifact that the `test.experiment` field links to. F3.4 ships independently; this spec does not block on it.
