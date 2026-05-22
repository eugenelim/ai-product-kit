# Plan: template-ost

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-22)
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for the spec. Allowed to change as we learn; changelog at the bottom.

## Approach

Seven sequential tasks landing in a single in-session loop: copy the skeleton, pre-fill the template's identity, swap the placeholder section headings for the five Handover-2 required sections in order, append the Handover-2-specific frontmatter under the convention's `# Handover-specific fields` block, VERIFY against the linter and pytest harness, REVIEW with `adversarial-reviewer`, then CAPTURE by appending one line to `templates/_meta/README.md` and checking off F3.2 in `ROADMAP.md`. The sequencing is load-bearing: the skeleton must be copied before any pre-fill, and frontmatter must be in place before VERIFY (otherwise `--check-template` cannot exit 0). Tasks 3 and 4 are mechanically independent but small; running them in series keeps each task one coherent commit-sized edit.

Why this approach over alternatives: handwriting the template from scratch (without the skeleton) would reintroduce the universal-schema-ordering drift the parent spec exists to prevent. Authoring the body sections in arbitrary order would risk the order-sensitive contract test T4. The skeleton-copy-then-specialize path is what the parent spec's authoring convention prescribes; deviating from it would break the parallel-safety contract across the ten F3.x specs.

No new dependencies. Python stdlib + pyyaml (already a kit dependency via `tools/lint-frontmatter.py`); no shell tooling beyond `cp`, `awk`, `grep`, and the existing `tools/pre-pr.sh`. The template is a static text file — no executable code.

## Constraints

