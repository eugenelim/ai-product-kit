# Spec: phase-2-discovery-pipeline

- **Status:** Approved
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** Coupled batch of seven kit components — five slash commands + two specialist agents. Mirrors the `phase-4-template-fill-commands` (seven commands under one work-loop) and `phase-2-discovery-primitives` (Batch A — four primitives under one work-loop) precedents.
- **Serves kit phase:** Discovery (Phase 2)
- **Constrained by:** ROADMAP **P2.1** `cmd-interview-snapshot`, **P2.3** `agent-interview-coder`, **P2.4** `cmd-extract-opportunities`, **P2.6** `cmd-cluster-opportunities`, **P2.7** `cmd-generate-ost`, **P2.9** `cmd-update-ost`, **P2.10** `agent-opportunity-merger`; Batch A outputs (`.claude/skills/interview-snapshot/SKILL.md` — P2.2; `.claude/skills/opportunity-clustering/SKILL.md` — P2.5; `scripts/validate_ost.py` — P2.8 with its JSON schema and action vocabulary); `context/frameworks/interview-snapshot.md`, `context/frameworks/opportunity-solution-tree.md`, `context/frameworks/continuous-discovery.md`; `docs/HANDOVERS.md` §"Handover 2" (Discovery → Validation handover contract); `docs/specs/phase-4-command-convention/` and `.claude/commands/_meta/command-skeleton.md` (the convention every new slash command consumes); `templates/ost.md` (F3.2) — the markdown OST template `/generate-ost` instantiates; `docs/CONVENTIONS.md` §"Specs and Plans" (kit-meta exemption); `.claude/skills/work-loop/SKILL.md`.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships the Phase-2 Discovery pipeline — the chain of commands and agents that turns raw customer interviews into a typed Opportunity Solution Tree (OST) suitable for the Discovery → Validation handover. The seven components compose into a real workflow: `/interview-snapshot` (per-transcript snapshots, dispatchable in parallel via `interview-coder` agent) → `/extract-opportunities` (snapshots → candidate Opportunities) → `/cluster-opportunities` (candidates → themed clusters via the P2.5 skill) → `/generate-ost` (clusters + parent intent → first-pass tree) → `/update-ost` (mutate tree per new evidence; emit change set; `opportunity-merger` agent fans out per-node merge work). `/generate-ost` and `/update-ost` both emit a JSON projection alongside the markdown OST and shell out to `scripts/validate_ost.py`; both refuse to persist on validator non-clean.

## Objective

Author seven components that together close the Phase-2 pipeline gap between raw interview material and the Discovery → Validation handover artifact (Handover 2). Each command follows the F4 command-skeleton convention; each agent follows the kit's agent shape. The seven deliverables:

| # | ROADMAP | Slug | Component | Output path |
|---|---|---|---|---|
| 1 | P2.1 | `cmd-interview-snapshot` | Slash command | `.claude/commands/interview-snapshot.md` |
| 2 | P2.3 | `agent-interview-coder` | Agent | `.claude/agents/interview-coder.md` |
| 3 | P2.4 | `cmd-extract-opportunities` | Slash command | `.claude/commands/extract-opportunities.md` |
| 4 | P2.6 | `cmd-cluster-opportunities` | Slash command | `.claude/commands/cluster-opportunities.md` |
| 5 | P2.7 | `cmd-generate-ost` | Slash command | `.claude/commands/generate-ost.md` |
| 6 | P2.9 | `cmd-update-ost` | Slash command | `.claude/commands/update-ost.md` |
| 7 | P2.10 | `agent-opportunity-merger` | Agent | `.claude/agents/opportunity-merger.md` |

These are authoring-time-independent (each is a markdown file with no cross-component code dependency) but runtime-dependent (the pipeline chain). The spec captures both: each component's contract is independent; the NEXT chain links them at run time.

## Why now

Batch A shipped the four primitives (`interview-snapshot` skill, `opportunity-clustering` skill, `ost-validator` script, `discovery-coach` agent). Those primitives are reusable rule libraries; they don't, by themselves, drive a Discovery workflow. Without the pipeline commands, a PM has the rules but no UX — they would have to assemble the workflow manually each time. The pipeline closes that gap and unblocks:

