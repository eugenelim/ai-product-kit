#!/usr/bin/env python3
"""audit-spec-linkage.py — Enforce Handover-5 spec→initiative linkage (P4.10).

One rule: every PM Spec at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`
must declare a `parent_initiative:` frontmatter value that resolves to an existing
`delivery/initiatives/<value>/README.md`.

Violation types:
  - missing-parent-initiative: field absent or empty.
  - dangling-parent-initiative: field present but target initiative not found.

Verdict thresholds (verbatim from F1.4 audit-traceability):
  - 0 clean: 0 broken links.
  - 1 drift: 1-3 broken links AND broken/audited <= 25%.
  - 2 broken: >3 broken links OR >25% systemic.
  - 3 insufficient-data: fewer than 3 specs in scope.

Argv mirrors `scripts/audit-traceability.py`: --root, --scope, --format, --write.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass, asdict, field
from datetime import date
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.graph import Graph, Node, build  # noqa: E402


SPEC_PATH_RE = re.compile(
    r"delivery/initiatives/(?P<initiative>[^/]+)/specs/(?P<spec>[^/]+)\.md$"
)


@dataclass
class Violation:
    spec_slug: str
    path: str
    violation_type: str
    remediation: str


@dataclass
class Report:
    date: str
    scope: str
    specs_audited: int
    broken_links: int
    verdict: str
    violations: list = field(default_factory=list)
    orphans: list = field(default_factory=list)


def _is_spec_path(path: Path, root: Path) -> Optional[tuple[str, str]]:
    """If `path` matches the flat-file PM-Spec layout, return (initiative_slug, spec_slug)."""
    try:
        rel = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        rel = path.as_posix()
    m = SPEC_PATH_RE.search(rel)
    if not m:
        return None
    return m.group("initiative"), m.group("spec")


def _initiative_exists(root: Path, initiative_slug: str) -> bool:
    return (root / "delivery" / "initiatives" / initiative_slug / "README.md").is_file()


def _initiative_id_to_slug(graph: Graph) -> dict[str, str]:
    """Map Initiative node ids (and slugs) to their slug values for resolution."""
    out: dict[str, str] = {}
    for node in graph.by_type("Initiative"):
        if node.slug:
            out[node.slug] = node.slug
        if node.id:
            out[node.id] = node.slug or node.id
    return out


def _resolves_to_initiative(
    parent_value: str, graph: Graph, root: Path
) -> bool:
    """Return True if `parent_value` resolves to an existing initiative."""
    id_or_slug_map = _initiative_id_to_slug(graph)
    if parent_value in id_or_slug_map:
        candidate_slug = id_or_slug_map[parent_value]
        if _initiative_exists(root, candidate_slug):
            return True
    # Fall back: treat the value as a direct slug.
    return _initiative_exists(root, parent_value)


def _next_action_for(verdict: str) -> str:
    if verdict == "clean":
        return "no action needed"
    if verdict in ("drift", "broken"):
        return "fix the listed broken parent_initiative links"
    return "expand scope or add specs"


def _verdict_for(specs_audited: int, broken_links: int) -> tuple[str, int]:
    if specs_audited < 3:
        return "insufficient-data", 3
    if broken_links == 0:
        return "clean", 0
    pct = broken_links / specs_audited
    if 1 <= broken_links <= 3 and pct <= 0.25:
        return "drift", 1
    return "broken", 2


def audit(root: Path, scope: Optional[str] = None) -> tuple[Report, int]:
    graph = build(root)
    spec_nodes: list[tuple[Node, str, str]] = []
    for node in graph.nodes.values():
        match = _is_spec_path(node.path, root)
        if match is None:
            continue
        initiative_slug, spec_slug = match
        if scope and scope != "all" and initiative_slug != scope:
            continue
        spec_nodes.append((node, initiative_slug, spec_slug))

    violations: list[Violation] = []
    for node, initiative_slug, spec_slug in spec_nodes:
        parent_value = node.frontmatter.get("parent_initiative")
        if isinstance(parent_value, list):
            parent_value = parent_value[0] if parent_value else None
        if isinstance(parent_value, str) and not parent_value.strip():
            parent_value = None
        rel_path = str(node.path.relative_to(root) if node.path.is_absolute() else node.path)
        if not parent_value:
            violations.append(Violation(
                spec_slug=spec_slug,
                path=rel_path,
                violation_type="missing-parent-initiative",
                remediation="Add `parent_initiative: <initiative-id-or-slug>` to the spec's frontmatter.",
            ))
            continue
        if not _resolves_to_initiative(str(parent_value), graph, root):
            violations.append(Violation(
                spec_slug=spec_slug,
                path=rel_path,
                violation_type="dangling-parent-initiative",
                remediation=(
                    f"`parent_initiative: {parent_value}` does not resolve. Expected "
                    f"`delivery/initiatives/{parent_value}/README.md` or an Initiative node with that id. "
                    f"Correct the value or create the initiative directory."
                ),
            ))

    if graph.parse_errors:
        print(
            f"Warning: {len(graph.parse_errors)} file(s) skipped due to parse errors; "
            f"audit results may be incomplete.",
            file=sys.stderr,
        )

    specs_audited = len(spec_nodes)
    broken_links = len(violations)
    verdict, code = _verdict_for(specs_audited, broken_links)
    report = Report(
        date=str(date.today()),
        scope=scope or "all",
        specs_audited=specs_audited,
        broken_links=broken_links,
        verdict=verdict,
        violations=violations,
        orphans=[],
    )
    return report, code


def render_markdown(report: Report) -> str:
    lines = [
        "---",
        f"date: {report.date}",
        f"scope: {report.scope}",
        f"specs_audited: {report.specs_audited}",
        f"broken_links: {report.broken_links}",
        f"verdict: {report.verdict}",
        "object_type: Audit Report",
        "status: Draft",
        f"last_updated: {report.date}",
        "---",
        "",
        f"# Spec linkage audit — {report.scope}",
        "",
        f"**Verdict:** {report.verdict}",
        "",
        "## Rule 1 violations",
        "",
    ]
    if report.violations:
        lines.append("| spec_slug | path | violation_type | remediation |")
        lines.append("|---|---|---|---|")
        for v in report.violations:
            lines.append(f"| {v.spec_slug} | {v.path} | {v.violation_type} | {v.remediation} |")
    else:
        lines.append("_None._")
    lines.append("")
    lines.append("## Orphans")
    lines.append("")
    if report.orphans:
        for o in report.orphans:
            lines.append(f"- {o}")
    else:
        lines.append("_None._")
    lines.append("")
    lines.append("## Recommended remediations")
    lines.append("")
    if report.violations:
        for v in report.violations:
            lines.append(f"- {v.spec_slug}: {v.remediation}")
    else:
        lines.append("_None — verdict is {0}._".format(report.verdict))
    lines.append("")
    return "\n".join(lines)


def render_json(report: Report) -> str:
    return json.dumps({
        "frontmatter": {
            "date": report.date,
            "scope": report.scope,
            "specs_audited": report.specs_audited,
            "broken_links": report.broken_links,
            "verdict": report.verdict,
        },
        "violations": [asdict(v) for v in report.violations],
        "orphans": report.orphans,
    }, indent=2)


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=str(path.parent), prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def render_stdout_header(report: Report) -> str:
    return (
        f"PHASE: Delivery → Spec linkage audit (scope={report.scope})\n"
        f"VERDICT: {report.verdict}\n"
        f"NEXT: {_next_action_for(report.verdict)}\n"
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=".")
    p.add_argument("--scope", default="all")
    p.add_argument("--format", default="markdown", choices=["markdown", "json"])
    p.add_argument("--write", action="store_true")
    args = p.parse_args()

    root = Path(args.root).resolve()
    scope = args.scope if args.scope != "all" else None
    report, code = audit(root, scope)

    payload = render_json(report) if args.format == "json" else render_markdown(report)
    header = render_stdout_header(report)

    if args.write:
        audits_dir = root / "docs" / "audits"
        report_path = audits_dir / f"spec-linkage-{report.date}.md"
        markdown_payload = render_markdown(report)
        _atomic_write(report_path, markdown_payload)
        log_path = audits_dir / "SPEC-LINKAGE-LOG.md"
        if not log_path.exists():
            log_path.write_text("# Spec linkage audit log\n\n")
        with log_path.open("a") as f:
            f.write(
                f"- {report.date} scope={report.scope} verdict={report.verdict} "
                f"specs={report.specs_audited} broken={report.broken_links}\n"
            )
        print(f"Report written to docs/audits/spec-linkage-{report.date}.md", file=sys.stderr)

    sys.stdout.write(header)
    sys.stdout.write("\n")
    sys.stdout.write(payload)
    if not payload.endswith("\n"):
        sys.stdout.write("\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
