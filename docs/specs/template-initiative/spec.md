# Spec: template-initiative

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template
- **Serves kit phase:** Delivery
- **Constrained by:** [`docs/specs/template-authoring-convention/spec.md`](../template-authoring-convention/spec.md) (parent contract — placeholder syntax, frontmatter ordering, pre-fill rules, linter contract, skeleton-as-copy-source, folder-template layout rule, per-child frontmatter resolution per its §"Open questions" Q4); `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" (source-of-truth for the Initiative folder layout — six child files — and the README frontmatter superset; quoted verbatim below); `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" and §"Universal metadata schema" and §"Lifecycle states" (frontmatter superset, ordering, folder-template layout, lifecycle enum); `context/frameworks/ontology.md` Domain D row "Initiative" and Domain E row "Capability" (the ontology types the Initiative composite touches); ROADMAP F3.7.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `templates/initiative/` — a folder template with `README.md` (initiative overview, carries universal-schema + HANDOVERS-5 frontmatter) plus five narrative child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) that hold no frontmatter. The folder's shape — README plus exactly these five child file names in this order — IS the contract: downstream commands (`/draft-initiative` P4.3, `/context-map` P4.4, `/end-to-end-flow` P4.5) target these exact paths, and HANDOVERS-5 enumerates them. A kit user copies `templates/initiative/` to `delivery/initiatives/<slug>/`, fills the README, then fills each narrative child file as the Initiative work progresses.

## Objective

`templates/initiative/` is the folder skeleton for the Initiative artifact — the load-bearing scaffold underneath HANDOVERS Handover 5 (Initiative → Spec). Today, a kit user wanting to draft an initiative has no copyable starting point: they would have to read HANDOVERS Handover 5 (which lists six required child files and a README frontmatter block), `docs/CONVENTIONS.md` §"Templates" (for folder-layout rules), the universal-metadata schema, the ontology Domain D row, the parent authoring convention, and `templates/_meta/template-skeleton.md`, and stitch them together themselves. They'd very likely (a) miss one of the six child files (the ROADMAP F3.7 row enumerates only five — `capabilities.md` is implicit in HANDOVERS-5 but missing from the row's prose); (b) put per-child frontmatter on the four narrative files where the parent convention's OQ4 explicitly says it doesn't belong; (c) write `status: Draft` on the README per the universal schema, missing the HANDOVERS-5 `status: active | paused | done` enum override. This template collapses that into one `cp -r templates/initiative/ delivery/initiatives/<slug>/` followed by placeholder replacement. The folder's shape — README plus exactly these five additional file names — IS the contract.

The Initiative is a **composite product artifact** (per ontology Domain D row "Initiative — Strategic body of work") and HANDOVERS-5 makes the composition explicit: the README is the index, the five narrative children carry the supporting prose / diagrams / manifests that an Initiative-shaped piece of work requires before a downstream spec author (F3.8 `templates/pm-spec.md`) can start writing individual specs inside `delivery/initiatives/<slug>/specs/<spec-slug>.md`.

The closest prior context in the repo is `templates/_meta/template-skeleton.md` (the shape contract this template's README copies from), `templates/experiment/` (the precedent folder template — the only one shipped before this one; sets the pattern for `mkdir + cp -r` and for per-child frontmatter decisions), and `templates/pm-spec.md` (the F3.8 sibling whose instantiations live inside `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` and are enumerated by this template's `child-specs.md`).

## Why now

ROADMAP F3.7 sits in the F3 block — the ten templates the parent `template-authoring-convention` spec made parallelizable. P4.3 (`/draft-initiative`) explicitly depends on F3.7: its `Depends on:` line in ROADMAP names this row. Until F3.7 ships, P4.3 is blocked, P4.4 (`/context-map`) and P4.5 (`/end-to-end-flow`) have nowhere to write into (no canonical filename), and the Delivery phase has no copyable starting point for the multi-file artifact that Handover 5 contracts. Shipping F3.7 unblocks all three downstream commands and gives kit users a one-line `cp -r` path into the layout the rest of the kit expects. The parent convention shipped 2026-05-22, so the contract surface F3.7 consumes is stable; the only other folder template shipped (F3.4 `templates/experiment/`) is the operative precedent for folder-template per-child frontmatter resolution.

F3.7 is the third folder template in the kit (after `templates/_meta/` infrastructure and `templates/experiment/` artifact). It is the most multi-file of all ten F3.x templates — six children — and the spec exists in part to encode the per-child frontmatter decisions explicitly so kit users do not re-litigate them at instantiation time.

## Inputs and outputs

**Inputs.**

