# Plan: ontology-classifier-skill

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

## Approach

Author a single `SKILL.md` ≤ ~250 lines plus a `fixtures/golden.md` with 5 inputs and expected classifications. SKILL.md teaches the classification protocol: read input, split into chunks, classify each chunk against the ontology, emit the structured proposal block.

The skill is a doctrine document, not a script. The "test" is the manual-gesture: load the skill in a fresh session, feed each golden fixture, verify the output matches. The lint-skill.sh check is the shape gate.

## Constraints

- Single SKILL.md, ≤ ~250 lines.
- Reference `context/frameworks/ontology.md` for the type list; don't embed.
- Manual-gesture verification recorded in `notes/manual-verification-2026-05-21.md`.
- No code dependencies (this is a skill, not a script).

## Tasks

### Task 1: Author `SKILL.md`

- **Depends on:** none.
- **Tests:**
  - `tools/lint-skill.sh .claude/skills/ontology-classifier/SKILL.md` exits 0.
  - SKILL.md frontmatter declares `name`, `description`, `tools: [Read, Grep, Glob]` (read-only access to the ontology + the input source), `model: sonnet`.
- **Approach:**
  - Frontmatter per the kit's skill convention.
  - Body sections: When to use; Inputs; Output (the structured proposal block, with example); How to classify (protocol: split → classify → field-resolve → confidence-label); The `| Adapted` escape hatch; Hard rules; Common gaps.
- **Done when:** SKILL.md exists, lint passes.

### Task 2: Author the 5 golden fixtures

- **Depends on:** Task 1.
- **Tests:** fixtures file exists with the 5 inputs and the expected classifications per spec §Contract tests.
- **Approach:**
  - `.claude/skills/ontology-classifier/fixtures/golden.md` lists each fixture as: `### Fixture N — <name>` / Input (block-quoted) / Expected (object_type, required fields, confidence summary).
- **Done when:** file exists; expected blocks are concrete enough for a verifier to compare against.

### Task 3: Manual-gesture verification

- **Depends on:** Tasks 1 + 2.
- **Tests:** for each fixture, the documented expected output is produced by Claude when the skill is loaded.
- **Approach:**
  - Verification MUST be performed in a fresh Claude Code session that has not been used to author the skill (per spec AC). Record outcomes in `docs/specs/ontology-classifier-skill/notes/manual-verification-2026-05-21.md` as a table: fixture | expected type | actual type | pass/fail | notes.
- **Done when:** verification table filled; 5 of 5 fixtures produce a top-level classification block; ≥4 of 5 proposed `object_type` values match the expected type exactly. A skill-flagged "candidates" block (not a top-level classification) counts as a miss for verification purposes; the missed fixture must be recorded with the actual output and an explicit `open_questions` entry, not silently passed.

### Task 4: Register

- **Depends on:** Tasks 1-3.
- **Tests:** the planned-marker grep returns zero hits for `ontology-classifier.*planned` (case-insensitive) across AGENTS.md, .claude/CLAUDE.md, context/README.md, .claude/skills/README.md, INVENTORY.md, **and `docs/adr/0002-adopt-product-business-ontology.md`** (which has two `planned — ROADMAP F1.3` occurrences at lines 62 and 117).
- **Approach:**
  - AGENTS.md: remove the planned-marker annotation.
  - .claude/CLAUDE.md: replace planned-marker with brief "shipped" mention.
  - context/README.md: update the ontology section's planned-marker.
  - `.claude/skills/README.md`: move from Planned to Shipped with a one-line description.
  - INVENTORY.md: flip status to `shipped` on the relevant row.
  - **`docs/adr/0002`**: line 62 — flip the planned-status annotation on the `ontology-classifier` skill bullet to "shipped 2026-05-21"; line 117 (in "Mitigated by" prose) — leave the retrospective decision-rationale text as historical context but add a parenthetical: "(shipped 2026-05-21 per F1.3)". User has authorized inline ADR edits during v0.x standup.
  - ROADMAP.md: check off F1.3.
- **Done when:** grep returns clean across all 6 files; all docs reflect shipped status.

## Rollout

- Downstream commands and agents can instruct Claude to load and follow this skill when they encounter unstructured input. (The skill is a doctrine document, not a programmatic API — "call out to" here means "include `Skill ontology-classifier` in the orchestrator's instructions," not an in-process function call.)
- The kit's "when uncertain" advice in AGENTS.md is now actionable.

## Risks

- **Skill drift vs ontology.** If the ontology adds Domain I types after the skill ships, the skill must learn about them. Mitigation: the SKILL.md explicitly instructs Claude to re-load `context/frameworks/ontology.md` on each invocation (per spec §Always do); new types are picked up automatically because the type list isn't embedded in the skill, only referenced.
- **Manual-gesture verification is subjective.** Two verifiers might score the same output differently. Mitigation: expected outputs for each fixture specify (a) the `object_type` value, (b) at least three required fields with their expected confidence label, (c) whether the fixture is single-chunk or multi-chunk. This is concrete enough for structural comparison.

## Changelog

- 2026-05-21: Initial plan.
