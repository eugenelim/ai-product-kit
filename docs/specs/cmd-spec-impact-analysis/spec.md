# Spec: cmd-spec-impact-analysis

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** command
- **Serves kit phase:** Delivery (Phase-4 spec-impact analysis)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md` (the build pattern this worker follows); `scripts/lib/graph.py` (F1.1 — the typed-object-graph walker this command consumes; this command does NOT reimplement traversal); `scripts/lib/frontmatter.py` (the frontmatter parser the graph walker uses); `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" (source-of-truth for Spec required frontmatter, the `parent_initiative:` and the initiative-README `crosses_teams:` list); `tools/lint-command.sh` (the per-command shape linter this command file must pass); `.claude/commands/_meta/command-skeleton.md` (NOTE: this skeleton is for template-fill commands; this command intentionally deviates from skeleton Steps 2–4 — declared in §"Body-shape contract"); `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands" (does NOT apply — this command is not a template-fill command; stated explicitly in §"Boundaries → Always do"); `.claude/commands/phase-guide.md` (analytical-command output-shape precedent — three labelled lines `PHASE: / VERDICT: / NEXT:`); `.claude/commands/audit-traceability.md` (F1-style audit precedent for report-section shape); `ROADMAP.md` P4.9.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Defines the literal `.claude/commands/spec-impact-analysis.md` slash command — a Phase-4 *analytical, read-only* worker that takes a `<spec-slug>` (optionally disambiguated by `--from-initiative <initiative-slug>`), locates the spec file at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`, builds the typed-object graph via `scripts.lib.graph.build(root)`, walks upward (`parent_*` ancestors), downward (children referencing this spec), and sideways (`related_*` shared-concept surface), detects cross-team boundaries from the parent initiative's `crosses_teams:` list, surfaces risk flags (orphan ancestors, dangling edges, high-risk Requirement count, cycle membership), and emits a structured stdout report. The command writes NO artifact and mutates NO file. Verification is goal-based — the command file passes `tools/lint-command.sh`, and a manual gesture against a fixture spec exits 0 with the documented report shape on stdout. **This command is not a template-fill command; the `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands" convention does not apply.**

## Objective

Ship `.claude/commands/spec-impact-analysis.md` — a single slash-command file (≤ 120 body lines) that answers one question for the Spec author and the Initiative owner: *what changes if this spec changes?* It reads one spec folder, consumes the typed-object graph that F1.1 already provides, walks upward to parent Initiative / Vision / Learning / Opportunity / Intent, downward to any artifacts that declare this spec as their parent, sideways across the `related_*` shared-concept surface, detects cross-team boundary signals against the parent initiative's `crosses_teams:` list, surfaces risk flags, and emits a verdict-headed report on stdout. The command is **analytical**: it never writes to disk, never instantiates a template, never asks the human to fill placeholders. Output goes to stdout; exit codes signal the four Phase-4-convention outcomes (0 success, 1 internal error, 2 pre-conditions failed, 3 reserved).

The component does not yet exist. `.claude/commands/spec-impact-analysis.md` is absent today. F1.1 (`scripts/lib/graph.py`) shipped earlier in the kit's foundation phase and exposes the traversal API this command consumes; no new graph code is needed.

## Why now

ROADMAP P4.9 `/spec-impact-analysis` lands in the Wave-3 Phase-4 batch alongside P4.2 `/vision-shape-check` and P4.10 `/audit-spec-linkage`. The three are analytical/auditing siblings (no artifact writes), and the kit's spec inventory has grown enough that a Spec author committing a change can no longer hold the impact surface in their head. The cost of authoring this command now: one focused work-loop, on top of an already-shipped traversal library (F1.1). The cost of deferring it: every Spec change forces the author to re-derive parent / related / cross-team impact by hand, which silently misses cross-team boundary signals — exactly the kind of drift the kit's traceability rules exist to prevent.

This command also locks the Wave-3 family verdict-header shape (`PHASE: ... / VERDICT: ... / NEXT: ...`, labels in ALL CAPS, `:` followed by a space) verbatim. P4.2 and P4.10 follow the same shape; the cross-cutting reviewer checks coherence across the three.

## Inputs and outputs

**Inputs.**

