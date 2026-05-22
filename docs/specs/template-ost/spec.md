# Spec: template-ost

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template
- **Serves kit phase:** Discovery
- **Constrained by:** `docs/specs/template-authoring-convention/spec.md` (parent authoring convention — placeholder syntax, frontmatter ordering, linter contract, skeleton source); `docs/HANDOVERS.md` §"Handover 2: Discovery → Validation" (required frontmatter + required sections, quoted verbatim); `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" + §"Universal metadata schema" + §"Lifecycle states" + §"Specs and Plans"; `context/frameworks/ontology.md` (Opportunity Solution Tree row in Domain I composite; Domain C atomic types Outcome, Opportunity, Job to Be Done, Problem, Evidence, Insight); ROADMAP F3.2.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships the literal file `templates/ost.md` — a single-file template a kit user copies to produce a real `discovery/trees/<slug>.md` Opportunity Solution Tree under the Discovery phase. The template gates Handover 2 (Discovery → Validation): when filled, the resulting artifact is the input contract Validation reads. The template's body is shape-only (no fabricated domain content); its frontmatter pre-fills only the template's identity (`object_type: Opportunity Solution Tree`, `status: Draft`); every other value is an angle-bracket placeholder. Conformance is mechanically verifiable via `tools/lint-frontmatter.py --check-template templates/ost.md` and the pytest harness `scripts/tests/test_templates_instantiate.py`.

## Objective

`templates/ost.md` is one of the ten F3.x templates fanned out from `template-authoring-convention`. It encodes the Handover 2 contract in `docs/HANDOVERS.md` as a copy-paste starting file: a kit user filling it in produces an OST artifact whose frontmatter and section structure satisfy the Discovery → Validation gate without re-reading HANDOVERS.md. The template's identity (`object_type`, `status: Draft`) is pre-filled; the user supplies the rest. No `templates/ost.md` exists in the repo today.

## Why now

Handover 2 is the load-bearing artifact for the Discovery phase. Until `templates/ost.md` ships, kit users either re-read `docs/HANDOVERS.md` and reinvent the shape per-OST (drift) or skip the contract entirely (operating-model failure mode #4: "interviews → let's build it" with no opportunity space). F3.2 is also the prerequisite for the future `/draft-ost` command (ROADMAP P2.7 / P2.9) and `/audit-discovery-coherence` (ROADMAP P2.11) — both consume an OST instance whose shape this template defines. F3.2 is parallel-safe with the other nine F3.x rows because the parent `template-authoring-convention` spec ships the skeleton, the linter mode, and the contract test; this spec only specializes them for the OST case.

## Inputs and outputs

**Inputs.**

- `templates/_meta/template-skeleton.md` — the canonical starting file every F3.x template copies (per `template-authoring-convention` spec §"Skeleton-text contract").
- `docs/HANDOVERS.md` §"Handover 2: Discovery → Validation" — the source of the required frontmatter and required sections, quoted verbatim below.
- `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" — the authoring convention (placeholder syntax, frontmatter ordering, pre-fill rules, linter contract).
- `context/frameworks/ontology.md` — confirms `Opportunity Solution Tree` is a Domain I composite type and is the correct value for the `object_type:` field; lists the atomic Domain C types (Outcome, Opportunity, Job to Be Done, Problem, Evidence, Insight) the artifact's body references.
- `tools/lint-frontmatter.py` (`--check-template` mode) — the validator the template must pass.
- `scripts/tests/test_templates_instantiate.py` — the pytest harness that walks `templates/*.md` and runs `--check-template` on each.

**Outputs.**

