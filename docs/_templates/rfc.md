# RFC <NNNN>: <Title>

- **Status:** Draft | Open for comment | Final comment period | Accepted | Rejected | Withdrawn
- **Author:**
- **Date:** <YYYY-MM-DD>
- **Final comment period closes:** <YYYY-MM-DD or n/a>

## Summary

One paragraph. What this RFC proposes, in plain English.

## Motivation

Why we should do this. What problem does it solve. What's broken or missing today.

Cite evidence — specific failures, friction observed, contributor pain. Speculative RFCs ("this might be useful someday") have a high bar; reactive RFCs ("this thing is consistently failing in <pattern>") have a low one.

## Detailed design

The actual proposal. Be specific. Name files, conventions, fields, behaviors. Show before/after where useful.

If the proposal touches the docs hierarchy (CHARTER, CONVENTIONS, AGENTS, INVENTORY, HANDOVERS, HUMAN-AI-OWNERSHIP), show the diff.

If the proposal touches the ontology (`context/frameworks/ontology.md`), show the type additions or rule changes explicitly.

If the proposal adds new top-level directories or modifies the phase structure, this is a high-bar change — make the case explicitly.

## Drawbacks

What goes wrong if we adopt this. Be honest. The most useful RFCs name their own weak points; the least useful ones pretend there are none.

## Alternatives

Other ways to solve the same problem. The status quo is always one of the alternatives. For each, name why it loses.

## Adoption strategy

How this gets rolled in. Specifically:
- Which existing artifacts get edited (and in which PR or sequence)?
- What backward compatibility is preserved?
- Is there a migration path for kit users already using the older convention?

## Unresolved questions

Things this RFC deliberately leaves open. The acceptance vote can still pass with open questions if the questions are explicitly deferred to follow-on work.

## Follow-on artifacts

If this RFC is accepted, what gets produced as a result:
- New or amended ADRs
- New specs
- Direct edits to CHARTER / CONVENTIONS / etc.

After all follow-ons exist, this RFC's job is done. It stays in the repo as history.