- **Positional 1 (required):** `<spec-slug>` — kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. The slug of a spec file at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` (flat-file layout per `templates/initiative/child-specs.md` and `.claude/commands/draft-spec.md:36`).
- **Flag (optional):** `--from-initiative <initiative-slug>` — disambiguates when the same `<spec-slug>` appears under multiple initiatives.
- **Filesystem:** the working tree's `delivery/initiatives/*/specs/<spec-slug>.md` glob. Discovery rule: if `--from-initiative` is given, the candidate path is computed directly as `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`; otherwise the command globs `delivery/initiatives/*/specs/<spec-slug>.md`. Zero matches → exit code 2 with "spec file not found at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`". Multiple matches without `--from-initiative` → exit code 2 with "ambiguous; pass --from-initiative".
- **`scripts/lib/graph.py`** — the F1.1 typed-object-graph walker. The command consumes `graph.build(root)`, then uses `Graph.nodes`, `Graph.by_type()`, `Graph.parents_of()`, `Graph.children_of()`, `Graph.related_of()`, `Graph.walk_up()`, `Graph.walk_down()`, `Graph.cycles()`, `Graph.dangling_edges()`. The command does NOT reimplement traversal; this is load-bearing.
- **`scripts/lib/frontmatter.py`** — the frontmatter parser the graph walker uses internally. The command reads the spec's frontmatter (and the parent initiative's README frontmatter for `crosses_teams:`) through the parsed graph nodes, not through ad-hoc parsing.
- **`docs/HANDOVERS.md` §"Handover 5: Initiative → Spec"** — the source-of-truth for the parent-initiative `crosses_teams:` list, which feeds the cross-team-boundary detection.
- **The spec's own frontmatter** — `parent_initiative:`, `parent_vision:`, plus any optional `related_*` edges. (Note: in the flat-file spec layout, there is no per-spec folder for sibling `requirements.yaml`; high-risk Requirement detection falls back to typed `Requirement` nodes anywhere in the graph whose `related_capabilities:` or other linkage ties them to this spec's Capabilities. Sparse today; see Open Questions.)
- **`tools/lint-command.sh`** — the per-command shape linter that gates this command file at build time.

**Outputs.**

1. `.claude/commands/spec-impact-analysis.md` — the new slash-command file. Frontmatter: `description:` (≤ 1024 chars; one sentence) and `argument-hint: <spec-slug> [--from-initiative <initiative-slug>]`. Body shape declared in §"Body-shape contract" below.
2. **Stdout report (the runtime output of the command itself).** No file write. Shape:

   The three-line header (printed first, contiguous, no blank lines between the labelled lines):

   ```
   PHASE: Delivery → Spec impact assessment for <spec-slug>
   VERDICT: contained | cross-team | high-risk | broken-links
   NEXT: <one-line recommended human action>
   ```

   Then a single blank line as separator, then the report body:

   ```
   ## Upstream parents
   | object_type | slug | path |
   | ...

   ## Downstream consumers
   | object_type | slug | path |
   | ...

   ## Related concept surface
   | kind | target_id | target_object_type | path |
   | ...

   ## Cross-team boundaries
   | boundary | owning_team_here | owning_team_other |
   | ...

   ## Risk flags
   - <one bullet per detected risk>
   ```

   The three labelled header lines use ALL-CAPS labels followed by `:` and a single space. This three-line header shape is shared verbatim with the Wave-3 siblings P4.2 and P4.10. The blank line between header and body is a separator, not a fourth header line.

