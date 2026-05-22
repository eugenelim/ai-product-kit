# Spec: hook-guard-credentials

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** hook (PreToolUse — Bash, Write, Edit, MultiEdit, Read)
- **Serves kit phase:** Meta (safety boundary; never blocks honest kit work)
- **Constrained by:** `AGENTS.md` ("Don't touch `~/.ssh`, credential stores, `.env*`, or push to protected branches. Hooks block these"); `.claude/CLAUDE.md` ("Never touch `~/.ssh`, `.env*`, credential paths"); F0.10

> **Spec contract.** Defines `scripts/guard-credentials.py` and `.claude/hooks/guard-credentials.md`. **Hard-blocks** any Bash, Write, Edit, or Read tool call whose payload references paths matching the credential allowlist of well-known secret locations. No override.

## Objective

Build a PreToolUse hook that blocks tool calls touching credential-y paths. Examples of blocked paths:

- `~/.ssh/**` (private/public keys, known_hosts, config)
- `.env`, `.env.*`, `.envrc` (anywhere in the tree)
- `**/credentials*` (`credentials.json`, `aws_credentials`, etc.)
- `**/*.pem`, `**/*.key` (private keys with conventional extensions)
- `**/.aws/credentials`, `**/.gnupg/**` (well-known cred dirs)
- `**/secrets/**`, `**/.secrets/**`

The hook is intentionally simple and **not bypassable** from the model's side — there is no `override` field. If a user genuinely needs to touch one of these (rare), they edit the file outside the agent or temporarily disable the hook via `/hooks`.

## Why now

Both `AGENTS.md` and `.claude/CLAUDE.md` already promise this hook exists ("Hooks block these"). Until it ships, the promise is documentary — the model is on the honor system. This is the lowest-cost, highest-value safety hook in the kit; it has zero upstream dependencies.

## Inputs and outputs

**Inputs.**
- Stdin: PreToolUse JSON with one of:
  - `tool_name: "Bash"`, `tool_input.command: <shell string>` — the script greps the command string for blocked path patterns.
  - `tool_name: "Write" | "Edit"`, `tool_input.file_path: <abs or relative path>`.
  - `tool_name: "MultiEdit"`, `tool_input.file_path: <path>` (the same path applies to all edits; the path is what matters for credential-guard, not the edit content).
  - `tool_name: "Read"`, `tool_input.file_path: <path>`.
- Disk: nothing read other than the path pattern table baked into the script.

**Outputs.**
- Exit 0: tool call allowed.
- Exit 2: tool call blocked. Stdout MUST be valid JSON: `{"decision":"block","reason":"guard-credentials: <category> match; refusing <tool_name>"}`. The `<category>` is a coarse label (`"ssh keys"`, `"env file"`, `"credentials file"`, `"private key"`, `"kubernetes config"`, `"npm token"`, `"pypi token"`, `"netrc"`) — never echoes the matched path verbatim. Stderr empty.
- **Fail-safe path:** on any internal error (malformed stdin, regex compilation failure, exception during dispatch), emit `{"decision":"block","reason":"guard-credentials: internal error; refusing as a precaution"}` to stdout AND exit 2. This ensures Claude Code's hook protocol always receives a well-formed block payload when we exit non-zero. Failing open (silent exit 2 with no JSON) is unacceptable for a safety hook.
- No model-side override. No silent allow.

**Path patterns + category labels (the load-bearing list — single source of truth):**

