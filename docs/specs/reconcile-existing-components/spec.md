# Spec: reconcile-existing-components

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** guide (kit-meta maintenance pass; not a new primitive)
- **Serves kit phase:** Meta (kit itself)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md` (loop doctrine); `docs/CONVENTIONS.md` (universal metadata); `ROADMAP.md` (the queue this work feeds)

> **Spec contract.** This document defines what "done" means for the inaugural reconcile-and-harden pass. The implementing work must match this spec, or update it in the same session. Verification must be derivable from this spec — if a behavior isn't here, it isn't promised.

## Objective

This spec covers a single, bounded maintenance pass that does two things to the kit's CURRENTLY-EXISTING surface:

1. **Reconcile doc-vs-reality drift**, without erasing forward-looking design intent. Doc text that names a kit component (skill, agent, command, hook, framework ref, doc) which doesn't yet exist on disk gets annotated with a `(planned — see ROADMAP)` marker AND ensured-present as a ROADMAP entry. Nothing is silently deleted. Plus: convert `CLAUDE.md` from a duplicate file into a symlink to `AGENTS.md` (currently it is a byte-identical duplicate; this is asserted by AGENTS.md line 3 and README line 30).
2. **Adversarially review the components that DO exist on disk** — 3 skills (`work-loop`, `ost-validator`, `strategy-coherence`), 2 agents (`adversarial-reviewer`, `competitor-research`), 5 commands (`audit-completeness`, `audit-portfolio-coherence`, `audit-traceability`, `competitive-research`, `phase-guide`), 1 hook (`assumption-threshold-lock`), and core docs (CHARTER, CONVENTIONS, HANDOVERS, HUMAN-AI-OWNERSHIP, INVENTORY, PHASE-GUIDE, architecture/overview), `context/frameworks/ontology.md`, and `context/README.md`. The 2 ADRs are reviewed read-only and tracked in a separate "Read-only" section of the verdicts log. Address every `block`-verdict reviewer finding in-pass; address or explicitly defer (with ROADMAP entry) every `needs-fixes` finding per Task E.

The drift fix protects every future agent from acting on poisoned context. The review hardens the foundations the rest of the ROADMAP will sit on.

## Why now

The repo's own AGENTS.md says: "AGENTS.md-vs-reality drift is the biggest cause of agent-quality decay." The repo is ~3 days old and the drift is already substantial: AGENTS.md lists 7 skills (4 don't exist), 8+ agents (6 don't exist), phase-guard hooks (don't exist), and 2 index READMEs (don't exist). Continuing to build ROADMAP items on top of a drift-poisoned context guarantees the kit will compound its own confusion.

This pass blocks no roadmap items but unblocks confidence in every subsequent one. It also produces and validates the kit's first real work-loop artifact, which is itself a meta-verification of the loop's tooling.

## Inputs and outputs

**Inputs.**
- `AGENTS.md` (canonical agent context, ~157 lines)
- `CLAUDE.md` (currently a byte-identical duplicate of AGENTS.md)
- `.claude/CLAUDE.md` (Claude-Code-specific overlay)
- `docs/INVENTORY.md` (forward-looking inventory of all promised primitives)
- `README.md`
- `ROADMAP.md` (the authoritative queue; assumed correct)
- All on-disk components listed above (skills, agents, commands, hook, core docs, ontology)
- The `adversarial-reviewer` subagent definition (`.claude/agents/adversarial-reviewer.md`)
- The work-loop SKILL (`.claude/skills/work-loop/SKILL.md`)
- The feedback memory `feedback-kit-drift-handling` (demote-don't-delete rule)

**Outputs.**
- `CLAUDE.md` → symlink pointing to `AGENTS.md`
- Edited `AGENTS.md` with planned-markers on every reference to an unbuilt primitive
- Edited `INVENTORY.md` with a `Status` column or per-row planned-marker convention, so readers can distinguish shipped from planned
- Edited `README.md` with planned-markers where it asserts an unbuilt primitive (specifically the quickstart references context files that don't exist as files yet)
- Edited `.claude/CLAUDE.md` with planned-markers where it asserts an unbuilt primitive (the `ontology-classifier` skill reference and any others)
- New `.claude/skills/README.md` (one-line index per existing skill, planned-markers for ROADMAP-listed skills)
- New `.claude/agents/README.md` (one-line index per existing agent, planned-markers for ROADMAP-listed agents)
- Edits to existing components per reviewer findings triaged as block/needs-fix
- An updated `ROADMAP.md` with check-marks against any items shipped in this pass (the two READMEs) and any new items surfaced by reviewer deferrals
- An updated `state.json` (frozen for the session) showing all phase gates passed
- This `spec.md` marked `Shipped`; the `plan.md` marked `Done`

A reader reading just `AGENTS.md`, `INVENTORY.md`, `README.md`, `.claude/CLAUDE.md`, and the two new READMEs should be unable to find a single confident reference to an unbuilt primitive that isn't tagged with the planned-marker convention.

## Boundaries

### Always do

- Apply the `feedback-kit-drift-handling` rule on every doc-vs-reality discrepancy: demote (mark planned) and link to ROADMAP; never delete the reference.
- Before annotating any item as planned, verify it appears in `ROADMAP.md`. If absent, add it under the appropriate Foundation/Phase section. If present, leave the roadmap row alone.
- Use one consistent planned-marker convention across all edited docs (proposed: `(planned — see [ROADMAP](path-to-ROADMAP.md#anchor))` inline, or a Status column for tables). The chosen convention is declared in `plan.md` Task B.1 and used uniformly.
- Run the `adversarial-reviewer` subagent on each existing component using the lenses defined in `.claude/agents/adversarial-reviewer.md` §4.
- Run `tools/check-done.py` at each phase gate (plan, verify, review) before transitioning.

### Ask first

- Building any *new* primitive beyond the two READMEs explicitly named in scope. The two READMEs are in scope because AGENTS.md treats them as canonical indexes and their absence is the drift, not a missing roadmap item. Any other new component requires a separate spec.
- Modifying `AGENTS.md` substantively (changing source-of-truth wording, restructuring sections, rewriting principles). Per AGENTS.md §"When this file is wrong": substantive changes go through an RFC. Annotating planned-markers and fixing the symlink claim are non-substantive; deeper edits are not. Surface, don't decide.
- Changing the `ROADMAP.md` ordering or adding/removing items beyond what reviewer findings or the demote pass surfaces.
- Editing any inspiration doc (`docs/inspiration/*.md`). Those are imported source material, not kit-authored content.

### Never do

- Delete a reference to an unbuilt primitive. (Demote-and-annotate only.)
- Create a stub file for an unbuilt primitive just to make the doc reference resolve. (That's the opposite failure mode — false-positive existence.)
- Build a new skill, agent, command, hook, script, or framework reference. The two index READMEs are the only new files this pass creates. Reviewer findings that demand new primitives become ROADMAP rows, not in-pass work.
- Modify any file under `docs/inspiration/`, `templates/`, `tools/`, or `.github/`. Out of scope.
- Add or modify hooks. The kit has one hook today; the rest are roadmap items.
- Touch `~/.ssh`, `.env*`, credential paths, or push to any remote.

## Verification mode

Goal-based check + audit-driven, mixed:

- **Goal-based check (drift):** A grep-based scan over the four edited docs (`AGENTS.md`, `INVENTORY.md`, `README.md`, `.claude/CLAUDE.md`), `context/README.md`, and the two new READMEs MUST find zero unannotated references to the explicit unbuilt-primitive list in §"Contract tests" below. The scan is the mechanical gate.
- **Goal-based check (symlink):** `[[ -L CLAUDE.md ]]` returns true; `readlink CLAUDE.md` returns `AGENTS.md`; `diff CLAUDE.md AGENTS.md` returns empty.
- **Audit-driven (component review):** Each in-scope existing component receives an `adversarial-reviewer` verdict of `pass` or `needs-fixes` — `block` findings escalate per the work-loop. `needs-fixes` findings are addressed in-pass or deferred to ROADMAP with a recorded rationale. For docs that lack a formal handover contract (the core docs, ontology ref, context/README.md), the reviewer is dispatched with the variant prompt "review against the component's own stated purpose" — see plan Task D.1 for the exact dispatch shape.
- **Audit-driven (linters):** `tools/lint-skill.sh`, `tools/lint-agent.sh`, `tools/lint-command.sh`, and `tools/lint-frontmatter.py` return exit 0 on every touched file *to which the linter applies*. Scope clarification:
    - `lint-skill.sh` applies to the 3 SKILL.md files under `.claude/skills/<name>/`.
    - `lint-agent.sh` applies to the 2 files under `.claude/agents/`.
    - `lint-command.sh` applies to the 5 files under `.claude/commands/`.
    - `lint-frontmatter.py` walks only `strategy/`, `discovery/`, `validation/`, `delivery/`, `market/` (see `PHASE_DIRS` in the script) — it does NOT walk `docs/specs/`, `.claude/`, the repo root, or `context/`. So this spec/plan, the two new READMEs, and CLAUDE.md/AGENTS.md/README.md are NOT in its scope.
    - `tools/lint-hook.sh` does not exist; `assumption-threshold-lock.md` is exempt from automated linting. Reviewer findings on it are addressed or deferred per Task E. Adding `lint-hook.sh` is out of scope and surfaced as a ROADMAP candidate during Task E.

## Contract tests

The mechanical gate. These are the things a verifier walks.

**Drift-scan checklist** — `grep` for each token below across `AGENTS.md`, `INVENTORY.md`, `README.md`, `.claude/CLAUDE.md`, `.claude/skills/README.md`, `.claude/agents/README.md`. Every hit must either be (a) inside a fenced code block describing it as planned, (b) annotated inline with the planned-marker, or (c) inside a section/row whose header marks the whole block as planned (e.g., INVENTORY's Status column).

Skills currently absent: `voice-check`, `dates`, `ears-lint`, `ontology-classifier`, `interview-snapshot`, `opportunity-clustering`, `experiment-template`, `wardley-evolution`.

Agents currently absent: `compliance-reviewer`, `quality-engineer`, `strategy-skeptic`, `discovery-coach`, `assumption-skeptic`, `roadmap-skeptic`, `landing-skeptic`, `interview-coder`, `opportunity-merger`, `experiment-designer`, `paper-summarizer`, `cohort-analyst`, `section-fact-checker`, `writing-critic`.

Hooks currently absent: `phase-guard`, `phase-link-check`, `mode-guard`, `cadence-nudge`, `ontology-type-check`, `check-handover-link`, `validate-ost`, `guard-credentials`, `pin-date`.

Commands currently absent: every slash command in INVENTORY that isn't in the five-item shipped list above.

Framework refs currently absent: every `context/frameworks/*.md` listed in ROADMAP F4 except `ontology.md` (the only one on disk).

Scheduled agents currently absent: `landings-manager`, `podcast-manager`, `sales-admin`, `coding-manager`, `discovery-manager`, `validation-manager`, `cadence-manager`.

Doc/dir refs currently absent on disk: any path under `docs/rfc/`, `docs/guides/`, `docs/specs/` except the spec this work is producing, plus `personal-os/agents/` (referenced in AGENTS.md line 83), `.claude/settings.json` (referenced in README.md layout), and the empty subdirectories under `personal-os/`, `plugins/<phase>/`.

**Symlink contract:**

```bash
[[ -L CLAUDE.md ]] && [[ "$(readlink CLAUDE.md)" == "AGENTS.md" ]] && diff -q CLAUDE.md AGENTS.md
```

Exits 0 when the contract holds.

**Per-component review:** Each component in §Objective receives one `adversarial-reviewer` invocation. Total: **3 skills + 2 agents + 5 commands + 1 hook + 7 core docs + 1 ontology ref + 1 context/README.md = 20 verdicts**. The 2 ADRs are reviewed read-only and recorded in a separate "Read-only" section of `notes/review-verdicts.md`, not counted toward the 20. Output verdicts MUST be `pass` or `needs-fixes`. A `block` verdict halts the loop and surfaces to the human per work-loop §3.4.

**Linter contract:** `bash tools/lint-skill.sh .claude/skills/<name>/SKILL.md` exits 0 for each of the three existing skills. Same for the agents and commands. `python tools/lint-frontmatter.py <file>` exits 0 for each edited file with frontmatter.

## Non-goals

- Building new skills, agents, commands, hooks, scripts, framework references, or templates. Every ROADMAP item except F0.* and the two index READMEs remains untouched as a build target.
- Rewriting AGENTS.md substantively, restructuring sections, or renaming principles. Annotations only.
- Editing `docs/inspiration/*`. Imported source material.
- Adding tests for `tools/check-done.py` or any other existing script (the work-loop SKILL itself promises a `tests/` adjacent to each script; that's a separate spec).
- Building `tools/lint-hook.sh`. Surfaced as a ROADMAP candidate only.
- Reviewing the unbuilt primitives. Cannot adversarially review what isn't there.
- Filling `context/personas/`, `context/products/`, `context/business/`, `context/voice/`, `context/glossary/` — those are user-supplied per the quickstart, not kit-authored.
- Filling any of the empty phase directories (`strategy/`, `discovery/`, `validation/`, `delivery/`, `personal-os/`, `market/`, `communication/`, `plugins/<phase>/`). User work product, not kit.
- Producing a separate "drift audit" report doc. The state of compliance after this pass IS the audit.

## Open questions

1. **Planned-marker convention for tables vs prose.** Tables (INVENTORY) likely want a `Status` column with values `shipped` / `planned (Fx.y)`. Prose (AGENTS.md, README.md) likely want inline `(planned — see [ROADMAP](#fx-y))`. Plan §B.1 picks the exact convention before any edits. _Resolved by:_ implementer, in plan.
2. **What to do when a reviewer finding on an existing component requires a new primitive to fix.** Treat as `defer`, add to ROADMAP under the most relevant Foundation, and record in `notes/deferred-findings.md`. _Resolved by:_ implementer, when the case first arises.
3. **`.claude/CLAUDE.md` mode-guard reference.** The file claims `mode-guard` blocks specific commands, but the hook doesn't exist. Annotate as planned? Or rewrite to say "will block once `hook-mode-guard` ships (ROADMAP F2.4)"? The latter is more honest. _Resolved by:_ implementer, in Task B.
4. **Should the existing ADRs (0001, 0002) be in scope for review?** ~~They are frozen by convention. Decision: review-but-don't-edit, surface any findings as RFC candidates rather than direct edits.~~ **Revised 2026-05-21 mid-pass:** User explicitly authorized inline ADR edits during this pass: "since we're just standing up this repo, you can fix the ADRs themselves in this round." Reviewer-flagged ADR issues are now in-pass; the supersession-via-new-ADR convention is paused until the kit ships v1. _Resolved by user._
5. **Spec template (`docs/_templates/spec.md`) lacks universal-metadata frontmatter (`object_type`, `status`, `last_updated`, `human_owned_decisions`).** This spec was scaffolded from that template and therefore inherits the omission. AGENTS.md §"Human-vs-AI responsibility" says "Every artifact carries explicit frontmatter" — but `tools/lint-frontmatter.py` does not walk `docs/specs/`, so the omission is silent. Decision: add a ROADMAP candidate during Task E (suggest extending ROADMAP F3.8 `template-pm-spec` or creating a new F0.9 `template-kit-spec-frontmatter`) and surface as a deferred finding. Do NOT amend the template in this pass (templates are out-of-scope per Never-do). _Resolved by:_ implementer, in Task E.
6. **Symlink-creation atomicity vs the plan's atomic-write constraint.** Task A uses `rm CLAUDE.md && ln -s AGENTS.md CLAUDE.md` (or `ln -sfn` if `-f` is acceptable on macOS APFS). The atomic-write constraint applies to file-content writes, not to symlink swap operations. Decision: use `ln -sfn` (POSIX-portable atomic replace) to satisfy the spirit of the constraint. _Resolved here._

## Acceptance criteria

- [ ] `CLAUDE.md` is a symlink to `AGENTS.md`; the symlink contract from §"Contract tests" exits 0.
- [ ] Every unbuilt-primitive token from the drift-scan checklist that appears in `AGENTS.md` / `INVENTORY.md` / `README.md` / `.claude/CLAUDE.md` / `.claude/skills/README.md` / `.claude/agents/README.md` is annotated with the chosen planned-marker convention OR appears under a section header that marks the block as planned.
- [ ] Every annotated planned-marker resolves to an existing ROADMAP entry. (No dangling planned-markers.)
- [ ] `.claude/skills/README.md` exists, indexes the 3 existing skills (one line each, ~150 chars max), and lists ROADMAP-promised skills under a separate "Planned" section with anchors back to ROADMAP.
- [ ] `.claude/agents/README.md` exists with the same shape for the 2 existing agents and ROADMAP-promised agents.
- [ ] `adversarial-reviewer` has been invoked once on each in-scope existing component; verdicts are recorded in `notes/review-verdicts.md` in this spec folder.
- [ ] All `needs-fixes` findings are addressed OR explicitly deferred with a ROADMAP entry + a one-line rationale in `notes/deferred-findings.md`.
- [ ] No `block` verdicts remain unaddressed (a `block` rolls the loop back).
- [ ] Every touched file *to which a linter applies per §Verification mode* exits 0 on its applicable linter. `assumption-threshold-lock.md` is explicitly exempt (lint-hook.sh not built). The spec, the plan, the two new READMEs, CLAUDE.md, AGENTS.md, README.md, INVENTORY.md, and `.claude/CLAUDE.md` are outside `lint-frontmatter.py`'s `PHASE_DIRS` and therefore not lintable by it — they are NOT required to pass it.
- [ ] `tools/check-done.py --phase plan --feature reconcile-existing-components` exits 0.
- [ ] `tools/check-done.py --phase verify --feature reconcile-existing-components` exits 0.
- [ ] `tools/check-done.py --phase review --feature reconcile-existing-components` exits 0.
- [ ] `ROADMAP.md` contains no new rows except those explicitly created by (a) checking off shipped items in this pass (the two index READMEs) or (b) deferring a reviewer finding with a corresponding entry in `notes/deferred-findings.md`. The spec-template-frontmatter ROADMAP candidate from Open Question 5 also counts.
- [ ] `spec.md` status flipped to `Shipped`; `plan.md` status flipped to `Done`.

## Cross-references

- **Consumed by:** Every future ROADMAP item — they'll read the reconciled `AGENTS.md` / `INVENTORY.md` / `.claude/skills/README.md` / `.claude/agents/README.md` as ground truth.
- **Consumes:** `.claude/skills/work-loop/SKILL.md` (doctrine); `.claude/agents/adversarial-reviewer.md` (review tool); `docs/HANDOVERS.md` (review contract reference); `feedback-kit-drift-handling` memory (drift rule); `ROADMAP.md` (planned-marker target).
- **Frontmatter fields owned:** None directly. The pass edits existing artifacts' frontmatter only where a reviewer finding requires it.
- **Ontology object types touched:** None directly produced; the pass operates on Cross-cutting kit infrastructure (work-loop spec docs are not ontology-typed artifacts).
