# Spec: audit-completeness-script

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored)
- **Component type:** script
- **Serves kit phase:** Phase 4D (Engineering Handoff)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md`; the existing `.claude/commands/audit-completeness.md`; `docs/HANDOVERS.md` Handover 6; ontology §41 (the 25-item checklist)

> **Spec contract.** Promote the prose `/audit-completeness` to a runnable `scripts/audit-completeness.py`.

## Objective

Build `scripts/audit-completeness.py`: walk the 25-item ontology pre-engineering-handoff checklist against a named initiative or handoff packet. Exit code encodes verdict; markdown report carries item-by-item pass/fail with `[ ]` / `[x]` / `[!]` (weak).

## Why now

`/audit-completeness` is the highest-stakes audit (gates the engineering handoff). Promoting to a script makes the 25 items deterministically checkable and CI-runnable.

## Inputs and outputs

**Inputs.**
- `--target`: `<initiative-slug>` | `<handoff-packet-slug>` (required).
- `--root`: kit root (default: cwd).
- `--format`: `markdown` | `json`.
- `--write`: write report to `delivery/handoff-packets/<slug>/completeness-audit-<YYYY-MM-DD>.md` (or the initiative fallback path if no packet exists).

**Outputs.**
- A markdown checklist report with frontmatter (matching the prose command's Step 4 schema): `date`, `target`, `items_checked`, `items_passed`, `items_weak`, `items_missing`, `human_approvals_outstanding`, `verdict`. (Field names match the prose command exactly so existing tooling reading either source consumes the same schema.)
- Sections: Verdict; Checklist (the 25 items, with item 24 split into 24a/24b per the in-pass review — 26 check functions covering 25 numbered items); Weak items detail; Missing items + remediation; Traceability sub-audit (cited from F1.4); Open questions.
- Exit code per the command-file thresholds (single source of truth: `.claude/commands/audit-completeness.md` §Verdict thresholds):
  - `0` pass: all 25 items `[x]`, traceability sub-audit clean, all required approvals obtained.
  - `1` needs-fixes: ≤5 items `[!]` or `[ ]`, no traceability breaks, ≤2 approvals outstanding.
  - `2` block: anything worse than needs-fixes, OR traceability sub-audit returns `broken`, OR target is an initiative without a handoff packet (a structural block — see §Always do).

## Boundaries

### Always do
- Use `scripts.lib.graph` and `scripts.lib.frontmatter`.
- Match the 25 items from the prose `/audit-completeness` line-for-line in *item text*. Each check function implements the verification logic per the command file's Step 2 for that item — categorized as one of: **presence-check** (file/section exists), **field-quality-check** (frontmatter field present and non-trivial), **strength-check** (evidence strength ≥ Moderate), **traceability-check** (parent link resolves), or **approval-check** (named human in `approvals_obtained:`). The per-item strategy is documented in a `CHECK_STRATEGY` table inside the script.
- Handle the "target is an initiative folder, no handoff packet exists yet" case as a hard structural block: emit `verdict: block` with a single diagnostic ("no handoff packet found at `delivery/handoff-packets/<slug>/`; checklist cannot be evaluated"). Do NOT attempt to evaluate individual items.
- Handle the "target is a handoff packet with no `parent_initiative:`" case the same way: structural block, single diagnostic.
- Handle the "multiple handoff packets exist for the same slug" case: use the most-recently-modified packet (by file mtime); add an `open_questions` entry noting the older packet(s) and recommending archive.
- Distinguish identified-vs-obtained approvals (the in-pass split into 24a + 24b — 26 check functions covering 25 numbered items).
- Append a one-line summary to `delivery/handoff-packets/AUDIT-LOG.md` (or `delivery/initiatives/AUDIT-LOG.md` fallback) when `--write` is set; create with header if absent.
- `--write` always produces markdown (`.md`); when `--format json` is also set, JSON is emitted to stdout and the markdown report is still written to disk. Don't conflate output stream with persistent artifact.
- Scope the traceability sub-audit to the target's subtree: invoke `scripts/audit-traceability.py --scope <target-slug>`, NOT `--scope all`. Misleading clean traceability on a wider-than-target scope is worse than a focused failure.

### Ask first
- Adding a 26th item or changing thresholds. Default: don't; track via RFC.

### Never do
- Mutate target artifacts.
- Write outside `delivery/handoff-packets/<slug>/` or `delivery/initiatives/<slug>/`.

## Verification mode

- **TDD.** Unit tests against the F1.1 fixture sample-kit.
- **Goal-based check.** Run against the sample-kit handoff packet; assert pass. Run against a deliberately-incomplete fixture; assert needs-fixes.

## Contract tests

- `test_pass_verdict_on_complete_sample_kit_packet`
- `test_block_verdict_on_initiative_without_handoff_packet`
- `test_needs_fixes_verdict_on_packet_with_2_weak_items`
- `test_block_verdict_on_packet_with_missing_required_approval`
- `test_traceability_subaudit_is_cited`
- `test_24a_vs_24b_approval_split_is_enforced`
- `test_write_flag_creates_report_under_packet_dir`
- `test_write_flag_falls_back_to_initiative_dir_when_packet_absent`
- `test_json_output_shape`
- `test_25_items_map_to_26_check_functions_via_24a_24b_split`
- `test_orphaned_handoff_packet_with_no_parent_initiative_yields_block`
- `test_traceability_subaudit_exit_2_forces_block`

## Non-goals

- Doing the traceability rules itself (cite F1.4's output).
- Coherence audits (F1.6).
- Auto-fixing — read-only audit.

## Open questions

1. **Cite F1.4 by invocation or import?** **Resolved: subprocess invocation.** The script shells out via `subprocess.run(["python3", "scripts/audit-traceability.py", "--scope", target_slug, "--root", root, "--format", "json"])` and parses the JSON output. Rationale: F1.4's public API is undefined (CLI-first design); subprocess gives a stable contract that doesn't require F1.4 to expose internals. Non-zero exit from the traceability sub-audit (exit 2 from F1.4) forces this audit's verdict to `block`; exit 1 (drift) flags the traceability section as `weak` but doesn't force `block`; exit 3 (insufficient-data) is reported as an open question, doesn't affect verdict.
2. **Per-item check functions:** lean — one function per item, all in a `CHECKS` dict keyed by item-id. 26 functions for 25 numbered items (24 splits into 24a/24b).

## Acceptance criteria

- [ ] `scripts/audit-completeness.py` exists, stdlib + `scripts.lib.*` only, ≤ ~400 LOC.
- [ ] `scripts/tests/test_audit_completeness.py` exists; all 10 contract tests pass.
- [ ] `python3 -m unittest scripts.tests.test_audit_completeness` exits 0.
- [ ] End-to-end: `python3 scripts/audit-completeness.py --target auth-uplift --root scripts/tests/fixtures/sample-kit` exits 0.
- [ ] `.claude/commands/audit-completeness.md` updated: shell-out subsection added; prose retained as fallback.
- [ ] INVENTORY.md `/audit-completeness` row Status: `shipped (script + prose fallback)`.
- [ ] ROADMAP.md: F1.5 checked off.
- [ ] PLAN/VERIFY/REVIEW gates exit 0.

## Cross-references

- **Consumed by:** `/audit-completeness` command; `/audit-all` aggregator (P6.3).
- **Consumes:** `scripts.lib.graph` (F1.1), `scripts.lib.frontmatter` (F1.2), `scripts.audit_traceability` (F1.4) for the traceability sub-audit.
- **Frontmatter fields owned:** writes its own report frontmatter.
- **Ontology object types touched:** Handoff Packet (Domain H), Initiative (Domain D), and every type the 25 items reference.
