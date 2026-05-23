---
description: Fill delivery/initiatives/<initiative-slug>/context-map.md in place — walk the bounded-context list and per-context detail (owner, public contract, Wardley-lite evolution check) interactively, lint the initiative README, chain to /end-to-end-flow.
argument-hint: <initiative-slug> [--force]
---

# /context-map

> Artifact-augmenting Phase-4 template-fill command. Operates on an existing `delivery/initiatives/<initiative-slug>/` folder; fills the placeholder `context-map.md` child file in place. No new artifact is created. Per the parent convention's argv contract, this command's positional is `<initiative-slug>` — the parent IS the initiative folder named by the positional. No `--from` flag, no parent resolution. Bumps the initiative README's `last_updated:` on success.

## When to run

- After `/draft-initiative <initiative-slug>` has scaffolded the initiative folder and the placeholder `context-map.md` child is in place.
- Before `/end-to-end-flow <initiative-slug>` — `end-to-end-flow`'s Mermaid swimlanes ARE this command's bounded contexts.
- When HANDOVERS-5 §"Required content" item 1 (per-bounded-context detail) is the missing artifact in the initiative folder.

## Inputs

1. The positional arg — `<initiative-slug>`. Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. Names the existing initiative folder; the command does NOT create it.
2. `templates/initiative/context-map.md` — the F3.7 child template (source-of-shape reference; not copied at runtime — already copied by `/draft-initiative`).
3. `delivery/initiatives/<initiative-slug>/context-map.md` — the in-place placeholder child file the command fills.
4. `delivery/initiatives/<initiative-slug>/README.md` — read for `human_owned_decisions:` (Step 4) and mutated in Step 5 (`last_updated:` + `approvals_obtained:`).
5. Optional flag `--force` — permits re-walking an already-filled `context-map.md`.

## Procedure

### Step 1 — verify the initiative folder and child file exist

Verify `delivery/initiatives/<initiative-slug>/` exists. If not, exit code 2 with: `"no initiative folder found at delivery/initiatives/<initiative-slug>/ — run /draft-initiative <initiative-slug> first."`

Verify `delivery/initiatives/<initiative-slug>/README.md` exists. If not, exit code 2 with: `"initiative folder present but README.md missing — restore it from templates/initiative/README.md or re-run /draft-initiative <initiative-slug> (the README is the source of human_owned_decisions: walked in Step 4 and the target of the last_updated: bump in Step 5)."`

Verify `delivery/initiatives/<initiative-slug>/context-map.md` exists. If not, exit code 2 with: `"no context-map.md found inside the initiative folder — run /draft-initiative <initiative-slug> first (the child file is created in placeholder form when the initiative folder is scaffolded from templates/initiative/)."`

This is the augmenting-command equivalent of the convention's Step 1. There is NO parent-artifact resolution; the parent IS the initiative folder named by the positional.

### Step 2 — locate the placeholder child file and check it's still placeholder-shaped

Open `delivery/initiatives/<initiative-slug>/context-map.md`. If the file contains no `<placeholder>` substrings (heuristic for "already filled") and `--force` is not set, exit code 2 with: `"context-map.md appears already filled (no <placeholder> substrings remain). Re-run with --force to walk the H2s again and overwrite."`

Augmenting commands do NOT pre-fill `id:` — there is no new artifact. They DO update `last_updated:` on the initiative README to today's date after Step 5 succeeds.

### Step 3 — walk H2 sections one at a time

Walk these prompts in document order. One question per turn. Never batch.

**`## Bounded contexts in this initiative` — orientation paragraph:**

1. _"What does 'bounded context' mean for this initiative? Write a one-sentence definition scoped to the initiative — the boundary criterion you'll use to decide whether two pieces of work belong in the same context or in different contexts."_
2. _"Which bounded contexts are explicitly **in scope** for this initiative? List them as a comma-separated list of short names — each name will become an H3 sub-section under §Per-bounded-context detail."_
3. _"Which bounded contexts are explicitly **out of scope** for this initiative? List them as a comma-separated list of short names. (Naming what's out of scope here prevents downstream specs from quietly absorbing the boundary.)"_

**`## Per-bounded-context detail` — one H3 block per bounded context.** For each in-scope context named in prompt 2, walk one full H3 block (four labeled fields). Confirm the block before asking whether to add another.

For context `<name>`:

