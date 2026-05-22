# check-handover-link hook

Refuses to Write or Edit a kit artifact under one of the seven canonical handover paths unless its frontmatter declares the required `parent_*` link for that path.

This is the mechanical version of "does the prior handover artifact exist?" — and the cheapest defense against phase-skipping, which `AGENTS.md` names as the kit's #1 silent failure mode.

## What it does

Registered as a `PreToolUse` hook on `Write`, `Edit`, and `MultiEdit`. Runs `scripts/check-handover-link.py`, which:

1. Reads the PreToolUse JSON payload from stdin and extracts `tool_input.file_path` plus the new content's frontmatter.
2. Matches the path against the seven path rules (one per handover in `docs/HANDOVERS.md`). Out-of-scope paths pass silently.
3. Parses the proposed frontmatter via `scripts.lib.frontmatter.parse`.
4. If the required `parent_*` field is missing or empty, **blocks the write** with `{"decision":"block","reason":...}` on stdout and exit 2.
5. If the field is present but the parent target file does not exist, **allows the write** and emits a one-line stderr warning. Broken-link detection at write time would be too noisy — the auditor catches it later.

The seven path rules (the load-bearing table):

| Path | Handover | Required `parent_*` field(s) | Parent target resolves to |
|---|---|---|---|
| `strategy/intents/*.md` | 1 | (none — `parent_diagnosis` is optional) | n/a |
| `discovery/trees/*.md` | 2 | `parent_intent` | `strategy/intents/<slug>.md` |
| `validation/learnings/*.md` | 3 | `parent_opportunity` | `discovery/opportunities/<slug>.md` |
| `delivery/visions/*.md` | 4 | `parent_learning` AND `parent_intent` | `validation/learnings/<slug>.md`; `strategy/intents/<slug>.md` |
| `delivery/initiatives/<slug>/README.md` | 5 | `parent_vision` | `delivery/visions/<slug>.md` |
| `delivery/handoff-packets/<slug>/README.md` | 6 | `parent_initiative` | `delivery/initiatives/<slug>/README.md` |
| `delivery/landings/*.md` | 7 | `parent_vision` AND `parent_handoff_packet` | `delivery/visions/<slug>.md`; `delivery/handoff-packets/<slug>/README.md` |

The fourth column is the dangling-link resolver: the hook tries exactly the listed path; there is no fallback between flat-file and README forms. If `HANDOVERS.md` is amended, edit `HANDOVER_RULES` in the script in the same change.

Edit / MultiEdit semantics: an edit whose `old_string` contains the `---` delimiter is treated as frontmatter-touching — the hook applies each `(old, new)` substitution to the on-disk file in order and parses the result. Body-only edits (no `---` in any `old_string`) use the on-disk frontmatter directly, because they aren't changing it.

## Why this matters

`AGENTS.md` calls out phase-skipping as the kit's #1 silent failure mode:

> Phase-skipping is the kit's #1 failure mode, and it's silent.

Without this hook, an author can produce a Vision with no `parent_learning`, an Initiative with no `parent_vision`, a Handoff Packet with no `parent_initiative` — and only a manual `/audit-traceability` run will catch the missing link after the fact. By then the chain has been quoted in three more documents.

The hook converts the prose discipline in `docs/HANDOVERS.md` into a write-time guard. Like `assumption-threshold-lock`, the goal is not to make the workflow harder — it's to make the discipline mechanical so the human reviewer's attention can go to the *content* of the link rather than the *presence* of the link.

## How to write a parent-linked artifact

For each handover the required frontmatter is exactly what `docs/HANDOVERS.md` already specifies. A few examples:

OST (Handover 2):

```yaml
---
object_type: Opportunity Solution Tree
parent_intent: <strategic-intent-slug>
# ... rest of OST frontmatter per HANDOVERS.md ...
---
```

Vision (Handover 4, dual parents):

```yaml
---
object_type: Vision
parent_learning: <validation-learning-slug>
parent_intent: <strategic-intent-slug>   # restated for traceability
# ...
---
```

Landing Report (Handover 7, dual parents):

```yaml
---
object_type: Landing Report
parent_vision: <vision-slug>
parent_handoff_packet: <handoff-packet-slug>
# ...
---
```

Strategic Intents (Handover 1) carry an optional `parent_diagnosis:` — the hook does not require it. Child specs under `delivery/initiatives/<slug>/specs/*.md` are out of scope here (they have their own `parent_initiative:` requirement covered by the `/audit-spec-linkage` detector, not this hook).

## Override

Sometimes you need to backfill an artifact that legitimately predates its parent's existence in the kit (e.g., a legacy strategic intent imported from a planning doc). Set in the artifact's frontmatter, mirroring the `assumption-threshold-lock` convention:

```yaml
override_handover_link: true
override_reason: <one-paragraph explanation>
override_authorized_by: <name>
override_authorized_at: <YYYY-MM-DD>
```

All four fields are required. The hook will allow the write AND append a one-line entry to `delivery/HANDOVER-OVERRIDE-LOG.md` recording date, path, authorizer, and reason. Overrides accumulate; if the log gets long, the kit is silently phase-skipping across the board — which is itself a signal worth surfacing in the next portfolio review.

## What's NOT enforced

- The hook does not validate the *content* of the parent target — that's `/audit-traceability`'s job.
- It does not cross-check the parent's lifecycle status (e.g., refusing a Vision write because its parent Learning is still `Draft`) — also audit-time.
- It does not guard child specs under `delivery/initiatives/<slug>/specs/*.md`. A follow-up hook will, once `/audit-spec-linkage` firms up.
- A dangling parent reference (the `parent_*` field points at a file that doesn't exist) **warns** rather than blocks. Authoring out of order is normal; auditing catches the unresolved link later.

## Configuration

Wired in `.claude/settings.json` as of F2.6 (2026-05-21):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {"type": "command", "command": "python3 scripts/check-handover-link.py"}
        ]
      }
    ]
  }
}
```

The hook is path-aware internally — it doesn't need a `matchPaths` filter at the settings layer. Writes outside the seven handover globs pass through with exit 0 and no output.

## Related

- `docs/HANDOVERS.md` — the seven handover contracts (the source of truth for the rules table above)
- `.claude/hooks/assumption-threshold-lock.md` — same override convention; sibling phase-discipline guard
- `/audit-traceability` — write-time guard is local; the audit is global
- `scripts/lib/frontmatter.py` (F1.2) — the parser this hook consumes
- `scripts/audit-traceability.py` — the read-time complement