```python
BLOCKED_PATTERNS = [
    # SSH
    (re.compile(r"(?:^|/)\.ssh(?:/|$)"),                  "ssh keys"),
    (re.compile(r"id_(?:rsa|ed25519|ecdsa|dsa)(?:\.pub)?\b"), "ssh keys"),
    # GPG
    (re.compile(r"(?:^|/)\.gnupg(?:/|$)"),                "gpg keyring"),
    # Cloud credentials
    (re.compile(r"(?:^|/)\.aws/credentials\b"),           "aws credentials"),
    (re.compile(r"(?:^|/)\.kube/config\b"),               "kubernetes config"),
    # Package registry tokens
    (re.compile(r"(?:^|/)\.npmrc\b"),                     "npm token"),
    (re.compile(r"(?:^|/)\.pypirc\b"),                    "pypi token"),
    (re.compile(r"(?:^|/)\.netrc\b"),                     "netrc"),
    # Env files (narrowed — excludes .env.example and .env.sample)
    (re.compile(r"(?:^|/)\.env(?:\.(?:local|production|staging|development|test|secret))?$"), "env file"),
    (re.compile(r"(?:^|/)\.envrc\b"),                     "env file"),
    # Credential files / secret dirs
    (re.compile(r"(?:^|/)credentials(?:\.|$)"),           "credentials file"),
    (re.compile(r"(?:^|/)\.?secrets/"),                   "secrets directory"),
    # Key extensions
    (re.compile(r"\.(?:pem|key|p12|pfx)\b"),              "private key"),
]
```

`.env.example` and `.env.sample` are NOT matched — those are documentation files, not secrets, and trigger constant false positives. The conservative-block policy applies to ambiguous paths, not to filenames whose name explicitly signals "example."

**Path normalization** (applied before pattern matching, for both Bash tokens and Write/Edit/MultiEdit/Read `file_path`):
1. `os.path.expanduser` — expand leading `~`.
2. `os.path.normpath` — collapse `./foo/../.ssh/id_rsa` → `.ssh/id_rsa` so traversal paths are caught.

For Bash, the script tokenizes the command string with `shlex.split` and tests each normalized token against the same patterns. Tokens that fail to shlex.split (e.g., partial quotes) fall back to a regex sweep on the raw string.

## Boundaries

### Always do
- Exit 2 on any match, with the well-formed JSON payload above on stdout.
- Operate on Bash, Write, Edit, MultiEdit, Read tool calls.
- Apply path normalization (`expanduser` + `normpath`) before matching.
- Public-key files (`*.pub`) are blocked by the same SSH-keys pattern as private keys, by design. The conservative policy prefers not distinguishing — an agent reading `id_rsa.pub` is often setting up to read `id_rsa` next.
- Be conservative on Bash: a false-positive (refusing a benign command that mentions ".env" in a comment) is acceptable; a false-negative (allowing a credential read) is not.

### Ask first
- Adding or removing patterns. Default: only the patterns above.
- Adding override semantics. Default: no override; the spec's contract is "no model-side override."

### Never do
- Touch the matched file.
- Log the matched payload (the payload could *contain* secrets).
- Allow a tool call when the path is uncertain — pattern match wins on doubt.

## Verification mode

- **TDD.** Unit tests under `scripts/tests/test_guard_credentials.py`.
- **Goal-based check.** `tools/lint-hook.sh .claude/hooks/guard-credentials.md` exits 0.
- **Manual gesture.** With the hook wired, `cat ~/.ssh/id_rsa` in Bash produces an immediate block; `cat README.md` succeeds.

## Contract tests

