# Plan: template-initiative

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-22)
- **Plan review:** approved (iter-2 clean — 2026-05-22)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

One single-commit task: scaffold `templates/initiative/` as a folder template with six child files (`README.md`, `context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`), pre-fill identity on the README, encode required sections per the spec's section taxonomy, append HANDOVERS-5-specific frontmatter on the README only, then VERIFY → REVIEW → CAPTURE. Five of the six child files carry **no frontmatter** per spec OQ4 resolution; only the README carries frontmatter (universal-schema + HANDOVERS-5-specific block). The folder layout is mechanical: a kit user `cp -r templates/initiative/ delivery/initiatives/<slug>/` lands them in the exact layout HANDOVERS-5 contracts and the future P4.3/P4.4/P4.5 commands will target.

Sequencing inside the task: scaffold the folder; copy the skeleton to `templates/initiative/README.md` and adapt (the most complex file — universal-schema frontmatter override on `status:`, second HANDOVERS-5 frontmatter block, three inferred H2 sections); author the five narrative child files from scratch (frontmatter-free, smaller bodies — each follows its HANDOVERS-5-sourced section taxonomy). VERIFY runs the contract tests T1–T15. REVIEW dispatches `adversarial-reviewer`. CAPTURE updates `templates/_meta/README.md`, ROADMAP F3.7 (checkbox + prose update to enumerate `capabilities.md`), and freezes spec.md / plan.md statuses.

Why one task rather than six: the six files are tightly coupled (same folder, same template identity, same VERIFY pass). Splitting into six tasks would multiply pre-pr.sh runs and adversarial-review hand-offs with no parallelism gain (all six files live in the same folder; no inter-task dependency to exploit). This matches the F3.4 (`templates/experiment/`) precedent: that template shipped its three child files as one commit.

## Constraints

- **Parent-convention prerequisite (C1).** F3.7's EXECUTE depends on the parent `template-authoring-convention` being live on the branch EXECUTE runs from — specifically (a) `tools/lint-frontmatter.py` supports the `--check-template <path>` mode (gates T2), (b) `scripts/tests/test_templates_instantiate.py` exists and auto-discovers `templates/*/README.md` (gates T13), (c) `templates/_meta/template-skeleton.md` exists for the README copy step. Confirm with `python3 tools/lint-frontmatter.py --check-template /dev/null 2>&1 | grep -q -- '--check-template\|usage:'` returns 0 AND `test -f scripts/tests/test_templates_instantiate.py` AND `test -f templates/_meta/template-skeleton.md` AND `test -f templates/CLAUDE.global.md` before beginning Task 1. On this PLAN-phase commit's branch (`eugenelim/template-initiative`, forked from `main` at 31381aa), only `templates/CLAUDE.global.md` is present; the other three prerequisites land via the parent convention's branch (separate work). If any prerequisite is missing at EXECUTE time, EXECUTE must not begin — the right path is to rebase onto the merged parent convention, not to author the prerequisites inline.
- Angle-bracket placeholder syntax only across all six files; no `{{...}}` or `__FILL__`.
- README's universal-schema frontmatter block ordering identical to `templates/_meta/template-skeleton.md`. The HANDOVERS-5-specific keys (`crosses_repos`, `crosses_teams`, `capabilities`, `context_map_signed_off`, `sign_off_by`) appear under a `# Handover-specific fields (per HANDOVERS.md Handover 5)` YAML comment. (This is a logical grouping inside a single `---`...`---` YAML document, not a second `---`-delimited block — two pairs would cause the linter to parse only the first; see spec.md §"Always do".)
- README's `status:` value is the augmented placeholder `<active | paused | done>`, **not** `Draft`. This is a deviation from the parent skeleton's pre-fill, mandated by HANDOVERS-5's enum and the spec's OQ1 resolution.
- README's `human_owned_decisions:` list contains the three HANDOVERS-5 strings verbatim and no others.
- README's `object_type:` is the literal string `Initiative` (Domain D); the file's H1 reads `# Initiative`.
- Five non-README files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`) carry **no YAML frontmatter**. First non-blank line of each is the H1 heading.
- File names pinned: `templates/initiative/{README,context-map,flow,child-specs,sequence,capabilities}.md` exactly. No suffix variants; no plural variants.
- Cross-cutting dedup convention applied: where HANDOVERS-5's frontmatter overlaps with the universal-metadata schema (`object_type`, `parent_vision`, `status`, `human_owned_decisions`, `human_approval_required` — the latter is implicit in universal schema but not in the HANDOVERS-5 block), the field appears once in its universal-schema position carrying the HANDOVERS-5-mandated value. The handover-specific second block carries only the five fields not in the universal schema.
- Mermaid blocks in `flow.md` and `sequence.md` are minimal-and-valid Mermaid skeletons (a `sequenceDiagram` for flow, a `graph LR` for sequence). The kit has no Mermaid syntax-validation tool; correctness is by visual inspection during VERIFY.
- Must not modify `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, `scripts/tests/test_templates_instantiate.py`, or `templates/_meta/template-skeleton.md`. Surfacing a contract-gap finding is allowed in adversarial review; resolving it is a separate spec.
- Stdlib only for any one-liner test invocations (no new dependencies).
- Atomic writes (the `Write` tool already writes atomically; no `tempfile + os.replace` plumbing needed beyond it).

