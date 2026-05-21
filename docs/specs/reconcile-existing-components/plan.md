# Plan: reconcile-existing-components

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** approved (iter 2 pass; reviewer verdict 2026-05-21)
- **Verify gate:** passed 2026-05-21 (linters clean; symlink contract holds; drift-scan zero)
- **Review gate:** passed 2026-05-21 (iter 1 of 5; reviewer returned needs-fixes on 5 items, all addressed in-pass)

> **Plan contract.** Implementation strategy for the reconcile-and-harden pass. Allowed to change as I learn. Substantive changes go in the Changelog at the bottom.

## Approach

The pass runs the five work-loop phases sequentially: PLAN (this doc + the spec + the pre-EXECUTE adversarial review), then EXECUTE (five tasks, see below), then VERIFY (linters + gates), then REVIEW (post-EXECUTE adversarial review on the patch surface), then CAPTURE.

The execution sequence is deliberate. **Task A (symlink) goes first** because once `CLAUDE.md` is a symlink to `AGENTS.md`, every subsequent edit to `AGENTS.md` automatically propagates — no two-place sync. **Task B (drift reconciliation) goes next** because every subsequent review will read the reconciled docs; we want them clean. **Task C (the two READMEs) goes next** because they are listed as canonical indexes by AGENTS.md (after Task B that reference will be planned-annotated, but the READMEs are the right way to discharge the annotation). **Task D (parallel adversarial review)** fans out across 20 components in one batch via parallel subagent invocations (plus 2 ADRs reviewed read-only and tracked separately). **Task E (apply findings)** is necessarily serial because findings may interact.

The single most load-bearing choice is the **planned-marker convention**, picked once and used uniformly:

- **Prose (AGENTS.md, README.md, .claude/CLAUDE.md, the two new READMEs):** inline annotation `*(planned — see [ROADMAP](ROADMAP.md))*` placed immediately after the first reference in the file. Subsequent references in the same file can reuse the bare name once the planned-marker has been established at the section level via a `> **Planned items below are listed for completeness; see [ROADMAP](ROADMAP.md) for build status.**` note at the top of the section.
- **Tables (INVENTORY.md):** add a `Status` column with values `shipped` or `planned (F1.3)` etc., where the parenthetical is the ROADMAP slug. Rows are not removed.
- **READMEs (skills/, agents/):** two-section structure — `## Shipped` (existing components, one-line each) and `## Planned` (ROADMAP-listed components with their ROADMAP anchor).

These three forms cover every doc shape touched by this pass.

## Constraints

- **No new primitives** beyond `.claude/skills/README.md` and `.claude/agents/README.md`. Every other new-file impulse is a ROADMAP candidate.
- **Symlink must be relative** (`AGENTS.md`, not an absolute path) — repo portability.
- **Atomic-write any file produced** — use `Edit` (which does atomic write) or `mv` from a tempfile when writing via Bash; never partial `>` redirects on large files. (Write tool used here is fine.)
- **Total token budget:** the spec's `state.json.token_budget_cap_pct` is 80%; the parallel review fan-out (Task D) is the biggest spend — bound it with a per-reviewer cap of ~10 KB output and have each reviewer focus only on its assigned component.
- **Stay inside the spec's Never-do list.** If a reviewer finding tempts an out-of-scope fix, defer it.
- **Universal metadata schema** (per `docs/CONVENTIONS.md`) is preserved on every touched file — don't strip frontmatter, only annotate.

## Construction tests

