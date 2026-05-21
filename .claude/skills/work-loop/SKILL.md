---
name: work-loop
description: The canonical pattern for building any non-trivial kit component (skill, agent, command, hook, script, framework reference, template). Plan → execute → verify → review → iterate, with spec/plan documents, state.json enforcement, hard iteration caps, and pre-execute adversarial review. Load this skill before any work that produces or modifies a kit component.
license: MIT
---

# work-loop

The kit's standard pattern for building or modifying its own components. Adapted from the agent-ready-repo engineering work-loop, reshaped for kit-build work — building skills, agents, commands, hooks, scripts, reference docs, templates.

This SKILL is the doctrine; `docs/CONVENTIONS.md` is the contract.

## When to use this skill

For anything beyond a one-line edit:

- Building a new skill, agent, command, hook, or script
- Substantively modifying an existing kit component (more than a typo)
- Adding or amending the kit's reference frameworks (`context/frameworks/*.md`)
- Adding or amending the kit's templates (`templates/*.md`)
- Authoring an ADR or RFC

For trivial edits (typo fixes, broken-link repairs, removing an obsolete sentence), skip the loop. Use judgment.

## Why a loop, not a single pass

LLM self-assessment is unreliable: agents declare victory when they *feel* done. The loop replaces "feel" with mechanical gates plus an adversarial review pass. It keeps iterating until both kinds of check are satisfied, or until the hard iteration cap fires.

Why iterate, not retry-from-scratch: most loops converge. Gates fail, review surfaces a finding, the next pass fixes it. Restart-from-scratch loses the planning context.

Why a hard cap: without one, you're hoping. The cap lives in `state.json` and is enforced by `tools/check-done.py`. If you hit it, the work is bigger than you thought — stop, re-plan, or split.

## The phases

```
PLAN → EXECUTE → VERIFY → REVIEW → (iterate ≤ max_iterations) → CAPTURE
```

Each phase has a clear entry condition, a clear exit condition, and a check from `tools/check-done.py`.

---

## PHASE 1 — PLAN

The cost of a wrong start is higher than the cost of thinking. Plan before touching the keyboard.

### Step 1.1 — Locate or create the spec

Every non-trivial change has a spec under `docs/specs/<feature>/`. If no spec exists:

1. Create the directory: `docs/specs/<feature>/`
2. Copy `docs/_templates/spec.md` → `docs/specs/<feature>/spec.md`
3. Copy `docs/_templates/plan.md` → `docs/specs/<feature>/plan.md`
4. Copy `docs/_templates/state.json` → `docs/specs/<feature>/state.json` (gitignored)
5. Set `state.json.feature` to the slug

### Step 1.2 — Fill the spec

Work through every required section. The spec is the **contract** — what "done" means. The spec must answer:

- **Component type** (skill / agent / command / hook / script / framework-ref / template / guide)
- **Kit phase** the component serves
- **Inputs and outputs** — concrete enough to write the interface from
- **Boundaries** (Always do / Ask first / Never do)
- **Verification mode** (TDD / goal-based / manual gesture / audit-driven)
- **Contract tests** — the gate
- **Non-goals** — what's explicitly excluded
- **Acceptance criteria** — verifiable predicates

### Step 1.3 — Fill the plan

The plan is the **implementation strategy** — allowed to change as you learn. The plan must declare:

- **Approach** — high-level strategy
- **Constraints** — cross-cutting things to respect
- **Tasks** — work-breakdown with `Depends on:` declared explicitly per task
- **Per-task: Tests come before Approach** — tests drive implementation, not the other way around
- **Per-task: Done when** — a single observable predicate

### Step 1.4 — Pre-EXECUTE adversarial review

Before any execute work, dispatch the `adversarial-reviewer` subagent against the **spec + plan**. This is the "review left" pattern — move review from after-implementation to before-implementation.

The reviewer reads the spec, plan, and any cross-references and returns findings. Treat findings as blocking. Address them or document why not, then re-run.

When the reviewer returns clean, set `state.json.plan_review_status = "approved"`.

### Step 1.5 — Plan gate

Run `tools/check-done.py --phase plan --feature <slug>`. Exit 0 means proceed to EXECUTE. Non-zero means the gate failed; the stderr message says why.

If `state.json.plan_review_status == "pending"` at this point, the gate will refuse. That's intentional — the adversarial-reviewer pass must have happened.

---

## PHASE 2 — EXECUTE

Build the component per the plan.

### Step 2.1 — One task at a time

For each task in `plan.md`:

1. Read the task's `Tests:` section first
2. Write the tests (red)
3. Implement to make tests pass (green)
4. Refactor if needed; tests must stay green (refactor)
5. Commit when the task's `Done when:` is satisfied

Use separate commits for red / green / refactor when the change is non-trivial. Conventional commit format: `<type>(<scope>): <subject>`. Footer: `Spec: docs/specs/<feature>/spec.md`.

### Step 2.2 — If the plan changes

If you learn something that means a task needs different tests or a different approach, update `plan.md` in the same commit as the work. Append a line to the plan's `## Changelog` explaining the change.

If you learn something that means the **spec** is wrong, stop. Update the spec, re-run the pre-EXECUTE adversarial review against the new spec, re-set `state.json.plan_review_status` if needed, and resume.

### Step 2.3 — Stay inside scope

