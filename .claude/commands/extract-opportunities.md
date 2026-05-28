---
description: Walks a set of Interview Snapshots and extracts candidate Opportunities — each candidate is one H3 sub-section with a one-line statement in the customer's voice, a non-empty `evidence_basis:` naming source `IS-NNN` snapshots, a `lens:` (pain / desire / aspiration), a `confidence:` score, and `open_questions:` for unresolved ambiguity. Refuses to produce candidates with empty `evidence_basis:` — the OST framework's "Source opportunities" rule is non-negotiable. Surfaces snapshot-level `[ambiguous: ...]` flags before walking and asks whether to skip or include them. Writes the batch file at `discovery/opportunities/<slug>.md`. Lints. Emits `NEXT: /cluster-opportunities`. Phase 2 (Discovery).
argument-hint: <slug> [--snapshots <comma-list>] [--force]
---

# /extract-opportunities

> Artifact-creating Phase-2 command. Walks Interview Snapshots from `discovery/snapshots/` and surfaces candidate Opportunities into a batch file at `discovery/opportunities/<slug>.md`. Each candidate is sourced — no `evidence_basis:` means no candidate. Feeds `/cluster-opportunities` (P2.6) and downstream `/generate-ost` (P2.7) — every Opportunity in a real OST must trace back through this batch to a snapshot per the framework's "Source opportunities" discipline.

## When to run

- After a working session of running `/interview-snapshot` (or `interview-coder` dispatches) has produced one or more new Interview Snapshots.
- Weekly, as part of the continuous-discovery habit — extract candidates from snapshots produced that week before they age.
- When `/cluster-opportunities` is about to be run but no batch file exists yet.

## Inputs

1. The positional arg — `<slug>` (the new extraction batch's slug). Kebab-case; default convention: today's date (`YYYY-MM-DD`).
2. `<repo-root>/discovery/snapshots/` — the directory walked for source snapshots.
3. Optional `--snapshots <comma-list>` — explicit list of snapshot slugs to walk. If absent, the command resolves the set of snapshots newer than the most recent batch's `created` (or all snapshots if no prior batch exists). When the set is empty (no new snapshots since the last batch), exit code 2 with `"no new snapshots since last batch — run /interview-snapshot or wait for new interviews."`
4. Optional `--force` flag — permits overwriting an existing batch file.

## Procedure

### Step 1 — resolve the set of snapshots to walk

Resolve `<repo-root>` as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`.

If `--snapshots` is given, verify each named slug resolves to `<repo-root>/discovery/snapshots/<slug>.md`. If any are missing, exit code 2 listing the missing slugs.

Otherwise, list all `<repo-root>/discovery/snapshots/*.md` files. Find the most recent batch under `<repo-root>/discovery/opportunities/*.md` (sort by `created:` field descending). The set to walk = snapshots whose `last_updated:` is newer than the most recent batch's `created:`. If no prior batch exists, the set = all snapshots.

If the resulting set is empty, exit code 2 with: `"no new snapshots since last batch <slug> created on <date> — run /interview-snapshot or wait for new interviews."`

Present the set as a numbered list to the human; confirm before advancing (never silently walk).

### Step 2 — surface and disposition snapshot-level ambiguities

For each snapshot in the set, grep for `[ambiguous: ...]` flags in the body. Surface them as a numbered list grouped by snapshot, and ask the human one question per ambiguity flag (never batch): _"Snapshot <slug> has ambiguity flag: `[ambiguous: <text>]`. Skip this bullet during extraction, or treat it as a candidate input?"_

Record the decisions. Skipped bullets do not contribute to candidates; included bullets become candidates with their `open_questions:` field carrying the original ambiguity text.

### Step 3 — instantiate the batch file

The destination is `<repo-root>/discovery/opportunities/<slug>.md`. If it exists and `--force` is not set, exit code 2 with the standard remediation hint.

Pre-fill frontmatter:

- `id: OPC-<NNN>` — scan existing batches under `<repo-root>/discovery/opportunities/*.md` for `id: OPC-`; max + 1, zero-padded.
- `slug:` — the positional argument.
- `object_type: Opportunity | Adapted` — kit-composite escape hatch (H1 names it "Opportunity Candidate Batch").
- `created:`, `last_updated:` — today's ISO date.
- `status: Draft`.
- `evidence_basis:` — list of `IS-NNN` ids for every snapshot walked, with `source: interview` and `strength: Strong` per snapshot.

### Step 4 — walk each snapshot one at a time, surfacing candidate Opportunities

For each snapshot in the resolved set:

1. Load the snapshot's eight fields.
2. Ask the human one question per candidate the snapshot might support: _"From snapshot `<slug>` (Direct Quote: \"<quote>\"), what candidate Opportunity does this snapshot support? State the Opportunity in the customer's voice (not feature language). If no Opportunity is sourced here, say 'none' and we skip."_
3. For each candidate confirmed, capture: a one-line statement, the `IS-<NNN>` reference into `evidence_basis:` (with the bullet from Pain Points or Workarounds that motivated it), `lens:` (one of `pain | desire | aspiration` — ask which), `confidence:` (one of `high | medium | low` — ask the human based on how directly the snapshot supports the candidate), and `open_questions:` (empty unless this candidate came from an ambiguity flag).
4. **Hard rule: never produce a candidate with empty `evidence_basis:`.** The framework's "Source opportunities" rule is non-negotiable. If the human's draft has an empty evidence list, re-prompt for the `IS-NNN` source.

Append each candidate as one H3 sub-section under H2 "Candidate Opportunities". Format each candidate's H3 heading as `### OPP-CAND-<NNN> — <one-line statement>`, with the metadata listed beneath.

### Step 5 — surface human-owned decisions

Present the batch's `human_owned_decisions:`:

- Accept candidates that survive — these become inputs to `/cluster-opportunities`.
- Reject candidates that are actually Solutions masquerading as Opportunities (per the framework's `## Common failure modes`).
- Park unsourced candidates (the command refused to write them, but the human may want to schedule follow-up interviews to surface the missing evidence).

Ask for explicit acknowledgement.

### Step 6 — lint the written artifact

Run `python3 <repo-root>/tools/lint-frontmatter.py <repo-root>/discovery/opportunities/<slug>.md`.

- Exit 0: proceed.
- Non-zero: offer to re-open relevant sections for correction; exit code 3 if the human declines or re-runs still fail.

### Step 7 — emit the next-command hint

Last line of output: `NEXT: /cluster-opportunities <slug>`.

## What this command will not do

- Not produce a candidate with empty `evidence_basis:`. The framework's "Source opportunities" rule is non-negotiable; unsourced candidates are conjecture and conjecture pollutes the OST.
- Not silently include `[ambiguous: ...]` bullets — surface them and ask the human first.
- Not promote a Solution masquerading as an Opportunity. The framework names this anti-pattern; the command surfaces it as a `human_owned_decision:`.
- Not overwrite an existing batch without `--force`.
- Not batch placeholder questions — one at a time per candidate.
- Not assume the working directory is the repo root when invoking the linter.
- Not silently walk snapshots — always confirm the resolved set with the human first.
