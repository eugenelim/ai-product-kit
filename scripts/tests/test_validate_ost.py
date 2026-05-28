"""Contract tests for scripts/validate_ost.py per docs/specs/phase-2-discovery-primitives §P2.8."""
from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO / "scripts" / "validate_ost.py"
FIX = REPO / "scripts" / "tests" / "fixtures" / "ost"


def _run(case: Path, fmt: str = "json", input_name: str = "input.json",
         output_name: str = "output.json", change_set_name: str = "change-set.json",
         input_path: str | None = None) -> subprocess.CompletedProcess:
    """Run the validator. case is a directory under FIX."""
    inp = input_path if input_path is not None else str(case / input_name)
    return subprocess.run(
        [
            "python3", str(SCRIPT),
            "--input", inp,
            "--output", str(case / output_name),
            "--change-set", str(case / change_set_name),
            "--format", fmt,
        ],
        capture_output=True, text=True,
    )


def _parse_violations(stderr: str) -> list[dict]:
    return json.loads(stderr)["violations"]


class ValidateOstTests(unittest.TestCase):

    # 1
    def test_all_valid_baseline_passes(self):
        r = _run(FIX / "valid" / "baseline")
        self.assertEqual(r.returncode, 0, msg=f"stderr={r.stderr!r}")
        self.assertEqual(r.stdout, "")
        self.assertEqual(r.stderr, "")

    # 2
    def test_orphan_node_fails_with_rule_no_orphans(self):
        r = _run(FIX / "invalid" / "no-orphans")
        self.assertEqual(r.returncode, 1)
        v = _parse_violations(r.stderr)
        self.assertTrue(any(x["rule"] == "no-orphans" for x in v))

    # 3
    def test_reparent_to_nonexistent_parent_fails_with_rule_no_orphans(self):
        r = _run(FIX / "invalid" / "no-orphans-reparent-to-missing")
        self.assertEqual(r.returncode, 1)
        v = _parse_violations(r.stderr)
        self.assertTrue(any(x["rule"] == "no-orphans" for x in v))

    # 4
    def test_double_reference_fails_with_rule_no_double_references(self):
        r = _run(FIX / "invalid" / "no-double-references")
        self.assertEqual(r.returncode, 1)
        v = _parse_violations(r.stderr)
        self.assertTrue(any(x["rule"] == "no-double-references" for x in v))

    # 5
    def test_non_is_evidence_under_two_opportunities_passes(self):
        r = _run(FIX / "valid" / "non-is-evidence")
        self.assertEqual(r.returncode, 0, msg=f"stderr={r.stderr!r}")

    # 6
    def test_data_loss_fails_with_rule_no_data_loss(self):
        r = _run(FIX / "invalid" / "no-data-loss")
        self.assertEqual(r.returncode, 1)
        v = _parse_violations(r.stderr)
        self.assertTrue(any(x["rule"] == "no-data-loss" for x in v))

    # 7
    def test_delete_with_children_fails_with_rule_no_data_loss(self):
        r = _run(FIX / "invalid" / "no-data-loss-delete-with-children")
        self.assertEqual(r.returncode, 1)
        v = _parse_violations(r.stderr)
        self.assertTrue(any(x["rule"] == "no-data-loss" for x in v))

    # 8
    def test_invalid_action_verb_fails_with_rule_valid_action_vocabulary(self):
        r = _run(FIX / "invalid" / "valid-action-vocabulary")
        self.assertEqual(r.returncode, 1)
        v = _parse_violations(r.stderr)
        self.assertTrue(any(x["rule"] == "valid-action-vocabulary" for x in v))

    # 9
    def test_silent_move_fails_with_rule_compound_operation_visibility(self):
        r = _run(FIX / "invalid" / "compound-operation-visibility")
        self.assertEqual(r.returncode, 1)
        v = _parse_violations(r.stderr)
        self.assertTrue(any(x["rule"] == "compound-operation-visibility" for x in v))

    # 10
    def test_non_deterministic_change_set_fails_with_rule_change_set_determinism(self):
        r = _run(FIX / "invalid" / "change-set-determinism")
        self.assertEqual(r.returncode, 1)
        v = _parse_violations(r.stderr)
        rules = {x["rule"] for x in v}
        # change-set-determinism fires when no more-specific diagnosis (Rule 4 etc.) matches
        self.assertIn("change-set-determinism", rules)

    # 11
    def test_empty_input_tree_with_add_actions_passes(self):
        r = _run(FIX / "valid" / "empty-input-add-actions")
        self.assertEqual(r.returncode, 0, msg=f"stderr={r.stderr!r}")

    # 12
    def test_empty_change_set_identical_input_output_passes(self):
        r = _run(FIX / "valid" / "empty-change-set-identical")
        self.assertEqual(r.returncode, 0, msg=f"stderr={r.stderr!r}")

    # 13
    def test_empty_change_set_with_different_output_fails_rule_1(self):
        r = _run(FIX / "invalid" / "change-set-determinism-empty-actions")
        self.assertEqual(r.returncode, 1)
        v = _parse_violations(r.stderr)
        rules = {x["rule"] for x in v}
        self.assertIn("change-set-determinism", rules)

    # 14
    def test_malformed_input_json_exits_2(self):
        bad = FIX / "valid" / "baseline"
        # Use the baseline output as the "input" but force a malformed json by writing one inline.
        tmp = FIX / "_tmp_malformed.json"
        tmp.write_text("{ not valid json")
        try:
            r = _run(bad, input_path=str(tmp))
            self.assertEqual(r.returncode, 2)
            payload = json.loads(r.stderr)
            self.assertEqual(payload["verdict"], "error")
            self.assertEqual(payload["reason"], "malformed-json")
        finally:
            tmp.unlink()

    # 15
    def test_missing_input_file_exits_2(self):
        r = _run(FIX / "valid" / "baseline", input_path=str(FIX / "_does_not_exist.json"))
        self.assertEqual(r.returncode, 2)
        payload = json.loads(r.stderr)
        self.assertEqual(payload["reason"], "missing-file")

    # 16
    def test_schema_violation_exits_2(self):
        r = _run(FIX / "error" / "schema-violation")
        self.assertEqual(r.returncode, 2)
        payload = json.loads(r.stderr)
        self.assertEqual(payload["reason"], "schema-violation")

    # 17
    def test_merge_with_nonexistent_id_exits_2(self):
        # Build inline fixture: merge naming a non-existent id.
        tmp_dir = FIX / "_tmp_merge_inconsistent"
        tmp_dir.mkdir(exist_ok=True)
        (tmp_dir / "input.json").write_text(json.dumps({
            "outcome": {"id": "OUT-001", "name": "O"},
            "nodes": [{"id": "OPP-001", "type": "Opportunity", "name": "A",
                       "parent": "OUT-001", "evidence_basis": []}],
        }))
        (tmp_dir / "output.json").write_text(json.dumps({
            "outcome": {"id": "OUT-001", "name": "O"},
            "nodes": [{"id": "OPP-001", "type": "Opportunity", "name": "A",
                       "parent": "OUT-001", "evidence_basis": []}],
        }))
        (tmp_dir / "change-set.json").write_text(json.dumps({
            "actions": [{"op": "merge", "ids": ["OPP-001", "OPP-999"], "into": "OPP-001"}],
        }))
        try:
            r = _run(tmp_dir)
            self.assertEqual(r.returncode, 2)
            payload = json.loads(r.stderr)
            self.assertEqual(payload["reason"], "change-set-inconsistent")
        finally:
            for f in tmp_dir.iterdir():
                f.unlink()
            tmp_dir.rmdir()

    # 18
    def test_human_format_failure_writes_paragraph_to_stderr(self):
        r = _run(FIX / "invalid" / "no-orphans", fmt="human")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout, "")
        # at least 2 sentences-worth (one period + content)
        self.assertGreater(len(r.stderr.strip()), 40)
        self.assertIn("no-orphans", r.stderr)

    # 19
    def test_human_format_pass_writes_confirmation_to_stdout(self):
        r = _run(FIX / "valid" / "baseline", fmt="human")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Validation passed", r.stdout)
        self.assertEqual(r.stderr, "")

    # 20
    def test_json_format_pass_silent_on_both_streams(self):
        r = _run(FIX / "valid" / "baseline", fmt="json")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "")
        self.assertEqual(r.stderr, "")

    # ------------ added per REVIEW iter-1 quality-engineer findings -----------

    # 21 — happy path for merge (T1)
    def test_valid_merge_passes(self):
        r = _run(FIX / "valid" / "merge")
        self.assertEqual(r.returncode, 0, msg=f"stderr={r.stderr!r}")

    # 22 — happy path for split with two new ids (T1)
    def test_valid_split_passes(self):
        r = _run(FIX / "valid" / "split")
        self.assertEqual(r.returncode, 0, msg=f"stderr={r.stderr!r}")

    # 23 — happy path for reframe (T1)
    def test_valid_reframe_passes(self):
        r = _run(FIX / "valid" / "reframe")
        self.assertEqual(r.returncode, 0, msg=f"stderr={r.stderr!r}")

    # 24 — happy path for reparent (T1)
    def test_valid_reparent_passes(self):
        r = _run(FIX / "valid" / "reparent")
        self.assertEqual(r.returncode, 0, msg=f"stderr={r.stderr!r}")

    # 25 — split where one of the new ids reuses the source id (T2)
    def test_valid_split_reusing_source_id_passes(self):
        r = _run(FIX / "valid" / "split-reusing-source")
        self.assertEqual(r.returncode, 0, msg=f"stderr={r.stderr!r}")

    # 26 — Rule 1 fires in the other direction (applied has extra nodes) (T3)
    def test_change_set_determinism_applied_superset_fails_rule_1(self):
        r = _run(FIX / "invalid" / "change-set-determinism-applied-superset")
        self.assertEqual(r.returncode, 1)
        v = _parse_violations(r.stderr)
        rules = {x["rule"] for x in v}
        self.assertIn("change-set-determinism", rules)
        # Rule 1 remediation should name the directional diff (O1)
        rule1 = next(x for x in v if x["rule"] == "change-set-determinism")
        self.assertIn("missing from output", rule1["remediation"])

    # 27 — add-outcome on a non-empty tree exits 2 (C2)
    def test_add_outcome_on_existing_tree_exits_2(self):
        tmp_dir = FIX / "_tmp_dbl_outcome"
        tmp_dir.mkdir(exist_ok=True)
        tree = {"outcome": {"id": "OUT-001", "name": "First"}, "nodes": []}
        (tmp_dir / "input.json").write_text(json.dumps(tree))
        (tmp_dir / "output.json").write_text(json.dumps(tree))
        (tmp_dir / "change-set.json").write_text(json.dumps({
            "actions": [{"op": "add-outcome", "id": "OUT-002", "name": "Second"}],
        }))
        try:
            r = _run(tmp_dir)
            self.assertEqual(r.returncode, 2)
            payload = json.loads(r.stderr)
            self.assertEqual(payload["reason"], "change-set-inconsistent")
        finally:
            for f in tmp_dir.iterdir():
                f.unlink()
            tmp_dir.rmdir()

    # 28 — merge with a single-element ids list exits 2 (F3)
    def test_merge_with_single_element_ids_exits_2(self):
        tmp_dir = FIX / "_tmp_single_merge"
        tmp_dir.mkdir(exist_ok=True)
        tree = {
            "outcome": {"id": "OUT-001", "name": "O"},
            "nodes": [{"id": "OPP-001", "type": "Opportunity", "name": "A",
                       "parent": "OUT-001", "evidence_basis": []}],
        }
        (tmp_dir / "input.json").write_text(json.dumps(tree))
        (tmp_dir / "output.json").write_text(json.dumps(tree))
        (tmp_dir / "change-set.json").write_text(json.dumps({
            "actions": [{"op": "merge", "ids": ["OPP-001"], "into": "OPP-001"}],
        }))
        try:
            r = _run(tmp_dir)
            self.assertEqual(r.returncode, 2)
            payload = json.loads(r.stderr)
            self.assertEqual(payload["reason"], "change-set-inconsistent")
        finally:
            for f in tmp_dir.iterdir():
                f.unlink()
            tmp_dir.rmdir()

    # 29 — malformed merge action (no ids field) exits 2 without crashing (R1)
    def test_malformed_merge_no_ids_exits_2(self):
        tmp_dir = FIX / "_tmp_malformed_merge"
        tmp_dir.mkdir(exist_ok=True)
        tree = {
            "outcome": {"id": "OUT-001", "name": "O"},
            "nodes": [{"id": "OPP-001", "type": "Opportunity", "name": "A",
                       "parent": "OUT-001", "evidence_basis": []}],
        }
        (tmp_dir / "input.json").write_text(json.dumps(tree))
        (tmp_dir / "output.json").write_text(json.dumps(tree))
        (tmp_dir / "change-set.json").write_text(json.dumps({
            "actions": [{"op": "merge"}],
        }))
        try:
            r = _run(tmp_dir)
            self.assertEqual(r.returncode, 2)
            payload = json.loads(r.stderr)
            self.assertEqual(payload["reason"], "change-set-inconsistent")
        finally:
            for f in tmp_dir.iterdir():
                f.unlink()
            tmp_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
