---
name: opportunity-clustering
description: Themes a list of raw opportunity candidates (one-line statements, each optionally carrying an `evidence_basis:` link) into a small number of clusters grouped by one of three named rules — shared customer behavior, shared workflow step, or shared workaround pattern. Each cluster carries a name, the named rule that anchors it, the member candidate ids, and a one-line rationale; candidates that don't fit any rule land in an `unclustered:` bucket rather than getting forced into a cluster. The skill consumes `context/frameworks/opportunity-solution-tree.md` as canon — it does not redefine what an Opportunity is. Output is a proposal — the skill never persists and never auto-promotes a cluster to an OST Opportunity (that's the downstream `/cluster-opportunities` command's job, gated by human acceptance). Dispatch typically inside `/cluster-opportunities` (planned — P2.6) after `/extract-opportunities` (planned — P2.4) has produced the candidate list.
license: MIT
---

# opportunity-clustering

This skill takes a list of raw opportunity candidates and proposes a thematic grouping of them into a small number of clusters. The three thematic rules — shared customer behavior, shared workflow step, shared workaround pattern — are the only anchors the skill recognizes; candidates that don't fit any of the three land in an `unclustered:` bucket rather than getting forced into a cluster to make the output look tidier.

The framework `context/frameworks/opportunity-solution-tree.md` owns the definition of an Opportunity. This skill consumes that definition; it does not redefine it. A "candidate Opportunity" here is a statement that *plausibly* names a customer pain, desire, or aspiration; the skill clusters candidates by theme but does not adjudicate whether each candidate is truly an Opportunity (that's a human decision downstream, gated by `evidence_basis:` per the framework's "Source opportunities" discipline).

## When to use this skill

- A `/extract-opportunities` invocation has just produced a list of raw candidate Opportunities from a batch of interview snapshots, and the list is long enough (≥ 6 candidates) that thematic synthesis is more useful than reading top-to-bottom.
- A team is staring at a parking-lot file of Opportunity candidates accumulated over weeks of interviews and wants to see what themes have built up.
- A `/cluster-opportunities` invocation needs the thematic-grouping transformation step.

## Invocation contract

**Input.** A list of raw opportunity candidates. Each candidate is one line plus optional `evidence_basis:` link:

```yaml
candidates:
  - id: OPP-CAND-001
    statement: "Analysts redo the same join logic across notebooks because they can't share saved fragments."
    evidence_basis: [IS-001, IS-014]
  - id: OPP-CAND-002
    statement: "Analysts re-derive cohort definitions every Monday morning."
    evidence_basis: [IS-002]
  # ...
```

The candidate id format is the orchestrator's responsibility; the skill consumes ids as opaque strings.

**Output.** A proposal block listing clusters and an unclustered bucket. Each cluster names the rule that anchors it.

```yaml
proposed_object_type: Opportunity Clustering (proposal)
clusters:
  - name: "Re-derived analytics intermediates"
    rule: shared-customer-behavior
    members: [OPP-CAND-001, OPP-CAND-002, OPP-CAND-007]
    rationale: "All three describe analysts re-running the same intermediate computation across sessions because the prior result wasn't share-able."
  - name: "Notebook-to-deck handoff friction"
    rule: shared-workflow-step
    members: [OPP-CAND-003, OPP-CAND-005]
    rationale: "Both candidates anchor on the moment of moving a result from a notebook into a stakeholder-facing deck."
unclustered:
  - id: OPP-CAND-009
    statement: "Customer asked for dark mode."
    reason: "Solution-shaped — no shared anchor with the other candidates."
human_owned_decisions:
  - Accept clusters or revise
  - Decide whether unclustered candidates are real Opportunities or should be parked
  - Decide which clusters to promote into the OST (downstream)
ai_assistance_used:
  - Thematic grouping against the three rules
  - Per-cluster rationale drafting
ai_assistance_allowed: restricted
human_approval_required: true
```

Never persist; never promote a cluster to an OST Opportunity. Promotion is the downstream `/cluster-opportunities` command's job, and it requires a human accepting the cluster.

## Shared customer behavior

Group candidates that describe the same observable customer action — what the customer is doing, not what they want or wish for.

**When to apply.** Two or more candidates anchor on the same verb-object pair from the customer's workflow: "copies rows from spreadsheet into deck," "re-runs the same SQL across sessions," "exports CSV and manually edits before sending." The action is the anchor; the variation in candidate wording is just different snapshots' framing of the same underlying behavior.

**Concrete example.** Three candidates: (a) "Analysts redo the same join logic across notebooks"; (b) "Analysts re-derive cohort definitions every Monday"; (c) "Analysts re-paste the same WHERE clause into every dashboard query." All three describe the same customer behavior — re-running an already-derived computation because the prior result wasn't share-able. Cluster name: "Re-derived analytics intermediates." Rule: shared-customer-behavior.

**Anti-pattern.** A cluster named "Things analysts do" — the rule is the action, not the actor. If the only thing the candidates share is "analysts" (the role), no thematic anchor exists; the candidates belong in different clusters or in the unclustered bucket.

## Shared workflow step

Group candidates that describe friction at the same step in a multi-step process.

**When to apply.** Two or more candidates name pain at the same workflow boundary — "moving result from notebook to deck," "sharing a draft for review before publishing," "switching from data-cleaning to analysis." The candidates differ on what *kind* of friction occurs at the step, but they agree on *which* step.

