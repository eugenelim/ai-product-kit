# ai-product-kit

A Claude Code-powered operating system for product managers, built on three foundations:

1. **A four-phase operating model** (Strategy → Discovery → Validation → Delivery → Landings) with each phase gated by a load-bearing handover artifact.
2. **A canonical product/business ontology** — eight domains, 82 documented typed objects (74 atomic + 8 composite), traceability rules from Market → Customer → Problem → Capability → Requirement → Outcome → Launch → Measurement.
3. **Claude Code mechanics** — markdown memory, slash commands, agents, skills, hooks, plug-ins — distilled from Teresa Torres's [Claude Code Recipes](https://www.producttalk.org/tag/claude-code-recipes/) series.

The first foundation tells you *what phase you're at*. The second tells you *what kind of object you're producing and what links it must carry*. The third tells you *which Claude Code primitive to reach for*.

The kit's central claim: **most PM tooling is flat — a catalog of activities with no phase awareness and no type system.** This kit refuses to be flat. Every artifact declares the phase it serves and the ontology type it is. The repo structure enforces handovers as artifacts rather than conversations.

---

## Start here

**For humans:**
- [`docs/CHARTER.md`](docs/CHARTER.md) — what this kit is, in/out of scope, principles, success criteria
- [`ROADMAP.md`](ROADMAP.md) — the ordered build queue (pick the lowest-numbered open item)
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — the minimum bar for a PR
- [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) — how work happens, universal metadata schema, ADR/RFC/spec lifecycle
- [`docs/architecture/overview.md`](docs/architecture/overview.md) — structural map of the repo
- [`docs/PHASE-GUIDE.md`](docs/PHASE-GUIDE.md) — "where am I, what's next?" decision table
- [`docs/HANDOVERS.md`](docs/HANDOVERS.md) — artifact contracts at every phase boundary
- [`docs/HUMAN-AI-OWNERSHIP.md`](docs/HUMAN-AI-OWNERSHIP.md) — what AI may assist with, what humans must own
- [`docs/INVENTORY.md`](docs/INVENTORY.md) — every command, agent, skill, hook in one table (each row has a `Status` column — shipped vs planned)
- [`docs/guides/`](docs/guides/) — user-facing docs in Diátaxis form (tutorials, how-to, reference, explanation) *(directory ships empty; populated as guides land)*

**For agents (Claude Code, Cursor, Codex, Gemini CLI, Copilot):**
- Read [`AGENTS.md`](AGENTS.md) first. `CLAUDE.md` is a symlink.

**To build a new kit component:**
```bash
tools/new-spec.sh <feature-slug>
# fill docs/specs/<slug>/spec.md and plan.md
# follow .claude/skills/work-loop/SKILL.md
```

## Quickstart

```bash
git clone <this-repo> ~/ai-product-kit
cd ~/ai-product-kit

# global preferences (once)
cp templates/CLAUDE.global.md ~/.claude/CLAUDE.md
$EDITOR ~/.claude/CLAUDE.md

# project-scoped: declare your mode
$EDITOR .claude/CLAUDE.md          # set mode: greenfield | enterprise

# fill your reference context — the context/ subdirectories ship empty;
# create these files as your project unfolds:
$EDITOR context/business/profile.md
$EDITOR context/personas/primary.md
$EDITOR context/products/<product>.md
$EDITOR context/voice/guide.md

# start
claude

# inside Claude Code
/phase-guide                       # what phase am I at, what's next
```

## Repository layout

