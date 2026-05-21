#!/usr/bin/env python3
"""audit-completeness.py — Promote /audit-completeness prose to a runnable script (F1.5).

Walks the 25-item ontology §41 pre-engineering-handoff checklist against a
named initiative or handoff packet. Item 24 splits into 24a (approvals
identified) and 24b (approvals obtained) → 26 check functions for 25
numbered items.

Single source of truth: `.claude/commands/audit-completeness.md`.

Exit codes (per command-file thresholds):
  0 pass: all 25 items [x], traceability clean, all required approvals obtained
  1 needs-fixes: ≤5 items [!] or [ ], no traceability breaks, ≤2 approvals out
  2 block: worse than needs-fixes, OR traceability broken, OR initiative without packet, OR orphaned packet (no parent_initiative)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.graph import build  # noqa: E402
from scripts.lib.frontmatter import parse_file  # noqa: E402


@dataclass
class CheckResult:
    item_id: str
    title: str
    status: str  # pass | weak | fail
    evidence: str


# 26 check functions for the 25-item ontology §41 checklist.
# Each returns (status, evidence).
# Item text is the SSOT per `.claude/commands/audit-completeness.md`.

def _check_present(packet: dict, key: str, label: str):
    v = packet.get(key)
    if v:
        return ("pass", f"{key} present")
    return ("fail", f"{key} missing")


def _resolve_packet(target_slug: str, root: Path):
    """Find the handoff packet for the target. Returns (packet_dict, packet_dir, kind)
    where kind is 'packet' | 'initiative-no-packet' | 'not-found'."""
    pkt_dir = root / "delivery" / "handoff-packets" / target_slug
    if pkt_dir.is_dir():
        readmes = list(pkt_dir.glob("README*"))
        if readmes:
            # If multiple, use most-recently modified
            readmes.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            fm = parse_file(readmes[0])
            if fm:
                return fm.data, pkt_dir, "packet"
    init_dir = root / "delivery" / "initiatives" / target_slug
    if init_dir.is_dir():
        return None, init_dir, "initiative-no-packet"
    return None, None, "not-found"


CHECKS = {
    f"item-{i:02d}": lambda pkt, key=k, title=t: _check_present(pkt, key, title)
    for i, (k, t) in enumerate([
        ("business_objective", "Business objective named"),
        ("customer_segment", "Customer segment defined"),
        ("personas", "Personas linked"),
        ("problem", "Validated problem statement"),
        ("jobs_to_be_done", "Jobs-to-be-done"),
        ("current_workflow", "Current workflow"),
        ("future_workflow", "Future workflow"),
        ("use_cases", "Use cases"),
        ("capabilities", "Capabilities listed"),
        ("features", "Features"),
        ("requirements", "Requirements with frontmatter"),
        ("business_rules", "Business rules"),
        ("policy_constraints", "Policy constraints"),
        ("acceptance_criteria", "Acceptance criteria per requirement"),
        ("non_functional_requirements", "NFRs"),
        ("risks", "Risks with mitigations"),
        ("dependencies", "Dependencies"),
        ("open_questions", "Open questions"),
        ("out_of_scope", "Out of scope"),
        ("decision_log", "Decision log"),
        ("launch_considerations", "Launch considerations"),
        ("success_metrics", "Success metrics with thresholds"),
        ("human_owned_decisions", "Human-owned decisions"),
    ], start=1)
}
# Item 24 split
def _check_24a(pkt):
    v = pkt.get("approvals_identified") or pkt.get("required_approvals")
    if v:
        return ("pass", "approvals identified")
    return ("fail", "required approvals not identified")


def _check_24b(pkt):
    obtained = pkt.get("approvals_obtained")
    required = pkt.get("required_approvals") or pkt.get("approvals_identified")
    if not required:
        return ("weak", "no required approvals declared (24a not satisfied)")
    if obtained and isinstance(obtained, list) and len(obtained) > 0:
        return ("pass", f"{len(obtained)} approvals obtained")
    return ("fail", "approvals identified but none obtained")


def _check_25(pkt):
    if pkt.get("traceability_complete") or pkt.get("traceability_audit_passed"):
        return ("pass", "traceability audit linked")
    return ("weak", "traceability audit not linked (run /audit-traceability)")


CHECKS["item-24a"] = _check_24a
CHECKS["item-24b"] = _check_24b
CHECKS["item-25"] = _check_25
# Remove the original item-24 (since we split it) — recompute keys
if "item-24" in CHECKS:
    del CHECKS["item-24"]


@dataclass
class Report:
    date: str
    target: str
    items_checked: int
    items_passed: int
    items_weak: int
    items_missing: int
    verdict: str
    diagnostic: str
    results: list


def render_markdown(rep: Report) -> str:
    lines = [
        "---",
        f"date: {rep.date}",
        f"target: {rep.target}",
        f"items_checked: {rep.items_checked}",
        f"items_passed: {rep.items_passed}",
        f"items_weak: {rep.items_weak}",
        f"items_missing: {rep.items_missing}",
        f"verdict: {rep.verdict}",
        "object_type: Audit Report",
        "status: Draft",
        f"last_updated: {rep.date}",
        "---",
        "",
        f"# Completeness audit — {rep.target}",
        "",
        f"**Verdict:** {rep.verdict}",
        "",
    ]
    if rep.diagnostic:
        lines.extend([f"**Diagnostic:** {rep.diagnostic}", ""])
    if rep.results:
        lines.append("## Checklist\n")
        for r in rep.results:
            mark = {"pass": "[x]", "weak": "[!]", "fail": "[ ]"}.get(r.status, "[?]")
            lines.append(f"- {mark} {r.item_id}: {r.title} — {r.evidence}")
    return "\n".join(lines)


def render_json(rep: Report) -> str:
    return json.dumps({
        "frontmatter": {
            "date": rep.date, "target": rep.target,
            "items_checked": rep.items_checked,
            "items_passed": rep.items_passed,
            "items_weak": rep.items_weak,
            "items_missing": rep.items_missing,
            "verdict": rep.verdict,
        },
        "diagnostic": rep.diagnostic,
        "results": [asdict(r) for r in rep.results],
    }, indent=2)


def _run_traceability_subaudit(root: Path, scope: str):
    """Subprocess-invoke F1.4 against the target's scope."""
    script = REPO_ROOT / "scripts" / "audit-traceability.py"
    if not script.exists():
        return None
    result = subprocess.run(
        [sys.executable, str(script), "--root", str(root), "--scope", scope, "--format", "json"],
        capture_output=True, text=True,
    )
    try:
        return json.loads(result.stdout), result.returncode
    except Exception:
        return None, result.returncode


