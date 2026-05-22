# Context map

This file is the bounded-contexts narrative for the Initiative. The four required per-bounded-context fields (owner, public contract, commodity-vs-custom Wardley evaluation, evolution stage) are sourced from `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" → §"Required content" item 1.

<!-- HANDOVERS-5's folder-contents description mentions "shared shapes" in addition to the four fields below. §"Required content" item 1 (the normative list) does NOT include "shared shapes"; this template treats item 1 as the binding contract and absorbs the shared-shape concern into the **Public contract:** field of each H3 block. If HANDOVERS-5 promotes "shared shapes" to a first-class field, this template adds a fifth labeled body line at that point. -->

## Bounded contexts in this initiative <!-- source: inferred (folder-index orientation); per-bounded-context fields below are HANDOVERS-5 §"Required content" item 1 -->

<One paragraph: what "bounded context" means for this Initiative; which contexts are in scope; which are explicitly out. A future kit-wide bounded-context vocabulary doc will be linked here when it ships (tracked under ROADMAP P4.4).>

## Per-bounded-context detail <!-- source: HANDOVERS-5 §"Required content" item 1 -->

<One paragraph introducing the repeated H3 sub-template below. Each bounded context the Initiative crosses gets one H3 block.>

### <Bounded context name>

**Owner:** <named human or team>

**Public contract:** <one-sentence summary of the boundary contract — the API, event schema, or shared shape that other contexts depend on>

**Commodity vs custom (Wardley):** <commodity | utility | product | custom>

**Evolution stage:** <genesis | custom | product | commodity>

> Duplicate the H3 block above for each bounded context in the initiative.
