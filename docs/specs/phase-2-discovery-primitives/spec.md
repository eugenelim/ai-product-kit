# Spec: phase-2-discovery-primitives

- **Status:** Shipped (2026-05-28)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** Coupled batch of four kit components — one script, two skills, one agent. Mirrors the `foundation-4-frameworks-batch` and `phase-4-post-ship-commands` precedents of shipping a coupled batch under one work-loop when artifacts share a phase home and an upstream framework surface.
- **Serves kit phase:** Discovery (Phase 2)
- **Constrained by:** ROADMAP **P2.2** `skill-interview-snapshot`, **P2.5** `skill-opportunity-clustering`, **P2.8** `script-ost-validator`, **P2.13** `agent-discovery-coach`, **D4** `ost-validator references` (`references/ost-schema.json`, `references/action-vocabulary.md`, `references/examples/`); `context/frameworks/interview-snapshot.md` (F4.3, shipped) — the canonical schema P2.2 implements; `context/frameworks/opportunity-solution-tree.md` (F4.2, shipped) — the tree-shape rules P2.8 enforces; `context/frameworks/continuous-discovery.md` (F4.1, shipped) — the discipline P2.13 coaches toward; `.claude/skills/ost-validator/SKILL.md` (shipped) — the doctrine P2.8's script implements (skill stays in place as the consumer-facing reference; the script becomes its mechanical engine); `scripts/lib/frontmatter.py` (F1.2, shipped); `docs/CONVENTIONS.md` §"Specs and Plans" (kit-meta exemption); `.claude/skills/work-loop/SKILL.md`.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships four Phase-2 primitives under one work-loop: (1) the runnable OST validator script promoted from its existing skill doctrine, with the D4 reference set; (2) the `interview-snapshot` skill that codifies how raw transcripts become snapshots; (3) the `opportunity-clustering` skill that themes raw opportunities into clusters; (4) the `discovery-coach` agent that auto-invokes when a team is stuck on an opportunity. Together they close the lowest-coupling subset of Phase 2 (no Phase-2-internal dependencies on each other) and unblock the Phase-2 pipeline commands (P2.1, P2.3, P2.4, P2.6, P2.7, P2.9, P2.10) and the Phase-2 audit/narrative/digest commands (P2.11, P2.12, P2.14).

## Objective

Author four kit components, each implementing one ROADMAP Phase-2 item plus the D4 reference set bundled into P2.8. The four deliverables, in dependency order (P2.8 first because its references inform the other three):

| # | ROADMAP | Slug | Component type | Output path(s) |
|---|---|---|---|---|
| 1 | P2.8 + D4 | `script-ost-validator` | Python script + JSON schema + reference docs + tests | `scripts/validate_ost.py`, `scripts/tests/test_validate_ost.py`, `scripts/tests/fixtures/ost/`, `.claude/skills/ost-validator/references/ost-schema.json`, `.claude/skills/ost-validator/references/action-vocabulary.md`, `.claude/skills/ost-validator/references/examples/{valid,invalid}/` |
| 2 | P2.2 | `skill-interview-snapshot` | Skill | `.claude/skills/interview-snapshot/SKILL.md` |
| 3 | P2.5 | `skill-opportunity-clustering` | Skill | `.claude/skills/opportunity-clustering/SKILL.md` |
| 4 | P2.13 | `agent-discovery-coach` | Agent | `.claude/agents/discovery-coach.md` |

P2.8's script promotes the procedural doctrine already shipped in `.claude/skills/ost-validator/SKILL.md` (line 26: `python scripts/validate_ost.py ...`) from a doctrinal IOU to a runnable. The skill stays in place; the script becomes the engine the skill names.

## Why now

