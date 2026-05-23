---
description: <one sentence, ≤ 1024 chars — the slash-command palette renders this>
argument-hint: <slug> [--from <parent-slug>] [--force]
# ↑ For artifact-creating commands. For augmenting commands (context-map,
# end-to-end-flow, sequence-initiative) use: <initiative-slug> [--force]
---

# /<command-name>

> <One paragraph: what this command produces, which HANDOVERS row it gates, which template it consumes, what artifact it writes (creating) OR which child file it fills (augmenting). State explicitly whether this is a creating or augmenting command.>

## When to run

- <Trigger 1 — e.g., "After a learning memo's status flips to survived">
- <Trigger 2>
- <Trigger N>

## Inputs

1. The positional arg — `<slug>` (creating commands; the new artifact's slug) OR `<initiative-slug>` (augmenting commands; the existing initiative folder). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars.
2. `templates/<template-path>` — the F3.x template this command consumes.
3. Parent artifact: `<delivery|validation|…>/<parent-family>/<parent-slug>` (creating commands; resolution rule below) OR the initiative folder named by the positional (augmenting commands; no resolution).
4. `<any other input — e.g., a fixture, a configuration file>`

## Procedure

### Step 1 — resolve parent artifact (creating commands) OR validate initiative folder exists (augmenting commands)

**Creating:** If `--from <parent-slug>` is given, use it. Otherwise list candidates from `<parent-family>/` whose `status:` is not in the terminal-or-killed set, sorted by `last_updated:` descending and capped at 10. Present as a numbered list; ask the human to pick one (or to specify `--from` for an older candidate). Never silently pick. If the candidate list is empty, exit with code 2 and surface the missing pre-condition with a remediation suggestion (e.g., "no <parent-type> found in <parent-family>/ — run `/<prerequisite-command>` first").

**Augmenting:** Verify `delivery/initiatives/<initiative-slug>/` exists. If not, exit code 2 with the remediation suggestion to run `/draft-initiative` first.

### Step 2 — instantiate the template (creating) OR locate the child file (augmenting)

**Creating:** Copy `templates/<template-path>` to `<delivery>/<destination-family>/<slug>.md` (or, for folder templates, `cp -r` to `<delivery>/<destination-family>/<slug>/`). If the destination exists and `--force` is not set, exit with code 2 and a remediation suggestion. Pre-fill mechanical fields (`id`, `slug`, `created`, `last_updated`, the resolved `parent_*`, `object_type`).

**Augmenting:** The target child file already exists inside the initiative folder (created by `/draft-initiative`). If the child file is already filled (heuristic: contains no `<placeholder>` substrings) and `--force` is not set, exit code 2 with the remediation suggestion to re-run with `--force`. Augmenting commands do NOT pre-fill `id:` (no new artifact); they update `last_updated:` on the initiative `README.md` to today's date after Step 5 succeeds.

### Step 3 — walk placeholders one H2 section at a time

For each H2 in the template body (or the child file), ask one question per placeholder, sequentially. If an H2 contains H3 sub-sections, treat each H3 as a separate fill unit and confirm all H3s within an H2 before advancing. Never batch. Confirm the section's filled content before advancing.

### Step 4 — surface human-owned decisions

Read the template's `human_owned_decisions:` frontmatter list (for creating commands) or the initiative README's `human_owned_decisions:` list (for augmenting commands). For each entry, present it to the human and ask for explicit confirmation that the decision is owned and (where applicable) signed off. Record the confirmations in `approvals_obtained:`.

### Step 5 — lint the written artifact

Resolve the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`; do not assume the working directory is the repo root. Run `python3 <repo-root>/tools/lint-frontmatter.py <written-path>` (default mode). Report the result.

- If the linter exits 0: proceed to Step 6.
- If the linter exits non-zero: offer to re-open the relevant sections for correction. If the human accepts and the corrections lint clean on re-run, proceed to Step 6 normally. If the human declines (or re-runs but lint still fails), exit code 3 with the linter output surfaced and the artifact left on disk.

### Step 6 — emit the next-command hint

Last line of output, formatted exactly: `NEXT: /<next-command-name> <positional>`. If the next command isn't yet shipped, append `(planned — ROADMAP P<row>)`. For `/sequence-initiative` only, also emit a `REVIEW: delivery/initiatives/<initiative-slug>/capabilities.md — verify the Capability list is filled and each row traces to a parent Problem before running /draft-spec.` line immediately before the NEXT line.

## What this command will not do

- Not overwrite an existing artifact (creating) or already-filled child (augmenting) without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the parent artifact lacks a referenced field, ask, do not invent.
- Not batch placeholder questions — one at a time.
- Not silently pick a parent artifact when multiple candidates exist (creating commands only).
- Not assume the working directory is the repo root when invoking the linter.
- <Add per-command non-behaviors here — e.g., "Not write a vision without citing a learning memo with `status: survived`".>
