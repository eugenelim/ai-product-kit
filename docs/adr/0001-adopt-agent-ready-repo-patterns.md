# 0001 — Adopt agent-ready-repo patterns for kit structure

* Status: accepted
* Deciders: kit author
* Date: 2026-05-20
* Supersedes: none

## Context and Problem Statement

v2 of the kit organized PM work around four phases (Strategy → Discovery → Validation → Delivery) plus a Landings phase, with handover artifacts at each boundary and a Torres-derived Claude Code mechanics layer (markdown memory, slash commands, agents, skills, hooks).

Two structural problems remained:

1. **No canonical agent-context file at the repo root.** v2 used a project-scoped `.claude/CLAUDE.md` only. This works for Claude Code but not for the other agent tools (Cursor, Codex, Gemini CLI, Copilot) that look for an `AGENTS.md` at the root via their own discovery rules. Cross-tool portability was implicit, not designed.

2. **No "source of truth" discipline.** v2 had folders for every phase but no top-level table answering "for question X, where does the answer live?". Adopters working in the kit had to learn its geography by exploration. Worse, when an answer didn't exist anywhere, the kit didn't say so — Claude (and humans) silently guessed.

3. **No lifecycle-aware doc taxonomy.** v2 mixed mission documents, decision records, proposals, and how-tos in the same folders. Charter-level statements (frozen) sat next to operational notes (living). When a convention changed, it was unclear whether the change should freeze (ADR) or remain editable (RFC).

4. **No engineering work-loop generalized for PM work.** v2 had skeptic agents and audit commands but no overarching pattern that ordered them: plan → execute → verify → review.

The agent-ready-repo template solves these for engineering repos. The question: are its patterns useful for a pre-engineering PM kit, and if so, which ones?

## Decision Drivers

- **Cross-tool portability.** The kit shouldn't lock to Claude Code. Other agent tools should be first-class.
- **Discoverability for new adopters.** A team joining the kit should be able to answer "where does X live?" in under a minute.
- **Frozen vs living distinction.** Decisions taken should be append-only; proposals in flight should be editable.
- **Symmetry with engineering downstream.** The PM kit hands off to engineering teams that may themselves use agent-ready-repo. Symmetry across the handoff is valuable.
- **Discipline against drift.** A clear "when this file is wrong" protocol prevents silent decay of agent-context files.

## Considered Options

### Option A — Keep v2 structure unchanged

Pro: zero migration cost. Con: doesn't solve any of the four problems. Cross-tool portability stays implicit; doc taxonomy stays flat; no work-loop discipline.

### Option B — Adopt agent-ready-repo wholesale

Pro: complete pattern, well-tested. Con: agent-ready-repo is built for engineering — has `apps/`, `packages/`, `tools/` folders that don't apply; assumes specs/plans live in repos; the work-loop is implementation-flavored. Forcing the kit into that shape would obscure the phase model.

### Option C — Adopt selectively: structural patterns yes, engineering-specific content no

Pro: keeps the phase model as the spine; adds the patterns that translate; avoids importing engineering-flavored content. Con: requires care to keep the adopted patterns coherent rather than mashed in.

### Option D — Build kit-specific equivalents from first principles

Pro: maximum fit. Con: reinvents wheels; loses the cross-tool standardization that AGENTS.md provides.

## Decision Outcome

**Option C — selective adoption.**

### What gets adopted

