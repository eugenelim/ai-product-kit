# Plan: template-assumption-map

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

> **Plan contract.** Implementation strategy for the F3.3 Assumption Map template. The build is a single-file authoring task: copy the canonical skeleton, pre-fill identity, splice the Handover-2.5 contract (frontmatter block + verbatim section headings), verify with the linter, review against the contract, capture in the kit index. Changelog at the bottom.

## Approach

This is a templating job, not a build job. The skeleton at `templates/_meta/template-skeleton.md` is the literal starting point; the work is mechanical substitution and a careful YAML splice. Sequence: `Task 1 → Task 2 → (Task 3 ∥ Task 4) → Task 5 → Task 6 → Task 7`.

The single technical risk is the nested `assumptions:` list-of-maps. The `--check-template` linter mode recurses into list-of-maps and rejects any leaf that is neither a valid placeholder nor a valid concrete value (the parent spec's T8f/T8g/T8h fixtures pin this). The Handover-2.5 YAML quotes lens choices as raw `lens: desirability | viability | feasibility | usability | ethical` — but in the placeholder template that's a bare scalar with `|`s, which the YAML parser treats as a single string and the linter then evaluates against the augmented-placeholder regex (`^[^<>]*(<\S(?:[^>]*\S)?>[^<>]*)+$`). Since the string has no `<` or `>`, it fails the regex *and* isn't a concrete enum match — so it must be rewritten as an angle-bracket placeholder (`<desirability | viability | feasibility | usability | ethical>`). Same pattern for `risk_if_wrong`, `evidence_today`, `test_priority`. The skeleton itself uses this convention (`priority: <Low | Medium | High | Critical>`). Task 4 is where this gets done; Task 5 verifies.

No new top-level dependencies. Existing kit tooling only: `templates/_meta/template-skeleton.md`, `tools/lint-frontmatter.py --check-template`, `scripts/tests/test_templates_instantiate.py`, `tools/pre-pr.sh`.

## Constraints

- Angle-bracket placeholder syntax only. No `{{...}}`, no `__FILL__`. The skeleton enforces this convention; T5 enforces it on F3.3.
- Frontmatter ordering: universal-schema fields in the order they appear in `templates/_meta/template-skeleton.md`; Handover-specific fields in a second block under `# Handover-specific fields` (CONVENTIONS §"Templates → Frontmatter ordering").
- The `assumptions:` list-of-maps must satisfy the linter's nested-container-placeholder rule: every leaf scalar is a valid placeholder (`ATOMIC_PLACEHOLDER` or `AUGMENTED_PLACEHOLDER`) or a valid concrete enum value. No leaf may be a bare `desirability | viability | …`-style scalar — wrap in angle brackets.
- HANDOVERS-2.5 frontmatter keys must appear *verbatim* — including key order within each `assumptions[*]` element matching the contract's order (`id`, `statement`, `lens`, `risk_if_wrong`, `evidence_today`, `test_priority`).
- The five required body sections must appear *verbatim* as H2 headings in the contract-mandated order.
- Must not edit `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `tools/lint-frontmatter.py`, or `scripts/tests/test_templates_instantiate.py`. Editing any of these would mean the parent spec's contract is wrong; surface that as an open question instead.
- Must not write `context/frameworks/assumption-tests.md`. F4.4 owns that file.
- `templates/_meta/README.md` is a shared write target with seven sibling F3 workers. The CAPTURE-phase append must happen at parent-orchestrator merge time (per parent spec's "Sequential README.md appends" rollout note), not inside the F3.3 worker's loop. Task 7's append is therefore an *intent recorded in the plan*; the orchestrator (parent task list item #9) executes the merge.

## Construction tests

Cross-cutting only. Per-task tests are inline under each task.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 after the template file lands. Mirrors the parent spec's pre-pr-clean construction test.

## Tasks

### Task 1: Skeleton copied to `templates/assumption-map.md`

- **Depends on:** none
- **Tests:**
  - `T1` from spec — `test -f templates/assumption-map.md` exits 0.
  - No-clobber sanity: pre-task, `test -f templates/assumption-map.md` exits non-zero (file did not exist before this loop). If it does, stop and reconcile.
- **Approach:**
  - `cp templates/_meta/template-skeleton.md templates/assumption-map.md` (or equivalent Write).
  - At this point the file is a literal copy of the skeleton — verbatim, including all placeholders.
- **Done when:** T1 passes.

### Task 2: Identity pre-filled (universal block + H1)

- **Depends on:** Task 1
- **Tests:**
  - `grep -c '^object_type: Assumption Map$' templates/assumption-map.md` returns exactly 1 (in the universal block).
  - `grep -c '^status: Draft' templates/assumption-map.md` returns exactly 1 (pre-fill confirmed).
  - `grep -c '^# Assumption Map$' templates/assumption-map.md` returns exactly 1 (H1 set).
- **Approach:**
  - Replace skeleton's `object_type: <pre-filled per template — e.g., Strategic Intent>` with `object_type: Assumption Map`.
  - Confirm `status: Draft   # product-artifact track entry state; see CONVENTIONS.md §"Lifecycle states"` is left intact (it's already pre-filled in the skeleton).
  - Replace H1 placeholder `# <Artifact name>` with `# Assumption Map`.
  - Update the H1's blockquote stub line to: `> Assumption Map for the chosen Opportunity. Gates Handover 2.5 (Discovery → Assumption Map) per docs/HANDOVERS.md.`
- **Done when:** all three greps return exactly 1.

### Task 3: Universal block tightened (delete inapplicable traceability fields)

- **Depends on:** Task 2
- **Tests:**
  - `grep -cE '^(parent_learning|parent_vision|parent_initiative):' templates/assumption-map.md` returns 0 (deleted — not applicable to an Assumption Map, which is upstream of Learning/Vision/Initiative).
  - `grep -c '^parent_intent:' templates/assumption-map.md` returns ≥ 1 (kept — applicable; restated for traceability per HANDOVERS-2.5).
  - `grep -c '^parent_opportunity:' templates/assumption-map.md` returns ≥ 1 (kept — required by HANDOVERS-2.5).
- **Approach:**
  - In the universal block's traceability section, delete the three lines `parent_learning: <…>`, `parent_vision: <…>`, `parent_initiative: <…>`. The skeleton comment `# Traceability (per HANDOVERS.md row for this handover; delete fields that don't apply)` explicitly authorizes this.
  - Leave `parent_intent` and `parent_opportunity` (both applicable to Handover 2.5).
  - Leave `related_problems`, `related_personas`, `related_kpis` — these are universally applicable traceability hooks and the Assumption Map will commonly reference them.
- **Done when:** the three greps above return their expected counts.

### Task 4: Handover-2.5 frontmatter block appended (with nested-placeholder discipline)

- **Depends on:** Task 2 (independent of Task 3 in YAML mechanics, but both edit the same frontmatter region — sequence them after the universal-block work)
- **Tests:**
  - `T3` from spec — all six top-level Handover-2.5 keys present in parsed YAML: `object_type`, `parent_opportunity`, `parent_intent`, `assumptions`, `riskiest_assumption`, `human_owned_decisions`. The first four were already covered by Tasks 2–3 (universal block); this task adds `assumptions` and `riskiest_assumption` to the handover-specific block, overrides `parent_opportunity`'s value from `<discovery opportunity id>` to `<OPP-NNN>`, and overrides `human_owned_decisions`'s generic placeholder with the two HANDOVERS-2.5 contract-literal bullets.
  - `T3b` from spec — every `assumptions[*]` element carries all six keys (`id`, `statement`, `lens`, `risk_if_wrong`, `evidence_today`, `test_priority`).
  - **Nested-placeholder shape check** (anticipates T2): `python3 tools/lint-frontmatter.py --check-template templates/assumption-map.md` exits 0 after this task. If it fails with a nested-container-placeholder error, the `assumptions[*]` enum fields were not wrapped in angle brackets — fix and re-run.
  - Universal-block overrides applied: `grep -c '^parent_opportunity: <OPP-NNN>$' templates/assumption-map.md` returns exactly 1; `grep -A2 '^human_owned_decisions:' templates/assumption-map.md` shows `  - Selection of the riskiest assumption to test next` and `  - Acceptance of assumptions marked "accept-as-bet"`.
- **Approach:**
  - Locate the skeleton's `# Handover-specific fields (per docs/HANDOVERS.md row for this handover)` comment. Append the two handover-specific keys immediately below it, **before** the closing `---`:

    ```yaml
    assumptions:
      - id: <ASM-NNN>
        statement: <one sentence>
        lens: <desirability | viability | feasibility | usability | ethical>
        risk_if_wrong: <Low | Medium | High | Critical>
        evidence_today: <Strong | Moderate | Weak | None>
        test_priority: <1 | 2 | 3 | ...>
    riskiest_assumption: <ASM-NNN>
    ```

  - Note 1: `object_type: Assumption Map` is already pre-filled in the universal block (Task 2); HANDOVERS-2.5 lists it under "additions on top of the universal schema" but the kit's universal block already owns the key, so it does not need to be duplicated in the Handover-specific block. Duplicating it would produce a YAML last-write-wins, which is harmless but noisy — omit it.
  - Note 2: `parent_opportunity`, `parent_intent`, and `human_owned_decisions` *also* sit in the universal-block traceability/ownership regions. Per CONVENTIONS §"Frontmatter ordering", universal-schema fields appear in the universal block. Single-source rule: each key appears in exactly one block. Therefore:
    - `parent_opportunity` lives in the universal block; **override its placeholder value from the skeleton's `<discovery opportunity id>` to HANDOVERS-2.5's `<OPP-NNN>`** for contract fidelity.
    - `parent_intent` lives in the universal block; value `<strategic intent slug>` (matches both the skeleton and HANDOVERS-2.5).
    - `human_owned_decisions` lives in the universal block; **replace the skeleton's generic placeholder list item with the two HANDOVERS-2.5 contract-literal bullets** (`Selection of the riskiest assumption to test next`, `Acceptance of assumptions marked "accept-as-bet"`).
    - The Handover-specific block under `# Handover-specific fields` therefore contains exactly two keys: `assumptions` and `riskiest_assumption`. That's the only delta vs the skeleton's frontmatter shape.
  - **Critical placeholder shapes for the nested leaves:**
    - `id: <ASM-NNN>` — atomic placeholder, valid.
    - `statement: <one sentence>` — atomic placeholder, valid.
    - `lens: <desirability | viability | feasibility | usability | ethical>` — atomic placeholder (entire string between `<` and `>`), valid. **Do NOT write `lens: desirability | viability | feasibility | usability | ethical` (no brackets) — that's a bare scalar with no `<>` that fails the augmented-placeholder regex and isn't a concrete enum value.**
    - `risk_if_wrong: <Low | Medium | High | Critical>` — same shape as the skeleton's `priority` and `risk_level` pre-fills.
    - `evidence_today: <Strong | Moderate | Weak | None>` — same shape.
    - `test_priority: <1 | 2 | 3 | ...>` — same shape (HANDOVERS-2.5 writes "1 | 2 | 3 | …"; the ellipsis becomes "..." inside the brackets to avoid non-ASCII drift, but either character is valid under the regex).
