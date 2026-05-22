# Plan: template-strategic-intent

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-22)
- **Plan review:** pending

> **Plan contract.** Implementation strategy for the spec. Allowed to change as we learn; changelog at the bottom.

## Approach

Seven sequential tasks. The arc: copy the parent convention's skeleton to the target path; pre-fill the template's identity (object_type, H1, status); replace the skeleton's generic `## <Required section N from HANDOVERS.md>` headings with the HANDOVERS-quoted headings for Handover 1; append the Handover-1-specific frontmatter fields as a second YAML block under the `# Handover-specific fields` comment that already exists at the bottom of the skeleton's first frontmatter block; verify against the parent convention's linter + pytest gates; harden via adversarial review; capture by appending to the `_meta` README and ticking the ROADMAP row.

Why sequential: every task after Task 1 reads or modifies the artifact produced by Task 1; Tasks 3 and 4 both write to the same file and could in principle run in parallel within a single editor session, but the diff hygiene of doing one then the other is worth the negligible time cost. Task 7 (CAPTURE) is intentionally split into a tiny dedicated commit per the parent plan's §Rollout note about race conditions on `templates/_meta/README.md` when multiple F3.x workers append concurrently — the orchestrator's Stage-2 merge resolves any append-only conflicts.

No new top-level dependencies. Python stdlib + the existing pyyaml import in `tools/lint-frontmatter.py` (called as a subprocess from the pytest harness). No shell tooling beyond what already ships.

## Constraints

- Angle-bracket placeholder syntax exclusively. `{{...}}` and `__FILL__` forbidden anywhere in the template body. T5 in the spec greps these.
- No domain content invented inside the template. Body H2 headings come from HANDOVERS verbatim; body content under each H2 is a one-line `<placeholder>` description, not an example Strategic Intent.
- No edits to `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, `scripts/tests/test_templates_instantiate.py`, or `templates/_meta/template-skeleton.md`. The parent convention's contract is committed; F3.1 is a downstream consumer only.
- The parent skeleton's ≤ 80-body-line discipline is inherited in spirit. Concrete value substitution may push the F3.1 template slightly over; treat ~120 body lines as a soft ceiling. Past that, re-plan — the template has stopped being shape-only.
- The CAPTURE-phase edits to `templates/_meta/README.md` ship as a tiny dedicated commit per the parent plan §Rollout, so the orchestrator's sequential-merge step is trivial.
- No commit during PLAN. The orchestrator owns commits across the eight parallel workers.

## Construction tests

Cross-cutting only. Per-task tests are inline under each task.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 after Task 5 lands; re-verified after Tasks 6 and 7. Run before each commit, not just at the end.

## Tasks

### Task 1: Copy `templates/_meta/template-skeleton.md` to `templates/strategic-intent.md`

- **Depends on:** none
- **Tests:**
  - T1 from spec — `test -f templates/strategic-intent.md` exits 0.
  - Byte-identity sanity (transient — only valid after Task 1, before Tasks 2–4): `cmp templates/_meta/template-skeleton.md templates/strategic-intent.md` exits 0. Asserts the copy is faithful before mutations begin.
- **Approach:**
  - `cp templates/_meta/template-skeleton.md templates/strategic-intent.md`.
  - Do not yet edit the copy; leave it byte-identical so the diff in Tasks 2–4 is reviewable.
- **Done when:** target file exists and is byte-identical to the skeleton.

### Task 2: Pre-fill the template's identity fields

- **Depends on:** Task 1
- **Tests:**
  - T10 from spec — `grep -E '^object_type: Strategic Intent$' templates/strategic-intent.md` returns 1; `grep -E '^status: Draft[[:space:]#]' templates/strategic-intent.md` returns 1 (the trailing character class rejects loose matches like `Drafting`).
  - H1 sanity — `grep -E '^# Strategic Intent$' templates/strategic-intent.md` returns 1 (the H1 below the closing `---`).
- **Approach:**
  - In the first YAML block, replace the line `object_type: <pre-filled per template — e.g., Strategic Intent>` with `object_type: Strategic Intent`.
  - Confirm `status: Draft` already matches (the skeleton ships with this pre-fill); no edit needed unless the skeleton drifts.
  - Replace the body's `# <Artifact name>` H1 with `# Strategic Intent`.
  - Replace the existing `> One-paragraph description...` blockquote line below the H1 with a one-paragraph description that names the artifact as the Strategy → Discovery handover and cites `docs/HANDOVERS.md` §"Handover 1: Strategy → Discovery". Angle-bracket placeholders for any kit-user-fillable phrasing.
