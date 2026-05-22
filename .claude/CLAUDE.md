# Project preferences — ai-product-kit (v3)

Loaded automatically when Claude is launched inside this folder. Kept short — detail belongs in `context/` and `docs/`.

**See `AGENTS.md` at the repo root for the canonical, cross-tool agent-context file.** This project file is a Claude-Code-specific overlay.

## Mode

```
mode: greenfield
```

Change to `mode: enterprise` for brownfield work. The `mode-guard` hook *(planned — [ROADMAP F2.4](../ROADMAP.md#foundation-2--hook-scripts); not yet enforced)* will read this and:
- In greenfield: block `/wardley-map`, `/internal-jtbd-interview`, `/value-chain-evolution`
- In enterprise: block `/competitive-research`, `/market-scan`, `/jtbd-analogues`

Both modes share `/strategy-refresh`, `/strategic-intent`, `/audit-portfolio-coherence`, `/cadence-check`. Until `mode-guard` ships, mode is documentary — set it correctly and avoid the wrong-mode commands by convention.

If you're working across both modes, keep them in separate project folders. Mode is project-scoped intentionally.

## How we work together

(In addition to what's in `AGENTS.md`:)

- Always plan before non-trivial work. Show me the plan; wait for approval before executing.
- Direct feedback. No hedging, no "great question," no gentle suggestions when something is wrong.
- One clarifying question at a time. Never batch.
- Bullets for summaries; prose for narratives meant for readers.
- No emojis unless I ask.
- For structural artifacts (OST, change set, context map, coherence audit): emit result AND steps, validate, repair via agent loop.

## Phase awareness

Run `/phase-guide` before any non-trivial session. The right next step is almost always producing a missing handover artifact, not skipping ahead.

Handover contracts: `docs/HANDOVERS.md`. Phase-guard hooks enforce them.

## Object types (ontology)

Every artifact declares its `object_type:` per `context/frameworks/ontology.md`. Eight domains (A–H) plus a kit-composite Domain I, for 82 documented types total (74 atomic + 8 composite handover artifacts). When uncertain, run the `ontology-classifier` skill — it surfaces missing fields and proposes the type.

## Human-vs-AI ownership

Every artifact declares `human_owned_decisions:`, `ai_assistance_used:`, `ai_assistance_allowed:`. See `docs/HUMAN-AI-OWNERSHIP.md`. AI defaults to "human-led with AI support" unless an activity is explicitly cleared for AI assistance.

## Defaults

- Default model: `sonnet`. `haiku` for cheap fan-out (per-competitor, per-paper, per-cohort). `opus` for hardest synthesis (full OST regeneration, exec narratives, portfolio-coherence audits, completeness audits on large initiatives).
- Default file format: markdown with YAML frontmatter using the universal metadata schema (`docs/CONVENTIONS.md`).
- Default filenames: kebab-case, dated when temporal.
- Never touch `~/.ssh`, `.env*`, credential paths. `scripts/guard-credentials.py` (the `guard-credentials` PreToolUse hook) hard-blocks these with no model-side override; don't propose.
