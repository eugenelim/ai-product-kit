"""Contract tests for scripts/guard-credentials.py (F2.8).

Tests construct payload dicts and call `check()` directly — they never touch
real credential paths. Synthetic paths like `/Users/foo/.ssh/id_rsa` are used
purely as pattern fodder.

Source of truth for the contract list: docs/specs/hook-guard-credentials/spec.md.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "guard-credentials.py"


def _load_module():
    """Load guard-credentials.py by path (hyphen in filename → not importable)."""
    spec = importlib.util.spec_from_file_location("guard_credentials", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gc = _load_module()


def bash_payload(cmd: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


def path_payload(tool: str, path: str) -> dict:
    return {"tool_name": tool, "tool_input": {"file_path": path}}


class GuardCredentialsContract(unittest.TestCase):
    # ------------------------------------------------------------------
    # Bash dispatch
    # ------------------------------------------------------------------

    def test_blocks_bash_cat_of_ssh_private_key(self):
        result = gc.check(bash_payload("cat ~/.ssh/id_rsa"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "ssh keys")
        self.assertEqual(result[1], "Bash")

    def test_blocks_bash_with_relative_ssh_path(self):
        result = gc.check(bash_payload("cp /Users/foo/.ssh/known_hosts /tmp/"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "ssh keys")

    def test_blocks_bash_traversal_path_to_ssh(self):
        result = gc.check(bash_payload("cat ./foo/../.ssh/id_rsa"))
        self.assertIsNotNone(result, "normpath should collapse ./foo/../ to catch the traversal")
        self.assertEqual(result[0], "ssh keys")

    def test_blocks_bash_referencing_pem_file(self):
        result = gc.check(bash_payload("openssl x509 -in foo.pem -text"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "private key")

    def test_blocks_bash_redirect_into_credentials_path(self):
        result = gc.check(bash_payload("echo $TOKEN > ~/.aws/credentials"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "aws credentials")

    def test_allows_bash_unrelated_command(self):
        self.assertIsNone(gc.check(bash_payload("ls -la")))

    def test_malformed_bash_quoting_falls_back_to_raw_regex(self):
        # Partial quote → shlex.split raises ValueError → raw regex sweep.
        cmd = 'bash -c \'cat ~/.ssh/id_rsa # has stray "\''
        result = gc.check(bash_payload(cmd))
        self.assertIsNotNone(result, "raw regex fallback should still catch ~/.ssh/id_rsa")
        self.assertEqual(result[0], "ssh keys")

    # ------------------------------------------------------------------
    # Write / Edit / MultiEdit / Read dispatch
    # ------------------------------------------------------------------

    def test_blocks_write_to_dot_env(self):
        result = gc.check(path_payload("Write", ".env"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "env file")
        self.assertEqual(result[1], "Write")

    def test_blocks_write_to_dot_env_dot_local(self):
        result = gc.check(path_payload("Write", ".env.local"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "env file")

    def test_allows_write_to_dot_env_dot_example(self):
        self.assertIsNone(gc.check(path_payload("Write", ".env.example")))

    def test_allows_write_to_dot_env_dot_sample(self):
        self.assertIsNone(gc.check(path_payload("Write", ".env.sample")))

    def test_blocks_write_to_kube_config(self):
        result = gc.check(path_payload("Write", "~/.kube/config"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "kubernetes config")

    def test_blocks_read_of_npmrc(self):
        result = gc.check(path_payload("Read", "~/.npmrc"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "npm token")

    def test_blocks_read_of_pypirc(self):
        result = gc.check(path_payload("Read", "~/.pypirc"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "pypi token")

    def test_blocks_read_of_netrc(self):
        result = gc.check(path_payload("Read", "~/.netrc"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "netrc")

    def test_blocks_read_of_credentials_json(self):
        result = gc.check(path_payload("Read", "~/.aws/credentials"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "aws credentials")

    def test_blocks_multiedit_to_credential_path(self):
        result = gc.check(path_payload("MultiEdit", ".env.production"))
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "env file")
        self.assertEqual(result[1], "MultiEdit")

    def test_allows_write_to_normal_file(self):
        self.assertIsNone(gc.check(path_payload("Write", "docs/specs/foo/spec.md")))

    def test_allows_read_of_kit_artifact(self):
        self.assertIsNone(gc.check(path_payload("Read", "strategy/intents/foo.md")))

    # ------------------------------------------------------------------
    # Block-reason hygiene + fail-safe + pass-through
    # ------------------------------------------------------------------

    def test_block_reason_does_not_echo_matched_text_verbatim(self):
        # Reason JSON must name the category, not the path.
        secret_path = "/Users/foo/private/.ssh/id_ed25519"
        result = gc.check(bash_payload(f"cat {secret_path}"))
        self.assertIsNotNone(result)
        category, tool_name = result
        reason = gc.block_payload(category, tool_name)
        self.assertIn("ssh keys", reason)
        self.assertNotIn(secret_path, reason)
        self.assertNotIn("id_ed25519", reason)
        self.assertNotIn("/Users/foo", reason)

    def test_internal_error_produces_valid_block_json(self):
        # Pipe garbage to stdin → top-level except → must emit well-formed
        # block JSON on stdout AND exit 2. Silent exit 2 would fail open.
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=b"\x00\x01not-json-at-all{{{",
            capture_output=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 2, "fail-safe must exit 2")
        self.assertTrue(result.stdout.strip(), "fail-safe must emit JSON on stdout")
        decoded = json.loads(result.stdout)
        self.assertEqual(decoded["decision"], "block")
        self.assertIn("internal error", decoded["reason"])

    def test_path_outside_patterns_passes_through(self):
        self.assertIsNone(gc.check(path_payload("Write", "tools/some-script.py")))


class GuardCredentialsSubprocess(unittest.TestCase):
    """End-to-end sanity: invoke the script and assert the protocol contract."""

    def test_subprocess_block_emits_json_and_exit_2(self):
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "~/.ssh/id_rsa"}})
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=payload.encode("utf-8"),
            capture_output=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 2)
        decoded = json.loads(result.stdout)
        self.assertEqual(decoded["decision"], "block")
        self.assertIn("ssh keys", decoded["reason"])
        self.assertIn("Read", decoded["reason"])

    def test_subprocess_allow_exits_0(self):
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls -la"}})
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=payload.encode("utf-8"),
            capture_output=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