- **Done when:** T10 passes; H1 sanity grep returns 1; no other field changes in this task.

### Task 3: Replace the skeleton's generic required-section headings with HANDOVERS-Handover-1 quotes

- **Depends on:** Task 2
- **Tests:**
  - T4 from spec — the five HANDOVERS-quoted headings appear in order: `## The challenge`, `## The guiding policy`, `## Coherent actions`, `## Coherence check`, `## Open questions for discovery`. Verify by recording line numbers with `grep -n` and asserting monotonicity.
  - Heading count sanity — `grep -cE '^## ' templates/strategic-intent.md` returns 6 (five required H2 + `## Optional sections`). If the skeleton ever stops shipping the `## Optional sections` heading, this count is 5; treat as drift and surface.
- **Approach:**
  - Remove the three `## <Required section N from HANDOVERS.md>` placeholder headings the skeleton ships with (the skeleton shows 1, 2, N).
  - Insert the five Handover-1 required-section H2 headings verbatim from HANDOVERS.md, in order.
  - Under each H2, leave a one-line `<placeholder>` body that paraphrases the HANDOVERS "what this section is" hint (e.g., under `## The challenge`: `<What specifically must be addressed; cite evidence — numbers, quotes, market signal.>`). The brackets keep it angle-bracket-only.
  - Preserve the trailing `## Optional sections` heading and its single sub-bullet — the skeleton's optional-sections discipline carries over.
- **Done when:** T4 and heading-count sanity pass.

### Task 4: Append the Handover-1-specific frontmatter fields

- **Depends on:** Task 2 (independent of Task 3 mechanically, but sequenced here for diff hygiene)
- **Tests:**
  - T3 from spec — every key in (universal-schema set ∪ Handover-1-specific set) appears at top level in the file's YAML frontmatter. Asserted by a python one-liner (assumes frontmatter starts at the first `---` on line 1, which the parent skeleton enforces — the skeleton's HTML comment sits below the closing `---`, in the body, not above the opening `---`): `python3 -c "import yaml,sys; body=open('templates/strategic-intent.md').read(); fm=body.split('---',2)[1]; data=yaml.safe_load(fm); required={'id','slug','object_type','name','description','owner','status','priority','risk_level','created','last_updated','parent_intent','parent_opportunity','parent_learning','parent_vision','parent_initiative','related_problems','related_personas','related_kpis','evidence_basis','open_assumptions','human_owned_decisions','ai_assistance_used','ai_assistance_allowed','human_approval_required','approvals_obtained','open_questions','risks','mode','central_challenge','guiding_policy','coherent_actions','horizon','business_objective','parent_diagnosis'}; missing=required - set(data.keys()); assert not missing, missing"`.
  - Handover-1 verbatim values for the human-owned-decision strings: `grep -F 'Whether to pursue this central challenge' templates/strategic-intent.md` returns ≥ 1; `grep -F 'Resource commitment behind coherent actions' templates/strategic-intent.md` returns ≥ 1.
- **Approach:**
  - The skeleton's first YAML block ends with three comment lines just above the closing `---`. Identify them by their exact verbatim text (not by position):
    > `# Handover-specific fields (per docs/HANDOVERS.md row for this handover)`
    > `# Add fields from HANDOVERS.md that are required for this artifact type.`
    > `# Example for Strategic Intent: central_challenge, guiding_policy, coherent_actions, horizon.`
  - Locate by content (grep the literal strings above), then delete the line beginning `# Example for Strategic Intent:`. Keep the first two comment lines as the section marker. Insert the seven Handover-1-specific fields after the two retained comment lines, quoted verbatim from HANDOVERS Handover 1:
    ```yaml
    mode: <greenfield | enterprise>
    central_challenge: <one sentence>
    guiding_policy: <one paragraph>
    coherent_actions:
      - <action 1>
      - <action 2>
      - <action 3>
      # 3-5 items, no more
    horizon: <quarters>
    business_objective: <linked Business Objective id>
    parent_diagnosis: <path to diagnosis>
    ```
  - In the first YAML block's universal-schema section, update the existing `human_owned_decisions:` list (currently `- <decision a human must make personally>`) to the two HANDOVERS-pinned items:
    ```yaml
    human_owned_decisions:
      - Whether to pursue this central challenge
      - Resource commitment behind coherent actions
    ```
    and update `human_approval_required:` from `<true | false>` to `true` (the Handover-1 contract pins it to `true`).
  - Do not repeat `object_type` in the second block — it lives in block 1 (universal schema) pre-filled to `Strategic Intent`. The parent convention's "Frontmatter ordering" rule treats universal-schema fields as block 1 and *additional* (handover-specific) fields as block 2.
