# Spec: template-pm-spec

- **Status:** Shipped (2026-05-22)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template
- **Serves kit phase:** Delivery
- **Constrained by:** `docs/specs/template-authoring-convention/spec.md` (parent authoring convention, including its Open Question 2 location resolution for PM-spec instantiated artifacts); `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" (parent Initiative folder contract) and §"Handover 6: Spec → Engineering Handoff Packet" (the downstream packet whose per-feature taxonomy this template's required-section list is a defensible subset of); `docs/CONVENTIONS.md` §"Templates", §"Universal metadata schema", §"Lifecycle states", §"Specs and Plans" (the exempt-from-universal-schema clause that applies to *kit-build* specs, NOT to product PM specs); `context/frameworks/ontology.md` Domain E (Capability, Feature, Requirement, Acceptance Criteria, Non-Functional Requirement, Dependency, Open Question); ROADMAP F3.8.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `templates/pm-spec.md` — a single-file template a kit user copies to `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` when authoring the PM-side spec for one feature listed in the parent Initiative's `child-specs.md` manifest. The template's `object_type:` is pre-filled to `Feature` (Domain E). The template gates the transition from Handover 5 (Initiative folder) into Handover 6 (Engineering Handoff Packet): one PM Spec per row in `child-specs.md`; each row corresponds to exactly one Feature, and each spec provides the per-feature contract that the Handoff Packet aggregates and dresses for engineering consumption. The template is angle-bracket-only, status pre-filled `Draft`, body sections derived as documented in §"Required-section provenance". Ontology-path reconciliation: `context/frameworks/ontology.md` Domain E shows `delivery/specs/` as the Feature artifact directory; the parent template-authoring-convention spec's Open Q2 resolution routes PM Specs to `delivery/initiatives/<initiative-slug>/specs/` (initiative-nested), which this spec adopts. The ontology table's `delivery/specs/` entry refers to the directory used by Features authored OUTSIDE an Initiative (an edge case not handled by F3.8).

## Objective

`templates/pm-spec.md` is the seed every PM-side feature spec is copied from. Without it, the PM side of `child-specs.md` manifests links to ad-hoc per-team scratch documents and the Handoff Packet author re-litigates structure feature-by-feature. With it, every PM Spec under every Initiative folder carries the same identity-shape (`object_type: Feature`, `parent_initiative`, `capabilities`, `status`), the same required-section ordering (problem → capabilities contributed to → user behaviour current vs future → functional requirements → acceptance criteria → NFRs → dependencies → out of scope → open questions), and instantiates as `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`. The instantiated artifact is the *predecessor* to a Handoff Packet for that one feature.

The component does not yet exist. There is no `templates/pm-spec.md`. ROADMAP F3.8 names the slug `template-pm-spec` and the target `templates/pm-spec.md`. The parent spec `docs/specs/template-authoring-convention/spec.md` is `Shipped` (2026-05-22) and ships the skeleton this template copies from (`templates/_meta/template-skeleton.md`), the authoring convention sub-section in `docs/CONVENTIONS.md`, and the `--check-template` linter mode with its companion contract test `scripts/tests/test_templates_instantiate.py`.

## Why now

F3.8 is one of ten F3.x templates the kit needs before any of the Phase-4 commands that draft PM specs from an initiative can ship. ROADMAP P4.x commands that consume this template are not yet enumerated as standalone rows; the closest enumerated downstream item is P4.11 (`/handoff-packet`, "Assemble the 23-section engineering deliverable"), which reads PM Specs as its primary input. A `/draft-pm-spec` command analogous to P4.1's `/draft-vision` is anticipated but unscheduled — its prerequisite is this template. Authoring the template now closes the F3 block and unblocks both the Phase-4 drafting commands and any human kit-adopter who wants to instantiate a PM Spec by hand.

The parent template-authoring convention is shipped, so the skeleton, the `--check-template` linter mode, and the contract test are all available. The cost of authoring this template now is one work-loop; the cost of deferring it is that adopters either invent their own per-feature spec shape (drift) or skip the PM Spec entirely (jumping straight from Initiative to Handoff Packet — Operating-model failure mode where engineering inherits an unstructured prose document instead of a structured deliverable).

## Inputs and outputs

**Inputs.**

- `templates/_meta/template-skeleton.md` — the canonical skeleton this template copies from (per parent spec §"Skeleton-text contract" and `docs/CONVENTIONS.md` §"Templates" → "Authoring a new template").
- `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" — the parent Initiative folder contract that names `child-specs.md` (table: spec slug, owning context, owning team, status, link) as the manifest each PM Spec links from. The `link` column is compatible with either a file or folder form; this spec adopts the single-file form (see §"Open questions" Q2). **Quoted verbatim** in §"Required-section provenance" below.
- `docs/HANDOVERS.md` §"Handover 6: Spec → Engineering Handoff Packet" — the downstream 23-file Handoff Packet contract; the PM Spec template's required sections are a per-feature subset of this taxonomy as documented in §"Required-section provenance". **Quoted verbatim** in §"Required-section provenance" below.
- `docs/CONVENTIONS.md` §"Templates" — placeholder syntax, frontmatter ordering, pre-fill vs placeholder, required-vs-optional sections, linter contract.
- `docs/CONVENTIONS.md` §"Universal metadata schema" — the universal frontmatter every product artifact carries. **The PM Spec is a product artifact, not kit-build scaffolding**, so it is NOT exempt from the universal schema (the exemption in §"Specs and Plans" applies only to kit-build specs under `docs/specs/<feature>/`).
- `docs/CONVENTIONS.md` §"Lifecycle states" — `status:` is pre-filled `Draft` (entry state of the product-artifact track).
- `context/frameworks/ontology.md` Domain E — the typed sub-objects the PM Spec describes (Capability, Feature, Requirement, Acceptance Criteria, Non-Functional Requirement, Dependency, Open Question).
- `tools/lint-frontmatter.py --check-template` — the linter mode the template must pass (test T2 below).
- `scripts/tests/test_templates_instantiate.py` — the existing contract test that automatically discovers `templates/*.md` and runs `--check-template` against each; this template lands and is exercised by that test without any test-file modification (the parametrize over `_discover_template_targets()` picks it up).

