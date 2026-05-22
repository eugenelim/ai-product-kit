# Plan: hook-check-handover-link

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Drafting
- **Plan review:** pending

## Approach

The script is a single-file Python entry point (`scripts/check-handover-link.py`) that reads PreToolUse JSON from stdin, decides whether the write is in-scope per the path globs table, parses the new-content frontmatter, and emits either exit 0 (allow) or exit 2 + JSON block on stdout (block) per the Claude Code hook protocol.

The seven path globs are compiled once at module load into a list of `(regex, required_fields, handover_number, parent_target_resolver)` tuples — single source of truth, easy to amend by RFC. The override fields (all four) are checked before any block decision.

Edit/MultiEdit semantics live in one place: classify each edit as "frontmatter-touching" (`---` in `old_string`) or "body-only." For body-only edits, the on-disk frontmatter is authoritative — it isn't being changed. For frontmatter-touching edits, apply the `(old, new)` substitutions to the on-disk file in-memory and parse the result. MultiEdit is a sequence — apply edits in order and parse the final result.

Tests come first, against fixtures composed in-memory (no temp files needed for the parse path; small tmpdir fixtures for the disk-fallback path).

## Constraints

- Python stdlib + `scripts.lib.frontmatter` only.
- ≤ 300 LOC. Verified by `wc -l scripts/check-handover-link.py` in Task 7.
- All exits ≤ 50ms — this is on the write path.
- Never crash: any uncaught exception caught at the top level → exit 0 with a stderr trace summary (degrade safely).
- Hook doc shape per F0.10 contract (H1 ending " hook", What/Why/Configuration sections).
- **Depends on:** F0.10 must ship before VERIFY runs.

## Tasks

### Task 1: Path-glob table and matcher (TDD red)

- **Depends on:** none.
- **Tests:**
  - `test_strategy_intent_matches`
  - `test_discovery_tree_matches`
  - `test_initiative_readme_path_pattern` (only `<slug>/README.md`, not nested specs)
  - `test_path_outside_handover_globs_passes_silently`
- **Approach:**
  - In `scripts/check-handover-link.py`: a module-level `HANDOVER_RULES` list of 7 entries, each `{"glob": re.compile(...), "required": ["parent_intent"], "handover": 2, "label": "OST"}`.
  - A `match_rule(path: str) -> Rule | None` function.
- **Done when:** the 4 tests pass.

### Task 2: Frontmatter check + block/allow decision (red → green)

- **Depends on:** Task 1.
- **Tests:**
  - `test_allows_write_with_required_parent_field`
  - `test_blocks_write_when_parent_field_missing`
  - `test_landing_requires_both_parent_fields`
  - `test_vision_requires_both_parent_fields`
  - `test_strategy_intent_passes_without_parent_diagnosis`
  - `test_override_with_all_fields_unblocks_and_logs`
  - `test_override_without_reason_blocks`
  - `test_override_without_authorizer_blocks`
  - `test_override_false_does_not_unblock`
- **Approach:**
  - `check(payload: dict) -> tuple[int, str | None, str | None]` returning `(exit_code, stdout_json, stderr_msg)`.
  - Parse new-content frontmatter via `scripts.lib.frontmatter.parse`.
  - Override check first: require `override_handover_link == True` (strict comparison, not truthy) AND all of `override_reason` / `override_authorized_by` / `override_authorized_at` non-empty; on pass, append to `delivery/HANDOVER-OVERRIDE-LOG.md` and exit 0; on any missing/empty, block with reason.
  - Required-fields loop; missing → block JSON.
- **Done when:** the 9 tests pass.

### Task 3: Edit / MultiEdit semantics

- **Depends on:** Task 2.
- **Tests:**
  - `test_edit_with_frontmatter_touching_old_string_reconstructs_proposed_state`
  - `test_edit_body_only_uses_on_disk_frontmatter`
  - `test_multiedit_treated_as_sequence_of_edits`
