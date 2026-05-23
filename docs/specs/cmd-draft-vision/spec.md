# Spec: cmd-draft-vision

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** slash command
- **Serves kit phase:** Delivery
- **Constrained by:** parent spec `docs/specs/phase-4-command-convention/spec.md` (the F4 template-fill command convention; carries body-structure, argv, parent-resolution, interactive-fill, pre-fill, linter, exit-code, and chaining contracts); `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative" (the source-of-truth for Vision required frontmatter and required sections); `templates/vision.md` (the F3.6 template this command consumes; shipped 2026-05-22); `docs/specs/template-vision/spec.md` (the F3.6 sibling spec — shape precedent for a per-component spec under the Phase-4 fan-out); `tools/lint-frontmatter.py` (default-mode linter the command runs against the written artifact); `tools/lint-command.sh` (the per-command shape linter this command file must pass); `.claude/skills/work-loop/SKILL.md` (the build pattern this worker follows); `ROADMAP.md` P4.1.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Defines the literal `.claude/commands/draft-vision.md` slash command — a Phase-4 *artifact-creating* template-fill worker that reads a `validation/learnings/<slug>.md` memo (status not `killed`), copies `templates/vision.md` to `delivery/visions/<slug>.md`, walks the template's six H2 sections one question at a time with the human, runs `tools/lint-frontmatter.py` against the written file, and emits a `NEXT: /draft-initiative <initiative-slug>` chain hint. The command's body follows `.claude/commands/_meta/command-skeleton.md` verbatim; per-command additions (the actual interactive prompts; the per-command non-behaviors) are enumerated below. Verification is goal-based — the command file passes `tools/lint-command.sh`, and the five parametrized in-scope tests for `draft-vision` in `scripts/tests/test_phase4_command_shape.py` flip from `pytest.skip` to `pass`.

## Objective

Ship `.claude/commands/draft-vision.md` — a single slash-command file, ≤ 120 body lines (skeleton parity), that authors a `delivery/visions/<slug>.md` Vision artifact end-to-end from a surviving learning memo. The command is the first link in the Phase-4 chain: it gates Handover 4 (Validation → Delivery) and emits the next-command hint that pulls the chain forward into `/draft-initiative`. The command is an **artifact-creating** worker in the Phase-4 sub-classification (per `phase-4-command-convention` §"Convention-text contract" → "Artifact-creating commands"); its positional is `<slug>` (the new Vision slug), and its destination is the new path `delivery/visions/<slug>.md`.

The component does not yet exist. `.claude/commands/draft-vision.md` is absent today. The parent convention has shipped `.claude/commands/_meta/command-skeleton.md` (the file this command copies), the convention text under `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands", and the contract test at `scripts/tests/test_phase4_command_shape.py` (currently auto-skipping `draft-vision`).

## Why now

ROADMAP P4.1 `/draft-vision` is the first row in the Phase-4 block and the first link in the seven-command chain that runs Validation → Delivery handovers. Two upstream dependencies are now stable: F3.6 `templates/vision.md` shipped 2026-05-22 (the template shape is locked); the F4 parent convention shipped 2026-05-23 (the command shape is locked). With both upstream contracts frozen, `draft-vision` can be authored without inventing either a Vision shape or a command shape. Authoring it now turns the Vision artifact from contract-on-paper into a one-command interactive draft, and unblocks the rest of the Phase-4 chain that takes a Vision as input (`/draft-initiative` P4.3 has `Depends on: P4.1`).

The cost of authoring after the convention shipped: one focused work-loop. The cost of authoring before the convention: re-deriving body structure, argv, parent-resolution, interactive-fill, and exit-code conventions from scratch — exactly the seven-way drift the convention exists to prevent.

## Inputs and outputs

**Inputs.**

