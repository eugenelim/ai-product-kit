# Plan: ears-lint

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for shipping F4.12 (`framework-ears`) and P4.7 (`skill-ears-lint`) together as Wave 2. Two coupled deliverables in one work-loop: the framework doc is the rule library; the skill is the consumer. Plan is allowed to change as we learn — substantive changes get a Changelog entry.

## Approach

Single sequential work-loop. The framework doc is authored first because the skill cites it; once the framework body is stable, the skill body refers to specific section headings inside it. The fixture is authored last because its expected classifications can only be ground-truthed against the final framework body (a rewrite that resolves a "common confusion" entry might change which classification a marginal sentence earns).

The framework is authored as a single-pass prose write — there's no procedure to TDD because the artifact is a reference doc, and the contract tests (T1–T5) are goal-based greps that can verify the shape mechanically after the file lands. The skill is authored similarly because its body is also prose; the contract test (T7) is a single linter exit code. The fixture is the only artifact with a true behavioral test (T10–T11), and that test is manual-gesture (in-session classification of each row), which is the most honest verification for a model-executed skill that has no runnable script form yet.

Sequence is load-bearing: framework → skill → fixture → manual-gesture verification → adversarial review. Re-ordering would either force the skill to be authored against an unstable rule source (framework→skill swap), or force the fixture's expected classifications to be guessed before the framework's "common confusion" entries are nailed down (fixture-first).

The framework + skill pair lives outside `PHASE_DIRS`, so the default-mode frontmatter linter does not walk them. The audit-driven gate is `lint-skill.sh` for the skill and a goal-based grep+wc check for the framework. There is no new test fixture under `scripts/tests/` — this wave does not add a Python-runnable form.

## Constraints