Three reasons. First, every other Phase-2 command in the ROADMAP — `/generate-ost`, `/update-ost`, `/extract-opportunities`, `/cluster-opportunities`, `/interview-snapshot`, `/audit-discovery-coherence` — depends on at least one of these four primitives. Without them, the Phase-2 pipeline cannot ship. Second, the four have **no Phase-2-internal dependencies on each other** — P2.8 needs F1.2 (shipped); P2.2 and P2.5 need F4.3 and F4.2 (both shipped); P2.13 needs F4.1 (shipped). They are the lowest-coupling batch in Phase 2 and the right place to start. Third, D4 (`references/ost-schema.json` + `action-vocabulary.md` + `examples/`) has been an open defer since the reconcile-and-harden pass on 2026-05-21; bundling it with P2.8 closes that defer in the same loop.

## Inputs and outputs

### P2.8 — `scripts/validate_ost.py` (the runnable validator)

**Inputs.** Three JSON files, all required: `--input <input-tree.json>`, `--output <output-tree.json>`, `--change-set <change-set.json>`. Optional `--format {json,human}` (default `json`; `human` prints a one-paragraph remediation summary for human reading). Optional `--schema <schema.json>` to override the bundled schema (used by tests).

**JSON tree shape** (single source of truth: `references/ost-schema.json`):

```json
{
  "outcome": {"id": "OUT-001", "name": "...", "metric": "..."},
  "nodes": [
    {"id": "OPP-001", "type": "Opportunity", "name": "...", "parent": "OUT-001", "evidence_basis": ["IS-001"]},
    {"id": "SOL-001", "type": "Solution", "name": "...", "parent": "OPP-001"},
    {"id": "AT-001",  "type": "AssumptionTest", "name": "...", "parent": "SOL-001", "threshold": "..."}
  ],
  "chosen_opportunity": {"id": "OPP-001", "rationale": "..."}
}
```

**Change-set shape** (single source of truth: `references/ost-schema.json`):

```json
{
  "actions": [
    {"op": "add-outcome",            "id": "OUT-001", "name": "..."},
    {"op": "add-opportunity",        "id": "OPP-001", "name": "...", "parent": "OUT-001"},
    {"op": "add-solution",           "id": "SOL-001", "name": "...", "parent": "OPP-001"},
    {"op": "reframe",                "id": "OPP-001", "name": "..."},
    {"op": "merge",                  "ids": ["OPP-001", "OPP-002"], "into": "OPP-001"},
    {"op": "split",                  "id": "OPP-001",  "into": ["OPP-001", "OPP-003"]},
    {"op": "delete",                 "id": "OPP-002"},
    {"op": "reparent",               "id": "SOL-001", "new_parent": "OPP-003"},
    {"op": "add-source-opportunity", "id": "IS-001",  "target": "OPP-001"}
  ]
}
```

The 9 action verbs above are exactly the vocabulary the existing skill names, and in the same order (line 40 of `.claude/skills/ost-validator/SKILL.md`).

**Per-action cascade semantics** (the rules Rule 1 and Rule 4 depend on; documented authoritatively in `references/action-vocabulary.md`):

- `add-outcome` — creates the root. Fails if an outcome already exists.
- `add-opportunity` — adds an Opportunity under an existing parent (Outcome or Opportunity).
- `add-solution` — adds a Solution under exactly one existing Opportunity.
- `reframe` — rewrites a node's `name` in place; preserves id, parent, children, and `evidence_basis`.
- `merge` — `ids[]` lists ≥2 node ids that must all exist; `into` is one of them. After the action: the `into` node retains its id; the **union of all `evidence_basis` entries** across merged nodes is assigned to `into`; **all children of the merged-not-`into` nodes are reparented to `into`**; the merged-not-`into` nodes are removed from the tree (no separate `delete` action required).
- `split` — `id` must exist; `into[]` is exactly two ids, one of which may equal `id`. After the action: the source node is replaced by the two new nodes; **children of the source are NOT distributed automatically** — the change set must follow `split` with explicit `reparent` actions for each child, OR with explicit `delete` actions if a child is genuinely dropped.
- `delete` — `id` must exist. **Delete does NOT cascade.** Children of a deleted node become candidates for Rule 2 (no-orphans) and Rule 4 (no-data-loss). The change set must include explicit `reparent` or `delete` actions for every child of a deleted node; without them, the validator raises Rule 4.
- `reparent` — `id` and `new_parent` must both exist after the change set is applied (not necessarily in the input). Reparent to a non-existent target is itself a Rule 2 violation.
- `add-source-opportunity` — `id` is an `IS-NNN`-prefixed source-opportunity reference; `target` is an Opportunity node id. Source opportunities are not nodes in the tree's `nodes[]`; they live inside an Opportunity's `evidence_basis:` array. See "Source-opportunity id convention" below.

