# Spec: cmd-launch-checklist

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command (Phase-4 post-ship operational-artifact slash command; **NOT** a member of the Phase-4 Template-Fill convention family — see §"Convention applicability" below)
- **Serves kit phase:** Delivery (post-Handover 6, pre-Handover 7) — produces the operational artifact that gates the move from "Handoff Packet ready for engineering" to "code is actually launchable for this change type"
- **Constrained by:** `docs/HANDOVERS.md` §"Handover 6" (the parent Handoff Packet whose `launch-considerations.md` child is this command's primary input) and §"Handover 7" (the Landing Report this command's output feeds into); `templates/handoff-packet/launch-considerations.md` (the THREE-section pricing/support/comms one-pager the checklist consumes and **extends**, not duplicates); `templates/launch-checklist/` (the F4.14 per-change-type folder template this command will ship alongside — authored under a separate template spec at EXECUTE time but pinned here by shape and per-file content rules); `.claude/commands/_meta/command-skeleton.md` (the skeleton this command file copies, with **declared deviations** for the change-type-keyed Step 3 walk and the operational-artifact argv shape — see §"Convention applicability" and §"Deviations from command-skeleton"); `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands" (explicitly **declared non-applicable** — the convention's own scope note in lines 256–257 excludes the nine post-ship P4.x items, naming `/launch-checklist` among them); `.claude/commands/handoff-packet.md` (P4.11 — produces the parent Handoff Packet whose slug is this command's positional argument); `.claude/skills/work-loop/SKILL.md` (the build pattern this spec follows); `.claude/CLAUDE.md` "one clarifying question at a time. Never batch." (the interactivity contract); ROADMAP P4.14 (the row this spec satisfies).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `.claude/commands/launch-checklist.md` — a change-type-aware operational-artifact slash command (P4.14) that takes a Handoff Packet slug, asks (or accepts via `--change-type`) which of four change-type lenses to apply (`new-feature` | `breaking-change` | `pricing` | `regulated`), copies the corresponding per-change-type template from `templates/launch-checklist/<change-type>.md` to `delivery/handoff-packets/<slug>/launch-checklist.md`, walks the checklist items interactively (one item at a time — never batch), records per-item `confirm | note | not-applicable` plus a free-text note, runs `tools/lint-frontmatter.py` (default mode) against the written artifact, and emits `NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5.x)` as the chain hint. The checklist **extends** `launch-considerations.md` (does not duplicate it): launch-considerations is the one-paragraph-per-section narrative summary; the checklist is the actionable per-item gate with change-type branching. The two coexist as siblings under the same Handoff Packet folder.

## Objective

`/launch-checklist <handoff-packet-slug>` is the slash command that turns the Handoff Packet's `launch-considerations.md` narrative one-pager into an actionable change-type-specific checklist artifact written at `delivery/handoff-packets/<handoff-packet-slug>/launch-checklist.md`. The problem it solves: today, a kit user has a Handoff Packet whose `launch-considerations.md` child summarizes pricing, support, and comms in three short paragraphs (per `templates/handoff-packet/launch-considerations.md`) — but that file is intentionally a **narrative summary**, not an operational gate. Launching a breaking API change requires a different checklist than launching a pricing change, which requires a different checklist than launching a regulated workflow change, which requires a different checklist than launching a generic new feature. A single one-size-fits-all checklist with change-type metadata bolted on would either be too long for any single launch (every item gated by an "if change-type == X" mental filter) or too thin (lowest-common-denominator items only). The kit's answer: **four change-type-keyed templates**, each a focused 10–13-item checklist, and a slash command that picks one per launch.

The command is the natural Phase-4 → Phase-5 (Landings) bridge for the operational dimension: the Handoff Packet (P4.11) is the *content* engineering consumes; the Launch Checklist (P4.14) is the *operational gate* engineering and PM clear together before the code is actually launchable; the Landing Report (P5.x) is the *post-launch verdict* on whether the change earned its place. The checklist's filled artifact carries the per-item confirmations that prove the kit user actually walked the change-type-specific risks — not just the generic ones.

The closest prior context is the F4 Template-Fill Commands convention (`docs/specs/phase-4-command-convention/spec.md`) — whose body-shape contract the command **deviates from in declared ways** (Step 3 walks per-checklist-item not per-H2; argv carries a `--change-type` flag absent from the convention; positional names a handoff-packet slug not a new-artifact slug) — and `.claude/commands/handoff-packet.md` (P4.11), whose written packet is this command's input. The four sibling post-ship commands (P4.12 `/release-notes`, P4.13 `/launch-comms`, P4.15 `/retro`) are being authored in parallel under their own per-command specs; this spec does not pin their shape, but the four post-ship commands together form the kit's post-Handover-6 operational layer.

## Why now

ROADMAP P4.14 sits in the Phase-4 post-ship block — the four commands (P4.12–P4.15) that produce the operational artifacts engineering and PM produce *after* the Handoff Packet is signed off and *before* the Landing Report is filed. P4.11 (`/handoff-packet`) shipped 2026-05-23, so the parent artifact this command extends (`templates/handoff-packet/launch-considerations.md`) is stable and its three sections (pricing & packaging, support & operational readiness, communications & rollout) are pinned. Until this command ships, kit users wanting to clear a change-type-specific launch gate must either (a) hand-write a checklist from scratch each launch, (b) re-use a single generic checklist that under-covers regulated/breaking changes, or (c) treat `launch-considerations.md` itself as the gate — which it is not designed to be (its three sections are narrative paragraphs, not actionable items).

P4.14 also seeds the kit's **post-ship operational vocabulary** for the four change types. Once the four templates ship (`templates/launch-checklist/new-feature.md`, `breaking-change.md`, `pricing.md`, `regulated.md`), the kit has named, content-distinguished checklists that other components (the future P4.13 `/launch-comms` command; the P5.x Landing Report's "what we cleared at launch" section) can reference by typed identifier. Without the four files, the kit's post-ship discipline stays informal.

## Convention applicability

**The Phase-4 Template-Fill Commands convention (`docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands") is explicitly NOT applicable to this command.** The convention's own scope note (lines 256–257) says: *"The other nine ROADMAP P4.x items (analytical commands, audits, comms commands, the retro facilitator, the EARS-lint skill, the roadmap-skeptic agent) are out of scope; they ship under their own per-item specs."* P4.14 `/launch-checklist` is one of those nine. The four reasons `/launch-checklist` cannot conform to the convention:

