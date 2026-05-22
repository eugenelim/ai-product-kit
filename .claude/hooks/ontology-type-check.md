# ontology-type-check hook

A soft nudge that catches the kit's highest-frequency drift mode: creating a typed artifact under its canonical path without declaring the matching `object_type:` in frontmatter.

This hook **warns**. It never blocks.

## What it does

Registered as a `PreToolUse` hook on `Write`, `Edit`, and `MultiEdit`.

Before any such write, the hook runs `scripts/check-ontology-type.py`, which:

1. Reads the proposed file path from the tool payload (strips a trailing slash before matching).
2. Looks up the path against the ten-row implied-type table below.
3. If the path matches a row, parses the post-edit frontmatter:
   - **Write:** the `content` field.
   - **Edit (body-only — no `---` in `old_string`):** the on-disk file as-is.
   - **Edit (frontmatter-touching):** the file with the replacement applied.
   - **MultiEdit:** applies edits sequentially and inspects the final state.
4. Compares the declared `object_type:` to the implied type using exact, case-sensitive equality.
5. If the value is missing or doesn't match, prints a one-line nudge to stderr and exits 0.
6. If the value matches exactly, stays silent.

Exit code is 0 in every branch. The write always proceeds.

## Why this matters

The kit's traceability audits (`/audit-traceability`, `/audit-completeness`) and the frontmatter linter (`tools/lint-frontmatter.py`) depend on every typed artifact declaring `object_type:`. Missing-or-wrong-type is the highest-frequency ontology-drift case the kit's conventions cite.

A warn-only PreToolUse hook is the right enforcement level — strong enough to catch the omission in the moment the file is being written, weak enough to never block a session. Hard enforcement lives in the audits and the frontmatter linter; this hook is the early signal.

The nudge philosophy: surface the drift at write time so the human or model can fix it now, rather than letting it silently accumulate until the next audit run.

## The ten path globs

| Path glob | Implied `object_type:` |
|---|---|
| `strategy/intents/*.md` | `Strategic Intent` |
| `discovery/trees/*.md` | `Opportunity Solution Tree` |
| `discovery/opportunities/*.md` | `Opportunity` |
| `validation/assumption-maps/*.md` | `Assumption Map` |
| `validation/experiments/*/experiment.md` | `Experiment` |
| `validation/learnings/*.md` | `Validation Learning Memo` |
| `delivery/visions/*.md` | `Vision` |
| `delivery/initiatives/<slug>/README.md` | `Initiative` |
| `delivery/handoff-packets/<slug>/README.md` | `Handoff Packet` |
| `delivery/landings/*.md` | `Landing Report` |

Notes:

- `validation/experiments/*/results.md` is **not** in the table. `Experiment Result` is not a canonical ontology type today; if one is added via RFC, append the row.
- Initiative and Handoff Packet match only `README.md`. Sub-artifacts (`specs/foo.md`, `context-map.md`) have their own object types and varied paths — out of scope for this soft nudge.
- The table is HANDOVERS-derived. When `docs/HANDOVERS.md` gains or renames an artifact path, review this table before merging.

## What's NOT enforced

- Whether `object_type:` is in the canonical type set (that's `tools/lint-frontmatter.py`).
- Other universal-metadata fields beyond `object_type:` (also `tools/lint-frontmatter.py`).
- Inferring `object_type:` from file content. Only path → implied type.
- Sub-artifact paths inside Initiative or Handoff Packet folders.

## Nudge format

```
ontology-type-check: <path-as-received> implies object_type: <Implied> but <details>
```

Where `<details>` is one of:

- `object_type is missing`
- `frontmatter declares <Other>`

The path is emitted verbatim from the tool payload — no normalization.

## Configuration

In `.claude/settings.json` (wired by F2.6):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "command": "python3 scripts/check-ontology-type.py"
      }
    ]
  }
}
```

## Related

- `tools/lint-frontmatter.py` — authoritative shape and type-set check (CI/PR gate).
- `/audit-traceability` — fails when a typed artifact's links can't be resolved.
- `/audit-completeness` — fails when an initiative's pre-handoff fields are missing.
- `context/frameworks/ontology.md` — canonical 74-atomic + 8-composite type set.
- `docs/HANDOVERS.md` — the path-to-Domain-I-type mapping this table is derived from.
