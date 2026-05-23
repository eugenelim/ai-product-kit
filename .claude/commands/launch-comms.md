---
description: Draft per-audience launch communications from a shipped Handoff Packet — copies templates/launch-comms/{internal,blog,email}.md to delivery/launch-comms/<slug>/, walks each audience's prompt set one question at a time (internal: on-call/runbook/kill-switch; blog: headline/benefit/segment/CTA; email: subject-first/preview/short body), produces audience-distinct copy (never undifferentiated), pre-populates customer-facing-copy-approval human_owned_decisions, lints each written file, and chains to /launch-checklist.
argument-hint: <slug> [--audience internal|external|email|blog|all] [--from <handoff-packet-slug>] [--force]
---

# /launch-comms

> Phase-4 post-ship comms-drafter (Wave-4, P4.13). Reads an existing Handoff Packet (HANDOVERS-6) — particularly `launch-considerations.md` §"Communications and rollout" — and writes audience-distinct drafts at `delivery/launch-comms/<slug>/{internal.md, blog.md, email.md}`. Each audience has its own prompt set; the per-file H2 asymmetry (internal has `## Kill-switch`; blog has `## Headline`; email has `## Subject line`) is the mechanical encoding of the audience-distinct contract. Customer-facing drafts (`blog.md`, `email.md`) are HUMAN-AI-OWNERSHIP zone-3 — the customer-facing-copy approval is a pre-populated `human_owned_decisions:` entry the human must own before publication. The command never auto-publishes, never fabricates metrics not in the parent packet, and never produces undifferentiated copy. Deviates from the F4 template-fill convention on three named points (output is a folder of interactively-filled siblings; parent is a Handoff Packet rather than an Initiative; output is post-ship human-facing copy whose audience-distinct voice is a semantic-not-syntactic check).

## When to run

- After the parent Handoff Packet's `engineering_review_passed:` date is filled (i.e., the packet is sealed for engineering) AND the rollout phase is decided in `launch-considerations.md` §"Communications and rollout" (e.g., "10% rollout to US-only at T+0; 100% at T+14d"). Running earlier risks the drafts being stale at publish time.
- After `/release-notes <slug>` has produced the customer release-note draft (the NEXT chain from P4.12 lands here); `/launch-comms` does NOT read the release-notes file but the human now has a customer-voice baseline.
- Before `/launch-checklist <slug>` (P4.14) clears the operational gate; the comms are drafted in parallel with the operational walkthrough so both surfaces are ready when the launch lever is pulled.

## Inputs

