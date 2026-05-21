# Fixtures for scripts/tests/

Test fixtures consumed by `test_graph.py` (F1.1) and downstream audit-script tests.

## Layout

```
fixtures/
├── sample-kit/                 a minimal-but-realistic kit tree
│   ├── strategy/intents/       2 intents (chain 1 + chain 2 for scope-filter test)
│   ├── discovery/trees/        2 OSTs (one per intent)
│   ├── discovery/opportunities/ 1 Problem with evidence_basis populated
│   ├── validation/learnings/   1 surviving learning under chain 1
│   ├── delivery/visions/       1 vision under chain 1 with KPI/Outcome
│   ├── delivery/initiatives/auth-uplift/
│   │                           README, capabilities.md (2 Capabilities)
│   ├── delivery/handoff-packets/auth-uplift/
│   │                           README, requirements.yaml (2 Requirements)
│   └── delivery/landings/      1 landing under chain 1
└── broken/                     intentionally-malformed fixtures
    ├── dangling-parent.md      parent_intent → nonexistent slug
    ├── cycle-a.md              mutual parent_intent with cycle-b.md
    └── cycle-b.md              mutual parent_intent with cycle-a.md
```

## What each fixture demonstrates (and which test it backs)

| File | Demonstrates | Test |
|---|---|---|
| `sample-kit/strategy/intents/north-star.md` | Chain-1 root; Strategic Intent composite type | `test_walk_up_reaches_strategic_intent_root` |
| `sample-kit/strategy/intents/cost-take-out.md` | Disconnected chain-2 root | `test_scope_filter_returns_only_connected_subtree` |
| `sample-kit/discovery/trees/onboarding-funnel.md` | OST with `parent_intent`, chosen_opportunity flagged | `test_parents_of_returns_resolved_parents` |
| `sample-kit/discovery/trees/billing-leaks.md` | OST under chain-2; isolation test | `test_scope_filter_returns_only_connected_subtree` |
| `sample-kit/discovery/opportunities/passwordless-friction.md` | Problem with non-empty `evidence_basis` (list-of-maps) | F1.4 Rule 3 |
| `sample-kit/validation/learnings/activation-cta.md` | Learning Memo with status: survived | F1.4 Rule 1+2 chain |
| `sample-kit/delivery/visions/passwordless.md` | Vision with `predicted_outcomes` (KPI list) | F1.4 Rule 4 |
| `sample-kit/delivery/initiatives/auth-uplift/README.md` | Initiative with `capabilities` list | F1.4 Rule 1+2 |
| `sample-kit/delivery/initiatives/auth-uplift/capabilities.md` | 2 Capabilities, each traced to a Problem | F1.4 Rule 2 |
| `sample-kit/delivery/handoff-packets/auth-uplift/README.md` | Handoff Packet with `fixed_vs_flexible` | F1.4 Rule 7 |
| `sample-kit/delivery/handoff-packets/auth-uplift/requirements.yaml` | 2 Requirements each tracing to a Capability | F1.4 Rule 1 |
| `sample-kit/delivery/landings/passwordless.md` | Landing Report under chain 1 | F1.4 traversal |
| `broken/dangling-parent.md` | Edge target_exists=False | `test_dangling_edges_flags_broken_parent_link` |
| `broken/cycle-a.md` + `cycle-b.md` | Tarjan SCC ≥ 2 | `test_cycles_detects_two_node_cycle` |