- `templates/_meta/template-skeleton.md` — the canonical skeleton this template copies for its `README.md` (read-only; not edited by this spec).
- `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" — source-of-truth for the folder contents enumeration, the README required frontmatter block, and the per-child required content. Quoted verbatim below.
- `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" — authoring convention. Specifically the "File layout" sub-section, which permits folder templates `templates/<slug>/` containing a `README.md` plus per-child-file templates where children carry their own frontmatter iff they instantiate a distinct ontology object.
- `docs/CONVENTIONS.md` §"Universal metadata schema" — universal frontmatter superset (inherited by the README).
- `docs/CONVENTIONS.md` §"Lifecycle states" — the canonical `LIFECYCLE_STATES` enum (`Draft`, `In Review`, `Validated`, …, `Shipped`, `Frozen`) that the default-mode linter enforces on `status:`. HANDOVERS-5's `status: active | paused | done` overrides this for the Initiative — surfaced as Open Question 1.
- `context/frameworks/ontology.md` Domain D row "Initiative" (line 80: "Strategic body of work") — confirms the `object_type:` pre-fill value as the single token `Initiative`. Domain E row "Capability" (line 88: "What the product must enable users or the business to do") — confirms the type referenced by the README's `capabilities:` list field and by the body of `capabilities.md`.
- `tools/lint-frontmatter.py --check-template` — the linter gate the README must pass. The four narrative child files have no frontmatter and are not subject to the linter.
- `scripts/tests/test_templates_instantiate.py` — discovery rule covers `templates/*/README.md`; this template's README is auto-discovered.
- Precedent: `templates/experiment/` (the F3.4 folder template) — sets the `mkdir + cp -r` pattern; sets the per-child frontmatter resolution pattern (children carry frontmatter only when instantiating distinct ontology objects).

**Outputs.**

1. `templates/initiative/README.md` — new file. Initiative overview. Universal-schema frontmatter (per skeleton, with `status:` overridden per HANDOVERS-5) plus a second Handover-5-specific frontmatter block carrying `parent_vision`, `crosses_repos`, `crosses_teams`, `capabilities`, `context_map_signed_off`, `sign_off_by`. Pre-filled: `object_type: Initiative`. Body is an orientation paragraph plus three H2 sections matching the README's role within the Initiative composite (per §"Required sections" below — Inferred from folder-index practice since HANDOVERS-5 specifies the *folder contents*, not the README's *internal* sections). Auto-discovered by `scripts/tests/test_templates_instantiate.py` via the `*/README.md` glob.
2. `templates/initiative/context-map.md` — new file. **No frontmatter** (narrative file; instantiates no distinct ontology object — "Bounded Context" is not in the ontology). Body: H1 + one-paragraph orientation + per-bounded-context section template with the four required fields from HANDOVERS-5 §"Required content" item 1 (owner, public contract, commodity-vs-custom Wardley evaluation, evolution stage). Multiple bounded contexts are represented as a repeated H2-or-H3 section pattern in the body.
3. `templates/initiative/flow.md` — new file. **No frontmatter** (narrative diagram file). Body: H1 + a Mermaid `sequenceDiagram` placeholder block per HANDOVERS-5 §"Required content" item 2 (end-to-end customer flow across contexts) + a brief one-paragraph caption block underneath.
4. `templates/initiative/child-specs.md` — new file. **No frontmatter** (manifest file). Body: H1 + one-paragraph orientation citing F3.8 (`templates/pm-spec.md`) as the type of artifact this file enumerates + a markdown table with five columns per HANDOVERS-5 §"Required content" item 3: spec slug, owning context, owning team, status, link.
5. `templates/initiative/sequence.md` — new file. **No frontmatter** (narrative DAG file). Body: H1 + one-paragraph orientation + a Mermaid `graph` (or `flowchart`) placeholder block representing the spec-by-spec dependency DAG per HANDOVERS-5 §"Required content" item 4 + a one-line "first-shippable subset" callout immediately below the diagram.
6. `templates/initiative/capabilities.md` — new file. **No frontmatter** (registry/reference file; the README's `capabilities: [<CAP-NNN>, ...]` field is the machine-readable Capability list, and individual Capability objects are instantiated elsewhere in the kit's broader Domain E structure — this file is human-readable elaboration). Body: H1 + one-paragraph orientation naming the README's `capabilities:` list as the machine-readable source + a per-capability section template with the four fields from HANDOVERS-5 §"Required content" item 5 (id, name, linked Problem, evidence strength, related KPI). Per-capability sections are H2 or H3 repeated.
7. `templates/_meta/README.md` — one-line append under "Shipped templates": `initiative/` (folder template). CAPTURE-phase only; tiny dedicated commit per parent plan §Rollout to avoid races with future folder-template workers.
8. `ROADMAP.md` — F3.7 checkbox marked. CAPTURE-phase only.
9. `docs/specs/template-initiative/spec.md` and `plan.md` frozen to `Status: Shipped (<date>)` / `Status: Done (<date>)` (CAPTURE phase only).

