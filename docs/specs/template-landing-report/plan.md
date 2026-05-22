# Plan: template-landing-report

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-22)
- **Plan review:** approved (pre-EXECUTE × 2 iterations, converged clean)

> **Plan contract.** Implementation strategy for the spec. Allowed to change as we learn; changelog at the bottom.

## Approach

Seven tightly-scoped tasks landing on one commit (or a small commit chain — orchestrator decides). The work is shape-only: copy `templates/_meta/template-skeleton.md` to `templates/landing-report.md`, pre-fill the four identity fields (the H1, `object_type: Landing Report`, `status: Draft`, the spec-cite blockquote), replace the placeholder section headings with HANDOVERS Handover 7's seven sections verbatim, and append the Handover-7-specific frontmatter under the `# Handover-specific fields` YAML comment block. Then VERIFY (`--check-template` + pytest + pre-pr.sh), REVIEW (adversarial-reviewer), CAPTURE (`_meta/README.md` entry + ROADMAP F3.10 checkbox).

Why this sequence: Tasks 1 → 2 → (3 ∥ 4) → 5 → 6 → 7. Task 1 (copy skeleton) is the load-bearing prerequisite. Task 2 (pre-fill identity) lets the H1 + frontmatter `object_type` be the file's signature. Tasks 3 (sections) and 4 (frontmatter) are independent and parallelizable — neither touches the other's region of the file. Task 5 (VERIFY) is the integration gate. Task 6 (REVIEW) is adversarial-reviewer. Task 7 (CAPTURE) does the README + ROADMAP updates and runs `bash tools/pre-pr.sh` one final time.

This is template-authoring work, not script-authoring work. No new code, no new dependencies, no new tests. The verification machinery (`--check-template` mode, `test_templates_instantiate.py`) was shipped by the parent convention (`docs/specs/template-authoring-convention/`); this loop only fills a single new artifact and lets the existing machinery exercise it.

## Constraints

