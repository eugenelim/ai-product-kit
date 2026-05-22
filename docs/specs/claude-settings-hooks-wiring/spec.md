# Spec: claude-settings-hooks-wiring

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** project settings (`.claude/settings.json`)
- **Serves kit phase:** Meta (wires the kit's six shipped hooks into Claude Code's tool-use lifecycle)
- **Constrained by:** Claude Code hook protocol (https://code.claude.com/docs/en/hooks); F2.1 / F2.2 / F2.3 / F2.4 / F2.5 / F2.8 (the six hook scripts being wired); `.claude/skills/work-loop/SKILL.md`

> **Spec contract.** Defines `.claude/settings.json` (committed, project-scope). Registers every shipped hook script with Claude Code's harness using the canonical hook-entry schema. Until this ships, the six F2 scripts are inert in real sessions.

## Objective

Build the single `.claude/settings.json` file that wires the six shipped Foundation 2 hooks into Claude Code's lifecycle:

- `check-handover-link` (F2.1) — `PreToolUse` on `Write|Edit|MultiEdit`
- `assumption-threshold-lock` (F2.2) — `PreToolUse` on `Write`
- `ontology-type-check` (F2.3) — `PreToolUse` on `Write|Edit|MultiEdit`
- `mode-guard` (F2.4) — `SessionStart` + `UserPromptExpansion` + `PreToolUse` on `Skill`
- `cadence-nudge` (F2.5) — `SessionStart`
- `guard-credentials` (F2.8) — `PreToolUse` on `Bash|Write|Edit|MultiEdit|Read`

The file uses the **canonical schema** from Claude Code's docs: each event holds an array of matcher entries; each matcher entry has a `hooks` array of typed command objects:

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<tool-pattern>",
        "hooks": [
          {"type": "command", "command": "python3 scripts/<name>.py"}
        ]
      }
    ]
  }
}
```

`SessionStart` entries have no applicable matcher (no tool name in the payload). `UserPromptExpansion` accepts an optional `matcher` matched against `command_name` — `mode-guard` omits it and dispatches internally on `command_name`, which is the simpler design for a hook that already maintains its own blocked-list table.

## Why now

All six hook scripts ship today. The doc promises they're enforced ("Hooks block these" — AGENTS.md, .claude/CLAUDE.md, and each hook doc). Until F2.6 lands, that promise is documentary — the scripts exist but never fire. F2.6 turns the kit's claimed enforcement on.

## Inputs and outputs

**Inputs.**
- Each shipped hook doc's `## Configuration` block (the six in `.claude/hooks/*.md`).
- The Claude Code hook protocol schema (verified against `notes/payload-shape.md` and the published docs).
- Existing `.claude/settings.local.json` (personal, gitignored) — must continue to coexist; F2.6 does NOT modify it.