**Source-opportunity id convention.** A source opportunity is an external evidence reference (interview snapshot, observed behavior, support thread) attached to an Opportunity via its `evidence_basis:` array. Source-opportunity ids carry the `IS-` prefix (e.g., `IS-001`, `IS-042`). Rule 3 (no-double-references) applies **only to entries whose id matches the `IS-NNN` pattern**; other evidence references (e.g., analytics cohorts named `ANL-NNN`, support threads named `SUP-NNN`) are not constrained by Rule 3 and may appear under multiple Opportunities.

**Outputs.** Exit 0 on validation pass. Exit 1 on validation failure (rule violation). Exit 2 on input error (file missing, malformed JSON, schema violation, internally-inconsistent change set such as `merge` naming a non-existent id). On failure, JSON report to stderr matching this shape:

```json
{
  "verdict": "fail",
  "violations": [
    {"rule": "no-orphans", "node_id": "SOL-002", "remediation": "node SOL-002 has parent OPP-099 which does not exist after change set applied; either add OPP-099 or reparent SOL-002"}
  ]
}
```

**Output destination by `--format`:**

| `--format` | On pass (exit 0) | On rule violation (exit 1) | On input error (exit 2) |
|---|---|---|---|
| `json` (default) | stdout silent; stderr silent | stderr: JSON failure report; stdout silent | stderr: JSON `{"verdict": "error", "reason": "<one of: missing-file, malformed-json, schema-violation, change-set-inconsistent>", "detail": "..."}`; stdout silent |
| `human` | stdout: one line `"Validation passed (N nodes, M actions)."`; stderr silent | stderr: one paragraph naming the rule and the remediation; stdout silent | stderr: one paragraph naming the error and the offending input; stdout silent |

The destination contract: **stdout is for human/orchestrator-readable pass-state confirmation only; stderr is for everything else.** A pass with `--format json` is silent on both streams (exit code alone is the signal). A pass with `--format human` writes one short confirmation line to stdout. Anything written to stderr is a failure or error.

The six rules from the skill (lines 38–43):

1. **Change-set determinism** — applying actions to input must produce output node-for-node.
2. **No orphans** — every non-root node has a parent in the output.
3. **No double-references** — each source opportunity appears under exactly one tree opportunity.
4. **No data loss** — every source opportunity and child of the input is accounted for in the output.
5. **Valid action vocabulary** — only the 9 actions above.
6. **Compound-operation visibility** — if sources moved between tree opportunities, the change set must contain the intermediate split/merge that explains the move.

### P2.2 — `.claude/skills/interview-snapshot/SKILL.md`

**Inputs.** Raw transcript text (the orchestrator pastes it or names a file). Optional `interviewer` and `date` overrides. Optional `recording_present` boolean (defaults true; false triggers the no-recording quote-attribution path documented in `context/frameworks/interview-snapshot.md`).

**Outputs.** A proposal block with the eight snapshot fields per `context/frameworks/interview-snapshot.md` (Goal, Workflow, Pain Points, Workarounds, Tools, Direct Quote, Date, Interviewer). The skill **never persists**; it proposes. The orchestrator (or a downstream command like `/interview-snapshot`) decides where to file.

Speaker-detection and time-aligned-quote-extraction rules are the skill's job (per the ROADMAP one-liner for P2.2). The framework reference is doctrine; the skill is the transformation rule library.

### P2.5 — `.claude/skills/opportunity-clustering/SKILL.md`

**Inputs.** A list of raw opportunity candidates (typically the output of a future `/extract-opportunities` run, or pasted manually). Each candidate is a one-line statement plus optional `evidence_basis:` link.

**Outputs.** A proposal block: clusters of opportunities grouped by theme, with a one-line cluster name and the constituent candidate ids. Skill never persists; it proposes.

