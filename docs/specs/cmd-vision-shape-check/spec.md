# Spec: cmd-vision-shape-check

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command
- **Serves kit phase:** Delivery (Phase-4 Vision → Initiative-or-Spec decision point)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md` (the build pattern this worker follows); `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative" (the source-of-truth for the Vision `crosses_teams:` frontmatter field that is the canonical decision signal); `tools/lint-command.sh` (the per-command shape linter this command file must pass at EXECUTE time); `.claude/commands/phase-guide.md` (analytical-command shape precedent — three-line labelled-header output); `.claude/commands/_meta/command-skeleton.md` (NOTE: this skeleton is authored for template-fill commands; this command intentionally deviates from skeleton Steps 2–4. **This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply.**); `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands" (the F4 template-fill convention; **does NOT apply to this command** — `/vision-shape-check` reads one artifact, asks at most one boolean, and emits a verdict; it does not copy a template, does not pre-fill mechanical fields, does not walk H2 placeholders interactively, does not run `tools/lint-frontmatter.py` against a written artifact, and does not chain via a `NEXT: /<creating-command> <new-slug>` artifact-creation hint); `ROADMAP.md` P4.2.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Defines the literal `.claude/commands/vision-shape-check.md` slash command — a Phase-4 *analyst-single-artifact* worker that reads a `delivery/visions/<slug>.md` artifact, inspects its `crosses_teams:` frontmatter field (plus narrative cues in §"The change" / §"What we believe and why" when the field is ambiguous), asks at most one direct boolean clarifying question of the human if and only if the field is missing or ambiguous, and emits a three-line PHASE/VERDICT/NEXT verdict header recommending either `/draft-initiative` (cross-team) or `/draft-spec` (single team). The command writes nothing; it modifies nothing; it does not invoke either downstream command. Verification is goal-based — the command file passes `tools/lint-command.sh` exit 0 — plus a manual gesture against a fixture vision.

## Objective

Ship `.claude/commands/vision-shape-check.md` — a single slash-command file, ≤ 120 body lines, that answers the question Phase 4's Vision → Initiative handover is engineered to surface: *does this Vision cross team boundaries, and therefore warrant an Initiative folder; or does it live inside a single team, and therefore warrant a single Spec?* The command's job is decision support for the human at the Vision-to-next-step boundary; it does not author the next artifact, and it does not modify the Vision.

The component does not exist today. `.claude/commands/vision-shape-check.md` is absent. The Vision artifact carries a `crosses_teams: true | false` frontmatter field per `docs/HANDOVERS.md` §"Handover 4" (line 186); this command is the first kit citizen that reads that field as its primary input. It complements `/draft-vision` (P4.1, shipped) upstream and `/draft-initiative` (P4.3, shipped) / `/draft-spec` (P4.5, shipped) downstream.

## Why now

ROADMAP P4.2 sits between P4.1 (`/draft-vision`, shipped 2026-05-23) and P4.3 (`/draft-initiative`, shipped 2026-05-23). The Phase-4 chain currently has a silent fork in the middle: a human reading a freshly drafted Vision has no commanded way to ask the kit "which downstream path?" — they either guess, or open an issue in their head. Shipping `/vision-shape-check` fills the fork with a one-command verdict that reads the Vision's own declared `crosses_teams:` field. Every other Phase-4 row above and below this one already ships; this is the last decision-support gap in the Phase-4 chain's first half.

