---
description: Decide whether a Vision warrants an Initiative folder (crosses teams) or a single Spec (single team). Reads delivery/visions/<slug>.md's crosses_teams frontmatter; asks one direct boolean if the field is ambiguous; emits a PHASE / VERDICT / NEXT verdict header recommending /draft-initiative or /draft-spec. Writes nothing.
argument-hint: <slug>
---

# /vision-shape-check

Decision support at the Phase-4 Vision → next-step boundary. Reads one Vision and recommends the downstream artifact shape (Initiative vs single Spec) based on whether the Vision crosses team boundaries. Writes nothing; modifies nothing; never auto-invokes the downstream command.

This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply. (See "What this command will not do" for the deviation declaration.)

## When to run

- After `/draft-vision` (P4.1) completes and the Vision draft is on disk
- Before deciding whether to run `/draft-initiative` (P4.3) or `/draft-spec` (P4.8)
- When the right downstream shape is unclear from the Vision narrative alone

## Inputs

1. Positional: `<slug>` — kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. The Vision's slug.
2. `delivery/visions/<slug>.md` — the Vision artifact (read-only). Primary signal is the `crosses_teams: true | false` frontmatter field, per `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative".
3. The Vision's §"The change" and §"What we believe and why" body sections — surfaced as context to the human only when the frontmatter field is missing or ambiguous.

## Procedure

### Step 1 — read the Vision and resolve `crosses_teams:`

Validate the positional matches `^[a-z0-9-]+$`. Open `delivery/visions/<slug>.md`. If the file does not exist, exit code 2 with: `"Vision '<slug>' not found at delivery/visions/<slug>.md — run /draft-vision <slug> first."` If the YAML frontmatter is malformed or absent, exit code 2 with: `"Vision at delivery/visions/<slug>.md has malformed or missing YAML frontmatter — repair it before running this command."`

Read the frontmatter `crosses_teams:` field:

- `true` → verdict `initiative`; skip Step 2.
- `false` → verdict `single-spec`; skip Step 2.
- absent or unparseable as a boolean → defer to Step 2.

### Step 2 — ask one clarifying boolean (only if Step 1 was ambiguous)

If and only if Step 1 did not resolve, surface the Vision's §"The change" and §"What we believe and why" body excerpts to the human as context, then ask exactly once:

> `Does this vision cross team boundaries? (y/n)`

One question. Never batched. On `y`/`yes` → verdict `initiative`. On `n`/`no` → verdict `single-spec`. On any other response, re-prompt once with the same question; on a second non-y/n answer, exit code 1 (human aborted) with stderr: `"Could not resolve crosses_teams: from frontmatter or human answer — aborted."`

### Step 3 — emit the three-line PHASE / VERDICT / NEXT verdict header

Print three labelled lines, in this exact order, contiguous (no blank lines between), labels in ALL CAPS followed by `: `:

```
PHASE: Delivery → Initiative-or-Spec decision
VERDICT: initiative | single-spec
NEXT: /draft-initiative <slug-tbd>   OR   /draft-spec <slug-tbd>
```

The `VERDICT:` line names exactly one value (`initiative` or `single-spec`). The `NEXT:` line names exactly one of `/draft-initiative <slug-tbd>` or `/draft-spec <slug-tbd>` corresponding to the verdict. `<slug-tbd>` is a literal angle-bracket placeholder — the human picks the downstream artifact's slug when they run that command. Exit code 0.

## Exit codes

- `0` — Vision read; verdict emitted as the three-line header.
- `1` — Human aborted before answering the Step-2 clarifying question (gave non-y/n response twice). No verdict emitted.
- `2` — Pre-condition failure: Vision missing, malformed frontmatter, or positional arg invalid. Stderr carries diagnostic + remediation hint. No stdout output.
- `3` — RESERVED. Not used by this analyst-single-artifact shape (this command writes no artifact, so the F4 convention's exit-3 "artifact written but post-write linter failed" case is unreachable here).

## What this command will not do

- **This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply.** The skeleton's Steps 2–6 (template instantiation; H2 placeholder walk; `human_owned_decisions` confirmation; written-artifact lint; new-slug chain-hint) do not run here — this command reads one artifact and emits a verdict.
- Never write, edit, or delete any file. The Vision is read-only input. No INVENTORY row, no ROADMAP flip, no `delivery/` write, no temp file.
- Never auto-invoke `/draft-initiative`, `/draft-spec`, or any other slash command. The `NEXT:` line is a typed recommendation; the human runs the next command themselves.
- Never batch clarifying questions. The single Step-2 boolean is the only allowed question; if more clarification is needed, surface the gap and stop.
- Never invent the next-artifact slug. `<slug-tbd>` is literal in the `NEXT:` line.
- Never run `tools/lint-frontmatter.py` against the Vision. The Vision is input, not a fresh write.
- Never silently default `crosses_teams:` to `true` or `false` when the field is absent. Ambiguity routes to the Step-2 clarifying question.
- Never re-derive what "crosses teams" means. The semantics live in `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative"; this command cites and applies.

$ARGUMENTS
