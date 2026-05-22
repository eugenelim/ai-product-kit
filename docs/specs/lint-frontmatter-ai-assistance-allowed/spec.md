# Spec: lint-frontmatter-ai-assistance-allowed

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** script (extension to existing linter)
- **Serves kit phase:** Meta (kit infrastructure — universal-metadata enforcement)
- **Constrained by:** ROADMAP F0.12; `docs/HUMAN-AI-OWNERSHIP.md` §"`ai_assistance_allowed` — value semantics" (the contract: `restricted` requires non-empty `ai_assistance_used`); existing `tools/lint-frontmatter.py` (extension target — must mirror its style and exit-code convention).

> **Spec contract.** Extends `tools/lint-frontmatter.py` with one new rule: `ai_assistance_allowed: restricted` ⇒ `ai_assistance_used:` non-empty list. Mirrors the existing `human_approval_required: true ⇒ human_owned_decisions: non-empty` rule in shape and error format.

## Objective

Add a single conditional check to `tools/lint-frontmatter.py` and four tests. When `ai_assistance_allowed: restricted` appears in an artifact's frontmatter, the same artifact must declare at least one item in `ai_assistance_used:`. The linter emits a clean error message on violation and exits 1.

## Why now

`HUMAN-AI-OWNERSHIP.md` already names this rule: "Only the specific activities listed in the same artifact's `ai_assistance_used:` field. The `ai_assistance_used:` list must be non-empty." Today the rule is documentary; nothing enforces it. F0.12 closes that gap before the kit accumulates compliance-sensitive artifacts under regulated domains. It's also the smallest possible extension to a known-working linter — high leverage, low cost.

## Inputs and outputs

**Inputs.** Same as the existing linter: paths to markdown files (or `--all` to walk PHASE_DIRS). Reads frontmatter via `scripts.lib.frontmatter`.

**Outputs.**
- New error message format (exactly mirroring the human-approval-required rule):
  ```
  lint-frontmatter: <path>: ai_assistance_allowed: restricted requires ai_assistance_used: list to be non-empty
  ```
- Exit code unchanged: 0 if all rules pass; 1 if any rule (existing or new) is violated.

## Boundaries

