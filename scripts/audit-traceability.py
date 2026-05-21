#!/usr/bin/env python3
"""audit-traceability.py — Promote /audit-traceability prose to a runnable script (F1.4).

Walks the seven traceability rules from `.claude/commands/audit-traceability.md`
across a kit's typed-object graph (built via scripts.lib.graph).

The command file is the single source of truth for rule text; this docstring
carries a semantic copy.

Rules:
  1. Every Requirement must trace to a Capability.
  2. Every Capability must trace to a Problem, Business Objective, or
     Policy Rule (Domain E).
  3. Every Problem must trace to Evidence (or be marked Assumption).
  4. Every KPI must trace to an Outcome.
  5. Every high-risk Requirement (risk_level: High | Critical) must have
     a named Owner and a Mitigation.
  6. Every artifact with object_type: Decision must have decision_owner
     (or named owner) AND a corresponding ADR in docs/adr/.
  7. Every Handoff Packet must identify fixed_vs_flexible.

Cycles map to Rule 1 with violation_type: "cycle".

Exit codes: 0 clean, 1 drift, 2 broken, 3 insufficient-data.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.graph import Graph, Node, build  # noqa: E402


@dataclass
class Violation:
    rule: int
    artifact_id: str
    artifact_path: str
    violation_type: str
    description: str
    remediation: str


@dataclass
class WeakChain:
    chain: list
    weak_link: str
    weakness: str


@dataclass
class Report:
    date: str
    scope: str
    objects_audited: int
    rules_violated: int
    broken_links: int
    weak_chains: list
    weak_chain_count: int
    verdict: str
    violations: list
    orphans: list


def check_rule_1(graph: Graph) -> list:
    out = []
    for req in graph.by_type("Requirement"):
        cap_links = req.frontmatter.get("related_capabilities") or []
        if not isinstance(cap_links, list):
            cap_links = [cap_links]
        has_cap = any(
            str(cid) in graph.nodes
            and graph.nodes[str(cid)].object_type == "Capability"
            for cid in cap_links
        )
        if not has_cap:
            out.append(Violation(
                rule=1, artifact_id=req.id, artifact_path=str(req.path),
                violation_type="missing-link",
                description="Requirement does not trace to a Capability.",
                remediation="Add related_capabilities: [<capability-id>].",
            ))
    for cyc in graph.cycles():
        ids = [n.id for n in cyc]
        out.append(Violation(
            rule=1, artifact_id=ids[0], artifact_path=str(cyc[0].path),
            violation_type="cycle",
            description=f"Cycle among parent_* edges: {' → '.join(ids + [ids[0]])}",
            remediation="Break the cycle by re-rooting one artifact's parent link.",
        ))
    return out


def check_rule_2(graph: Graph) -> list:
    out = []
    ok_types = {"Problem", "Business Objective", "Policy Rule"}
    for cap in graph.by_type("Capability"):
        related = cap.frontmatter.get("related_problems") or []
        if not isinstance(related, list):
            related = [related]
        traced = any(
            (n := graph.nodes.get(str(rid))) is not None and n.object_type in ok_types
            for rid in related
        )
        if not traced:
            for parent in graph.parents_of(cap):
                if parent.object_type in ok_types:
                    traced = True
                    break
        if not traced:
            out.append(Violation(
                rule=2, artifact_id=cap.id, artifact_path=str(cap.path),
                violation_type="missing-link",
                description="Capability does not trace to a Problem, Business Objective, or Policy Rule.",
                remediation="Add related_problems: [<problem-id>] or parent link.",
            ))
    return out


def check_rule_3(graph: Graph) -> list:
    out = []
    for prob in graph.by_type("Problem"):
        evidence = prob.frontmatter.get("evidence_basis")
        if isinstance(evidence, list) and evidence:
            continue
        out.append(Violation(
            rule=3, artifact_id=prob.id, artifact_path=str(prob.path),
            violation_type="missing-evidence",
            description="Problem has no evidence_basis entries.",
            remediation="Add evidence_basis, OR mark object_type: Assumption.",
        ))
    return out


def check_rule_4(graph: Graph) -> list:
    out = []
    for kpi in graph.by_type("KPI"):
        traced = any(p.object_type == "Outcome" for p in graph.parents_of(kpi))
        if not traced:
            related = kpi.frontmatter.get("related_outcomes") or []
            if not isinstance(related, list):
                related = [related]
            traced = any(
                (n := graph.nodes.get(str(rid))) is not None and n.object_type == "Outcome"
                for rid in related
            )
        if not traced:
            out.append(Violation(
                rule=4, artifact_id=kpi.id, artifact_path=str(kpi.path),
                violation_type="missing-link",
                description="KPI does not trace to an Outcome.",
                remediation="Add related_outcomes: [<outcome-id>].",
            ))
    return out


def check_rule_5(graph: Graph) -> list:
    out = []
    for req in graph.by_type("Requirement"):
        if req.frontmatter.get("risk_level") not in ("High", "Critical"):
            continue
        has_owner = bool(req.frontmatter.get("owner"))
        has_mit = bool(
            req.frontmatter.get("mitigation") or req.frontmatter.get("related_mitigations")
        )
        if not has_owner or not has_mit:
            out.append(Violation(
                rule=5, artifact_id=req.id, artifact_path=str(req.path),
                violation_type="missing-owner-or-mitigation",
                description=f"High-risk Requirement missing {'owner' if not has_owner else 'mitigation'}.",
                remediation="Add owner: <name> and mitigation: <description>.",
            ))
    return out


def check_rule_6(graph: Graph) -> list:
    out = []
    adr_dir = REPO_ROOT / "docs" / "adr"
    adr_files = {p.name for p in adr_dir.glob("*.md")} if adr_dir.is_dir() else set()
    for dec in graph.by_type("Decision"):
        owner = dec.frontmatter.get("decision_owner") or dec.frontmatter.get("owner")
        has_owner = bool(owner) and owner not in ("TBD", "<TBD>")
        has_adr = any(dec.id in name or (dec.slug and dec.slug in name) for name in adr_files)
        if not has_owner or not has_adr:
            out.append(Violation(
                rule=6, artifact_id=dec.id, artifact_path=str(dec.path),
                violation_type="missing-owner-or-adr",
                description=f"Decision missing {'decision_owner' if not has_owner else 'ADR'}.",
                remediation="Add decision_owner: <name> and create docs/adr/NNNN-<slug>.md.",
            ))
    return out


def check_rule_7(graph: Graph) -> list:
    out = []
    for hop in graph.by_type("Handoff Packet"):
        ffu = hop.frontmatter.get("fixed_vs_flexible")
        if isinstance(ffu, dict) and any(k in ffu for k in ("fixed", "flexible", "unknown")):
            continue
        out.append(Violation(
            rule=7, artifact_id=hop.id, artifact_path=str(hop.path),
            violation_type="missing-fixed-flexible-unknown",
            description="Handoff Packet missing fixed_vs_flexible.",
            remediation="Add fixed_vs_flexible: {fixed: [...], flexible: [...], unknown: [...]}.",
        ))
    return out


def assess_weak_chains(graph: Graph) -> list:
    out = []
    for prob in graph.by_type("Problem"):
        evidence = prob.frontmatter.get("evidence_basis")
        if not isinstance(evidence, list):
            continue
        for ev in evidence:
            if isinstance(ev, dict) and ev.get("strength") == "Weak":
                out.append(WeakChain(
                    chain=[prob.id, ev.get("source", "<unknown>")],
                    weak_link=prob.id,
                    weakness="evidence_basis: Weak",
                ))
    return out


def verdict_for(objects_audited: int, broken_links: int, weak_pct: float):
    if objects_audited < 3:
        return "insufficient-data", 3
    if broken_links == 0 and weak_pct <= 10.0:
        return "clean", 0
    if broken_links > 3 or weak_pct > 25.0:
        return "broken", 2
    return "drift", 1


def render_markdown(report: Report) -> str:
    lines = [
        "---",
        f"date: {report.date}",
        f"scope: {report.scope}",
        f"objects_audited: {report.objects_audited}",
        f"rules_violated: {report.rules_violated}",
        f"broken_links: {report.broken_links}",
        f"weak_chains: {report.weak_chain_count}",
        f"verdict: {report.verdict}",
        "object_type: Audit Report",
        "status: Draft",
        f"last_updated: {report.date}",
        "---",
        "",
        f"# Traceability audit — {report.scope}",
        "",
        f"**Verdict:** {report.verdict}",
        "",
    ]
    if report.violations:
        lines.append("## Rule violations\n")
        for v in report.violations:
            lines.append(f"- **Rule {v.rule}** ({v.violation_type}) — {v.artifact_id}")
            lines.append(f"  - {v.description}")
            lines.append(f"  - Fix: {v.remediation}")
        lines.append("")
    if report.weak_chains:
        lines.append("## Weak chains\n")
        for wc in report.weak_chains:
            lines.append(f"- {wc.weak_link} — {wc.weakness}")
        lines.append("")
    if report.orphans:
        lines.append("## Orphans\n")
        for o in report.orphans:
            lines.append(f"- {o}")
        lines.append("")
    return "\n".join(lines)


def render_json(report: Report) -> str:
    return json.dumps({
        "frontmatter": {
            "date": report.date,
            "scope": report.scope,
            "objects_audited": report.objects_audited,
            "rules_violated": report.rules_violated,
            "broken_links": report.broken_links,
            "weak_chains": report.weak_chain_count,
            "verdict": report.verdict,
        },
        "violations": [asdict(v) for v in report.violations],
        "weak_chains_detail": [asdict(w) for w in report.weak_chains],
        "orphans": report.orphans,
    }, indent=2)


def audit(root: Path, scope: Optional[str] = None):
    graph = build(root, scope=scope) if scope else build(root)
    if scope and len(graph.nodes) == 0:
        rep = Report(
            date=str(date.today()), scope=scope, objects_audited=0,
            rules_violated=0, broken_links=0, weak_chains=[],
            weak_chain_count=0, verdict="insufficient-data",
            violations=[], orphans=[],
        )
        return rep, 3
    violations = []
    for fn in (check_rule_1, check_rule_2, check_rule_3, check_rule_4,
               check_rule_5, check_rule_6, check_rule_7):
        violations.extend(fn(graph))
    weak = assess_weak_chains(graph)
    objects_audited = len(graph.nodes)
    broken_links = (
        len([v for v in violations if v.violation_type in ("missing-link", "cycle")])
        + len([e for e in graph.edges if not e.target_exists])
    )
    weak_pct = (len(weak) / max(objects_audited, 1)) * 100.0
    verdict, code = verdict_for(objects_audited, broken_links, weak_pct)
    rep = Report(
        date=str(date.today()),
        scope=scope or "all",
        objects_audited=objects_audited,
        rules_violated=len({v.rule for v in violations}),
        broken_links=broken_links,
        weak_chains=weak,
        weak_chain_count=len(weak),
        verdict=verdict,
        violations=violations,
        orphans=[n.id for n in graph.orphans()],
    )
    return rep, code


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=".")
    p.add_argument("--scope", default=None)
    p.add_argument("--format", default="markdown", choices=["markdown", "json"])
    p.add_argument("--write", action="store_true")
    args = p.parse_args()
    root = Path(args.root).resolve()
    rep, code = audit(root, args.scope)
    out = render_json(rep) if args.format == "json" else render_markdown(rep)
    if args.write:
        audits_dir = root / "docs" / "audits"
        audits_dir.mkdir(parents=True, exist_ok=True)
        (audits_dir / f"traceability-{rep.date}.md").write_text(render_markdown(rep))
        log_path = audits_dir / "TRACEABILITY-LOG.md"
        if not log_path.exists():
            log_path.write_text("# Traceability audit log\n\n")
        with log_path.open("a") as f:
            f.write(
                f"- {rep.date} scope={rep.scope} verdict={rep.verdict} "
                f"objects={rep.objects_audited} broken={rep.broken_links}\n"
            )
        print(f"Report written to docs/audits/traceability-{rep.date}.md", file=sys.stderr)
    print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
