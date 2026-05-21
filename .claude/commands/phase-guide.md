---
description: Interactive "where am I, what's next?" diagnostic. Asks what artifact you currently have signed off, tells you what phase you're at, and recommends the next artifact to produce.
---

# /phase-guide

When something feels stuck, the answer is almost always *go back one phase*. This command finds your phase and tells you what's next.

## When to run

- When you don't know where to start
- When work feels like it's spinning
- After a long break from a project
- At the start of any planning session

## Procedure

### Step 1 — read state
Scan the file system and produce a current-state report (without asking yet):
- Most recent `strategy/intents/` (date + slug + `last_refresh`)
- Most recent `discovery/trees/` (date + slug + whether `chosen_opportunity` is set)
- Most recent `validation/learnings/` (date + slug + status)
- Most recent `delivery/visions/` (date + slug)
- Most recent `delivery/initiatives/*/README.md` (date + slug)
- Most recent `delivery/specs/` (date + slug)
- Most recent `delivery/handoff-packets/` (date + slug + completeness audit verdict)
- Most recent `delivery/landings/` (date + slug + verdict)
- `mode:` from project `CLAUDE.md`

### Step 2 — diagnose
Use `docs/PHASE-GUIDE.md` as the rule table. Map the most-recent signed-off artifact to a phase and a next-artifact recommendation.

### Step 3 — surface drift
Check:
- Strategy intent older than 90 days? → strategy refresh overdue
- Most-recent OST older than 35 days? → OST stale
- Any `chosen_opportunity` with no assumption map for >7 days? → assumption-coverage drift
- Any shipped initiative >30 days old with no landing report? → landings debt
- Any artifact with `human_approval_required: true` and empty `approvals_obtained:` for >7 days? → approval drift (new in v3, per the ontology)

If any drift is detected, surface it **before** the next-artifact recommendation. The drift may be the real problem.

### Step 4 — ask one clarifying question if needed
If multiple active intents exist and it's ambiguous which I'm working on, ask exactly one question. Never batch.

### Step 5 — recommend
Output three lines:

```
PHASE: <name>
DRIFT: <none | listed items>
NEXT: <command + one-sentence why>
```

Then offer to run the next command, but wait for me to say yes.

## What this command will not do

- Not skip phases. If state shows we're at Discovery and you ask for a spec, tell what's missing rather than help skip.
- Not invent an intent. If `strategy/intents/` is empty, route to `/strategy-refresh`; do not pretend to know the business.
- Not run audits unprompted. If drift is severe, surface it and ask; don't auto-run.