1. **`AGENTS.md` as canonical agent-context file** at the repo root. `CLAUDE.md` is a symlink (confirmed in the kit's reconcile-and-harden pass, 2026-05-21 — `readlink CLAUDE.md` returns `AGENTS.md`). Kept under ~250 lines; points at deeper docs.

2. **"Source of truth" table** as the centerpiece of AGENTS.md. Every kind of decision has exactly one place it lives, with the explicit rule: *if you can't find the answer in one of these places, the answer doesn't exist yet — ask, or open an RFC. Don't guess.*

3. **Lifecycle-aware doc taxonomy:**
   - `docs/CHARTER.md` — mission, scope, principles (frozen; substantive changes via RFC)
   - `docs/CONVENTIONS.md` — how work happens, including the universal metadata schema (living)
   - `docs/adr/` — Architecture Decision Records (frozen, append-only, supersession protocol). **Caveat: while the kit is being stood up (v0.x), inline ADR edits are permitted to fix drift surfaced by the reconcile-and-harden work-loop. The frozen/append-only discipline reactivates once the kit ships v1.**
   - `docs/rfc/` — Requests for Comments (living during review; locked when accepted)
   - `docs/guides/` — user-facing docs in Diátaxis form
   - `docs/inspiration/` — source documents the kit synthesizes

4. **Plan → Execute → Verify → Review work-loop** as a kit skill (`.claude/skills/work-loop/`). Reshaped for pre-engineering PM work: verification modes are audit-driven / repair-loop / human-review / threshold-check rather than TDD / goal-based / visual.

5. **Specialist reviewer subagents** with sharp, differentiable lenses:
   - `adversarial-reviewer` (default; artifact-vs-contract drift) — **shipped**
   - `compliance-reviewer` (regulatory, legal, privacy, ethics) — *planned (ROADMAP P6.1)*
   - `quality-engineer` (testability, observability of the eventual implementation — for specs and handoff packets) — **shipped**

6. **"When this file is wrong, flag drift" protocol** in AGENTS.md and CONVENTIONS.md. Reality-vs-doc drift is named as the biggest cause of agent-quality decay; the kit treats fixing it as part of every session. The reconcile-and-harden pass (`docs/specs/reconcile-existing-components/`) is the operational backstop for when drift accumulates faster than per-session flagging catches it.

7. **Conventional commits** and the per-scope organization that mirrors phase folders.

### What's explicitly not adopted

- The engineering folder shape (`apps/`, `packages/`, `tools/`) — not applicable to a PM kit. `tools/` is repurposed for the build harness.
- TDD-flavored verification as the primary mode — replaced with the four PM-applicable verification modes (audit-driven / repair-loop / human-review / threshold-check). TDD remains available for kit-build scripts under `scripts/` and `tools/` where compressible invariants exist.
- The Ralph harness for unattended runs — the kit's scheduled team-of-agents (ROADMAP P9.6, planned) is the intended substitute, modeled on Torres's daily-rhythm pattern. The substitute is not yet built; the rejection of Ralph is therefore conditional on P9.6 shipping.
- The `docs/specs/` engineering-spec convention — the kit's `delivery/specs/` is the PM equivalent and lives outside `docs/`. `docs/specs/` IS used by the kit's own build process for kit-component specs (see `reconcile-existing-components/` for the first worked example).
- The PR-template + CODEOWNERS protocol — out of scope for a single-author kit at v0.x; will be reconsidered if the kit becomes multi-contributor.

### Consequences

**Positive:**
- Cross-tool portable: any agent tool that reads AGENTS.md can use the kit
- New adopters orient via the source-of-truth table in 60 seconds
- Decisions are recorded with rationale and traceable over time (ADRs)
- Kit changes follow a known governance pattern (RFCs)
- The work-loop gives a single repeatable shape to all non-trivial PM work
- Specialist reviewers add a review layer the kit was missing

**Negative / accepted tradeoffs:**
- Kit complexity is higher; the AGENTS.md + CHARTER + CONVENTIONS + HUMAN-AI-OWNERSHIP + HANDOVERS + PHASE-GUIDE + INVENTORY split is more documents to maintain. Mitigation: the reconcile-and-harden work-loop catches drift between them.
- ADRs and RFCs add ceremony; for a single-user kit this may feel heavy. Acceptable because the kit is intended to be shared and adopted across teams.
- Symlink from `CLAUDE.md` to `AGENTS.md` requires filesystem support; on Windows or restricted environments, the two files may need to be identical copies, with drift risk. AGENTS.md line 3 documents the fallback.
- Two of three specialist reviewers are not yet shipped (`compliance-reviewer` P6.1, `quality-engineer` P6.2). Until they ship, the specialist-review layer is partial — only adversarial review is automated; compliance and quality engineering judgment remains manual. The ADR commits to building both; the consequence is that the kit's review backstop is currently 1/3 of intent.
- Cross-tool portability is by design intent. Not yet verified empirically across Cursor / Codex / Gemini CLI / Copilot — the claim is that those tools *will* discover AGENTS.md via their own rules, not that the kit has been tested with each. Treat as an open assumption pending a cross-tool smoke test.

**Neutral:**
- Migration from v2 is non-trivial but mechanical: existing v2 folders fit under the v3 phase structure unchanged; the changes are additive (AGENTS.md, CHARTER, CONVENTIONS, ADRs, RFCs) rather than restructuring

## Alternatives Considered (in detail)

### Option A — Keep v2 structure unchanged (rejected)

**Failure on cross-tool portability:** v2 ships only `.claude/CLAUDE.md`. Cursor, Codex, Gemini CLI, and Copilot have their own discovery rules that look at the repo root. v2 forces every non-Claude-Code tool to read project-scoped files via custom configuration. The kit's ambition is cross-tool portability; A forecloses it.

**Failure on discoverability:** v2 has no source-of-truth table. A new adopter looking for "where does the strategy intent live?" has to grep the tree or read the README's prose. The Charter+ADR+RFC distinction also doesn't exist — every document is treated as living, so frozen decisions can be silently re-litigated.

**Failure on work-loop discipline:** v2 has audit commands but no overarching pattern. An agent operating on a vision artifact has no single instruction to "plan → execute → verify → review" — instead it has to assemble that from scattered hook documentation. This is the most consequential failure: most kit-build failures the reconcile-and-harden pass surfaced would have been caught earlier had the work-loop been the standard pattern from day one.

### Option B — Adopt agent-ready-repo wholesale (rejected)

**Failure on folder shape:** agent-ready-repo's `apps/`, `packages/`, and `tools/` folder structure assumes a code repo. Forcing the kit into that shape would either (a) leave `apps/` and `packages/` empty (cosmetic clutter), or (b) shoehorn PM artifacts into those folders against their intent. Either way the kit's phase structure (`strategy/`, `discovery/`, etc.) loses primacy as the spine.

**Failure on verification mode:** agent-ready-repo's primary verification mode is TDD. PM artifacts don't have unit tests in the same sense; they have audit-pass checks, repair loops, human-review sign-offs, and threshold-comparison gates. Forcing TDD framing on a learning memo or strategic intent would either trivialize the verification or block it entirely.

**Failure on spec/plan location:** agent-ready-repo's `docs/specs/` is for engineering features. The kit needs `docs/specs/` for kit-build artifacts AND `delivery/specs/` for PM-work artifacts. Wholesale adoption conflates the two.

### Option D — Build kit-specific equivalents from first principles (rejected)

**Failure on standardization:** rebuilding the AGENTS.md pattern from scratch produces something slightly different from what the wider agent-tool ecosystem reads, losing the cross-tool portability that adoption preserves. Cursor and Codex docs explicitly cite AGENTS.md by name; a kit-specific equivalent would not benefit from that.

**Failure on rework cost:** the source-of-truth table, the Charter/ADR/RFC structure, the work-loop, and the specialist-reviewer pattern are non-trivial design artifacts. Reinventing them produces months of work for marginal differentiation.

### Option C wins because

The three rejected options each fail on at least one of the four decision drivers (cross-tool portability, discoverability, frozen-vs-living distinction, work-loop discipline). Option C accepts the cost of "selective adoption requires care" because the resulting kit retains: (a) the spine of the phase model, (b) the cross-tool portability from agent-ready-repo, (c) the discipline of the work-loop, and (d) the symmetry with engineering repos downstream that may also use agent-ready-repo. The "care" requirement is met by the reconcile-and-harden work-loop pattern, which is itself the application of agent-ready-repo's discipline to the kit's own contents.

## Links

* parent_intent: — (this is a kit-architecture decision, not a product-strategy decision)
* affected_artifacts: AGENTS.md, README.md, docs/CHARTER.md, docs/CONVENTIONS.md, docs/HUMAN-AI-OWNERSHIP.md, docs/INVENTORY.md, .claude/skills/work-loop/, .claude/agents/adversarial-reviewer.md
* superseded_by: —
* references:
  * the agent-ready-repo template (AGENTS.md pattern, source-of-truth table, work-loop)
  * `docs/inspiration/product_business_knowledge_ontology_agent_handoff.md` (the parallel adoption of the ontology — see ADR 0002)