- The Discovery → Validation handover (`docs/HANDOVERS.md` §"Handover 2") — every step in the chain feeds the OST artifact this handover requires.
- The Phase-2 audit + comms commands (Batch C — `/audit-discovery-coherence`, `/opportunity-narrative`, `/discovery-update`) — they consume the artifacts this pipeline produces.
- Real-world dogfooding: a PM running through the pipeline end-to-end is the only way to surface the convention-level gaps that the kit's framework references can't anticipate.

## Inputs and outputs

### P2.1 — `/interview-snapshot <slug>`

**Inputs.**
- Positional `<slug>` — kebab-case identifier for the new snapshot. Convention: `<interviewee-firstname>-<YYYY-MM-DD>`.
- `--from <transcript-path>` — required for non-interactive mode; otherwise the command asks for the transcript file path or pasted content.
- `--interviewer <name>` — optional; defaults to prompting the human.
- `--date <YYYY-MM-DD>` — optional; defaults to today.
- `--no-recording` — optional flag; switches the quote-attribution to the framework's `[no recording]` path.
- `--force` — optional; permits overwriting existing snapshot.

**Outputs.** Writes `discovery/snapshots/<slug>.md` with frontmatter (`object_type: Insight | Adapted` — the `| Adapted` suffix is the kit's documented escape hatch in `tools/lint-frontmatter.py` for kit-composite types not yet in the ontology; the body's H1 names it as an Interview Snapshot per `context/frameworks/interview-snapshot.md`. `id: IS-<NNN>`, `slug`, `interviewer`, `date`, `created`, `last_updated`, the universal `human_owned_decisions:` / `ai_assistance_used:` / etc.) and an H2-sectioned body holding the eight snapshot fields per the framework. Pre-fills mechanical fields; walks each of the eight fields one at a time via the P2.2 skill. Lints with `<repo-root>/tools/lint-frontmatter.py`. Emits `NEXT: /extract-opportunities <slug-or-batch>` on success.

### P2.3 — `interview-coder` agent

