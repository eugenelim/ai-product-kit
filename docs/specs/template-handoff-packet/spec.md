# Spec: template-handoff-packet

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template
- **Serves kit phase:** Delivery
- **Constrained by:** [`docs/specs/template-authoring-convention/spec.md`](../template-authoring-convention/spec.md) (parent contract — placeholder syntax, frontmatter ordering, pre-fill rules, linter contract, skeleton-as-copy-source, folder-template layout rule, per-child frontmatter resolution per its §"Open questions" Q4 — which names this template's `requirements.yaml` explicitly as the Requirement-bearing child); `docs/HANDOVERS.md` §"Handover 6: Spec → Engineering Handoff Packet" (source-of-truth for the 23-file folder layout and the README frontmatter superset; quoted verbatim below); `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" and §"Universal metadata schema" and §"Lifecycle states" (frontmatter superset, ordering, folder-template layout, lifecycle enum — `Ready for Engineering` is in the enum so no enum override is needed); `context/frameworks/ontology.md` Domain H row "Handoff Packet" (line 150), Domain E rows "Requirement", "Feature", "Capability", "Acceptance Criteria", "Business Rule", "Non-Functional Requirement", and Domain G rows "Risk", "Mitigation" (the ontology types this composite touches); `.claude/commands/audit-completeness.md` §"The 25-item checklist" (the verification surface the 23 files collectively satisfy); ROADMAP F3.9 and P4.11.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `templates/handoff-packet/` — a folder template with `README.md` (Product Brief, carries universal-schema + HANDOVERS-6 frontmatter superset), `requirements.yaml` (structured YAML data file enumerating Requirement objects with ontology metadata per the parent convention's OQ4 resolution), and 21 narrative child files corresponding 1:1 to the remaining HANDOVERS-6 §"Folder contents" enumeration. The folder's shape — exactly 23 child files in the order HANDOVERS-6 names them — IS the contract: downstream commands (`/handoff-packet` P4.11) target these exact paths, and `/audit-completeness`'s 25-item checklist maps to content slices within these files. A kit user copies `templates/handoff-packet/` to `delivery/handoff-packets/<slug>/`, fills the README, then fills each child file as the packet's pre-engineering deliverable comes together.

## Objective

