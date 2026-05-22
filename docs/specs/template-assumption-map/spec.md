# Spec: template-assumption-map

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template
- **Serves kit phase:** Validation (the artifact instantiated from this template lives at `validation/assumption-maps/<slug>.md`)
- **Constrained by:** parent spec `docs/specs/template-authoring-convention/` (authoring convention + skeleton + `--check-template` linter mode + Handover-2.5 text contract); `docs/HANDOVERS.md` §"Handover 2.5: Discovery → Assumption Map"; `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" + §"Universal metadata schema" + §"Lifecycle states"; `context/frameworks/ontology.md` Domain C (Assumption — atomic) and Domain I (Assumption Map — composite handover); ROADMAP F3.3 (this item) and ROADMAP D7 (the Handover-2.5 contract this template instantiates — already shipped by the parent spec on 2026-05-22).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** This document defines what "done" means for the F3.3 Assumption Map template. The deliverable is a single file at `templates/assumption-map.md` that a kit user copies into `validation/assumption-maps/<slug>.md` to produce a real Assumption Map artifact satisfying the Handover-2.5 contract.

## Objective

Ship a single-file template at `templates/assumption-map.md` that is a literal, copy-and-fill skeleton for the Assumption Map handover artifact. The template:

- Carries the universal-metadata schema frontmatter (per `docs/CONVENTIONS.md` §"Universal metadata schema") with the template's identity pre-filled (`object_type: Assumption Map`, `status: Draft`, H1 `# Assumption Map`).
- Carries the Handover-2.5-specific frontmatter block (`parent_opportunity`, `parent_intent`, `assumptions:` list-of-maps, `riskiest_assumption`, `human_owned_decisions`) under a `# Handover-specific fields` YAML comment, quoted verbatim from `docs/HANDOVERS.md` §"Handover 2.5".
- Carries the five required body sections verbatim from `docs/HANDOVERS.md` §"Handover 2.5" in the contract-mandated order.
- Passes `python3 tools/lint-frontmatter.py --check-template templates/assumption-map.md` with exit 0 — including the linter's **nested-container-placeholder rule**, which the `assumptions:` list-of-maps will exercise non-trivially (every leaf scalar inside each `assumptions[*]` map must be a valid angle-bracket placeholder or a valid concrete value).
- Is wired into `scripts/tests/test_templates_instantiate.py` (covered automatically by the test's `*.md` glob over `templates/`).
- Is listed in `templates/_meta/README.md`'s index.

The Handover-2.5 contract (ROADMAP D7) is *already shipped* by the parent template-authoring-convention spec. F3.3 was previously blocked on D7; that block is now resolved. This spec consumes the contract; it does not author it.

## Why now

F3.3 sits in the F3 block (ten per-ontology-type templates) and is one of eight fan-out workers running in parallel against the shared authoring convention. The Validation phase is gated by Handover 2.5 — without an Assumption Map artifact, teams jump from "we picked an opportunity" to "we ran an experiment" and produce validation theatre. Shipping the template lowers the cost of producing a correct Assumption Map from "read HANDOVERS.md + reconstruct the shape" to "copy and fill." The downstream consumer is ROADMAP P3.11 `/audit-assumption-coverage` (planned), which will flag chosen opportunities with no assumption map — the audit becomes runnable only once authors have a low-friction way to produce the artifact in the first place.

## Inputs and outputs

**Inputs.** This template reads no inputs at instantiation time — it's a static file a kit user copies. The authoring of the template reads:

- `templates/_meta/template-skeleton.md` — the canonical skeleton to copy.
- `docs/HANDOVERS.md` §"Handover 2.5: Discovery → Assumption Map" — source of truth for required frontmatter and required sections, quoted verbatim.
- `docs/CONVENTIONS.md` §"Universal metadata schema", §"Templates", §"Lifecycle states" — the authoring convention.
- `context/frameworks/ontology.md` — Domain C (Assumption — "Belief not yet proven") and Domain I (Assumption Map — "The Chosen-Opportunity → Validation handover. Five-lens inventory of assumptions with a single named riskiest. Lives at `validation/assumption-maps/<slug>.md`.").

**Outputs.** A single file: `templates/assumption-map.md`. Its frontmatter is the union of two blocks:

1. **Universal-metadata schema block**, ordered exactly as `templates/_meta/template-skeleton.md` orders it. Identity fields pre-filled (`object_type: Assumption Map`, `status: Draft`); every other field a valid angle-bracket placeholder. Inapplicable traceability fields (`parent_learning`, `parent_vision`, `parent_initiative`) are deleted per the skeleton's instruction `"delete fields that don't apply"`.

2. **Handover-specific fields block** — quoted verbatim from `docs/HANDOVERS.md` §"Handover 2.5". The exact YAML body (per HANDOVERS Handover 2.5):

   ```yaml
   object_type: Assumption Map
   parent_opportunity: <OPP-NNN>
   parent_intent: <strategic intent slug>     # restated for traceability
   assumptions:
     - id: <ASM-NNN>
       statement: <one sentence>
       lens: desirability | viability | feasibility | usability | ethical
       risk_if_wrong: Low | Medium | High | Critical
       evidence_today: Strong | Moderate | Weak | None
       test_priority: 1 | 2 | 3 | …          # 1 = test first
   riskiest_assumption: <ASM-NNN>             # the one Validation will test next
   human_owned_decisions:
     - Selection of the riskiest assumption to test next
     - Acceptance of assumptions marked "accept-as-bet"
   ```

   In the template file the `assumptions[*]` leaf scalars are rewritten as angle-bracket placeholders so the file passes `--check-template`. `object_type` and `parent_opportunity` are already covered (universal block pre-fills the former; the latter is a normal placeholder). The `assumptions:` enum-choice fields (`lens`, `risk_if_wrong`, `evidence_today`, `test_priority`) are wrapped in angle brackets per the kit's "no bare `|` enum lists in placeholder positions" convention (mirroring how the skeleton wraps `priority: <Low | Medium | High | Critical>`). The `human_owned_decisions` items are kept as the Handover-2.5 contract's literal text — they are concrete, contract-mandated values, not placeholders.

The body of the template carries the five required sections (per Handover-2.5) verbatim as H2 headings, in this order:

1. `## The chosen opportunity`
2. `## Assumptions, by lens`
3. `## Risk-vs-evidence ranking`
4. `## The riskiest assumption`
5. `## Accepted bets`

Each section's body is a one-paragraph placeholder citing what the section must contain per HANDOVERS-2.5. Section 2 cites `context/frameworks/assumption-tests.md` *(planned — ROADMAP F4.4)* for the five-lens definitions, and falls back to ontology Domain C entries until F4.4 ships — verbatim from the Handover-2.5 contract.

The template ends with the standard `## Optional sections` heading containing a one-line "delete if none apply" instruction.

A reader of this section should be able to write the template file with the plan as a companion.

## Boundaries

### Always do

- Copy `templates/_meta/template-skeleton.md` as the starting point. Match its frontmatter field order exactly.
- When HANDOVERS-2.5 fields overlap with the universal-metadata schema (`object_type`, `parent_opportunity`, `parent_intent`, `human_owned_decisions`), the field appears once — in its universal-schema position — carrying the HANDOVERS-2.5-mandated value. The universal-schema placeholder is deleted in the same edit. The handover-specific block carries only fields not present in the universal schema (`assumptions`, `riskiest_assumption`).
- Quote `docs/HANDOVERS.md` §"Handover 2.5" frontmatter and section names *verbatim* in the template. The template re-projects the handover contract; it is not a parallel source of truth.
- Pre-fill `object_type: Assumption Map`, `status: Draft`, and the H1 (`# Assumption Map`) — these are the template's identity per CONVENTIONS §"Pre-fill vs placeholder".
- Use angle-bracket placeholders exclusively (`<one sentence>`, `<OPP-NNN>`, `<YYYY-MM-DD>`). No `{{...}}`, no `__FILL__`.
- For every nested leaf in the `assumptions:` list-of-maps, ensure the value is either an angle-bracket placeholder or a contract-mandated concrete literal. The linter's nested-container-placeholder rule recurses into the list-of-maps and rejects any malformed leaf — this is the load-bearing shape check for F3.3.
- Delete the universal block's `parent_learning`, `parent_vision`, `parent_initiative` fields (they do not apply to the Assumption Map handover, which is upstream of Learning/Vision/Initiative). The skeleton's traceability-block comment explicitly authorizes this (`"delete fields that don't apply"`).
- Append an entry to `templates/_meta/README.md`'s index list in the CAPTURE phase. Sequential merge per the parent spec's "Sequential README.md appends" rollout note.
- Check off ROADMAP F3.3 in the CAPTURE phase.

### Ask first

- Adding any frontmatter field not present in either `docs/CONVENTIONS.md` §"Universal metadata schema" *or* `docs/HANDOVERS.md` §"Handover 2.5". The template re-projects those two sources; it does not extend them.
- Reordering frontmatter fields away from the skeleton's order. The convention's "Frontmatter ordering" clause is load-bearing for cross-template diff readability.
- Deleting or renaming any of the five required sections from Handover 2.5. Required sections "appear in the template body verbatim" per CONVENTIONS §"Templates → Required vs optional sections".

### Never do

- Author definitions for the five lenses (desirability / viability / feasibility / usability / ethical) inside this template. Those definitions live in `context/frameworks/assumption-tests.md` *(planned — ROADMAP F4.4, currently absent)*. Per the Handover-2.5 contract, until F4.4 ships, cite ontology Domain C entries for the named lenses. This template's §"Assumptions, by lens" section quotes the Handover-2.5 instruction text and stops there.
- Add the `assumptions:` element keys (`id`, `statement`, `lens`, `risk_if_wrong`, `evidence_today`, `test_priority`) to `docs/CONVENTIONS.md`'s universal-metadata schema or to the canonical key set in `scripts/tests/test_templates_instantiate.py::test_skeleton_field_names_are_known`. They are *handover-specific*, not universal; that test asserts about the skeleton, not about per-template handover blocks.
- Amend `docs/HANDOVERS.md` §"Handover 2.5". The contract is owned by the parent template-authoring-convention spec (shipped 2026-05-22). If a divergence surfaces here, surface it as an open question; do not silently edit HANDOVERS.
- Add an ad-hoc ontology type for the template itself. Domain I's "Assumption Map" composite is the type; F3.3 instantiates it. (Mirrors the parent spec's "Never do → no `kit-template` type.")
- Edit `tools/lint-frontmatter.py`. The `--check-template` mode is fully built by the parent spec. If F3.3 needs a linter change, that's a spec-bug in the parent, not in F3.3.
- Walk `templates/` from the linter's default mode. Out of scope (same reason as parent spec).