- **Done when:** T3 passes; both HANDOVERS-verbatim string greps return ≥ 1; no key in the universal-schema block is duplicated in the Handover-1 block; sanity check `grep -c '# Handover-specific fields' templates/strategic-intent.md` returns exactly 1 (the section marker is intact and not duplicated); sanity check `grep -c '# Example for Strategic Intent' templates/strategic-intent.md` returns 0 (the example comment was removed).

### Task 5: VERIFY — linter, pytest, pre-pr all green

- **Depends on:** Tasks 3 and 4
- **Tests:**
  - T2 from spec — `python3 tools/lint-frontmatter.py --check-template templates/strategic-intent.md` exits 0.
  - T5 from spec — `grep -c '{{' templates/strategic-intent.md` returns 0; `grep -c '__FILL__' templates/strategic-intent.md` returns 0.
  - T6 from spec — `python3 -m pytest scripts/tests/test_templates_instantiate.py -k 'strategic-intent.md'` exits 0 and selects exactly 1 parametrized test (the path-token form matches pytest's parametrized ID `test_template_passes_check_template_mode[templates/strategic-intent.md]`; verified by `--collect-only`). Running the whole file is also acceptable since the exit code is all that matters.
  - T11 from spec — `python3 tools/lint-frontmatter.py --all` exits 0 (default mode does not traverse `templates/`; mode-separation property).
  - `pre-pr-clean` cross-cutting — `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Run the five predicates above in order.
  - On any red: read the linter / pytest output, fix the smallest thing that explains the failure (almost always a misplaced field or a malformed placeholder), re-run. Cap at three iterations per the work-loop's max-five rule applied to the VERIFY sub-loop; if still red, surface and stop.
- **Done when:** all five tests above pass on a single clean run.

### Task 6: REVIEW — dispatch adversarial-reviewer against the shipped template

- **Depends on:** Task 5
- **Tests:**
  - Reviewer returns no Blocking findings against `templates/strategic-intent.md` vs `docs/HANDOVERS.md` §"Handover 1: Strategy → Discovery" and `docs/specs/template-authoring-convention/spec.md`.
  - All spec tests (T1–T7, T10, T11) and `pre-pr-clean` still green after any reviewer-driven fixes.
- **Approach:**
  - Dispatch `adversarial-reviewer` with the prompt: "Review `templates/strategic-intent.md` against `docs/HANDOVERS.md` §'Handover 1: Strategy → Discovery' and `docs/specs/template-authoring-convention/spec.md`. Look for: HANDOVERS-vs-template drift (missing required fields, missing required sections, headings not quoted verbatim); placeholder-syntax violations; ontology-domain content leaking into the template body; frontmatter ordering deviations from the parent convention; missing pre-fills the parent convention demands. Return findings as a numbered list with severity Blocking | Suggested | Nit."
  - Address Blocking findings by editing the template. Re-run Task 5's VERIFY before re-dispatching the reviewer.
  - Max 3 review passes. If still Blocking at iter 3, stop and surface to the orchestrator.
- **Done when:** reviewer returns clean (no Blocking findings); Task 5's tests still pass.

### Task 7: CAPTURE — append to `_meta` README; tick ROADMAP F3.1; freeze spec + plan status

- **Depends on:** Task 6
- **Tests:**
  - T8 from spec — `grep -c '^- \[x\] \*\*F3\.1\*\*' ROADMAP.md` returns 1.
  - T9 from spec — `grep -c 'strategic-intent.md' templates/_meta/README.md` returns ≥ 1.
  - Spec status frozen: `grep -E '^- \*\*Status:\*\* Shipped' docs/specs/template-strategic-intent/spec.md` returns 1.
  - Plan status frozen: `grep -E '^- \*\*Status:\*\* Done' docs/specs/template-strategic-intent/plan.md` returns 1.
  - `pre-pr-clean` cross-cutting — `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Append a line to the "Shipped templates" list in `templates/_meta/README.md`: ``- [`strategic-intent.md`](../strategic-intent.md) — Strategy → Discovery handover (HANDOVERS §"Handover 1"). Spec: `docs/specs/template-strategic-intent/`.``. Replace the placeholder italic "_(None yet. …)_" line iff this is the first F3.x append; otherwise add a new bullet beneath the existing list (the orchestrator's sequential-merge step resolves cross-worker conflicts).
  - Edit `ROADMAP.md`: change `- [ ] **F3.1**` to `- [x] **F3.1**` and append `Shipped: <YYYY-MM-DD>` after the existing slug parenthetical.
  - Freeze `docs/specs/template-strategic-intent/spec.md` Status to `Shipped (<YYYY-MM-DD>)`.
  - Freeze `docs/specs/template-strategic-intent/plan.md` Status to `Done (<YYYY-MM-DD>)` and `Plan review:` to `approved`.
  - Bundle into a tiny dedicated commit per parent plan §Rollout to make Stage-2 merging trivial.
- **Done when:** all five CAPTURE-phase predicates pass.

## Rollout

- ROADMAP P7.2 (`/strategic-intent` synthesis command) becomes unblocked once F3.1 ships.
- `templates/_meta/README.md` gains one bullet; index now lists one shipped template.
- No INVENTORY row added — templates are content, not tooling (parent plan §Rollout pinned this).
- No `AGENTS.md` edit required — the source-of-truth table already points at `templates/` indirectly via CONVENTIONS.md §"Templates" (the parent convention's sub-section).
- No `docs/HANDOVERS.md` edit. The Handover-1 contract is the source-of-truth that F3.1 re-projects.

## Risks

- **HANDOVERS-vs-template drift.** If a future edit to HANDOVERS Handover 1 (adding a required field, renaming a section) lands without a corresponding update to `templates/strategic-intent.md`, the template silently goes stale. Mitigation: Task 6's adversarial review explicitly diffs the template against HANDOVERS, and the parent convention's `scripts/tests/test_templates_instantiate.py` auto-discovers `templates/*.md` so any frontmatter-shape regression surfaces via the linter — but field-name additions in HANDOVERS that aren't yet keys the linter knows about would not surface until a future audit. Track as a kit-wide concern, not an F3.1-specific bug.
- **pyyaml block-scalar handling on the `guiding_policy: <one paragraph>` field.** HANDOVERS shows `guiding_policy: <one paragraph>` as an inline scalar; if a kit user later switches it to a `|` block scalar, the `--check-template` mode handles it (parent spec T9 covers this). For F3.1 itself, we ship the inline form to match HANDOVERS verbatim.
- **Race on `templates/_meta/README.md`** during Stage-2 merge across the parallel F3.x workers. Mitigation: the CAPTURE commit is tiny, append-only, and conflict-resolution is mechanical. Parent plan §Rollout already pinned this strategy.
- **The `coherent_actions:` field includes a `# 3-5 items, no more` comment from HANDOVERS.** pyyaml drops comments on parse; the linter's `--check-template` mode operates on parsed data, so the comment survives in the markdown source but doesn't influence linting. Verified by inspection. No mitigation needed.
- **The reviewer subagent may surface a HANDOVERS gap** (e.g., a required-section heading that doesn't make sense for a single-file Strategic Intent). Mitigation: if surfaced as Blocking, surface upward to the orchestrator; do not edit HANDOVERS inside F3.1. Per spec §Boundaries → Never do.

## Changelog

- 2026-05-22 (review-iter-1): Applied adversarial-reviewer fixes — Finding 2 (Task 4 comment-line precision), Finding 3 (one-liner skeleton-leading clarification), Finding 5 (T10 regex tightening), Finding 6 (T6 pytest filter form), cross-cutting T11 framing correction, cross-cutting dedup convention bullet added.