**Inputs.** Manually invoked by an orchestrator (typically a future batched-processing command not in scope here, or the user from a PM's working session). Each dispatch handles one transcript at a time. Inputs: one transcript path + optional metadata (interviewer, date, recording-present boolean). Tools: `[Read, Write]` — writes the snapshot file via the same convention as `/interview-snapshot` Step 5 (lint then persist), but does not chain forward (no NEXT line emitted by an agent). Model: `haiku` (fan-out-cheap; per-transcript transformation is bounded work).

**Outputs.** One `discovery/snapshots/<slug>.md` per dispatch, lint-clean. Structured stdout summary: `{slug, id, snapshot_path, ambiguity_flags_count}`. **On lint failure:** the agent deletes the partially-written file before exiting (rollback semantics) and writes the lint output to stderr; does not retry; surfaces failure to the orchestrator. A partial snapshot file on disk is worse than no snapshot file — downstream commands (`/extract-opportunities`) walk `discovery/snapshots/` blindly and would consume a lint-failed file.

### P2.4 — `/extract-opportunities <slug> [--snapshots ...]`

**Inputs.**
- Positional `<slug>` — kebab-case identifier for the extraction batch. Default convention: today's date (`YYYY-MM-DD`).
- `--snapshots <comma-list>` — optional list of specific snapshot slugs to walk; defaults to walking every snapshot in `discovery/snapshots/` whose `last_updated` is newer than the most recent extraction batch's `created` (or all snapshots if no prior batch exists).
- `--force` — optional.

**Outputs.** Writes `discovery/opportunities/<slug>.md` — a flat list of candidate Opportunities surfaced from the walked snapshots. Each candidate is one H3 sub-section under H2 "Candidate Opportunities" with: candidate-id (`OPP-CAND-<NNN>`), one-line statement in customer's voice, `evidence_basis:` list naming the source snapshots' `IS-<NNN>` ids and the relevant quote-or-pain-point bullet, `lens:` (one of `pain | desire | aspiration`), `confidence:` (high / medium / low based on snapshot evidence density), `open_questions:` if any ambiguity bullets in the source snapshots haven't been resolved. Pre-walk: surfaces snapshots that had `[ambiguous: ...]` flags and asks the human whether to skip the ambiguous bullets or treat them as inputs anyway. Walks one snapshot at a time. Frontmatter: `object_type: Opportunity | Adapted` (per the same kit-composite escape hatch — the H1 names it as an "Opportunity Candidate Batch"), `id: OPC-<NNN>`, parent-snapshot references in `evidence_basis:`. Lints. Emits `NEXT: /cluster-opportunities <slug>`.

### P2.6 — `/cluster-opportunities <slug> [--from <batch-slug>]`

**Inputs.**
- Positional `<slug>` — clustering proposal identifier. Default: today's date.
- `--from <batch-slug>` — optional explicit parent batch (a file under `discovery/opportunities/`); otherwise resolves the most recent batch via the F4 candidate-listing rule.
- `--force` — optional.

**Outputs.** Writes `discovery/opportunities/clusters/<slug>.md`. Dispatches the P2.5 `opportunity-clustering` skill against the parent batch's candidate list; receives the proposed clusters (each with `name`, `rule`, `members`, `rationale`) plus the `unclustered:` bucket. Walks one cluster at a time; for each, asks the human to accept/revise/reject. Rejected clusters' members move to `unclustered:`. Frontmatter: `object_type: Opportunity | Adapted` (H1 names it "Opportunity Clusters"), `id: OPCL-<NNN>`, `parent_batch: <batch-slug>`. Lints. Emits `NEXT: /generate-ost <slug-or-intent>`. **Zero-candidate-batch case:** if the resolved parent batch is empty (or no batch exists), exit code 2 with `NEXT: /extract-opportunities` as the remediation hint, matching the F4 skeleton's Step 1 empty-list contract.

### P2.7 — `/generate-ost <slug>`

**Inputs.**
- Positional `<slug>` — OST identifier.
- `--from <intent-slug>` — required parent strategic intent (resolution rule per the F4 convention).
- `--from-clusters <clusters-slug>` — optional explicit cluster batch; otherwise resolves the most recent.
- `--force` — optional.

**Outputs.** Two files:
- `discovery/trees/<slug>.md` — markdown OST, instantiated from `templates/ost.md`. Frontmatter pre-fills `parent_intent`, `outcome.id`, the universal metadata schema. The body is walked H2 by H2 per the template; the H2 "Opportunity space" is filled by promoting clusters from the parent clusters file (each accepted cluster becomes one OST Opportunity node, each member candidate becomes its OST Opportunity's `evidence_basis:` source).
- `discovery/trees/<slug>.json` — the JSON projection per `scripts/validate_ost.py`'s contract. The projection is the source of truth for the validator; the markdown is the human-readable rendering. Both files share the same content but in different shapes. The command builds the JSON tree node-by-node from the walked H2 sections. Then shells out to `<repo-root>/scripts/validate_ost.py --input <empty-input> --output <slug>.json --change-set <generated-change-set>`. **The empty-input JSON is canonical:** `{"nodes": []}` — the validator's schema (as of Batch A iter-2) makes `outcome` optional precisely so first-generation trees can start from this seed. The command writes the seed to an `mktemp`-managed temp file before invocation (cleaned up after). The change-set is the action sequence that produced the tree from the empty seed: `[add-outcome, add-opportunity*, add-source-opportunity*, ...]` in the order the human filled the H2 sections. If the validator exits non-zero, the command refuses to persist (rolls back any partial writes) and surfaces the validator's remediation output. **The repair loop is unconditional** — the command always offers up to 5 repair rounds on validator non-clean (matching the existing `ost-validator` SKILL.md's "5 turns" cap). The `--force` flag governs only whether existing on-disk files may be overwritten; it has no effect on the repair loop. On validator exit 0: lints the markdown, emits `NEXT: /update-ost <slug>` (or, if the team is ready to choose a `chosen_opportunity:`, suggest `NEXT: /audit-discovery-coherence` (planned — P2.11)).

**Zero-clusters-files case:** if `--from-clusters` is not given and no clusters file exists, exit code 2 with `NEXT: /cluster-opportunities` as the remediation hint. The continuous-discovery framework permits generating an OST from raw snapshots without a clustering pass, but the spec does not promise that path — to keep `/generate-ost` predictable, treat clusters as a soft prerequisite and surface the missing-prereq message. A future flag (`--from-clusters none --from-snapshots ...`) can open the raw-snapshots path; not in this batch.

### P2.9 — `/update-ost <slug>`

**Inputs.**
- Positional `<slug>` — existing OST identifier (file must exist at `discovery/trees/<slug>.md`).
- `--from-snapshots <comma-list>` — optional list of new snapshots whose evidence should be integrated.
- `--from-clusters <clusters-slug>` — optional new clusters batch.
- `--update-evidence-only` — flag; integrates new `IS-<NNN>` refs into existing Opportunities without restructuring the tree.
- `--add-node <node-spec>` — flag; for adding one Solution or Assumption Test interactively.
- `--force` — optional; permits the validator to be re-run after a human-acknowledged repair loop.

**Outputs.** Mutates `discovery/trees/<slug>.md` and `discovery/trees/<slug>.json`; emits a change-set JSON to `discovery/trees/<slug>-change-set-<YYYY-MM-DDTHH-MM-SS>-<4-hex>.json` capturing the actions applied (the random 4-hex suffix prevents same-second collision on rapid re-runs — the audit trail must never overwrite). Workflow:

1. Read the existing markdown OST + the JSON projection. If the two diverge (a human edited the markdown directly), surface the diff and ask the human to resolve before proceeding.
2. Walk the human through proposed changes one at a time; each proposed change is converted into one or more actions from the 9-verb vocabulary (`add-opportunity`, `add-solution`, `reframe`, `merge`, `split`, `delete`, `reparent`, `add-source-opportunity`). **When `--update-evidence-only` is set, the permitted action vocabulary is restricted to `{add-source-opportunity}` only**; any proposed change requiring a different verb triggers a warning and a prompt to re-run without the flag.
3. Optionally dispatch `opportunity-merger` agent (P2.10) for per-node verdict on **any `merge` or `split` action** (these verbs are structurally complex regardless of total-node count), and additionally when a single change set's total touched-node count is ≥ 3. See §"Open questions" for the threshold's rationale.
4. Build the new claimed-output JSON and the change-set JSON.
5. Shell out to `<repo-root>/scripts/validate_ost.py --input <current-projection> --output <new-projection> --change-set <change-set>`. **The repair loop is unconditional** — on non-clean validator output, present the validator's report and offer up to 5 repair rounds before giving up. The `--force` flag governs only whether existing files may be overwritten; it has no effect on the repair loop.
6. On validator pass: write the new markdown (re-render from the JSON — see §"Open questions" SC1 for the JSON→markdown render contract), the new JSON, and the change-set trail file; bump `last_updated`.
7. Lint. Run a brief human-review prompt asking the human to scan the re-rendered markdown for fidelity (until the re-render contract is mechanically tested). Emit `NEXT: /audit-discovery-coherence <slug>` (planned — P2.11) or `NEXT: /assumption-test` (planned — P3.1) when `chosen_opportunity:` is set.

### P2.10 — `opportunity-merger` agent

**Inputs.** Dispatched by `/update-ost` for any `merge` or `split` action (these verbs are structurally complex regardless of total-node count), AND additionally when a single change set's total touched-node count is ≥ 3 nodes. Each dispatch: one node id + the proposed action (`merge`, `split`, `reparent`, or `reframe`) + the current OST JSON projection. Tools: `[Read]` — judgment only; never writes. Model: `haiku` (fan-out-cheap).

**Outputs.** Structured stdout: `{node_id, verdict: accept|revise|reject, rationale, alternative_action_proposal?}`. Returns to `/update-ost` which collects the verdicts, then assembles the final change set. Never persists; never overrides the human's prior commitments.

## Boundaries

### Always do

- Follow the F4 command-skeleton convention (frontmatter `description` ≤ 1024 chars + `argument-hint`; H1 matching name; `## When to run`; `## Inputs`; `## Procedure` with numbered Steps; `## What this command will not do`).
- **Resolve the repo root** as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`, matching the F4 skeleton Step 5 contract. Every invocation of `tools/lint-frontmatter.py`, `scripts/validate_ost.py`, and any other repo-rooted script must use this resolved path — never assume the working directory is the repo root.
- Resolve parent artifacts by listing candidates and asking the human (never silently pick).
- Pre-fill mechanical frontmatter (`id`, `slug`, `created`, `last_updated`, the resolved parent_*); never ask the human for these.
- Walk H2 sections one question at a time. Never batch.
- Lint every written artifact with `<repo-root>/tools/lint-frontmatter.py` before declaring the command successful.
- For `/generate-ost` and `/update-ost`: shell out to `<repo-root>/scripts/validate_ost.py` before persisting; refuse to persist on validator non-clean.
- Cite the framework documents (`context/frameworks/interview-snapshot.md`, `opportunity-solution-tree.md`, `continuous-discovery.md`) when prompting the human — frame each placeholder question in the framework's vocabulary.

### Ask first

- Renaming the existing `discovery/` subdirectory layout (`snapshots/`, `opportunities/`, `outcomes/`, `trees/`). The dirs already exist (empty); commands write into them.
- Introducing a new ontology object_type beyond what the framework references already name (e.g., adding `Opportunity Candidate Batch` as a kit-meta composite — it does not currently exist in the ontology and may need an RFC).
- Changing `validate_ost.py`'s CLI contract — the script is shipped; if the commands need extra flags, surface as a sub-task of the existing P2.8 spec.

### Never do

- Never persist an OST that fails `scripts/validate_ost.py`. The validator is the gate; bypassing it produces silent structural drift the downstream consumers (Validation phase, audits) will catch much later.
- Never auto-promote a clustering proposal to OST nodes — the human accepts/revises each cluster per the no-auto-promote rule from the P2.5 skill.
- Never fabricate evidence — if a snapshot's `evidence_basis:` is missing, surface the gap; do not invent.
- Never let `/extract-opportunities` produce a candidate with empty `evidence_basis:` — the framework's "Source opportunities" rule is non-negotiable.
- Never let the `opportunity-merger` agent persist anything. Agents return verdicts; the command persists.
- Never skip the H2-by-H2 walk for `/interview-snapshot`. The P2.2 skill's paraphrase enforcement only works when the human reviews one bullet at a time.
- Never add an `add-outcome` action via `/update-ost` when the existing OST already has an outcome — use `reframe` instead (per `.claude/skills/ost-validator/references/action-vocabulary.md`).

## Verification mode

**Goal-based check** for all seven components:

- Per-component linter exits 0 (`lint-command.sh` for the five commands; `lint-agent.sh` for the two agents).
- `tools/pre-pr.sh` exits 0 across the repo.
- Cross-cutting: every command's body contains an explicit reference to its NEXT chain target (the file linter doesn't enforce this but a grep does).

**Manual gesture** (recorded under `notes/manual-verification.md`):

- Fresh session runs `/interview-snapshot test-interview` with a paste-mode transcript; produces `discovery/snapshots/test-interview.md` with the eight fields and a quote-with-timestamp Direct Quote.
- Fresh session runs `/extract-opportunities` against the snapshot; produces a candidates file with at least one candidate naming the snapshot's `IS-<NNN>` id in `evidence_basis`.
- Fresh session runs `/cluster-opportunities` against the candidates; produces a clusters file with at least one cluster naming the three grouping rules.
- Fresh session runs `/generate-ost test-tree --from <intent-slug> --from-clusters <clusters-slug>`; produces both the markdown OST and the JSON projection; the validator exits 0.

The manual gestures are recorded after EXECUTE — a real dogfooding pass is the right time to verify the pipeline's UX, and it's the team's responsibility per the spec's `human_owned_decisions:` rationale.

## Contract tests

### Per-command mechanical tests

For each of the five commands and two agents:

- File exists at the declared path.
- `tools/lint-command.sh` (commands) or `tools/lint-agent.sh` (agents) exits 0.
- Frontmatter `description` ≤ 1024 chars.
- Body contains H1 matching the command/agent name.

### Cross-cutting tests

- `tools/pre-pr.sh` exits 0.
- Each command's body emits a `NEXT:` chain line per the F4 convention; a grep confirms.
- `/generate-ost.md` and `/update-ost.md` bodies both contain a reference to `scripts/validate_ost.py` invocation.
- `interview-coder.md` and `opportunity-merger.md` bodies both contain `model: haiku` in frontmatter.
- The two slash commands that consume Batch A skills (`/interview-snapshot` and `/cluster-opportunities`) each name the respective skill (`interview-snapshot`, `opportunity-clustering`) in their procedure body.

### Test isolation

No script-level unit tests in this batch (the only Python script was shipped in Batch A as P2.8). The seven new components are doctrine documents (markdown). Mechanical-gate failure (linter non-zero) is the only test surface.

## Non-goals

- **Not building `/audit-discovery-coherence` (P2.11), `/opportunity-narrative` (P2.12), or `/discovery-update` (P2.14).** Those are Batch C.
- **Not adding new ontology types.** `Opportunity Candidate Batch` and `Opportunity Clusters` are kit-composite frontmatter labels for the artifacts these commands produce; they are NOT new Domain A-I ontology types. If the kit's ontology genuinely needs new types, that's an RFC, not this spec.
- **Not modifying `scripts/validate_ost.py` or its tests.** Shipped in Batch A; reused as-is.
- **Not modifying any `context/frameworks/*.md`.** Frameworks are canon; commands consume them.
- **Not building a markdown↔JSON projection library as a separate script.** The projection logic lives inside `/generate-ost` and `/update-ost`'s procedure bodies. Extracting it to a script is a future-batch concern (would only matter if the projection is reused outside these two commands).
- **Not implementing the F2.7 `hook-validate-ost` PostToolUse hook.** That's a separate ROADMAP item; until it ships, `/generate-ost` and `/update-ost`'s own shell-out to `validate_ost.py` is the only enforcement surface for the validator.

## Open questions

- **Markdown↔JSON round-trip determinism.** `/generate-ost` writes both formats from the same in-memory representation, so round-trip is internal. `/update-ost` reads the markdown back at start-of-session — if a human edited the markdown directly between sessions, the JSON projection is stale. **Workaround for this batch:** `/update-ost` re-reads BOTH files and surfaces a warning if they disagree; the human resolves the divergence interactively. **When to address properly:** when F2.7 (the hook) ships and forces sync at write time.
- **Cluster acceptance UX.** `/cluster-opportunities` walks one cluster at a time and asks accept/revise/reject. With 6 clusters and 30 candidates, this is a long interactive session. **Workaround:** offer `--batch-accept-confidence-high` flag that auto-accepts clusters whose member-candidate `confidence:` is uniformly `high` (still surfaces the cluster name + member ids for human spot-check, but doesn't require per-cluster Y/N). **When to address:** ship without the flag in this batch; add it in a follow-up if real usage shows the friction.
- **`/update-ost` repair-loop semantics.** When the validator returns non-clean, the existing `ost-validator` SKILL.md says "1-2 turns typically converge; 5 turns is the abort threshold." The command must offer the human a choice between "fix manually" and "show me what the validator wants and try again." **Workaround:** the command's Step 5 enumerates the choices and defers to the human; no machinery beyond that. **When to address:** real usage will calibrate the right UX; defer.
- **`opportunity-merger` fan-out threshold.** The spec fires the agent on any `merge` or `split` action AND on change sets touching ≥ 3 nodes total. The "≥ 3" threshold is a starting heuristic — small enough to skip judgment overhead on trivial 1-2 node edits, large enough to fan out when a session is restructuring meaningful subtree shape. **When to address:** real usage will calibrate; revisit when the kit has logged ~10 real `/update-ost` runs.
- **SC1 — JSON→markdown re-render fidelity for `/update-ost`.** Step 6 of `/update-ost` re-renders the markdown OST from the updated JSON projection. This is a *new* contract — there is no prior art in the kit (Batch A's `validate_ost.py` only does JSON→JSON apply). The render contract: the output markdown must satisfy `templates/ost.md`'s H2 structure (the four required H2 sections — outcome / opportunity space / chosen one / source opportunities, plus optionally excluded) and carry the OST frontmatter per Handover 2. The linter is the only mechanical gate. **Workaround:** `/update-ost` Step 7 runs a human-review prompt asking the user to scan the re-rendered markdown for fidelity before the NEXT hint is emitted. **When to address:** when a re-render unit test (potentially as part of P2.8's test suite, or a new fixture-comparison test) exists. Track as a sub-task of P2.9 or as a new follow-up spec.
- **Same-second change-set trail filename collision.** `/update-ost` writes change-set trails with `<ISO-8601-timestamp>-<4-hex-suffix>.json` to avoid the case where two rapid runs collide. The 4-hex suffix gives 65,536 collision-resistant slots per second — adequate for human-driven workflow; would not be adequate for automated bulk-import. **When to address:** when the kit grows automated OST mutation (e.g., a future bulk-import command); defer.

## Acceptance criteria

- [ ] `.claude/commands/interview-snapshot.md` exists, lint-clean, body cites the `interview-snapshot` skill, emits `NEXT: /extract-opportunities`.
- [ ] `.claude/commands/extract-opportunities.md` exists, lint-clean, body enforces "every candidate must have non-empty `evidence_basis`", emits `NEXT: /cluster-opportunities`.
- [ ] `.claude/commands/cluster-opportunities.md` exists, lint-clean, body dispatches the `opportunity-clustering` skill, emits `NEXT: /generate-ost`.
- [ ] `.claude/commands/generate-ost.md` exists, lint-clean, body shells out to `scripts/validate_ost.py`, refuses to persist on non-clean, emits `NEXT: /update-ost`.
- [ ] `.claude/commands/update-ost.md` exists, lint-clean, body shells out to the validator with a repair loop and the optional `opportunity-merger` fan-out, emits `NEXT:` to `/audit-discovery-coherence` (planned — P2.11) or `/assumption-test` (planned — P3.1).
- [ ] `.claude/agents/interview-coder.md` exists, lint-clean, declares `model: haiku`, `tools: [Read, Write]`, body documents the one-transcript-per-dispatch contract.
- [ ] `.claude/agents/opportunity-merger.md` exists, lint-clean, declares `model: haiku`, `tools: [Read]` (judgment only), body documents the per-node verdict contract.
- [ ] `tools/pre-pr.sh` exits 0 across the whole repo.
- [ ] `ROADMAP.md` rows P2.1, P2.3, P2.4, P2.6, P2.7, P2.9, P2.10 are marked `[x]` with `**Shipped:** 2026-05-28`.
- [ ] `docs/INVENTORY.md` Phase-2 table updates the seven rows from "planned" to "shipped".
- [ ] `.claude/agents/README.md` moves `interview-coder` and `opportunity-merger` from "Planned" to "Shipped".

## Cross-references

- **Consumed by (when shipped):** `/audit-discovery-coherence` (P2.11), `/opportunity-narrative` (P2.12), `/discovery-update` (P2.14), and the Discovery → Validation handover artifact at `discovery/trees/<slug>.md`.
- **Consumes:** Batch A primitives (`interview-snapshot` skill, `opportunity-clustering` skill, `validate_ost.py`); `templates/ost.md`; framework refs; the F4 command-skeleton convention.
- **Frontmatter fields owned:** introduces three kit-composite uses of the `<type> | Adapted` linter escape hatch — `Insight | Adapted` (for interview snapshots, H1 names "Interview Snapshot"), `Opportunity | Adapted` (for opportunity candidate batches, H1 names "Opportunity Candidate Batch"), `Opportunity | Adapted` (for clustering proposals, H1 names "Opportunity Clusters"). These are NOT new Domain A-I ontology types; they consume the kit's documented escape hatch for kit-composite intermediate artifacts. A future RFC may promote them to first-class Domain I composites if they prove load-bearing.
- **Ontology object types touched:** *Interview Snapshot* (Domain B/C — Insight), *Opportunity* (Domain C), *Outcome* (Domain D), *Opportunity Solution Tree* (Domain I composite). All read-write in the artifact files this batch produces.