3. **Exit codes** (mirror the Phase-4 convention's four-code semantics for kit consistency):
   - `0` — spec located; report emitted.
   - `1` — internal error (graph build failed; uncaught exception). Surface details on stderr.
   - `2` — pre-conditions failed: spec file not found at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`; ambiguous match without `--from-initiative`; spec file's frontmatter is missing or malformed; positional fails `^[a-z0-9-]+$`.
   - `3` — RESERVED (declared explicitly so the four-code surface is stable across Wave-3).

**Verdict precedence (when multiple signals apply).** The VERDICT line names the dominant signal. Precedence, from highest priority to lowest:

1. `broken-links` — any dangling `parent_*` or `related_*` edge from this spec or any of its `walk_up` ancestors, OR any orphan ancestor (`target_exists == False`).
2. `high-risk` — this spec's `requirements.yaml` (or sibling Requirement nodes) contains ≥ 1 Requirement with `risk_level: High | Critical`, OR this node sits inside a `graph.cycles()` SCC.
3. `cross-team` — at least one detected cross-team boundary (sibling spec whose owning context's team is in the parent initiative's `crosses_teams:` and differs from this spec's owning team).
4. `contained` — none of the above. The default-clean verdict.

The VERDICT line names exactly one label; the dominant signal wins. The body sections still list every detected signal — precedence only governs the headline.

## Body-shape contract

The command body intentionally deviates from `.claude/commands/_meta/command-skeleton.md` Steps 2–4 (template-instantiation, interactive H2-walk, human_owned_decisions confirmation). This command is **not a template-fill command**; the `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands" convention does NOT apply. Declared verbatim in §"Boundaries → Always do" below.

The body H2 structure is:

- `## When to run` — triggers (after editing a spec; before requesting handoff-packet generation; during a cross-team review).
- `## Inputs` — the positional, the optional flag, the consumed library API surface.
- `## Procedure` — four H3 Steps:
  - **Step 1 — resolve the spec file.** Validate positional matches `^[a-z0-9-]+$`. If `--from-initiative` is given, compute path as `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`; else glob `delivery/initiatives/*/specs/<spec-slug>.md`. Zero matches or ambiguous → exit 2 with remediation.
  - **Step 2 — build the typed graph.** Call `scripts.lib.graph.build(root)` (no scope filter at the build call — the command does the scoping in Step 3 by locating the spec node). Locate the spec node by matching `Node.path` against the resolved `.md` file path.
  - **Step 3 — walk upward, downward, sideways; detect cross-team and risks.** Upstream via `walk_up` (parent_*); downstream via `walk_down` / `children_of` (parents-of-others pointing here); sideways via `related_of` for each of `related_problems`, `related_personas`, `related_kpis`, `related_capabilities`. Cross-team: read the parent initiative's README `crosses_teams:` list and flag any sibling spec whose owning team is in that list and differs from this spec's owning team. Risks: count high-risk Requirements, check `graph.cycles()` membership, list dangling-edges from this subtree, list orphan ancestors.
  - **Step 4 — emit the report.** Print the three labelled header lines, then the five H2 sections in order. No artifact write.
- `## What this command will not do` — the never-do list (no artifact write, no graph reimplementation, no human-fill, no automatic handoff-packet generation).

The H1 is exactly `# /spec-impact-analysis`.

## Boundaries

### Always do

- **ALWAYS consume `scripts.lib.graph` and `scripts.lib.frontmatter`; never reimplement typed-graph traversal in this command.** F1.1 owns the traversal contract; this command is a thin analytical caller.
- **ALWAYS declare verbatim in this command's body that this command is not a template-fill command; the `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands" convention does not apply.** The Wave-3 reviewer checks for this phrase.
- **ALWAYS emit the three labelled header lines first (`PHASE: ... / VERDICT: ... / NEXT: ...`), in that order, with ALL-CAPS labels followed by `:` and a single space.**
- **ALWAYS exit with one of {0, 1, 2}; reserve 3.**

### Ask first

- Whether to surface a `cross-team` verdict when the spec is itself the cross-team boundary owner (rare edge case; default behavior is to flag it, but if the cross-team is intentional and signed off, the verdict should still report it — the human decides what to do, not the command).

### Never do

- **NEVER write any artifact.** No `delivery/`, no `docs/audits/`, no anywhere. Stdout only.
- **NEVER mutate any spec or initiative file** (no frontmatter updates, no `last_updated:` bumps, no sibling-file writes).
- **NEVER reimplement graph traversal** — call `scripts.lib.graph` exclusively.
- **NEVER automatically generate a handoff packet** — that is `/handoff-packet`'s job; this command only signals when a spec's impact surface warrants one.
- **NEVER fabricate downstream consumers** — if the F1 graph doesn't yet model spec→spec dependencies, state that explicitly under §"Open questions" and surface as a "downstream consumers" empty list with a note, rather than inventing edges.

## Verification mode

**Goal-based check, plus a manual gesture.**

- **Goal-based check:** `tools/lint-command.sh .claude/commands/spec-impact-analysis.md` exits 0. This validates frontmatter shape (description ≤ 1024 chars), H1 format (`# /spec-impact-analysis`), and presence of `## When to run` or `## Procedure`.
- **Manual gesture:** run the command (interactively, in a Claude Code session) against an existing spec in this kit (e.g., `spec-impact-analysis cmd-draft-vision --from-initiative <known-initiative-or-omit-if-unambiguous>`). Confirm the three labelled header lines appear, the five H2 sections appear in order, the upstream parents list is non-empty (every kit spec has a parent_initiative), and the verdict is one of the four documented labels.

No TDD — the command is a markdown file that orchestrates an existing Python library; there is no per-command Python code in this spec.
No audit-driven — this command is itself an analyst, not a kit-wide gate.

## Contract tests

T1 — `tools/lint-command.sh .claude/commands/spec-impact-analysis.md` exits 0.

T2 — The command body contains exactly the H2 sections `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`, in that order.

T3 — The command body H1 is exactly `# /spec-impact-analysis` on its own line.

T4 — The command frontmatter `description:` field is ≤ 1024 characters.

T5 — The command body contains the verbatim sentence: "This command is not a template-fill command; the `docs/CONVENTIONS.md` §Phase-4 Template-Fill Commands convention does not apply." (or its dashed-section-symbol variant — see §"Open questions"). This locks the F4-deviation declaration.

T6 — The command body declares the verdict-header shape verbatim — specifically the three labelled lines beginning `PHASE:`, `VERDICT:`, `NEXT:` (each with ALL-CAPS label, `:`, single space), AND lists the four verdict labels (`contained`, `cross-team`, `high-risk`, `broken-links`) AND the precedence order.

T7 — The command body cites `scripts/lib/graph.py` (or the import path `scripts.lib.graph`) as the consumed traversal API, AND explicitly states that this command does not reimplement traversal.

All seven tests are reproducible manually (T1 via `tools/lint-command.sh`; T2–T7 via `grep` against the command file). They become candidates for promotion into `scripts/tests/test_phase4_command_shape.py` after the command ships, but that promotion is not part of this spec.

## Non-goals

- **No artifact write.** The command produces no file on disk. Reports are stdout-only.
- **No graph-traversal reimplementation.** Every traversal call goes through `scripts.lib.graph`.
- **No automatic handoff-packet generation.** A `cross-team` verdict signals the human to consider `/handoff-packet`; the command does not chain into it.
- **No spec→spec dependency modeling.** The F1 graph models `parent_*` and `related_*` edges, not arbitrary spec-to-spec dependencies; this command honors that limit and does not invent edges. Surfaced as an Open Question.
- **No cross-initiative analytics.** The command analyses one spec at a time. Initiative-wide rollup is `/audit-spec-linkage`'s job (P4.10), not this command's.
- **No EARS-pattern check on Requirements.** That is `ears-lint`'s job (P4.7); high-risk count is the only Requirement-attribute this command reads.

## Open questions

- **Spec→spec dependencies not modeled in the F1 graph.** If a Spec A explicitly depends on Spec B (e.g., shared schema, shared capability rollout sequence), the F1 graph today has no `depends_on:` edge type. The downstream consumers section will therefore be sparse for most specs. **Who can answer:** the F1 maintainer + the kit author, at next ROADMAP review. **Decision needed:** whether to extend `RELATED_FIELDS` (or introduce a new edge kind) to capture spec-dependency. **Until decided:** the command states this limit in the report when downstream consumers is empty.
- **Section-symbol vs dashed-section in the F4-deviation declaration sentence.** The test T5 accepts both `§"Phase-4 Template-Fill Commands"` and a dashed variant. Decide on canonical form at first cross-cutting review.
- **Cross-team detection when the spec's owning context's team isn't declared.** If `delivery/initiatives/<init>/context-map.md` doesn't enumerate the owning team for this spec's bounded context, cross-team detection falls back to "unknown — flag as Open Question in the report." Decision needed at first manual gesture: should this raise a verdict signal, or stay silent?
- **Behavior when the parent initiative's README has no `crosses_teams:` field at all.** Treat as "single-team initiative; no cross-team boundaries possible" — i.e., a quiet pass on the cross-team check. Confirm at first manual gesture.

## Acceptance criteria

- [ ] `.claude/commands/spec-impact-analysis.md` exists.
- [ ] `tools/lint-command.sh .claude/commands/spec-impact-analysis.md` exits 0.
- [ ] All seven contract tests T1–T7 pass via manual reproduction (grep + linter).
- [ ] The command body cites `scripts/lib/graph.py` and `scripts/lib/frontmatter.py` as the consumed APIs and explicitly states no reimplementation.
- [ ] The command body declares the F4-deviation declaration sentence verbatim (per T5).
- [ ] The command body declares the verdict-header shape and the four verdict labels with precedence (per T6).
- [ ] A manual gesture against an existing in-kit spec produces the documented stdout report shape and exits with code 0.
- [ ] The command produces NO file write under any code path (no Write, no Edit, no append).
- [ ] `state.json.plan_review_status` flipped to `approved` before EXECUTE.
- [ ] Spec status set to `Approved` (and later `Shipped: <date>` post-CAPTURE — supervisor handles).

## Cross-references

- **Consumed by:** the human Spec author after editing a spec; the Initiative owner during a cross-team review; (later, optionally) the `/handoff-packet` command as a pre-check.
- **Consumes:** `scripts.lib.graph` (F1.1); `scripts.lib.frontmatter`; `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" (read at runtime indirectly via the parent initiative's parsed frontmatter); `tools/lint-command.sh` (at build time).
- **Frontmatter fields read:** `parent_initiative`, `parent_vision`, `parent_learning`, `parent_opportunity`, `parent_intent` (the `walk_up` chain); `related_problems`, `related_personas`, `related_kpis`, `related_capabilities` (the related surface); `risk_level` (on sibling Requirement nodes); `crosses_teams` (on the parent initiative's README); `owning_team` and/or `owning_context` (on this spec, when present).
- **Frontmatter fields written:** none.
- **Ontology object types touched:** Spec, Initiative, Vision, Learning Memo, Opportunity (OST opportunity node), Strategic Intent, Requirement, Capability, Problem, Persona, KPI.
