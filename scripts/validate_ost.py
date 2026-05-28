#!/usr/bin/env python3
"""
validate_ost.py — Validate an Opportunity Solution Tree change set.

Usage:
    python scripts/validate_ost.py \\
        --input <input-tree.json> \\
        --output <output-tree.json> \\
        --change-set <change-set.json> \\
        [--schema <schema.json>] \\
        [--format json|human]

Exit codes:
    0 — pass
    1 — rule violation (see the six rules below)
    2 — input error (missing file, malformed JSON, schema violation, change-set internally inconsistent)

The six validation rules, matching `.claude/skills/ost-validator/SKILL.md`:
    1. change-set-determinism — applying actions to input produces output node-for-node
    2. no-orphans — every non-root node has a parent in the output
    3. no-double-references — each IS-NNN source opportunity appears under exactly one Opportunity
    4. no-data-loss — every IS-NNN reference and every child of the input is accounted for in the output
    5. valid-action-vocabulary — every action `op` is in the canonical 9-verb set
    6. compound-operation-visibility — sources moved between Opportunities require merge/split

JSON-input contract: all three of --input, --output, --change-set are JSON files.
Markdown OSTs (templates/ost.md) must be projected to JSON before invoking this script;
the projection is the responsibility of the calling command (e.g., /generate-ost,
/update-ost). See docs/specs/phase-2-discovery-primitives/spec.md §"Open questions".
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

# Python version guard. `from __future__ import annotations` makes function
# signatures lazy but variable annotations (`x: set[str] = ...`) are evaluated
# at runtime on Python < 3.9. The kit's minimum is 3.9 — declared here and in
# pyproject.toml.
if sys.version_info < (3, 9):
    sys.exit(
        "validate_ost: Python 3.9+ required; got "
        f"{sys.version_info.major}.{sys.version_info.minor}"
    )

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA = REPO_ROOT / ".claude" / "skills" / "ost-validator" / "references" / "ost-schema.json"

VALID_OPS = {
    "add-outcome",
    "add-opportunity",
    "add-solution",
    "reframe",
    "merge",
    "split",
    "delete",
    "reparent",
    "add-source-opportunity",
}

NODE_TYPES = {"Opportunity", "Solution", "AssumptionTest"}
IS_PREFIX = "IS-"


# ---------- I/O ---------------------------------------------------------------


def _load_json(path: str, label: str) -> Any:
    p = Path(path)
    if not p.exists():
        _emit_error("missing-file", f"{label} file not found: {path}")
        sys.exit(2)
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as e:
        _emit_error("malformed-json", f"{label} file is not valid JSON ({path}): {e}")
        sys.exit(2)


def _emit_error(reason: str, detail: str) -> None:
    payload = {"verdict": "error", "reason": reason, "detail": detail}
    if _FORMAT == "human":
        print(f"validate_ost: {reason}: {detail}", file=sys.stderr)
    else:
        print(json.dumps(payload), file=sys.stderr)


def _emit_failure(violations: list[dict]) -> None:
    if _FORMAT == "human":
        # one paragraph naming the first violation's rule + remediation
        v = violations[0]
        para = (
            f"Validation failed: rule {v['rule']} on node {v.get('node_id', '?')}. "
            f"{v['remediation']} "
            f"{len(violations) - 1} additional violation(s) elided; re-run with --format json for the full report."
        )
        print(para, file=sys.stderr)
    else:
        print(json.dumps({"verdict": "fail", "violations": violations}), file=sys.stderr)


def _emit_pass(node_count: int, action_count: int) -> None:
    if _FORMAT == "human":
        print(f"Validation passed ({node_count} nodes, {action_count} actions).")
    # json default: silent on both streams


# ---------- schema validation (top-level shape only) -------------------------


def _validate_schema(doc: Any, schema: dict, root: str) -> str | None:
    """Returns an error string when doc fails the top-level schema, else None."""
    defs = schema.get("definitions", {})
    sub = defs.get(root)
    if sub is None:
        return f"schema has no definition for {root!r}"
    return _check(doc, sub, path=f"<{root}>")


def _check(doc: Any, sch: dict, path: str) -> str | None:
    t = sch.get("type")
    if t == "object":
        if not isinstance(doc, dict):
            return f"{path}: expected object, got {type(doc).__name__}"
        for req in sch.get("required", []):
            if req not in doc:
                return f"{path}: missing required field {req!r}"
        props = sch.get("properties", {})
        addl = sch.get("additionalProperties", True)
        for k, v in doc.items():
            if k in props:
                err = _check(v, props[k], path=f"{path}.{k}")
                if err:
                    return err
            elif addl is False:
                return f"{path}: unexpected field {k!r}"
        return None
    if t == "array":
        if not isinstance(doc, list):
            return f"{path}: expected array, got {type(doc).__name__}"
        items = sch.get("items")
        if items:
            for i, item in enumerate(doc):
                err = _check(item, items, path=f"{path}[{i}]")
                if err:
                    return err
        return None
    if t == "string":
        if not isinstance(doc, str):
            return f"{path}: expected string, got {type(doc).__name__}"
        enum = sch.get("enum")
        if enum and doc not in enum:
            return f"{path}: value {doc!r} not in enum {enum}"
        return None
    if "oneOf" in sch:
        # any branch that validates is fine
        for branch in sch["oneOf"]:
            if _check(doc, branch, path) is None:
                return None
        return f"{path}: value {doc!r} did not match any oneOf branch"
    return None  # unknown type: don't constrain


# ---------- per-node-type validation ------------------------------------------


def _validate_node_types(tree: dict) -> str | None:
    for n in tree.get("nodes", []):
        ntype = n.get("type")
        if ntype not in NODE_TYPES:
            return f"node {n.get('id', '?')!r}: type {ntype!r} not in {sorted(NODE_TYPES)}"
        if ntype == "Opportunity" and "evidence_basis" not in n:
            return f"Opportunity {n.get('id', '?')!r} missing required field evidence_basis"
        if ntype == "AssumptionTest" and "threshold" not in n:
            return f"AssumptionTest {n.get('id', '?')!r} missing required field threshold"
    return None


# ---------- change-set internal consistency -----------------------------------


def _check_change_set_consistency(input_tree: dict, change_set: dict) -> Optional[str]:
    known_ids: Set[str] = {input_tree["outcome"]["id"]} if input_tree.get("outcome", {}).get("id") else set()
    known_ids.update(n["id"] for n in input_tree.get("nodes", []))
    outcome_present = bool(input_tree.get("outcome", {}).get("id"))
    for i, a in enumerate(change_set.get("actions", [])):
        op = a.get("op")
        # Validate references; new ids get added as actions are walked. Also
        # validate per-action required sub-fields here — schema enforces only
        # top-level shape (presence of `op`), so per-op field requirements live
        # in code. A malformed action is exit 2 (input error), not exit 1.
        if op == "add-outcome":
            if "id" not in a or "name" not in a:
                return f"action[{i}] add-outcome requires id and name"
            if outcome_present:
                # add-outcome on a tree that already has an Outcome would
                # silently overwrite the root; the vocabulary doc forbids this.
                return f"action[{i}] add-outcome used on a tree that already has an Outcome (id={input_tree['outcome']['id']!r}); use reframe to rename"
            known_ids.add(a["id"])
            outcome_present = True
        elif op in {"add-opportunity", "add-solution"}:
            if "id" not in a or "name" not in a or "parent" not in a:
                return f"action[{i}] {op} requires id, name, parent"
            # Parent existence is NOT a consistency error — Rule 2 (no-orphans)
            # catches missing parents on the resulting tree. This keeps the
            # consistency check focused on actions that cannot be applied at all
            # (merge / split / delete / reframe / add-source-opportunity targeting
            # nodes that aren't there).
            known_ids.add(a["id"])
        elif op == "reframe":
            if "id" not in a or "name" not in a:
                return f"action[{i}] reframe requires id and name"
            if a["id"] not in known_ids:
                return f"action[{i}] reframe references unknown id {a['id']!r}"
        elif op == "merge":
            if "ids" not in a or "into" not in a:
                return f"action[{i}] merge requires ids[] and into"
            ids = a["ids"]
            if not isinstance(ids, list) or len(ids) < 2:
                return f"action[{i}] merge requires ids[] with at least 2 entries; got {ids!r}"
            for j in ids:
                if j not in known_ids:
                    return f"action[{i}] merge references unknown id {j!r}"
            into = a["into"]
            if into not in ids:
                return f"action[{i}] merge into={into!r} not in ids={ids}"
            # remove merged-not-into from known_ids (they're consumed by the merge)
            for j in ids:
                if j != into and j in known_ids:
                    known_ids.discard(j)
        elif op == "split":
            if "id" not in a or "into" not in a:
                return f"action[{i}] split requires id and into[]"
            if a["id"] not in known_ids:
                return f"action[{i}] split references unknown id {a['id']!r}"
            into = a["into"]
            if not isinstance(into, list) or len(into) != 2:
                return f"action[{i}] split requires into[] of exactly 2 ids; got {into!r}"
            known_ids.discard(a["id"])
            known_ids.update(into)
        elif op == "delete":
            if "id" not in a:
                return f"action[{i}] delete requires id"
            if a["id"] not in known_ids:
                return f"action[{i}] delete references unknown id {a['id']!r}"
            known_ids.discard(a["id"])
        elif op == "reparent":
            if "id" not in a or "new_parent" not in a:
                return f"action[{i}] reparent requires id and new_parent"
            if a["id"] not in known_ids:
                return f"action[{i}] reparent references unknown id {a['id']!r}"
            # new_parent existence is checked by Rule 2 (no-orphans) on the resulting tree
        elif op == "add-source-opportunity":
            if "id" not in a or "target" not in a:
                return f"action[{i}] add-source-opportunity requires id and target"
            if a["target"] not in known_ids:
                return f"action[{i}] add-source-opportunity references unknown target {a['target']!r}"
        # Unknown op: Rule 5 will catch it later; not a consistency error.
    return None


# ---------- _apply_change_set (pure transformation) ---------------------------


def _apply_change_set(input_tree: dict, change_set: dict) -> dict:
    """Apply actions to input_tree. Returns a new dict. Pure function.

    Precondition: _check_change_set_consistency has already run clean against
    the same change_set, so every action's required fields are present and
    every referenced id exists at the point it's referenced.
    """
    tree = copy.deepcopy(input_tree)
    for a in change_set.get("actions", []):
        op = a.get("op")
        if op == "add-outcome":
            tree["outcome"] = {"id": a["id"], "name": a["name"]}
        elif op == "add-opportunity":
            tree["nodes"].append({
                "id": a["id"], "type": "Opportunity", "name": a["name"],
                "parent": a["parent"], "evidence_basis": [],
            })
        elif op == "add-solution":
            tree["nodes"].append({
                "id": a["id"], "type": "Solution", "name": a["name"], "parent": a["parent"],
            })
        elif op == "reframe":
            for n in tree["nodes"]:
                if n["id"] == a["id"]:
                    n["name"] = a["name"]
        elif op == "merge":
            ids = a["ids"]
            into = a["into"]
            # union evidence_basis
            union_evidence: List[str] = []
            for n in tree["nodes"]:
                if n["id"] in ids:
                    for ev in n.get("evidence_basis", []):
                        if ev not in union_evidence:
                            union_evidence.append(ev)
            # reparent children of merged-not-into nodes to into
            merged_others = [i for i in ids if i != into]
            for n in tree["nodes"]:
                if n.get("parent") in merged_others:
                    n["parent"] = into
            # remove merged-not-into nodes
            tree["nodes"] = [n for n in tree["nodes"] if n["id"] not in merged_others]
            # assign union to into
            for n in tree["nodes"]:
                if n["id"] == into and n["type"] == "Opportunity":
                    n["evidence_basis"] = union_evidence
        elif op == "split":
            source_id = a["id"]
            into = a["into"]
            source = next((n for n in tree["nodes"] if n["id"] == source_id), None)
            if source is None:
                continue
            # Replace source with two new nodes of same type and parent.
            new_nodes = []
            for i in into:
                copy_node = {"id": i, "type": source["type"], "name": source["name"],
                             "parent": source["parent"]}
                if source["type"] == "Opportunity":
                    copy_node["evidence_basis"] = []
                new_nodes.append(copy_node)
            # remove source if its id is not in `into`
            tree["nodes"] = [n for n in tree["nodes"] if n["id"] != source_id]
            tree["nodes"].extend(new_nodes)
        elif op == "delete":
            tree["nodes"] = [n for n in tree["nodes"] if n["id"] != a["id"]]
        elif op == "reparent":
            for n in tree["nodes"]:
                if n["id"] == a["id"]:
                    n["parent"] = a["new_parent"]
        elif op == "add-source-opportunity":
            for n in tree["nodes"]:
                if n["id"] == a["target"] and n["type"] == "Opportunity":
                    if a["id"] not in n.get("evidence_basis", []):
                        n.setdefault("evidence_basis", []).append(a["id"])
        # Unknown op: Rule 5 will catch it.
    return tree


# ---------- the six rules -----------------------------------------------------


def _rule_5_valid_action_vocabulary(change_set: dict) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    for i, a in enumerate(change_set.get("actions", [])):
        op = a.get("op")
        if op not in VALID_OPS:
            violations.append({
                "rule": "valid-action-vocabulary",
                "node_id": f"action[{i}]",
                "remediation": (
                    f"action #{i} uses op {op!r} which is not in the canonical "
                    f"9-verb vocabulary; valid ops are {sorted(VALID_OPS)}"
                ),
            })
    return violations


def _rule_1_change_set_determinism(applied: dict, output: dict) -> List[Dict[str, Any]]:
    if _trees_equal(applied, output):
        return []
    applied_ids = {n["id"] for n in applied.get("nodes", [])}
    output_ids = {n["id"] for n in output.get("nodes", [])}
    extra_in_output = sorted(output_ids - applied_ids)
    extra_in_applied = sorted(applied_ids - output_ids)
    outcome_diff = applied.get("outcome") != output.get("outcome")
    diff_parts = []
    if extra_in_output:
        diff_parts.append(f"nodes in output not produced by the change set: {extra_in_output}")
    if extra_in_applied:
        diff_parts.append(f"nodes produced by the change set but missing from output: {extra_in_applied}")
    if outcome_diff:
        diff_parts.append(f"outcome differs: applied={applied.get('outcome')!r}, output={output.get('outcome')!r}")
    if not diff_parts:
        diff_parts.append("node-content fields differ (parent, name, or evidence_basis); compare applied tree to output tree")
    return [{
        "rule": "change-set-determinism",
        "node_id": "<tree>",
        "remediation": (
            "applying the change set to the input did not produce the claimed output. "
            + "; ".join(diff_parts) + ". "
            "Either revise the change set to explain how the output is reached, or "
            "correct the output to reflect what the change set actually produces."
        ),
    }]


def _rule_2_no_orphans(output: dict) -> List[Dict[str, Any]]:
    valid_parents: Set[str] = set()
    outcome_id = output.get("outcome", {}).get("id")
    if outcome_id:
        valid_parents.add(outcome_id)
    valid_parents.update(n["id"] for n in output.get("nodes", []))
    violations: List[Dict[str, Any]] = []
    for n in output.get("nodes", []):
        if n.get("parent") not in valid_parents:
            violations.append({
                "rule": "no-orphans",
                "node_id": n["id"],
                "remediation": (
                    f"node {n['id']} has parent {n.get('parent')!r} which does not exist in the output; "
                    f"either add the missing parent or reparent the node."
                ),
            })
    return violations


def _rule_3_no_double_references(output: dict) -> List[Dict[str, Any]]:
    seen: Dict[str, str] = {}
    violations: List[Dict[str, Any]] = []
    for n in output.get("nodes", []):
        if n.get("type") != "Opportunity":
            continue
        for ev in n.get("evidence_basis", []):
            if not ev.startswith(IS_PREFIX):
                continue
            if ev in seen and seen[ev] != n["id"]:
                violations.append({
                    "rule": "no-double-references",
                    "node_id": ev,
                    "remediation": (
                        f"source opportunity {ev} appears under both "
                        f"{seen[ev]} and {n['id']}; remove one reference or "
                        f"merge the two Opportunities."
                    ),
                })
            else:
                seen[ev] = n["id"]
    return violations


def _rule_4_no_data_loss(input_tree: dict, output: dict, change_set: dict) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    # 4a — IS-NNN references: any IS-NNN that appeared in input must appear in output.
    input_is_refs = _collect_is_refs(input_tree)
    output_is_refs = _collect_is_refs(output)
    for ev in input_is_refs:
        if ev not in output_is_refs:
            violations.append({
                "rule": "no-data-loss",
                "node_id": ev,
                "remediation": (
                    f"source opportunity {ev} appeared in the input but is absent from the output; "
                    f"the change set must explicitly transfer it via add-source-opportunity "
                    f"to another Opportunity, or the Opportunity it was attached to must be "
                    f"explicitly preserved."
                ),
            })
    # 4b — child nodes: any input node-id missing from output must be explicitly deleted.
    explicit_deletes = {a.get("id") for a in change_set.get("actions", []) if a.get("op") == "delete"}
    # Also count merges (merged-not-into nodes are implicitly removed) and split sources.
    for a in change_set.get("actions", []):
        if a.get("op") == "merge":
            for i in a.get("ids", []):
                if i != a.get("into"):
                    explicit_deletes.add(i)
        if a.get("op") == "split":
            sid = a.get("id")
            if sid and sid not in a.get("into", []):
                explicit_deletes.add(sid)
    input_ids = {n["id"] for n in input_tree.get("nodes", [])}
    output_ids = {n["id"] for n in output.get("nodes", [])}
    for nid in input_ids - output_ids:
        if nid not in explicit_deletes:
            violations.append({
                "rule": "no-data-loss",
                "node_id": nid,
                "remediation": (
                    f"node {nid} was in the input but is absent from the output, and the "
                    f"change set contains no explicit delete or merge action for it. "
                    f"Add `{{op: delete, id: {nid}}}` or reparent it before deleting its parent."
                ),
            })
    return violations


def _rule_6_compound_operation_visibility(
    input_tree: dict, output: dict, change_set: dict
) -> List[Dict[str, Any]]:
    """If an IS-NNN moved between Opportunities, the change set must contain a merge or split
    involving both the source and target Opportunities."""
    input_map = _is_ref_owners(input_tree)
    output_map = _is_ref_owners(output)
    violations: List[Dict[str, Any]] = []
    merge_split_pairs: Set[Tuple[str, str]] = set()
    for a in change_set.get("actions", []):
        if a.get("op") == "merge":
            ids = a.get("ids", [])
            for i in ids:
                for j in ids:
                    if i != j:
                        merge_split_pairs.add((i, j))
        if a.get("op") == "split":
            sid = a.get("id")
            for i in a.get("into", []):
                merge_split_pairs.add((sid, i))
                merge_split_pairs.add((i, sid))
    for ev, src_opp in input_map.items():
        tgt_opp = output_map.get(ev)
        if tgt_opp is None or tgt_opp == src_opp:
            continue
        if (src_opp, tgt_opp) not in merge_split_pairs:
            violations.append({
                "rule": "compound-operation-visibility",
                "node_id": ev,
                "remediation": (
                    f"source opportunity {ev} moved from {src_opp} to {tgt_opp} but the change "
                    f"set contains no merge or split that explains the move; either add the "
                    f"intermediate operation or revert the move."
                ),
            })
    return violations


# ---------- helpers -----------------------------------------------------------


def _trees_equal(a: dict, b: dict) -> bool:
    # outcome strict equality
    if a.get("outcome") != b.get("outcome"):
        return False
    # nodes: order-insensitive (by id)
    a_nodes = sorted(a.get("nodes", []), key=lambda n: n["id"])
    b_nodes = sorted(b.get("nodes", []), key=lambda n: n["id"])
    if len(a_nodes) != len(b_nodes):
        return False
    for n1, n2 in zip(a_nodes, b_nodes):
        n1c = dict(n1)
        n2c = dict(n2)
        # normalize evidence_basis ordering
        if "evidence_basis" in n1c:
            n1c["evidence_basis"] = sorted(n1c["evidence_basis"])
        if "evidence_basis" in n2c:
            n2c["evidence_basis"] = sorted(n2c["evidence_basis"])
        if n1c != n2c:
            return False
    # chosen_opportunity strict equality if either side has it
    if a.get("chosen_opportunity") != b.get("chosen_opportunity"):
        return False
    return True


def _collect_is_refs(tree: dict) -> Set[str]:
    refs: Set[str] = set()
    for n in tree.get("nodes", []):
        for ev in n.get("evidence_basis", []) or []:
            if ev.startswith(IS_PREFIX):
                refs.add(ev)
    return refs


def _is_ref_owners(tree: dict) -> Dict[str, str]:
    """Returns {is_ref_id: opportunity_id} — first occurrence wins."""
    owners: Dict[str, str] = {}
    for n in tree.get("nodes", []):
        if n.get("type") != "Opportunity":
            continue
        for ev in n.get("evidence_basis", []) or []:
            if ev.startswith(IS_PREFIX) and ev not in owners:
                owners[ev] = n["id"]
    return owners


# ---------- main --------------------------------------------------------------


_FORMAT = "json"  # set by main(); used by _emit_* helpers


def main() -> int:
    global _FORMAT
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", required=True, help="Path to input-tree JSON.")
    parser.add_argument("--output", required=True, help="Path to claimed-output-tree JSON.")
    parser.add_argument("--change-set", required=True, dest="change_set", help="Path to change-set JSON.")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="Override the bundled schema path (testing).")
    parser.add_argument("--format", choices=["json", "human"], default="json", dest="fmt")
    args = parser.parse_args()
    _FORMAT = args.fmt

    # Load all three files (exit 2 on missing-file or malformed-json).
    input_tree = _load_json(args.input, "input")
    output_tree = _load_json(args.output, "output")
    change_set = _load_json(args.change_set, "change-set")

    # Schema validate top-level shape.
    schema = _load_json(args.schema, "schema")
    for doc, root, label in (
        (input_tree, "tree", "input"),
        (output_tree, "tree", "output"),
        (change_set, "change-set", "change-set"),
    ):
        err = _validate_schema(doc, schema, root)
        if err:
            _emit_error("schema-violation", f"{label}: {err}")
            return 2

    # The output tree must have an outcome — the input may be an empty seed
    # tree (no outcome yet) when used by /generate-ost on a fresh strategy, but
    # the claimed output of any change set is a valid OST and must declare its
    # outcome. The schema makes outcome optional to support the empty-seed case;
    # the script enforces "outcome-on-output" as a node-type-style check.
    if not output_tree.get("outcome", {}).get("id"):
        _emit_error("schema-violation", "output: tree must declare an outcome with an id")
        return 2

    # Per-node-type validation (input and output).
    for tree, label in ((input_tree, "input"), (output_tree, "output")):
        err = _validate_node_types(tree)
        if err:
            _emit_error("schema-violation", f"{label}: {err}")
            return 2

    # Rule 5 (valid-action-vocabulary) — run before consistency / apply so an
    # invalid op produces a Rule violation, not a downstream crash.
    rule5 = _rule_5_valid_action_vocabulary(change_set)
    if rule5:
        _emit_failure(rule5)
        return 1

    # Change-set internal consistency (references to nodes that don't exist).
    err = _check_change_set_consistency(input_tree, change_set)
    if err:
        _emit_error("change-set-inconsistent", err)
        return 2

    # Apply.
    applied = _apply_change_set(input_tree, change_set)

    # Run rules. Order: Rule 4 (data loss — more specific diagnosis) before Rule 1
    # (generic determinism) so a "node dropped without delete" reports as Rule 4.
    # This ordering is a load-bearing invariant: reordering it produces correct
    # exit codes but worse remediation messages (Rule 1's generic "trees differ"
    # would mask Rule 4's specific "node dropped without delete").
    violations: List[Dict[str, Any]] = []
    violations.extend(_rule_4_no_data_loss(input_tree, output_tree, change_set))
    violations.extend(_rule_6_compound_operation_visibility(input_tree, output_tree, change_set))
    violations.extend(_rule_2_no_orphans(output_tree))
    violations.extend(_rule_3_no_double_references(output_tree))
    if not violations:
        violations.extend(_rule_1_change_set_determinism(applied, output_tree))

    if violations:
        _emit_failure(violations)
        return 1

    _emit_pass(len(output_tree.get("nodes", [])), len(change_set.get("actions", [])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
