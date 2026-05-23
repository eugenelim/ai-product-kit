---
description: Walk the typed graph outward from one PM Spec to surface upstream parents, downstream consumers, related concept surface, cross-team boundaries, and risk flags. Stdout-only report; writes nothing. Consumes scripts/lib/graph.py (F1.1) — does not reimplement traversal.
argument-hint: <spec-slug> [--from-initiative <initiative-slug>]
---

# /spec-impact-analysis

Answer the question every spec author hits after a non-trivial spec edit: *what changes if this spec changes?* Reads one PM Spec, walks the typed-object graph outward via `scripts/lib/graph.py`, and emits a structured impact report. No artifact write. No graph reimplementation.

This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply. (See "What this command will not do" for the deviation declaration.)

## When to run

- After editing a PM Spec at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` and before requesting handoff-packet generation
- During a cross-team review, to surface every team boundary this spec touches
- When a spec's risk level escalates and the owner needs to know what's downstream
- Before declaring a Handover 5 sound

## Inputs

1. Positional: `<spec-slug>` — kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. The slug of a spec file at `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md` (flat-file layout per `templates/initiative/child-specs.md` and `.claude/commands/draft-spec.md:36`).
2. Flag (optional): `--from-initiative <initiative-slug>` — disambiguates when the same `<spec-slug>` appears under multiple initiatives.
3. `scripts/lib/graph.py` (F1.1) — the typed-object graph walker. **The command consumes `graph.build(root)` and the `Graph.nodes`, `Graph.by_type()`, `Graph.parents_of()`, `Graph.children_of()`, `Graph.related_of()`, `Graph.walk_up()`, `Graph.walk_down()`, `Graph.cycles()`, `Graph.dangling_edges()` API. The command does NOT reimplement graph traversal.**
4. `scripts/lib/frontmatter.py` (F1.2) — the parser the graph walker uses internally; spec frontmatter is read through parsed graph nodes, not ad-hoc parsing.

## Procedure

### Step 1 — resolve the spec file

Validate the positional matches `^[a-z0-9-]+$`. If `--from-initiative` is given, compute the path directly as `delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md`. Otherwise, glob `delivery/initiatives/*/specs/<spec-slug>.md`. Zero matches → exit code 2 with `"spec file not found at delivery/initiatives/<initiative-slug>/specs/<spec-slug>.md"`. Multiple matches without `--from-initiative` → exit code 2 with `"ambiguous spec slug — pass --from-initiative <initiative-slug>"`.

### Step 2 — build the typed graph

Call `scripts.lib.graph.build(root)` (no scope filter at the build call — scoping happens by locating the spec node). Locate the spec node by matching `Node.path` against the resolved `.md` file path.

### Step 3 — walk upward, downward, sideways; detect cross-team and risks

- **Upstream:** `graph.walk_up(spec_node)` over `parent_*` edges (`parent_initiative` → `parent_vision` → `parent_learning` → `parent_opportunity` → `parent_intent`).
- **Downstream:** `graph.walk_down(spec_node)` over reverse `parent_*` edges. (Sparse today: the F1 graph does not yet model spec→spec dependencies; the report states this when the list is empty.)
- **Related concept surface:** `graph.related_of(spec_node)` for each of `related_problems`, `related_personas`, `related_kpis`, `related_capabilities`.
- **Cross-team boundaries:** read the parent initiative's README `crosses_teams:` list; flag any sibling spec whose owning team is in that list and differs from this spec's owning team.
- **Risk flags:** count high-risk Requirement nodes (`risk_level: High | Critical`) linked to this spec's Capabilities; check `graph.cycles()` membership; list `graph.dangling_edges()` from this subtree; list orphan ancestors.

### Step 4 — emit the report

Print the three labelled header lines first, in this exact order, contiguous (no blank lines between):

```
PHASE: Delivery → Spec impact assessment for <spec-slug>
VERDICT: contained | cross-team | high-risk | broken-links
NEXT: <one-line recommended human action>
```

Verdict precedence (the headline names exactly one label; the body still lists every detected signal):

1. `broken-links` — any dangling `parent_*` or `related_*` edge from this spec or any walk_up ancestor, OR any orphan ancestor.
2. `high-risk` — ≥1 linked Requirement with `risk_level: High | Critical`, OR this node sits inside a `graph.cycles()` SCC.
3. `cross-team` — at least one detected cross-team boundary.
4. `contained` — none of the above.

Then a single blank line, then the body sections:

```
## Upstream parents
| object_type | slug | path |

## Downstream consumers
| object_type | slug | path |

## Related concept surface
| kind | target_id | target_object_type | path |

## Cross-team boundaries
| boundary | owning_team_here | owning_team_other |

## Risk flags
- <one bullet per detected risk>
```

Exit code 0.

## Exit codes

- `0` — spec located; report emitted.
- `1` — internal error (graph build failed; uncaught exception). Stderr carries details.
- `2` — pre-conditions failed: spec file not found at the resolved path; ambiguous match without `--from-initiative`; spec file's frontmatter missing or malformed; positional fails `^[a-z0-9-]+$`.
- `3` — RESERVED. Not used by this analyst-graph-traversal shape (this command writes no artifact, so the F4 convention's exit-3 case is unreachable here).

## What this command will not do

- **This command is not a template-fill command; the docs/CONVENTIONS.md §Phase-4 Template-Fill Commands convention does not apply.** The skeleton's Steps 2–6 (template instantiation; H2 placeholder walk; `human_owned_decisions` confirmation; written-artifact lint; new-slug chain-hint) do not run here.
- Never write any artifact. No `delivery/`, no `docs/audits/`, no temp file. Stdout only.
- Never mutate any spec or initiative file (no frontmatter updates, no `last_updated:` bumps, no sibling-file writes).
- Never reimplement graph traversal — call `scripts.lib.graph` exclusively. The F1.1 contract owns traversal semantics.
- Never automatically generate a handoff packet. A `cross-team` verdict signals the human to consider `/handoff-packet`; the command does not chain into it.
- Never fabricate downstream consumers. If the F1 graph doesn't model spec→spec dependencies for a given edge, the section lists "(none — F1 graph models parent_*/related_* edges only)" rather than inventing edges.
- Never batch clarifying questions. The command is non-interactive at runtime.

$ARGUMENTS
