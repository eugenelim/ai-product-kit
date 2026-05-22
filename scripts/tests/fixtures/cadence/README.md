# Cadence-nudge fixtures

Fixture trees backing `scripts/tests/test_cadence_nudge.py`. All tests pin `today = date(2026, 5, 21)`.

| Fixture | Backs |
|---|---|
| `empty/` | `test_silent_on_empty_kit` |
| `all-fresh/` | `test_silent_when_all_within_thresholds`, `test_does_not_fire_orphan_ost_when_chosen_opportunity_set`, `test_does_not_fire_kill_drought_when_recent_killed_learning_exists` |
| `stale-strategy/` | `test_fires_stale_strategy_on_92_day_old_intent` |
| `boundary-strategy/` | `test_does_not_fire_stale_strategy_on_90_day_old_intent` |
| `orphan-ost/` | `test_fires_orphan_ost_when_chosen_opportunity_unset_and_ost_31d_old` |
| `kill-drought/` | `test_fires_kill_drought_when_no_killed_learning_in_60_days`, `test_fires_kill_drought_when_no_learnings_exist_and_chosen_opportunity_alive` (subset variants composed via script) |
| `chosen-already-killed/` | `test_does_not_fire_kill_drought_when_chosen_opportunity_already_killed` |
| `all-three-fire/` | `test_message_lists_all_firing_signals_in_one_block`, `test_message_under_600_chars`, `test_truncation_uses_ellipsis_when_value_list_exceeds_500` |

Each fixture parses cleanly through `scripts.lib.graph.build`. Use `build(fixture_root, include_globs=("strategy", "discovery", "validation"))` so the walker scopes to the cadence-relevant phases.
