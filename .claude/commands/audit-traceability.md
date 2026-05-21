---
description: Audit the kit's traceability chain — every Requirement traces to a Capability, every Capability to a Problem, every Problem to Evidence, every KPI to an Outcome, every high-risk Requirement to an Owner and Mitigation. Fails on broken or weak links.
argument-hint: "[optional: scope — 'all' | <initiative-slug> | <intent-slug>]"
---

# /audit-traceability

Run the ontology's seven traceability rules across the kit. Without this, requirements can drift away from problems, capabilities can drift away from objectives, and the kit silently accumulates engineering work disconnected from business value.

**Canonical implementation:** `scripts/audit-traceability.py` (F1.4 — shipped 2026-05-21). When the script is available, invoke it directly:

```bash
python3 scripts/audit-traceability.py --root . --scope all --format markdown
```

Exit codes: 0 clean, 1 drift, 2 broken, 3 insufficient-data. Add `--write` to persist the report to `docs/audits/traceability-<date>.md` and append a log entry. The procedure below remains the prose fallback when reviewing the contract or when the script is unavailable.

## When to run

- Weekly as part of the trio cadence review
- Before any `/audit-completeness` on a major initiative
- Before any quarterly `/strategy-refresh` — orphaned artifacts upstream of strategy decay the next intent
- When something feels wrong — orphaned traceability is the most common silent failure

## Inputs

1. The scope (default: `all`; or a single intent / initiative slug)
2. `context/frameworks/ontology.md` — the type system and traceability rules
3. Every artifact in the scoped subtree

## The seven traceability rules

1. **Every Requirement must trace to a Capability.**
2. **Every Capability must trace to a Problem, Business Objective, or Policy Rule (Domain E).**
3. **Every Problem must trace to Evidence** (or be explicitly marked Assumption until evidence exists).
4. **Every KPI must trace to an Outcome.**
5. **Every high-risk Requirement must have a named Owner and a Mitigation.**
6. **Every major Decision must have a Decision Owner and Rationale** recorded in `docs/adr/`.
7. **Every engineering Handoff Packet must identify what is fixed, flexible, and unknown.**

## Procedure

### Step 1 — scope the audit

If `all`, audit the whole kit. Otherwise resolve the slug to its subtree:
- Intent slug → all OSTs and downstream artifacts citing it
- Initiative slug → all specs / handoff packets citing it; upward to the parent vision, learning, opportunity, intent

### Step 2 — extract the graph

Build the directed graph of typed objects. Each node is an artifact + its `object_type:`. Each edge is a `parent_*:` or `related_*:` link.

If the scope contains many objects, fan out to sub-agents — one per upstream subtree — using the `traceability-walker` worker agent. Each walks its subtree and returns the broken-link list.

### Step 3 — apply the rules

For each rule, traverse the graph and flag violations:

- **Rule 1:** any Requirement node without an outgoing edge to a Capability
- **Rule 2:** any Capability without an outgoing edge to {Problem | Business Objective | Policy Rule}
- **Rule 3:** any Problem without an outgoing edge to Evidence, AND not marked `object_type: Assumption`
- **Rule 4:** any KPI without an outgoing edge to an Outcome
- **Rule 5:** any Requirement with `risk_level: High | Critical` AND missing `owner:` OR missing related Mitigation
- **Rule 6:** any artifact with `object_type: Decision` missing either `decision_owner:` (or `owner:` mapped to a named individual) OR with no corresponding ADR in `docs/adr/` referencing the decision's id. (Distinct from the lifecycle-state `approvals_obtained:` check, which is the completeness audit's job, not traceability's.)
- **Rule 7:** any Handoff Packet missing the "fixed / flexible / unknown" section

### Step 4 — assess link strength

For each surviving link, check the linked artifact's evidence quality:
- Strong evidence → link counted as solid
- Moderate evidence → link counted but flagged
- Weak evidence or pure assumption → link flagged as **weak**

A "weak chain" is one where any link in the upstream chain has weak evidence. Engineering should know.

### Step 5 — produce the audit

Write `docs/audits/traceability-<YYYY-MM-DD>.md` with frontmatter:

```yaml
---
date: <YYYY-MM-DD>
scope: <all | slug>
objects_audited: <count>
rules_violated: <count of distinct violations>
broken_links: <count>
weak_chains: <count>
verdict: clean | drift | broken
---
```

Sections:

1. **Verdict** — clean / drift / broken in one paragraph
2. **Rule violations** — one section per violated rule, with the list of offending artifacts and their remediation
3. **Weak chains** — every chain with one or more weak-evidence links, with the specific link flagged
4. **Orphans** — artifacts at the top of their subtree with no parent (these are either roots, or symptoms of a missing upstream artifact)
5. **Recommended remediations** — for each violation, the named next action

### Step 6 — log

Append to `docs/audits/TRACEABILITY-LOG.md`: date, scope, verdict, counts.

## Verdict thresholds

- **clean** — all rules pass; no broken links; ≤10% weak chains
- **drift** — 1–3 broken links; ≤25% weak chains; recoverable in a single session
- **broken** — >3 broken links or systemic weakness; the upstream phase is failing; surface to the human

A `broken` verdict means the kit is shipping confidence the evidence doesn't support. That's the failure mode the audit exists to prevent.

## Why this matters

From the ontology, section 32: "Every requirement must trace to a capability. Every capability must trace to a problem, business objective, or policy rule. Every problem must trace to evidence." Engineering inherits whatever business context is *traceable*. Anything that isn't, engineering re-derives — usually wrong, usually after wasting weeks.

$ARGUMENTS