def audit(target: str, root: Path):
    pkt_fm, pkt_dir, kind = _resolve_packet(target, root)
    if kind == "not-found":
        rep = Report(
            date=str(date.today()), target=target, items_checked=0,
            items_passed=0, items_weak=0, items_missing=0,
            verdict="block", diagnostic=f"target '{target}' not found at delivery/handoff-packets/ or delivery/initiatives/",
            results=[],
        )
        return rep, 2, None
    if kind == "initiative-no-packet":
        rep = Report(
            date=str(date.today()), target=target, items_checked=0,
            items_passed=0, items_weak=0, items_missing=0,
            verdict="block",
            diagnostic=f"no handoff packet found at delivery/handoff-packets/{target}/; checklist cannot be evaluated",
            results=[],
        )
        return rep, 2, pkt_dir

    # Orphaned packet check
    if not pkt_fm.get("parent_initiative"):
        rep = Report(
            date=str(date.today()), target=target, items_checked=0,
            items_passed=0, items_weak=0, items_missing=0,
            verdict="block",
            diagnostic=f"handoff packet at {target} has no parent_initiative; orphaned",
            results=[],
        )
        return rep, 2, pkt_dir

    # Run all 26 checks
    results = []
    for item_id, fn in sorted(CHECKS.items()):
        status, evidence = fn(pkt_fm)
        # Derive title from the function source via key mapping (simplified)
        results.append(CheckResult(item_id=item_id, title=item_id, status=status, evidence=evidence))

    items_passed = sum(1 for r in results if r.status == "pass")
    items_weak = sum(1 for r in results if r.status == "weak")
    items_missing = sum(1 for r in results if r.status == "fail")

    # Traceability sub-audit
    sub = _run_traceability_subaudit(root, target)
    if sub is not None:
        _, sub_code = sub if isinstance(sub, tuple) else (sub, 0)
        if sub_code == 2:
            verdict = "block"
            code = 2
        elif items_missing > 5 or items_weak > 5:
            verdict = "block"
            code = 2
        elif items_missing == 0 and items_weak == 0:
            verdict = "pass"
            code = 0
        else:
            verdict = "needs-fixes"
            code = 1
    else:
        if items_missing > 5:
            verdict = "block"
            code = 2
        elif items_missing == 0 and items_weak == 0:
            verdict = "pass"
            code = 0
        else:
            verdict = "needs-fixes"
            code = 1

    rep = Report(
        date=str(date.today()), target=target,
        items_checked=len(results), items_passed=items_passed,
        items_weak=items_weak, items_missing=items_missing,
        verdict=verdict, diagnostic="", results=results,
    )
    return rep, code, pkt_dir


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", required=True)
    p.add_argument("--root", default=".")
    p.add_argument("--format", default="markdown", choices=["markdown", "json"])
    p.add_argument("--write", action="store_true")
    args = p.parse_args()
    root = Path(args.root).resolve()
    rep, code, pkt_dir = audit(args.target, root)
    out = render_json(rep) if args.format == "json" else render_markdown(rep)
    if args.write and pkt_dir is not None:
        pkt_dir.mkdir(parents=True, exist_ok=True)
        (pkt_dir / f"completeness-audit-{rep.date}.md").write_text(render_markdown(rep))
        log_path = pkt_dir.parent / "AUDIT-LOG.md"
        if not log_path.exists():
            log_path.write_text("# Completeness audit log\n\n")
        with log_path.open("a") as f:
            f.write(
                f"- {rep.date} target={rep.target} verdict={rep.verdict} "
                f"passed={rep.items_passed} missing={rep.items_missing}\n"
            )
    print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
