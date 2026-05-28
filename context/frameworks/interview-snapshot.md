# Interview Snapshot

> A one-page structured summary of one customer interview, defined by Teresa Torres in *Continuous Discovery Habits* (2021), ch. 5. The snapshot is the bridge between raw transcript and downstream theming: every Opportunity in an OST traces back to one (or several) snapshots. This kit consumes snapshots via `/interview-snapshot` (planned — P2.1), the `interview-snapshot` skill (planned — P2.2), and the `interview-coder` agent (planned — P2.3, a fan-out worker that codes one transcript at a time).

## The snapshot schema

A snapshot is one artifact per interviewee per session — never an aggregate. The fields are deliberately narrow; the discipline is in what doesn't go in.

- **Goal** — what the customer was trying to do, in their words. Not what the PM thinks the goal was; not the assumed job-to-be-done. The customer's stated goal, paraphrased faithfully.
- **Workflow** — the actual sequence of steps the customer described taking, in order. Not the steps the PM expected; the steps the customer narrated.
- **Pain Points** — where the customer got stuck, frustrated, or surprised. One bullet per distinct moment, anchored to a workflow step if possible.
- **Workarounds** — what the customer did to cope with each pain point. Workarounds are often more revealing than complaints: a customer who built a spreadsheet to compensate is telling you the magnitude of the pain in their own time-spent.
- **Tools** — what the customer used (the product, adjacent products, manual processes, side channels). Names of tools, not categories.
- **Direct Quote** — exactly one verbatim quote, with attribution to the speaker and a timestamp into the recording if available. Format: `"<verbatim text>" — <Speaker Name>, <MM:SS>` (for example: `"I just gave up and emailed it to myself." — Priya R., 14:32`). The quote is load-bearing for downstream Opportunity sourcing — Opportunities should be able to cite the snapshot by quote, not by paraphrase.
- **Date** — when the interview happened (ISO YYYY-MM-DD).
- **Interviewer** — the named human who conducted the interview. Not a role ("PM"); a name.

## Transcript extraction rules

- **Paraphrase, do not invent.** If the customer didn't say it, it doesn't go in the snapshot. The temptation to fill in "what they probably meant" is the single biggest source of fabricated insight.

  Concrete contrast — suppose the customer says:

  > "I open the spreadsheet, copy the row, and paste it into the deck — and yeah, it's annoying."

  A *valid paraphrase* records: `Customer copies rows from the spreadsheet into the deck manually and describes the step as annoying.`

  An *invented version* would read: `Customer is frustrated by the lack of integration between the spreadsheet and the deck tool and wants an export feature.` That sentence adds three things the customer never said:
    - a diagnosis (*lack of integration*) the customer did not name,
    - an emotion (*frustrated*) escalated from the milder *annoying* the customer actually used,
    - a feature request (*export*) that was never uttered.

  Three fabrications in one sentence. The paraphrase rule is what keeps the snapshot honest enough to be downstream-citable.

- **One snapshot per interviewee per session.** Compositing snapshots across two interviews — even of the same person — loses session-level context (what they had just been doing; what mood they were in; what came up). Two interviews = two snapshots.

- **Quotes verbatim with attribution.** The direct-quote field is the most-cited part of the snapshot downstream; getting the wording right matters for traceability and for honest representation of the customer's voice. If the recording is unclear and a word is inaudible, mark it `[inaudible]` rather than guessing — never silently smooth a quote into something the customer didn't say.

- **Ambiguous statements get flagged, not resolved.** When the customer says something the interviewer doesn't fully understand, the snapshot records the statement as ambiguous and the interview moves on — the snapshot does not pretend to clarity that wasn't there.

  Concrete example — when the customer says:

  > "and then I usually just do the thing"

  the snapshot records the workflow step as:

  > `[ambiguous: "the thing" — unclear referent; follow-up needed]`

  rather than inferring `the thing = saving the file` (or any other plausible-sounding completion). The flag itself is downstream-useful — `/extract-opportunities` can surface ambiguous workflow steps as candidate follow-up questions for the next interview round, which means the ambiguity is recoverable. A silently-resolved ambiguity is not.

- **Never extrapolate to "what they probably meant."** If a follow-up question is needed, schedule another interview; don't fabricate the answer.

## What a good snapshot is *not*

- **A summary of what the PM thinks.** The PM's interpretation belongs in the OST, not in the snapshot. The snapshot is what was observed.
- **A synthesized persona.** Personas are aggregates across many snapshots; one snapshot is not a persona, and a snapshot that reads like a persona has been over-synthesized.
- **A sales-style needs assessment.** Sales needs-assessments are oriented toward fit-with-product; snapshots are oriented toward fit-with-the-customer's-world. Different artifact, different question.
- **An opportunity list.** Opportunities derive from snapshots, downstream. A snapshot that opens with "here are the opportunities" has skipped a step — and the opportunities will be undersourced.
- **A feature request list.** Customers often request features; the snapshot records the request (in the Tools or Workarounds field) but does not promote it. The job of turning requests into Opportunities is downstream.
- **A proxy-research substitute.** A snapshot is the output of a 1-on-1 interview with a single customer, conducted by a named human interviewer in real time. A document assembled from any of the following is *not* a snapshot — even if the schema fields are filled in:
    - a Slack thread or Discord conversation,
    - a sales call recording (the sales call's frame is fit-with-product, not fit-with-the-customer's-world),
    - a support ticket or NPS verbatim,
    - a teammate's secondhand recollection ("I was talking to a customer at the conference and they said…").

  Those artifacts may be useful in their own right (a support-pattern observation, a sales signal, a research note), but they do not carry the evidentiary weight a snapshot does downstream, and they must not be cited as snapshots when an Opportunity in the OST claims source-trace to interview data. If the only "snapshots" feeding the OST are proxy artifacts, the OST is undersourced — flag the gap and schedule real interviews before the next strategy refresh.

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
