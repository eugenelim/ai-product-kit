# `templates/_meta/`

Infrastructure for the kit's template system, not a template itself. `_meta/` holds the canonical skeleton every F3.x template copies from, plus this index of all shipped templates. Templates instantiated from this skeleton live as `templates/<slug>.md` (single-file) or `templates/<slug>/README.md` (folder-based) — see [`docs/CONVENTIONS.md` §"Templates"](../../docs/CONVENTIONS.md#templates--templatesslugmd) for the full authoring convention.

## Files

- [`template-skeleton.md`](./template-skeleton.md) — the canonical skeleton. Copy this to start any new template. Body capped at ≤ 80 lines so it stays a shape contract, not a parallel source of truth.
- `README.md` (this file) — index of shipped templates, updated as each F3.x lands. Prose-only; no YAML frontmatter.

## Shipped templates

_(None yet. F3.x workers append their templates here in their CAPTURE phase.)_

## Why this directory

The ten F3.x templates share contract surface (frontmatter ordering, placeholder syntax, required-vs-optional section convention). Without a shared skeleton, ten parallel work-loops would drift on shape. The skeleton + convention collapse those ten shape-decisions into one. See `docs/specs/template-authoring-convention/spec.md` for the full rationale.