1. The positional arg — `<slug>` (the launch-comms folder slug; typically the same as the parent Handoff Packet's slug for traceability; the human chooses). Kebab-case, `^[a-z0-9-]+$`, ≤ 80 chars.
2. Optional flag `--audience <internal|external|email|blog|all>` — scopes which audience drafts the command walks and writes. Default: `all` (walks internal → blog → email in that order). Aliases: `--audience external` ≡ `--audience blog`.
3. Optional flag `--from <handoff-packet-slug>` — explicit selection of the parent Handoff Packet. Without it, the command lists candidates and asks.
4. Optional flag `--force` — permits overwriting an existing audience draft at the destination (per-file semantics — see Step 2).
5. `templates/launch-comms/` — the folder template this command consumes. Three children: `internal.md`, `blog.md`, `email.md`. Each carries universal-schema frontmatter plus audience-specific H2 sections.
6. Parent artifact: a Handoff Packet at `delivery/handoff-packets/<handoff-packet-slug>/` whose `status:` is not `Deprecated`. Read: `README.md` (`id`, `slug`, `parent_initiative`, the `## Product brief` paragraph), `launch-considerations.md` §"Communications and rollout" (substantive content for internal-team announcement), `customer-segment.md` (segment targeting in blog and email), `success-metrics.md` (KPI claims; fabrication forbidden — only metrics in this file may be referenced).
7. `tools/lint-frontmatter.py` — default-mode linter run against each written audience draft.

## Procedure

### Step 1 — resolve parent Handoff Packet

If `--from <handoff-packet-slug>` is given, validate `delivery/handoff-packets/<handoff-packet-slug>/` exists with `status:` not `Deprecated`. If not, exit code 2: `"no Handoff Packet found at delivery/handoff-packets/<handoff-packet-slug>/ — run /handoff-packet <slug> first, then /audit-completeness <slug>, then re-run /launch-comms."`

Otherwise list candidates from `delivery/handoff-packets/` whose `status:` is not `Deprecated`, sorted by `last_updated:` descending, capped at 10. Present as a numbered list; ask the human to pick one. **Never silently pick — always confirm, even when only one candidate exists.** If the list is empty, exit code 2: `"no Handoff Packet found in delivery/handoff-packets/ — run /handoff-packet <slug> first."`

### Step 2 — instantiate the audience folder

Create `delivery/launch-comms/<slug>/` (`mkdir -p` — creates the family directory `delivery/launch-comms/` on first invocation). Determine the audience scope from `--audience`:
- `all` (default) — operate on internal, blog, email (in that order).
- `internal` / `blog` / `email` / `external` (alias for blog) — operate on the single named audience.

For each audience in scope: if `delivery/launch-comms/<slug>/<audience>.md` already exists and `--force` is not set, the existing sibling is **left untouched** and the audience is skipped with a one-line warning. (Per-file overwrite contract: a `--audience internal` invocation on Tuesday and `--audience blog` on Wednesday leaves Tuesday's `internal.md` untouched on Wednesday; only `--force` overwrites. The folder is **not** atomically replaced — each audience file has its own overwrite gate.)

**Before overwriting a customer-facing audience draft (`blog.md` or `email.md`) with `--force`**, read the existing file's `approvals_obtained:` frontmatter. If any entry has a concrete date (not the angle-bracket placeholder), echo the list to the human and ask: _"Confirm overwrite? The above approval records (Marketing/Legal/Compliance sign-off dates) will be lost."_ Refuse on `no`; proceed on `yes`. The `internal.md` audience is exempt from this guard — its `approvals_obtained:` is operational (runbook-accuracy, kill-switch sign-off), not customer-facing zone-3 sign-off. Silent destruction of customer-facing approvals is forbidden per HUMAN-AI-OWNERSHIP.

For each audience in scope that is not skipped: copy `templates/launch-comms/<audience>.md` to `delivery/launch-comms/<slug>/<audience>.md`. Pre-fill the mechanical frontmatter:

- `id: LC-<NNN>` — scan `delivery/launch-comms/*/*.md` for `id: LC-` lines, take max + 1, zero-pad to three digits (or `001` if none). Each audience draft gets its own sequential id.
- `slug:` — the positional argument plus an audience suffix (`<slug>-internal`, `<slug>-blog`, `<slug>-email`).
- `created:`, `last_updated:` — today's date (ISO-8601, system clock at command start).
- `parent_handoff_packet:` — the resolved Handoff Packet slug.
- `parent_initiative:` — read from the parent packet's `README.md` frontmatter; carry through.
- `audience:` — re-assert per template (`internal-team` / `external-blog` / `customer-email`).
- `object_type: Launch Communication` — re-assert per template.
- `status: Draft` — re-assert.

### Step 3 — walk the audience-distinct prompts (one at a time, never batched)

For each audience in scope, walk that audience's prompt set sequentially. One question per turn. Confirm each answer before advancing. After the last prompt for an audience, echo the assembled draft and ask: _"Does this <audience-name> draft read in the right voice for its audience? Confirm or revise."_ A `revise` response replays the audience's walk; `confirm` advances to the next audience.

**Internal-team announcement (`internal.md`) — 4 prompts:**

1. _"What shipped, in one paragraph for an internal-team audience? Name the product behaviour and the rollout phase (e.g., '10% rollout to US-only at T+0; 100% at T+14d')."_
2. _"Who owns this at launch? List the on-call rotation, the runbook link, and the escalation path. The parent packet's `launch-considerations.md` §'Communications and rollout' should already name these; copy through if so."_
3. _"What is the kill-switch / rollback plan if something breaks? Quote the parent packet's plan verbatim if one exists; otherwise stop — kill-switch is required for any internal-team launch announcement."_
4. _"What internal questions are anticipated? List 3–6 question / answer pairs. Focus on operational concerns (load, dependencies, on-call burden), not customer-facing FAQ."_

**External blog post (`blog.md`) — 5 prompts:**

1. _"Write the headline. One sentence, customer-facing claim. Voice: direct address ('you'), not internal ('we shipped'). The headline is the load-bearing copy unit; spend the time."_
2. _"Write the opening paragraph for `## What this means for you`. Lead with the customer benefit, not the internal capability. Voice: second person."_
3. _"Describe how the feature works in plain language. 2–3 sentences. Where would a screenshot go? Insert `![placeholder]` marker; the human attaches the actual image post-walk."_
4. _"Who is this for? Reference the customer segment from the parent packet's `customer-segment.md`. Direct quote or paraphrase allowed; do NOT fabricate a segment that isn't in the packet."_
5. _"What is the single primary CTA? Provide the link and the action verb (e.g., 'Get started in the dashboard'). One CTA — no secondary actions."_

**Customer email (`email.md`) — 4 prompts (subject-first, per email-copywriting discipline):**

1. _"Write the subject line. ≤ 60 chars. The subject is what gets opened; everything else is downstream. Confirm character count before advancing."_ (The command computes and echoes the char count.)
2. _"Write the preview text. ≤ 90 chars. This is the snippet that appears in the inbox between subject and body in most clients."_
3. _"Write the email body. Three short paragraphs maximum. One opening sentence ('here's what's new'); one benefit paragraph linking to the blog post you just drafted; one closing sentence with the CTA."_
4. _"Write the call to action. One line. MUST match the `Get started` CTA in `blog.md` for cross-channel consistency — paste it through. The command will not auto-link; you confirm the match."_

### Step 4 — surface human-owned decisions per audience

For each written audience draft, surface the `human_owned_decisions:` list (pre-populated by the template). For customer-facing drafts (`blog.md`, `email.md`), the canonical entries include:

- "Customer-facing copy approval (this draft will not be published without a named approver's sign-off)."
- "Headline / subject-line factual accuracy (no claim outside the parent Handoff Packet's verified content)."
- "Marketing / Legal / Compliance review status (none of these reviews are run by this command; the human routes the draft to the named reviewer)."

For the internal draft, the canonical entries include:

- "Runbook accuracy (the on-call rotation and runbook link are verified by the named engineering owner)."
- "Kill-switch / rollback plan accuracy (verbatim copy through from the parent packet, or a named owner has approved a divergence)."

Ask the human to name a human owner per entry. Record under `approvals_obtained:` as `<role>: <YYYY-MM-DD>`. **The command will not auto-publish, auto-send, or auto-link any draft to any publishing surface.**

### Step 5 — lint each written audience draft

For each written audience draft, run `python3 <repo-root>/tools/lint-frontmatter.py <written-path>` (default mode). Resolve repo root as nearest ancestor of CWD containing `tools/lint-frontmatter.py`.

- All exit 0: proceed to Step 6.
- Any non-zero: surface the linter output for that file; offer to re-open relevant sections. If the human accepts and the re-lint exits 0, proceed; otherwise exit code 3 with the linter output surfaced and the folder persisting in known-imperfect state.

### Step 6 — emit the next-command hint

Echo a summary: per-audience destination paths, the `human_owned_decisions:` lists with named owners, the per-file `approvals_obtained:` entries.

Last line of output, formatted exactly:

```
NEXT: /launch-checklist <slug>
```

If `/launch-checklist` (P4.14) has not yet shipped at command-run time, append the kit-drift annotation: `NEXT: /launch-checklist <slug> (planned — ROADMAP P4.14)`.

No `REVIEW:` line is emitted.

## Exit codes

- `0` — folder instantiated, all audience drafts in scope walked and filled, all written files linted clean, NEXT emitted.
- `1` — human aborted mid-walk before Step 5. Partial folder left on disk; confirmed audience drafts are persisted, the in-progress audience is at its last-confirmed state. Resume by re-running with the same `<slug>` and `--audience` scope plus `--force`.
- `2` — pre-conditions failed: slug malformed; `--audience` value invalid; `--from <handoff-packet-slug>` named a missing or `Deprecated` packet; candidate packet list empty; `templates/launch-comms/` missing.
- `3` — folder written but one or more audience drafts failed default-mode lint and the human declined re-open (or re-lint still failed). Folder persists on disk in known-imperfect state.

## What this command will not do

- Not produce undifferentiated copy across the three audience files. The audience-distinct voice / length / concerns contract is load-bearing; the per-audience prompt sets and H2 asymmetry are the mechanical encoding. An executor that paraphrases the same paragraph three times fails the manual-gesture review.
- Not auto-publish, auto-send, auto-post, or auto-link any audience draft to any publishing surface (CMS, email-sending platform, social network, Slack).
- Not fabricate metrics, customer quotes, segment definitions, KPIs, or claims not already present in the parent Handoff Packet. If the human asks for a number that isn't in the packet, ask which source it came from and require a citation before allowing it into a customer-facing draft.
- Not fill `blog.md` or `email.md` without surfacing the customer-facing-copy-approval `human_owned_decisions:` entry. Customer-facing claims are HUMAN-AI-OWNERSHIP zone-3 — AI must never be the final owner.
- Not modify `templates/launch-comms/` at runtime. The templates are frozen by this command's spec.
- Not add a new ontology type at runtime. `Launch Communication` is added by the spec's ontology extension (P4.13 EXECUTE phase); ad-hoc additions are forbidden.
- Not write the folder under `delivery/handoff-packets/<slug>/launch-comms/` (Option B). Destination is `delivery/launch-comms/<slug>/` (Option A) per the spec's destination resolution.
- Not silently pick a parent Handoff Packet when multiple candidates exist (or when only one exists — always confirm).
- Not overwrite an existing audience draft — sibling drafts are **left untouched** by subsequent `--audience <other>` runs unless `--force` is passed (per-file overwrite contract).
- Not silently overwrite a customer-facing audience draft (`blog.md` / `email.md`) carrying concrete `approvals_obtained:` entries when `--force` is passed — first echo the existing approvals and require explicit human confirmation. Operational drafts (`internal.md`) are exempt.
- Not skip the `human_owned_decisions:` confirmation step.
- Not batch placeholder questions — one at a time, sequentially.
- Not assume the working directory is the repo root when invoking the linter.
- Not run a voice-check, sentiment, or readability check. `voice-check` is planned (ROADMAP P8.4); not consumed here.
- Not auto-translate drafts into other languages.

$ARGUMENTS
