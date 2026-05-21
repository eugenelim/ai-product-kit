---
description: Run the ontology's 25-item pre-engineering-handoff checklist against a named initiative or handoff packet. Flags every missing field, missing approval, untraceable requirement, or weak-evidence link. Refuses to mark complete without the named human signatures.
argument-hint: "<initiative-slug> | <handoff-packet-slug>"
---

# /audit-completeness

**Canonical implementation:** `scripts/audit-completeness.py` (F1.5 — shipped 2026-05-21). When the script is available:

```bash
python3 scripts/audit-completeness.py --target <slug> --root . --format markdown
```

Exit codes: 0 pass, 1 needs-fixes, 2 block. Add `--write` to persist the report under `delivery/handoff-packets/<slug>/completeness-audit-<date>.md` and append to `AUDIT-LOG.md`. The prose procedure below is the fallback when reviewing the contract.

---

Run the canonical pre-engineering-handoff checklist (ontology section 41) against a named initiative or handoff packet. This is the single command that determines whether engineering should accept the work.

The audit is mechanical. The decision to *override* a flagged item is human-only.

## When to run

- Before declaring a `delivery/initiatives/<slug>/` ready for engineering handoff
- Before assembling a `delivery/handoff-packets/<slug>/` for an engineering team
- As a recurring audit on active initiatives (the `delivery-manager` scheduled agent runs this weekly)
- As a final check before a vision transitions from `In Review` to `Approved`

## Inputs

1. The named initiative folder (`delivery/initiatives/<slug>/`) OR handoff packet (`delivery/handoff-packets/<slug>/`)
2. Every traced artifact upstream: vision → learning → opportunity → OST → intent
3. `context/frameworks/ontology.md` — the type system being applied
4. `docs/CONVENTIONS.md` — the universal metadata schema
5. `docs/HUMAN-AI-OWNERSHIP.md` — the human-approval requirements

If any of these are missing, surface that and stop. An audit on missing inputs returns false confidence.

## The 25-item checklist

Walk through each item. For each, mark `[x]` if present and valid, `[ ]` if missing, `[!]` if present but weak (evidence, ownership, or rationale).

```
[ ] 1.  Business objective is defined.                          (Domain A)
[ ] 2.  Target customer segment is defined.                     (Domain B)
[ ] 3.  Primary personas are defined.                           (Domain B)
[ ] 4.  Problem statement is clear.                             (Domain C)
[ ] 5.  Evidence is attached to the problem.                    (Domain C)
[ ] 6.  Current workaround is understood.                       (Domain C)
[ ] 7.  Jobs to Be Done are documented.                         (Domain C)
[ ] 8.  Desired outcomes are defined.                           (Domain D)
[ ] 9.  KPIs are defined.                                       (Domain D)
[ ] 10. Capabilities are defined.                               (Domain E)
[ ] 11. Features are mapped to capabilities.                    (Domain E)
[ ] 12. Requirements are mapped to features and capabilities.   (Domain E)
[ ] 13. Acceptance criteria are defined.                        (Domain E)
[ ] 14. Business rules are documented.                          (Domain E)
[ ] 15. Policy or compliance constraints are documented.        (Domains A, E)
[ ] 16. Risks are documented.                                   (Domain G)
[ ] 17. Mitigations or controls are assigned.                   (Domain G)
[ ] 18. Dependencies are identified.                            (Domain E)
[ ] 19. Open questions are listed.                              (Domain E)
[ ] 20. Out-of-scope items are listed.                          (Domain E)
[ ] 21. Pricing or packaging implications are flagged.          (Domain F)
[ ] 22. Support and operational implications are flagged.       (Domain G)
[ ] 23. Human-owned decisions are explicitly marked.            (Domain H)
[ ] 24. Required approvals are identified.                      (Domain H)
[ ] 25. Decision log is current.                                (Domain H)
```

## Procedure

### Step 1 — locate the artifact

Resolve the slug to a folder. If both an initiative and a handoff packet exist with the same slug, prefer the handoff packet (it's the more synthesized form).

### Step 2 — walk the checklist

For each item:
1. Identify the artifact and field where the item lives (per `docs/CONVENTIONS.md`).
2. Check presence: is the field populated?
3. Check quality: if `evidence_basis:`, is the strength `Strong | Moderate` (mark `[x]`) or `Weak` (mark `[!]`)?
4. Check traceability: does the linked parent exist? Is the link unbroken?
5. Check approval: if `human_approval_required: true`, are the `approvals_obtained:` complete?

### Step 3 — traceability sub-audit

For each Requirement in the initiative:
- Trace upward: Requirement → Capability → Problem → Evidence
- Trace toward outcomes: Requirement → Acceptance Criteria → KPI → Outcome → Business Objective
- A break anywhere in the chain is a `[!]`; missing nodes are `[ ]`

### Step 4 — produce the report

Write `delivery/handoff-packets/<slug>/completeness-audit-<YYYY-MM-DD>.md` with frontmatter:

```yaml
---
date: <YYYY-MM-DD>
target_slug: <slug>
target_type: initiative | handoff-packet
items_passed: <count>
items_weak: <count>
items_missing: <count>
human_approvals_outstanding: <count>
verdict: pass | needs-fixes | block
verdict_rationale: <one paragraph>
---
```

Sections:

1. **Verdict** — pass / needs-fixes / block, in one paragraph
2. **Checklist** — the 25 items with `[x]`, `[ ]`, `[!]` marks and pointers
3. **Traceability breaks** — every Requirement with an unbroken / weak chain, with diagnosis
4. **Outstanding human approvals** — required approvals not yet obtained, with named owner
5. **Recommended remediations** — for each `[!]` and `[ ]`, the specific next action

### Step 5 — log

Append to `delivery/handoff-packets/AUDIT-LOG.md`: date, target slug, verdict, counts.

## Stop conditions

Stop and surface to the user before continuing if:
- The target slug doesn't resolve to a folder
- The target has no `parent_initiative:` or `parent_vision:` link (the artifact is orphaned; the upstream chain is missing)
- More than 8 active initiatives passed to a batch run (the audit is detailed; parallelize via sub-agents rather than serial)

## Verdict thresholds

- **pass** — all 25 items `[x]`, traceability complete, all required approvals obtained
- **needs-fixes** — ≤5 items `[!]` or `[ ]`, no traceability breaks, ≤2 approvals outstanding
- **block** — anything worse than needs-fixes; engineering should not begin

A `block` verdict is mechanical. The decision to override and proceed anyway is human-only and must be recorded as an ADR (`docs/adr/`) naming the override and its risk.

## Why this matters

From the ontology: "Before engineering, the product/business side should not merely say 'feature: add AI audit export.' It should say [the full handoff narrative]. That is the level of definition that creates a strong product-to-engineering handoff."

`/audit-completeness` is the mechanical version of that judgment. It doesn't tell you whether the work is *good*; it tells you whether engineering has enough to start without re-deriving the business context themselves.

$ARGUMENTS
