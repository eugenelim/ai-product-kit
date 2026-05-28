---
description: Mutates an existing Opportunity Solution Tree — integrates new snapshot evidence, adds Solutions, names `chosen_opportunity:`, restructures the tree via the 9-verb action vocabulary (merge / split / reparent / reframe / delete / add-*). Reads both `discovery/trees/<slug>.md` and `discovery/trees/<slug>.json`; warns on divergence. Converts each human-proposed change into action(s) from the vocabulary. For change sets touching ≥ 3 nodes OR containing any `merge` / `split`, dispatches the `opportunity-merger` agent per affected node for verdicts. Shells out to `scripts/validate_ost.py` with unconditional 5-round repair loop. Writes change-set trail at `discovery/trees/<slug>-change-set-<ISO-timestamp>-<4-hex>.json`. Re-renders markdown from validated JSON. Emits `NEXT: /audit-discovery-coherence` (when `chosen_opportunity:` is set) or stays on `/update-ost`. Phase 2 (Discovery).
argument-hint: <slug> [--from-snapshots <comma-list>] [--from-clusters <clusters-slug>] [--update-evidence-only] [--add-node <spec>] [--force]
---

# /update-ost

> Artifact-mutating Phase-2 command. The companion to `/generate-ost` — every OST evolves via this command after first-pass generation. Reads the existing tree (markdown + JSON), walks proposed changes one at a time, converts them to the 9-verb action vocabulary, optionally fans out to the `opportunity-merger` agent for per-node verdicts on structural changes, validates via `scripts/validate_ost.py` with unconditional 5-round repair, persists, and writes the change-set trail. Gates Handover 2 (Discovery → Validation) — naming `chosen_opportunity:` happens here. Also handles the steady-state weekly habit of integrating new evidence into a living tree.

## When to run

- After `/generate-ost` produced a first-pass tree and the team is ready to name `chosen_opportunity:`.
- Weekly, to integrate new snapshots' evidence into existing Opportunities (use `--update-evidence-only`).
- After a `/cluster-opportunities` run produced new clusters that should be added as Opportunities or merged into existing ones.
- To add Solutions and Assumption Tests as the team's understanding deepens (use `--add-node`).
- To restructure (merge two Opportunities, split a wide one, reparent a Solution) as the OST is iterated.

## Inputs

