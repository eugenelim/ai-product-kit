# Spec: cmd-draft-spec

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command
- **Serves kit phase:** Delivery (Phase 4) — gates Handover 5 (Initiative → Spec) by authoring one PM Spec under an existing Initiative folder.
- **Constrained by:** `docs/specs/phase-4-command-convention/spec.md` (the parent F4 authoring convention this command instantiates — argv contract, body structure, parent-resolution rule, interactive-fill discipline, pre-fill rules, exit codes, chaining hint); `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" (the parent Initiative folder contract whose `child-specs.md` manifest this command appends to); `docs/HANDOVERS.md` §"Handover 6: Spec → Engineering Handoff Packet" (downstream consumer — the PM Spec this command writes is the per-feature input the Handoff Packet aggregates); `templates/pm-spec.md` (the F3.8 single-file template this command consumes — shipped 2026-05-22); `docs/specs/template-pm-spec/spec.md` (the F3.8 spec that authored the template; Open Question 2 OVERRIDES the parent template-authoring-convention's Open Question 2 and resolves the destination to `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` — single file, not folder); `docs/specs/template-authoring-convention/spec.md` Open Question 2 (initial directory resolution to `delivery/initiatives/<initiative-slug>/specs/`; the per-spec form is the single-file override from F3.8); `tools/lint-command.sh` (existing shape linter for `.claude/commands/*.md`); `tools/lint-frontmatter.py` (default mode — the linter this command runs against the artifact it writes); `.claude/skills/work-loop/SKILL.md` (the build pattern this command's spec follows); `.claude/CLAUDE.md` "How we work together" (one-question-at-a-time interactivity contract); ROADMAP P4.8.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships `.claude/commands/draft-spec.md` — an **artifact-creating** Phase-4 template-fill slash command. Reads an existing Initiative folder; copies `templates/pm-spec.md` to `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`; walks the template's placeholders one H2 section at a time interactively; appends a row to the parent Initiative's `child-specs.md` manifest (the load-bearing side effect that gates Handover 5 → Handover 6 traceability); runs `tools/lint-frontmatter.py` against the written file; emits a `NEXT:` chaining hint. Deviates from the parent convention in TWO documented places: (1) the two-positional resolution form (`/draft-spec <slug> --from <initiative-slug>`) — `--from` is required-or-prompted-for, because a PM Spec's destination path is initiative-nested and the command cannot resolve the destination without an initiative slug; (2) the Procedure has SEVEN numbered Steps instead of the convention's six — the `child-specs.md` append (Step 6) is a non-homogeneous side-effect that must be separated from the chaining-hint emit (Step 7) so the side-effect can be skipped cleanly on exit code 3 without aborting the NEXT emit. Per the convention's `Boundaries → Never do` rule, both deviations are surfaced here for the per-command adversarial review.

## Objective

`/draft-spec` is the Phase-4 command that turns one row in an Initiative's `child-specs.md` manifest into a real PM Spec on disk. Without it, the PM either (a) instantiates the F3.8 template by hand and re-derives the parent-resolution, pre-fill, and lint steps each time, or (b) skips the PM Spec entirely and asks engineering to inherit a row in `child-specs.md` instead of a structured per-feature artifact — the operating-model failure mode F3.8 was designed to prevent. With `/draft-spec`, every PM Spec under every Initiative folder is instantiated identically: same frontmatter pre-fill (`id`, `slug`, `object_type: Feature`, `status: Draft`, `parent_initiative`, `created`, `last_updated`), same interactive walk through the template's nine required H2 sections plus the optional Business-rules block, same lint gate, same chaining hint. The component does not yet exist; ROADMAP P4.8 names the slug `cmd-draft-spec` and the target `.claude/commands/draft-spec.md`.

## Why now

P4.8 is one of seven Phase-4 template-fill commands in the F4 fan-out parallelized by `docs/specs/phase-4-command-convention/spec.md` (shipped 2026-05-23). The parent convention is shipped, the template (F3.8, shipped 2026-05-22) is shipped, and the prerequisite `/draft-initiative` (P4.3) is in the same fan-out batch. Authoring `/draft-spec` now closes the inner loop of the Delivery chain (`/draft-initiative` → augmenting commands → `/draft-spec` per child → `/handoff-packet`) and unblocks the only path by which a kit-adopter can author the PM-side per-feature contract before the engineering Handoff Packet is assembled. The cost is one work-loop running in parallel with six siblings; the cost of deferring is that adopters either drift on by-hand template instantiation or skip the PM Spec and re-introduce the Handover 5 → 6 gap.

## Inputs and outputs

**Inputs.**

- The positional arg — `<slug>` — the new PM Spec's slug. Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars.
- `--from <initiative-slug>` — explicit parent-Initiative selection (overrides interactive pick). Same kebab-case constraint. **Effectively required**: see §"Parent-artifact resolution" below — without it, the command must enter the interactive picker to choose an initiative because the destination path is initiative-nested.
- `--force` — permit overwriting an existing PM Spec at the destination.
- `templates/pm-spec.md` — the F3.8 single-file template this command copies from. Shipped 2026-05-22; 92 body lines; `object_type: Feature` and `status: Draft` are the only pre-filled identity values, everything else is an angle-bracket placeholder.
- Parent artifact: `delivery/initiatives/<initiative-slug>/` — must exist on disk before this command can write. Candidate list comes from `delivery/initiatives/` filtered by `status:` not in the terminal-or-killed set (`Deprecated` per the universal-schema lifecycle).
- The parent Initiative's `README.md` frontmatter — read for `parent_initiative` value (the slug itself) and to copy down any per-spec inheritable fields the human is asked to confirm during the interactive walk (e.g., `capabilities:` list — the PM Spec lists a subset).
- The parent Initiative's `child-specs.md` — read to (a) detect slug collisions with rows already present, (b) preserve the table structure when the side-effect append happens at Step 6.
- `docs/HANDOVERS.md` §"Handover 5" — quoted in the body when the command introduces the `child-specs.md` append step (so the human understands the side effect's contract).
- `tools/lint-frontmatter.py` (default mode) — the linter the command runs against the written `<spec-slug>.md` (Step 5 of the convention's body skeleton).
- The kit's current ISO-8601 date (system clock at command-start) — pre-fills `created:` and `last_updated:`.

**Outputs.**

1. `.claude/commands/draft-spec.md` — new file, ≤ ~120 body lines, copied from `.claude/commands/_meta/command-skeleton.md` and filled. Frontmatter: `description:` (one sentence, ≤ 1024 chars), `argument-hint: <slug> [--from <initiative-slug>] [--force]`. Body has the four convention-required H2 sections in order: `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`.
2. **Side effect at runtime (not at spec-ship time):** the command appends one row to `delivery/initiatives/<initiative-slug>/child-specs.md`. The row columns are `spec slug | owning context | owning team | status | link`, per Handover 5's `child-specs.md` content contract. The command pre-fills `spec slug` (the positional), `status` (`Draft`, matching the PM Spec's pre-filled status), and `link` (the relative path `specs/<spec-slug>.md`). It asks the human for `owning context` and `owning team` interactively (one question at a time). If `child-specs.md` does not exist (defensive: it should, because `/draft-initiative` creates it), the command surfaces this as a precondition failure and exits code 2 with a remediation suggestion to re-run `/draft-initiative`.
3. **Side effect at runtime:** the parent Initiative's `README.md` `last_updated:` is bumped to today's date (the initiative state changed — its manifest gained a row).

A reader of this section should be able to write the command's interface signature without reading anything else.

## Body-shape contract (the filled command file)

The filled `.claude/commands/draft-spec.md` ships with the body skeleton from `.claude/commands/_meta/command-skeleton.md`, filled per the convention. The filled body's structure is documented here verbatim so the EXECUTE pass writes from a fixed contract.

**Frontmatter.**

```yaml
---
description: Draft a PM Spec under an existing Initiative, walking templates/pm-spec.md interactively. Appends a row to the parent Initiative's child-specs.md.
argument-hint: <slug> [--from <initiative-slug>] [--force]
---
```

**H1.** `# /draft-spec`

**Intro blockquote.** One paragraph: states this is an **artifact-creating** command; names the template consumed (`templates/pm-spec.md`); names the destination (`delivery/initiatives/<initiative-slug>/specs/<slug>.md`); cites HANDOVERS §"Handover 5" as the source contract for the `child-specs.md` append side-effect.

**`## When to run`.** Three bullets:

- After a parent Initiative folder exists at `delivery/initiatives/<initiative-slug>/` with `child-specs.md` declaring at least one expected per-feature spec slug.
- When a single Feature within that Initiative is ready to gain its own per-feature PM-side contract (per-Feature granularity, not per-Capability).
- Before `/handoff-packet` runs against the Initiative — the Handoff Packet reads each PM Spec as its primary per-feature input.

**`## Inputs`.** Numbered list of four items, verbatim from the convention's body-structure rule: positional, template path, parent artifact, child-specs.md.

**`## Procedure`.** Seven numbered sub-sections, in order, per the convention's Step-N skeleton, with one P4.8-specific insertion (Step 6 — the `child-specs.md` append):

- **Step 1 — resolve parent Initiative.** If `--from <initiative-slug>` given, validate that `delivery/initiatives/<initiative-slug>/` exists; if not, exit code 2 with "run `/draft-initiative <initiative-slug>` first." If `--from` is absent, list candidates from `delivery/initiatives/` filtered by `status:` not in `{Deprecated}` (per universal lifecycle), sorted by `last_updated:` descending, capped at 10. Present as numbered list; ask the human to pick one (or to re-run with `--from` for an older candidate). Never silently pick, even with one candidate (convention §"Parent-artifact resolution"). If the candidate list is empty, exit code 2 with the remediation message "no Initiative found in `delivery/initiatives/` — run `/draft-initiative <slug>` first."
- **Step 2 — instantiate the template.** Copy `templates/pm-spec.md` to `delivery/initiatives/<initiative-slug>/specs/<slug>.md`. If the destination file exists and `--force` is not set, exit code 2 with the remediation suggestion. If the `specs/` directory does not exist, create it (mkdir -p). Pre-fill mechanical fields per §"Pre-fill rules" below.
- **Step 3 — walk placeholders one H2 section at a time.** Per §"Per-section interactive prompts" below. Never batch. Confirm each section's filled content before advancing.
- **Step 4 — surface human-owned decisions.** Read the written file's `human_owned_decisions:` list; for each entry, ask the human for explicit confirmation; record confirmations as `approvals_obtained:` inline-list entries (`"<role>: <YYYY-MM-DD>"`).
- **Step 5 — lint the written artifact.** Resolve repo root as nearest ancestor of CWD containing `tools/lint-frontmatter.py`. Run `python3 <repo-root>/tools/lint-frontmatter.py <written-path>` (default mode, NOT `--check-template`). On exit 0, proceed. On non-zero, offer to re-open the relevant sections; if human declines or re-run still fails, exit code 3 with the artifact left on disk.
- **Step 6 — append the row to `child-specs.md`.** This is the load-bearing P4.8-specific side effect. Read `delivery/initiatives/<initiative-slug>/child-specs.md`. Locate the manifest table (the first markdown table with header columns `spec slug | owning context | owning team | status | link`). Detect slug collision: if `<slug>` is already a row, do not duplicate — surface a warning and skip the append (the human already declared the row in `/draft-initiative`; this run merely instantiates the file). Otherwise, append a row `<slug> | <owning-context> | <owning-team> | Draft | specs/<slug>.md`, where `owning-context` and `owning-team` were collected during the Step-3 pre-walk (asked in the same interactive walk, surfaced explicitly to the human as the side-effect-of-this-command fields, not as PM Spec body content). Update the parent Initiative `README.md`'s `last_updated:` to today's date.
- **Step 7 — emit the next-command hint.** Last line of output, formatted exactly: `NEXT: /handoff-packet <initiative-slug>`. Append a one-line note: `(If more PM Specs remain in this Initiative's child-specs.md, run /draft-spec <next-slug> --from <initiative-slug> first.)` This honors the convention's "emit the next command in the chain" rule while surfacing the chain ambiguity (multiple PM Specs per Initiative is the common case) explicitly to the human rather than the command pretending to know which case applies.

**`## What this command will not do`.** Bulleted list:

- Not write a PM Spec when the chosen parent Initiative's `status:` is `Deprecated` (universal lifecycle terminal state).
- Not write a Requirement (REQ-NNN row) inside the Functional-requirements section without an `id:` assigned by the human during the interactive walk (the downstream Handoff Packet's `requirements.yaml` aggregates per `id:`; an un-ided requirement breaks the aggregation contract).
- Not skip the EARS-pattern fill prompt within the Functional-requirements H2 (the human is asked, per Requirement, whether the predicate matches one of the five EARS patterns — Ubiquitous, Event-driven, State-driven, Optional, Unwanted-behavior; the command does NOT lint the answer mechanically — the `ears-lint` skill is planned per ROADMAP P4.7 — but it surfaces the prompt so the eventual lint pass has well-formed input).
- Not overwrite an existing PM Spec at the destination without `--force`.
- Not skip the `human_owned_decisions:` confirmation step.
- Not fabricate evidence — if the parent Initiative lacks a referenced Capability id, ask the human, do not invent.
- Not batch placeholder questions — one at a time.
- Not silently pick a parent Initiative when multiple candidates exist (convention §"Parent-artifact resolution").
- Not assume the working directory is the repo root when invoking the linter.
- Not run `/audit-spec-linkage` automatically (Handover 5's detector); the human runs it later, against the whole Initiative, after all PM Specs have been drafted.

## Per-section interactive prompts

Verbatim phrasing per H2 of `templates/pm-spec.md` (read 2026-05-23; ten `## ` headings including the bottom `## Optional sections` block). One question per H2; H2s with implicit sub-units (e.g., per-Requirement loops) iterate the sub-prompt as documented.

**Step 3 pre-walk (side-effect fields).** Before walking the template body, ask the two `child-specs.md` row fields:

- `Which bounded context owns this spec? (See the parent Initiative's context-map.md for the candidate list.)`
- `Which team owns this spec? (Free-text; e.g., "Pricing", "Checkout", "Platform".)`

**H1 — Feature name.**

- `What is the human-readable name of this Feature? (One short phrase; will become the H1 of the PM Spec.)`

**Intro blockquote.**

- `Write one paragraph: what this Feature is, which parent Initiative it sits under, and which Capability id(s) from the parent Initiative's capabilities.md it contributes to. I'll cite HANDOVERS §"Handover 5" and §"Handover 6" automatically.`

**`## Problem this spec addresses`.**

- `What is the specific customer or business issue this Feature addresses? Keep it scoped to this Feature only — the parent Initiative already holds the broader problem statement. Cite the linked Problem id from the parent Initiative's capabilities.md.`

**`## Capabilities contributed to`.**

- `Which Capability id(s) from the parent Initiative's capabilities.md does this Feature contribute to? (Ontology direction: Capability → Feature is decomposition; one Feature can contribute to one or more Capabilities.)`

**`## User behaviour — current vs future`.**

- `Describe how the user behaves today, in one paragraph.`
- `Describe how the user will behave after this Feature ships, in one paragraph.`

**`## Functional requirements`.** Iterates per Requirement. For each Requirement the human declares:

- `What is the next Functional Requirement this Feature must support? (One predicate per Requirement. Reply "done" when no more remain.)`
- `Assign this Requirement an id (REQ-NNN). The next unused id in this Initiative is REQ-<next-int>; press Enter to accept or type a different id.`
- `Which EARS pattern does this Requirement follow — Ubiquitous, Event-driven, State-driven, Optional, or Unwanted-behavior? (For reference; not linted in this command. The /ears-lint skill is planned per ROADMAP P4.7.)`

**`## Acceptance criteria`.** Iterates per Requirement declared above.

- `For REQ-<id>, write the observable predicate that confirms the Requirement is met. Format: "REQ-NNN: <predicate>" — the downstream Handoff Packet's acceptance-criteria.md aggregates per-Requirement without re-mapping.`

**`## Non-functional requirements`.**

- `What non-functional requirements apply to this Feature? (Performance, reliability, security, accessibility, observability constraints — one per line. Reply "none" if no NFRs apply at per-Feature scope.)`

**`## Dependencies`.**

- `What upstream Features (FEAT-NNN), Capabilities (CAP-NNN), or external systems does this Feature depend on? Use typed ids so the downstream Handoff Packet's dependencies.md can cross-reference without re-triage.`

**`## Out of scope`.**

- `What does this Feature explicitly NOT do? (Surface the dog that doesn't bark — it's often more informative than the "in scope" list.)`

**`## Open questions`.**

- `What questions remain for engineering, design, legal, compliance, or human stakeholders to resolve before this Feature can ship?`

**`## Optional sections` → `### Business rules`.**

- `Are there business-logic rules beyond the Acceptance Criteria that this Feature must enforce? (Reply "skip" to remove this optional section from the written file. Otherwise: one rule per line.)`

The command emits exactly one question at a time and waits for confirmation before advancing. Confirmation is per-H2 (not per-question within a section); the human re-reads the filled section and replies `confirm` or asks to amend.

## Pre-fill rules

Mechanical fields the command fills before asking the human anything. The human is never asked to type these.

- `id: FEAT-<NNN>` — the next unused integer across `delivery/initiatives/*/specs/*.md` files whose `object_type:` is `Feature`. The command scans, finds the max existing `FEAT-N`, and assigns `N+1`. If no Feature exists yet, assigns `FEAT-001`. (Three-digit zero-pad matches the universal-schema convention used by sibling ontology types.)
- `slug: <positional-arg>` — the positional `<slug>`.
- `created: <YYYY-MM-DD>` — today, ISO-8601, resolved from system clock at command-start.
- `last_updated: <YYYY-MM-DD>` — same as `created` on first instantiation.
- `parent_initiative: <initiative-slug>` — the parent slug resolved at Step 1.
- `object_type: Feature` — already pre-filled in the template by F3.8; the command re-asserts as a defensive check (per the convention's "re-assert object_type" rule).
- `status: Draft` — already pre-filled in the template by F3.8; re-asserted.

If any mechanical field cannot be resolved (parent Initiative does not exist, `FEAT-NNN` numbering corrupt, system clock unreachable), exit code 2 with the missing pre-condition surfaced.

## Linter integration

Per the convention §"Linter integration". After Step 3 (interactive walk) completes, the command resolves repo root as the nearest ancestor of CWD containing `tools/lint-frontmatter.py`, then runs `python3 <repo-root>/tools/lint-frontmatter.py delivery/initiatives/<initiative-slug>/specs/<slug>.md` in default mode. PM Specs live under `delivery/` which is in `PHASE_DIRS` for the default-mode linter, so the file is in-scope without flag changes. On exit 0, proceed to Step 6. On non-zero, surface the linter output, offer to re-open the relevant sections; if the human accepts and re-run is clean, proceed. If the human declines or re-run still fails, exit code 3 with the artifact left on disk in a known-imperfect state.

The command does NOT run `--check-template` (the artifact is now a real product artifact, not a template).

## Exit codes

Per the convention §"Exit codes":

- `0` — PM Spec written, linter passed, `child-specs.md` row appended (or skipped because a row with the same slug already existed), parent Initiative `README.md` `last_updated:` bumped, NEXT hint emitted.
- `1` — Human aborted the interactive walk before completion. Partial PM Spec left on disk; `child-specs.md` NOT updated; `README.md` NOT bumped. Resume by re-running with the same `<slug>` and `--from <initiative-slug>` (the command detects the partial file and offers to resume vs `--force`-overwrite).
- `2` — Pre-conditions failed: parent Initiative not found; `--from <initiative-slug>` resolves to a non-existent folder; candidate list empty; destination exists without `--force`; parent Initiative `status: Deprecated`; `child-specs.md` missing from parent folder; slug malformed.
- `3` — Artifact written but post-fill linter exited non-zero, and the human declined or re-run failed. `child-specs.md` NOT appended (the spec did not pass quality bar; do not pollute the manifest). The artifact persists on disk; the human fixes manually and re-runs the lint by hand.

## Chaining hint

The command's last output lines name the next command in the Phase-4 chain. The chain ambiguity (multiple PM Specs per Initiative) is surfaced explicitly rather than mechanically resolved.

- **Primary NEXT line (always emitted):** `NEXT: /handoff-packet <handoff-packet-slug>` where `<handoff-packet-slug>` is a literal angle-bracket placeholder — the human supplies the packet slug when invoking `/handoff-packet`. (The packet's slug is the packet's own positional, NOT the parent initiative slug — the initiative slug is passed via `--from <initiative-slug>` to `/handoff-packet`. This mirrors `/draft-vision`'s `NEXT: /draft-initiative <initiative-slug>` pattern, where the next-command argument is a placeholder for a yet-to-be-named artifact, not a pass-through of the current positional.)
- **Annotation (always emitted on the next line, prose):** `(If more PM Specs remain in this Initiative's child-specs.md, run /draft-spec <next-slug> --from <initiative-slug> first. /handoff-packet should only run when every row in child-specs.md has an instantiated PM Spec file. The handoff-packet slug is typically the same as the initiative slug for clarity, but the human chooses it.)`

This honors the convention's "emit the next command in the chain" rule (single primary NEXT) while making the chain's branching point legible to the human reader. The command does NOT inspect `child-specs.md` to determine whether more PM Specs remain — that's a `/handoff-packet`-side precondition (P4.11's spec), not a per-PM-Spec concern, and inspecting it here would couple `/draft-spec` to `/handoff-packet`'s readiness contract.

If `/handoff-packet` is not yet shipped at runtime, the convention's kit-drift rule applies: append `(planned — ROADMAP P4.11)` to the NEXT line.

## Boundaries

### Always do

- Quote `docs/specs/phase-4-command-convention/spec.md` §"Convention-text contract" for the H2 structure, argv form, parent-resolution rule, pre-fill rules, exit codes, and chaining hint. This spec is a per-command instantiation of the convention; the convention is the source of truth.
- Use the F3.8 single-file destination form: `delivery/initiatives/<initiative-slug>/specs/<slug>.md`. The F3.8 spec's Open Question 2 OVERRIDES the parent template-authoring-convention's Open Question 2 folder-form resolution; this command honors the F3.8 override.
- Append exactly one row per run to `child-specs.md`. Idempotent: if the row already exists, do not duplicate; surface a warning and proceed.
- Re-assert `object_type: Feature` and `status: Draft` on the written file as a defensive check, even though `templates/pm-spec.md` ships these pre-filled.
- Surface the chain branching point (multi-spec Initiative case) to the human in the NEXT-line annotation rather than mechanically resolving it.

### Ask first

- Adding a second positional argument (e.g., `/draft-spec <slug> <initiative-slug>` instead of `/draft-spec <slug> --from <initiative-slug>`). Convention §"Argv contract" → Open Q6 resolved positional-after-slug ambiguity in favor of the flag form; this command honors that. Reversal requires amending the convention first.
- Auto-running `/audit-spec-linkage` after Step 6 (i.e., mechanically validating the Handover-5 detector against the just-written file). The convention's chain rule names `/handoff-packet` as the NEXT, not the audit; the audit runs at human discretion later. Reversing this couples per-spec write to audit cadence; surface as a follow-up convention amendment if a reviewer disagrees.
- Bumping the parent Initiative `README.md`'s `status:` (e.g., from `active` to anything else). The PM Spec's instantiation does not change the Initiative's status; only its `last_updated:` field. If a reviewer concludes status should change on first spec-instantiation, surface as a separate spec.

### Never do

- Write a PM Spec when the chosen parent Initiative's `status:` is `Deprecated`. Universal-schema terminal state; writing a child to a deprecated parent is silent ontology drift.
- Write a Functional-requirements row without an `id:` (REQ-NNN). The downstream Handoff Packet's `requirements.yaml` aggregates by `id:`; an un-ided row breaks the aggregation contract documented in Handover 6.
- Skip the EARS-pattern fill prompt within the Functional-requirements walk. The `ears-lint` skill (planned P4.7) consumes the EARS classification; even though it's not yet shipped, the field is collected so the eventual lint pass has well-formed input. The command does NOT validate the EARS answer — it surfaces the prompt only.
- Touch any field in the parent Initiative's `README.md` other than `last_updated:`. Other initiative fields are out of scope; if a write-back is needed, surface as a separate spec.
- Skip the `child-specs.md` append on a successful exit-0 run. The append is the load-bearing Handover-5 traceability link; without it, `/handoff-packet` cannot enumerate the per-feature specs.
- Pre-fill any body section (e.g., dropping example Acceptance Criteria into `## Acceptance criteria`). The template is shape-only per F3.8 §"Boundaries → Never do"; content belongs in the human's answers, not in the command's pre-fill.
- Modify `templates/pm-spec.md`. The template is frozen by F3.8 as of 2026-05-22; the command consumes it, does not change it.

## Verification mode

- **Goal-based check** for the command's existence and shape: `tools/lint-command.sh .claude/commands/draft-spec.md` exits 0; the four required H2 sections are present; `argument-hint:` matches `<slug> [--from <initiative-slug>] [--force]`.
- **Audit-driven** for kit-wide health: `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (the contract test auto-discovers `draft-spec` once shipped and asserts: lint-command passes, required H2s present, argv form matches the `POSITIONAL` map (`<slug>` per the artifact-creating sub-class), cited template path `templates/pm-spec.md` exists, cited destination directory `delivery/initiatives/` exists); `bash tools/pre-pr.sh` exits 0.
- **No manual gesture** at spec-ship time. The command's interactive behavior is exercised by a kit-user-driven slash-command invocation against a real Initiative; that's the consumer's responsibility, not this spec's verify phase. (The convention deliberately defers manual-gesture verification to each per-command consumer's first real use.)

## Contract tests

- **T1** — `test -f .claude/commands/draft-spec.md`.
- **T2** — `bash tools/lint-command.sh .claude/commands/draft-spec.md` exits 0.
- **T3** — The four required H2 sections appear in order: `awk '/^## /' .claude/commands/draft-spec.md` returns `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do` as the first four `## ` headings.
- **T4** — `argument-hint:` matches the convention's artifact-creating form: `grep -E '^argument-hint: <slug> \[--from <initiative-slug>\] \[--force\]$' .claude/commands/draft-spec.md` returns exactly 1 line.
- **T5** — `description:` is present and ≤ 1024 chars: `awk -F': ' '/^description:/{print length($2); exit}' .claude/commands/draft-spec.md` prints a number ≤ 1024.
- **T6** — Body cites the template path: `grep -c 'templates/pm-spec.md' .claude/commands/draft-spec.md` returns ≥ 1.
- **T7** — Body cites the destination family directory: `grep -c 'delivery/initiatives/' .claude/commands/draft-spec.md` returns ≥ 1.
- **T8** — Body cites the `child-specs.md` side effect explicitly (the load-bearing P4.8-specific append step): `grep -c 'child-specs.md' .claude/commands/draft-spec.md` returns ≥ 2 (one in the body intro / Inputs, one in the Step-6 procedure).
- **T9** — Body cites the F3.8 single-file destination form (not the folder form): `grep -E 'delivery/initiatives/<initiative-slug>/specs/<slug>\.md' .claude/commands/draft-spec.md | wc -l` returns ≥ 1.
- **T10** — Body emits the chain-ambiguity annotation: `grep -c 'If more PM Specs remain' .claude/commands/draft-spec.md` returns ≥ 1.
- **T11** — `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0 (auto-discovered via the convention's `INSCOPE` constant).
- **T12** — `bash tools/pre-pr.sh` exits 0.
- **T13** — ROADMAP P4.8 row is checked with `Shipped: <today>`: `grep -nE '^- \[x\] \*\*P4\.8\*\*' ROADMAP.md` returns exactly 1 line. (Asserted by the supervising orchestrator's CAPTURE pass per the brief; not gated by this spec.)

## Non-goals

- **Not** authoring `/audit-spec-linkage` (Handover 5's detector). That's a separate ROADMAP item; this command emits the precondition for that audit (PM Spec on disk with `parent_initiative:` populated), not the audit itself.
- **Not** authoring the `/handoff-packet` command (P4.11). This command emits the NEXT hint for it; `/handoff-packet` is its own per-command spec running in parallel in the F4 fan-out.
- **Not** authoring the `ears-lint` skill (P4.7). This command surfaces the EARS-pattern question for each Requirement; mechanical EARS classification is the skill's responsibility, not this command's.
- **Not** modifying `templates/pm-spec.md`. Frozen by F3.8.
- **Not** modifying `tools/lint-frontmatter.py` or `tools/lint-command.sh`. Both are frozen by their respective specs.
- **Not** introducing per-spec `owning_context:` or `owning_team:` frontmatter on the PM Spec itself. F3.8 §"Non-goals" deliberately excluded these — they live in the parent Initiative's `child-specs.md` manifest columns. This command honors that by collecting the two values during Step 3 (pre-walk) and writing them ONLY into the `child-specs.md` row, NOT into the PM Spec's frontmatter.
- **Not** authoring any of the sibling F4 commands (`/draft-vision`, `/draft-initiative`, `/context-map`, `/end-to-end-flow`, `/sequence-initiative`, `/handoff-packet`). Each runs as its own per-command spec in the F4 fan-out.
- **Not** introducing a `--dry-run` flag. Convention §"Open questions" Q1 resolved this as deferred for the whole F4 batch; this command honors that.

## Open questions

1. **`parent_initiative:` field name on the PM Spec frontmatter.** Resolved by reference: F3.8 §"Outputs" item 1 pins `parent_initiative: <initiative slug>` as the load-bearing universal-schema field. This command pre-fills it; no question to resolve here. _Cited for completeness; not actually open._

2. **OQ2 from the parent F4 convention — PM-spec destination form.** _Resolved by reference: the parent F4 convention's OQ2 cites `template-authoring-convention` OQ2 (folder form), but F3.8 §"Open Questions" Q2 OVERRIDES that resolution to single-file form via the parent's escape clause ("if the F3.8 worker disagrees, that surfaces as a finding from its own adversarial review and we reconcile then"). The F3.8 override stands; this command writes to `delivery/initiatives/<initiative-slug>/specs/<slug>.md` (single file). No new question to resolve._

3. **REQ-NNN numbering scope.** The pre-fill rule assigns `REQ-<next-int>` "across the Initiative" — i.e., the next unused REQ id within `delivery/initiatives/<initiative-slug>/specs/*.md` (per-Initiative scope), NOT kit-wide. Rationale: a REQ id is most useful to the downstream Handoff Packet aggregator (Handover 6), which aggregates per-Initiative; kit-wide numbering would force every adopter into one numeric namespace for an artifact whose aggregation boundary is the Initiative. **Settled here as per-Initiative.** If a reviewer prefers kit-wide, surface as a follow-up convention amendment.

4. **FEAT-NNN numbering scope.** Mirrors Q3 but applies to the PM Spec's `id:` field. Resolved here as **kit-wide** (single namespace across `delivery/initiatives/*/specs/*.md`). Rationale: a PM Spec is the kit's unit of per-feature traceability; the universal-schema `id:` field is a stable identifier for cross-referencing from `requirements.yaml`, `acceptance-criteria.md`, and any downstream Handoff Packet. Per-Initiative numbering would mean two Features in different Initiatives could share `FEAT-001`, which breaks the universal-schema's identifier-uniqueness invariant. Settled as kit-wide.

5. **Resume behavior on exit-1.** If a previous run exited 1 (human aborted mid-walk), how does `/draft-spec <same-slug> --from <same-initiative>` handle the partial file on disk? Resolved here as **prompt-and-merge**: detect that the file exists, detect that not all H2 sections are filled (heuristic: at least one section still contains an `<angle-bracket>` placeholder), offer the human two choices — "resume from the first unfilled section" or "discard and start over with `--force`". The resume path does NOT re-pre-fill mechanical fields (they're already set); it resumes the Step-3 interactive walk at the first unfilled H2.

6. **What if the parent Initiative's `child-specs.md` has no manifest table yet?** The defensive behavior is to exit code 2 with the remediation message "child-specs.md is empty — run `/draft-initiative <slug>` first to populate the manifest." Rationale: if the manifest is empty, the Initiative has not yet declared which Features it expects, and the PM is operating ahead of the Initiative-level decomposition. Settled here as **exit-2-and-redirect-to-/draft-initiative**. Alternative considered: silently append the row as the first manifest entry; rejected because it inverts the Handover-5 contract (the manifest is the Initiative's declaration of expected Features, populated during `/draft-initiative`, not by per-Feature drift after-the-fact).

7. **EARS classification storage.** Where does the EARS-pattern answer per Requirement live, given the PM Spec template has no dedicated EARS field? Resolved here as **inline comment within the Functional-requirements section body**, format: `REQ-NNN: <predicate> <!-- EARS: <pattern> -->`. The HTML comment is lint-invisible (the kit's default-mode linter walks frontmatter, not body), and the `ears-lint` skill (planned P4.7) parses the comment when it's authored. If P4.7 decides to use a different storage form, the EARS-lint skill's spec amends `/draft-spec`'s prompt; until then, the inline-comment form is the bridge.

## Acceptance criteria

- [ ] `.claude/commands/draft-spec.md` exists, ≤ ~120 body lines, copied from `.claude/commands/_meta/command-skeleton.md` and filled per §"Body-shape contract".
- [ ] Frontmatter: `description:` (one sentence, ≤ 1024 chars) and `argument-hint: <slug> [--from <initiative-slug>] [--force]`.
- [ ] H1 is `# /draft-spec`. Intro blockquote states this is an artifact-creating command, names `templates/pm-spec.md` as the template consumed, names `delivery/initiatives/<initiative-slug>/specs/<slug>.md` as the destination, cites HANDOVERS §"Handover 5" for the `child-specs.md` append.
- [ ] Four required H2 sections present in order: `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`.
- [ ] `## Procedure` declares seven steps (1, 2, 3, 4, 5, 6, 7) per §"Body-shape contract".
- [ ] All per-section interactive prompts from §"Per-section interactive prompts" appear verbatim in the body's Step-3 walk.
- [ ] Pre-fill rules per §"Pre-fill rules" documented in the body's Step-2 instantiation.
- [ ] Linter integration per §"Linter integration" documented in Step 5.
- [ ] All four exit codes documented per §"Exit codes".
- [ ] Chaining hint per §"Chaining hint" emitted as the last two output lines.
- [ ] T1–T12 from §"Contract tests" all pass after EXECUTE.
- [ ] T13 (ROADMAP row checked) handled in the CAPTURE phase per the supervisor's brief; not gated by this spec.
- [ ] No new ontology type added; no F3.x template modified; no existing slash command modified; no `tools/` script modified; no edit to `docs/HANDOVERS.md` or `docs/CONVENTIONS.md`.

## Cross-references

- **Consumed by:** kit users authoring a PM Spec under an Initiative; the F4 chain's `/handoff-packet` command (P4.11) reads each PM Spec the command writes as its primary per-feature input.
- **Consumes:** `templates/pm-spec.md` (F3.8); `docs/specs/phase-4-command-convention/spec.md` (parent convention); `docs/HANDOVERS.md` §"Handover 5" + §"Handover 6"; `tools/lint-frontmatter.py` (default mode); `tools/lint-command.sh` (shape linter); `.claude/commands/_meta/command-skeleton.md` (copied to create the command file); the parent Initiative folder's `README.md` and `child-specs.md`.
- **Frontmatter fields owned:** pre-fills `id`, `slug`, `object_type`, `status`, `created`, `last_updated`, `parent_initiative` on the written PM Spec. Bumps `last_updated:` on the parent Initiative's `README.md`. Appends one row (slug, owning-context, owning-team, status, link) to `child-specs.md`.
- **Ontology object types touched:** `Feature` (Domain E — `object_type:` of the written artifact). The command references but does not classify: `Initiative` (Domain D — parent, named via `--from`), `Capability` (Domain E — listed in `capabilities:`), `Requirement` (Domain E — collected per REQ-NNN row in the Functional-requirements walk), `Acceptance Criteria` (Domain E — per-Requirement), `Non-Functional Requirement` (Domain E), `Dependency` (Domain E), `Open Question` (Domain E).
