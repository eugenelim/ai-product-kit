---
description: Writes the customer-shaped one-pager that crosses the Discovery → Validation handover boundary alongside the OST. Reads a parent OST whose chosen_opportunity is BOTH set AND resolves to an actual Opportunity node; refuses to draft otherwise (the kit's anti-prematurity guard at Handover 2). Walks five H2 sections one at a time (The customer / The pain / Why this, why now / What we're betting / Open questions for Validation) — cites at least one Direct Quote from a sourcing snapshot in the framework's exact format; never fabricates. Writes discovery/opportunities/narratives/<slug>.md. Lints. Emits NEXT /assumption-test (planned P3.1).
argument-hint: <slug> --from <ost-slug> [--force]
---

# /opportunity-narrative

> Artifact-creating Phase-2 command. Reads a parent OST with a resolved `chosen_opportunity:` and writes the customer-shaped one-pager at `discovery/opportunities/narratives/<slug>.md` — the narrative that crosses the Discovery → Validation handover boundary alongside the OST. Five H2 sections walked interactively; Direct Quotes cited from sourcing snapshots; anti-prematurity guard refuses to draft against an OST whose chosen Opportunity is unset or unresolved. Gates Handover 2 (Discovery → Validation) — the OST + narrative pair is what Validation consumes.

## When to run

- After `/update-ost` has set `chosen_opportunity:` on an OST AND the team is ready to translate the choice into a customer-shaped artifact for Validation.
- Before `/assumption-test` (planned — P3.1) — the Assumption Map's chosen-opportunity restatement reads from this narrative.
- When `/audit-discovery-coherence` returns `clean` with a NEXT pointing here (an OST has `chosen_opportunity:` set but no narrative exists yet).

## Inputs

