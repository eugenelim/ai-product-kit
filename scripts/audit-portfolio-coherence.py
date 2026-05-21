#!/usr/bin/env python3
"""audit-portfolio-coherence.py — Promote /audit-portfolio-coherence prose to a runnable script (F1.6).

Pairwise Rumelt coherence check across active Strategic Intents, Initiatives,
and Visions. Classifies each pair on three axes (resources / capabilities /
market_posture). Tightened-coherent / richer sequencing deferred to D11; this
script implements the skill as currently written:

- coherent: reinforces on ≥2 axes, neutral on the third
- adjacent: reinforces on 1 axis, neutral on others
- drifting: contradicts on 1 axis, neutral on others
- incoherent: contradicts on ≥2 axes
- sequenced: at least one of the pair declares sequencing_after — short-circuit
- unknown: all axes unknown

Exit codes (per command-file thresholds):
  0 clean: 0 contradictions
  1 drift: 1-2 contradictions or any drifting pair
  2 incoherent: ≥3 contradictions or any unmitigated incoherent pair
  3 no-portfolio: 0 artifacts in scope
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.graph import build  # noqa: E402


ACTIVE_TYPES = {"Strategic Intent", "Initiative", "Vision"}
INACTIVE_STATUSES = {"Deprecated", "killed", "done"}


@dataclass
class PairResult:
    a: str
    b: str
    axes: dict
    label: str
    rationale: str


@dataclass
class Report:
    date: str
    artifacts_audited: int
    pairs_checked: int
    contradictions_flagged: int
    verdict: str
    pairs: list


def _classify_axis(a_claim, b_claim) -> str:
    if not a_claim or not b_claim:
        return "unknown"
    # Naive overlap check: if the claim strings share keywords → reinforces.
    a_str = str(a_claim).lower()
    b_str = str(b_claim).lower()
    if a_str == b_str:
        return "reinforces"
    a_words = set(a_str.split())
    b_words = set(b_str.split())
    if a_words & b_words:
        return "reinforces"
    return "contradicts"


def classify_pair(a: dict, b: dict) -> dict:
    return {
        "resources": _classify_axis(a.get("resource_claims"), b.get("resource_claims")),
        "capabilities": _classify_axis(a.get("capability_focus"), b.get("capability_focus")),
        "market_posture": _classify_axis(a.get("market_posture"), b.get("market_posture")),
    }


def label_pair(a: dict, b: dict, axes: dict) -> str:
    # Sequencing short-circuit
    if a.get("sequencing_after") or b.get("sequencing_after"):
        return "sequenced"
    vals = list(axes.values())
    contradicts = vals.count("contradicts")
    reinforces = vals.count("reinforces")
    unknowns = vals.count("unknown")
    if unknowns == 3:
        return "unknown"
    if contradicts >= 2:
        return "incoherent"
    if contradicts == 1:
        return "drifting"
    if reinforces >= 2:
        return "coherent"
    if reinforces == 1:
        return "adjacent"
    return "unknown"


def discover_active(graph) -> list:
    out = []
    for n in graph.nodes.values():
        if n.object_type not in ACTIVE_TYPES:
            continue
        if n.status in INACTIVE_STATUSES:
            continue
        out.append(n)
    return out


def verdict_for(pairs):
    contradictions = sum(1 for p in pairs if p.label == "incoherent")
    drifting = sum(1 for p in pairs if p.label == "drifting")
    if contradictions >= 1:  # any incoherent pair is bad
        if contradictions >= 3:
            return "incoherent", 2, contradictions
        return "incoherent", 2, contradictions
    if drifting >= 1:
        return "drift", 1, drifting
    return "clean", 0, 0


def render_markdown(rep: Report) -> str:
    lines = [
        "---",
        f"date: {rep.date}",
        f"artifacts_audited: {rep.artifacts_audited}",
        f"pairs_checked: {rep.pairs_checked}",
        f"contradictions_flagged: {rep.contradictions_flagged}",
        f"verdict: {rep.verdict}",
        "object_type: Audit Report",
        "status: Draft",
        f"last_updated: {rep.date}",
        "human_owned_decisions:",
        "  - Remediation choice per contradiction (resolve / sequence / kill)",
        "---",
        "",
        f"# Portfolio coherence audit",
        "",
        f"**Verdict:** {rep.verdict}",
        "",
    ]
    if rep.pairs:
        lines.append("## Pairs\n")
        for p in rep.pairs:
            lines.append(f"- {p.a} ↔ {p.b}: {p.label} — {p.rationale}")
    return "\n".join(lines)


def render_json(rep: Report) -> str:
    return json.dumps({
        "frontmatter": {
            "date": rep.date,
            "artifacts_audited": rep.artifacts_audited,
            "pairs_checked": rep.pairs_checked,
            "contradictions_flagged": rep.contradictions_flagged,
            "verdict": rep.verdict,
        },
        "pairs": [asdict(p) for p in rep.pairs],
    }, indent=2)


def audit(root: Path):
    graph = build(root)
    active = discover_active(graph)
    if len(active) == 0:
        return Report(
            date=str(date.today()), artifacts_audited=0,
            pairs_checked=0, contradictions_flagged=0,
            verdict="no-portfolio", pairs=[],
        ), 3
    if len(active) == 1:
        return Report(
            date=str(date.today()), artifacts_audited=1,
            pairs_checked=0, contradictions_flagged=0,
            verdict="clean", pairs=[],
        ), 0
    if len(active) > 10:
        print(f"warning: portfolio size {len(active)} > 10; consider fan-out (D13)",
              file=sys.stderr)
    pairs = []
    for a, b in itertools.combinations(active, 2):
        axes = classify_pair(a.frontmatter, b.frontmatter)
        label = label_pair(a.frontmatter, b.frontmatter, axes)
        rationale_parts = [
            f"{axis}: {v}" for axis, v in axes.items() if v != "unknown"
        ]
        rationale = "; ".join(rationale_parts) if rationale_parts else "all axes unknown"
        pairs.append(PairResult(
            a=a.id, b=b.id, axes=axes, label=label, rationale=rationale,
        ))
    verdict, code, contradictions = verdict_for(pairs)
    rep = Report(
        date=str(date.today()),
        artifacts_audited=len(active),
        pairs_checked=len(pairs),
        contradictions_flagged=contradictions,
        verdict=verdict,
        pairs=pairs,
    )
    return rep, code


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=".")
    p.add_argument("--format", default="markdown", choices=["markdown", "json"])
    p.add_argument("--write", action="store_true")
    args = p.parse_args()
    root = Path(args.root).resolve()
    rep, code = audit(root)
    out = render_json(rep) if args.format == "json" else render_markdown(rep)
    if args.write:
        d = root / "strategy" / "diagnoses"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{rep.date}-coherence-audit.md").write_text(render_markdown(rep))
        log_path = d / "COHERENCE-LOG.md"
        if not log_path.exists():
            log_path.write_text("# Coherence audit log\n\n")
        with log_path.open("a") as f:
            f.write(
                f"- {rep.date} artifacts={rep.artifacts_audited} "
                f"verdict={rep.verdict} contradictions={rep.contradictions_flagged}\n"
            )
    print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
