# Spec: <component-name>

- **Status:** Draft | In Review | Approved | Implementing | Shipped | Frozen
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** skill | agent | command | hook | script | framework-ref | template | guide
- **Serves kit phase:** Strategy | Discovery | Validation | Delivery | Landings | Cross-cutting | Meta (kit itself)
- **Constrained by:** <ADR / RFC / parent spec ids>

> **Spec contract.** This document defines what "done" means for this kit component. The implementing work must match this spec, or update it in the same session. Verification must be derivable from this spec — if a behavior isn't here, it isn't promised.

## Objective

One paragraph. What this component is, what problem in the kit it solves, what concrete behavior changes when it ships.

If the component already exists in a stub form somewhere (a markdown file describing it, an inventory entry), name where so an agent can find the prior context.

## Why now

One paragraph. Why this is the right thing to build next given the current state of the kit. What it unblocks. Which other roadmap items depend on it.

## Inputs and outputs

**Inputs.** What this component reads. Files, frontmatter fields, context the orchestrator passes in, environment, other kit components it calls.

**Outputs.** What this component writes. Files produced, frontmatter set, exit codes, stdout/stderr contracts, side effects on disk.

A reader of this section should be able to write the component's interface signature without reading anything else.

## Boundaries

The three-tier guard that keeps an implementing agent inside the lines. *Always do* applies without asking; *Ask first* requires human sign-off before proceeding; *Never do* is a hard rule, even under time pressure.

### Always do

-
-
-

### Ask first

-
-
-

### Never do

-
-
-

## Verification mode

Name the verification mode(s) this spec uses. The `work-loop` skill defines four for kit-build work:

- **TDD** — for scripts with compressible invariants (audit logic, validators, parsers). Tests come before code.
- **Goal-based check** — a one-liner verifies the outcome (a linter exit code, a `grep`, a JSON-schema check). For artifacts whose "shape" is the contract.
- **Manual gesture** — a recorded reproduction step against a known fixture, for components whose behavior emerges in interactive Claude Code sessions and can't be cheaply automated.
- **Audit-driven** — the component is "done" when the relevant kit audit (`/audit-completeness`, `/audit-traceability`, `lint-skill.sh`, etc.) returns clean.

A spec may pick one or mix them. State which mode each behavior falls under, and why.

## Contract tests

Black-box tests that define "done." These are the gate. Any valid implementation must pass them. They are stable against implementation change; they evolve only with behavioural (spec) change.

For scripts: list test cases by name with inputs and expected outputs. Place actual test files under `tests/` adjacent to the script and reference them here.

For skills/agents/commands: list the manual-gesture reproductions or audit-pass checks that constitute "done."

For frontmatter / schema components: list the JSON-schema or linter assertions.

## Non-goals

What this component will explicitly NOT do. The dog that doesn't bark — often more informative than the goals.

## Open questions

Things this spec deliberately leaves unresolved. Each open question should name who can answer it and when (before implementing? at first review? after first usage?).

## Acceptance criteria

The list a reviewer reads to decide whether to approve a PR. Each criterion is a verifiable predicate. The work-loop's verify phase walks this list.

- [ ]
- [ ]
- [ ]

## Cross-references

- **Consumed by:** which audits, commands, agents, or skills call this component
- **Consumes:** which audits, commands, agents, or skills this component calls
- **Frontmatter fields owned:** which fields of the universal metadata schema this component reads or writes
- **Ontology object types touched:** which Domain A-H types this component classifies, links, or audits
