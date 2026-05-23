# Spec: cmd-retro

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command (with a small optional template — see §"Inputs and outputs" → "Template question")
- **Serves kit phase:** Delivery → Landings (Phase 4 terminal facilitator; bridges Handover 7 back into Phase 1 Strategy at quarterly cadence)
- **Constrained by:** ROADMAP P4.15; `docs/HANDOVERS.md` §"Handover 7: Engineering → Landings"; `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands" (partial-fit — this is a **facilitator**, not a template-fill command; deviations enumerated in §"Boundaries → Deviations from the Phase-4 template-fill convention"); `.claude/commands/_meta/command-skeleton.md`; `templates/landing-report.md` (F3.10 — `/retro`'s output relates to but does not replace this artifact)

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** This document defines what "done" means for `/retro`. The command's load-bearing behavior is **facilitation, not document production**: it asks five fixed questions in a fixed order, one at a time, and assembles the human's answers into a retro document. The five-question contract is machine-checkable. If a future change collapses the five prompts into a single "tell me how it went" or reorders them, the contract test fails and the spec is violated.

## Objective

`/retro` facilitates a structured five-question retrospective over a recently-shipped initiative — either a Landing Report (post-30-day measurement, the canonical post-ship trigger) or a Handoff Packet (immediate post-ship, before the landing report's 30-day window has elapsed). The command's primary work is **walking the human through five fixed prompts, one at a time, in fixed order**, capturing each answer with explicit confirmation before advancing to the next. The assembled answers become a retro document persisted alongside (or appended to) the relevant landing report.

The five questions are:

1. **What worked?**
2. **What didn't?**
3. **What surprised us?**
4. **What would we repeat?**
5. **What would we change?**

These five, in this order, are the kit's load-bearing retro shape. `/retro` is therefore framed as **a facilitator that incidentally writes a doc**, not as **a doc producer that uses prompts as scaffolding**. The interactivity contract (one question, wait, confirm, next — never batch) is the same load-bearing rule that governs every other Phase-4 walk command (see `.claude/CLAUDE.md` "One clarifying question at a time. Never batch.") — but for `/retro` the rule is the entire product, not a sub-step.

The command exists because the kit's cycle re-enters Strategy after Landings (per `docs/HANDOVERS.md` Handover 7: "landings feed directly into the next `/strategy-refresh`"). Without a structured retro between landing and the next strategy refresh, learnings are lost in the gap. `/retro` is the bridge.

## Why now

ROADMAP row P4.15 is the last unchecked Phase-4 item the `/retro` slug names. The four other Wave-4 commands (P4.12 `/release-notes`, P4.13 `/launch-comms`, P4.14 `/launch-checklist`, this row P4.15 `/retro`) are being authored in parallel as the final Phase-4 wave; once they ship, every Phase-4 ROADMAP row except P4.16 (the `roadmap-skeptic` agent) is checked.

`/retro` unblocks the kit's loop closure: Phase-4 → Phase-5 → Phase-1. Until `/retro` exists, the only post-ship artifact is the Landing Report, which is structured for adoption-metric verdicts (`adopt | fix | kill`) — not for process retrospection ("what did we learn about how we work"). Those are different artifacts with different audiences, and the kit needs both. The Landing Report is consumed by execs (verdict signal); the retro is consumed by the team and the next strategy refresh (process signal).

## Inputs and outputs

### Inputs

1. **The positional arg** — `<slug>`. Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. Names the initiative being retro'd. **Not the slug of the new retro file** (the retro file's path is derived from the input slug — see destination resolution below). This deviates from the Phase-4 template-fill convention where the positional names the *new* artifact.
2. **Optional flag** — `--scope landing|handoff`. Selects which upstream artifact to retro against. Default behavior: prefer a landing report at `delivery/landings/<slug>.md` if one exists; otherwise fall back to a handoff packet at `delivery/handoff-packets/<slug>/`. If neither exists, exit code 2 with the missing pre-condition surfaced.
3. **Optional flag** — `--force`. Permits overwriting an existing retro file at the resolved destination.
4. **Upstream artifact body** — read-only. The command reads the landing report's `verdict:`, `parent_vision:`, `parent_handoff_packet:` (when scope=landing); or the handoff packet's `parent_initiative:` and `engineering_partner:` (when scope=handoff). These pre-fill the retro's mechanical frontmatter; they are **not** surfaced as facilitation prompts (the human is not asked to retype them).

### Outputs

1. **The retro file** — a single markdown file at the resolved destination path (see destination resolution below).
2. **A NEXT chaining hint** on the last line of stdout — see §"Chaining".
3. **An exit code** — see §"Exit codes" within Contract tests CT-6.

The retro file's body contains exactly five H2 sections, in the fixed order above, each holding the human's answer to one of the five questions. The body is the assembled facilitation output; the command does not synthesize, summarize, or analyze the answers. The frontmatter carries traceability links to the upstream artifact (landing report or handoff packet) plus the universal-metadata fields.

### Destination path resolution

Three options were considered; the spec picks option B-sub-1 with rationale:

- **(A) Top-level family** — `delivery/retros/<slug>.md`. **Rejected.** AGENTS.md §"Things you should not do without asking" explicitly names "Don't create new top-level folders" as a guard. Even though `delivery/retros/` is one level down from `delivery/`, introducing a new family without an RFC violates the kit's structure-stability discipline. Also: a retro is per-landing, not a strategy-level cross-cutting artifact, so a sibling family alongside `landings/`, `visions/`, `initiatives/`, `handoff-packets/` is the wrong shape.

- **(B-sub-1) Sibling flat file under existing `landings/` family** — `delivery/landings/<slug>-retro.md` (when scope=landing) or `delivery/handoff-packets/<slug>/retro.md` (when scope=handoff, nested inside the existing packet folder). **Picked.** When scope=landing, the retro sits beside the landing report it retros — same family, same naming root, easily discoverable (`ls delivery/landings/` shows the pair). When scope=handoff, the retro sits inside the packet folder (the packet IS a folder per F3.9), as a sibling of the 22 children. Neither path introduces a new top-level folder. Cross-link discovery is mechanical: glob `delivery/landings/<slug>*` or look inside the packet folder.

- **(B-sub-2) Append to the existing landing report's body** — modify `delivery/landings/<slug>.md` in place by appending a `## Retrospective` section. **Rejected.** The landing report is signed off by named humans (per HANDOVERS-7 `verdict_by:` frontmatter); appending to it after sign-off is silent ontology drift. The retro and the landing report are also conceptually different artifacts with different audiences (exec verdict vs team process); collapsing them into one file loses that distinction. Keeping them as siblings preserves both signals.

