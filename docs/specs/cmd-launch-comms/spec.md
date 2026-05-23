# Spec: cmd-launch-comms

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command (Phase-4 post-ship, comms-drafter, multi-audience — folder output) + template-folder (`templates/launch-comms/` with three audience-specific children)
- **Serves kit phase:** Delivery (post-ship comms; consumes Handover 6 Handoff-Packet content, specifically `launch-considerations.md` §"Communications and rollout")
- **Constrained by:** [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Phase-4 Template-Fill Commands" (partial-fit — see §"Convention applicability" below); [`docs/HANDOVERS.md`](../../HANDOVERS.md) §"Handover 6" (the upstream Handoff Packet supplies the substantive content); [`.claude/commands/_meta/command-skeleton.md`](../../../.claude/commands/_meta/command-skeleton.md) (skeleton, with declared deviations); [`templates/handoff-packet/launch-considerations.md`](../../../templates/handoff-packet/launch-considerations.md) (sibling F3.9 child — the §"Communications and rollout" sub-section is this command's primary substantive input); [`.claude/commands/handoff-packet.md`](../../../.claude/commands/handoff-packet.md) (P4.11 sibling — folder-template precedent for a command that ships its own multi-child template directory); [`.claude/commands/draft-spec.md`](../../../.claude/commands/draft-spec.md) (P4.8 sibling — single-file template-fill precedent); [`docs/HUMAN-AI-OWNERSHIP.md`](../../HUMAN-AI-OWNERSHIP.md) ("customer-facing claims" is named as an area AI must never be the final owner); ROADMAP P4.13.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `.claude/commands/launch-comms.md` plus `templates/launch-comms/{internal.md, blog.md, email.md}` — a Phase-4 comms-drafter that reads an existing Handoff Packet (HANDOVERS-6, post-engineering-handoff, typically post-ship), walks the human through three audience-distinct interactive prompt sets, and writes audience-distinct drafts at `delivery/launch-comms/<slug>/{internal.md, blog.md, email.md}`. The command MUST produce per-audience-differentiated copy (different voice, length, and concerns per audience) — NOT one undifferentiated draft labelled three ways. Customer-facing drafts (`blog.md`, `email.md`) are surfaced as `human_owned_decisions:` per [`docs/HUMAN-AI-OWNERSHIP.md`](../../HUMAN-AI-OWNERSHIP.md); the command never auto-publishes and never fabricates metrics, customer quotes, or claims not already present in the parent Handoff Packet.

## Objective

`/launch-comms <slug> [--audience internal|external|email|blog|all]` is the slash command that turns a shipped feature's Handoff Packet (or one at-or-after its named ship date, once the rollout phase is decided) into the three launch-communication drafts a typical product launch requires: an internal-team announcement (operational, runbook-aware, on-call-aware), an external blog post (customer-benefit-led, narrative, ungated), and a customer email (subject line + one-action CTA, short). The command is most effective once the parent Handoff Packet's `engineering_review_passed:` date is filled and `launch-considerations.md` §"Communications and rollout" names the rollout phase (e.g., "10% rollout to US-only at T+0; 100% at T+14d"); running earlier risks the drafts being stale at publish time. Today, a kit user wanting these three drafts assembled would either (a) hand the Handoff Packet's `launch-considerations.md` §"Communications and rollout" sub-section to a generic LLM and accept undifferentiated copy, or (b) draft each audience by hand against the packet's structured content. This command collapses that work into one interactive walk that produces three audience-distinct files, each anchored to the packet's substantive content (business objective, customer segment, success metrics, rollout phasing, kill-switch) so no audience draft fabricates evidence the packet does not already supply.

The closest prior context is `.claude/commands/handoff-packet.md` (P4.11 — the folder-template-shipping sibling whose pattern this command extends; `/handoff-packet` ships a 23-child template, `/launch-comms` ships a 3-child template) and `.claude/commands/draft-spec.md` (P4.8 — the single-file template-fill sibling whose interactive-walk discipline this command inherits). `/launch-comms` is the first Phase-4 command whose output is **post-ship product communication**, not a pre-engineering structural artifact; the audience-distinct-output contract is the load-bearing differentiator.

## Why now

ROADMAP P4.13 sits in the Phase-4 post-ship-commands block alongside P4.12 `/release-notes`, P4.14 `/launch-checklist`, P4.15 `/retro`. The upstream dependency — F3.9 `templates/handoff-packet/launch-considerations.md` — shipped 2026-05-22, so the substantive input surface is stable. The Handover-6 contract is finalised in `docs/HANDOVERS.md`. The Phase-4 template-fill command convention shipped 2026-05-23 (P4.10), so the per-command body shape is locked. Until P4.13 ships, kit users have a structured Handoff Packet but no kit-native way to turn its launch sub-section into the three audience drafts every real launch needs; the work falls outside the kit's interactive-walk discipline and produces undifferentiated copy that conflates audiences (the typical failure mode — "internal-comms voice on a customer email").

P4.13 is also the kit's first commitment to **audience-distinct output** as a first-class contract. The audience-distinct rule (different voice / length / concerns per file) is restated in the spec's Boundaries → Never do and gated by a manual-gesture check at REVIEW phase; the rule becomes a transferable constraint that other Phase-4 comms-drafter commands (release-notes, launch-checklist) may inherit.

## Convention applicability

`docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands" was authored for the seven Phase-4 *template-fill* commands (the four artifact-creating and three artifact-augmenting variants — `/draft-vision`, `/draft-initiative`, `/draft-spec`, `/handoff-packet`, `/context-map`, `/end-to-end-flow`, `/sequence-initiative`). `/launch-comms` is a **partial-fit case**: it shares the convention's interactivity discipline (one question at a time; never batch), parent-resolution discipline (candidate list from a family directory, never auto-pick), pre-fill discipline (mechanical frontmatter fields filled before prompting), linter integration (default-mode `tools/lint-frontmatter.py` against each written file), and exit-code contract (0/1/2/3 with the same semantics). It **deviates** from the convention in three named ways, declared here so an executor can recognise the divergence rather than re-deriving it:

1. **Output shape — folder of three audience-distinct files, not a single artifact or a single folder-template.** The convention's two sub-classes are "one new artifact at a new destination path" (creating) and "fill one child file inside an existing folder" (augmenting). `/launch-comms` writes a *folder of three sibling drafts*, each authored by a different audience-scoped prompt set. The closest convention precedent is `/handoff-packet` (which ships a 23-child folder) — but `/handoff-packet`'s 22 children are copied verbatim as placeholders, whereas `/launch-comms`' three children are each interactively filled in the same command invocation. This makes `/launch-comms` simultaneously "creating" (the destination folder did not exist) and "interactive-walking three sibling files" (each is filled, none is left as a placeholder).

2. **Parent artifact is a Handoff Packet, not an Initiative / Vision / Learning Memo.** The convention's parent-resolution rule names the upstream family by handover number; `/launch-comms`' upstream is HANDOVERS-6 (Handoff Packet), which is downstream of every parent the existing seven commands resolve against. The parent-resolution mechanics are identical (candidate list from `delivery/handoff-packets/` filtered by `status:` not `Deprecated`); only the family directory differs.

3. **Output is post-ship product communication.** The convention's seven commands produce pre-engineering structural artifacts whose linter contract is "default-mode `tools/lint-frontmatter.py` plus universal-schema frontmatter." `/launch-comms`' three outputs carry universal-schema frontmatter (so the default-mode linter applies) but the *body* is human-facing copy, not structured kit content. The audience-distinct-body contract (§"Per-audience differentiation" below) is the load-bearing semantic check; the linter only gates frontmatter shape, not body voice.

The deviation set is declared verbatim in `.claude/commands/launch-comms.md`'s opening blockquote and in this spec's `Constrained by:` line above.

## Inputs and outputs

**Inputs.**

1. Positional argument `<slug>` — kebab-case identifier matching `^[a-z0-9-]+$`, ≤ 80 chars, naming the launch-comms folder (typically the same as the parent Handoff Packet's slug for traceability; the human chooses).
2. Optional flag `--audience <internal|external|email|blog|all>` — scopes which audience drafts the command walks and writes. Default: `all` (walks all three audiences in sequence). Aliases: `--audience external` is a synonym for `--audience blog`. The flag is a scope filter, not a content switch; the audience-distinct prompts per audience are fixed by this spec.
3. `templates/launch-comms/` — the folder template this command consumes (ships under this same spec). Contains `internal.md`, `blog.md`, `email.md` — each with audience-specific H2 sections and per-section prompts. See §"Inputs and outputs (template files)" for the verbatim section list.
4. Parent artifact: a Handoff Packet at `delivery/handoff-packets/<handoff-packet-slug>/` whose `status:` is not `Deprecated`. Resolution rule follows the convention's "Parent-artifact resolution" sub-section (`--from <handoff-packet-slug>` for explicit selection; candidate list from `delivery/handoff-packets/` sorted by `last_updated:` descending, capped at 10; never silently pick).
5. The parent Handoff Packet's `launch-considerations.md` §"Communications and rollout" sub-section — the substantive content the human will be asked to translate into per-audience drafts. Also read: parent Handoff Packet's `README.md` (for the Product brief paragraph), `customer-segment.md` (for audience targeting in `blog.md` and `email.md`), `success-metrics.md` (for KPI claims the human may or may not include in the blog post — fabrication is forbidden; only KPIs already named in the packet may be referenced).
6. Optional flag `--force` — permits overwriting an existing `delivery/launch-comms/<slug>/` folder.
7. `tools/lint-frontmatter.py` — default-mode linter the command runs against each written audience draft.

**Outputs.**

1. `.claude/commands/launch-comms.md` — the new slash-command file. Frontmatter declares `description:` (one sentence ≤ 1024 chars) and `argument-hint:` set to `<slug> [--audience internal|external|email|blog|all] [--from <handoff-packet-slug>] [--force]`. Body follows the command skeleton with three declared deviations (§"Convention applicability" above).
2. `templates/launch-comms/` — the new folder template. Three children: `internal.md`, `blog.md`, `email.md`. Each child carries universal-schema frontmatter (including `object_type:` — see §"Open questions" #2) and audience-specific H2 sections.
3. `delivery/launch-comms/<slug>/` — the command's runtime output. Three files per the audience filter: `internal.md`, `blog.md`, `email.md` (with `--audience all`), or a subset per `--audience <name>`. Each file's frontmatter is pre-filled mechanically; each file's body is filled by the human via the interactive walk.
4. Stdout — the interactive walk's prompts and confirmations, per-file linter reports, plus the chain hint. Last line is exactly `NEXT: /launch-checklist <slug>` (with `(planned — ROADMAP P4.14)` suffix if P4.14 is unshipped at command-run time, per kit-drift policy).
5. Exit code — one of `0` (success), `1` (human aborted mid-walk), `2` (pre-conditions failed), `3` (lint failed on one or more written files and human declined re-open). See §"Exit codes" below.

A reader of this section can construct the command's interface signature without reading anything else.

## Destination path resolution

Two candidates were considered:

- **(A) Top-level family — `delivery/launch-comms/<slug>/{internal.md, blog.md, email.md}`.** Symmetric to `delivery/handoff-packets/`, `delivery/initiatives/`, `delivery/visions/`. New top-level family under `delivery/`.
- **(B) Nested under the Handoff Packet — `delivery/handoff-packets/<slug>/launch-comms/{internal.md, ...}`.** Sub-folder inside the packet.

**Chosen: (A) — `delivery/launch-comms/<slug>/`.** Three reasons:

1. **Lifecycle decoupling.** The Handoff Packet's lifecycle freezes at `status: Ready for Engineering` once `/audit-completeness` and the named reviewer subagents pass; the four `*_review_passed:` audit-gate fields flip to concrete dates and the packet becomes a read-only historical artifact. Launch comms are authored *after* the packet freezes (typically on or near ship date, sometimes weeks later), and may be revised after ship. Nesting comms under a frozen folder mixes two lifecycle phases inside one directory — the packet's "frozen, audit-gated" semantics would have to be relaxed to permit comms edits, which silently violates the packet's freeze contract.
2. **Convention symmetry.** Every other Phase-4 destination is a top-level family under `delivery/`. Option B would introduce a "sub-family inside a family" pattern with no other precedent; the kit's source-of-truth table in `AGENTS.md` would gain an asymmetric row.
3. **Discoverability.** Kit users browsing `delivery/` would find launch-comms as a sibling to handoff-packets and initiatives; under Option B, they would have to know to descend into a specific packet to find them.

The trade-off accepted: the comms folder's `parent_handoff_packet:` frontmatter field carries the traceability that the directory nesting would have made visual. The `audit-traceability` skill (Phase-5 entry) can verify the link mechanically; visual proximity is not required.

The new top-level directory `delivery/launch-comms/` is created on first command invocation (via `mkdir -p`); the family directory's own README is not introduced by this spec (open question 4 — defer until adopters request it).

## Inputs and outputs (template files)

**`templates/launch-comms/internal.md`** ships with:

- Frontmatter: `object_type: Launch Communication` (proposed — see open question 2), `audience: internal-team`, `parent_handoff_packet: <placeholder>`, plus the universal-schema base.
- H2 sections (in source order, all required):
  - `## What shipped` — one paragraph naming the product behaviour and the rollout phase.
  - `## Who owns what at launch` — explicit table of on-call rotations, runbook link, escalation paths.
  - `## Kill-switch and rollback plan` — verbatim text the engineer-on-call can read and act on; pulled from the parent packet's `launch-considerations.md` §"Communications and rollout" sub-section.
  - `## Internal FAQ` — anticipated internal questions and answers (typically 3–6).
  - `## Talking points for customer-facing teams` — short bullet list sales / support / CSM can use *internally* (the customer-facing version lives in `blog.md` and `email.md`).

**`templates/launch-comms/blog.md`** ships with:

- Frontmatter: `object_type: Launch Communication` (proposed), `audience: external-blog`, `parent_handoff_packet: <placeholder>`, plus the universal-schema base.
- H2 sections:
  - `## Headline` — one sentence customer-facing claim (the load-bearing copy unit; never auto-generated).
  - `## What this means for you` — customer-benefit-led opening paragraph; voice is direct address ("you"), not internal ("we shipped").
  - `## How it works` — one screenshot beat (placeholder for image link) + 2–3 sentences of plain-language behaviour description.
  - `## Who this is for` — short paragraph naming the customer segment from the packet's `customer-segment.md`. Direct quote / paraphrase is allowed; fabrication is forbidden.
  - `## Get started` — one CTA (link to docs, sign-up flow, or feature flag). Single primary action.

**`templates/launch-comms/email.md`** ships with:

- Frontmatter: `object_type: Launch Communication` (proposed), `audience: customer-email`, `parent_handoff_packet: <placeholder>`, plus the universal-schema base.
- H2 sections:
  - `## Subject line` — single line, ≤ 60 chars (the email's load-bearing unit; everything else is body). The interactive prompt asks for the subject FIRST and asks the human to confirm character count before advancing.
  - `## Preview text` — ≤ 90 chars (the inbox preview snippet; lives between subject and body in most clients).
  - `## Body` — three short paragraphs maximum. One opening sentence ("here's what's new"), one middle paragraph naming the benefit and linking to the blog post, one closing sentence with the single CTA.
  - `## Call to action` — one line; matches the `Get started` CTA in `blog.md` for cross-channel consistency.

The three templates are deliberately **different in section count, section length, and voice**. The audience-distinct-body contract is encoded by these per-audience section lists; an executor cannot accidentally produce undifferentiated copy because the templates' H2 lists do not overlap.

## Per-audience differentiation

The audience-distinct contract is the load-bearing semantic check this spec enforces. Three differentiation axes:

1. **Voice.** Internal = direct, operational, runbook-aware ("on-call rotation: …", "escalate to …"). Blog = customer-benefit-led, narrative, second-person ("you can now …"). Email = imperative, scannable, single-action ("Get started in two clicks.").
2. **Length.** Internal: 5 H2s, target 300–600 words. Blog: 5 H2s, target 250–500 words. Email: 4 H2s, target 80–150 words (the whole email).
3. **Concerns named.** Internal names on-call / runbook / kill-switch. Blog names benefit / use-case / segment. Email names subject / preview / one CTA.

The interactive walk's prompts are per-audience-distinct. Per the parent convention's "one question at a time" rule, the command asks one question per placeholder, sequentially. The verbatim per-audience prompts (the command file contains the full set; this section is the reference):

**Internal-team announcement (`internal.md`) — 4 prompts (one per `## What shipped`, `## Who owns what at launch`, `## Kill-switch and rollback plan`, `## Internal FAQ`; the `## Talking points for customer-facing teams` section is filled by deriving from the prior four):**

1. "What shipped, in one paragraph for an internal-team audience? Name the product behaviour and the rollout phase (e.g., '10% rollout to US-only')." [Confirmation echo follows.]
2. "Who owns this at launch? List the on-call rotation, the runbook link, and the escalation path. The parent packet's `launch-considerations.md` §'Communications and rollout' should already name these; copy through if so."
3. "What is the kill-switch / rollback plan if something breaks? Quote the parent packet's plan verbatim if one exists; otherwise stop — kill-switch is required for any internal-team launch announcement."
4. "What internal questions are anticipated? List 3–6 question / answer pairs. Focus on operational concerns (load, dependencies, on-call burden), not customer-facing FAQ."

**External blog post (`blog.md`) — 5 prompts:**

1. "Write the headline. One sentence, customer-facing claim. Voice: direct address ('you'), not internal ('we shipped'). The headline is the load-bearing copy unit; spend the time."
2. "Write the opening paragraph for `## What this means for you`. Lead with the customer benefit, not the internal capability. Voice: second person."
3. "Describe how the feature works in plain language. 2–3 sentences. Where would a screenshot go? (Insert `![placeholder]` marker; the human attaches the actual image post-walk.)"
4. "Who is this for? Reference the customer segment from the parent packet's `customer-segment.md`. Direct quote / paraphrase is allowed; do NOT fabricate a segment that isn't in the packet."
5. "What is the single primary CTA? Provide the link and the action verb (e.g., 'Get started in the dashboard'). One CTA — no secondary actions."

**Customer email (`email.md`) — 4 prompts (subject-first, per email-copywriting discipline):**

1. "Write the subject line. ≤ 60 chars. The subject is what gets opened; everything else is downstream. Confirm character count before advancing." [Command computes and echoes char count.]
2. "Write the preview text. ≤ 90 chars. This is the snippet that appears in the inbox between subject and body in most clients. Confirm character count before advancing."
3. "Write the email body. Three short paragraphs maximum. One opening sentence ('here's what's new'), one benefit paragraph linking to the blog post you just drafted, one closing sentence with the CTA."
4. "Write the call to action. One line. MUST match the `Get started` CTA in `blog.md` for cross-channel consistency — paste it through. The command will not auto-link the two; you confirm the match."

The command does **not** ask the same generic question three times labelled differently. Each audience's prompt set references audience-specific concerns; an executor that produces undifferentiated copy will fail the manual-gesture review at §"Verification mode."

## Interactivity contract

One prompt at a time, sequentially. Never batch. Per parent convention, this is the kit's `.claude/CLAUDE.md` "one clarifying question at a time" rule made mechanical.

The `--audience` flag scopes which audience drafts are walked. With `--audience all`, the command walks all three audiences in sequence: internal first (operational concerns clear the deck), then blog (the customer-narrative anchor), then email (which references the blog's CTA). With `--audience <single>`, the command walks only that audience's prompt set and writes only that file; if a user invokes `--audience internal` on Tuesday and `--audience blog` on Wednesday, the existing `internal.md` is left untouched on Wednesday's invocation (the `--force` flag would be required to overwrite it).

The flag aliases `--audience external` ≡ `--audience blog`; `--audience email`, `--audience internal`, `--audience blog` are the three primary modes. `--audience all` is the default.

Per-audience walks proceed: prompt → human answer → confirmation echo → next prompt. Within a walk, after the last prompt is answered, the assembled audience draft is echoed and the human is asked: "Does this <audience-name> draft read in the right voice for its audience? Confirm or revise." A revise loop replays the per-prompt walk for that audience.

## Procedure

### Step 1 — resolve parent Handoff Packet

If `--from <handoff-packet-slug>` is given, validate that `delivery/handoff-packets/<handoff-packet-slug>/` exists with `status:` not `Deprecated`. If not, exit code 2 with: `"no Handoff Packet found at delivery/handoff-packets/<handoff-packet-slug>/ — run /handoff-packet <slug> first, then /audit-completeness <slug>, then re-run /launch-comms."`

Otherwise list candidates from `delivery/handoff-packets/` whose `status:` is not `Deprecated`, sorted by `last_updated:` descending, capped at 10. Present as a numbered list; ask the human to pick one (or re-run with `--from`). Never silently pick — always confirm, even when only one candidate exists.

If the candidate list is empty, exit code 2 with: `"no Handoff Packet found in delivery/handoff-packets/ — run /handoff-packet <slug> first."`

### Step 2 — instantiate the folder

Create `delivery/launch-comms/<slug>/` (`mkdir -p`; creates the family directory `delivery/launch-comms/` on first invocation). If the destination exists and `--force` is not set, exit code 2 with: `"delivery/launch-comms/<slug>/ already exists — re-run with --force to overwrite, or pick a different slug."`

Per the `--audience` flag, copy a subset of `templates/launch-comms/*.md` to the destination. `--audience all` copies all three; `--audience internal|blog|email|external` copies the named single file (`external` ≡ `blog`). Pre-fill each copied file's mechanical frontmatter:

- `id: LC-<NNN>` — scan `delivery/launch-comms/*/*.md` for `id: LC-` lines, take max + 1, zero-pad to three digits (or `001` if none). Each audience draft gets its own `id:` (so a `--audience all` invocation produces three sequential `LC-NNN` values).
- `slug:` — the positional argument plus an audience suffix (e.g., `<slug>-internal`, `<slug>-blog`, `<slug>-email`).
- `created:` — today's date, ISO-8601, resolved from system clock at command-start.
- `last_updated:` — same as `created`.
- `parent_handoff_packet:` — the resolved Handoff Packet slug from Step 1.
- `parent_initiative:` — read from the parent Handoff Packet's `README.md` frontmatter and carried through.
- `audience:` — pre-filled to the audience the template was authored for (`internal-team`, `external-blog`, `customer-email`). Re-asserted per the template's pre-filled value (defensive check).
- `object_type: Launch Communication` — re-asserted per the template's pre-filled value (defensive check).
- `status: Draft` — re-asserted; the artifact lifecycle begins at Draft and flips to `Approved` only after the human-owned-decisions confirmation step.

### Step 3 — walk the audience-distinct prompts

For each audience in the resolved `--audience` scope (default order: internal → blog → email), walk that audience's prompt set per §"Per-audience differentiation" above. One question per turn. Confirm each prompt's answer before advancing. After the last prompt for an audience, echo the assembled draft and ask the per-audience voice-check question. A `revise` response replays that audience's walk; a `confirm` response advances to the next audience (or to Step 4 if no audiences remain).

### Step 4 — surface human-owned decisions

For each written audience draft, surface the human-owned-decisions list. The customer-facing drafts (`blog.md`, `email.md`) carry — at minimum — these `human_owned_decisions:` entries (pre-filled by the template):

- "Customer-facing copy approval (this draft will not be published without a named approver's sign-off)."
- "Headline / subject-line factual accuracy (no claim outside the parent Handoff Packet's verified content)."
- "Marketing / Legal / Compliance review status (none of these reviews are run by this command; the human routes the draft to the named reviewer)."

The internal draft carries:

- "Runbook accuracy (the on-call rotation and runbook link are verified by the named engineering owner)."
- "Kill-switch / rollback plan accuracy (verbatim copy through from the parent packet, or a named owner has approved a divergence)."

For each entry, ask the human to confirm the decision is owned by a named human. Record confirmations under `approvals_obtained:` in `<role>: <YYYY-MM-DD>` form. **The command will not auto-publish, auto-send, or auto-link any draft to any publishing surface.**

### Step 5 — lint each written file

For each audience draft written, run `python3 <repo-root>/tools/lint-frontmatter.py <written-path>` (default mode). Repo root resolved as nearest ancestor of CWD containing `tools/lint-frontmatter.py`.

- If all written files exit 0: proceed to Step 6.
- If any file exits non-zero: surface the linter output, offer to re-open that file's relevant sections for correction. If the human accepts and the corrections re-lint clean, proceed. If the human declines (or re-lints still fail), exit code 3 with the linter output surfaced and the folder left on disk in known-imperfect state.

### Step 6 — emit the next-command hint

Last line of output, formatted exactly:

```
NEXT: /launch-checklist <slug>
```

If `/launch-checklist` (P4.14) has not yet shipped at the time `/launch-comms` runs, the line is `NEXT: /launch-checklist <slug> (planned — ROADMAP P4.14)` per the kit's drift-handling convention. The human runs `/launch-checklist` next to confirm the launch is operationally ready before any of the comms drafts go live.

No `REVIEW:` line is emitted.

## Exit codes

- `0` — folder instantiated, all audience drafts in scope walked and filled, all written files linted clean, NEXT emitted.
- `1` — human aborted the interactive walk before Step 5 completed. Partial folder left on disk (any audience drafts already confirmed are present; the in-progress audience is at its last-confirmed state). Resume by re-running with the same `<slug>` and the same `--audience` scope plus `--force`.
- `2` — pre-conditions failed: positional `<slug>` malformed; destination exists without `--force`; `templates/launch-comms/` missing; candidate parent Handoff Packet list empty; `--from <handoff-packet-slug>` named but the named packet does not exist or is `Deprecated`; `--audience` flag named an invalid value.
- `3` — folder written but one or more audience drafts failed default-mode lint, and the human declined re-open (or re-opened but re-lint still failed). Folder persists on disk in known-imperfect state. Automation consumers MUST treat exit 3 as distinct from exit 0.

## Boundaries

### Always do

- Walk the audience-distinct prompt sets per §"Per-audience differentiation." Never substitute a generic prompt for an audience-specific one.
- Resolve the parent Handoff Packet via the candidate-list discipline (never auto-pick; always confirm; cap at 10; sort by `last_updated:` descending).
- Surface the `human_owned_decisions:` confirmation step for every written audience draft, including the customer-facing copy-approval decision (load-bearing per `docs/HUMAN-AI-OWNERSHIP.md`).
- Quote the parent Handoff Packet's `launch-considerations.md` §"Communications and rollout" sub-section verbatim into `internal.md`'s `## Kill-switch and rollback plan` section when the packet provides one; ask the human if the packet does not, and refuse to proceed for the internal draft if no kill-switch plan exists.
- Confirm the parent Handoff Packet choice with the human even when only one candidate exists.
- Resolve the repo root as nearest ancestor of CWD containing `tools/lint-frontmatter.py`; never assume CWD is the repo root.
- Emit `NEXT: /launch-checklist <slug>` (with `(planned — ROADMAP P4.14)` if unshipped) on success.

### Ask first

- Adding a fourth audience to the canonical set (e.g., a Slack message, a social post, a partner-facing brief). The current three are deliberately chosen to cover the highest-frequency launch surfaces; expanding the set risks the command becoming "four separate commands in a trench coat." Surface as a per-command-spec deviation note and consider whether to split before adding.
- Adding `--non-interactive` mode (auto-fill from the parent Handoff Packet without prompting). The interactivity contract is load-bearing because audience-distinct voice cannot be auto-derived from structured packet content.
- Adding a `--cross-link-ctas` flag that auto-substitutes the `blog.md` CTA into `email.md`. The human is responsible for confirming cross-channel CTA consistency in Step 3; auto-substitution shadows that decision.

### Never do

- Produce undifferentiated copy across the three audience files. The audience-distinct voice / length / concerns contract (§"Per-audience differentiation") is load-bearing. An executor that fills all three files with paraphrased versions of the same paragraph fails the manual-gesture review. **This is the load-bearing semantic check of this spec.**
- Auto-publish, auto-send, auto-post, or auto-link any audience draft to any publishing surface (CMS, email-sending platform, social network, Slack). The command writes files to disk and exits; downstream publishing is a separately-owned human workflow.
- Fabricate metrics, customer quotes, segment definitions, KPIs, or claims not already present in the parent Handoff Packet. If the human asks for a number that isn't in the packet, ask which source it came from and require a citation before allowing it into a customer-facing draft.
- Fill `blog.md` or `email.md` without surfacing the customer-facing-copy-approval `human_owned_decisions:` entry. Per `docs/HUMAN-AI-OWNERSHIP.md`, customer-facing claims are an area AI must never be the final owner.
- Modify `templates/launch-comms/` from inside the command at runtime. The templates are frozen by this spec.
- Add a new ontology type without an RFC. `Launch Communication` is a new sub-type that this spec proposes (see open question 2); the executor must confirm before treating it as canonical.
- Write the launch-comms folder under `delivery/handoff-packets/<slug>/launch-comms/` (Option B). The destination is `delivery/launch-comms/<slug>/` per §"Destination path resolution."
- Silently pick a parent Handoff Packet when multiple candidates exist (or when only one exists — always confirm).

## Verification mode

- **Goal-based check** — `.claude/commands/launch-comms.md` passes `bash tools/lint-command.sh`. The body's H2 superset matches the convention's required H2s. The `argument-hint:` frontmatter starts with `<slug>` per the artifact-creating sub-class. The body cites `templates/launch-comms/`, `delivery/launch-comms/`, and `delivery/handoff-packets/`.
- **Goal-based check** — each of `templates/launch-comms/{internal.md, blog.md, email.md}` passes `python3 tools/lint-frontmatter.py --check-template <path>` (template-mode lint that accepts angle-bracket placeholders).
- **Manual gesture** — one recorded reproduction: from a fixture Handoff Packet, invoke `/launch-comms my-test-comms --from <fixture-packet-slug> --audience all` in a Claude Code session. The reviewer verifies (a) three files written at `delivery/launch-comms/my-test-comms/`; (b) each file's H2 list matches its template's H2 list; (c) the three drafts are demonstrably different in voice, length, and concerns — not paraphrases of the same paragraph; (d) the command surfaced the customer-facing-copy-approval `human_owned_decisions:` entry for `blog.md` and `email.md`; (e) the NEXT line is exactly `NEXT: /launch-checklist my-test-comms` (or with the `(planned …)` suffix). Recorded in `notes/manual-gesture.md` at CAPTURE phase.
- **Audit-driven** — none directly. The command's outputs are linted via the default-mode frontmatter linter (Step 5); no kit-wide audit gates this command's correctness beyond shape lint.

## Contract tests

Each test is one shell line or one pytest case. They are the gate.

- `T1` — `test -f .claude/commands/launch-comms.md` exits 0.
- `T2` — `bash tools/lint-command.sh .claude/commands/launch-comms.md` exits 0.
- `T3` — `grep -cE "^## (When to run|Inputs|Procedure|What this command will not do)" .claude/commands/launch-comms.md` returns 4 (required H2 superset).
- `T4` — `grep -cE "^argument-hint: <slug>" .claude/commands/launch-comms.md` returns 1.
- `T5` — `grep -c "templates/launch-comms/" .claude/commands/launch-comms.md` returns ≥ 1 AND `test -d templates/launch-comms` (cited template path exists).
- `T6` — `grep -c "delivery/launch-comms/" .claude/commands/launch-comms.md` returns ≥ 1.
- `T7` — `grep -c "delivery/handoff-packets/" .claude/commands/launch-comms.md` returns ≥ 1 (parent family cited).
- `T8` — `grep -cE "^NEXT: /launch-checklist <slug>" .claude/commands/launch-comms.md` returns ≥ 1 (chain hint present; line may include a trailing `(planned — ROADMAP P4.14)` suffix per kit-drift policy).
- `T9` — `test -f templates/launch-comms/internal.md && test -f templates/launch-comms/blog.md && test -f templates/launch-comms/email.md` (the three audience-distinct template files exist).
- `T10` — `python3 tools/lint-frontmatter.py --check-template templates/launch-comms/internal.md templates/launch-comms/blog.md templates/launch-comms/email.md` exits 0 (all three templates pass template-mode lint).
- `T11` — Per-audience H2 lists are distinct: `grep -c "^## " templates/launch-comms/internal.md` returns 5, `grep -c "^## " templates/launch-comms/blog.md` returns 5, `grep -c "^## " templates/launch-comms/email.md` returns 4 (the deliberate-asymmetry contract; mirrors §"Per-audience differentiation").
- `T12` — `grep -c "^## Subject line$" templates/launch-comms/email.md` returns 1 AND `grep -c "^## Subject line$" templates/launch-comms/blog.md` returns 0 AND `grep -c "^## Subject line$" templates/launch-comms/internal.md` returns 0 (subject-line section is unique to email — voice asymmetry check).
- `T13` — `grep -cE "^## Kill-switch" templates/launch-comms/internal.md` returns 1 AND `grep -cE "^## Kill-switch" templates/launch-comms/blog.md` returns 0 AND `grep -cE "^## Kill-switch" templates/launch-comms/email.md` returns 0 (kill-switch section is unique to internal — concerns asymmetry check).
- `T14` — `grep -c "human_owned_decisions" templates/launch-comms/blog.md` returns ≥ 1 AND `grep -c "human_owned_decisions" templates/launch-comms/email.md` returns ≥ 1 (customer-facing-copy approval surfaced per HUMAN-AI-OWNERSHIP).
- `T15` — `bash tools/pre-pr.sh` exits 0 (no kit-wide regression).
- `T16` — `grep -cE "^- \[ \] \*\*P4\.13\*\*" ROADMAP.md` returns 1 at PLAN-phase time (the P4.13 row is still unchecked; flips to `[x]` only at CAPTURE).
- `T17` — `grep -c "untouched" .claude/commands/launch-comms.md` returns ≥ 1 (the per-file overwrite contract is documented in the command body: existing sibling audience drafts are left untouched on subsequent `--audience <other>` invocations without `--force`; not just declared in the spec).

## Non-goals

- Auto-publishing any draft to any platform. Out of scope by design — customer-facing claims are an area AI must never be the final owner (per `docs/HUMAN-AI-OWNERSHIP.md`).
- Drafting Slack messages, social-network posts, partner-facing briefs, sales-team enablement decks, support-team macros, or any audience outside the canonical three. Out of scope by design; surfaces as open question 1 if adopters need a fourth audience.
- Running a voice-check skill against the drafts. The `voice-check` skill is planned (ROADMAP P8.4) but unshipped; this command does not gate on it. When `voice-check` ships, a future revision of this spec may add it as an optional Step 5.5.
- Auto-translating drafts into other languages. Out of scope.
- Auto-generating images, screenshots, or screen recordings to insert into `blog.md`. The command inserts a `![placeholder]` marker for the human to replace.
- Running a sentiment / readability / Flesch-Kincaid check on the drafts. Out of scope; surfaces in the human-led customer-facing-copy-approval step.
- Linking the drafts to a CMS, an email-sending platform, a social-scheduling tool, or any external system.
- Modifying `templates/handoff-packet/launch-considerations.md`. The sub-section "Communications and rollout" is this command's input, not its output; the template is frozen by F3.9.
- Adding a `--non-interactive` mode that fills from the parent packet without prompting. Per parent convention's load-bearing interactivity contract.
- Authoring P4.14 `/launch-checklist`. Out of scope; sibling spec under P4.14.

## Open questions

1. **Should the canonical audience set include a fourth audience (e.g., Slack channel announcement, partner-facing brief, social post)?** _Deferred. The three-audience set covers the most-frequent launch surfaces (internal team, customer email, public blog) — these are the audiences every product launch needs. A fourth audience (Slack, social, partner) is needed maybe one launch in three; folding it into this command risks the audience-distinct contract degrading (the three current audiences have meaningfully different voice / length / concerns; a fourth audience would either inherit one of the existing voices or require a new prompt set). **If the audience set grows to 4+ AND per-audience copy diverges enough that the command starts to feel like four separate commands, the supervisor MAY split** into `/launch-comms-internal`, `/launch-comms-customer`, `/launch-comms-public`. Flag for first-usage feedback. (Surfaces the supervisor's brief's explicit split-question.)_
2. **Should `Launch Communication` be added as a new ontology type in `context/frameworks/ontology.md`?** _Deferred. The kit currently lacks an atomic ontology type for launch comms (Domain H names `Communication Plan` as the closest neighbour, per HANDOVERS-6 §"Folder contents"). Whether `Launch Communication` is a new atomic type (a sub-type of Communication Plan) or a polymorphic-content type within Communication Plan is an ontology decision that warrants an RFC. The spec uses `object_type: Launch Communication` as the proposed value for the template frontmatter; the executor MUST flag this for an RFC if the ontology audit at REVIEW phase rejects the value. If the RFC route is taken before EXECUTE, the spec adopts the RFC's resolution; otherwise `Launch Communication` ships as a proposal and the RFC lands in CAPTURE._
3. **Should the command emit a per-audience word-count check (e.g., warn if `blog.md` body exceeds 800 words)?** _Deferred. The voice-check skill (planned — ROADMAP P8.4) is the natural home for body-length heuristics; folding it into this command duplicates the discipline. Surface as a future polish item once voice-check ships._
4. **Should `delivery/launch-comms/` carry a family-level README explaining the contents (mirroring `delivery/handoff-packets/`'s implicit family-level discoverability)?** _Deferred. The new family directory is created on first command invocation via `mkdir -p`; no family-level README is shipped by this spec. Surface if adopters report discoverability friction._
5. **Should the email draft (`email.md`) include an A/B subject-line option section (two subject lines instead of one)?** _Deferred. The current spec ships one subject line; A/B testing is a marketing-team workflow that lives downstream of this command. Surface if adopters request._

## Acceptance criteria

- [ ] `.claude/commands/launch-comms.md` exists with the body shape specified in §"Procedure" (four required H2s plus the per-audience prompt sets from §"Per-audience differentiation").
- [ ] `argument-hint:` frontmatter is exactly `<slug> [--audience internal|external|email|blog|all] [--from <handoff-packet-slug>] [--force]`.
- [ ] `description:` frontmatter is one sentence, ≤ 1024 chars, accurately summarising the command's audience-distinct multi-output behaviour.
- [ ] `templates/launch-comms/` exists with exactly three children: `internal.md`, `blog.md`, `email.md`.
- [ ] Each template child's H2 list matches §"Inputs and outputs (template files)" exactly; the per-audience asymmetry (internal: 5 H2s including Kill-switch; blog: 5 H2s including Headline; email: 4 H2s including Subject line) is preserved.
- [ ] Each template child carries `human_owned_decisions:` frontmatter that includes the customer-facing-copy-approval entry for `blog.md` and `email.md`; the internal template includes runbook accuracy and kill-switch accuracy.
- [ ] The command body documents the destination path as `delivery/launch-comms/<slug>/` (Option A); Option B (nesting under handoff-packets) is explicitly named in §"Destination path resolution" and rejected with rationale.
- [ ] The command body documents the audience-distinct prompt sets (per-audience prompts cited verbatim or by reference to §"Per-audience differentiation").
- [ ] The command body documents the four-code exit-code contract verbatim per parent convention.
- [ ] The command body's last documented output line is exactly `NEXT: /launch-checklist <slug>` (with `(planned — ROADMAP P4.14)` suffix if unshipped at command-run time).
- [ ] All contract tests pass: T1–T17.
- [ ] No new ontology type committed without an RFC (`Launch Communication` flagged in open question 2; executor confirms with supervisor before treating as canonical).
- [ ] No modification to `templates/handoff-packet/`, `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, or any tooling under `tools/`.

## Cross-references

- **Consumed by:** kit users running `/launch-comms <slug>` in Claude Code, after `/handoff-packet <slug>` and `/audit-completeness <slug>` have run and the named feature is shipping / has shipped. Downstream chain: `NEXT: /launch-checklist <slug>` (P4.14 — planned).
- **Consumes:** `templates/launch-comms/` (ships with this spec), `delivery/handoff-packets/` (parent-resolution family directory), the parent Handoff Packet's `launch-considerations.md`, `README.md`, `customer-segment.md`, `success-metrics.md`, `tools/lint-frontmatter.py` (default mode), `.claude/commands/_meta/command-skeleton.md` (copy-source for the command file).
- **Frontmatter fields owned:** none directly on existing artifacts. The three template children declare new frontmatter fields: `audience:` (controlled vocabulary: `internal-team`, `external-blog`, `customer-email`), `parent_handoff_packet:` (slug ref), and re-asserts `object_type: Launch Communication` (proposed — see open question 2). The command pre-fills these mechanically per Step 2.
- **Ontology object types touched:** `Launch Communication` (proposed new type — flagged in open question 2; executor confirms with supervisor and supervisor decides whether to open an RFC before CAPTURE). `Handoff Packet` (Domain H — read for parent resolution). `Customer Segment` (Domain A — read from parent packet's `customer-segment.md`, never modified). `KPI` (Domain D — KPI claims in `blog.md` MUST cite the parent packet's `success-metrics.md`; fabrication is forbidden).