## Verification mode

- **Goal-based check** for the template's *shape*. The one-liner `python3 tools/lint-frontmatter.py --check-template templates/assumption-map.md` exits 0. The linter mechanically asserts every frontmatter constraint the convention specifies: required keys present, placeholder shape valid, nested-container leaves valid, enum violations rejected.
- **Audit-driven** for kit-wide health. `bash tools/pre-pr.sh` exits 0. `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (the test auto-discovers `templates/assumption-map.md` via its `*.md` glob; no test code change needed in F3.3).

No TDD: no script logic is being built here. No manual gesture: behavior is fully mechanically checkable.

## Contract tests

Each test is one shell line or one pytest case. They are the gate.

- `T1` — `test -f templates/assumption-map.md` exits 0.
- `T2` — `python3 tools/lint-frontmatter.py --check-template templates/assumption-map.md` exits 0. **This is the load-bearing test.** It exercises the nested-container-placeholder rule on the `assumptions:` list-of-maps; if any nested leaf is malformed (e.g., a bare `< >`, an unquoted enum-violating literal, or a missing key), the linter rejects.
- `T3` — Required-frontmatter keys present. Implemented as a one-line python check that loads the template's frontmatter and asserts every key in the canonical Handover-2.5 set is present:

  ```sh
  python3 -c "import sys; sys.path.insert(0, '.'); from scripts.lib.frontmatter import parse_file; fm=parse_file('templates/assumption-map.md'); req={'object_type','parent_opportunity','parent_intent','assumptions','riskiest_assumption','human_owned_decisions'}; missing=req - set(fm.data.keys()); assert not missing, f'missing: {missing}'"
  ```

- `T3b` — Nested-element keys present in every `assumptions[*]` map. Asserts each element of `assumptions:` carries the six Handover-2.5-required keys (`id`, `statement`, `lens`, `risk_if_wrong`, `evidence_today`, `test_priority`). One-liner:

  ```sh
  python3 -c "import sys; sys.path.insert(0, '.'); from scripts.lib.frontmatter import parse_file; fm=parse_file('templates/assumption-map.md'); req={'id','statement','lens','risk_if_wrong','evidence_today','test_priority'}; bad=[i for i,a in enumerate(fm.data.get('assumptions') or []) if req - set((a or {}).keys())]; assert not bad, f'incomplete assumptions[]: {bad}'"
  ```

- `T3c` — Block placement: dedup-overlapping keys (`parent_opportunity`, `parent_intent`, `human_owned_decisions`) are NOT present in the YAML text after the `# Handover-specific fields` comment line. Last-write-wins YAML means a duplicate in the handover-specific block silently overrides the universal value; this test rejects that. One-liner:

  ```sh
  python3 -c "body=open('templates/assumption-map.md').read(); hs=body.split('# Handover-specific fields',1)[1].split('---',1)[0]; assert 'parent_opportunity:' not in hs and 'parent_intent:' not in hs and 'human_owned_decisions:' not in hs, 'dedup violated'"
  ```