### P2.13 — `.claude/agents/discovery-coach.md`

**Inputs.** Invocation context: an OST whose `chosen_opportunity:` is set but whose corresponding subtree has zero Solutions, or whose Solutions have zero Assumption Tests — the "stuck" condition. Manually invocable by the orchestrator; auto-invoke is deferred (see Open questions).

**Outputs.** A coaching prompt sequence (not a finished artifact): 3–5 open questions the team can answer that unblock divergent generation. Returns proposed Solutions or Assumption Tests as candidates; never persists. Model: `sonnet` (judgment-heavy; not fan-out-cheap).

## Boundaries

### Always do

- Treat the existing `.claude/skills/ost-validator/SKILL.md` as the **source of truth** for the six rules and the 9-verb action vocabulary. The script implements; it does not redefine.
- Treat `context/frameworks/interview-snapshot.md` as the **source of truth** for the eight-field snapshot schema and the paraphrase/ambiguity/no-recording rules. The skill operationalizes; it does not redefine.
- Treat `context/frameworks/opportunity-solution-tree.md` as the **source of truth** for what an Opportunity is. The clustering skill does not change the definition.
- Author all JSON test fixtures under `scripts/tests/fixtures/ost/{valid,invalid}/` with one fixture per rule + one all-valid baseline. Each invalid fixture must exercise exactly one rule violation (test isolation).
- Atomic-write any file the script produces (`tmp + os.replace`). The script only writes when explicitly asked via a flag; no flag in this batch (read-only validator), so this is forward-compatible discipline only.
- Lint each component with its matching linter before declaring task done: `tools/lint-skill.sh` for skills, `tools/lint-agent.sh` for the agent. The script is checked by `python -m unittest`.

### Ask first

- **Renaming any of the 9 action verbs** in the action vocabulary. They are pinned by the existing skill; changing them is a contract break across any future `/generate-ost` and `/update-ost` consumer. If a rename is genuinely needed, surface as an RFC, not as a silent script-side rename.
- **Extending the JSON tree shape** beyond what the existing skill implies (e.g., adding a per-node `risk_level` field). The validator implements; spec changes go upstream first.
- **Adding new validation rules** beyond the six the skill names. The skill is canon; new rules surface as a skill update + spec update first.

### Never do

- **Never re-implement the snapshot schema** inside the `interview-snapshot` skill. The skill points at the framework reference and adds *operational* rules (how to detect speakers in a raw transcript, how to time-align quotes); it does not redefine the eight fields.
- **Never persist OSTs from the validator.** The script is read-only by contract. Persistence is the orchestrator's job (`/generate-ost`, `/update-ost`).
- **Never auto-promote candidate Opportunities in the clustering skill.** Clustering is a *proposal* operation; promoting candidates into the OST is a downstream command's job and requires a human acceptance.
- **Never bypass `evidence_basis:` requirements in any of the four components.** An Opportunity without evidence is conjecture; downstream artifacts that consume these primitives must see the gap, not have it papered over.
- **Never make the discovery-coach agent persist suggestions.** It returns candidates for human review.

## Verification mode

Mixed by component:

- **P2.8 (script)** — **TDD**. Every rule has at least one invalid-fixture test (rule violation) and the all-valid baseline must pass. The unit-test suite under `scripts/tests/test_validate_ost.py` is the gate. Run via `python -m unittest scripts.tests.test_validate_ost -v`.
- **P2.2, P2.5 (skills)** — **Goal-based check**. `tools/lint-skill.sh` exits 0; **the framework reference's path (`context/frameworks/interview-snapshot.md` for P2.2; `context/frameworks/opportunity-solution-tree.md` for P2.5) appears at least once in the body, AND the body does NOT contain any verbatim enumeration of the framework's canonical schema** (for P2.2 specifically: the body does not contain a list/heading enumeration of all eight snapshot field names `Goal / Workflow / Pain Points / Workarounds / Tools / Direct Quote / Date / Interviewer` as a definitional list — only as a `@see` pointer or inline reference). Both checks are mechanical greps.
- **P2.13 (agent)** — **Goal-based check**. `tools/lint-agent.sh` exits 0; the body documents the two named stuck-condition triggers (no-Solutions-under-chosen-Opportunity; Solutions-present-but-zero-Assumption-Tests) and a 3–5-question prompt pattern with one named example per trigger.

