# Spec: template-vision

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template
- **Serves kit phase:** Delivery
- **Constrained by:** parent spec `docs/specs/template-authoring-convention/spec.md` (the authoring convention; carries the placeholder, frontmatter-ordering, pre-fill, nested-container-placeholder, and linter contracts); `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative" (the source-of-truth for Vision required frontmatter and required sections); `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" + §"Universal metadata schema" + §"Lifecycle states"; `context/frameworks/ontology.md` Domain D (Value Proposition, Differentiator, Product Objective) + Domain G (Risk) + Domain C (Open Assumption) — atomics composed by the Vision Domain I composite (`context/frameworks/ontology.md` line 165); `ROADMAP.md` F3.6.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Defines the literal `templates/vision.md` file that a kit user copies to start a `delivery/visions/<slug>.md` Vision artifact. The Vision is the Validation → Delivery handover composite (Domain I) that gates Handover 4: Vision → Initiative. The template encodes the Handover 4 contract — required frontmatter (including the three nested-container fields `predicted_outcomes:`, `open_assumptions:`, `counter_metrics:`) and six required sections — verbatim, so a kit user filling the template cannot accidentally drift from the contract. Verification by the parent spec's `--check-template` linter and the existing `scripts/tests/test_templates_instantiate.py` (the template wires itself into the test's discovery set by virtue of landing at `templates/vision.md`, which the test's `templates/*.md` glob already covers).

## Objective

Ship `templates/vision.md` — a single-file template, ≤ 80 body lines, that pre-fills the Vision artifact's identity fields (`object_type: Vision`, `status: Draft`, H1 heading `# Vision`) and placeholders everything else per the parent template-authoring convention. The template encodes the Handover 4 required frontmatter (including three nested list-of-maps blocks with leaf-scalar placeholders, one of which carries a three-value enum that must be representable inside `--check-template` mode) and the six Handover 4 required sections in their HANDOVERS.md order. After this template ships, ROADMAP P4.1 `/draft-vision` has a concrete artifact shape to populate; the Vision artifact stops being a contract-on-paper and becomes a contract-in-a-file.

The component does not yet exist. `templates/vision.md` is absent today; the parent spec `template-authoring-convention` has already shipped the skeleton at `templates/_meta/template-skeleton.md` and the `--check-template` linter mode this template is built against.

## Why now

ROADMAP P4.1 `/draft-vision` has `Depends on: F3.6` — until this template lands, P4.1 cannot be authored without inventing a Vision shape that may or may not match HANDOVERS Handover 4. Authoring the template first means P4.1's draft logic is constrained to fill an existing shape, not to invent one. F3.7 `template-initiative` (a sibling F3 worker) is downstream too: its instantiated Initiative artifacts carry a `parent_vision:` traceability field that points at an instantiated Vision shaped by *this* template. F3.6 is part of the F3.1–F3.10 parallel-fan-out block per the parent spec's rationale; this is the slot for it.

## Inputs and outputs

**Inputs.**

- `templates/_meta/template-skeleton.md` — the literal file to copy as the starting point. Pre-fill rules per the parent spec's §"Convention-text contract" → "Pre-fill vs placeholder".
- `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative" — the source-of-truth for the required frontmatter block and the six required sections. The template's required-section headings and the handover-specific frontmatter block are quoted from here verbatim.
- `docs/CONVENTIONS.md` §"Universal metadata schema" — the universal-schema field list and order that appears first in the template's frontmatter (the skeleton already encodes this).
- `context/frameworks/ontology.md` Domain D (Value Proposition, Differentiator, Product Objective), Domain G (Risk), Domain C (Open Assumption), and the Vision row (line 165) — the atomics composed by the Vision composite; informational only (the template carries no `object_type:` field per atomic, only the composite type at the top of the frontmatter).
- `tools/lint-frontmatter.py` `--check-template` mode — the validator the template must pass. Already shipped by the parent spec.

**Outputs.**

1. `templates/vision.md` — the new template file. Single file, no folder. Body ≤ 80 lines (skeleton parity; the handover-specific block adds three nested fields, small enough to fit).
2. One-line append to `templates/_meta/README.md`'s index list naming `vision.md` and pointing at this spec. (Per the parent spec's §"Rollout" — sequential README.md appends across the ten F3.x workers.)
3. One-line check on `ROADMAP.md` F3.6 row: `[ ]` → `[x]` with `Shipped: <date>` per the F3 plan's CAPTURE phase.

**Pre-filled fields** (the template's identity, not user choices):
- `object_type: Vision`
- `status: Draft` (entry state of the product-artifact lifecycle track; the *instantiated* Vision artifact starts here when a kit user copies the template — not the template file itself, whose kit-build-component lifecycle is managed in this spec)
- H1 heading: `# Vision`

