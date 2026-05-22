# Spec: template-strategic-intent

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** template
- **Serves kit phase:** Strategy
- **Constrained by:** [`docs/specs/template-authoring-convention/spec.md`](../template-authoring-convention/spec.md) (parent contract — placeholder syntax, frontmatter ordering, pre-fill rules, linter contract, skeleton-as-copy-source); `docs/HANDOVERS.md` §"Handover 1: Strategy → Discovery" (source-of-truth for required frontmatter and required sections, quoted verbatim below); `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" and §"Universal metadata schema" (frontmatter superset and ordering); `context/frameworks/ontology.md` Domain A (Strategy) row "Strategic Intent" (the kit-composite type this template instantiates); ROADMAP F3.1.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `templates/strategic-intent.md`, the literal skeleton a kit user copies to produce a Strategic Intent — the Strategy → Discovery handover artifact (per `docs/HANDOVERS.md` §"Handover 1"). The template encodes the universal-metadata-schema frontmatter, the Handover-1-specific frontmatter additions, and the five required sections, with angle-bracket placeholders everywhere a kit user must fill. Copying it and replacing the placeholders produces a valid `strategy/intents/<slug>.md` that gates entry to Discovery.

## Objective

`templates/strategic-intent.md` is the single-file skeleton for the Strategic Intent artifact — the Strategy → Discovery handover (per HANDOVERS Handover 1). Today, an author wanting to draft a Strategic Intent has no copyable starting point: they would have to read HANDOVERS.md, the universal-metadata schema, the ontology row for Strategic Intent, and `templates/_meta/template-skeleton.md`, and stitch them together themselves. This template collapses that into one `cp` command. The template's shape is the contract: its frontmatter ordering is the universal-schema superset prescribed in CONVENTIONS.md plus the Handover-1 additions in a second block under the `# Handover-specific fields` YAML comment; its body's required H2 headings are the five required-sections list from HANDOVERS Handover 1, quoted verbatim; its placeholder syntax is angle-bracket-only per the parent convention. Pre-filled fields are the template's identity only: `object_type: Strategic Intent` and `status: Draft`. Everything else is a placeholder. No stub of this file exists in the repo today; the closest prior context is `templates/_meta/template-skeleton.md` (the shape contract this template copies).

## Why now

ROADMAP F3.1 sits at the front of the F3 block — the ten templates that the parent `template-authoring-convention` spec made parallelizable. P7.2 (`/strategic-intent`, the command that synthesizes a one-pager Strategic Intent) explicitly depends on F3.1: its `Depends on:` line in ROADMAP names this row. Until F3.1 ships, P7.2 is blocked and the Strategy phase has no canonical authoring path that the rest of the kit can rely on. The parent convention shipped 2026-05-22, so the contract surface F3.1 consumes is stable and committed. F3.1 is also the first F3.x to ship, which means its review will surface any latent ambiguity in the parent convention before nine more workers copy the same pattern — making it the natural canary.

## Inputs and outputs

**Inputs.**

