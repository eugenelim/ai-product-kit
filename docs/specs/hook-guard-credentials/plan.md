# Plan: hook-guard-credentials

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** approved

## Approach

Single-file Python entry point at `scripts/guard-credentials.py`. Compiled regex+category list at module load. All paths normalized through `expanduser` + `normpath` before matching. Tool dispatch on `tool_name`:

- `Bash` → `shlex.split(command)`; normalize and check each token against `BLOCKED_PATTERNS`. On `shlex` error, fall back to raw regex sweep on the command string (no tokenization, but patterns still match).
- `Write` | `Edit` | `MultiEdit` | `Read` → normalize and check `tool_input.file_path` against `BLOCKED_PATTERNS`.

A block triggers a JSON `{"decision":"block","reason":"guard-credentials: <category> match; refusing <tool_name>"}` on stdout, exit 2. The `category` is a coarse label from the spec table — never the matched string.

Tests construct payloads in-memory; no filesystem access required for the path checks (tests use synthetic paths like `/tmp/test-only/.ssh/id_rsa` that match the pattern but aren't real cred locations).

## Constraints

- Python stdlib only.
- ≤ 250 LOC.
- ≤ 20ms wall time per invocation (fires on every Bash and every Read/Write/Edit/MultiEdit).
- The block reason MUST NOT echo the raw matched path or command — categorical label only.
- Top-level try/except → exit 2 **with the well-formed `{"decision":"block","reason":"...internal error..."}` JSON payload on stdout**. Silent exit 2 (no JSON) would fail open — Claude Code's protocol requires the JSON on the block path. Fail safe means produce the right JSON, not "produce no JSON."
- **Depends on:** F0.10 must ship before VERIFY runs.

## Tasks

### Task 1: Pattern table + category labels + normalization

- **Depends on:** none.
- **Tests:**
  - `test_block_reason_does_not_echo_matched_text_verbatim`
  - `test_blocks_bash_traversal_path_to_ssh` (proves normalization works end-to-end)
- **Approach:**
  - Module-level `BLOCKED_PATTERNS: list[tuple[re.Pattern, str]]` — patterns paired with category labels per the spec table (single source of truth in spec).
  - `normalize(p: str) -> str`: `os.path.normpath(os.path.expanduser(p))`.
  - `match_category(s: str) -> str | None`: applies patterns to `normalize(s)`.
- **Done when:** 2 tests pass.

### Task 2: Bash dispatch

- **Depends on:** Task 1.
- **Tests:**
  - `test_blocks_bash_cat_of_ssh_private_key`
  - `test_blocks_bash_with_relative_ssh_path`
  - `test_blocks_bash_referencing_pem_file`
  - `test_blocks_bash_redirect_into_credentials_path`
  - `test_allows_bash_unrelated_command`
  - `test_malformed_bash_quoting_falls_back_to_raw_regex`
- **Approach:**
  - `check_bash(command: str) -> str | None` returns the matched category or None.
  - Try `shlex.split`; on `ValueError`, raw-string fallback.
- **Done when:** 6 tests pass.

### Task 3: Write/Edit/MultiEdit/Read dispatch

- **Depends on:** Task 1.
- **Tests:**
  - `test_blocks_write_to_dot_env`
  - `test_blocks_write_to_dot_env_dot_local`
  - `test_allows_write_to_dot_env_dot_example`
  - `test_allows_write_to_dot_env_dot_sample`
  - `test_blocks_write_to_kube_config`
  - `test_blocks_read_of_npmrc`
  - `test_blocks_read_of_pypirc`
  - `test_blocks_read_of_netrc`
  - `test_blocks_read_of_credentials_json`
  - `test_blocks_multiedit_to_credential_path`
  - `test_allows_write_to_normal_file`
  - `test_allows_read_of_kit_artifact`
- **Approach:**
  - `check_path(path: str) -> str | None`.
  - Applied for `Write`, `Edit`, `MultiEdit`, `Read` tool names uniformly.
- **Done when:** 12 tests pass.

### Task 4: Entry point + dispatch + fail-safe path

- **Depends on:** Tasks 2, 3.
- **Tests:**
  - `test_path_outside_patterns_passes_through`
  - `test_internal_error_produces_valid_block_json`
  - Subprocess test on one block and one allow case.
- **Approach:**
  - `if __name__ == "__main__":` reads stdin, dispatches on tool_name, emits JSON + exit 2 on block, exit 0 otherwise.
  - Top-level try/except: any exception → write `json.dumps({"decision":"block","reason":"guard-credentials: internal error; refusing as a precaution"})` to stdout AND exit 2. The JSON must always accompany a non-zero exit on this hook — Claude Code's protocol expects it for the block to take effect.
- **Done when:** subprocess tests + 2 contract tests pass.

### Task 5: Hook doc

- **Depends on:** Task 4.
- **Tests:** `bash tools/lint-hook.sh .claude/hooks/guard-credentials.md` exits 0.
- **Approach:** sections: What it does, Why this matters (safety boundary, no model-side override), Patterns (the full list), Configuration (PreToolUse matchers Bash, Write, Edit, Read), Related.
- **Done when:** lint passes.

### Task 6: CAPTURE

- **Depends on:** Task 5.
- **Approach:**
  - `AGENTS.md` — update the "Don't touch `~/.ssh`..." line to drop the "(planned)" qualifier (if any) and name the hook script.
  - `.claude/CLAUDE.md` — same.
  - `docs/INVENTORY.md` — new row.
  - `ROADMAP.md` — check off F2.8.
- **Done when:** edits land.

## Rollout

- F2.6 wires the matcher: PreToolUse with `Bash|Write|Edit|MultiEdit|Read`.
- **Pre-F2.6 standalone wiring:** for manual validation before F2.6 ships, add the PreToolUse entry directly to `.claude/settings.json` (or `.claude/settings.local.json` for personal use) with a comment marking the entry provisional. F2.6 will consolidate.
- After ship, every credential-touching tool call gets blocked — including by the model itself when scaffolding test fixtures. Tests use *synthetic* paths (`/tmp/test-only/.ssh/id_rsa`) that match the pattern but aren't real cred locations.

## Risks

- **False positives in Bash.** A command like `echo "see .env.example for config"` triggers a block. Mitigation: spec adopts conservative-block as policy. The cost is a transparent error; the alternative is silent secret exposure.
- **Categorical reason instead of exact path.** If users find the block hard to debug because the reason is vague, future iteration can widen the message — but only via spec change, since echoing paths is a known risk.
- **Self-block during testing.** Writing fixture paths in tests like `/tmp/.ssh/id_rsa` would be blocked if the hook ran during test development. Mitigation: tests construct payload dicts and call the check functions directly — they never invoke the hook via the real tool layer.

## Changelog

- 2026-05-21: Initial plan.
- 2026-05-21: Addressed adversarial review (11 findings). Added MultiEdit to all matchers and contract tests. Fail-safe path now emits well-formed block JSON to stdout (was silently exiting 2 — would fail open in Claude Code's protocol). Added `~/.kube/config`, `~/.npmrc`, `~/.pypirc`, `~/.netrc` to pattern table with category labels. Narrowed `.env*` regex to known suffixes only — `.env.example` and `.env.sample` are explicitly allowed (their names signal "documentation"). Added path normalization (`expanduser` + `normpath`) for traversal-path coverage. Documented `*.pub` blocking as deliberate policy. Added `eval $VAR` and GPG-key-ID and Windows-paths as explicit non-goals. Added F0.10 dependency and standalone-wiring note for pre-F2.6 manual use.
- 2026-05-21: **Shipped.** `scripts/guard-credentials.py` (165 LOC, stdlib only) + `scripts/tests/test_guard_credentials.py` (22 contract tests + 2 subprocess sanity tests, all passing) + `.claude/hooks/guard-credentials.md`. `tools/lint-hook.sh` and `tools/pre-pr.sh` both exit 0. Implementation deviations from plan: (a) `check_bash` also runs a `match_category` over the raw command after tokenization as a belt-and-braces measure — does not weaken the contract, only strengthens it; (b) test count is 24 total (22 contract + 2 subprocess) rather than the spec's "20" — additional tests cover `MultiEdit` and subprocess exit-code sanity, both required by the EXECUTE prompt.