**Outputs.**

1. `templates/pm-spec.md` — the new single-file template. Body shape:
   - Universal-metadata frontmatter block (per CONVENTIONS.md §"Universal metadata schema"), field-order matching the schema verbatim, with pre-filled identity:
     - `object_type: Feature`
     - `status: Draft`
     - All other universal-schema fields rendered as angle-bracket placeholders (e.g., `name: <feature name>`, `description: <one to three sentences>`, `owner: <named human or role>`, `priority: <Low | Medium | High | Critical>`, `risk_level: <Low | Medium | High | Critical>`, `created: <YYYY-MM-DD>`, `last_updated: <YYYY-MM-DD>`).
     - Traceability fields kept as placeholders where applicable; fields with no parent in this context (e.g., `parent_intent`, `parent_opportunity`, `parent_learning`, `parent_vision`) are deleted per the skeleton's "delete fields that don't apply" guidance — `parent_initiative` is the load-bearing parent for a PM Spec.
     - Evidence/assumption block and human-vs-AI block as in the skeleton (placeholders preserved).
   - `# Handover-specific fields` block under a YAML comment, per CONVENTIONS.md §"Templates" → "Frontmatter ordering". Fields added (each named by inference from Handover 6's 23-file taxonomy applied at per-feature scope; provenance marked). Per the cross-cutting dedup convention in §"Boundaries → Always do", any field already present in the universal-metadata schema (e.g., `parent_initiative`, `related_kpis`) appears once — in its universal-schema position — and is NOT duplicated under this comment block.
     - `parent_initiative: <initiative slug>` — load-bearing; inferred from HANDOVERS Handover 5 (the manifest implies a parent Initiative link). Carried in the universal-schema position per the dedup convention.
     - `capabilities: [<CAP-NNN>, ...]` — the Capability id(s) this Feature contributes to; verbatim from HANDOVERS Handover 5 `README.md` frontmatter (`capabilities: [<CAP-NNN>, ...]`) and from Handover 6 `capabilities.md`.
     - `related_kpis: [<KPI-NNN>, ...]` — universal-schema field, surfaced here as a PM-spec concern because the parent Vision's predicted outcomes flow down through Capability into per-Feature success measurement. Carried in the universal-schema position per the dedup convention.
   - H1: `# <Feature name>`.
   - Body intro blockquote: one paragraph naming the Feature, citing the parent Initiative slug, citing HANDOVERS §"Handover 5" (manifest source) and §"Handover 6" (downstream consumer).
   - Required sections (provenance for each in §"Required-section provenance" below). The section order must match the order Handover 6's file list arranges its per-feature content; the `T4` contract test enforces this exact sequence against `awk '/^## /'` output.
     1. `## Problem this spec addresses`
     2. `## Capabilities contributed to`
     3. `## User behaviour — current vs future`
     4. `## Functional requirements`
     5. `## Acceptance criteria`
     6. `## Non-functional requirements`
     7. `## Dependencies`
     8. `## Out of scope`
     9. `## Open questions`
   - `## Optional sections` heading at the bottom with one example optional sub-section (`### Business rules`) per parent spec's "Required vs optional sections" convention.
   - File length: ≤ 120 body lines (skeleton is ≤ 80; this template adds the Handover-specific frontmatter block plus 9 required-section headings plus an Optional-sections block, so ~30-40 additional lines is realistic).

2. `templates/_meta/README.md` — append one line under "## Shipped templates" naming this template and a one-clause description ("`pm-spec.md` — PM-side spec for one Feature listed in an Initiative's child-specs manifest").

3. ROADMAP `F3.8` row — checked with `Shipped: <today>`.

A reader of this section should be able to construct the diff without reading anything else.

## Required-section provenance

This sub-section pins which required-section headings derive verbatim from HANDOVERS.md and which are inferred. Inferred sections cite the Handover 6 file or column they map from and explain the inference.

**HANDOVERS-verbatim (Handover 6 file list, applied at per-feature scope):**

- `## Problem this spec addresses` — maps to Handover 6's `problem.md` ("validated problem statement + evidence"), scoped to the per-feature problem (not the parent Initiative's full problem statement, which is held in the Initiative's `capabilities.md` row's `linked Problem`).
- `## Capabilities contributed to` — maps to Handover 6's `capabilities.md` ("from the parent initiative") and Handover 5's `capabilities.md` ("each Capability with linked Problem, evidence strength, related KPI"). The PM Spec restates which Capability(s) this Feature contributes to (per ontology Domain E direction: `Capability → Feature` is decomposition; a Feature is part of one or more Capabilities).
- `## User behaviour — current vs future` — maps to Handover 6's `current-workflow.md` ("how it works today") and `future-workflow.md` ("how it'll work"). Combined into a single section here at per-feature scope because at one-feature granularity the workflow delta is typically one paragraph each, not two files.
- `## Functional requirements` — maps to Handover 6's `requirements.yaml` ("REQ-NNN files with full ontology metadata"). The PM Spec lists the Requirements this Feature comprises; the engineering Handoff Packet's `requirements.yaml` is the structured aggregation.
- `## Acceptance criteria` — maps to Handover 6's `acceptance-criteria.md` ("per-requirement"). Listed per-requirement.
- `## Non-functional requirements` — maps to Handover 6's `non-functional-requirements.md`. Verbatim heading.
- `## Dependencies` — maps to Handover 6's `dependencies.md`. Verbatim heading.
- `## Out of scope` — maps to Handover 6's `out-of-scope.md`. Verbatim heading.
- `## Open questions` — maps to Handover 6's `open-questions.md` AND universal-schema's `open_questions:` frontmatter field. The frontmatter holds the structured list; the section holds the per-question rationale.

