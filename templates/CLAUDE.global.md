# Global preferences (Layer 1)

Copy to `~/.claude/CLAUDE.md` and personalize. Loaded into every session, everywhere. Keep lean — every line costs context budget on every turn.

## Working style

- Always plan before non-trivial work; wait for approval before executing
- Direct feedback, no hedging
- One clarifying question at a time
- Bullets for summaries, prose for narratives
- No emojis unless I ask
- For structural artifacts: emit result + steps + validate + repair

## Code & file conventions

- Markdown with YAML frontmatter for everything that isn't code
- Kebab-case filenames, ISO dates (`YYYY-MM-DD`) for temporal files
- Frontmatter `parent_*:` links for handover artifacts
- Frontmatter `object_type:` per the ontology (when in a kit-aware project)

## Phase awareness

Before producing any phase-handover artifact (intent, OST, learning, vision, initiative, spec, handoff packet, landing), confirm the prior phase's artifact exists. If it doesn't, surface that and recommend producing it first. Phase-skipping is the kit's #1 failure mode, and it's silent.

## Human-vs-AI ownership

When working in an ai-product-kit project: every artifact declares `human_owned_decisions:` and `ai_assistance_used:` in frontmatter. AI defaults to "human-led with AI support" unless an activity is explicitly cleared. Never make commitments — pricing, roadmap, legal, customer-facing claims — on the human's behalf; surface them as human-owned decisions instead.

## Safety

- Never touch `~/.ssh`, credentials, `.env*` files
- Never push to protected branches (`main`, `master`, `production`, `release/*`)
- If you find yourself wanting to run something destructive, stop and ask

## When unsure

Read project `AGENTS.md` (or `CLAUDE.md`) + relevant files in `context/` before guessing.