**Quoted-verbatim Handover 4 required frontmatter** (copied verbatim from `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative"; values re-encoded as angle-bracket placeholders per the parent spec's pre-fill rule). Overlapping universal-schema fields (`object_type`, `parent_intent`, `parent_learning`, `human_owned_decisions`, `human_approval_required`, `open_assumptions`) keep their universal-schema position with the HANDOVERS-4 value/shape; the handover-specific block below carries only the non-universal additions:

```yaml
# In the universal-schema block (HANDOVERS-4 values applied in place):
object_type: Vision
parent_intent: <strategic intent slug>
parent_learning: <validation learning slug>
open_assumptions:                              # list-of-maps form OVERRIDES the skeleton's flat-list `[<text>, ...]`
  - assumption: <text>
    tier: <must-test-before-shipping | accept-as-bet | will-monitor-post-ship>
human_owned_decisions:
  - Customer-shaped framing of the value proposition
  - Differentiator selection
  - Predicted outcome thresholds
human_approval_required: <true | false>

# In the handover-specific block (fields not present in the universal schema):
crosses_teams: <true | false>
predicted_outcomes:
  - kpi_id: <KPI-NNN>
    threshold: <value>
    measure_at: <weeks-after-launch>
counter_metrics:
  - kpi_id: <KPI-NNN>
```

The three list-of-maps blocks (`predicted_outcomes:`, `open_assumptions:`, `counter_metrics:`) are nested-container placeholders per the parent spec's §"Outputs" item 4 — every leaf scalar must satisfy one of the three placeholder shapes (atomic / augmented / block) or be a valid concrete value. The `open_assumptions[*].tier` field carries the three-value enum `must-test-before-shipping | accept-as-bet | will-monitor-post-ship`; in the template, this is encoded as the atomic placeholder `<must-test-before-shipping | accept-as-bet | will-monitor-post-ship>` so the linter accepts it under `--check-template` while still signaling the three legal values to the kit user. (Encoding the bare token would put a literal concrete value like `must-test-before-shipping` in place — a misleading single-value pre-fill — instead of communicating the enum's alternatives.)

**Quoted-verbatim Handover 4 required sections** (six, in the order they appear in HANDOVERS.md):

1. **The customer-shaped pitch** — narrative voice, persona-aware, drawing on surviving learning
2. **The change** — what's different for the customer
3. **What we believe and why** — citing learning memos
4. **What we're still betting on** — open assumptions, tiered (must-test, accept-as-bet, monitor)
5. **Counter-metrics** — what we'd watch to know we made it worse
6. **Predicted outcomes** — what success looks like; measurement plan

These six headings appear in the template body verbatim, in this order, between the closing `---` of the frontmatter and the `## Optional sections` heading at the bottom (per the parent spec's §"Convention-text contract" → "Required vs optional sections").

The spec's §"Inputs and outputs" is sufficient to produce the template file without opening HANDOVERS.md, CONVENTIONS.md, or the skeleton.

## Boundaries

### Always do

- Use angle-bracket placeholder syntax exclusively. No `{{...}}`, no `__FILL__`, no bare TODOs. (Parent spec test T16 enforces this kit-wide; this template inherits the rule.)
- Quote the Handover 4 required-frontmatter *field names* (top-level and nested) and the six required-section headings verbatim from `docs/HANDOVERS.md`. The template is a re-projection of HANDOVERS, not a parallel source of truth. (*Values* whose HANDOVERS form is an unwrapped enum like `true | false` or `must-test-before-shipping | accept-as-bet | will-monitor-post-ship` are re-encoded as angle-bracket placeholders for `--check-template` compliance per the pre-fill-vs-placeholder rule; the field name and the legal-value alternatives remain identical.)
- Pre-fill `object_type: Vision` and `status: Draft` (template identity, not user choice).
- Encode the `open_assumptions[*].tier` enum as `<must-test-before-shipping | accept-as-bet | will-monitor-post-ship>` (atomic placeholder wrapping the three-value enum). Same pattern for `crosses_teams: <true | false>` and `human_approval_required: <true | false>` — even though HANDOVERS.md prints them unwrapped, the kit's `--check-template` rule requires a placeholder wrapper for any value that isn't pre-filled to the template's identity. HANDOVERS.md is the contract for the *instantiated* artifact's field values; the template wraps the same enums in placeholders.
- Keep the body ≤ 80 lines (skeleton parity).
- Apply nested-container-placeholder rule recursively: every leaf scalar inside `predicted_outcomes:`, `open_assumptions:`, `counter_metrics:`, `human_owned_decisions:`, `evidence_basis:`, etc., must be a placeholder or a valid concrete value.
- When HANDOVERS-4 fields overlap with the universal-metadata schema (`object_type`, `parent_intent`, `parent_learning`, `human_owned_decisions`, `human_approval_required`, `open_assumptions`), the field appears once — in its universal-schema position — carrying the HANDOVERS-4-mandated value or shape. The universal-schema placeholder is deleted in the same edit. The handover-specific block carries only fields not present in the universal schema (`crosses_teams`, `predicted_outcomes`, `counter_metrics`).
- The `open_assumptions:` field's universal-schema flat-list form (`[<text>, ...]`) is OVERRIDDEN by Handover-4's list-of-maps form (each item `{assumption: <text>, tier: <enum>}`). The Vision template carries only the Handover-4 form, in the universal-schema position (since `open_assumptions` is a universal-schema field). The skeleton's flat-list line is deleted in the same edit.

### Ask first

- Adding any required field beyond what HANDOVERS Handover 4 specifies. The template is a re-projection, not a superset.
- Changing the ordering of the six required sections from the HANDOVERS.md order. The HANDOVERS.md ordering is the contract.
- Adding child files (turning this into a folder template). HANDOVERS Handover 4's artifact is a single file (`delivery/visions/<slug>.md`); this template must mirror that shape.

### Never do

- Invent customer-shaped narrative content as example body. The template body for required sections is `<one-paragraph placeholder>` shape, not seeded prose. Seeded prose would be plagiarized by every kit user.
- Weaken or rename the `open_assumptions[*].tier` three-value enum (`must-test-before-shipping | accept-as-bet | will-monitor-post-ship`). The tiering is what makes Vision honest about what we're still betting on; the Validation → Vision causal chain depends on it (HANDOVERS Handover 2.5's §"Accepted bets" section propagates `accept-as-bet` assumptions into this exact field).
- Add a new ontology type (e.g., `Vision Template`, `Kit Template`). Templates are kit-build scaffolding, not ontology objects. (Identical reasoning to the parent spec's "Never do" line on `kit-template`.)
- Walk `templates/vision.md` from the linter's default mode. `--check-template` is the only mode that touches `templates/`; mode separation is the load-bearing safety property the parent spec establishes.

## Verification mode

- **Goal-based check** — the template's "shape" is the contract. A grep + the linter's `--check-template` exit code together verify the template is correctly shaped.
- **Audit-driven** — kit-wide health: `bash tools/pre-pr.sh` exits 0 after the template ships.

(TDD does not apply here — the parent spec already TDD'd the `--check-template` mode and the contract-test runner. This template consumes those gates rather than re-implementing them.)

## Contract tests

Each test is one shell line or one pytest case. They are the gate.

- `T1` — file exists: `test -f templates/vision.md` exits 0.
- `T1b` — body ≤ 80 lines: `[[ $(awk '/^---$/{f=!f; if(!f)c=0} f{c++} END{print c}' templates/vision.md) -le 80 ]]` exits 0. (Body = content between the two frontmatter `---` fences, exclusive.)
- `T2` — `python3 tools/lint-frontmatter.py --check-template templates/vision.md` exits 0. Exercises the nested-container-placeholder rule against three list-of-maps blocks (`predicted_outcomes:`, `open_assumptions:`, `counter_metrics:`) and confirms the `<must-test-before-shipping | accept-as-bet | will-monitor-post-ship>` enum placeholder passes. T2 is the completeness gate for the full universal-schema block.
- `T3` — Handover-4-specific frontmatter additions present (NOT the universal-schema completeness gate; that is T2). T3 asserts: a YAML parse of the file's frontmatter has the following top-level keys with non-empty values: `object_type`, `parent_learning`, `parent_intent`, `crosses_teams`, `predicted_outcomes`, `open_assumptions`, `counter_metrics`, `human_owned_decisions`, `human_approval_required`. Inside `predicted_outcomes[0]`: keys `kpi_id`, `threshold`, `measure_at`. Inside `open_assumptions[0]`: keys `assumption`, `tier`, where `tier` resolves to the literal placeholder string `<must-test-before-shipping | accept-as-bet | will-monitor-post-ship>` (preserving the enum signal). Inside `counter_metrics[0]`: key `kpi_id`. Pre-filled values: `object_type == "Vision"`, `status == "Draft"`. `human_owned_decisions` values are validated as concrete non-empty strings (not placeholders), per parent spec §"Outputs item 4" untyped-list-element rule. Shell form: a small Python snippet using `yaml.safe_load` against the frontmatter block; failure exits non-zero.
- `T4` — the six required-section headings appear in the body, verbatim from HANDOVERS Handover 4, in order. Verifiable as: `grep -n -E "^## (The customer-shaped pitch|The change|What we believe and why|What we're still betting on|Counter-metrics|Predicted outcomes)$" templates/vision.md` returns exactly six lines, and the line-number sequence is monotonically increasing in the HANDOVERS order. (Section names use ASCII apostrophes and hyphens as in HANDOVERS.md.)
- `T4b` — intro blockquote names Handover 4: `grep -E "^> .*[Hh]andover 4" templates/vision.md` returns at least one line.
- `T5` — angle-bracket only: `python3 -c "body=open('templates/vision.md').read(); body_only=body.split('---',2)[2] if body.count('---')>=2 else body; assert '{{' not in body_only and '__FILL__' not in body_only, 'non-angle-bracket placeholders found'"` exits 0. (Mirrors parent spec T16.)
- `T6` — pytest passes: `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0. The template wires itself into discovery via the test's `templates/*.md` glob; no test code change required.
- `T7` — kit-wide health: `bash tools/pre-pr.sh` exits 0.
- `T8` — ROADMAP F3.6 row marked `[x]` with `Shipped: <date>`: `grep -E "^\- \[x\] \*\*F3\.6\*\*" ROADMAP.md` returns one line.
- `T9` — `templates/_meta/README.md` lists `vision.md` in its index: `grep -E "\bvision\.md\b" templates/_meta/README.md` returns at least one line.

## Non-goals

- Building `/draft-vision` (ROADMAP P4.1). Separate spec with its own loop; P4.1 *consumes* this template but doesn't ship with it.
- Authoring an instantiated Vision artifact under `delivery/visions/<slug>.md`. This spec ships the template only; a real Vision is produced by `/draft-vision` (when shipped) or by a human copying the template manually.
- Authoring the Initiative template (`templates/initiative/`, F3.7). F3.7 carries a `parent_vision:` field pointing at instantiated Visions; F3.7 is a sibling F3 worker running in parallel.
- Changing the HANDOVERS Handover 4 contract. If the contract is wrong, surface it via the work-loop's "spec is wrong" path; do not fix it inside this spec's edit.
- Adding tier-enum validation logic to the linter. The linter's `--check-template` mode accepts the placeholder string `<must-test-before-shipping | accept-as-bet | will-monitor-post-ship>` as an atomic placeholder; per-enum-value validation is the job of the instantiated artifact's default-mode lint, not the template.
- Adding commentary explaining "why" each Handover 4 section matters. The kit user reads HANDOVERS.md for the why; the template carries shape only.

## Open questions

1. **Should the template body include a `parent_vision:` field for future Initiative-template traceability?** No — `parent_vision:` lives on the *Initiative* artifact (HANDOVERS Handover 5), not on the Vision itself. Already resolved: the Vision template carries only the fields HANDOVERS Handover 4 names. Surface to the F3.7 worker; not relevant here.
2. **HANDOVERS Handover 4 prints `crosses_teams: true | false` and `human_approval_required: true` unwrapped — should the template encode these as `<true | false>` placeholders or as a literal token?** Resolved per §"Boundaries → Always do": wrap as `<true | false>`. The instantiated artifact's value is a kit-user choice (the team that copies the template doesn't yet know whether the initiative will cross teams); the template can't pre-fill it. HANDOVERS prints `human_approval_required: true` (no choice for the value) — for the template we still wrap as `<true | false>` so `--check-template` accepts it without confusing a kit user; the *instantiated* artifact's default-mode lint then enforces the Handover 4 value. If a future reviewer disagrees, surface as a finding from this spec's adversarial review.
3. **Should the `## Optional sections` heading remain in the template even when Handover 4 names no optional sections?** Yes, per the parent spec's §"Convention-text contract" → "Required vs optional sections": the heading always appears with the standard "Delete the heading and all unused sections below if none apply" prose. The Handover 4 contract names no optional sections, so the template ships with an empty `## Optional sections` block (heading + delete-line), which a kit user removes when they fill the template. (Open to revision if the parent spec's convention is amended.)

## Acceptance criteria

- [ ] `templates/vision.md` exists, single file (T1).
- [ ] Body ≤ 80 lines (T1b).
- [ ] `python3 tools/lint-frontmatter.py --check-template templates/vision.md` exits 0 (T2). Confirms all three nested-container fields pass the nested-leaf placeholder rule and the tier-enum placeholder is accepted.
- [ ] Required frontmatter keys present including nested keys, with the documented pre-filled values (T3): `object_type: Vision`, `status: Draft`, the eight other Handover 4 top-level fields, and the four nested-list-of-maps inner keys (`kpi_id`/`threshold`/`measure_at`; `assumption`/`tier`; `kpi_id`).
- [ ] Six required-section headings appear in HANDOVERS Handover 4's order (T4).
- [ ] Intro blockquote names Handover 4 (T4b).
- [ ] Angle-bracket placeholder syntax only (T5).
- [ ] `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (T6); template auto-discovered.
- [ ] `bash tools/pre-pr.sh` exits 0 (T7).
- [ ] ROADMAP F3.6 row checked with `Shipped: <date>` (T8).
- [ ] `templates/_meta/README.md` lists `vision.md` (T9).
- [ ] No new ontology type added; no `templates/` walk added to default linter mode; no Handover 4 contract change.

## Cross-references

- **Consumed by:** ROADMAP P4.1 `/draft-vision` (depends on F3.6); ROADMAP F3.7 `template-initiative` (its instantiated Initiative artifacts carry `parent_vision:` pointing at an instantiated Vision shaped by this template); ROADMAP P4.2 `/vision-shape-check` (reads the instantiated Vision's `crosses_teams:` value to decide initiative-vs-spec).
- **Consumes:** `templates/_meta/template-skeleton.md` (copy source); `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative" (required-frontmatter + required-sections source); `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" + §"Universal metadata schema" + §"Lifecycle states"; `context/frameworks/ontology.md` Domain D + Domain G + Domain C atomics + Domain I Vision row (line 165); `tools/lint-frontmatter.py` (`--check-template` mode); `scripts/tests/test_templates_instantiate.py` (discovery via `templates/*.md` glob).
- **Frontmatter fields owned:** the Handover 4 fields (`parent_learning`, `parent_intent`, `crosses_teams`, `predicted_outcomes`, `open_assumptions`, `counter_metrics`) plus the universal schema fields pre-filled to Vision identity (`object_type: Vision`, `status: Draft`).
- **Ontology object types touched:** Vision (Domain I composite, the template's `object_type:`); Value Proposition, Differentiator, Product Objective (Domain D atomics composed by Vision — content surfaces in the required sections); Risk (Domain G — surfaces in universal `risks:` field); Open Assumption (Domain C — surfaces in `open_assumptions:` Handover 4 block).
