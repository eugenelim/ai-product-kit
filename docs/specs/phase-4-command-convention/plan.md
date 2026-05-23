# Plan: phase-4-command-convention

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for `phase-4-command-convention`. Mirrors the F3 `template-authoring-convention` plan in shape because the work is structurally analogous: lock a shared shape, ship a literal copyable skeleton, ship a contract test, update reference docs, prepend a one-line cross-reference into ROADMAP. The whole plan is sized to one short work-loop because the cost of the spec stands or falls on whether seven F4 fan-out specs can land in parallel afterward.

## Approach

Three-stage build, each stage a single coherent commit. The stages are ordered so the contract test (Task 2) lands before the convention text (Task 3) — TDD discipline applied to documentation: the test is what enforces the convention; writing it first forces concrete decisions about the convention's machine-checkable surface (which keys, which paths, which sections). Task 1 ships the copyable skeleton because the skeleton's exact lines are the most-quoted artifact downstream; locking it before either the test or the convention text means the test and the convention text reference a real on-disk path, not a forward reference.

The convention is doc + test + skeleton. There is no Python source code beyond the pytest module, no script, no skill body. Verification is goal-based (greps + lint exit codes) plus the new pytest module. No dependency on the seven F4 in-scope commands existing — the contract test auto-skips not-yet-shipped commands per the spec's design.

CAPTURE (Task 5) folds INVENTORY, ROADMAP cross-reference, and status freezes into one commit at the very end, after adversarial review passes.

## Constraints

- Must not introduce any new top-level dependencies. Stdlib + pytest (already used by `scripts/tests/test_lint_frontmatter.py`).
- Must not exceed 120 body lines in `.claude/commands/_meta/command-skeleton.md` (per spec acceptance criterion). The skeleton grew during pre-EXECUTE review because the creating-vs-augmenting command split became load-bearing; 120 (not 100) is the operative ceiling.
- Must not modify any existing `.claude/commands/*.md` file. The five shipped commands remain untouched — the convention is forward-looking for the seven in-scope P4.x commands, not retroactive.
- Must not modify `tools/lint-command.sh` or `tools/lint-frontmatter.py`. Convention enforcement lives in `scripts/tests/test_phase4_command_shape.py`, not in the generic linters.
- Must not modify any of the seven F3.x templates (`templates/vision.md`, `templates/initiative/*`, `templates/pm-spec.md`, `templates/handoff-packet/*`). They are frozen as of 2026-05-22.
- Must not touch any `delivery/` artifacts (this spec adds no product artifacts).
- All file writes use UTF-8; line endings LF; trailing newline present per kit convention.

## Construction tests

Cross-cutting tests that span tasks (per-task tests live under each task below):

- `bash tools/pre-pr.sh` exits 0 at the end of Task 5 (regression sentinel — confirms no kit-wide breakage).
- `python3 tools/lint-frontmatter.py --all` exits 0 at the end of Task 5 (no `delivery/` regression).

## Tasks

### Task 1: Ship the copyable command skeleton

- **Depends on:** none
- **Tests:**
  - `T2` — `test -f .claude/commands/_meta/command-skeleton.md && [[ $(wc -l < .claude/commands/_meta/command-skeleton.md) -le 120 ]]`
  - `T3` — `test -f .claude/commands/_meta/README.md`
  - `T4` — `bash tools/lint-command.sh .claude/commands/_meta/command-skeleton.md` exits 0
  - `T6` — `grep -c "<command-name>" .claude/commands/_meta/command-skeleton.md` returns ≥ 1
  - `T11` — `grep -nE "^# /<command-name>" .claude/commands/_meta/command-skeleton.md` returns exactly 1
