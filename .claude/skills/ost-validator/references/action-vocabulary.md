# OST change-set action vocabulary

This document is the canonical reference for the nine action verbs that `scripts/validate_ost.py` accepts in a change set. The list and order mirror `.claude/skills/ost-validator/SKILL.md` line 40. The JSON-Schema enum in `ost-schema.json` is the mechanical enforcement; this document is the human-readable semantics.

> **Internal-consistency convention.** Every verb that takes an `id`, `ids[]`, `target`, `new_parent`, or `into` reference assumes the referenced node either exists in the input tree OR is added by an earlier action in the same change set. A change set that names a non-existent reference is **internally inconsistent**; the validator exits 2 (input error) with `reason: change-set-inconsistent`, not 1 (rule violation). This contract applies to all id-referencing verbs below.

## `add-outcome`

Adds the root Outcome.

- **Required fields.** `id` (the new Outcome id), `name`.
- **Behavior.** Sets `tree.outcome = {id, name, ...}`. Fails if the input tree already has an Outcome (only one Outcome per tree per `context/frameworks/opportunity-solution-tree.md` tree-shape rules).
- **Valid example.** `{"op": "add-outcome", "id": "OUT-001", "name": "Weekly active analysts producing a saved query"}`.
- **Common misuse.** Using `add-outcome` to rename an existing Outcome — use `reframe` instead.

## `add-opportunity`

Adds an Opportunity under an existing parent.

