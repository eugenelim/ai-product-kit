# Spec: audit-graph-walker

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored)
- **Component type:** script (shared library)
- **Serves kit phase:** Meta (kit infrastructure consumed by every audit)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md`; `docs/CONVENTIONS.md` (universal metadata, traceability links); `context/frameworks/ontology.md` (the type set + Domain I composites); the seven traceability rules in `docs/HANDOVERS.md` and `/audit-traceability.md`

> **Spec contract.** Defines `scripts/lib/graph.py` — the typed-object-graph walker every Foundation 1 audit script will use.

## Objective

Build `scripts/lib/graph.py`: scan a kit directory (or a scoped subtree), parse each artifact's frontmatter (via `scripts.lib.frontmatter`), build an in-memory directed graph of typed objects, and expose query primitives the audits need: walk parent links, walk related links, find orphans, find cycles, find dangling references, group by `object_type`.

This is the shared substrate. F1.4 (traceability), F1.5 (completeness), F1.6 (portfolio coherence), F1.7 (traceability-walker agent) all build on it.

## Why now

The three F1 audit scripts would duplicate ~80% of setup logic (scan, parse, link, traverse) without a graph lib. Building the graph once means each audit's script is ~80 LOC of audit-specific logic on top of `from scripts.lib.graph import build, Graph`.

## Inputs and outputs

**Inputs.**
- A root path to scan (default: repo root).
- Optional `include_globs` (default: `strategy/`, `discovery/`, `validation/`, `delivery/`, `market/`, `personal-os/`, `context/personas/`, `context/products/`, `context/business/`). `context/personas/` etc. are included by default so `related_personas:` edges resolve to nodes; `context/frameworks/` and `context/voice/` etc. are NOT included (those are framework refs, not typed artifacts).
- Optional `scope`: an artifact id or slug; the walker scopes to that artifact's connected subtree (upward + downward).
- Optional `object_type` filter list.

**Outputs.**
- A `Graph` object exposing:
  - `nodes: dict[str, Node]` keyed by artifact id (or path-relative-to-root when id missing).
  - `edges: list[Edge]` with fields `source`, `target`, `kind` (verbatim source frontmatter field name, e.g., `"parent_intent"`, `"related_kpis"`), `target_exists` (bool).
  - `by_type(t: str) -> list[Node]`.
  - `parents_of(node) -> list[Node]` — follows `parent_*` edges only. Excludes `related_*` neighbors.
  - `children_of(node) -> list[Node]` — reverse traversal of `parent_*` edges only.
  - `related_of(node, kind: str|None = None) -> list[Node]` — follows `related_*` edges, optionally filtered by kind (e.g., `related_personas`).
  - `walk_up(node) -> Iterator[Node]` — yields ancestors in order via `parent_*`. Tracks visited nodes so cyclic graphs terminate.
  - `walk_down(node) -> Iterator[Node]` — BFS over children (via `parent_*` back-edges). Verified BFS-order on a branching fixture, not just a linear chain.
  - `orphans() -> list[Node]` — typed nodes whose `object_type` appears in ORPHAN_RULES but whose required parent edge does not resolve to an existing node.
  - `cycles() -> list[list[Node]]` — Tarjan SCCs of size ≥ 2.
  - `self_loops() -> list[Node]` — nodes whose `parent_*` link points to themselves. (Reported separately from `cycles()`.)
  - `dangling_edges() -> list[Edge]` — edges whose target id is not a node (`target_exists == False`).
  - `parse_errors: list[tuple[Path, str]]` — files that failed to parse, surfaced not raised.
  - `id_collisions: list[tuple[str, list[Path]]]` — id values declared by more than one file; last-write-wins on `nodes[]` but the collision is recorded here.

A `Node` carries: `id`, `slug`, `object_type`, `status`, `path`, `frontmatter: dict`. When `id:` is missing from frontmatter, the node's `id` field is set to the path-relative-to-root string and the node is added to `nodes[]` keyed by that string. If a later artifact declares `id: <that-same-path-string>`, this is recorded in `id_collisions` and the later artifact wins.

## Boundaries

### Always do
- Use stdlib + `scripts.lib.frontmatter` only.
- Skip dotdirs, `__pycache__`, `node_modules`, `.git`.
- Skip files without frontmatter silently — they aren't typed artifacts.
- Surface parse errors as data on the `Graph` object; don't raise.
- Treat path-only references (no id) as nodes keyed by path-relative-to-root.

### Ask first
- Adding edge kinds beyond what HANDOVERS.md / CONVENTIONS.md / ontology Rules name. Default: don't.
- Caching the graph to disk. Default: in-memory only.

### Never do
- Mutate any artifact on disk.
- Take an external dep (networkx, etc.).
- Treat a missing frontmatter field as an error during graph construction (audits do field-level checks; the graph is structural only).

## Verification mode

- **TDD.** Unit tests under `scripts/tests/test_graph.py` drive implementation.
- **Goal-based check.** A fixture tree under `scripts/tests/fixtures/sample-kit/` represents a minimal-but-realistic kit instance. Tests assert specific structural properties.

## Contract tests

- `test_builds_empty_graph_on_empty_dir`
- `test_builds_graph_from_sample_kit_fixture` — assert expected node/edge counts and `object_type` distribution.
- `test_parents_of_returns_resolved_parents`
- `test_walk_up_reaches_strategic_intent_root`
- `test_walk_down_bfs_visits_each_node_once`
- `test_orphans_flags_OST_without_parent_intent`
- `test_dangling_edges_flags_broken_parent_link`
- `test_cycles_returns_empty_on_acyclic_graph`
- `test_cycles_detects_two_node_cycle` (fixture: two artifacts mutually pointing as parents)
- `test_by_type_groups_correctly`
- `test_scope_filter_returns_only_connected_subtree`
- `test_parse_errors_surface_on_malformed_file_without_raising`
- `test_default_excludes_skip_dot_and_pycache`
- `test_id_collision_records_warning` — two artifacts declaring the same `id:` produce a `parse_errors` entry; last-write-wins on the node dict.
- `test_walk_up_terminates_on_cycle` — `walk_up` tracks visited nodes; doesn't infinite-loop on the cycle fixture.
- `test_edge_kind_carries_field_name` — `Edge.kind` is the verbatim frontmatter field name (e.g., `"parent_vision"`), not a category.
- `test_children_of_returns_only_parent_back_edges` — `children_of` follows `parent_*` edges in reverse; does NOT include `related_*` neighbors.
- `test_self_loop_flagged_separately_from_cycles` — a node with `parent_intent` pointing to itself appears in `self_loops()` and NOT in `cycles()`.
- `test_related_field_accepts_id_or_path` — `related_personas: [PERSONA-001, ../personas/admin.md]` resolves both forms to the correct nodes.
- `test_walk_down_bfs_order_on_branching_fixture` — fixture has a node with 2 children which each have 2 children; `walk_down` visits depth-1 nodes before depth-2 nodes (BFS, not DFS).
- `test_multivalued_parent_field_handled_gracefully` — if a `parent_initiative:` field contains a list rather than a scalar, the graph builder records a `parse_errors` entry and uses the first value; doesn't crash.

## Non-goals

- Visualization (graphviz, mermaid).
- Persistence — in-memory only.
- Editing artifacts.
- Implementing the seven traceability rules — F1.4's job; this lib gives F1.4 the graph.

## Open questions

1. **Edge-kind enumeration: hardcoded or discovered?** Lean: hardcoded `PARENT_FIELDS` / `RELATED_FIELDS` constants matching HANDOVERS.md; new edges require code change.
2. **Node identity when `id:` missing:** lean — fall back to path-relative-to-repo-root as key.

## Acceptance criteria

- [ ] `scripts/lib/graph.py` exists, stdlib + `scripts.lib.frontmatter` only, ≤ ~400 LOC.
- [ ] `scripts/tests/test_graph.py` exists; all 13 contract tests pass.
- [ ] `scripts/tests/fixtures/sample-kit/` exists with the minimal kit instance; `scripts/tests/fixtures/broken/` exists with the cycle + dangling fixtures.
- [ ] `python3 -m unittest scripts.tests.test_graph` exits 0.
- [ ] PLAN/VERIFY/REVIEW gates exit 0.

## Cross-references

- **Consumed by:** F1.4, F1.5, F1.6, F1.7. (F1.3, the ontology-classifier skill, does NOT directly consume this graph lib — it uses `scripts.lib.frontmatter` for round-trip persistence at most.)
- **Consumes:** stdlib + `scripts.lib.frontmatter` (F1.2).
- **Frontmatter fields owned:** none.
- **Ontology object types touched:** all (type-agnostic; reads `object_type`).