1. The positional arg — `<slug>` (the existing OST's slug). The command verifies `<repo-root>/discovery/trees/<slug>.md` exists.
2. `<repo-root>/scripts/validate_ost.py` — the validator.
3. `<repo-root>/.claude/agents/opportunity-merger.md` — the fan-out agent dispatched for `merge` / `split` / ≥-3-nodes change sets.
4. Optional `--from-snapshots <comma-list>` — explicit list of new snapshot slugs whose evidence to integrate.
5. Optional `--from-clusters <clusters-slug>` — explicit new clusters proposal whose accepted clusters should be promoted into the tree.
6. Optional `--update-evidence-only` flag — restricts the permitted action vocabulary to `{add-source-opportunity}` only.
7. Optional `--add-node <spec>` flag — for adding one Solution or Assumption Test interactively (`--add-node solution:<parent-OPP-id>` or `--add-node test:<parent-SOL-id>`).
8. Optional `--force` flag — permits overwriting if the new file disagrees with the existing one in expected ways. Has NO effect on the repair loop.

## Procedure

### Step 1 — load and validate the existing tree

Resolve `<repo-root>` as the nearest ancestor containing `tools/lint-frontmatter.py`.

Verify `<repo-root>/discovery/trees/<slug>.md` and `<repo-root>/discovery/trees/<slug>.json` both exist. If either is missing, exit code 2 with: `"OST '<slug>' is missing one of {markdown, JSON projection} — run /generate-ost first."`

Load both files. Compute a quick divergence check: do the H2 "Opportunity space" Opportunities in the markdown have the same id set as `nodes[].id` in the JSON? If not, surface the diff and ask: _"The markdown and JSON projection disagree. A human likely edited the markdown directly between sessions. Trust the markdown (re-derive the JSON) or trust the JSON (re-render the markdown)?"_ Pause and wait for the human's decision before proceeding.

### Step 2 — walk proposed changes one at a time

Ask the human one question to start: _"What would you like to change about this OST? (Add new snapshot evidence, add a Solution / Assumption Test, restructure via merge / split / reparent, name `chosen_opportunity:`, or other.)"_

For each proposed change, walk the human through one or more actions from the 9-verb vocabulary (see `<repo-root>/.claude/skills/ost-validator/references/action-vocabulary.md`):

- **"Add new snapshot evidence to an existing Opportunity"** → one or more `add-source-opportunity` actions.
- **"Add a Solution under Opportunity X"** → one `add-solution` action.
- **"Add an Assumption Test under Solution Y"** → **known gap.** The current 9-verb vocabulary (per `<repo-root>/.claude/skills/ost-validator/references/action-vocabulary.md`) does not include an `add-assumption-test` verb, and `add-solution` produces a Solution node (per `_apply_change_set` in `scripts/validate_ost.py`), not an AssumptionTest. Until the vocabulary is extended (RFC required), this command **cannot** mechanically add an AssumptionTest via the validator-gated change-set path. Workaround for this batch: surface the gap to the human, ask them to add the AssumptionTest manually to the markdown (post-validator), and emit an `open_questions:` entry on the OST referencing this RFC need. Cite `context/frameworks/opportunity-solution-tree.md` §"The four node types" for what an AssumptionTest is and `context/frameworks/falsification.md` for the predeclared-threshold rule. The human's manual edit will not be JSON-projected and may diverge — `/update-ost`'s Step 1 divergence check will catch it next session.
- **"Merge OPP-A and OPP-B"** → one `merge` action with `ids: [A, B]` and `into: A` (or B). Per the spec, this triggers `opportunity-merger` fan-out.
- **"Split OPP-A into two finer Opportunities"** → one `split` action with `id: A` and `into: [new-1, new-2]`. Also triggers fan-out.
- **"Move SOL-1 to OPP-B"** → one `reparent` action.
- **"Rewrite OPP-A's name"** → one `reframe` action.
- **"Delete OPP-A"** → one `delete` action; surface the children-handling concern (per Rule 4: explicit `delete` or `reparent` for every child).
- **"Name `chosen_opportunity:`"** → not a vocabulary action; set the JSON's `chosen_opportunity:` field directly, with `id` and one-paragraph `rationale` from the human.

**`--update-evidence-only` enforcement:** if the flag is set, the permitted action set is `{add-source-opportunity}` only. Any proposed change that would require a different verb triggers a warning and a prompt to re-run without the flag.

Walk each change one at a time. Build up the change-set JSON action list as the session progresses. Confirm each proposed change before advancing.

### Step 3 — optionally dispatch the `opportunity-merger` agent

After the proposed changes are collected, evaluate whether to fan out:

- **Any `merge` or `split` action present?** Yes → fan out.
- **Total touched-node count ≥ 3?** Yes → fan out. (Counting every node that any action's `id`, `ids[]`, `target`, `new_parent`, or `into` field references — per the `opportunity-merger` agent's invocation contract.)

If fanning out, dispatch the `opportunity-merger` agent per affected node. Each dispatch receives:

- `node_id` — the node id under review.
- `proposed_action` — the action that affects this node.
- `current_tree_json_path` — the current OST JSON.
- `proposed_change_set_json_path` — the in-progress change set (saved to a `$(mktemp)` temp file for the agent to read).
- `repo_root`.

Collect verdicts from all dispatches. For each `revise` or `reject` verdict, present to the human:

- _"opportunity-merger reviewed node `<id>` for action `<op>` and returned `<verdict>`. Rationale: `<rationale>`. Alternative action proposal: `<alt>`. Accept the agent's revision, override (keep original), or rework?"_

Update the change set per human decisions. Clean up the temp file.

### Step 4 — build the new projection JSON

Apply the change-set actions to the loaded JSON in memory (mirroring `_apply_change_set` semantics in `scripts/validate_ost.py`). Build the new claimed-output JSON. Save both to `$(mktemp)` temp files.

### Step 5 — shell out to the validator (unconditional repair loop)

```bash
python3 <repo-root>/scripts/validate_ost.py \
  --input <current-projection-tmp-path> \
  --output <new-projection-tmp-path> \
  --change-set <change-set-tmp-path> \
  --format json
```

**The repair loop is unconditional** — the `--force` flag governs only whether existing on-disk files may be overwritten; it has no effect here.

Interpret:

- **Exit 0 (pass):** proceed to Step 6.
- **Exit 1 (rule violation):** parse the JSON failure report. Present violations to the human. Offer up to 5 repair rounds. Each round: revise the change set based on the validator's remediation; rebuild the new-projection JSON; re-invoke the validator. If 5 rounds elapse without convergence, exit code 3 with cumulative validator output; the existing OST is NOT mutated (the temp files were the only changes; clean them up).
- **Exit 2 (input error):** the validator surfaces `reason:`. The bug is in the change-set construction or the projection. Exit code 3 with the validator's report; the command refuses to retry (the bug is internal).

### Step 6 — persist the updated tree (atomic dual-write)

On validator pass:

1. Atomic-write the new JSON projection to `<repo-root>/discovery/trees/<slug>.json` (`tmp + os.replace`-equivalent shell pattern).
2. **Re-render the markdown** from the validated JSON. The render contract — see §"Open question SC1" in the spec: the output markdown must satisfy `templates/ost.md`'s H2 structure (outcome / opportunity space / chosen one / source opportunities / excluded) and carry the OST frontmatter per Handover 2. Walk the JSON's `nodes[]` and group by parent to render H2 "Opportunity space" with H3 sub-sections per Opportunity. Carry `chosen_opportunity:` into both frontmatter and the "Chosen one" H2.
3. Atomic-write the re-rendered markdown to `<repo-root>/discovery/trees/<slug>.md`.
4. Write the change-set trail to `<repo-root>/discovery/trees/<slug>-change-set-<YYYY-MM-DDTHH-MM-SS>-<4-hex>.json`. The random 4-hex suffix prevents same-second collision on rapid re-runs; the trail must never overwrite (the audit history depends on it).
5. Bump `last_updated:` on the markdown frontmatter.

### Step 7 — human-review the re-rendered markdown + emit the next-command hint

Run `python3 <repo-root>/tools/lint-frontmatter.py <repo-root>/discovery/trees/<slug>.md`.

- Exit 0: proceed.
- Non-zero: offer to re-open relevant sections; exit code 3 if the human declines or re-runs still fail.

**Human-review prompt** (until the re-render contract is mechanically tested per Open Question SC1): _"I re-rendered the markdown from the validated JSON. Please scan it for fidelity to the template's structure and the customer-voice tone of the Opportunities. Confirm before I emit the next-command hint."_ Wait for explicit acknowledgement.

Last line of output:

- If `chosen_opportunity:` is set: `NEXT: /assumption-test <chosen-opportunity-slug>` (planned — P3.1).
- Else: `NEXT: /audit-discovery-coherence <slug>` (planned — P2.11), OR `NEXT: /update-ost <slug>` (to continue iterating).

## What this command will not do

- Not persist the OST if `scripts/validate_ost.py` returns non-clean after 5 repair rounds.
- Not override the human's existing `chosen_opportunity:` automatically. A change that mutates the chosen Opportunity's semantic identity (`reframe`, `delete`) requires explicit human acknowledgement that the chosen Opportunity is being un-chosen.
- Not silently move IS-NNN source references between Opportunities. Per Rule 6 (`compound-operation-visibility`), the change set must include intermediate `merge` or `split` actions; if the human's proposed change is a bare reparent of evidence, surface Rule 6 and require restructuring.
- Not run `add-outcome` on a tree that already has an Outcome (per the action vocabulary doc). Use `reframe` to rename.
- Not extend the action vocabulary beyond the 9 canonical verbs. If a proposed change cannot be expressed as one or more existing verbs, surface that as an open question; the human and the kit's RFC process address it, not this command.
- Not assume the working directory is the repo root when invoking the linter or the validator.
- Not overwrite the change-set trail file. Same-second collisions are prevented via the 4-hex suffix; if a write nonetheless fails due to filename collision (e.g., the random suffix coincided), exit code 3 — do not silently overwrite the audit history.
- Not batch placeholder questions — one proposed change at a time.