- **Approach:**
  - `mkdir -p .claude/commands/_meta`
  - Write `.claude/commands/_meta/command-skeleton.md` matching the spec's §"Skeleton-text contract" exact body, byte-for-byte. Verify line count ≤ 120 with `wc -l`.
  - Write `.claude/commands/_meta/README.md` — prose-only, no YAML frontmatter. One paragraph naming what `_meta/` is for, naming the skeleton, pointing to `docs/CONVENTIONS.md §"Phase-4 Template-Fill Commands"` (the convention's home, which lands in Task 3 — at the time Task 1 commits, this is a forward reference; resolved when Task 3 ships in the same PR).
  - Run `tools/lint-command.sh` against the skeleton to confirm it passes.
- **Done when:** All five tests (T2, T3, T4, T6, T11) pass. The skeleton is a real on-disk file Task 2 and Task 3 can reference.

### Task 2: Ship the contract test

- **Depends on:** Task 1
- **Tests:**
  - `T5` — `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0
  - Per spec §"Outputs" item 4, the test module implements eight test cases:
    1. `test_skeleton_passes_lint_command`
    2. `test_skeleton_uses_placeholder_h1`
    3. `test_inscope_commands_pass_lint` (auto-skip per name)
    4. `test_inscope_commands_have_required_h2s` (auto-skip per name)
    5. `test_inscope_commands_declare_argv` (auto-skip per name)
    6. `test_inscope_commands_cite_template_path` (auto-skip per name)
    7. `test_inscope_commands_cite_destination_path` (auto-skip per name)
    8. `test_inscope_count_is_seven`
- **Approach:**
  - Write `scripts/tests/test_phase4_command_shape.py` with TWO module-level constants: `INSCOPE = ["draft-vision", "draft-initiative", "context-map", "end-to-end-flow", "sequence-initiative", "draft-spec", "handoff-packet"]` AND `POSITIONAL = {"draft-vision": "<slug>", "draft-initiative": "<slug>", "context-map": "<initiative-slug>", "end-to-end-flow": "<initiative-slug>", "sequence-initiative": "<initiative-slug>", "draft-spec": "<slug>", "handoff-packet": "<slug>"}`. `test_inscope_commands_declare_argv` reads the expected positional from `POSITIONAL[name]`.
  - Implement the eight test cases. The five "inscope" tests use `pytest.skip(f"{name}: not yet shipped at .claude/commands/{name}.md")` when the file doesn't exist; assert when it does. The two skeleton tests run unconditionally; `test_inscope_count_is_seven` runs unconditionally and asserts both `len(INSCOPE) == 7` AND `len(POSITIONAL) == 7`.
  - The skeleton tests shell out to `tools/lint-command.sh` via `subprocess.run`. Resolve the repo root via `Path(__file__).resolve().parents[2]` so the test is runnable from any working directory.
  - The `test_inscope_commands_cite_template_path` test scans the body with a regex matching `templates/[a-z0-9-]+(?:\.md|/)` and asserts at least one match exists on disk. If none match, the test fails with a message naming the command and its body's lack of a template path.
  - The `test_inscope_commands_cite_destination_path` test scans the body for `delivery/[a-z0-9-]+/` patterns (the family directory, NOT a per-slug subpath) and asserts at least one parent dir exists on disk.
  - The `test_inscope_count_is_seven` test asserts `len(INSCOPE) == 7` — guards against silent in-scope-list growth or shrinkage.
  - Use `@pytest.mark.parametrize("name", INSCOPE)` on each of the five inscope-loop tests so each `(test, command)` pair shows as a discrete pytest node. This makes the auto-tightening visible: as P4.x workers ship a command, the corresponding skip flips to pass without any change to the test file.
  - Run `python3 -m pytest scripts/tests/test_phase4_command_shape.py -v` and confirm exit 0. Expect 3 unconditional passes (`test_skeleton_passes_lint_command` + `test_skeleton_uses_placeholder_h1` + `test_inscope_count_is_seven`) plus 35 parametrized skips (5 inscope tests × 7 commands). Skips do not fail pytest's exit code.
- **Done when:** `python3 -m pytest scripts/tests/test_phase4_command_shape.py` exits 0. The auto-skip behavior is visible in `-v` output. No in-scope command exists yet, so all parametrized inscope tests skip; the unconditional skeleton tests and the count test pass.

### Task 3: Ship the convention text

- **Depends on:** Task 1, Task 2
- **Tests:**
  - `T1` — `grep -c "### Phase-4 Template-Fill Commands" docs/CONVENTIONS.md` returns exactly 1
  - `T10` — `grep -c "phase-4-command-convention" docs/CONVENTIONS.md` returns 0 (convention text does not self-reference the spec slug)
  - `T14` — `awk '/^### Templates — \`templates\/<slug>\.md\`/{seen=1} /^### Phase-4 Template-Fill Commands/{if(seen) exit 0; else exit 1} END{if(NR>0) exit 1}' docs/CONVENTIONS.md` exits 0 (sub-section appears after the F3 Templates sub-section)
  - `T15` — `grep -c "^> - \`3\` — artifact was written but the post-fill linter exited non-zero" docs/CONVENTIONS.md` returns exactly 1 (exit code 3 is documented under the quoted "Exit codes" block)
- **Approach:**
  - Locate the §"Templates — `templates/<slug>.md`" sub-section in `docs/CONVENTIONS.md`.
  - Append the new §"Phase-4 Template-Fill Commands — `.claude/commands/draft-*.md` and siblings" sub-section immediately after it, matching the spec's §"Convention-text contract" exact body. The new sub-section sits adjacent to the F3 Templates sub-section because the two are paired: templates declare the artifact shape, commands declare the artifact-instantiation behavior.
  - Confirm the doc still parses as valid Markdown (verify H3 nests correctly under the parent H2).
  - Confirm no `phase-4-command-convention` substring leaked into the convention body. The convention's closing paragraph names `docs/specs/cmd-<verb>/` as the per-command-spec home and references `this convention's notes/` for the checklist — neither names the parent spec's slug, so T10 passes.
  - Confirm the §"Exit codes" block in the convention text lists all four codes (0, 1, 2, 3) verbatim per the spec §"Convention-text contract"; T15 specifically protects against accidentally omitting exit code 3 during the copy.
- **Done when:** T1, T10, T14, and T15 pass. The convention is on-disk where future authors look for it, in the correct position, with the four-code exit schema intact.

### Task 4: Ship the per-command spec checklist

- **Depends on:** none for file creation; logically depends on Task 3 (the checklist restates the convention text — order Task 4 after Task 3 within the same PR even though file-level independence is preserved).
- **Tests:**
  - `T12` — `test -f docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md`
  - `T12b` — `grep -cE "^- \[ \] " docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md` returns at least 5 (the five enumerated rows from the spec are present as checklist items).
- **Approach:**
  - `mkdir -p docs/specs/phase-4-command-convention/notes`
  - Write `notes/per-command-spec-checklist.md` with the five-row checklist from the spec's §"Outputs" item 5: (a) cites this convention as `Constrained by:` in the spec header, (b) names the template path consumed (creating commands) OR names the augmented child file path (augmenting commands), (c) names the destination write path (creating) OR confirms the parent-initiative folder pre-exists (augmenting), (d) declares the parent-artifact-resolution rule (auto-detect-with-confirm vs explicit `--from`; skipped for augmenting commands), (e) enumerates the per-section interactive prompts with the human-facing copy. Each as a `- [ ] ` markdown checklist item.
  - The checklist is editorial guidance, not machine-checkable beyond T12b's count; the file is brief (≤ 50 lines). It serves as the page each F4 worker reads while writing their per-command spec, alongside the convention text.
- **Done when:** T12 and T12b pass. The checklist is on-disk where F4 workers will look for it, with the five rows actually present.

### Task 5: CAPTURE — update reference docs and ROADMAP

- **Depends on:** Task 1, Task 2, Task 3, Task 4
- **Tests:**
  - `T7` — `bash tools/pre-pr.sh` exits 0
  - `T8` — `grep -E "^- \[ \] \*\*P4\.(1|3|4|5|6|8|11)\*\*" ROADMAP.md | wc -l` returns 7
  - `T9` — `grep -c "phase-4-command-convention" ROADMAP.md` returns ≥ 1
  - `T13` — `python3 tools/lint-frontmatter.py --all` exits 0
- **Approach:**
  - Edit `ROADMAP.md`: prepend a one-line cross-reference under the `## Phase 4 — Delivery and Engineering Handoff` heading. The cross-reference reads: "P4.1, P4.3, P4.4, P4.5, P4.6, P4.8, P4.11 items consume the command convention from `docs/specs/phase-4-command-convention/`. Read that spec first; copy `.claude/commands/_meta/command-skeleton.md` to start each command." Place it as the first line under the heading (mirrors the F3 placement from `template-authoring-convention`).
  - Do NOT flip any P4.x checkboxes — those flip when each P4.x ships.
  - Add a row in `docs/INVENTORY.md` under whichever section currently houses `template-authoring-convention` (locate during execution). Row format matches the F3 row's shape.
  - Update `.claude/skills/work-loop/SKILL.md`? **No** — the SKILL.md doesn't enumerate phase-specific conventions; it points to `docs/CONVENTIONS.md` as the contract home. CONVENTIONS.md is where the new sub-section lands; no SKILL.md edit needed.
  - Update `AGENTS.md`? **No** — AGENTS.md names CONVENTIONS.md as the source of truth for "Required metadata for any artifact"; the new sub-section is reached transitively. No AGENTS edit needed.
  - Update `README.md`? **No** — kit's top-level README doesn't enumerate Phase-4 conventions.
  - Run `bash tools/pre-pr.sh` and confirm exit 0.
  - Run `python3 tools/lint-frontmatter.py --all` and confirm exit 0.
  - Freeze the spec: set `Status: Shipped (<today>)` in spec.md; set `Status: Done (<today>)` in plan.md. **CAPTURE-phase only** — these edits land in the same commit as the INVENTORY and ROADMAP updates.
- **Done when:** T7, T8, T9, T13 pass. The spec is `Shipped`; the plan is `Done`; INVENTORY has a row; ROADMAP has the cross-reference; no checkboxes flipped on P4.x rows.

## Rollout

- **Consumed by F4 fan-out:** seven per-command specs (`cmd-draft-vision`, `cmd-draft-initiative`, `cmd-context-map`, `cmd-end-to-end-flow`, `cmd-sequence-initiative`, `cmd-draft-spec`, `cmd-handoff-packet`). Each worker copies `.claude/commands/_meta/command-skeleton.md` and reads `docs/specs/phase-4-command-convention/notes/per-command-spec-checklist.md` while writing their per-command spec. The seven workers may run in parallel after this spec ships.
- **Existing slash commands are untouched.** The five shipped commands (`phase-guide`, `audit-traceability`, `audit-completeness`, `audit-portfolio-coherence`, `competitive-research`) are not in the in-scope list (none are template-fill commands) and remain on their own per-command shape.
- **Future Phase-4 commands beyond the seven** (e.g., a future `/release-notes` rewrite that turns out to fit the template-fill shape) can opt into the convention by citing it in their per-command spec; they don't need a separate convention spec.
- **No INVENTORY edits required** beyond a single row addition (above).
- **No agent or skill updates required** — the work-loop skill applies as-is to every per-command spec; no Phase-4-specific work-loop variant is needed.

## Risks

- **Contract test brittleness on path-format edge cases.** The two "cite path" tests (`test_inscope_commands_cite_template_path`, `test_inscope_commands_cite_destination_path`) use regexes against the command body's prose. A per-command spec author who names the path inside a code block, a link, or a sentence works fine; an author who names the path inside an HTML comment stripped at render time may evade the regex. Mitigation: the test is intentionally lenient (any `templates/...` or `delivery/.../` substring in the body counts); aggressive evasion would have to be willful, not accidental. If a real F4 worker hits a false-positive failure, surface as a per-command spec finding, not as a convention-spec amendment.
- **In-scope-list drift.** If a future contributor adds an eighth command to the in-scope list without thinking, `test_inscope_count_is_seven` catches it immediately. The reverse risk (a contributor silently removes one) is also caught by the count test. Test exists explicitly to make in-scope-list edits a conscious choice.
- **`docs/CONVENTIONS.md` becoming the kit's single longest file.** This spec adds another sub-section to an already-long document. Mitigation: keep the convention text terse — the spec's §"Convention-text contract" is the upper bound. If the file grows past readability, future RFC.
- **Skeleton drift from per-command reality.** As the seven F4 workers run, they may discover the skeleton is missing a section the convention should have included. The work-loop's "drift is a bug" rule applies: the discovering worker amends this convention spec in the same loop, re-runs the adversarial review, and updates the skeleton. The convention is allowed to evolve during F4 fan-out; quiet per-command deviations are not.
- **Chain-hint correctness.** Open Question 4 resolves the chain ordering (`/draft-initiative` → `/context-map` → `/end-to-end-flow` → `/sequence-initiative` → `/draft-spec` → `/handoff-packet`); per-command specs encode it. If a future worker challenges the ordering during their adversarial review, the convention is amended once and the other six commands re-emit their NEXT lines. This is cheap because the NEXT line is one line.
- **F3.x template stability assumption.** This spec assumes `templates/vision.md`, `templates/initiative/*`, `templates/pm-spec.md`, `templates/handoff-packet/*` are frozen as of 2026-05-22. Each F3.x spec has its own open questions; if one resolves in a way that materially changes the template body before all seven Phase-4 fan-out specs ship, the skeleton's Step-3 placeholder-walk wording and the checklist's per-section-prompt row (e) may need a minor update. Mitigation: per-command specs cite the exact template path; if the path or its contents change, the per-command spec's adversarial review catches the drift before the command ships.
- **Convention amendment during fan-out.** No locking or coordination mechanism is specified for the case where two of the seven parallel fan-out workers simultaneously discover conflicting amendments to this convention. The plan assumes single-threaded fan-out in practice (a human orchestrator runs the seven specs in a deterministic order, even if their work-loops are conceptually parallel). If the kit moves to true concurrent multi-worker authoring later, this assumption needs revisiting — likely via a lightweight RFC.

## Changelog

- 2026-05-23: Initial draft. PLAN phase.
- 2026-05-23: Adversarial-review iter-1 fixes applied (still PLAN phase): split convention into artifact-creating (4) vs artifact-augmenting (3) sub-classes; added exit code 3 for "linter non-zero after write"; named the terminal-or-killed parent-status set inline; replaced "heading granularity" with explicit H2/H3 rule; added candidate-list 10-row cap and empty-list exit-2 path; required repo-root resolution before invoking the linter; added the capabilities.md REVIEW interstitial after `/sequence-initiative`; tightened argv test to use a `POSITIONAL` map; added T14 (placement after F3 Templates), T15 (exit code 3 documented), T12b (checklist row count); justified the no-`lint-command.sh` mode asymmetry vs F3; added the lint-command.sh-H1-regex-hardening rule under §"Boundaries → Never do"; added F3.x-template-stability and convention-amendment-during-fan-out risks; bumped skeleton ceiling to 120 lines.
- 2026-05-23: Adversarial-review iter-2 fix applied: bumped plan's Task 1 T2 ceiling and approach prose from `≤ 100` to `≤ 120` to match spec acceptance criterion. Iter-2 NF2 (REVIEW-vs-NEXT ordering wording in convention text) deferred per reviewer's recommendation (skeleton is unambiguous; convention text is acceptably compatible).
