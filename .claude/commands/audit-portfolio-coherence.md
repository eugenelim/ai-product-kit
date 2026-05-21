---
description: Rumelt-style coherence audit across all active strategic intents and delivery initiatives. Flags pairs of bets that pull in opposite directions on resources, capabilities, or market posture.
argument-hint: "[optional: 'verbose' for the full reasoning trace]"
---

# /audit-portfolio-coherence

**Canonical implementation:** `scripts/audit-portfolio-coherence.py` (F1.6 — shipped 2026-05-21). When the script is available:

```bash
python3 scripts/audit-portfolio-coherence.py --root . --format markdown
```

Exit codes: 0 clean, 1 drift, 2 incoherent, 3 no-portfolio. Add `--write` to persist to `strategy/diagnoses/<date>-coherence-audit.md` and append to `COHERENCE-LOG.md`. The prose procedure below is the fallback when reviewing the contract.

---

**Phase:** Strategy (1), cross-portfolio
**Ontology types audited:** Strategic Intent, Initiative, Vision

Run a Rumelt coherence audit across the active portfolio. Coherence — the second-most-named strategy failure after "list of goals" — is what kills strategy execution most often: initiatives that each look reasonable in isolation but cancel each other out in aggregate.

## When to run

- Weekly, as part of the trio cadence review
- Before any new initiative is approved
- Immediately if `/cadence-check` flags a strategy refresh as overdue
- During quarterly `/strategy-refresh` (as input to the next intent)

## Inputs

1. Every file in `strategy/intents/*.md`
2. Every active vision in `delivery/visions/*.md` (status not `done` or `killed`)
3. Every active initiative in `delivery/initiatives/*/README.md` (status `active`)
4. Every recent landing in `delivery/landings/*.md` from the last 90 days
5. `context/frameworks/strategic-coherence.md` — the rule library

If the most recent strategy intent is older than 90 days, surface that first and ask whether to proceed (coherence on a stale intent is unreliable).

## Procedure

### Step 1 — extract bets
For each artifact, extract declared bets along three axes (using the `strategy-coherence` skill):
- **Resources** — eng time, capital, attention, headcount
- **Capabilities** — what muscle it builds or atrophies by neglect
- **Market posture** — premium / price-leader / innovator / integrator; self-serve / sales-led

Emit a structured table to `/tmp/portfolio-bets.md` and show me before continuing.

### Step 2 — pairwise check
For every pair of active artifacts, ask Rumelt's three coherence questions:
1. Do they share a focusing logic?
2. Do they reinforce each other's resources?
3. Are their market postures consistent?

For >10 active artifacts, fan out to sub-agents (N² grows fast).

### Step 3 — produce the audit
Write to `strategy/diagnoses/<YYYY-MM-DD>-coherence-audit.md` with frontmatter:

```yaml
---
object_type: Coherence Audit
date: <YYYY-MM-DD>
artifacts_audited: <count>
pairs_checked: <count>
contradictions_flagged: <count>
worst_contradiction: <pair>
status: clean | drift | incoherent
human_owned_decisions:
  - Remediation choice per contradiction (resolve / sequence / kill)
---
```

Sections:
1. **Verdict** — clean / drift / incoherent in one paragraph
2. **Contradictions found** — each as: pair, axis, nature, recommended remediation
3. **Adjacency** — places where small adjustments would increase reinforcement (not contradictions)
4. **What's at risk** — per contradiction, the failure mode if unresolved

### Step 4 — propose remediation
For each contradiction, exactly one of:
- **Resolve** — change one artifact's frontmatter to align
- **Sequence** — both can survive if one waits; state which goes first
- **Kill** — one must drop; state which and why

Do not silently accept contradictions. Every pair gets a named remediation, even if it's "leadership decision required."

### Step 5 — log
Append to `strategy/diagnoses/COHERENCE-LOG.md`: date, status, contradictions, link.

## Stop conditions

Stop and ask before continuing if:
- More than 12 active artifacts (confirm scope)
- Most recent strategy intent is older than 90 days
- Any active artifact is missing required frontmatter

## Why this matters

From the operating model: "Three concurrent initiatives that each look reasonable in isolation but contradict each other in aggregate — Rumelt's 'list of wishes' failure at the portfolio level." This is the mechanical detector for that failure.

$ARGUMENTS
