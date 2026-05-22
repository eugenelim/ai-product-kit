# Spec: hook-mode-guard

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** hook (SessionStart + UserPromptExpansion + PreToolUse on `Skill` tool)
- **Serves kit phase:** Meta (mode guard between greenfield and enterprise modes)
- **Constrained by:** `.claude/CLAUDE.md` `mode:` declaration (the source of truth); `ROADMAP.md` F2.4 description (names the wrong-mode commands per side); F0.10

> **Spec contract.** Defines `scripts/mode-guard.py` and `.claude/hooks/mode-guard.md`. Reads `mode: greenfield | enterprise` from `.claude/CLAUDE.md` and (a) on SessionStart, surfaces the active mode + the list of blocked commands as context; (b) on PreToolUse for `SlashCommand` calls, blocks invocations of wrong-mode commands with a clear reason.

## Objective

Build a three-event hook that reads the project's `mode:` and enforces blocked-command lists per mode:

- **SessionStart** — inject a one-block system-reminder via `hookSpecificOutput.additionalContext` so the model knows the active mode and the blocked-list without re-reading `.claude/CLAUDE.md`.
- **UserPromptExpansion** — fires when the user types `/wardley-map` directly. Block protocol: exit 0 + `{"decision":"block","reason":"..."}` on stdout.
- **PreToolUse on `Skill` tool** — fires when the model invokes a skill via the Skill tool. Block protocol: exit 2 + same JSON on stdout.

Mode → blocked list:

- **greenfield mode** — blocks `wardley-map`, `internal-jtbd-interview`, `value-chain-evolution`.
- **enterprise mode** — blocks `competitive-research`, `market-scan`, `jtbd-analogues`.

Both modes share `strategy-refresh`, `strategic-intent`, `audit-portfolio-coherence`, `cadence-check`, `phase-guide` (never blocked).

The hook intentionally wires both `UserPromptExpansion` and `PreToolUse(Skill)` because Claude Code documents them as the two distinct paths a slash command can take (user-typed vs model-invoked). Wiring only one leaves a silent evasion gap.

## Why now

`.claude/CLAUDE.md` already documents the rule prose. Until this hook ships, mode is documentary — divergence is discovered only when the wrong-mode command runs to completion and produces drift artifacts. The hook converts a soft convention into a write-time gate.

No upstream dependency in the F1 chain — this hook reads `.claude/CLAUDE.md` directly. F0.10 ships the doc linter prerequisite.

**Payload shape resolved 2026-05-21** via Anthropic's published hook docs (https://code.claude.com/docs/en/hooks). See `notes/payload-shape.md` for the captured schemas. Two events, two distinct field paths, two block-protocol variants. The "SlashCommand" tool name the original draft assumed does not exist; the docs explicitly route slash commands through `UserPromptExpansion` (user-typed path) and `PreToolUse` on `Skill` (model-invoked path).

## Inputs and outputs

**Inputs.**
- Disk: `.claude/CLAUDE.md`. The hook greps the `mode:` block via `re.compile(r'^mode:\s*(greenfield|enterprise)\s*$', re.MULTILINE)`.
- Stdin for `UserPromptExpansion`: `{"hook_event_name":"UserPromptExpansion","expansion_type":"slash_command","command_name":"<name>","command_args":"<args>","prompt":"/<name> <args>",...}`. Read the command name from top-level `command_name`.
- Stdin for `PreToolUse` on Skill: `{"tool_name":"Skill","tool_input":{"skill_name":"<name>","skill_input":"<args>"},...}`. Read the command name from `tool_input.skill_name`.
- Stdin for `SessionStart`: empty payload.

The script discriminates events by checking `hook_event_name` first (UserPromptExpansion / SessionStart paths set it), then falls back to `tool_name == "Skill"` for the PreToolUse path. Unknown events exit 0 silently.

**Outputs.**
- **SessionStart:** stdout JSON `{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"<one-block reminder>"}}`. Exit 0.
- **UserPromptExpansion on a wrong-mode command:** stdout JSON
  ```json
  {"decision":"block","reason":"mode-guard: /<cmd> is blocked in <mode> mode. Use <suggested-allowed-command> instead, or change mode: to <other-mode> in .claude/CLAUDE.md.","hookSpecificOutput":{"hookEventName":"UserPromptExpansion"}}
  ```
  Exit **0** (UserPromptExpansion uses the `decision` field on stdout JSON; non-zero exits are reserved for non-blocking errors).
