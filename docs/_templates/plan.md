# Plan: <component-name>

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting | Approved | Executing | Done
- **Plan review:** [pending | approved] (set by `tools/check-done.py --phase plan`)

> **Plan contract.** This is the implementation strategy. Unlike the spec, this document is allowed to change as you learn. When it changes substantially (a different approach, not just a re-ordering), note why in the changelog at the bottom.

## Approach

One to three paragraphs. The high-level strategy. Why this approach over alternatives. What's load-bearing about the sequence of work.

If the component is a script: name the language (Python by default for this kit), the entry-point shape (`__main__` block, CLI flags), the library boundaries, the dependency posture (stdlib only is preferred; document any deviation).

If the component is a skill/agent/command: name the file path it'll live at, the frontmatter fields it'll declare, the body's outline.

## Constraints

Cross-cutting things the implementer must respect. Examples:
- "Must not introduce new top-level dependencies beyond stdlib + pyyaml"
- "Must not exceed 200 lines in the SKILL.md body"
- "Must work without an internet connection"
- "Must atomic-write any file it produces (tmp + os.replace)"

## Construction tests

Most construction tests live under **Tasks** below (per-task `Tests:` subsections). This top-level section is only for cross-cutting tests that span tasks.

## Tasks

The work-breakdown. Tasks are sized so each one is a coherent commit. Phrase each task as a verifiable goal, not a procedure. The task name *is* the success criterion.

Within each task, `Tests:` comes before `Approach:` — tests drive implementation, not the other way around.

Every task must declare `Depends on:` explicitly — list prior task IDs or `none`. "Obvious from order" is the failure mode that hides serial-by-default thinking. `none` is a valid and common answer; it signals work that can be done in parallel.

### Task 1: <verifiable goal>

- **Depends on:** none
- **Tests:**
  - <construction test name and what it asserts>
  - <…>
- **Approach:**
  - <step>
  - <step>
- **Done when:** <single observable predicate>

### Task 2: <verifiable goal>

- **Depends on:** Task 1 | none
- **Tests:**
- **Approach:**
- **Done when:**

## Rollout

How this component gets adopted by the rest of the kit once shipped. Specifically:
- Does any existing audit, command, agent, or skill need to be updated to call this component?
- Does AGENTS.md or any reference doc need to be edited to point at it?
- Does INVENTORY.md need a new row?

If the answer is "no callers and no doc updates," the component is unreachable — surface that as a problem.

## Risks

Specific to this implementation strategy. Risks that would change the spec are out of scope here; flag those upward via an open question on the spec.

## Changelog

Append entries when the plan changes substantially during execution. Format: `<YYYY-MM-DD>: <one-line description of the change and why>`.

-
