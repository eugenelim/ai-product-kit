---
description: Draft customer-facing release notes from a shipped Handoff Packet (default) or a Landing Report (`--from-landing`) — copies templates/release-notes.md to delivery/release-notes/<slug>.md, walks a customer-voice "what's new" paragraph plus 3-to-7 user-visible feature bullets one prompt at a time, pre-populates a human_owned_decisions entry that gates publication on a named human approving the claims, lints the written file, and chains to /launch-comms.
argument-hint: <slug> [--from-landing <landing-slug>] [--force]
---

# /release-notes

> Phase-4 post-ship comms-drafter (Wave-4, P4.12). Reads a Handoff Packet by default (or a Landing Report when `--from-landing` is passed); writes `delivery/release-notes/<slug>.md`; walks the customer-voice body one prompt at a time; surfaces the produced copy as a `human_owned_decisions:` item that gates publication; emits `NEXT: /launch-comms <slug>`. Customer-facing claims are HUMAN-AI-OWNERSHIP zone-3 — this command never auto-publishes, never invents metrics not in the parent's content, and never overrides the named decision owner. Deviates from the F4 template-fill convention on three named points (two parent families alternated by flag; output is a draft, not a finished artifact; NEXT enforces the zone-3 review through the human_owned_decisions entry rather than a separate review-prompt).

## When to run

- After a Handoff Packet has shipped (engineering has handed off and the change is rolling out or has rolled out) and you need a customer-facing release-note draft.
- After a Landing Report has been filed (`--from-landing <landing-slug>`) and you need a customer-facing post-ship recap drawing on adoption / outcome content rather than the original product brief.
- Before invoking `/launch-comms <slug>` if a single-audience customer release note is part of the launch comms set you'll route through `/launch-comms`.

## Inputs