- **PreToolUse on Skill with a wrong-mode skill name:** stdout JSON `{"decision":"block","reason":"<same format>"}`. Exit **2** (PreToolUse uses non-zero exit + JSON for blocks).
- Either path on an allowed command: exit 0 silently.
- PreToolUse on a non-Skill tool: exit 0 silently. (The Skill matcher in `.claude/settings.json` filters this at the harness level too, but the script is defensive.)
- If `.claude/CLAUDE.md` is missing or doesn't declare `mode:`:
  - SessionStart: emit stderr warning; no `additionalContext` JSON; exit 0.
  - UserPromptExpansion / PreToolUse(Skill) on a slash-command path: exit 0 + stderr notice `mode-guard: mode undeclared in .claude/CLAUDE.md — enforcement inactive`. At-the-moment visibility.
- If `mode:` is declared with an unknown value (e.g., `mode: enterprise-lite`), treat identically to "undeclared mode." `read_mode()` returns only `"greenfield"` or `"enterprise"`; anything else is None.

**Mode → blocked-commands map (single source of truth):**

```python
BLOCKED_BY_MODE = {
    "greenfield": ["wardley-map", "internal-jtbd-interview", "value-chain-evolution"],
    "enterprise": ["competitive-research", "market-scan", "jtbd-analogues"],
}
SHARED = {"strategy-refresh", "strategic-intent", "audit-portfolio-coherence", "cadence-check", "phase-guide"}
# `phase-guide` added to SHARED explicitly. The implicit "anything not in BLOCKED is allowed" rule
# already permits it, but listing it shuts down the failure mode of someone accidentally adding it
# to a blocked list. Comment in the script will name the implicit-allow rule too.
```

**Repo-root resolution:** the script reads `.claude/CLAUDE.md` from the directory found by ascending `__file__`'s parent chain until a `.claude/` directory is found, or via `CLAUDE_WORKSPACE` env var if set.

## Boundaries

### Always do
- Read `mode:` from `.claude/CLAUDE.md` via the regex `re.compile(r'^mode:\s*(greenfield|enterprise)\s*$', re.MULTILINE)`. Strict-anchor: only `greenfield` or `enterprise` match; other values return None (unknown-mode path). `.strip()` the captured group to handle CRLF line endings.
- Discriminate events: `hook_event_name == "UserPromptExpansion"` → UserPromptExpansion path; `hook_event_name == "SessionStart"` (or absence of `tool_name`) → SessionStart path; `tool_name == "Skill"` → PreToolUse(Skill) path; anything else → exit 0 silently.
- Inject the SessionStart context block via the `hookSpecificOutput.additionalContext` channel.
- **Degrade safely** is operationally defined: on any unhandled exception or unreadable input, write a one-line stderr message and exit 0. Never exit non-zero except when intentionally blocking via the PreToolUse(Skill) path.

### Ask first
- Adding commands to either blocked list. Default: only the six the ROADMAP names.
- Changing the source-of-truth location (e.g., reading mode from a separate `.kit-mode` file). Default: `.claude/CLAUDE.md` is the source.

### Never do
- Modify `.claude/CLAUDE.md`.
- Block any non-slash tool.
- Block during the SessionStart event (SessionStart is informational only — the wiring deliberately separates the two events).
- Persist any state to disk. Mode is re-read each invocation.

## Verification mode

- **TDD.** Unit tests under `scripts/tests/test_mode_guard.py`.
- **Goal-based check.** `tools/lint-hook.sh .claude/hooks/mode-guard.md` exits 0.
- **Manual gesture.** Set `.claude/CLAUDE.md` `mode: greenfield`, attempt `/wardley-map` in a fresh session → blocked with reason. Switch to `enterprise`, retry `/wardley-map` → succeeds; `/market-scan` is now blocked.

## Contract tests

### `read_mode()` helper
- `test_reads_greenfield_mode_from_claudemd` — `.claude/CLAUDE.md` says `mode: greenfield` → `"greenfield"`.
- `test_reads_enterprise_mode_from_claudemd` — `mode: enterprise` → `"enterprise"`.
- `test_returns_none_when_mode_undeclared` — None.
- `test_returns_none_when_mode_unknown_value` — `mode: enterprise-lite` → None (strict-anchor regex rejects).
- `test_returns_none_when_claudemd_missing` — None, no exception.
- `test_handles_crlf_line_endings` — CRLF file still parses.

### SessionStart event
- `test_session_start_emits_active_mode_context` — SessionStart → stdout JSON includes the active mode and the blocked-list.
- `test_session_start_warns_on_missing_mode` — SessionStart with no mode declaration → exit 0, stderr warning.