- `T4` — Five required H2 section headings present in contract-mandated order. One-liner:

  ```sh
  awk '/^## /' templates/assumption-map.md | head -5 | diff - <(printf '## The chosen opportunity\n## Assumptions, by lens\n## Risk-vs-evidence ranking\n## The riskiest assumption\n## Accepted bets\n')
  ```

- `T4b` — H1 blockquote stub line present exactly once: `grep -c 'Assumption Map for the chosen Opportunity' templates/assumption-map.md` returns exactly 1.

- `T5` — Angle-bracket-only placeholder discipline. `grep -nE '\{\{|__FILL__' templates/assumption-map.md` returns no matches (exits non-zero).
- `T6` — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0. (The test auto-discovers `templates/assumption-map.md`; this asserts the new file is picked up and passes both `test_template_passes_check_template_mode` and `test_target_count_nonzero`.)
- `T7` — `bash tools/pre-pr.sh` exits 0. (Kit-wide health.)
- `T8` — ROADMAP F3.3 checkbox is marked: `grep -c '^- \[x\] \*\*F3\.3\*\*' ROADMAP.md` returns exactly 1.
- `T9` — `templates/_meta/README.md` lists the template: `grep -c 'assumption-map\.md' templates/_meta/README.md` returns ≥ 1.

