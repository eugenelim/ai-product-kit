# Plan: phase-2-discovery-pipeline

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** approved (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for shipping P2.1, P2.3, P2.4, P2.6, P2.7, P2.9, P2.10 in a single coupled work-loop. The seven components are each independent markdown files; authoring is parallel-friendly. Runtime coupling (the pipeline chain) is captured in the spec.

## Approach

**Each component is a markdown file under `.claude/commands/` or `.claude/agents/`.** No code dependencies between authoring tasks. The work-loop:

1. **Spec + plan + adversarial review** — done before EXECUTE.
2. **Per-component authoring** — seven parallel-safe tasks. Each consumes `.claude/commands/_meta/command-skeleton.md` (commands) or `.claude/agents/traceability-walker.md` (agents) as the shape exemplar. Each fills the H2/H3 sections with command-specific Procedure steps. Each emits a NEXT chain line per the F4 convention.
3. **Lint each** with `tools/lint-command.sh` or `tools/lint-agent.sh`.
4. **Cross-cutting verify** — `tools/pre-pr.sh`.
5. **Review** — adversarial-reviewer for drift / scope creep; quality-engineer is NOT in scope (no scripts in this batch).
6. **Capture** — ROADMAP / INVENTORY / agent README updates.

**Subagent dispatch posture.** Per Batch A's experience, parallel-dispatched subagents may hit sandboxing on `Write` to new paths. Mitigation: pre-create target directories before dispatching. If sandboxing still blocks: author the files directly. The marginal cost of authoring directly vs. dispatching is small for markdown files.

## Constraints

- **No new scripts.** Authoring-only batch.
- **No edits to existing kit components** beyond what's required to make the new commands' references resolve. Specifically: no edits to `validate_ost.py`, the existing skills, `templates/ost.md`, or any `context/frameworks/*.md`.
- **F4 convention compliance.** Every new command file must match the `.claude/commands/_meta/command-skeleton.md` shape. The five commands consume the convention; they do not modify it.
- **Body cap.** Target ≤ 300 lines per command file; hard cap none (the existing `/draft-vision` and `/draft-initiative` are ~250-350 lines and pass lint). Agents target ≤ 150 lines.
- **Date discipline.** All `Shipped:` timestamps use 2026-05-28 (today).
- **Branch hygiene.** Work continues on `eugenelim/phase-2-batch-b`.

## Construction tests

Cross-cutting checks (not specific to one task):

- `tools/pre-pr.sh` exits 0 across the whole repo at the end of EXECUTE.
- For each command body: a grep confirms (a) the NEXT chain line is present, (b) `lint-frontmatter.py` is invoked in Step 5 (the F4 convention requires this), (c) the F4 Step pattern is followed (numbered Steps 1–6 minimum), (d) the body uses `<repo-root>` or equivalent path-resolution language when invoking `lint-frontmatter.py` (and, for `/generate-ost` / `/update-ost`, when invoking `validate_ost.py`) — never a bare `python3 tools/...` or `python3 scripts/...` that assumes the working directory is the repo root.
- For `/generate-ost` and `/update-ost` specifically: a grep confirms `validate_ost.py` appears in the body.
- For every produced artifact (snapshot, opportunity batch, clusters, OST): the `object_type:` value resolves through the linter's `<type> | Adapted` escape — confirmed by running `python3 <repo-root>/tools/lint-frontmatter.py` against a sample artifact each command would write (deferred to post-EXECUTE manual gesture, since this batch authors only the commands themselves, not sample artifacts).

## Tasks

Each of T1–T7 authors one component. T1–T7 are fully parallelizable; the spec's runtime coupling does not impose authoring order.

### Task T1: ship `.claude/commands/interview-snapshot.md`

- **Depends on:** none.
- **Tests:**
  - `tools/lint-command.sh` exits 0.
  - Body cites `interview-snapshot` skill (mechanical grep).
  - Body emits `NEXT: /extract-opportunities` (mechanical grep).
  - Body has numbered Procedure steps 1–6 minimum.
- **Approach:**
  - Copy `.claude/commands/_meta/command-skeleton.md` shape.
  - Frontmatter `description` ≤ 1024 chars summarizing the spec's §"P2.1" inputs/outputs.
  - `argument-hint: <slug> [--from <transcript-path>] [--interviewer <name>] [--date <YYYY-MM-DD>] [--no-recording] [--force]`.
  - Procedure: (1) ensure transcript source available, (2) instantiate snapshot file at `discovery/snapshots/<slug>.md` (pre-fill `id: IS-<NNN>`, `slug`, `interviewer`, `date`), (3) load the `interview-snapshot` skill, walk the 8 fields one at a time (Goal / Workflow / Pain Points / Workarounds / Tools / Direct Quote / Date / Interviewer), (4) surface `human_owned_decisions:` ("Confirm faithfulness to the customer's words"), (5) lint with `tools/lint-frontmatter.py`, (6) emit `NEXT: /extract-opportunities <today-or-batch-slug>`.
  - `## What this command will not do`: never persist without lint-clean; never fabricate fields when the transcript doesn't support them; never invent timestamps when `--no-recording` is set.
- **Done when:** file exists; lint exits 0; grep checks pass.

### Task T2: ship `.claude/agents/interview-coder.md`

- **Depends on:** none.
- **Tests:**
  - `tools/lint-agent.sh` exits 0.
  - Frontmatter declares `model: haiku`, `tools: [Read, Write]`.
  - Body documents the one-transcript-per-dispatch contract.
  - Body cites the `interview-snapshot` skill as the rule library it consumes.
- **Approach:**
  - Copy `.claude/agents/traceability-walker.md` shape as exemplar.
  - Frontmatter `name: interview-coder`, `description` ≤ 1024 chars naming the fan-out role (one transcript at a time; consumes the P2.2 skill; never NEXT-chains).
  - Body §s: When the orchestrator invokes you; Your inputs (one transcript + metadata); Your output (one snapshot file + structured stdout summary); How to work (load the skill, run the eight-field walk, write the file, lint, return summary); Hard rules; Failure modes; When this agent is wrong.
- **Done when:** file exists; lint exits 0; grep checks pass.

### Task T3: ship `.claude/commands/extract-opportunities.md`

- **Depends on:** none.
- **Tests:**
  - `tools/lint-command.sh` exits 0.
  - Body emits `NEXT: /cluster-opportunities`.
  - Body explicitly enforces "every candidate must have non-empty `evidence_basis:`" (mechanical grep on the phrase).
  - Body has Procedure steps 1–6.
- **Approach:**
  - Frontmatter description names: snapshots → candidates; non-empty evidence_basis; lints; NEXT.
  - `argument-hint: <slug> [--snapshots <comma-list>] [--force]`.
  - Procedure: (1) resolve set of snapshots to walk (default: snapshots newer than the most recent batch's `created`), (2) instantiate `discovery/opportunities/<slug>.md`, (3) walk each snapshot, extracting candidate Opportunities (one H3 sub-section per candidate; each carries `lens:`, `confidence:`, non-empty `evidence_basis:`, optional `open_questions:`), (4) surface `human_owned_decisions:` ("Accept candidates / reject conjecture"), (5) lint, (6) emit `NEXT: /cluster-opportunities <slug>`.
  - `## What this command will not do`: never produce a candidate with empty evidence_basis; never silently include ambiguous bullets (surface the ambiguity first); never restate Solutions as Opportunities.
- **Done when:** file exists; lint exits 0; grep checks pass.

### Task T4: ship `.claude/commands/cluster-opportunities.md`

- **Depends on:** none.
- **Tests:**
  - `tools/lint-command.sh` exits 0.
  - Body cites `opportunity-clustering` skill (mechanical grep).
  - Body emits `NEXT: /generate-ost`.
  - Body has Procedure steps 1–6.
- **Approach:**
  - Frontmatter description names: candidates → clusters via the P2.5 skill; per-cluster human accept/revise/reject; unclustered bucket preserved.
  - `argument-hint: <slug> [--from <batch-slug>] [--force]`.
  - Procedure: (1) resolve parent candidate batch, (2) instantiate clusters file, (3) dispatch the P2.5 skill against the candidate list, walk each proposed cluster one at a time (human accept/revise/reject; rejected members move to `unclustered:`), (4) surface human_owned_decisions, (5) lint, (6) emit `NEXT: /generate-ost <slug-or-intent>`.
  - `## What this command will not do`: never auto-promote a cluster (no-auto-promote rule from the skill); never force-cluster candidates with no shared anchor (leave them in unclustered); never edit candidate text.
- **Done when:** file exists; lint exits 0; grep checks pass.

### Task T5: ship `.claude/commands/generate-ost.md`

- **Depends on:** none.
- **Tests:**
  - `tools/lint-command.sh` exits 0.
  - Body references `scripts/validate_ost.py` (mechanical grep).
  - Body emits `NEXT: /update-ost`.
  - Body documents the markdown + JSON projection dual-write.
  - Body has Procedure steps 1–7 (the validator step adds one beyond the F4 minimum).
- **Approach:**
  - Frontmatter description names: clusters + intent → first-pass OST; markdown + JSON dual-write; validator gate.
  - `argument-hint: <slug> --from <intent-slug> [--from-clusters <clusters-slug>] [--force]`.
  - Procedure: (1) resolve parent intent, (2) instantiate `discovery/trees/<slug>.md` from `templates/ost.md` (pre-fill `parent_intent`, `outcome.id`, mechanical fields), (3) walk OST H2 sections (outcome, opportunity space — promote accepted clusters here; chosen one — usually deferred to /update-ost; source opportunities — already in evidence_basis; excluded), (4) build JSON projection node-by-node, (5) write the canonical empty seed `{"nodes": []}` to a `$(mktemp)`-created temp file, then shell out to `<repo-root>/scripts/validate_ost.py --input <mktemp-path> --output <slug>.json --change-set <generated>`; clean up the temp file after the validator returns. The repair loop is unconditional (up to 5 rounds on non-clean); `--force` only governs file-overwrite behavior, not the repair loop. (6) write markdown + JSON + change-set trail; lint markdown, (7) emit `NEXT: /update-ost <slug>`.
  - `## What this command will not do`: never persist OST on validator non-clean; never fabricate Opportunities not in the parent clusters file; never name `chosen_opportunity:` automatically (human-owned).
- **Done when:** file exists; lint exits 0; grep checks pass.

### Task T6: ship `.claude/commands/update-ost.md`

- **Depends on:** none.
- **Tests:**
  - `tools/lint-command.sh` exits 0.
  - Body references `scripts/validate_ost.py` (mechanical grep).
  - Body emits `NEXT:` to a downstream phase command (one of `/audit-discovery-coherence`, `/assumption-test`, or `/discovery-update`).
  - Body documents the optional `opportunity-merger` fan-out.
- **Approach:**
  - Frontmatter description names: mutate existing OST; convert proposed changes to the 9-verb vocabulary; validator gate with repair loop; optional opportunity-merger fan-out.
  - `argument-hint: <slug> [--from-snapshots ...] [--from-clusters ...] [--update-evidence-only] [--add-node <spec>] [--force]`.
  - Procedure: (1) load existing markdown + JSON (warn on divergence), (2) walk proposed changes one at a time, converting each to actions from the 9-verb vocabulary, (3) if changes touch ≥ 3 nodes, dispatch `opportunity-merger` agent per affected node (collect verdicts), (4) build new JSON + change-set, (5) shell out to validator (repair loop up to 5 rounds), (6) on pass: re-render markdown from JSON + write change-set trail to `discovery/trees/<slug>-change-set-<timestamp>.json`; bump last_updated; lint, (7) emit NEXT based on whether `chosen_opportunity:` is set.
  - `## What this command will not do`: never persist on validator non-clean; never override human's `chosen_opportunity:`; never add `add-outcome` to a tree that has an outcome (use reframe); never silently move IS-<NNN> sources between Opportunities (Rule 6 catches this).
- **Done when:** file exists; lint exits 0; grep checks pass.

### Task T7: ship `.claude/agents/opportunity-merger.md`

- **Depends on:** none.
- **Tests:**
  - `tools/lint-agent.sh` exits 0.
  - Frontmatter declares `model: haiku`, `tools: [Read]`.
  - Body documents the per-node verdict contract (`accept | revise | reject` with optional alternative).
- **Approach:**
  - Copy `traceability-walker.md` shape.
  - Frontmatter `name: opportunity-merger`, `description` ≤ 1024 chars naming the fan-out role (one node at a time; consumes the current OST JSON; never persists).
  - Body §s: When the orchestrator (`/update-ost`) invokes you; Your inputs (one node id + proposed action + current OST JSON); Your output (verdict block); How to work (read the current tree, evaluate the proposed action against the OST framework's rules, return verdict); Hard rules; Failure modes; When this agent is wrong.
- **Done when:** file exists; lint exits 0; grep checks pass.

## Rollout

- `tools/pre-pr.sh` picks up the new commands and agents automatically — no wiring.
- `docs/INVENTORY.md` Phase-2 table: flip the 7 rows from `planned (P2.x)` to `shipped (P2.x, 2026-05-28)`.
- `ROADMAP.md`: mark P2.1, P2.3, P2.4, P2.6, P2.7, P2.9, P2.10 `[x]` with shipped dates.
- `.claude/agents/README.md`: move `interview-coder` and `opportunity-merger` from "Planned — fan-out workers" to "Shipped".
- `AGENTS.md` and `.claude/CLAUDE.md`: not edited (no policy change).
- The discovery sub-directories (`discovery/snapshots/`, `discovery/opportunities/`, `discovery/trees/`) are already present (Batch A or earlier work created them); commands write into them.

## Risks

- **F4 convention drift.** Seven new commands authored in one batch — risk of subtle drift from the convention (forgotten Step 6 NEXT line; missed lint step). Mitigation: each task's Tests bullet enumerates the convention checks as mechanical greps; the verify gate catches drift before review.
- **`/generate-ost` and `/update-ost` complexity.** These two are the most complex commands in the kit so far (markdown + JSON dual-write; validator shell-out; optional fan-out). Risk: the procedure body grows past the 300-line target and becomes hard to follow. Mitigation: keep the procedure step-by-step in the command body; defer detailed projection logic to inline code blocks within the steps; surface as a follow-up if the bodies exceed 400 lines.
- **Sandboxing on parallel subagent dispatch** (per Batch A). Mitigation: pre-create `.claude/commands/` and `.claude/agents/` parent dirs (they already exist); if dispatch fails, author directly.
- **Manual gesture verification deferred to post-EXECUTE.** A dogfood-style end-to-end run against a real transcript is the right way to validate the UX, and that's a follow-up exercise beyond this loop's mechanical gates. Mitigation: surface this in the spec's verification-mode section as an explicit deferral.

## Changelog

- 2026-05-28 (PLAN-iter-2): Adversarial review surfaced 2 block + 8 needs-fix + 1 defer findings. Spec updated: (a) all three new `object_type` values changed to use the `<type> | Adapted` linter escape hatch (`Insight | Adapted` for snapshots; `Opportunity | Adapted` for candidate batches and clusters); (b) `<empty-input.json>` for `/generate-ost` defined as canonical `{"nodes": []}` via `mktemp`; (c) repo-root resolution added to §Always do and to per-task tests; (d) `opportunity-merger` fan-out trigger refined to "any merge or split, OR ≥ 3 nodes total" with rationale moved to Open questions; (e) zero-candidates and zero-clusters first-run cases handled with exit-2 + NEXT remediation hints; (f) `--update-evidence-only` permitted-verb set defined as `{add-source-opportunity}` only; (g) `--force` decoupled from the validator repair loop (loop is unconditional; `--force` only governs file-overwrite); (h) JSON→markdown re-render contract surfaced as Open Question SC1 with a human-review gate; (i) `interview-coder` lint-failure rollback semantics added; (j) change-set trail filename gets random 4-hex suffix to prevent same-second collision.