1. The positional arg — `<slug>` (the new release note's slug). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars.
2. `templates/release-notes.md` — the F3 single-file template this command copies.
3. Parent artifact (default): a Handoff Packet folder at `delivery/handoff-packets/<parent-slug>/` whose `status:` is not `Deprecated`. Frontmatter read: `id`, `slug`, `parent_initiative`, `parent_vision`. The packet's `## Product brief` H2 (from `README.md`) and the files `features.md`, `success-metrics.md` are surfaced as read-only context during the walk.
4. Parent artifact (with `--from-landing <landing-slug>`): a Landing Report at `delivery/landings/<landing-slug>.md`. Frontmatter read: `id`, `slug`, `parent_vision`, `parent_handoff_packet`. The H2s `## The shipped change`, `## Predicted outcomes vs actuals`, `## What landed and what didn't` are surfaced as read-only context.
5. Optional flag `--from-landing <landing-slug>` — selects the Landing-Report parent path instead of the default Handoff-Packet path. Mutually exclusive with the default-parent resolution; only one parent family is active per invocation.
6. Optional flag `--force` — permits overwriting an existing `delivery/release-notes/<slug>.md`.
7. `tools/lint-frontmatter.py` — default-mode linter the command runs against the written artifact.

## Procedure

### Step 1 — resolve parent artifact

**Default (no `--from-landing`):** List candidates from `delivery/handoff-packets/` filtered by `status:` not in `{Deprecated}`, sorted by `last_updated:` descending, capped at 10. Present as a numbered list; ask the human to pick one. **Never silently pick — always confirm, even when only one candidate exists.** If the candidate list is empty, exit code 2 with: `"no Handoff Packet found in delivery/handoff-packets/ — run /handoff-packet <slug> first."`.

**With `--from-landing <landing-slug>`:** Validate `delivery/landings/<landing-slug>.md` exists and its `verdict:` frontmatter is set (i.e., not still placeholder-shaped). If not, exit code 2 with the missing pre-condition named. Confirm the selected landing with the human even though it was explicit.

Surface the resolved parent's `parent_initiative:` and `parent_vision:` to the human; if either is missing in the parent's frontmatter, warn (one line) — the corresponding output field will be omitted from the written file, and the human may want to abort and fix the parent before continuing.

### Step 2 — instantiate the template at the destination

Copy `templates/release-notes.md` to `delivery/release-notes/<slug>.md`. If the destination exists and `--force` is not set, exit code 2: `"delivery/release-notes/<slug>.md already exists — re-run with --force or pick a different slug."`. If the `delivery/release-notes/` directory does not exist, create it (`mkdir -p`).

Pre-fill the mechanical frontmatter (the human is never asked for these):

- `id: RN-<NNN>` — scan `delivery/release-notes/*.md` for `id: RN-` lines, take max + 1, zero-pad to three digits (or `001` if none exist).
- `slug:` — the positional argument.
- `object_type: Customer Communication` — re-assert (template pre-fills).
- `status: Draft` — re-assert.
- `created:` — today's date (ISO-8601, system clock at command start).
- `last_updated:` — same as `created`.
- `parent_handoff_packet:` (default parent) **or** `parent_landing:` (when `--from-landing` is set) — the resolved parent slug. The other field is removed from frontmatter (not left as a placeholder).
- `parent_initiative:`, `parent_vision:` — transitive carry-through from the parent's frontmatter, if present; omit the field entirely if missing.
- `ai_assistance_used`, `ai_assistance_allowed: restricted`, `human_approval_required: true` — re-assert (template pre-fills).
- `human_owned_decisions:` — re-assert the canonical entry: "Approval of customer-facing claims in the draft body before publication". The human may add additional zone-3 entries during Step 4.

### Step 3 — walk the body one section at a time

For each H2 in the template body, ask one question per turn, never batched. Confirm each section's filled content before advancing.

- **`## What's new` (one prompt + one confirmation):** _"In one paragraph, what's new for the customer in this release? Write in customer voice — name what they can now do that they couldn't before. The product brief from the parent says: '<one-sentence quote from parent>'. Reply with your paragraph, or 'show' to see the full parent context first."_ After the paragraph is supplied, echo it back and ask: _"Does this paragraph speak to the customer as the customer would describe the change? Confirm or revise."_
- **`## Features in this release` (loop until 3-to-7 collected, then confirmation):**
  - _"Name the next user-visible feature in this release, in one short line of customer voice. (Already collected: <N>. Need 3-to-7 total. Reply 'done' when finished, or 'show' to see the parent's features.md / success-metrics.md.)"_
  - **Jargon heuristic.** If the supplied bullet (case-insensitive) contains any of: `kubernetes`, `microservice`, `microservices`, `feature flag`, `feature-flag`, `rollout %`, `canary`, `dogfood`, `internal-only`, `internal only`, `eng-only`, `eng only`, `mvp` — ask: _"That bullet contains '<token>', which reads as internal jargon. Confirm or rewrite in customer voice."_ Non-blocking; the human always overrides.
  - When the human says `done` with ≥ 3 bullets: echo the list and ask: _"Confirm this is the user-visible feature list as the customer would see it. Confirm or revise."_
  - If the human says `done` with < 3 bullets: refuse to advance; prompt for more.
- **`## Known limitations` (one opt-in prompt, then per-bullet loop if opted-in):**
  - _"Does this release have known limitations the customer should be told about up front? (yes/no — replying 'no' deletes this optional section from the file.)"_
  - If yes: per-bullet loop until `done`. If no: delete the H2 and its placeholder from the written file.

### Step 4 — surface human-owned decisions

Read the written file's `human_owned_decisions:` list (pre-filled per Step 2). For the canonical entry: _"The pre-populated human-owned decision is: 'Approval of customer-facing claims in the draft body before publication'. Name the human (role and name) who will own this approval, in the form '<role>: <name>'."_

Ask whether additional zone-3 decisions apply to this release (pricing changes, customer commitments, regulatory claims). Add entries one at a time. Record confirmations under `approvals_obtained:` in `<role>: <YYYY-MM-DD>` form.

### Step 5 — lint the written artifact

Resolve repo root as the nearest ancestor of CWD containing `tools/lint-frontmatter.py`; do not assume CWD is the repo root. Run `python3 <repo-root>/tools/lint-frontmatter.py delivery/release-notes/<slug>.md` (default mode).

- Exit 0: proceed to Step 6.
- Non-zero: surface the linter output; offer to re-open the relevant sections for correction. If the human accepts and the re-lint exits 0, proceed normally. If the human declines (or re-lint still fails), exit code 3.

### Step 6 — emit the final summary and NEXT line

Echo: the resolved parent, the produced `## What's new` paragraph, the produced `## Features in this release` bullets, the produced `## Known limitations` bullets (if any), the `human_owned_decisions:` list with confirmed owners, and the destination path. Remind the named approver that the customer-facing claims must be reviewed (not the command's responsibility to enforce — the human_owned_decisions entry is the load-bearing gate).

Last line of output, formatted exactly:

```
NEXT: /launch-comms <slug>
```

The customer-facing-copy zone-3 review is a precondition for *publication*, enforced by the `human_owned_decisions:` entry — not by the NEXT line. The human runs `/launch-comms` next to assemble the broader launch comms set; `/launch-comms` does not read this file. No `REVIEW:` line is emitted.

## Exit codes

- `0` — release notes written, linter passed, human_owned_decisions confirmed, NEXT emitted.
- `1` — human aborted the interactive walk before Step 5 completed. Partial release-notes file left on disk. Resume by re-running with the same `<slug>` plus `--force`.
- `2` — pre-conditions failed: slug malformed; destination exists without `--force`; candidate Handoff-Packet list empty; `--from-landing <landing-slug>` named a missing or verdict-unset landing report; `templates/release-notes.md` missing.
- `3` — file written but post-fill linter exited non-zero and human declined re-open. File persists on disk in known-imperfect state.

## What this command will not do

- Not auto-publish the draft to any external surface. No CMS, blog, email, social, or status-page integration. The command writes a file and exits; publication is a separately-owned human workflow gated by the `human_owned_decisions:` approval.
- Not accept internal jargon without prompting. The jargon heuristic surfaces a confirmation; the human always overrides.
- Not invent metrics not in the parent's content. If the human asks for a benefit, claim, or number not present in the parent Handoff Packet (or, with `--from-landing`, the Landing Report), refuse and ask the human to source it.
- Not modify the parent Handoff Packet or Landing Report. Both are read-only at invocation time.
- Not modify `templates/release-notes.md`. The template is frozen by this command's spec.
- Not overwrite an existing release-notes file without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not batch placeholder questions — one at a time, sequentially.
- Not silently pick a parent when multiple candidates exist (or when only one exists — always confirm).
- Not assume the working directory is the repo root when invoking the linter.
- Not chain to `/audit-completeness`, `/audit-traceability`, or any other audit. Post-ship comms have no canonical audit gate.
- Not produce multi-language drafts. Single-language only.

$ARGUMENTS