Cross-cutting tests that span tasks. (Per-task tests live in each task's `Tests:` block.)

- After Task B + Task C complete, the drift-scan grep (per spec §Contract tests) returns zero unannotated hits for any token on the unbuilt-primitive list across the six target files.
- After Task A, the symlink contract from spec §Contract tests exits 0.
- After Task D's fan-out, `notes/review-verdicts.md` exists and contains one verdict line per in-scope component.

## Tasks

### Pre-Task-A: discharge the PLAN gate

Before any EXECUTE task runs:

- After the pre-EXECUTE adversarial-reviewer findings are addressed (this revision is the addressing), set `state.json.plan_review_status = "approved"`.
- Run `tools/check-done.py --phase plan --feature reconcile-existing-components` and confirm exit 0.
- Only then proceed to Task A.

### Task A: Convert CLAUDE.md to a symlink to AGENTS.md

- **Depends on:** none (after the PLAN gate is discharged)
- **Tests:**
  - `[[ -L CLAUDE.md ]] && [[ "$(readlink CLAUDE.md)" == "AGENTS.md" ]] && diff -q CLAUDE.md AGENTS.md` exits 0
  - `git ls-files --stage CLAUDE.md` (if git-init'd) shows mode `120000` — N/A in this repo as it isn't a git repo currently.
  - `tools/lint-frontmatter.py CLAUDE.md` (called manually, not via `--all`) either dereferences correctly to AGENTS.md content OR exits cleanly; if it errors due to symlink handling, surface as a ROADMAP candidate during Task E (it's not in the linter's `--all` walk path so this is an edge case only triggered by explicit invocation).
- **Approach:**
  - `ln -sfn AGENTS.md CLAUDE.md` (atomic replace via `-f` + `-n` to avoid following an existing symlink directory). This is the POSIX-portable atomic-replace pattern; satisfies the spec's atomic-write constraint for symlink ops.
  - Verify with the symlink contract one-liner.
- **Done when:** symlink contract exits 0.

### Task B: Reconcile drift in AGENTS.md, INVENTORY.md, README.md, .claude/CLAUDE.md, context/README.md

- **Depends on:** Task A (so AGENTS.md edits flow through to CLAUDE.md automatically)
- **Tests:**
  - For each token on the spec's unbuilt-primitive list, grep across the five files (plus the two new READMEs after Task C); every hit is annotated per the chosen convention OR sits under a section header that marks the block as planned.
  - For each planned-marker added, the linked ROADMAP entry exists. (`grep -F "$slug" ROADMAP.md` returns a hit.)
- **Approach:**
  - **B.0** (ROADMAP completeness pre-check) Before any annotations, walk the spec's unbuilt-primitive list and confirm every item has a ROADMAP row. For each absent item, add a row under the appropriate Foundation/Phase section with a short description copied from the asserting doc. This satisfies the spec's §"Always do" rule ("Before annotating any item as planned, verify it appears in ROADMAP.md") as an executable step rather than a runtime check during annotation.
  - **B.1** (decision) Pick and document the planned-marker convention (already chosen above; locked in this plan).
  - **B.2** (AGENTS.md) Add planned-markers to the section-level notes for: §"Skills available to you" (4 unbuilt skills); §"Specialist subagents" (2 unbuilt reviewer agents + the phase-skeptic/fan-out lists); §"Phase-aware behavior" "phase-guard hooks" reference. Add planned-marker to `.claude/skills/README.md` and `.claude/agents/README.md` references — these become shipped after Task C, then planned-marker comes off. Also annotate the `personal-os/agents/` reference (line 83): "(planned — see ROADMAP P9.6 `sched-personal-os-agents`)".
  - **B.3** (INVENTORY.md) Add a `Status` column to each table. Mark shipped rows: `audit-completeness`, `audit-portfolio-coherence`, `audit-traceability`, `competitive-research`, `phase-guide`, `adversarial-reviewer`, `competitor-research`, `ost-validator`, `strategy-coherence`, `work-loop`, `assumption-threshold-lock`, `ontology` (REF). All other rows: `planned (Fx.y)` with the matching ROADMAP slug.
  - **B.4** (README.md) Fix the symlink claim (now true after Task A — no change needed there). Annotate the Quickstart's context-file edits as "(create these as your project unfolds; the directories ship empty)". Annotate the Repository-layout `← phase-guard scripts` (only one exists today). Annotate the `.claude/settings.json ← hook config, status line, deny rules` row (file does not exist; planned per ROADMAP F2.6).
  - **B.5** (.claude/CLAUDE.md) Annotate the `mode-guard` reference (the hook doesn't exist — annotate as "planned (ROADMAP F2.4)"). Annotate the `ontology-classifier` skill reference (planned — ROADMAP F1.3). Keep the rest of the file as-is.
  - **B.6** (context/README.md) Read the file; annotate any references to absent primitives or absent context subdirectory contents per the planned-marker convention. (If the file does not exist, surface as a finding: context/ has subdirs but no kit-authored README.)
  - **B.7** Run the drift-scan; iterate until zero unannotated hits.
- **Done when:** the drift-scan grep returns zero unannotated hits across all six target files AND every planned-marker resolves to an existing ROADMAP entry.

### Task C: Write `.claude/skills/README.md` and `.claude/agents/README.md`

- **Depends on:** Task B (so AGENTS.md links to these files don't fail-silent during review)
- **Tests:**
  - Both files exist.
  - Each file contains a `## Shipped` section listing exactly the existing skills/agents (3 / 2 respectively), one line each, ≤ ~150 chars.
  - Each file contains a `## Planned` section listing every ROADMAP-listed skill/agent with an anchor link back to its ROADMAP row.
  - `tools/lint-frontmatter.py` exits 0 on both files (these are markdown indexes; if frontmatter is required, add minimal; if not, none).
- **Approach:**
  - **C.1** Author `.claude/skills/README.md`. Shipped: `work-loop`, `ost-validator`, `strategy-coherence`. Planned: copy from ROADMAP F1.3 (`ontology-classifier`), P2.2 (`interview-snapshot`), P2.5 (`opportunity-clustering`), P3.3 (`experiment-template`), P4.7 (`ears-lint`), P7.8 (`wardley-evolution`), P8.4 (`voice-check`), P9.1 (`dates`).
  - **C.2** Author `.claude/agents/README.md`. Shipped: `adversarial-reviewer`, `competitor-research`. Planned: copy from ROADMAP P2.3, P2.10, P2.13, P3.2, P3.5, P4.16, P5.5, P5.7, P6.1, P6.2, P7.3, P8.8, P8.9. Plus scheduled agents listed in ROADMAP P5.10 (`sched-landings-manager`), P7.6 (`sched-cadence-manager`), P9.6 (`sched-personal-os-agents` — covers `podcast-manager`, `sales-admin`, `coding-manager`, `discovery-manager`, `validation-manager`). Scheduled agents are a separate concept; list them in their own `### Planned — scheduled agents` subsection with the group slug as the anchor.
  - **C.3** Verify with linter (lint-frontmatter only — these aren't skills/agents themselves, they're indexes; no skill/agent linter applies).
- **Done when:** both READMEs exist, contain the shipped+planned shape, and lint clean.

### Task D: Parallel adversarial review of every existing component

- **Depends on:** Task B (reviewers will read the reconciled docs)
- **Tests:**
  - `notes/review-verdicts.md` exists with one verdict line per component. **Count: 20** (3 skills + 2 agents + 5 commands + 1 hook + 7 core docs + 1 ontology ref + 1 context/README). The 2 ADRs are recorded in a separate "Read-only" section and do not count toward the 20.
  - Each verdict is one of `pass` / `needs-fixes` / `block`.
- **Approach:**
  - **D.1** Build the review prompt template. Gives the reviewer (a) the file path, (b) for components with a handover contract: the relevant section of `docs/HANDOVERS.md`; for core docs / ontology ref / context/README that lack a formal contract: the explicit variant prompt "review against the component's own stated purpose — its first paragraph and any 'Why this exists' / 'Objective' section is the contract", (c) instructions to produce the structured output from `adversarial-reviewer.md` §Output, (d) the noise-reduction directive: "Focus your findings on Critical Issues; note but do not expand on items that are pass-level or purely stylistic — keep your Vague Language and Hidden Assumptions sections short unless an item is materially load-bearing."
  - **D.2** Dispatch all 20 invocations in a single message (parallel tool-call block) for maximum throughput. Sub-batches by category:
    - Skills batch (3): `work-loop`, `ost-validator`, `strategy-coherence`
    - Agents batch (2): `adversarial-reviewer` (self-review — explicitly request the dispatched instance to be skeptical of its own contract, especially that the self-defining nature of the contract is a known bias source), `competitor-research`
    - Commands batch (5): `audit-completeness`, `audit-portfolio-coherence`, `audit-traceability`, `competitive-research`, `phase-guide`
    - Hook batch (1): `assumption-threshold-lock`
    - Docs batch (7): CHARTER, CONVENTIONS, HANDOVERS, HUMAN-AI-OWNERSHIP, INVENTORY, PHASE-GUIDE, architecture/overview
    - Refs batch (2): `context/frameworks/ontology.md`, `context/README.md`
    - Read-only batch (2, separate section): ADR 0001, ADR 0002
  - **D.3** Collect verdicts into `notes/review-verdicts.md` as a table: component | verdict | issue count | one-line summary | link to full findings (the full findings live in the same notes file under a per-component heading). ADRs go in a separate `## Read-only` section.
- **Done when:** all 20 verdicts recorded; ADRs recorded in Read-only section; no verdict pending.

### Task E: Apply review findings

- **Depends on:** Task D
- **Tests:**
  - Every `needs-fixes` finding is either (a) addressed (a corresponding edit exists in the touched file) or (b) recorded in `notes/deferred-findings.md` with a rationale and a ROADMAP entry.
  - No `block` verdicts remain (or, if a `block` is unresolvable in-pass, the loop halts and surfaces — per work-loop §3.4).
  - Open Question 5 (spec-template-frontmatter) is recorded in `notes/deferred-findings.md` with a corresponding ROADMAP entry (recommend: append a new bullet under ROADMAP F0 — Build harness — as F0.9, or amend F3.8 `template-pm-spec` to encompass the kit-spec template too).
  - The `lint-hook.sh` ROADMAP candidate (from spec §Verification mode) is recorded in `notes/deferred-findings.md` with a corresponding ROADMAP entry (recommend: append under ROADMAP F0 as F0.10).
- **Approach:**
  - **E.1** Triage findings into `block` / `needs-fix` / `defer` per work-loop §4.2.
  - **E.2** For `block`: stop, surface, re-plan. Do not silently grind.
  - **E.3** For `needs-fix`: apply the smallest edit that addresses the finding. Re-run the relevant linter on the touched file.
  - **E.4** For `defer`: append to `notes/deferred-findings.md` with (file, finding, rationale, ROADMAP-slug-to-add-or-link).
  - **E.5** If new ROADMAP entries were created, append them under the most relevant Foundation/Phase section in `ROADMAP.md`.
- **Done when:** every needs-fixes finding has a disposition; ROADMAP captures any new items including the two known deferrals (spec-template frontmatter, lint-hook.sh).

## Rollout

After this pass ships:

- `AGENTS.md` is the canonical source; `CLAUDE.md` resolves to it via symlink. Anyone editing `AGENTS.md` only touches one file.
- `INVENTORY.md` gains a `Status` column readers can scan to find shipped vs. planned without cross-referencing ROADMAP.
- `.claude/skills/README.md` and `.claude/agents/README.md` discharge their references in AGENTS.md; the planned-markers introduced for them in Task B come off.
- `ROADMAP.md` gets check-marks against the two READMEs (which become new shipped items) and any new entries surfaced by reviewer deferrals — including the two known deferrals (spec-template frontmatter, `lint-hook.sh`).
- This `spec.md` and `plan.md` become the kit's first concrete worked example of the work-loop for the next contributor to copy.

The pass produces no new skill/agent/command/hook/script primitives and no new INVENTORY rows beyond the two READMEs. Individual component edits from Task E are bounded edits to existing files (frontmatter clarifications, vague-language replacements, missing-edge-case additions), not new artifacts; each is captured in `notes/review-verdicts.md` with the specific change.

## Risks

- **Reviewer-finding sprawl.** 20 parallel reviewers can produce a flood of low-severity findings. Mitigation: the dispatch prompt includes the noise-reduction directive (Task D.1): "Focus your findings on Critical Issues; note but do not expand on items that are pass-level or purely stylistic — keep your Vague Language and Hidden Assumptions sections short unless an item is materially load-bearing." This narrows output without suppressing block-level findings.
- **Planned-marker convention drift.** Once chosen, the convention must be applied uniformly. Mitigation: B.7's drift-scan + the post-EXECUTE adversarial review on the patch surface (work-loop REVIEW phase) catches inconsistency.
- **Iteration cap hit on a single needs-fix loop.** If a reviewer keeps surfacing the same finding across iterations, work-loop §3.4 fingerprint-stasis detection fires and the loop halts. Acceptable behavior — better than grinding.
- **Symlink behavior on the user's filesystem.** macOS APFS supports symlinks; if the repo is ever cloned to a non-symlink-supporting filesystem (rare), AGENTS.md notes "where the filesystem supports it; otherwise treat the two as identical." This pass takes the symlink path; the fallback wording in AGENTS.md remains accurate.
- **Self-review of `adversarial-reviewer`.** Asking the agent to adversarially review its own definition introduces obvious bias. Mitigation: dispatch a fresh subagent instance with an explicit "you are reviewing the contract that defines your own role; treat self-defining contracts as a known bias source — be especially skeptical of any claim that is verifiable only against the contract itself" line in the prompt.
- **Reviewer dispatched against core docs without a handover contract.** `adversarial-reviewer.md` §"When the orchestrator invokes you" lists specific artifact types (intents, OSTs, learning memos, visions, initiatives, specs, handoff packets). Core docs are not in that list. Mitigation: Task D.1's variant prompt explicitly addresses this — the reviewer is told to use the doc's own stated purpose as the contract.

## Changelog

- 2026-05-21: Initial plan drafted.
- 2026-05-21: Revised per pre-EXECUTE adversarial-reviewer findings (12 items, 3 critical). Changes: added Pre-Task-A gate-discharge step; added B.0 ROADMAP completeness pre-check; expanded Task B scope to include `context/README.md` and `personal-os/agents/`; corrected Task D count to 20 (was 17); added explicit ADR-handling subsection; added noise-reduction directive to Task D.1 dispatch prompt; added Task E deferrals for spec-template frontmatter and lint-hook.sh; rephrased Rollout to acknowledge Task E may edit existing files.
- 2026-05-21 (mid-execute): User authorized inline ADR edits ("since we're just standing up this repo, you can fix the ADRs themselves in this round"). Open Question 4 revised; both ADRs received substantive edits during Task E.
- 2026-05-21 (mid-execute): User added `competitor-research` and `competitive-research` to the in-pass scope ("please also add the competitor research agent findings to scope, those are key"). Both received in-pass fixes for the critical findings (originally deferred per spec Never-do).
- 2026-05-21 (post-REVIEW iter 1): Reviewer found 5 items, 3 critical. Three were partial-fix propagation gaps (Policy Need → Policy Rule not propagated to all sites; Status type not removed from CONVENTIONS Domain H list; ~80 types claim not updated in AGENTS/README/CLAUDE/context README). Two were process gaps (deferred-findings ROADMAP entries absent; spec/plan status not flipped). All five addressed in iter 1.
