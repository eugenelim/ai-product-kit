# Spec: template-authoring-convention

- **Status:** Shipped (2026-05-22)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template + docs reconciliation + contract test
- **Serves kit phase:** Meta (kit infrastructure — the contract for all `templates/<slug>.md` files)
- **Constrained by:** ROADMAP F3.1–F3.10 (the ten templates that consume this convention); ROADMAP D7 (Assumption Map handover contract, authored inline here); `docs/HANDOVERS.md` (source-of-truth for every template's frontmatter); `docs/CONVENTIONS.md` §"Universal metadata schema" and §"Specs and Plans"; `context/frameworks/ontology.md` (the ontology types each template instantiates).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Defines the authoring convention every F3.x template must follow, ships a literal `templates/_meta/template-skeleton.md` they copy from, ships a contract test (`scripts/tests/test_templates_instantiate.py`) that mechanically validates each template once authored, and authors the missing Handover-2.5 (Assumption Map) contract that F3.3 needs. The whole point is that the ten F3.x workers can run in parallel without converging on inconsistent shape.

## Objective

Four coupled deliverables that, together, make F3.1–F3.10 safely parallelizable:

1. **A short authoring convention** appended to `docs/CONVENTIONS.md` as a new §"Templates — `templates/<slug>.md`" sub-section. Names file location, placeholder syntax, frontmatter ordering, pre-fill rules, required-vs-optional marking, linter contract.
2. **A literal skeleton file** at `templates/_meta/template-skeleton.md` that every F3.x worker copies and fills. One file. ≤ 80 body lines. No domain-specific content — only shape contract.
3. **A `--check-template` mode** on `tools/lint-frontmatter.py` plus a contract test at `scripts/tests/test_templates_instantiate.py`. The mode is identical to default linting but tolerates `<placeholder>` literal values where a concrete value would be required. The test walks `templates/*.md` and `templates/*/README.md` and asserts the mode exits 0 on each. F3.x workers wire their template into this test as their final VERIFY gate.
4. **The Handover-2.5 (Assumption Map) contract** appended to `docs/HANDOVERS.md` as a new top-level section between Handover 2 and Handover 3. Closes ROADMAP D7. Required so F3.3 has a contract to cite.

## Why now

F3.1–F3.10 are the next ten ROADMAP items, sequenced as a Foundation block precisely because they share contract surface. Authoring this convention before fanning out collapses ten "shape" decisions into one and turns ten serialized loops into ten parallel ones. The cost is one short loop. The cost of *not* doing it is ten templates that drift on placeholder syntax, frontmatter ordering, and section-heading style, then a remediation pass that touches all ten.

F3.3 (Assumption Map template) is blocked on D7 (the missing Handover-2.5 contract). Authoring D7 here, in the same loop, removes that blocker.

## Inputs and outputs

**Inputs.**

- `docs/HANDOVERS.md` — the source contract for Handovers 1–7. Every F3.x template's required frontmatter and required sections are quoted directly from here.
- `docs/CONVENTIONS.md` §"Universal metadata schema" — the universal frontmatter superset every template carries.
- `context/frameworks/ontology.md` — the ontology types each template's `object_type:` field will be pre-filled with.
- `tools/lint-frontmatter.py` — current behavior (walks `PHASE_DIRS = ["strategy", "discovery", "validation", "delivery", "market"]`; does NOT walk `templates/`). Source for the `--check-template` mode.
- Existing `templates/CLAUDE.global.md` — confirms `templates/` is a live top-level directory; no scaffolding needed.

**Outputs.**

1. `docs/CONVENTIONS.md` — new §"Templates — `templates/<slug>.md`" sub-section at the end of §"Specs and Plans" (so templates and specs sit adjacent in the conventions doc). Exact text contract in §"Convention-text contract" below.
2. `templates/_meta/template-skeleton.md` — new file. Exact text contract in §"Skeleton-text contract" below.
3. `templates/_meta/README.md` — new file. One-paragraph index that explains what `_meta/` is for, lists all current `templates/*.md`, and points to the convention. **No YAML frontmatter** — this README is prose-only documentation, not a kit artifact. The contract test (item 5 below) skips `templates/_meta/` exactly because of this. F3.x workers append their entries here in their CAPTURE phase; the F3 plan's Stage 2 validates the index matches the directory listing.
4. `tools/lint-frontmatter.py` — add `--check-template <path>` mode. Behavior: same as default, but values matching the **placeholder rule** are accepted as if concrete. The placeholder rule has four shapes, applied recursively to the YAML value tree:

   - **Atomic placeholder.** A scalar matching `^<\S(?:[^>]*\S)?>$` — angle brackets enclosing at least one non-whitespace character. Rejects `<>` and `< >`.
   - **Augmented placeholder.** A scalar matching `^[^<>]*(<\S(?:[^>]*\S)?>[^<>]*)+$` — one or more atomic placeholders interleaved with literal text (no `<` or `>` in the literal part). Accepts forms like `<role>: <YYYY-MM-DD>` (the way `approvals_obtained` items render when the existing `frontmatter.py` falls back to a scalar parse), or `<NNN>-<kebab-case>`.
   - **Block-scalar placeholder.** A `|` or `>` style block scalar whose first non-empty line matches the augmented-placeholder rule.
   - **Nested-container placeholder.** A list or mapping value is accepted iff every **leaf scalar** inside it (recursively into nested lists and maps) is either (a) one of the three placeholder shapes above OR (b) a valid concrete value per the rule for concrete values below. This covers list-of-maps shapes like `evidence_basis: [{source: <…>, strength: <…>, link: <…>}]`.

   **Concrete-value validation under `--check-template`.** A concrete (non-placeholder) value must still satisfy its field's type and enum constraints (e.g., `status:` must be a literal from the lifecycle-states enum; `priority:` must be one of the four enum members). For **untyped list-element fields** like `related_problems` where the existing linter has no per-element schema, a concrete element is invalid only if it is an empty string. Required-key-present checks are unchanged from default mode.
5. `scripts/tests/test_templates_instantiate.py` — new pytest file. Discovery rule: target set = (`templates/*.md`) ∪ (`templates/*/README.md`) ∪ (the explicit path `templates/_meta/template-skeleton.md`). For each target, runs `lint-frontmatter.py --check-template <path>` and asserts exit 0. **Permanent skip list:** `templates/CLAUDE.global.md` (it's the seed CLAUDE.md a kit-user project gets, not a kit-artifact template) and `templates/_meta/README.md` (prose-only, no frontmatter). Skip rationale is documented inline in the test. **Discovered-and-not-skipped count must be ≥1** after Task 2 ships — the explicit `template-skeleton.md` entry guarantees this, so the test is never a silent no-op (asserted as a separate test case `test_target_count_nonzero`).
6. `docs/HANDOVERS.md` — new top-level §"Handover 2.5: Discovery → Assumption Map" inserted between current Handover 2 and Handover 3. Exact text in §"Handover-2.5 text contract" below. Handover 2's detector line ("`/audit-assumption-coverage` flags chosen opportunities with no assumption map") moves into Handover 2.5; Handover 2 keeps `/audit-discovery-coherence` only.
7. `ROADMAP.md` — F3 block prepended with a one-line cross-reference ("F3.x items consume the authoring convention from `docs/specs/template-authoring-convention/`. Read that spec first."). Mark D7 with `Shipped: <date>` once Handover 2.5 lands.

A reader of this section should be able to construct the diff without reading anything else.

## Convention-text contract

The new §"Templates — `templates/<slug>.md`" sub-section in `docs/CONVENTIONS.md` ships with this exact body (reviewed before execution, not authored during it):

> ### Templates — `templates/<slug>.md`
>
> The kit ships per-ontology-type templates under `templates/`. Each template is a literal skeleton a kit user copies and fills to produce a real product artifact under `strategy/`, `discovery/`, `validation/`, `delivery/`, or `market/`. Templates are *not* product artifacts themselves — they live outside `PHASE_DIRS` and are not linted in default mode.
>
> **File layout.**
> - Single-file template: `templates/<slug>.md` (slug matches the ontology-type kebab-case name, e.g., `strategic-intent`, `vision`, `landing-report`).
> - Multi-file template (folders such as Initiative, Handoff Packet): `templates/<slug>/` containing a `README.md` plus the per-child-file templates. The folder's `README.md` carries the universal-schema frontmatter; child files carry their own type-specific frontmatter if and only if they instantiate distinct ontology objects.
>
> **Placeholder syntax.** Use angle-bracket placeholders exactly as in `docs/HANDOVERS.md`: angle brackets wrap a descriptor with no whitespace between bracket and content, e.g. `<one sentence>`, `<YYYY-MM-DD>`, `<OPP-NNN>`. The linter requires at least one non-whitespace character inside the brackets — `<>` and `< >` are rejected. Curly-brace and double-underscore styles are not used.
>
> **Frontmatter ordering.** Universal-metadata schema fields (per §"Universal metadata schema") appear first, in the order shown there. Handover-specific fields (per `docs/HANDOVERS.md`) appear in a second block under a `# Handover-specific fields` YAML comment. This makes diffs across templates trivial to read.
>
> **Pre-fill vs placeholder.** A field whose value is the *template's identity* is pre-filled (e.g., `object_type: Strategic Intent` in `templates/strategic-intent.md` — the type is known, not a user choice). Every other field is a placeholder. The `status:` field is pre-filled to `Draft` — this is the entry state of the **product-artifact lifecycle track** (per CONVENTIONS.md §"Lifecycle states"), which is what the instantiated artifact (not the template file itself) will inherit when a kit user copies the template. The template file as a kit-build component lives on a separate lifecycle track that is managed via its companion spec under `docs/specs/template-<slug>/`, not via the template's YAML body.
>
> **Required vs optional sections.** Required sections (per the relevant `HANDOVERS.md` row) appear in the template body verbatim. Optional sections appear under a single `## Optional sections` heading at the bottom of the template, each with a one-line description of when to use it. Authors of derived artifacts delete unused optional sections; required sections must remain.
>
> **Linter contract.** Templates pass `tools/lint-frontmatter.py --check-template <path>`, which accepts angle-bracket placeholders where concrete values would otherwise be required. Default mode (which walks `PHASE_DIRS`) does not walk `templates/` and is unchanged. The contract test at `scripts/tests/test_templates_instantiate.py` runs `--check-template` against every template in CI.
>
> **Authoring a new template.** Copy `templates/_meta/template-skeleton.md`. Read the relevant `docs/HANDOVERS.md` row for the handover this template gates. Fill the spec under `docs/specs/template-<slug>/` first (the F3 block in `ROADMAP.md` lists ten such specs as worked examples).

## Skeleton-text contract

`templates/_meta/template-skeleton.md` ships with this exact body. Comments preserved (they're the author-guidance the F3.x workers read while filling).

```markdown
<!--
This skeleton produces a single-file template. For folder-based templates
(Initiative, Handoff Packet), the convention is: a `README.md` carries this
frontmatter; child files carry their own frontmatter ONLY when they
instantiate a distinct ontology object (see CONVENTIONS.md §"Templates"
→ "File layout"; F3.7 and F3.9 specs encode the per-child decision).
-->
---
# Universal-metadata schema (per docs/CONVENTIONS.md §"Universal metadata schema").
# Order matches CONVENTIONS.md exactly. Pre-filled fields are the template's identity.
id: <type-prefix>-<NNN>
slug: <kebab-case>
object_type: <pre-filled per template — e.g., Strategic Intent>
name: <human-readable name>
description: <one to three sentences>
owner: <named human or role>
status: Draft   # product-artifact track entry state; see CONVENTIONS.md §"Lifecycle states"
priority: Low | Medium | High | Critical
risk_level: Low | Medium | High | Critical
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>

# Traceability (per HANDOVERS.md row for this handover; delete fields that don't apply)
parent_intent: <strategy intent slug>
parent_opportunity: <discovery opportunity id>
parent_learning: <validation learning slug>
parent_vision: <delivery vision slug>
parent_initiative: <delivery initiative slug>
related_problems: [<id>, ...]
related_personas: [<id>, ...]
related_kpis: [<id>, ...]

# Evidence vs assumption
evidence_basis:
  - source: <interview | ticket | metric | market-signal>
    strength: Strong | Moderate | Weak
    link: <path or url>
open_assumptions: [<text>, ...]

# Human-vs-AI ownership
human_owned_decisions:
  - <decision a human must make personally>
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: true | restricted | not-allowed
human_approval_required: true | false
approvals_obtained:
  - <role>: <YYYY-MM-DD>

# Open items
open_questions: [<text>, ...]
risks: [<id>, ...]
# Handover-specific fields (per docs/HANDOVERS.md row for this handover)
# Add fields from HANDOVERS.md that are required for this artifact type.
# Example for Strategic Intent: central_challenge, guiding_policy, coherent_actions, horizon.
---

# <Artifact name>

> One-paragraph description of what this artifact is and what handover it gates. Cite the HANDOVERS.md section.

## <Required section 1 from HANDOVERS.md>

<Placeholder body. One paragraph or list. The required sections are quoted verbatim from HANDOVERS.md for this handover.>

## <Required section 2 from HANDOVERS.md>

<...>

## <Required section N from HANDOVERS.md>

<...>

## Optional sections

Delete the heading and all unused sections below if none apply.

### <Optional section A>

<When to use this section; what it contains.>
```

## Handover-2.5 text contract

A new top-level §"Handover 2.5: Discovery → Assumption Map" inserted between the existing Handover 2 and Handover 3 sections of `docs/HANDOVERS.md`. Closes D7. Exact body:

> ## Handover 2.5: Discovery → Assumption Map
>
> **Artifact:** `validation/assumption-maps/<slug>.md`
> **Object types:** Assumption (Domain C), Opportunity (Domain C, by reference)
>
> The chosen Opportunity from Handover 2 lists its assumptions; the Assumption Map is where those assumptions get *typed*, *ranked*, and *prioritized for testing*. Without this artifact, Validation jumps straight from "we picked an opportunity" to "we ran an experiment" — skipping the step where the team agrees on *which* assumption is the riskiest. That's the failure that produces validation theatre: testing the easy assumption because the riskiest one is uncomfortable.
>
> **Required frontmatter (additions on top of the universal schema):**
>
> ```yaml
> object_type: Assumption Map
> parent_opportunity: <OPP-NNN>
> parent_intent: <strategic intent slug>     # restated for traceability
> assumptions:
>   - id: <ASM-NNN>
>     statement: <one sentence>
>     lens: desirability | viability | feasibility | usability | ethical
>     risk_if_wrong: Low | Medium | High | Critical
>     evidence_today: Strong | Moderate | Weak | None
>     test_priority: 1 | 2 | 3 | …          # 1 = test first
> riskiest_assumption: <ASM-NNN>             # the one Validation will test next
> human_owned_decisions:
>   - Selection of the riskiest assumption to test next
>   - Acceptance of assumptions marked "accept-as-bet"
> ```
>
> **Required sections:**
>
> 1. **The chosen opportunity** — one-paragraph restatement; link to the OST node.
> 2. **Assumptions, by lens** — every assumption underneath the opportunity, classified into the five-lens taxonomy (desirability / viability / feasibility / usability / ethical). Cite `context/frameworks/assumption-tests.md` *(planned — ROADMAP F4.4)* for definitions; until that framework ships, link to ontology Domain C entries for the named lenses.
> 3. **Risk-vs-evidence ranking** — each assumption plotted on (risk_if_wrong × evidence_today). The riskiest under-evidenced assumption is the next test target.
> 4. **The riskiest assumption** — restated; why it earned the rank; what we'd lose if it's wrong.
> 5. **Accepted bets** — assumptions the team explicitly chooses not to test (with rationale). These propagate to the Vision artifact's `open_assumptions:` block as tier `accept-as-bet`.
>
> **Failure if missing:** Validation theatre. Teams test the cheapest assumption rather than the riskiest, then declare "validated" on a test that wouldn't have changed the decision.
>
> **Detector:** `/audit-assumption-coverage` *(planned — ROADMAP P3.11)* flags chosen opportunities with no assumption map after >7 days. Until shipped, audit manually.

Handover 2's existing detector line — "`/audit-assumption-coverage` flags chosen opportunities with no assumption map" — is removed from Handover 2 (its proper home is Handover 2.5). Handover 2's detector becomes `/audit-discovery-coherence` only.

## Boundaries

### Always do

- Quote `docs/HANDOVERS.md` verbatim for every required-section and required-frontmatter claim in the convention text. The convention is a re-projection of HANDOVERS, not a parallel source of truth.
- Keep `templates/_meta/template-skeleton.md` ≤ 80 body lines. If it grows, the convention has become a parallel source of truth and we have a drift problem.
- Update `docs/HANDOVERS.md` Handover 2's detector line in the same edit that adds Handover 2.5 (relocate, do not duplicate).
- Use angle-bracket placeholder syntax exclusively in the skeleton.

### Ask first

- Adding any new frontmatter field not already in `docs/CONVENTIONS.md` §"Universal metadata schema" or `docs/HANDOVERS.md`. The convention is downstream of those two docs.
- Walking `templates/` from `lint-frontmatter.py`'s default mode. That's an enforcement change, not a convention change; out of scope here.

### Never do

- Add `kit-template` or `Template` as an ontology type. Domain I is phase-boundary handover composites; templates are kit-build scaffolding. Identical reasoning to F0.11 (`template-kit-spec-frontmatter`) — see that spec's "Never do" section.
- Author placeholder content inside the skeleton that pretends to be ontology-domain content. No "example Strategic Intent body" inside the skeleton; the skeleton is shape-only, domain-agnostic.
- Edit any of the existing F3.x ROADMAP rows other than to add the cross-reference pointer named in §"Outputs" item 7. F3.x rows are still owned by their own future specs.

## Verification mode

- **Goal-based check** for the docs edits (greps assert added phrases; CONVENTIONS.md and HANDOVERS.md still parse as valid Markdown).
- **TDD** for the `--check-template` mode and `scripts/tests/test_templates_instantiate.py`: tests come before code. Required fixtures (under `scripts/tests/fixtures/templates/`):
  - `valid-all-placeholders.md` — all placeholders, all required keys present.
  - `missing-object-type.md` — required key missing.
  - `bogus-enum-value.md` — concrete value violating an enum (e.g., `status: ShippedYesterday`).
  - `placeholder-block-scalar.md` — `description: |` block whose first non-empty line is `<one to three sentences>`.
  - `whitespace-only-placeholder.md` — a field value of `< >`; must be rejected.
  - `augmented-placeholder.md` — `approvals_obtained: ["<role>: <YYYY-MM-DD>"]` (the multi-token scalar form `frontmatter.py` falls back to); must be accepted.
  - `nested-container-placeholder.md` — `evidence_basis: [{source: <…>, strength: <…>, link: <…>}]`; must be accepted.
  - `nested-container-invalid.md` — `evidence_basis: [{source: <…>, strength: NotInEnum, link: <…>}]` (one nested leaf is an enum-violating concrete value); must be rejected.
  - `nested-whitespace-placeholder.md` — `evidence_basis: [{source: < >, strength: <…>, link: <…>}]` (one nested leaf is a malformed `< >` placeholder); must be rejected. _Added by adversarial-review iter-2._
  - `mixed-list-placeholders.md` — `related_problems: [<id>, OPP-001]`; must be accepted.
  - `mixed-list-invalid.md` — `related_problems: [<id>, ""]`; must be rejected (empty-string rule for untyped list fields).
- **Audit-driven** for kit-wide health: `tools/pre-pr.sh` exits 0.

## Contract tests

Each test is one shell line or one pytest case. They are the gate.

- `T1` — `grep -c "### Templates — \`templates/<slug>.md\`" docs/CONVENTIONS.md` returns exactly 1.
- `T2` — `grep -c "## Handover 2.5: Discovery → Assumption Map" docs/HANDOVERS.md` returns exactly 1.
- `T3` — `test -f templates/_meta/template-skeleton.md && [[ $(wc -l < templates/_meta/template-skeleton.md) -le 80 ]]` (skeleton stays terse).
- `T4` — `test -f templates/_meta/README.md` (index exists).
- `T5` — `python3 tools/lint-frontmatter.py --check-template templates/_meta/template-skeleton.md` exits 0 (the skeleton itself passes the linter it advertises).
- `T6` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/valid-all-placeholders.md` exits 0.
- `T7` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/missing-object-type.md` exits non-zero.
- `T8` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/bogus-enum-value.md` exits non-zero (enum violations still rejected under `--check-template`).
- `T8b` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/whitespace-only-placeholder.md` exits non-zero (whitespace-only `< >` rejected).
- `T8c` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/mixed-list-placeholders.md` exits 0 (a list mixing one placeholder and one valid concrete value is accepted).
- `T8d` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/mixed-list-invalid.md` exits non-zero (a list whose concrete element is itself invalid — here an empty string — is rejected; placeholder mode doesn't suppress concrete-value validation).
- `T8e` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/augmented-placeholder.md` exits 0 (the augmented form `<role>: <YYYY-MM-DD>` matches the placeholder rule).
- `T8f` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/nested-container-placeholder.md` exits 0 (list-of-maps with all leaf-scalar placeholders is accepted).
- `T8g` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/nested-container-invalid.md` exits non-zero (one nested leaf scalar is an enum-violating concrete value).
- `T8h` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/nested-whitespace-placeholder.md` exits non-zero (malformed `< >` placeholder *inside* a nested `evidence_basis` dict — confirms the placeholder rule propagates recursively, not only on top-level scalars). _Added by adversarial-review iter-2 to close the recursive-dict coverage gap that T8b alone did not exercise._
- `T9` — `python3 tools/lint-frontmatter.py --check-template scripts/tests/fixtures/templates/placeholder-block-scalar.md` exits 0 (multi-line placeholder accepted).
- `T10` — `python3 tools/lint-frontmatter.py scripts/tests/fixtures/templates/valid-all-placeholders.md` exits non-zero (placeholders rejected in default mode — mode separation confirmed).
- `T11` — `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0; the test walks `templates/*.md` (excluding `CLAUDE.global.md`) and `templates/*/README.md`.
- `T12` — `python3 tools/lint-frontmatter.py --all` exits 0 (no regression on default-mode behavior across the existing kit).
- `T13` — `bash tools/pre-pr.sh` exits 0.
- `T14a` — Total `audit-assumption-coverage` mentions in HANDOVERS.md: `grep -c "audit-assumption-coverage" docs/HANDOVERS.md` returns exactly 1 (the detector exists, not duplicated).
- `T14b` — The one mention sits inside Handover 2.5, not Handover 2: `awk '/^## Handover 2\.5/,/^## Handover 3/' docs/HANDOVERS.md | grep -c "audit-assumption-coverage"` returns exactly 1. The tightened awk range starts at `## Handover 2.5` specifically (not `## Handover 2`), so a stray copy left behind in Handover 2's body would fail this test.
- `T14c` — Handover heading count is exactly 8 (1, 2, 2.5, 3, 4, 5, 6, 7): `[[ $(grep -cE "^## Handover [0-9](\.[0-9])?:" docs/HANDOVERS.md) -eq 8 ]]` exits 0.
- `T14d` — Handover 2.5 appears between Handover 2 and Handover 3: `awk '/^## Handover 2:/{seen2=1} /^## Handover 2\.5:/{if(seen2)seen25=1; else exit 1} /^## Handover 3:/{if(seen25)exit 0; else exit 1}' docs/HANDOVERS.md` exits 0.
- `T15` — `grep -nE "^(\|\s*)?[Kk]it.[Tt]emplate" context/frameworks/ontology.md` returns 0 (no ad-hoc ontology type added).
- `T16` — Skeleton placeholder-syntax purity: `python3 -c "body=open('templates/_meta/template-skeleton.md').read(); body_only=body.split('---',2)[2] if body.count('---')>=2 else body; assert '{{' not in body_only and '__FILL__' not in body_only, 'non-angle-bracket placeholders found'"` exits 0.

## Non-goals

- Authoring any of the ten F3.x templates themselves. Those are separate specs that run in parallel after this one ships.
- Walking `templates/` from `lint-frontmatter.py`'s default mode. Out of scope; a future enforcement spec if anyone wants it.
- Changing the universal-metadata schema in `docs/CONVENTIONS.md` or the existing Handover 1–7 contracts in `docs/HANDOVERS.md`. We *add* Handover 2.5 and *add* a Templates sub-section; we don't rewrite anything pre-existing other than relocating one detector line.
- Adding `tools/new-template.sh` (a template scaffolder analogous to `new-spec.sh`). Convenience tooling; deferable. Surfaced as Open Question 3.
- Reconciling D18 (the six catalogued-but-unscheduled frameworks). Separate concern.

## Open questions

1. **Multi-line placeholder values** (`description: |` block whose body is `<one to three sentences>`) — should `--check-template` accept these? _Resolved here: yes. A literal-block scalar whose first non-empty line matches `^<[^>]+>$` is accepted. Encoded in fixture `placeholder-block-scalar.md` and test T9._
2. **Where do F3.8 (PM Spec) instantiated artifacts live** — `delivery/specs/<slug>/` or `delivery/initiatives/<slug>/specs/<slug>/`? HANDOVERS Handover 5 implies the latter. _Resolved here: PM specs live inside their parent initiative folder (`delivery/initiatives/<initiative-slug>/specs/<spec-slug>/`). F3.8's spec will cite this resolution; if the F3.8 worker disagrees, that surfaces as a finding from its own adversarial review and we reconcile then._
3. **Should we ship `tools/new-template.sh` alongside the skeleton?** _Resolved here: no, defer. Ten F3.x workers each copy the skeleton manually; convenience tooling is justified only when adopters start authoring templates outside the F3 block. Track as a separate ROADMAP candidate._
4. **F3.7 and F3.9 child-file frontmatter** — does every child file in a folder template carry frontmatter, or only the `README.md`? _Resolved here: per-child frontmatter when the child instantiates a distinct ontology object (e.g., F3.9's `requirements.yaml` carries Requirement-level metadata); no frontmatter when the child is purely narrative (e.g., `current-workflow.md`). F3.7 and F3.9 specs encode the per-child decision in their own contracts._

## Acceptance criteria

- [ ] `docs/CONVENTIONS.md` gains the §"Templates — `templates/<slug>.md`" sub-section with the exact body in §"Convention-text contract."
- [ ] `templates/_meta/template-skeleton.md` exists, matches the §"Skeleton-text contract" body, and is ≤ 80 body lines.
- [ ] `templates/_meta/README.md` exists and points to the skeleton and the convention.
- [ ] `tools/lint-frontmatter.py` accepts a `--check-template <path>` flag and behaves per §"Outputs" item 4.
- [ ] `scripts/tests/test_templates_instantiate.py` exists, walks `templates/*.md` (skipping `CLAUDE.global.md`) and `templates/*/README.md`, and passes.
- [ ] `docs/HANDOVERS.md` gains §"Handover 2.5: Discovery → Assumption Map" with the exact body in §"Handover-2.5 text contract"; Handover 2's detector line is relocated (not duplicated).
- [ ] `ROADMAP.md`: F3 block gains the one-line cross-reference; D7 marked `Shipped: <date>`.
- [ ] All contract tests pass: T1–T13 plus T8b–T8h (placeholder edge cases incl. recursive-dict malformed-placeholder), T14a–T14d (detector relocation + heading count + sequence), T15, T16.
- [ ] No new ontology type added; no `templates/` walk added to default linter mode; no F3.x template authored.

## Cross-references

- **Consumed by:** F3.1–F3.10 (ten template specs that copy `template-skeleton.md` and cite this spec); any future adopter authoring a new template type.
- **Consumes:** `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`.
- **Frontmatter fields owned:** none directly; specifies the *ordering* convention for universal-schema + handover-specific fields inside template files.
- **Ontology object types touched:** Assumption Map (existing Domain I composite per `docs/CONVENTIONS.md`'s Domain I list; this spec authors the handover contract that operationalizes the type).
