# guard-credentials hook

The kit's safety boundary on credential paths. Hard-blocks any tool call that
touches a well-known secret location. **No model-side override** — the spec is
explicit: refusing a benign command that mentions `.env` in a comment is
acceptable; allowing a credential read is not.

## What it does

Registered as a `PreToolUse` hook matching `Bash`, `Write`, `Edit`,
`MultiEdit`, and `Read`. Before any matching tool call executes, the hook runs
`scripts/guard-credentials.py`, which:

1. Reads the PreToolUse JSON payload from stdin.
2. Dispatches on `tool_name`:
   - `Bash` — tokenizes `tool_input.command` with `shlex.split`; on parse
     failure (partial quotes etc.) falls back to a raw regex sweep on the
     command string. Each token is normalized (`expanduser` + `normpath`) and
     checked against the pattern table.
   - `Write` | `Edit` | `MultiEdit` | `Read` — normalizes
     `tool_input.file_path` and checks it against the same table.
3. On the first match, exits 2 with a JSON payload on stdout:
   `{"decision":"block","reason":"guard-credentials: <category> match; refusing <tool_name>"}`.
4. On no match, exits 0 (allow).
5. **Fail-safe path:** on any internal exception (malformed stdin, etc.) the
   script emits `{"decision":"block","reason":"guard-credentials: internal error; refusing as a precaution"}`
   and exits 2. Claude Code's protocol requires JSON on the block path —
   silent exit 2 would fail open.

The block `reason` names the matched **category** (e.g. `"ssh keys"`), never
the matched path verbatim. The path itself could be sensitive context.

## Why this matters

`AGENTS.md` and `.claude/CLAUDE.md` both promise: "Don't touch `~/.ssh`,
credential stores, `.env*`. Hooks block these." Until this hook shipped, that
promise was documentary — the model was on the honor system. The honor system
is not a safety boundary.

This is the lowest-cost, highest-value safety hook in the kit. It costs the
occasional false-positive (a Bash command that mentions a credential path in a
comment gets blocked); it prevents a class of failure that would otherwise be
silent and irreversible.

There is **no model-side override field** on this hook. If a user genuinely
needs to touch one of these paths (rare), they edit outside the agent or
disable the hook via `/hooks` for that session. The model cannot grant itself
an exception.

## Patterns

The single source of truth for the pattern table lives in
[`docs/specs/hook-guard-credentials/spec.md`](../../docs/specs/hook-guard-credentials/spec.md).
The in-code copy is in `scripts/guard-credentials.py` (`BLOCKED_PATTERNS`).
Categories enforced:

- **ssh keys** — `~/.ssh/**`, `id_rsa`, `id_ed25519`, `id_ecdsa`, `id_dsa`
  (including `.pub` variants — an agent reading `id_rsa.pub` is often
  setting up to read `id_rsa` next).
- **gpg keyring** — `~/.gnupg/**`.
- **aws credentials** — `~/.aws/credentials`.
- **kubernetes config** — `~/.kube/config`.
- **npm token** — `~/.npmrc`.
- **pypi token** — `~/.pypirc`.
- **netrc** — `~/.netrc`.
- **env file** — `.env`, `.env.local`, `.env.production`, `.env.staging`,
  `.env.development`, `.env.test`, `.env.secret`, and `.envrc`.
  Explicitly **not blocked:** `.env.example` and `.env.sample` — those are
  documentation files, and false-positives on them generate constant noise.
- **credentials file** — paths matching `credentials.*` or named exactly
  `credentials` (e.g. `aws_credentials`, `credentials.json`).
- **secrets directory** — any path component `secrets/` or `.secrets/`.
- **private key** — files ending in `.pem`, `.key`, `.p12`, `.pfx`.

Path normalization applies before matching: `os.path.expanduser` then
`os.path.normpath`. Traversal paths like `./foo/../.ssh/id_rsa` collapse to
`.ssh/id_rsa` and match.

## Non-goals

- **Content-based scanning.** The hook is path-based. Detecting that an
  arbitrary file *contains* secrets is a different layer.
- **Variable-expanded shell commands.** `eval $VAR` and `sh -c "$CMD"` where
  the credential is hidden inside `$CMD` can't be inspected pre-execution
  without a shell interpreter. Accepted false-negative.
- **GPG key IDs as arguments** (`git commit --gpg-sign=ABCD1234`). The key ID
  is not a path.
- **Windows path separators.** The kit is macOS/Linux-first. If Windows
  adopters arrive, the patterns need backslash variants.
- **Override mechanics.** Per the spec, there is no override. Disable the
  hook via `/hooks` if you need a one-session exception.

## Configuration

In `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit|MultiEdit|Read",
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/guard-credentials.py"
          }
        ]
      }
    ]
  }
}
```

F2.6 (`hooks-wired-in-settings`) will consolidate this entry alongside the
other PreToolUse matchers. Until then, the snippet above is the standalone
wiring for manual validation.

## Related

- `docs/specs/hook-guard-credentials/spec.md` — the spec; single source of
  truth for the pattern table and contract tests.
- `scripts/guard-credentials.py` — the implementation.
- `scripts/tests/test_guard_credentials.py` — 22 contract tests + 2
  subprocess sanity tests.
- `AGENTS.md` — the "Don't touch credential stores" promise this hook
  fulfills.
- `.claude/hooks/assumption-threshold-lock.md` — the other always-on safety
  hook in the kit.