**Inferred (no direct HANDOVERS row but subset of the per-feature scope, as documented in §"Required-section provenance"):**

- The H1 + intro blockquote (citation pattern) — inferred from the parent template-authoring convention's skeleton (`templates/_meta/template-skeleton.md` lines 56-58). Not a content section, just the citation envelope.
- The `## Optional sections` block — inferred from the parent template-authoring convention's "Required vs optional sections" rule (CONVENTIONS.md §"Templates"). Example optional section `### Business rules` maps to Handover 6's `business-rules.md`, which is optional at per-feature scope because some Features have no business-logic rules beyond their Acceptance Criteria.

**Deliberately not included (out of scope for the PM Spec; held at packet-level instead):**

- `business-objective.md`, `customer-segment.md`, `personas.md` — held at the parent Initiative's `README.md` frontmatter and at the Vision; restated at packet level for engineering convenience but not duplicated per-feature in the PM Spec.
- `jobs-to-be-done.md` — held at parent Initiative or upstream Discovery OST; not per-feature.
- `policy-constraints.md`, `risks.md`, `decision-log.md`, `launch-considerations.md`, `success-metrics.md`, `human-owned-decisions.md` — packet-level aggregations of cross-feature concerns; the PM Spec surfaces them via universal-schema frontmatter (`risks:`, `human_owned_decisions:`) where applicable but does not author them as standalone body sections.
- `features.md` — the parent Initiative's `child-specs.md` IS the Features list; restating it at per-feature scope inside one PM Spec is circular.

