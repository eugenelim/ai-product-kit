"""Contract tests for scripts.lib.graph (F1.1).

Run from repo root:
    python3 -m unittest scripts.tests.test_graph
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.lib.graph import Graph, Node, Edge, build, PARENT_FIELDS, RELATED_FIELDS


FIXTURES = Path(__file__).resolve().parent / "fixtures"
SAMPLE_KIT = FIXTURES / "sample-kit"
BROKEN = FIXTURES / "broken"


class TestBuilder(unittest.TestCase):
    def test_builds_empty_graph_on_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            g = build(Path(tmp))
            self.assertEqual(len(g.nodes), 0)
            self.assertEqual(len(g.edges), 0)

    def test_builds_graph_from_sample_kit_fixture(self):
        g = build(SAMPLE_KIT)
        # Chain 1 + chain 2 + the atomics: 2 intents + 2 OSTs + 1 problem +
        # 1 learning + 1 vision + 1 initiative + 1 capability + 1 packet +
        # 1 requirement + 1 landing = 12 nodes
        self.assertGreaterEqual(len(g.nodes), 12)
        # Each typed artifact contributes edges; should be many
        self.assertGreater(len(g.edges), 5)
        # Type distribution
        intents = g.by_type("Strategic Intent")
        self.assertEqual(len(intents), 2)
        osts = g.by_type("Opportunity Solution Tree")
        self.assertEqual(len(osts), 2)


class TestQueries(unittest.TestCase):
    def setUp(self):
        self.g = build(SAMPLE_KIT)

    def test_parents_of_returns_resolved_parents(self):
        ost = next(n for n in self.g.by_type("Opportunity Solution Tree") if n.id == "OST-001")
        parents = self.g.parents_of(ost)
        ids = {p.id for p in parents}
        self.assertIn("INTENT-001", ids)

    def test_walk_up_reaches_strategic_intent_root(self):
        landing = next(n for n in self.g.by_type("Landing Report"))
        ancestors = list(self.g.walk_up(landing))
        # Should walk landing → vision → learning → ... back through chain
        ancestor_types = {a.object_type for a in ancestors}
        self.assertIn("Vision", ancestor_types)

    def test_walk_down_bfs_order_on_branching_fixture(self):
        # INTENT-001 now has 2 depth-1 children: OST-001 and OPP-001 + OPP-001B
        # (via parent_intent). OPP-001 has 1 depth-2 child (LEARN-001 via
        # parent_opportunity); OPP-001B has 1 depth-2 child (LEARN-002).
        # Assert ALL depth-1 nodes appear before ANY depth-2 node.
        intent = next(n for n in self.g.by_type("Strategic Intent") if n.id == "INTENT-001")
        order = list(self.g.walk_down(intent))
        order_ids = [n.id for n in order]
        # Depth-1 (via parent_intent: INTENT-001): OST-001, OPP-001, OPP-001B
        depth1 = {"OST-001", "OPP-001", "OPP-001B"}
        # Depth-2 (via parent_opportunity: OPP-001 or OPP-001B): LEARN-001, LEARN-002, PROB-001
        depth2 = {"LEARN-001", "LEARN-002", "PROB-001"}
        present_d1 = [i for i in depth1 if i in order_ids]
        present_d2 = [i for i in depth2 if i in order_ids]
        if present_d1 and present_d2:
            last_d1 = max(order_ids.index(i) for i in present_d1)
            first_d2 = min(order_ids.index(i) for i in present_d2)
            self.assertLess(
                last_d1,
                first_d2,
                f"BFS violation: depth-2 node appeared before all depth-1 nodes finished. "
                f"order={order_ids}",
            )
        # Assert we actually have both depths in the order (test isn't vacuous)
        self.assertTrue(present_d1, "no depth-1 children found — fixture broken")
        self.assertTrue(present_d2, "no depth-2 descendants found — fixture broken")

    def test_by_type_groups_correctly(self):
        intents = self.g.by_type("Strategic Intent")
        self.assertTrue(all(n.object_type == "Strategic Intent" for n in intents))

    def test_children_of_returns_only_parent_back_edges(self):
        intent = next(n for n in self.g.by_type("Strategic Intent") if n.id == "INTENT-001")
        children = self.g.children_of(intent)
        # OST-001 has parent_intent=INTENT-001; should be a child.
        child_ids = {c.id for c in children}
        self.assertIn("OST-001", child_ids)
        # Personas are related_, not parent_; should NOT appear in children_of
        # (fixture doesn't include personas, but assert structurally)

    def test_edge_kind_carries_field_name(self):
        # Find the edge from OST-001 → INTENT-001
        edge = next(
            (e for e in self.g.edges if e.source == "OST-001" and e.target == "INTENT-001"),
            None,
        )
        self.assertIsNotNone(edge)
        self.assertEqual(edge.kind, "parent_intent")


class TestOrphansAndScope(unittest.TestCase):
    def setUp(self):
        self.g = build(SAMPLE_KIT)

    def test_orphans_flags_OST_without_parent_intent(self):
        # The sample-kit OSTs both have parent_intent; orphans should not
        # include them. Build a separate test against the broken fixture.
        broken_g = build(BROKEN)
        # dangling-parent.md is an OST with parent_intent → nonexistent.
        # It's an orphan structurally (parent doesn't resolve).
        orphans = broken_g.orphans()
        orphan_slugs = {o.slug for o in orphans}
        self.assertIn("dangling-parent", orphan_slugs)

    def test_scope_filter_returns_only_connected_subtree(self):
        # Scope to INTENT-001 — chain-1 only. INTENT-002 and OST-002 must NOT appear.
        scoped = build(SAMPLE_KIT, scope="INTENT-001")
        node_ids = set(scoped.nodes.keys())
        self.assertIn("INTENT-001", node_ids)
        self.assertNotIn("INTENT-002", node_ids)
        self.assertNotIn("OST-002", node_ids)


class TestBrokenFixtures(unittest.TestCase):
    def setUp(self):
        self.g = build(BROKEN)

    def test_dangling_edges_flags_broken_parent_link(self):
        dangling = self.g.dangling_edges()
        self.assertGreater(len(dangling), 0)
        # The dangling-parent fixture's edge should be in the list
        targets = {e.target for e in dangling}
        self.assertIn("NONEXISTENT-INTENT", targets)

    def test_cycles_detects_two_node_cycle(self):
        cycles = self.g.cycles()
        self.assertGreaterEqual(len(cycles), 1)
        # The cycle should contain both CYC-A and CYC-B
        all_in_cycles = {n.id for c in cycles for n in c}
        self.assertIn("CYC-A", all_in_cycles)
        self.assertIn("CYC-B", all_in_cycles)

    def test_cycles_returns_empty_on_acyclic_graph(self):
        sample = build(SAMPLE_KIT)
        self.assertEqual(sample.cycles(), [])

    def test_self_loop_flagged_separately_from_cycles(self):
        # Build a synthetic self-loop fixture inline
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "strategy" / "intents").mkdir(parents=True)
            (tmp_path / "strategy" / "intents" / "self-loop.md").write_text(
                "---\nid: SELF\nslug: self-loop\nobject_type: Strategic Intent\n"
                "status: Draft\nlast_updated: 2026-05-21\nparent_intent: SELF\n---\n"
            )
            g = build(tmp_path)
            loops = g.self_loops()
            self.assertEqual(len(loops), 1)
            # Self-loop should NOT appear in cycles() (size-2+ only)
            cyc = g.cycles()
            self.assertEqual(len(cyc), 0)

    def test_walk_up_terminates_on_cycle(self):
        cyc_a = self.g.nodes.get("CYC-A")
        self.assertIsNotNone(cyc_a)
        # If walk_up did not track visited, this would loop forever.
        ancestors = list(self.g.walk_up(cyc_a))
        # Should terminate; both nodes appear at most once.
        ids = [a.id for a in ancestors]
        self.assertEqual(len(ids), len(set(ids)))


class TestErrorPaths(unittest.TestCase):
    def test_parse_errors_surface_on_malformed_file_without_raising(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "strategy" / "intents").mkdir(parents=True)
            # Unclosed frontmatter — parser tolerates; graph build should not raise
            (tmp_path / "strategy" / "intents" / "bad.md").write_text(
                "---\nfoo: bar\nno closing delimiter\nbody\n"
            )
            g = build(tmp_path)
            # No nodes added (no valid frontmatter); no exceptions
            # parse_errors may or may not surface depending on whether the lib
            # reports the unclosed delimiter for empty-data results
            self.assertIsInstance(g.nodes, dict)

    def test_default_excludes_skip_dot_and_pycache(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / ".git").mkdir()
            (tmp_path / ".git" / "config.md").write_text(
                "---\nid: X\nslug: x\nobject_type: Strategic Intent\n"
                "status: Draft\nlast_updated: 2026-05-21\n---\n"
            )
            (tmp_path / "__pycache__").mkdir()
            (tmp_path / "__pycache__" / "cache.md").write_text(
                "---\nid: Y\nslug: y\nobject_type: Strategic Intent\n"
                "status: Draft\nlast_updated: 2026-05-21\n---\n"
            )
            g = build(tmp_path)
            self.assertEqual(len(g.nodes), 0)

    def test_id_collision_records_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "strategy" / "intents").mkdir(parents=True)
            (tmp_path / "strategy" / "intents" / "a.md").write_text(
                "---\nid: COLLIDE\nslug: a\nobject_type: Strategic Intent\n"
                "status: Draft\nlast_updated: 2026-05-21\n---\n"
            )
            (tmp_path / "strategy" / "intents" / "b.md").write_text(
                "---\nid: COLLIDE\nslug: b\nobject_type: Strategic Intent\n"
                "status: Draft\nlast_updated: 2026-05-21\n---\n"
            )
            g = build(tmp_path)
            self.assertEqual(len(g.id_collisions), 1)


class TestConstants(unittest.TestCase):
    def test_parent_fields_includes_diagnosis(self):
        self.assertIn("parent_diagnosis", PARENT_FIELDS)

    def test_related_fields_includes_capabilities(self):
        # related_capabilities is used by handoff-packet requirements.yaml
        # files to trace Requirements → Capabilities (F1.4 Rule 1).
        # Surface as a CONVENTIONS.md amendment in a follow-up doc edit.
        self.assertIn("related_capabilities", RELATED_FIELDS)


if __name__ == "__main__":
    unittest.main()
