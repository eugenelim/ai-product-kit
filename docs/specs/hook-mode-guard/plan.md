# Plan: hook-mode-guard

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** approved

## Approach

Single-file Python entry point at `scripts/mode-guard.py`. The script dispatches on the hook event and runs one of three paths:

- **SessionStart:** read mode → emit `hookSpecificOutput.additionalContext` JSON.
- **UserPromptExpansion** (user typed `/wardley-map`): read mode → check if `command_name` is in the wrong-mode list → block (exit 0 + JSON) or allow.
- **PreToolUse on Skill** (model invoked Skill tool): read mode → check if `tool_input.skill_name` is in the wrong-mode list → block (exit 2 + JSON) or allow.

Event discrimination: read `hook_event_name` first; if absent or unrecognized, fall back to `tool_name == "Skill"`. Anything else exits 0 silently.

A common helper `read_mode() -> str | None` parses `.claude/CLAUDE.md` with strict regex `^mode:\s*(greenfield|enterprise)\s*$` (multiline, `.strip()` to handle CRLF).

Tests are in-memory: compose payloads matching the three event shapes, point the helper at a temp `.claude/CLAUDE.md` via a `claudemd_path` parameter.

## Constraints

- Python stdlib only. No `scripts.lib.frontmatter` needed (no YAML parsing — just a regex line scan).
- ≤ 200 LOC.
- Top-level try/except → exit 0 (degrade safely).
- The SessionStart context block is short — ≤ 5 lines of injected text — so it doesn't bloat the per-session prompt.

## Tasks

### Task 0: Resolved — payload shape captured from docs

Anthropic publishes the schema at https://code.claude.com/docs/en/hooks. Findings in `notes/payload-shape.md`. Key result: slash commands flow through two distinct events (`UserPromptExpansion` + `PreToolUse(Skill)`), not a single `SlashCommand` tool. Spec rewritten 2026-05-21 to reflect this.

### Task 1: `read_mode()` helper

- **Depends on:** none.
- **Tests:**
  - `test_reads_greenfield_mode_from_claudemd`
  - `test_reads_enterprise_mode_from_claudemd`
  - `test_returns_none_when_mode_undeclared`
  - `test_returns_none_when_mode_unknown_value`
  - `test_returns_none_when_claudemd_missing`
  - `test_handles_crlf_line_endings`
- **Approach:**
  - `def read_mode(claudemd_path: Path) -> str | None`. Uses `re.compile(r'^mode:\s*(greenfield|enterprise)\s*$', re.MULTILINE)` (strict-anchor; only the two known values; trailing `$` rejects `enterprise-lite`).
  - `.strip()` the captured group to handle CRLF.
- **Done when:** 6 tests pass.

### Task 2: SessionStart path

- **Depends on:** Task 1.
- **Tests:**
  - `test_session_start_emits_active_mode_context`
  - `test_session_start_warns_on_missing_mode`
- **Approach:**
  - `session_start(mode: str | None) -> tuple[int, str, str]` returns `(exit_code, stdout_json, stderr)`.
  - On valid mode: emit `{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"<block>"}}`.
  - On None: exit 0 with stderr warning (no JSON block).
- **Done when:** 2 tests pass.

### Task 3: UserPromptExpansion path (user-typed slash command)

- **Depends on:** Task 1.
- **Tests:**
  - `test_upe_blocks_wrong_mode_command`
  - `test_upe_allows_correct_mode_command`
  - `test_upe_allows_shared_command_in_any_mode`
  - `test_upe_emits_stderr_notice_when_mode_undeclared`
- **Approach:**
  - `handle_upe(mode: str | None, payload: dict) -> tuple[int, str, str]`.
  - Extract command name from top-level `payload["command_name"]`.
  - Compare against `BLOCKED_BY_MODE[mode]`.
  - Block → exit **0** + stdout `{"decision":"block","reason":"<reason>","hookSpecificOutput":{"hookEventName":"UserPromptExpansion"}}`.
  - Allow → exit 0, empty stdout.
  - mode is None → exit 0 + stderr notice.
- **Done when:** 4 tests pass.

### Task 4: PreToolUse(Skill) path (model-invoked Skill tool)

- **Depends on:** Task 1.
- **Tests:**
  - `test_pretooluse_skill_blocks_wrong_mode`
  - `test_pretooluse_skill_allows_correct_mode`
  - `test_pretooluse_skill_allows_shared_skill`
  - `test_pretooluse_ignores_non_skill_tool`
  - `test_pretooluse_skill_emits_stderr_notice_when_mode_undeclared`
  - `test_pretooluse_skill_emits_stderr_notice_when_mode_unknown_value`
