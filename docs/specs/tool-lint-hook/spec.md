# Spec: tool-lint-hook

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** script (shell linter)
- **Serves kit phase:** Meta (kit infrastructure — verify gate for hook docs)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md` §3.2 (names `tools/lint-hook.sh` as the per-component-type linter for hooks); existing sibling linters `tools/lint-skill.sh`, `tools/lint-agent.sh`, `tools/lint-command.sh` (shape conventions to mirror); the existing `.claude/hooks/assumption-threshold-lock.md` (the de facto template for what a hook doc looks like)

> **Spec contract.** Defines `tools/lint-hook.sh` — the shape linter for hook documentation files under `.claude/hooks/`. F2.1–F2.5 + F2.8 each ship a hook doc that must lint clean; this script is the gate.

## Objective

Build `tools/lint-hook.sh`: a bash linter that validates one `.claude/hooks/<slug>.md` file against the kit's hook-doc contract. Exits 0 on clean, 1 with errors to stderr on failure. Same shape and exit-code convention as `lint-skill.sh` / `lint-agent.sh` / `lint-command.sh`.

A hook doc is a markdown file (no frontmatter) that documents what a hook does, when it fires, what it blocks, how to override it, and how it's wired into `.claude/settings.json`. The doc is the human-readable contract; the Python (or shell) script next to it in `scripts/` is the enforcement.

## Why now

`.claude/skills/work-loop/SKILL.md` §3.2 names `tools/lint-hook.sh` as the component-specific linter for hooks. Six hooks ship in Foundation 2 (F2.1–F2.5, F2.8) — each produces a `.claude/hooks/<slug>.md` doc. Without this linter, those six docs ship without a shape gate, meaning `tools/pre-pr.sh` and `.github/workflows/lint.yml` can't enforce hook-doc shape. That's exactly the "fix it later" path the work-loop is built to prevent.

F0.10 is also surfaced as a Foundation-0-X defer (D1, work-loop reviewer finding) — this spec discharges that defer.

## Inputs and outputs

**Inputs.**
- One CLI argument: path to a `.claude/hooks/<slug>.md` file.
- Reads the file from disk; no other I/O.

**Outputs.**
- Exit 0: file conforms.
- Exit 1: one or more errors written to stderr, in the format `lint-hook: <path> <error description>`. **Includes the file-not-found case** — matches the sibling convention in `lint-skill.sh:27` and `lint-agent.sh:22`, so `pre-pr.sh`'s `run_linter` wrapper treats it identically to any other lint failure.
- Exit 2: usage error (wrong arg count only).
- Stdout: nothing on success; nothing on failure (errors go to stderr).

A reader of this section should be able to write the call sites — both the `for f in .claude/hooks/*.md` loops in `tools/pre-pr.sh` and `.github/workflows/lint.yml` — without reading the body of this script.

## Boundaries

### Always do
- Exit 0 / 1 / 2 per the contract above.
- Mirror the shape of `lint-skill.sh` (bash, `set -euo pipefail`, `ERRORS` counter, stderr for errors).
- Treat the file as plain markdown — no YAML frontmatter parsing.

### Ask first
- Adding required-section rules beyond the four listed under Contract tests. Default: don't; this is shape-only.
- Adding a soft body-length cap beyond the one specified here. Default: ≤ 250 lines soft warning. (Same mechanism as `lint-skill.sh`'s 400-line cap, but lower threshold — hook docs are intentionally tighter than skill bodies.)

### Never do
- Read or write any file other than the one passed in.
- Take a Python or external-tool dependency. Bash + `grep` + `awk` only.
- Lint the script that the hook doc references (that's the Python script's own test suite).
- Require frontmatter — hook docs deliberately have none (mirroring `.claude/hooks/assumption-threshold-lock.md`).

## Verification mode

- **Goal-based check.** The linter is the verification: it must exit 0 against every existing hook doc and 1 against the broken-fixture hook docs.

## Contract tests

Captured as a small test harness shell script `tools/tests/test-lint-hook.sh` that drives `lint-hook.sh` against fixtures in `tools/tests/fixtures/lint-hook/`.

- `test_passes_on_assumption_threshold_lock_doc` — the existing `.claude/hooks/assumption-threshold-lock.md` exits 0.
- `test_fails_on_missing_h1` — fixture without an H1 heading exits 1; stderr names the missing H1.
- `test_fails_on_missing_what_it_does` — fixture without `## What it does` exits 1.
- `test_fails_on_missing_why_this_matters` — fixture without `## Why this matters` exits 1.
- `test_fails_on_missing_configuration` — fixture without `## Configuration` exits 1.
- `test_fails_on_h1_not_matching_hook_pattern` — fixture whose H1 does not end with " hook" exits 1 (matches the existing convention "# assumption-threshold-lock hook").
- `test_usage_error_on_no_args` — invocation without args exits 2.
- `test_error_on_missing_file` — invocation with a nonexistent path exits **1** (matches `lint-skill.sh` / `lint-agent.sh` convention); stderr names "file not found".
- `test_soft_warns_on_long_body` — fixture > 250 lines exits 0 but emits a WARN line on stderr in the exact format `lint-hook: WARN <path> is <N> lines (soft cap 250)` (mirrors `lint-skill.sh:70`).

Each enforced rule is one line of `grep`-or-`awk` in the linter. Rules:

1. **H1 present and matches `^# .+ hook$`.** Requires a non-empty slug between `# ` and ` hook` (e.g., `# mode-guard hook`). `.*` would permit a literal `# hook` line; `.+` rejects it.
2. **`## What it does` section present.**
3. **`## Why this matters` section present.**
4. **`## Configuration` section present.**
5. **Soft cap:** body > 250 lines emits a WARN on stderr but does not fail.

Rationale for rules 2–4: every hook is judged on (a) what it mechanically does, (b) why that matters in the kit's discipline, (c) how to wire it. Anything else (override, related links, examples) is optional but encouraged.

## Non-goals

- Validating the referenced Python/shell script's behavior (that script has its own tests).
- Parsing or executing the `## Configuration` JSON block (it's documentary).
- Enforcing the presence of `## Override`, `## Related`, or other optional sections.
- Cross-linking to `.claude/settings.json` (the wiring linter — possibly a future audit — is out of scope).
- Linting the `README.md` in `.claude/hooks/`. **Note (behavioral, not a non-goal):** the call-site loops in `tools/pre-pr.sh` and `.github/workflows/lint.yml` skip `README.md` — same convention as the agents/skills loops after the F2 CI fix. The linter itself is content-agnostic; the skip happens at the call site.

## Open questions

1. **Should H1 require the literal " hook" suffix or just a non-empty H1?** Lean: require the suffix. The existing doc uses it (`# assumption-threshold-lock hook`); it's a useful invariant for the index. If a future hook doc doesn't fit the pattern, file an RFC, not a workaround.

2. **Should the linter also forbid YAML frontmatter (since hook docs don't use it)?** Lean: no. Adding frontmatter doesn't break anything; not requiring it is enough.

## Acceptance criteria

- [ ] `tools/lint-hook.sh` exists, executable, bash + grep/awk only, ≤ 100 lines.
- [ ] `tools/tests/test-lint-hook.sh` exists and exercises every contract test.
- [ ] `tools/tests/fixtures/lint-hook/` contains one good fixture + one broken-per-rule fixture.
- [ ] `bash tools/lint-hook.sh .claude/hooks/assumption-threshold-lock.md` exits 0 — verified manually as part of Task 2's "Done when" (the existing doc must pass all four rules against the actual grep patterns).
- [ ] `tools/pre-pr.sh` invokes `lint-hook.sh` on every `.claude/hooks/*.md` (excluding `README.md`); on a clean kit it stays green.
- [ ] `.github/workflows/lint.yml` invokes `lint-hook.sh` in the artifact-linters job (excluding `README.md`).
- [ ] PLAN / VERIFY / REVIEW gates exit 0.

## Cross-references

- **Consumed by:** `tools/pre-pr.sh`, `.github/workflows/lint.yml`, the work-loop SKILL (§3.2). Indirectly consumed by every F2.x spec's verify gate.
- **Consumes:** nothing (stdlib bash + grep/awk).
- **Frontmatter fields owned:** none.
- **Ontology object types touched:** none (kit infrastructure).
