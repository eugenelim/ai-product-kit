# Spec: hook-check-handover-link

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** hook (PreToolUse — Write, Edit, MultiEdit)
- **Serves kit phase:** Cross-cutting (enforces phase handover rules from `docs/HANDOVERS.md`)
- **Constrained by:** `docs/HANDOVERS.md` (the seven handover frontmatter contracts); `docs/CONVENTIONS.md` (universal-metadata schema + `parent_*` fields); F1.2 (`scripts/lib/frontmatter`); F0.10 (`tools/lint-hook.sh` — verify gate for the doc); `.claude/skills/work-loop/SKILL.md`

> **Spec contract.** Defines `scripts/check-handover-link.py` and `.claude/hooks/check-handover-link.md`. Refuses any Write/Edit to a kit artifact under one of the seven handover paths unless its frontmatter declares the required `parent_*` link for that path.

## Objective

Build a PreToolUse hook on `Write|Edit` that runs `scripts/check-handover-link.py`. The script reads the proposed tool input (path + new-content frontmatter), determines from the path which Handover the artifact belongs to (per `docs/HANDOVERS.md`), and verifies the artifact's frontmatter declares the required `parent_*` field. If absent, the hook blocks the write (exit 2 with reason). If present but the parent target file does not exist, the hook warns (exit 0 with stderr note) — broken-link detection is the auditor's job, not the gate's.

This converts the prose discipline in HANDOVERS.md into a write-time guard.

## Why now

Phase-skipping is named in `AGENTS.md` as the kit's #1 silent failure mode. The mechanical version of "did the prior handover artifact exist?" is "does the new artifact's frontmatter point at one?" Without this hook, an author can silently produce a Vision with no `parent_learning`, an Initiative with no `parent_vision`, a Handoff Packet with no `parent_initiative` — and only a manual `/audit-traceability` run will catch it after the fact.

F1.2 (frontmatter parser) and F1.1 (graph walker) shipped on 2026-05-21 — the dependency is satisfied. F0.10 ships in the same batch as a prerequisite to lint the hook doc.

## Inputs and outputs

