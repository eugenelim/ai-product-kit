# Interview Snapshot

> A one-page structured summary of one customer interview, defined by Teresa Torres in *Continuous Discovery Habits* (2021), ch. 5. The snapshot is the bridge between raw transcript and downstream theming: every Opportunity in an OST traces back to one (or several) snapshots. This kit consumes snapshots via `/interview-snapshot` (planned — P2.1), the `interview-snapshot` skill (planned — P2.2), and the `interview-coder` agent (planned — P2.3, a fan-out worker that codes one transcript at a time).

## The snapshot schema

A snapshot is one artifact per interviewee per session — never an aggregate. The fields are deliberately narrow; the discipline is in what doesn't go in.

- **Goal** — what the customer was trying to do, in their words. Not what the PM thinks the goal was; not the assumed job-to-be-done. The customer's stated goal, paraphrased faithfully.
- **Workflow** — the actual sequence of steps the customer described taking, in order. Not the steps the PM expected; the steps the customer narrated.
- **Pain Points** — where the customer got stuck, frustrated, or surprised. One bullet per distinct moment, anchored to a workflow step if possible.
- **Workarounds** — what the customer did to cope with each pain point. Workarounds are often more revealing than complaints: a customer who built a spreadsheet to compensate is telling you the magnitude of the pain in their own time-spent.
- **Tools** — what the customer used (the product, adjacent products, manual processes, side channels). Names of tools, not categories.
- **Direct Quote** — exactly one verbatim quote, with attribution to the speaker and a timestamp into the recording if available. The quote is load-bearing for downstream Opportunity sourcing — Opportunities should be able to cite the snapshot by quote, not by paraphrase.
- **Date** — when the interview happened (ISO YYYY-MM-DD).
- **Interviewer** — the named human who conducted the interview. Not a role ("PM"); a name.

## Transcript extraction rules

- **Paraphrase, do not invent.** If the customer didn't say it, it doesn't go in the snapshot. The temptation to fill in "what they probably meant" is the single biggest source of fabricated insight.
- **One snapshot per interviewee per session.** Compositing snapshots across two interviews — even of the same person — loses session-level context (what they had just been doing; what mood they were in; what came up). Two interviews = two snapshots.
- **Quotes verbatim with attribution.** The direct-quote field is the most-cited part of the snapshot downstream; getting the wording right matters for traceability and for honest representation of the customer's voice.
- **Ambiguous statements get flagged, not resolved.** When the customer says something the interviewer doesn't fully understand, the snapshot records the statement as ambiguous and the interview moves on — the snapshot does not pretend to clarity that wasn't there.
- **Never extrapolate to "what they probably meant."** If a follow-up question is needed, schedule another interview; don't fabricate the answer.

## What a good snapshot is *not*

- **A summary of what the PM thinks.** The PM's interpretation belongs in the OST, not in the snapshot. The snapshot is what was observed.
- **A synthesized persona.** Personas are aggregates across many snapshots; one snapshot is not a persona, and a snapshot that reads like a persona has been over-synthesized.
- **A sales-style needs assessment.** Sales needs-assessments are oriented toward fit-with-product; snapshots are oriented toward fit-with-the-customer's-world. Different artifact, different question.
- **An opportunity list.** Opportunities derive from snapshots, downstream. A snapshot that opens with "here are the opportunities" has skipped a step — and the opportunities will be undersourced.
- **A feature request list.** Customers often request features; the snapshot records the request (in the Tools or Workarounds field) but does not promote it. The job of turning requests into Opportunities is downstream.

## How the kit uses this framework

- `/interview-snapshot` (planned — ROADMAP P2.1) — the command that produces a snapshot from a raw transcript.
- `interview-snapshot` skill (planned — ROADMAP P2.2) — speaker detection + time-aligned quote extraction; the dispatched-by-command rule library.
- `interview-coder` agent (planned — ROADMAP P2.3) — fan-out worker, one transcript at a time, used when there's a batch of interviews to code.
- `/extract-opportunities` (planned — ROADMAP P2.4) — consumes snapshots and emits opportunity candidates that feed the OST.
- `context/frameworks/opportunity-solution-tree.md` — every Opportunity in an OST must source-trace to at least one snapshot.

Frame: snapshots are the raw material the OST consumes. A team that runs `/extract-opportunities` against zero snapshots gets zero real Opportunities — the OST is only as evidence-grounded as the snapshots feeding it.

## References

- Torres, T. (2021). *Continuous Discovery Habits: Discover Products that Create Customer Value and Business Value*. Product Talk LLC. Chapter 5 ("Interviewing for Opportunities") — the canonical source for the snapshot schema.
- `context/frameworks/continuous-discovery.md` — the weekly habit that produces snapshots at cadence.
- `context/frameworks/opportunity-solution-tree.md` — the downstream consumer.
