# example-good hook

A minimal valid hook documentation file used by `tools/tests/test-lint-hook.sh`.

## What it does

Documents the four required-section shape for a hook doc.

## Why this matters

Without a shape gate, hook docs drift and stop being useful.

## Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "Write", "hooks": [{"type": "command", "command": "scripts/example.py"}]}
    ]
  }
}
```

## Related

- `tools/lint-hook.sh` — the linter this fixture is verified against.
