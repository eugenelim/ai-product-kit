# Plan: agent-roadmap-skeptic

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done (2026-05-23)
- **Plan review:** approved

> **Plan contract.** Implementation strategy for shipping `.claude/agents/roadmap-skeptic.md` — the Phase-4 specialist-reviewer agent encoding the bets-vs-commitments lens.

## Approach

One agent file, no scripts, no fixtures. The work is overwhelmingly prose-design: encoding the bets-vs-commitments lens concretely enough that two invocations against the same artifact produce comparable findings.

The agent file lives at `.claude/agents/roadmap-skeptic.md` and mirrors the structural shape of the two precedent specialist-reviewer agents (`adversarial-reviewer`, `quality-engineer`) — same frontmatter shape, same body skeleton (When-the-orchestrator-invokes-you / Your-inputs / Your-output / What-you-check / What-you-don't-check / Hard rules / When this agent is wrong), but with the bets-vs-commitments lens decomposed into the seven category headings the spec lists. The frontmatter shape is fixed by `tools/lint-agent.sh` (required fields `name`, `description`, `tools`, `model`; model ∈ {haiku, sonnet, opus}). The tools list is `[Read, Glob, Grep]` and the model is `sonnet` — matching the two precedent specialist reviewers and the kit's defaults in `.claude/CLAUDE.md`.

The load-bearing design choice is keeping the six categories (§3–§8 from the spec's §Outputs section) machine-instructable, not philosophical. Each category gets:
1. A one-line definition of what the category catches.
2. A concrete walking pattern (which frontmatter fields and which artifact paths to read, in what order).
3. The finding-repair template the spec declares for §3 vs §4–§8.

Anchoring the entire lens is the Definitions block from the spec (Commitment vs Bet, with the three-element predicate {owner, dependency map, falsifiable delivery condition}). The agent body must cite this block — verbatim or near-verbatim — under "What you check" before the six categories, so the bet-vs-commitment classifier is read by the model at every invocation. Without that anchor, the six categories collapse into generic "are you sure?" prompting and §8 duplicates `adversarial-reviewer`'s hidden-assumptions check.

## Constraints

- **Body length:** soft cap ~160 lines (≤ the longer precedent reviewer's body — `quality-engineer.md` is 153 lines; `adversarial-reviewer.md` is 115 lines). Anything longer and the agent prose loses its sharpness.
- **Tools list:** read-only `[Read, Glob, Grep]`. No Write/Edit (the agent never modifies the artifact). No Bash (no shell-outs).
- **Model:** `sonnet`. Reviewer-style synthesis, not cheap fan-out.
- **Description field:** ≤ 1024 chars (lint-agent.sh doesn't enforce a length cap directly, but the Claude Code runtime does). Must name *when the orchestrator invokes the agent*, not vague "is a helper" prose.
- **No new top-level dependencies, no new tooling.** All verification is via existing `tools/lint-agent.sh`, `tools/pre-pr.sh`, `tools/lint-frontmatter.py`.
- **Stay inside the lens.** Categories that overlap with `adversarial-reviewer` or `quality-engineer` are renamed or dropped, not preserved as duplicates.

## Construction tests

Cross-cutting (live above Tasks):

- After EXECUTE, `bash tools/pre-pr.sh` must still exit 0.
- After EXECUTE, `python3 tools/lint-frontmatter.py --all` must still exit 0.
- After EXECUTE, `python3 -m pytest scripts/tests/` shows exactly 1 pre-existing failure (`test_existing_kit_files_parse_compatibly`) — no new failures introduced.

Per-task tests live under the Tasks section.

## Tasks

### Task 1: Author `.claude/agents/roadmap-skeptic.md`

- **Depends on:** none.
- **Tests:**
  - `bash tools/lint-agent.sh .claude/agents/roadmap-skeptic.md` exits 0.
  - File has YAML frontmatter with required fields (`name: roadmap-skeptic`, `description:` ≤ 1024 chars naming invocation conditions, `tools: [Read, Glob, Grep]`, `model: sonnet`).
  - File has H1 `# roadmap-skeptic`.
  - File has the seven required body sections enumerated in spec §Contract tests: "When the orchestrator invokes you", "Your inputs", "Your output" (with frontmatter block), "What you check" (containing the Definitions block + six categories §3–§8), "What you don't check" (explicit differentiation from `adversarial-reviewer` and `quality-engineer` *by name*), "Hard rules", "When this agent is wrong".
  - The six category headings (§3–§8 from spec §"Outputs to the orchestrator") appear verbatim (or near-verbatim — slug-stable) in the agent body.
  - The Definitions block (Commitment vs Bet, with the three-element predicate) is cited verbatim or near-verbatim in the agent body under "What you check".
  - The hard `block` predicate (must-test-before-shipping treated as settled) appears in the agent body's "Hard rules" or "Verdict" section.
- **Approach:**
  - Read `.claude/agents/adversarial-reviewer.md` and `.claude/agents/quality-engineer.md` end-to-end to pin shape.
  - Draft the frontmatter first; verify against `lint-agent.sh` immediately.
  - Draft the body section by section, in spec-declared order.
  - Each of the six category sections under "What you check" gets: (i) one-line definition, (ii) what to read (which frontmatter fields, which parent artifacts, in what order), (iii) finding-repair template (from the spec's §Outputs).
  - Cite the Definitions block (Commitment vs Bet) verbatim or near-verbatim before the six categories.
  - In "What you don't check", name `adversarial-reviewer` (drift) and `quality-engineer` (operational quality) explicitly. State the boundary in both directions ("if you find X, say so and stay in lens"). Include the explicit §8-vs-hidden-assumptions boundary the spec calls out.
  - Cite the hard `block` predicate in "Hard rules" or "Verdict".
- **Done when:** `lint-agent.sh` exits 0 against the new file AND the seven required body sections + six category headings + Definitions block + hard `block` predicate are present in the body.

### Task 2: Verify against the cross-cutting gates

- **Depends on:** Task 1.
- **Tests:**
  - `bash tools/pre-pr.sh` exits 0.
  - `python3 tools/lint-frontmatter.py --all` exits 0.
  - `python3 -m pytest scripts/tests/` shows exactly 1 pre-existing failure (`test_existing_kit_files_parse_compatibly`), 0 new failures.
- **Approach:**
  - Run the three commands above.
  - If any newly-failing assertion appears, fix the agent file and re-run.
- **Done when:** all three commands return the expected exit-code / failure profile.

### Task 3: REVIEW — dispatch `adversarial-reviewer` against the shipped agent file

- **Depends on:** Task 2.
- **Tests:**
  - Reviewer returns a structured verdict block in the canonical adversarial-reviewer format.
  - Verdict is `pass` or `needs-fixes` (a `block` rolls back to Task 1).
  - No recurring-fingerprint stasis pattern (≥3 identical findings across iterations).
- **Approach:**
  - Dispatch the reviewer with the four specific questions from the upstream prompt:
    1. Is the differentiation from `adversarial-reviewer` clearly encoded in the agent body, or does the skeptic re-derive drift checks?
    2. Is the bets-vs-commitments lens specific enough to be machine-instructable, or does it collapse into generic "are you sure?" prompting?
    3. Does the agent body encode *when* the orchestrator invokes the skeptic (Phase-4 artifacts only — not Phase-3 OSTs or Phase-5 landings)?
    4. Does the output shape pin a structured verdict block parallel to `adversarial-reviewer`'s frontmatter?
  - Address any `needs-fixes` findings in Task 1; re-run Task 2; re-dispatch.
  - Hard cap at 5 iterations per `work-loop`'s default `max_iterations`.
- **Done when:** reviewer returns `pass` (or `needs-fixes` with all flagged items addressed and a clean re-review).

### Task 4: CAPTURE — flip docs and roadmap markers

- **Depends on:** Task 3.
- **Tests:**
  - `grep -nE "^- \[x\] \*\*P4\.16\*\*" ROADMAP.md` returns 1 match.
  - `grep -n "roadmap-skeptic" docs/INVENTORY.md` shows a row with "shipped" status (not "planned").
  - `grep -n "roadmap-skeptic" AGENTS.md` shows the line WITHOUT the "*(planned — ROADMAP P4.16)*" annotation for the `roadmap-skeptic` slug specifically; the four other phase-skeptics in that line retain their planned annotations.
  - `spec.md` H2 status line is `Shipped (<date>)`.
  - `plan.md` status line is `Done (<date>)` and a changelog entry exists.
- **Approach:**
  - Edit ROADMAP.md row P4.16: flip `[ ]` → `[x]`; append `**Shipped:** <YYYY-MM-DD>`.
  - Edit INVENTORY.md row 155: flip "planned (P4.16)" → "shipped <YYYY-MM-DD> (P4.16)"; refresh Purpose column to the shipped one-liner.
  - Edit AGENTS.md §"Specialist subagents" phase-skeptic parenthetical: remove the "*(planned — ROADMAP P4.16)*" annotation from the `roadmap-skeptic` entry only. The other four phase-skeptics in the same parenthetical retain their planned annotations.
  - Edit spec.md status to `Shipped (<date>)`; edit plan.md status to `Done (<date>)` and append a changelog entry.
- **Done when:** all four greps return the expected results and the status lines in spec.md / plan.md are flipped.

### Task 5: COMMIT — two commits, push to main

- **Depends on:** Task 4.
- **Tests:**
  - `git log --oneline origin/main..HEAD` shows two new commits: `docs(agent-roadmap-skeptic): spec + plan — PLAN-phase` and `feat(agent-roadmap-skeptic): ship Phase-4 bets-vs-commitments specialist reviewer`.
  - Commit messages contain no Claude/Anthropic/AI attribution (per repo memory).
  - `git push origin HEAD:main` succeeds.
  - state.json files are NOT staged (gitignored).
- **Approach:**
  - First commit (PLAN-phase, made BEFORE EXECUTE actually runs — see Rollout below for ordering): stage `docs/specs/agent-roadmap-skeptic/spec.md` and `docs/specs/agent-roadmap-skeptic/plan.md` only; commit with the PLAN-phase message.
  - Second commit (after EXECUTE + REVIEW + CAPTURE all pass): stage `.claude/agents/roadmap-skeptic.md` + the CAPTURE edits to ROADMAP.md, INVENTORY.md, AGENTS.md, spec.md, plan.md; commit with the feat message.
  - Push with `git push origin HEAD:main`.
- **Done when:** both commits are on `origin/main` and `pre-pr.sh` still passes against `HEAD`.

## Rollout

Order matters: the PLAN-phase commit happens between Task 0 (pre-EXECUTE adversarial review on spec+plan) and Task 1 (EXECUTE proper), so the spec+plan land independently of the agent file. The shipping commit lands after Task 4.

Downstream consumers to update (Task 4 above):
- ROADMAP.md: row P4.16 check-off.
- INVENTORY.md: row 155 status flip + Purpose refresh.
- AGENTS.md §"Specialist subagents": phase-skeptic parenthetical de-annotation.

No existing audit / command / skill needs to be updated to call this new agent in this PR — orchestrator dispatch is a `work-loop` REVIEW-phase concern, and the spec leaves first-usage dispatch wiring as the natural follow-up. (Future wiring: `/audit-completeness` may grow a Phase-4 dispatch block that runs `adversarial-reviewer`, `quality-engineer`, and `roadmap-skeptic` in sequence — out of scope for this spec.)

## Risks

- **Lens collapse into "generic drift review".** Mitigation: the seven-category decomposition under "What you check" is the load-bearing scaffolding. If the adversarial-reviewer's review (Task 3) flags this as the failure mode on iteration 2, surface to the human rather than grinding (per upstream prompt's stop conditions).
- **Description-field length overrun.** `lint-agent.sh` doesn't enforce 1024-char limit directly, but `claude` runtime does. Mitigation: draft description first; count chars; trim if needed before any other body writing.
- **Body bloat past the soft cap.** Mitigation: each category section is one short paragraph (definition + walking pattern + finding template), not a treatise.

## Changelog

- 2026-05-23: Shipped after three REVIEW iterations. Iteration 1 added the discretionary `block` trigger, under-scope direction on §5, softened the "mechanical predicate" claim, concretized §Critical-issues enumeration, added absent-`upstream_chain` handling, and named README.md as the frontmatter source for Initiative/Handoff-Packet folders. Iteration 2 fixed C-1 (escalation rule for §6 placeholder `human_owned_decisions` made conditional on `human_approval_required: true` lacking `approvals_obtained:`), replaced "flood of spurious findings" with concrete language, and promoted the Draft-Vision early-exit to a second hard `block` predicate in §Hard rules. Iteration 3 returned `verdict: pass`; two stylistic tidy-ups in the spec's prose sections were folded into the same commit.