- No new top-level dependencies. Stdlib only (the only "tool" added is a prose-procedure skill).
- Framework body ≤ 150 lines; the linter-style cap is 200 to catch runaway drafts (T2).
- Skill body ≤ 200 lines (workplace soft cap from `lint-skill.sh`'s 400-line absolute cap).
- No modification to `docs/HANDOVERS.md`, `docs/CONVENTIONS.md`, `context/frameworks/ontology.md`, `tools/lint-frontmatter.py`, `.claude/commands/draft-spec.md`, or any other Phase-4 command in this loop.
- No new ontology object_type. Framework-reference docs are kit-meta (existing posture: `context/frameworks/ontology.md` carries no frontmatter and is not in any ontology domain).
- Atomic writes only — each file is written with the Write tool in one shot; no partial-file edits leave a half-state behind.
- Manual-gesture verification is in-session (this Claude Code session, the same one that authored the skill). Fresh-session re-verification is a deferred F1-G1-style follow-up; the in-session gesture is sufficient per the work-loop SKILL's "Manual gesture" verification mode.
- Two-commit shape per the original prompt: `docs(ears-lint): F4.12 + P4.7 spec + plan — PLAN-phase` for the spec+plan; `feat(ears-lint): ship F4.12 framework-ears + P4.7 ears-lint skill` for everything else.
- Git author is the per-repo `eugenelim` identity (already configured locally for this clone); branch prefix `eugenelim/ears-lint`; no Claude/Anthropic/AI attribution anywhere in commit messages, PR bodies, or any public GitHub artifact.

## Construction tests

The cross-cutting tests are the §"Contract tests" of the spec (T1–T18). No additional cross-task tests beyond those.

## Tasks

Tasks are sized so each is a coherent unit; the second commit bundles Tasks 1, 2, 3, 5, 6, 7 (everything past the PLAN-phase spec+plan commit).

### Task 1: Author `context/frameworks/ears.md`

- **Depends on:** none.
- **Tests:**
  - T1: `test -f context/frameworks/ears.md` exits 0.
  - T2: `[[ $(wc -l < context/frameworks/ears.md) -le 200 ]]` exits 0 (target ≤ 150; cap at 200 for runaway-draft detection).
  - T3: `grep -c -E "^### (Ubiquitous|Event-driven|State-driven|Optional-feature|Unwanted-behavior)$" context/frameworks/ears.md` returns exactly 5.
  - T4: `grep -c "^## The Complex combination form$" context/frameworks/ears.md` returns exactly 1.
  - T5: `grep -c "Mavin" context/frameworks/ears.md` returns ≥ 1.
- **Approach:** Write the file per the §"Inputs and outputs" output-1 outline in the spec. Use the existing `context/frameworks/ontology.md` as the shape precedent (prose-only, no YAML frontmatter, H1 + intro blockquote + H2/H3 sections). Quote Mavin et al. (2009) verbatim for each pattern's sentence template; add one canonical example, a one-line "when to use" note, and a "common confusion" note per pattern. End with the References section.
- **Done when:** T1–T5 pass; file body is ≤ 150 lines.

### Task 2: Author `.claude/skills/ears-lint/SKILL.md`

- **Depends on:** Task 1 (the skill cites the framework).
- **Tests:**
  - T6: `test -f .claude/skills/ears-lint/SKILL.md` exits 0.
  - T7: `bash tools/lint-skill.sh .claude/skills/ears-lint/SKILL.md` exits 0.
  - T18: `grep -c "context/frameworks/ears.md" .claude/skills/ears-lint/SKILL.md` returns ≥ 1.
- **Approach:** Write the file per the §"Inputs and outputs" output-2 outline. Frontmatter declares `name: ears-lint`, `description:` (≤ 1024 chars), `license: MIT`. Body has H1 `# ears-lint`, intro paragraph, the six required H2 sections in order. Use the existing `.claude/skills/ost-validator/SKILL.md` as shape precedent. Cite `context/frameworks/ears.md` from the body explicitly at least once (the classification procedure section is the natural seam).
- **Done when:** T6, T7, T18 pass; body ≤ 200 lines.

### Task 3: Author `.claude/skills/ears-lint/references/fixture-sentences.md`

- **Depends on:** Tasks 1 and 2.
- **Tests:**
  - T8: `test -f .claude/skills/ears-lint/references/fixture-sentences.md` exits 0.
  - T9: `[[ $(grep -c "^| " <file>) -ge 13 ]]` exits 0 (header + separator + ≥ 11 sentence rows after spec iter-1 added passive-voice-no-actor and If-without-then coverage).
  - T10: Seven separate grep predicates confirm at least one row per verdict label.
- **Approach:** Markdown table with columns `| # | Sentence | Expected pattern | Rationale |`. Author the ≥11 rows per the §"Inputs and outputs" output-3 coverage list. Each row's Rationale column is one short sentence explaining why the sentence earns its classification.
- **Done when:** T8–T10 pass.

### Task 4: Manual-gesture verification (records `notes/manual-verification-2026-05-23.md`)

- **Depends on:** Tasks 1, 2, 3.
- **Tests:**
  - T11: Every fixture row's expected classification matches the in-session classification recorded in the notes file, OR discrepancies are resolved by re-authoring the fixture / framework, OR deferred-findings are explicitly documented.
- **Approach:** Load the skill into the active session. For each fixture row, **first** apply the skill's classification procedure to the sentence in isolation (without looking at the row's expected label) and write the actual pattern + rationale + suggested_rewrite to the notes file. **Then** compare against the expected column. The record-before-compare order is the only mitigation against trivial self-confirmation when the executing model is the same instance that authored the fixture: writing the actual classification before reading the expected column at least exposes which sentences the procedure flagged versus which the fixture labelled, even when the model wrote both. If any row disagrees, surface the disagreement and resolve before VERIFY exits (preferred: tighten the framework's "common confusion" entry; fallback: rewrite the fixture row's expected label; never silently change the actual classification to match).
- **Done when:** T11 passes; notes file exists at `docs/specs/ears-lint/notes/manual-verification-2026-05-23.md`.

### Task 5: VERIFY gates

- **Depends on:** Tasks 1–4.
- **Tests:**
  - T7 (re-run after any skill edit): `bash tools/lint-skill.sh ...` exits 0.
  - T12: `python3 tools/lint-frontmatter.py --all` exits 0.
  - T13: `bash tools/pre-pr.sh` exits 0.
