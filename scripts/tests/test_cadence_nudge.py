"""Contract tests for scripts/cadence-nudge.py (F2.5).

All tests pin today=date(2026, 5, 21). Fixtures live under
scripts/tests/fixtures/cadence/<name>/.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path


# Load scripts/cadence-nudge.py as a module (the filename contains a dash, so
# we can't `import scripts.cadence_nudge`).
REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "cadence-nudge.py"
FIXTURE_ROOT = REPO_ROOT / "scripts" / "tests" / "fixtures" / "cadence"

_spec = importlib.util.spec_from_file_location("cadence_nudge", SCRIPT_PATH)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
sys.modules["cadence_nudge"] = _mod  # required so @dataclass can resolve cls.__module__
_spec.loader.exec_module(_mod)  # type: ignore[attr-defined]
run = _mod.run
compose = _mod.compose
stale_strategy = _mod.stale_strategy
orphan_ost = _mod.orphan_ost
kill_drought = _mod.kill_drought
is_empty_kit = _mod.is_empty_kit


from scripts.lib.graph import build  # noqa: E402

TODAY = date(2026, 5, 21)


def fx(name: str) -> Path:
    return FIXTURE_ROOT / name


class TestEmptyKit(unittest.TestCase):
    def test_silent_on_empty_kit(self):
        body = run(fx("empty"), TODAY)
        self.assertIsNone(body)


class TestAllFresh(unittest.TestCase):
    def test_silent_when_all_within_thresholds(self):
        body = run(fx("all-fresh"), TODAY)
        self.assertIsNone(body)


class TestStaleStrategy(unittest.TestCase):
    def test_fires_stale_strategy_on_92_day_old_intent(self):
        body = run(fx("stale-strategy"), TODAY)
        self.assertIsNotNone(body)
        self.assertIn("Stale strategy", body)
        self.assertIn("old-intent", body)

    def test_does_not_fire_stale_strategy_on_90_day_old_intent(self):
        body = run(fx("boundary-strategy"), TODAY)
        self.assertIsNone(body)


class TestOrphanOST(unittest.TestCase):
    def test_fires_orphan_ost_when_chosen_opportunity_unset_and_ost_31d_old(self):
        body = run(fx("orphan-ost"), TODAY)
        self.assertIsNotNone(body)
        self.assertIn("Orphan OST", body)
        self.assertIn("no-chosen", body)

    def test_does_not_fire_orphan_ost_when_chosen_opportunity_set(self):
        # all-fresh OST has chosen_opportunity: OPP-001 → no orphan-ost line.
        body = run(fx("all-fresh"), TODAY)
        if body is not None:
            self.assertNotIn("Orphan OST", body)


class TestKillDrought(unittest.TestCase):
    def test_fires_kill_drought_when_no_killed_learning_in_60_days(self):
        # kill-drought fixture: only `status: survived` learning >60d old.
        body = run(fx("kill-drought"), TODAY)
        self.assertIsNotNone(body)
        self.assertIn("Kill drought", body)

    def test_does_not_fire_kill_drought_when_recent_killed_learning_exists(self):
        body = run(fx("all-fresh"), TODAY)
        # all-fresh has a status:killed learning 29 days old → no kill-drought.
        if body is not None:
            self.assertNotIn("Kill drought", body)

    def test_fires_kill_drought_when_no_learnings_exist_and_chosen_opportunity_alive(self):
        # Build a graph from a slice of kill-drought (no learnings folder) by
        # using include_globs to omit `validation`. The cadence-nudge `run()`
        # uses default includes, so simulate via a direct call:
        graph = build(fx("kill-drought"), include_globs=("strategy", "discovery"))
        findings = kill_drought(graph, TODAY)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].signal, "kill-drought")
        # Drought-by-absence wording when zero learnings:
        self.assertTrue(any("no killed learnings on file" in v for v in findings[0].values))

    def test_does_not_fire_kill_drought_when_chosen_opportunity_already_killed(self):
        body = run(fx("chosen-already-killed"), TODAY)
        if body is not None:
            self.assertNotIn("Kill drought", body)


class TestComposition(unittest.TestCase):
    def test_message_lists_all_firing_signals_in_one_block(self):
        body = run(fx("all-three-fire"), TODAY)
        self.assertIsNotNone(body)
        self.assertIn("Stale strategy", body)
        self.assertIn("Orphan OST", body)
        self.assertIn("Kill drought", body)
        # One block: a single header line + signal bullets + footer.
        self.assertTrue(body.startswith("Cadence drift detected:"))
        self.assertIn("Consider:", body)

    def test_message_under_600_chars(self):
        body = run(fx("all-three-fire"), TODAY)
        self.assertIsNotNone(body)
        self.assertLess(len(body), 600, msg=f"len={len(body)}; body=\n{body}")

    def test_truncation_uses_ellipsis_when_value_list_exceeds_500(self):
        body = run(fx("all-three-fire"), TODAY)
        self.assertIsNotNone(body)
        # Five stale intents with ~100-char slugs → rendered value-list exceeds
        # 500 chars → items beyond index 1 are replaced with `…`.
        self.assertIn("…", body)
        # Sort is oldest-first, so the first two retained are the oldest
        # (stale-five 2026-01-01, stale-four 2026-01-05). The three newer
        # ones must be dropped.
        for missing in (
            "stale-three-with-quite-long-slug-name-for-truncation-testing-of-the-cadence-nudge-message-rendering",
            "stale-two-equally-verbose-slug-name-for-truncation-testing-of-the-cadence-nudge-message-rendering",
            "stale-one-with-a-rather-long-slug-name-for-truncation-testing-of-the-cadence-nudge-message-rendering",
        ):
            self.assertNotIn(missing, body)


class TestDegradation(unittest.TestCase):
    def test_graph_build_error_degrades_to_stderr_not_crash(self):
        # Subprocess test: run the script as a process with cwd=fixtures/broken
        # (or any malformed-fixture path). Confirm exit 0, no stdout JSON.
        broken_root = REPO_ROOT / "scripts" / "tests" / "fixtures" / "broken"
        if not broken_root.is_dir():
            self.skipTest("broken fixture not present")
        proc = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            cwd=str(broken_root),
            input="",
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(proc.returncode, 0)
        # If graph.build does not raise (it surfaces errors as data), stdout
        # may be empty (the broken fixture has no typed nodes of our 3 target
        # types). Either way: no crash.
        # We don't assert specifically on stderr — only that exit is 0.


if __name__ == "__main__":
    unittest.main()