1. The positional arg — `<slug>` (the new narrative's slug). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars.
2. `--from <ost-slug>` — required parent OST. Resolves to `<repo-root>/discovery/trees/<ost-slug>.md` AND its JSON projection at `<ost-slug>.json` (per Batch B's dual-write convention). The OST MUST satisfy **both** anti-prematurity conditions:
   - (a) `chosen_opportunity:` block is present and non-empty.
   - (b) `chosen_opportunity.id` resolves to an actual Opportunity node in the OST body (a `merge` or `delete` action via `/update-ost` may have invalidated a previously-set `chosen_opportunity.id`; this is the case `/audit-discovery-coherence`'s Rule 3 catches).
   If either condition fails, the command exits code 2 with a remediation message naming the failed condition and pointing at `/audit-discovery-coherence` (for diagnosis) or `/update-ost` (to re-set a valid chosen opportunity).
3. Optional `--force` — permits overwriting an existing narrative file. Does NOT bypass the anti-prematurity guard.
4. Read-only context surfaced during the walk: the chosen Opportunity's `evidence_basis:` snapshots (every `IS-<NNN>` snapshot's Goal / Workflow / Pain Points / Workarounds / Direct Quote fields), the OST's `outcome:`, the parent strategic intent's `central_challenge` and `guiding_policy`.

## Procedure

### Step 1 — resolve the parent OST and enforce the anti-prematurity guard

Resolve `<repo-root>` as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`.

Verify `<repo-root>/discovery/trees/<ost-slug>.md` exists. If missing, exit code 2 with: `"OST '<ost-slug>' not found under discovery/trees/ — pick an existing OST or run /generate-ost first."`

Parse the OST's frontmatter. **Anti-prematurity guard:**

- If `chosen_opportunity:` block is empty or missing entirely, exit code 2 with: `"OST '<ost-slug>' has no chosen_opportunity — Discovery has not converged on a single Opportunity to pursue. Run /update-ost <ost-slug> to set chosen_opportunity, then re-run /opportunity-narrative. See context/frameworks/opportunity-solution-tree.md §'The chosen one' for the framework's rationale on premature commitment."`
- If `chosen_opportunity.id` is set but does not resolve to an Opportunity node in the OST body (check both the H2 "Opportunity space" sub-tree AND the JSON projection's `nodes[]` if present), exit code 2 with: `"OST '<ost-slug>' has chosen_opportunity.id=<X> but no Opportunity node with that id exists in the tree body. The chosen Opportunity may have been merged/deleted by a prior /update-ost run. Run /audit-discovery-coherence <ost-slug> to diagnose, or /update-ost <ost-slug> to re-set chosen_opportunity to a valid id."`

The guard is hard — `--force` does NOT bypass it. A meaningful narrative requires a resolved chosen Opportunity.

### Step 2 — instantiate the narrative file

The destination is `<repo-root>/discovery/opportunities/narratives/<slug>.md`. If it exists and `--force` is not set, exit code 2 with: `"narrative '<slug>' already exists — re-run with --force to overwrite, or pick a different slug."`

Pre-fill mechanical frontmatter:

- `id: ONA-<NNN>` — scan `<repo-root>/discovery/opportunities/narratives/*.md` for `id: ONA-`; max + 1, zero-padded to three digits.
- `slug:` — positional argument.
- `object_type: Opportunity | Adapted` — kit-composite escape hatch (the H1 names it "Opportunity Narrative").
- `parent_ost:` — the resolved `--from` slug.
- `parent_opportunity:` — the OST's `chosen_opportunity.id`.
- `parent_intent:` — read from the OST's frontmatter (the OST already declared this).
- `created:`, `last_updated:` — today's ISO date.
- `status: Draft`.
- `human_owned_decisions:` — pre-fill with: "Confirm the narrative faithfully represents the snapshots' customer-voice content"; "Decide whether the riskiest assumption named in §'What we're betting' is the one Validation should test first".

### Step 3 — load context from the chosen Opportunity's snapshots

Read the chosen Opportunity's `evidence_basis:` list. For each `IS-<NNN>` reference, load `<repo-root>/discovery/snapshots/<slug>.md` where the file's `id:` matches. Collect the eight snapshot fields (Goal / Workflow / Pain Points / Workarounds / Tools / Direct Quote / Date / Interviewer) for each.

Surface to the human as read-only context before the walk: _"This narrative will draw on N snapshots (`IS-001`, `IS-014`, ...). I'll cite at least one Direct Quote in §'The pain' — review the loaded snapshots and confirm before we begin the walk."_

Ask for explicit acknowledgement that the snapshots' content is faithful (this is the first `human_owned_decisions:` checkpoint).

### Step 4 — walk the five H2 sections one at a time

Never batch. Confirm each section's content before advancing.

**H2 1 — The customer.** Ask: _"In one paragraph, narrative voice — who is the customer? Name the segment, the role, what they're trying to accomplish. Draw on the snapshots' Goal and Workflow fields. Do not generalize beyond what the snapshots support; if you only have one interviewee, say so explicitly."_

**H2 2 — The pain.** Ask: _"In one paragraph — what specifically is the customer hitting, in their words? Cite AT LEAST ONE Direct Quote from a sourcing snapshot in the framework's exact format: `\"<verbatim>\" — <Speaker Name>, <MM:SS>` (or `, [no recording]` if the snapshot uses the no-recording fallback). Do NOT fabricate a quote. If no Direct Quote is available across all sourcing snapshots, surface `[ambiguous: no-verbatim-quote-available]` and ask whether to ship with the marker or schedule a follow-up interview."_

**H2 3 — Why this, why now.** Ask: _"In one paragraph — what makes this Opportunity worth pursuing relative to the sibling Opportunities the OST surfaced? Cite the OST's `chosen_opportunity.rationale` verbatim if helpful, and (briefly) name one or two excluded sibling Opportunities — why they were considered and excluded. The framework's §'The chosen one' says the choice should be a *comparison*, not a default."_

**H2 4 — What we're betting.** Ask: _"In one paragraph — what is the riskiest assumption underneath this Opportunity? Frame informally (the formal Assumption Map is downstream in `/assumption-test` and `/design-experiment`); the point here is to prime Validation. Cite `context/frameworks/falsification.md` for the predeclared-threshold discipline — the bet will need a falsifier."_

**H2 5 — Open questions for Validation.** Ask: _"Bullet list — what does the team not yet know that the Validation phase will address? Each bullet is a candidate assumption for the Assumption Map (per Handover-2.5 in `docs/HANDOVERS.md`). Three to seven bullets is a good range — fewer and Validation may be undersourced; more and the team is likely conflating multiple distinct assumptions."_

### Step 5 — surface human-owned decisions

Re-present the `human_owned_decisions:` list and ask for explicit acknowledgement that each is owned:

- Confirm the narrative faithfully represents the snapshots' customer-voice content.
- Decide whether the riskiest assumption named in §"What we're betting" is the one Validation should test first.

Record acknowledgements in `approvals_obtained:` per the universal-metadata schema.

### Step 6 — lint the written artifact

Run `python3 <repo-root>/tools/lint-frontmatter.py <repo-root>/discovery/opportunities/narratives/<slug>.md`.

- Exit 0: proceed to Step 7.
- Non-zero: offer to re-open the relevant frontmatter or H2 sections for correction. If the human accepts and the corrections lint clean on re-run, proceed. If the human declines or re-runs still fail, exit code 3 with the linter output; the narrative stays on disk for manual repair.

### Step 7 — emit the next-command hint

Last line of output: `NEXT: /assumption-test <slug>` (planned — P3.1). The downstream `/assumption-test` command will consume this narrative as the chosen-opportunity restatement when seeding the Assumption Map.

## What this command will not do

- **Never draft a narrative against an OST without `chosen_opportunity:` set, OR against an OST whose `chosen_opportunity.id` doesn't resolve to a node in the tree body.** The anti-prematurity guard is hard; `--force` does not bypass it.
- **Never fabricate Direct Quotes.** If the chosen Opportunity's `evidence_basis:` snapshots have no Direct Quotes (e.g., no-recording fallback was used and no verbatim quote survives), surface `[ambiguous: no-verbatim-quote-available]` and let the human decide whether to ship with the marker or schedule a follow-up.
- **Never silently extrapolate beyond what the snapshots support.** If the snapshots only contain one interviewee's voice, the narrative must say so — don't pluralize "customers" when the evidence is one customer.
- **Never invoke `/audit-discovery-coherence`, `/update-ost`, or any other downstream command on behalf of the human.** The narrative is a draft; the human shares it (or runs the NEXT command).
- **Never overwrite an existing narrative without `--force`.**
- **Never batch placeholder questions — one section at a time.**
- **Never assume the working directory is the repo root when invoking the linter.**