1. `templates/ost.md` — a single-file template with:
   - **Pre-filled identity fields** (the template's identity per the authoring convention §"Pre-fill vs placeholder"):
     - `object_type: Opportunity Solution Tree`
     - `status: Draft`
   - **Universal-metadata schema fields** in the order defined by `docs/CONVENTIONS.md` §"Universal metadata schema" (matching the skeleton's order). All non-identity values are angle-bracket placeholders.
   - **Handover-2-specific frontmatter** appended under the `# Handover-specific fields` YAML-comment block, quoted verbatim from `docs/HANDOVERS.md` §"Handover 2":

     ```yaml
     object_type: Opportunity Solution Tree
     parent_intent: <strategic intent slug>
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
     related_personas: [<persona ids>]
     related_problems: [<problem ids>]
     human_owned_decisions:
       - Selection of the chosen opportunity
       - What opportunities to explicitly exclude from the tree
     ```

     The `object_type:` line in this block is the same identity-pre-fill named above; the line appears once (in the universal-schema block per ordering) and is not duplicated in the handover-specific block. The two nested mappings (`outcome:` and `chosen_opportunity:`) require the **nested-container-placeholder** rule from the parent spec's §"Outputs" item 4 — every leaf scalar inside the nested mapping is itself an angle-bracket placeholder, which makes the whole mapping acceptable under `--check-template`.

     **Skeleton traceability-key retention.** The `templates/_meta/template-skeleton.md` universal-schema block carries traceability placeholders (`parent_intent`, `parent_opportunity`, `parent_learning`, `parent_vision`, `parent_initiative`, `related_personas`, `related_problems`, `related_kpis`). For `templates/ost.md` the retention call is: **keep** `parent_intent` (Handover 2 requires it), `related_personas` (Handover 2 requires it), `related_problems` (Handover 2 requires it), and `related_kpis` (universal-schema, useful for OST instances even though Handover 2 does not require it); **drop** `parent_opportunity`, `parent_learning`, `parent_vision`, `parent_initiative` from the skeleton (an OST is the Discovery phase's starting artifact — none of those upstream artifacts pre-exist when an OST is drafted). T3 asserts only the retained set; T2 (the `--check-template` linter) remains the authoritative completeness gate.

   - **Required body sections**, in this exact order, quoted verbatim from `docs/HANDOVERS.md` §"Handover 2" — required sections list:

     1. **The outcome** — measurable, tied to the parent intent's coherent action
     2. **Opportunity space** — all opportunities surfaced, as a tree
     3. **The chosen one** — why this, why now, what we'd give up by choosing it
     4. **Source opportunities** — interview-level evidence under each tree node
     5. **Excluded** — opportunities considered and explicitly excluded (and why)

     Each section heading appears as a level-2 Markdown heading; each section body is a single angle-bracket placeholder describing what to write (one sentence per section). The template body is shape-only — no fabricated opportunity content, no example node tree.

   - A `## Optional sections` heading at the bottom per the authoring convention §"Required vs optional sections," with the standard "delete if none apply" guidance. No specific optional sections are enumerated by Handover 2; this section is present as the convention requires but lists no entries.

2. **No other files.** `templates/ost.md` is a single file (not a folder). The sibling structured `discovery/trees/<slug>.json` that HANDOVERS.md mentions for the OST validator is **explicitly out of scope** for this spec (see §"Non-goals" and §"Open questions").

A reader of this section should be able to write the template's frontmatter and section headings without reading anything else.

## Boundaries

### Always do

- Quote the five Handover 2 required sections from `docs/HANDOVERS.md` verbatim, in the order listed (Outcome → Opportunity space → Chosen one → Source opportunities → Excluded). The template is a re-projection of HANDOVERS, not a parallel source of truth.
- Quote the Handover 2 required-frontmatter YAML verbatim, preserving nested-mapping structure for `outcome:` (five keys: `id`, `metric`, `current`, `target`, `measurement`) and `chosen_opportunity:` (two keys: `id`, `rationale`).
- Pre-fill `object_type: Opportunity Solution Tree` and `status: Draft`. Every other field is an angle-bracket placeholder per `docs/CONVENTIONS.md` §"Templates" → "Pre-fill vs placeholder".
- Use the angle-bracket placeholder syntax exclusively. Forms like `<one sentence>`, `<YYYY-MM-DD>`, `<OPP-NNN>` are valid; `<>`, `< >`, `{{...}}`, `__FILL__` are not.
- Copy from `templates/_meta/template-skeleton.md` as the starting file; preserve the universal-schema field order it defines.
- Run `tools/lint-frontmatter.py --check-template templates/ost.md` and `python3 -m pytest scripts/tests/test_templates_instantiate.py` as the verification gates.
- **Dedup convention (universal-schema first).** When HANDOVERS-2 fields overlap with the universal-metadata schema (e.g., `human_owned_decisions:`, `object_type:`), the field appears once — in its universal-schema position — carrying the HANDOVERS-2-mandated value. The universal-schema placeholder is deleted in the same edit. The handover-specific block carries only fields not present in the universal schema (`parent_intent`, `outcome`, `opportunity_count`, `chosen_opportunity`, `related_personas`, `related_problems`). This preserves the parent spec's "universal-schema first, handover-specific second" frontmatter-ordering rule.

### Ask first

- Adding any frontmatter field not present in `docs/CONVENTIONS.md` §"Universal metadata schema" or `docs/HANDOVERS.md` §"Handover 2". The template is downstream of those two docs.
- Authoring an example OST body (a worked tree, sample opportunities, illustrative evidence). The convention is shape-only; example content belongs in a `docs/guides/` how-to, not in the template file.
- Extending scope to ship the sibling structured `discovery/trees/<slug>.json` file. That artifact serves the OST validator (ROADMAP P2.8) and is a separate ROADMAP row, not F3.2.

### Never do

- Invent Opportunity Solution Tree domain content (specific outcomes, opportunities, jobs-to-be-done, evidence quotes, insights). The template body is angle-bracket placeholders only.
- Add an ontology type for "OST template" or "Kit Template." Domain I is phase-boundary handover composites; templates are kit-build scaffolding. Identical reasoning to F0.11 (`template-kit-spec-frontmatter`) and the parent spec's "Never do" section.
- Walk `templates/` from `lint-frontmatter.py`'s default mode. Out of scope; mode separation is the safety property the parent spec ships.
- Modify shared kit infrastructure during this spec's execution: `templates/_meta/README.md` is the only shared file this spec's CAPTURE phase appends to, and it's append-only (one line). `tools/lint-frontmatter.py`, `scripts/tests/test_templates_instantiate.py`, `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, and the other nine F3.x specs are not touched.
- Pre-fill any user-supplied value (e.g., `parent_intent`, `outcome.metric`, `chosen_opportunity.rationale`). Pre-fills are reserved for the template's identity.

## Verification mode

- **Goal-based check** for the template's structural conformance — `tools/lint-frontmatter.py --check-template templates/ost.md` exits 0, and the pytest harness `scripts/tests/test_templates_instantiate.py` passes (the harness already auto-discovers `templates/*.md`, so the new file is picked up without harness edits).
- **Audit-driven** for kit-wide health — `bash tools/pre-pr.sh` exits 0.

No TDD or manual gesture: the template is a static file whose contract is fully expressible as linter + pytest + grep checks.

## Contract tests

- `T1` — `templates/ost.md` exists at the repo root: `test -f templates/ost.md` exits 0.
- `T2` — `python3 tools/lint-frontmatter.py --check-template templates/ost.md` exits 0 (all placeholders accepted; required keys present; nested-mapping placeholders accepted under the nested-container-placeholder rule).
- `T3` — Required universal-schema and Handover-2 frontmatter keys are present (per the retention call in §"Outputs" item 1). Specifically the parsed YAML has:
  - Universal schema: `id`, `slug`, `object_type`, `name`, `description`, `owner`, `status`, `priority`, `risk_level`, `created`, `last_updated`.
  - Retained traceability keys: `parent_intent`, `related_personas`, `related_problems`, `related_kpis`.
  - Dropped traceability keys (asserted absent): `parent_opportunity`, `parent_learning`, `parent_vision`, `parent_initiative`.
  - Handover-2 required fields: `object_type` (pre-filled in the universal block), `parent_intent`, `outcome`, `opportunity_count`, `chosen_opportunity`, `related_personas`, `related_problems`, `human_owned_decisions`.
  - Nested keys under `outcome:`: `id`, `metric`, `current`, `target`, `measurement` (all five present).
  - Nested keys under `chosen_opportunity:`: `id`, `rationale` (both present).
  - Asserted by a one-liner: `python3 -c "import yaml; d=yaml.safe_load(open('templates/ost.md').read().split('---',2)[1]); assert set(d.get('outcome',{}).keys()) >= {'id','metric','current','target','measurement'}; assert set(d.get('chosen_opportunity',{}).keys()) >= {'id','rationale'}; assert all(k in d for k in ['parent_intent','outcome','opportunity_count','chosen_opportunity','related_personas','related_problems','related_kpis','human_owned_decisions']); assert not any(k in d for k in ['parent_opportunity','parent_learning','parent_vision','parent_initiative'])"`. Note: T2 (the `--check-template` linter) is the authoritative completeness gate; T3 here pins the specific retention decision for `templates/ost.md`.
- `T4` — Required section headings appear in order: `awk '/^## /' templates/ost.md` lists exactly (in this order) `## The outcome`, `## Opportunity space`, `## The chosen one`, `## Source opportunities`, `## Excluded`, then `## Optional sections` (the convention-required tail).
- `T5` — Angle-bracket placeholder discipline: `python3 -c "body=open('templates/ost.md').read(); body_only=body.split('---',2)[2] if body.count('---')>=2 else body; assert '{{' not in body_only and '__FILL__' not in body_only"` exits 0.
- `T6` — Pytest harness passes: `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (the new file is auto-discovered and validates clean).
- `T7` — Kit-wide health: `bash tools/pre-pr.sh` exits 0 after the file lands.
- `T8` — `ROADMAP.md` F3.2 row is checked: `grep -E "^- \[x\] \*\*F3\.2\*\*" ROADMAP.md` returns exactly one line.
- `T9` — `templates/_meta/README.md` lists `templates/ost.md` in its index: `grep -c "ost.md" templates/_meta/README.md` returns at least 1.

## Non-goals

- **Not building** `/draft-ost`, `/generate-ost`, `/update-ost`, or `/audit-discovery-coherence` (ROADMAP P2.7, P2.9, P2.10, P2.11). Those commands and agents consume the template once it ships; they are not part of F3.2.
- **Not authoring** the sibling structured `discovery/trees/<slug>.json` companion file referenced by `docs/HANDOVERS.md` for the OST validator. That artifact serves ROADMAP P2.8 (`script-ost-validator`) and is a separate row (deferred to ROADMAP P2.8; see Open Question 1 for rationale).
- **Not authoring** any instantiated OST under `discovery/trees/`. The template is the scaffold; the instance is what a kit user produces when they apply it.
- **Not adding** new ontology types. The artifact's `object_type` is the existing Domain I composite `Opportunity Solution Tree` — no new entry in `context/frameworks/ontology.md`.
- **Not modifying** `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, or `scripts/tests/test_templates_instantiate.py`. Any change to those would belong to a different spec (or to the parent `template-authoring-convention`, which has already shipped).
- **Not enumerating** Handover-2 optional sections. Handover 2 lists no optional sections explicitly; the convention-required `## Optional sections` heading is present as a discipline marker only.

## Open questions

1. **Sibling structured `discovery/trees/<slug>.json` companion.** `docs/HANDOVERS.md` §"Handover 2" names a structured `discovery/trees/<slug>.json` file "for the OST validator." Whether that companion file belongs in F3.2 (as `templates/ost.json`) or in the ROADMAP P2.8 (`script-ost-validator`) row is ambiguous in the current ROADMAP. **Resolved here: defer to P2.8.** Reasoning: F3.2 is scoped as the `.md` template (the human-facing artifact); the `.json` schema is an interchange format consumed by the validator script and its shape is owned by that script's spec. If the F3-block executor disagrees during the F3.2 EXECUTE phase, surface it as a finding for the orchestrator to reconcile with P2.8; do not silently expand F3.2's scope.
2. **Should the `## Source opportunities` section have a sub-heading per-node convention?** Handover 2 says "interview-level evidence under each tree node" but does not prescribe whether each tree node gets its own `### <node-id>` sub-heading. **Resolved here: no.** The template ships a single level-2 heading with an angle-bracket placeholder body describing the contract; a kit user adds level-3 sub-headings per node as they fill in the tree. Encoding a per-node sub-structure in the template would either fix the tree shape (limiting OST topologies) or require placeholder sub-headings whose count is unknown at template-write time. Surface this to a guide author (a future `docs/guides/how-to-draft-an-ost.md`) rather than to the template.

## Acceptance criteria

- [ ] `templates/ost.md` exists and is a single file (not a folder).
- [ ] Frontmatter pre-fills `object_type: Opportunity Solution Tree` and `status: Draft`; every other field is an angle-bracket placeholder.
- [ ] All seven Handover-2 required fields are present in the parsed YAML (`object_type` pre-filled in the universal block; `parent_intent`, `outcome`, `opportunity_count`, `chosen_opportunity`, `related_personas`, `related_problems`, `human_owned_decisions`), including the five nested keys under `outcome:` (`id`, `metric`, `current`, `target`, `measurement`) and the two nested keys under `chosen_opportunity:` (`id`, `rationale`).
- [ ] The five Handover-2 required sections (`## The outcome`, `## Opportunity space`, `## The chosen one`, `## Source opportunities`, `## Excluded`) appear as level-2 headings in that exact order, followed by `## Optional sections`.
- [ ] `tools/lint-frontmatter.py --check-template templates/ost.md` exits 0.
- [ ] `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0.
- [ ] `bash tools/pre-pr.sh` exits 0.
- [ ] `ROADMAP.md` F3.2 row is checked off.
- [ ] `templates/_meta/README.md` lists `templates/ost.md`.
- [ ] No new ontology type added; no edits to HANDOVERS, CONVENTIONS, ontology, the linter, or the pytest harness.
- [ ] No angle-bracket-malformed placeholder (`<>`, `< >`, `{{...}}`, `__FILL__`) appears in the file body.
- [ ] No fabricated OST domain content (specific outcomes, opportunities, evidence, insights) appears in the body.

## Cross-references

- **Consumed by:**
  - Future `/draft-ost` / `/generate-ost` (ROADMAP P2.7, P2.9) — these commands instantiate a `discovery/trees/<slug>.md` by copying this template.
  - Future `/audit-discovery-coherence` (ROADMAP P2.11) — reads OST frontmatter to detect missing `parent_intent`; the field's name and presence are pinned by this template.
  - Future `validate-ost.py` (ROADMAP F2.7) and `script-ost-validator` (ROADMAP P2.8) — validate OST instances; the field shapes pinned here are the validator's input contract.
  - Future `docs/guides/how-to-draft-an-ost.md` (no ROADMAP row yet; surfaced as a guide candidate) — the human-facing how-to that walks a kit user through filling the template.
- **Consumes:**
  - `templates/_meta/template-skeleton.md` (the source the template copies from).
  - `docs/HANDOVERS.md` §"Handover 2: Discovery → Validation" (the verbatim source of the required frontmatter and required sections).
  - `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" and §"Universal metadata schema" (placeholder syntax, frontmatter ordering, pre-fill rules).
  - `context/frameworks/ontology.md` (Domain I composite `Opportunity Solution Tree`; Domain C atomic types Outcome, Opportunity, Job to Be Done, Problem, Evidence, Insight).
  - `tools/lint-frontmatter.py --check-template` (the validator).
  - `scripts/tests/test_templates_instantiate.py` (the pytest harness).
- **Frontmatter fields owned:** none uniquely. The template re-projects the Handover-2 contract from `docs/HANDOVERS.md` and the universal schema from `docs/CONVENTIONS.md`; both remain canonical.
- **Ontology object types touched:** `Opportunity Solution Tree` (Domain I composite); `Outcome` (Domain D, by reference in `outcome:`); `Opportunity` (Domain C, by reference in `chosen_opportunity:` and across the opportunity space); `Job to Be Done`, `Problem`, `Evidence`, `Insight` (Domain C, by reference in source-opportunities content).