- **Approach:**
  - `handle_pretooluse_skill(mode: str | None, payload: dict) -> tuple[int, str, str]`.
  - Extract command name from `payload["tool_input"]["skill_name"]`.
  - Compare against `BLOCKED_BY_MODE[mode]`.
  - Block → exit **2** + stdout `{"decision":"block","reason":"<reason>"}`.
  - Allow / non-Skill tool → exit 0.
  - mode is None → exit 0 + stderr notice.
- **Done when:** 6 tests pass.

### Task 5: Event dispatch + entry point

- **Depends on:** Tasks 2, 3, 4.
- **Tests:** Subprocess smoke tests: one per event (SessionStart silent / SessionStart with mode / UserPromptExpansion allow / UserPromptExpansion block / PreToolUse(Skill) allow / PreToolUse(Skill) block).
- **Approach:**
  - Read stdin JSON.
  - Dispatch: if `payload.get("hook_event_name") == "UserPromptExpansion"` → `handle_upe`; elif `payload.get("hook_event_name") == "SessionStart"` (or absence of `tool_name`) → `session_start`; elif `payload.get("tool_name") == "Skill"` → `handle_pretooluse_skill`; else exit 0 silently.
- **Done when:** subprocess tests pass.

### Task 6: Hook doc

- **Depends on:** Tasks 1–5.
- **Tests:** `bash tools/lint-hook.sh .claude/hooks/mode-guard.md` exits 0.
- **Approach:** sections: What it does, Why this matters (mode is project-scoped intentionally), Configuration (the wiring for all three events: SessionStart + UserPromptExpansion + PreToolUse(Skill)), Override (no override — switch the mode in `.claude/CLAUDE.md`), Related.
- **Done when:** lint passes.

### Task 7: Update `.claude/CLAUDE.md`

- **Depends on:** Task 6.
- **Tests:** none (doc-only).
- **Approach:** strip the `*(planned — [ROADMAP F2.4](...); not yet enforced)*` qualifier on the mode-guard description. Keep the mode value as `mode: greenfield`.
- **Done when:** the edit lands.

### Task 8: CAPTURE

- **Depends on:** Tasks 1–7.
- **Approach:**
  - `docs/INVENTORY.md` — new row for the hook.
  - `ROADMAP.md` — check off F2.4.
- **Done when:** edits land.

## Rollout

- F2.6 wires three matchers: SessionStart, UserPromptExpansion (one entry per blocked command per mode, or matcher-less + script-side dispatch — F2.6 decides), and PreToolUse on `Skill`.
- After ship, the user can switch mode by editing `.claude/CLAUDE.md` — no other action needed; the hook re-reads on each invocation.

## Risks

- **`.claude/CLAUDE.md` mode-line collision.** Currently `mode:` lives inside a fenced code block. If someone later writes the word elsewhere (e.g., "switch the mode: enterprise to greenfield"), the regex's first-match-only behavior catches the legitimate one — the strict anchors `(greenfield|enterprise)\s*$` reject any inline variant. Risk is low.
- **Event-coverage drift.** If Anthropic introduces a new way for slash commands to expand (a third event), the hook won't cover it. Mitigation: the cross-reference in `notes/payload-shape.md` links the doc URL; review on Claude Code minor-version updates.

## Changelog

- 2026-05-21: Initial plan.
- 2026-05-21: Addressed adversarial review (10 findings). Open Question 1 (slash-command payload shape) elevated to Task 0 PLAN-phase blocker.
- 2026-05-21: Task 0 resolved — Anthropic's hook docs (https://code.claude.com/docs/en/hooks) settle the shape. Spec rewritten: there is no `SlashCommand` tool. Slash commands flow through `UserPromptExpansion` (user-typed; field: top-level `command_name`; block via exit 0 + JSON) and `PreToolUse` on `Skill` (model-invoked; field: `tool_input.skill_name`; block via exit 2 + JSON). The hook now wires three events: SessionStart + UserPromptExpansion + PreToolUse(Skill). Findings captured in `notes/payload-shape.md`. State.json `plan_review_status` can move to approved.
- 2026-05-21: **Shipped.** `scripts/mode-guard.py` + `scripts/tests/test_mode_guard.py` + `.claude/hooks/mode-guard.md` landed. `python3 -m unittest scripts.tests.test_mode_guard` passes 18 tests (6 helper + 2 SessionStart + 4 UPE + 6 PreToolUse(Skill); the acceptance-criteria summary said "17 total / 5 PreToolUse" but the contract-tests list enumerates 6 in PreToolUse(Skill) — implementation matches the enumerated list). `tools/lint-hook.sh .claude/hooks/mode-guard.md` and `tools/pre-pr.sh` both exit 0. `.claude/CLAUDE.md` planned-qualifier dropped. ROADMAP F2.4 checked off.