## Non-goals

- **Authoring `context/frameworks/assumption-tests.md`** — that's ROADMAP F4.4. This template *cites* the framework as planned and falls back to ontology Domain C per the Handover-2.5 contract; it does not embed lens definitions.
- **Building `/audit-assumption-coverage`** — ROADMAP P3.11. This template is an *input* to that audit; the audit itself is out of scope.
- **Amending `docs/HANDOVERS.md` §"Handover 2.5"** — already shipped by the parent template-authoring-convention spec. If a missing field or ambiguity surfaces, raise it as an open question on this spec; do not edit HANDOVERS in this loop.
- **Authoring a `/draft-assumption-map` command** — future ROADMAP item; not in F3.
- **Changing the universal metadata schema in `docs/CONVENTIONS.md`** — out of scope; the schema is owned upstream.
- **Adding a per-element schema for `assumptions[*]` to `tools/lint-frontmatter.py`** — the existing `--check-template` mode handles nested-container leaves recursively. Per-element typed validation (e.g., asserting `lens` is one of the five canonical strings on concrete instantiations) is a future enforcement enhancement, not an F3 deliverable. Tracked under "Open questions" below.

## Open questions

1. **Per-element enum validation for `assumptions[*]` concrete values.** When a kit user fills `templates/assumption-map.md` and produces a real artifact, the `lens` field should be one of `desirability | viability | feasibility | usability | ethical` (and similarly for `risk_if_wrong`, `evidence_today`). The current `--check-template` mode validates against the universal-schema enums in `TEMPLATE_FIELD_ENUMS` only; the handover-specific enums on `assumptions[*]` leaves are not yet wired in. _Who can answer:_ the F1 enforcement track (linter ownership) or a follow-up F3-G spec. _When:_ after F3.3 ships; raise via a ROADMAP F3-G entry if it bites. Not blocking for F3.3 — the load-bearing safety property (no broken placeholder shapes, no missing required keys) is already enforced.
2. **Sequential-merge protocol for `templates/_meta/README.md`.** Eight F3 fan-out workers append entries concurrently; the parent spec's rollout note acknowledges this and accepts trivially-mergeable append-only conflicts. F3.3's CAPTURE step must therefore write its index entry *after* its parent fan-out merge; otherwise the entry races with sibling workers' entries. _Who can answer:_ the F3 fan-out orchestrator. _When:_ at aggregate-and-commit stage (parent task list item #9). Not blocking for plan approval.

