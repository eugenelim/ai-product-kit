# `templates/_meta/`

Infrastructure for the kit's template system, not a template itself. `_meta/` holds the canonical skeleton every F3.x template copies from, plus this index of all shipped templates. Templates instantiated from this skeleton live as `templates/<slug>.md` (single-file) or `templates/<slug>/README.md` (folder-based) — see [`docs/CONVENTIONS.md` §"Templates"](../../docs/CONVENTIONS.md#templates--templatesslugmd) for the full authoring convention.

## Files

- [`template-skeleton.md`](./template-skeleton.md) — the canonical skeleton. Copy this to start any new template. Body capped at ≤ 80 lines so it stays a shape contract, not a parallel source of truth.
- `README.md` (this file) — index of shipped templates, updated as each F3.x lands. Prose-only; no YAML frontmatter.

## Shipped templates

- [`strategic-intent.md`](../strategic-intent.md) — Strategy → Discovery handover (HANDOVERS §"Handover 1"). Spec: `docs/specs/template-strategic-intent/`.
- [`ost.md`](../ost.md) — Opportunity Solution Tree, Discovery → Validation handover (HANDOVERS §"Handover 2"). Spec: `docs/specs/template-ost/`.
- [`assumption-map.md`](../assumption-map.md) — Discovery → Assumption Map handover (HANDOVERS §"Handover 2.5"). Spec: `docs/specs/template-assumption-map/`.
- [`experiment/`](../experiment/) — Experiment design + results folder template, scaffolds the artifact pair the Validation Learning Memo's `test.experiment:` link resolves to (per HANDOVERS §"Handover 3" + `assumption-threshold-lock` hook). Spec: `docs/specs/template-experiment/`.
- [`learning-memo.md`](../learning-memo.md) — Validation Learning Memo, Validation → Vision handover (HANDOVERS §"Handover 3"). Spec: `docs/specs/template-learning-memo/`.
- [`vision.md`](../vision.md) — Vision → Initiative handover (HANDOVERS §"Handover 4"). Spec: `docs/specs/template-vision/`.
- [`initiative/`](../initiative/) — Initiative folder template (per HANDOVERS §"Handover 5"); README + five narrative child files (`context-map.md`, `flow.md`, `child-specs.md`, `sequence.md`, `capabilities.md`). Spec: `docs/specs/template-initiative/`.
- [`pm-spec.md`](../pm-spec.md) — PM-side Feature spec, sits under an Initiative's `child-specs.md` manifest; instantiates as `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`. Spec: `docs/specs/template-pm-spec/`.
- [`landing-report.md`](../landing-report.md) — Engineering → Landings handover (HANDOVERS §"Handover 7"); predicted-vs-actual outcomes, adoption curve, counter-metrics, verdict. Spec: `docs/specs/template-landing-report/`.
- [`handoff-packet/`](../handoff-packet/) — Handoff Packet folder template (per HANDOVERS §"Handover 6"); README + 21 narrative content files + `requirements.yaml` (Requirement registry). Spec: `docs/specs/template-handoff-packet/`.

## Why this directory

The ten F3.x templates share contract surface (frontmatter ordering, placeholder syntax, required-vs-optional section convention). Without a shared skeleton, ten parallel work-loops would drift on shape. The skeleton + convention collapse those ten shape-decisions into one. See `docs/specs/template-authoring-convention/spec.md` for the full rationale.
