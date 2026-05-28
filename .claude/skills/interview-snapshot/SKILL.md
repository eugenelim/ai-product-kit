---
name: interview-snapshot
description: Transforms a raw customer-interview transcript (audio-derived or notes-only) into a proposal block matching the eight-field Interview Snapshot schema defined in `context/frameworks/interview-snapshot.md`. The skill consumes the framework as canon — it never redefines the schema. It applies four operational transformations the framework does not specify mechanically: speaker detection on transcripts that lack explicit markers, time-aligned quote extraction, paraphrase enforcement against the canonical fabrication patterns, and a no-recording fallback for note-only interviews. Output is a proposal — the skill never persists. Dispatch per transcript inside `/interview-snapshot` (planned — P2.1) or as a fan-out target inside the `interview-coder` agent (planned — P2.3). Load whenever the orchestrator needs one snapshot from one transcript.
license: MIT
---

# interview-snapshot

This skill turns one raw customer-interview transcript into one structured proposal block matching the eight-field Interview Snapshot schema. The schema, the paraphrase discipline, and the ambiguity-flagging pattern are owned by `context/frameworks/interview-snapshot.md`; this skill cites that framework and adds only the operational rules the framework does not specify mechanically (how to detect speakers, how to extract timestamps, how to enforce paraphrase, how to fall back when there is no recording).

The skill never persists. It proposes a snapshot; the orchestrator (typically `/interview-snapshot`) decides where to file it.

## When to use this skill

- A raw transcript (audio-derived markdown, captioning export, paste of a notes app) has just landed and needs to become a structured snapshot before downstream commands (`/extract-opportunities`, `/cluster-opportunities`) can consume it.
- A `/interview-snapshot` invocation needs the per-transcript transformation step.
- The `interview-coder` agent dispatches you per transcript when a batch of interviews needs coding in parallel.
- An OST audit (`/audit-discovery-coherence`, planned) surfaces an Opportunity whose `evidence_basis:` cites an `IS-NNN` reference that does not yet have a snapshot on disk; the orchestrator may invoke this skill to draft the missing snapshot from the source transcript.

## Invocation contract

**Input.**

- The raw transcript text. The orchestrator either pastes the transcript inline or names a file path.
- Optional `interviewer` (named human; defaults to "<TBD>" if absent — the orchestrator surfaces the gap).
- Optional `date` (ISO `YYYY-MM-DD`; defaults to "<TBD>").
- Optional `recording_present` boolean (defaults to `true`; setting `false` switches the quote-attribution path to the no-recording fallback below).

**Output.** A proposal block with the eight fields the framework defines (`@see context/frameworks/interview-snapshot.md` for the canonical schema), shaped as YAML frontmatter plus a `## Direct Quote` body block (mirroring the universal-metadata schema convention in `docs/CONVENTIONS.md`):

```yaml
---
proposed_object_type: Interview Snapshot
proposed_slug: <interviewee-firstname-YYYY-MM-DD>
proposed_id: IS-<NNN — leave as TBD if no numbering is obvious>
goal: <one sentence in the customer's stated framing>
workflow: <ordered list, one bullet per step the customer described>
pain_points: <one bullet per distinct moment of friction>
workarounds: <one bullet per coping mechanism the customer named>
tools: <named tools the customer mentioned, not categories>
date: <YYYY-MM-DD>
interviewer: <named human>
ambiguities: <list of [ambiguous: ...] flags surfaced by the transcript>
human_owned_decisions:
  - Confirm faithfulness to the customer's words
  - Decide whether to schedule a follow-up on any ambiguity flags
ai_assistance_used:
  - Speaker detection
  - Timestamp-aligned quote extraction
  - Paraphrase rule application
ai_assistance_allowed: restricted
human_approval_required: true
---

"<verbatim>" — <Speaker Name>, <MM:SS>
```

Never persist; never write the proposal to disk yourself. The orchestrator decides where the snapshot lands.

## Speaker detection

Transcripts arrive in several shapes. Apply the rules below in order; stop at the first match.

1. **Explicit speaker tags.** Lines prefixed with `Speaker A:` / `Speaker B:`, `Customer:` / `Interviewer:`, or named-speaker tags (`Priya:`) — accept the tags as authoritative. Map the customer-side tag to the interviewee; map the interviewer-side tag to the named interviewer in the optional `interviewer:` input.
2. **Timestamped dialog blocks.** Lines of the shape `[Speaker A 14:32]` or `Speaker A (14:32):` — treat the speaker label inside the bracket as authoritative; the time component flows into time-aligned quote extraction below.
3. **Bracketed monologue with single named speaker.** A transcript that names one speaker once at the top (e.g., `# Interview with Priya R., 2026-05-12`) and then runs without further attribution — treat the whole transcript as the customer's monologue; the interviewer's prompts are paraphrased into the workflow steps rather than quoted.
4. **No markers at all.** When the transcript provides no attribution cues, surface as `[ambiguous: speaker-attribution]` and ask the orchestrator (or the named human) to disambiguate before writing the snapshot. Do not guess. The framework's paraphrase rule explicitly forbids inventing attribution the transcript did not contain.

The "transcript starts mid-utterance" case (no header, dialog begins with `"... so anyway, what I usually do is..."`) is the no-markers case — surface the ambiguity flag.