Authoring this command after P4.1 / P4.3 shipped costs one focused work-loop. The contract is small (one read, one optional boolean, three lines out) and the inputs are stable (the Vision frontmatter shape froze with F3.6; the verdict-header shape is a sibling of `/phase-guide`'s three-line shape). The cross-cutting cost — wave-3 of Phase-4 introduces three analyst commands (P4.2, P4.9, P4.10) that share a labelled-header output format — is paid here once and reused by the other two.

## Inputs and outputs

**Inputs.**

- Positional argv: `<slug>` (the Vision slug). Required. Must match `^[a-z0-9-]+$` and be ≤ 80 chars. No flags. No `--from-*` parent-resolution.
- `delivery/visions/<slug>.md` — the Vision artifact whose shape is being decided. Required to exist. The command reads the file's YAML frontmatter (specifically the `crosses_teams:` key, which per `docs/HANDOVERS.md` §"Handover 4" line 186 is declared as `true | false`) and the narrative bodies of §"The change" and §"What we believe and why" (used only when the frontmatter field is missing or ambiguous, as additional context surfaced to the human alongside the clarifying question).
- `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative" — the source-of-truth for the `crosses_teams:` field's semantics. The command does not re-derive the rule; it cites the handover.
- `.claude/skills/work-loop/SKILL.md` — the build pattern this worker follows (plan → execute → verify → review). Not invoked at runtime; constrains the build.
- `.claude/CLAUDE.md` "How we work together" — "One clarifying question at a time. Never batch." Load-bearing for Step 2: the command asks one boolean, never a batch.

**Outputs.**

1. `.claude/commands/vision-shape-check.md` — the new slash-command file. Frontmatter: `description:` (≤ 1024 chars; one sentence) and `argument-hint: <slug>` (positional only; no flags). Body H2 structure: `## When to run`, `## Inputs`, `## Procedure` (with Steps 1–3 as H3s), `## Exit codes`, `## What this command will not do`. Body ≤ 120 lines.
2. **Runtime stdout** — exactly three labelled lines, in this exact order, with labels in ALL CAPS followed by `:` and a single space, as the structured top of the command's output:

    ```
    PHASE: Delivery → Initiative-or-Spec decision
    VERDICT: initiative | single-spec
    NEXT: /draft-initiative <slug-tbd>   OR   /draft-spec <slug-tbd>
    ```

    The `<slug-tbd>` is a literal angle-bracket placeholder — the command does not invent a next-artifact slug; the human picks it when they run the recommended downstream command. The command MAY emit additional human-readable explanatory prose before or after the three-line header, but the three labelled lines are the canonical machine-readable verdict surface. The header lines appear contiguously in the order PHASE → VERDICT → NEXT, with no blank lines between them.

3. **Runtime side effects:** none. The command writes no file, modifies no file, and invokes no other slash command. It does not run `tools/lint-frontmatter.py` against the Vision (the Vision is the input, not a fresh write). It does not flip any roadmap row.

**Exit codes.** Mirroring the Phase-4 template-fill convention's four-code semantics for kit consistency, even though the F4 convention does not formally apply:

- `0` — Vision read successfully; `crosses_teams:` either resolved directly from frontmatter, or resolved by the human's answer to the single clarifying question; verdict emitted as the three-line header.
- `1` — Human aborted before answering the clarifying question (e.g., they Ctrl-C'd or gave a non-y/n response after re-prompt). No verdict emitted; stderr message indicating abort.
- `2` — Pre-condition failure. One of: `delivery/visions/<slug>.md` does not exist; the file is unreadable; the YAML frontmatter is malformed or absent; the positional arg fails `^[a-z0-9-]+$` or is empty. Stderr carries a one-line diagnostic plus a remediation hint (e.g., "Vision `<slug>` not found at `delivery/visions/<slug>.md` — run `/draft-vision <slug>` first" or "positional arg must match `^[a-z0-9-]+$`"). NO partial output to stdout.
- `3` — RESERVED. Not used by this analyst-single-artifact shape. (The Phase-4 template-fill convention uses code 3 for "artifact written but post-write linter failed"; this command writes no artifact, so code 3 is unreachable. Declared explicitly so a reader of the four-code table is not surprised by a gap.)

## Body-shape contract

The command's body intentionally deviates from `.claude/commands/_meta/command-skeleton.md` Steps 2–4. **This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply.** The skeleton's Steps 2 (template instantiation), 3 (H2-by-H2 placeholder walk), 4 (human_owned_decisions confirmation), 5 (lint the written artifact), and 6 (NEXT chain hint to a creating command with a new slug) are not appropriate for an analyst-shape command that reads one artifact, asks at most one boolean, and emits a verdict.

The body's H2 order is exactly: `## When to run`, `## Inputs`, `## Procedure` (with Steps 1–3 as H3s), `## Exit codes`, `## What this command will not do`. The Procedure's three Steps are:

- **Step 1 — read the Vision and resolve `crosses_teams:`.** Validate the positional arg matches `^[a-z0-9-]+$`. Open `delivery/visions/<slug>.md`. If the file does not exist or YAML frontmatter is malformed, exit code 2 with diagnostic. Read the `crosses_teams:` field. If `true` → verdict `initiative`; if `false` → verdict `single-spec`; if absent or unparseable → defer to Step 2.
- **Step 2 — ask one clarifying boolean if and only if `crosses_teams:` was ambiguous in Step 1.** Surface to the human: the Vision's §"The change" body excerpt and §"What we believe and why" body excerpt as context, then ask exactly once: `"Does this vision cross team boundaries? (y/n)"`. One question, never batched (per `.claude/CLAUDE.md`). On `y` → verdict `initiative`; on `n` → verdict `single-spec`; on any other response → re-prompt once; on a second non-y/n → exit code 1. Skip this Step entirely if Step 1 already resolved.
- **Step 3 — emit the three-line PHASE/VERDICT/NEXT verdict header.** Print the three labelled lines in the exact order PHASE → VERDICT → NEXT, with labels in ALL CAPS followed by `:` and a single space, with no blank lines between them. The `NEXT:` line names `/draft-initiative <slug-tbd>` (for verdict `initiative`) or `/draft-spec <slug-tbd>` (for verdict `single-spec`), with `<slug-tbd>` as a literal angle-bracket placeholder. Exit code 0.

The deviation from the skeleton is declared verbatim in the body's `## What this command will not do` section (per the Boundaries → Never do list below).

## Boundaries

### Always do

- Read `delivery/visions/<slug>.md`'s frontmatter and check `crosses_teams:` as the *primary* decision signal before considering any narrative cue.
- Emit the verdict as a three-line PHASE/VERDICT/NEXT header — three labelled lines, ALL CAPS labels followed by `: `, in that exact order, contiguously, as the canonical machine-readable verdict surface.
- Declare in the body's `## What this command will not do` section, verbatim: "This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply."
- Cite `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative" as the source-of-truth for the `crosses_teams:` field; do not re-derive the rule in the command body.
- Exit code 2 with a remediation hint if the Vision is missing, malformed, or the positional arg is invalid.
- Ask at most one clarifying boolean, and only when the frontmatter field is absent or unparseable.

### Ask first

- If a follow-up scope question is needed beyond the single `crosses_teams:` boolean (e.g., the human says "it depends on how we slice it"), surface the ambiguity to the human and ask them to either edit the Vision's `crosses_teams:` field directly or pick a verdict explicitly. Never batch a second auto-question.
- If the human answers ambiguously to the single clarifying question (anything other than `y`/`yes`/`n`/`no` after a single re-prompt), exit code 1 — do not silently pick.

### Never do

- Never write, edit, or delete any file — including the Vision being read, any downstream initiative or spec, the INVENTORY/ROADMAP rows, or temp files on disk.
- Never invoke `/draft-initiative`, `/draft-spec`, or any other slash command automatically. The `NEXT:` line is a recommendation surfaced to the human, not an auto-chained dispatch.
- Never batch clarifying questions. The single Step-2 boolean is the only allowed question; if more clarification is needed, surface the gap and stop.
- Never invent a `<slug-tbd>` for the downstream command. The placeholder is literal; the human picks the slug when they run the next command.
- Never run `tools/lint-frontmatter.py` against the Vision — it is the input, not a fresh write.
- Never silently default `crosses_teams:` to `true` or `false` when the field is missing. Ambiguity routes to Step 2.

## Verification mode

**Goal-based check.** The command file passes `tools/lint-command.sh <path>` with exit code 0. Specifically:

- YAML frontmatter present and well-formed.
- `description:` field present, ≤ 1024 chars.
- H1 line begins with `# /` (specifically `# /vision-shape-check`).
- Body declares `## When to run` or `## Procedure` (both, in fact).

**Manual gesture.** Against a fixture Vision (a `delivery/visions/<fixture-slug>.md` whose `crosses_teams:` is set to `true`, then re-run with `false`, then re-run with the field deleted) the command produces the three correct verdict-header outputs (`initiative`, `single-spec`, `initiative`-or-`single-spec`-after-clarifying-boolean respectively). The gesture is recorded in `plan.md` Task 2.

This command is not a script with compressible invariants; TDD does not apply. There is no parametrized contract test of the form `test_phase4_command_shape.py` for it (that suite tests F4 template-fill commands only).

## Contract tests

Goal-based, gated by `tools/lint-command.sh` and a body-shape inspection. The tests below are stable against implementation change; they evolve only with spec change.

- **T1 — `tools/lint-command.sh .claude/commands/vision-shape-check.md` exits 0.** The structural gate.
- **T2 — Required H2s present.** The body contains both `## When to run` and `## Procedure` headers (the linter requires one of the two; both are required by this spec).
- **T3 — H1 is exactly `# /vision-shape-check`.** The H1 line matches the slash-command name.
- **T4 — `description:` frontmatter ≤ 1024 chars** and is a single sentence ending in a period.
- **T5 — Body declares the deviation from the F4 template-fill convention verbatim.** The string "This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply." appears in the `## What this command will not do` section.
- **T6 — Body declares the three-line PHASE/VERDICT/NEXT output shape.** The body contains all three labels `PHASE:`, `VERDICT:`, and `NEXT:` (each followed by `: `) in the Step-3 description, in that order, and names both verdict values `initiative` and `single-spec`, and names both downstream commands `/draft-initiative` and `/draft-spec`.

## Non-goals

- The command does NOT write any artifact. No Vision, no Initiative, no Spec, no INVENTORY row, no ROADMAP flip.
- The command does NOT modify the Vision — including the case where the Vision's `crosses_teams:` field is missing and the human supplies the answer at Step 2. The kit's principle is that authors edit the Vision; a verdict command does not silently write back.
- The command does NOT auto-invoke `/draft-initiative` or `/draft-spec`. The `NEXT:` line is a typed recommendation; the human runs the next command themselves.
- The command does NOT compute or recommend the next artifact's slug. `<slug-tbd>` is literal.
- The command does NOT walk multiple Visions, take a `--from-*` parent flag, or fan out. One positional, one Vision, one verdict.
- The command does NOT re-derive what "crosses teams" means. The semantics live in `docs/HANDOVERS.md` §"Handover 4"; the command cites and applies.
- The command does NOT participate in the F4 template-fill contract test suite (`scripts/tests/test_phase4_command_shape.py`). It is not a template-fill command.

## Open questions

- Q1 — Should the three-line verdict-header shape become a shared `verdict-header.md` reference doc (sibling to the F4 convention) once P4.9 and P4.10 also ship and ratify the format? **Decided by:** the cross-cutting reviewer on the wave-3 review pass; answerable after all three command specs (P4.2, P4.9, P4.10) are drafted. Not blocking for this spec.
- Q2 — When `crosses_teams:` is present but set to a non-boolean (e.g., a list, per the Initiative frontmatter's list-of-teams shape which `docs/HANDOVERS.md` line 237 also defines), should the command treat that as "ambiguous → Step 2" or as "malformed → exit 2"? **Decided by:** the human reviewer at spec-review time. Current spec says "ambiguous → Step 2" because a list of team names is itself evidence of crossing teams, but the safer alternative is to refuse parsing and exit 2.

## Acceptance criteria

- [ ] `.claude/commands/vision-shape-check.md` exists at the named path.
- [ ] T1 passes: `tools/lint-command.sh .claude/commands/vision-shape-check.md` exits 0.
- [ ] T2 passes: body contains both `## When to run` and `## Procedure`.
- [ ] T3 passes: H1 is exactly `# /vision-shape-check`.
- [ ] T4 passes: `description:` ≤ 1024 chars, single sentence ending in a period.
- [ ] T5 passes: body declares the F4-deviation sentence verbatim in `## What this command will not do`.
- [ ] T6 passes: body declares the three-line PHASE/VERDICT/NEXT output shape and names both verdicts and both downstream commands.
- [ ] Body ≤ 120 lines.
- [ ] Manual gesture against a fixture vision produces the three correct verdict-header outputs (true → initiative; false → single-spec; absent → asks clarifying boolean then emits matching verdict).

## Cross-references

- **Consumed by:** the human at the Phase-4 Vision → next-step decision point. No automated audit consumes this command's output today.
- **Consumes:** `delivery/visions/<slug>.md` (read-only); `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative" (rule source, cited).
- **Frontmatter fields read:** `crosses_teams:` (on the Vision artifact).
- **Frontmatter fields written:** none.
- **Ontology object types touched:** Vision (read). The command classifies nothing and links nothing.
- **Sibling specs (wave-3 analyst commands sharing the PHASE/VERDICT/NEXT header):** `docs/specs/cmd-spec-impact-analysis/spec.md` (P4.9), `docs/specs/cmd-audit-spec-linkage/spec.md` (P4.10).
