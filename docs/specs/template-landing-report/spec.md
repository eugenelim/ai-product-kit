# Spec: template-landing-report

- **Status:** Shipped (2026-05-22)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template
- **Serves kit phase:** Landings
- **Constrained by:** `docs/specs/template-authoring-convention/spec.md` (parent authoring contract — every F3.x template must obey it); `docs/HANDOVERS.md` §"Handover 7: Engineering → Landings" (required frontmatter and required sections source-of-truth); `docs/CONVENTIONS.md` §"Templates" + §"Universal metadata schema" + §"Lifecycle states"; `context/frameworks/ontology.md` (Landing Report composite in Domain I; Outcome and KPI atomics in Domain D; Decision in Domain H); ROADMAP **F3.10**.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `templates/landing-report.md` — the single-file skeleton a kit user copies to produce a real Landing Report at `delivery/landings/<slug>.md`. The Landing Report is the Engineering → Landings handover artifact (Handover 7 in `docs/HANDOVERS.md`): it gates whether a shipped initiative gets adopted, fixed, or killed, and it feeds the next quarterly `/strategy-refresh`. The template pre-fills the template's identity (`object_type: Landing Report`, `status: Draft`, the H1, and the seven required-section headings quoted verbatim from HANDOVERS), leaves every other field as an angle-bracket placeholder, and passes `tools/lint-frontmatter.py --check-template`.

## Objective

Author the literal file `templates/landing-report.md` — derived by copying `templates/_meta/template-skeleton.md`, replacing the generic body with the seven Handover-7 required sections quoted verbatim from `docs/HANDOVERS.md`, appending Handover-7-specific frontmatter under the `# Handover-specific fields` block, and pre-filling the four identity fields (`object_type: Landing Report`, `status: Draft`, the H1 `# Landing Report`, and the spec-cite blockquote). The file becomes the canonical entry point a kit user copies when producing a Landing Report. Downstream, ROADMAP **P5.1 `/landing-report`** generates instantiated Landing Reports by filling this template; ROADMAP **P5.9 `/audit-landings-debt`** flags shipped initiatives missing one. Without this template, both commands have no skeleton to write into and no shape to audit against.

## Why now

Foundation 3 fans out ten parallel template authors after `template-authoring-convention` shipped the shared skeleton and convention. F3.10 is the last template in the block. It directly unblocks:

- **P5.1 `/landing-report`** (depends on F3.10) — the command that synthesizes a Landing Report from the parent Vision's predictions plus the shipped initiative's measured outcomes.
- **P5.9 `/audit-landings-debt`** (depends on F1.1; consumes the Landing Report shape this template defines) — flags shipped initiatives with no landing report after 30 days.
- The future `/strategy-refresh` rhythm — Handover 7's "Feedback to strategy" section is the input loop that closes the operating model. Without a Landing Report template, refresh sessions have nothing structured to read.

Authoring this template now (in parallel with F3.1–F3.9) collapses ten serial loops into one parallel block. Cost: one tightly-scoped loop. Cost of skipping: P5.1 and P5.9 stall.

## Inputs and outputs

**Inputs.**