- `.claude/commands/_meta/command-skeleton.md` — the literal file to copy as the starting point. Pre-fill rules per the parent convention's §"Skeleton-text contract".
- `docs/specs/phase-4-command-convention/spec.md` — the F4 convention. This spec consumes the convention by reference; this spec adds only the per-command additions (the actual interactive prompts, the per-command non-behaviors).
- `docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md` — the editorial checklist the spec satisfies (five rows).
- `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative" — the source-of-truth for Vision required frontmatter (top-level keys, three nested list-of-maps blocks, the three `human_owned_decisions:` entries) and the six required H2 sections. The interactive prompts below are organized H2-by-H2 against this contract.
- `templates/vision.md` (F3.6, shipped 2026-05-22) — the single-file template the command copies. Six H2 sections per HANDOVERS-4: The customer-shaped pitch / The change / What we believe and why / What we're still betting on / Counter-metrics / Predicted outcomes.
- `validation/learnings/` — the parent-artifact family. Each memo carries `object_type: Learning Memo` (per HANDOVERS Handover 3) with a `status:` of `survived` or `killed`. The command filters out `killed` (the convention's terminal-or-killed set; the Learning-Memo track's `killed` value is the analog of the product-artifact track's `Deprecated`).
- `tools/lint-frontmatter.py` (default mode, NOT `--check-template`) — the linter the command runs against the written `delivery/visions/<slug>.md` after the fill completes. Default mode walks `delivery/` per the F3 convention.
- `tools/lint-command.sh` — the per-command shape linter that gates this command file at build time (and the contract test's `test_inscope_commands_pass_lint` case at session time).
- `scripts/tests/test_phase4_command_shape.py` — the contract test that auto-tightens when this command ships. Its `INSCOPE` constant already lists `draft-vision`; its `POSITIONAL` constant already declares `"draft-vision": "<slug>"`.
- `.claude/skills/work-loop/SKILL.md` — the build pattern this worker follows (plan → execute → verify → review).
- `.claude/CLAUDE.md` "How we work together" — "One clarifying question at a time. Never batch." The interactivity contract the Step-3 walk encodes per-question.

**Outputs.**

1. `.claude/commands/draft-vision.md` — the new slash-command file. Frontmatter: `description:` (≤ 1024 chars; one sentence) and `argument-hint: <slug> [--from <learning-slug>] [--force]` (creating-command form, per convention argv contract). Body follows `.claude/commands/_meta/command-skeleton.md` H2 structure verbatim — `## When to run`, `## Inputs`, `## Procedure` (Steps 1–6), `## What this command will not do` — with the per-command fill enumerated in §"Per-section interactive prompts" and §"Boundaries → Never do" below. Body ≤ 120 lines (skeleton parity).
2. One-line check on `ROADMAP.md` P4.1 row: `[ ]` → `[x]` with `Shipped: <date>` per the CAPTURE phase. Enumerated in `plan.md` Task 4.
3. One-line update on `docs/INVENTORY.md` for the `/draft-vision` row. Enumerated in `plan.md` Task 4.

**Written artifact (what the command produces at runtime).** A `delivery/visions/<slug>.md` file shaped per HANDOVERS-4 (its frontmatter and six required sections), pre-filled per the convention's §"Pre-fill rules" (`id`, `slug`, `created`, `last_updated`, `parent_intent`, `parent_learning`, `object_type`), with the six H2 bodies filled interactively from the human's answers to the prompts below. The command runs `tools/lint-frontmatter.py` against this file before declaring success.