## Time-aligned quote extraction

The Direct Quote field is load-bearing for downstream Opportunity source-tracing. Extract exactly one verbatim quote from the transcript that captures the most decision-useful customer voice on the named workflow/pain.

Recognized timestamp formats:

- `MM:SS` (e.g., `14:32`)
- `HH:MM:SS` (e.g., `01:14:32`)
- `[HH:MM:SS]` (bracketed; common in captioning exports)
- `(MM:SS)` (parenthesized; common in note-taking apps)

Quote-with-timestamp format **must** be exactly: `"<verbatim text>" — <Speaker Name>, <MM:SS>` (or `<HH:MM:SS>`). Inaudible words inside the quote are marked `[inaudible]`; do not guess. If the most decision-useful moment in the transcript is multi-sentence and the customer was not interrupted, the quote may span 2-3 sentences; do not exceed three sentences in one quote.

## Paraphrase enforcement

The framework's canonical example (the "spreadsheet → deck" exchange in `context/frameworks/interview-snapshot.md`) names exactly three fabrication patterns that paraphrase must NOT produce:

1. **Invented diagnosis** — adding a cause the customer did not name (e.g., "lack of integration").
2. **Emotion escalation** — promoting a milder customer-stated emotion (`annoying`) to a stronger one (`frustrated`).
3. **Invented feature request** — adding an "export feature" the customer never asked for.

Before emitting the proposal, walk each Goal / Workflow / Pain Points / Workarounds bullet against these three patterns. If a draft bullet would commit any of them, rewrite the bullet to record only what the customer actually said. The Direct Quote field exists precisely so a reviewer can verify the paraphrase against the source line.

## No-recording fallback

When `recording_present: false` (note-only interviews), the Direct Quote field cannot carry a timestamp. Use the framework's no-recording attribution pattern instead:

```
"<verbatim text>" — <Speaker Name>, [no recording]
```

Do NOT fabricate a timestamp to satisfy the format. The `[no recording]` marker is downstream-readable; a fake `12:00` is not.

When notes are too summarized to support a verbatim quote (only paraphrases survive), surface `[ambiguous: no-verbatim-quote-available]` and ask the orchestrator whether to ship the snapshot with a paraphrased Direct Quote (marked as such) or schedule a follow-up. The orchestrator's choice is human-owned.

## Ambiguity flagging

When the customer says something the interviewer didn't fully understand (the framework's `"and then I usually just do the thing"` canonical example), the snapshot records the statement as ambiguous and the interview moves on. Record the flag inside the Workflow or Pain Points bullet:

```
- [ambiguous: "the thing" — unclear referent; follow-up needed]
```

`/extract-opportunities` (planned — P2.4) and the `interview-coder` agent (planned — P2.3) surface ambiguous bullets as candidate follow-up questions for the next interview round. A silently-resolved ambiguity is the failure mode this flag prevents.

## What this skill never does

- **Never redefines the eight snapshot fields.** The schema lives in `context/frameworks/interview-snapshot.md`; this skill points at it.
- **Never persists the proposal to disk.** The orchestrator (typically `/interview-snapshot`) decides where the snapshot lands.
- **Never composites snapshots across two interviews — even of the same person.** One interviewee per session ⇒ one snapshot. Composite snapshots lose session-level context.
- **Never extrapolates to "what they probably meant."** If a follow-up is needed, surface the ambiguity flag; never fabricate the answer.
- **Never treats a sales-call recording, Slack thread, support ticket, or NPS verbatim as a snapshot source.** Those produce different artifacts (research notes, support patterns); a snapshot requires a real 1-on-1 interview with a named interviewer in real time.
- **Never auto-fills the `interviewer:` field with a role.** "PM" is not a name. If no name is provided, surface `<TBD>` and let the orchestrator resolve.

## When this skill is wrong

- **The transcript is from a sales call, not a discovery interview.** Sales-call framing is fit-with-product; snapshots are fit-with-the-customer's-world. Decline to produce a snapshot; surface that the source artifact does not match the schema's evidentiary contract.
- **The transcript lacks any single named speaker on the customer side.** A roundtable transcript with three customers is three potential snapshots, one per interviewee. Ask the orchestrator which speaker to code.
- **The transcript is short (< 5 minutes' worth of content) or summarized to the point that no verbatim quote survives.** Produce the snapshot but surface the `[no-verbatim-quote-available]` ambiguity flag; the orchestrator decides whether to ship or schedule a follow-up.
- **The Goal field would be a feature request rather than a stated goal.** A customer who says "I want an export feature" has named a Solution, not a Goal. Surface this as `[ambiguous: solution-stated-as-goal]` and rewrite the Goal field in terms of the customer's underlying objective if the transcript supports it; otherwise leave `<TBD>` and ask.

## References

- `context/frameworks/interview-snapshot.md` — the canonical eight-field schema, the paraphrase rule, the ambiguity-flagging pattern, the no-recording attribution rule. Source of truth.
- `context/frameworks/continuous-discovery.md` — the weekly habit that produces transcripts at cadence; the upstream practice this skill serves.
- `context/frameworks/opportunity-solution-tree.md` §"Source opportunities" — the downstream contract that snapshot ids (`IS-NNN`) satisfy via the `evidence_basis:` field on Opportunity nodes.