## Construction tests

Cross-cutting only. Per-task tests are inline under the single task below.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 before the commit (run after VERIFY, before CAPTURE).

## Tasks

### Task 1: `templates/initiative/` folder template lands with six child files; README passes `--check-template`; the five narrative files are frontmatter-free; pytest auto-discovery includes README; adversarial review clean

- **Depends on:** none (parent convention `template-authoring-convention` is already shipped 2026-05-22; the skeleton and `--check-template` mode are live).
- **Tests:** (every spec contract test)
  - `T1` — folder + six child files exist.
  - `T2` — `--check-template templates/initiative/README.md` exits 0.
  - `T3` — README frontmatter contains the universal-schema key set.
  - `T4` — README frontmatter contains the HANDOVERS-5-specific keys (`crosses_repos`, `crosses_teams`, `capabilities`, `context_map_signed_off`, `sign_off_by`).
  - `T4b` — README frontmatter retains `parent_vision:` (per HANDOVERS-5; pins presence under aggressive trim).
  - `T5` — README `object_type: Initiative` exact and `status:` is the `<active | paused | done>` augmented placeholder.
  - `T6` — README `human_owned_decisions:` list matches HANDOVERS-5 verbatim.
  - `T7a/T7b/T7c/T7d/T7e` — none of the five non-README files carries YAML frontmatter (`head -5 <file> | grep -c '^---'` returns 0).
  - `T8a–T8f` — required H2 headings present in order on each of the six files.
  - `T9` — `flow.md` contains a fenced Mermaid block.
  - `T10` — `sequence.md` contains a fenced Mermaid block AND a "First shippable subset" callout.
  - `T11` — `child-specs.md` contains the markdown table with the five HANDOVERS-5 columns.
  - `T12` — angle-bracket-only placeholders across the folder.
  - `T13` — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0.
  - `T14` — `bash tools/pre-pr.sh` exits 0.
  - `T15` — `python3 tools/lint-frontmatter.py --all` exits 0 (mode-separation by non-traversal).
  - `T16` — ROADMAP F3.7 checkbox flipped (CAPTURE-phase).
  - `T16b` — ROADMAP F3.7 row prose grep contains `capabilities` (CAPTURE-phase; mechanical gate).
  - `T17` — `templates/_meta/README.md` lists `initiative/` (CAPTURE-phase).
  - `T18` — adversarial-reviewer Blocking-findings count is 0.