**Multi-source settings semantics.** Claude Code loads settings in order user → project → local. Per the Claude Code settings schema (`allowedMcpServers`, `deniedMcpServers`, and `allowedHttpHookUrls` all document "Arrays merge across settings sources"), and per the documented hooks-handling, hooks arrays from multiple sources are concatenated per event — not overridden. So `settings.local.json`'s SessionStart hook (the branch-rename) and `settings.json`'s SessionStart hooks (mode-guard + cadence-nudge) all fire on session start. If at runtime that assumption proves wrong (only one source's hooks fire), F2.6 still functions for any session that doesn't have a competing `settings.local.json`; the local-file user can re-add the personal hook to settings.json under their own login.

**Outputs.**
- A new file: `.claude/settings.json` (committed; project-scope).
- Updated hook docs (the 5 with shorthand-schema `## Configuration` blocks): each Configuration block re-rendered in canonical form so the doc matches the wiring exactly.

**The complete wiring** (load-bearing):

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {"type": "command", "command": "python3 scripts/mode-guard.py"},
          {"type": "command", "command": "python3 scripts/cadence-nudge.py"}
        ]
      }
    ],
    "UserPromptExpansion": [
      {
        "hooks": [
          {"type": "command", "command": "python3 scripts/mode-guard.py"}
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit|MultiEdit|Read",
        "hooks": [
          {"type": "command", "command": "python3 scripts/guard-credentials.py"}
        ]
      },
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {"type": "command", "command": "python3 scripts/check-handover-link.py"},
          {"type": "command", "command": "python3 scripts/check-ontology-type.py"}
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {"type": "command", "command": "python3 scripts/check-assumption-threshold.py"}
        ]
      },
      {
        "matcher": "Skill",
        "hooks": [
          {"type": "command", "command": "python3 scripts/mode-guard.py"}
        ]
      }
    ]
  }
}
```

**PreToolUse entry ordering (best-effort, see Risk #3 in plan):**

Anthropic's hook docs do not (as of 2026-05-21) document whether per-event entries fire in declared order or in parallel. The spec assumes declared-order firing and arranges entries accordingly:

1. `guard-credentials` — listed first. Safety boundary; the spec prefers this fire before any other PreToolUse hook in case a Bash command references a credential path.
2. `check-handover-link` + `check-ontology-type` — co-located under one `Write|Edit|MultiEdit` matcher entry (single `matcher` entry with two `hooks` array members). handover-link can block; ontology-type only nudges. Order is commutative under their matcher.
3. `check-assumption-threshold` — narrower `Write` matcher; the script path-filters internally.
4. `mode-guard` (Skill) — only fires when `tool_name == "Skill"`; no overlap with other entries.

If the harness ignores declared order, the wiring is still correct: each script's contract holds independently. The "guard-credentials first" choice is a defensive preference, not a hard dependency.

## Boundaries

### Always do
- Use the **canonical schema**: every event entry contains a `hooks: [{type, command}]` array. No shorthand `{"matcher": ..., "command": ...}` form.
- Use `python3` as the interpreter (matches what each hook doc declares).
- Reference scripts via repo-relative paths (`scripts/<name>.py`), not absolute paths. Claude Code resolves these against `$CLAUDE_PROJECT_DIR` at hook-invocation time — confirmed by the existing `.claude/settings.local.json` SessionStart hook which uses the same env var. If a session is launched from outside the repo, the harness still sets `$CLAUDE_PROJECT_DIR` to the project root.
- Co-locate matchers when multiple hooks share an identical tool-pattern (`check-handover-link` + `check-ontology-type` under `Write|Edit|MultiEdit`). This minimizes file length without losing semantics.
- Validate the file with `jq -e` after every change.

### Ask first
- Adding any hook beyond the six shipped (F2.7 + F2.9 are blocked on their upstream deps).
- Changing the firing order. Default: `guard-credentials` first; the rest are commutative under their matchers.
- Adding `timeout`, `async`, or `if` fields. Default: stdlib defaults are fine.

### Never do
- Modify or read `.claude/settings.local.json`. That's the user's personal scope.
- Add hooks for scripts that don't yet exist on disk.
- Use `matchPaths` (not in the published hook schema as of 2026-05-21).
- Add Claude/Anthropic/AI attribution anywhere in the file or commits.

## Verification mode

- **Goal-based check.** The wiring is the verification: a well-formed `.claude/settings.json` that `jq -e` validates against the documented schema shape; every shipped hook script has a corresponding entry; every entry's `command` resolves to an existing executable file.
- **Schema validation.** A small `tools/tests/test-settings-json.sh` harness runs:
  - `jq -e .hooks .claude/settings.json` succeeds.
  - For every entry, `jq -e '.hooks[] | objects' .claude/settings.json` returns objects with required fields.
  - For every `.command` referenced, the file exists in `scripts/`.
  - No `matchPaths` field appears (it's not in the schema).
- **Manual-gesture test** (documented for the user; not automated): in a fresh Claude Code session against this repo, (a) attempt to `Write` a `delivery/visions/foo.md` without `parent_learning` → blocked by `check-handover-link`. (b) `cat ~/.ssh/id_rsa` → blocked by `guard-credentials`. (c) `/wardley-map` in greenfield mode → blocked by `mode-guard` via `UserPromptExpansion`. (d) New session → `cadence-nudge` injects a one-block reminder if any drift signal fires.

## Contract tests

`tools/tests/test-settings-json.sh` runs these assertions (each a `jq -e` call or path existence check):

- `test_settings_file_exists` — `.claude/settings.json` is a regular file.
- `test_settings_is_valid_json` — `jq -e . .claude/settings.json` succeeds.
- `test_has_session_start_array` — `jq -e '.hooks.SessionStart | type == "array"'`.
- `test_has_user_prompt_expansion_array` — `jq -e '.hooks.UserPromptExpansion | type == "array"'`.
- `test_has_pre_tool_use_array` — `jq -e '.hooks.PreToolUse | type == "array"'`.
- `test_every_entry_uses_canonical_hooks_shape` — every event entry has a `hooks` sub-array; every sub-array element has `type == "command"` and a `command` string. (No shorthand `{matcher, command}` siblings without the inner array.)
- `test_no_matchPaths_field` — `jq -e '[.. | objects | has("matchPaths")] | any | not' .claude/settings.json` returns true; i.e., no `matchPaths` key appears in any nested object. The previous `// empty | length == 0` form silently passed on empty streams and was replaced after pre-EXECUTE review caught the bug.
- `test_every_command_script_exists` — every `command` value contains a `scripts/<name>.py` path; the corresponding file must exist on disk.
- `test_guard_credentials_matcher_covers_all_io_tools` — the entry with `command` containing `guard-credentials.py` has `matcher` matching `"Bash|Write|Edit|MultiEdit|Read"` (in any field order).
- `test_check_handover_link_wired_to_write_edit_multiedit` — entry with `check-handover-link.py` has matcher `Write|Edit|MultiEdit`.
- `test_check_ontology_type_wired_to_write_edit_multiedit` — same matcher; can share the same entry as check-handover-link.
- `test_assumption_threshold_wired_to_write_only` — entry with `check-assumption-threshold.py` has matcher `Write`.
- `test_mode_guard_wired_to_three_events` — `mode-guard.py` appears in SessionStart, UserPromptExpansion, and PreToolUse(Skill).
- `test_cadence_nudge_wired_to_session_start` — `cadence-nudge.py` appears in SessionStart.