4. **Owner.** _"Who owns context `<name>`? Name a single human or team. Do NOT pick on the human's behalf, even if only one candidate is obvious from the initiative's `crosses_teams:` list — always ask. Per the initiative README's `human_owned_decisions:` list, bounded-context ownership assignment is a human-owned decision."_
5. **Public contract.** _"What is the public contract of context `<name>`? Write a one-sentence summary of the boundary contract — the API, event schema, or shared shape that other contexts depend on. If multiple other contexts depend on different surfaces of `<name>`, name the most load-bearing one and add a note about the others."_
6. **Commodity vs custom (Wardley).** _"Pick one for context `<name>`: `commodity` | `utility` | `product` | `custom`. The Wardley-lite evolution check — per the initiative README's `human_owned_decisions:` list (`Build vs buy decisions in the evolution check`), this is a human-owned decision. If the call is unclear, prefer `custom` and add a one-line note explaining the uncertainty. Do not skip this prompt for any context."_
7. **Evolution stage.** _"Pick one for context `<name>`: `genesis` | `custom` | `product` | `commodity`. Evolution stage names where the context is *today*; the Wardley call in the previous question names where it should be. The two often agree; when they disagree, the disagreement is itself the surfaced finding."_

After all four fields are filled for context `<name>`:

8. **Add another context?** _"Add another bounded context block under §Per-bounded-context detail? `y` to walk the next context, `n` to advance to Step 4 (human-owned-decisions confirmation)."_

### Step 4 — surface human-owned decisions

Read the initiative README's `human_owned_decisions:` list (F3.7 pre-fills HANDOVERS-5's three strings: `Bounded-context ownership assignment`, `Build vs buy decisions in the evolution check`, `Delivery sequencing`). The first two are directly relevant to this command's walk. Present each to the human for explicit confirmation. Record confirmations in the initiative README's `approvals_obtained:` list (append, do not overwrite).

### Step 5 — lint the filled file and bump last_updated

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py` (do not assume cwd). Run `python3 <repo-root>/tools/lint-frontmatter.py delivery/initiatives/<initiative-slug>/README.md` (default mode). `context-map.md` has no frontmatter (F3.7 OQ4) and is not separately linted.

- Exit 0: bump the README's `last_updated:` to today's date (ISO-8601). Proceed to Step 6.
- Non-zero: surface the linter output; offer to re-open the relevant README sections for correction. If the human accepts and re-lint exits 0, bump `last_updated:` and proceed. If the human declines (or re-lint still fails), exit code 3. Do NOT bump `last_updated:` in the exit-3 path.

### Step 6 — emit the next-command hint

Last line of output, formatted exactly:

```
NEXT: /end-to-end-flow <initiative-slug>
```

No `REVIEW:` line is emitted (only `/sequence-initiative` emits a REVIEW interstitial).

## Exit codes

- `0` — child file walked and filled, README `last_updated:` bumped, linter passed, NEXT emitted.
- `1` — human aborted the interactive walk before Step 5 completed. The child file is left in whatever partial state Step 3 reached; the README's `last_updated:` is NOT bumped. Resume by re-running with the same slug (and `--force` if the partial fill removed `<placeholder>` substrings).
- `2` — pre-conditions failed (initiative folder missing; README missing; `context-map.md` missing; file already filled without `--force`).
- `3` — child walked successfully but the post-fill README lint exited non-zero, and the human declined re-open (or re-open failed). Child file persists; `last_updated:` is NOT bumped.

## What this command will not do

- Not create a new artifact at any path — fills a placeholder child file in place.
- Not skip the Wardley-lite commodity-vs-custom evolution check for any bounded context. The four HANDOVERS-5 fields are non-negotiable.
- Not auto-pick the bounded-context owner — always ask, even when only one candidate is obvious from the initiative's `crosses_teams:` list.
- Not overwrite an already-filled `context-map.md` without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the initiative README lacks a referenced field, ask, do not invent.
- Not batch placeholder questions — one at a time.
- Not assume the working directory is the repo root when invoking the linter.
- Not modify the initiative README beyond `last_updated:` (bumped on success) and `approvals_obtained:` (appended at Step 4).
- Not touch `flow.md`, `sequence.md`, `child-specs.md`, or `capabilities.md` inside the same folder — those have their own commands.
- Not modify `templates/initiative/context-map.md`. The template is the source-of-shape, frozen by F3.7.
- Not pre-fill `id:` — augmenting commands have no new artifact.

$ARGUMENTS