`templates/handoff-packet/` is the folder skeleton for the Handoff Packet artifact — the ontology's signature pre-engineering deliverable (Domain H, line 150 of `context/frameworks/ontology.md`) and the load-bearing scaffold underneath HANDOVERS Handover 6 (Spec → Engineering Handoff Packet). Today, a kit user wanting to assemble a packet has no copyable starting point: they would have to read HANDOVERS Handover 6 (which lists 23 required files plus a nine-key README frontmatter block including the `fixed_vs_flexible:` nested map), `docs/CONVENTIONS.md` §"Templates" (for folder-layout rules), the universal-metadata schema, the ontology Domain H row, the ontology Domain E + G rows that the per-file content references, the `/audit-completeness` 25-item checklist (the verification surface), the parent authoring convention, and `templates/_meta/template-skeleton.md`, then stitch them together themselves. They'd very likely (a) miss one or more of the 23 files (the count alone is the failure mode); (b) put frontmatter on the 21 narrative files where the parent convention's OQ4 explicitly says it doesn't belong; (c) leave `requirements.yaml` as a markdown file rather than a YAML data file with per-Requirement entries (the parent convention's OQ4 names this child explicitly as carrying "Requirement-level metadata"); (d) miss the four `*_review_passed:` audit-gate fields on the README that gate the packet's `Ready for Engineering` lifecycle transition; (e) miss the `fixed_vs_flexible:` block's three-key nested structure (`fixed:` / `flexible:` / `unknown:` lists of requirement ids). This template collapses that into one `cp -r templates/handoff-packet/ delivery/handoff-packets/<slug>/` followed by placeholder replacement. The folder's shape — README plus 22 additional file names in HANDOVERS-6's order — IS the contract.

The Handoff Packet is a **composite product artifact** (per ontology Domain H row "Handoff Packet — Final bundle to engineering") and HANDOVERS-6 makes the composition explicit: the README is the index plus Product Brief, the 21 narrative children carry the content slices that the `/audit-completeness` 25-item checklist verifies, and `requirements.yaml` is the structured-data child carrying the typed Requirement objects that the kit's traceability audits walk (every Requirement → Capability → Problem → Evidence per ontology §"Traceability rules" rule 1). This composite is the engineering team's actual consumable: HANDOVERS-6's "ready for engineering" test says the packet is ready when engineering can say "we understand the customer problem, the business objective, the required product behavior, what is fixed and what is flexible, the risks, how success will be measured, and which questions remain unresolved."

The closest prior context in the repo is `templates/_meta/template-skeleton.md` (the shape contract this template's README copies from), `templates/experiment/` (the F3.4 precedent folder template — sets the `mkdir + cp -r` pattern and the per-child frontmatter decisions), `templates/initiative/` (F3.7 — the second folder template; the immediate sibling in scope; sets the README + HANDOVERS-specific second frontmatter block pattern; ships in parallel with F3.9), and the `/audit-completeness` 25-item checklist (the verification surface this packet must satisfy at instantiation time — but not at template-shipping time; an empty template is not expected to pass the audit).

## Why now

ROADMAP F3.9 sits in the F3 block — the ten templates the parent `template-authoring-convention` spec made parallelizable. P4.11 (`/handoff-packet`) explicitly depends on F3.9: its `Depends on:` line in ROADMAP names this row plus F1.5. Until F3.9 ships, P4.11 is blocked, kit users assembling a handoff packet have nowhere to copy from, and the Delivery → Engineering boundary — the kit's most consequential phase boundary, since this is what engineering actually consumes — has no copyable starting point for the multi-file artifact that Handover 6 contracts. Shipping F3.9 unblocks P4.11 and gives kit users a one-line `cp -r` path into the layout the rest of the kit expects. The parent convention shipped 2026-05-22, so the contract surface F3.9 consumes is stable; F3.4 (`templates/experiment/`) and F3.7 (`templates/initiative/`) — the operative folder-template precedents — set the per-child frontmatter resolution pattern this spec consumes.

F3.9 is the third folder template in the kit (after `templates/_meta/` infrastructure, `templates/experiment/`, and `templates/initiative/`). It is the largest-file-count of all ten F3.x templates — 23 children — and the spec exists in part to encode the per-child frontmatter decisions explicitly across all 23 so kit users do not re-litigate them at instantiation time, and in part to encode the unusual `requirements.yaml`-as-YAML-data-file decision the parent convention's OQ4 anticipated.

## Inputs and outputs

**Inputs.**

- `templates/_meta/template-skeleton.md` — the canonical skeleton this template copies for its `README.md` (read-only; not edited by this spec).
- `docs/HANDOVERS.md` §"Handover 6: Spec → Engineering Handoff Packet" — source-of-truth for the 23-file folder-contents enumeration, the README's nine-key frontmatter block (including `fixed_vs_flexible:` nested map), and the "ready for engineering" semantic test. Quoted verbatim below.
- `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" — authoring convention. Specifically the "File layout" sub-section, which permits folder templates `templates/<slug>/` containing a `README.md` plus per-child-file templates where children carry their own frontmatter iff they instantiate a distinct ontology object.
- `docs/CONVENTIONS.md` §"Universal metadata schema" — universal frontmatter superset (inherited by the README).
- `docs/CONVENTIONS.md` §"Lifecycle states" — the canonical `LIFECYCLE_STATES` enum. `Ready for Engineering` is in the enum (`tools/lint-frontmatter.py` line 43), so the README's pre-filled `status: Ready for Engineering` value passes the default-mode linter on instantiation; **no enum override is needed for this template** (contrast F3.7, whose `status:` enum mismatch is its OQ1).
- `context/frameworks/ontology.md` Domain H row "Handoff Packet" (line 150: "Final bundle to engineering") — confirms the `object_type:` pre-fill value as the two-token `Handoff Packet`. Domain E row "Requirement" (line 90: "A specific condition the product must satisfy") — the typed object instantiated by `requirements.yaml` entries. Domain E rows "Feature", "Capability", "Acceptance Criteria", "Business Rule", "Non-Functional Requirement" and Domain G rows "Risk", "Mitigation" — the ontology types the per-file content references (but does not instantiate; those rows are tracked elsewhere in Domain E/G structures or inline in their respective files).
- `.claude/commands/audit-completeness.md` §"The 25-item checklist" — the verification surface the *instantiated* packet must satisfy. The empty template does not need to pass `/audit-completeness`; only the kit user's filled-in instantiation does. The template's job is to provide the file slots the checklist items map to (e.g., item 1 "Business objective is defined" → `business-objective.md`; item 25 "Decision log is current" → `decision-log.md`).
- `tools/lint-frontmatter.py --check-template` — the linter gate the README must pass. `requirements.yaml` is a YAML data file (not a markdown file with frontmatter) and is **not** subject to the markdown-frontmatter linter; the 21 narrative child files have no frontmatter and are not subject to the linter either.
- `scripts/tests/test_templates_instantiate.py` — discovery rule covers `templates/*/README.md`; this template's README is auto-discovered. Neither `requirements.yaml` nor the 21 narrative files are auto-discovered.
- Precedent: `templates/experiment/` (F3.4 — first folder template; `mkdir + cp -r` pattern) and `templates/initiative/` (F3.7 — second folder template; README + HANDOVERS-specific second frontmatter block pattern). F3.7 and F3.9 are the two F3.x rows the parent convention names explicitly under §"File layout" as multi-file templates.

**Outputs.**

1. `templates/handoff-packet/README.md` — new file. Product Brief + folder index. Universal-schema frontmatter (per skeleton, with `status:` pre-filled to `Ready for Engineering` AND accompanied by an inline HTML body warning that the four audit-gate date fields must be completed before the packet is actually handed off — see §"Boundaries → Always do" and OQ7 below for the rationale) plus the HANDOVERS-6-specific frontmatter block (the four `*_review_passed:` / `compliance_review_status:` gate fields, `engineering_partner:`, and the `fixed_vs_flexible:` nested map). Pre-filled: `object_type: Handoff Packet`. Body is an orientation paragraph plus three H2 sections matching the README's role as Product Brief + folder index (per §"Required sections" below — **Inferred from the F3.4 (`templates/experiment/`) README-as-index precedent plus HANDOVERS-6's "README.md ← Product Brief" gloss** since HANDOVERS-6 specifies the *folder contents*, not the README's *internal* sections; the README does NOT carry an `## Optional sections` block — the Handoff Packet README is a structured brief, not a freeform artifact, and the three H2s are exhaustive). Auto-discovered by `scripts/tests/test_templates_instantiate.py` via the `*/README.md` glob. **HANDOVERS-6 path-pointer drift note:** HANDOVERS-6 line 272 reads `README.md ← Product Brief (template in templates/handoff-brief.md)` — pointing to a path that will not exist once F3.9 ships, since this spec ships the template at `templates/handoff-packet/README.md`. Modifying HANDOVERS-6 is explicitly out of scope per §"Non-goals" below; the path-pointer correction is tracked as a CAPTURE-phase follow-on candidate (a one-line edit to HANDOVERS-6's gloss). Per the kit-drift policy: demote-and-annotate; never delete.
2. `templates/handoff-packet/requirements.yaml` — new file. **YAML data file** (not markdown; no markdown frontmatter). One YAML document containing a single top-level `requirements:` key whose value is a list of Requirement entries. Each entry has the ontology Requirement object's typed metadata (`id`, `object_type: Requirement`, `description`, `parent_capability`, `parent_feature`, `acceptance_criteria_ref`, `risk_level`, `owner`, `status`, `fixed_vs_flexible`). The `acceptance_criteria_ref` value is **the exact heading content** (e.g., `REQ-001`) that appears as a `### REQ-001` H3 in `acceptance-criteria.md` — the F1.4 `/audit-traceability` walker matches the H3 heading text verbatim, case-sensitive. No GitHub fragment-slug normalization. The `status` field accepts only product-artifact-track values (`Draft | In Review | Validated | Approved | Ready for Engineering`) — not kit-build-track states (`Shipped`, `Frozen`, `Implementing`); annotated inline in the placeholder comment. A single placeholder entry demonstrates the shape; the kit user duplicates entries on instantiation. **Resolves parent convention OQ4 verbatim** ("F3.9's `requirements.yaml` carries Requirement-level metadata").
3. `templates/handoff-packet/business-objective.md` — new file. **No frontmatter**. Body: H1 + one-paragraph orientation citing HANDOVERS-6 + the parent strategic intent + the linked Business Objective object. Maps to checklist item 1.
4. `templates/handoff-packet/customer-segment.md` — new file. No frontmatter. Body: H1 + orientation + a pointer-to-segment-definition section. Maps to checklist item 2.
5. `templates/handoff-packet/personas.md` — new file. No frontmatter (manifest pointing to `context/personas/*.md`; the persona objects themselves live there). Body: H1 + orientation + a markdown table with two columns (persona id, link). Maps to checklist item 3.
6. `templates/handoff-packet/problem.md` — new file. No frontmatter. Body: H1 + validated problem statement section + an `evidence:` sub-section enumerating source / strength / link (mirrors the universal-schema `evidence_basis:` structure as prose, not frontmatter). Maps to checklist items 4 and 5.
7. `templates/handoff-packet/jobs-to-be-done.md` — new file. No frontmatter. Body: H1 + orientation + repeated JTBD entry sub-template. Maps to checklist item 7.
8. `templates/handoff-packet/current-workflow.md` — new file. No frontmatter. Body: H1 + orientation + a numbered-list workflow-step sub-template. Maps to checklist item 6.
9. `templates/handoff-packet/future-workflow.md` — new file. No frontmatter. Body: H1 + orientation + a numbered-list workflow-step sub-template + a one-line callout naming the diff from `current-workflow.md`.
10. `templates/handoff-packet/capabilities.md` — new file. No frontmatter (registry pointing to the parent Initiative's `capabilities.md` per HANDOVERS-6's "from the parent initiative" gloss). Body: H1 + orientation + a markdown table with three columns (capability id, capability name, linked Problem). Maps to checklist item 10.
11. `templates/handoff-packet/features.md` — new file. No frontmatter. Body: H1 + orientation + a markdown table with three columns (feature id, feature name, **parent capability id — the traceability anchor for checklist item 11 "Features are mapped to capabilities" and for `/audit-traceability`'s downstream capability-to-feature walk; values must match capability ids enumerated in `capabilities.md` and referenced from `requirements.yaml` entries' `parent_capability:` field**). Maps to checklist item 11.
12. `templates/handoff-packet/business-rules.md` — new file. No frontmatter. Body: H1 + orientation + repeated `### <rule id> — <rule name>` sub-template with three labeled body fields (statement, source, related requirement ids). Maps to checklist item 14.
13. `templates/handoff-packet/policy-constraints.md` — new file. No frontmatter. Body: H1 + orientation + repeated `### <constraint id>` sub-template with three labeled body fields (statement, regulatory source, related requirement ids). Maps to checklist item 15.
14. `templates/handoff-packet/acceptance-criteria.md` — new file. No frontmatter. Body: H1 + orientation + repeated `### <requirement id>` sub-template with a bulleted list of acceptance criteria per requirement. Maps to checklist item 13.
15. `templates/handoff-packet/non-functional-requirements.md` — new file. No frontmatter. Body: H1 + orientation + repeated `### <NFR id>` sub-template with three labeled body fields (statement, target threshold, related requirement ids). Maps to checklist item 22 (operational implications) and partly item 12.
16. `templates/handoff-packet/risks.md` — new file. No frontmatter. Body: H1 + orientation + repeated `### <RISK-NNN>` sub-template with four labeled body fields (description, likelihood, impact, **mitigation**). The Mitigation sub-field on each Risk is the load-bearing mapping to checklist item 17 (mitigations or controls are assigned) — combined into one file rather than a separate `mitigations.md` because HANDOVERS-6's folder enumeration shows `risks.md ← with mitigations` as a single file.
17. `templates/handoff-packet/dependencies.md` — new file. No frontmatter. Body: H1 + orientation + a markdown table with three columns (dependency name, type — internal-team | external-vendor | upstream-system, blocker level). Maps to checklist item 18.
18. `templates/handoff-packet/open-questions.md` — new file. No frontmatter. Body: H1 + orientation + repeated `### <Q-NNN>` sub-template with three labeled body fields (question, owner, target resolution date). Maps to checklist item 19.
19. `templates/handoff-packet/out-of-scope.md` — new file. No frontmatter. Body: H1 + orientation + a bulleted list sub-template (one bullet per excluded item, with a parenthetical reason for exclusion). Maps to checklist item 20.
20. `templates/handoff-packet/decision-log.md` — new file. No frontmatter. Body: H1 + orientation citing `docs/adr/` as the canonical home for full ADRs and naming this file as the summary; a markdown table with three columns (decision date, decision summary, ADR link). Maps to checklist item 25.
21. `templates/handoff-packet/launch-considerations.md` — new file. No frontmatter. Body: H1 + orientation + three H2 sub-sections (`## Pricing and packaging`, `## Support and operational readiness`, `## Communications and rollout`). Maps to checklist items 21 (pricing/packaging) and 22 (support/operational).
22. `templates/handoff-packet/success-metrics.md` — new file. No frontmatter. Body: H1 + orientation + repeated `### <KPI-NNN> — <metric name>` sub-template with three labeled body fields (current baseline, target threshold, measurement window). Maps to checklist items 8 (desired outcomes) and 9 (KPIs).
23. `templates/handoff-packet/human-owned-decisions.md` — new file. No frontmatter (human-readable elaboration; the README's `human_owned_decisions:` frontmatter list is the machine-readable index). Body: H1 + orientation noting that the README's `human_owned_decisions:` list is the canonical machine-readable source + repeated `### <decision name>` sub-template with three labeled body fields (decision, owner, decision date or status). Maps to checklist item 23 (human-owned decisions explicitly marked — satisfied by this file's body) **and checklist item 24 (required approvals identified — satisfied by the dual mapping per HANDOVERS-6 line 314: this file's body PLUS the README's `approvals_obtained:` frontmatter field, both inspected by `/audit-completeness` step 4's "check approval" predicate)**.
24. `templates/_meta/README.md` — one-line append under "Shipped templates": `handoff-packet/` (folder template). CAPTURE-phase only; tiny dedicated commit per parent plan §Rollout to avoid races with future folder-template workers.
25. `ROADMAP.md` — F3.9 checkbox marked. CAPTURE-phase only.
26. `docs/specs/template-handoff-packet/spec.md` and `plan.md` frozen to `Status: Shipped (<date>)` / `Status: Done (<date>)` (CAPTURE phase only).

**Required HANDOVERS-6 frontmatter block (quoted verbatim from `docs/HANDOVERS.md` §"Handover 6: Spec → Engineering Handoff Packet").** This is the contract surface the README must shape:

```yaml
object_type: Handoff Packet
parent_initiative: <slug>
status: Ready for Engineering
completeness_audit_passed: <YYYY-MM-DD>
adversarial_review_passed: <YYYY-MM-DD>
quality_engineer_review_passed: <YYYY-MM-DD>
compliance_review_status: passed | not-required | <YYYY-MM-DD>
engineering_partner: <name>
fixed_vs_flexible:
  fixed: [<requirement ids that must not change>]
  flexible: [<requirement ids open to engineering tradeoffs>]
  unknown: [<questions for engineering to weigh in on>]
```

**Folder-contents enumeration (quoted verbatim from HANDOVERS-6).** This is the load-bearing list — 23 files, in this order:

> Folder contents (the ontology's section 28, 23 items, as files or as sections in a single brief):
>
> ```
> README.md                       ← Product Brief (template in templates/handoff-brief.md)
> business-objective.md           ← cite the strategic intent
> customer-segment.md             ← cite the segment definition
> personas.md                     ← linked persona files from context/personas/
> problem.md                      ← validated problem statement + evidence
> jobs-to-be-done.md
> current-workflow.md             ← how it works today
> future-workflow.md              ← how it'll work
> capabilities.md                 ← from the parent initiative
> features.md
> requirements.yaml               ← REQ-NNN files with full ontology metadata
> business-rules.md
> policy-constraints.md
> acceptance-criteria.md          ← per-requirement
> non-functional-requirements.md
> risks.md                        ← with mitigations
> dependencies.md
> open-questions.md
> out-of-scope.md
> decision-log.md                 ← summary; full ADRs in docs/adr/
> launch-considerations.md
> success-metrics.md              ← KPIs with thresholds
> human-owned-decisions.md
> ```

**HANDOVERS-6-vs-ROADMAP reconciliation.** ROADMAP F3.9's row reads "Handoff Packet template (`templates/handoff-packet/` with the 23 required sections from the ontology)" — the ROADMAP row counts 23 files, matching HANDOVERS-6. There is no F3.7-style ROADMAP-vs-HANDOVERS file-count mismatch here.

**`requirements.yaml` shape (the load-bearing per-child decision).** Per the parent convention's OQ4 resolution (which names this file explicitly), `requirements.yaml` carries Requirement-level ontology metadata. It is a YAML data file — **not a markdown file with YAML frontmatter** — and is structured as:

```yaml
requirements:
  - id: <REQ-NNN>
    object_type: Requirement
    description: <one-line statement of what must be true>
    parent_capability: <CAP-NNN>
    parent_feature: <FEAT-NNN>
    acceptance_criteria_ref: <ref into acceptance-criteria.md, e.g. the heading slug>
    risk_level: <Low | Medium | High | Critical>
    owner: <named human or role>
    status: <Draft | In Review | Validated | Approved | Ready for Engineering>
    fixed_vs_flexible: <fixed | flexible | unknown>
```

A single placeholder entry demonstrates the shape. The kit user duplicates the entry block on instantiation. The file is NOT processed by `tools/lint-frontmatter.py` (which only handles markdown frontmatter); it is NOT auto-discovered by `scripts/tests/test_templates_instantiate.py`. Mechanical validation of the YAML structure is by `python3 -c 'import yaml; yaml.safe_load(open("templates/handoff-packet/requirements.yaml"))'` returning exit 0 (T19 below).

**Required sections (per child file).**

For `README.md` (Product Brief + folder index — three H2 sections, ordered; **inferred from folder-index-plus-brief practice** since HANDOVERS-6 enumerates folder *contents*, not README *internal* sections):

1. **Product Brief** — one-paragraph restatement of what is being shipped, the customer it serves, and the strategic intent it advances. Pointer to `business-objective.md` for full elaboration. *(Inferred — Product Brief framing per HANDOVERS-6 line "README.md ← Product Brief".)*
2. **Folder index** — a markdown table listing the 22 sibling files (file name, one-line purpose). The table is pre-filled with all 22 entries so the kit user does not have to re-derive the layout. *(Inferred — folder-index navigation; the README is the entry point.)*
3. **Ready-for-engineering test** — short prose restating HANDOVERS-6's seven-clause "ready for engineering" semantic test (we understand the customer problem / business objective / required product behavior / what is fixed and flexible / risks / how success is measured / which questions remain). One line per clause. *(Inferred — HANDOVERS-6's "ready for engineering" test is the semantic gate; the README is the right surface for it.)*

For each of the 21 narrative child files: a single H1 + a short orientation paragraph + the file-specific sub-template described above in §"Outputs". The required-H1 strings for each child are pinned (see T8 family below). Inline HTML comments mark sources: `<!-- source: HANDOVERS-6 §"Folder contents" -->` on each file's H1 area for files whose presence is HANDOVERS-6-sourced; `<!-- source: inferred ... -->` on H2 sub-sections that go beyond what HANDOVERS-6 prescribes.

For `requirements.yaml`: a single top-level `requirements:` key with a YAML block-list of one placeholder Requirement entry whose ten keys are listed above. A top-of-file YAML comment line documents the source: `# Requirements registry — per HANDOVERS-6 §"Folder contents" and ontology §"Domain E — Requirement".`

**Downstream consumers.** ROADMAP P4.11 (`/handoff-packet`) reads `templates/handoff-packet/` as its scaffolding source. `/audit-completeness` (shipped as prose procedure; runnable script F1.5 shipped 2026-05-21) walks the 23 files at instantiation time and runs the 25-item checklist against the kit user's filled-in content — but does not run against the empty template. F1.4 `/audit-traceability` walks the Requirement entries in `requirements.yaml` per ontology traceability rule 1 (every Requirement must trace to a Capability) — again, only on instantiated packets, not on the empty template.

## Boundaries

### Always do

- Use the folder layout `templates/handoff-packet/` with exactly **23** child files, named and ordered per HANDOVERS-6's "Folder contents" block quoted above. File names pinned by HANDOVERS-6. `handoff-packet/` is the third folder template in the kit (after `experiment/` and `initiative/`) and is authorized by the parent convention §"File layout" plus the parent spec's enumeration "Multi-file template (folders such as Initiative, Handoff Packet)" — language naming this template explicitly.
- Use angle-bracket placeholder syntax exclusively (`<descriptor>`) in the README and the 21 narrative child files; inherit the skeleton's placeholder discipline. In `requirements.yaml` the placeholder syntax is also angle-bracket (`<REQ-NNN>`, `<one-line statement of what must be true>`, etc.) — the YAML parser tolerates angle brackets inside double-quoted strings; the file uses unquoted scalar values where YAML's plain-scalar rules permit angle brackets (which they do, since `<` is not a YAML indicator at the start of a scalar). Where ambiguous, double-quote the placeholder (e.g., `description: "<one-line statement of what must be true>"`). The augmented-placeholder rule (e.g., `<Low | Medium | High | Critical>`) is accepted by the parent linter's `AUGMENTED_PLACEHOLDER` rule on the README and is mirrored in `requirements.yaml` for human-facing clarity (YAML processes it as a plain string scalar).
- Quote HANDOVERS-6's frontmatter block on the README verbatim (with placeholder substitution where the value is the kit-user's choice). The nine HANDOVERS-6 fields (`object_type`, `parent_initiative`, `status`, `completeness_audit_passed`, `adversarial_review_passed`, `quality_engineer_review_passed`, `compliance_review_status`, `engineering_partner`, `fixed_vs_flexible`) appear in the README exactly as in HANDOVERS-6. `fixed_vs_flexible` is a nested map with exactly three sub-keys (`fixed`, `flexible`, `unknown`) each carrying a YAML inline-list placeholder.
- Pre-fill the template's identity fields on the README: `object_type: Handoff Packet` and `status: Ready for Engineering`. Unlike F3.7's `status:` enum mismatch (its OQ1), the value `Ready for Engineering` is in `LIFECYCLE_STATES` (`tools/lint-frontmatter.py` line 43), so the default-mode linter on an instantiated packet accepts the value. No enum override is needed. **However:** pre-filling `Ready for Engineering` on an empty skeleton creates a silent-theatre risk — a kit user who copies the template and pushes without running `/audit-completeness` would have an artifact whose `status:` already says ready while the four audit-gate date fields are still placeholders. Mitigation: a mandatory inline HTML body warning comment immediately under the `status:` line in the template body (per plan step 2) reads `<!-- WARNING: pre-filled to satisfy LIFECYCLE_STATES; the four audit-gate date fields above (completeness_audit_passed / adversarial_review_passed / quality_engineer_review_passed / compliance_review_status) MUST be completed with concrete values before this packet is handed to engineering. -->`. Tracked as OQ7 below.
- `compliance_review_status:` field is **not enum-checked by the linter** (only the universal-schema `status:` field is — per `tools/lint-frontmatter.py` line 243; no per-field enum constraint exists for `compliance_review_status:`). The template pre-fill uses the augmented-placeholder form `<passed | not-required | <YYYY-MM-DD>>` (parser-tolerated under `--check-template`); on instantiation, the kit user replaces the placeholder with one of the three concrete forms (`passed`, `not-required`, or a YYYY-MM-DD date string) and the default-mode linter passes the value through without enum check. T6 tests the augmented-placeholder form is present in the template.
- The README does NOT carry an `## Optional sections` block. Unlike single-file templates that inherit the skeleton's `## Optional sections` heading, the Handoff Packet README is a structured Product Brief + folder index; its three H2 sections are exhaustive (T8b asserts the three are present in order; the absence of a fourth H2 is implicit by reading the README as authored).
- **Traceability field retention.** From the skeleton's traceability block, **retain** `parent_intent` (restated for upstream traceability), `parent_initiative` (HANDOVERS-6 explicitly requires it; goes in its universal-schema traceability-block position per the dedup convention; the Handoff Packet's direct parent is the Initiative), `parent_vision` (the Initiative's parent; restated for upstream traceability per the Vision-template precedent). **Delete** `parent_opportunity` and `parent_learning` from the README's traceability block — HANDOVERS-6 does not require them, and by the time the packet is being assembled the Validation learning has long since fed into the Initiative.
- Keep the README's universal-schema frontmatter block ordering identical to `templates/_meta/template-skeleton.md` (the parent convention pins ordering). Append HANDOVERS-6-specific fields **not present in the universal schema** (`completeness_audit_passed`, `adversarial_review_passed`, `quality_engineer_review_passed`, `compliance_review_status`, `engineering_partner`, `fixed_vs_flexible`) after a `# Handover-specific fields (per HANDOVERS.md Handover 6)` YAML comment line inside the same `---`...`---` frontmatter block. The README's frontmatter is a **single YAML document** delimited by exactly one pair of `---` markers; the "second block" is a logical grouping under a YAML-comment separator, not a second `---`-delimited document. (Two `---` pairs would only get the first parsed by the linter — same constraint as F3.7.)
- Cross-cutting dedup convention. Where HANDOVERS-6 fields overlap with the universal-metadata schema (e.g., `status:` — present in the universal schema and in HANDOVERS-6 with the value `Ready for Engineering`; `parent_initiative:` — present in both with the same semantic), the field appears **once** in its universal-schema position carrying the HANDOVERS-6-mandated value. The handover-specific second block carries only fields not present in the universal schema.
- For all 21 narrative child files: **no YAML frontmatter**. Begin the file with the H1 heading. This is the OQ4 resolution from the parent convention applied to F3.9: child files carry frontmatter only when they instantiate a distinct ontology object. None of the 21 narrative files do; they are content slices that the `/audit-completeness` 25-item checklist verifies.
- For `requirements.yaml`: a YAML data file with one top-level `requirements:` key. **No markdown frontmatter** (the file is not markdown). The Requirement entries inside the YAML list carry the ontology Requirement object's metadata directly as YAML keys (`id`, `object_type: Requirement`, etc.) — this is the parent convention's OQ4 "Requirement-level metadata" verbatim.
- Pass `tools/lint-frontmatter.py --check-template templates/handoff-packet/README.md` and `python3 -m pytest scripts/tests/test_templates_instantiate.py` cleanly before CAPTURE.
- Pass `python3 -c 'import yaml; yaml.safe_load(open("templates/handoff-packet/requirements.yaml"))'` cleanly before CAPTURE (mechanical YAML-parse gate; the kit's stdlib-only constraint is honored because `pyyaml` is already a kit dependency consumed by `scripts/lib/frontmatter.py`).
- Cite HANDOVERS-6 inline in the README body's opening blockquote so a reader scanning the markdown knows the source contract. Cite the 25-item checklist (`/audit-completeness`) inline in the README body as the audit surface the packet must satisfy on instantiation.

### Ask first

- Adding a frontmatter field to the README not present in `docs/CONVENTIONS.md` §"Universal metadata schema" or `docs/HANDOVERS.md` §"Handover 6". The convention is downstream of those two docs.
- Adding YAML frontmatter to any of the 21 narrative non-README child files. The OQ4 resolution is explicit and any per-child frontmatter would require ontology evidence that the child instantiates a distinct typed object.
- Adding a 24th required child file, or removing one of the 23. The folder contents are pinned by HANDOVERS-6; changing the count requires editing HANDOVERS-6, which is out of scope here.
- Pre-filling `engineering_partner:` with a literal name. The field is the kit-user's choice; pre-filling would imply a default engineering partner exists, which would be misleading.
- Pre-filling `compliance_review_status:` with `passed` or `not-required`. The field is the kit-user's choice; pre-filling either value would imply a default compliance posture, which would be misleading. The augmented placeholder `<passed | not-required | <YYYY-MM-DD>>` is the safe pre-fill (and matches HANDOVERS-6 verbatim).

### Never do

- Invent domain content. The body of each child file is shape-only: H1, optional H2/H3 headings, plus `<placeholder>` body fields. No example business objectives, no real personas, no real Requirement ids, no real risks.
- Use `{{...}}` or `__FILL__` placeholder syntax anywhere across the 23 files. The parent convention permits angle-bracket only.
- Rename any child file. The names are pinned by HANDOVERS-6 — any other name silently bypasses `/audit-completeness`'s checklist-to-file mapping and `/audit-traceability`'s Requirement-walk.
- Add YAML frontmatter to any of the 21 narrative child files. Per OQ4 resolution; documented as a positive contract not just an omission.
- Add markdown frontmatter to `requirements.yaml`. The file is not markdown.
- Pre-fill the four audit-gate date fields (`completeness_audit_passed`, `adversarial_review_passed`, `quality_engineer_review_passed`, `compliance_review_status`) with concrete dates or `passed` values. These are audit-outcome lockfields the kit user records after running the corresponding audits; pre-filling would defeat the lockfield's purpose. The augmented placeholders `<YYYY-MM-DD>` for the three date fields and `<passed | not-required | <YYYY-MM-DD>>` for `compliance_review_status:` are the safe values. The plan, spec verbatim quote of HANDOVERS-6, and T6 all use the same augmented-placeholder form consistently.
- Add `## Optional sections` to the README. The Handoff Packet README is a structured brief — its three H2s are exhaustive. (Inherited skeleton `## Optional sections` heading is removed on copy-adapt; see plan §"Approach" step 2.)
- Add `Product Brief`, `Requirement Registry`, `Audit Lockfield`, or any other ad-hoc ontology type. The parent convention's "Never do — Add … as an ontology type" rule applies; templates are kit-build scaffolding, not ontology-type-creation sites.
- Modify `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, `scripts/tests/test_templates_instantiate.py`, or `templates/_meta/template-skeleton.md`. The parent contract surface is committed; F3.9 is a downstream consumer only. If adversarial review surfaces a contradiction, resolve via a separate spec.
- Walk `templates/handoff-packet/` from the default-mode linter. The linter contract (parent spec) keeps `templates/` outside `PHASE_DIRS`; only `--check-template` runs against it, and only against the README (the other 22 files are either YAML or have no frontmatter).
- Combine multiple HANDOVERS-6 files into one. The 23-file layout is pinned; combining `risks.md` and `dependencies.md` (or any pair) into one file silently bypasses `/audit-completeness`'s file-level checklist mapping.
- Split one HANDOVERS-6 file into multiple. Same reason. In particular, do **not** split `risks.md` (which HANDOVERS-6 explicitly notes "← with mitigations") into separate `risks.md` and `mitigations.md` files.

## Verification mode

- **Goal-based check** for the template's shape — required headings present on each child file; required frontmatter keys present on the README (incl. HANDOVERS-6 block keys); placeholder-syntax purity; child-file existence and count (23 exact); absence of frontmatter on the 21 narrative files; YAML well-formedness of `requirements.yaml`. Each check is a one-line shell or python predicate.
- **Audit-driven** for the linter and pytest gates: `python3 tools/lint-frontmatter.py --check-template templates/handoff-packet/README.md` exits 0; `python3 -m pytest scripts/tests/test_templates_instantiate.py` (which auto-discovers `templates/handoff-packet/README.md` via the `*/README.md` glob) exits 0; `bash tools/pre-pr.sh` exits 0.
- **Adversarial review** (manual gesture against the shipped template files) — dispatch the `adversarial-reviewer` subagent against the 23 files versus HANDOVERS §"Handover 6", the parent authoring convention, ontology Domain H + E + G, and the `/audit-completeness` 25-item checklist mapping. Iterate fixes inline; max 3 review passes per the work-loop default. The reviewer should specifically check: (a) the 21 narrative files carry no frontmatter; (b) `requirements.yaml` is a YAML data file with no markdown frontmatter and parses with `yaml.safe_load`; (c) the README's HANDOVERS-6 block matches verbatim including the `fixed_vs_flexible:` nested map; (d) the 25-item checklist's file-mapping is complete and unambiguous (every checklist item maps to one or more files in the template); (e) the inferred sections (README's three H2s) are flagged with source comments.

The template is done when T1–T22 all pass (T1–T19 at VERIFY time; T20, T20b, T21 at CAPTURE time; T22 at REVIEW time).

## Checklist-to-file mapping (T19 input)

This is the literal mapping T19 loads into its python one-liner. Encoded as a YAML dictionary for unambiguous copy-paste into the EXECUTE-phase test code. Every checklist item ∈ {1..25} appears as a key; each value is the list of files (and/or frontmatter-field references) the kit user populates to satisfy that item. Items 5, 17, 22, 24 have multi-target mappings per `/audit-completeness` step 2.5 and HANDOVERS-6 line 314.

```yaml
checklist_to_files:
  1:  [business-objective.md]
  2:  [customer-segment.md]
  3:  [personas.md]
  4:  [problem.md]
  5:  [problem.md, requirements.yaml]                       # evidence: problem.md body + acceptance_criteria_ref chain
  6:  [current-workflow.md]
  7:  [jobs-to-be-done.md]
  8:  [success-metrics.md]
  9:  [success-metrics.md]
  10: [capabilities.md]
  11: [features.md]                                          # parent capability id column = traceability anchor
  12: [requirements.yaml]
  13: [acceptance-criteria.md]
  14: [business-rules.md]
  15: [policy-constraints.md]
  16: [risks.md]
  17: [risks.md]                                             # Mitigation sub-field within each Risk H3 block
  18: [dependencies.md]
  19: [open-questions.md]
  20: [out-of-scope.md]
  21: [launch-considerations.md]                             # ## Pricing and packaging H2
  22: [launch-considerations.md, non-functional-requirements.md]  # ## Support and operational readiness H2 + NFR file
  23: [human-owned-decisions.md]
  24: [human-owned-decisions.md, README.md:approvals_obtained]    # body PLUS README frontmatter (HANDOVERS-6 line 314)
  25: [decision-log.md]
```

The `README.md:approvals_obtained` notation in item 24 denotes a frontmatter-field target on the README (not a separate file). T19 normalizes this to "the README file" for the file-existence check; the frontmatter-field-presence semantic is verified by `/audit-completeness` on instantiated packets, not by T19 on the empty template.

## Contract tests

Each test is one shell line or one pytest case.

- `T1` — folder + all 23 child files exist. Asserted by one shell line: `test -d templates/handoff-packet && for f in README.md business-objective.md customer-segment.md personas.md problem.md jobs-to-be-done.md current-workflow.md future-workflow.md capabilities.md features.md requirements.yaml business-rules.md policy-constraints.md acceptance-criteria.md non-functional-requirements.md risks.md dependencies.md open-questions.md out-of-scope.md decision-log.md launch-considerations.md success-metrics.md human-owned-decisions.md; do test -f "templates/handoff-packet/$f" || exit 1; done` exits 0.
- `T1b` — the folder contains **exactly 23** files and no extras. Asserted by `[ "$(ls templates/handoff-packet/ | wc -l | tr -d ' ')" = "23" ]` exits 0. Mechanical guard against silent file-count drift.
- `T2` — `python3 tools/lint-frontmatter.py --check-template templates/handoff-packet/README.md` exits 0.
- `T3` — README frontmatter contains the universal-schema key set inherited from the skeleton (asserted by a python one-liner that parses YAML and checks every skeleton-required top-level key — `id`, `slug`, `object_type`, `name`, `description`, `owner`, `status`, `priority`, `risk_level`, `created`, `last_updated`, plus the traceability, evidence, human-ownership, and open-items blocks — is present).
- `T4` — README frontmatter contains the six HANDOVERS-6-specific keys not present in the universal schema: `completeness_audit_passed`, `adversarial_review_passed`, `quality_engineer_review_passed`, `compliance_review_status`, `engineering_partner`, `fixed_vs_flexible`. Asserted by a python one-liner.
- `T4b` — README's `fixed_vs_flexible:` value is a YAML map with exactly three sub-keys: `fixed`, `flexible`, `unknown`. Asserted by a python one-liner that parses YAML and inspects the nested structure.
- `T4c` — README frontmatter retains `parent_initiative` (HANDOVERS-6 requires it; this test pins its presence in case the author over-trims the traceability block while deleting Initiative-irrelevant fields). Asserted by `grep -c '^parent_initiative:' templates/handoff-packet/README.md` returns 1.
- `T5` — README's `object_type` value is exactly `Handoff Packet` and `status` value is exactly `Ready for Engineering` (pre-fill — both values are in their respective enums; no augmented-placeholder syntax). Asserted by a python one-liner that parses YAML and inspects the two values.
- `T6` — README's four audit-gate fields carry safe augmented-placeholder values, not concrete dates or `passed` literals. `completeness_audit_passed`, `adversarial_review_passed`, `quality_engineer_review_passed` each match the augmented-placeholder pattern `<YYYY-MM-DD>`; `compliance_review_status` matches `<passed | not-required | <YYYY-MM-DD>>` (the HANDOVERS-6 form with nested angle brackets is allowed inside the outer placeholder). Asserted by a python one-liner.
- `T7` — None of the 21 narrative child files carries YAML frontmatter (no `---` delimiter in the first 5 lines). Asserted by a shell loop: `for f in business-objective.md customer-segment.md personas.md problem.md jobs-to-be-done.md current-workflow.md future-workflow.md capabilities.md features.md business-rules.md policy-constraints.md acceptance-criteria.md non-functional-requirements.md risks.md dependencies.md open-questions.md out-of-scope.md decision-log.md launch-considerations.md success-metrics.md human-owned-decisions.md; do [ "$(head -5 "templates/handoff-packet/$f" | grep -c '^---')" = "0" ] || exit 1; done` exits 0. (Absence-of-`---` is the load-bearing predicate.)
- `T7b` — `requirements.yaml` has no markdown frontmatter delimiter (the file is YAML; a `---` at line 1 would be a YAML document separator, which is allowed but unnecessary; the linter only matters for markdown files and does not touch this one). Asserted by `head -1 templates/handoff-packet/requirements.yaml | grep -c '^---'` returns 0 (we choose: do not lead with a `---`; lead with a `# ...` YAML comment for human readability and so the YAML parser treats the file as a single document with the comment as preface).
- `T8` — Required H1 headings present on each of the 23 files. Asserted by a shell loop that greps for the file-specific H1 strings:
  - README → `# Handoff Packet`
  - business-objective.md → `# Business objective`
  - customer-segment.md → `# Customer segment`
  - personas.md → `# Personas`
  - problem.md → `# Problem`
  - jobs-to-be-done.md → `# Jobs to be done`
  - current-workflow.md → `# Current workflow`
  - future-workflow.md → `# Future workflow`
  - capabilities.md → `# Capabilities`
  - features.md → `# Features`
  - business-rules.md → `# Business rules`
  - policy-constraints.md → `# Policy constraints`
  - acceptance-criteria.md → `# Acceptance criteria`
  - non-functional-requirements.md → `# Non-functional requirements`
  - risks.md → `# Risks`
  - dependencies.md → `# Dependencies`
  - open-questions.md → `# Open questions`
  - out-of-scope.md → `# Out of scope`
  - decision-log.md → `# Decision log`
  - launch-considerations.md → `# Launch considerations`
  - success-metrics.md → `# Success metrics`
  - human-owned-decisions.md → `# Human-owned decisions`
  - (`requirements.yaml` is YAML; no H1 — skipped from this test.)
  - Each predicate is `grep -c '^# <heading>$' templates/handoff-packet/<file>` returns >= 1.
- `T8b` — README required H2 headings present in order, and **exactly three H2 headings exist** (no `## Optional sections` or any fourth H2). Asserted by `grep -c '^## ' templates/handoff-packet/README.md` returns `3` AND `grep -n '^## ' templates/handoff-packet/README.md` returns the three expected lines (`## Product brief`, `## Folder index`, `## Ready-for-engineering test`) in that order.
- `T8c` — `launch-considerations.md` required H2 headings present: `## Pricing and packaging`, `## Support and operational readiness`, `## Communications and rollout`. Asserted by `grep -n`.
- `T9` — README's folder-index table contains rows naming all 22 sibling files. Asserted by a shell loop: `for f in business-objective.md customer-segment.md personas.md problem.md jobs-to-be-done.md current-workflow.md future-workflow.md capabilities.md features.md requirements.yaml business-rules.md policy-constraints.md acceptance-criteria.md non-functional-requirements.md risks.md dependencies.md open-questions.md out-of-scope.md decision-log.md launch-considerations.md success-metrics.md human-owned-decisions.md; do grep -c "$f" templates/handoff-packet/README.md > /dev/null || exit 1; done` exits 0.
- `T10` — `risks.md` body sub-template references a Mitigation field (per HANDOVERS-6's "← with mitigations" annotation): `grep -ic 'mitigation' templates/handoff-packet/risks.md` returns >= 1.
- `T11` — `decision-log.md` body cites `docs/adr/`: `grep -c 'docs/adr' templates/handoff-packet/decision-log.md` returns >= 1.
- `T12` — `personas.md` body references `context/personas/`: `grep -c 'context/personas' templates/handoff-packet/personas.md` returns >= 1.
- `T13` — Angle-bracket-only placeholder syntax across all 23 files: `grep -rc '{{' templates/handoff-packet/` returns 0 (sum across files) and `grep -rc '__FILL__' templates/handoff-packet/` returns 0.
- `T14` — `requirements.yaml` parses as YAML: `python3 -c 'import yaml,sys; yaml.safe_load(open("templates/handoff-packet/requirements.yaml")); sys.exit(0)'` exits 0.
- `T15` — `requirements.yaml` top-level structure is `{requirements: [...]}` and the first list entry carries the ten Requirement-metadata keys (`id`, `object_type`, `description`, `parent_capability`, `parent_feature`, `acceptance_criteria_ref`, `risk_level`, `owner`, `status`, `fixed_vs_flexible`). Asserted by a python one-liner.
- `T15b` — `requirements.yaml`'s first entry has `object_type: Requirement` (matches ontology Domain E row). Asserted by a python one-liner.
- `T16` — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (the parametrized `test_template_passes_check_template_mode` test includes `templates/handoff-packet/README.md` via the `*/README.md` glob; the other 22 files are not auto-discovered, which is the load-bearing OQ4 resolution).
- `T17` — `bash tools/pre-pr.sh` exits 0 (kit-wide health check after the template lands).
- `T18` — `python3 tools/lint-frontmatter.py --all` exits 0 (default mode does not traverse `templates/handoff-packet/**` — mode-separation by non-traversal, identical to F3.4's T11 and F3.7's T15).
- `T19` — `/audit-completeness` checklist file-mapping is complete: every one of the 25 checklist items maps to at least one of the 23 files (or to the README's `approvals_obtained:` frontmatter field, per the item-24 dual-target mapping). Asserted by a python one-liner that loads the literal mapping dict from §"Checklist-to-file mapping" above as a python `dict[int, list[str]]` and checks (a) every key ∈ {1..25} is present, (b) every value list is non-empty, (c) every plain filename in any value list refers to a file that exists in `templates/handoff-packet/`, (d) the one frontmatter-field reference (`README.md:approvals_obtained`) normalizes to a file that exists. **NOTE:** This is a static structural check at the template level; it does NOT run the audit against an empty template (an empty template would correctly fail the audit). The mapping itself is the contract surface this test guards.
- `T20` — ROADMAP F3.9 checkbox flipped (CAPTURE-phase predicate): `grep -c '^- \[x\] \*\*F3\.9\*\*' ROADMAP.md` returns 1.
- `T20b` — ROADMAP F3.9 row's prose unchanged from its shipped form (since the row's prose already enumerates `templates/handoff-packet/` correctly with no count mismatch — contrast F3.7's row, which needed a prose update for `capabilities.md`). Asserted by `grep -E '\*\*F3\.9\*\*.*templates/handoff-packet/.*23 required sections' ROADMAP.md` returns 1.
- `T21` — `templates/_meta/README.md` lists the template (CAPTURE-phase predicate): `grep -c 'handoff-packet/' templates/_meta/README.md` returns >= 1.
- `T22` — Adversarial-reviewer subagent returns 0 Blocking findings against the 23 shipped files versus HANDOVERS §"Handover 6", parent authoring convention, ontology Domain H + E + G, and `/audit-completeness`'s 25-item checklist mapping.

## Non-goals

- Authoring an instantiated handoff packet under `delivery/handoff-packets/<slug>/`. F3.9 ships the skeleton; the kit user (or P4.11 `/handoff-packet` when shipped) instantiates the artifact.
- Building P4.11 (`/handoff-packet`). Separate ROADMAP row; F3.9 unblocks it but does not implement it.
- Making the empty template pass `/audit-completeness`. The audit is a verification surface for the *instantiated* packet, not the empty template; an empty template would (correctly) fail every checklist item. The template's job is to provide the 23 file slots the checklist items map to.
- Modifying `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, or `scripts/tests/test_templates_instantiate.py`. The pytest harness auto-discovers `templates/handoff-packet/README.md` via the `*/README.md` glob; F3.9 needs no test-harness wiring. The 22 non-README files (21 narrative + 1 YAML) are intentionally outside the linter's discovery scope; this is the OQ4 resolution.
- Adding `tools/new-template.sh` or any folder-template scaffolder. Out of scope per parent spec's §Non-goals.
- Adding F3.8 (`templates/pm-spec.md`) child-spec instances under `templates/handoff-packet/`. The packet is downstream of the spec; it does not host spec templates.
- Adding a `templates/handoff-packet/CLAUDE.md`-style per-template guidance file. The README plus the spec are sufficient.
- Authoring F3.7 (`templates/initiative/`). Separate parallel F3 row; the other folder template in the F3 block.
- Defining or extending the ontology's Requirement, Risk, Mitigation, or related Domain E/G types. The template instantiates `object_type: Requirement` inside `requirements.yaml` entries; it does not define new types.
- Validating Mermaid syntax. Unlike F3.7, this template does not ship Mermaid blocks (none of the 23 files require them; `current-workflow.md` and `future-workflow.md` use numbered-list workflows, not diagrams).

## Open questions

1. **Single-file-brief alternative to the 23-file folder layout.** HANDOVERS-6 says "23 items, as files or as sections in a single brief." A single-file brief variant would put all 23 sections into one markdown file. Resolved here: ship the **folder** variant only (per ROADMAP F3.9's row, which says "`templates/handoff-packet/` with the 23 required sections"). The single-file-brief alternative is deferred to a separate spec if a kit user requests it; the folder variant is HANDOVERS-6's canonical form (its `delivery/handoff-packets/<slug>/` instantiation path is folder-shaped).
2. **`requirements.yaml` per-entry frontmatter granularity.** The parent convention's OQ4 names this file as carrying "Requirement-level metadata" but does not enumerate the exact key set. Resolved here: ten keys per entry (`id`, `object_type: Requirement`, `description`, `parent_capability`, `parent_feature`, `acceptance_criteria_ref`, `risk_level`, `owner`, `status`, `fixed_vs_flexible`). The choice is derived from ontology Domain E row "Requirement" plus the traceability rules ("every Requirement must trace to a Capability") plus the HANDOVERS-6 frontmatter's `fixed_vs_flexible:` field (Requirements are the elements that get classified into fixed/flexible/unknown). If adversarial review rejects the key set, iterate within the 3-pass limit.
3. **README internal H2 sections are inferred, not HANDOVERS-sourced.** HANDOVERS-6 specifies the folder *contents* but not the README's *internal* sections. Resolved here: three H2 sections (`Product brief`, `Folder index`, `Ready-for-engineering test`) inferred from HANDOVERS-6's "Product Brief" framing and its seven-clause "ready for engineering" test. Each H2 in the body carries an inline HTML comment `<!-- source: inferred -->`. If adversarial review rejects the inferred taxonomy, iterate within the 3-pass limit.
4. **Sub-section taxonomy for the 21 narrative child files.** HANDOVERS-6 names the 23 files but does not prescribe each file's internal sub-section structure. Resolved here: each narrative child gets a single H1 + one orientation paragraph + a file-specific sub-template (markdown table, repeated H3 sub-blocks, numbered list, or H2 sub-sections — see §"Outputs" 3–23). Each H2 or H3 sub-template carries an inline HTML comment marking source: HANDOVERS-6 where the gloss line names the structure (`"with mitigations"`, `"per-requirement"`, `"summary; full ADRs in docs/adr/"`), inferred otherwise. If adversarial review rejects a sub-template, iterate per-file within the 3-pass limit. The default sub-structure choice is the lightest shape that lets `/audit-completeness` find the corresponding checklist item.
5. **`/audit-completeness` checklist-to-file mapping.** The mapping in §"Outputs" 3–23 is canonical for this spec. Some checklist items map to multiple files (e.g., item 5 "Evidence is attached to the problem" maps to `problem.md`'s evidence sub-section AND any inline evidence links in `requirements.yaml` entries via `acceptance_criteria_ref`); some files satisfy multiple items (e.g., `launch-considerations.md` covers items 21 and 22; `risks.md` covers items 16 and 17). Resolved here: the mapping is encoded only in this spec (it does not live in HANDOVERS-6 or `/audit-completeness`'s command file). If `/audit-completeness` later gains a machine-readable mapping table, this spec's mapping becomes the input. T19 mechanically validates that every checklist item ∈ {1..25} has at least one file in the mapping.
6. **YAML well-formedness vs YAML semantic correctness on `requirements.yaml`.** T14 / T15 / T15b validate well-formedness and shape but do not validate that each entry's `parent_capability:` actually exists (capability resolution is the kit user's job at instantiation time; the template's placeholder is `<CAP-NNN>`). Resolved here: structural validation only at template-ship time; full semantic validation runs via `/audit-traceability` on the instantiated packet. The template-level T15 is a known shape gate, not a semantic one.
7. **Status pre-fill on empty skeleton vs silent-theatre risk.** The README pre-fills `status: Ready for Engineering` because the value is in `LIFECYCLE_STATES`. But a freshly-copied skeleton then technically reads "ready for engineering" while the four audit-gate fields are still placeholders. Resolved here: keep the concrete pre-fill but add a mandatory inline HTML body warning comment immediately under the `status:` line (per §"Boundaries → Always do" above). The alternative — switching to the augmented placeholder `<Ready for Engineering>` — would defeat the convenience of a copy-able default and would require T5 to switch from concrete-value match to augmented-placeholder match. If adversarial review during EXECUTE rejects the warning-comment mitigation, the fallback is the augmented-placeholder form. Either way, this is the kit's most consequential phase boundary; the OQ is recorded as load-bearing.
8. **`capabilities.md` pointer model loses traceability if the parent initiative is renamed.** The Handoff Packet's `capabilities.md` re-states the Capability list from the parent Initiative (per HANDOVERS-5's Initiative contract — the canonical source of `capabilities:` for the parent Initiative). The pointer is prose-only. If `/audit-traceability` later gains cross-file capability-sync checking, the walk has no machine-readable anchor. Resolved here: the template body includes a `<!-- source: parent Initiative's capabilities list per HANDOVERS-5; canonical source remains the Initiative; copy and maintain in sync. -->` HTML comment at the top of the `capabilities.md` body (per plan step 10). Machine-readable cross-file capability-sync is deferred to a separate spec (likely paired with the `/audit-traceability` extension that needs it).
9. **"orientation paragraph" definition across 21 narrative files.** The spec says each narrative child file has "H1 + one-paragraph orientation" but does not define what orientation must accomplish. Resolved here: each narrative child file's orientation paragraph must name (a) the `/audit-completeness` checklist item(s) it satisfies, (b) the HANDOVERS-6 gloss line that names the file (where one exists), and (c) a pointer to where the corresponding content is elaborated or linked upstream. The plan's per-file approach steps 3–24 each include these orientation constraints. If adversarial review during EXECUTE finds an orientation paragraph that satisfies the count predicate but not the content predicate, fix in-session.
10. **Inferred-section source traceability.** Where the spec marks a section as "Inferred from ... practice", the source path is `templates/experiment/README.md` (F3.4 precedent of README-as-folder-index) plus HANDOVERS-6's gloss text. Resolved here: each H2 in the README body carries an inline HTML comment naming the source — either `<!-- source: HANDOVERS-6 gloss "<text>" -->` where HANDOVERS-6 provides text, or `<!-- source: inferred per F3.4 README-as-index precedent -->` where the section is fully inferred. This is a positive contract; a missing source comment fails T8b's spirit (though T8b's mechanical grep only checks heading presence).
11. **Review finding triage discipline.** The plan's iteration cap (3 passes) applies equally to all findings unless triaged. Resolved here: findings are triaged Block / Needs-fix / Defer per the work-loop skill's REVIEW phase. **Block** findings must be resolved before marking `plan_review_status = "approved"` (PLAN phase) or before VERIFY (EXECUTE phase). **Needs-fix** findings must be resolved in-session in the same loop. **Defer** findings are added as new OQs in the spec and tracked as follow-on ROADMAP candidates; they do not block the loop. The iteration cap counts only iterations that produced new Block or Needs-fix findings.

## Acceptance criteria

- [ ] `templates/handoff-packet/` folder exists with all 23 child files in HANDOVERS-6's order (asserted by T1).
- [ ] Folder contains exactly 23 files, no extras (asserted by T1b).
- [ ] README passes `python3 tools/lint-frontmatter.py --check-template templates/handoff-packet/README.md` (asserted by T2).
- [ ] README frontmatter contains every key in the universal-schema set (asserted by T3).
- [ ] README frontmatter contains the six HANDOVERS-6-specific keys: `completeness_audit_passed`, `adversarial_review_passed`, `quality_engineer_review_passed`, `compliance_review_status`, `engineering_partner`, `fixed_vs_flexible` (asserted by T4).
- [ ] README `fixed_vs_flexible:` is a YAML map with exactly three sub-keys: `fixed`, `flexible`, `unknown` (asserted by T4b).
- [ ] README retains `parent_initiative:` per HANDOVERS-6 (asserted by T4c).
- [ ] README `object_type: Handoff Packet` exactly and `status: Ready for Engineering` exactly (asserted by T5).
- [ ] README four audit-gate fields carry safe augmented-placeholder values, not concrete dates or `passed` literals (asserted by T6).
- [ ] None of the 21 narrative child files carries YAML frontmatter (asserted by T7).
- [ ] `requirements.yaml` does not lead with a `---` markdown frontmatter delimiter (asserted by T7b).
- [ ] Required H1 headings present on each of the 22 markdown files in the folder (asserted by T8).
- [ ] README required H2 headings present in order (asserted by T8b).
- [ ] `launch-considerations.md` required H2 headings present (asserted by T8c).
- [ ] README's folder-index table names all 22 sibling files (asserted by T9).
- [ ] `risks.md` body references a Mitigation field (asserted by T10).
- [ ] `decision-log.md` cites `docs/adr/` (asserted by T11).
- [ ] `personas.md` references `context/personas/` (asserted by T12).
- [ ] No `{{` or `__FILL__` placeholders across the folder (asserted by T13).
- [ ] `requirements.yaml` parses with `yaml.safe_load` (asserted by T14).
- [ ] `requirements.yaml` first entry carries the ten Requirement-metadata keys (asserted by T15).
- [ ] `requirements.yaml` first entry has `object_type: Requirement` (asserted by T15b).
- [ ] `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (asserted by T16).
- [ ] `bash tools/pre-pr.sh` exits 0 (asserted by T17).
- [ ] Default-mode `--all` linter does NOT visit `templates/handoff-packet/**` (asserted by T18 — mode-separation by non-traversal).
- [ ] Every one of `/audit-completeness`'s 25 checklist items maps to at least one of the 23 files (asserted by T19).
- [ ] ROADMAP.md F3.9 row is checked off (asserted by T20) and the row's prose continues to enumerate the 23-file folder (asserted by T20b — mechanical grep gate).
- [ ] `templates/_meta/README.md` "Shipped templates" list includes `handoff-packet/` (asserted by T21).
- [ ] `adversarial-reviewer` subagent returns no Blocking findings (asserted by T22).

## Cross-references

- **Consumed by:** ROADMAP P4.11 (`/handoff-packet`) — depends on F3.9 per its `Depends on:` line. `/audit-completeness` (shipped as command; F1.5 script shipped 2026-05-21) walks the instantiated packet's 23 files at audit time. `/audit-traceability` (F1.4 shipped) walks the Requirement entries in `requirements.yaml` on instantiated packets per ontology traceability rule 1.
- **Consumes:** `templates/_meta/template-skeleton.md` (copied for README); `docs/HANDOVERS.md` §"Handover 6: Spec → Engineering Handoff Packet" (quoted frontmatter block and folder-contents list); `docs/CONVENTIONS.md` §"Templates" (folder-layout rule), §"Universal metadata schema", §"Lifecycle states" (`Ready for Engineering` is in the enum — no override needed); `context/frameworks/ontology.md` Domain H row "Handoff Packet", Domain E rows "Requirement"/"Feature"/"Capability"/"Acceptance Criteria"/"Business Rule"/"Non-Functional Requirement", Domain G rows "Risk"/"Mitigation"; `.claude/commands/audit-completeness.md` §"The 25-item checklist"; `tools/lint-frontmatter.py --check-template`; `scripts/tests/test_templates_instantiate.py`.
- **Frontmatter fields owned:** the README encodes (at the template level — canonical source remains HANDOVERS-6) the HANDOVERS-6-specific keys `completeness_audit_passed`, `adversarial_review_passed`, `quality_engineer_review_passed`, `compliance_review_status`, `engineering_partner`, `fixed_vs_flexible` (nested map: `fixed`/`flexible`/`unknown`). Inherits the full universal-schema key set from the skeleton.
- **Ontology object types touched:** Handoff Packet (Domain H; the type the README instantiates as `object_type: Handoff Packet`). Requirement (Domain E; instantiated per-entry inside `requirements.yaml`). Capability, Feature, Acceptance Criteria, Business Rule, Non-Functional Requirement (Domain E; referenced as content across the 21 narrative files — not instantiated by this template). Risk, Mitigation (Domain G; referenced inline in `risks.md` body — not instantiated by this template).
