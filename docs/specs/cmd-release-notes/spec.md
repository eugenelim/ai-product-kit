# Spec: cmd-release-notes

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command (plus a small single-file template — `templates/release-notes.md` — shipped alongside; see §"Component type" below for the explicit rationale)
- **Serves kit phase:** Delivery (post-ship comms — between Handover 6 and Handover 7)
- **Constrained by:** ROADMAP row P4.12; `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands"; `docs/HANDOVERS.md` §"Handover 6" and §"Handover 7"; `docs/HUMAN-AI-OWNERSHIP.md` zone 1 (release-notes drafting is AI-assisted) and zone 3 (customer-facing claims are human-only). The command **partially conforms** to the F4 template-fill convention — see §"F4 template-fill convention applicability" for the explicit deviation list.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** This document defines what "done" means for the `/release-notes` slash command and its companion `templates/release-notes.md` template. The implementing work must match this spec, or update it in the same session. Verification must be derivable from this spec — if a behavior isn't here, it isn't promised.

## Objective

`/release-notes <slug> [--from-landing <landing-slug>]` is the Phase-4 post-ship comms-drafter command that produces a customer-facing release-note draft for a shipped change. It reads either a Handoff Packet (default) or a Landing Report (when `--from-landing` is passed); copies `templates/release-notes.md` to `delivery/release-notes/<slug>.md`; walks the template body interactively to collect a one-paragraph "what's new" plus a 3-to-7-item bulleted feature list, both in customer voice; pre-fills mechanical frontmatter; runs `tools/lint-frontmatter.py` against the written file; surfaces the produced copy as a `human_owned_decisions:` item for the named human to review before publication; emits a NEXT hint pointing at the human review (no downstream command in the chain). The command exists because customer-facing copy is the kit's most exposed AI-assisted-but-human-owned surface — release notes are explicitly cleared for AI drafting (HUMAN-AI-OWNERSHIP zone 1) but the *claims they make* are zone 3 (human-only). Centralising the draft path is what keeps the zone-1/zone-3 split visible.

The command has no prior stub. The slug `cmd-release-notes` is the canonical name per ROADMAP row P4.12; the template slug is `release-notes` per the kit's template-naming convention.

## Why now

P4.11 (`/handoff-packet`) shipped on 2026-05-23, closing the Phase-4 template-fill chain through Handover 6. P4.12 is the first post-ship comms command, and the ROADMAP slates P4.12 → P4.13 (`/launch-comms`, internal + external launch messaging) → P4.14 (`/launch-checklist`) → P4.15 (`/retro`) as a four-command Phase-4 post-ship cluster. `/release-notes` is the cluster's smallest, narrowest command (single audience: customer; single output: external-facing copy) and is the right place to land the comms-drafter shape before the broader `/launch-comms` (multi-audience) variant in P4.13. Without this command, customer-facing copy is drafted ad-hoc, which is precisely the failure mode HUMAN-AI-OWNERSHIP zone-3 controls are meant to prevent.

It also gives the F1 audit family (`/audit-spec-linkage`, `/audit-traceability`) a real fixture surface in `delivery/release-notes/` once instances start landing.

## Component type

Two kit components ship together under this spec:

1. **The slash command** — `.claude/commands/release-notes.md`. Authored under this spec; `tools/lint-command.sh` passes.
2. **The template** — `templates/release-notes.md`. Authored under this spec (a small single-file template, ≤ 60 lines including frontmatter). It is in scope here because (a) every other Phase-4 template-fill command consumes a `templates/<slug>.md` and the contract test `scripts/tests/test_templates_instantiate.py` walks `templates/*.md`, (b) the customer-voice body shape (one-paragraph "what's new" + bulleted user-visible feature list + audience metadata) is non-trivial and benefits from a canonical skeleton, (c) consolidating into one work-loop iteration is cheaper than splitting into two specs that ship together.

Both components are produced under this spec; both must pass their respective linters at VERIFY. If the template later grows substantially (e.g., per-audience variants), it should be split into its own follow-up spec — flagged in open questions.

## Destination path resolution

**Choice: Option A — top-level family at `delivery/release-notes/<slug>.md`.**

Rationale:

- A release note is a Customer Communication (ontology Domain G), a distinct lifecycle object from the Handoff Packet (Domain H). Nesting one inside the other couples their lifecycles — if the packet is deprecated or restructured, the release note travels with it for no good reason.
- A single shipped change can produce more than one release note over time (initial release, follow-up announcement of a fix, GA-after-beta). One-to-many fits a top-level family; one-to-one nesting does not.
- The `--from-landing` parent path treats a Landing Report as the input. A Landing Report lives at `delivery/landings/<landing-slug>.md`, not under a packet — so the nesting option only makes sense for the default parent (a packet), not for `--from-landing`. Top-level placement gives both parent paths a uniform destination.
- The audit family `/audit-spec-linkage` (HANDOVERS-5) and the planned `/audit-landings-debt` (HANDOVERS-7) both walk `delivery/<family>/`; a top-level `delivery/release-notes/` participates naturally.

The trade-off: option B (`delivery/handoff-packets/<slug>/release-notes.md`) would have given engineers a single folder to read end-to-end at handoff time, but the post-ship audience is customer-facing, not engineering, so co-location optimises for the wrong reader.

## F4 template-fill convention applicability

**Partial conformance.** The convention (`docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands") was authored around the *artifact-creating* sub-class (`/draft-vision`, `/draft-initiative`, `/draft-spec`, `/handoff-packet`), which writes a *primary product artifact* into a phase-folder. `/release-notes` shares most of that shape but deviates on three points; deviations declared explicitly here (per `_meta/command-skeleton.md`'s instruction to declare deviations in `Constrained by:`).

**Conforming behaviours:**

- Frontmatter: `description:` (≤ 1024 chars) + `argument-hint:` only — matches the convention exactly.
- Argv: first positional is `<slug>` (kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars) — matches the artifact-creating sub-class.
- Procedure shape: resolve parent → copy template → interactive walk one-section-at-a-time → surface human-owned decisions → lint → emit NEXT hint.
- Exit codes: 0 / 1 / 2 / 3 per the convention.
- Pre-fill rules: `id`, `slug`, `created`, `last_updated`, `parent_handoff_packet` (or `parent_landing` when `--from-landing` is set), `object_type`.
- Never-batch interactive contract.

**Explicit deviations:**

1. **Two parent families, alternated by flag.** Default parent is a Handoff Packet at `delivery/handoff-packets/<parent-slug>/`; with `--from-landing <landing-slug>`, the parent is a Landing Report at `delivery/landings/<landing-slug>.md`. The convention assumes one parent family; this command requires two. Resolution proceeds against whichever family the flag selects; default is `handoff-packets`. The two flags are mutually exclusive (only `--from-landing` exists today; `--from <packet-slug>` is rejected, the positional already names the release-notes slug).
2. **Output is a draft, not a finished artifact.** The convention treats the written file as a complete product artifact gated by the linter. For release notes, the linter pass is necessary but not sufficient — the body is a *draft for human review*. The command surfaces the produced copy as a `human_owned_decisions:` item ("Approval of customer-facing claims in the draft body before publication") and the NEXT line names the human review, not a downstream slash command. Publication is explicitly never a behaviour of this command.
3. **NEXT line points to the Wave-4 sibling that produces the broader launch comms; human-review of the draft is a precondition for publication, not a downstream chain step.** The Wave-4 post-ship chain is `/release-notes` → `/launch-comms` (P4.13) → `/launch-checklist` (P4.14) → `/landing-report` (planned P5.x). The NEXT line for `/release-notes` therefore reads: `NEXT: /launch-comms <slug>`. The human-review of the customer-facing draft (the zone-3 gate) is enforced via the pre-populated `human_owned_decisions:` entry plus the explicit `## What this command will not do` non-behaviour ("never auto-publish"). The human is expected to (a) read and approve the draft before publishing it externally, and (b) run `/launch-comms` next to assemble the broader launch comms set; the two are not sequenced relative to each other (publication can wait on approval; `/launch-comms` doesn't read this file).

The deviations are minor — every convention-mandated behaviour is preserved, with output-handling added that the convention does not address. The contract test for Phase-4 commands (`scripts/tests/test_phase_4_command_convention.py`, if it exists at EXECUTE time) is expected to either skip P4.12 or be amended to recognise the post-ship sub-class; flagged as an open question.

## Inputs and outputs

**Inputs.**

1. The positional argument `<slug>` — the release note's slug. Kebab-case, `^[a-z0-9-]+$`, ≤ 80 chars.
2. The flag `--from-landing <landing-slug>` (optional). When set, the parent is a Landing Report; when unset, the parent is a Handoff Packet (default).
3. The flag `--force` (optional). Permits overwriting an existing `delivery/release-notes/<slug>.md`.
4. `templates/release-notes.md` — the single-file template this command copies.
5. **Default parent path:** `delivery/handoff-packets/<parent-slug>/README.md`. Frontmatter fields read: `id`, `slug`, `parent_initiative`, `parent_vision`. The README's `## Product brief` H2 is surfaced as read-only context for the "what's new" prompt (not copied verbatim — the human re-states in customer voice). The packet's `features.md` and `success-metrics.md` files are surfaced as read-only context the human can refer to during the walk.
6. **`--from-landing` parent path:** `delivery/landings/<landing-slug>.md`. Frontmatter fields read: `id`, `slug`, `parent_vision`, `parent_handoff_packet`. The landing's `## The shipped change`, `## Predicted outcomes vs actuals`, and `## What landed and what didn't` H2s are surfaced as read-only context.

The command does **not** read `templates/handoff-packet/launch-considerations.md` from the packet folder — that file is the packet's internal rollout-plan section, not source material for customer-facing claims. The human may consult it manually; the command does not auto-extract from it.

**Outputs.**

1. **File written:** `delivery/release-notes/<slug>.md`. Contents:
   - Frontmatter — universal-metadata schema with mechanical fields pre-filled (see "Pre-fill rules" below) and `human_owned_decisions:` pre-populated with the canonical decision "Approval of customer-facing claims in the draft body before publication".
   - Body — two required H2s populated from the interactive walk: `## What's new` (one paragraph, customer voice) and `## Features in this release` (3-to-7 bulleted user-visible features, customer voice). Optional H2 `## Known limitations` walked only if the human opts in.
2. **Linter exit code surfaced.** `python3 tools/lint-frontmatter.py delivery/release-notes/<slug>.md` (default mode) must exit 0 before NEXT is emitted.
3. **NEXT line on stdout (last line):** `NEXT: /launch-comms <slug>` — the Wave-4 post-ship chain continuation. The customer-facing-copy human-review gate is enforced via the pre-populated `human_owned_decisions:` entry (not via the NEXT line); approval is a precondition for *publication*, not for invoking the next slash command.
4. **Side effect:** none. The command does **not** modify the parent Handoff Packet, the parent Landing Report, INVENTORY.md, ROADMAP.md, or any other file. The release-notes family is `delivery/release-notes/<slug>.md` only.

The template `templates/release-notes.md` is a separate output, written once at component-build time, not per invocation.

### Pre-fill rules

Before the interactive walk, the command pre-fills (the human is never asked for these):

- `id: RN-<NNN>` — scan `delivery/release-notes/*.md` for `id: RN-` lines, take max + 1, zero-pad to three digits (or `001` if none exist). `RN` is the chosen prefix for Release Notes; this spec asserts the prefix as authoritative.
- `slug:` — the positional argument.
- `object_type: Customer Communication` — Domain G atomic type (per `context/frameworks/ontology.md`).
- `status: Draft` — product-artifact lifecycle entry state.
- `created:` — today's date (ISO-8601, system clock at command start).
- `last_updated:` — same as `created`.
- `parent_handoff_packet:` (default parent) **or** `parent_landing:` (when `--from-landing` is set) — the resolved parent slug. The other field is omitted from frontmatter (not left as a placeholder).
- `parent_vision:` and `parent_initiative:` — transitive carry-through from the parent's frontmatter, if present. If either is missing in the parent, omit the field and surface a one-line warning naming the unresolved link (not blocking).
- `ai_assistance_used: ["Draft of customer-facing what's-new and feature-list copy"]`.
- `ai_assistance_allowed: restricted` — release notes are AI-assisted (zone 1) but the *claims they make* are zone 3, so `restricted` is the correct value.
- `human_approval_required: true`.
- `human_owned_decisions: ["Approval of customer-facing claims in the draft body before publication"]` — pre-populated; the human may add entries during Step 4.

If any mechanical field cannot be resolved, exit code 2 with the missing pre-condition named.

## Boundaries

### Always do

- Surface every produced bullet and the produced paragraph back to the human as a draft to be reviewed before publication. The produced copy must be visible in the final stdout summary, not only written to disk.
- Pre-populate `human_owned_decisions:` with the canonical "Approval of customer-facing claims..." entry, regardless of how the interactive walk proceeds.
- Resolve the repo root as the nearest ancestor of CWD containing `tools/lint-frontmatter.py`; do not assume CWD is the repo root.
- Honour `--force`'s semantics exactly (overwrite if and only if set).
- Confirm parent selection with the human even when only one candidate exists. Never silently pick.
- Emit the NEXT line as the last stdout line, formatted exactly as specified.

### Ask first

- Before walking the optional `## Known limitations` H2: ask the human whether the release has known limitations the customer should be told about. Skip the section if the answer is no.
- If the parent's frontmatter lacks `parent_initiative:` or `parent_vision:`, surface the gap to the human before writing — they may want to abort and fix the parent.
- If a supplied feature-list bullet contains internal jargon (heuristic check against a small token list defined in `plan.md`), ask the human to confirm or revise. The check is heuristic and non-blocking — it surfaces a prompt, never overrides.

### Never do

- Never publish the draft to any external surface. The command's output is a file on disk plus a stdout summary — nothing else. No HTTP, no shell-out to a CMS, no clipboard copy.
- Never invent metrics, feature claims, or customer-segment language that does not appear in the parent's frontmatter or in `templates/handoff-packet/success-metrics.md` (when the default parent is a packet). If the human asks the command to "make up a benefit," refuse and ask the human to source it.
- Never read or write any file outside `delivery/release-notes/<slug>.md`, the parent file (read-only), `templates/release-notes.md` (read-only at invocation time), or `tools/lint-frontmatter.py`.
- Never auto-publish, auto-PR, or auto-commit. Git is never touched.
- Never skip the `human_owned_decisions:` confirmation step (Step 4 in the Procedure).
- Never emit the NEXT line until the linter has exited 0.

## Verification mode

**Goal-based check** plus **audit-driven**. Three mechanical gates:

1. **`tools/lint-command.sh .claude/commands/release-notes.md` exits 0.** Validates the command file's frontmatter and body shape. Goal-based check.
2. **`tools/lint-frontmatter.py --check-template templates/release-notes.md` exits 0.** Validates the template's frontmatter with placeholders accepted. Audit-driven (template-instantiation contract).
3. **`scripts/tests/test_templates_instantiate.py` continues to pass after `templates/release-notes.md` is added.** The contract test walks every `templates/*.md` and runs `--check-template`; adding the new template must not break it.

No new pytest is mandated by this spec; the existing test_templates_instantiate.py walks the new template by glob. A fixture-based end-to-end test of the interactive walk is out of scope and flagged in open questions.

## Contract tests

- **CT-1:** `.claude/commands/release-notes.md` exists; `tools/lint-command.sh` against it exits 0.
- **CT-2:** `.claude/commands/release-notes.md` H1 is exactly `# /release-notes`.
- **CT-3:** The command file declares both `## When to run` and `## Procedure` sections (lint-command requires at least one; this spec requires both for parity with the F4 cohort).
- **CT-4:** The command file's `argument-hint:` frontmatter value is exactly `<slug> [--from-landing <landing-slug>] [--force]`.
- **CT-5:** The command file's body declares a `## What this command will not do` section, and that section contains literal mentions of the three non-behaviours: "auto-publish", "internal jargon", and "metrics not in".
- **CT-6:** `templates/release-notes.md` exists and `tools/lint-frontmatter.py --check-template templates/release-notes.md` exits 0.
- **CT-7:** `templates/release-notes.md` frontmatter contains `object_type: Customer Communication`, `status: Draft`, `ai_assistance_allowed: restricted`, and `human_approval_required: true` as pre-filled values (not placeholders).
- **CT-8:** `templates/release-notes.md` body contains exactly the H2s `## What's new` and `## Features in this release` (required), plus `## Optional sections` at the bottom containing `### Known limitations`.
- **CT-9:** `scripts/tests/test_templates_instantiate.py` continues to pass.
- **CT-10:** The command file's `description:` frontmatter is ≤ 1024 chars (enforced by lint-command, asserted here for completeness).

## Interactivity contract

The interactive walk is one prompt per turn, never batched. The prompts in order:

**Step 1 — parent confirmation (after resolution):**
- _"I've resolved the parent as <parent-type> '<parent-slug>'. The transitive parent_vision is '<value-or-NONE>' and parent_initiative is '<value-or-NONE>'. Confirm I should draft release notes against this parent, or cancel."_

**Step 2 — none (template copy is mechanical).**

**Step 3 — walk the body, one section at a time:**

- **`## What's new` (one prompt + one confirmation):** _"In one paragraph, what's new for the customer in this release? Write in customer voice — name what they can now do that they couldn't before. The product brief from the parent says: '<one-sentence quote from parent>'. Reply with your paragraph, or 'show' to see the full parent context first."_
  - After the paragraph is supplied, echo it and ask: _"Does this paragraph speak to the customer as the customer would describe the change? Confirm or revise."_
- **`## Features in this release` (loop until 3-to-7 collected, then confirmation):**
  - _"Name the next user-visible feature in this release, in one short line of customer voice. (Already collected: <N>. Need 3-to-7 total. Reply 'done' when finished, or 'show' to see the parent's features.md / success-metrics.md.)"_
  - If the supplied bullet matches the jargon heuristic: _"That bullet contains '<token>', which reads as internal jargon. Confirm or rewrite in customer voice."_
  - When the human says 'done' with ≥ 3 bullets: echo the list and ask _"Confirm this is the user-visible feature list as the customer would see it. Confirm or revise."_
  - If the human says 'done' with < 3 bullets: refuse to advance, prompt for more.
- **`## Known limitations` (one opt-in prompt, then per-bullet loop if opted-in):**
  - _"Does this release have known limitations the customer should be told about up front? (yes/no — replying 'no' deletes this optional section from the file.)"_
  - If yes: _"Name the next known limitation in customer voice. Reply 'done' when finished."_

**Step 4 — surface human-owned decisions:**
- _"The pre-populated human-owned decision is: 'Approval of customer-facing claims in the draft body before publication'. Name the human (role and name) who will own this approval, in the form '<role>: <name>'. Add more entries if there are additional zone-3 decisions in this release (pricing changes, customer commitments, etc.)."_

**Step 5 — linter run (no prompt unless lint fails):**
- On lint failure: _"The linter exited non-zero. Errors: <captured stderr>. Open the relevant sections for correction, or exit with code 3 and the file persisting in known-imperfect state."_

**Step 6 — final summary (no prompt; informational):**
- Echo: resolved parent; produced `## What's new` paragraph; produced `## Features in this release` bullets; produced `## Known limitations` bullets (if any); the `human_owned_decisions:` list with confirmed owners; the destination path.
- Then the NEXT line.

All prompts wait for human input. No prompt is auto-resolved.

## Procedure (summary; the command file `.claude/commands/release-notes.md` carries the canonical version)

1. **Resolve parent.** If `--from-landing <landing-slug>`: validate `delivery/landings/<landing-slug>.md` exists and `verdict:` is set. Otherwise: list `delivery/handoff-packets/` candidates filtered by `status:` not in `{Deprecated}`, sorted by `last_updated:` descending, capped at 10. Present numbered list; confirm with human. Empty list → exit 2 with remediation.
2. **Copy template.** `cp templates/release-notes.md delivery/release-notes/<slug>.md`. If destination exists and `--force` is not set, exit 2.
3. **Pre-fill mechanical frontmatter** (see "Pre-fill rules" above).
4. **Walk body one section at a time** (see "Interactivity contract" above).
5. **Surface `human_owned_decisions:`** for explicit confirmation.
6. **Lint:** `python3 tools/lint-frontmatter.py delivery/release-notes/<slug>.md`. On non-zero, offer re-open then re-lint; on persistent failure, exit 3.
7. **Emit final summary + NEXT line.** Final line: `NEXT: /launch-comms <slug>`. The summary echoes the pre-populated `human_owned_decisions:` entry ("Approval of customer-facing claims...") with the named owner — the customer-facing-copy review is a precondition for *publication*, enforced via that decision item, not via the NEXT line. No `/audit-*` follow-up command.

## Non-goals

- Not a multi-audience comms drafter. Customer is the single audience; the `internal + external` shape is P4.13 (`/launch-comms`).
- Not a publication tool. No CMS, blog, email, or status-page integration. Output is a file on disk plus a stdout summary; the human publishes elsewhere.
- Not a metrics generator. Does not invent or compute landing metrics; reads them from the parent's frontmatter if needed.
- Not a Landing Report writer. Does not modify `delivery/landings/`; `--from-landing` is read-only against landing reports.
- Not a Handoff Packet writer. Does not modify the packet; the packet is read-only at invocation time.
- Not chained to `/audit-completeness`, `/audit-traceability`, or any other audit. The post-ship comms cluster has no canonical audit gate (per ROADMAP P4.12–P4.15).
- Not responsible for catching jargon comprehensively. The jargon heuristic is intentionally tiny and surfaces a prompt; the human is the canonical filter.
- Not responsible for translating the copy into other languages. Single-language draft only.

## Open questions

1. **`RN-` prefix authority.** This spec asserts `RN-<NNN>` as the id prefix for Release Notes. The ontology (`context/frameworks/ontology.md`) does not currently fix prefixes for Domain G atomic types; this spec is making a local choice. Is that the right place to do it, or should an RFC/ontology update fix the prefix table once? **Answerable by:** the ontology maintainer at the first review of this spec. **Before implementing.**
2. **F4 contract test amendment.** If a contract test exists that asserts every Phase-4 command conforms to the artifact-creating sub-class (mutually exclusive with augmenting), `/release-notes` introduces a third sub-class (post-ship comms) that needs to be recognised. **Answerable by:** the agent executing this spec, by inspecting `scripts/tests/test_phase_4_command_convention.py` if it exists.
3. **Template growth path.** If `/launch-comms` (P4.13) introduces per-audience variants, the question becomes whether `templates/release-notes.md` should be subsumed into a `templates/launch-comms/release-notes.md` folder template. **Answerable by:** the author of the P4.13 spec.
4. **End-to-end pytest fixture.** Whether a Python integration test exercising the full interactive walk against a fixture parent packet is in scope. This spec defers it to a follow-up. **Answerable by:** the supervisor running the REVIEW phase.
5. **Jargon heuristic expansion.** The initial token list is small and English-only. A larger list (or a configurable file) might be wanted long-term. **Answerable by:** the first kit user who hits a false-negative.

## Acceptance criteria

- [ ] `.claude/commands/release-notes.md` exists; passes `tools/lint-command.sh`.
- [ ] `.claude/commands/release-notes.md`'s frontmatter has `description:` (≤ 1024 chars) and `argument-hint:` exactly `<slug> [--from-landing <landing-slug>] [--force]`. No other frontmatter keys.
- [ ] `.claude/commands/release-notes.md`'s body declares `## When to run`, `## Inputs`, `## Procedure`, and `## What this command will not do`, in that order.
- [ ] The command's `## What this command will not do` section names "auto-publish", "internal jargon", and "metrics not in" as explicit non-behaviours.
- [ ] The command's last stdout line is exactly `NEXT: /launch-comms <slug>` (Wave-4 post-ship chain continuation).
- [ ] `templates/release-notes.md` exists; passes `tools/lint-frontmatter.py --check-template`.
- [ ] `templates/release-notes.md`'s frontmatter pre-fills `object_type: Customer Communication`, `status: Draft`, `ai_assistance_allowed: restricted`, `human_approval_required: true`. Pre-populates `human_owned_decisions:` with the canonical "Approval of customer-facing claims..." entry.
- [ ] `templates/release-notes.md`'s body has H2s `## What's new` and `## Features in this release` (both required), plus a `## Optional sections` block at the bottom containing `### Known limitations`.
- [ ] `scripts/tests/test_templates_instantiate.py` passes after the new template is added.
- [ ] The command file's `description:` accurately summarises the command in one sentence, ≤ 1024 chars, mentions the two parent paths (handoff packet default, landing optional) and the human-review zone-3 gate.
- [ ] An adversarial-reviewer pass against the spec + plan returns no `block` or `needs-fix` findings (or all surfaced findings are explicitly addressed in this spec).

## Cross-references

- **Consumed by:** the human PM, post-ship. No automated audit consumes it directly today; planned `/audit-landings-debt` (ROADMAP P5.9, planned) may walk `delivery/release-notes/` as adjacent evidence.
- **Consumes:** `templates/release-notes.md` (read at invocation); `tools/lint-frontmatter.py`; `delivery/handoff-packets/<slug>/README.md` (default parent, read-only); `delivery/landings/<slug>.md` (`--from-landing` parent, read-only). Does not consume `templates/handoff-packet/launch-considerations.md` directly.
- **Frontmatter fields owned:** writes `id`, `slug`, `object_type`, `name`, `description`, `owner`, `status`, `created`, `last_updated`, `parent_handoff_packet` OR `parent_landing` (one, not both), `parent_vision`, `parent_initiative`, `ai_assistance_used`, `ai_assistance_allowed`, `human_approval_required`, `human_owned_decisions`. Reads `id`, `slug`, `parent_initiative`, `parent_vision`, `parent_handoff_packet` (from a landing).
- **Ontology object types touched:** writes `Customer Communication` (Domain G atomic). Reads `Handoff Packet` (Domain H) and/or `Landing Report` (Domain I composite).