- **Required fields.** `id`, `name`, `parent`.
- **Behavior.** Appends a node `{id, type: "Opportunity", name, parent}` to `tree.nodes[]`. The parent must be the Outcome or another Opportunity (per the OST framework's tree-shape rules — Opportunities can decompose into sub-Opportunities).
- **Valid example.** `{"op": "add-opportunity", "id": "OPP-001", "name": "Analysts redo the same join logic across notebooks", "parent": "OUT-001"}`.
- **Common misuse.** Adding an Opportunity with a Solution as parent (category violation; Rule 2 catches it as an orphan because Solutions aren't valid Opportunity parents under the framework's layering).

## `add-solution`

Adds a Solution under exactly one Opportunity.

- **Required fields.** `id`, `name`, `parent`.
- **Behavior.** Appends `{id, type: "Solution", name, parent}` to `tree.nodes[]`. Parent must be an Opportunity (the framework explicitly forbids a Solution under two Opportunities — see Rule 6 compound-operation-visibility).
- **Valid example.** `{"op": "add-solution", "id": "SOL-001", "name": "Saved-query snippets pinned to the workspace sidebar", "parent": "OPP-001"}`.
- **Common misuse.** Adding the same Solution under two different Opportunities — split the Solution into two Solutions, or rebracket the Opportunities into one. The validator surfaces this as a tree-shape error at write time (per the framework's "Solutions are children of one Opportunity" rule).

## `reframe`

Rewrites a node's `name` in place.

- **Required fields.** `id`, `name` (the new name).
- **Behavior.** Updates `nodes[id].name`. Preserves the node's `id`, `parent`, child relationships, and `evidence_basis`.
- **Valid example.** `{"op": "reframe", "id": "OPP-001", "name": "Analysts cannot share saved query fragments across notebooks"}`.
- **Common misuse.** Using `reframe` to change a node's `type` (e.g., Opportunity → Solution) — that's a category change, not a reframe; use `delete` + `add-solution` and let Rule 4 (no-data-loss) audit the loss of the original Opportunity's evidence.

## `merge`

Combines two or more nodes into one.

- **Required fields.** `ids[]` (≥2 node ids, all of which must exist), `into` (one of the ids in `ids[]`).
- **Behavior.** The `into` node retains its id and name. The **union of all `evidence_basis` entries** across the merged nodes is assigned to `into`. **All children of the merged-not-`into` nodes are reparented to `into`.** The merged-not-`into` nodes are removed from the tree — **no separate `delete` action required**.
- **Valid example.** `{"op": "merge", "ids": ["OPP-001", "OPP-002"], "into": "OPP-001"}` — OPP-002's evidence is unioned into OPP-001; OPP-002's children become children of OPP-001; OPP-002 is removed.
- **Common misuse.** Listing an `into` that is not in `ids[]` (the validator exits 2: change-set-inconsistent). Or merging a Solution into an Opportunity — that's a category violation, not a merge; use `delete` instead.

## `split`

Replaces one node with two new nodes.

- **Required fields.** `id` (the source node, must exist), `into[]` (exactly two ids; one of them MAY equal `id`).
- **Behavior.** The source node is replaced by the two named new nodes (same type, same parent). **Children of the source are NOT automatically distributed** — the change set must follow `split` with explicit `reparent` actions for each child OR explicit `delete` actions if a child is genuinely dropped. Without follow-up actions for the children, the validator raises Rule 4 (no-data-loss) for each orphaned child.
- **Valid example.** `{"op": "split", "id": "OPP-001", "into": ["OPP-001", "OPP-003"]}` followed by `{"op": "reparent", "id": "SOL-001", "new_parent": "OPP-001"}` for each former child of OPP-001 that belongs under the surviving id.
- **Common misuse.** Forgetting to handle children. The most common shape of this bug: `split` an Opportunity, then both new ids end up with no Solutions even though the source had Solutions — the framework's "Solutions are children of one Opportunity" rule means each Solution must be explicitly reparented to exactly one of the new Opportunities.

## `delete`

Removes a node.

- **Required fields.** `id` (must exist in the input or have been added by an earlier action).
- **Behavior.** Removes the node. **Delete does NOT cascade.** Children of the deleted node become candidates for Rule 2 (no-orphans) and Rule 4 (no-data-loss). The change set must include explicit `reparent` or `delete` actions for every child of a deleted node; without them, the validator raises Rule 4 for each unhandled child. Likewise for `evidence_basis` entries on a deleted Opportunity — every `IS-NNN` reference must be explicitly re-attached to another Opportunity via `add-source-opportunity` or accepted as data loss.
- **Valid example.** `{"op": "delete", "id": "OPP-002"}` paired with explicit `reparent` actions for each former child of OPP-002.
- **Common misuse.** Deleting a parent without handling children — the most common Rule 4 violation. If the team genuinely intends to drop the children too, follow with explicit `delete` actions for each; the audit trail makes the data loss intentional.

## `reparent`

Moves a node to a different parent.

- **Required fields.** `id` (must exist in the input or have been added), `new_parent` (must exist in the input or have been added by an earlier action).
- **Behavior.** Updates `nodes[id].parent = new_parent`. Preserves the node's id, name, type, children, and `evidence_basis`.
- **Valid example.** `{"op": "reparent", "id": "SOL-001", "new_parent": "OPP-003"}`.
- **Common misuse.** Reparenting to a `new_parent` that exists nowhere in the tree (after the change set is applied). This is Rule 2 (no-orphans), not change-set-inconsistent — the orphan is a structural smell the rule catches at validation time.

## `add-source-opportunity`

Attaches an external source-opportunity reference to an Opportunity's `evidence_basis`.

- **Required fields.** `id` (the source reference; an `IS-NNN`-prefixed id), `target` (an Opportunity node id).
- **Behavior.** Appends `id` to `nodes[target].evidence_basis[]`. The source reference is NOT a node in `tree.nodes[]`; it lives only inside Opportunity `evidence_basis` arrays. Source references with the `IS-` prefix are subject to **Rule 3 (no-double-references)** — each `IS-NNN` may appear under at most one Opportunity. Other evidence prefixes (`ANL-NNN` analytics cohorts, `SUP-NNN` support threads) are unconstrained by Rule 3 and may appear under multiple Opportunities.
- **Valid example.** `{"op": "add-source-opportunity", "id": "IS-014", "target": "OPP-001"}`.
- **Common misuse.** Attaching the same `IS-NNN` to two Opportunities in the same change set — the validator surfaces this as Rule 3 (no-double-references). Or attaching a source to a Solution or AssumptionTest — only Opportunities carry `evidence_basis` per the framework.

## Cross-references

- `.claude/skills/ost-validator/SKILL.md` — the consumer-facing skill; this file is its reference.
- `.claude/skills/ost-validator/references/ost-schema.json` — the JSON-Schema mechanical enforcement for the action `op` enum and per-action common-field shapes.
- `context/frameworks/opportunity-solution-tree.md` — the tree-shape rules every verb above respects.
- `scripts/validate_ost.py` — the runnable validator implementing the six rules over change sets that use these verbs.
- `docs/specs/phase-2-discovery-primitives/spec.md` §"Per-action cascade semantics" — the spec's authoritative statement of the cascade behavior summarized here.