- `test_blocks_bash_cat_of_ssh_private_key` — `cat ~/.ssh/id_rsa` → exit 2.
- `test_blocks_bash_with_relative_ssh_path` — `cp /Users/foo/.ssh/known_hosts /tmp/` → exit 2.
- `test_blocks_bash_traversal_path_to_ssh` — `cat ./foo/../.ssh/id_rsa` → exit 2 (normpath catches it).
- `test_blocks_write_to_dot_env` — Write `.env` → exit 2.
- `test_blocks_write_to_dot_env_dot_local` — Write `.env.local` → exit 2.
- `test_allows_write_to_dot_env_dot_example` — Write `.env.example` → exit 0 (documentation, not a secret).
- `test_allows_write_to_dot_env_dot_sample` — Write `.env.sample` → exit 0.
- `test_blocks_write_to_kube_config` — Write `~/.kube/config` → exit 2 (kubernetes config).
- `test_blocks_read_of_npmrc` — Read `~/.npmrc` → exit 2.
- `test_blocks_read_of_pypirc` — Read `~/.pypirc` → exit 2.
- `test_blocks_read_of_netrc` — Read `~/.netrc` → exit 2.
- `test_blocks_read_of_credentials_json` — Read `~/.aws/credentials` → exit 2.
- `test_blocks_bash_referencing_pem_file` — `openssl x509 -in foo.pem -text` → exit 2.
- `test_blocks_bash_redirect_into_credentials_path` — `echo $TOKEN > ~/.aws/credentials` → exit 2.
- `test_blocks_multiedit_to_credential_path` — MultiEdit `tool_input.file_path: .env.production` → exit 2.
- `test_allows_bash_unrelated_command` — `ls -la` → exit 0.
- `test_allows_write_to_normal_file` — Write `docs/specs/foo/spec.md` → exit 0.
- `test_allows_read_of_kit_artifact` — Read `strategy/intents/foo.md` → exit 0.
- `test_block_reason_does_not_echo_matched_text_verbatim` — the JSON reason names the category (e.g., "ssh keys") rather than echoing the full path.
- `test_malformed_bash_quoting_falls_back_to_raw_regex` — `bash -c 'cat ~/.ssh/id_rsa # has stray "'` (partial quote) → `shlex.split` raises; raw regex sweep matches → exit 2.
- `test_internal_error_produces_valid_block_json` — pipe garbage to stdin (non-JSON bytes) → exit 2 + well-formed `{"decision":"block","reason":"guard-credentials: internal error..."}` on stdout.
- `test_path_outside_patterns_passes_through` — `tools/some-script.py` → exit 0.

## Non-goals

- Validating that the matched file actually *contains* secrets (the spec is path-based; content-based scanning is a different layer).
- Distinguishing comment-mentions from real touches in shell commands. Conservative-block is the policy.
- Network-credential checks (`gh auth status`, `aws sts get-caller-identity`). Those don't read credential files at the shell level.
- Auditing the git history for accidentally committed secrets. Out of scope.
- Override mechanics (per the spec). If a user must bypass, they disable the hook for one session via `/hooks`.
- **Commands that expand shell variables before execution** (`eval $VAR`, `sh -c "$CMD"` with the secret in `$CMD`). These cannot be inspected at the pre-execution layer without a shell interpreter. Accepted false-negatives under the path-based model.
- **GPG key IDs as command arguments** (e.g., `git commit --gpg-sign=ABCD1234`). The key ID is not a path; not in scope for a path-based hook.
- **Windows path separators** (`C:\Users\foo\.ssh\id_rsa`). The kit is macOS/Linux-first per AGENTS.md. If Windows adopters arrive, the patterns will need backslash variants.

## Open questions

(Both prior questions closed. Q1: `.env.example` and `.env.sample` are explicitly NOT blocked; the regex is narrowed to known-suffix variants only. Q2: Windows paths moved to Non-goals as accepted scope limit.)

## Acceptance criteria

- [ ] `scripts/guard-credentials.py` exists, stdlib only, ≤ 250 LOC.
- [ ] `scripts/tests/test_guard_credentials.py` exists; all 20 contract tests pass.
- [ ] `.claude/hooks/guard-credentials.md` exists; `tools/lint-hook.sh` exits 0 against it.
- [ ] `python3 -m unittest scripts.tests.test_guard_credentials` exits 0.
- [ ] PLAN / VERIFY / REVIEW gates exit 0.
- [ ] **Depends on:** F0.10 (`tools/lint-hook.sh`) must ship before VERIFY can run.

## Cross-references

- **Consumed by:** F2.6 (PreToolUse matchers `Bash|Write|Edit|Read`).
- **Consumes:** stdlib only.
- **Frontmatter fields owned:** none.
- **Ontology object types touched:** none — pure safety boundary.