Cross-cutting: the existing skill (`.claude/skills/ost-validator/SKILL.md`) is updated only if its line 25 invocation snippet drifts from what the script accepts (the snippet currently reads `python scripts/validate_ost.py --input ... --output ... --change-set ...` — the script must accept this verbatim; if the script requires extra flags, the skill is updated in the same commit).

## Contract tests

### P2.8 contract tests (`scripts/tests/test_validate_ost.py`)

1. `test_all_valid_baseline_passes` — apply a valid change set to a valid input; output matches; exit 0; stdout silent (json default); stderr silent.
2. `test_orphan_node_fails_with_rule_no_orphans` — invalid fixture with one orphan Solution (the Solution's parent does not exist in the output); exit 1; JSON violation names rule `no-orphans` and the orphan node id.
3. `test_reparent_to_nonexistent_parent_fails_with_rule_no_orphans` — change set contains `reparent SOL-001 → OPP-999` where `OPP-999` exists nowhere; exit 1; rule `no-orphans`.
4. `test_double_reference_fails_with_rule_no_double_references` — same `IS-NNN`-prefixed source opportunity under two tree Opportunities' `evidence_basis:`; exit 1; rule `no-double-references`.
5. `test_non_is_evidence_under_two_opportunities_passes` — same `ANL-NNN` (analytics cohort) under two Opportunities' `evidence_basis:`; exit 0. Rule 3 applies only to `IS-NNN` ids.
6. `test_data_loss_fails_with_rule_no_data_loss` — input has source opportunity X attached to OPP-001; change set deletes OPP-001 without an explicit transfer of X; exit 1; rule `no-data-loss`.
7. `test_delete_with_children_fails_with_rule_no_data_loss` — change set deletes an Opportunity that has a Solution child, with no explicit `delete` or `reparent` action for the child; exit 1; rule `no-data-loss`.
8. `test_invalid_action_verb_fails_with_rule_valid_action_vocabulary` — change set contains action verb `transmogrify`; exit 1; rule `valid-action-vocabulary`.
9. `test_silent_move_fails_with_rule_compound_operation_visibility` — sources moved between tree Opportunities without intermediate split/merge; exit 1; rule `compound-operation-visibility`.
10. `test_non_deterministic_change_set_fails_with_rule_change_set_determinism` — applying actions to input does NOT produce output (extra node in output not explained by change set); exit 1; rule `change-set-determinism`.
11. `test_empty_input_tree_with_add_actions_passes` — input tree `{"nodes": []}` plus a change set of one `add-outcome` + one `add-opportunity`; exit 0. Rule 4 does not flag added-but-not-in-input nodes.
12. `test_empty_change_set_identical_input_output_passes` — `actions: []`, input equals output; exit 0.
13. `test_empty_change_set_with_different_output_fails_rule_1` — `actions: []`, output differs from input; exit 1; rule `change-set-determinism`.
14. `test_malformed_input_json_exits_2` — input file is not valid JSON; exit 2; stderr JSON `verdict: error`, `reason: malformed-json`.
15. `test_missing_input_file_exits_2` — input file does not exist; exit 2; `reason: missing-file`.
16. `test_schema_violation_exits_2` — input is valid JSON but does not match top-level shape (e.g., `outcome` field missing); exit 2; `reason: schema-violation`.
17. `test_merge_with_nonexistent_id_exits_2` — change set contains `merge` naming an id absent from the input; exit 2; `reason: change-set-inconsistent`.
18. `test_human_format_failure_writes_paragraph_to_stderr` — with `--format human` on a rule violation, stderr contains a paragraph (≥2 sentences); stdout silent.
19. `test_human_format_pass_writes_confirmation_to_stdout` — with `--format human` on a pass, stdout has the one-line `"Validation passed (N nodes, M actions)."` confirmation; stderr silent.
20. `test_json_format_pass_silent_on_both_streams` — with `--format json` on a pass, stdout silent; stderr silent; exit 0.

### P2.2 contract tests (manual gesture)

- Fresh session loads the skill, pastes the framework reference's "concrete contrast" transcript snippet (the spreadsheet → deck case), and the skill produces a proposal block that records the paraphrase-rule-compliant version. Recorded under `docs/specs/phase-2-discovery-primitives/notes/manual-verification-p2.2.md`.

### P2.5 contract tests (manual gesture)

- Fresh session loads the skill, pastes a six-candidate opportunity list with three thematic clusters apparent, and the skill produces a proposal with three clusters. Recorded under `notes/manual-verification-p2.5.md`.

### P2.13 contract tests (manual gesture)

- Fresh session loads the agent, presents an OST with `chosen_opportunity:` set but zero Solutions under that Opportunity, and the agent returns 3–5 open questions plus candidate Solutions. Recorded under `notes/manual-verification-p2.13.md`.

### Cross-cutting

- `tools/lint-skill.sh` exits 0 on both new SKILL.md files.
- `tools/lint-agent.sh` exits 0 on the new agent.md.
- `tools/pre-pr.sh` exits 0 across the whole batch.

## Non-goals

- **Not building `/interview-snapshot`, `/extract-opportunities`, `/cluster-opportunities`, `/generate-ost`, `/update-ost`, or `/audit-discovery-coherence`.** Those are P2.1, P2.4, P2.6, P2.7, P2.9, P2.11 — Batch B and Batch C work.
- **Not building the `interview-coder` agent (P2.3) or the `opportunity-merger` agent (P2.10).** Both depend on commands not in this batch.
- **Not modifying `context/frameworks/interview-snapshot.md`, `opportunity-solution-tree.md`, or `continuous-discovery.md`.** They are canon; the new components consume them.
- **Not updating `.claude/skills/ost-validator/SKILL.md`** beyond what's required to make its invocation snippet match the shipped script's CLI. The doctrine stays.
- **Not authoring an audit script that runs the validator on every OST under `discovery/trees/**`.** That's F2.7 (`hook-validate-ost`), explicitly downstream of P2.8.
- **Not adding new ontology types.** The Opportunity / Solution / Assumption Test / Outcome types exist in `context/frameworks/ontology.md`; the validator uses them as-is.

## Open questions

- **JSON-vs-markdown OST input.** The existing skill's invocation snippet implies JSON input. The kit's OSTs are authored in markdown with frontmatter (`templates/ost.md`). The validator works on JSON projections. **Who answers:** the orchestrator of P2.7 (`/generate-ost`) and P2.9 (`/update-ost`) — they will emit JSON projections alongside the markdown OST. **When:** at first usage during P2.7 build. **Workaround for this batch:** the validator takes JSON; the markdown-to-JSON projection is the consuming command's job, not the validator's. The script's `--help` will name this contract explicitly.
- **Stuck-condition auto-invoke for `discovery-coach`.** The trigger is documented in the agent body but is not yet wired (no hook fires it). **Who answers:** ROADMAP item that wires the trigger (likely a future scheduled-agents addition; not in this batch). **When:** when a real PM hits the stuck condition in practice. **For this batch:** the agent is invocable manually; auto-invoke is a forward-compatible posture.
- **Schema-validation split between JSON Schema and code-side checks.** The bundled `references/ost-schema.json` enforces **top-level shape only** — the presence of `outcome`, `nodes`, `chosen_opportunity` at the tree root; the presence of `actions` at the change-set root; and per-element types (string id, string name, array `evidence_basis`). **Per-node-type required fields** (e.g., `AssumptionTest` requires `threshold`; `Opportunity` requires `evidence_basis`) are validated in the script's `_validate_node_types(...)` function, not by the schema. Rationale: implementing JSON Schema `oneOf` / `if-then-else` in the stdlib-only subset would roughly triple the schema-validator code; splitting concerns keeps the schema and the script each readable. **Trade-off:** a downstream consumer that reuses the schema without the script will get top-level validation only. The schema's header comment names this explicitly so a future consumer doesn't expect more.
- **discovery-coach visibility surface for PMs.** The agent is invocable manually but a PM hitting the stuck condition needs a discovery surface (a sentence in `context/frameworks/opportunity-solution-tree.md` §"Common failure modes" that points at the agent). Recorded as `notes/deferred-findings.md` D-H3 for the next Phase-2 work-loop; not blocking this batch.

## Acceptance criteria

- [ ] `scripts/validate_ost.py` exists; `python -m unittest scripts.tests.test_validate_ost -v` returns 0 with ≥ 20 named tests, including one per rule plus the malformed/missing-input/schema-violation/change-set-inconsistent input-error cases plus the empty-tree, empty-change-set, reparent-to-missing-parent, delete-with-children, and non-IS-evidence edge cases named in §"Contract tests".
- [ ] `scripts/tests/fixtures/ost/valid/` contains the all-valid baseline triple (input, output, change-set).
- [ ] `scripts/tests/fixtures/ost/invalid/` contains one triple per rule violation (6 rules).
- [ ] `.claude/skills/ost-validator/references/ost-schema.json` is a valid JSON Schema covering both tree and change-set shapes.
- [ ] `.claude/skills/ost-validator/references/action-vocabulary.md` documents the 9 action verbs with one-paragraph semantics each.
- [ ] `.claude/skills/ost-validator/references/examples/` contains at least one valid + one invalid example triple (the invalid case names which rule it violates).
- [ ] `.claude/skills/ost-validator/SKILL.md`'s invocation snippet matches the shipped script's CLI exactly.
- [ ] `.claude/skills/interview-snapshot/SKILL.md` exists, has the required frontmatter (name/description/license), passes `tools/lint-skill.sh`, and the body cites `context/frameworks/interview-snapshot.md` as canon.
- [ ] `.claude/skills/opportunity-clustering/SKILL.md` exists, passes `tools/lint-skill.sh`, body cites `context/frameworks/opportunity-solution-tree.md`.
- [ ] `.claude/agents/discovery-coach.md` exists, has frontmatter (name/description/tools/model with `model: sonnet`), passes `tools/lint-agent.sh`, body documents the stuck-condition triggers.
- [ ] `tools/pre-pr.sh` exits 0 across the whole repo.
- [ ] `ROADMAP.md` rows P2.2, P2.5, P2.8, P2.13, D4 are marked `[x]` with `**Shipped:** 2026-05-28`.
- [ ] `docs/INVENTORY.md` has rows for the four shipped components.
- [ ] `.claude/skills/README.md` and `.claude/agents/README.md` reference the new components.
- [ ] `AGENTS.md` and `.claude/CLAUDE.md` are not edited (no policy change; primitives are pure additions).

## Cross-references

- **Consumed by (when shipped):** `/interview-snapshot` (P2.1), `/extract-opportunities` (P2.4), `/cluster-opportunities` (P2.6), `/generate-ost` (P2.7), `/update-ost` (P2.9), `/audit-discovery-coherence` (P2.11), `hook-validate-ost` (F2.7), `interview-coder` (P2.3), `opportunity-merger` (P2.10).
- **Consumes:** `scripts/lib/frontmatter.py` (F1.2, shipped); `context/frameworks/interview-snapshot.md` (F4.3); `context/frameworks/opportunity-solution-tree.md` (F4.2); `context/frameworks/continuous-discovery.md` (F4.1); `.claude/skills/ost-validator/SKILL.md` (existing doctrine).
- **Frontmatter fields owned:** none directly — primitives consume `evidence_basis:`, `chosen_opportunity:`, `parent_intent:` (defined in `docs/CONVENTIONS.md`); they do not introduce new fields.
- **Ontology object types touched:** *Interview Snapshot* (Domain B), *Opportunity* (Domain C), *Solution / Feature / Capability* (Domain E), *Assumption Test / Experiment* (Domain C), *Outcome* (Domain D), *Opportunity Solution Tree* (Domain I composite). All read-only — no new types introduced.
