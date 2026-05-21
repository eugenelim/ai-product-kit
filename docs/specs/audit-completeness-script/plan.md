# Plan: audit-completeness-script

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

## Approach

The script is a registry of 25 per-item check functions plus a runner that aggregates results. Each check function takes the target artifact + the kit graph and returns `(status, evidence)` where status ∈ `pass | weak | fail`. The runner walks the registry, aggregates, decides verdict, renders.

Item 24 splits into 24a (approvals identified) and 24b (approvals obtained) per the in-pass review fix.

## Constraints

- Stdlib + `scripts.lib.*` only.
- ≤ ~400 LOC.
- Match the 25 items line-for-line with `.claude/commands/audit-completeness.md`.

## Tasks

### Task 1: Write `scripts/tests/test_audit_completeness.py` (red)

- **Depends on:** F1.1 + F1.2 + F1.4 shipped.
- **Tests:** all 10 contract tests.
- **Approach:** add `scripts/tests/fixtures/completeness/` with: a complete packet, an initiative without a packet, a packet missing 2 items, a packet missing a required approval.
- **Done when:** suite fails as expected.

### Task 2: Implement `scripts/audit-completeness.py` (green)

- **Depends on:** Task 1.
- **Approach:**
  - `CHECKS: dict[str, Callable]` — 25 (or 26 with 24a/24b split) functions.
  - `audit(target, root) -> Report`.
  - `verdict_for(report)`.
  - `render_markdown(report)`, `render_json(report)`.
  - Imports `scripts.audit_traceability` and calls its rule functions for the traceability sub-audit.
- **Done when:** unit tests pass; smoke command exits 0.

### Task 3: Update `.claude/commands/audit-completeness.md`

- **Depends on:** Task 2.
- **Approach:** add shell-out subsection; keep the 25-item checklist text in sync with the script. The command file is the SSOT for item text; the script's `CHECKS` dict carries verbatim copies.
- **Done when:** lint-command.sh exits 0. A diff between the command's 25 item lines and the script's `CHECKS` keys-and-titles shows no mismatch (run this as a manual sanity check in the spec's `notes/`).

### Task 4: Register

- **Depends on:** Tasks 1-3.
- **Approach:** INVENTORY status update; ROADMAP F1.5 check.
- **Done when:** ROADMAP shows F1.5 checked.

## Rollout

- `/audit-completeness` becomes deterministically runnable.
- F1.5 unblocks the work-loop's CAPTURE-phase audit recommendation.

## Risks

- **25-item checklist drift between script and command file.** Mitigation: the command file is the single source of truth; the script carries verbatim copies of the item text in a `CHECKS` dict. Task 3 runs a manual diff sanity check.
- **Coupling to F1.4.** Mitigated by the subprocess-invocation decision (spec OQ1 resolved): we shell out to F1.4's CLI and parse JSON output, so we depend only on F1.4's documented CLI contract, not its internals.
- **F1.1 / F1.2 dependency.** This spec's EXECUTE is BLOCKED until F1.1 and F1.2 ship. The plan's Task 1 enforces this as a precondition.

## Changelog

- 2026-05-21: Initial plan.