If you find yourself wanting to fix something out of scope, write it down (in `notes/` or as an issue) and keep going. Scope creep is the most common cause of failed review.

---

## PHASE 3 — VERIFY

Run the mechanical gates. These are objective; they pass or they don't.

### Step 3.1 — Pick the verification mode

Whichever modes the spec declared. For this kit, the four are:

- **TDD:** all tests green; coverage of the contract tests is complete
- **Goal-based check:** the one-liner returns the expected value (e.g., `tools/lint-skill.sh .claude/skills/<name>/SKILL.md` exits 0; the new audit returns the expected verdict on the fixture)
- **Manual gesture:** the recorded gesture against the fixture produces the documented behavior in a fresh Claude Code session
- **Audit-driven:** the relevant kit audit returns clean against the new component

### Step 3.2 — Run the gates

In order:

1. **Component-specific linter** — `tools/lint-skill.sh`, `tools/lint-agent.sh`, `tools/lint-command.sh`, `tools/lint-hook.sh` per component type
2. **Cross-cutting linters** — `tools/lint-frontmatter.sh` for any artifact that should declare ontology object_type
3. **Tests** — if the component is a script, run its test suite
4. **Integration audit** — if the component is consumed by an existing audit, run that audit against the kit and confirm it passes

### Step 3.3 — Verify gate

Run `tools/check-done.py --phase verify --feature <slug>`. Exit 0 means proceed to REVIEW.

If any gate failed, fix and re-run. Don't proceed with red gates.

---

## PHASE 4 — REVIEW

Mechanical gates catch shape failures. Adversarial review catches drift, missed cases, and over-confidence.

### Step 4.1 — Dispatch reviewers

For each non-trivial change, run `adversarial-reviewer` against the implementation. The reviewer compares spec + plan against the actual files produced and returns findings.

Layer additional specialist reviewers when the change warrants:

- `compliance-reviewer` — if the component touches user data, claims, regulatory workflows, or anything with legal exposure. Most kit components don't.
- `quality-engineer` — if the component is a script, the kit's audit pipeline, or anything where testability / observability / reliability of the *built thing* matters.

Don't run all three by default. Pick the lenses the change actually warrants.

### Step 4.2 — Triage findings

For each finding:

- **Block** — must fix before proceeding
- **Needs-fix** — fix in this loop; document the fix
- **Defer** — record as a follow-up spec or open question; do not silently drop

A `block` finding rolls the loop back to PLAN or EXECUTE depending on its severity.

### Step 4.3 — Stuck-loop detection

The reviewer's findings are hashed and stored in `state.json.finding_fingerprints`. On the next REVIEW iteration, compare against `previous_finding_fingerprints`. If the same fingerprints recur three times, you're circling — stop and surface to the human.

### Step 4.4 — Review gate

Run `tools/check-done.py --phase review --feature <slug>`. Exit 0 means review passed. Non-zero means either:
- Findings remain unaddressed → back to EXECUTE
- Iteration cap hit → stop and surface to the human
- Fingerprint stasis → stop and surface

---

## PHASE 5 — CAPTURE

A loop that finishes without updating *some* doc, skill, or note has wasted what it learned.

### Step 5.1 — Update reference docs

If the component is referenced anywhere (AGENTS.md, INVENTORY.md, README.md, PHASE-GUIDE.md, HANDOVERS.md, context/README.md, the relevant framework reference), update those files in the same PR. Drift is a bug.

### Step 5.2 — Update the inventory

Every shipped component gets a row in `docs/INVENTORY.md` under its phase + practice-area cell. If it's a new audit, also add its detector hook to AGENTS.md.

### Step 5.3 — Freeze the spec

Set `spec.md`'s status to `Shipped` (and eventually `Frozen` when no further work on this component is expected). Set `plan.md`'s status to `Done`. State.json gets deleted on PR merge (it's gitignored).

### Step 5.4 — Mark the roadmap

Update `ROADMAP.md` — check off the shipped item and surface its number in the next-up section if it unblocked downstream work.

---

## Iteration cap

The hard cap is `max_iterations` (default 5) in `state.json`. Each REVIEW pass that doesn't return clean increments `iteration_count`. When the count hits the cap:

1. STOP. Don't grind.
2. Surface to the human with a one-page summary: what's converged, what's circling, what the reviewer keeps flagging.
3. The right next move is usually one of: re-plan, split the spec into smaller specs, escalate the spec to an RFC, or accept the open findings as known limitations.

## Common rationalizations (the lies)

| The lie | The rebuttal |
|---|---|
| "I'll update the spec after the implementation." | Drift is a bug, not follow-up work. Update spec and implementation in the same PR. |
| "I'll verify this manually, just this once." | The verification mode is declared in the plan. If manual is right, declare it; if it isn't, don't improvise. |
| "I can fix this while I'm here." | Out-of-scope changes need a separate spec. Scope creep is the single most common cause of failed review. |
| "This decision doesn't need an ADR — it's obvious." | If you're making it, it isn't obvious to the next person. Writing it now costs less than someone re-litigating in six months. |
| "The reviewer is being too strict; I'll just merge." | The reviewer is the gate. If you disagree, defer the finding explicitly via a follow-up spec — don't silently override. |

## When this skill is wrong

If this loop produces friction that isn't earning its keep, say so via RFC. Don't quietly deviate. The whole point of writing it down is that the rules are visible and contestable.
