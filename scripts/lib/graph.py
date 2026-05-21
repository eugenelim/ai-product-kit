"""Typed-object-graph walker (F1.1).

Scans a kit directory, builds a directed graph of typed artifacts, exposes
query primitives the audits need (parent/child traversal, orphan detection,
cycle detection, dangling edges, scope filtering).

Consumed by F1.4 (audit-traceability), F1.5 (audit-completeness),
F1.6 (audit-portfolio-coherence), F1.7 (traceability-walker agent).

Read-only — never mutates artifacts. Stdlib + scripts.lib.frontmatter only.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator, Optional

from scripts.lib.frontmatter import parse_file


# Edge-kind catalog — derived from HANDOVERS.md frontmatter examples.
PARENT_FIELDS: tuple[str, ...] = (
    "parent_diagnosis",
    "parent_intent",
    "parent_opportunity",
    "parent_learning",
    "parent_vision",
    "parent_initiative",
    "parent_handoff_packet",
)

# Derived from CONVENTIONS.md universal schema. `related_capabilities` is
# also included because the kit's handoff-packet `requirements.yaml` files
# use it to trace Requirements → Capabilities (the F1.4 Rule-1 traceability).
# It is not in CONVENTIONS.md's universal schema example block today; surface
# as a CONVENTIONS.md amendment in a follow-up doc edit.
RELATED_FIELDS: tuple[str, ...] = (
    "related_problems",
    "related_personas",
    "related_kpis",
    "related_capabilities",
)

# Orphan rules: Domain I composite types and their required parent field per
# HANDOVERS.md. A typed node in this map without a resolved parent edge of
# the required kind is an orphan.
ORPHAN_RULES: dict[str, str] = {
    "Opportunity Solution Tree": "parent_intent",
    "Assumption Map": "parent_opportunity",
    "Validation Learning Memo": "parent_opportunity",
    "Vision": "parent_learning",
    "Initiative": "parent_vision",
    "Handoff Packet": "parent_initiative",
    # Landing Report: parent_vision OR parent_handoff_packet — see ORPHAN_ALT_RULES
    "Landing Report": "parent_vision",
}

# Some types accept any one of several parent fields. ORPHAN_ALT_RULES lists
# alternative parent fields per object_type; if EITHER the ORPHAN_RULES entry
# OR any ORPHAN_ALT_RULES entry resolves, the node is NOT an orphan.
ORPHAN_ALT_RULES: dict[str, tuple[str, ...]] = {
    "Landing Report": ("parent_handoff_packet",),
}

# Default include-globs. context/personas|products|business included so
# `related_*` edges to those typed artifacts resolve; context/frameworks,
# context/voice etc. are reference content, not typed artifacts.
DEFAULT_INCLUDES: tuple[str, ...] = (
    "strategy",
    "discovery",
    "validation",
    "delivery",
    "market",
    "personal-os",
    "context/personas",
    "context/products",
    "context/business",
)

# Directories always skipped (regardless of include_globs).
DEFAULT_SKIPS: tuple[str, ...] = (".git", "__pycache__", "node_modules", ".worktrees")


@dataclass
class Node:
    id: str
    slug: str
    object_type: str
    status: str
    path: Path
    frontmatter: dict[str, Any]


@dataclass
class Edge:
    source: str
    target: str
    kind: str  # verbatim source frontmatter field name
    target_exists: bool


@dataclass
class Graph:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    parse_errors: list[tuple[Path, str]] = field(default_factory=list)
    id_collisions: list[tuple[str, list[Path]]] = field(default_factory=list)

    # --- Queries -----------------------------------------------------------

    def by_type(self, t: str) -> list[Node]:
        return [n for n in self.nodes.values() if n.object_type == t]

    def parents_of(self, node: Node) -> list[Node]:
        """Follow parent_* edges only (NOT related_*)."""
        out: list[Node] = []
        for e in self.edges:
            if e.source == node.id and e.kind in PARENT_FIELDS and e.target_exists:
                target = self.nodes.get(e.target)
                if target is not None:
                    out.append(target)
        return out

    def children_of(self, node: Node) -> list[Node]:
        """Reverse traversal of parent_* edges only."""
        out: list[Node] = []
        for e in self.edges:
            if e.target == node.id and e.kind in PARENT_FIELDS and e.target_exists:
                src = self.nodes.get(e.source)
                if src is not None:
                    out.append(src)
        return out

    def related_of(
        self, node: Node, kind: Optional[str] = None
    ) -> list[Node]:
        """Follow related_* edges, optionally filtered by kind."""
        out: list[Node] = []
        for e in self.edges:
            if e.source != node.id:
                continue
            if e.kind not in RELATED_FIELDS:
                continue
            if kind is not None and e.kind != kind:
                continue
            if e.target_exists:
                target = self.nodes.get(e.target)
                if target is not None:
                    out.append(target)
        return out

    def walk_up(self, node: Node) -> Iterator[Node]:
        """Yield ancestors via parent_* edges. Cycle-safe."""
        seen: set[str] = {node.id}
        current = [node]
        while current:
            next_level: list[Node] = []
            for c in current:
                for p in self.parents_of(c):
                    if p.id in seen:
                        continue
                    seen.add(p.id)
                    yield p
                    next_level.append(p)
            current = next_level

    def walk_down(self, node: Node) -> Iterator[Node]:
        """BFS over children (reverse parent_* edges). Cycle-safe."""
        seen: set[str] = {node.id}
        queue: deque[Node] = deque([node])
        first = True
        while queue:
            c = queue.popleft()
            if not first:
                yield c
            first = False
            for child in self.children_of(c):
                if child.id in seen:
                    continue
                seen.add(child.id)
                queue.append(child)

    def orphans(self) -> list[Node]:
        out: list[Node] = []
        for node in self.nodes.values():
            required_parent = ORPHAN_RULES.get(node.object_type)
            if required_parent is None:
                continue
            alt_parents = ORPHAN_ALT_RULES.get(node.object_type, ())
            acceptable = (required_parent,) + alt_parents
            # Look for an edge of any acceptable kind from this node
            has_resolved = False
            for e in self.edges:
                if (
                    e.source == node.id
                    and e.kind in acceptable
                    and e.target_exists
                ):
                    has_resolved = True
                    break
            if not has_resolved:
                out.append(node)
        return out

    def cycles(self) -> list[list[Node]]:
        """Tarjan SCCs of size ≥ 2 (parent_* edges only). Self-loops excluded."""
        adj: dict[str, list[str]] = defaultdict(list)
        for e in self.edges:
            if e.kind in PARENT_FIELDS and e.target_exists:
                adj[e.source].append(e.target)

        index_counter = [0]
        stack: list[str] = []
        on_stack: set[str] = set()
        indices: dict[str, int] = {}
        lowlinks: dict[str, int] = {}
        sccs: list[list[str]] = []

        def strongconnect(v: str) -> None:
            indices[v] = index_counter[0]
            lowlinks[v] = index_counter[0]
            index_counter[0] += 1
            stack.append(v)
            on_stack.add(v)
            for w in adj.get(v, []):
                if w not in indices:
                    strongconnect(w)
                    lowlinks[v] = min(lowlinks[v], lowlinks[w])
                elif w in on_stack:
                    lowlinks[v] = min(lowlinks[v], indices[w])
            if lowlinks[v] == indices[v]:
                component: list[str] = []
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    component.append(w)
                    if w == v:
                        break
                if len(component) >= 2:
                    sccs.append(component)

        for v in self.nodes:
            if v not in indices:
                strongconnect(v)

        return [[self.nodes[nid] for nid in c if nid in self.nodes] for c in sccs]

    def self_loops(self) -> list[Node]:
        """Nodes whose parent_* link points to themselves."""
        out: list[Node] = []
        for e in self.edges:
            if (
                e.kind in PARENT_FIELDS
                and e.source == e.target
                and e.target_exists
            ):
                n = self.nodes.get(e.source)
                if n is not None and n not in out:
                    out.append(n)
        return out

    def dangling_edges(self) -> list[Edge]:
        return [e for e in self.edges if not e.target_exists]


# --- Build --------------------------------------------------------------


def build(
    root: Path,
    include_globs: Optional[tuple[str, ...]] = None,
    scope: Optional[str] = None,
) -> Graph:
    """Scan root, parse frontmatter, build the typed-object graph.

    Args:
      root: kit root directory.
      include_globs: subpaths to scan (default: DEFAULT_INCLUDES). Each item
        is interpreted relative to root.
      scope: an artifact id or slug. If set, restricts the returned graph
        to the connected subtree (upward + downward) of that node.

    Returns a Graph with nodes, edges, parse_errors, id_collisions.
    Never raises on parse failure — surfaces errors as data.
    """
    graph = Graph()

    # Resolve scan directories.
    if include_globs is None:
        scan_dirs = [root / inc for inc in DEFAULT_INCLUDES]
        scan_dirs = [d for d in scan_dirs if d.is_dir()]
        if not scan_dirs:
            # Fallback: no kit-phase subdirs exist at root; scan root itself.
            # (This is the common case for test-fixture trees that don't mirror
            # the kit phase layout — e.g., scripts/tests/fixtures/broken/.)
            scan_dirs = [root]
    else:
        scan_dirs = [root / inc if inc else root for inc in include_globs]
        scan_dirs = [d for d in scan_dirs if d.is_dir()]

    # 1. Scan
    md_files: list[Path] = []
    for d in scan_dirs:
        for p in list(d.rglob("*.md")) + list(d.rglob("*.yaml")):
            if any(s in p.parts for s in DEFAULT_SKIPS):
                continue
            md_files.append(p)

    # 2. Parse + node build
    id_to_paths: dict[str, list[Path]] = defaultdict(list)
    for path in md_files:
        try:
            fm = parse_file(path)
        except Exception as e:
            graph.parse_errors.append((path, str(e)))
            continue
        if fm is None or not fm.data:
            continue
        data = fm.data
        if "object_type" not in data:
            continue
        node_id = data.get("id") or str(path.relative_to(root))
        node_slug = data.get("slug", "")
        node_type = data.get("object_type", "")
        node_status = data.get("status", "")
        node = Node(
            id=node_id,
            slug=node_slug,
            object_type=node_type,
            status=node_status,
            path=path,
            frontmatter=data,
        )
        id_to_paths[node_id].append(path)
        graph.nodes[node_id] = node  # last-write-wins on collision

    # Record collisions
    for nid, paths in id_to_paths.items():
        if len(paths) > 1:
            graph.id_collisions.append((nid, paths))

    # 3. Build edges
    for node in list(graph.nodes.values()):
        for field_name in PARENT_FIELDS:
            v = node.frontmatter.get(field_name)
            if v is None or v == "":
                continue
            if isinstance(v, list):
                # Multi-valued parent_* — record parse_error, use first
                graph.parse_errors.append(
                    (node.path, f"{field_name}: list value not supported; using first")
                )
                v = v[0] if v else None
                if not v:
                    continue
            target_id = str(v)
            target_exists = target_id in graph.nodes
            graph.edges.append(
                Edge(
                    source=node.id,
                    target=target_id,
                    kind=field_name,
                    target_exists=target_exists,
                )
            )
        for field_name in RELATED_FIELDS:
            v = node.frontmatter.get(field_name)
            if v is None:
                continue
            if not isinstance(v, list):
                v = [v]
            for target in v:
                if not target:
                    continue
                target_id = str(target)
                target_exists = target_id in graph.nodes
                graph.edges.append(
                    Edge(
                        source=node.id,
                        target=target_id,
                        kind=field_name,
                        target_exists=target_exists,
                    )
                )

    # 4. Scope filter (optional)
    if scope is not None:
        return _apply_scope(graph, scope)

    return graph


def _apply_scope(graph: Graph, scope: str) -> Graph:
    """Return a new Graph containing only the connected subtree of `scope`."""
    # Find the scope node by id or slug
    scope_node: Optional[Node] = graph.nodes.get(scope)
    if scope_node is None:
        for n in graph.nodes.values():
            if n.slug == scope:
                scope_node = n
                break
    if scope_node is None:
        # Scope didn't resolve — return empty graph but surface the failure
        # so callers don't silently audit zero nodes.
        empty = Graph()
        empty.parse_errors = list(graph.parse_errors)
        empty.parse_errors.append(
            (Path("."), f"scope '{scope}' did not resolve to any node id or slug")
        )
        return empty

    # BFS upward and downward over parent_* edges
    keep_ids: set[str] = {scope_node.id}
    # Up
    for ancestor in graph.walk_up(scope_node):
        keep_ids.add(ancestor.id)
    # Down
    for descendant in graph.walk_down(scope_node):
        keep_ids.add(descendant.id)

    new = Graph()
    new.parse_errors = graph.parse_errors
    new.id_collisions = graph.id_collisions
    new.nodes = {nid: graph.nodes[nid] for nid in keep_ids if nid in graph.nodes}
    new.edges = [e for e in graph.edges if e.source in keep_ids and (e.target in keep_ids or not e.target_exists)]
    return new