**Resolved destination rule:**

- If `--scope landing` (or auto-resolved to landing): write to `delivery/landings/<slug>-retro.md`.
- If `--scope handoff` (or auto-resolved to handoff): write to `delivery/handoff-packets/<slug>/retro.md`. If the handoff packet's folder does not exist, exit code 2.

### Relationship to the Landing Report

**Adjacent, not inside, not replacing.** The retro is a separate sibling file (option B-sub-1). The Landing Report (HANDOVERS-7) is structured for the adopt/fix/kill verdict and metric-vs-prediction comparison — that content stays in the landing report. The retro carries the team-process content (what worked, what didn't, what we'd repeat, what we'd change, what surprised us) — that content lives in the retro file. The two cross-link via frontmatter: the retro's `parent_landing:` points at the landing report (when scope=landing).

### Phase-4 Template-Fill Convention applicability

Partial-fit. `/retro` deviates in three load-bearing ways and conforms in everything else:

- **Conforms:** body H2 structure (When to run / Inputs / Procedure / What this command will not do), kebab-case positional `<slug>` argv shape, `--force` flag semantics, one-question-per-turn interactivity contract, `tools/lint-frontmatter.py` lint gate, NEXT chaining-hint emission, exit-code set {0, 1, 2, 3}.
- **Deviates:** (1) the positional `<slug>` names the *upstream* artifact being retro'd, not the new artifact being written — the new artifact's name is mechanically derived (`<slug>-retro.md` or `<slug>/retro.md`); (2) there is **no parent-artifact resolution loop with numbered-list picker** — the positional already names the upstream, and the `--scope` flag picks landing vs handoff (no auto-detection over multiple candidates); (3) **the template is optional and minimal** — see "Template question" below; the load-bearing content is the five-question facilitator script, not template placeholders.

### Template question

A small `templates/retro.md` is shipped as part of this spec **for symmetry with the rest of Phase-4** (every other Phase-4 command consumes an F3.x template). The template is light: frontmatter block (universal-metadata schema + retro-specific traceability fields) plus five empty H2 sections in the fixed order plus a stub `## Cross-references` H2. **The load-bearing contract is the five-question script in the command body, not the template** — if the template were deleted but the command body's five prompts remained, `/retro` would still satisfy its contract. The template exists to avoid hand-typing the frontmatter and the five H2 headers, and to give `tools/lint-frontmatter.py --check-template` something to lint in CI.

The template is NOT a Domain I composite handover artifact (no new ontology type). The retro document carries `object_type: Decision` (Domain H) — the retro IS a small Decision-class artifact (decisions about what to repeat, what to change), and Domain H's `Decision` type fits without a new ontology entry.

## Boundaries

### Always do

- Ask the five questions in the fixed order: **What worked? → What didn't? → What surprised us? → What would we repeat? → What would we change?**
- Ask **exactly one question per turn**. Wait for the human's answer. Echo the captured answer back. Ask the human to confirm or revise. Only then advance to the next question.
- Use the five questions verbatim (the words above), once at the H2 heading level in the written file, and once as the facilitation prompt. The contract test (see §"Contract tests") greps for the literal heading text.
- Pre-fill mechanical frontmatter (`id:`, `slug:`, `created:`, `last_updated:`, `parent_landing:` or `parent_handoff_packet:`, `parent_vision:`, `object_type: Decision`) before any facilitation prompt.
- After all five answers are captured and confirmed, run `tools/lint-frontmatter.py <written-path>` and surface its exit code.
- Emit the NEXT chaining hint as the last line of stdout.

### Ask first

- If the resolved destination file already exists and `--force` is not set, exit 2 with remediation (do not auto-overwrite, do not auto-rename).
- If the upstream artifact (landing report or handoff packet) cannot be resolved, exit 2; do not invent the upstream.
- If the linter fails post-fill, offer to re-open the relevant section for correction; do not silently leave the file in a known-bad state without surfacing.

### Never do

- **Never batch the five questions into one prompt.** The single most load-bearing rule for this command. A prompt like "Walk me through what worked, what didn't, what surprised you, what you'd repeat, and what you'd change" is a contract violation, even if it elicits the same five answers.
- **Never reorder the five questions.** The order is fixed. "What worked?" comes first because it primes the team for honest reflection on what didn't. "What would we change?" comes last because it's the actionable output the next strategy refresh consumes.
- **Never collapse two questions into a single H2.** Five questions → five H2 sections → five answer blocks. Not four, not six.
- **Never synthesize or summarize the human's answers.** `/retro` is a facilitator. It captures verbatim what the human types. It does not paraphrase, does not bullet-ify a prose answer, does not "improve" the wording. The retro is the human's voice.
- **Never produce metric analysis.** That is the Landing Report's job (HANDOVERS-7 "Predicted outcomes vs actuals" + "Counter-metrics"). The retro does not re-litigate adoption numbers.
- **Never produce customer-facing copy.** That is `/release-notes` (P4.12) and `/launch-comms` (P4.13). The retro is internal team reflection.
- **Never append to the landing report's body in place.** The landing report is signed off; the retro is a sibling file.
- **Never overwrite an existing retro file without `--force`.**
- **Never write a retro file when the linter fails post-fill** without explicit human confirmation (exit 3 — known-imperfect state).
- **Never assume cwd is the repo root.** Resolve repo root via nearest-ancestor-containing-`tools/lint-frontmatter.py`, per the Phase-4 convention.

### Deviations from the Phase-4 template-fill convention

Restated for explicit `Constrained by:` traceability:

- Positional `<slug>` is the **upstream artifact's** slug, not the new artifact's slug. The new artifact's path is derived.
- No multi-candidate parent-resolution numbered-list picker. The positional + `--scope` flag pin the upstream deterministically.
- Template is optional / minimal; the load-bearing contract is the in-command five-question script. The convention's "consume a kit-provided F3.x template" step is satisfied technically, but the template is not the primary artifact's mold.

These deviations are intentional. The convention exists for **artifact-creating template-fill commands**. `/retro` is a **facilitator that incidentally writes**, which is a different shape. The deviations are documented here and re-stated in `## What this command will not do` in the implementation, per the convention's own "Authoring a new in-scope command" guidance about declaring deviations.

## Verification mode

**Mixed: goal-based check (primary) + audit-driven (secondary).**

- **Goal-based check (primary):** the contract tests below pass — `tools/lint-command.sh` exits 0 on `.claude/commands/retro.md`; a grep-based contract test confirms the implementation body contains exactly five distinct prompt blocks in the fixed order; `tools/lint-frontmatter.py --check-template templates/retro.md` exits 0 (if the template is shipped).
- **Audit-driven (secondary):** when `/retro` runs against a fixture initiative with a real landing report, the resulting `delivery/landings/<slug>-retro.md` file passes `tools/lint-frontmatter.py` (default mode). This is the same gate the Phase-4 template-fill commands use.

**Not TDD.** The component is a slash-command markdown file plus an optional template markdown file; there is no Python module to write red/green/refactor tests against. The contract tests are filesystem-level (lint exit codes + grep-based shape checks).

**Not manual gesture (alone).** A manual gesture (record a fresh-session run against a fixture) is a useful supplementary check but is not the gate — the five-question contract is machine-checkable (grep the body for the five literal heading strings, in order), so the gate is mechanical.

## Contract tests

Black-box tests that define "done." Stable against implementation change; evolve only with spec change.

### CT-1: command lints clean

`tools/lint-command.sh .claude/commands/retro.md` exits 0. Implies: YAML frontmatter delimited by `---`; `description:` field present and ≤ 1024 chars; H1 begins with `/`; body declares `## When to run` or `## Procedure`.

### CT-2: five literal question headings, in fixed order

A grep-based check against `.claude/commands/retro.md` confirms the body contains, in this order, all five of the literal strings (as H2 headings AND/OR as quoted prompt strings — the implementation's choice, but each must appear at least once with the exact wording):

1. `What worked?`
2. `What didn't?`
3. `What surprised us?`
4. `What would we repeat?`
5. `What would we change?`

The check fails if any of the five is missing, if any appears out of order (relative to the others), or if the body contains a meta-prompt batching them (e.g., a single prompt block listing all five).

Concrete test form: a shell test (`scripts/tests/test_cmd_retro_contract.sh`, or embedded in `tools/pre-pr.sh`) that runs `grep -n` for each of the five literals and asserts the line numbers are strictly ascending.

### CT-3: five H2 sections in the written artifact's structure

The template (`templates/retro.md` if shipped) AND the implementation's described written-file structure both declare five H2 sections with the exact heading text from CT-2. The contract test asserts:

- Template file (if shipped): `grep -c '^## What' templates/retro.md` returns 5.
- Implementation body: the documented "the written file will contain five H2 sections" enumeration in `.claude/commands/retro.md`'s Procedure step lists all five headings verbatim.

### CT-4: implementation declares the one-question-at-a-time contract

The implementation body explicitly states, in prose, that the five questions are asked one at a time, never batched, in the fixed order, with confirmation between each. Grep the implementation for the strings `one at a time` (or `one per turn`) and `never batch` (the kit's canonical phrasing from `.claude/CLAUDE.md`). Both must appear.

### CT-5: implementation declares the upstream-pin behavior

The implementation body documents the `--scope landing|handoff` flag, the default behavior (prefer landing if present, else handoff), and the destination paths (`delivery/landings/<slug>-retro.md` and `delivery/handoff-packets/<slug>/retro.md`). Grep the implementation for both destination-path templates.

### CT-5b: implementation documents the both-candidates exit-2 path

The implementation body (within `## Procedure` Step 1 or `## Exit codes` section) explicitly names the case where both `delivery/landings/<slug>.md` AND `delivery/handoff-packets/<slug>/` exist and `--scope` is absent — and declares the exit-2 behaviour ("demand `--scope <landing|handoff>`; do not auto-pick"). Grep contract: `grep -c "both" .claude/commands/retro.md` returns ≥ 1 AND the body contains the literal string "demand `--scope`" (or equivalent unambiguous "require `--scope`" wording). Catches the regression where an executor reads the spec's default-resolution rule ("prefer landing if both exist") and turns it into silent auto-pick.

### CT-6: implementation declares the four explicit exit codes

The body's `## Exit codes` (or equivalent) section names exit 0, 1, 2, 3 with the convention's semantics: 0 = success; 1 = human aborted mid-walk; 2 = pre-conditions failed; 3 = post-fill linter exited non-zero and human declined re-open.

### CT-7: template (if shipped) lints clean

`tools/lint-frontmatter.py --check-template templates/retro.md` exits 0 (per the F3 template authoring convention).

### CT-8: implementation declares the NEXT chaining hint shape

The implementation body's Procedure step that emits NEXT shows the literal expected output line. See §"Chaining" — the chain terminates with a NEXT line naming `/strategy-refresh` as the cadence-level (not auto-chained) successor.

## Non-goals

- **Does NOT produce metric analysis** — adoption curves, KPI vs threshold, counter-metric comparisons. That content lives in the Landing Report (HANDOVERS-7).
- **Does NOT produce customer-facing copy** — release notes, launch announcements, blog posts. Those live under `/release-notes` (P4.12) and `/launch-comms` (P4.13).
- **Does NOT produce a verdict** — `adopt | fix | kill` is the Landing Report's `verdict:` frontmatter, decided by named humans (HANDOVERS-7). The retro is process-reflection, not disposition.
- **Does NOT auto-resolve the upstream artifact across multiple candidates.** The positional `<slug>` plus optional `--scope` flag pins the upstream deterministically. If `<slug>` matches both a landing and a handoff (e.g., `delivery/landings/foo.md` exists AND `delivery/handoff-packets/foo/` exists), `--scope` is **required** — exit 2 otherwise. This deviates from the convention's numbered-list picker, which is correct for that command class but wrong here.
- **Does NOT synthesize or summarize the human's answers.** The retro is verbatim capture.
- **Does NOT auto-invoke `/strategy-refresh` or any successor command.** The NEXT line names `/strategy-refresh` for discoverability; the human runs it on a cadence decision, not as part of this run.
- **Does NOT call `/audit-portfolio-coherence` or any other audit.** The retro is local to one initiative; portfolio audits are quarterly-cadence concerns.
- **Does NOT bump any sibling artifact's `last_updated:`.** Unlike `/draft-spec` (which bumps the parent Initiative's README) and the augmenting commands (which bump the Initiative's README), `/retro` writes a sibling file only. The upstream Landing Report is signed off and should not be touched.

## Open questions

- **OQ1 (defer until first usage):** should the retro file's `object_type:` be `Decision` (Domain H, as proposed) or a new Domain I composite (`Retro` or `Retrospective`)? Domain I is reserved for phase-boundary handover artifacts (HANDOVERS-1 through HANDOVERS-7); a retro is post-Handover-7 reflection, not a phase boundary itself. The conservative choice is `Decision`. If adopters surface that `Decision` is the wrong shape for `/audit-traceability`'s walk, RFC a new Domain I type. **Who answers:** the kit author + first adopter, after first real use.
- **OQ2 (defer until first usage):** should `/retro` support a multi-participant facilitation mode (i.e., the human running `/retro` is a facilitator capturing answers from a team meeting, not a single PM answering for themselves)? The current spec assumes single-participant — one human answers all five questions. Multi-participant would change the prompts ("What did X think worked?" instead of "What worked?"). **Defer until** the first adopter reports the single-participant mode produces shallow retros for team-shipped initiatives.
- **OQ3 (defer until P7.1 ships):** when `/strategy-refresh` (P7.1) ships, should `/retro`'s NEXT line name it conditionally (e.g., "if more than three retros have accumulated since the last strategy refresh, run `/strategy-refresh`")? The current spec emits an unconditional terminal-chain NEXT line. **Defer until** P7.1 lands and the cadence-driven retro→strategy feedback loop has a real definition.
- **OQ4 (now):** should `/retro` enforce a minimum time-since-ship before allowing scope=landing? HANDOVERS-7 requires `measured_at` ≥ 30 days post-ship for the landing report itself; the retro presumably shouldn't run earlier. **Resolution:** check is delegated to the upstream artifact's existence — if the landing report exists, its `measured_at` was already validated when it was written. `/retro` does not re-validate the 30-day window; it trusts the upstream artifact's sign-off. Documented here so a future reviewer doesn't add the check redundantly.
- **OQ5 (now):** should the retro file carry `human_approval_required: true`? Landings and Visions do. **Resolution:** no — the retro is reflection, not a decision requiring sign-off. The frontmatter declares `human_approval_required: false`. Adopters can override per-artifact if their org requires team-lead sign-off on retros.

## Acceptance criteria

A reviewer reads this list and decides whether to approve a PR. Each criterion is verifiable.

- [ ] `.claude/commands/retro.md` exists with frontmatter `description:` and `argument-hint: <slug> [--scope landing|handoff] [--force]`.
- [ ] `tools/lint-command.sh .claude/commands/retro.md` exits 0.
- [ ] The implementation body contains the five literal question strings, in order, each at least once: `What worked?`, `What didn't?`, `What surprised us?`, `What would we repeat?`, `What would we change?`. Grep-based ordering check (CT-2) passes.
- [ ] The implementation body explicitly declares the "one question at a time, never batch" interactivity contract (CT-4).
- [ ] The implementation body documents the `--scope landing|handoff` flag, the default-resolution rule (prefer landing if present), and both destination paths (CT-5).
- [ ] The implementation body documents the both-candidates exit-2 case (when both landing and handoff exist for `<slug>` and `--scope` is absent, demand `--scope`, do not auto-pick) (CT-5b).
- [ ] The implementation body documents exit codes 0, 1, 2, 3 with the convention's semantics (CT-6).
- [ ] The implementation body's NEXT line declares the chain terminates (CT-8).
- [ ] If `templates/retro.md` is shipped: it contains five H2 sections with the exact heading text from CT-2, in order; `tools/lint-frontmatter.py --check-template templates/retro.md` exits 0 (CT-3, CT-7).
- [ ] The spec's deviations from the Phase-4 template-fill convention (positional names upstream, no candidate-picker, light template) are restated in the implementation's `## What this command will not do` section so a reader sees them without consulting the spec.
- [ ] No new top-level folder is created under `delivery/`. Destination paths use existing `delivery/landings/` and `delivery/handoff-packets/<slug>/` only.
- [ ] No INVENTORY.md or ROADMAP.md edits happen during the PLAN phase of this spec (those are CAPTURE-phase concerns, out of scope here).

## Cross-references

- **Consumed by:** humans, post-ship, on a per-initiative cadence. No automated callers; `/retro` is a terminal Phase-4 facilitator. Future: `/cadence-check` (P7.5, planned) may surface "retros owed" the way `/audit-landings-debt` (P5.9, planned) surfaces landing reports owed.
- **Consumes:** `templates/retro.md` (if shipped — optional minimal template); `tools/lint-frontmatter.py` (gate); `delivery/landings/<slug>.md` (read-only, when scope=landing); `delivery/handoff-packets/<slug>/README.md` (read-only, when scope=handoff).
- **Frontmatter fields owned:** the retro file's `object_type: Decision`, `parent_landing:` or `parent_handoff_packet:`, `parent_vision:` (transitive carry-through), `human_owned_decisions:` (the five answers themselves are human-authored content; the field captures any explicit decisions the retro surfaces, e.g., "stop doing X").
- **Ontology object types touched:** Decision (Domain H) — the retro IS a Decision-class artifact (decisions about repeat / change). Reads but does not write: Landing Report (Domain I composite, HANDOVERS-7), Handoff Packet (Domain H), Vision (Domain I composite, HANDOVERS-4) — all read-only for transitive frontmatter carry-through.

## Chaining

The NEXT chaining hint formatted exactly:

```
NEXT: /strategy-refresh (planned — ROADMAP P7.1; Phase-4 chain ends here, the kit re-enters Phase 1 Strategy on a cadence decision, not an auto-chain)
```

This is a terminal-but-discoverable NEXT line. `/retro` is the end of the Phase-4 chain; the kit's cycle continues by re-entering Phase 1 Strategy on a quarterly cadence, but that transition is human-decided, not command-chained. The NEXT line names the cadence vehicle (`/strategy-refresh`) for discoverability and surfaces its planned status per the kit-drift policy.

No `REVIEW:` line is emitted (only `/sequence-initiative` emits a REVIEW interstitial).
