---
description: Audit Handover-5 linkage — every PM Spec under delivery/initiatives/*/specs/ must declare a parent_initiative that resolves to an existing initiative. Fails on missing or dangling links. Mirrors the F1.4 audit-traceability script + prose-fallback shape.
argument-hint: "[optional: scope — 'all' | <initiative-slug>]"
---

# /audit-spec-linkage

Enforce the one structural rule from Handover 5 (Initiative → Spec): every PM Spec lives under an Initiative and declares a resolving `parent_initiative:` frontmatter field. Without this audit, specs can drift away from their parent initiative silently, breaking cross-team traceability and the engineering-handoff chain.

**Canonical implementation:** `scripts/audit-spec-linkage.py` (P4.10). When the script is available, invoke it directly:

```bash
python3 scripts/audit-spec-linkage.py --root . --scope all --format markdown
```

Exit codes: 0 clean, 1 drift, 2 broken, 3 insufficient-data. Add `--write` to persist the report to `docs/audits/spec-linkage-<date>.md` and append a log entry to `docs/audits/SPEC-LINKAGE-LOG.md`. `--write` always persists a markdown report regardless of `--format`; the `--format` flag governs only what is written to stdout. The prose procedure below remains the fallback when reviewing the contract or when the script is unavailable.

This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply.

## When to run

- Before any `/audit-traceability` on an initiative — Handover-5 must be sound before deeper rules are meaningful
- Before declaring a Handover 5 sound for engineering pickup
- Weekly as part of the delivery cadence
- After any bulk spec-rename or initiative-reorganization
- When `/phase-guide` surfaces "specs without parent_initiative" drift

## Inputs

1. The scope (default `all`; or a single `<initiative-slug>` to limit to one subtree)
2. The kit tree under `delivery/initiatives/*/specs/*.md`
3. `scripts/lib/graph.py` (F1.1) and `scripts/lib/frontmatter.py` (F1.2) — consumed by the script for graph traversal and frontmatter parsing

## The rule

**Rule 1:** Every PM Spec at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` must declare `parent_initiative:` in its frontmatter, AND the value must resolve to an existing `delivery/initiatives/<value>/README.md`.

Violation kinds:
- `missing-parent-initiative` — the `parent_initiative:` field is absent or empty.
- `dangling-parent-initiative` — the `parent_initiative:` field is present but its target initiative folder is missing.

## Stdout header (printed before the markdown payload)

The script prints three labelled lines to stdout, in order, before the markdown payload (the Wave-3 family shape shared with `/vision-shape-check` and `/spec-impact-analysis`):

```
PHASE: Delivery → Spec linkage audit (scope=<scope>)
VERDICT: clean | drift | broken | insufficient-data
NEXT: <one-line recommended human action>
```

The `--write` path persists only the markdown payload (frontmatter + body); the three-line header is for the human reading the terminal and is not included in the written file or the log entry.

## Procedure

### Step 1 — scope the audit

If `all`, audit every initiative subtree. Otherwise resolve the slug to a single `delivery/initiatives/<initiative-slug>/specs/` subtree.

### Step 2 — extract the spec set

Build the typed-object graph via `scripts.lib.graph.build(root)`. Filter to nodes whose path matches `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` (the flat-file layout per `templates/initiative/child-specs.md` and `.claude/commands/draft-spec.md:36`).

### Step 3 — apply Rule 1

For each PM Spec node:

- If `parent_initiative:` is absent or empty → `missing-parent-initiative`.
- If `parent_initiative:` is present but the target initiative folder (`delivery/initiatives/<value>/README.md`) is missing → `dangling-parent-initiative`.

### Step 4 — produce the audit

Emit a markdown report with frontmatter:

```yaml
---
date: <YYYY-MM-DD>
scope: <all | initiative-slug>
specs_audited: <count>
broken_links: <count of violations>
verdict: clean | drift | broken | insufficient-data
object_type: Audit Report
status: Draft
last_updated: <YYYY-MM-DD>
---
```

Sections:

1. **Verdict** — one paragraph.
2. **Rule 1 violations** — table: `spec_slug | path | violation_type | remediation`.
3. **Orphans** — specs at the top of their subtree with no parent (roots or symptoms of missing initiatives).
4. **Recommended remediations** — named next action per violation.

### Step 5 — log (only when `--write`)

Append to `docs/audits/SPEC-LINKAGE-LOG.md`: date, scope, verdict, counts. Format: `- <date> scope=<scope> verdict=<verdict> specs=<n> broken=<n>`.

## Verdict thresholds

- **clean** — 0 broken links.
- **drift** — 1–3 broken links AND ≤25% of audited specs are broken; recoverable in a single session.
- **broken** — >3 broken links OR >25% systemic; surface to the human.
- **insufficient-data** — fewer than 3 specs in scope.

A `broken` verdict means cross-team handoffs are silently re-litigated inside individual specs. That is exactly the failure mode Handover 5 was authored to prevent.

## Why this matters

Handover 5 (`docs/HANDOVERS.md` §"Handover 5: Initiative → Spec") binds layout to contract: a PM Spec only carries the cross-team and capability context it inherits from a named parent Initiative. A spec without a resolving `parent_initiative:` is engineering work disconnected from initiative-level prioritization, ownership, and Capability traceability. This audit is the F2.5 `check-handover-link` hook's deferred child-spec coverage (`.claude/hooks/check-handover-link.md:79,98`).

$ARGUMENTS
