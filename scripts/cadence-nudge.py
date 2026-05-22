#!/usr/bin/env python3
"""SessionStart cadence-nudge hook (F2.5).

Three drift signals: stale Strategic Intent (>90d), orphan OST (no
chosen_opportunity AND >30d stale), kill-drought (no killed learning in 60d,
or zero learnings + alive chosen opportunity). Emits a single
hookSpecificOutput.additionalContext block or nothing. Never crashes a session.
Stdlib + scripts.lib.graph + scripts.lib.frontmatter only.
"""

from __future__ import annotations

import json
import sys
import traceback
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.lib.graph import Graph, build  # noqa: E402


# --- Thresholds (cited from operating model's three-tier cadence) -----------

STALE_STRATEGY_DAYS = 90   # quarterly
ORPHAN_OST_DAYS = 30       # monthly
KILL_DROUGHT_DAYS = 60     # bimonthly

# Message rendering budget.
MESSAGE_HARD_CAP = 600
PER_FINDING_VALUE_BUDGET = 500


@dataclass
class Finding:
    """One drift signal hit. `values` is the list of per-item descriptors."""
    signal: str           # "stale-strategy" | "orphan-ost" | "kill-drought"
    headline: str         # e.g. "Stale strategy"
    values: list[str]     # rendered per-item strings, in stable order
    summary: Optional[str] = None  # for single-value signals (kill-drought)


# --- Helpers -----------------------------------------------------------------


def _parse_date(v: Any) -> Optional[date]:
    """Coerce a `last_updated:` value to date. Frontmatter parser yields str."""
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    if isinstance(v, str):
        try:
            return datetime.strptime(v.strip(), "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


# --- Signals -----------------------------------------------------------------


def stale_strategy(graph: Graph, today: date) -> list[Finding]:
    """Strategic Intents whose `last_updated` > 90 days ago."""
    items: list[tuple[str, date]] = []
    for n in graph.by_type("Strategic Intent"):
        lu = _parse_date(n.frontmatter.get("last_updated"))
        if lu is None:
            continue
        if (today - lu).days > STALE_STRATEGY_DAYS:
            items.append((n.slug or n.id, lu))
    if not items:
        return []
    items.sort(key=lambda t: (t[1], t[0]))  # oldest first, slug as tiebreaker
    values = [f"{slug} ({lu.isoformat()})" for slug, lu in items]
    return [Finding(
        signal="stale-strategy",
        headline="Stale strategy",
        values=values,
        summary=f"last updated >{STALE_STRATEGY_DAYS} days ago",
    )]


def orphan_ost(graph: Graph, today: date) -> list[Finding]:
    """OSTs with no `chosen_opportunity:` set AND `last_updated` > 30 days ago."""
    items: list[tuple[str, int]] = []
    for n in graph.by_type("Opportunity Solution Tree"):
        chosen = n.frontmatter.get("chosen_opportunity")
        if chosen:  # field present and non-empty → not orphaned
            continue
        lu = _parse_date(n.frontmatter.get("last_updated"))
        if lu is None:
            continue
        days = (today - lu).days
        if days > ORPHAN_OST_DAYS:
            items.append((n.slug or n.id, days))
    if not items:
        return []
    items.sort(key=lambda t: (-t[1], t[0]))  # oldest drift first
    values = [f"{slug} ({days}d)" for slug, days in items]
    return [Finding(
        signal="orphan-ost",
        headline="Orphan OST",
        values=values,
        summary=f"no chosen_opportunity for >{ORPHAN_OST_DAYS} days",
    )]


def kill_drought(graph: Graph, today: date) -> list[Finding]:
    """No killed learning in 60 days; or zero learnings + alive chosen-opp."""
    learnings = graph.by_type("Validation Learning Memo")
    killed_dates: list[date] = []
    for n in learnings:
        if str(n.frontmatter.get("status", "")).lower() != "killed":
            continue
        lu = _parse_date(n.frontmatter.get("last_updated"))
        if lu is not None:
            killed_dates.append(lu)

    if killed_dates:
        latest = max(killed_dates)
        days = (today - latest).days
        if days > KILL_DROUGHT_DAYS:
            return [Finding(
                signal="kill-drought",
                headline="Kill drought",
                values=[f"{days} days since last killed learning"],
                summary=None,
            )]
        return []

    # No killed learnings exist. Check whether any chosen opportunity is alive.
    osts = graph.by_type("Opportunity Solution Tree")
    alive_chosen: list[str] = []
    for ost in osts:
        chosen_id = ost.frontmatter.get("chosen_opportunity")
        if not chosen_id:
            continue
        target = graph.nodes.get(str(chosen_id))
        if target is None:
            continue
        if str(target.frontmatter.get("status", "")).lower() != "killed":
            alive_chosen.append(target.slug or target.id)
    if alive_chosen:
        # Drought-by-absence: validation is implied (chosen opp alive) but no
        # kill verdicts on file.
        return [Finding(
            signal="kill-drought",
            headline="Kill drought",
            values=[
                f"no killed learnings on file (chosen: {', '.join(sorted(set(alive_chosen)))})"
            ],
            summary=None,
        )]
    return []


# --- Composition + truncation ------------------------------------------------


SIGNAL_ORDER = ("stale-strategy", "orphan-ost", "kill-drought")


def _render_finding(f: Finding) -> str:
    """Render one finding bullet. Value-list >500 chars → keep first 2 + `…`."""
    rendered_values = list(f.values)
    joined = ", ".join(rendered_values)
    if len(joined) > PER_FINDING_VALUE_BUDGET and len(rendered_values) > 2:
        rendered_values = rendered_values[:2] + ["…"]
        joined = ", ".join(rendered_values)
    line = f"- {f.headline}: {joined}"
    if f.summary:
        line += f" ({f.summary})"
    return line


def compose(findings: list[Finding]) -> Optional[str]:
    """Return the additionalContext block, or None if no findings."""
    if not findings:
        return None
    ordered = sorted(findings, key=lambda f: SIGNAL_ORDER.index(f.signal))
    lines = ["Cadence drift detected:"]
    for f in ordered:
        lines.append(_render_finding(f))
    lines.append("Consider: /cadence-check, /strategy-refresh, /kill-or-survive")
    return "\n".join(lines)


def is_empty_kit(graph: Graph) -> bool:
    """All three target types are absent → no nudges, no output."""
    return (
        len(graph.by_type("Strategic Intent")) == 0
        and len(graph.by_type("Opportunity Solution Tree")) == 0
        and len(graph.by_type("Validation Learning Memo")) == 0
    )


def run(root: Path, today: date) -> Optional[str]:
    """Pure orchestration entry point — returns the message body or None."""
    graph = build(root)
    if is_empty_kit(graph):
        return None
    findings: list[Finding] = []
    findings.extend(stale_strategy(graph, today))
    findings.extend(orphan_ost(graph, today))
    findings.extend(kill_drought(graph, today))
    return compose(findings)


def main() -> int:
    # Stdin is the SessionStart payload — read and ignore.
    try:
        sys.stdin.read()
    except Exception:
        pass
    try:
        root = Path.cwd()
        body = run(root, date.today())
        if body is None:
            return 0
        out = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": body,
            }
        }
        sys.stdout.write(json.dumps(out))
        return 0
    except Exception:
        # Never crash a session — surface the trace on stderr only.
        sys.stderr.write("cadence-nudge: degraded\n")
        traceback.print_exc(file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
