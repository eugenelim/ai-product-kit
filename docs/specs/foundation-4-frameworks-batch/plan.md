# Plan: foundation-4-frameworks-batch

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Approved (2026-05-28; PLAN phase passed pre-EXECUTE adversarial review iter-1 inline)
- **Plan review:** approved (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for shipping all 12 remaining Foundation 4 framework docs (F4.1–F4.11, F4.13; F4.12 already shipped) in one umbrella work-loop. The plan is allowed to change as we learn — substantive changes get a Changelog entry. The contract is the spec; this plan is the path.

## Approach

Two commits, one work-loop, one umbrella spec. Each framework is a leaf research-and-write task fanned out in parallel; verify and review are batched.

**Why one spec, not 12.** The 12 framework docs share a single shape contract (no frontmatter, ≤200 lines, H1 + intro + N×H2 + `## How the kit uses this framework` + `## References`) and are not coupled to each other or to any consumer in this wave. Twelve specs is twelve sets of bullet metadata, twelve plan files, twelve state.json files, twelve pre-EXECUTE reviews. The F3 `template-authoring-convention` spec set the precedent: ten templates under one work-loop, one pre-EXECUTE review, one post-EXECUTE review fanned out per template. We apply the same pattern here.

**Why parallel EXECUTE.** The 12 docs are independent — no doc consumes another in the same wave (cross-links are documentary, not load-bearing). Twelve parallel `general-purpose` agent dispatches collapse what would otherwise be ~3 hours of serial authoring into one wall-clock-fan-out round. The user's global `~/.claude/CLAUDE.md` flags Claude Code bug #57037 (intermittent cascade-permission-denial on parallel dispatch); the fallback is sequential dispatch per slug, which does not count against the work-loop iteration cap.

**Why single VERIFY + single REVIEW.** The contract tests are mechanical greps; running them once across all 12 outputs is the same cost as running per-output and surfaces cross-cutting drift (a docs-style inconsistency, a citation pattern that diverges across half the batch) earlier. The post-EXECUTE adversarial-reviewer pass is the one place fan-out earns its keep: each framework's slice of the spec is small enough that a dedicated reviewer dispatch can compare carefully, and aggregating findings centrally is cheap.

**Sequence is load-bearing.** PLAN → first commit (spec + plan only) → EXECUTE (fan-out) → VERIFY → REVIEW (fan-out) → CAPTURE → second commit. The two-commit shape mirrors the F4.12 / P4.7 wave (per the ears-lint plan) and the F3 template-authoring-convention wave.

## Constraints

- No new top-level dependencies; no new Python modules; no new top-level folders.
- Each framework body ≤ 200 lines (hard cap; per-framework target lines named in the spec).
- No YAML frontmatter on any framework doc (matches `ears.md` and `ontology.md` precedents).
- Atomic writes only — each framework file is written with the `Write` tool in one shot per the agent dispatch.
- Sub-agent dispatch obeys the project `.claude/settings.json` permissions (WebFetch was added to the project-level allowlist earlier this session, so sub-agents can fetch canonical sources where they are online and CC-licensed).
- Branch: current `eugeneacn/nicosia` branch (per spec Open Question §4 — user explicitly framed this work as "complete in this session" without a branch-rename request).
- Two commits, both authored by `eugenelim` (per repo-local git config, per auto-memory `project_git_author`). No Claude/Anthropic/AI mention in either commit message (per auto-memory `feedback_no_claude_coauthor`).
- Ship date in all `Shipped:` annotations = the calendar date the second commit lands (today: 2026-05-28; if work slips one day, all dates flip in one find-replace before the second commit).

## Construction tests

The cross-cutting tests are the spec's §"Contract tests" (T-<slug>-1 through T-<slug>-7 for each of the 12 slugs, plus T-K1 through T-K7). No additional cross-task tests beyond those.

## Tasks

Tasks are sized so each is a coherent unit. Tasks 1 and 2 are sequential (PLAN-phase commit gate). Task 3 fans out 12-way. Tasks 4 and 5 are sequential. Task 6 fans out 12-way (one adversarial-reviewer per framework). Task 7 is sequential. Task 8 ends the loop.

### Task 1: Author spec.md + plan.md

- **Depends on:** none.
- **Tests:**
  - `test -f docs/specs/foundation-4-frameworks-batch/spec.md` exits 0.
  - `test -f docs/specs/foundation-4-frameworks-batch/plan.md` exits 0.
  - `grep -c "## Per-framework required content" docs/specs/foundation-4-frameworks-batch/spec.md` returns ≥ 1.
  - `grep -c -E "^- \`T-[a-z-]+-[1-7]\`" docs/specs/foundation-4-frameworks-batch/spec.md` returns 0 (T-<slug>-N tests are described in prose with the for-each loop, not per-row — see spec §"Contract tests" for the loop construct).
- **Approach:** Author the spec per the template; fill all required sections. Author the plan (this file). The spec's §"Per-framework required content" is the most load-bearing section — it must give a downstream agent everything needed to write one framework without reading anything else.
- **Done when:** Both files exist; spec has all required H2 sections; plan has all required H2 sections.

### Task 2: Pre-EXECUTE adversarial-reviewer pass

- **Depends on:** Task 1.
- **Tests:**
  - `adversarial-reviewer` returns findings list (zero is acceptable but unlikely on first pass).
  - Each finding is either (a) addressed by editing spec/plan, or (b) explicitly deferred with a one-line note under `## Open questions` in the spec or in `notes/deferred-findings.md`.
- **Approach:** Dispatch one `adversarial-reviewer` against the spec + plan. The reviewer specifically checks: (a) the §"Per-framework required content" is concrete enough that a fresh agent can write the doc without reading anything else; (b) the canonical-author requirements are tight enough to pass T-<slug>-7 without ambiguity; (c) the kit-synthesis frameworks (validation-theatre, strategic-coherence, landings-not-launches, competitive-analysis) are honestly labelled as synthesis, not attributed to a single canonical author; (d) the scope of the batch matches what was approved (12 docs, no D18 expansion); (e) the failure-mode-tax catalog is complete (no "we forgot the obvious anti-pattern" finding on post-EXECUTE review).
- **Done when:** All findings are either addressed or deferred with a written record; `state.json.plan_review_status` flipped to `approved`.

### Task 3: PLAN-phase commit (sequential, mandatory before EXECUTE)

- **Depends on:** Task 2.
- **Tests:**
  - `git log -1 --pretty=%s` matches `docs(foundation-4-frameworks-batch): F4.1–F4.13 spec + plan — PLAN-phase`.
  - The commit contains only `docs/specs/foundation-4-frameworks-batch/spec.md`, `docs/specs/foundation-4-frameworks-batch/plan.md`, and any `notes/` files written during Task 2.
  - No Claude/Anthropic/AI mention in the commit message.
- **Approach:** Stage the spec, plan, and any deferred-findings notes file. Commit with the conventional message above and a one-paragraph body describing the contract surface. Author `eugenelim`.
- **Done when:** `git log` shows the commit at HEAD with the correct subject and author.

### Task 4: EXECUTE — parallel fan-out, 12 framework-author agents

- **Depends on:** Task 3.
- **Tests:**
  - 12 files exist under `context/frameworks/`: `continuous-discovery.md`, `opportunity-solution-tree.md`, `interview-snapshot.md`, `assumption-tests.md`, `falsification.md`, `validation-theatre.md`, `rumelt.md`, `wardley.md`, `jtbd.md`, `strategic-coherence.md`, `landings-not-launches.md`, `competitive-analysis.md`.
  - Each file has its H1, the required H2 set per the spec's §"Per-framework required content", a `## How the kit uses this framework` section, and a `## References` section.
  - Each file is ≤ 200 lines.
  - Each file has the canonical-author last-name(s) per T-<slug>-7.
- **Approach:** Dispatch **12 parallel `general-purpose` agents in a single message**. Each agent receives a self-contained prompt (≤ 40 lines) with:
  - The target file path (`context/frameworks/<slug>.md`).
  - The required H2 list verbatim from the spec.
  - The canonical author(s) and source(s) verbatim from the spec's §"Objective" table.
  - The line-cap budget (target + hard cap).
  - The shape precedent reference path (`context/frameworks/ears.md`).
  - The "paraphrase, do not copy; short attributed quotes only" rule.
  - The "name the kit consumer(s)" requirement, with pointers to `ROADMAP.md`, `.claude/commands/`, `.claude/skills/`, `.claude/agents/`, `scripts/`, `templates/` for finding consumers.
  - WebFetch authorization for the openly-licensed sources (Wardley Maps online book; HBR public abstracts; Product Talk blog posts where Torres summarizes her own book; David J. Bland's testing-business-ideas summaries).
  - The "no YAML frontmatter" rule.
  - The required cross-links to companion frameworks in this batch (per spec).
  - Write the file with the `Write` tool in one shot when ready.
  - Report back in ≤ 200 words: file path, line count, the H2 list it wrote, which canonical-author it cited.
  - Fall-back instruction: If you cannot find a primary source online, paraphrase from public summaries and cite the book + year — the spec explicitly allows this. For `wardley.md` specifically, the spec's §"Per-framework required content" F4.8 has inlined the four evolution-axis stage names and five climatic patterns so the agent can author the doc without WebFetch. For `jtbd.md` the spec inlines the Ulwick outcome-statement four-part shape with a worked example for the same reason.
- **Failure handling:** If parallel dispatch cascade-fails (per CLAUDE.md note on Claude Code bug #57037), dispatch the failed agents serially in subsequent messages. The retry does not count against the work-loop iteration cap.
- **Done when:** All 12 files exist; each agent has reported back; the orchestrator has stripped any inadvertent frontmatter (atomic write means each agent's output is final, but the orchestrator should sanity-check before VERIFY).

### Task 5: VERIFY — run contract tests T-<slug>-1..7 + T-K1, T-K2

- **Depends on:** Task 4.
- **Tests:**
  - All 12 × 7 per-file predicates pass.
  - `python3 tools/lint-frontmatter.py --all` exits 0.
  - `bash tools/pre-pr.sh` exits 0.
- **Approach:** Write a one-shot shell loop that iterates the 12 slugs and runs T-<slug>-1 through T-<slug>-7 for each. Output a per-slug pass/fail summary. Run the two kit-wide commands. Fix any failure in-place (most likely failure modes: a sub-agent wrote frontmatter despite the instruction; a sub-agent exceeded the line cap; a sub-agent omitted the canonical-author citation; a sub-agent omitted a required H2). Each fix is a single Edit or Write against the offending file — do not regenerate the file from scratch.
- **Done when:** All gates exit 0.

### Task 6: REVIEW — adversarial-reviewer fan-out, 12 dispatches

- **Depends on:** Task 5.
- **Tests:**
  - Each framework's reviewer returns a findings list; findings are triaged per the work-loop SKILL rules (block / needs-fix / defer).
  - All `block` findings addressed in-loop.
  - All `needs-fix` findings either addressed in-loop or deferred to `notes/deferred-findings.md` with a per-finding one-line rationale.
- **Approach:** Dispatch **12 parallel `adversarial-reviewer` agents in a single message**, one per framework. Each reviewer's prompt names:
  - The framework's target file path.
  - The slice of the spec that governs it (§"Per-framework required content" → the framework's bullet list).
  - The contract test list T-<slug>-1..7.
  - The kit's `AGENTS.md` "Don't reproduce competitor copy verbatim" rule, extended to the framework's canonical source.
  - The reviewer is asked to specifically check: (a) is the canonical author cited correctly; (b) are the required H2s all present and substantively filled; (c) is the kit consumer named accurately; (d) is the doc honest about kit-synthesis vs canonical-attribution; (e) are there factual errors against the canonical source.
- **Iteration cap:** ≤ 5 per the work-loop SKILL. The `state.json.iteration_count` increments per REVIEW pass that produces blocks. Fingerprint stasis detection per work-loop SKILL §4.3.
- **Done when:** All 12 reviewers return clean or all blocks are addressed; `state.json.iteration_count` ≤ 5; `python3 tools/check-done.py --phase review --feature foundation-4-frameworks-batch` exits 0.

### Task 7: CAPTURE — ROADMAP, INVENTORY, context/README, AGENTS, status freezes

- **Depends on:** Task 6.
- **Tests:**
  - T-K3 — ROADMAP F4.1–F4.11 and F4.13 all `[x]` with `**Shipped:** 2026-05-28` (or actual ship date).
  - T-K4 — `context/README.md` zero remaining `*(planned — F4.x)*` for any of the 12 shipped slugs.
  - T-K5 — `docs/INVENTORY.md` contains one REF row per shipped framework.
  - T-K6 — spec.md status = `Shipped (2026-05-28)`; plan.md status = `Done (2026-05-28)`.
- **Approach:** Twelve mechanical edits in `ROADMAP.md` (12 rows from `[ ]` → `[x] **Shipped:** 2026-05-28`). Twelve `context/README.md` catalog-line flips from `*(planned — F4.x)*` to `*(shipped)*` (lines 56–82 region) **plus one additional flip for the stale `ears.md *(planned — F4.12)*` on line 77 → `ears.md *(shipped)*`** (the existing dateless style matches `ontology.md *(shipped)*` on line 54). Twelve INVENTORY REF row insertions, placement per the spec's §"Boundaries — Always do" pointer (INVENTORY has no separate Phase 1 strategy table; strategy lives under `## Phase 7 — Phase 1 strategy commands` with `### Enterprise-mode strategy` and `### Greenfield-mode strategy` sub-sections):
  - `continuous-discovery`, `opportunity-solution-tree`, `interview-snapshot` → Phase 2 — Discovery table
  - `assumption-tests`, `falsification`, `validation-theatre` → Phase 3 — Validation table
  - `rumelt`, `strategic-coherence`, `jtbd` → the main table under `## Phase 7 — Phase 1 strategy commands` (above the enterprise/greenfield sub-sections)
  - `wardley` → `### Enterprise-mode strategy` sub-section
  - `competitive-analysis` → `### Greenfield-mode strategy` sub-section
  - `landings-not-launches` → Phase 5 — Landings table
  - Each row uses the existing `EARS framework | REF | (pulled) | — | context/frameworks/<slug>.md | shipped (<date>)` template.
- AGENTS.md check: walk the AGENTS.md skill/agent/command lists and confirm no row references a now-shipped framework as `(planned — ROADMAP F4.x)`. If any does, flip the annotation. (Most likely: none, because AGENTS.md mostly names the skill/agent/command, not the underlying framework.)
- Freeze spec.md status to `Shipped (2026-05-28)`; plan.md status to `Done (2026-05-28)`; append a Changelog entry to plan.md.
- **Done when:** T-K3, T-K4, T-K5, T-K6 all pass; everything committable.

### Task 8: SHIP-phase commit (sequential; ends the loop)

- **Depends on:** Task 7.
- **Tests:**
  - `git log -1 --pretty=%s` matches `feat(foundation-4-frameworks-batch): ship F4.1–F4.13 (12 reference frameworks)`.
  - The commit contains: all 12 `context/frameworks/<slug>.md` files; the ROADMAP edits; the INVENTORY edits; the context/README.md edits; any AGENTS.md edits; the spec/plan status freezes; any `notes/` written during VERIFY or REVIEW.
  - No Claude/Anthropic/AI mention in the commit message.
- **Approach:** Stage everything except `state.json` (gitignored). Commit with the conventional message and a one-paragraph body. Author `eugenelim`.
- **Done when:** `git log --oneline -2` shows both commits at HEAD with correct subjects and authors.

## Changelog

- 2026-05-28 — Initial plan authored alongside the spec. PLAN phase entry.
- 2026-05-28 — Pre-EXECUTE adversarial-reviewer iter-1 addressed inline: C1 (T-<slug>-2 advisory-vs-gated cap clarified), C2 (stale `ears.md` catalog-line flip added to scope + T-K4 expanded), C3 (validation-theatre T-<slug>-7 OR → AND), D1 (section-level headers explicitly out of scope, deferred to D18 batch), D2 (INVENTORY Phase 7 strategy-table pointer made precise), H1 (self-consistency limitation strengthened — reviewer checks against spec not source), H2 (Ulwick outcome-statement template inlined with worked example), V1 (date find-replace targets named — four files), V2 (AGENTS.md flip added to spec Boundaries + Acceptance criteria), E1 (T-<slug>-8 per-framework H2 content keyword grep added), E2 (Wardley evolution stages + climatic patterns inlined in spec), E3 (script path confirmed exists at spec-time), E4 (T-K7 changed from `git log -1` to `git log --oneline -2`), F1 (rumelt diagnosis-as-complaint added), F2 (jtbd solution-as-job added). Zero deferrals.