### Always do
- Mirror the existing `human_approval_required` rule's **structural shape**: same conditional pattern (`fm.get(...) == <value>`), same `errors.append(f"{path}: ...")` shape, same placement convention (immediately after the previous policy rule).
- **Strengthen the emptiness check** beyond the existing rule's: also reject non-list types (scalar string, dict, int) — author writes `ai_assistance_used: "drafted prose"` (a single string) is a common authoring mistake that the spec must catch. The corrected check is `not aiu or not isinstance(aiu, list) or len(aiu) == 0`. The existing `human_owned_decisions` check has the same latent bug; surface that as a deferred finding (Task 5), not a fix in this PR.
- Use the exact lowercase string `"restricted"` for the trigger value (matches HUMAN-AI-OWNERSHIP.md's vocabulary). Case-sensitive match by design — author typos like `Restricted` won't be caught; the enum-membership rule (future, not this spec) will catch those.

### Ask first
- Validating the **content** of `ai_assistance_used:` items (e.g., requiring a verb). Out of scope.
- Validating that `ai_assistance_allowed` is one of {`true`, `restricted`, `not-allowed`} — that's a separate enum-membership rule and not part of F0.12's surface.
- Back-fitting the corrected emptiness check (`not isinstance(aiu, list)`) to the existing `human_approval_required` rule. Out of scope for F0.12; logged as a defer in Task 5.

### Never do
- Walk `docs/specs/`. Specs are exempt per F0.11.
- Touch the existing `human_approval_required` rule's logic.
- Add a new dependency.

## Verification mode

- **TDD.** Two new fixtures and four new tests drive the implementation. The tests live in `scripts/tests/test_lint_frontmatter.py` (or sibling — see Task 1).

## Contract tests

Tests added to the linter's test suite. Implementation file location resolved in Task 1.

- `test_restricted_without_ai_assistance_used_fails` — fixture has `ai_assistance_allowed: restricted` and omits `ai_assistance_used`; linter exits 1; stderr contains the new error message.
- `test_restricted_with_empty_ai_assistance_used_fails` — fixture has `ai_assistance_allowed: restricted` and `ai_assistance_used: []`; linter exits 1; stderr contains the new error message.
- `test_restricted_with_scalar_string_ai_assistance_used_fails` — fixture has `ai_assistance_allowed: restricted` and `ai_assistance_used: "drafted prose"` (a string, not a list); linter exits 1; stderr contains the new error message. Closes the latent "non-list type" gap.
- `test_restricted_with_nonempty_list_ai_assistance_used_passes` — fixture has `ai_assistance_allowed: restricted` and `ai_assistance_used: ["drafted prose"]`; linter exits 0 (no error from this rule).
- `test_not_restricted_with_empty_ai_assistance_used_passes` — fixture has `ai_assistance_allowed: true` (YAML boolean) and no `ai_assistance_used`; linter exits 0 (rule does not fire because `True != "restricted"`).

## Non-goals

- Enumerating the legal values of `ai_assistance_allowed`. (Future rule, not this spec.)
- Adding a corresponding rule for `ai_assistance_allowed: not-allowed`. The HUMAN-AI-OWNERSHIP doc doesn't require a non-empty `ai_assistance_used:` in that case (it forbids AI content; the field may legitimately be empty).
- **Flagging `ai_assistance_allowed: not-allowed` with non-empty `ai_assistance_used:`.** This is internally contradictory (the field says AI helped; the policy says AI was forbidden) but out of scope for F0.12. Deferred to a future enum-and-consistency rule.
- Adjusting `PHASE_DIRS`.
- Adding tests for the existing rules (out of scope; covered by their original specs).
- Fixing the latent non-list-type bug in the existing `human_approval_required` rule. Recorded as a deferred finding in Task 5.

## Open questions

1. **Does `scripts/tests/test_lint_frontmatter.py` exist?** If not, what's the closest sibling test pattern to follow? Lean: follow the test pattern from F1.4/F1.5 audit scripts (`scripts/tests/test_audit_*.py`) — subprocess invocation against fixture dirs. _Resolved by:_ implementer, in Task 1.

2. **Where do the test fixtures live?** Lean: `scripts/tests/fixtures/lint-frontmatter/restricted-ok/`, `.../restricted-missing/`, `.../restricted-empty/`, `.../restricted-scalar-string/`, `.../true-no-used/`. _Resolved here._

3. **Case sensitivity of the `"restricted"` match.** A typo like `Restricted` or `RESTRICTED` will silently skip the rule. _Resolved here: case-sensitive lowercase match by design._ HUMAN-AI-OWNERSHIP.md specifies the vocabulary; the future enum-membership rule (out of scope for F0.12) will catch typos at the value-set boundary.

4. **Parser type guarantees.** `scripts.lib.frontmatter` must return `True` (Python bool) for YAML `true` and `"restricted"` (Python str) for YAML `restricted`. Task 2 includes an explicit assertion verifying both fixture types parse to the expected Python types — if the parser quotes booleans or coerces strings, the spec's logic breaks.

## Acceptance criteria

- [ ] `tools/lint-frontmatter.py` has the new conditional immediately after the existing human-approval-required block, using the strengthened check `not aiu or not isinstance(aiu, list) or len(aiu) == 0`.
- [ ] Five contract tests are in place and pass.
- [ ] Existing tests still pass (no regression).
- [ ] `bash tools/pre-pr.sh` exits 0.
- [ ] `python3 tools/lint-frontmatter.py --all` exits 0 against the current kit (no shipped artifact violates the new rule).
- [ ] ROADMAP.md F0.12 marked checked with `Shipped: 2026-05-21`.
- [ ] INVENTORY.md `tools/lint-frontmatter.py` row's "Rules" cell mentions the new check.
- [ ] Latent non-list-type bug in the existing `human_approval_required` check surfaced as ROADMAP F0.14 (`lint-frontmatter-non-list-retrofit`). `notes/deferred-findings.md` holds the local working detail (gitignored per kit convention).

## Cross-references

- **Consumed by:** `tools/pre-pr.sh`, `.github/workflows/lint.yml`.
- **Consumes:** `scripts.lib.frontmatter` (unchanged).
- **Frontmatter fields owned:** `ai_assistance_allowed`, `ai_assistance_used` (read-only — the linter validates the relationship between them).
- **Ontology object types touched:** none (kit infrastructure).