- **Done when:** T3, T3b pass; `--check-template` exits 0; universal-block override greps return their expected counts.

### Task 5: Required body sections appended verbatim

- **Depends on:** Task 1 (body editing is independent of frontmatter; serialize after Task 4 only to keep verification batched)
- **Tests:**
  - `T4` from spec — five H2 headings present in contract-mandated order.
  - `grep -c '^## The chosen opportunity$' templates/assumption-map.md` returns exactly 1; same for the other four headings.
  - Section bodies are non-empty (each H2 followed by at least one non-blank line before the next H2 or EOF).
- **Approach:**
  - Replace the skeleton's three placeholder section headings (`## <Required section 1 from HANDOVERS.md>`, `## <Required section 2 from HANDOVERS.md>`, `## <Required section N from HANDOVERS.md>`) with the five HANDOVERS-2.5 required sections, in order:
    1. `## The chosen opportunity` — body: "<One-paragraph restatement of the chosen Opportunity from Handover 2; link to the OST node at `discovery/trees/<slug>.md#<OPP-NNN>`.>"
    2. `## Assumptions, by lens` — body: "<Every assumption underneath the opportunity, classified into the five-lens taxonomy (desirability / viability / feasibility / usability / ethical). Cite `context/frameworks/assumption-tests.md` *(planned — ROADMAP F4.4)* for definitions; until that framework ships, link to ontology Domain C entries for the named lenses.>"
    3. `## Risk-vs-evidence ranking` — body: "<Each assumption plotted on (risk_if_wrong × evidence_today). The riskiest under-evidenced assumption is the next test target.>"
    4. `## The riskiest assumption` — body: "<Restated; why it earned the rank; what we'd lose if it's wrong.>"
    5. `## Accepted bets` — body: "<Assumptions the team explicitly chooses not to test (with rationale). These propagate to the Vision artifact's `open_assumptions:` block as tier `accept-as-bet`.>"
  - The skeleton's `## Optional sections` block stays as-is (instruction-only; kit users delete or fill).