**NEXT-line behavior.** The command's last output line is `NEXT: /draft-initiative <initiative-slug>` where `<initiative-slug>` is a literal angle-bracket placeholder (the Vision draft does not pre-determine the Initiative slug; the human chooses it when they run `/draft-initiative` next). This is consistent with the convention's chaining-hint contract (`NEXT: /<command-name> <slug>` where `<slug>` is the *next* artifact's slug). The command does NOT prompt the human for the Initiative slug — that conversation belongs to `/draft-initiative`, not here. The placeholder makes the chain transition explicit without leaking forward-looking decisions into the Vision draft. The command emits NO `REVIEW:` interstitial — only `/sequence-initiative` emits one (per convention §"Capabilities-file interstitial").

## Body-shape contract

The command body follows `.claude/commands/_meta/command-skeleton.md` verbatim. The skeleton's six Steps are copied as-is; the per-command fill replaces the skeleton's `<placeholder>` substitutions with the concrete values below. No new H2 sections are introduced; no Step is renumbered, deleted, or merged. The body's H2 order is exactly: `## When to run`, `## Inputs`, `## Procedure` (with Step 1 through Step 6 as H3s), `## What this command will not do`.

## Per-section interactive prompts

The H2-by-H2 prompts the command speaks to the human during Step 3 (walk placeholders one section at a time). Each prompt is the exact phrasing the command emits; no batching. Within an H2 that has H3 sub-units (only "What we're still betting on", which tiers assumptions), the H3 prompts are enumerated separately. The kit's "one clarifying question at a time" rule from `.claude/CLAUDE.md` is load-bearing here.

### H2 1 — The customer-shaped pitch

> "In one paragraph, narrative voice: who is the customer, what problem are they hitting, and how does this change land in their words? Draw on the surviving learning memo `<parent-learning-slug>` — paraphrase the customer language verbatim where you can."

### H2 2 — The change

> "In one paragraph: what is different for the customer when this ships? Name the before-state and the after-state in the customer's own frame — not in feature language."

### H2 3 — What we believe and why

> "In one paragraph: which beliefs anchor this Vision, and which learning memos anchor each belief? Cite the memo slugs inline (e.g., `validation/learnings/<slug>.md`). Beliefs without a cited memo are surfaced as Open Assumptions in the next section, not here."

### H2 4 — What we're still betting on

This H2 has three H3 tiers per HANDOVERS-4 and the F3.6 template. The command walks them in order; each H3 is its own fill unit; do not advance to H2 5 until all three are confirmed.

#### H3 4a — must-test-before-shipping

> "What's the riskiest assumption that, if wrong, kills the Vision and must be tested before any shipping? One assumption per line. Each one becomes a `tier: must-test-before-shipping` entry in `open_assumptions:`. If there are none, say 'none' — I'll record an empty list and we move on."

#### H3 4b — accept-as-bet

> "What assumptions are you accepting as bets — explicitly known-uncertain, but you're choosing to commit and learn on the way? One per line. Each one becomes a `tier: accept-as-bet` entry."

#### H3 4c — will-monitor-post-ship

> "What assumptions will you watch in production but not test pre-ship? One per line. Each one becomes a `tier: will-monitor-post-ship` entry."

### H2 5 — Counter-metrics

> "In one paragraph: which metrics would tell us we made the product *worse*, not better? For each counter-metric, give me the KPI id (format `KPI-NNN` per the ontology). If the KPI doesn't yet have an id, say so — I won't fabricate one; you create the KPI separately and we link it back."

### H2 6 — Predicted outcomes

> "In one paragraph: what does success look like, and how will you measure it? For each predicted outcome, give me three values: the KPI id (`KPI-NNN`), the threshold (the numeric or qualitative bar that counts as success), and the measure-at horizon (weeks-after-launch). If you don't have the KPI ids yet, name the metric in prose and I'll surface 'KPI id needed' as an open item — I won't invent ids."

## Pre-fill rules

Before the Step-3 walk begins, the command pre-fills the mechanical fields the F3.6 template's frontmatter declares as placeholders (per convention §"Pre-fill rules"):

- `id:` — derived as `VIS-<NNN>` where `<NNN>` is the next unused integer in `delivery/visions/` (scan existing files for `id: VIS-` lines, take max + 1, zero-pad to three digits).
- `slug:` — the positional argument, validated as kebab-case `^[a-z0-9-]+$` and ≤ 80 chars per the convention's argv contract.
- `created:` — today's date, ISO-8601, resolved from the system clock at command start.
- `last_updated:` — same as `created` on first instantiation.
- `parent_learning:` — the resolved learning-memo slug from Step 1.
- `parent_intent:` — restated for traceability per HANDOVERS-4; resolved by reading the chosen learning memo's `parent_intent:` field (the memo carries it from HANDOVERS-3). If the memo's `parent_intent:` is empty, ask the human for the slug and surface the missing-link as an Open Question on the Vision.
- `object_type: Vision` — already pre-filled in `templates/vision.md` per F3.6; the command re-asserts it (defensive check).
- `status: Draft` — already pre-filled in `templates/vision.md`; the command re-asserts.

The human is never asked to type any of these. If a mechanical field cannot be resolved (no learning memo found; `parent_intent:` empty on the chosen memo and human declines to supply), the command stops and reports the missing pre-condition with a remediation suggestion.

## Parent-artifact-resolution rule

The parent-artifact family is `validation/learnings/`. The command applies the convention's resolution rule (Step 1) as follows:

- If `--from <learning-slug>` is given, use it. The command verifies the file exists at `validation/learnings/<learning-slug>.md`; if not, exit code 2 with a remediation suggestion naming the malformed slug.
- Otherwise, list candidate learning memos in `validation/learnings/` filtered by `status:` not in `{killed}`. The Learning-Memo track's terminal-or-killed set per HANDOVERS-3 is `{killed}` only (the `survived` track is the live one). Sort by `last_updated:` descending; cap at 10 most-recent.
- Present the candidates as a numbered list; ask the human to pick one (or `--from` for an older candidate). **Always confirm even on a single candidate** (per convention Open Question 7).
- If the candidate list is empty, exit code 2 with the exact remediation suggestion: *"no learning memo found in `validation/learnings/` with `status:` not in `{killed}`. Run `/learning-memo` first to produce a surviving learning, then re-run `/draft-vision <slug>`."*

The command never silently picks. The auto-pick failure mode is exactly the silent failure HANDOVERS-4 is designed to prevent (a Vision attached to the wrong learning memo, polluting every downstream Initiative and Spec).

**Per-command non-behavior — refuse `killed` memos.** The convention's terminal-or-killed-set filter already excludes `status: killed` from the candidate list. The command adds a belt-and-suspenders check: if `--from <learning-slug>` names a memo whose `status:` is `killed`, exit code 2 with the message *"learning memo `<slug>` has `status: killed`; a Vision cannot be drafted from a killed learning. Pick a memo with `status: survived` or re-run `/learning-memo` to capture a new learning."* This protects against an adopter explicitly overriding into a known-bad parent.

## Linter integration

After the interactive fill completes (Step 5 of the convention's body skeleton), the command resolves the repo root as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py` (do not assume cwd is the repo root) and runs `python3 <repo-root>/tools/lint-frontmatter.py delivery/visions/<slug>.md` in **default mode** (NOT `--check-template`; the artifact is now a real product artifact, not a template).

- Exit 0 → proceed to Step 6 (emit NEXT line).
- Non-zero → surface the linter output, offer to re-open the relevant sections for correction. If the human accepts and re-lint exits 0, proceed normally. If the human declines (or re-lint still fails), exit code 3 with the artifact left on disk in the known-imperfect state.

## Exit codes

The four convention exit codes apply verbatim; no per-command additions:

- `0` — Vision written at `delivery/visions/<slug>.md`, linter passed, NEXT line emitted.
- `1` — human aborted the Step-3 walk before completion. Partial artifact left at `delivery/visions/<slug>.md`; command emits a "resume by re-running `/draft-vision <slug>`" hint.
- `2` — pre-conditions failed: no candidate learning memo, malformed slug, destination already exists without `--force`, `templates/vision.md` missing, `--from` names a `killed` or non-existent memo, mechanical pre-fill cannot be resolved. Artifact not written.
- `3` — Vision written but post-fill linter exited non-zero and human declined (or failed) correction. Artifact persists in a known-imperfect state. Automation consumers MUST treat exit 3 as distinct from exit 0.

## Chaining hint

Last line of output, formatted exactly:

```
NEXT: /draft-initiative <initiative-slug>
```

No `REVIEW:` interstitial line is emitted (per convention §"Capabilities-file interstitial", only `/sequence-initiative` emits one). The `<initiative-slug>` is a literal angle-bracket placeholder; the human supplies a concrete slug when they invoke `/draft-initiative`.

## Boundaries

### Always do

- Walk the six H2 sections of `templates/vision.md` in HANDOVERS-4 order (`The customer-shaped pitch` → `The change` → `What we believe and why` → `What we're still betting on` → `Counter-metrics` → `Predicted outcomes`).
- Walk the three H3 tiers under "What we're still betting on" as separate fill units (must-test-before-shipping → accept-as-bet → will-monitor-post-ship), confirming each tier before advancing.
- Pre-fill `id: VIS-<NNN>`, `slug`, `created`, `last_updated`, `parent_learning`, `parent_intent`, `object_type: Vision`, `status: Draft` before the Step-3 walk begins.
- Run `tools/lint-frontmatter.py` (default mode) against the written file in Step 5, with the repo-root resolution rule (do not assume cwd).
- Emit the `NEXT: /draft-initiative <initiative-slug>` line as the last line of output, with the literal angle-bracket placeholder.
- Confirm the parent learning memo even when only one candidate exists.
- Surface every `human_owned_decisions:` entry (the three from HANDOVERS-4: customer-shaped framing, differentiator selection, predicted outcome thresholds) for explicit human confirmation in Step 4 before linting.

### Ask first

- Adding any frontmatter key to the written Vision artifact beyond what HANDOVERS-4 specifies. The command is a re-projection of the contract, not a superset.
- Auto-promoting an `open_assumption:` from one tier to another based on heuristics (e.g., promoting a `will-monitor-post-ship` to `accept-as-bet` because it "feels" risky). The tiering is a `human_owned_decisions:` field — the human owns it.
- Pre-filling `predicted_outcomes[*].kpi_id` or `counter_metrics[*].kpi_id` from any heuristic (search for KPI ids in the chosen learning memo; assume a default; etc.). The KPI id is a human input; the command never invents one.

### Never do

- Write a Vision when the chosen learning memo's `status:` is `killed`. Refuse via exit code 2 (per §"Parent-artifact-resolution rule"). The Validation → Vision causal chain requires a surviving learning; drafting from a killed one is the silent failure HANDOVERS-4 prevents.
- Fabricate `predicted_outcomes[*].kpi_id` or `counter_metrics[*].kpi_id` values. KPI ids are human-owned per HANDOVERS-4's "Predicted outcome thresholds" `human_owned_decisions:` entry; if the human doesn't have the id, the command records "KPI id needed" as an open item, not a synthesized `KPI-001`.
- Batch the six H2 prompts (or the three H3 tier prompts) into a single multi-question turn. The "one question at a time, never batch" rule from `.claude/CLAUDE.md` is the load-bearing interactivity contract.
- Silently pick a parent learning memo when only one candidate exists. Always confirm.
- Overwrite an existing `delivery/visions/<slug>.md` without `--force`. Exit code 2 with a remediation suggestion.
- Auto-invoke `/draft-initiative` after the Vision is written. The chain is human-driven (the NEXT line is a hint, not an automatic dispatch).
- Modify `templates/vision.md`. The template is frozen by F3.6; this command wraps it, it does not change it.
- Assume the current working directory is the repo root when invoking the linter. Always resolve repo root upward.
- Pre-fill `human_owned_decisions:` with anything other than the three values HANDOVERS-4 names verbatim (Customer-shaped framing of the value proposition / Differentiator selection / Predicted outcome thresholds). The list is contract-mandated; do not add or rephrase entries.

## Verification mode

- **Goal-based check** — the command file's "shape" is the contract. `tools/lint-command.sh .claude/commands/draft-vision.md` exits 0 (gates frontmatter presence, `description:` length, H1 starting with `/`, and at least one of the required body H2s). The five parametrized in-scope test cases for `draft-vision` in `scripts/tests/test_phase4_command_shape.py` flip from `pytest.skip` to `pass` (lint passes; required H2s present; argv positional `<slug>`; template path `templates/vision.md` cited and exists; destination directory `delivery/visions/` cited and exists).
- **Audit-driven** — kit-wide health: `bash tools/pre-pr.sh` exits 0.

The command itself is **not** verified by a manual end-to-end runtime gesture in this spec's verify phase. A runtime exercise (run `/draft-vision <fixture-slug>` against a real learning memo and read the written file) is a future smoke-test candidate but not a contract test. The contract test plus the linter together encode every machine-checkable claim.

## Contract tests

Each test is one shell line or one pytest case. They are the gate. T1–T5 are the five parametrized in-scope tests in `scripts/tests/test_phase4_command_shape.py` flipping from skip to pass for `draft-vision`.

- `T1` — `bash tools/lint-command.sh .claude/commands/draft-vision.md` exits 0. (Convention contract test `test_inscope_commands_pass_lint` parametrized for `draft-vision`.)
- `T2` — `.claude/commands/draft-vision.md` body contains all four required H2s in order: `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`. (`test_inscope_commands_have_required_h2s` parametrized for `draft-vision`.)
- `T3` — frontmatter `argument-hint:` starts with the literal token `<slug>` (the creating-command positional per `POSITIONAL["draft-vision"]`). (`test_inscope_commands_declare_argv` parametrized for `draft-vision`.)
- `T4` — body contains the path `templates/vision.md` and that path exists in the repo. (`test_inscope_commands_cite_template_path` parametrized for `draft-vision`.)
- `T5` — body contains a `delivery/visions/` path and the directory `delivery/visions/` exists in the repo. (`test_inscope_commands_cite_destination_path` parametrized for `draft-vision`.)
- `T6` — `python3 -m pytest scripts/tests/test_phase4_command_shape.py -v` exits 0. All five parametrized in-scope cases for `draft-vision` flip from skip to pass; the other six commands continue to auto-skip.
- `T7` — body ≤ 120 lines (skeleton parity, soft cap): `[[ $(awk '/^---$/{f=!f; if(!f)c=0} f{c++} END{print c}' .claude/commands/draft-vision.md) -le 120 ]]` exits 0.
- `T8` — frontmatter `description:` field present and ≤ 1024 chars. (Already enforced by `tools/lint-command.sh`; restated here for completeness.)
- `T9` — H1 line is exactly `# /draft-vision` (literal verb; the skeleton's `<command-name>` placeholder is replaced).
- `T10` — kit-wide health: `bash tools/pre-pr.sh` exits 0.

## Non-goals

- Authoring `/draft-initiative` (P4.3) or any other command downstream in the Phase-4 chain. Each is a separate spec running in parallel under the F4 fan-out.
- Authoring a Vision artifact under `delivery/visions/<slug>.md` directly. This spec ships the *command* that authors Visions; a real Vision is produced at the human's invocation, not at spec ship time.
- Modifying `templates/vision.md` (F3.6, frozen 2026-05-22), `tools/lint-frontmatter.py`, `tools/lint-command.sh`, `scripts/tests/test_phase4_command_shape.py`, or `.claude/commands/_meta/command-skeleton.md`. The command consumes these; it does not change them.
- Adding tier-enum validation logic to the linter for `open_assumptions[*].tier`. The default-mode linter's validation of instantiated artifacts is the linter's responsibility, not this command's.
- Auto-invoking `/draft-initiative` after the Vision is written. The chain is human-driven; the `NEXT:` line is a hint, not a dispatch.
- Running any of the audits (`/audit-traceability`, `/audit-completeness`, `/audit-portfolio-coherence`) as part of the command. Audits are explicit human gestures at the human's choosing.
- Authoring multiple Visions in a single invocation. One slug, one Vision, one work-loop session.
- Pre-filling the Initiative slug in the `NEXT:` line. The Initiative slug is `/draft-initiative`'s positional, not this command's responsibility to pre-determine.

## Open questions

None. The eight Open Questions on the parent convention spec are resolved there; the per-section interactive prompts are specified verbatim above; the parent-resolution rule and the `killed`-memo refusal are explicit; the `NEXT:` line's literal-placeholder behavior is documented. No genuine OQ remains that requires sign-off before EXECUTE.

## Acceptance criteria

- [ ] `.claude/commands/draft-vision.md` exists, single file.
- [ ] Body ≤ 120 lines (T7).
- [ ] `bash tools/lint-command.sh .claude/commands/draft-vision.md` exits 0 (T1).
- [ ] Required four H2s present in order (T2).
- [ ] `argument-hint:` frontmatter starts with `<slug>` (T3).
- [ ] Body cites `templates/vision.md` and the file exists (T4).
- [ ] Body cites `delivery/visions/` and the directory exists (T5).
- [ ] `python3 -m pytest scripts/tests/test_phase4_command_shape.py -v` exits 0; all five parametrized cases for `draft-vision` pass (no longer skip) (T6).
- [ ] H1 is `# /draft-vision` (T9).
- [ ] `bash tools/pre-pr.sh` exits 0 (T10).
- [ ] The six H2 interactive prompts and the three H3 tier prompts in §"Per-section interactive prompts" appear in the command body verbatim (the prompts are the load-bearing per-command fill — without them, the command is generic).
- [ ] The `killed`-memo refusal text appears in `## What this command will not do` and the parent-resolution prose.
- [ ] No new ontology type added; no F3.6 template modified; no `tools/` script modified; no `scripts/tests/` file modified; no skeleton modified.

## Cross-references

- **Consumes:** `docs/specs/phase-4-command-convention/spec.md` (parent convention); `docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md`; `docs/HANDOVERS.md` §"Handover 4: Vision → Initiative"; `templates/vision.md` (F3.6); `.claude/commands/_meta/command-skeleton.md`; `tools/lint-frontmatter.py` (default mode); `tools/lint-command.sh`; `scripts/tests/test_phase4_command_shape.py`; `.claude/skills/work-loop/SKILL.md`; `.claude/CLAUDE.md` "How we work together".
- **Consumed by:** ROADMAP P4.3 `/draft-initiative` (the next chain link; consumes the `delivery/visions/<slug>.md` artifact this command writes).
- **Frontmatter fields owned:** none directly on this spec (specs are universal-schema-exempt); specifies the pre-fill rules for the `id`, `slug`, `created`, `last_updated`, `parent_learning`, `parent_intent`, `object_type`, `status` fields of the *written* Vision artifact.
- **Ontology object types touched:** Vision (Domain I composite; the `object_type:` of the written artifact). The command does not introduce new ontology types.
