# Plan: template-handoff-packet

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-22)
- **Plan review:** approved (pre-EXECUTE adversarial review iter-1 returned 3 Block + 6 Needs-fix + 5 Defer findings on 2026-05-22; all Block + Needs-fix findings resolved in-spec/in-plan; Defer findings logged as spec OQ7–OQ11)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

One single-commit task: scaffold `templates/handoff-packet/` as a folder template with 23 child files in the order HANDOVERS-6 names them — `README.md`, then 21 narrative markdown files (frontmatter-free), then `requirements.yaml` (YAML data file). Pre-fill identity on the README (`object_type: Handoff Packet`, `status: Ready for Engineering`), encode required sections per the spec's section taxonomy, append HANDOVERS-6-specific frontmatter on the README only (the six fields plus the `fixed_vs_flexible:` nested map), then VERIFY → REVIEW → CAPTURE. 22 of the 23 child files carry **no markdown frontmatter** per spec OQ4 resolution; `requirements.yaml` is a YAML data file whose entries carry Requirement-level ontology metadata. The folder layout is mechanical: a kit user `cp -r templates/handoff-packet/ delivery/handoff-packets/<slug>/` lands them in the exact layout HANDOVERS-6 contracts and the future P4.11 command will target.

Sequencing inside the task: scaffold the folder; copy the skeleton to `templates/handoff-packet/README.md` and adapt (the most complex file — universal-schema frontmatter, HANDOVERS-6 second frontmatter block including the `fixed_vs_flexible:` nested map, three inferred H2 sections, folder-index table pre-filled with 22 sibling rows); author `requirements.yaml` from scratch (YAML data file with one placeholder Requirement entry); author the 21 narrative child files from scratch (each frontmatter-free, with file-specific sub-templates per spec §"Outputs" 3–23). VERIFY runs the contract tests T1–T18. REVIEW dispatches `adversarial-reviewer`. CAPTURE updates `templates/_meta/README.md`, ROADMAP F3.9 (checkbox flip only — no prose update needed; the row's prose already enumerates 23 files), and freezes spec.md / plan.md statuses.

Why one task rather than 23: the 23 files are tightly coupled (same folder, same template identity, same VERIFY pass). Splitting into 23 tasks (or even into 3 tasks — README, YAML, narratives) would multiply pre-pr.sh runs and adversarial-review hand-offs with no parallelism gain. This matches the F3.4 (`templates/experiment/`) and F3.7 (`templates/initiative/`) precedents: each shipped its child files in one commit.

## Constraints

- **Parent-convention prerequisite (C1).** F3.9's EXECUTE depends on the parent `template-authoring-convention` being live on the branch EXECUTE runs from — specifically (a) `tools/lint-frontmatter.py` supports the `--check-template <path>` mode (gates T2), (b) `scripts/tests/test_templates_instantiate.py` exists and auto-discovers `templates/*/README.md` (gates T16), (c) `templates/_meta/template-skeleton.md` exists for the README copy step. As of this PLAN-phase commit on `main` (post-merge of PR #1 at 2026-05-22), all three prerequisites are live. If any prerequisite is missing at EXECUTE time, EXECUTE must not begin — rebase onto current `main`.
- Angle-bracket placeholder syntax only across all 23 files (markdown placeholders); no `{{...}}` or `__FILL__`. In `requirements.yaml`, placeholders use the same angle-bracket form; where YAML's plain-scalar rules are ambiguous (e.g., values containing `|` like `<Low | Medium | High | Critical>`), double-quote the value.
- README's universal-schema frontmatter block ordering identical to `templates/_meta/template-skeleton.md`. The HANDOVERS-6-specific keys (`completeness_audit_passed`, `adversarial_review_passed`, `quality_engineer_review_passed`, `compliance_review_status`, `engineering_partner`, `fixed_vs_flexible`) appear under a `# Handover-specific fields (per HANDOVERS.md Handover 6)` YAML comment line. (This is a logical grouping inside a single `---`...`---` YAML document, not a second `---`-delimited block — same constraint as F3.7.)
- README's `status:` value is the concrete enum value `Ready for Engineering`. This is a deviation from the parent skeleton's default `status: Draft`, mandated by HANDOVERS-6. Unlike F3.7, the value is **in the LIFECYCLE_STATES enum** so the default-mode linter on an instantiated packet accepts it — no enum override needed and no spec OQ to track.
- README's `object_type:` is the literal two-token string `Handoff Packet` (Domain H, line 150 of `context/frameworks/ontology.md`); the file's H1 reads `# Handoff Packet`.
- 21 narrative child files (`business-objective.md`, `customer-segment.md`, `personas.md`, `problem.md`, `jobs-to-be-done.md`, `current-workflow.md`, `future-workflow.md`, `capabilities.md`, `features.md`, `business-rules.md`, `policy-constraints.md`, `acceptance-criteria.md`, `non-functional-requirements.md`, `risks.md`, `dependencies.md`, `open-questions.md`, `out-of-scope.md`, `decision-log.md`, `launch-considerations.md`, `success-metrics.md`, `human-owned-decisions.md`) carry **no YAML frontmatter**. First non-blank line of each is the H1 heading.
- `requirements.yaml` is a YAML data file with `# ...` comment as the first line (for the source citation), not a markdown frontmatter `---` delimiter. The file's top-level key is `requirements:` whose value is a YAML block-list with one placeholder Requirement entry carrying the ten keys named in spec §"Outputs" item 2.
- File names pinned: 23 files exactly, names matching HANDOVERS-6's "Folder contents" block verbatim. No suffix variants; no plural variants; no combinations or splits (in particular, no `risks-and-mitigations.md` and no separate `mitigations.md` — HANDOVERS-6's `risks.md ← with mitigations` is one file).
- Cross-cutting dedup convention applied: where HANDOVERS-6's frontmatter overlaps with the universal-metadata schema (`object_type`, `parent_initiative`, `status`), the field appears once in its universal-schema position carrying the HANDOVERS-6-mandated value. The handover-specific second block carries only the six fields not in the universal schema.
- Must not modify `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, `scripts/tests/test_templates_instantiate.py`, or `templates/_meta/template-skeleton.md`. Surfacing a contract-gap finding is allowed in adversarial review; resolving it is a separate spec.
- Must not modify `.claude/commands/audit-completeness.md`. The 25-item checklist is the verification surface; the spec's §"Outputs" 3–23 encodes the file-mapping. If the checklist gains a machine-readable mapping table later, that's a separate spec.
- Stdlib + `pyyaml` only (no new dependencies; `pyyaml` is already a kit dependency via `scripts/lib/frontmatter.py`).
- Atomic writes (the `Write` tool already writes atomically; no `tempfile + os.replace` plumbing needed beyond it).

## Construction tests

Cross-cutting only. Per-task tests are inline under the single task below.

- `pre-pr-clean` — `bash tools/pre-pr.sh` exits 0 before the commit (run after VERIFY, before CAPTURE).

## Tasks

### Task 1: `templates/handoff-packet/` folder template lands with 23 child files; README passes `--check-template`; the 21 narrative files are frontmatter-free; `requirements.yaml` is well-formed YAML with one Requirement entry; pytest auto-discovery includes README; adversarial review clean

- **Depends on:** none (parent convention `template-authoring-convention` is already shipped 2026-05-22; the skeleton and `--check-template` mode are live).
- **Tests:** (every spec contract test)
  - `T1` — folder + all 23 child files exist (shell loop).
  - `T1b` — folder contains exactly 23 files, no extras.
  - `T2` — `--check-template templates/handoff-packet/README.md` exits 0.
  - `T3` — README frontmatter contains the universal-schema key set.
  - `T4` — README frontmatter contains the six HANDOVERS-6-specific keys.
  - `T4b` — README `fixed_vs_flexible:` is a map with three sub-keys.
  - `T4c` — README retains `parent_initiative:`.
  - `T5` — README `object_type: Handoff Packet` exact and `status: Ready for Engineering` exact.
  - `T6` — README four audit-gate fields carry safe augmented-placeholder values, not concrete dates or `passed` literals.
  - `T7` — none of the 21 narrative files carries YAML frontmatter (shell loop; `head -5 <file> | grep -c '^---'` returns 0 for each).
  - `T7b` — `requirements.yaml` does not lead with a `---` delimiter.
  - `T8` — required H1 heading present on each of the 22 markdown files (file-specific strings per spec §"Contract tests" T8).
  - `T8b` — README required H2 headings present in order.
  - `T8c` — `launch-considerations.md` required H2 headings present.
  - `T9` — README's folder-index table names all 22 sibling files (shell loop).
  - `T10` — `risks.md` body references a Mitigation field.
  - `T11` — `decision-log.md` cites `docs/adr/`.
  - `T12` — `personas.md` references `context/personas/`.
  - `T13` — angle-bracket-only placeholders across the folder.
  - `T14` — `requirements.yaml` parses with `yaml.safe_load`.
  - `T15` — `requirements.yaml` first entry carries the ten Requirement-metadata keys.
  - `T15b` — `requirements.yaml` first entry has `object_type: Requirement`.
  - `T16` — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0.
  - `T17` — `bash tools/pre-pr.sh` exits 0.
  - `T18` — `python3 tools/lint-frontmatter.py --all` exits 0 (mode-separation by non-traversal).
  - `T19` — `/audit-completeness` checklist file-mapping is complete (every checklist item ∈ {1..25} has at least one file).
  - `T20` — ROADMAP F3.9 checkbox flipped (CAPTURE-phase).
  - `T20b` — ROADMAP F3.9 row prose grep contains the 23-file enumeration (CAPTURE-phase).
  - `T21` — `templates/_meta/README.md` lists `handoff-packet/` (CAPTURE-phase).
  - `T22` — adversarial-reviewer Blocking-findings count is 0.
- **Approach:**
  1. **Scaffold.** `mkdir -p templates/handoff-packet/`. No `tools/new-template.sh` exists (deferred per parent spec); use the kit's standard `mkdir` + `cp` pattern.
  2. **README.md — copy and adapt skeleton.** `cp templates/_meta/template-skeleton.md templates/handoff-packet/README.md`. Then edit:
     - Pre-fill `object_type: Handoff Packet` (replace the `<pre-filled per template ...>` placeholder).
     - **Override** `status: Draft` (skeleton default) with `status: Ready for Engineering` per HANDOVERS-6. No augmented-placeholder syntax — the concrete value is in `LIFECYCLE_STATES` and is the pre-fill per HANDOVERS-6. Immediately under the `status:` line, insert an inline HTML body warning comment (mandatory per spec OQ7 + §"Boundaries → Always do"): `<!-- WARNING: pre-filled to satisfy LIFECYCLE_STATES; the four audit-gate date fields above (completeness_audit_passed / adversarial_review_passed / quality_engineer_review_passed / compliance_review_status) MUST be completed with concrete values before this packet is handed to engineering. -->`. If adversarial review during EXECUTE rejects the warning-comment mitigation, the fallback is to switch the pre-fill to the augmented-placeholder form `<Ready for Engineering>` and update T5 accordingly.
     - Pre-fill `human_owned_decisions:` with three HANDOVERS-6-aligned strings: `Final fixed_vs_flexible classification`, `Compliance review acceptance`, `Engineering partner sign-off`. (These are derived from the README's audit-gate fields; the actual human decisions the packet locks in.) **NOTE — flag during adversarial review:** HANDOVERS-6 does not list `human_owned_decisions:` strings verbatim the way HANDOVERS-5 does for the Initiative. If the reviewer rejects the derived strings, fall back to the skeleton's single `<decision a human must make personally>` placeholder.
     - Pre-fill `parent_initiative: <slug>` in the universal-schema traceability block (the field already exists in the skeleton's traceability block as `parent_initiative:`; per the cross-cutting dedup convention, the universal-schema position carries the HANDOVERS-6 value).
     - Delete the skeleton's other traceability fields that don't apply to a Handoff Packet (`parent_opportunity`, `parent_learning` — these have long since fed up into the Initiative by the time the packet exists); keep `parent_intent` and `parent_vision` for restated upstream traceability (matching the Initiative/Vision-template precedents).
     - Under the existing `# Handover-specific fields ...` comment, replace the example (Strategic Intent) line with the HANDOVERS-6 block — six keys: `completeness_audit_passed: <YYYY-MM-DD>`, `adversarial_review_passed: <YYYY-MM-DD>`, `quality_engineer_review_passed: <YYYY-MM-DD>`, `compliance_review_status: <passed | not-required | <YYYY-MM-DD>>` (augmented-placeholder form with nested angle brackets — consistent with spec T6 and the HANDOVERS-6 verbatim quote; `compliance_review_status:` is not enum-checked by the linter so concrete values `passed` / `not-required` / a date string all pass on instantiation), `engineering_partner: <name>`, and the `fixed_vs_flexible:` nested map with three sub-keys:
       ```yaml
       fixed_vs_flexible:
         fixed: [<requirement ids that must not change>]
         flexible: [<requirement ids open to engineering tradeoffs>]
         unknown: [<questions for engineering to weigh in on>]
       ```
       Update the YAML comment line itself to read `# Handover-specific fields (per HANDOVERS.md Handover 6)`.
     - Replace the H1 `<Artifact name>` with `# Handoff Packet`.
     - Replace the one-paragraph blockquote with: a single paragraph naming the artifact ("This is a Handoff Packet — the ontology's signature pre-engineering deliverable per Domain H"), citing HANDOVERS-6 by name (`docs/HANDOVERS.md` §"Handover 6: Spec → Engineering Handoff Packet"), citing the 25-item checklist (`/audit-completeness`) as the audit surface the packet must satisfy on instantiation, and naming the 22 sibling child files (by class — "21 narrative content files plus `requirements.yaml`").
     - Replace the body section-heading templates with the three inferred H2 sections per spec §"Required sections": `## Product brief`, `## Folder index`, `## Ready-for-engineering test`. Each H2 carries an inline HTML comment `<!-- source: inferred ... -->` so an adversarial reviewer can see the source-marker.
     - **Folder-index table.** Under `## Folder index`, author a markdown table with two columns: `| File | Purpose |`. Pre-fill 22 data rows, one per sibling file, in HANDOVERS-6's order. The Purpose column uses the verbatim gloss text where HANDOVERS-6 provides one (e.g., for `business-objective.md` → `cite the strategic intent`), and a one-line description otherwise (e.g., for `jobs-to-be-done.md` → `documented JTBDs for the target customer`).
     - **Ready-for-engineering test block.** Under `## Ready-for-engineering test`, author seven bulleted lines, one per clause of HANDOVERS-6's "ready for engineering" semantic test. Quoted verbatim where HANDOVERS-6 provides text.
     - **Remove** the `## Optional sections` heading and its example sub-section that the skeleton ships with. The Handoff Packet README is a structured Product Brief + folder index; the three required H2s are exhaustive per spec §"Boundaries → Always do" and §"Never do". T8b mechanically asserts exactly three H2 headings (no fourth).
  3. **business-objective.md — author from scratch (no frontmatter).** Body:
     - H1 `# Business objective`. One-paragraph orientation: cites the parent strategic intent (`parent_intent:` in README); maps to `/audit-completeness` checklist item 1.
     - Inline HTML comment `<!-- source: HANDOVERS-6 §"Folder contents" — `business-objective.md ← cite the strategic intent` -->`.
     - Body placeholder: one paragraph `<Restate the Business Objective per ontology Domain A — measurable outcome the business is pursuing.>`.
  4. **customer-segment.md — author from scratch (no frontmatter).** Body:
     - H1 `# Customer segment`. Orientation paragraph citing HANDOVERS-6 + the segment definition.
     - Inline HTML comment marking source (HANDOVERS-6 `cite the segment definition` gloss).
     - Body placeholder: one paragraph naming the segment + a pointer-to-segment-definition line `<Path to segment definition or inline summary.>`.
  5. **personas.md — author from scratch (no frontmatter).** Body:
     - H1 `# Personas`. Orientation paragraph noting that persona objects live under `context/personas/*.md` and this file is the manifest.
     - Inline HTML comment marking source.
     - A markdown table with two columns: `| Persona id | Link |`. One placeholder data row: `| <PERSONA-NNN> | [<persona-slug>](../../context/personas/<persona-slug>.md) |`. One-line note immediately after: `> Duplicate the data row for each persona relevant to this packet.`
  6. **problem.md — author from scratch (no frontmatter).** Body:
     - H1 `# Problem`. Orientation citing HANDOVERS-6's `validated problem statement + evidence` gloss and checklist items 4 + 5.
     - `## Problem statement` — H2 with one paragraph placeholder.
     - `## Evidence` — H2 with a sub-template mirroring the universal-schema `evidence_basis:` shape as prose: a markdown table with three columns `| Source | Strength | Link |` and one placeholder data row.
  7. **jobs-to-be-done.md — author from scratch (no frontmatter).** Body:
     - H1 `# Jobs to be done`. Orientation citing checklist item 7.
     - `## JTBDs in scope` — H2 with repeated H3 sub-template `### <JTBD short description>` containing three labeled body lines: `**Actor:** <persona id or role>`, `**Context:** <triggering situation>`, `**Outcome:** <successful completion criterion>`.
     - One-line note: `> Duplicate the H3 block above for each Job to be Done.`
  8. **current-workflow.md — author from scratch (no frontmatter).** Body:
     - H1 `# Current workflow`. Orientation citing HANDOVERS-6 `how it works today` gloss + checklist item 6.
     - `## Steps today` — H2 with a numbered-list sub-template: `1. <Step 1 — actor + action + system touched>` … `5. <...>`. One-line note: `> Add or remove steps as the actual workflow requires.`
  9. **future-workflow.md — author from scratch (no frontmatter).** Body:
     - H1 `# Future workflow`. Orientation citing HANDOVERS-6 `how it'll work` gloss.
     - `## Steps after shipping` — H2 with the same numbered-list sub-template as `current-workflow.md`.
     - `## What changes` — H2 with a one-paragraph callout naming the delta from `current-workflow.md` (which steps are new, which are removed, which are unchanged).
  10. **capabilities.md — author from scratch (no frontmatter).** Body:
      - H1 `# Capabilities`. Orientation noting that HANDOVERS-6's gloss `from the parent initiative` means this file restates the Capability list per the parent Initiative's contract (HANDOVERS-5 §"Handover 5: Initiative → Spec" — the canonical source of `capabilities:` for the parent Initiative); re-stated for engineering convenience; canonical source remains the parent Initiative. (Citing HANDOVERS-5 the contract — not F3.7 the template — keeps this plan independent of F3.7's EXECUTE status; F3.7 is a parallel F3.x row whose shipping is not a prerequisite for F3.9.)
      - At the top of the body, an HTML comment: `<!-- source: parent Initiative's capabilities list per HANDOVERS-5; canonical source remains the Initiative; copy and maintain in sync. -->` (per spec OQ8).
      - A markdown table with three columns: `| Capability id | Capability name | Linked Problem |`. One placeholder data row.
      - One-line note for duplication.
  11. **features.md — author from scratch (no frontmatter).** Body:
      - H1 `# Features`. Orientation citing checklist item 11.
      - A markdown table with three columns: `| Feature id | Feature name | Parent capability id |`. One placeholder data row.
      - One-line note for duplication.
  12. **requirements.yaml — author from scratch (YAML data file, no markdown frontmatter).**
      - First line: `# Requirements registry — per HANDOVERS-6 §"Folder contents" and ontology §"Domain E — Requirement".`
      - Second line: `# Each entry instantiates one Requirement object. Duplicate the entry block for additional requirements.`
      - Body:
        ```yaml
        requirements:
          - id: <REQ-NNN>
            object_type: Requirement
            description: "<one-line statement of what must be true>"
            parent_capability: <CAP-NNN>
            parent_feature: <FEAT-NNN>
            acceptance_criteria_ref: "<heading slug in acceptance-criteria.md>"
            risk_level: "<Low | Medium | High | Critical>"
            owner: "<named human or role>"
            status: "<Draft | In Review | Validated | Approved | Ready for Engineering>"
            fixed_vs_flexible: "<fixed | flexible | unknown>"
        ```
        Double-quote any value that contains a `|` (which is a YAML flow-indicator); leave bare scalars unquoted where unambiguous. Angle-bracket placeholders are accepted inside double-quoted YAML strings.
  13. **business-rules.md — author from scratch (no frontmatter).** Body:
      - H1 `# Business rules`. Orientation citing checklist item 14 + Domain E row "Business Rule".
      - Repeated `### <BR-NNN> — <rule name>` sub-template with three labeled body lines: `**Statement:**`, `**Source:**`, `**Related requirement ids:**`.
      - One-line note for duplication.
  14. **policy-constraints.md — author from scratch (no frontmatter).** Body:
      - H1 `# Policy constraints`. Orientation citing checklist item 15 + Domain E row "Policy Rule".
      - Repeated `### <POL-NNN>` sub-template with three labeled body lines: `**Statement:**`, `**Regulatory source:**`, `**Related requirement ids:**`.
      - One-line note for duplication.
  15. **acceptance-criteria.md — author from scratch (no frontmatter).** Body:
      - H1 `# Acceptance criteria`. Orientation citing HANDOVERS-6's `per-requirement` gloss + checklist item 13.
      - Repeated `### <REQ-NNN>` sub-template with a bulleted list of three placeholder acceptance criteria per requirement (`- <criterion 1>`, etc.).
      - One-line note for duplication.
  16. **non-functional-requirements.md — author from scratch (no frontmatter).** Body:
      - H1 `# Non-functional requirements`. Orientation citing checklist item 22 + Domain E row "Non-Functional Requirement".
      - Repeated `### <NFR-NNN>` sub-template with three labeled body lines: `**Statement:**`, `**Target threshold:**`, `**Related requirement ids:**`.
      - One-line note for duplication.
  17. **risks.md — author from scratch (no frontmatter).** Body:
      - H1 `# Risks`. Orientation citing HANDOVERS-6's `with mitigations` gloss + checklist items 16 + 17 (the Mitigation sub-field is the load-bearing mapping to item 17).
      - Repeated `### <RISK-NNN>` sub-template with four labeled body lines: `**Description:**`, `**Likelihood:** <Low | Medium | High>`, `**Impact:** <Low | Medium | High>`, `**Mitigation:** <one-line mitigation or control assignment>`.
      - One-line note for duplication.
  18. **dependencies.md — author from scratch (no frontmatter).** Body:
      - H1 `# Dependencies`. Orientation citing checklist item 18.
      - A markdown table with three columns: `| Dependency name | Type | Blocker level |`. The Type column placeholder is `<internal-team | external-vendor | upstream-system>`; the Blocker level column placeholder is `<hard | soft>`.
      - One placeholder data row; one-line note for duplication.
  19. **open-questions.md — author from scratch (no frontmatter).** Body:
      - H1 `# Open questions`. Orientation citing checklist item 19.
      - Repeated `### <Q-NNN>` sub-template with three labeled body lines: `**Question:**`, `**Owner:**`, `**Target resolution date:** <YYYY-MM-DD>`.
      - One-line note for duplication.
  20. **out-of-scope.md — author from scratch (no frontmatter).** Body:
      - H1 `# Out of scope`. Orientation citing checklist item 20.
      - A bulleted list sub-template: `- <Excluded item> — <one-line reason for exclusion>`. One placeholder bullet; one-line note for duplication.
  21. **decision-log.md — author from scratch (no frontmatter).** Body:
      - H1 `# Decision log`. Orientation citing HANDOVERS-6's `summary; full ADRs in docs/adr/` gloss + checklist item 25.
      - A markdown table with three columns: `| Decision date | Decision summary | ADR link |`. One placeholder data row pointing at `[<ADR-NNN>](../../docs/adr/<NNN>-<slug>.md)`.
      - One-line note for duplication.
  22. **launch-considerations.md — author from scratch (no frontmatter).** Body:
      - H1 `# Launch considerations`. Orientation citing checklist items 21 + 22.
      - Three H2 sub-sections:
        - `## Pricing and packaging` — one paragraph placeholder citing checklist item 21.
        - `## Support and operational readiness` — one paragraph placeholder citing checklist item 22.
        - `## Communications and rollout` — one paragraph placeholder for the kit user to enumerate the launch comms / rollout plan.
  23. **success-metrics.md — author from scratch (no frontmatter).** Body:
      - H1 `# Success metrics`. Orientation citing HANDOVERS-6's `KPIs with thresholds` gloss + checklist items 8 + 9.
      - Repeated `### <KPI-NNN> — <metric name>` sub-template with three labeled body lines: `**Current baseline:**`, `**Target threshold:**`, `**Measurement window:**`.
      - One-line note for duplication.
  24. **human-owned-decisions.md — author from scratch (no frontmatter).** Body:
      - H1 `# Human-owned decisions`. Orientation noting that the README's `human_owned_decisions:` frontmatter list is the machine-readable source and that this file is the human-readable elaboration; citing checklist items 23 + 24.
      - Repeated `### <Decision name>` sub-template with three labeled body lines: `**Decision:**`, `**Owner:**`, `**Status:** <pending | decided <YYYY-MM-DD>>`.
      - One-line note for duplication.
  25. **VERIFY.** Run T1 through T19 in order:
     - Shell loops for T1 + T1b.
     - One `python3 tools/lint-frontmatter.py --check-template` invocation for T2.
     - Python YAML-parse one-liner for T3 (walk the universal-schema keys).
     - Python YAML-parse one-liner for T4 (walk the six HANDOVERS-6 keys).
     - Python YAML-parse one-liner for T4b (inspect `fixed_vs_flexible:` sub-keys).
     - `grep -c '^parent_initiative:'` invocation for T4c.
     - Python YAML-parse one-liner for T5 (inspect `object_type` and `status`).
     - Python YAML-parse one-liner for T6 (regex-check the four audit-gate field values).
     - Shell loop for T7 (head/grep across the 21 narrative files).
     - One `head/grep` invocation for T7b on `requirements.yaml`.
     - Shell loop for T8 (file-specific H1 strings across 22 markdown files).
     - `grep -n` for T8b + T8c.
     - Shell loop for T9 (folder-index sibling-file coverage).
     - One `grep -c` per file for T10 + T11 + T12.
     - One `grep -rc` across the folder for T13.
     - `python3 -c 'import yaml; yaml.safe_load(open("templates/handoff-packet/requirements.yaml"))'` for T14.
     - Python one-liner for T15 + T15b (inspect first entry's keys and `object_type:`).
     - `python3 -m pytest scripts/tests/test_templates_instantiate.py` for T16.
     - `bash tools/pre-pr.sh` for T17. Iterate any reds.
     - `python3 tools/lint-frontmatter.py --all` for T18; assert exit 0 (default mode does not traverse `templates/` — the load-bearing mode-separation property).
     - Python one-liner for T19 (static mapping dictionary; every checklist item ∈ {1..25} maps to at least one file).
     - Defer T20 + T20b + T21 to CAPTURE.
  26. **REVIEW.** Dispatch `adversarial-reviewer` against all 23 files versus the constraint set (HANDOVERS §"Handover 6", parent authoring convention, ontology Domain H + E + G, `/audit-completeness` 25-item checklist mapping). Max 3 iterations per work-loop default. **Triage findings per spec OQ11**: Block findings must be resolved before VERIFY proceeds; Needs-fix findings must be resolved in-session in the same loop; Defer findings are added as new OQs in the spec and tracked as follow-on ROADMAP candidates. The iteration cap counts only iterations that produced new Block or Needs-fix findings. Specific things the reviewer should check: (a) the 21 narrative files carry no frontmatter; (b) `requirements.yaml` is a YAML data file with no markdown frontmatter and parses with `yaml.safe_load`; (c) the README's HANDOVERS-6 block matches verbatim including `fixed_vs_flexible:` nested-map structure; (d) the 25-item checklist's file-mapping (per spec §"Checklist-to-file mapping") is complete and unambiguous, with item 24's dual-target mapping (file + frontmatter field) intact; (e) the inferred sections (README's three H2s) carry source comments; (f) the dedup convention is consistently applied between universal-schema and HANDOVERS-6 fields; (g) the pre-filled `human_owned_decisions:` list (per step 2 above) is not over-asserting — fall back to a placeholder if the reviewer pushes back; (h) the README's status pre-fill warning comment is present and worded as specified in step 2.
  27. **CAPTURE.** In a single small commit at the end of the loop (per parent plan §Rollout — sequential README appends across F3.x workers):
     - Append a one-line entry to `templates/_meta/README.md` under "Shipped templates": `- \`handoff-packet/\` — Handoff Packet folder template (per HANDOVERS §"Handover 6"); README + 21 narrative content files + \`requirements.yaml\` (Requirement registry).` (gates T21).
     - Flip ROADMAP F3.9 checkbox: `- [ ] **F3.9**` → `- [x] **F3.9**` (gates T20). No prose update needed — the existing row prose enumerates the 23-file folder layout correctly (gates T20b).
     - Update `docs/specs/template-handoff-packet/spec.md` Status: `Shipped (<YYYY-MM-DD>)`.
     - Update `docs/specs/template-handoff-packet/plan.md` Status: `Done (<YYYY-MM-DD>)` and append a changelog entry.
- **Done when:** T1–T22 all pass; pre-pr-clean exits 0; adversarial review returns 0 Blocking findings.

## Rollout

- ROADMAP P4.11 (`/handoff-packet`) is unblocked once this template lands (P4.11's `Depends on:` line names F3.9 + F1.5; F1.5 is already shipped 2026-05-21).
- `templates/_meta/README.md` gets a new "Shipped templates" entry. Per parent plan §Rollout, F3.x workers' README appends are sequential — this F3.9 worker's append happens at CAPTURE time in its own commit.
- `docs/HANDOVERS.md` Handover 6 is unchanged; F3.9 is a downstream re-projection. The detector line on Handover 6 references `/audit-completeness` (shipped) plus the `adversarial-reviewer` (shipped) and `compliance-reviewer` + `quality-engineer` reviewers (planned — ROADMAP P6.1 / P6.2); none of those are coupled to F3.9's shape.
- `.claude/commands/audit-completeness.md` is unchanged; F3.9 's §"Outputs" 3–23 encodes the checklist-to-file mapping in the spec only. If a future ROADMAP row promotes the mapping into the command file or a runnable script extension, that's a separate spec.
- AGENTS.md and INVENTORY.md: no row added. The template is infrastructure (same pattern as `templates/_meta/template-skeleton.md`, `templates/experiment/`, and `templates/initiative/`); the parent convention spec already established that templates are not INVENTORY rows.
- F3.7 (`templates/initiative/`) consumes none of F3.9's shape — they are parallel. Spec OQ3 (single-file-brief alternative to the folder layout) becomes a new follow-up candidate at CAPTURE time only if a kit user requests it; the plan does NOT author this candidate inline.

## Risks

- **23 files vs 22 in the count.** Two count-related failure modes: (a) the kit user / template author misses one file (e.g., omits `non-functional-requirements.md` because it overlaps semantically with `requirements.yaml`); (b) the kit user / template author adds an extra file that "feels right" (e.g., `mitigations.md` split out of `risks.md`). **Mitigation:** T1 enumerates all 23 names verbatim; T1b pins the exact count; both are mechanical. The spec's §"Never do" explicitly forbids combinations and splits.
- **README's `human_owned_decisions:` pre-fill is derived, not HANDOVERS-sourced.** Unlike HANDOVERS-5 (which pins three strings for the Initiative), HANDOVERS-6 does not enumerate `human_owned_decisions:` strings for the Handoff Packet. The plan derives three strings from the README's audit-gate fields. **Mitigation:** §"Never do" does NOT pin specific strings; the adversarial review step 27.(g) explicitly tests this; if the reviewer pushes back, fall back to the skeleton's single `<...>` placeholder. The fallback is documented in the plan, not the spec, so the spec contract is not violated either way.
- **`requirements.yaml` as YAML data file (not markdown).** This is the only non-markdown file in the kit's `templates/` directory. Tooling that recursively walks `templates/` expecting markdown (e.g., a future markdown-link checker) would skip this file silently. **Mitigation:** the parent convention's OQ4 explicitly anticipates this child; T14 + T15 + T15b mechanically validate the file at template-ship time; the spec's §"Boundaries" → "Always do" and "Never do" make the YAML-data-file decision explicit.
- **Inferred README H2 sections.** HANDOVERS-6 specifies folder *contents*, not the README's *internal* sections. The three H2 sections (`Product brief`, `Folder index`, `Ready-for-engineering test`) are inferred from HANDOVERS-6's "Product Brief" framing and its seven-clause semantic test. **Mitigation:** each H2 carries an inline HTML comment marking source-as-inferred; adversarial review explicitly checks the inferred set.
- **Inferred sub-section taxonomy across 21 narrative files.** HANDOVERS-6 names the 23 files but does not prescribe each file's internal sub-section structure. The plan derives a sub-template per file. **Mitigation:** each H2 or H3 sub-template carries an inline HTML comment marking source (HANDOVERS-6 gloss text where it exists, inferred otherwise); spec OQ4 records the resolution; adversarial review checks per-file. If the reviewer rejects a sub-template, iterate per-file within the 3-pass limit.
- **`/audit-completeness` checklist-to-file mapping lives only in this spec.** The mapping is not in HANDOVERS-6 or in `.claude/commands/audit-completeness.md`. T19 validates the mapping at template-ship time but the mapping is itself a derived artifact. **Mitigation:** spec OQ5 records the resolution; if `/audit-completeness` later gains a machine-readable mapping table, this spec's mapping becomes the input. The empty template does not need to pass the audit; only the instantiated packet does.
- **Pytest harness covers only README**, not the 22 non-README files. **Mitigation:** spec-local T7 (frontmatter absence across the 21 narrative files), T7b (YAML file has no markdown frontmatter), T8 (per-file H1 strings across 22 markdown files), and T14 + T15 + T15b (`requirements.yaml` shape) substitute. The gap is acceptable because the 22 non-README files have no markdown frontmatter — there is no `--check-template` validation to run against them. If a future ROADMAP row promotes any of these files to frontmatter-bearing, the harness glob needs widening at the same time.
- **No Mermaid blocks.** Unlike F3.7, this template does not ship Mermaid blocks. No mitigation needed; this is a contrast, not a risk.

## Changelog

Append entries when the plan changes substantially during execution. Format: `<YYYY-MM-DD>: <one-line description of the change and why>`.

- 2026-05-22: EXECUTE+VERIFY+REVIEW+CAPTURE landed in one session on branch `eugenelim/implement-f3.9-spec`. Adversarial review returned pass with 0 critical / 2 Needs-fix / 5 Defer. Needs-fix fixes applied in-session: (a) reverted README warning-comment wording to spec-verbatim form (dropped explanatory prefix; restored "audit-gate date fields"); (b) added in-file callout to `requirements.yaml` that `parent_capability` + `parent_feature` fields satisfy `/audit-completeness` checklist item 12. Defer-V1 (engineering-ready phrasing in `open-questions.md`) also fixed in-session per the "small cosmetic defers in-session" rule. Other Defer findings (D2 blank-line cosmetic; H1 business-objective placeholder additive sub-prompts; H2 NFR "in part" cross-pointer; M2 future-workflow.md has no mapped checklist item — spec gap, not template bug) left as known limitations; M2 is the only one that may warrant a follow-up spec (extend `/audit-completeness` item 6 to cover both current and future workflow, or add a new checklist item).