- **Angle-bracket placeholders only.** No `{{`, `__FILL__`, `???`, ` TBD`. Enforced by spec T5.
- **Date placeholders are exactly `<YYYY-MM-DD>`.** Five places: `created`, `last_updated`, `shipped`, `measured_at`, `verdict_at`. Consistency is what lets `--check-template` succeed and a kit user scan-fill the file.
- **Verdict enum placeholder shape: exactly `<adopt | fix | kill>`.** One angle-bracket group around the three enum members, pipe-separated. Enforced by spec T10.
- **`# at least 30 days post-ship` comment on `measured_at` is verbatim.** Enforced by spec T11.
- **No edits to shared files** (`docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `templates/_meta/template-skeleton.md`, `tools/lint-frontmatter.py`, `scripts/tests/test_templates_instantiate.py`, `context/frameworks/ontology.md`). Read-only inputs.
- **`templates/_meta/README.md` is a shared write target** (ten F3.x workers append to it). This worker's append must be a clean single-line addition that is trivially merge-conflict-resolvable (per parent convention §"Rollout"). The line goes under §"Shipped templates" only; no other section touched.
- **No new ontology types.** Enforced by spec T14.
- **Atomic writes via the editing tools' built-in tempfile + replace** (the Edit/Write tools the executor uses already do atomic writes; no custom Python machinery needed).
- **Stdlib + pyyaml only** if any verification step uses a Python one-liner (pyyaml is already a kit dependency via `tools/lint-frontmatter.py`).
- **Total iterations capped at 5** per state.json. Hit-the-cap → stop, replan, do not grind.

## Construction tests

Cross-cutting only. Per-task tests live under each Task below.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 at end of Task 5 and again at end of Task 7. Two clean passes is the gate.

## Tasks

### Task 1: Copy `templates/_meta/template-skeleton.md` to `templates/landing-report.md`

- **Depends on:** none
- **Tests:**
  - **T1** from spec — `test -f templates/landing-report.md` succeeds.
  - Skeleton-equivalence sanity check: pre-pre-fill, `diff -q templates/_meta/template-skeleton.md templates/landing-report.md` returns "files match" (the copy was clean, not corrupted). Run this check before Task 2 starts.
- **Approach:**
  - Read `templates/_meta/template-skeleton.md` (the canonical skeleton).
  - Write the same body to `templates/landing-report.md` using the Write tool.
- **Done when:** T1 passes; the diff check returns "files match."

### Task 2: Pre-fill the four identity fields in `templates/landing-report.md`

- **Depends on:** Task 1
- **Tests:**
  - **T12** from spec — `grep -E "^status: Draft" templates/landing-report.md` returns exactly one line. (The skeleton already pre-fills this; Task 2 just preserves it.)
  - **T13** from spec — `grep -E "^object_type: Landing Report$" templates/landing-report.md` returns exactly one line.
  - H1 check — `grep -E "^# Landing Report$" templates/landing-report.md` returns exactly one line.
  - Blockquote check — `grep -E "^> .*HANDOVERS\.md.*Handover 7" templates/landing-report.md` returns at least one line.
- **Approach:**
  - Edit `object_type:` line: replace `<pre-filled per template — e.g., Strategic Intent>` with `Landing Report`.
  - Edit the H1 `# <Artifact name>` to `# Landing Report`.
  - Edit the H1-following blockquote: replace the placeholder one-line description with a one-paragraph description citing `docs/HANDOVERS.md` §"Handover 7: Engineering → Landings" and restating the 30-day measurement gap. Format: `> This artifact is the Engineering → Landings handover... Cite docs/HANDOVERS.md §"Handover 7: Engineering → Landings". The "measured_at" date must be at least 30 days after "shipped"; otherwise the report is premature.`
  - `status: Draft` is already pre-filled by the skeleton — preserve it; do not edit.
- **Done when:** T12, T13, the H1 check, and the blockquote check all pass.

### Task 3: Replace the placeholder required-section headings with HANDOVERS Handover 7's seven sections verbatim

- **Depends on:** Task 2 (the identity must be in place so the file's purpose is unambiguous before adding handover-specific structure)
- **Tests:**
  - **T4** from spec — the seven required section headings appear verbatim in HANDOVERS-defined order:
    1. `## The shipped change`
    2. `## Predicted outcomes vs actuals`
    3. `## Adoption curve`
    4. `## Counter-metrics`
    5. `## What landed and what didn't`
    6. `## Verdict`
    7. `## Feedback to strategy`
  - **T5** from spec — angle-bracket placeholders only; no forbidden placeholder tokens introduced.
- **Approach:**
  - Replace the skeleton's three `## <Required section N from HANDOVERS.md>` placeholder headings (and their bodies) with seven `## …` headings drawn verbatim from `docs/HANDOVERS.md` §"Handover 7: Engineering → Landings" Required sections list.
  - Each section body is one angle-bracket placeholder paraphrasing HANDOVERS Handover 7's prose for that section. Examples (final wording finalized during EXECUTE):
    - `## The shipped change` → `<One-paragraph recap of the shipped change. Cite the parent handoff packet and the shipped commit/PR.>`
    - `## Predicted outcomes vs actuals` → `<Table: KPI id, predicted threshold (from the parent Vision's predicted_outcomes), measured actual, delta, met-yes-no. Cite the Vision's predicted thresholds verbatim.>`
    - `## Adoption curve` → `<Visualization or table of adoption by cohort or surface, from shipped through measured_at. Note where the curve plateaus or rolls back.>`
    - `## Counter-metrics` → `<For each counter-metric KPI declared in the Vision, the measured value at measured_at. Did we break anything we said we were watching?>`
    - `## What landed and what didn't` → `<Surviving assumptions that held up in production; surviving assumptions that did not. Tie each to a learning memo if available.>`
    - `## Verdict` → `<One of: adopt (move on), fix (named change), kill (rollback). Justify in one paragraph.>`
    - `## Feedback to strategy` → `<What this teaches for the next quarterly /strategy-refresh. Surface any contradictions with the parent intent's guiding policy.>`
  - Preserve the `## Optional sections` block from the skeleton at the bottom of the file unchanged.
- **Done when:** T4 and T5 pass.

### Task 4: Append Handover-7-specific frontmatter under the `# Handover-specific fields` block

- **Depends on:** Task 2 (the file's identity must be set; the existing `# Handover-specific fields` YAML comment block is the insertion point)
- **Tests:**
  - **T3** from spec — all ten Handover-7 frontmatter keys present.
  - **T3b** from spec — dedup block-placement invariant: `object_type`, `human_owned_decisions`, `human_approval_required` are absent from the handover-specific block.
  - **T10** from spec — `grep -E "^verdict: <adopt \| fix \| kill>$"` returns exactly one line.
  - **T11** from spec — `grep -E "^measured_at: <YYYY-MM-DD>\s+# at least 30 days post-ship$"` returns exactly one line.
- **Approach:**
  - Inside the YAML frontmatter (between the two `---` markers), find the `# Handover-specific fields` YAML comment block (and its accompanying two guidance comment lines from the skeleton). Replace those two guidance lines with the Handover-7 additions block, in exactly this order and form:

    ```yaml
    # Handover-specific fields (per docs/HANDOVERS.md §"Handover 7: Engineering → Landings")
    # object_type, human_owned_decisions, human_approval_required: set in universal block above.
    parent_vision: <vision slug>
    parent_handoff_packet: <handoff packet slug>
    shipped: <YYYY-MM-DD>
    measured_at: <YYYY-MM-DD>     # at least 30 days post-ship
    verdict: <adopt | fix | kill>
    verdict_at: <YYYY-MM-DD>
    verdict_by: ["<name>: <YYYY-MM-DD>"]
    ```

  - **Do not duplicate** `object_type`, `human_owned_decisions`, or `human_approval_required` here — those keys exist in the universal-schema block at the top of the frontmatter. The Handover-7 contract names them, but they live in the universal block; the handover-specific block adds only the *new* fields. Note this fact in the changelog if the reviewer flags it.
  - **Augment** the universal-schema block's `human_owned_decisions:` list (which currently reads `- <decision a human must make personally>`) by adding the two Handover-7-mandated bullets verbatim:
    ```yaml
    human_owned_decisions:
      - Verdict
      - Decision to revert, double-down, or fix
      - <decision a human must make personally>
    ```
    Keep the trailing placeholder so a kit user knows additional decisions can be added.
- **Done when:** T3, T3b, T10, T11 pass.

### Task 5: VERIFY — `--check-template` exits 0; pytest exits 0; pre-pr exits 0

- **Depends on:** Task 3 AND Task 4
- **Tests:**
  - **T2** from spec — `python3 tools/lint-frontmatter.py --check-template templates/landing-report.md` exits 0.
  - **T3b** from spec — dedup block-placement invariant holds.
  - **T5** from spec — placeholder-syntax purity (re-run after Tasks 3 + 4).
  - **T6** from spec — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0.
  - **T14** from spec — no new ontology type added (`grep -nE "^(\|\s*)?[Ll]anding [Rr]eport [Vv]erdict" context/frameworks/ontology.md` returns zero hits).
  - **T15** from spec — `## Optional sections` block preserved (`grep -cE "^## Optional sections" templates/landing-report.md` returns exactly 1).
  - `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Run the four commands above in sequence.
  - On a single failure: diagnose against the file at `templates/landing-report.md`. Likely cause vectors: malformed angle-bracket placeholder (e.g., `< >` whitespace-only), missing required frontmatter key, accidental `{{` introduced by paste, accidental edit to a shared file. Fix locally; re-run.
  - On three consecutive same-error failures: state.json `consecutive_same_error_count` triggers a stop. Replan; do not grind.
- **Done when:** all seven checks pass in one clean sequence.

### Task 6: REVIEW — dispatch `adversarial-reviewer`

- **Depends on:** Task 5
- **Tests:**
  - Reviewer returns "no findings" OR all findings are resolvable in ≤ 3 review iterations (per `max_iterations` cap in state.json).
- **Approach:**
  - Dispatch `adversarial-reviewer` with the prompt named in spec §"Verification mode" — i.e., review the spec and plan against the parent convention and against HANDOVERS Handover 7; look for drift, missing frontmatter keys, uncovered acceptance criteria, the 30-day measurement-gap encoding, the verdict-enum placeholder shape, vague language, angle-bracket discipline, and the `verdict_by` placeholder form's well-definedness.
  - For each numbered finding: triage severity (Critical/High/Medium/Low). Address Critical and High in the same loop. Defer Medium/Low to a follow-up issue only if scope-adjacent to the parent convention; otherwise resolve in-session per the `feedback_small_defers_same_session` user memory.
- **Done when:** the reviewer returns clean OR three iterations have closed all High+ findings and any remaining are explicitly marked deferred.

### Task 7: CAPTURE — `_meta/README.md` index entry + ROADMAP F3.10 checkbox + final pre-pr

- **Depends on:** Task 6
- **Tests:**
  - **T8** from spec — `grep -E "^- \[x\] \*\*F3\.10\*\*" ROADMAP.md` returns exactly one line.
  - **T9** from spec — `grep -E "landing-report\.md" templates/_meta/README.md` returns at least one line.
  - `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 (second clean pass).
- **Approach:**
  - Append a one-line entry under `templates/_meta/README.md` §"Shipped templates": `- [\`landing-report.md\`](../landing-report.md) — Engineering → Landings handover (Handover 7). Predicted-vs-actual outcomes, adoption curve, counter-metrics, verdict.`
  - Remove the `_(None yet. F3.x workers append their templates here in their CAPTURE phase.)_` line if this is the first F3.x worker to land; otherwise simply append. (Coordinated with the other nine F3.x workers' README appends per the parent convention's §"Rollout".)
  - Edit `ROADMAP.md`: flip F3.10's `- [ ]` to `- [x]` on the single line that begins `- [ ] **F3.10** Landing Report template.`
  - Run `bash tools/pre-pr.sh` one final time.
- **Done when:** T8 and T9 pass; pre-pr is clean.

## Rollout

- **`templates/landing-report.md` is callable immediately** by anyone who reads `templates/_meta/README.md`'s §"Shipped templates" list. No announcement step needed.
- **P5.1 `/landing-report`** (the downstream command) becomes implementable. Its spec lists F3.10 as a dependency; with F3.10 shipped, P5.1's loop can start.
- **P5.9 `/audit-landings-debt`** has a shape to audit against. Its spec can be authored without further blocker.
- **No edit needed to AGENTS.md.** The "Required metadata for any artifact?" row already points at `docs/CONVENTIONS.md`, and the new template is discoverable via the `templates/_meta/README.md` index.
- **No INVENTORY.md row added.** Templates are infrastructure (parallel reasoning to the parent convention's §"Rollout").
- **No new audit or skill required.** The template is consumed by `--check-template` (existing linter mode) and `test_templates_instantiate.py` (existing pytest).

## Risks

- **Race on `templates/_meta/README.md` append.** Ten F3.x workers each append to the same file's §"Shipped templates" list. Mitigation: each worker writes a single trivially-mergeable line; the F3 plan's Stage 2 merge sequentializes the PRs (per parent convention §"Rollout"). If a merge conflict surfaces, resolve by accepting both lines in order.
- **`verdict_by` placeholder shape disagreement.** Spec Open Question 1 names this as a deliberate enrichment over HANDOVERS' literal text. If the adversarial reviewer rejects the augmented form, fall back to `verdict_by: [<names>]` (single-line edit in Task 4). Cost: lose timestamp guidance, but stay strictly faithful to HANDOVERS.
- **30-day measurement-gap signal disagreement.** Spec Open Question 2 names the blockquote restatement as additive guidance. If the reviewer rejects it, drop it from the blockquote in Task 2 (keep only the `# at least 30 days post-ship` frontmatter comment). The HANDOVERS-verbatim comment is non-negotiable; only the blockquote restatement is up for debate.
- **Date-placeholder shape inconsistency.** Five date placeholders across the file (`created`, `last_updated`, `shipped`, `measured_at`, `verdict_at`). Risk: a typo introduces `<YYYY-MM-DDD>` or `<yyyy-mm-dd>`. Mitigation: a one-line grep during VERIFY — `grep -cE "<YYYY-MM-DD>" templates/landing-report.md` returns ≥ 5. If lower, find the typo and fix.
- **Verdict enum placeholder gets split.** If a kit user (or the executor) accidentally writes `verdict: <adopt> | <fix> | <kill>` instead of `verdict: <adopt | fix | kill>`, T10 fails. Mitigation: T10's exact-match regex catches this; the fix is a single Edit call.
- **`object_type` duplicated across universal and handover-specific blocks.** The skeleton's universal block carries `object_type:`; HANDOVERS Handover 7 also names `object_type: Landing Report`. Task 4's approach explicitly de-duplicates by listing `object_type` in the universal block only and *not* in the handover-specific block. Risk: a reviewer reads HANDOVERS verbatim and flags the omission. Mitigation: leave a one-line YAML comment in the handover-specific block — `# object_type, human_owned_decisions, human_approval_required: set in universal block above.` This makes the design choice explicit at the diff site.

## Changelog

- 2026-05-22 (review-iter-1): Applied adversarial-reviewer fixes — Finding 1 (OQ1 verdict_by augmented form resolved), Finding 2 (OQ2 blockquote+YAML-comment dual-signal resolved), Finding 3 (T3b dedup block-placement test added), Finding 4 (plan Task 4 YAML excerpt comment added), Finding 5 (T15 Optional sections preservation test added), cross-cutting dedup convention bullet added.