- **Approach:** Run the three linters in order. The framework doc is not walked by default mode; the SKILL.md is not walked by default mode (only `.claude/skills/*/SKILL.md` is walked by `lint-skill.sh`, which we already ran in Task 2's gate). Fix anything non-zero in-place; do not proceed to REVIEW until all three exit 0.
- **Done when:** `python3 tools/check-done.py --phase verify --feature ears-lint` exits 0.

### Task 6: REVIEW — post-EXECUTE adversarial reviewer

- **Depends on:** Task 5.
- **Tests:**
  - The reviewer's findings list is either empty or every finding has been addressed in a follow-up edit + re-run.
- **Approach:** Dispatch `adversarial-reviewer` against the four artifacts (spec, plan, framework, skill+fixture). The reviewer specifically checks: (a) the five EARS patterns are correctly named per Mavin et al. and not invented; (b) the skill's invocation contract is concrete enough that a future `/draft-spec` patch can call it without ambiguity; (c) the framework doc and the skill are not duplicating rule definitions; (d) the manual-gesture verification actually exercises all five patterns + Complex + non-conformant. Iterate ≤ 5 times. Defer findings only with explicit `notes/deferred-findings.md`.
- **Done when:** `python3 tools/check-done.py --phase review --feature ears-lint` exits 0.

### Task 7: CAPTURE — ROADMAP + INVENTORY + AGENTS + README + status freezes

- **Depends on:** Task 6.
- **Tests:**
  - T14: spec.md status = `Shipped (2026-05-23)`; plan.md status = `Done (2026-05-23)`.
  - T15: ROADMAP F4.12 and P4.7 both `[x]` with `**Shipped:** 2026-05-23`.
  - T16: INVENTORY framework row inserted; skill row updated.
  - T17: AGENTS.md and `.claude/skills/README.md` updated.
- **Approach:** Seven edits in order:
  1. Flip ROADMAP F4.12 to `[x] **F4.12** … **Shipped:** 2026-05-23` (matches the F3 row format used by the seven Wave-1 P4 commands).
  2. Flip ROADMAP P4.7 to `[x] **P4.7** … **Shipped:** 2026-05-23`.
  3. Insert a Phase-4-Spec INVENTORY row for `context/frameworks/ears.md` (Block: REF, Inv: pulled, Produces: —, Purpose: `context/frameworks/ears.md`, Status: shipped (2026-05-23)). Mirror the existing REF rows at lines 63–65 and 85–86.
  4. Update the existing INVENTORY row at line 143 — flip the `ears-lint` skill's Status from `planned (P4.7)` to `shipped (2026-05-23)`.
  5. Edit AGENTS.md `## Skills available to you` section — remove the `(planned — ROADMAP P4.7)` annotation and the conditional language around `ears-lint`; the bullet now reads as a shipped skill.
  6. Edit `.claude/skills/README.md` — move the `ears-lint` line from "Planned" to "Shipped" with a one-line description matching the other shipped entries.
  7. Freeze spec.md status to `Shipped (2026-05-23)`; plan.md status to `Done (2026-05-23)`; append a Changelog entry to plan.md.
- **Done when:** T14–T17 pass; everything committable.

### Task 8: Two commits + push to main

- **Depends on:** Task 7.
- **Tests:**
  - Two commits on `eugenelim/ears-lint`: one matching `docs(ears-lint): F4.12 + P4.7 spec + plan — PLAN-phase`, one matching `feat(ears-lint): ship F4.12 framework-ears + P4.7 ears-lint skill`.
  - No Claude/Anthropic/AI mention in either commit message.
  - `git push origin HEAD:main` succeeds.
- **Approach:** First commit is created at the end of Task 1.5 (after the PLAN phase passes its adversarial review and the gate); contains only `docs/specs/ears-lint/spec.md` and `docs/specs/ears-lint/plan.md`. Second commit (after Task 7) contains the framework doc, the skill files, the fixture, the manual-verification note, the ROADMAP/INVENTORY/AGENTS/README updates, and the spec/plan status freezes. Push with `git push origin HEAD:main`.
- **Done when:** `git log origin/main --oneline -3` shows both commits at the tip.

## Changelog

- 2026-05-23 — Initial plan authored alongside the spec. PLAN phase entry.
- 2026-05-23 — Pre-EXECUTE adversarial-reviewer iter-1: addressed C1 (T3/T4/T5/T9/T18 grep predicates wrapped in `[[ ... ]]` assertions), C2 (self-consistency limitation acknowledged in Verification mode + record-before-compare ordering added to Task 4), D2 (Task 7 sub-step count corrected), H1 (orchestrator-side splitter failure modes named in Invocation contract), H2 (Open Question §2 enforcement gap flagged), V1 (runnable Python form tracking location named via `notes/deferred-findings.md` + placeholder slug), E1 (passive-voice fixture row added; non-conformant failure modes (e) added), E2 (Always-do rule resolves `If … shall …` without `then` as Unwanted-behavior; fixture row added). E3 deferred to post-EXECUTE Task 6 review per the reviewer's recommendation.
