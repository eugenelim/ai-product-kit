# mode-guard hook

Enforces the project's declared `mode:` (greenfield vs enterprise) at the slash-command boundary. Blocks wrong-mode commands at write time so mode stops being documentary and starts being a real gate.

## What it does

A three-event hook wired to `SessionStart`, `UserPromptExpansion`, and `PreToolUse` on the `Skill` tool. On every invocation it re-reads `.claude/CLAUDE.md` for the `mode:` line (no cached state) and dispatches:

1. **SessionStart** — injects a one-block context reminder via `hookSpecificOutput.additionalContext`, telling the model the active mode plus the per-mode blocked-command list. Always exit 0; never blocks.
2. **UserPromptExpansion** (fires when the user types `/wardley-map` directly) — reads `payload["command_name"]`. If the command is in the wrong-mode blocked list, blocks via stdout `{"decision":"block","reason":"...","hookSpecificOutput":{"hookEventName":"UserPromptExpansion"}}` and exits **0** (this event treats stdout JSON as the block channel; non-zero exits are reserved for non-blocking errors).
3. **PreToolUse on Skill** (fires when the model invokes the `Skill` tool) — reads `payload["tool_input"]["skill_name"]`. If blocked, emits stdout `{"decision":"block","reason":"..."}` and exits **2** (PreToolUse's block protocol).

Per-mode blocked lists:

- **greenfield** blocks `wardley-map`, `internal-jtbd-interview`, `value-chain-evolution`.
- **enterprise** blocks `competitive-research`, `market-scan`, `jtbd-analogues`.

Shared across both modes (never blocked): `strategy-refresh`, `strategic-intent`, `audit-portfolio-coherence`, `cadence-check`, `phase-guide`.

If `mode:` is undeclared, missing, or set to an unknown value (e.g. `enterprise-lite`), the hook degrades safely: SessionStart emits a stderr warning, UPE and PreToolUse(Skill) emit a stderr notice and allow the call. Enforcement only fires when the mode is explicitly one of the two known values.

## Why this matters

Mode is project-scoped intentionally. Greenfield and enterprise pursue different strategy methods — running a `/wardley-map` in a kit that is supposed to be greenfield-mode (or vice versa) produces drift artifacts in the wrong folder, weakens the OST, and makes the resulting strategy harder to defend.

Until this hook ships, the rule in `.claude/CLAUDE.md` is documentary. Divergence is only caught after a wrong-mode command runs to completion. The hook converts that soft convention into a write-time gate. You can still switch modes — just by editing one line in `.claude/CLAUDE.md` — but you can't silently drift into the other mode by invoking its commands.

The kit explicitly wires both UPE and PreToolUse(Skill) because Anthropic's docs route the two slash-command paths (user-typed vs model-invoked) through different events. Wiring only one would leave a silent evasion gap.

## Override

There is no per-call override. To run a blocked command, change the `mode:` line in `.claude/CLAUDE.md` to the matching mode. The decision is intentionally a single source of truth — encoding overrides in the hook would re-introduce the drift problem the hook exists to prevent.

If you're working across both modes, the right answer per the kit's own guidance is to use separate project folders.

## Configuration

Wired in `.claude/settings.json` as of F2.6 (2026-05-21):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {"type": "command", "command": "python3 scripts/mode-guard.py"}
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
        "matcher": "Skill",
        "hooks": [
          {"type": "command", "command": "python3 scripts/mode-guard.py"}
        ]
      }
    ]
  }
}
```

The script dispatches internally on the payload's `hook_event_name` (and `tool_name` for PreToolUse), so a single entry point handles all three wirings. No per-command matcher loop is required.

## Related

- `.claude/CLAUDE.md` — the source of truth for `mode:`
- `docs/specs/hook-mode-guard/spec.md` — full contract and test list
- `scripts/mode-guard.py` — implementation
- `ROADMAP.md` F2.6 — wires this hook into `.claude/settings.json`