## Boundaries

### Always do

- Quote `docs/HANDOVERS.md` §"Handover 6" file list verbatim for every required-section claim; mark inferred sections explicitly per §"Required-section provenance" above.
- Use angle-bracket placeholder syntax exclusively (per parent spec §"Convention-text contract" → "Placeholder syntax"). Pre-fill ONLY `object_type: Feature` and `status: Draft`; every other field is a placeholder.
- Place universal-schema frontmatter first, then a `# Handover-specific fields` YAML comment, then the per-PM-Spec fields. (Per CONVENTIONS.md §"Templates" → "Frontmatter ordering".)
- **Cross-cutting dedup convention.** When HANDOVERS-mandated fields overlap with the universal-metadata schema, the field appears once — in its universal-schema position — carrying the HANDOVERS-mandated value. The universal-schema placeholder is deleted in the same edit. The handover-specific block carries only fields not present in the universal schema. (Per kit convention used by F3.3/F3.5/F3.10.)
- Pass `tools/lint-frontmatter.py --check-template templates/pm-spec.md` with exit 0.
- Pass `python3 -m pytest scripts/tests/test_templates_instantiate.py` with the new template auto-discovered.
- Append the template's entry to `templates/_meta/README.md` `## Shipped templates` in the same task that lands the template file (per parent spec's "Sequential README.md appends" rollout note — this is the load-bearing concurrency-safety note for the F3 fan-out).

### Ask first

- Adding any new frontmatter field not enumerated in CONVENTIONS.md §"Universal metadata schema" or in Handover 5's README.md frontmatter or Handover 6's README.md frontmatter.
- Changing the resolved `object_type:` from `Feature` to anything else. The choice is documented in §"Open questions" and the surface area is small enough to flip in one edit, but it ripples into the section-heading order and the `capabilities:` field's semantics (a `Feature` contributes to one or more Capabilities; `Capability` would invert the relationship).
- Splitting the single-file template into a folder. The default is single-file per the rationale in §"Open questions" Q2; reversing requires reading what a kit user actually writes when they instantiate the template (none yet).

### Never do

- Add `PM Spec` or `Product Spec` as an ontology type. Domain I is phase-boundary handover composites; the PM Spec is the per-feature contract *underneath* a Handover 5 manifest, not itself a phase-boundary handover. Identical reasoning to the parent spec's "Never do" entry against adding `kit-template`. Use `Feature` (existing Domain E).
- Edit `docs/HANDOVERS.md` to add a new "Handover 5.5: Initiative → PM Spec" row. The PM Spec is internal to the Handover 5 → Handover 6 transition; the manifest (`child-specs.md`) is already the contract. If a future spec disagrees, surface as an Open Question — do not author the row here.
- Edit `docs/CONVENTIONS.md` to amend the §"Specs and Plans" → "Exempt from the universal metadata schema" clause. That clause is correct as written (it scopes itself to *kit-build* specs); the PM Spec is a product artifact and inherits the universal schema by default. If a reviewer reads the clause as ambiguous, surface as an Open Question — do not author the amendment here.
- Pre-fill the template body with example content for any required section. The template is shape-only; content belongs in the instantiated PM Spec, not in the template.
- Walk `templates/` from the default-mode linter. Out of scope (the parent spec already declared this Non-goal).

## Verification mode