- **Angle-bracket placeholders only.** Every non-identity value is `<descriptor>`-shaped per `docs/CONVENTIONS.md` §"Templates" → "Placeholder syntax". No `{{...}}`, no `__FILL__`, no `<>` or `< >`. Concrete-value validation under `--check-template` rejects malformed forms; the spec's T5 enforces this with a grep.
- **Nested-container-placeholder rule applies.** The Handover-2 frontmatter has two nested mappings (`outcome:` with five keys, `chosen_opportunity:` with two keys) and three list-shaped fields (`opportunity_count` is scalar; `related_personas`, `related_problems`, `human_owned_decisions`). Per the parent spec §"Outputs" item 4, a nested mapping is acceptable iff every **leaf scalar** inside it is a valid placeholder. Both nested mappings must therefore have every leaf as `<…>`-form; mixing a concrete value with placeholders inside the same nested map is allowed only if the concrete value satisfies its field's type/enum constraint, which Handover-2 doesn't impose on these leaves.
- **Universal-schema field ordering must match the skeleton.** Re-ordering would silently break templates downstream (downstream `--check-template` doesn't enforce order, but diffs across the ten F3.x templates do — that's the parent spec's "frontmatter ordering" contract).
- **Status pre-filled to `Draft`** (the product-artifact lifecycle entry state — see `docs/CONVENTIONS.md` §"Lifecycle states"). Status is the *template's instance's* initial status, not the template-file-itself's status (that's tracked by this spec's `Status:` bullet).
- **`object_type: Opportunity Solution Tree`** is the one and only ontology-type identity pre-fill. Do not duplicate the `object_type:` line in the handover-specific block; it lives once in the universal-schema position.
- **No edits to shared kit infrastructure** during this task other than the two append-only edits in Task 7 (`templates/_meta/README.md` and `ROADMAP.md` F3.2 checkbox). No edits to `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, or `scripts/tests/test_templates_instantiate.py`.
- **No fabricated OST domain content** in the body. The five required sections each carry a one-line angle-bracket placeholder describing what the kit user writes — not an example of what they might write.

## Construction tests

Cross-cutting only. Per-task tests are inline under each task.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 after the loop. Run before declaring Done.

## Tasks

### Task 1: `templates/ost.md` exists, copied verbatim from the skeleton

- **Depends on:** none
- **Tests:**
  - `T1` from spec — `test -f templates/ost.md` exits 0.
  - Byte-for-byte equality with the skeleton at this point: `diff templates/_meta/template-skeleton.md templates/ost.md` returns empty.
- **Approach:**
  - `cp templates/_meta/template-skeleton.md templates/ost.md`.
  - No edits yet — the file is the literal skeleton.
- **Done when:** T1 passes; diff against skeleton is empty.

### Task 2: Identity pre-fills land (`object_type`, `status`, H1)

- **Depends on:** Task 1
- **Tests:**
  - Frontmatter has `object_type: Opportunity Solution Tree` (exact string).
  - Frontmatter has `status: Draft` (already in skeleton; assert preserved).
  - H1 line is `# Opportunity Solution Tree` (replacing skeleton's `# <Artifact name>`).
  - Asserted by: `grep -E "^object_type: Opportunity Solution Tree$" templates/ost.md` returns 1; `grep -E "^# Opportunity Solution Tree$" templates/ost.md` returns 1.
- **Approach:**
  - Replace the skeleton's `object_type: <pre-filled per template — e.g., Strategic Intent>` with `object_type: Opportunity Solution Tree`.
  - Leave `status: Draft` as-is (skeleton already pre-fills it).
  - Replace H1 `# <Artifact name>` with `# Opportunity Solution Tree`.
  - Replace the skeleton's one-paragraph description placeholder with a one-paragraph angle-bracket placeholder pointing at HANDOVERS §"Handover 2": `> <One-paragraph description of the OST artifact this instance represents. Cite docs/HANDOVERS.md §"Handover 2: Discovery → Validation".>`. (The leading `>` keeps it a blockquote per skeleton shape.)
- **Done when:** the three greps above return their expected counts; no other line changed.

### Task 3: Body sections replaced with the five Handover-2 required sections, in order

- **Depends on:** Task 2
- **Tests:**
  - `T4` from spec — `awk '/^## /' templates/ost.md` returns exactly, in this order:
    ```
    ## The outcome
    ## Opportunity space
    ## The chosen one
    ## Source opportunities
    ## Excluded
    ## Optional sections
    ```
  - No fabricated content: each of the five sections has a single angle-bracket-placeholder body line (one sentence describing what to write, not an example).
- **Approach:**
  - Replace the skeleton's three required-section placeholder headings (`## <Required section 1 from HANDOVERS.md>`, `## <Required section 2 …>`, `## <Required section N …>`) with the five Handover-2 headings, in order — i.e., expand from three to five (the OST requires more sections than the skeleton pre-allocates).
  - Under each, write one angle-bracket placeholder line describing the section's contract, paraphrased from HANDOVERS §"Handover 2" required-sections list. Examples:
    - `## The outcome` body: `<The measurable outcome this tree pursues, tied to the parent intent's coherent action.>`
    - `## Opportunity space` body: `<The tree of opportunities surfaced from discovery interviews.>`
    - `## The chosen one` body: `<Why this opportunity, why now, and what we give up by choosing it.>`
    - `## Source opportunities` body: `<Interview-level evidence under each tree node.>`
    - `## Excluded` body: `<Opportunities considered and explicitly excluded, with reason.>`
  - Leave the `## Optional sections` heading and its "Delete the heading…" guidance line from the skeleton; remove the `### <Optional section A>` sub-heading example since Handover 2 enumerates no optional sections.
- **Done when:** T4 passes; body is shape-only.

### Task 4: Handover-2 frontmatter appended under `# Handover-specific fields` block

- **Depends on:** Task 2 (frontmatter must exist before append; mechanically independent of Task 3)
- **Tests:**
  - `T2` from spec — `python3 tools/lint-frontmatter.py --check-template templates/ost.md` exits 0.
  - `T3` from spec — the parsed YAML has all seven Handover-2 keys (`object_type`, `parent_intent`, `outcome`, `opportunity_count`, `chosen_opportunity`, `related_personas`, `related_problems`, `human_owned_decisions`), all five nested keys under `outcome:`, and both nested keys under `chosen_opportunity:`.
  - Nested-container placeholder validity: `outcome.id`, `outcome.metric`, `outcome.current`, `outcome.target`, `outcome.measurement`, `chosen_opportunity.id`, `chosen_opportunity.rationale` are all angle-bracket placeholders (asserted by the linter's nested-leaf recursion).
- **Approach:**
  - Locate the skeleton's `# Handover-specific fields (per docs/HANDOVERS.md row for this handover)` comment block (just before the closing `---`).
  - Apply the **universal-schema-first dedup convention** (spec §"Boundaries → Always do"). HANDOVERS-2 fields that overlap the universal-schema block — `object_type`, `parent_intent`, `related_personas`, `related_problems`, `human_owned_decisions` — stay in their universal-schema positions (retained per the traceability-key call in spec §"Outputs" item 1), carrying the HANDOVERS-2-mandated values; their placeholders are NOT restated under the handover-specific block. The handover-specific block carries only fields not present in the universal schema. The block lands as:

    ```yaml
    outcome:
      id: <OUT-NNN>
      metric: <name>
      current: <value>
      target: <value>
      measurement: <how, where, by when>
    opportunity_count: <total nodes>
    chosen_opportunity:
      id: <OPP-NNN>
      rationale: <one paragraph>
    ```

  - In the universal-schema block: overwrite the skeleton's `human_owned_decisions:` placeholder list with the two HANDOVERS-2-mandated entries ("Selection of the chosen opportunity", "What opportunities to explicitly exclude from the tree"). Retain `parent_intent`, `related_personas`, `related_problems`, `related_kpis` placeholders as-is (their values stay user-supplied angle-bracket placeholders). Drop the skeleton's `parent_opportunity`, `parent_learning`, `parent_vision`, `parent_initiative` lines (an OST is the Discovery phase's starting artifact — no upstream artifacts pre-exist; see spec §"Outputs" item 1). Do NOT duplicate any of these keys under the handover-specific block — that would create duplicate top-level YAML keys and violate the dedup convention.
  - Mind the **nested-container-placeholder rule** for `outcome:` and `chosen_opportunity:`: every leaf must be `<…>`-shaped. Test before commit.
- **Done when:** T2 passes; T3 passes.

### Task 5: VERIFY — linter clean, pytest clean, kit-wide health clean

- **Depends on:** Tasks 3 and 4
- **Tests:**
  - `T2` (already gated in Task 4, re-run after Task 3 lands to confirm body changes don't break the linter).
  - `T5` — angle-bracket discipline: `python3 -c "body=open('templates/ost.md').read(); body_only=body.split('---',2)[2] if body.count('---')>=2 else body; assert '{{' not in body_only and '__FILL__' not in body_only"` exits 0.
  - `T6` — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0.
  - `T7` / `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0.
- **Approach:**
  - Run each test in sequence. If any fail, fix the underlying placeholder/section/frontmatter issue, then re-run. Hard cap: 5 iterations per the work-loop skill.
  - Common failure modes:
    - **Nested-container-placeholder rejected.** A leaf scalar under `outcome:` or `chosen_opportunity:` was left as a concrete value or a malformed `<>` form. Fix by replacing with `<descriptor>`.
    - **Required key missing.** Linter reports the key; add it under the Handover-specific block.
    - **Section heading drift.** T4's awk comparison fails; restore the exact wording from HANDOVERS §"Handover 2".
  - Diagnostic: if the linter rejects on a key the spec asserts is present, run `python3 -c "import yaml; print(list(yaml.safe_load(open('templates/ost.md').read().split('---',2)[1]).keys()))"` to see what the parser actually sees.
- **Done when:** all five contract tests above exit 0.

### Task 6: REVIEW — adversarial-reviewer against templates/ost.md vs HANDOVERS Handover 2

- **Depends on:** Task 5
- **Tests:**
  - Adversarial-reviewer findings: no Blocking findings remain after iteration.
- **Approach:**
  - Dispatch the `adversarial-reviewer` subagent with this prompt: "Review templates/ost.md against docs/HANDOVERS.md §'Handover 2: Discovery → Validation' and docs/specs/template-authoring-convention/spec.md. Look for drift in required frontmatter keys (top-level and nested under `outcome:` / `chosen_opportunity:`), required-section wording or order, placeholder discipline, identity-pre-fill correctness (`object_type` and `status` only), fabricated OST domain content, and section-body shape (one angle-bracket placeholder per section, no example tree). Return findings numbered with severity Blocking | Suggested | Nit."
  - Iterate inline. Hard cap: 3 review iterations after Task 5. If still red after 3, stop and re-plan; do not grind.
- **Done when:** reviewer returns no Blocking findings; Suggested/Nit findings are addressed or explicitly deferred with a Changelog entry.

### Task 7: CAPTURE — README index, ROADMAP checkbox, status freeze

- **Depends on:** Task 6
- **Tests:**
  - `T8` from spec — `grep -E "^- \[x\] \*\*F3\.2\*\*" ROADMAP.md` returns exactly one line.
  - `T9` from spec — `grep -c "ost.md" templates/_meta/README.md` returns at least 1.
  - Spec `Status:` line is `Shipped (<today>)`; plan `Status:` is `Done`.
- **Approach:**
  - Append a one-line entry for `templates/ost.md` to `templates/_meta/README.md` under its existing index list. Preserve alphabetical ordering if the README uses one; otherwise append at the end. **Mind concurrent appends:** the other nine F3.x workers also touch this file; per the parent spec's §"Rollout", merge conflicts here are expected and trivially mergeable (append-only). If a conflict occurs at merge time, resolve by including both entries.
  - Check off `ROADMAP.md` F3.2: change `- [ ] **F3.2** OST template (\`templates/ost.md\`). **Slug:** \`template-ost\`.` to `- [x] **F3.2** OST template (\`templates/ost.md\`). **Slug:** \`template-ost\`. **Shipped:** <today>.`
  - Freeze spec `Status:` to `Shipped (<YYYY-MM-DD>)`. Freeze plan `Status:` to `Done`.
- **Done when:** T8 and T9 pass; status fields frozen; `bash tools/pre-pr.sh` still exits 0.

## Rollout

- F3.2 unblocks `/draft-ost` / `/generate-ost` (ROADMAP P2.7, P2.9), `/audit-discovery-coherence` (P2.11), and the future `validate-ost.py` hook (F2.7) / `script-ost-validator` (P2.8). None of those consumers need to be edited as part of this spec — they don't exist yet — but their future implementers will read `templates/ost.md` as their input contract.
- `templates/_meta/README.md` gains one row (the index entry); `ROADMAP.md` gains the F3.2 checkbox flip. Both are tiny append-shaped edits.
- `INVENTORY.md`: F3.2 is a template (similar to F3.1, F3.3, …); per the parent spec's rollout note, INVENTORY is not edited for individual templates (no per-template row exists in the existing inventory).
- `AGENTS.md` and `docs/CONVENTIONS.md`: no edits. Both already point readers at the relevant source-of-truth docs.
- No CI changes. `scripts/tests/test_templates_instantiate.py` already auto-discovers `templates/*.md` via glob; the new file is picked up without harness edits.

## Risks

- **Nested-container-placeholder rejection at VERIFY.** If a leaf under `outcome:` or `chosen_opportunity:` is accidentally left as a concrete value (e.g., the HANDOVERS verbatim text leaks a default), the linter rejects. Mitigation: Task 4's approach explicitly verbatim-quotes the HANDOVERS YAML, which already uses angle-bracket placeholders for every leaf; the risk is typo-only. Fix in <5 minutes if it happens.
- **`human_owned_decisions:` (and other overlapping fields) duplication.** The skeleton declares `human_owned_decisions:`, `parent_intent:`, `related_personas:`, `related_problems:` as universal-schema fields with placeholder values; HANDOVERS Handover 2 also lists them. Naively appending both blocks would produce duplicate top-level YAML keys (pyyaml accepts but warns; some validators reject). Mitigation: Task 4 applies the **universal-schema-first dedup convention** (spec §"Boundaries → Always do") — these fields stay in their universal-schema positions carrying HANDOVERS-2-mandated values; they are not restated under the handover-specific block.
- **`templates/_meta/README.md` concurrent appends across the ten F3.x workers.** Parent spec §"Rollout" already addresses this — append-only, mergeable. Worst case: one merge conflict at integration time, trivially resolved.
- **Adversarial-reviewer flags the section-body placeholders as too thin or too prescriptive.** Could oscillate. Mitigation: hard cap at 3 review iterations; if still red, accept the reviewer's wording or defer the disagreement to a Changelog entry and ship.
- **Open Question 1 (the `.json` companion) is reopened during EXECUTE.** If the F3.2 executor decides the `.json` companion belongs in F3.2, the scope expands and the spec drifts. Mitigation: §"Boundaries" → "Ask first" explicitly blocks this without orchestrator sign-off; surface the disagreement to the orchestrator rather than expanding scope unilaterally.

## Changelog

- 2026-05-22 (review-iter-1): Applied adversarial-reviewer fixes — Finding 1 (traceability-key retention decision), Findings 2/3/4/5 (Boundaries clarification, AC wording, Task 3 expansion language, Non-goals scope-defer), cross-cutting dedup convention reversed to universal-schema-first direction.

