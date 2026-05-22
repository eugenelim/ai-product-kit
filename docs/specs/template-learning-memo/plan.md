# Plan: template-learning-memo

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Approved
- **Plan review:** approved (pre-EXECUTE inline adversarial review, 1 iteration with 5 findings, all addressed; iter-2 clean)

> **Plan contract.** Implementation strategy for the spec. Allowed to change as we learn; changelog at the bottom.

## Approach

Copy `templates/_meta/template-skeleton.md` to `templates/learning-memo.md`, then edit *only* the parts the spec names: pre-fill the identity fields (`object_type`, `status`, `human_approval_required`, the H1), append the Handover-3 frontmatter block under the existing `# Handover-specific fields` comment with nested `test:` and `result:` containers fully placeholdered, replace the four `<Required section N from HANDOVERS.md>` heading rows with the five Handover-3 required headings verbatim (the skeleton's "Section N" row stretches; add the fifth heading and remove the surplus stub row), VERIFY the file shape with the kit's existing tools, REVIEW with `adversarial-reviewer`, then CAPTURE (ROADMAP tick + index append).

The work is one commit's worth of editing. The placeholder discipline is mechanical (parent linter is the gate); the threshold-lock readability is positional (a single Python one-liner checks `predeclared_at:` precedes `result.*`). The two together close every acceptance criterion in the spec.

Sequence-load-bearing: Task 2 (identity pre-fill) must happen before Task 3 (required-section verbatim quote) because the H1 sits above the section headings; both must happen before Task 4 (Handover-3 frontmatter append) because the universal-schema block dictates where the `# Handover-specific fields` comment lives. Tasks 5–7 are VERIFY/REVIEW/CAPTURE in order.

No new dependencies. No new tools. No new fixtures. The parent spec's `--check-template` mode and `test_templates_instantiate.py` are the gates.

## Constraints

- **Angle-bracket placeholders only.** Curly braces and `__FILL__` rejected. T5 enforces.
- **Nested-container placeholder discipline.** Every leaf scalar inside `test:` and `result:` must be a valid placeholder (atomic, augmented, or block-scalar shape). The parent linter recurses into both lists and maps; one bad leaf rejects the whole template (parent T8g + T8h exercise the negative case on fixtures, T2 here exercises the positive case end-to-end on the live template).
- **Preserve threshold-lock readability.** `predeclared_at:` is a plain top-level scalar at the bottom of the `test:` block — not inside a deeper nested mapping, not inside a block scalar, not split across lines. The hook reads it as a YAML scalar; the value is opaque to the template (a placeholder), but the *key* must be findable. T10 asserts the positional ordering relative to `result:`; the linter's parse asserts the YAML well-formedness.
- **Quote HANDOVERS-3 verbatim** for the five required-section headings and the required-frontmatter keys. The template is a re-projection of HANDOVERS-3, not a parallel source of truth (same discipline the parent convention applied to its CONVENTIONS.md re-projection).
- **No commits in this loop.** Caller commits the aggregated F3 fan-out result. This worker stops at `plan_review_status: approved`.
- **`templates/learning-memo.md` must NOT exist at the end of PLAN.** This worker authors spec + plan + state.json only.

## Construction tests

Cross-cutting only. Per-task tests are inline under each task.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 after EXECUTE completes (a single run, since EXECUTE is a single edit pass).

## Tasks

### Task 1: copy `templates/_meta/template-skeleton.md` to `templates/learning-memo.md`

- **Depends on:** none
- **Tests:**
  - `T1` — `test -f templates/learning-memo.md`.
- **Approach:**
  - `cp templates/_meta/template-skeleton.md templates/learning-memo.md`. The skeleton is ≤ 80 body lines and ships the universal-schema block, the `# Handover-specific fields` comment marker, the five required-section heading stubs (currently four labeled "1, 2, N"), the `## Optional sections` trailer, and the H1 placeholder. All edits in subsequent tasks are scoped to this file.
  - The skeleton's `<!-- ... -->` HTML comment block sits AFTER the closing frontmatter `---`, not before — so `body.split('---')[1]` in Task 4's T3 one-liner correctly slices the frontmatter region (index 0 is the empty string before the opening `---`, index 1 is the frontmatter body, index 2 is everything after the closing `---` including the HTML comment).
- **Done when:** T1 passes.

### Task 2: pre-fill identity (`object_type`, `status`, `human_approval_required`, H1)

- **Depends on:** Task 1
- **Tests:**
  - `grep -nE "^object_type: Validation Learning Memo\$" templates/learning-memo.md` returns exactly 1.
  - `grep -nE "^status: Draft" templates/learning-memo.md` returns exactly 1. (Inherited from skeleton; this task asserts it survived the copy and was not edited.)
  - `grep -nE "^human_approval_required: true\$" templates/learning-memo.md` returns exactly 1.
  - `grep -nE "^# Validation Learning Memo\$" templates/learning-memo.md` returns exactly 1.
- **Approach:**
  - Replace `object_type: <pre-filled per template — e.g., Strategic Intent>` with `object_type: Validation Learning Memo`.
  - Leave `status: Draft` as-is (already pre-filled by the skeleton — this is the universal product-artifact-track entry state).
  - The skeleton's `human_approval_required: <true | false>` is in the universal block. Per spec Open Question 3, override to the concrete value `human_approval_required: true` (HANDOVERS-3 fixes this contractually for the handover). This is an exception to the "every non-identity field is a placeholder" rule, justified by the handover-level contract.
  - **Single-emission discipline.** Edit the universal-block `human_approval_required:` line in place — do NOT re-emit `human_approval_required:` in the Handover-specific block below. Two emissions of the same top-level YAML key would make the file ambiguous to `yaml.safe_load` (and, more importantly, an invalid YAML mapping per the spec). Task 4's Handover-3 frontmatter block must omit `human_approval_required:` for the same reason.
  - Replace the skeleton's `# <Artifact name>` H1 with `# Validation Learning Memo`.
- **Done when:** All four greps return 1.

### Task 3: replace required-section headings with HANDOVERS-3 sections verbatim

- **Depends on:** Task 2
- **Tests:**
  - `T4` — required-section headings present in document order: "The assumption tested", "The test", "The result", "What we learned", "The disposition". One-liner: `grep -nE "^## " templates/learning-memo.md | head -5 | awk -F'## ' '{print $2}'` lists those five strings in that order (any em-dash gloss after each heading is permitted; matching is exact-prefix).
- **Approach:**
  - The skeleton ships three "Required section N from HANDOVERS.md" stub headings. Replace them in document order with the first three Handover-3 headings: "The assumption tested", "The test", "The result". Insert two new `## ` headings for "What we learned" and "The disposition" before the existing `## Optional sections` trailer.
  - Under each of the five headings, write one placeholder paragraph that names what the section contains. Form: `<One paragraph: …>`. No example content. Cite the Handover-3 gloss inline (e.g., "The assumption tested — restated; why it was the riskiest"). The gloss makes the placeholder self-documenting for the kit user.
  - **Optional-sections trailer cleanup.** The parent skeleton ships with a `## Optional sections` heading followed by "Delete the heading and all unused sections below if none apply." and a `### <Optional section A>` stub. Handover 3 enumerates no optional sections, so remove the `### <Optional section A>` stub and its placeholder body, leaving only the `## Optional sections` heading and the "Delete..." line. This matches the spec's acceptance criterion "the body underneath is a one-line ... note." Without this trim, a kit user copying the template inherits a phantom optional-section stub that has no Handover-3 mandate.
- **Done when:** T4 passes.

### Task 4: append Handover-3 frontmatter under `# Handover-specific fields` with nested `test:` and `result:` blocks

- **Depends on:** Task 2 (the comment marker `# Handover-specific fields` sits inside the universal-schema YAML block established in Task 2)
- **Tests:**
  - `T3` — Python one-liner asserting every Handover-3 frontmatter key is present (incl. nested keys). Concretely:

    ```bash
    python3 -c "
    import yaml, pathlib
    body = pathlib.Path('templates/learning-memo.md').read_text()
    fm = yaml.safe_load(body.split('---')[1])
    assert {'object_type','parent_opportunity','riskiest_assumption','test','result','human_owned_decisions','human_approval_required'} <= set(fm), set(fm)
    assert isinstance(fm['test'], dict) and {'type','experiment','predeclared_threshold','predeclared_at'} <= set(fm['test']), fm['test']
    assert isinstance(fm['test']['predeclared_threshold'], dict) and {'success','falsification'} <= set(fm['test']['predeclared_threshold'])
    assert isinstance(fm['result'], dict) and {'actual','status','decided','decided_by'} <= set(fm['result'])
    "
    ```

  - `T10` — `predeclared_at:` line index is strictly less than `result:` line index. Python one-liner:

    ```bash
    python3 -c "
    lines = open('templates/learning-memo.md').read().split('---')[1].splitlines()
    pi = [i for i,l in enumerate(lines) if l.lstrip().startswith('predeclared_at:')][0]
    ri = [i for i,l in enumerate(lines) if l.startswith('result:')][0]
    assert pi < ri, (pi, ri)
    "
    ```

  - `T2` — `python3 tools/lint-frontmatter.py --check-template templates/learning-memo.md` exits 0. This is the gate that catches a missed nested-leaf placeholder; if any leaf under `test:` or `result:` is non-placeholder + non-concrete-valid, T2 fails.
- **Approach:**
  - Append the Handover-3 block under the existing `# Handover-specific fields` comment marker inside the YAML frontmatter (i.e., before the closing `---`). The block matches spec §"Inputs and outputs" verbatim, with these placeholder shapes:
    - `parent_opportunity: <opportunity id>` — atomic.
    - `riskiest_assumption: <one sentence>` — atomic.
    - `test:` — nested-container; leaves: `type: <desirability | viability | feasibility | usability | ethical>` (augmented), `experiment: <link to validation/experiments/<id>/>` (augmented), `predeclared_threshold:` nested mapping with `success: <quantitative criterion>` and `falsification: <quantitative criterion>` (both atomic), `predeclared_at: <YYYY-MM-DD>` (atomic, last scalar in the block).
    - `result:` — nested-container; leaves: `actual: <value>`, `status: <survived | killed>`, `decided: <YYYY-MM-DD>`, `decided_by: <names>` (all atomic/augmented).
    - `human_owned_decisions:` — list of two literal HANDOVERS-3 strings (verbatim, no placeholder): "Whether to survive or kill on ambiguous results" and "Whether to proceed to delivery given remaining open assumptions". These are concrete contract text from HANDOVERS-3, not user-supplied content. The parent linter's `--check-template` mode treats non-empty concrete strings in untyped list-element fields as valid (per parent spec's "Concrete-value validation under `--check-template`" rule).
    - `human_approval_required: true` — concrete (already set in Task 2 by overriding the skeleton's universal-block value; this task does not re-emit it).
  - Order the nested `test:` keys exactly as HANDOVERS-3 prints them: `type`, `experiment`, `predeclared_threshold`, `predeclared_at`. The `predeclared_at` placement at the bottom of `test:` is load-bearing for T10 and for the threshold-lock hook's read order on instantiated memos.
  - Order the nested `result:` keys exactly as HANDOVERS-3 prints them: `actual`, `status`, `decided`, `decided_by`.
  - Do **not** add a `predeclared_at:` to `result:`. The single field at the bottom of `test:` is the only one.
- **Done when:** T2, T3, T10 all pass.

### Task 5: VERIFY

- **Depends on:** Task 3, Task 4
- **Tests:**
  - `T2`, `T3`, `T4`, `T5`, `T6`, `T10` from spec — re-run the full set, not just the new ones, to confirm no regression from the heading edits in Task 3 vs the frontmatter edits in Task 4.
  - `T7` — `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Run, in order: `T1`, `T5`, `T2`, `T4`, `T3`, `T10`, `T6`, `T7`.
  - If any test fails, re-enter EXECUTE for the offending task, then re-run VERIFY from the top (do not partial-skip).
- **Done when:** every test listed above exits 0 / returns the expected value.

### Task 6: REVIEW (`adversarial-reviewer`)

- **Depends on:** Task 5
- **Tests:**
  - Reviewer returns "clean" (no `block` or `needs-fix` findings unresolved).
- **Approach:**
  - Dispatch `adversarial-reviewer` against `templates/learning-memo.md` plus this spec + plan. Prompt: "Review templates/learning-memo.md against docs/specs/template-learning-memo/spec.md and docs/HANDOVERS.md §'Handover 3: Validation → Vision'. Confirm: every required Handover-3 frontmatter key is present (incl. nested `test.*` and `result.*`); the five required-section headings are verbatim and in order; `predeclared_at:` is the last scalar under `test:` and precedes every `result.*` scalar; no example learning content present; angle-bracket-only placeholder discipline; nested-container placeholder discipline (every leaf inside `test:` and `result:`); identity pre-fill correct (`object_type: Validation Learning Memo`, `status: Draft`, `human_approval_required: true`, H1 verbatim); the template does not leave room for a kit user to record a backdated `predeclared_at:`. Return findings numbered with severity (block / needs-fix / defer)."
  - Triage findings per work-loop §4.2. Block + needs-fix issues route back to the right earlier task; defer issues are recorded in the spec's Open Questions or as a follow-up note under `notes/`.
- **Done when:** reviewer returns clean, or all surfaced findings are addressed and the next iteration returns clean. Hard cap 5; expectation ≤ 2.

### Task 7: CAPTURE

- **Depends on:** Task 6
- **Tests:**
  - `T8` — `grep -E "^- \[x\] \*\*F3\.5\*\*" ROADMAP.md` returns exactly 1.
  - `T9` — `grep -F "learning-memo.md" templates/_meta/README.md` returns ≥ 1.
- **Approach:**
  - Tick the F3.5 row in `ROADMAP.md`: `- [ ] **F3.5** Learning Memo template. **Slug:** \`template-learning-memo\`.` → `- [x] **F3.5** Learning Memo template. **Slug:** \`template-learning-memo\`. **Shipped:** <YYYY-MM-DD>.`
  - Append one bullet under `templates/_meta/README.md`'s "Shipped templates" section: `- [\`learning-memo.md\`](../learning-memo.md) — Validation Learning Memo. Closes Handover 3 (Validation → Vision). Spec: \`docs/specs/template-learning-memo/\`.` (Concurrent-append risk handled by the parent plan's Stage-1 sequential merge convention; this worker emits the bullet, the aggregator resolves merge order.)
  - Set spec `Status:` to `Shipped (<YYYY-MM-DD>)`. Set plan `Status:` to `Done (<YYYY-MM-DD>)`.