- **Approach:**
  1. **Scaffold.** `mkdir -p templates/initiative/`. No `tools/new-template.sh` exists (deferred per parent spec); use the kit's standard `mkdir` + `cp` pattern.
  2. **README.md — copy and adapt skeleton.** `cp templates/_meta/template-skeleton.md templates/initiative/README.md`. Then edit:
     - Pre-fill `object_type: Initiative` (replace the `<pre-filled per template ...>` placeholder).
     - **Override** `status: Draft` (skeleton default) with `status: <active | paused | done>` per HANDOVERS-5's enum and the spec's OQ1 resolution.
     - Pre-fill `human_owned_decisions:` with the three HANDOVERS-5 strings verbatim in a YAML block-list (replace the skeleton's single placeholder bullet).
     - Pre-fill `parent_vision: <vision slug>` in the universal-schema traceability block (the field already exists in the skeleton's traceability block as `parent_vision:`; per the cross-cutting dedup convention, the universal-schema position carries the HANDOVERS-5 value).
     - Delete the skeleton's other traceability fields that don't apply to an Initiative (`parent_opportunity`, `parent_learning`, `parent_initiative` — the README **is** an Initiative; it doesn't have a parent Initiative; the parent is the Vision); keep `parent_intent` as it's restated for traceability (matching the Vision template's pattern).
     - Under the existing `# Handover-specific fields ...` comment, replace the example (Strategic Intent) line with the HANDOVERS-5 block — five keys: `crosses_repos: [<repo>, <repo>]`, `crosses_teams: [<team>, <team>]`, `capabilities: [<CAP-NNN>, ...]`, `context_map_signed_off: <YYYY-MM-DD>`, `sign_off_by: [<names>]`. Update the YAML comment line itself to read `# Handover-specific fields (per HANDOVERS.md Handover 5)`.
     - Replace the H1 `<Artifact name>` with `# Initiative`.
     - Replace the one-paragraph blockquote with: a single paragraph naming the artifact ("This is an Initiative — a Strategic body of work per ontology Domain D"), citing HANDOVERS-5 by name (`docs/HANDOVERS.md` §"Handover 5: Initiative → Spec"), naming the five sibling child files in the folder, and naming the `status:` enum deviation as a known issue tracked under the spec's OQ1.
     - Replace the body section-heading templates with the three inferred H2 sections per spec §"Required sections": `## What this initiative is`, `## Scope and bounded contexts`, `## Delivery sequencing`. Each H2 carries an inline HTML comment `<!-- source: inferred (folder-index orientation) -->` so an adversarial reviewer can see the source-marker at a glance.
     - Keep the `## Optional sections` heading at the bottom (per skeleton convention) with one example optional sub-section `### Cross-team risk register`.
  3. **context-map.md — author from scratch (no frontmatter).** Body:
     - H1 `# Context map`. One-paragraph orientation citing HANDOVERS-5 §"Required content" item 1 and naming the four required per-bounded-context fields.
     - `## Bounded contexts in this initiative` — H2; one-paragraph introductory text. Inline HTML comment `<!-- source: HANDOVERS-5 §"Required content" item 1 -->`.
     - `## Per-bounded-context detail` — H2; one paragraph introducing the H3-sub-template that follows. Inline HTML comment marking source. Then a single H3 placeholder block `### <Bounded context name>` containing four labeled body lines:
       - `**Owner:** <named human or team>`
       - `**Public contract:** <one-sentence summary of the boundary contract>`
       - `**Commodity vs custom (Wardley):** <commodity | utility | product | custom>`
       - `**Evolution stage:** <genesis | custom | product | commodity>`
     - One-line note immediately after the H3 block: `> Duplicate the H3 block above for each bounded context in the initiative.`
  4. **flow.md — author from scratch (no frontmatter).** Body:
     - H1 `# End-to-end flow`. One-paragraph orientation citing HANDOVERS-5 §"Required content" item 2.
     - `## End-to-end customer flow` — H2; inline HTML comment marking source. A fenced Mermaid block (Mermaid-safe identifiers — angle-bracket kit-placeholder syntax breaks Mermaid's tokenizer, so the block uses bare CamelCase identifiers that a kit user replaces on instantiation):
       ````
       ```mermaid
       sequenceDiagram
           participant ActorA
           participant ActorB
           ActorA->>ActorB: TriggerEvent
           ActorB-->>ActorA: ResponseOrSuccessOutcome
       ```
       ````
       One-paragraph caption underneath the diagram naming the trigger event, the actors, and the success outcome (all as `<placeholder>` text in prose — angle-bracket syntax is fine in caption prose; it only breaks inside the Mermaid block). Add a one-line instruction immediately under the caption: `> Replace \`ActorA\`, \`ActorB\`, \`TriggerEvent\`, and \`ResponseOrSuccessOutcome\` with the real actor names and event labels for this initiative.`
  5. **child-specs.md — author from scratch (no frontmatter).** Body:
     - H1 `# Child specs`. One-paragraph orientation citing F3.8 (`templates/pm-spec.md`) as the artifact type these rows enumerate, naming the instantiation path `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`, and HANDOVERS-5 §"Required content" item 3.
     - `## Specs in this initiative` — H2; inline HTML comment marking source. A markdown table with the five HANDOVERS-5 columns:
       ```
       | Spec slug | Owning context | Owning team | Status | Link |
       |-----------|----------------|-------------|--------|------|
       | <spec-slug> | <bounded context> | <team> | <Draft \| Approved \| Shipped> | [<spec-slug>](./specs/<spec-slug>.md) |
       ```
       One-line note immediately after the table: `> Duplicate the data row for each child spec in the initiative.`
  6. **sequence.md — author from scratch (no frontmatter).** Body:
     - H1 `# Delivery sequence`. One-paragraph orientation citing HANDOVERS-5 §"Required content" item 4 and naming the "first-shippable subset" callout that follows the diagram.
     - `## Delivery sequence` — H2; inline HTML comment marking source. A fenced Mermaid block (Mermaid-safe identifiers per the same reason as `flow.md` — bare alphanumeric node IDs and bracketed labels without angle brackets):
       ````
       ```mermaid
       graph LR
           SpecA[Spec A] --> SpecB[Spec B]
           SpecA --> SpecC[Spec C]
           SpecB --> SpecD[Spec D]
       ```
       ````
       One-line instruction immediately after the block: `> Replace \`SpecA\`/\`SpecB\`/etc. with real spec slugs from \`child-specs.md\`.`
       One-line callout immediately under that: `**First shippable subset:** <list of spec slugs that compose the smallest viable end-to-end ship>`.
  7. **capabilities.md — author from scratch (no frontmatter).** Body:
     - H1 `# Capabilities`. One-paragraph orientation noting that the README's `capabilities:` list is the machine-readable source and that this file is the human-readable elaboration; citing HANDOVERS-5 §"Required content" item 5; citing ontology Domain E row "Capability".
     - `## Capabilities in this initiative` — H2; inline HTML comment marking source. One-paragraph introductory text.
     - `## Per-capability detail` — H2; inline HTML comment marking source. A single H3 placeholder block `### <CAP-NNN> — <capability name>` containing four labeled body lines:
       - `**Linked Problem:** <PROB-NNN or one-line description>`
       - `**Evidence strength:** <Strong | Moderate | Weak>`
       - `**Related KPI:** <KPI-NNN or one-line description>`
       - `**Notes:** <one-line free-form expansion (optional)>`
     - One-line note immediately after the H3 block: `> Duplicate the H3 block above for each Capability listed in the README's \`capabilities:\` field.`
  8. **VERIFY.** Run T1 through T15 in order:
     - `test -d` and `test -f` for T1.
     - One `python3 tools/lint-frontmatter.py --check-template` invocation for T2.
     - Python YAML-parse one-liner for T3 (walk the universal-schema keys).
     - Python YAML-parse one-liner for T4 (walk the five HANDOVERS-5 keys).
     - `grep -c '^parent_vision:'` invocation for T4b.
     - Python YAML-parse one-liner for T5 (inspect `object_type` and `status`).
     - Python YAML-parse one-liner for T6 (compare `human_owned_decisions:` list to the HANDOVERS-5 triple).
     - Five `head -5 <file> | grep -c '^---'` invocations for T7a/T7b/T7c/T7d/T7e (each must return 0).
     - Six `grep -n` invocations for T8a/T8b/T8c/T8d/T8e/T8f checking H2 monotonicity.
     - One `grep -c` invocation per file for T9, T10, T11.
     - One `grep -rc` invocation across the folder for T12.
     - `python3 -m pytest scripts/tests/test_templates_instantiate.py` for T13.
     - `bash tools/pre-pr.sh` for T14. Iterate any reds.
     - `python3 tools/lint-frontmatter.py --all` for T15; assert exit 0 (default mode does not traverse `templates/` — the load-bearing mode-separation property).
     - Defer T16 and T17 to CAPTURE.
  9. **REVIEW.** Dispatch `adversarial-reviewer` against all six files versus the constraint set (HANDOVERS §"Handover 5", parent authoring convention, ontology Domain D + E). Max 3 iterations per work-loop default. Any Blocking finding fixed in-session; non-blocking findings tracked in spec's open-questions / risks as appropriate. Specific things the reviewer should check: (a) the five non-README files carry no frontmatter; (b) the README's HANDOVERS-5 block matches verbatim; (c) the per-child required-content lists match HANDOVERS-5 verbatim where sourced, and the inferred sections (README H2s) carry source comments; (d) the dedup convention is consistently applied between universal-schema and HANDOVERS-5 fields.
  10. **CAPTURE.** In a single small commit at the end of the loop (per parent plan §Rollout — sequential README appends across F3.x workers):
     - Append a one-line entry to `templates/_meta/README.md` under "Shipped templates": `- \`initiative/\` — Initiative folder template (per HANDOVERS §"Handover 5"); README + five narrative child files (context-map, flow, child-specs, sequence, capabilities).` (T17).
     - Flip ROADMAP F3.7 checkbox: `- [ ] **F3.7**` → `- [x] **F3.7**` (gates T16).
     - Update ROADMAP F3.7's prose to enumerate all six files: "Initiative README + context-map + flow + child-specs + sequence + capabilities templates" (resolves spec OQ3; gates T16b).
     - Update `docs/specs/template-initiative/spec.md` Status: `Shipped (<YYYY-MM-DD>)`.
     - Update `docs/specs/template-initiative/plan.md` Status: `Done (<YYYY-MM-DD>)` and append a changelog entry.
- **Done when:** T1–T18 all pass; pre-pr-clean exits 0; adversarial review returns 0 Blocking findings.

## Rollout

- ROADMAP P4.3 (`/draft-initiative`) is unblocked once this template lands (P4.3's `Depends on:` line names F3.7 directly). P4.4 (`/context-map`) and P4.5 (`/end-to-end-flow`) gain **stable target filenames** (`context-map.md`, `flow.md`) once this template lands — their file-contract dependency on F3.7 is satisfied, but each may carry additional dependencies (e.g., a bounded-context vocabulary framework reference) that F3.7 does not address; their full unblocking is per-their-own-spec, not per-F3.7. P4.10 (`/audit-spec-linkage`) gains a stable folder layout to walk.
- `templates/_meta/README.md` gets a new "Shipped templates" entry. Per parent plan §Rollout, F3.x workers' README appends are sequential — this F3.7 worker's append happens at CAPTURE time in its own commit.
- `docs/HANDOVERS.md` Handover 5 is unchanged; F3.7 is a downstream re-projection. The detector line on Handover 5 references `/audit-spec-linkage` (P4.10, not yet shipped) and `/audit-traceability` (F1.4, shipped); the latter will walk the Initiative's Capabilities through the README's `capabilities:` list field once kit users instantiate the template.
- AGENTS.md and INVENTORY.md: no row added. The template is infrastructure (same pattern as `templates/_meta/template-skeleton.md` and `templates/experiment/`); the parent convention spec already established that templates are not INVENTORY rows.
- F3.8 (`templates/pm-spec.md`) consumes the folder layout contract (its instantiations live at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` — under the folder this template scaffolds). F3.8 has already shipped; no coordination needed.
- Spec OQ1 (universal-lifecycle-vs-HANDOVERS-5-enum mismatch) becomes a new follow-up ROADMAP candidate at CAPTURE time. The plan does NOT author this candidate inline — surfacing happens via the spec's open-question record, not via a ROADMAP edit.

## Risks

- **README's `status:` enum deviation.** The README pre-fills `status: <active | paused | done>` per HANDOVERS-5, deviating from the parent skeleton's `status: Draft`. The parent linter's `--check-template` mode accepts the augmented placeholder, so T2 passes. But the deviation is visible to any reader of `templates/_meta/README.md` who compares the Initiative template to the eight already-shipped F3.x templates and sees the inconsistency. **Mitigation:** the spec's OQ1 records the deviation and the deferred resolution; the README's body blockquote calls it out explicitly. If adversarial review pushes back, the fallback is to carry `status: Draft` and add an inline body note that the kit user must override to one of HANDOVERS-5's values on instantiation — but that fallback hides the contract from the YAML where audits would read it.
- **Inferred README H2 sections.** HANDOVERS-5 specifies folder *contents*, not the README's *internal* sections. The three H2 sections (`What this initiative is`, `Scope and bounded contexts`, `Delivery sequencing`) are inferred from folder-index practice. **Mitigation:** each H2 carries an inline HTML comment marking source-as-inferred; adversarial review explicitly checks the inferred set. If the reviewer rejects the taxonomy, iterate within the 3-pass limit; if no convergence, surface to parent fan-out aggregate and defer to a separate ROADMAP candidate.
- **Per-child frontmatter decision on `capabilities.md`.** The file lists multiple Capability (Domain E) objects but carries no frontmatter under the spec's OQ2 resolution. A future ROADMAP row that promotes Capabilities to per-file artifacts (e.g., `delivery/capabilities/<CAP-NNN>.md`) might reasonably want `capabilities.md` to become a frontmatter-bearing manifest at that point. **Mitigation:** the OQ2 record names this as the future-evolution path; T7e treats frontmatter-absence as a positive contract (a future change must also flip T7e).
- **ROADMAP F3.7 row prose-update at CAPTURE.** The CAPTURE phase rewrites ROADMAP F3.7's prose to enumerate `capabilities.md`. This is a substantive ROADMAP edit. **Mitigation:** the spec's OQ3 records the resolution and the CAPTURE step calls out the prose edit explicitly. If a ROADMAP maintainer disagrees, the resolution is documented and reverted to a checkbox-only flip — the spec then ships with HANDOVERS-5 as source-of-truth and ROADMAP's prose noted as a known-outdated enumeration.
- **Mermaid block validity.** `flow.md` and `sequence.md` ship with placeholder Mermaid blocks. The kit has no Mermaid syntax linter. **Mitigation:** the placeholder Mermaid is minimal-and-valid (rendered cleanly by GitHub's Mermaid renderer); visual inspection during VERIFY confirms. If a kit user pastes broken Mermaid into the instantiated artifact, that's a kit-user problem the template cannot prevent.
- **Pytest harness covers only README**, not the five narrative child files. **Mitigation:** the spec's OQ5 records the gap; spec-local T7a–T7e (frontmatter absence) plus T8b–T8f (heading presence) substitute. The gap is acceptable because the five files have no frontmatter — there is no `--check-template` validation to run against them. If a future ROADMAP row promotes any of these files to frontmatter-bearing, the harness glob needs widening at the same time.

## Changelog

Append entries when the plan changes substantially during execution. Format: `<YYYY-MM-DD>: <one-line description of the change and why>`.

- 2026-05-22: REVIEW iter-1 — adversarial-reviewer returned needs-fixes. Applied D2 fix (corrected source-comment attribution on the orientation H2s of `context-map.md` and `capabilities.md`: they are inferred folder-index orientation, not HANDOVERS-5 item-1/item-5 verbatim — those items source only the per-X fields below). Applied D1 mitigation (added an HTML comment in `context-map.md` documenting that HANDOVERS-5's folder-contents description mentions "shared shapes" but §"Required content" item 1 — the binding contract per the spec — does not; the shared-shape concern is absorbed into each H3's `**Public contract:**` descriptor; if HANDOVERS-5 promotes shared-shapes to a first-class field, the template adds a fifth labeled body line at that point). Spec-text findings (C1 internal "verbatim" inconsistency for `status:`; H1 missing OQ entry on item-1-as-exhaustive) deferred — OQ1 already documents the `status:` deviation and the README's inline comment on line 10 calls it out for readers; no contract bug. E1/E2/E3 deferred per reviewer disposition.