**Concrete example.** Two candidates: (a) "Analysts paste static screenshots into the deck because the deck tool can't render the notebook chart"; (b) "Analysts re-create the chart in the deck's native tool, drifting from the notebook's underlying logic." Both anchor on the same workflow step (notebook → deck handoff). Different friction; same step. Cluster name: "Notebook-to-deck handoff friction." Rule: shared-workflow-step.

**Anti-pattern.** A cluster grouping "everything that happens in the morning" — workflow steps are bounded by inputs/outputs, not by time-of-day. If the candidates don't share an input/output boundary, they don't share a workflow step.

## Shared workaround pattern

Group candidates that describe customers building or using the same external coping mechanism.

**When to apply.** Two or more candidates name a workaround the customer adopted — a spreadsheet built outside the product, a Slack channel used as a notification queue, a manual checklist replicated across teams. The workaround is the anchor; the underlying pain may differ slightly but the customers all converged on the same compensating behavior.

**Concrete example.** Three candidates: (a) "Analysts build personal spreadsheets to track which queries they've already run"; (b) "PMs maintain a side-doc listing 'queries we've already answered' for the analyst pool"; (c) "Teams adopt a Notion board to track recurring data requests." All three converged on a manual external memory layer because the product's own query history is insufficient. Cluster name: "External memory of past queries." Rule: shared-workaround-pattern.

**Anti-pattern.** A cluster named "uses Excel" — Excel-as-tool is too broad to anchor a cluster. The shared anchor is the *purpose* of the workaround (external memory, tracking, cross-team coordination), not the tool used to implement it.

## Common failure modes

- **Over-clustering** — every candidate becomes its own cluster of one. The output looks like the input; no synthesis happened. Recovery: if the longest cluster has only 1-2 members and there are ≥ 10 candidates, the rule application is too strict — re-walk the three rules with looser anchors.

- **Under-clustering** — "everything in one bucket" because every candidate involves the same role or product surface. Recovery: re-cluster by sub-rule; "all things analysts do in the query editor" is the universe, not a cluster. Apply the three rules within that universe.

- **Forced-clustering** — candidates with no shared anchor get grouped to fit a tidy number of clusters (three is suspiciously common). Recovery: the `unclustered:` bucket exists exactly to absorb candidates that don't fit. Forcing a fit makes the cluster's rationale handwave-y, and downstream the cluster will fail the framework's "every Opportunity must trace to a customer-research moment" check.

- **Solution-shaped candidates clustered as Opportunities** — a candidate like "ship dark mode" is a Solution, not an Opportunity (the framework's "solution tree" anti-pattern). The clustering skill cannot promote a Solution to an Opportunity. Surface Solution-shaped candidates in the `unclustered:` bucket with a one-line note pointing at the framework's Opportunity-vs-Solution distinction; the human disposes of them.

## No-auto-promote rule

The skill proposes clusters. It does not promote them. Promoting a cluster to an Opportunity in the OST is the downstream `/cluster-opportunities` command's job, and the promotion is gated on a named human accepting the cluster and confirming the cluster's `evidence_basis:` aggregates from the member candidates meets the framework's source-opportunities discipline.

The reason the skill cannot promote: the framework's tree-shape rules (one Outcome at the root; Opportunities are additive children; chosen Opportunity is named explicitly) require structural decisions the skill is not authorized to make. The OST's `chosen_opportunity:` field exists precisely so a human can decide which Opportunity to pursue once the clusters are visible — automating that choice would silently skip the Validation phase the kit's HANDOVERS contract requires.

## What this skill never does

- Never persists the proposal to disk.
- Never auto-promotes a cluster to an OST Opportunity.
- Never edits candidate text — clusters are *groupings*, not *rewrites*. A candidate whose wording needs cleanup is the orchestrator's problem, not this skill's.
- Never redefines what an Opportunity is. The framework owns that.
- Never invents a fourth grouping rule — if a candidate doesn't fit one of the three, it belongs in `unclustered:`.

## When this skill is wrong

- **Fewer than three candidates.** Clustering three or fewer candidates is not meaningful synthesis; surface back to the orchestrator with "too few candidates — interview more or wait for more snapshots before clustering."

- **No shared anchors across any pair of candidates.** When every pairwise comparison returns "no shared rule," the candidate list is too heterogeneous; the unclustered bucket will be the entire list. Surface this as a signal that the upstream `/extract-opportunities` step may have over-broadly extracted, or that the snapshots feeding it covered too wide a customer base.

- **Candidates are all Solutions masquerading as Opportunities.** When most of the candidate list reads like a feature roadmap (cite the framework's "solution tree" anti-pattern), the skill cannot rescue the list by clustering. Surface the structural smell and ask the orchestrator to re-run `/extract-opportunities` with stricter opportunity-vs-solution discipline.

- **Candidates carry no `evidence_basis:` links.** The framework's "Source opportunities" rule says every Opportunity must trace to a specific research moment. A candidate with no evidence is conjecture, and clustering conjecture produces themed conjecture. Surface the gap; do not silently cluster unsourced candidates.

## References

- `context/frameworks/opportunity-solution-tree.md` — the canonical OST framework. The skill consumes the four-node-type definitions and respects the §"Source opportunities" discipline (`evidence_basis:` requirement on every Opportunity). Source of truth.
- `context/frameworks/interview-snapshot.md` — the upstream artifact (`IS-NNN` snapshots) that supplies the `evidence_basis:` links the clustering skill expects on each candidate.
- `context/frameworks/continuous-discovery.md` — the weekly habit that produces the candidate stream this skill consumes.