- `templates/_meta/template-skeleton.md` — the canonical skeleton this template copies (read-only; not edited by this spec).
- `docs/HANDOVERS.md` §"Handover 1: Strategy → Discovery" — source-of-truth for the required frontmatter additions and the five required sections. Quoted verbatim below.
- `docs/CONVENTIONS.md` §"Universal metadata schema" — the universal frontmatter superset (inherited from the skeleton; no field added or removed).
- `docs/CONVENTIONS.md` §"Templates — `templates/<slug>.md`" — the authoring convention (placeholder syntax, frontmatter ordering, pre-fill rules).
- `context/frameworks/ontology.md` row "Strategic Intent" (Domain A + Domain D composite per HANDOVERS Handover 1's "Object type" line) — confirms the `object_type:` pre-fill value.
- `tools/lint-frontmatter.py --check-template` — the linter gate the template must pass.

**Outputs.**

1. `templates/strategic-intent.md` — new file. Single-file template. Copy of `templates/_meta/template-skeleton.md` with: `object_type:` pre-filled to `Strategic Intent`; H1 set to `# Strategic Intent`; the five required-section H2 headings replaced by the HANDOVERS-quoted headings; the Handover-1-specific frontmatter fields appended in a second block under the `# Handover-specific fields` YAML comment; the body's one-paragraph description below H1 citing HANDOVERS Handover 1.
2. `templates/_meta/README.md` — one-line append under "Shipped templates" (CAPTURE phase only; tiny dedicated commit per parent plan §Rollout to avoid races with other F3.x workers).
3. `ROADMAP.md` — F3.1 checkbox marked, no other edits (CAPTURE phase only).
4. `docs/specs/template-strategic-intent/spec.md` frozen to `Status: Shipped (<date>)` and `plan.md` frozen to `Status: Done (<date>)` (CAPTURE phase only).

**Required Handover-1 frontmatter (quoted verbatim from HANDOVERS.md §"Handover 1: Strategy → Discovery").** These are the additions on top of the universal schema that the template's second YAML block must encode:

```yaml
object_type: Strategic Intent
mode: greenfield | enterprise
central_challenge: <one sentence>
guiding_policy: <one paragraph>
coherent_actions:
  - <action 1>
  - <action 2>
  - <action 3>
  # 3-5 items, no more
horizon: <quarters>
business_objective: <linked Business Objective id>
parent_diagnosis: <path to diagnosis>
human_owned_decisions:
  - Whether to pursue this central challenge
  - Resource commitment behind coherent actions
human_approval_required: true
```

Note on integration with the universal schema: `object_type`, `human_owned_decisions`, and `human_approval_required` already exist in the universal schema (block 1 of the template's frontmatter); the template pre-fills `object_type: Strategic Intent` in block 1 and does NOT repeat it in block 2. `human_owned_decisions` and `human_approval_required` likewise live in block 1; the HANDOVERS Handover-1 contract pins their *values* (the two specific decisions and `true`), which the template encodes as the block-1 default values. The genuinely new (Handover-1-specific) fields the template appends in block 2 are: `mode`, `central_challenge`, `guiding_policy`, `coherent_actions`, `horizon`, `business_objective`, `parent_diagnosis`.

**Required sections (quoted verbatim from HANDOVERS.md §"Handover 1: Strategy → Discovery").** These become the template's five H2 headings, in this order:

1. **The challenge** — what specifically must be addressed; cite evidence (numbers, quotes, market signal)
2. **The guiding policy** — what *kind* of response we commit to; what we are *not* responding with
3. **Coherent actions** — 3-5 actions that reinforce each other; for each, name what it commits and what it forecloses
4. **Coherence check** — explicitly check pairs and confirm they don't cancel out
5. **Open questions for discovery** — what we don't know that discovery will address

**Downstream consumers.** P7.2 (`/strategic-intent` synthesis command) reads `templates/strategic-intent.md` as its scaffolding source. No other shipped or planned ROADMAP row consumes the template file directly today.

## Boundaries

### Always do

- Use angle-bracket placeholder syntax exclusively (`<descriptor>`); inherit the skeleton's placeholder discipline.
- Quote the five HANDOVERS Handover-1 required-section headings verbatim — the template's H2 text must match.
- Quote the Handover-1 frontmatter additions verbatim from HANDOVERS.md — field names, ordering, and inline-value choices (e.g., `greenfield | enterprise`, the human-owned-decision strings) match HANDOVERS.
- Pre-fill the template's identity fields and only those: `object_type: Strategic Intent` and `status: Draft`. Every other field is a placeholder.
- Keep the universal-schema block ordering identical to `templates/_meta/template-skeleton.md` (the parent convention pins ordering).
- Append the Handover-1-specific fields under the `# Handover-specific fields` YAML comment as a second block (per the parent convention's "Frontmatter ordering" rule).
- Pass `tools/lint-frontmatter.py --check-template templates/strategic-intent.md` and `python3 -m pytest scripts/tests/test_templates_instantiate.py` cleanly before CAPTURE.
- When HANDOVERS-1 fields overlap with the universal-metadata schema (e.g., `human_owned_decisions:`, `human_approval_required:`, `object_type:`), the field appears once — in its universal-schema position — carrying the HANDOVERS-1-mandated value. The universal-schema placeholder is deleted in the same edit. The handover-specific block carries only fields not present in the universal schema (for Handover 1: `mode`, `central_challenge`, `guiding_policy`, `coherent_actions`, `horizon`, `business_objective`, `parent_diagnosis`).

### Ask first

- Adding a field to the template not present in `docs/CONVENTIONS.md` §"Universal metadata schema" or `docs/HANDOVERS.md` §"Handover 1". The template is a re-projection of those two docs, not a parallel source of truth.
- Authoring a sixth required H2 section. HANDOVERS Handover 1 lists exactly five; adding a sixth requires editing HANDOVERS first.
- Pre-filling the `mode:` field. HANDOVERS lists it as `greenfield | enterprise` — a user choice tied to project mode (see `.claude/CLAUDE.md` §"Mode"). Leave it as the placeholder string `<greenfield | enterprise>`.

### Never do

- Invent domain content. The template body is shape-only: H2 headings plus one-line `<placeholder>` bodies. No example Strategic Intent prose, no real challenges, no real coherent actions.
- Use `{{...}}` or `__FILL__` placeholder syntax anywhere. The parent convention permits angle-bracket only; T16 in the parent spec greps these from the skeleton.
- Add `Strategic Intent template` (or similar) as a new ontology type. Templates are kit-build scaffolding; the ontology only carries instantiated-artifact types.
- Walk `templates/strategic-intent.md` from the default-mode linter. The linter contract (parent spec) keeps `templates/` outside `PHASE_DIRS`; only `--check-template` runs against it.
- Edit `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, or `scripts/tests/test_templates_instantiate.py`. If reality demands a HANDOVERS edit during EXECUTE, surface as a finding from adversarial review and resolve in a separate spec; do not silently rewrite the source-of-truth doc inside the F3.1 loop.

## Verification mode

- **Goal-based check** for the template's shape — required headings present in order, required frontmatter keys present, placeholder-syntax purity. Each check is a one-line shell or python predicate.
- **Audit-driven** for the linter and pytest gates: `python3 tools/lint-frontmatter.py --check-template templates/strategic-intent.md` exits 0; `python3 -m pytest scripts/tests/test_templates_instantiate.py` (which auto-discovers `templates/*.md`) exits 0; `bash tools/pre-pr.sh` exits 0.
- **Adversarial review** (manual gesture against a shipped template) — dispatch the `adversarial-reviewer` subagent against `templates/strategic-intent.md` versus HANDOVERS §"Handover 1" after the audit gate passes. Iterate fixes inline; max 3 review passes per the work-loop default.

The shape is the contract; once the shape passes the linter and the contract tests below, the template is done. Adversarial review hardens against drift, not correctness — correctness is mechanically verified.

## Contract tests

Each test is one shell line or one pytest case.

- `T1` — `test -f templates/strategic-intent.md` exits 0 (target file exists).
- `T2` — `python3 tools/lint-frontmatter.py --check-template templates/strategic-intent.md` exits 0 (passes the parent convention's linter gate).
- `T3` — Required frontmatter keys present. The union of universal-schema keys (from `templates/_meta/template-skeleton.md`) and Handover-1-specific keys must all appear:
  - Universal-schema keys: `id`, `slug`, `object_type`, `name`, `description`, `owner`, `status`, `priority`, `risk_level`, `created`, `last_updated`, `parent_intent`, `parent_opportunity`, `parent_learning`, `parent_vision`, `parent_initiative`, `related_problems`, `related_personas`, `related_kpis`, `evidence_basis`, `open_assumptions`, `human_owned_decisions`, `ai_assistance_used`, `ai_assistance_allowed`, `human_approval_required`, `approvals_obtained`, `open_questions`, `risks`.
  - Handover-1-specific keys (in the second block): `mode`, `central_challenge`, `guiding_policy`, `coherent_actions`, `horizon`, `business_objective`, `parent_diagnosis`.
  - Asserted by a python one-liner that parses the file's YAML frontmatter and asserts every key in the union appears at top level.
- `T4` — Required H2 section headings present in order. The five headings — `## The challenge`, `## The guiding policy`, `## Coherent actions`, `## Coherence check`, `## Open questions for discovery` — appear in `templates/strategic-intent.md` in that order. Asserted by `awk` or `grep -n` recording line numbers and checking monotonicity.
- `T5` — Angle-bracket-only placeholder syntax in the template body. `grep -c '{{' templates/strategic-intent.md` returns 0; `grep -c '__FILL__' templates/strategic-intent.md` returns 0.
- `T6` — Pytest harness picks the template up and passes: `python3 -m pytest scripts/tests/test_templates_instantiate.py -k 'strategic-intent.md'` exits 0 and selects exactly 1 parametrized test (the parametrized ID is `test_template_passes_check_template_mode[templates/strategic-intent.md]`; the path-token substring is the matcher), and the full pytest run on the same file still exits 0.
- `T7` — `bash tools/pre-pr.sh` exits 0 (kit-wide health check after the template lands).
- `T8` — ROADMAP F3.1 checkbox flipped: `grep -c '^- \[x\] \*\*F3\.1\*\*' ROADMAP.md` returns 1 (CAPTURE-phase predicate).
- `T9` — `templates/_meta/README.md` lists the template: `grep -c 'strategic-intent.md' templates/_meta/README.md` returns ≥ 1 (CAPTURE-phase predicate).
- `T10` — Pre-filled identity fields are exact: `grep -E '^object_type: Strategic Intent$' templates/strategic-intent.md` returns 1; `grep -E '^status: Draft[[:space:]#]' templates/strategic-intent.md` returns 1 (the trailing character class rejects loose matches like `Drafting`).
- `T11` — Default-mode linter does not traverse `templates/` (mode-separation property): `python3 tools/lint-frontmatter.py --all` exits 0 even though `templates/strategic-intent.md` carries placeholders that would fail validation if walked. This pins the parent convention's mode-separation property at the F3.1 level — if a future change to the linter ever started walking `templates/` from default mode silently, the default-mode sweep would surface placeholder failures and T11 would fail.

## Non-goals

- Authoring an instantiated Strategic Intent. F3.1 ships the skeleton; the kit user (or P7.2, when shipped) instantiates `strategy/intents/<slug>.md`.
- Building P7.2 (`/strategic-intent` synthesis command). Separate ROADMAP row; F3.1 unblocks it but does not implement it.
- Editing `docs/HANDOVERS.md`. The Handover-1 contract is stable; F3.1 is a downstream re-projection only. If adversarial review surfaces an actual contract gap, that becomes a separate spec, not an in-session HANDOVERS edit.
- Editing `docs/CONVENTIONS.md` or the universal-metadata schema. Same reasoning.
- Editing `tools/lint-frontmatter.py` or `scripts/tests/test_templates_instantiate.py`. The pytest harness auto-discovers `templates/*.md`; F3.1 needs no wiring.
- Adding `templates/CLAUDE.md`-style per-template guidance file. The skeleton + the spec are sufficient.
- Adding any of F3.2–F3.10 templates or shipping `tools/new-template.sh`. Out of scope per parent spec's §Non-goals.

## Open questions

1. **Should the template's H1 read `# Strategic Intent` (the type) or `# <Strategic Intent name>` (a placeholder for the kit-user-chosen name)?** Resolved here: `# Strategic Intent` as the H1 plus a one-paragraph description below that cites HANDOVERS Handover 1; the kit user replaces the H1 with their specific Strategic Intent name when instantiating. This mirrors how the parent skeleton's H1 (`# <Artifact name>`) becomes type-specific in each F3.x template. If the F3.2–F3.10 workers reach a different convention via their own adversarial reviews, F3.1 will follow in a tiny patch.
2. **Should `priority:` and `risk_level:` carry sensible defaults for Strategic Intents (e.g., `High`)?** Resolved here: no. Pre-fill only the template's identity fields (`object_type`, `status`); leave priority/risk-level as the skeleton's `<Low | Medium | High | Critical>` placeholder. Justification: a Strategic Intent could legitimately ship at any priority depending on context; pre-filling would bias the kit user.
3. **Does HANDOVERS' `central_challenge: <one sentence>` constrain placement to the YAML frontmatter only, or also as a quoted sentence at the top of the body?** Resolved here: frontmatter only. HANDOVERS lists `central_challenge` under "Required frontmatter," not under "Required sections" — the body section it maps to is `## The challenge` (which is more discursive). If P7.2 wants to synthesize an executive-summary block that pulls `central_challenge` into the body, that's its concern, not the template's.

## Acceptance criteria

- [ ] `templates/strategic-intent.md` exists at the named path.
- [ ] `python3 tools/lint-frontmatter.py --check-template templates/strategic-intent.md` exits 0.
- [ ] The template's frontmatter contains every key in the universal-schema set AND every Handover-1-specific key listed in §"Inputs and outputs" (asserted by T3).
- [ ] The five H2 headings appear in order: `## The challenge`, `## The guiding policy`, `## Coherent actions`, `## Coherence check`, `## Open questions for discovery` (asserted by T4).
- [ ] `grep -c '{{' templates/strategic-intent.md` returns 0 AND `grep -c '__FILL__' templates/strategic-intent.md` returns 0 (asserted by T5).
- [ ] `python3 -m pytest scripts/tests/test_templates_instantiate.py` exits 0 (asserted by T6).
- [ ] `bash tools/pre-pr.sh` exits 0 (asserted by T7).
- [ ] ROADMAP.md F3.1 row is checked off (asserted by T8).
- [ ] `templates/_meta/README.md` "Shipped templates" list includes `strategic-intent.md` (asserted by T9).
- [ ] Pre-filled identity fields are exact: `object_type: Strategic Intent` and `status: Draft` (asserted by T10).
- [ ] Default-mode linter does not traverse `templates/` (asserted by T11).
- [ ] `adversarial-reviewer` subagent returns no Blocking findings against the shipped template vs HANDOVERS §"Handover 1".

## Cross-references

- **Consumed by:** ROADMAP P7.2 `/strategic-intent` (synthesis command; depends on F3.1 per its `Depends on:` line). Any future kit user authoring a Strategic Intent by hand.
- **Consumes:** `templates/_meta/template-skeleton.md`; `docs/HANDOVERS.md` §"Handover 1: Strategy → Discovery"; `docs/CONVENTIONS.md` §"Templates" and §"Universal metadata schema"; `context/frameworks/ontology.md` Domain A row "Strategic Intent"; `tools/lint-frontmatter.py --check-template`; `scripts/tests/test_templates_instantiate.py`.
- **Frontmatter fields owned:** the template encodes (and thereby "owns" at the template level — the canonical source remains HANDOVERS) the Handover-1-specific keys `mode`, `central_challenge`, `guiding_policy`, `coherent_actions`, `horizon`, `business_objective`, `parent_diagnosis`, plus the Handover-1-mandated values of `human_owned_decisions` (the two named decisions) and `human_approval_required: true`. Inherits the full universal-schema key set from the skeleton; does not add new universal-schema fields.
- **Ontology object types touched:** Strategic Intent (Domain A + Domain D composite; the type instantiated by `strategy/intents/<slug>.md`). Business Objective (Domain D; referenced via the `business_objective:` frontmatter field — by id, not instantiated here).