## Non-goals

- **Adding F2.7 (`validate-ost`) or F2.9 (`pin-date`) wiring.** Both blocked on upstream specs (P2.8 / P9.1) per ROADMAP. They'll be added by their own EXECUTE phases.
- **Live integration tests.** Verifying real hook firing requires a Claude Code session restart, which is out-of-band of unit tests. The manual-gesture list above is the human-driven verification.
- **Modifying `.claude/settings.local.json`.** That's personal scope.
- **Adding `timeout`, `async`, `statusMessage`, or `if` fields.** Default harness behavior is adequate.
- **Using `agent` or `prompt` hook types.** All six shipped hooks are `command` type.

## Open questions

1. **Should `check-handover-link` and `check-ontology-type` share a single matcher entry or live as separate entries?** Lean: share — both fire on `Write|Edit|MultiEdit`, no functional difference, half the file size. Spec adopts shared.

2. **Does the harness deduplicate when a matcher is duplicated?** If F2.6 declares two separate `PreToolUse` matcher entries each with pattern `Write|Edit|MultiEdit`, both fire — but is order preserved? Lean: yes per Anthropic's docs. Adopting "co-locate when matcher is identical" eliminates the question entirely.

3. **What happens when a hook script is missing executable bit or `python3` isn't found?** Out of scope — operational concern; documented as a known limitation in the hook doc cleanup task.

## Acceptance criteria

- [ ] `.claude/settings.json` exists at the project root's `.claude/` directory.
- [ ] `jq -e . .claude/settings.json` exits 0.
- [ ] `tools/tests/test-settings-json.sh` exists and passes all 14 contract tests.
- [ ] All five hook docs with shorthand-schema Configuration blocks are updated to canonical form: `check-handover-link.md`, `assumption-threshold-lock.md`, `ontology-type-check.md`, `mode-guard.md`, `cadence-nudge.md`. (`guard-credentials.md` is already canonical — no change.)
- [ ] `tools/pre-pr.sh` still exits 0 (all hook docs continue to lint clean after edits).
- [ ] `ROADMAP.md` F2.6 line: `[ ]` → `[x]`, append `**Shipped:** 2026-05-21.`
- [ ] `.claude/settings.local.json` is unchanged.

## Cross-references

- **Consumes:** the six F2 hook scripts (F2.1, F2.2, F2.3, F2.4, F2.5, F2.8). Indirectly: F0.10 (`tools/lint-hook.sh`) which gates the hook-doc edits.
- **Consumed by:** Claude Code's harness — every tool-use lifecycle event the kit cares about routes through this file.
- **Frontmatter fields owned:** none (it's a JSON config file).
- **Ontology object types touched:** none directly; activates every hook that touches typed artifacts.
