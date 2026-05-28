---
description: Turns one raw customer-interview transcript into one structured Interview Snapshot artifact at `discovery/snapshots/<slug>.md`. Loads the `interview-snapshot` skill, walks the eight snapshot fields (Goal / Workflow / Pain Points / Workarounds / Tools / Direct Quote / Date / Interviewer) one at a time via the skill's operational rules — speaker detection, time-aligned quote extraction, paraphrase enforcement, no-recording fallback. Refuses to fabricate; surfaces ambiguity flags. Lints the written file. Emits `NEXT: /extract-opportunities` so the snapshot can feed candidate-Opportunity extraction. Phase 2 (Discovery), Handover-2 prerequisite.
argument-hint: <slug> [--from <transcript-path>] [--interviewer <name>] [--date <YYYY-MM-DD>] [--no-recording] [--force]
---

# /interview-snapshot

> Artifact-creating Phase-2 command. Walks one raw customer-interview transcript through the `interview-snapshot` skill's operational rules and writes a structured Interview Snapshot file at `discovery/snapshots/<slug>.md`. Eight snapshot fields from `context/frameworks/interview-snapshot.md` are filled one at a time, with paraphrase rules enforced against the canonical fabrication patterns (invented diagnosis, emotion escalation, invented feature request). Gates Handover 2 (Discovery → Validation) — every Opportunity in a downstream OST must trace to at least one snapshot via its `evidence_basis:` field.

## When to run

- After conducting a customer-discovery interview (recording or notes), to capture the structured snapshot before the raw transcript ages out of memory.
- When a batch of transcripts needs coding — prefer dispatching the `interview-coder` agent in parallel per transcript, and use this command for the single-transcript interactive session.
- When an audit pipeline surfaces an OST Opportunity whose `evidence_basis:` cites an `IS-NNN` reference with no on-disk snapshot — re-run this command against the original transcript.

## Inputs

