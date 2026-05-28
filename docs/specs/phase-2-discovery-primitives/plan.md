# Plan: phase-2-discovery-primitives

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Approved
- **Plan review:** approved (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for shipping P2.2 + P2.5 + P2.8 (with D4 references) + P2.13 in a single coupled work-loop. The four components are independent enough to build in parallel after the schema is locked, but they share lint, verify, review, and capture gates.

## Approach

**Stage 1 — Schema-first.** Author `references/ost-schema.json` and `references/action-vocabulary.md` first. They are the contract every other piece of P2.8 (script, tests, fixtures, examples) leans on. Authoring out-of-order produces drift that only surfaces in REVIEW.

**Stage 2 — Build P2.8 script TDD.** Write fixtures first, then `test_validate_ost.py` as red tests against a stub script, then implement `validate_ost.py` rule-by-rule until all 20 tests pass. The six rules are independent functions; the script's `main()` composes them. Stdlib only (`json`, `argparse`, `pathlib`); no third-party JSON-schema library — implement an in-line schema validator that enforces **top-level shape only** (`type`, `required`, `enum`, `properties`, `items`, `additionalProperties`); per-node-type required fields (e.g., `AssumptionTest` requires `threshold`; `Opportunity` requires `evidence_basis`) are checked in a dedicated `_validate_node_types(...)` function. This split keeps the schema in a stdlib-friendly subset and makes per-type validation diff-able with the rule functions. The schema-file header comment names this split explicitly so a downstream consumer doesn't expect more.

**Stage 3 — Parallel-build P2.2, P2.5, P2.13 with implementer subagents.** Each is a single markdown file with frontmatter + body. They have no code dependencies on each other, on T1, or on T2 — they can dispatch immediately after spec approval. Dispatch three `general-purpose` implementer subagents in one message (preferred per `~/.claude/CLAUDE.md` guidance; fall back to sequential on cascade-fail per the noted bug). Each agent's brief: read the spec + plan + the relevant framework reference + an exemplar — **for the two skills the exemplar is `.claude/skills/ears-lint/SKILL.md`** (a rule-library skill for a specific transformation, the closest shape match to interview-snapshot and opportunity-clustering, not `ontology-classifier` which is a fan-out classifier with a different body shape); **for the agent the exemplar is `.claude/agents/traceability-walker.md`**. Each brief names exactly the required H2 sections (per T3/T4/T5 below) so the three deliverables share structure. The orchestrator lints after each returns.

**Why this sequencing.** P2.8 has real code dependencies (schema → fixtures → tests → script). Stages 1–2 cannot parallelize past schema lock. Stage 3 components are independent prose deliverables fully decoupled from Stages 1–2; running Stage 3 concurrently with Stage 2 cuts wall time and reduces lock-up risk if Stage 2 runs over.

## Constraints

- **Stdlib only** for `validate_ost.py`. No `jsonschema`, no `pyyaml`. The kit's `scripts/lib/frontmatter.py` (F1.2) is YAML-subset for frontmatter only; OST inputs are pure JSON, so even that dependency is unneeded.
- **Atomic-write** any file the script produces. The script is read-only by design in this batch, so this discipline applies to test-fixture authoring only.
- **No edits** to `context/frameworks/*.md`, `AGENTS.md`, `.claude/CLAUDE.md`, or `docs/CONVENTIONS.md`. Spec-pinned in §"Non-goals" and §"Acceptance criteria".
- **Skill / agent body cap** — skill bodies ≤ 250 lines target (the `lint-skill.sh` soft cap is 400; tighter local target keeps doctrine readable); agent body ≤ 200 lines (no formal lint cap, but matches `traceability-walker`'s shape).
- **Existing skill** — `.claude/skills/ost-validator/SKILL.md` is canon for the rule list and action vocabulary. The script implements its semantics verbatim. If the script needs extra CLI flags beyond the snippet on line 26, update the snippet in the **same commit** as the script (drift is a bug per CLAUDE.md).
- **Test isolation** — each invalid fixture exercises exactly one rule violation. Mixing two violations in one fixture makes diagnostic remediation messages ambiguous.
- **Date discipline** — all `Shipped:` timestamps use 2026-05-28 (today, per session context).
- **Branch hygiene** — work continues on the renamed `eugenelim/phase-2-roadmap` branch. Commit per task with conventional-commits format and `Spec:` footer.
- **State.json discipline** — `iteration_count` increments on each REVIEW pass that returns findings; hard cap 5 per `state.json` `max_iterations`.

## Construction tests

The cross-cutting checks (not specific to one task):

- `tools/pre-pr.sh` exits 0 across the whole repo at the end of EXECUTE.
- `tools/lint-frontmatter.py` (default mode) does not regress against the kit's existing artifacts.
- The new `.claude/skills/ost-validator/references/examples/{valid,invalid}/` triples must themselves pass / fail through the validator script (self-consistency check — the examples are tests of the examples).

## Tasks

The work-breakdown. Tasks T1–T2 are serial (schema → script). T3, T4, T5, T6 are parallelizable after T2 is green.

### Task T1: ship the JSON Schema + action-vocabulary reference

- **Depends on:** none
- **Tests:**
  - `references/ost-schema.json` parses as valid JSON.
  - `references/ost-schema.json` schema validates the spec's example tree-shape and change-set-shape JSON snippets (mechanical check via a one-liner Python harness in T2's tests, deferred there).
  - `references/action-vocabulary.md` documents exactly 9 action verbs (named in the spec); body length ≤ 150 lines.
- **Approach:**
  - Author `references/ost-schema.json` with two top-level definitions: `tree` (outcome + nodes[] + chosen_opportunity) and `change-set` (actions[]).
  - Each action `op` has its own required-field profile (e.g., `merge` requires `ids[]` + `into`; `reparent` requires `id` + `new_parent`).
  - Use JSON Schema draft-07 (broadest tool support).
  - Author `references/action-vocabulary.md` with one H2 per verb: semantics, required fields, one valid example, one common misuse.
- **Done when:** both files exist; the schema parses; the vocabulary doc names the 9 verbs and is lint-clean (markdown only).

### Task T2: ship `validate_ost.py` + tests + fixtures (TDD)

- **Depends on:** T1
- **Tests:** the 20 tests named in spec §"P2.8 contract tests".
- **Approach:**
  - Create fixtures first under `scripts/tests/fixtures/ost/`:
    - `valid/baseline/{input,output,change-set}.json` — the all-valid triple.
    - `valid/empty-input-tree-add-actions/...` — input has `nodes: []`; change set adds outcome + opportunity.
    - `valid/empty-change-set-identical/...` — input equals output; `actions: []`.
    - `valid/non-is-evidence-under-two-opportunities/...` — same `ANL-001` under two Opportunities (Rule 3 does not apply).
    - `invalid/no-orphans/{input,output,change-set}.json` — change-set produces an orphan Solution.
    - `invalid/no-orphans-reparent-to-missing/...` — reparent to `OPP-999` which exists nowhere.
    - `invalid/no-double-references/...` — same `IS-001` referenced under two tree Opportunities.
    - `invalid/no-data-loss/...` — source opportunity dropped without delete or reparent.
    - `invalid/no-data-loss-delete-with-children/...` — delete an Opportunity whose Solution child is not explicitly handled.
    - `invalid/valid-action-vocabulary/...` — change-set contains `transmogrify`.
    - `invalid/compound-operation-visibility/...` — sources move between tree opportunities with no intermediate split/merge.
    - `invalid/change-set-determinism/...` — output has an extra node not produced by the actions.
    - `invalid/change-set-determinism-empty-actions/...` — `actions: []`, output differs from input.
    - `error/malformed-json/...` — input file is not parseable JSON.
    - `error/missing-file/...` — input path does not exist (referenced from the test, not a fixture file).
    - `error/schema-violation/...` — JSON valid but `outcome` field missing.
    - `error/change-set-inconsistent-merge/...` — `merge` names an id absent from the input.
  - Write `scripts/tests/test_validate_ost.py` against a stub script (red).
  - Implement `scripts/validate_ost.py`:
    - `argparse` CLI matching the spec.
    - `_load_json(path) -> dict` with `exit(2)` on `FileNotFoundError` (`reason: missing-file`) or `JSONDecodeError` (`reason: malformed-json`).
    - `_validate_schema(doc, schema)` — implements the stdlib-subset (`type`, `required`, `enum`, `properties`, `items`, `additionalProperties`) for **top-level shape only**; `exit(2)` with `reason: schema-violation` on failure.
    - `_validate_node_types(tree)` — per-node-type required-field checks (e.g., `Opportunity` ⇒ `evidence_basis`; `AssumptionTest` ⇒ `threshold`); `exit(2)` with `reason: schema-violation` on failure.
    - `_check_change_set_internal_consistency(change_set, input_tree)` — confirms all action ids reference nodes that exist in the input or are added by an earlier action in the same change set; `exit(2)` with `reason: change-set-inconsistent` on failure.
    - `_apply_change_set(input_tree, change_set) -> dict` — pure function returning the computed-output tree. Implements the cascade semantics defined in spec §"Inputs and outputs" (merge unions evidence + reparents children; split does NOT auto-distribute; delete does NOT cascade).
    - Six rule functions returning `[{rule, node_id, remediation}]`.
    - `main()` composes: load → schema-validate top-level → validate node types → check change-set internal consistency → apply → compare to output (Rule 1) → run remaining rules → emit JSON or human report per the §"Output destination by `--format`" table → exit 0/1.
  - Iterate until all 20 tests pass (green).
  - Refactor if there's duplication across rule functions; tests stay green.
- **Done when:** `python -m unittest scripts.tests.test_validate_ost -v` exits 0 with 20 named tests; the script's `--help` describes the JSON-input contract; `--format human` on a pass writes the confirmation line to stdout per the §"Output destination" table.

### Task T3: ship `.claude/skills/interview-snapshot/SKILL.md`

- **Depends on:** none (no T1/T2 cross-link; fully independent of OST work).
- **Tests:**
  - `tools/lint-skill.sh .claude/skills/interview-snapshot/SKILL.md` exits 0.
  - Body cites `context/frameworks/interview-snapshot.md` by path in §"References".
  - Body has exactly these four operational sub-sections, in order, as H2 headings (or as the body's named-section bullets if the implementer chooses to roll them under a single `## How to extract a snapshot` parent): **Speaker detection**, **Time-aligned quote extraction**, **Paraphrase enforcement**, **No-recording fallback**.
  - Body does NOT contain a definitional list of all eight snapshot field names (`Goal`, `Workflow`, `Pain Points`, `Workarounds`, `Tools`, `Direct Quote`, `Date`, `Interviewer`) as a canonical-list enumeration — only as a `@see` pointer or inline reference to the framework. Mechanical grep: a `^- \*\*Goal\*\*` or `^### Goal` heading that introduces the field's definition is disallowed; the body may name fields when describing operational rules (e.g., "the Direct Quote field requires a timestamp"), but the field-list itself is the framework's job.
- **Approach:**
  - Use `.claude/skills/ears-lint/SKILL.md` as the shape exemplar (rule-library skill: frontmatter + intro line + `## When to use` + `## Invocation contract` + named operational sections + `## When this skill is wrong`).
  - Frontmatter `name: interview-snapshot`, `description:` ≤ 1024 chars, `license: MIT`.
  - Body §s: When to use this skill; Invocation contract (Inputs: raw transcript text + optional `interviewer` / `date` / `recording_present` overrides; Output: proposal block); Speaker detection (heuristic rules: timestamped lines, dialog patterns, single-speaker monologue case); Time-aligned quote extraction (timestamp formats `MM:SS`, `[HH:MM:SS]`); Paraphrase enforcement (cite framework's spreadsheet → deck canonical example); No-recording fallback (the `[no recording]` attribution pattern from the framework); Ambiguity flagging (cite framework's `[ambiguous: ...]` pattern); What this skill never does (no schema redefinition, no persistence, no cross-snapshot synthesis); References.
- **Done when:** file exists; lint exits 0; body cites the framework as the canonical source for the eight fields and the paraphrase rule; the four named operational sub-sections are present and findable by grep.

### Task T4: ship `.claude/skills/opportunity-clustering/SKILL.md`

- **Depends on:** none (independent of T1, T2, T3).
- **Tests:**
  - `tools/lint-skill.sh` exits 0.
  - Body cites `context/frameworks/opportunity-solution-tree.md` in §"References".
  - Body documents these three thematic-grouping rules by name: **shared customer behavior**, **shared workflow step**, **shared workaround pattern**.
  - Body explicitly states the no-auto-promote rule (clusters propose; humans decide).
- **Approach:**
  - Use `.claude/skills/ears-lint/SKILL.md` as the shape exemplar (same as T3).
  - Body §s: When to use this skill; Invocation contract (Inputs: raw opportunity candidate list with one-line statement + optional `evidence_basis:` per candidate; Output: proposal block listing clusters with name + member candidate ids + one-line rationale); Three grouping rules (one named subsection per rule); Common failure modes (over-clustering / under-clustering / "everything in one bucket"); No-auto-promote rule; What this skill never does; References.
- **Done when:** file exists; lint exits 0; body explicitly cites the OST framework's source-opportunities discipline and names the three grouping rules.

### Task T5: ship `.claude/agents/discovery-coach.md`

- **Depends on:** none (independent of T1, T2, T3, T4).
- **Tests:**
  - `tools/lint-agent.sh` exits 0.
  - Frontmatter declares `model: sonnet`, `tools: [Read]` (judgment-only; no Write).
  - Body documents the two stuck-condition triggers by name: **no Solutions under chosen Opportunity** and **Solutions present but zero Assumption Tests**.
  - Body documents a 3–5-question prompt pattern with one named example sequence per trigger.
  - Body has an explicit `Hard rules` (or equivalent) section that names: never persist; never auto-pick a Solution; never override the human's `chosen_opportunity:`; **escalate to the human if the coaching sequence reaches five turns without the team producing candidate Solutions or Assumption Tests** (turn-cap addresses adversarial-review V3).
- **Approach:**
  - Copy `.claude/agents/traceability-walker.md` shape as the precedent.
  - Frontmatter `name: discovery-coach`, `description:` ≤ 1024 chars naming when to invoke (the two stuck conditions), `tools: [Read]`, `model: sonnet`, `license: MIT`.
  - Body §s: When the orchestrator invokes you; Your inputs (the OST path or pasted tree + the named-stuck-condition trigger); Your output (3–5 open questions + candidate Solutions or Assumption Tests; never persists); Stuck-condition triggers (named with examples); Prompt patterns per trigger (one example sequence per trigger); Hard rules (including the 5-turn cap); Failure modes; When this agent is wrong.
- **Done when:** file exists; lint exits 0; body cites `context/frameworks/continuous-discovery.md` for the divergent-then-convergent discipline; the 5-turn escalation rule is present.

### Task T6: update `.claude/skills/ost-validator/SKILL.md` if the script's CLI drifts

- **Depends on:** T2 (CLI must be locked).
- **Tests:**
  - Line 26's invocation snippet matches `python -m scripts.validate_ost --help`'s leading example exactly.
  - `tools/lint-skill.sh .claude/skills/ost-validator/SKILL.md` exits 0 (it should already; this task only catches drift).
- **Approach:** read the script's `--help`; diff against the skill line; if equal, no-op task (note in plan changelog); if different, edit the skill line and commit with the script in the same commit.
- **Done when:** lint clean; CLI snippet matches.

## Rollout

- **`tools/pre-pr.sh`** picks up the new fixtures and tests automatically — no wiring needed.
- **`docs/INVENTORY.md`** — add one row per component under the Phase-2 "Discovery" sub-section. Format per existing rows.
- **`ROADMAP.md`** — flip P2.2, P2.5, P2.8, P2.13, and D4 from `[ ]` to `[x]` with shipped date 2026-05-28 and slug reference.
- **`.claude/skills/README.md`** — add table rows for the two new skills (model the existing `ontology-classifier` and `ears-lint` rows).
- **`.claude/agents/README.md`** — add a table row for `discovery-coach`.
- **`AGENTS.md` and `.claude/CLAUDE.md`** — not edited (no policy change).
- **No CI changes** — the new tests are auto-discovered by the `python -m unittest scripts.tests` invocation in `tools/pre-pr.sh`.

## Risks

- **Schema rigidity vs forward extensibility.** Locking the 9 action verbs in JSON Schema makes any future verb addition a script-side change. Mitigation: the schema is in a kit-internal `references/` folder, not a published artifact; a future verb addition flows through an RFC + schema bump. Risk lives downstream of this batch.
- **Implementer-subagent divergence on the three skill/agent files.** Three parallel agents may produce inconsistent voice or structure across the three files. Mitigation: each agent's brief names the same exemplar (`ears-lint` for the two skills; `traceability-walker` for the agent) and lists the required H2 sections explicitly per T3 / T4 / T5; the orchestrator's review checks for shape consistency before VERIFY.
- **Cascade-permission-denial bug on parallel dispatch** (per `~/.claude/CLAUDE.md`). If T3+T4+T5 parallel dispatch comes back with cascade denials, fall back to sequential dispatch — does not count against the work-loop iteration cap.
- **JSON-vs-markdown OST input ambiguity** (named in spec §"Open questions"). The validator works on JSON only. Downstream commands (`/generate-ost`, `/update-ost`) must emit JSON projections. Mitigation: the script's `--help` says so explicitly, so a downstream author cannot miss the contract.
- **TDD discipline slip on T2.** With 12 tests and 6 rule functions, the temptation is to implement the script first and write tests after. Mitigation: write red tests against a stub before any rule logic; commit red-green-refactor separately when non-trivial.

## Changelog

- 2026-05-28 (PLAN-iter-2): Adversarial review surfaced 2 block + 9 needs-fix + 3 defer findings. Spec updated: cascade semantics now defined per-action (merge/split/delete); IS-NNN convention specified; human-format pass output destination defined; 8 new tests added (20 total); schema-vs-code-side validation split named explicitly. Plan updated: T3/T4/T5 dependencies corrected (no T1 dep); exemplar switched from `ontology-classifier` to `ears-lint`; T2 fixture list expanded to match new tests; T5 5-turn cap added. Three defer findings logged in `notes/deferred-findings.md` (D-H3 discovery-coach visibility, D-V3 SKILL.md vague language, D-E6 merge-with-missing-id behavior).