### Resolved

- **OQ-A:** Render `test_priority` placeholder as `<1 | 2 | 3 | ...>` (ASCII ellipsis) rather than HANDOVERS-2.5's `1 | 2 | 3 | …` (Unicode). _Resolved: ASCII chosen to avoid downstream encoding drift; both forms regex-valid under `--check-template`._

### Open assumptions

- Orchestrator merge protocol for concurrent `templates/_meta/README.md` appends exists and handles append-only YAML conflicts — not verified as of 2026-05-22; per parent template-authoring-convention plan §Rollout, each F3.x worker writes its README.md update in a tiny dedicated commit at the end of its own loop and merge conflicts are trivially append-only mergeable.

## Acceptance criteria

- [ ] `templates/assumption-map.md` exists with `object_type: Assumption Map`, `status: Draft` pre-filled in the universal block and H1 `# Assumption Map`.
- [ ] Universal-schema frontmatter block ordered exactly as `templates/_meta/template-skeleton.md` orders it; inapplicable traceability fields (`parent_learning`, `parent_vision`, `parent_initiative`) deleted.
- [ ] Frontmatter (parsed YAML, across both universal and handover-specific blocks) carries all six top-level keys from HANDOVERS-2.5 (`object_type`, `parent_opportunity`, `parent_intent`, `assumptions`, `riskiest_assumption`, `human_owned_decisions`). Of these, `object_type`, `parent_opportunity`, `parent_intent`, and `human_owned_decisions` live in the universal block (with HANDOVERS-2.5-mandated values); `assumptions` and `riskiest_assumption` live in the handover-specific block under the `# Handover-specific fields` YAML comment.
- [ ] Every `assumptions[*]` map carries all six Handover-2.5 keys (`id`, `statement`, `lens`, `risk_if_wrong`, `evidence_today`, `test_priority`); every leaf scalar is either an angle-bracket placeholder or a contract-mandated concrete literal.
- [ ] The five required body sections appear as H2 headings in the contract-mandated order: chosen opportunity / assumptions by lens / risk-vs-evidence ranking / riskiest assumption / accepted bets.
- [ ] T1, T2, T3, T3b, T3c, T4, T4b, T5, T6, T7, T8, T9 all pass.
- [ ] `templates/_meta/README.md` lists `assumption-map.md` in its index.
- [ ] ROADMAP F3.3 row is checked off.
- [ ] No `context/frameworks/assumption-tests.md` authored; no `/audit-assumption-coverage` built; no edits to `docs/HANDOVERS.md`.

## Cross-references

- **Consumed by:** future `/draft-assumption-map` command (planned — not in F3); ROADMAP P3.11 `/audit-assumption-coverage` (planned) which will detect missing/incomplete assumption maps in the wild; kit users producing `validation/assumption-maps/<slug>.md` artifacts.
- **Consumes:** `docs/HANDOVERS.md` §"Handover 2.5" (verbatim quote source for both frontmatter and required sections); `docs/CONVENTIONS.md` §"Templates", §"Universal metadata schema", §"Lifecycle states"; `templates/_meta/template-skeleton.md` (literal starting point); `context/frameworks/ontology.md` Domain C and Domain I (cited for lens definitions until F4.4 ships).
- **Frontmatter fields owned in the handover-specific block:** `assumptions` (with nested keys `id` / `statement` / `lens` / `risk_if_wrong` / `evidence_today` / `test_priority`) and `riskiest_assumption`. `parent_opportunity`, `parent_intent`, and `human_owned_decisions` are universal-schema fields whose values are overridden to HANDOVERS-2.5-mandated text.
- **Ontology object types touched:** Assumption Map (Domain I composite — the type this template instantiates); Assumption (Domain C atomic — the element type populating `assumptions[*]`); Opportunity (Domain C — referenced by `parent_opportunity`).
