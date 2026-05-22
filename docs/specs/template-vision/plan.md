# Plan: template-vision

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** approved (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

Single-file template, single commit-sized loop. The strategy is mechanical, not creative: (1) copy the parent-spec-shipped skeleton; (2) pre-fill the template's identity fields per the parent spec's pre-fill rule; (3) replace the skeleton's placeholder required-section headings with the six HANDOVERS Handover 4 headings quoted verbatim; (4) append the Handover-4-specific frontmatter block (with the three nested list-of-maps fields fully placeholdered and the `open_assumptions[*].tier` enum represented as an atomic placeholder `<must-test-before-shipping | accept-as-bet | will-monitor-post-ship>`); (5) VERIFY against `--check-template` and the contract-test pytest; (6) REVIEW with `adversarial-reviewer`; (7) CAPTURE — append to `templates/_meta/README.md`, mark ROADMAP F3.6 shipped.

Load-bearing in the sequence:
- Task 1 must run before any frontmatter or section editing — the file has to exist at the right path with the skeleton shape so the linter and pytest can see it.
- Tasks 3 and 4 can run in parallel after Task 2 (both edit different sections of the same file but no logical overlap).
- VERIFY (Task 5) is the gate between authoring and review; if VERIFY is red, do not dispatch the reviewer (the reviewer's job is spec-vs-artifact drift, not basic linting).
- CAPTURE (Task 7) holds the README.md write and ROADMAP check; these are observably append-only and cross-worker-safe per the parent spec's §"Rollout" reasoning.

## Constraints

- Angle-bracket placeholder syntax exclusively (parent spec test T16 inherited; per spec §"Boundaries → Always do").
- Nested-container-placeholder rule applies recursively to `predicted_outcomes:`, `open_assumptions:`, `counter_metrics:`, and every other list-of-maps the template carries (per parent spec §"Outputs" item 4; the kit's `--check-template` mode enforces this).
- Body ≤ 80 lines (skeleton parity).
- Do not introduce new top-level dependencies; the linter and pytest already ship.
- Do not edit `tools/lint-frontmatter.py` or `scripts/tests/test_templates_instantiate.py`. Those are parent-spec-owned; this template consumes them.
- `templates/_meta/README.md` is shared across the ten F3.x workers — keep edits append-only and trivially merge-friendly (a single one-line list entry).
- ROADMAP edit must touch only the F3.6 row (one checkbox + a `Shipped: <date>` annotation).

## Construction tests

Cross-cutting only. Per-task tests are inline under each task.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 after Task 5 and again at the end of CAPTURE.

## Tasks

### Task 1: copy skeleton to `templates/vision.md`

- **Depends on:** none
- **Tests:**
  - `T1` from spec — file exists at `templates/vision.md` (a simple `test -f`).
  - Skeleton parity — the copied file's body matches `templates/_meta/template-skeleton.md` byte-for-byte at copy time (informational; will diverge as Tasks 2–4 edit it).
- **Approach:**
  - `cp templates/_meta/template-skeleton.md templates/vision.md` (atomic single-file copy; no `os.replace` ritual needed for a `cp`).
  - Confirm the destination did not already exist (the spec's "the component does not yet exist" precondition).
- **Done when:** `templates/vision.md` exists; its content is the unmodified skeleton.

### Task 2: pre-fill template identity (`object_type: Vision`, `status: Draft`, H1 `# Vision`)

- **Depends on:** Task 1
- **Tests:**
  - Identity check — `yaml.safe_load` on the frontmatter resolves `object_type` to the literal string `"Vision"` and `status` to the literal string `"Draft"`.
  - H1 — `grep -E "^# Vision\b" templates/vision.md` returns one line.
- **Approach:**
  - Replace the skeleton's `object_type: <pre-filled per template — e.g., Strategic Intent>` line with `object_type: Vision`.
  - Leave `status: Draft` as-is (the skeleton already pre-fills this — confirm, don't edit).
  - Replace the skeleton's H1 `# <Artifact name>` with `# Vision`.
- **Done when:** identity check and H1 grep pass.

### Task 3: replace required-section headings with HANDOVERS Handover 4 sections verbatim

- **Depends on:** Task 2 (skeleton must be in place with its placeholder section headings)
- **Tests:**
  - `T4` from spec — the six required-section headings appear in order: `## The customer-shaped pitch`, `## The change`, `## What we believe and why`, `## What we're still betting on`, `## Counter-metrics`, `## Predicted outcomes`.
  - Section-body shape — each of the six sections has a single `<one-paragraph placeholder>` line beneath it (no seeded prose).
- **Approach:**
  - Locate the skeleton's three placeholder section headings (`## <Required section 1 from HANDOVERS.md>`, `## <Required section 2 from HANDOVERS.md>`, `## <Required section N from HANDOVERS.md>`) and the body placeholders beneath each.
  - Replace with the six Handover 4 headings, in HANDOVERS.md order, each followed by a one-line angle-bracket placeholder body (e.g., `<one-paragraph customer-shaped pitch>`).
  - Leave the `## Optional sections` heading and its "Delete the heading and all unused sections below if none apply" line intact (HANDOVERS Handover 4 names no optional sections; the heading remains per the parent spec's convention).
  - Confirm the body line count is ≤ 80 after the edit.
- **Done when:** T4 passes; body line count ≤ 80.

### Task 4: dedup overlapping fields into universal-schema position; append Handover-4-only fields under the `# Handover-specific fields` comment

- **Depends on:** Task 2 (the identity fields anchor the placement)
- **Tests:**
  - `T3` from spec — required Handover 4 frontmatter keys present including nested keys, with the documented pre-filled values.
  - `T2` from spec — `python3 tools/lint-frontmatter.py --check-template templates/vision.md` exits 0.
  - Tier-enum placeholder — `grep -F "<must-test-before-shipping | accept-as-bet | will-monitor-post-ship>" templates/vision.md` returns one line.
  - Pre-author regex check — `python3 -c "import re; r=re.compile(r'^<\S(?:[^>]*\S)?>$'); s='<must-test-before-shipping | accept-as-bet | will-monitor-post-ship>'; print(bool(r.match(s)))"` returns `True`. (Confirms the tier-enum placeholder satisfies the atomic-placeholder regex `ATOMIC_PLACEHOLDER = r"^<\S(?:[^>]*\S)?>$"` before authoring; if this fails, fall back per the Risk in §Risks.)
- **Approach:**
  - **Dedup convention (universal-schema position wins).** For keys appearing in both the skeleton's universal-schema block and Handover-4's handover-specific block (`parent_intent`, `parent_learning`, `human_owned_decisions`, `human_approval_required`, `object_type`, `open_assumptions`), keep the field in its universal-schema position with the HANDOVERS-4-mandated value or shape. Delete the duplicate restatement from the handover-specific block. The handover-specific block carries only fields not present in the universal schema (`crosses_teams`, `predicted_outcomes`, `counter_metrics`). This matches the kit's convention as used by F3.3, F3.5, F3.10.
  - **`open_assumptions` schema override.** The universal-schema flat-list form `open_assumptions: [<text>, ...]` (line 31 of the skeleton) is OVERRIDDEN by Handover-4's list-of-maps form. In the same edit that introduces the Handover-4 block, delete the skeleton's flat-list line and replace it in-place (still in the universal-schema block) with:
    ```yaml
    open_assumptions:
      - assumption: <text>
        tier: <must-test-before-shipping | accept-as-bet | will-monitor-post-ship>
    ```
    The list-of-maps form is the canonical shape on the Vision template.
  - **Universal-schema block edits (in place, in the existing position):**
    - `object_type: Vision` (replaces the skeleton's `<pre-filled per template — e.g., Strategic Intent>` per Task 2 already).
    - `parent_intent: <strategic intent slug>` — keep the skeleton's placeholder (HANDOVERS-4's restatement is dropped from the handover-specific block).
    - `parent_learning: <validation learning slug>` — keep the skeleton's placeholder (HANDOVERS-4's value is identical).
    - `open_assumptions:` — replace the flat-list with the list-of-maps form above (Handover-4 shape).
    - `human_owned_decisions:` — replace the skeleton's `<decision a human must make personally>` list with the three HANDOVERS-4 items verbatim (`Customer-shaped framing of the value proposition`, `Differentiator selection`, `Predicted outcome thresholds`). The linter's `--check-template` mode accepts concrete non-empty strings under untyped list-element fields.
    - `human_approval_required: <true | false>` — already placeholder-shaped in the skeleton; HANDOVERS-4 prints `true` literally but the template stays placeholder-shaped per spec §"Boundaries → Always do" (the kit's `--check-template` rule requires a placeholder wrapper for any non-identity value).
  - **Handover-specific block (between the universal-schema block and the closing `---`):** Replace the skeleton's example comment lines (`# Example for Strategic Intent: ...`) with ONLY the non-universal Handover-4 fields:
    - `crosses_teams: <true | false>` (wrap the unwrapped HANDOVERS form per spec §"Boundaries → Always do" and Open Question 2).
    - `predicted_outcomes:` block — one list element with three nested keys:
      ```yaml
      predicted_outcomes:
        - kpi_id: <KPI-NNN>
          threshold: <value>
          measure_at: <weeks-after-launch>
      ```
      Every leaf scalar is an atomic placeholder; the nested-container-placeholder rule passes recursively.
    - `counter_metrics:` block — one list element with one nested key:
      ```yaml
      counter_metrics:
        - kpi_id: <KPI-NNN>
      ```
  - After the edit, `yaml.safe_load` on the frontmatter parses without "found duplicate key" errors (PyYAML's default `safe_load` is lenient on duplicates — last wins — but the linter rejects duplicates explicitly; T2 will catch any residual duplication).
- **Done when:** T2 and T3 pass; the tier-enum grep finds the literal placeholder string; the pre-author regex check returned `True`.

### Task 5: VERIFY

- **Depends on:** Task 3 and Task 4 (both required for the file to be in its final shape)
- **Tests:**
  - All spec contract tests T1–T7 pass.
  - `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Run T1 through T7 in order; fix any red. T8 and T9 are CAPTURE-phase tests (deferred to Task 7) because they depend on edits to shared files.
  - If `--check-template` fails on `predicted_outcomes` or `open_assumptions` nested structures, re-inspect the placeholder shape — most common cause is a leaf scalar that ended up as a bare concrete value (e.g., `kpi_id: KPI-NNN` instead of `kpi_id: <KPI-NNN>`).
  - If pytest fails the auto-discovery, confirm `templates/vision.md` is at the correct path (the test's glob is `templates/*.md`).
- **Done when:** all of T1–T7 pass; `pre-pr.sh` exits 0.

### Task 6: REVIEW — dispatch `adversarial-reviewer`

- **Depends on:** Task 5 (no point reviewing a file that fails its own tests)
- **Tests:**
  - Reviewer returns findings (a list, possibly empty) categorized by severity.
  - Iterate: any finding at Critical or High severity must be addressed (either fix the artifact, or revise the spec and re-run the loop). Iteration cap: 5 per the kit's standard work-loop.
- **Approach:**
  - Dispatch `adversarial-reviewer` with the prompt: "Review templates/vision.md against docs/HANDOVERS.md §'Handover 4: Vision → Initiative' and docs/specs/template-vision/spec.md. Look for: missing required frontmatter keys (top-level and nested under `predicted_outcomes`, `open_assumptions`, `counter_metrics`); missing required section headings or wrong order; pre-fill rule violations; angle-bracket discipline; nested-container-placeholder rule application; tier-enum preservation; HANDOVERS-vs-template drift; uncovered acceptance criteria."
  - Apply findings; re-run Task 5 if any artifact change.
- **Done when:** reviewer returns clean (no Critical or High findings), and Task 5 still passes.

### Task 7: CAPTURE — README.md index + ROADMAP F3.6 check

- **Depends on:** Task 6
- **Tests:**
  - `T8` from spec — `grep -E "^\- \[x\] \*\*F3\.6\*\*" ROADMAP.md` returns one line.
  - `T9` from spec — `grep -E "\bvision\.md\b" templates/_meta/README.md` returns ≥1 line.
  - `pre-pr-clean` after CAPTURE — `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Append one bullet to the `templates/_meta/README.md` index listing `vision.md` (link target: `../vision.md`) with a one-clause description (e.g., "Vision template — the Validation → Vision handover artifact's shape; see `docs/specs/template-vision/`.").
  - Mark ROADMAP F3.6 row: `- [ ] **F3.6** Vision template ...` → `- [x] **F3.6** Vision template ... Shipped: <YYYY-MM-DD>`.
  - Update this plan's status from `Drafting` to `Done`.
  - Update spec's status from `Draft` to `Shipped (<YYYY-MM-DD>)` (kit-build-component lifecycle track).
  - Run `pre-pr.sh` once more.
- **Done when:** T8, T9 pass; `pre-pr.sh` exits 0.

## Rollout

- ROADMAP P4.1 `/draft-vision` becomes unblocked. Its own spec will reference `templates/vision.md` in `Constrained by:` and consume it as the literal shape its drafter populates.
- ROADMAP F3.7 `template-initiative` (sibling F3 worker) gains a concrete target for its `parent_vision:` traceability field — F3.7's instantiated Initiative artifacts will reference `delivery/visions/<slug>.md` files shaped by this template.
- `templates/_meta/README.md` gains a new index row (per Task 7); the parent spec's §"Rollout" anticipated this and gave it sequential-or-trivially-mergeable semantics.
- No `INVENTORY.md` row needed (the parent spec already declined to row-list templates as infrastructure).
- No `AGENTS.md` edit needed (the source-of-truth table already points at `docs/CONVENTIONS.md` for "Required metadata for any artifact?"; this template is downstream of that pointer).
- No new command, audit, or hook ships in this loop; the template is purely a copy source.

## Risks

- **Tier-enum placeholder shape rejection by `--check-template`.** The literal placeholder string `<must-test-before-shipping | accept-as-bet | will-monitor-post-ship>` has internal whitespace and pipe characters but no internal angle brackets, so it should match `ATOMIC_PLACEHOLDER = r"^<\S(?:[^>]*\S)?>$"` (the regex requires ≥1 non-whitespace char and no internal `>`). Mitigation: T2 (the linter exit code) catches any failure; if the regex unexpectedly rejects the form, fall back to encoding `tier:` as the bare augmented-placeholder string `<tier-name>` and naming the three-value enum in a YAML comment above the line. Surface as a finding in REVIEW if it happens.
- **Race on `templates/_meta/README.md`.** Ten F3.x workers each append one line to this shared file. Mitigation per the parent spec's §"Rollout": each worker writes its append in a tiny dedicated commit late in its loop; the F3 stage-2 CAPTURE merge resolves conflicts (append-only, trivially mergeable). This worker's append is a single-line entry; the merge surface is one line.
- **HANDOVERS.md drift after the template ships.** If a future edit to HANDOVERS §"Handover 4" changes the required-frontmatter or required-sections list, this template silently diverges. Mitigation: the parent spec's §"Convention-text contract" puts the source-of-truth burden on HANDOVERS.md and treats the template as a re-projection; a future kit audit (proposed but not in this spec's scope) could cross-check templates against HANDOVERS programmatically. For now, the work-loop's "spec is wrong" path is the mitigation: if a future PM session finds the template out of sync, the right move is to update the template in the same session, not to silently work around it.
- **`crosses_teams: <true | false>` and `human_approval_required: <true | false>` wrapping disagreement.** Spec §"Open questions" #2 resolved this in favor of wrapping; if the adversarial reviewer disagrees and prefers unwrapped (matching HANDOVERS.md byte-for-byte), the fix is either to update the spec's resolution OR to leave them unwrapped and add a one-line YAML comment naming the legal values. Surface in REVIEW.

## Changelog

Append entries when the plan changes substantially during execution. Format: `<YYYY-MM-DD>: <one-line description of the change and why>`.

- 2026-05-22 (review-iter-1): Applied adversarial-reviewer fixes — F1 (flipped dedup direction to keep universal-schema position; reversed plan Task 4 and spec §Boundaries), F2 (open_assumptions schema override), F3 (tier-enum regex pre-check), F4-F8 (T3 clarification, vague-language tightening, T1b body-line-count test, T4b intro blockquote test, T3 completeness-gate scope), cross-cutting dedup convention reversed.