- **Approach:**
  - Classify each `(old_string, new_string)` pair: frontmatter-touching if `---` appears in `old_string`.
  - Body-only edits: parse and use the on-disk file's frontmatter (it's not being changed by this edit).
  - Frontmatter-touching edits: apply `(old → new)` substitutions to the on-disk file in-memory (string `.replace(old, new, 1)` — first occurrence, same as Claude Code's Edit semantics), then parse the result.
  - MultiEdit: apply edits in array order, then parse the final reconstructed string.
- **Done when:** the 3 tests pass.

### Task 4: Dangling-link warning + degraded paths

- **Depends on:** Task 3.
- **Tests:**
  - `test_warns_when_parent_target_file_missing`
  - `test_dangling_parent_initiative_resolves_to_readme_not_flat_md`
  - `test_dangling_parent_vision_resolves_to_flat_md_not_readme`
  - `test_malformed_frontmatter_degrades_to_warning_not_crash`
  - `test_uppercase_path_warns_but_does_not_block`
- **Approach:**
  - Parent target resolution is **per-field** (driven by the fourth column of the spec's path table):
    - `parent_intent` → `strategy/intents/<slug>.md`
    - `parent_opportunity` → `discovery/opportunities/<slug>.md`
    - `parent_learning` → `validation/learnings/<slug>.md`
    - `parent_vision` → `delivery/visions/<slug>.md`
    - `parent_initiative` → `delivery/initiatives/<slug>/README.md`
    - `parent_handoff_packet` → `delivery/handoff-packets/<slug>/README.md`
  - Each `parent_*` field has exactly one resolver; no fallback between flat-file and README forms.
  - Uppercase-under-phase-root warning: if the path matches `(?i)^(strategy|discovery|validation|delivery)/` but doesn't match any glob exactly (case-sensitive), emit a one-line stderr nudge about the kebab-case convention.
  - Top-level try/except wraps the whole `main()` — catch-all degrades to exit 0 + stderr.
- **Done when:** the 5 tests pass.

### Task 5: Entry point + JSON protocol

- **Depends on:** Tasks 2–4.
- **Tests:**
  - End-to-end: run `scripts/check-handover-link.py` as a subprocess with a constructed stdin JSON; assert exit code and stdout JSON shape.
- **Approach:**
  - `if __name__ == "__main__":` block reads `sys.stdin`, calls `check(payload)`, writes `stdout_json` to stdout if present, `stderr_msg` to stderr, exits with the returned code.
- **Done when:** the subprocess test passes.

### Task 6: Author `.claude/hooks/check-handover-link.md`

- **Depends on:** Tasks 1–5 (so the doc accurately describes what the script does).
- **Tests:** `bash tools/lint-hook.sh .claude/hooks/check-handover-link.md` exits 0.
- **Approach:** modelled on `assumption-threshold-lock.md`. Sections: What it does, Why this matters, How to write a parent-linked artifact (with examples), Override, Configuration (settings.json fragment), Related.
- **Done when:** lint-hook passes; the doc explains the seven-path table verbatim.

### Task 7: Update reference docs (CAPTURE)

- **Depends on:** Tasks 1–6.
- **Tests:** none.
- **Approach:**
  - `docs/INVENTORY.md` — add row for the hook under the hooks section.
  - `AGENTS.md` — update the "Don't skip a phase silently" line to name this hook as the write-time enforcement.
  - `ROADMAP.md` — check off F2.1, append `**Shipped:** <date>`.
- **Done when:** all three edits land.

## Rollout

- F2.6 (`claude-settings-hooks-wiring`) is the consumer that activates this hook. Until F2.6 ships, this hook is shippable but inert.
- No other component depends on this hook's interface; the doc is the contract for adopters.

## Risks

- **Edit-without-frontmatter disk-fallback** can read a stale on-disk file mid-edit on slow filesystems. Mitigation: if disk read fails or returns no frontmatter, degrade to a warning (not a block) — the audit catches the lasting state later. Documented as Open Question 1.
- **Path globs drift from HANDOVERS.md.** If HANDOVERS.md is amended (e.g., D7 adds Handover 2.5), this hook misses it silently. Mitigation: cross-reference in the hook doc says "edit the HANDOVER_RULES table when amending HANDOVERS.md."

## Changelog

- 2026-05-21: Initial plan.
- 2026-05-21: Addressed adversarial review (10 findings). Replaced fictional `parse_text` with `parse` (real F1.2 API). Added MultiEdit to matchers. Rewrote Edit semantics: frontmatter-touching (old_string contains `---`) vs body-only — body-only uses on-disk frontmatter directly. Added per-field parent-target resolver column to the path table (initiative/handoff-packet → README.md only; flat-file types → `.md`). Switched override convention to mirror `assumption-threshold-lock.md` (`override_handover_link:` + reason + authorizer + log). Added Vision dual-parent requirement (`parent_learning` AND `parent_intent` per HANDOVERS.md). Added child-spec non-goal. Closed open questions. Bumped LOC ceiling to 300 and added explicit verify gate. Added F0.10 dependency to acceptance criteria.
