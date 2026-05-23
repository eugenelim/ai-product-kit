---
description: Walk the human through filling delivery/initiatives/<initiative-slug>/sequence.md — the dependency DAG of child specs and first-shippable subset — and emit a REVIEW reminder pointing at capabilities.md before chaining to /draft-spec.
argument-hint: <initiative-slug> [--force]
---

# /sequence-initiative

> Artifact-augmenting Phase-4 template-fill command. Operates on an existing `delivery/initiatives/<initiative-slug>/` folder; fills the placeholder `sequence.md` child in place with a Mermaid `graph LR` DAG of child specs (nodes = spec slugs from `child-specs.md`) plus a `**First shippable subset:**` callout. **This is the ONE command in the seven that emits a `REVIEW:` line in its chaining hint** — per the convention's §"Capabilities-file interstitial", the REVIEW line precedes the NEXT line and points at `capabilities.md` for human review before `/draft-spec` runs. The REVIEW + NEXT lines ship as a pair; emitting one without the other is a regression.

## When to run

- After `/end-to-end-flow <initiative-slug>` has run cleanly. Both `context-map.md` and `flow.md` must be filled — the DAG draws on both.
- After `child-specs.md` lists at least one spec slug (typically populated incidentally during `/draft-initiative`'s walk or appended by earlier `/draft-spec` runs).
- Before `/draft-spec` — the sequencing decision drives which spec the human drafts first.

## Inputs

1. The positional arg — `<initiative-slug>`. Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. Names the existing initiative folder.
2. `templates/initiative/sequence.md` — the F3.7 child template (source-of-shape reference; already at the destination).
3. `delivery/initiatives/<initiative-slug>/sequence.md` — the in-place placeholder child file the command fills.
4. `delivery/initiatives/<initiative-slug>/context-map.md` and `flow.md` — pre-condition files. Both must be filled (no `<placeholder>` substrings; for `flow.md`, also no `ActorA`/`ActorB`/`TriggerEvent`/`ResponseOrSuccessOutcome` template-default identifiers).
5. `delivery/initiatives/<initiative-slug>/child-specs.md` — the manifest table of spec slugs that become DAG nodes.
6. `delivery/initiatives/<initiative-slug>/capabilities.md` — referenced by the REVIEW interstitial; not modified by this command.
7. `delivery/initiatives/<initiative-slug>/README.md` — read for `human_owned_decisions:` (Step 4) and mutated in Step 5 (`last_updated:` bump).
8. Optional flag `--force` — permits re-walking an already-filled `sequence.md`.

## Procedure

### Step 1 — verify the initiative folder, README, and pre-conditions

Verify `delivery/initiatives/<initiative-slug>/` exists. If not, exit code 2 with: `"no initiative folder found at delivery/initiatives/<initiative-slug>/ — run /draft-initiative <initiative-slug> first."`

Verify `delivery/initiatives/<initiative-slug>/README.md` exists. If not, exit code 2 with a remediation to restore from `templates/initiative/README.md` or re-run `/draft-initiative`.

Verify `context-map.md` is filled (no `<placeholder>` substrings). If not, exit code 2 with remediation to run `/context-map <initiative-slug>` first.

Verify `flow.md` is filled — use the same heuristic `/end-to-end-flow` uses for `--force` detection (no `<placeholder>` substrings AND no `ActorA`/`ActorB`/`TriggerEvent`/`ResponseOrSuccessOutcome` template-default identifiers). If not filled, exit code 2 with remediation to run `/end-to-end-flow <initiative-slug>` first.

Verify `child-specs.md` lists at least one spec slug. If empty, exit code 2 with: `"child-specs.md is empty — populate it manually with at least one spec slug, or run /draft-spec first to append a row, before sequencing."`

This is the augmenting-command equivalent of the convention's Step 1. There is NO parent-artifact resolution; the parent IS the initiative folder named by the positional.

### Step 2 — locate the placeholder child file

Open `delivery/initiatives/<initiative-slug>/sequence.md`. If the file is already filled (heuristic: contains no `<placeholder>`, `SpecA`, `SpecB`, `SpecC`, or `SpecD` substrings — the F3.7 template's example placeholders have been overwritten) and `--force` is not set, exit code 2 with: `"sequence.md appears already filled. Re-run with --force to overwrite, or edit the file directly if the change is small."`

Augmenting commands do NOT pre-fill `id:` — there is no new artifact. They DO update `last_updated:` on the initiative README to today's date after Step 5 succeeds.

### Step 3 — walk the single H2 section one prompt at a time

The template has exactly one H2 — `## Delivery sequence` — containing one Mermaid `graph LR` fenced block and one `**First shippable subset:**` callout. Walk these prompts in order. One question per turn. Never batch.

1. _"Open `child-specs.md` for this initiative. List the spec slugs that exist in the manifest. I will use these as the node IDs of the DAG. Confirm the slug list, or amend it now."_
2. _"For each spec slug, name its upstream dependencies — the specs whose output it consumes. A spec with no upstream dependencies is a root; a spec with no downstream consumers within this initiative is a leaf. I will ask you slug-by-slug. We begin with `<first-slug-from-child-specs>`. What are its upstream dependencies (zero or more, comma-separated spec slugs from this initiative's `child-specs.md`)?"_ (Repeated per slug, one slug at a time, in the order they appear in `child-specs.md`.)
3. _"Which specs can ship in parallel? Group any specs that share no dependency edges and depend on the same upstream parents. Parallelizability is a delivery-team decision; I am asking, not deriving."_
4. _"Identify the first-shippable subset: the smallest set of specs that, shipped together, deliver an end-to-end customer outcome — even if narrower than the full Initiative. This is a human-owned sequencing decision per the initiative README's `human_owned_decisions:` list. Name the spec slugs in the first-shippable subset."_
5. _"For each spec in the first-shippable subset, confirm whether it is a leaf (the customer-facing terminal output) or a root (an upstream prerequisite). The leaf-vs-root call drives which spec `/draft-spec` should be authored first — usually the leaf, because the leaf's acceptance criteria constrain the roots."_
6. _"Render the DAG in Mermaid `graph LR` syntax inside the fenced block. Use bare alphanumeric node IDs (the spec slugs themselves, kebab-case stripped to alphanumeric-and-dashes — Mermaid tolerates dashes in node IDs). I will substitute the rendered block into `sequence.md` and replace the placeholder `SpecA[Spec A] --> SpecB[Spec B]` example block."_
7. _"Confirm the rendered DAG. Adjust nodes or edges if needed before I write the file."_
8. _"Update the `**First shippable subset:**` callout immediately below the diagram with the comma-separated spec slug list you named in step 4."_
9. _"Finally — and this is the question whose answer becomes the NEXT-line argument when this command exits — which spec slug should be drafted first via `/draft-spec`? Typically a leaf of the first-shippable subset. If you decline to name one now, the NEXT line will surface a literal placeholder and you will name it when you run `/draft-spec`."_

### Step 4 — surface human-owned decisions

Re-surface the initiative README's `human_owned_decisions:` list (specifically "Delivery sequencing", verbatim from HANDOVERS-5) and ask for explicit confirmation that the sequencing decisions just captured are owned. Append confirmations to `approvals_obtained:` (do not overwrite).

### Step 5 — lint the initiative README and bump last_updated

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py` (do not assume cwd). Run `python3 <repo-root>/tools/lint-frontmatter.py delivery/initiatives/<initiative-slug>/README.md` (default mode). `sequence.md` has no frontmatter (F3.7 OQ4) and is not separately linted.

- Exit 0: bump the README's `last_updated:` to today's date. Proceed to Step 6.
- Non-zero: surface the linter output; offer to re-open the relevant README sections. If the human accepts and re-lint exits 0, bump and proceed. If the human declines (or re-lint still fails), exit code 3. Do NOT bump `last_updated:` in the exit-3 path.

### Step 6 — emit the REVIEW + NEXT two-line chaining hint

The final two lines of stdout, in this exact order:

```
REVIEW: delivery/initiatives/<initiative-slug>/capabilities.md — verify the Capability list is filled and each row traces to a parent Problem before running /draft-spec.
NEXT: /draft-spec <first-spec-slug>
```

The REVIEW line **precedes** the NEXT line. The two are written as a pair: emitting NEXT without REVIEW (or REVIEW without NEXT) is a regression. `<first-spec-slug>` is the spec slug the human named in prompt 9; if the human declined to name one, the NEXT line emits the literal placeholder `<slug>`. If `/draft-spec` is not yet shipped at the moment this command runs, append `(planned — ROADMAP P4.8)` to the NEXT line per the kit-drift policy — in practice the seven Phase-4 commands ship as one wave, so this branch is expected to be un-exercised in the first roll-out; the guard must still be implemented.

The REVIEW line is the kit's mitigation for the gap that `capabilities.md` has no dedicated Phase-4 command. Without a forced human pause here, `/draft-spec` would consume a possibly-empty or possibly-untraced Capability list, and the traceability chain `Requirement → Capability → Problem` would silently break.

## Exit codes

- `0` — `sequence.md` filled, README `last_updated:` bumped, linter passed, REVIEW + NEXT two-line hint emitted.
- `1` — human aborted the walk before Step 5 completed. `sequence.md` left in partial state; README NOT bumped. Resume by re-running with the same slug and `--force`.
- `2` — pre-conditions failed (initiative folder missing; README missing; `context-map.md` or `flow.md` still in placeholder form; `sequence.md` already filled without `--force`; `child-specs.md` empty).
- `3` — `sequence.md` written but post-fill README lint exited non-zero, and the human declined re-open. Both files persist in their known-imperfect state.

## What this command will not do

- Not create a new artifact at any path — fills a placeholder child file in place.
- Not emit a NEXT line without the preceding REVIEW line — they ship as a pair. Emitting one without the other is a regression.
- Not auto-pick the first-shippable subset. The human owns sequencing decisions per the initiative README's `human_owned_decisions:` list.
- Not build the DAG without consulting `context-map.md` and `flow.md`. Both are pre-condition checks in Step 1; exit 2 with remediation if either is still in placeholder form.
- Not fabricate spec slugs not present in `child-specs.md`. The DAG nodes ARE the manifest rows.
- Not auto-run `/audit-traceability` against `capabilities.md`. The REVIEW line is a human-judgment substitution; the audit runs at human discretion later.
- Not modify `capabilities.md`. The REVIEW line points at it for the human to review; this command does not write to it.
- Not overwrite an already-filled `sequence.md` without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the initiative README lacks a referenced field, ask, do not invent.
- Not batch placeholder questions — one at a time.
- Not assume the working directory is the repo root when invoking the linter.
- Not modify the initiative README beyond `last_updated:` (bumped on success) and `approvals_obtained:` (appended at Step 4).
- Not touch `context-map.md`, `flow.md`, `child-specs.md`, or `capabilities.md` (read-only references).
- Not lint `sequence.md` itself — it has no frontmatter. The lint target is the initiative README.
- Not modify `templates/initiative/sequence.md`. The template is frozen by F3.7.
- Not pre-fill `id:` — augmenting commands have no new artifact.

$ARGUMENTS
