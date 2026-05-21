#!/usr/bin/env python3
"""
check-done.py — Enforce work-loop phase transitions.

Usage:
    tools/check-done.py --phase {plan,verify,review} --feature <slug>

Exits 0 when the named phase's gate conditions are satisfied for the given
spec, non-zero otherwise. On non-zero, prints a one-line reason to stderr.

Reads state from docs/specs/<feature>/state.json (gitignored, per-session).

The work-loop SKILL.md is the authoritative description of what each phase
gate means; this script is the mechanical implementation. If the two
disagree, the SKILL wins and this script is a bug.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = REPO_ROOT / "docs" / "specs"


def load_state(feature: str) -> dict:
    state_path = SPECS_DIR / feature / "state.json"
    if not state_path.exists():
        sys.exit(_fail(f"no state.json at {state_path.relative_to(REPO_ROOT)} — "
                       f"run the work-loop PLAN phase first"))
    try:
        return json.loads(state_path.read_text())
    except json.JSONDecodeError as e:
        sys.exit(_fail(f"state.json malformed: {e}"))


def _fail(msg: str) -> int:
    print(f"check-done: {msg}", file=sys.stderr)
    return 1


def gate_plan(state: dict, feature: str) -> int:
    """Plan gate. Plan is approved iff plan_review_status == 'approved'."""
    status = state.get("plan_review_status", "pending")
    if status == "approved":
        return 0
    return _fail(
        f"plan not approved (plan_review_status={status!r}); "
        f"run adversarial-reviewer against docs/specs/{feature}/spec.md "
        f"and docs/specs/{feature}/plan.md, address findings, then set "
        f"plan_review_status to 'approved' in state.json"
    )


def gate_verify(state: dict, feature: str) -> int:
    """Verify gate. Plan must be approved AND no consecutive same errors over threshold."""
    plan_status = state.get("plan_review_status", "pending")
    if plan_status != "approved":
        return _fail(
            f"verify requires plan_review_status='approved', got {plan_status!r}"
        )
    same_errs = state.get("consecutive_same_error_count", 0)
    same_thresh = state.get("consecutive_same_error_threshold", 3)
    if same_errs >= same_thresh:
        return _fail(
            f"verify gates have failed with the same error {same_errs} times "
            f"(threshold {same_thresh}) — stop and re-plan; do not retry"
        )
    return 0


def gate_review(state: dict, feature: str) -> int:
    """Review gate. Iteration cap, fingerprint stasis, token budget."""
    plan_status = state.get("plan_review_status", "pending")
    if plan_status != "approved":
        return _fail(
            f"review requires plan_review_status='approved', got {plan_status!r}"
        )

    iter_count = state.get("iteration_count", 0)
    max_iter = state.get("max_iterations", 5)
    if iter_count >= max_iter:
        return _fail(
            f"iteration cap hit ({iter_count}/{max_iter}) — STOP and surface "
            f"to the human; do not grind. Re-plan, split the spec, or accept "
            f"open findings explicitly."
        )

    token_used = state.get("token_budget_used_pct", 0)
    token_cap = state.get("token_budget_cap_pct", 80)
    if token_used >= token_cap:
        return _fail(
            f"token budget hit ({token_used}%/{token_cap}%) — stop the loop "
            f"and either /clear or split the work"
        )

    current = set(state.get("finding_fingerprints", []))
    previous = set(state.get("previous_finding_fingerprints", []))
    if current and current == previous:
        return _fail(
            f"finding stasis: the reviewer returned the same findings two "
            f"iterations running — stop and surface to the human"
        )

    # Allow proceeding when there are no findings (clean review) OR findings
    # have changed (loop is making progress). The orchestrator is responsible
    # for emptying finding_fingerprints when review passes clean.
    if current:
        return _fail(
            f"review has {len(current)} unaddressed findings — back to EXECUTE"
        )

    return 0


GATES = {
    "plan": gate_plan,
    "verify": gate_verify,
    "review": gate_review,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phase",
        required=True,
        choices=sorted(GATES.keys()),
        help="Which phase gate to check",
    )
    parser.add_argument(
        "--feature",
        required=True,
        help="Spec slug (the directory name under docs/specs/)",
    )
    args = parser.parse_args()

    state = load_state(args.feature)
    return GATES[args.phase](state, args.feature)


if __name__ == "__main__":
    sys.exit(main())
