# Spec: template-kit-spec-frontmatter

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template + docs reconciliation
- **Serves kit phase:** Meta (kit infrastructure — the contract for what a spec carries)
- **Constrained by:** ROADMAP F0.11; `docs/specs/reconcile-existing-components/spec.md` Open Question 5; AGENTS.md §"Human-vs-AI responsibility" ("Every artifact carries explicit frontmatter"); `docs/CONVENTIONS.md` §"Universal metadata schema"; `context/frameworks/ontology.md` §"When the ontology is wrong" (don't invent ad-hoc types).

> **Spec contract.** Resolves the contradiction between AGENTS.md's "every artifact" frontmatter claim and the fact that `docs/_templates/spec.md` declares its metadata as a markdown bullet block (not YAML frontmatter) and is not walked by `tools/lint-frontmatter.py`. Picks **option (b)** from the ROADMAP F0.11 description: document the spec template as an **explicit exemption** from the universal-metadata schema, and rewrite the universalist claims so they match reality.

## Objective

Reconcile three documents (AGENTS.md, `.claude/CLAUDE.md`, `docs/CONVENTIONS.md`) and one template (`docs/_templates/spec.md`) so that:

1. The universal-metadata schema is explicitly scoped to **product artifacts** under the PM phase directories (`strategy/`, `discovery/`, `validation/`, `delivery/`, `market/`), matching what `tools/lint-frontmatter.py` actually enforces.
2. Kit-meta scaffolding (specs, plans, state) is named as exempt, with the existing markdown-bullet header block in the spec template explicitly designated as the spec's metadata surface.
3. The spec template itself carries a one-line note that points the reader to the exemption rationale in CONVENTIONS.md.

This is a **docs reconciliation** spec, not a code spec. No script changes. No template body rewrites beyond the one-line exemption note.

## Why now

F0.11 is the lowest-numbered unchecked Foundation item. Every spec scaffolded from `tools/new-spec.sh` inherits the unresolved contradiction. Resolving it now (cheap, docs-only) prevents the contradiction from compounding as Foundation 3 ships ten more templates. Choosing option (b) over option (a) avoids:
- Inventing a `kit-spec` ontology type, which the ontology's own §"When the ontology is wrong" explicitly warns against
- Back-filling YAML frontmatter into 16 existing specs that would never be linted (lint-frontmatter doesn't walk `docs/specs/`)
- Conflating the kit-build lifecycle (Draft → Implementing → Shipped → Frozen) with the product-artifact lifecycle

## Inputs and outputs

**Inputs.** Current text of:
- `AGENTS.md` line 91 (the "Every artifact carries explicit frontmatter" sentence + YAML example that follows)
- `.claude/CLAUDE.md` line 40 ("Every artifact declares its `object_type:` …") and line 44 ("Every artifact declares `human_owned_decisions:` …")
- `README.md` lines 11, 134, 135 (three "Every artifact …" sentences in kit-facing prose)
- `CONTRIBUTING.md` line 35 (the "Every artifact declares `object_type:`" sentence)
- `docs/CHARTER.md` line 36 (the "Every artifact declares its `object_type:` and uses the universal metadata schema" sentence)
- `docs/CONVENTIONS.md` line 7 (the "Markdown with YAML frontmatter for everything that isn't code" sentence — broader universalist claim), line 14 (the `## Universal metadata schema` section opener "Every kit artifact carries the frontmatter block below"), the YAML example-block comment ("Human-vs-AI ownership (every artifact must declare this)"), and §"Specs and Plans" (target for the new exemption sub-section)
- `docs/_templates/spec.md` (the existing bullet-block header)

**Out of scope (do not touch).**
- `AGENTS.md` line 67 ("Every artifact declares *how* it'll be verified") — different claim (verification mode, not frontmatter), and verification-mode declaration applies to kit-meta specs too.
- `templates/CLAUDE.global.md` line 27 — this template ships into kit-user projects, so its "every artifact" claim is correctly scoped to product artifacts already.
- `context/frameworks/ontology.md` line 221 — describes Domain H's location and is already implicitly product-scoped.
- `docs/inspiration/*` — imported source material.
- `tools/new-spec.sh` — scaffolder already writes the template verbatim with no frontmatter insertion step; behaviorally correct for option (b).

**Outputs.**
- `AGENTS.md`: line 91 narrowed to "Every product artifact carries explicit frontmatter" + one-sentence exemption pointer to `docs/CONVENTIONS.md` §"Specs and Plans".
- `.claude/CLAUDE.md`: lines 40 and 44 narrowed identically; one-sentence exemption pointer near §"Object types" or §"Human-vs-AI ownership".
- `README.md`: lines 11, 134, 135 narrowed to "Every product artifact" (each — minimal-word change, no exemption-pointer paragraph; readers needing the rationale follow the CONVENTIONS.md link already present elsewhere in README).
- `CONTRIBUTING.md`: line 35 narrowed to "Every product artifact declares `object_type:`" with a parenthetical "(kit-meta scaffolding is exempt — see CONVENTIONS.md §"Specs and Plans")".
- `docs/CHARTER.md`: line 36 narrowed to "Every product artifact declares its `object_type:` and uses the universal metadata schema" + the same parenthetical.
- `docs/CONVENTIONS.md`: line 7 narrowed to "Markdown with YAML frontmatter for every product artifact that isn't code" + parenthetical; §"Specs and Plans" gains a new sub-section "Exempt from the universal metadata schema" with the three-bullet rationale (drafted below in this spec — see "Exemption-text contract").
- `docs/_templates/spec.md`: a one-line italic note added under the existing bullet block (NOT new frontmatter) referencing the CONVENTIONS exemption.

A reader of this section should be able to construct the diff without reading anything else.

## Exemption-text contract

The new §"Exempt from the universal metadata schema" sub-section in CONVENTIONS.md ships with this exact content (so the rationale is reviewed before execution, not authored during it):

> ### Exempt from the universal metadata schema
>
> Specs (`docs/specs/<feature>/spec.md`), plans (`plan.md`), and state files (`state.json`) do not carry the universal-metadata YAML frontmatter. The exemption rests on three facts:
>
> - Specs use the **kit-build lifecycle track** (`Draft → In Review → Approved → Implementing → Shipped → Frozen`), which is separate from the product-artifact track and has different downstream consumers.
> - The **markdown bullet block under the spec's H1** (Status, Plan, State, Component type, Serves kit phase, Constrained by) IS the spec's metadata surface. It carries the same information the universal schema does for product artifacts.
> - `tools/lint-frontmatter.py` walks only `PHASE_DIRS = ["strategy", "discovery", "validation", "delivery", "market"]`. Universal-schema frontmatter on a spec under `docs/specs/` would never be enforced.
>
> Adding `kit-spec` as an ontology type was considered and rejected: `context/frameworks/ontology.md` §"When the ontology is wrong" warns against ad-hoc additions, and Domain I composites are explicitly phase-boundary handovers — not kit-build scaffolding.

## Boundaries

### Always do
- Keep the spec template's existing bullet-block header **unchanged in structure**. Only add the one-line exemption note.
- Phrase the exemption as "this header block IS the spec's metadata" — not "specs have no metadata."
- Mirror the narrowing language across all three documents (AGENTS.md, .claude/CLAUDE.md, CONVENTIONS.md) so they don't drift again.

### Ask first
- Editing the spec template's required sections (Objective, Inputs and outputs, Boundaries, etc.). Out of scope for F0.11.
- Touching `tools/lint-frontmatter.py` to start walking `docs/specs/`. That would be an enforcement change, not a docs reconciliation. Defer.

### Never do
- Add a `kit-spec` (or `Kit Spec`) entry to the ontology. Domain I is for **phase-boundary handovers**; specs are kit-build scaffolding. The ontology explicitly warns against ad-hoc additions.
- Back-fill YAML frontmatter into existing `docs/specs/<slug>/spec.md` files.
- Amend `tools/check-done.py` or `tools/pre-pr.sh`.

## Verification mode

- **Goal-based check.** Greps must return the expected matches; lint-frontmatter and pre-pr must still exit 0 against the kit.

## Contract tests

Verifications (each is one shell line). Tests come in pairs: a positive assertion that the narrowed phrase was added AND a negative assertion that the original unnarrowed phrase was removed.

- `T1a` — `grep -ci "Every product artifact carries explicit frontmatter" AGENTS.md` returns ≥1.
- `T1b` — `grep -c "Every artifact carries explicit frontmatter" AGENTS.md` returns 0. (Removal verified.)
- `T2` — `grep -n "Exempt from the universal metadata schema" docs/CONVENTIONS.md` returns exactly 1 hit. This is the new sub-section heading.
- `T3` — `grep -nE "exempt from the universal" docs/_templates/spec.md` returns exactly 1 hit (the new one-line note).
- `T4a` — `grep -ci "every product artifact" .claude/CLAUDE.md` returns ≥2 hits (one per narrowed line, lines 40 + 44).
- `T4b` — `grep -c "Every artifact declares its \`object_type:\` per \`context/frameworks/ontology.md\`" .claude/CLAUDE.md` returns 0. (The exact original line 40 sentence is gone.)
- `T5a` — `grep -ci "every product artifact" README.md` returns ≥3.
- `T5b` — `grep -c "Every artifact declares its \`object_type:\` and links into the traceability chain" README.md` returns 0. (Line 134 narrowed.)
- `T6` — `grep -ci "every product artifact" CONTRIBUTING.md` returns ≥1.
- `T7` — `grep -ci "every product artifact" docs/CHARTER.md` returns ≥1.
- `T8` — `grep -c "Markdown with YAML frontmatter for everything that isn't code" docs/CONVENTIONS.md` returns 0. (Line 7 narrowed.)
- `T8b` — `grep -c "Every kit artifact carries the frontmatter block" docs/CONVENTIONS.md` returns 0. (Line 14 — `## Universal metadata schema` section opener — narrowed to "Every product artifact carries the frontmatter block …".)
- `T8c` — `grep -c "Human-vs-AI ownership (every artifact must declare this)" docs/CONVENTIONS.md` returns 0. (YAML example-block comment narrowed.)
- `T9` — `python3 tools/lint-frontmatter.py --all` exits 0 (no regression; the linter's behavior is unchanged).
- `T10` — `bash tools/pre-pr.sh` exits 0 (kit-wide health unchanged).
- `T11` — `grep -ncE '^\|\s*([Kk]it[ -][Ss]pec)\s*\|' context/frameworks/ontology.md` returns 0 hits. (Precise check: matches an ontology-type *table row* declaring `Kit Spec` / `kit-spec` / `Kit-Spec` etc. Avoids false positives against the pre-existing prose phrase "kit-specific" in §I's heading.)

## Non-goals

- Adding any new lint rule. F0.12 is the linter-change ROADMAP slot.
- Changing how `tools/new-spec.sh` scaffolds (no per-slug substitution beyond what's there).
- Rewriting CONVENTIONS.md's universal-metadata block. We narrow its scope by addition, not by deletion.
- Reconciling AGENTS.md's "every artifact" claim everywhere it appears in inspiration docs (`docs/inspiration/*`). Those are imported source material.
- Adding a `kit-spec.md` template under `docs/_templates/`. The existing template is the kit-spec template.

## Open questions

1. **Should the narrowing language be "every product artifact" or "every PM artifact"?** Lean: "product artifact" because CONVENTIONS.md §"Lifecycle states" already uses "product-artifact track" as the canonical phrase. _Resolved here: use "product artifact."_

2. **Should the spec template's exemption note live above or below the existing bullet block?** Lean: below — the bullets are the contract; the exemption is the meta-commentary. _Resolved here: below._

## Acceptance criteria

- [ ] AGENTS.md narrows the line-91 frontmatter claim to "Every product artifact" + names the kit-meta exemption.
- [ ] `.claude/CLAUDE.md` narrows lines 40 and 44 identically.
- [ ] `README.md` lines 11, 134, 135 narrowed.
- [ ] `CONTRIBUTING.md` line 35 narrowed with parenthetical exemption pointer.
- [ ] `docs/CHARTER.md` line 36 narrowed with parenthetical exemption pointer.
- [ ] `docs/CONVENTIONS.md` line 7 narrowed AND §"Specs and Plans" gains the exempt sub-section with the exact text from "Exemption-text contract" above.
- [ ] `docs/_templates/spec.md` carries a one-line exemption note under the existing bullet block.
- [ ] Contract tests T1–T11 all pass.
- [ ] No new ontology type added; no template structure changed beyond the one-line note.
- [ ] `ROADMAP.md` F0.11 marked checked with `Shipped: 2026-05-21` in the CAPTURE phase (per work-loop SKILL §5.4).

## Cross-references

- **Consumed by:** every future spec scaffolded from `docs/_templates/spec.md`; the work-loop SKILL §1.1 (which references the template).
- **Consumes:** nothing.
- **Frontmatter fields owned:** none. The whole point is that specs don't own universal-schema frontmatter.
- **Ontology object types touched:** none.