- **Done when:** T4 passes; all five headings present in order; each section has placeholder body content.

### Task 6: VERIFY — full contract-test suite green

- **Depends on:** Tasks 2, 3, 4, 5 (frontmatter and body both in their final shape)
- **Tests:**
  - All of T1, T2, T3, T3b, T4, T5, T6, T7 from spec.
  - `pre-pr-clean` (construction test).
- **Approach:**
  - Run each spec contract test in order; collect failures.
  - For any failure, fix in place and re-run. If the same gate fails twice with the same fingerprint, stop and surface — the spec or the linter is wrong.
  - T2's nested-container rule is the highest-risk gate. If it fails, the failure message will name the offending leaf path (e.g., `assumptions[0].lens`); fix the placeholder shape.
  - T6 walks the `templates/` directory via the existing pytest. The new file is auto-discovered by the `*.md` glob; no test code change. If the test fails on a *different* template, that's a sibling-worker bug, not F3.3's — surface as a finding for the aggregate-and-commit step (parent task #9).
- **Done when:** all listed tests exit 0.

### Task 7: REVIEW — adversarial review against HANDOVERS-2.5 and parent spec

- **Depends on:** Task 6
- **Tests:**
  - Adversarial-reviewer returns clean (no severity-high findings).
  - If findings, iterate; hard cap 5 REVIEW iterations per work-loop discipline. After 5, stop and re-plan.
- **Approach:**
  - Dispatch `adversarial-reviewer` (the default reviewer per AGENTS.md §"Workflow") against the produced `templates/assumption-map.md` with prompt: "Review templates/assumption-map.md against (a) docs/HANDOVERS.md §'Handover 2.5: Discovery → Assumption Map' and (b) docs/specs/template-authoring-convention/spec.md §'Convention-text contract' and §'Handover-2.5 text contract'. Look for: missing required frontmatter keys (incl. nested `assumptions[*]` keys), drift on section names or order, malformed angle-bracket placeholders (especially nested ones), scope creep into lens-taxonomy definitions (F4.4 territory), divergence from skeleton frontmatter ordering."
  - Apply fixes; re-run Task 6.
- **Done when:** reviewer returns clean.

### Task 8: CAPTURE — index entry + ROADMAP checkoff + spec/plan freeze intent

- **Depends on:** Task 7
- **Tests:**
  - `T8`, `T9` from spec.
- **Approach:**
  - Append a one-line entry to `templates/_meta/README.md` under the index list (e.g., `- templates/assumption-map.md — Assumption Map (Handover 2.5, Discovery → Assumption Map)`). Per the parent spec's rollout note, this is "sequential append" — coordinate via the parent orchestrator (task #9 of the parent task list); if a sibling worker has appended in parallel, resolve the trivially-mergeable conflict at merge time.
  - Mark ROADMAP F3.3 with `- [x]` and add a `Shipped: <YYYY-MM-DD>` suffix at the orchestrator's merge step.
  - Update this plan's Status to `Done` and the spec's Status to `Shipped` (with date) only at the same merge step.
- **Done when:** T8 and T9 pass.

## Rollout

- **Downstream:** ROADMAP P3.11 `/audit-assumption-coverage` will consume `templates/assumption-map.md` indirectly (it detects missing/incomplete instances under `validation/assumption-maps/`). Shipping F3.3 unblocks meaningful adoption; the audit itself is still planned-not-built.
- **Sibling templates:** F3.1, F3.2, F3.4–F3.10 are in flight as parallel fan-out workers. They share `templates/_meta/README.md` as a write target; trivial merge conflicts on the README index are acceptable per the parent spec's rollout note.
- **Docs / INVENTORY:** no INVENTORY row needed (templates are infrastructure, mirroring how the parent spec's skeleton has no INVENTORY row). No AGENTS.md or CLAUDE.md update needed.
- **`/draft-assumption-map`:** future command (not in F3). When it lands, it will reference this template path.

## Risks

- **Nested-container-placeholder rule trips on `assumptions[*]` enum fields.** Mitigation: Task 4's "Critical placeholder shapes" subsection. Verification at Task 6 (T2 catches it mechanically). Worst case: linter rejects, error message names the leaf, fix is one line.
- **Confusion about block placement of `parent_opportunity` / `parent_intent` / `human_owned_decisions`.** All three appear in HANDOVERS-2.5 *and* in the universal-schema block. Mitigation: Task 4 resolves this explicitly — these keys live in the universal block (with HANDOVERS-2.5-mandated values), not duplicated into the Handover-specific block. The acceptance criterion's "carries the key" predicate tests parsed-YAML presence, not block location.
- **`templates/_meta/README.md` race with sibling F3 workers.** Mitigation: deferred to the orchestrator's merge step (parent task #9). F3.3's plan records the intended index entry; the orchestrator applies it during sequential merge.
- **A sibling worker's template introduces a `--check-template` regression that breaks T6.** Mitigation: T6 runs over all templates, so a sibling's bug shows up in F3.3's loop. If T6 fails on a *different* template, surface as a finding for the aggregate-and-commit step and don't grind on F3.3.
- **Lens definitions get inlined into §"Assumptions, by lens" by an over-eager fill.** Mitigation: Task 5's body text is bounded to the HANDOVERS-2.5 instruction text plus the F4.4 citation. The "Never do" boundary explicitly forbids authoring lens definitions in this template.

## Changelog

- 2026-05-22 (review-iter-1): Applied adversarial-reviewer fixes — added T3c block-placement assertion, OQ-A ellipsis resolution, cross-references owned-fields correction, README.md merge-protocol open_assumption entry, vague-language rewording, T4b H1 blockquote test, dedup convention bullet in §Boundaries.
