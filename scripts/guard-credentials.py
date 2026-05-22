#!/usr/bin/env python3
"""guard-credentials.py — PreToolUse hook that hard-blocks tool calls touching
well-known credential paths (F2.8, slug: hook-guard-credentials).

This is the kit's safety boundary. There is NO model-side override. If a user
genuinely needs to touch one of these paths (rare), they edit outside the agent
or temporarily disable the hook via `/hooks`.

Tool dispatch:
  - Bash: shlex.split(command); normalize and check each token. On shlex
    ValueError, raw regex sweep on the command string.
  - Write | Edit | MultiEdit | Read: normalize and check `tool_input.file_path`.

Fail-safe path: on ANY internal error (malformed stdin, unexpected shape,
exception during dispatch), emit a well-formed block JSON payload to stdout
AND exit 2. Claude Code's hook protocol requires the JSON on the block path —
silent exit 2 would fail open.

Block reason names the matched category (e.g. "ssh keys") — never echoes the
matched path verbatim (the path could itself leak sensitive context).

Source of truth for the pattern table: docs/specs/hook-guard-credentials/spec.md.
Exit codes: 0 = allow, 2 = block (always with JSON on stdout).
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from typing import Optional


# ---------------------------------------------------------------------------
# Pattern table — single source of truth lives in the spec; this is the
# load-bearing in-code copy. Keep in sync with
# docs/specs/hook-guard-credentials/spec.md.
# ---------------------------------------------------------------------------

BLOCKED_PATTERNS: list[tuple[re.Pattern, str]] = [
    # SSH
    (re.compile(r"(?:^|/)\.ssh(?:/|$)"), "ssh keys"),
    (re.compile(r"id_(?:rsa|ed25519|ecdsa|dsa)(?:\.pub)?\b"), "ssh keys"),
    # GPG
    (re.compile(r"(?:^|/)\.gnupg(?:/|$)"), "gpg keyring"),
    # Cloud credentials
    (re.compile(r"(?:^|/)\.aws/credentials\b"), "aws credentials"),
    (re.compile(r"(?:^|/)\.kube/config\b"), "kubernetes config"),
    # Package registry tokens
    (re.compile(r"(?:^|/)\.npmrc\b"), "npm token"),
    (re.compile(r"(?:^|/)\.pypirc\b"), "pypi token"),
    (re.compile(r"(?:^|/)\.netrc\b"), "netrc"),
    # Env files (narrowed — excludes .env.example and .env.sample).
    (
        re.compile(
            r"(?:^|/)\.env(?:\.(?:local|production|staging|development|test|secret))?$"
        ),
        "env file",
    ),
    (re.compile(r"(?:^|/)\.envrc\b"), "env file"),
    # Credential files / secret dirs
    (re.compile(r"(?:^|/)credentials(?:\.|$)"), "credentials file"),
    (re.compile(r"(?:^|/)\.?secrets/"), "secrets directory"),
    # Key extensions
    (re.compile(r"\.(?:pem|key|p12|pfx)\b"), "private key"),
]

TOOLS_PATH_FIELD = {"Write", "Edit", "MultiEdit", "Read"}


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------


def normalize(p: str) -> str:
    """Expand ~ and collapse traversal segments before pattern matching."""
    return os.path.normpath(os.path.expanduser(p))


def match_category(s: str) -> Optional[str]:
    """Return the matched category label, or None if no pattern fires."""
    n = normalize(s)
    for pattern, category in BLOCKED_PATTERNS:
        if pattern.search(n):
            return category
    return None


def check_path(path: str) -> Optional[str]:
    """Check a single path payload. Returns matched category or None."""
    if not isinstance(path, str) or not path:
        return None
    return match_category(path)


def check_bash(command: str) -> Optional[str]:
    """Check a Bash command string. Returns matched category or None.

    Tokenizes with shlex; falls back to raw-string regex sweep on shlex error
    (partial quotes, etc.) so malformed commands cannot bypass the guard.
    """
    if not isinstance(command, str) or not command:
        return None
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        # Raw-string fallback: scan the command as a whole, normalized.
        return match_category(command)
    for token in tokens:
        cat = match_category(token)
        if cat:
            return cat
    # Belt-and-braces: also scan the raw command for patterns that survived
    # tokenization without becoming a standalone token (e.g. inside a quoted
    # redirect target). Conservative-block policy: false positives acceptable.
    return match_category(command)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------


def check(payload: dict) -> Optional[tuple[str, str]]:
    """Inspect a PreToolUse payload. Returns (category, tool_name) on block,
    or None to allow.

    Pure function — does no I/O. Tests call this directly with constructed
    dicts; no real filesystem paths are touched.
    """
    if not isinstance(payload, dict):
        return None
    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_name, str) or not isinstance(tool_input, dict):
        return None

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        cat = check_bash(command)
        if cat:
            return (cat, tool_name)
        return None

    if tool_name in TOOLS_PATH_FIELD:
        path = tool_input.get("file_path", "")
        cat = check_path(path)
        if cat:
            return (cat, tool_name)
        return None

    # Unknown tool — pass through. The matcher list in settings.json is what
    # restricts which tools we get invoked for; defensive default is allow.
    return None


def block_payload(category: str, tool_name: str) -> str:
    return json.dumps(
        {
            "decision": "block",
            "reason": (
                f"guard-credentials: {category} match; refusing {tool_name}"
            ),
        }
    )


def internal_error_payload() -> str:
    return json.dumps(
        {
            "decision": "block",
            "reason": (
                "guard-credentials: internal error; refusing as a precaution"
            ),
        }
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        result = check(payload)
        if result is None:
            return 0
        category, tool_name = result
        sys.stdout.write(block_payload(category, tool_name))
        return 2
    except Exception:
        # Fail-safe: ALWAYS emit a well-formed block JSON on the non-zero exit.
        # Silent exit 2 would fail open in Claude Code's hook protocol.
        try:
            sys.stdout.write(internal_error_payload())
        except Exception:
            pass
        return 2


if __name__ == "__main__":
    sys.exit(main())