**Inputs.**
- Hook stdin: the standard PreToolUse JSON payload — `{ "tool_name": "Write" | "Edit" | "MultiEdit", "tool_input": { "file_path": <abs>, "content": <new content> | "new_string": ... | "edits": [{old_string,new_string},...], ... } }`.
- Reads `tool_input.file_path` and the new content's frontmatter (parsed via `scripts.lib.frontmatter.parse`).
- **Edit / MultiEdit semantics:** A "frontmatter-touching" edit is one whose `old_string` contains a `---` delimiter (i.e., the edit's source region overlaps the frontmatter block). For frontmatter-touching edits, the proposed final frontmatter is reconstructed by applying each `(old_string, new_string)` to the current on-disk file and parsing the result. For body-only edits (no `---` in `old_string`), the on-disk frontmatter is authoritative — the edit doesn't change `parent_*` fields. MultiEdit is treated as a sequence of Edits.

**Outputs.**
- Exit 0: write allowed. No stdout/stderr.
- Exit 2: write blocked. Stdout = a JSON object with `decision: "block"` and `reason: "<one-line explanation>"` per Claude Code hook protocol.
- Exit 0 with stderr: warning (parent declared but target file missing). Write proceeds; audit catches the dangling link later.

The path→handover map (the **load-bearing table**):

| Path glob | Handover | Required `parent_*` field(s) | Parent target resolves to |
|---|---|---|---|
| `strategy/intents/*.md` | 1 | (none — `parent_diagnosis` is optional) | n/a |
| `discovery/trees/*.md` | 2 | `parent_intent` | `strategy/intents/<slug>.md` |
| `validation/learnings/*.md` | 3 | `parent_opportunity` | `discovery/opportunities/<slug>.md` |
| `delivery/visions/*.md` | 4 | `parent_learning` AND `parent_intent` | learning → `validation/learnings/<slug>.md`; intent → `strategy/intents/<slug>.md` |
| `delivery/initiatives/<slug>/README.md` | 5 | `parent_vision` | `delivery/visions/<slug>.md` |
| `delivery/handoff-packets/<slug>/README.md` | 6 | `parent_initiative` | `delivery/initiatives/<slug>/README.md` |
| `delivery/landings/*.md` | 7 | `parent_vision` AND `parent_handoff_packet` | vision → `delivery/visions/<slug>.md`; handoff packet → `delivery/handoff-packets/<slug>/README.md` |

Each row's source is the corresponding Handover block in `docs/HANDOVERS.md` — the parent-field strings are taken verbatim from the frontmatter examples there. The fourth column is the dangling-link resolver: the hook tries the listed path; if the file doesn't exist, the link is dangling.

**Child specs under initiative directories** (`delivery/initiatives/<slug>/specs/*.md`) are deliberately **out of scope** for this hook. They have their own `parent_initiative:` requirement per HANDOVERS.md's `/audit-spec-linkage` detector (P4.10 — unbuilt), but the seven canonical Handover contracts cover only `README.md` for folder artifacts. A separate write-time guard for child specs is a future spec; see Non-goals.

## Boundaries

### Always do
- Operate as a PreToolUse hook reading stdin JSON.
- Match path globs from the table above against `tool_input.file_path`.
- Use `scripts.lib.frontmatter.parse` to parse the new-content frontmatter.
- On block, return JSON `{"decision":"block","reason":...}` to stdout.
- Honor an opt-out via the **same convention** as `.claude/hooks/assumption-threshold-lock.md`: frontmatter must declare ALL of `override_handover_link: true`, `override_reason: <non-empty>`, `override_authorized_by: <name>`, `override_authorized_at: <YYYY-MM-DD>`. On override, allow the write AND append a one-line entry to `delivery/HANDOVER-OVERRIDE-LOG.md` (creates the file if absent) recording date/path/authorizer/reason.

### Ask first
- Adding new path globs (a new handover, a new artifact subtype). Default: only the seven table rows are enforced.
- Changing the override field names. Default: match `assumption-threshold-lock.md` — `override_handover_link:` + `override_reason:` + `override_authorized_by:` + `override_authorized_at:` + log.

### Never do
- Read or modify any file other than what the tool_input points at (and the same file's existing on-disk content for Edit-without-frontmatter cases).
- Raise an uncaught Python exception — any internal error degrades to exit 0 + stderr warning so the hook never bricks the session.
- Touch paths outside the seven handover globs — out-of-scope writes pass through silently.

## Verification mode

- **TDD.** Unit tests under `scripts/tests/test_check_handover_link.py` drive implementation.
- **Goal-based check.** `tools/lint-hook.sh .claude/hooks/check-handover-link.md` exits 0.
- **Manual gesture.** With the hook wired in a fresh session, attempting to Write a `discovery/trees/foo.md` whose frontmatter lacks `parent_intent` produces a visible block message; adding `parent_intent: <slug>` and retrying succeeds.

## Contract tests

- `test_allows_write_with_required_parent_field` — `discovery/trees/foo.md` with `parent_intent: some-intent` passes.
- `test_blocks_write_when_parent_field_missing` — same path, no `parent_intent` → exit 2 with reason mentioning `parent_intent`.
- `test_warns_when_parent_target_file_missing` — `parent_intent: nonexistent-slug` declared but file doesn't exist → exit 0 + stderr note.
- `test_landing_requires_both_parent_fields` — `delivery/landings/foo.md` needs both `parent_vision` AND `parent_handoff_packet`; missing either blocks.
- `test_vision_requires_both_parent_fields` — `delivery/visions/foo.md` needs both `parent_learning` AND `parent_intent` (per HANDOVERS.md Handover 4); missing either blocks.
- `test_strategy_intent_passes_without_parent_diagnosis` — `strategy/intents/foo.md` with no `parent_diagnosis` is allowed (it's optional).
- `test_override_with_all_fields_unblocks_and_logs` — frontmatter has all four override fields → exit 0; `delivery/HANDOVER-OVERRIDE-LOG.md` gains a line.
- `test_override_without_reason_blocks` — `override_handover_link: true` but `override_reason:` empty → exit 2.
- `test_override_without_authorizer_blocks` — `override_handover_link: true`, reason present, `override_authorized_by:` empty → exit 2.
- `test_override_false_does_not_unblock` — `override_handover_link: false` is treated as no-override (normal blocking behavior applies).
- `test_path_outside_handover_globs_passes_silently` — `tools/some-script.py` or `context/README.md` passes through with exit 0, no warnings.
- `test_edit_with_frontmatter_touching_old_string_reconstructs_proposed_state` — Edit whose `old_string` contains `---` is applied to the on-disk file; the proposed final frontmatter is what the hook validates.
- `test_edit_body_only_uses_on_disk_frontmatter` — Edit `new_string` is body-only (no `---` in `old_string`); the hook reads the on-disk file's frontmatter unchanged; an unchanged correct frontmatter passes silently.
- `test_multiedit_treated_as_sequence_of_edits` — MultiEdit with one frontmatter-touching edit and one body edit is validated against the post-sequence file state.
- `test_dangling_parent_initiative_resolves_to_readme_not_flat_md` — `parent_initiative: foo` resolves only to `delivery/initiatives/foo/README.md`, never `delivery/initiatives/foo.md`.
- `test_dangling_parent_vision_resolves_to_flat_md_not_readme` — `parent_vision: foo` resolves to `delivery/visions/foo.md`, not `delivery/visions/foo/README.md`.
- `test_malformed_frontmatter_degrades_to_warning_not_crash` — a file with an unclosed `---` block exits 0 with a stderr note, not exit 2.
- `test_initiative_readme_path_pattern` — only `delivery/initiatives/<slug>/README.md` matches Handover 5; `delivery/initiatives/<slug>/specs/foo.md` does not.
- `test_uppercase_path_warns_but_does_not_block` — `Delivery/Visions/foo.md` (mixed case) does not match any glob; exit 0 with a stderr note ("ontology-naming-convention: uppercase path under a phase root").

## Non-goals

- Validating that the *content* of the parent target is well-formed (that's `/audit-traceability`).
- Cross-checking the parent's lifecycle status (e.g., refusing a Vision write because its parent Learning is `Draft`). That's an audit-time concern.
- Enforcing parent links for **child specs** under `delivery/initiatives/<slug>/specs/*.md`. HANDOVERS.md doesn't include them in the seven canonical handovers; their `parent_initiative:` requirement will be guarded by a follow-up hook spec when `/audit-spec-linkage` (P4.10) firms up.
- Acting as a PostToolUse hook (deferred to the audit suite — this is a write-time gate only).

## Open questions

(None remain blocking. Both prior questions were resolved into Boundaries + Contract tests during pre-EXECUTE review.)

## Acceptance criteria

- [ ] `scripts/check-handover-link.py` exists, stdlib + `scripts.lib.frontmatter` only.
- [ ] `wc -l scripts/check-handover-link.py` reports ≤ 300 (verified by Task 7's pre-pr.sh wiring; design constraint, not aspirational).
- [ ] `scripts/tests/test_check_handover_link.py` exists; all 17 contract tests pass.
- [ ] `.claude/hooks/check-handover-link.md` exists; `tools/lint-hook.sh` exits 0 against it.
- [ ] `python3 -m unittest scripts.tests.test_check_handover_link` exits 0.
- [ ] PLAN / VERIFY / REVIEW gates exit 0.
- [ ] **Depends on:** F0.10 (`tools/lint-hook.sh`) must ship before VERIFY can run.
- [ ] (F2.6 will wire the hook into `.claude/settings.json` — not a gate for this spec.)

## Cross-references

- **Consumed by:** F2.6 (claude-settings-hooks-wiring) — adds the matcher entry.
- **Consumes:** `scripts.lib.frontmatter` (F1.2). Does NOT consume F1.1 (no graph walk needed at write-time — the seven path rules are local).
- **Frontmatter fields owned:** reads all seven `parent_*` fields; introduces `override_handover_link:` + `override_reason:` + `override_authorized_by:` + `override_authorized_at:` (same convention as `.claude/hooks/assumption-threshold-lock.md`).
- **Ontology object types touched:** Strategic Intent, OST, Validation Learning Memo, Vision, Initiative, Handoff Packet, Landing Report (the seven Domain I composites).