- **Done when:** T8 and T9 pass; spec and plan status fields updated.

## Rollout

- **F3.6 (Vision)** will cite `templates/learning-memo.md` in its `Cross-references → Consumes` block (its instantiated form's `parent_learning:` slug points at a learning memo produced from this template).
- **`/draft-vision` (P4.1, planned)** reads instantiated learning memos; this template guarantees the shape it'll find. No code change needed in P4.1's spec to reference this template — the contract surface is HANDOVERS-3, which P4.1 already cites.
- **`/audit-vision-evidence` (P3.12, planned)** walks Vision → cited learning memo; this template makes the walk well-typed.
- **`templates/_meta/README.md`'s "Shipped templates" list** gains a row in Task 7.
- **`ROADMAP.md` F3.5** gets ticked in Task 7.
- **`INVENTORY.md`** does not get a new row — templates are infrastructure (per parent plan's Rollout section, same posture).
- **`AGENTS.md`** source-of-truth table already routes "What did we learn from each test?" → `validation/learnings/<slug>.md`. The template at `templates/learning-memo.md` is the upstream skeleton, not a routing target; no edit required.

## Risks

- **Nested-container placeholder discipline.** The deepest leaf under `test:` is `test.predeclared_threshold.success` (and its sibling `falsification`) — two levels of nesting. If either leaf is left without a valid placeholder, the parent linter's recursive `_value_acceptable_as_template` rejects the whole template. T2 catches this immediately; mitigation is mechanical (re-emit the leaf as `<quantitative criterion>`).
- **Threshold-lock readability if `predeclared_at:` is buried inside a deeper block-scalar.** The hook reads YAML, but if a future edit moves `predeclared_at:` into, say, a `> ` folded block scalar under a sub-key, the hook's key-lookup fails silently. Mitigation: T10 asserts positional ordering; the spec's "Never do" bullet explicitly bans burying `predeclared_at:` inside a deeper block scalar. Both gates plus reviewer-pass close this risk.
- **HANDOVERS-3 verbatim drift.** If a future edit to `docs/HANDOVERS.md` renumbers or rewords Handover 3 sections, this template's headings drift silently. Mitigation: out of scope for F3.5; HANDOVERS edits are guarded by the parent spec's contract test (T14 family). If HANDOVERS-3 ever changes, this template's T4 fails on the next CI run.
- **`human_approval_required: true` pre-fill is contestable.** A reviewer might argue this should remain a placeholder per the spec's "every non-identity field is a placeholder" doctrine. The spec's Open Question 3 resolves this in favor of pre-fill, citing HANDOVERS-3's literal value. Documented; reviewer can override.
- **`human_owned_decisions:` block as concrete (not placeholder) values.** Same posture as above — HANDOVERS-3 prints the two list items as literal contract text, so this template carries them verbatim. The parent linter's `--check-template` accepts concrete non-empty strings in untyped list-element fields (per parent spec); no exception needed.

## Changelog

- **2026-05-22 (pre-EXECUTE review iter-1):** Five inline-adversarial-review findings applied. Spec: (1) §"Inputs and outputs" gained a one-paragraph note flagging the angle-bracket wrapper around enum-choice values as a deliberate deviation from HANDOVERS-3's bare-prose form, with rationale (linter compatibility). (2) §"Verification mode" gained an explicit non-guarantee disclaimer naming backdating-prevention as the threshold-lock hook's job, not the template's. (3) T6 tightened to require `-v` output listing `templates/learning-memo.md` as a discovered non-skipped target, guarding against silent-discovery regression. Plan: (4) Task 2 Approach made single-emission discipline explicit — universal-block `human_approval_required:` is edited in place, never re-emitted in the Handover-specific block. (5) Task 3 Approach gained an optional-sections-trailer-cleanup bullet — remove the `### <Optional section A>` stub since Handover 3 enumerates no optional sections.
- 2026-05-22 (review-iter-1): Applied adversarial-reviewer fixes — D1 (skeleton-matching angle-bracket enum form in inline YAML), H1 (HTML comment position bullet), V1 (verification-mode rewording), E1 (T6 PASSED/SKIPPED disambiguation), cross-cutting dedup convention bullet added.