- `templates/_meta/template-skeleton.md` — the canonical skeleton this template copies and fills (parent convention, item 2 in the convention's §"Outputs").
- `docs/HANDOVERS.md` §"Handover 7: Engineering → Landings" — source-of-truth for required frontmatter and the seven required section headings; both are quoted verbatim into the template body.
- `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" — the placeholder syntax, frontmatter ordering, pre-fill rules, and linter contract.
- `docs/CONVENTIONS.md` §"Universal metadata schema" — the universal frontmatter superset every template carries.
- `context/frameworks/ontology.md` — confirms `Landing Report` is a Domain I composite (kit-composite handover artifact); confirms Outcome and KPI live in Domain D; confirms Decision lives in Domain H. These are existing types — none added.
- `tools/lint-frontmatter.py --check-template` — the linter mode whose exit code 0 is the goal-based gate for T2.
- `scripts/tests/test_templates_instantiate.py` — the pytest that walks `templates/*.md` and asserts `--check-template` exit 0 on each. This template enters the discovery set automatically once it lands at `templates/landing-report.md`.

**Outputs.**

1. `templates/landing-report.md` — a single-file template (single ontology object → single file). Universal-metadata schema block appears first (in CONVENTIONS.md order); a second block under a `# Handover-specific fields` YAML comment appears next, containing **only** the Handover-7 additions that are *not* already in the universal block. `object_type` (set to `Landing Report` in the universal block), `human_owned_decisions` (augmented in the universal block with the two HANDOVERS-mandated bullets), and `human_approval_required` (present in the universal block) are deliberately not duplicated here — a YAML comment names the design choice. The handover-specific block reads exactly:

   ```yaml
   # Handover-specific fields (per docs/HANDOVERS.md §"Handover 7: Engineering → Landings")
   # object_type, human_owned_decisions, human_approval_required: set in universal block above.
   parent_vision: <vision slug>
   parent_handoff_packet: <handoff packet slug>
   shipped: <YYYY-MM-DD>
   measured_at: <YYYY-MM-DD>     # at least 30 days post-ship
   verdict: <adopt | fix | kill>
   verdict_at: <YYYY-MM-DD>
   verdict_by: ["<name>: <YYYY-MM-DD>"]
   ```

   In the universal block, `human_owned_decisions` is augmented (the two HANDOVERS-mandated bullets `Verdict` and `Decision to revert, double-down, or fix` are pre-filled above the skeleton's trailing `<decision a human must make personally>` placeholder, which stays so a kit user knows additional decisions can be added). `object_type:` is pre-filled to `Landing Report`. `human_approval_required:` keeps the skeleton's `<true | false>` placeholder (HANDOVERS Handover 7 says `true` but the kit user owns that final keystroke). The `measured_at` line keeps the HANDOVERS comment verbatim (`# at least 30 days post-ship`) so the 30-day measurement-gap rule travels with the placeholder — the rule is content-level (the linter cannot detect it without comparing two dates against today; that's the runtime audit `/audit-landings-debt`'s job, not this template's). The H1 reads `# Landing Report`. The H1-following blockquote points to `docs/HANDOVERS.md` §"Handover 7: Engineering → Landings" and restates the 30-day measurement gap so the rule is visible above the fold. The seven required section headings appear in this exact order, verbatim from HANDOVERS Handover 7:

   1. `## The shipped change`
   2. `## Predicted outcomes vs actuals`
   3. `## Adoption curve`
   4. `## Counter-metrics`
   5. `## What landed and what didn't`
   6. `## Verdict`
   7. `## Feedback to strategy`

   Each section body is a single angle-bracket placeholder describing what the section contains (per HANDOVERS Handover 7's prose for that section).

2. `templates/_meta/README.md` — append a one-line entry under §"Shipped templates" pointing at `templates/landing-report.md` with a one-sentence description naming Handover 7. (Shared write target; see Plan §"Risks" for the concurrent-append rationale carried from the parent convention's §"Rollout".)

3. `ROADMAP.md` — F3.10's checkbox flipped to checked. No other ROADMAP edits.

A reader of this section should be able to construct the template diff without reading anything else.

## Boundaries

### Always do

- Quote the seven required section headings from `docs/HANDOVERS.md` §"Handover 7" **verbatim**. The template is a re-projection of HANDOVERS, not a parallel source-of-truth. Wording drift is the failure mode.
- Quote the Handover-7 frontmatter additions verbatim — including the `# at least 30 days post-ship` comment on the `measured_at` line. The comment is the only visual signal in the frontmatter that surfaces the 30-day measurement-gap invariant to a kit user reading the template; it must be preserved exactly.
- Use angle-bracket placeholder syntax exclusively. Curly braces, double underscores, `TBD`, `???` are all forbidden. The placeholder rule from the parent convention applies: atomic (`<…>`), augmented (`<role>: <YYYY-MM-DD>`-style), block-scalar, and nested-container forms accepted by `--check-template`.
- Pre-fill the template's identity: `object_type: Landing Report`, `status: Draft`, H1 `# Landing Report`. Nothing else is pre-filled.
- Place handover-specific frontmatter (the Handover-7 additions) under a `# Handover-specific fields` YAML comment, **after** the universal-schema block. Order matches the parent convention.
- When HANDOVERS-7 fields overlap with the universal-metadata schema (`object_type`, `human_owned_decisions`, `human_approval_required`), the field appears once — in its universal-schema position — carrying the HANDOVERS-7-mandated value. The universal-schema placeholder is deleted in the same edit. The handover-specific block carries only fields not present in the universal schema (`parent_vision`, `parent_handoff_packet`, `shipped`, `measured_at`, `verdict`, `verdict_at`, `verdict_by`).
- Keep the verdict enum as a single angle-bracket placeholder wrapping the three values: `verdict: <adopt | fix | kill>`. The pipe-separated form inside one placeholder preserves the enum visually without breaking the placeholder rule.
- Render `verdict_by` as an inline list with the augmented-placeholder form: `verdict_by: ["<name>: <YYYY-MM-DD>"]`. HANDOVERS shows `verdict_by: [<names>]` as a list of names only — but each kit-user filling this template should record *who* signed off *when*, mirroring the universal schema's `approvals_obtained: ["<role>: <YYYY-MM-DD>"]` convention. Inline-list-with-augmented-placeholder is the same form `template-skeleton.md` uses for `approvals_obtained`. (See Open Question 1 — this is a deliberate enrichment of HANDOVERS' `[<names>]`; if the F3.10 reviewer disagrees, fall back to `verdict_by: [<names>]`.)
- Render date placeholders as `<YYYY-MM-DD>` consistently across `shipped`, `measured_at`, `verdict_at`, `created`, `last_updated` — same form `template-skeleton.md` uses.

### Ask first

- Adding any required section beyond the seven HANDOVERS lists. The Optional sections heading is the place for extras; if Handover 7 should grow a section, that's a HANDOVERS edit through an RFC, not a template author's call.
- Adding frontmatter fields not in HANDOVERS Handover 7 or in the universal schema. If a kit user needs something extra for their org, that's a fork; the template stays minimal.
- Substituting the augmented `verdict_by: ["<name>: <YYYY-MM-DD>"]` form back to HANDOVERS' simpler `verdict_by: [<names>]`. The augmented form makes the timestamp visible to kit users; reverting reduces guidance. Surface to reviewer.

### Never do

- Invent body content for any required section. The seven section bodies are angle-bracket placeholders only — no example outcomes, no fictional KPIs, no fictional verdict text. The skeleton is shape-only, domain-agnostic.
- Weaken the verdict enum. The three values are `adopt`, `fix`, `kill`. No fourth value, no merging of `fix` and `adopt`, no synonyms.
- Add `Landing Report Verdict` or any new ontology type. Landing Report, Outcome, KPI, Decision are existing types — Domain I, Domain D, Domain D, Domain H respectively. No additions.
- Weaken or remove the `# at least 30 days post-ship` HANDOVERS comment on `measured_at`. That comment is the placement-level invariant signal.
- Edit `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `templates/_meta/template-skeleton.md`, `tools/lint-frontmatter.py`, `scripts/tests/test_templates_instantiate.py`, or `context/frameworks/ontology.md` from this loop. All are shared with other F3.x workers and the parent convention. Read-only inputs.

## Verification mode

- **Goal-based check** for the template file's shape contract — `tools/lint-frontmatter.py --check-template templates/landing-report.md` exits 0. This is the primary gate; the template's "shape" is its contract.
- **Audit-driven** for kit-wide health — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (the template lands inside the test's discovery set automatically); `bash tools/pre-pr.sh` exits 0.

Both modes are inherited from the parent convention. No new verification machinery introduced by this spec.

## Contract tests

Each test is one shell line or one pytest case. They are the gate.

- **T1** — file exists: `test -f templates/landing-report.md`.
- **T2** — linter passes in `--check-template` mode: `python3 tools/lint-frontmatter.py --check-template templates/landing-report.md` exits 0. This exercises both the augmented placeholder for `verdict_by: ["<name>: <YYYY-MM-DD>"]` and every date placeholder (`shipped`, `measured_at`, `verdict_at`, `created`, `last_updated`).
- **T3** — required Handover-7 frontmatter keys present: a one-line Python check parses the file's YAML frontmatter and asserts the key set `{object_type, parent_vision, parent_handoff_packet, shipped, measured_at, verdict, verdict_at, verdict_by, human_owned_decisions, human_approval_required}` is a subset of the frontmatter keys.
- **T3b** — dedup block-placement invariant: `python3 -c "import yaml; body=open('templates/landing-report.md').read(); hs=body.split('# Handover-specific fields',1)[1].split('---',1)[0]; d=yaml.safe_load('---\n'+hs); assert d is None or ('object_type' not in d and 'human_owned_decisions' not in d and 'human_approval_required' not in d), 'dedup violated — these keys must live in universal-schema block only'"` exits 0. Catches the failure mode where `object_type`, `human_owned_decisions`, or `human_approval_required` get duplicated into the handover-specific block (YAML last-write-wins would mask this from T3).
- **T4** — the seven required section headings appear verbatim in HANDOVERS-defined order. A one-line Python check finds each heading's offset in the file and asserts the offsets are all positive and strictly increasing in the order listed under §"Outputs" item 1.
- **T5** — angle-bracket placeholders only: `grep -E "(\{\{|__FILL__|\?\?\?| TBD)" templates/landing-report.md` returns zero matches.
- **T6** — pytest discovery picks up the new template and `--check-template` passes on it: `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0.
- **T7** — kit-wide health: `bash tools/pre-pr.sh` exits 0.
- **T8** — ROADMAP F3.10 checked: `grep -E "^- \[x\] \*\*F3\.10\*\*" ROADMAP.md` returns exactly one line.
- **T9** — `_meta/README.md` lists this template under §"Shipped templates" with a link target of `../landing-report.md`: `grep -E "landing-report\.md" templates/_meta/README.md` returns at least one line.
- **T10** — verdict-enum placeholder preserved exactly: `grep -E "^verdict: <adopt \| fix \| kill>$" templates/landing-report.md` returns exactly one line.
- **T11** — `# at least 30 days post-ship` comment preserved verbatim on the `measured_at` line: `grep -E "^measured_at: <YYYY-MM-DD>\s+# at least 30 days post-ship$" templates/landing-report.md` returns exactly one line.
- **T12** — `status: Draft` is pre-filled (matches skeleton): `grep -E "^status: Draft" templates/landing-report.md` returns exactly one line.
- **T13** — `object_type: Landing Report` is pre-filled: `grep -E "^object_type: Landing Report$" templates/landing-report.md` returns exactly one line.
- **T14** — no new ontology type added: `grep -nE "^(\|\s*)?[Ll]anding [Rr]eport [Vv]erdict" context/frameworks/ontology.md` returns zero hits.
- **T15** — skeleton's `## Optional sections` block preserved: `grep -cE "^## Optional sections" templates/landing-report.md` returns exactly 1.

## Non-goals

- **Not building `/landing-report` (P5.1).** That's a separate command spec. F3.10 is upstream — it ships the file the command writes into.
- **Not building `/audit-landings-debt` (P5.9).** That's a separate audit spec. F3.10 is upstream — it ships the shape the audit reads.
- **Not authoring an instantiated landing report.** No `delivery/landings/<slug>.md` is produced by this loop. The template is shape-only.
- **Not editing HANDOVERS Handover 7.** This template re-projects HANDOVERS verbatim; if HANDOVERS Handover 7 needs to change, that's an RFC against the handover contract, not work for F3.10.
- **Not authoring `context/frameworks/landings-rhythm.md`** or any other framework reference about how landings feed strategy refreshes. Out of scope.
- **Not changing the universal-metadata schema.** Inherited from CONVENTIONS verbatim via the skeleton.
- **Not adding `tools/new-template.sh` convenience tooling.** Out of scope per parent convention's Open Question 3.

## Open questions

1. **`verdict_by` placeholder shape — augmented vs. simple list.** HANDOVERS Handover 7 shows `verdict_by: [<names>]` (a list of names only). This template renders it as `verdict_by: ["<name>: <YYYY-MM-DD>"]` (augmented form, mirroring the universal schema's `approvals_obtained` convention in `template-skeleton.md`). Rationale: the augmented form makes the *date of sign-off* a visible required field per signer, which matches how the kit treats every other approval-style record. Risk: it diverges very slightly from HANDOVERS' literal text. _Resolved: augmented form `["<name>: <YYYY-MM-DD>"]` retained; deviation from HANDOVERS-7's `[<names>]` literal text is intentional, mirrors the skeleton's `approvals_obtained:` pattern, and is documented in a YAML inline-comment on the field itself in the template body._

2. **30-day measurement-gap visualization — comment alone vs. richer signal.** The `# at least 30 days post-ship` comment on the `measured_at` line is the only signal in the frontmatter about the 30-day rule. Should the H1-following blockquote also restate it? _Resolved: blockquote retained as additive user guidance; the YAML `# at least 30 days post-ship` comment is the non-negotiable HANDOVERS-7 signal. Both kept; T11 asserts the YAML comment only._

3. **Whether to add a P5.9 forward-reference to this spec's `Cross-references` block before P5.9 itself is shipped.** _Proposed resolution: yes — listing P5.9 as a consumer documents the contract direction even if P5.9 is still planned. Mark `(planned — ROADMAP P5.9)` to match the kit's drift convention._

## Acceptance criteria

A reviewer reads this list to decide whether to approve a PR. Each criterion is a verifiable predicate matching a contract test above.

- [ ] T1 passes — `templates/landing-report.md` exists.
- [ ] T2 passes — `--check-template` exits 0.
- [ ] T3 passes — all ten Handover-7 frontmatter keys present.
- [ ] T3b passes — `object_type`, `human_owned_decisions`, `human_approval_required` are absent from the handover-specific block (dedup invariant).
- [ ] T4 passes — the seven required section headings appear verbatim in order.
- [ ] T5 passes — angle-bracket placeholders only; no `{{`, `__FILL__`, `???`, or ` TBD`.
- [ ] T6 passes — pytest discovers and lints the new template.
- [ ] T7 passes — `tools/pre-pr.sh` exits 0.
- [ ] T8 passes — ROADMAP F3.10 row is checked.
- [ ] T9 passes — `templates/_meta/README.md` lists this template.
- [ ] T10 passes — verdict enum placeholder is exactly `<adopt | fix | kill>`.
- [ ] T11 passes — `measured_at` line preserves the HANDOVERS-verbatim `# at least 30 days post-ship` comment.
- [ ] T12 passes — `status: Draft` is pre-filled.
- [ ] T13 passes — `object_type: Landing Report` is pre-filled.
- [ ] T14 passes — no new ontology type added.
- [ ] T15 passes — skeleton's `## Optional sections` block survives in the template.
- [ ] Adversarial review converges clean within ≤ 3 iterations.

## Cross-references

- **Consumed by:**
  - **P5.1 `/landing-report`** *(planned — ROADMAP P5.1; explicit dependency on F3.10)* — copies this template and fills it with predicted-vs-actual outcomes from the parent Vision + adoption data.
  - **P5.9 `/audit-landings-debt`** *(planned — ROADMAP P5.9)* — flags shipped initiatives missing a Landing Report after 30 days; reads the shape this template defines.
  - **Future `/strategy-refresh`** *(planned — ROADMAP P7.1)* — Handover 7's "Feedback to strategy" section is the input the next quarterly refresh reads; this template structures that input.
- **Consumes:**
  - `docs/HANDOVERS.md` §"Handover 7: Engineering → Landings" — required frontmatter and required sections quoted verbatim.
  - `docs/CONVENTIONS.md` §"Templates" + §"Universal metadata schema" + §"Lifecycle states" — placeholder syntax, frontmatter ordering, pre-fill rules.
  - `templates/_meta/template-skeleton.md` — the literal skeleton copied as the starting point.
  - `context/frameworks/ontology.md` — confirms Landing Report (Domain I), Outcome and KPI (Domain D), Decision (Domain H) all exist; no additions.
- **Frontmatter fields owned:**
  - Reads/writes: `object_type`, `parent_vision`, `parent_handoff_packet`, `shipped`, `measured_at`, `verdict`, `verdict_at`, `verdict_by`, `human_owned_decisions`, `human_approval_required` (Handover-7 additions), plus the universal schema superset inherited from the skeleton.
- **Ontology object types touched:**
  - Landing Report (Domain I composite) — primary; this is the type the template instantiates.
  - Outcome, KPI (Domain D) — referenced by the §"Predicted outcomes vs actuals" and §"Counter-metrics" sections; the Vision's predicted thresholds carry KPI ids forward.
  - Decision (Domain H) — the §"Verdict" section produces a Decision (`adopt | fix | kill`) tied to `verdict_at` and `verdict_by`.