- **Goal-based check** for the template file's existence, shape, and frontmatter. One-liner: `python3 tools/lint-frontmatter.py --check-template templates/pm-spec.md` exits 0.
- **Audit-driven** for kit-wide health: `bash tools/pre-pr.sh` exits 0; `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (the existing test auto-discovers the new template via `_discover_template_targets()`).

No TDD — there is no compressible-invariant code to test-first. No manual gesture — the template is consumed by a future drafting command, not by interactive human gestures.

## Contract tests

- **T1** — `test -f templates/pm-spec.md` exits 0.
- **T2** — `python3 tools/lint-frontmatter.py --check-template templates/pm-spec.md` exits 0.
- **T3** — Required universal-schema frontmatter keys present: `python3 -c "import sys; sys.path.insert(0, '.'); from scripts.lib.frontmatter import parse_file; fm = parse_file('templates/pm-spec.md'); keys = set(fm.data.keys()); required = {'id', 'slug', 'object_type', 'name', 'description', 'owner', 'status', 'priority', 'risk_level', 'created', 'last_updated', 'parent_initiative', 'capabilities', 'human_owned_decisions', 'ai_assistance_used', 'ai_assistance_allowed', 'human_approval_required'}; missing = required - keys; assert not missing, missing"` exits 0.
- **T4** — Required-section headings present in the load-bearing order, immediately preceding the `## Optional sections` block: `awk '/^## /' templates/pm-spec.md` returns these nine lines in this order as the first nine `## ` headings, followed by `## Optional sections` as the tenth and final `## ` heading: `## Problem this spec addresses`, `## Capabilities contributed to`, `## User behaviour — current vs future`, `## Functional requirements`, `## Acceptance criteria`, `## Non-functional requirements`, `## Dependencies`, `## Out of scope`, `## Open questions`, `## Optional sections`. (The test compares against the explicit ten-line sequence; bare-count tests would mask a missing or extra heading.)
- **T5** — Angle-bracket-only placeholder discipline: `grep -nE '(\{\{|__FILL__)' templates/pm-spec.md` returns no matches (exit 1 from grep is a pass for this test).
- **T6** — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (the new template is auto-discovered by `_discover_template_targets()` and exercised by the parametrized `test_template_passes_check_template_mode`).
- **T7** — `bash tools/pre-pr.sh` exits 0.
- **T8** — `grep -nE "^- \[x\] \*\*F3\.8\*\*" ROADMAP.md` returns exactly 1 line (F3.8 checked).
- **T9** — `templates/_meta/README.md` lists this template under "## Shipped templates": `grep -nE 'pm-spec\.md' templates/_meta/README.md` returns ≥ 1 line.
- **T10** — `object_type:` pre-filled to `Feature`: `awk '/^object_type:/{print $2; exit}' templates/pm-spec.md` prints `Feature`.
- **T11** — `status:` pre-filled to `Draft`: `awk '/^status:/{print $2; exit}' templates/pm-spec.md` prints `Draft`.

## Non-goals

- **Not** building the `/draft-pm-spec` command (or any other Phase-4 command that instantiates this template). That's a separate ROADMAP item (a candidate P4.x slot, not yet rowed).
- **Not** authoring an instantiated PM Spec under `delivery/initiatives/<some-initiative>/specs/<some-spec>.md`. The kit ships no real Initiative folder yet; the template is shape-only and is exercised only by the linter and the contract test until a kit user instantiates it.
- **Not** amending `docs/HANDOVERS.md` to add a "Handover 5.5: Initiative → PM Spec" row. The PM Spec is internal to Handover 5 → Handover 6; if a reviewer concludes a dedicated row is necessary, that's a follow-up spec, surfaced here as Open Question 3.
- **Not** amending `docs/CONVENTIONS.md` §"Specs and Plans" exemption clause. The clause already scopes itself to kit-build specs; the PM Spec is a product artifact and inherits the universal schema. Surfaced as Open Question 4.
- **Not** reconciling whether F1-G7's `related_capabilities` field belongs in the universal schema. The parent spec deliberately excluded that key from the canonical-key-set test; this spec uses `capabilities: [<CAP-NNN>, ...]` (handover-specific block) rather than `related_capabilities` to stay inside the parent spec's drawn line.
- **Not** designing the `child-specs.md` manifest format itself (that's F3.7's domain — `template-initiative`).
- **Not** introducing per-spec `owning_context` / `owning_team` frontmatter (per Decision B). These dimensions live in the parent Initiative's `child-specs.md` manifest columns per Handover 5. If a future consuming command needs them per-spec, that command's spec amends F3.8.

## Open questions