### UserPromptExpansion event (user typing `/wardley-map`)
- `test_upe_blocks_wrong_mode_command` — `mode: greenfield`, `command_name: "wardley-map"` → **exit 0** + stdout `{"decision":"block","reason":"mode-guard: /wardley-map is blocked in greenfield mode. Use /competitive-research instead, or change mode: to enterprise in .claude/CLAUDE.md.","hookSpecificOutput":{"hookEventName":"UserPromptExpansion"}}`.
- `test_upe_allows_correct_mode_command` — `mode: greenfield`, `command_name: "competitive-research"` → exit 0, no JSON block.
- `test_upe_allows_shared_command_in_any_mode` — either mode, `command_name: "strategy-refresh"` or `"phase-guide"` → exit 0.
- `test_upe_emits_stderr_notice_when_mode_undeclared` — no `mode:`, `command_name: "wardley-map"` → exit 0 + stderr notice.

### PreToolUse on Skill event (model invoking Skill)
- `test_pretooluse_skill_blocks_wrong_mode` — `mode: greenfield`, `tool_name: "Skill"`, `tool_input.skill_name: "wardley-map"` → **exit 2** + stdout `{"decision":"block","reason":"..."}`.
- `test_pretooluse_skill_allows_correct_mode` — exit 0 silently.
- `test_pretooluse_skill_allows_shared_skill` — exit 0.
- `test_pretooluse_ignores_non_skill_tool` — `tool_name: "Write"` → exit 0 silently regardless of mode.
- `test_pretooluse_skill_emits_stderr_notice_when_mode_undeclared` — no `mode:`, blocked skill → exit 0 + stderr notice.
- `test_pretooluse_skill_emits_stderr_notice_when_mode_unknown_value` — `mode: enterprise-lite`, blocked skill → exit 0 + stderr notice.

## Non-goals

- Mode switching from inside the hook.
- Validating that the project actually *is* greenfield vs enterprise (the mode is declarative).
- Enforcing the mode at any boundary besides slash-command invocation (no `Write|Edit` blocks based on mode).
- Adding any mode beyond the two named in CLAUDE.md.
- **Catching slash commands invoked via `Bash` (e.g., `claude /some-command` as a shell call).** Neither event covers this path; the model would have to do something unusual to evade via Bash. Accepted limitation; if it becomes an evasion path in practice, surface as a follow-up spec.

## Open questions

(Question 1 — slash-command payload shape — is no longer open; per Why now §pre-EXECUTE blocker, this MUST be resolved before plan-review can transition to approved. Question 2 below remains open as a known-limitation defer.)

1. **SessionStart vs UserPromptSubmit for the surfacing.** SessionStart fires once per session; UserPromptSubmit fires every prompt. SessionStart is cheaper but the context block can be elided after autocompact. Decision: SessionStart only. The PreToolUse path provides at-the-moment visibility for the wrong-mode block, which is the more important UX channel. If post-compact drift becomes a problem in practice, add UserPromptSubmit as a follow-up spec.

## Acceptance criteria

- [ ] `scripts/mode-guard.py` exists, stdlib only, ≤ 200 LOC.
- [ ] `scripts/tests/test_mode_guard.py` exists; all 17 contract tests pass (6 helper + 2 SessionStart + 4 UPE + 5 PreToolUse(Skill)).
- [ ] `.claude/hooks/mode-guard.md` exists; `tools/lint-hook.sh` exits 0 against it.
- [ ] `python3 -m unittest scripts.tests.test_mode_guard` exits 0.
- [ ] `.claude/CLAUDE.md` updated: drop the "*(planned)*" qualifier on the `mode-guard` references.
- [ ] **Manual-gesture verification** uses `/competitive-research` (an enterprise-blocked command that ships today) for the enterprise-mode block test; the greenfield-blocked commands are unbuilt and noted as pending P7.7 / P7.9 / P7.10.
- [ ] PLAN / VERIFY / REVIEW gates exit 0.
- [ ] **Depends on:** F0.10 (`tools/lint-hook.sh`) must ship before VERIFY can run. Payload shape verified 2026-05-21 — see `notes/payload-shape.md`.

## Cross-references

- **Consumed by:** F2.6.
- **Consumes:** `.claude/CLAUDE.md` (read-only).
- **Frontmatter fields owned:** none (reads project-config, not artifact frontmatter).
- **Ontology object types touched:** none directly; affects which Strategy-phase commands the user can invoke.
