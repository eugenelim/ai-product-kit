# Plan: audit-graph-walker

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

## Approach

Build `scripts/lib/graph.py` in three layers:
1. **Scanner** — walks `include_globs` from root, finds `.md` files, returns `(path, frontmatter)` tuples via `scripts.lib.frontmatter.parse_file`.
2. **Graph builder** — turns scan into `Node` objects keyed by id-or-path, walks `parent_*` / `related_*` fields to build `Edge` objects. Dangling edges recorded as edges to a non-existent node (`target_exists=False`).
3. **Query layer** — methods on `Graph` (`parents_of`, `walk_up`, `orphans`, `cycles`, etc.).

Tests drive each layer: scanner first against the fixture, then builder, then queries.

The fixture tree is the load-bearing test asset — realistic enough to exercise every downstream traceability rule, small enough to read in one screen.

## Constraints

- Stdlib + `scripts.lib.frontmatter` only.
- ≤ ~400 LOC for `graph.py`.
- Fixture files have valid frontmatter; the broken fixtures are isolated under `fixtures/broken/`.

## Tasks

### Task 1: Build the fixture tree

- **Depends on:** F1.2 shipped (need the parser).
- **Tests:** fixture exists; every valid file parses (non-None `Frontmatter`).
- **Approach:**
  - `scripts/tests/fixtures/sample-kit/`:
    - **Backbone chain 1** (the main 7-hop): `strategy/intents/north-star.md`, `discovery/trees/onboarding-funnel.md`, `validation/learnings/activation-cta.md`, `delivery/visions/passwordless.md`, `delivery/initiatives/auth-uplift/README.md`, `delivery/handoff-packets/auth-uplift/README.md`, `delivery/landings/passwordless.md`.
    - **Disconnected chain 2** (for the scope-filter test): `strategy/intents/cost-take-out.md` plus `discovery/trees/billing-leaks.md` (linked to intent #2 only).
    - **Domain E atomics** (for F1.4 traceability rules 1-5): `delivery/initiatives/auth-uplift/capabilities.md` listing 2 Capabilities; `delivery/handoff-packets/auth-uplift/requirements.yaml` listing 2 Requirements (each tracing to one Capability); `discovery/opportunities/passwordless-friction.md` containing a Problem with `evidence_basis:` populated.
    - **Domain D KPI**: a KPI declared inside `delivery/visions/passwordless.md` frontmatter under `predicted_outcomes:` with traced Outcome.
  - `scripts/tests/fixtures/broken/`: `dangling-parent.md` (parent_intent → nonexistent slug), `cycle-a.md` + `cycle-b.md` (mutual parents).
  - `scripts/tests/fixtures/README.md` documents what each fixture demonstrates and which contract test it backs.
- **Done when:** all valid files parse; broken files exist with documented breakage.

### Task 2: Write `scripts/tests/test_graph.py` (red)

- **Depends on:** Task 1.
- **Tests:** all 13 contract tests from spec §Contract tests.
- **Approach:** stdlib `unittest`. Each test pins scan root to a sub-path of the fixture tree.
- **Done when:** suite runs and all tests fail with ImportError.

### Task 3: Implement `scripts/lib/graph.py` (green)

- **Depends on:** Task 2.
- **Tests:** Task 2's tests pass.
- **Approach:**
  - `@dataclass Node`: id, slug, object_type, status, path, frontmatter.
  - `@dataclass Edge`: source, target, kind, target_exists.
  - `class Graph`: methods per spec.
  - `def build(root, include_globs=None, scope=None) -> Graph`.
  - Tarjan SCC for cycle detection; SCCs ≥ 2 = cycles; self-loops flagged separately.
  - Constants:
    - `PARENT_FIELDS = ("parent_diagnosis", "parent_intent", "parent_opportunity", "parent_learning", "parent_vision", "parent_initiative", "parent_handoff_packet")` — derived from HANDOVERS.md frontmatter examples (one entry per `parent_*` field shown across Handovers 1-7).
    - `RELATED_FIELDS = ("related_problems", "related_personas", "related_kpis")` — derived from CONVENTIONS.md universal schema. `related_capabilities` is NOT included (no source doc names it; if a future RFC adds it, append here with a citing comment).
  - `ORPHAN_RULES: dict[str, str]` — full enumeration of Domain I composite types and their required parent field, per HANDOVERS.md:
    - `"Opportunity Solution Tree" → "parent_intent"` (Handover 2)
    - `"Assumption Map" → "parent_opportunity"` (Handover 2.5 — when D7 ships)
    - `"Validation Learning Memo" → "parent_opportunity"` (Handover 3)
    - `"Vision" → "parent_learning"` (Handover 4)
    - `"Initiative" → "parent_vision"` (Handover 5)
    - `"Handoff Packet" → "parent_initiative"` (Handover 6)
    - `"Landing Report" → "parent_vision"` (Handover 7) — also accepts `parent_handoff_packet`
    - Strategic Intent has `parent_diagnosis` per HANDOVERS Handover 1 but treats it as optional (a diagnosis is a Strategy phase artifact, not a Domain I composite). Not in ORPHAN_RULES; surfaced as `weak` if absent.
  - `Edge.kind` is set to the source frontmatter field name verbatim (e.g., `"parent_initiative"`, `"related_kpis"`). This lets F1.4 filter edges by traceability rule precisely (e.g., Rule for Initiative→Vision requires `kind == "parent_vision"`).
- **Done when:** `python3 -m unittest scripts.tests.test_graph` exits 0.

## Rollout

- F1.4, F1.5, F1.6 each `from scripts.lib.graph import build, Graph` and write only audit-specific logic.
- ROADMAP F1.1 checked off.
- `scripts/lib/.gitkeep` removed.

## Risks

- **Fixture maintenance.** As HANDOVERS evolves, the fixture tree must too. Mitigation: `fixtures/README.md` lists what each file demonstrates.
- **Edge-kind hardcoding.** If HANDOVERS later names a new `parent_*` field, the walker misses it silently. Mitigation: `PARENT_FIELDS` constant at top of file is the single source of truth; cross-check is a follow-up.

## Changelog

- 2026-05-21: Initial plan.