**Required HANDOVERS-5 frontmatter block (quoted verbatim from `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec").** This is the contract surface the README must shape:

```yaml
object_type: Initiative
parent_vision: <vision slug>
crosses_repos: [<repo>, <repo>]
crosses_teams: [<team>, <team>]
capabilities: [<CAP-NNN>, ...]
status: active | paused | done
context_map_signed_off: <YYYY-MM-DD>
sign_off_by: [<names>]
human_owned_decisions:
  - Bounded-context ownership assignment
  - Build vs buy decisions in the evolution check
  - Delivery sequencing
```

**Folder-contents enumeration (quoted verbatim from HANDOVERS-5).** This is the load-bearing list:

> Folder contents:
> - `README.md` — initiative overview
> - `context-map.md` — bounded contexts, ownership, shared shapes, Wardley-lite evolution check
> - `flow.md` — end-to-end flow (Mermaid)
> - `child-specs.md` — manifest of spec files
> - `sequence.md` — dependency-aware delivery sequence
> - `capabilities.md` — Capability list with traceability to parent Problems

**ROADMAP-vs-HANDOVERS reconciliation.** ROADMAP F3.7's row reads "Initiative README + context-map + flow + child-specs + sequence templates" — enumerating **five** files (omitting `capabilities.md`). HANDOVERS-5 enumerates **six**. HANDOVERS-5 is the source-of-truth per the parent authoring convention ("Quote `docs/HANDOVERS.md` verbatim for every required-section and required-frontmatter claim in the convention text"). This spec follows HANDOVERS-5 and ships all six files; the ROADMAP row is updated in the CAPTURE phase to include `capabilities.md` in its prose (and to flip the checkbox). See §"Open questions" Q3.

**Required sections (per child file).**

For `README.md` (initiative overview — three H2 sections, ordered; **inferred from folder-index practice** since HANDOVERS-5 enumerates folder *contents*, not README *internal* sections):

1. **What this initiative is** — one-paragraph restatement of the Vision's `change`, scoped to what this Initiative delivers. Cite the parent Vision via `parent_vision:`. *(Inferred — folder-index orientation; HANDOVERS-4's Vision is the upstream artifact.)*
2. **Scope and bounded contexts** — short pointer prose; defer the full content to `context-map.md`. Names which bounded contexts the Initiative crosses. Cite `context-map.md`. *(Inferred — folder-index navigation; the README is the index, not the substantive home.)*
3. **Delivery sequencing** — short pointer prose; defer the full content to `sequence.md` and `child-specs.md`. Names the first-shippable subset and the dependency-driving spec. *(Inferred — folder-index navigation; the README points at the manifests.)*

For `context-map.md` (bounded-contexts narrative — two H2 sections + one H3 sub-template, ordered; **sourced from HANDOVERS-5 §"Required content" item 1**):

1. **Bounded contexts in this initiative** — H2; introductory paragraph naming what a bounded context means for this Initiative, links out to the kit's bounded-context-vocabulary doc if one exists *(planned — ROADMAP P4.4 will likely ship one; until then, prose-only).*
2. **Per-bounded-context detail** — H2 introducing a repeated H3-sub-section template `### <Bounded context name>` containing four required body fields per HANDOVERS-5 §"Required content" item 1: `**Owner:**`, `**Public contract:**`, `**Commodity vs custom (Wardley):**`, `**Evolution stage:**`. Multiple bounded contexts are represented by duplicating the H3 block. *(Sourced from HANDOVERS-5 verbatim.)*

For `flow.md` (end-to-end flow — one H2 section + one Mermaid block, ordered; **sourced from HANDOVERS-5 §"Required content" item 2**):

1. **End-to-end customer flow** — H2; a Mermaid `sequenceDiagram` placeholder block (fenced as `` ```mermaid `` … `` ``` ``) that demonstrates the kit's preferred shape; one-paragraph caption immediately under the diagram explaining the trigger event, the actors, and the success outcome. *(Sourced from HANDOVERS-5: "flow.md — end-to-end flow (Mermaid)".)*

For `child-specs.md` (spec manifest — one H2 section + one table, ordered; **sourced from HANDOVERS-5 §"Required content" item 3**):

1. **Specs in this initiative** — H2; one-paragraph orientation citing F3.8 (`templates/pm-spec.md`) as the artifact type; a markdown table with five columns matching HANDOVERS-5: `| Spec slug | Owning context | Owning team | Status | Link |`. Header row plus one placeholder data row. *(Sourced from HANDOVERS-5 verbatim.)*

For `sequence.md` (dependency DAG — one H2 section + one Mermaid block + one callout, ordered; **sourced from HANDOVERS-5 §"Required content" item 4**):

1. **Delivery sequence** — H2; a Mermaid `graph LR` (or `flowchart LR`) placeholder block fenced as `` ```mermaid `` representing the spec dependency DAG; one one-line callout immediately below the diagram: `**First shippable subset:** <list of spec slugs>` (the "first-shippable subset called out" requirement). *(Sourced from HANDOVERS-5 verbatim.)*

For `capabilities.md` (Capability registry narrative — two H2 sections + one H3 sub-template, ordered; **sourced from HANDOVERS-5 §"Required content" item 5**):

1. **Capabilities in this initiative** — H2; one-paragraph orientation noting that the README's `capabilities:` list is the machine-readable source and this file is the elaboration.
2. **Per-capability detail** — H2 introducing a repeated H3 sub-section template `### <CAP-NNN> — <capability name>` containing four required body fields per HANDOVERS-5 §"Required content" item 5: `**Linked Problem:**`, `**Evidence strength:**`, `**Related KPI:**`, `**Notes:**` (where Notes is a one-line free-form addition for kit-user expansion; the four HANDOVERS-5 fields are id+name in the H3 heading itself plus the three body bullets). Multiple capabilities are represented by duplicating the H3 block. *(Sourced from HANDOVERS-5 verbatim.)*

**Downstream consumers.** ROADMAP P4.3 (`/draft-initiative`) reads `templates/initiative/` as its scaffolding source. P4.4 (`/context-map`) and P4.5 (`/end-to-end-flow`) gain **stable target filenames** (`context-map.md` and `flow.md`) once this template ships — their *file-contract* dependency on F3.7 is satisfied, but each of those commands may carry additional dependencies (e.g., a bounded-context vocabulary framework reference) that F3.7 does not address. P4.10 (`/audit-spec-linkage`) reads the Initiative folder layout to walk specs by `parent_initiative:`. F3.8 (`templates/pm-spec.md`) instantiates `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` — the Initiative folder hosts those specs alongside the six template-shipped files.

## Boundaries

### Always do

- Use the folder layout `templates/initiative/` with exactly **six** child files: `README.md`, `context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`. File names pinned by HANDOVERS-5's "Folder contents" enumeration. `initiative/` is the second folder template in the kit (after `experiment/`) and is authorized by parent convention §"File layout" plus the parent spec's enumeration "Multi-file template (folders such as Initiative, Handoff Packet)" — language naming this template explicitly.
- Use angle-bracket placeholder syntax exclusively (`<descriptor>`); inherit the skeleton's placeholder discipline. The README's `status:` value `<active | paused | done>` is an augmented placeholder per the parent linter's `AUGMENTED_PLACEHOLDER` rule, accepted under `--check-template`.
- Quote HANDOVERS-5's frontmatter block on the README verbatim (with placeholder substitution where the value is the kit-user's choice). The eight HANDOVERS-5 fields (`object_type`, `parent_vision`, `crosses_repos`, `crosses_teams`, `capabilities`, `status`, `context_map_signed_off`, `sign_off_by`) and the three `human_owned_decisions:` strings (`Bounded-context ownership assignment`, `Build vs buy decisions in the evolution check`, `Delivery sequencing`) appear in the README exactly as in HANDOVERS-5.
- Pre-fill only the template's identity field: `object_type: Initiative` on the README. The `status:` field is **not** pre-filled to `Draft` (the parent skeleton's default); it carries the HANDOVERS-5 enum placeholder `<active | paused | done>` because the Initiative's lifecycle uses a domain-specific enum. Document this deviation in the README body and in §"Open questions" Q1.
- **Traceability field retention.** From the skeleton's traceability block, **retain** `parent_intent` (restated for upstream traceability, matching the Vision-template precedent) and `parent_vision` (HANDOVERS-5 explicitly requires it; goes in its universal-schema traceability-block position per the dedup convention). **Delete** `parent_opportunity`, `parent_learning`, and `parent_initiative` from the README's traceability block — HANDOVERS-5 does not require them, and an Initiative does not have a parent Initiative.
- Keep the README's universal-schema frontmatter block ordering identical to `templates/_meta/template-skeleton.md` (the parent convention pins ordering). Append HANDOVERS-5-specific fields **not present in the universal schema** (`crosses_repos`, `crosses_teams`, `capabilities`, `context_map_signed_off`, `sign_off_by`) after a `# Handover-specific fields (per HANDOVERS.md Handover 5)` YAML comment line inside the same `---`...`---` frontmatter block. The README's frontmatter is a **single YAML document** delimited by exactly one pair of `---` markers; the "second block" is a logical grouping under a YAML-comment separator, not a second `---`-delimited document. (Two `---` pairs would only get the first parsed by the linter.)
- Cross-cutting dedup convention. When HANDOVERS-5 fields overlap with the universal-metadata schema (e.g., `human_owned_decisions:`, `parent_vision:` which appears in both the universal-schema traceability block and the HANDOVERS-5 block), the field appears **once** in its universal-schema position, carrying the HANDOVERS-5-mandated value. The universal-schema placeholder is deleted in the same edit. The handover-specific second block carries only fields not present in the universal schema (`crosses_repos`, `crosses_teams`, `capabilities`, `context_map_signed_off`, `sign_off_by`).
- For the four narrative child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`) and the `capabilities.md` registry: **no YAML frontmatter**. Begin the file with the H1 heading. This is the OQ4 resolution from the parent convention applied to F3.7: child files carry frontmatter only when they instantiate a distinct ontology object, and none of these five do.
- Pass `tools/lint-frontmatter.py --check-template templates/initiative/README.md` and `python3 -m pytest scripts/tests/test_templates_instantiate.py` cleanly before CAPTURE.
- Cite HANDOVERS-5 inline in the README body's opening blockquote so a reader scanning the markdown knows the source contract.

### Ask first

- Adding a frontmatter field to the README not present in `docs/CONVENTIONS.md` §"Universal metadata schema" or `docs/HANDOVERS.md` §"Handover 5". The convention is downstream of those two docs.
- Adding YAML frontmatter to any of the five non-README child files. The OQ4 resolution is explicit and any per-child frontmatter would require ontology evidence that the child instantiates a distinct typed object.
- Adding a seventh required child file. The folder contents are pinned by HANDOVERS-5; adding a seventh requires editing HANDOVERS-5, which is out of scope here.
- Pre-filling the `human_owned_decisions:` list with values **other than** the three HANDOVERS-5 strings. The list is HANDOVERS-5-pinned; adding or substituting requires HANDOVERS-5 editing.

### Never do

- Invent domain content. The body of each child file is shape-only: H2/H3 headings plus one-line `<placeholder>` bodies. No example bounded contexts, no real flow steps, no real spec slugs, no real Capability ids.
- Use `{{...}}` or `__FILL__` placeholder syntax anywhere. The parent convention permits angle-bracket only.
- Rename any child file. The names are pinned by HANDOVERS-5 — any other name silently bypasses any future audit that walks the Initiative folder by filename (`/audit-spec-linkage` P4.10 is one such future audit).
- Add YAML frontmatter to `context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, or `capabilities.md`. Per OQ4 resolution; documented as a positive contract not just an omission.
- Pre-fill `status: Draft` on the README. The Initiative's status enum is HANDOVERS-5's `active | paused | done`, not the universal lifecycle. Pre-filling `Draft` would set kit users up to write a concrete `Draft` value that the default-mode linter on the instantiated artifact would accept under the universal lifecycle but that contradicts HANDOVERS-5.
- Add `Initiative-Folder`, `Bounded Context`, `Capability Registry`, or any other ad-hoc ontology type. The parent convention's "Never do — Add … as an ontology type" rule applies; templates are kit-build scaffolding, not ontology-type-creation sites.
- Resolve the universal-lifecycle-vs-HANDOVERS-5-`active|paused|done` enum mismatch inside this spec. Surface as Open Question 1; defer to a separate spec (likely a `lint-frontmatter.py` per-type-override extension or a HANDOVERS-5 amendment).
- Modify `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, `scripts/tests/test_templates_instantiate.py`, or `templates/_meta/template-skeleton.md`. The parent contract surface is committed; F3.7 is a downstream consumer only. If adversarial review surfaces a contradiction, resolve via a separate spec.
- Walk `templates/initiative/` from the default-mode linter. The linter contract (parent spec) keeps `templates/` outside `PHASE_DIRS`; only `--check-template` runs against it, and only against the README (the other five files have no frontmatter).

## Verification mode

- **Goal-based check** for the template's shape — required headings present in order on each child file; required frontmatter keys present on the README (incl. HANDOVERS-5 block keys); placeholder-syntax purity; child-file existence; absence of frontmatter on the five non-README files. Each check is a one-line shell or python predicate.
- **Audit-driven** for the linter and pytest gates: `python3 tools/lint-frontmatter.py --check-template templates/initiative/README.md` exits 0; `python3 -m pytest scripts/tests/test_templates_instantiate.py` (which auto-discovers `templates/initiative/README.md` via the `*/README.md` glob) exits 0; `bash tools/pre-pr.sh` exits 0.
- **Adversarial review** (manual gesture against the shipped template files) — dispatch the `adversarial-reviewer` subagent against the six files versus HANDOVERS §"Handover 5", the parent authoring convention, and ontology Domain D + E. Iterate fixes inline; max 3 review passes per the work-loop default. The reviewer should specifically check: (a) the five non-README files carry no frontmatter; (b) the README's HANDOVERS-5 block matches verbatim; (c) the per-child required-content lists match HANDOVERS-5 verbatim where sourced, and the inferred sections (README H2s) are flagged with source comments.

The template is done when T1–T18 all pass (T1–T15 at VERIFY time; T16, T16b, T17 at CAPTURE time; T18 at REVIEW time).

## Contract tests

Each test is one shell line or one pytest case.

- `T1` — `test -d templates/initiative && test -f templates/initiative/README.md && test -f templates/initiative/context-map.md && test -f templates/initiative/flow.md && test -f templates/initiative/child-specs.md && test -f templates/initiative/sequence.md && test -f templates/initiative/capabilities.md` exits 0 (target folder + all six child files exist).
- `T2` — `python3 tools/lint-frontmatter.py --check-template templates/initiative/README.md` exits 0.
- `T3` — README frontmatter contains the universal-schema key set inherited from the skeleton (asserted by a python one-liner that parses YAML and checks every skeleton-required key — `id`, `slug`, `object_type`, `name`, `description`, `owner`, `status`, `priority`, `risk_level`, `created`, `last_updated`, plus the traceability, evidence, human-ownership, and open-items blocks — is present at top level).
- `T4` — README frontmatter contains the HANDOVERS-5-specific keys not present in the universal schema: `crosses_repos`, `crosses_teams`, `capabilities`, `context_map_signed_off`, `sign_off_by`. Asserted by a python one-liner.
- `T4b` — README frontmatter retains `parent_vision` (HANDOVERS-5 requires it; this test pins its presence in case the author over-trims the traceability block while deleting the three Initiative-irrelevant fields). Asserted by `grep -c '^parent_vision:' templates/initiative/README.md` returns 1.
- `T5` — README's `object_type` value is exactly `Initiative` and `status` value is the augmented placeholder `<active | paused | done>` (not `Draft`, not a concrete `active`). Asserted by a python one-liner that parses YAML and inspects the two values.
- `T6` — README's `human_owned_decisions:` list contains the three HANDOVERS-5 strings verbatim: `Bounded-context ownership assignment`, `Build vs buy decisions in the evolution check`, `Delivery sequencing`. Asserted by a python one-liner.
- `T7a` — `context-map.md` has **no YAML frontmatter** (no `---` delimiter line in the first 5 lines of the file). Asserted by `head -5 templates/initiative/context-map.md | grep -c '^---'` returns 0. (Absence-of-`---` is the load-bearing predicate; an `^# ` presence check would false-positive if the author added an HTML comment before the H1.)
- `T7b` — `flow.md` has no YAML frontmatter. Same pattern: `head -5 ... | grep -c '^---'` returns 0.
- `T7c` — `child-specs.md` has no YAML frontmatter. Same pattern.
- `T7d` — `sequence.md` has no YAML frontmatter. Same pattern.
- `T7e` — `capabilities.md` has no YAML frontmatter. Same pattern.
- `T8a` — README required H2 headings present in order: `## What this initiative is`, `## Scope and bounded contexts`, `## Delivery sequencing`. Asserted by `grep -n` recording line numbers and checking monotonicity.
- `T8b` — `context-map.md` required H2 headings present in order: `## Bounded contexts in this initiative`, `## Per-bounded-context detail`. Asserted by `grep -n`.
- `T8c` — `flow.md` required H2 heading present: `## End-to-end customer flow`. Asserted by `grep -n`.
- `T8d` — `child-specs.md` required H2 heading present: `## Specs in this initiative`. Asserted by `grep -n`.
- `T8e` — `sequence.md` required H2 heading present: `## Delivery sequence`. Asserted by `grep -n`.
- `T8f` — `capabilities.md` required H2 headings present in order: `## Capabilities in this initiative`, `## Per-capability detail`. Asserted by `grep -n`.
- `T9` — `flow.md` contains a fenced Mermaid block: `grep -c '^```mermaid' templates/initiative/flow.md` returns >= 1.
- `T10` — `sequence.md` contains a fenced Mermaid block AND a "First shippable subset" callout: `grep -c '^```mermaid' templates/initiative/sequence.md` returns >= 1 AND `grep -c 'First shippable subset' templates/initiative/sequence.md` returns >= 1.
- `T11` — `child-specs.md` contains a markdown table with the five HANDOVERS-5 columns: `grep -E '^\| Spec slug \| Owning context \| Owning team \| Status \| Link \|' templates/initiative/child-specs.md` returns 1 (header row).
- `T12` — Angle-bracket-only placeholder syntax across all six files: `grep -rc '{{' templates/initiative/` returns 0 and `grep -rc '__FILL__' templates/initiative/` returns 0.
- `T13` — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (the parametrized `test_template_passes_check_template_mode` test will include `templates/initiative/README.md` via the `*/README.md` glob; the other five files are not auto-discovered, which is the load-bearing OQ4 resolution).
- `T14` — `bash tools/pre-pr.sh` exits 0 (kit-wide health check after the template lands).
- `T15` — `python3 tools/lint-frontmatter.py --all` exits 0 (default mode does not traverse `templates/initiative/**` — mode-separation by non-traversal, identical to F3.4's T11).
- `T16` — ROADMAP F3.7 checkbox flipped (CAPTURE-phase predicate): `grep -c '^- \[x\] \*\*F3\.7\*\*' ROADMAP.md` returns 1.
- `T16b` — ROADMAP F3.7 row's prose enumerates `capabilities` among the templates shipped (resolves spec OQ3): `grep -E '\*\*F3\.7\*\*.*capabilities' ROADMAP.md` returns 1. Mechanical guard so the prose update is not relying on visual-only confirmation.
- `T17` — `templates/_meta/README.md` lists the template (CAPTURE-phase predicate): `grep -c 'initiative/' templates/_meta/README.md` returns >= 1.
- `T18` — Adversarial-reviewer subagent returns 0 Blocking findings against the six shipped files versus HANDOVERS §"Handover 5", parent authoring convention, ontology Domain D + E.

## Non-goals

- Authoring an instantiated initiative under `delivery/initiatives/<slug>/`. F3.7 ships the skeleton; the kit user (or P4.3 `/draft-initiative` when shipped) instantiates the artifact.
- Building P4.3 (`/draft-initiative`), P4.4 (`/context-map`), or P4.5 (`/end-to-end-flow`). Separate ROADMAP rows; F3.7 unblocks them but does not implement them.
- Modifying `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, or `scripts/tests/test_templates_instantiate.py`. The pytest harness auto-discovers `templates/initiative/README.md` via the `*/README.md` glob; F3.7 needs no test-harness wiring. The five narrative child files have no frontmatter and are intentionally outside the linter's discovery scope; this is the OQ4 resolution.
- Resolving the universal-lifecycle-vs-HANDOVERS-5-`active|paused|done` enum mismatch. Out of scope; defer to a separate spec.
- Adding `tools/new-template.sh` or any folder-template scaffolder. Out of scope per parent spec's §Non-goals.
- Adding F3.8 (`templates/pm-spec.md`) child-spec instances under `templates/initiative/specs/`. F3.8 ships its own single-file template; the Initiative folder template does not pre-populate spec instances. The kit user (or P4.3) creates the `specs/` subfolder on instantiation.
- Adding a `templates/initiative/CLAUDE.md`-style per-template guidance file. The README plus the spec are sufficient.
- Authoring F3.9 (`templates/handoff-packet/`). Separate parallel F3 row; the only remaining F3.x row alongside F3.7.

## Open questions

1. **Universal lifecycle enum vs HANDOVERS-5 `active | paused | done` enum.** The README's `status:` value is the HANDOVERS-5-pinned augmented placeholder `<active | paused | done>`, which the parent linter accepts in `--check-template` mode. But on an *instantiated* artifact (`delivery/initiatives/<slug>/README.md`), a concrete value like `active` would fail the default-mode linter's `LIFECYCLE_STATES` enum check (which permits `Draft`, `In Review`, `Validated`, `Approved`, `Ready for Engineering`, `In Build`, `Launched`, `Measured`, `Deprecated`, `Shipped`, `Frozen`). Resolved here for F3.7's scope: the template carries the HANDOVERS-5 placeholder; the enum mismatch is real and surfaced but **not fixed here**. Tracked as a separate spec — either (a) extend `LIFECYCLE_STATES` with the Initiative-specific values, or (b) introduce a per-`object_type` status enum override in `tools/lint-frontmatter.py`, or (c) amend HANDOVERS-5 to use universal-lifecycle values. The cost of NOT resolving it here: kit users instantiating an Initiative would hit a default-mode linter failure the first time they set `status: active`. The mitigation: this template's README body includes a one-line callout noting the enum mismatch and the deferred resolution.
2. **Per-child frontmatter on `capabilities.md`.** The parent convention's OQ4 rule says "per-child frontmatter when the child instantiates a distinct ontology object." `capabilities.md` is a registry/reference enumerating Capability (Domain E) objects — but it lists multiple, not one, and the README's machine-readable `capabilities: [<CAP-NNN>, ...]` field is the canonical source. Resolved here: **no frontmatter on `capabilities.md`**. The file is human-readable elaboration of the README's list; individual Capability objects are tracked elsewhere in the kit's broader Domain E structure (not pre-defined by this spec; likely under `delivery/capabilities/` or inlined in the Initiative folder by a future P4.10-related spec). If a future ROADMAP row formalizes per-Capability artifact files, `capabilities.md` may evolve into a frontmatter-bearing manifest — but that's a separate spec.
3. **ROADMAP F3.7 row enumerates 5 files; HANDOVERS-5 enumerates 6.** Resolved here: follow HANDOVERS-5 (six files). The CAPTURE phase updates ROADMAP F3.7's prose to read "Initiative README + context-map + flow + child-specs + sequence + capabilities templates" and flips the checkbox. If the ROADMAP maintainer disagrees during adversarial review, the resolution is documented and reverted.
4. **README internal H2 sections are inferred, not HANDOVERS-sourced.** HANDOVERS-5 specifies the folder *contents* but not the README's *internal* sections. Resolved here: three H2 sections (`What this initiative is`, `Scope and bounded contexts`, `Delivery sequencing`) inferred from folder-index practice. Each H2 in the body carries an inline HTML comment `<!-- source: inferred -->`. If adversarial review rejects the inferred taxonomy, iterate within the 3-pass limit.
5. **Pytest-harness coverage of the five narrative child files.** The harness globs `templates/*.md` and `templates/*/README.md`; the five non-README files in `templates/initiative/` are NOT auto-discovered. Resolved here: known coverage gap, mitigated by spec-local T7a–T7e (frontmatter-absence) and T8b–T8f (heading-presence) shell tests. The coverage gap is OK because the five files have no frontmatter — the `--check-template` linter has nothing to validate on them. The shell-level structural tests substitute. If a future ROADMAP row promotes any of these files to frontmatter-bearing, the harness glob needs widening at the same time.
6. **Mermaid syntax validation.** The template's `flow.md` and `sequence.md` carry placeholder Mermaid blocks. The kit has no Mermaid syntax-validation tool. Resolved here: the placeholder blocks use **Mermaid-safe identifiers** (bare CamelCase node IDs and participant names — `ActorA`, `SpecA`, `TriggerEvent`) rather than the kit's angle-bracket placeholder syntax, because angle brackets inside a Mermaid block break Mermaid's tokenizer (GitHub renders the diagram broken, even though T9/T10 — which only check for the fenced-block presence — would pass). Each Mermaid block is followed by a one-line prose instruction directing the kit user to substitute real names/slugs on instantiation. Structural validation is by visual inspection during VERIFY (rendering preview in GitHub or any Mermaid renderer). No mechanical Mermaid linter is in scope.

## Acceptance criteria

- [ ] `templates/initiative/` folder exists with all six child files: `README.md`, `context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md` (asserted by T1).
- [ ] README passes `python3 tools/lint-frontmatter.py --check-template templates/initiative/README.md` (asserted by T2).
- [ ] README frontmatter contains every key in the universal-schema set (asserted by T3).
- [ ] README frontmatter contains the five HANDOVERS-5-specific keys: `crosses_repos`, `crosses_teams`, `capabilities`, `context_map_signed_off`, `sign_off_by` (asserted by T4).
- [ ] README `object_type: Initiative` exactly and `status:` value is `<active | paused | done>` (HANDOVERS-5 augmented placeholder, not `Draft`) (asserted by T5).
- [ ] README `human_owned_decisions:` list matches HANDOVERS-5 verbatim (asserted by T6).
- [ ] None of `context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md` carries YAML frontmatter (asserted by T7a–T7e).
- [ ] Required H2 headings present in order on each of the six files (asserted by T8a–T8f).
- [ ] `flow.md` contains a fenced `mermaid` block (asserted by T9).
- [ ] `sequence.md` contains a fenced `mermaid` block AND a "First shippable subset" callout (asserted by T10).
- [ ] `child-specs.md` contains a markdown table with the five HANDOVERS-5 columns (asserted by T11).
- [ ] No `{{` or `__FILL__` placeholders across the folder (asserted by T12).
- [ ] `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (asserted by T13).
- [ ] `bash tools/pre-pr.sh` exits 0 (asserted by T14).
- [ ] Default-mode `--all` linter does NOT visit `templates/initiative/**` (asserted by T15 — mode-separation by non-traversal).
- [ ] ROADMAP.md F3.7 row is checked off (asserted by T16) **and** the row's prose includes `capabilities` in the templates enumeration (asserted by T16b — mechanical grep gate, no longer relying on visual-only confirmation).
- [ ] `templates/_meta/README.md` "Shipped templates" list includes `initiative/` (asserted by T17).
- [ ] `adversarial-reviewer` subagent returns no Blocking findings (asserted by T18).

## Cross-references

- **Consumed by:** ROADMAP P4.3 (`/draft-initiative`) — depends on F3.7 per its `Depends on:` line; P4.4 (`/context-map`) — writes into the `context-map.md` filename pinned by this template; P4.5 (`/end-to-end-flow`) — writes into the `flow.md` filename pinned by this template; P4.10 (`/audit-spec-linkage`) — walks `delivery/initiatives/<slug>/specs/*` per the layout this template establishes. F3.8's `templates/pm-spec.md` instances live inside `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` — F3.8 does not consume this template's file content but consumes its folder layout contract.
- **Consumes:** `templates/_meta/template-skeleton.md` (copied for README); `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" (quoted frontmatter block and required-content lists); `docs/CONVENTIONS.md` §"Templates" (folder-layout rule), §"Universal metadata schema", §"Lifecycle states" (the enum F3.7 surfaces as deviating from HANDOVERS-5); `context/frameworks/ontology.md` Domain D row "Initiative" and Domain E row "Capability"; `tools/lint-frontmatter.py --check-template`; `scripts/tests/test_templates_instantiate.py`.
- **Frontmatter fields owned:** the README encodes (at the template level — canonical source remains HANDOVERS-5) the HANDOVERS-5-specific keys `parent_vision`, `crosses_repos`, `crosses_teams`, `capabilities`, `context_map_signed_off`, `sign_off_by`. Inherits the full universal-schema key set from the skeleton.
- **Ontology object types touched:** Initiative (Domain D; the type the README instantiates as `object_type: Initiative`). Capability (Domain E; referenced via the README's `capabilities:` list field and elaborated in `capabilities.md` body — not instantiated by this template). Vision (Domain D; referenced via the README's `parent_vision:` traceability field — not instantiated here).
