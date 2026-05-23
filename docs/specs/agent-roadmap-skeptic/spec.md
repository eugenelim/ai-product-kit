# Spec: agent-roadmap-skeptic

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** agent (specialist reviewer — sibling of `adversarial-reviewer`, `quality-engineer`; NOT a fan-out worker)
- **Serves kit phase:** Phase 4 Delivery (Vision, Initiative, Spec, Handoff Packet — the four Phase-4 artifact types)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md`; `.claude/agents/adversarial-reviewer.md` (canonical specialist-reviewer shape); `.claude/agents/quality-engineer.md` (second specialist-reviewer precedent); `docs/HANDOVERS.md` §"Handover 4" and §"Handover 5"; ROADMAP P4.16.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Defines the `roadmap-skeptic` specialist-reviewer agent: a Phase-4-only review lens that audits the **bets-vs-commitments posture** of a delivery artifact. The agent is invoked by the orchestrator (typically via `/audit-completeness` or the `work-loop` REVIEW phase) against one Phase-4 artifact at a time and returns a structured verdict + categorized findings. It is a sibling reviewer to `adversarial-reviewer` (drift) and `quality-engineer` (operational quality) — it complements them, does not replace them, and does not relitigate their checks.

## Objective

Build `.claude/agents/roadmap-skeptic.md`: the Phase-4 member of the kit's phase-skeptic family (alongside the planned `strategy-skeptic`, `discovery-coach`, `assumption-skeptic`, `landing-skeptic`). The agent reads one Phase-4 artifact — a Vision, Initiative, Spec, or Handoff Packet — and challenges whether each dated promise names an owner, a dependency map, and a falsifiable delivery condition: which dated promises are actually bets, which "requirements" are unvalidated assumptions, which scope items have drifted beyond what the parent Vision's `predicted_outcomes` can justify, which `human_owned_decisions` are still placeholders on an artifact being treated as ready-to-ship, and which dated language lacks an evidence basis. Output is a structured review document (verdict + categorized findings) mirroring `adversarial-reviewer`'s output shape, so the orchestrator can aggregate verdicts across reviewers uniformly.

### Definitions (load-bearing — the agent body MUST cite this block)

- **Commitment.** A dated promise that names (a) an accountable owner, (b) its dependencies (other shipped or planned artifacts whose completion gates this one), and (c) a falsifiable delivery condition (what must be true by when for this to be on-track — observable from existing telemetry, an acceptance-criteria predicate, or a named approval gate).
- **Bet.** A dated promise that lacks any one of {owner, dependency map, falsifiable delivery condition}. A bet is not a defect — it is unavoidable in Phase 4 — but every bet must be flagged so the artifact's commitment posture is honest. The repair is either to upgrade the bet to a commitment by supplying the missing element, or to move the item to `open_assumptions:` with a tier of `accept-as-bet`.

Two invocations of the roadmap-skeptic against the same Phase-4 artifact must produce comparable findings because the bet-vs-commitment classifier is a mechanical predicate, not a taste judgment.

Prior stub context: ROADMAP.md row P4.16 (`roadmap-skeptic` agent — Bets vs commitments lens, slug `agent-roadmap-skeptic`); INVENTORY.md row 155 (planned); AGENTS.md §"Specialist subagents" parenthetical naming the phase-skeptic family.

## Why now

Three of the four canonical Phase-4 artifact types — Vision, Initiative, Spec — and the Phase-4-exit Handoff Packet are now buildable end-to-end via the recently shipped commands (`/draft-vision`, `/draft-initiative`, `/draft-spec`, `/handoff-packet`, `/sequence-initiative`, `/launch-checklist`, `/retro`, etc.). The existing review gates (`/audit-completeness`, `/audit-traceability`, `/audit-spec-linkage`, `adversarial-reviewer`, `quality-engineer`) catch structural completeness, traceability, drift, and operational gaps — but none of them surface the kit's most common Phase-4 failure mode: **dated commitments that are actually bets**. A roadmap that says "we'll ship X by Q3" usually means "we believe we'll ship X by Q3 if these five things go right" — and the kit's phase-4 artifacts inherit that posture unless something challenges it. Without this agent, the kit's Phase-4 review gates can pass an artifact whose every dependency is silently a bet, and the failure shows up only at landing time. Shipping P4.16 closes the phase-skeptic gap for Phase 4 — `strategy-skeptic`, `discovery-coach`, `assumption-skeptic`, and `landing-skeptic` will close the same gap for the other phases.

## Inputs and outputs

**Inputs from the orchestrator.**

- `target_path` — the artifact path. Must resolve to exactly one of these four canonical Phase-4 paths; if it does not, the agent declines (see §Boundaries §Ask first):
  - a Vision file: `delivery/visions/<slug>.md`
  - an Initiative folder: `delivery/initiatives/<slug>/` (the agent reads `README.md` first, then `child-specs.md`, `sequence.md`, `capabilities.md` as needed)
  - a Spec file: `delivery/specs/<slug>/spec.md` (kit-canonical spec location)
  - a Handoff Packet folder: `delivery/handoff-packets/<slug>/` (the agent reads `README.md` first, then `launch-considerations.md`, `risks.md`, `dependencies.md`, `acceptance-criteria.md` as needed)
- `handover_contract_section` — pointer to the relevant section of `docs/HANDOVERS.md`:
  - Vision → Handover 4
  - Initiative → Handover 5
  - Spec → Handover 6
  - Handoff Packet → Handover 6
- `upstream_chain` — the parent artifacts back to the Strategic Intent: parent learning memo, parent vision, parent initiative as applicable. The orchestrator passes paths; the agent reads them to compare child claims against parent commitments. **Unresolvable parents:** if a path in `upstream_chain` does not resolve to a readable file, the agent notes it in the review document as an unresolvable parent, marks every finding that would have required parent-chain reading as "unconfirmed pending parent resolution", and sets `verdict: needs-fixes` minimum (never `pass`). **Absent `upstream_chain`** (null, empty, or omitted by the orchestrator): treat as unresolvable for all §4 / §5 / §8 checks that require parent-chain reading, state this in the Verdict, and cap at `needs-fixes`.
- Optional: prior reviewer output (e.g. `adversarial-reviewer`'s verdict) so the agent can stay out of that lens.

**Outputs to the orchestrator.**

A single review document (returned as the agent's final message; not written to disk by the agent — the orchestrator persists it). The document must start with a YAML frontmatter block:

```yaml
---
reviewer: roadmap-skeptic
target: <artifact path>
date: <YYYY-MM-DD>
verdict: pass | needs-fixes | block
issues_found: <count>
critical_issues: <count>
---
```

Body sections, in this order:

1. **Verdict** — one paragraph naming the verdict and the top reason.
2. **Critical issues** — findings that require backing up to a parent phase. Always-Critical conditions: (a) the parent Vision's `predicted_outcomes` cannot justify the artifact's scope; (b) an `open_assumption` flagged `must-test-before-shipping` in the parent is being treated as settled here without a link to a `status: survived` learning memo. Conditional-Critical: a §6 finding (placeholder `human_owned_decisions:`) escalates into §Critical issues only when the artifact's `human_approval_required: true` lacks a matching `approvals_obtained:` entry; otherwise the finding stays in §6. Each Critical-issues finding cites a specific file and line/section and proposes a concrete fix.
3. **Commitments that are actually bets** — dated promises that fail the three-element commitment predicate from the Definitions block above (missing owner, missing dependency map, or missing falsifiable delivery condition).
4. **Assumptions treated as settled requirements** — scope items whose acceptance criteria assume a learning that hasn't been validated or that the parent Vision listed under `open_assumptions:` without resolution.
5. **Scope beyond parent justification** — Initiative or Spec scope items that the parent Vision's `predicted_outcomes` thresholds cannot justify — or scope that has shrunk below what those thresholds require. Cite the predicted_outcome and the scope item.
6. **Placeholder human_owned_decisions** — `human_owned_decisions:` entries still in template/placeholder form on an artifact whose `status:` or `human_approval_required:` posture implies it is ready for the next phase.
7. **Dated language without evidence basis** — "by end of Q2", "in two weeks", "next quarter", etc., with no link to a learning memo, an evidence basis, or an explicit `accept-as-bet` tag.
8. **Capabilities / Features promised without traced commitment-grounding** — items that name a deliverable capability or feature where the *commitment to deliver* lacks a link to a surviving learning memo or an explicit `accept-as-bet` tag. Applies to `capabilities.md` (Initiative) and `acceptance-criteria.md` (Handoff Packet); for Spec artifacts, apply to the Spec's Acceptance Criteria and walk the parent Initiative's `capabilities.md` via the upstream chain. (Distinct from `adversarial-reviewer`'s "hidden assumption" check: this lens asks specifically whether the *commitment to deliver* is grounded, not whether the *claim about the customer* is. If the commitment is grounded and the customer-claim is ambiguous, stay silent — that is adversarial-reviewer's territory.)

Sections with no findings may be omitted (empty sections are noise). A verdict of `pass` is allowed when no findings exist in any category.

**Finding-repair templates** the agent body must apply:
- For findings in §3 (Commitments that are actually bets): "This is a bet, not a commitment — either supply the missing {owner, dependency map, falsifiable delivery condition}, or move it to `open_assumptions:` with tier `accept-as-bet`."
- For findings in §4–§8: "Cite the resolved learning memo (path), or move the item to `open_assumptions:` with an explicit tier {must-test-before-shipping, accept-as-bet, will-monitor-post-ship}."

**`block` verdict — hard predicates (never require calibration), plus a discretionary block.**
- **Hard `block` predicate 1:** any `open_assumption` from the parent Vision tagged `tier: must-test-before-shipping` that the child artifact treats as settled without a link to a learning memo whose `status: survived` resolves it is *always* a `block`. Not `needs-fixes`.
- **Hard `block` predicate 2 (Draft-Vision early-exit):** a Vision with `status: Draft` (or missing) AND `human_approval_required: true` lacking a matching `approvals_obtained:` entry is *always* a `block`. The agent returns immediately on this case (see §Boundaries §"Ask first" above and the agent body's §"When the orchestrator invokes you").
- **Discretionary `block`:** the artifact's commitment posture cannot be repaired in-place — the parent phase (Vision, Learning, or Strategic Intent) needs to be reopened. Surface that explicitly in the Verdict paragraph.

## Boundaries

### Always do

- Stay in the bets-vs-commitments lens. If a finding doesn't fit one of the six category headings (§3–§8 in §"Outputs to the orchestrator"), it doesn't belong in this review.
- Read the parent chain before judging the child. A scope item that looks unjustified at the Spec level may be fully justified by the parent Vision's `predicted_outcomes` — and the reverse.
- Cite specific files and sections in every finding. Findings without a citation are philosophical observations, not actionable.
- Apply the finding-repair templates declared in §"Outputs to the orchestrator". Repair text is not improvised per finding.
- Return a structured frontmatter block plus categorized sections. The orchestrator aggregates by frontmatter fields, not by free-text.

### Ask first

- Reviewing an artifact whose phase is ambiguous (e.g., a `delivery/visions/<slug>.md` that's clearly still a Phase-3 learning memo dressed up as a Vision). Return a structured `block` verdict naming the phase confusion; the orchestrator decides whether to route to `discovery-coach`/`assumption-skeptic` instead.
- Reviewing a "Phase-4 artifact" that lives outside the four canonical paths above (e.g., a one-off planning doc). Decline cleanly and recommend `adversarial-reviewer` instead.
- Reviewing a Vision with `status: Draft` (or no `status:` field) and no `approvals_obtained:` entry corresponding to its `human_approval_required: true`. A Draft Vision produces a high rate of false-positive §3–§5 findings because `predicted_outcomes:` is typically unfilled and `human_owned_decisions:` typically unresolved. Return a structured `block` naming the incomplete-gate condition and recommend `/audit-completeness` runs first; do not run the bets-vs-commitments lens. (This is one of two hard `block` predicates the agent encodes — see spec §"`block` verdict" below and the agent body's §Hard rules.)
- Receiving a `target_path` that does not resolve to one of the four canonical Phase-4 paths in §Inputs. Decline cleanly and ask the orchestrator to re-resolve; do not pick a closest match.

### Never do

- Modify the artifact. The reviewer's output is a verdict + findings, period. The artifact owner makes the edits.
- Relitigate `adversarial-reviewer`'s drift checks. If the spec drifts from its handover contract, that's the drift reviewer's lens; if asked to dual-purpose, note the drift exists and stay in your lens.
- Relitigate `quality-engineer`'s testability/observability/reliability/maintainability checks. Different lens.
- Auto-approve. The agent's output is a verdict; flipping status to "Approved" / "Ready for Engineering" is the artifact owner's job.
- Override `human_owned_decisions`. The agent flags placeholders and missing entries; it does not pick a side on the underlying decision (pricing, roadmap priority, customer commitment, etc.).
- Run on non-Phase-4 artifacts (strategic intents, OSTs, learning memos, landing reports). Decline and recommend the right reviewer.
- Take a Write or Edit tool. Tools list is read-only: `[Read, Glob, Grep]` — same as `adversarial-reviewer` and `quality-engineer`.

## Verification mode

Two modes, both required:

- **Goal-based check.** `tools/lint-agent.sh .claude/agents/roadmap-skeptic.md` exits 0. This is the mechanical gate — frontmatter shape, required fields, model in {haiku, sonnet, opus}, H1 present.
- **Audit-driven (cross-cutting).** `bash tools/pre-pr.sh` exits 0 (which transitively runs `lint-agent` plus the settings-json tests), and `python3 tools/lint-frontmatter.py --all` exits 0.

A third "manual-gesture" mode is explicitly out of scope for this spec — fixture-based dispatch against a sample Phase-4 artifact would be valuable but is deferred (see Open questions §1). The two automated gates above are sufficient for ship.

## Contract tests

Goal-based:

- `lint-agent.sh` passes on `.claude/agents/roadmap-skeptic.md`. (Frontmatter present and well-formed; required fields `name`, `description`, `tools`, `model` declared; `model` ∈ {haiku, sonnet, opus}; H1 present.)
- `pre-pr.sh` continues to exit 0 after the agent file is added. (No new lint-agent failures introduced; existing kit components still pass.)
- `lint-frontmatter.py --all` continues to exit 0.

Structural (read-and-walk). The agent file must declare these seven required body sections:

1. "When the orchestrator invokes you"
2. "Your inputs"
3. "Your output" — containing the frontmatter block
4. "What you check" — decomposed into the six category headings (§3–§8 from §"Outputs to the orchestrator" above), plus an inline restatement of the Definitions block (Commitment / Bet) load-bearing for §3
5. "What you don't check" — naming `adversarial-reviewer` (drift lens) AND `quality-engineer` (operational quality lens) explicitly, with the boundary stated in both directions
6. "Hard rules"
7. "When this agent is wrong"

Additional structural assertions:

- The agent's `description:` field is ≤ 1024 chars and names *when the orchestrator invokes it* (per `lint-agent.sh`'s rejection of vague "is a helper"-style descriptions).
- The agent's tools list is `[Read, Glob, Grep]` (read-only — same as `adversarial-reviewer`, `quality-engineer`).
- The agent's `model:` is `sonnet` (per `.claude/CLAUDE.md` Defaults — synthesis-shaped review, not cheap fan-out).
- The agent's "Verdict" / "Hard rules" body cites the hard `block` predicate (must-test-before-shipping treated as settled).

## Non-goals

- **Not a drift reviewer.** Spec-vs-handover-contract drift is `adversarial-reviewer`'s lens. If a finding sounds like "the spec says X but the handover contract requires Y", it belongs there, not here.
- **Not a compliance reviewer.** Regulatory, legal, privacy, ethics — these are the planned `compliance-reviewer`'s lens (ROADMAP P6.1).
- **Not a quality-engineer.** Testability, observability, reliability, maintainability of *promises engineering will inherit* — that's `quality-engineer`. The roadmap-skeptic asks whether the *commitment to deliver* is grounded, not whether the *delivered behavior* will be operable.
- **Not a scope-trimmer.** The agent surfaces "this scope item is unjustified by the parent Vision's predicted_outcomes" — it does not decide to cut the scope. That decision is `human_owned_decisions:` territory.
- **Not a phase-1/2/3/5 reviewer.** Strategic intents, OSTs, learning memos, landing reports each have their own (planned) phase-skeptic. Decline cleanly on non-Phase-4 artifacts.
- **Not a writer.** The agent never edits the artifact under review. Output is a review document only, returned via the agent's final message.
- **Not a fan-out worker.** Unlike `traceability-walker` / `competitor-research`, this agent does one artifact per invocation. The orchestrator can dispatch multiple in parallel if it wants portfolio-wide coverage; that orchestration is out of scope here.

## Open questions

1. **Fixture-based contract test.** Should the kit ship a small fixture (a known-bad Phase-4 Vision with planted bets-vs-commitments failures) and a manual-gesture verification that the agent's verdict matches the seeded findings? Deferred to first-usage (the orchestrator dispatching the agent against a real artifact will surface whether the lens lands). Owner: next P4.16 follow-up.
2. **Count-based threshold for `block` vs `needs-fixes`.** This spec defines one hard `block` predicate (must-test-before-shipping treated as settled) but does not name a count-based threshold (e.g., "≥N findings in §3 → block"). Tightening this is deferred — let the first real usages calibrate. Owner: human reviewer (artifact owner / kit author) at first usage.
3. **Aggregation behavior on conflicting verdicts across the reviewer family.** When `adversarial-reviewer`, `quality-engineer`, and `roadmap-skeptic` return different verdicts for the same artifact (e.g., roadmap-skeptic `pass`, adversarial-reviewer `block`), the orchestrator's resolution rule is not stated anywhere in the kit. The conservative rule ("lowest verdict wins") is the obvious default but has not been written down. Cross-cutting; not a roadmap-skeptic-specific question. Owner: kit author; the right home is `docs/HANDOVERS.md` §Handover 6 (where all three reviewers are cited) or a new ADR.
4. **Bets-vs-commitments framing for retros and landings.** A roadmap-skeptic-flavored lens may also be useful at retro/landing time ("which of our shipped commitments turned out to have been bets all along?"). Deferred — `landing-skeptic` (P5.7) is the natural home for that variant, not this agent.

## Acceptance criteria

- [ ] `.claude/agents/roadmap-skeptic.md` exists.
- [ ] `bash tools/lint-agent.sh .claude/agents/roadmap-skeptic.md` exits 0.
- [ ] `bash tools/pre-pr.sh` exits 0.
- [ ] `python3 tools/lint-frontmatter.py --all` exits 0.
- [ ] The agent file declares the seven required body sections (per Contract tests above) AND the six category headings under "What you check" (one per output section §3–§8 in §"Outputs to the orchestrator").
- [ ] The agent file's "What you check" section cites the Definitions block (Commitment / Bet) from this spec verbatim (or near-verbatim) so the bet-vs-commitment classifier is in the agent body, not only in the spec.
- [ ] The agent file's "What you don't check" section explicitly differentiates the lens from `adversarial-reviewer` (drift) and `quality-engineer` (operational quality) by name, including the explicit boundary on §8 (Capabilities) vs adversarial-reviewer's hidden-assumptions check.
- [ ] The agent file's "Hard rules" or "Verdict" section cites the hard `block` predicate (must-test-before-shipping treated as settled).
- [ ] The agent's tools list is `[Read, Glob, Grep]`; model is `sonnet`; description is ≤ 1024 chars and names invocation conditions.
- [ ] ROADMAP.md row P4.16: `[ ]` → `[x]` with `**Shipped:** <date>` appended.
- [ ] INVENTORY.md row 155: "planned (P4.16)" → "shipped <date> (P4.16)" with the Purpose column refreshed to the shipped description.
- [ ] AGENTS.md §"Specialist subagents": the `roadmap-skeptic` annotation in the phase-skeptic parenthetical is shifted from "*(planned — ROADMAP P4.16)*" to a shipped marker (or removed entirely, leaving the other four phase-skeptics still annotated). The four siblings remain "*(planned — ...)*".
- [ ] `spec.md` status flipped to `Shipped (<date>)`.
- [ ] `plan.md` status flipped to `Done (<date>)` with a changelog entry.
- [ ] PLAN-phase commit and EXECUTE/CAPTURE commit pushed to `origin/main`.

## Cross-references

- **Consumed by:** `work-loop` REVIEW phase when the artifact under review is one of {Vision, Initiative, Spec, Handoff Packet}; `/audit-completeness` (orchestrator may dispatch this reviewer alongside `adversarial-reviewer` and `quality-engineer` on Phase-4 artifacts).
- **Consumes:** Reads the target artifact, the parent chain (learning → vision → initiative → spec → handoff-packet), and `docs/HANDOVERS.md` Handovers 4–6 for the relevant contract section. No script shell-outs; no write tools.
- **Frontmatter fields owned:** none directly. Reads (does not write) `predicted_outcomes`, `open_assumptions`, `counter_metrics`, `human_owned_decisions`, `human_approval_required`, `evidence_basis`, `parent_vision`, `parent_initiative`, `parent_learning`, `parent_intent`, `status`.
- **Ontology object types touched:** Vision (D), Initiative (D), Spec (D), Engineering Handoff Packet (Domain I composite), Capability (E), Feature (E), Open Assumption (C), Predicted Outcome (D), KPI (H), Risk (G) — read-only, for analysis.
