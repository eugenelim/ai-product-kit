# Plan: template-kit-spec-frontmatter

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** approved

> **Plan contract.** Docs-only reconciliation. No code paths touched.

## Approach

Edit seven files in a single pass: AGENTS.md (line 91), .claude/CLAUDE.md (lines 40, 44), README.md (lines 11, 134, 135), CONTRIBUTING.md (line 35), docs/CHARTER.md (line 36), docs/CONVENTIONS.md (line 7 + new sub-section), docs/_templates/spec.md (one note). All small text additions/narrowings. No new files. No script changes.

Order matters only in that CONVENTIONS.md gains the new sub-section first (Task 1), so every other file's exemption-pointer parenthetical resolves to a real target. All other edits are line-precise — no `replace_all`, no global pattern matches — each edit names the exact sentence being narrowed.

## Constraints

- Do not edit the YAML example block in AGENTS.md / .claude/CLAUDE.md / CONVENTIONS.md beyond the surrounding prose. The schema itself is unchanged.
- Do not change the spec template's existing required sections, header bullet block, or order.
- Do not add a `kit-spec` ontology entry.
- One commit. The four edits are one logical change.

## Tasks

### Task 1: CONVENTIONS.md gains the exemption sub-section (and line 7 narrowing)

- **Depends on:** none
- **Tests:**
  - T2 from spec passes.
  - T8 from spec passes (line 7 narrowed).
- **Approach:**
  - **Line 7 narrowing:** change "Markdown with YAML frontmatter for everything that isn't code." to "Markdown with YAML frontmatter for every product artifact that isn't code (kit-meta scaffolding — specs, plans, state — is exempt; see §"Specs and Plans")."
  - **New sub-section:** after the "Cite upward, never downward" sub-section, insert `### Exempt from the universal metadata schema` with the exact text from the spec's "Exemption-text contract" section.
- **Done when:** T2 and T8 pass.

### Task 2: AGENTS.md line 91 narrowed

- **Depends on:** Task 1
- **Tests:** T1a and T1b from spec pass.
- **Approach:** At AGENTS.md line 91, replace `Every artifact carries explicit frontmatter:` with `Every product artifact carries explicit frontmatter (kit-meta scaffolding — specs, plans, state — is exempt; see` `` `docs/CONVENTIONS.md` `` §"Specs and Plans"):
- **Done when:** T1a and T1b pass.

### Task 3: .claude/CLAUDE.md lines 40 and 44 narrowed

- **Depends on:** Task 1
- **Tests:** T4a and T4b from spec pass.
- **Approach:**
  - Line 40: replace `Every artifact declares its` `` `object_type:` `` `per` `` `context/frameworks/ontology.md` `` `.` with `Every product artifact declares its` `` `object_type:` `` `per` `` `context/frameworks/ontology.md` `` `.` (only the first three words change; the rest of the line is preserved).
  - Line 44: same narrowing pattern — `Every artifact declares` → `Every product artifact declares`.
- **Done when:** T4a and T4b pass.

### Task 4: README.md lines 11, 134, 135 narrowed

- **Depends on:** Task 1
- **Tests:** T5a and T5b from spec pass.
- **Approach:**
  - Line 11: replace `Every artifact declares the phase it serves` with `Every product artifact declares the phase it serves`.
  - Line 134: replace `Every artifact declares its` `` `object_type:` `` `and links into the traceability chain.` with `Every product artifact declares its` `` `object_type:` `` `and links into the traceability chain.`
  - Line 135: replace `every artifact declares` `` `human_owned_decisions:` `` with `every product artifact declares` `` `human_owned_decisions:` ``.
- **Done when:** T5a and T5b pass.

### Task 5: CONTRIBUTING.md line 35 narrowed

- **Depends on:** Task 1
- **Tests:** T6 from spec passes.
- **Approach:** At line 35, replace `Every artifact declares` `` `object_type:` `` `per the ontology in` with `Every product artifact declares` `` `object_type:` `` `per the ontology in` (kit-meta scaffolding — specs, plans, state — is exempt; see` `` `docs/CONVENTIONS.md` `` §"Specs and Plans").`. Apply the same parenthetical to the human_owned_decisions sentence later in the same line.
- **Done when:** T6 passes.

### Task 6: docs/CHARTER.md line 36 narrowed

- **Depends on:** Task 1
- **Tests:** T7 from spec passes.
- **Approach:** Replace `Every artifact declares its` `` `object_type:` `` `and uses the universal metadata schema.` with `Every product artifact declares its` `` `object_type:` `` `and uses the universal metadata schema (kit-meta scaffolding is exempt; see` `` `docs/CONVENTIONS.md` `` §"Specs and Plans").`
- **Done when:** T7 passes.

### Task 7: spec template carries the exemption note

- **Depends on:** Task 1
- **Tests:** T3 from spec passes.
- **Approach:** In `docs/_templates/spec.md`, after the bullet block ending with `- **Constrained by:** ...` and before the existing `> **Spec contract.**` blockquote, insert a one-line italic note: `_Specs are exempt from the universal metadata schema (see` `` `docs/CONVENTIONS.md` `` §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._`
- **Done when:** T3 passes.

### Task 8: verify no regression and ontology stays clean

- **Depends on:** Tasks 1–7
- **Tests:** T9, T10, T11 from spec all pass.
- **Approach:**
  - Run `python3 tools/lint-frontmatter.py --all` — should still exit 0.
  - Run `bash tools/pre-pr.sh` — should still exit 0.
  - Run T11's precise grep (`'^\|\s*([Kk]it[ -][Ss]pec)\s*\|'`) — should return 0 hits.
- **Done when:** all three commands return their expected exit codes.

## Rollout

- AGENTS.md, `.claude/CLAUDE.md`, CONVENTIONS.md, and the spec template are the rollout. No other reference docs are affected.
- ROADMAP.md F0.11 row is marked `Shipped: 2026-05-21` in the CAPTURE phase.
- INVENTORY.md does not need a row (this is a docs reconciliation, not a new component).

## Risks

- **Linguistic drift between the seven narrowed files.** Mitigation: each narrowed file is verified by a positive AND a negative grep (Tests T1a/T1b, T4a/T4b, T5a/T5b). If a narrowing was applied incompletely (positive added but negative not removed), the negative-grep test fails.
- **A future contributor adds frontmatter to a spec, thinking it's required.** Mitigation: the one-line exemption note in the template is visible at scaffolding time; CONVENTIONS.md sub-section is the authoritative rationale and is linked from every narrowed file.
- **A reader of `docs/inspiration/*` encounters the unnarrowed claim.** Accepted: inspiration docs are imported source material per Non-goals; they are not authoritative.

## Changelog

- 2026-05-21: T11 grep refined from `kit-spec|Kit Spec` to a table-row anchored pattern (`'^\|\s*([Kk]it[ -][Ss]pec)\s*\|'`) after the original pattern produced a false-positive substring match against the pre-existing prose "kit-specific" in ontology.md §I's heading. Spec and plan updated in the same edit pass.
- 2026-05-21 (iter 2): Post-execute adversarial review surfaced two unnarrowed claims in CONVENTIONS.md not covered by the original scope: line 14 ("Every kit artifact carries the frontmatter block below" — the §"Universal metadata schema" opener) and the YAML example-block comment "Human-vs-AI ownership (every artifact must declare this)". Both narrowed. T8b and T8c added to the spec as negative-assertion contract tests for these two phrases. Line 14 also carries an inline anchor pointer to the exemption sub-section so a reader landing on the section header gets the qualifier without scrolling 200 lines.
