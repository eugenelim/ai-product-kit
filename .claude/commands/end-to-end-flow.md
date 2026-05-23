---
description: Fill delivery/initiatives/<initiative-slug>/flow.md in place — walk the Mermaid sequence diagram body and caption interactively (one prompt at a time), lint the initiative README, chain to /sequence-initiative.
argument-hint: <initiative-slug> [--force]
---

# /end-to-end-flow

> Artifact-augmenting Phase-4 template-fill command. Operates on an existing `delivery/initiatives/<initiative-slug>/` folder; fills the placeholder `flow.md` child in place with a Mermaid `sequenceDiagram` body and one-paragraph caption matching HANDOVERS-5 §"Required content" item 2. Pre-condition: `context-map.md` must already be filled — the Mermaid swimlanes ARE the context-map's bounded contexts. No `--from` flag, no parent resolution. Bumps the initiative README's `last_updated:` on success.

## When to run

- After `/context-map <initiative-slug>` has run cleanly on the same initiative (context-map.md must be filled — its bounded contexts become this command's Mermaid swimlanes).
- Before `/sequence-initiative <initiative-slug>` — the sequencing DAG reasons over the end-to-end flow.
- When HANDOVERS-5 §"Required content" item 2 (Mermaid sequence diagram of end-to-end customer flow across contexts) is the missing artifact.

## Inputs

1. The positional arg — `<initiative-slug>`. Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. Names the existing initiative folder; the command does NOT create it.
2. `templates/initiative/flow.md` — the F3.7 child template (source-of-shape reference; the file already exists at the destination, copied by `/draft-initiative`).
3. `delivery/initiatives/<initiative-slug>/flow.md` — the in-place placeholder child file the command fills.
4. `delivery/initiatives/<initiative-slug>/context-map.md` — the pre-condition file. Must be filled (no `<placeholder>` substrings). Exit 2 if still in placeholder form.
5. `delivery/initiatives/<initiative-slug>/README.md` — read for `human_owned_decisions:` (Step 4) and mutated in Step 5 (`last_updated:` bump).
6. Optional flag `--force` — permits re-walking an already-filled `flow.md`.

## Procedure

### Step 1 — verify the initiative folder, README, and context-map prerequisite

Verify `delivery/initiatives/<initiative-slug>/` exists. If not, exit code 2 with: `"no initiative folder found at delivery/initiatives/<initiative-slug>/ — run /draft-initiative <initiative-slug> first."`

Verify `delivery/initiatives/<initiative-slug>/README.md` exists. If not, exit code 2 with: `"initiative folder present but README.md missing — restore it from templates/initiative/README.md or re-run /draft-initiative (the README is the source of human_owned_decisions: and the target of the last_updated: bump in Step 5)."`

Verify `delivery/initiatives/<initiative-slug>/context-map.md` exists AND is filled (contains no `<placeholder>` substrings). If missing or still placeholder-shaped, exit code 2 with: `"context-map.md still in placeholder form — run /context-map <initiative-slug> first. The Mermaid swimlanes in flow.md must match the bounded contexts named in context-map.md; without that, the flow is incoherent."`

This is the augmenting-command equivalent of the convention's Step 1. There is NO parent-artifact resolution; the parent IS the initiative folder named by the positional.

### Step 2 — locate the placeholder child file

Open `delivery/initiatives/<initiative-slug>/flow.md`. If the file is already filled (heuristic: contains no `<placeholder>` substrings AND no `ActorA`/`ActorB`/`TriggerEvent`/`ResponseOrSuccessOutcome` template-default identifiers) and `--force` is not set, exit code 2 with: `"flow.md appears already filled. Re-run with --force to overwrite — the kit user re-answers every prompt and the prior content is replaced wholesale."`

Augmenting commands do NOT pre-fill `id:` — there is no new artifact. They DO update `last_updated:` on the initiative README to today's date after Step 5 succeeds.

### Step 3 — walk the single H2 section one prompt at a time

The template has exactly one H2 — `## End-to-end customer flow` — containing a Mermaid `sequenceDiagram` fenced block and a one-paragraph caption. Walk these prompts in order. One question per turn. Never batch. Render the assembled Mermaid block to the human (as raw markdown) for visual confirmation before write.

1. **Actor list (Mermaid `participant` declarations).** _"Looking at `context-map.md`, which bounded contexts participate in this end-to-end flow as actors? List them in the order they first appear in the happy path, using bare CamelCase identifiers (Mermaid's tokenizer breaks on angle brackets). Example: `Frontend`, `OrdersService`, `PaymentGateway`."_
2. **Swimlanes per bounded context.** _"For each bounded context you named, confirm whether it appears as a single `participant` line or whether you want to split it into multiple swimlanes (e.g., `OrdersServiceAPI` and `OrdersServiceWorker`). One swimlane per Mermaid `participant` declaration. If unsure, prefer one per bounded context."_
3. **Trigger event.** _"What is the trigger event that starts the happy path? Name the actor that initiates it and the event label. This becomes the first `->>` arrow in the diagram. Example: `User ->> Frontend: PlaceOrder`."_
4. **Happy-path sequence.** _"Walk me through the happy-path sequence one message at a time. For each message: source actor, destination actor, message label (CamelCase, no angle brackets), and whether it is a request (`->>`) or a response (`-->>`). Say `done` when the happy path reaches the success outcome."_
5. **Success outcome.** _"What is the success outcome — the final response or state change that completes the happy path? This becomes the caption's `<success outcome>` and the diagram's last arrow."_
6. **Error / failure branches.** _"Are there error or failure branches that belong in scope for this end-to-end flow? If yes, name each branch by its trigger condition and the actors involved. If the flow is happy-path-only at this stage, say `none` — error branches can be added later by re-running with `--force`."_
7. **Async / out-of-band boundaries.** _"Are there async or out-of-band boundaries in the flow — e.g., a message queue, a webhook, an eventual-consistency boundary that the diagram must represent? If yes, name each and the actors on either side. If the flow is fully synchronous, say `none`."_
8. **Caption prose.** _"Write a one-paragraph caption naming the trigger event, the actors involved, and the success outcome. Angle-bracket placeholders are fine in this prose (Mermaid's tokenizer constraint applies only inside the fenced block)."_

### Step 4 — surface human-owned decisions

Read the initiative README's `human_owned_decisions:` list. For each entry, ask the human for explicit confirmation. Append confirmations to `approvals_obtained:` (do not overwrite).

### Step 5 — lint the initiative README and bump last_updated

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py` (do not assume cwd). Run `python3 <repo-root>/tools/lint-frontmatter.py delivery/initiatives/<initiative-slug>/README.md` (default mode). `flow.md` has no frontmatter (F3.7 OQ4) and is not separately linted.

- Exit 0: bump the README's `last_updated:` to today's date. Proceed to Step 6.
- Non-zero: surface the linter output; offer to re-open the relevant README sections. If the human accepts and re-lint exits 0, bump and proceed. If the human declines (or re-lint still fails), exit code 3. Do NOT bump `last_updated:` in the exit-3 path.

### Step 6 — emit the next-command hint

Last line of output, formatted exactly:

```
NEXT: /sequence-initiative <initiative-slug>
```

No `REVIEW:` line is emitted (only `/sequence-initiative` emits a REVIEW interstitial).

## Exit codes

- `0` — `flow.md` filled, README `last_updated:` bumped, linter passed, NEXT emitted.
- `1` — human aborted the walk before Step 5 completed. `flow.md` left in partial state; README NOT bumped. Resume by re-running with the same slug and `--force`.
- `2` — pre-conditions failed (initiative folder missing; README missing; `context-map.md` still in placeholder form; `flow.md` already filled without `--force`).
- `3` — `flow.md` written but post-fill README lint exited non-zero, and the human declined re-open. Artifact persists; `last_updated:` is NOT bumped.

## What this command will not do

- Not create a new artifact at any path — fills a placeholder child file in place.
- Not invent a bounded-context name not present in `context-map.md`. Exit 2 with remediation if `context-map.md` is still in placeholder form.
- Not auto-generate Mermaid syntax without confirming the actors and swimlanes with the human first.
- Not write angle brackets inside the fenced Mermaid block — Mermaid's tokenizer rejects them. (Angle-bracket placeholders are fine in the caption prose outside the fenced block.)
- Not overwrite an already-filled `flow.md` without `--force`. With `--force`, the prior content is replaced wholesale, not merged.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the initiative README lacks a referenced field, ask, do not invent.
- Not batch placeholder questions — one at a time.
- Not assume the working directory is the repo root when invoking the linter.
- Not modify the initiative README beyond `last_updated:` (bumped on success) and `approvals_obtained:` (appended at Step 4).
- Not touch `context-map.md`, `sequence.md`, `child-specs.md`, or `capabilities.md` inside the same folder — those have their own commands.
- Not lint `flow.md` itself — it has no frontmatter. The lint target is the initiative README.
- Not modify `templates/initiative/flow.md`. The template is frozen by F3.7.
- Not pre-fill `id:` — augmenting commands have no new artifact.

$ARGUMENTS
