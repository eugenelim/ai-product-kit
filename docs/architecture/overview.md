# Architecture overview

The map of the kit's repository. Not the why (ADRs do that); not where it's heading (ROADMAP does that); what it looks like today.

## Top-level shape

```
ai-product-kit/
├── AGENTS.md, CLAUDE.md       canonical agent context (CLAUDE.md is a symlink)
├── README.md, CONTRIBUTING.md, ROADMAP.md, LICENSE
├── .editorconfig, .gitignore, .github/workflows/
├── .claude/                   Claude Code primitives
│   ├── CLAUDE.md              project-scoped preferences (declares mode:)
│   ├── commands/              slash commands (5 shipped; the rest planned per ROADMAP)
│   ├── agents/                subagents (2 shipped: adversarial-reviewer, competitor-research; rest planned)
│   ├── skills/                portable skills with SKILL.md (3 shipped: work-loop, ost-validator, strategy-coherence)
│   └── hooks/                 hook documentation (1 shipped: assumption-threshold-lock; rest planned per ROADMAP F2)
├── tools/                     build harness scripts
│   ├── check-done.py          phase-gate enforcement
│   ├── lint-*.{sh,py}         shape and content linters
│   ├── pre-pr.sh              aggregation hook
│   └── new-spec.sh            spec scaffolder
├── scripts/                   runtime utilities the commands shell out to (planned — empty today; ROADMAP F1.1, F1.2, F1.4-1.6, F2.x will populate it)
│   └── lib/                   shared Python libraries (planned — graph walker F1.1, frontmatter parser F1.2)
├── context/                   Layer-3 reference, pulled on demand by Claude
│   ├── personas/, products/, business/, voice/, glossary/   (ship empty — populated by the user as their project unfolds)
│   └── frameworks/            (1 shipped: ontology.md; the other framework refs are planned per ROADMAP F4)
├── docs/                      kit's own documentation
│   ├── CHARTER.md             frozen one-page constitution
│   ├── CONVENTIONS.md         how work happens (universal metadata schema, ADR/RFC/spec mechanics)
│   ├── HUMAN-AI-OWNERSHIP.md  what AI may assist with vs what humans must own
│   ├── HANDOVERS.md           artifact contracts at every phase boundary
│   ├── PHASE-GUIDE.md         where am I, what's next
│   ├── INVENTORY.md           every command, agent, skill, hook in one table
│   ├── adr/                   frozen decision records
│   ├── rfc/                   in-flight proposals
│   ├── specs/<feature>/       per-kit-component contract + plan
│   ├── _templates/            spec / plan / state.json / adr / rfc starters
│   ├── architecture/          this file lives here
│   ├── guides/                Diátaxis user docs
│   └── inspiration/           source documents the kit synthesizes
├── strategy/                  Phase 1 PM artifacts
│   ├── diagnoses/, wardley-maps/, intents/
├── discovery/                 Phase 2
│   ├── outcomes/, interviews/, snapshots/, opportunities/, trees/, research-digest/
├── validation/                Phase 3
│   ├── assumption-maps/, experiments/, learnings/
├── delivery/                  Phase 4
│   ├── visions/, initiatives/, specs/, handoff-packets/, release-notes/, landings/, retros/
├── communication/             cross-cutting
├── market/                    greenfield-mode competitor analysis
├── personal-os/               daily rhythm + scheduled agent identity files
├── plugins/                   shippable bundles, organized by phase
└── templates/                 frontmatter templates per ontology type
```

## Two structural distinctions

**Kit components vs PM artifacts.** Everything under `.claude/`, `tools/`, `scripts/`, `context/frameworks/`, `templates/`, `docs/` (except `docs/specs/` for the kit's own build) is the kit machinery itself. Everything under `strategy/`, `discovery/`, `validation/`, `delivery/`, `market/`, `communication/`, `personal-os/` is the PM artifacts the kit produces and audits. The work-loop and the spec/plan system operate on the *kit* side; the audits and handover contracts operate on the *PM* side.

**`docs/_templates/` vs `templates/` — two template stores.** Both exist, on purpose, for different audiences:
- **`docs/_templates/`** — scaffolding for *kit-internal* artifacts. Contains `spec.md`, `plan.md`, `state.json`, `adr.md`, `rfc.md`. Used by `tools/new-spec.sh` when scaffolding a new kit-component spec. A kit contributor building a new skill/agent/command reaches here.
- **`templates/`** — frontmatter starters for *PM-work* artifacts (per ontology type). A PM using the kit to draft an intent, OST, vision, etc. reaches here. Currently sparse (only `CLAUDE.global.md`); the per-type templates are planned per ROADMAP F3.

A new contributor adding a template should ask: is this for the kit (kit-build) or for a PM using the kit (PM-work)? Place accordingly.

**Directories shown reflect the target structure.** Several ship empty or partially populated; see [`docs/INVENTORY.md`](INVENTORY.md)'s `Status` column for what is currently built. Treat the tree above as the design surface, not a snapshot of the working state.

**Frozen vs living docs.** Charter, ADRs, shipped specs — frozen. CONVENTIONS, AGENTS.md, INVENTORY, PHASE-GUIDE, HANDOVERS, HUMAN-AI-OWNERSHIP, ROADMAP — living. RFCs — in flight until accepted, then frozen. The work-loop's CAPTURE phase requires updating the living docs in the same PR as any change that affects them; drift between living docs and reality is the most common cause of agent-quality decay.

## Where things get added

When you build:

| Adding a... | Goes to... | Linted by... |
|---|---|---|
| Slash command | `.claude/commands/<name>.md` | `tools/lint-command.sh` |
| Sub-agent | `.claude/agents/<name>.md` | `tools/lint-agent.sh` |
| Skill | `.claude/skills/<name>/SKILL.md` | `tools/lint-skill.sh` |
| Hook | `.claude/hooks/<name>.md` (doc) + `scripts/<name>.py` (script) | (project-specific) |
| Runtime utility | `scripts/<name>.{py,sh}` | (its own test suite) |
| Shared library | `scripts/lib/<name>.py` | (its own test suite) |
| Build tool | `tools/<name>.{py,sh}` | (its own test suite) |
| Reference framework | `context/frameworks/<name>.md` | `tools/lint-frontmatter.py` (light) |
| Template | `templates/<type>.md` | (manual review) |
| Spec | `docs/specs/<feature>/` | the spec template structure itself |
| ADR | `docs/adr/<NNNN>-<slug>.md` | (manual review) |
| RFC | `docs/rfc/<NNNN>-<slug>.md` | (manual review) |
| User guide | `docs/guides/{tutorials,how-to,reference,explanation}/` | (manual review) |

## The Charter / ADR / RFC / Spec hierarchy

```
                CHARTER (frozen one-page constitution)
                   ↓
         ┌─────────┼─────────┐
         ↓                   ↓
       ADRs                RFCs
   (frozen history)   (proposed changes)
                              ↓
                          accepted →
                              ↓
                            SPECS
                  (per-component contract + plan)
                              ↓
                       shipped components
                              ↓
                       update INVENTORY, AGENTS.md
                       check off in ROADMAP.md
```

The lower layers cite the upper layers; upper layers do not know about lower layers. That's the whole point of the hierarchy.