1. The positional arg — `<slug>` (the new snapshot's slug). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. Convention: `<interviewee-firstname>-<YYYY-MM-DD>`.
2. `<repo-root>/.claude/skills/interview-snapshot/SKILL.md` (P2.2) — the canonical rule library the command loads in Step 3.
3. The raw transcript — either `--from <transcript-path>` or, if absent, the command prompts the human for a file path or pasted content.
4. Optional `--interviewer <name>` — defaults to prompting the human.
5. Optional `--date <YYYY-MM-DD>` — defaults to today.
6. Optional `--no-recording` flag — switches the Direct Quote attribution to the framework's `[no recording]` path.
7. Optional `--force` flag — permits overwriting an existing `discovery/snapshots/<slug>.md`.

## Procedure

### Step 1 — resolve the transcript source

If `--from <transcript-path>` is given, verify the file exists. If absent, exit code 2 with: `"transcript file '<path>' not found — provide a path that exists or omit --from to paste the transcript inline."`

If `--from` is not given, ask the human one question: "Paste the transcript inline, or give me a path to the transcript file." Wait for response. If the response is a path, resolve it. If the response is inline content, capture it.

If the transcript is empty (≤ 50 characters), exit code 2 with: `"transcript appears empty — discovery interviews are typically ≥ 5 minutes of content; re-run with the real transcript or schedule a follow-up interview."`

### Step 2 — instantiate the snapshot file

Resolve `<repo-root>` as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`.

The destination is `<repo-root>/discovery/snapshots/<slug>.md`. If it already exists and `--force` is not set, exit code 2 with: `"discovery/snapshots/<slug>.md already exists — re-run with --force to overwrite, or pick a different slug."`

Pre-fill mechanical frontmatter (do not ask the human):

- `id: IS-<NNN>` — scan `<repo-root>/discovery/snapshots/` for existing `id: IS-` lines, take max + 1, zero-pad to three digits. If none exist, start at `IS-001`.
- `slug:` — the positional argument.
- `object_type: Insight | Adapted` — the kit-composite escape hatch per `tools/lint-frontmatter.py` (the H1 names it as "Interview Snapshot" per the framework; the linter accepts `<type> | Adapted` for kit-composite types not yet in the ontology).
- `created:` — today's ISO date.
- `last_updated:` — same as `created`.
- `status: Draft`.

Ask the human only for `interviewer:` and `date:` if they were not supplied as flags. Confirm both before advancing.

### Step 3 — load the `interview-snapshot` skill, then walk the eight snapshot fields

Load the P2.2 skill (`.claude/skills/interview-snapshot/SKILL.md`). The skill's `## Speaker detection`, `## Time-aligned quote extraction`, `## Paraphrase enforcement`, and `## No-recording fallback` sections are the operational rules for this step.

Walk the eight fields per `context/frameworks/interview-snapshot.md`, one at a time. Never batch. Confirm each field's content before advancing.

**Field 1 — Goal.** Ask: _"In one sentence, in the customer's own framing — what was the customer trying to do? Paraphrase faithfully; do not infer a goal they didn't state."_ If the customer's stated goal is feature-shaped (e.g., "I want an export feature"), surface that and ask whether to record the literal stated goal or rephrase to the underlying objective the transcript supports.

**Field 2 — Workflow.** Ask: _"List the ordered steps the customer described — one bullet per step, in the order they narrated. If a step is ambiguous (the customer said something like 'and then I just do the thing'), record it as `[ambiguous: ...]` per the framework — do not infer."_

**Field 3 — Pain Points.** Ask: _"One bullet per distinct moment of friction. Anchor each bullet to a workflow step if possible. Apply the paraphrase rule — record what the customer said, not your diagnosis of what was wrong."_

**Field 4 — Workarounds.** Ask: _"What did the customer do to cope with each pain point? Workarounds are often more revealing than complaints — record them faithfully."_

**Field 5 — Tools.** Ask: _"What tools did the customer name? Use the names they used, not the categories."_

**Field 6 — Direct Quote.** Ask: _"One verbatim quote from the transcript, in the framework's exact format `\"<verbatim>\" — <Speaker Name>, <MM:SS>` (or `, [no recording]` if --no-recording is set). If the most decision-useful quote is multi-sentence, up to three sentences is fine. Inaudible words are marked `[inaudible]`; do not guess. If no verbatim quote survives, surface `[ambiguous: no-verbatim-quote-available]` and confirm with me whether to ship with the marker."_

**Field 7 — Date.** Pre-filled from `--date` or step 2; confirm once.

**Field 8 — Interviewer.** Pre-filled from `--interviewer` or step 2; confirm once. A role ("PM") is not a name — re-prompt if needed.

### Step 4 — surface human-owned decisions

Present the snapshot's `human_owned_decisions:` list:

- Confirm faithfulness to the customer's words.
- Decide whether to schedule a follow-up on any ambiguity flags (count them; list them).

Ask for explicit acknowledgement before advancing.

### Step 5 — lint the written artifact

Run `python3 <repo-root>/tools/lint-frontmatter.py <repo-root>/discovery/snapshots/<slug>.md`.

- **Exit 0:** proceed to Step 6.
- **Non-zero:** offer to re-open the relevant frontmatter fields for correction. If the human accepts and the corrections lint clean on re-run, proceed normally. If the human declines or re-runs but lint still fails, exit code 3 with the linter output surfaced; the file remains on disk for manual repair.

### Step 6 — emit the next-command hint

Last line of output: `NEXT: /extract-opportunities <today-or-batch-slug>`.

## What this command will not do

- Not persist a snapshot whose lint check fails.
- Not fabricate fields the transcript does not support (per the framework's three named fabrication patterns: invented diagnosis, emotion escalation, invented feature request).
- Not invent a timestamp when `--no-recording` is set. Use `[no recording]`.
- Not composite snapshots across two interviews — even of the same person.
- Not silently resolve ambiguity. Use the `[ambiguous: ...]` flag per the framework.
- Not overwrite an existing snapshot without `--force`.
- Not batch placeholder questions — one at a time.
- Not assume the working directory is the repo root when invoking the linter.