1. **Positional argument names the *parent artifact*, not a new artifact's slug.** The convention's argv contract requires the positional to be a new-artifact slug (artifact-creating sub-class) or an initiative slug (artifact-augmenting sub-class). `/launch-checklist`'s positional is a **handoff-packet slug** — the parent Handoff Packet that owns the destination folder. The destination filename (`launch-checklist.md`) is fixed by the destination-path resolution rule, not derived from the positional.
2. **Step-3 walk is per-checklist-item, not per-H2 placeholder.** The convention's "Interactive fill" rule says "walk the template's placeholders one H2 section at a time." Per-change-type templates ship a single H2 (`## Checklist`) whose body is a markdown checkbox list; the command walks the list **items**, one per turn, asking confirm/note/not-applicable per item. The convention's per-H2 walk rule does not fit this content shape.
3. **A `--change-type` flag is required and absent from the convention's argv set.** The convention's flag set is `{--from, --force}` only. `/launch-checklist` adds `--change-type new-feature|breaking-change|pricing|regulated` (when absent, the command asks).
4. **No `id:` pre-fill.** The artifact is not a typed ontology object with a `<TYPE>-<NNN>` id form; it is an operational sibling-child of the Handoff Packet, identified by its containing folder.

The command **does honor** the convention's *non-controversial* discipline: one question at a time, never batch, confirm `human_owned_decisions:`, run `tools/lint-frontmatter.py` against the written artifact, emit a `NEXT:` chain hint, and the four-code exit-code contract (`0`/`1`/`2`/`3`). Deviations are limited to the four numbered items above.

## Deviations from command-skeleton

Per `.claude/commands/_meta/command-skeleton.md`, the skeleton's Step 1 (resolve parent) and Step 2 (instantiate template at destination) are **specialized** for this command:

- **Step 1** resolves the parent **Handoff Packet** (not an Initiative or Vision). The candidate filter is `delivery/handoff-packets/*/README.md` whose `status:` is not in the terminal-or-killed set (`Deprecated`).
- **Step 2** asks for / accepts the `--change-type` value **before** copying the template. The template path is `templates/launch-checklist/<change-type>.md` — a different file per change type.
- **Step 3** walks the checklist items, not H2 placeholders (per §"Convention applicability" #2 above).

The four required H2 sections of the skeleton (`## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`) are retained verbatim. The `argument-hint:` frontmatter is `<handoff-packet-slug> [--change-type new-feature|breaking-change|pricing|regulated] [--force]` (positional named explicitly — not `<slug>` or `<initiative-slug>`, because neither is the right token).

## Relationship to `launch-considerations.md`

**The checklist EXTENDS `launch-considerations.md`.** Decision recorded explicitly here so a reader of either file can tell which is the gate and which is the narrative summary.

- `launch-considerations.md` is the **narrative one-pager** the Handoff Packet ships with: three short paragraphs (pricing & packaging, support & operational readiness, communications & rollout) per the F3.9 template. It is read at engineering handoff time as part of the packet; it answers "what does engineering need to know about how this thing will land."
- `launch-checklist.md` is the **operational gate** produced post-handoff, change-type-aware: 10–13 actionable items the kit user walks one at a time, recording per-item confirmation. It answers "have we actually cleared the change-type-specific risks before the launch lever is pulled."

The two are **siblings** under the same `delivery/handoff-packets/<slug>/` folder. The relationship is one-way: the checklist's prompts (see §"Per-change-type checklist items" below) explicitly cite `launch-considerations.md` as context (e.g., "Pricing checklist item 2: the grandfathering policy is recorded in `launch-considerations.md` §Pricing and packaging — confirm the policy is filled and signed off by the pricing decision owner cited in `human-owned-decisions.md`"), so a kit user filling the checklist re-reads the narrative summary as input. The narrative summary does **not** cite the checklist back — `launch-considerations.md` is fixed by F3.9 and remains the same three-section one-pager for every Handoff Packet, regardless of which change type the launch ultimately uses.

Alternatives considered and rejected:

- **Duplicate** — copy launch-considerations content into the checklist. Rejected: creates drift between the two; doubles maintenance.
- **Replace** — checklist becomes the operational artifact; `launch-considerations.md` becomes a stub. Rejected: HANDOVERS-6 explicitly names `launch-considerations.md` as a Handoff Packet child; stub-ifying it would silently degrade the engineering-handoff content. The narrative summary has its own readers (engineering at handoff time) distinct from the checklist's readers (PM/engineering at launch time).
- **Orthogonal** — the two have no declared relationship. Rejected: leaves the kit user guessing which is the gate. Explicit "extend" is the lower-friction answer.

## Destination path resolution

**Decision: option (B) — nested under the Handoff Packet folder at `delivery/handoff-packets/<slug>/launch-checklist.md`.**

Rationale:
- HANDOVERS-6 §"Folder contents" already names `launch-considerations.md` as a Handoff Packet child. The Handoff Packet is the canonical home for all launch-related operational artifacts for a single shipped change; adding `launch-checklist.md` as a sibling preserves the "one folder = all artifacts for this shipped change" rule.
- The positional argument is a **handoff-packet slug**, not a new-artifact slug. Nesting the destination under the named packet eliminates an ambiguity-window where two checklists with different slugs but the same packet might disagree on which packet they bind to.
- Option (A) — `delivery/launch-checklists/<slug>.md` as a new top-level family — adds a 14th top-level `delivery/` family for a single artifact per launch, which is structurally heavier than the artifact's load justifies. It also forces a new slug-naming convention for launch checklists distinct from the Handoff Packet slug, creating a 1:1 mapping the file system already encodes for free under option (B).

Trade-off acknowledged: option (B) means the launch checklist is filed under the Handoff Packet folder *after* the packet is sealed for engineering (the README's four `*_review_passed:` audit-gate fields are flipped). The Handoff Packet's `last_updated:` field will need to bump when the checklist is added, even though no other packet content changed. The command handles this in Step 6 (bump the packet README's `last_updated:` only; the parent Initiative's `README.md` is **not** touched).

## Inputs and outputs

**Inputs.**

1. Positional argument `<handoff-packet-slug>` — kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars, names an existing Handoff Packet folder at `delivery/handoff-packets/<handoff-packet-slug>/`. Per §"Convention applicability" #1, the positional names the parent, not a new slug.
2. Optional flag `--change-type new-feature|breaking-change|pricing|regulated` — selects which per-change-type template to copy. If absent, Step 2 of the command asks the human interactively (one question; the four options listed). The four values map 1:1 to the four files under `templates/launch-checklist/`.
3. Optional flag `--force` — permits overwriting an existing `delivery/handoff-packets/<slug>/launch-checklist.md`. Without `--force`, an existing destination causes exit 2.
4. `templates/launch-checklist/<change-type>.md` — the per-change-type single-file template the command copies. Four files: `new-feature.md`, `breaking-change.md`, `pricing.md`, `regulated.md`. Each ships frontmatter (universal-schema superset; `object_type: Launch Checklist` (proposed — see Open Question 6)) plus a single `## Checklist` H2 whose body is the change-type-specific checkbox list.
5. `delivery/handoff-packets/<slug>/README.md` — the parent Handoff Packet's frontmatter. Read for `parent_initiative:`, `parent_vision:`, `parent_intent:`, `status:`. The packet's `status:` must not be `Deprecated`; if it is, the command exits 2.
6. `delivery/handoff-packets/<slug>/launch-considerations.md` — the narrative one-pager the checklist extends. Read for **citation context** during the interactive walk; checklist item prompts reference its three sections by name where applicable. If the file is missing or still placeholder-shaped, the command's behaviour is **change-type-conditional**:
   - For `--change-type new-feature` or `--change-type pricing`: surface a **non-blocking warning** ("the parent Handoff Packet's `launch-considerations.md` still holds placeholders — checklist items that cite it may be hard to confirm; continuing") and proceed.
   - For `--change-type breaking-change` or `--change-type regulated`: surface a **blocking prompt** that requires explicit human confirmation before proceeding. Rationale: breaking-change items cite `launch-considerations.md §Communications and rollout` for deprecation timing and rollout cadence; regulated items cite the same section for customer-disclosure routing. Running these checklists against placeholder-shaped `launch-considerations.md` produces unconfirmable items at scale, which is checklist-theatre.
7. `delivery/handoff-packets/<slug>/risks.md` — read for risk-driven checklist items (especially in `breaking-change` and `regulated` templates, which cross-reference risk ids).
8. `delivery/handoff-packets/<slug>/requirements.yaml` — read for requirement-citation context in checklist items that name specific REQ-NNN ids (especially in `regulated`'s policy-compliance items).
9. `tools/lint-frontmatter.py` — default-mode linter the command runs against the written checklist artifact. Default mode walks `PHASE_DIRS = ["strategy", "discovery", "validation", "delivery", "market"]` so `delivery/handoff-packets/<slug>/launch-checklist.md` is in scope.

**Outputs.**

1. `.claude/commands/launch-checklist.md` — the new slash-command file. Body follows `.claude/commands/_meta/command-skeleton.md` with the four declared deviations above. Frontmatter declares `description:` (≤ 1024 chars; one sentence) and `argument-hint: <handoff-packet-slug> [--change-type new-feature|breaking-change|pricing|regulated] [--force]`.
2. `delivery/handoff-packets/<handoff-packet-slug>/launch-checklist.md` — the instantiated artifact. Filled frontmatter (`object_type: Launch Checklist` (proposed — see Open Question 6), `parent_handoff_packet: <slug>`, `parent_initiative:`/`parent_vision:`/`parent_intent:` carried from the packet README, `change_type: <selected>`, `created:`, `last_updated:`, plus `human_owned_decisions:` with the change-type's canonical decisions, `approvals_obtained:` collected during Step 4). Body is the change-type-specific checklist with each item walked, per-item confirmation (`[x]` for confirmed, `[ ]` for not-yet, `[~]` for not-applicable with rationale required), and per-item free-text note inline beneath.
3. `delivery/handoff-packets/<handoff-packet-slug>/README.md` — `last_updated:` bumped to today's date (Step 6 side-effect). No other field on the packet README is touched.
4. Stdout — interactive prompts, per-item confirmations, linter report, chain hint. Last line exactly `NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5.x)` (the chain successor is not yet shipped; kit-drift policy mandates the `(planned — ROADMAP …)` annotation). The line is followed in stdout by a one-line commentary: "After the landing report is filed (measured at T+30d), run `/retro <slug>` for the team-process retrospective." This makes `/retro` (P4.15) discoverable as the cadence-level successor to the landing report; the chain does not auto-invoke either command.
5. Exit code — one of `0` (success), `1` (human aborted), `2` (pre-conditions failed), `3` (lint failed post-write and human declined to re-open).

A reader of this section can construct the command's interface signature without reading anything else.

## Per-change-type checklist items

The four per-change-type templates ship under `templates/launch-checklist/`. Each is a single-file template with universal-schema frontmatter and a single `## Checklist` H2 whose body is the change-type-specific checkbox list. The four template files are authored **under this spec's plan (Task 0)**, not a sibling spec; this section pins the content (items per change type) verbatim, and the plan's Task 0 mandates verbatim copy.

**Important: the four lists are intentionally distinguishable**, not a single union list with change-type metadata bolted on. Per the supervisor brief: "the change-type-keyed checklist MUST actually branch by change-type (different items for breaking-change vs pricing vs regulated). NOT a single one-size-fits-all list."

### `new-feature.md` (10 items)

The generic-launch checklist. Items address: feature flag, documentation, success-metric instrumentation, observability, support readiness, beta cohort, rollback, internal comms, customer comms (light-touch), post-launch retro.

1. Feature-flag wired and tested in staging; flag default is OFF for non-beta cohort.
2. User-facing docs published (help center / in-product) and discoverable from the feature surface.
3. Success-metric instrumentation (per `success-metrics.md`) is live and validated against a known event in staging.
4. Observability dashboard names the feature and its key counters / SLO targets; alert thresholds are committed.
5. Support team briefed; FAQ + escalation path documented; on-call coverage confirmed for first 72h.
6. Beta cohort (≤ 5% rollout) selected and named; cohort selection criteria recorded in `launch-considerations.md` §Communications and rollout.
7. Rollback plan: feature flag is the kill switch; named owner for the rollback decision; rollback drill performed in staging.
8. Internal comms (engineering + customer-facing teams) scheduled at T-3 days with the named copy.
9. Customer comms (light-touch — blog or in-product banner) drafted and routed to the named approver per `human-owned-decisions.md`.
10. Post-launch retro scheduled at T+14 days with named facilitator; metric-review meeting separately scheduled at T+30 days.

### `breaking-change.md` (12 items)

The "we are intentionally breaking something existing customers depend on" checklist. Distinguishing items address: deprecation notice timing, customer migration tooling, sunset date commitment, support runbook for the deprecation window, comms cadence (T-90/T-30/T-7), per-segment customer outreach for high-impact accounts, version-skew compatibility window, dependency-team coordination (SDK clients), API change-log entry, customer-success ticket tagging strategy, named rollback-or-stop-the-bleeding owner with paging contract, post-deprecation cleanup audit.

1. Deprecation notice published with named sunset date; sunset date is ≥ 90 days from notice (or rationale for shorter window recorded in `decision-log.md`).
2. Customer migration tooling published (script, codemod, in-product wizard, or guided runbook); the tooling is tested against a representative sample of customer data.
3. Per-segment customer outreach completed for the high-impact accounts named in `customer-segment.md`; outreach record (date + customer-side acknowledgment) logged in the Handoff Packet folder (free-text appendix or linked CRM record).
4. Communications cadence committed: T-90 announcement, T-30 reminder, T-7 final notice. Copy drafted and routed for all three; first send-date recorded.
5. Version-skew compatibility window confirmed: the old and new behaviors coexist for the full deprecation window (or a documented exception with risk-acceptance signature in `human-owned-decisions.md`).
6. Dependency-team coordination completed: every team consuming the deprecated surface (SDK clients, mobile apps, partner integrations per `dependencies.md`) has a named contact who has acknowledged the deprecation timeline.
7. API change-log entry (or equivalent versioned-contract entry) published; the entry cites the deprecation rationale and the named sunset date.
8. Customer-success ticket tagging strategy in place: tickets mentioning the deprecated behavior auto-tag with `<feature>-deprecation-2026` (or equivalent) so support sees aggregate volume.
9. Support runbook for the deprecation window: stock answers for "why is this changing," "what do I do," "can I get an extension"; named on-call coverage for the deprecation window.
10. Rollback-or-stop-the-bleeding owner named with paging contract; rollback is realistically scoped (full revert is often infeasible mid-window — name the actual recovery path).
11. Post-deprecation cleanup audit scheduled: at T+30-post-sunset, confirm the deprecated surface is actually removed (not just hidden) and that no customers still depend on it.
12. Legal / compliance review confirmed if the deprecated behavior was part of a contractual commitment to specific customers; sign-off recorded under `approvals_obtained:`.

### `pricing.md` (11 items)

The "we are changing how customers pay" checklist. Distinguishing items address: pricing-decision-owner sign-off (an area where AI must never be the final owner per HUMAN-AI-OWNERSHIP.md), grandfathering policy for existing customers, billing-system change validation, finance team sign-off, customer-segment comms timing (existing vs new), sales-team enablement, support ticket triage policy for pricing complaints, revenue-impact forecast review, comms to investor relations if material, A/B test gate if testing price elasticity, contract-customer renegotiation list.

1. Pricing decision owner (a named human, never AI per `docs/HUMAN-AI-OWNERSHIP.md`) has signed off on the new pricing model; signature recorded in `human-owned-decisions.md` and mirrored in `approvals_obtained:`.
2. Grandfathering policy explicit: which existing customers (by segment, contract type, or join-date) keep the old pricing, for how long, under what conditions; policy recorded in `launch-considerations.md` §Pricing and packaging.
3. Billing-system change validated end-to-end: a test transaction at the new price succeeds; a test transaction for a grandfathered customer succeeds at the old price.
4. Finance team sign-off on revenue-impact forecast and on the accounting treatment of the change; sign-off recorded under `approvals_obtained:`.
5. Customer comms timeline: existing customers notified ≥ 30 days before change (or contractual notice window, whichever is longer); new customers see the new price from day one. Both sets of copy drafted and routed.
6. Sales-team enablement: pricing FAQ, objection-handling guide, and updated quote templates distributed; sales lead has confirmed receipt.
7. Support ticket triage policy for pricing complaints: stock answer, escalation path (named person), discount-authority limits (do front-line reps have a "save the customer" lever, and what is its dollar ceiling).
8. Revenue-impact forecast reviewed against a sensitivity range (best / base / worst); the worst-case impact is acceptable per the named decision owner.
9. Investor-relations comms drafted if the pricing change is **material** (per the org's definition of materiality, not the kit's); IR sign-off recorded if applicable, or "not material" recorded with rationale.
10. A/B test gate: if the change is being tested rather than launched in full, the test's success/falsification thresholds are predeclared (per the kit's `assumption-threshold-lock` discipline) and recorded in the linked experiment artifact.
11. Contract-customer renegotiation list: every customer with a contract that names a specific price has a renegotiation owner and target close date; the list is closed (no "TBD" customers) before launch.

### `regulated.md` (13 items)

The "this change touches a regulated workflow" checklist. Distinguishing items address: legal/compliance sign-off (mandatory, not optional), regulator notification timing, audit-log instrumentation for the regulated workflow, evidence-of-controls documentation, data-handling per the relevant regulatory regime (GDPR, HIPAA, SOC 2, PCI-DSS, etc.), retention-policy review, breach-notification runbook, third-party processor list update, customer-disclosure language review, internal-audit pre-review, regulatory-change-log entry, sunset of any non-compliant prior behavior, named compliance-officer accountability.

1. Legal / compliance sign-off recorded (named human, not AI per `docs/HUMAN-AI-OWNERSHIP.md`); sign-off names the specific regulatory regime(s) the change interacts with. Recorded in `human-owned-decisions.md` and `approvals_obtained:`.
2. Regulator notification timing confirmed if the regime requires advance notification (e.g., financial-services pre-launch filings); filing reference number recorded.
3. Audit-log instrumentation: the regulated workflow's user-facing actions emit audit events with the regulator-required fields (actor, action, timestamp, affected record id, before/after state where applicable); a test event is verified end-to-end in staging.
4. Evidence-of-controls documentation: the change's control-design rationale is documented under `policy-constraints.md` or a linked controls-evidence file; the documentation is in the format the org's compliance team will surface in the next audit cycle.
5. Data-handling compliance: PII / PHI / cardholder data classifications confirmed; the change does not expand the data-classification scope without compensating controls; classification recorded in `non-functional-requirements.md` §Data.
6. Retention-policy review: data the change creates is subject to the named retention policy (e.g., 7-year retention for financial records); retention configuration verified in staging.
7. Breach-notification runbook updated: in the event of a breach involving the change's data surface, the named runbook step ("who to call, what to say, in what timeframe per the regulation's notification deadline") is current.
8. Third-party processor list updated if the change introduces a new sub-processor; customer-facing sub-processor list and any DPAs (Data Processing Agreements) updated.
9. Customer-disclosure language reviewed by legal: privacy notice, terms-of-service, in-product disclosures all reflect the change; review record cited under `approvals_obtained:`.
10. Internal-audit pre-review completed: the org's internal-audit function has reviewed the change (or has explicitly waived the review with rationale); waiver, if used, is recorded.
11. Regulatory-change-log entry filed: the org's internal regulatory-change tracker has an entry for this launch with the named regime(s) and effective date.
12. Sunset of any non-compliant prior behavior: if the change brings something into compliance, the non-compliant behavior is removed (not just supplemented); removal verified.
13. Named compliance-officer accountability: a specific named compliance officer (not "the compliance team") is on the hook for the change's regulatory posture for the first 90 days post-launch; name recorded in `human-owned-decisions.md`.

**Why the four lists are distinguishable, not unioned.** The breaking-change items 1–4 (deprecation timing, migration tooling, per-segment outreach, comms cadence) are nonsensical for a `new-feature` launch (there's nothing to deprecate). The pricing items 1–2 (pricing decision owner, grandfathering policy) are nonsensical for a `breaking-change` API deprecation (no price changed). The regulated items 1, 9, 13 (legal sign-off, customer-disclosure review, compliance-officer accountability) are not items every launch needs — applying them to a generic new feature would create checklist-theatre. The four-template structure forces the kit user to pick the lens, then walk only the items that actually matter for that change type.

A launch can be multi-typed (e.g., breaking-change + pricing in the same release); the v1 behavior is to run `/launch-checklist` twice with different `--change-type` values, writing two checklist files. The destination filename (`launch-checklist.md`) means the second run requires `--force` and overwrites the first. **Open question 1 below** considers whether to support a multi-type composite mode.

## Interactivity contract

The interactive walk has three phases inside Step 3, all subject to the kit's "one question at a time, never batch" rule:

1. **Change-type confirmation** (one prompt) — asked only if `--change-type` was not supplied. Format: "Which change type is this launch? Choose one: `new-feature`, `breaking-change`, `pricing`, `regulated`. (Pick the lens most applicable; multi-type launches run the command once per type.)" The chosen value pins which template file is copied.
2. **Per-item walk** (10–13 prompts, one per item). For each checkbox item in the chosen template's `## Checklist` H2, in source order:
   - Echo the item text verbatim.
   - Ask: "Confirm, note, or mark not-applicable? (Reply `confirm` to mark `[x]`; `note: <text>` to mark `[ ]` with an inline note explaining what's blocking; `n/a: <rationale>` to mark `[~]` with a rationale.)"
   - Record the response inline: `[x]` for confirm, `[ ]` for note (with the note text indented two spaces under the item), `[~]` for not-applicable (with the rationale indented two spaces under the item).
   - Confirm the recorded line back to the human before advancing to the next item.
3. **`human_owned_decisions:` confirmation** (one prompt per entry). Read the chosen template's `human_owned_decisions:` frontmatter list (each per-change-type template ships its own canonical list — e.g., for `pricing`, the canonical entries include "Pricing model sign-off" and "Grandfathering policy approval"). For each entry, ask the human to confirm the decision is owned by a named human and (where applicable) signed off. Update `approvals_obtained:` inline-list entries as the human dictates.

Step 3 is not skippable. A `--non-interactive` mode is explicitly out of scope (see §"Boundaries → Ask first").

## Side effects on the parent Handoff Packet README

On exit 0 only, Step 6 of the command bumps `delivery/handoff-packets/<slug>/README.md`'s `last_updated:` field to today's date. The bump is mechanical (sed-style replacement of the date string). No other packet README field is touched. The bump records that the packet's folder content changed (a new sibling child was added) without re-opening the packet's audit-gate fields.

The parent **Initiative** README (`delivery/initiatives/<initiative-slug>/README.md`) is **not** touched. The checklist is a sibling of the packet, not of the initiative; the initiative's `last_updated:` is decoupled from per-launch operational artifacts by design.

On exit 1, 2, or 3, the packet README is **not** bumped (the command's success is a precondition for the bump). This is the same posture `/draft-spec` uses for its `child-specs.md` append (no append on exit 3).

## Boundaries

### Always do

- Walk the checklist items **one at a time** — never batch. Restates the kit's `.claude/CLAUDE.md` "one clarifying question at a time" rule mechanically.
- Ask for `--change-type` interactively if not supplied; never silently pick a default. The four options are listed in the prompt verbatim.
- Resolve the parent Handoff Packet's `status:` against the terminal-or-killed set before proceeding; refuse if the packet is `Deprecated`.
- Cite `launch-considerations.md` as context in any checklist item that references its three sections; the citation is part of the per-item prompt verbatim, not an aside.
- Resolve the repo root as the nearest ancestor of the working directory containing `tools/lint-frontmatter.py`; do not assume the working directory is the repo root.
- Bump the parent Handoff Packet `README.md`'s `last_updated:` to today's date on success (exit 0). No other packet README field is touched.
- Emit the `NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5.x)` hint on success. The `(planned …)` annotation is mandatory per the kit-drift policy until the successor ships.

### Ask first

- Adding any change-type beyond the four pinned in this spec. The four (`new-feature`, `breaking-change`, `pricing`, `regulated`) are a load-bearing typology choice; adding a fifth (e.g., `security-patch`, `removal`) requires a per-spec deviation note and a corresponding new template file.
- Pre-filling any checklist item's `[x]` confirmation based on inference from the parent Handoff Packet content. The kit's "Not fabricate evidence" discipline applies — confirmations are human acts, not AI inferences.
- Adding a `--non-interactive` mode that fills the checklist from the packet's frontmatter without walking items. The interactivity contract is load-bearing here; bypassing it produces checklist-theatre.
- Walking items from a different change-type template after one has been selected. The selection is final per run; multi-type composite mode is the §"Open question 1" outcome.
- **Before overwriting an existing `delivery/handoff-packets/<slug>/launch-checklist.md` with `--force`, surface the existing file's confirmed items to the human and ask them to confirm the overwrite is intentional.** Rationale: a `breaking-change + pricing` multi-type launch runs the command twice with different `--change-type` values; the second run's `--force` destroys the first run's per-item confirmations (legal/compliance sign-off, per-segment outreach, etc.). Silent overwrite is data loss. The command MUST echo the existing file's `[x]`-confirmed items, the existing `change_type:`, and the existing `approvals_obtained:` list, then ask: "Confirm overwrite? The above per-item confirmations and approvals will be lost." Refuse on `no`; proceed on `yes`.

### Never do

- Pre-fill checklist items with `[x]` confirmations. The artifact's value is the per-item human walk; pre-filled confirmations destroy the artifact's purpose. **This is the load-bearing design decision of this spec.**
- Touch `launch-considerations.md` from inside this command. The narrative one-pager is owned by F3.9; the checklist extends it but does not write to it.
- Run `/landing-report` automatically as part of this command's success path. The chain hint names it; the human runs it next.
- Modify `templates/launch-checklist/` from inside the command. The per-change-type templates are frozen by the sibling template spec.
- Add a new ontology type beyond `Launch Checklist`. The Launch Checklist type is added by the sibling template spec; this command instantiates it but does not introduce a second new type.
- Silently pick a change-type when `--change-type` is absent. Always ask.
- Silently overwrite an existing `delivery/handoff-packets/<slug>/launch-checklist.md` without `--force`.

## Verification mode

- **Goal-based check** — the command file at `.claude/commands/launch-checklist.md` passes `bash tools/lint-command.sh`; the file declares the four required H2s (`## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`); the `argument-hint:` frontmatter starts with the literal `<handoff-packet-slug>` token (not `<slug>` or `<initiative-slug>`); the body cites `templates/launch-checklist/` and the path exists at EXECUTE time; the body cites `delivery/handoff-packets/` and the directory exists; the NEXT line is exactly `NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5.x)`.
- **Manual gesture** — from a fixture Handoff Packet (with at least a filled README and `launch-considerations.md`), invoke `/launch-checklist <fixture-slug> --change-type breaking-change` in a Claude Code session; verify the destination file is created at `delivery/handoff-packets/<fixture-slug>/launch-checklist.md`; verify the 12 breaking-change items are walked one at a time; verify the linter ran in default mode against the written artifact; verify the parent packet's README `last_updated:` was bumped; verify the NEXT line is exact. Recorded in this spec's `notes/manual-gesture.md` at CAPTURE phase.
- **Audit-driven** — no kit audit consumes the checklist directly in v1. The Landing Report (P5.x) will reference it; until that command ships, the checklist's verification is the manual gesture only.

The command is **not** verified by a runtime-behavior simulation in pytest — the command's body is a prose procedure for Claude Code to follow interactively, not a runnable Python entry-point. Same posture as the seven P4 template-fill commands.

## Contract tests

- `T1` — `test -f .claude/commands/launch-checklist.md` (the command file exists at EXECUTE-end).
- `T2` — `bash tools/lint-command.sh .claude/commands/launch-checklist.md` exits 0 (passes the generic command-shape linter).
- `T3` — `grep -cE "^## (When to run|Inputs|Procedure|What this command will not do)" .claude/commands/launch-checklist.md` returns 4 (the four required H2s are present).
- `T4` — `grep -cE "^argument-hint: <handoff-packet-slug>" .claude/commands/launch-checklist.md` returns 1 (the operational-artifact positional is declared, not the template-fill convention's `<slug>`).
- `T5` — `grep -c "templates/launch-checklist/" .claude/commands/launch-checklist.md` returns ≥ 1 AND `test -d templates/launch-checklist` (the cited template directory exists at EXECUTE-end).
- `T6` — `grep -c "delivery/handoff-packets/" .claude/commands/launch-checklist.md` returns ≥ 1 AND `test -d delivery/handoff-packets` (the destination family directory exists).
- `T7` — `grep -c "^NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5\\.x)$" .claude/commands/launch-checklist.md` returns ≥ 1 (the chain hint is present in the documented exact form, with the `(planned …)` annotation per kit-drift policy).
- `T8` — `grep -cE "(new-feature|breaking-change|pricing|regulated)" .claude/commands/launch-checklist.md` returns ≥ 4 (the four pinned change-type values appear in the command body).
- `T9` — `grep -c "launch-considerations.md" .claude/commands/launch-checklist.md` returns ≥ 1 (the relationship to launch-considerations is cited in the command body).
- `T10` — `grep -c "_meta/command-skeleton.md" .claude/commands/launch-checklist.md` returns 0 (the command file does NOT reference the skeleton path inside its own body — the skeleton is a copy-source, not a runtime reference).
- `T11` — `bash tools/pre-pr.sh` exits 0 (no regression on kit-wide health).
- `T12` — `grep -cE "^- \\[ \\] \\*\\*P4\\.14\\*\\*" ROADMAP.md` returns 1 at PLAN-phase time (the P4.14 row is still unchecked; flips to `[x]` at CAPTURE phase only).
- `T13` — at EXECUTE-end, `test -f templates/launch-checklist/new-feature.md && test -f templates/launch-checklist/breaking-change.md && test -f templates/launch-checklist/pricing.md && test -f templates/launch-checklist/regulated.md` (the four per-change-type template files exist).
- `T14` — at EXECUTE-end, for each of the four template files: `grep -cE "^## Checklist" templates/launch-checklist/<change-type>.md` returns 1 (each template has exactly one `## Checklist` H2).
- `T15` — at EXECUTE-end, numbered-item counts match this spec: `grep -cE "^[0-9]+\\." templates/launch-checklist/new-feature.md` returns 10; `breaking-change.md` returns 12; `pricing.md` returns 11; `regulated.md` returns 13.

## Non-goals

- Pre-filling checklist items with `[x]` confirmations from the parent Handoff Packet's frontmatter. Out of scope by design (load-bearing — see §"Boundaries → Never do").
- Running `/landing-report` automatically. Out of scope; the chain hint names it; the human runs it next.
- ~~Authoring the four per-change-type template files inside this spec.~~ **Updated 2026-05-23:** the four templates ARE authored under this spec's plan (Task 0), not under a separate sibling spec. This corrects the original spec author's "phantom sibling spec" assumption, which the cross-cutting PLAN-phase review flagged. The content is still pinned by spec §"Per-change-type checklist items"; the template author honours the pinned items verbatim.
- Modifying `templates/handoff-packet/launch-considerations.md`. Out of scope; F3.9 owns it.
- Modifying `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, or the F4 Template-Fill convention. Out of scope; the convention's own scope note excludes this command.
- Supporting multi-type composite mode (a single checklist file that unions items from multiple change types). Out of scope for v1; deferred to Open Question 1.
- Adding a fifth change-type beyond the four pinned. Out of scope for v1; deferred to Open Question 2.
- Authoring the `/landing-report` command (P5.x). Out of scope; named only as the NEXT chain target.
- Adding a `--dry-run` flag. Per the F4 convention's OQ1 (parallel question deferred there), and consistent in this spec.

## Open questions

1. **Should the command support a multi-type composite mode (e.g., `--change-type breaking-change,pricing` produces one checklist file with items from both)?** _Resolved-for-v1: no. v1 supports one change-type per run; a multi-type launch runs the command twice with different `--change-type` values, the second with `--force`, overwriting the first. Rationale: the v1 use case is the simple single-lens launch; multi-type launches are rare enough to defer the composite UX until a real adopter requests it. Re-open once the kit has ≥ 3 logged multi-type launches (track in the kit's adoption notes)._
2. **Should the command add `--change-type security-patch` or `--change-type removal` as a fifth/sixth lens?** _Deferred. Decision criterion: an adopter ships ≥ 2 launches that genuinely don't fit one of the four pinned lenses. Until then, security-patch lives under `regulated` (its compliance overlap) or `breaking-change` (its customer-impact overlap), and removal lives under `breaking-change`._
3. **Should the command refuse to run when the parent Handoff Packet's four `*_review_passed:` audit-gate fields are still at their placeholder values (i.e., the packet is not yet sealed for engineering)?** _Resolved here: no. The checklist is the operational gate post-handoff; running it pre-handoff is non-standard but not destructive. Surface as a non-blocking warning: "the parent Handoff Packet's audit gates are not all passed — running the launch checklist on an unsealed packet may be premature." Proceed if the human says yes._
4. **Should the command append a row to a centralized launch-log file (e.g., `delivery/launch-log.md`)?** _Deferred. A centralized launch-log is a separate cross-launch artifact, not a per-launch one; it can be derived from `delivery/handoff-packets/*/launch-checklist.md` by a downstream `/audit-launches` command (not on the roadmap). Adding it inside this command's contract conflates per-launch and cross-launch concerns._
5. **Should the four per-change-type templates be a single-file template with H2-keyed sections (`## new-feature`, `## breaking-change`, …) or a folder?** _Resolved here: **folder**, four files. Rationale: each template's frontmatter declares `change_type: <type>`, so per-file frontmatter is correct (single-file would force a synthetic frontmatter or omit it). Walking a single H2 per file is also simpler than walking a single H2 within a multi-H2 file. The folder structure also lets a future fifth template (open question 2) ship as a new file without touching the existing four._
6. **`Launch Checklist` ontology type — proposed, pending RFC.** The kit's ontology (`context/frameworks/ontology.md`) does not list `Launch Checklist` as an atomic type in Domain H today. The closest existing types are `Decision` (Domain H — fits the "operational sign-off artifact" semantics, also used by `/retro` per P4.15) and `Launch Plan` (Domain G — "activities to release and promote"). This spec ships `object_type: Launch Checklist` as a **proposed** value in the four template files' frontmatter, mirroring P4.13's "proposed `Launch Communication`" pattern. The supervisor MUST flag this for an RFC trigger; the RFC's resolution (a) adds `Launch Checklist` as a Domain H atomic type and the template frontmatter is correct, or (b) re-types the artifact as `Decision` and the four template files plus the command's pre-fill rule update accordingly. Resolution before EXECUTE-end is preferred; if deferred, the templates ship with the proposed value and the RFC lands in the CAPTURE batch.
7. **Does adding `launch-checklist.md` after the parent Handoff Packet's audit gates are passed require re-running `/audit-completeness`?** _Resolved here: no. The packet's `last_updated:` bump is metadata-only; the four `*_review_passed:` audit-gate fields are not re-opened. The audit-completeness checklist (ontology §41) does not name `launch-checklist.md` as a gated artifact — so adding it post-seal is additive, not state-changing. If a future revision of `/audit-completeness` adds the checklist to its 25-item walk, this open question is re-opened. Documented here so a future reviewer doesn't add the re-audit step redundantly._

## Acceptance criteria

- [ ] `.claude/commands/launch-checklist.md` exists at EXECUTE-end with the body shape specified above (the four required H2s plus the per-step refinements declared in §"Deviations from command-skeleton").
- [ ] `argument-hint:` frontmatter is exactly `<handoff-packet-slug> [--change-type new-feature|breaking-change|pricing|regulated] [--force]`.
- [ ] `description:` frontmatter is one sentence, ≤ 1024 chars, and accurately summarizes the command's behavior including the change-type-aware nature.
- [ ] The body cites `templates/launch-checklist/` as the consumed template family and `delivery/handoff-packets/` as the destination family.
- [ ] The body declares the parent-artifact-resolution rule: candidates from `delivery/handoff-packets/` filtered by `status:` not equal to `Deprecated`; empty list → exit 2 with a remediation message naming `/handoff-packet` as the prerequisite.
- [ ] The body documents the four pinned change-type values and their 1:1 mapping to the four template files.
- [ ] The body documents the relationship to `launch-considerations.md` as **extend** (not duplicate / replace / orthogonal).
- [ ] The body documents the four-code exit-code contract (`0`, `1`, `2`, `3`) verbatim per the parent skeleton.
- [ ] The body's last documented output line is exactly `NEXT: /landing-report <handoff-packet-slug> (planned — ROADMAP P5.x)`.
- [ ] All contract tests pass: T1–T15.
- [ ] No F3.9 template modified (specifically `templates/handoff-packet/launch-considerations.md` is untouched); no `tools/` script modified; no `docs/HANDOVERS.md` or `docs/CONVENTIONS.md` modified.
- [ ] `state.json.plan_review_status` is `pending` at PLAN-phase exit (per supervisor brief; flips to `approved` only after cross-cutting adversarial review).

## Cross-references

- **Consumed by:** kit users running `/launch-checklist <handoff-packet-slug>` interactively in Claude Code post-Handover-6. Downstream chain: `/landing-report <handoff-packet-slug>` (planned — ROADMAP P5.x). The filled `launch-checklist.md` artifact is also referenced by the P5.x Landing Report's "what we cleared at launch" section.
- **Consumes:** `templates/launch-checklist/` (sibling per-template spec — four single-file templates), `templates/handoff-packet/launch-considerations.md` (read as citation context per §"Relationship to launch-considerations.md"), `delivery/handoff-packets/` (family directory for parent resolution), `tools/lint-frontmatter.py` (default mode), `.claude/commands/_meta/command-skeleton.md` (copy-source, with declared deviations).
- **Frontmatter fields owned:** the written `launch-checklist.md` declares `object_type: Launch Checklist` (proposed — see Open Question 6), `change_type:`, `parent_handoff_packet:`. The `Launch Checklist` ontology type is proposed here as a new Domain H atomic (Decision-adjacent operational artifact); RFC-pending. The four template files ship the proposed value; the command instantiates it.
- **Ontology object types touched:** Launch Checklist (instantiated; **proposed new Domain H atomic type — RFC-pending per Open Question 6**). Handoff Packet (Domain H, read for parent resolution). Risk (Domain G, read for `breaking-change` and `regulated` risk-driven items). Requirement (Domain E, read for `regulated` policy-compliance items). Decision (Domain H, read implicitly — the per-item confirmations are kit-recognized Decision-adjacent records).
