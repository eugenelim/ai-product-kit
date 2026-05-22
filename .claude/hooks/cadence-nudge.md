# cadence-nudge hook

A quiet ambient reminder on SessionStart. Surfaces three categorical drift signals — stale strategy, orphan OST, kill-drought — that the kit's three-tier operating cadence (quarterly / monthly / bimonthly) makes invisible by default.

Never blocks. Never demands action. Just makes the drift visible.

## What it does

Registered as a `SessionStart` hook. On every session, runs `scripts/cadence-nudge.py`, which:

1. Builds the typed-object graph via `scripts.lib.graph.build` (read-only).
2. Runs three independent signal functions:
   - **Stale strategy** — any `Strategic Intent` with `last_updated` more than **90 days** ago.
   - **Orphan OST** — any `Opportunity Solution Tree` whose frontmatter has no `chosen_opportunity:` value AND whose `last_updated` is more than **30 days** ago.
   - **Kill-drought** — no `Validation Learning Memo` with `status: killed` in the last **60 days**; OR no learnings at all AND at least one OST whose `chosen_opportunity:` points at a node with `status != killed`.
3. If any signal fires, emits a single `hookSpecificOutput.additionalContext` block on stdout. If no signal fires, exits silently.
4. If the graph build raises, exits 0 + stderr trace (SessionStart is informational; never block the user).

Empty-kit predicate: if the graph contains zero typed nodes of all three target types, the hook exits silently — a freshly-initialised kit isn't drifting.

## Why this matters

The kit declares quarterly, monthly, and weekly rhythms in `docs/PHASE-GUIDE.md`. Nothing currently surfaces a missed beat. Drift is silent, which is precisely the failure mode the operating model warns about: a strategy that was last touched five months ago and is still being referenced as live, an OST whose chosen-bet was never named, a validation queue with no kill verdicts on file (the textbook validation-theatre signature).

This hook is the ambient counterpart to the eventual `/cadence-check` (P7.5) command. The audit goes deep on a single phase's rhythm; this nudge stays light and runs on every session.

Repetition is the feature. The hook keeps firing every session until the user acts — refreshes the intent, names a chosen opportunity, files a kill verdict. There is no per-session de-duplication.

## What it does NOT do

- Distinguish "no validation yet" from "validation went cold." The kit's freshness is the proxy; perfect distinction is overkill.
- Track individual cadence rhythms (weekly retros, monthly reviews, quarterly resets). That's `/cadence-check`.
- Modify any artifact. The hook is read-only.
- Persist nudge state across sessions. The user is supposed to see the same nudge until they act.
- Run on any event other than `SessionStart`.

## Message format

When any signal fires, the hook emits one block:

```
Cadence drift detected:
- Stale strategy: <slug> (<YYYY-MM-DD>), … (last updated >90 days ago)
- Orphan OST: <slug> (<N>d) (no chosen_opportunity for >30 days)
- Kill drought: <N> days since last killed learning
Consider: /cadence-check, /strategy-refresh, /kill-or-survive
```

Findings render in fixed order (stale-strategy → orphan-ost → kill-drought). Each signal's value-list is rendered inline; if it would exceed 500 characters, items beyond index 1 are replaced with `…` so the whole block stays under 600 characters. The truncation is deterministic — the same kit always produces the same nudge.

## Override

There is no override. The signals fire on real drift; the way to silence them is to act on them. Specifically:

- Stale strategy → run `/strategy-refresh` (or update `last_updated:` deliberately if the intent is still current as-is).
- Orphan OST → name a `chosen_opportunity:` on the OST node's frontmatter (or kill the OST).
- Kill drought → file a `Validation Learning Memo` with `status: killed` (real kills only — don't manufacture verdicts to silence the hook).

If a signal is genuinely a false positive (e.g., the team has decided 180 days is the right strategy-refresh cadence for their domain), surface it as an RFC under `docs/rfc/` to tune the threshold; do not patch the hook in-session.

## Configuration

In `.claude/settings.json` (wired by F2.6):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "python3 scripts/cadence-nudge.py"
      }
    ]
  }
}
```

The hook reads stdin (the SessionStart payload) and ignores it. It always exits 0. On any internal failure, it prints a trace to stderr and exits 0 — SessionStart is on the user's interactive critical path; never block.

## Related

- `/cadence-check` (P7.5, planned) — the deep human-driven audit. This hook is its ambient counterpart.
- `/strategy-refresh` — produces an updated `strategy/intents/<slug>.md`.
- `/kill-or-survive` (planned) — files a kill verdict learning.
- `scripts/lib/graph.py` (F1.1) — the typed-object walker.
- `scripts/lib/frontmatter.py` (F1.2) — the YAML-subset parser.
- `docs/PHASE-GUIDE.md` — the three-tier cadence rhythms cited by the thresholds.