```
ai-product-kit/
├── AGENTS.md                       ← canonical agent context (read first)
├── CLAUDE.md                       ← symlink to AGENTS.md
├── README.md                       ← this file
├── .claude/
│   ├── CLAUDE.md                   ← project-scoped preferences (mode: greenfield | enterprise)
│   ├── settings.json               ← hook config, status line, deny rules (planned — ROADMAP F2.6)
│   ├── commands/                   ← slash commands (5 shipped; rest planned per ROADMAP)
│   ├── agents/                     ← project-scoped sub-agents (2 shipped: adversarial-reviewer + competitor-research; rest planned)
│   ├── skills/                     ← portable skills (3 shipped: work-loop, ost-validator, strategy-coherence; rest planned)
│   └── hooks/                      ← phase-guard scripts (1 shipped: assumption-threshold-lock; rest planned per ROADMAP F2)
├── docs/                           ← the kit's own documentation
│   ├── CHARTER.md                  ← mission, scope, principles (one page)
│   ├── CONVENTIONS.md              ← how work happens, universal metadata schema
│   ├── PHASE-GUIDE.md              ← "where am I, what's next"
│   ├── HANDOVERS.md                ← artifact contracts at every phase boundary
│   ├── HUMAN-AI-OWNERSHIP.md       ← what AI may assist with, what humans must own
│   ├── INVENTORY.md                ← every command, agent, skill, hook
│   ├── adr/                        ← Architecture Decision Records (frozen)
│   ├── rfc/                        ← Requests for Comments (kit governance)
│   ├── guides/                     ← Diátaxis user docs
│   └── inspiration/                ← source documents this kit synthesizes
├── context/                        ← Layer-3 reference, pulled on demand
│   ├── personas/
│   ├── products/
│   ├── business/
│   ├── voice/
│   ├── frameworks/                 ← Rumelt, OST, JTBD, Wardley, EARS, ONTOLOGY
│   └── glossary/
├── strategy/                       ← Phase 1
│   ├── diagnoses/
│   ├── wardley-maps/
│   └── intents/                    ← THE handover artifact
├── discovery/                      ← Phase 2
│   ├── outcomes/
│   ├── interviews/
│   ├── snapshots/
│   ├── opportunities/
│   ├── trees/                      ← THE handover artifact (chosen opportunity flagged)
│   └── research-digest/
├── validation/                     ← Phase 3
│   ├── assumption-maps/
│   ├── experiments/
│   └── learnings/                  ← THE handover artifact
├── delivery/                       ← Phase 4
│   ├── visions/                    ← Vision sub-phase
│   ├── initiatives/                ← Initiative sub-phase
│   ├── specs/                      ← Spec sub-phase
│   ├── handoff-packets/            ← Engineering handoff (the ontology's signature deliverable)
│   ├── release-notes/
│   ├── landings/                   ← Phase 5: outcome vs prediction
│   └── retros/
├── communication/                  ← cross-cutting
├── market/                         ← greenfield mode primarily
├── personal-os/                    ← daily rhythm
├── plugins/                        ← shippable bundles
├── scripts/                        ← Python / Node utilities
└── templates/                      ← frontmatter templates per object type
```

## What's new in v3 (vs v2)

- **AGENTS.md as canonical agent context** — adopted from the agent-ready-repo template. Works across Claude Code, Cursor, Codex, Gemini CLI, Copilot. `CLAUDE.md` is a symlink.
- **Source-of-truth table** — every kind of decision has exactly one place it lives. "If you can't find it in one of these places, the answer doesn't exist yet — ask, or open an RFC."
- **Charter / ADR / RFC structure** — lifecycle-aware doc taxonomy. Charter is frozen one-page constitution; ADRs record decisions with their full rationale; RFCs propose changes to the kit.
- **Canonical product/business ontology** — eight domains, 82 documented typed objects (74 atomic + 8 composite), universal metadata schema. Every artifact declares its `object_type:` and links into the traceability chain.
- **Human-vs-AI ownership model** — every artifact declares `human_owned_decisions:`, `ai_assistance_used:`, `ai_assistance_allowed:`, `human_approval_required:`. The completeness audit refuses to mark an artifact `Approved` without the named human signatures.
- **Specialist reviewer subagents** — `adversarial-reviewer`, `compliance-reviewer`, `quality-engineer`. Sharp, differentiable lenses; pick the ones the artifact warrants.
- **The work-loop skill** — plan → execute → verify → review, the kit's standard PM-work pattern.
- **New audits** — `/audit-traceability` (every requirement traces to evidence), `/audit-completeness` (the ontology's pre-engineering-handoff checklist as a single command).
- **Engineering handoff packet as a first-class artifact** — `delivery/handoff-packets/<slug>/` with required contents per the ontology's section 28.

## Reading order

**Operating-model side:**
1. Rumelt, *Good Strategy / Bad Strategy*
2. Perri, *Escaping the Build Trap*
3. Torres, *Continuous Discovery Habits*
4. Cagan, *Inspired* / *Empowered*
5. Bland & Osterwalder, *Testing Business Ideas*
6. Wardley, *Wardley Maps* (free online)

**Mechanics side:**
- Torres's [Claude Code Recipes](https://www.producttalk.org/tag/claude-code-recipes/) series — eight articles
- The agent-ready-repo template README

The kit is the synthesis. The books and the template are the source.

## Credits

- Four-phase operating model: [`docs/inspiration/product-operating-model.md`](docs/inspiration/product-operating-model.md)
- Product/business ontology: [`docs/inspiration/product_business_knowledge_ontology_agent_handoff.md`](docs/inspiration/product_business_knowledge_ontology_agent_handoff.md)
- Practitioner's stack: [`docs/inspiration/product-research-development-strategy.md`](docs/inspiration/product-research-development-strategy.md)
- Repo-as-agent-context structure, source-of-truth pattern, Charter/ADR/RFC, work-loop, specialist reviewers, "when this file is wrong" discipline: the agent-ready-repo template
- Claude Code primitives, three-layer memory, parallel agents, scheduled team-of-agents, validate-then-repair pattern: Teresa Torres's [Claude Code Recipes](https://www.producttalk.org/tag/claude-code-recipes/)
- Landings-not-launches: 2026 industry consensus
- Strategic coherence audit: Rumelt's coherence principle + 2025/26 incoherence research