1. **Object_type resolution: `Feature` vs `Capability` vs new Domain I composite.** Settled here as `Feature` (Domain E). Rationale: per `context/frameworks/ontology.md` Domain E, "Feature = a concrete product function that delivers a capability." A PM Spec describes one feature with the requirements/acceptance/NFRs that compose it. `Capability` was rejected because Capabilities are enumerated at parent-Initiative scope (Handover 5's `capabilities.md`) and one Capability typically spans multiple Features. A new Domain I composite was rejected because Domain I is explicitly phase-boundary handover composites (Strategic Intent, OST, Assumption Map, Vision, Landing Report, etc.); the PM Spec is internal to the Handover 5 → 6 transition, not its own phase boundary, and the parent spec's "Never do" forbids ad-hoc ontology additions. Reviewer is the parent-spec adversarial-reviewer pass; reconciliation, if needed, happens before EXECUTE.

2. **Single-file vs folder.** Settled here as single-file (`templates/pm-spec.md` → `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`). Rationale (strengthened per Decision A):
   - HANDOVERS Handover 5's `child-specs.md` `link` column is compatible with either form — file or folder — so the manifest does not force the choice.
   - **Reduced-ceremony argument (load-bearing).** A PM Spec is one file per Feature. A folder is overhead unless multiple files are needed. Handoff Packets (Handover 6) are folder-based because they aggregate 23 files; PM Specs at one file each don't need that ceremony.
   - The Handoff Packet (Handover 6) explodes into 23 files — but that's a packet-level aggregation downstream of the PM Spec. The PM Spec sits before that explosion, at a granularity that a single markdown file comfortably holds.
   - If kit-adopters start authoring PM Specs that consistently outgrow one file, surface the call as a follow-up spec; not in scope here.

   **Override clause.** This F3.8 spec OVERRIDES parent template-authoring-convention spec Open Q2's folder resolution. Per the parent spec's escape clause ("if the F3.8 worker disagrees, that surfaces as a finding from its own adversarial review and we reconcile then"), this adversarial-review reconciliation ratifies the single-file form. The parent spec is frozen (Status: Shipped); this override is documented here in F3.8 and does not require amending the parent. Future F3.x worker authors should read this resolution as the authoritative.

3. **Does HANDOVERS.md need a dedicated "Handover 5.5: Initiative → PM Spec" row?** Settled here as **no, defer**. Handover 5's `child-specs.md` manifest is already the contract that gates "an Initiative has spelled out its Features." Authoring a Handover 5.5 row would duplicate the manifest's role; the PM Spec is internal to Handover 5 → 6, not a phase-boundary handover. The parent spec's "Never do" against editing HANDOVERS in F3.x worker specs reinforces this. Reviewer is the adversarial-reviewer pass; if it concludes otherwise, raise as a follow-up RFC, do not author the row in this loop.

4. **CONVENTIONS.md exemption clause clarity.** The §"Specs and Plans" → "Exempt from the universal metadata schema" clause names "specs (`docs/specs/<feature>/spec.md`), plans (`plan.md`), and state files (`state.json`)" as the exempt set. Reading it strictly, that exempts only files under `docs/specs/` — the PM Spec lives under `delivery/initiatives/<initiative-slug>/specs/` and is therefore NOT in the exempt set. Settled here as **the strict reading is correct**: PM Specs are product artifacts and carry full universal-schema frontmatter. **Recommended follow-up (upgraded from deferred non-goal per reviewer Finding E3):** a follow-up spec should amend CONVENTIONS §"File conventions" to read "kit-build scaffolding — specs under `docs/specs/`, plans, state — is exempt" (tightening the unqualified "specs" to "specs under `docs/specs/`"). Owner: anyone touching CONVENTIONS next; not in F3.8's scope.

5. **Initiative-folder `specs/` sub-directory existence.** The parent template-authoring-convention spec's Open Question 2 resolved the directory as `specs/` inside the initiative folder (`delivery/initiatives/<initiative-slug>/specs/`, not `delivery/specs/<slug>/`); that directory-level resolution stands. The parent additionally proposed the per-spec form as `<spec-slug>/` (folder); this F3.8 spec OVERRIDES that to `<spec-slug>.md` (single file). See Q2 above for the strengthened rationale and override-clause text. The instantiated path is `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`.

6. **Cross-context Features.** A Feature whose implementation touches multiple bounded contexts has no native representation in this template; the current template assumes one Feature per spec. **Resolved:** cross-context Features should be split into separate PM Specs per context before being entered in `child-specs.md`. If splitting is impossible, the consuming Initiative's `context-map.md` is the right home for the cross-context interaction, not per-spec frontmatter.

7. **Audit-gap acknowledgment.** The PM Spec has no dedicated HANDOVERS row; `/audit-completeness` runs on the parent Initiative's Handoff Packet (Handover 6), not on per-PM-Spec contents. Closing this gap would require either a "Handover 5.5: Spec → Spec-Completeness" row in HANDOVERS.md OR extending `/audit-spec-linkage` to verify per-spec section presence. Not in F3.8's scope; track as a follow-up ROADMAP candidate.

## Acceptance criteria

- [ ] `templates/pm-spec.md` exists, single-file, derived from `templates/_meta/template-skeleton.md`.
- [ ] `object_type:` pre-filled to `Feature`. `status:` pre-filled to `Draft`. All other universal-schema fields are angle-bracket placeholders.
- [ ] Frontmatter ordering: universal-schema block first (carrying `parent_initiative`, `capabilities`, `related_kpis` in their universal-schema positions per the dedup convention), then `# Handover-specific fields` YAML comment, then any fields not present in the universal schema. Per Decision B, `owning_context` and `owning_team` are NOT introduced; they live in the parent Initiative's `child-specs.md` manifest columns.
- [ ] Required-section headings present in order: Problem this spec addresses → Capabilities contributed to → User behaviour — current vs future → Functional requirements → Acceptance criteria → Non-functional requirements → Dependencies → Out of scope → Open questions.
- [ ] `## Optional sections` block present at the bottom with at least one example optional sub-section.
- [ ] T1 through T11 from §"Contract tests" all pass.
- [ ] `templates/_meta/README.md` lists `pm-spec.md` under "## Shipped templates".
- [ ] ROADMAP F3.8 marked `Shipped: <YYYY-MM-DD>`.
- [ ] No new ontology type added (T15 from the parent spec's contract test set still passes — `grep -nE "^(\|\s*)?[Pp][Mm][- ][Ss]pec" context/frameworks/ontology.md` returns 0).
- [ ] No edit to `docs/HANDOVERS.md`. No edit to `docs/CONVENTIONS.md`.

## Cross-references

- **Consumed by:** future `/draft-pm-spec` command (anticipated under ROADMAP P4.x, currently unscheduled); kit users authoring a PM Spec by hand; the `/handoff-packet` command (P4.11) when it walks a parent Initiative's `child-specs.md` manifest and reads each PM Spec to assemble the 23-file packet.
- **Consumes:** `templates/_meta/template-skeleton.md` (the canonical skeleton); `docs/HANDOVERS.md` §"Handover 5" + §"Handover 6"; `docs/CONVENTIONS.md` §"Templates" + §"Universal metadata schema" + §"Lifecycle states"; `context/frameworks/ontology.md` Domain E; `tools/lint-frontmatter.py` (in `--check-template` mode); `scripts/tests/test_templates_instantiate.py` (auto-discovers this template).
- **Frontmatter fields owned:** This template adds no NEW fields to the universal schema. It pins which existing fields are required for a PM Spec (`parent_initiative`, `capabilities`, `related_kpis`) and which are optional. Per Decision B, no non-universal-schema fields are introduced; `owning_context` and `owning_team` remain in the parent Initiative's `child-specs.md` manifest columns (Handover 5) and are not duplicated as per-spec frontmatter.
- **Ontology object types touched:** `Feature` (Domain E — `object_type:` value). The PM Spec references but does not classify: `Capability` (Domain E — listed in `capabilities:` frontmatter; the Feature contributes to one or more Capabilities); `Requirement`, `Acceptance Criteria`, `Non-Functional Requirement`, `Dependency`, `Open Question` (Domain E — listed in the respective body sections); `Initiative` (Domain D — parent, via `parent_initiative:`); `KPI` (Domain D — listed in `related_kpis:`).
- **`parent_initiative:` enforcement delegation (per reviewer Finding E2):** The `parent_initiative:` placeholder is enforced as non-empty by `/audit-spec-linkage` (Handover 5's detector), NOT by `--check-template` (which accepts any angle-bracket value). The template only ensures the field exists and is angle-bracketed; the linkage audit verifies the instantiated value resolves to a real Initiative slug.
- **Note on the kit's `docs/_templates/spec.md`.** The kit ships `docs/_templates/spec.md` as the seed for *kit-build* specs (audience: an agent building a kit component; artifact lives under `docs/specs/<feature>/spec.md` and is exempt from the universal-metadata schema). This F3.8 template is the *product-PM-spec* analog (audience: a PM authoring a per-feature spec under a real Initiative; artifact lives under `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`; not exempt from the universal schema). The two templates share the *idea* of "spec.md = contract for one buildable unit" but have different frontmatter, different sections, different audiences, and different downstream consumers. They are deliberately separate. (This note describes the difference; the single-file rationale in §"Open questions" Q2 does NOT depend on this precedent.)
