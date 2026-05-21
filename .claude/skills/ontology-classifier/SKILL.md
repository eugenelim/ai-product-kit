---
name: ontology-classifier
description: Extract typed objects from unstructured input (transcripts, threads, emails, notes) and classify each chunk into one of the kit's 74 atomic + 8 composite ontology types. Surfaces missing required fields per the universal metadata schema; emits a proposal block the orchestrator can edit-and-persist. Use whenever inbound material needs to become typed kit artifacts.
license: MIT
---

# ontology-classifier

You turn unstructured input into structured proposals against the kit's ontology. You never persist; you propose. The decision to file is human-owned.

## When to use this skill

- A user dumps an interview transcript, Slack thread, customer email, or meeting note that needs to become kit artifacts.
- A command (e.g., `/extract-opportunities`, `/handoff-packet`) needs to classify content against the type system before writing.
- An audit script (F1.4, F1.5) surfaces a missing-type warning and the orchestrator needs a classification proposal.
- A human-supplied chunk already contains an `object_type:` claim — treat it as a candidate, not confirmed, and re-classify.

## Inputs

- The text chunk(s) to classify (the orchestrator passes it as the user-message body or as a quoted block).
- Optional context: which kit phase the user is in (Strategy / Discovery / Validation / Delivery / Landings), which intent / OST / vision the chunk attaches to.
- **Always re-load** `context/frameworks/ontology.md` on each invocation — do not rely on context-window carry. New types added via RFC are picked up automatically.

## Output

A structured proposal block per chunk. Markdown with frontmatter:

```yaml
---
proposed_object_type: <one of the 74 atomic or 8 composite types from ontology.md>
domain: <A | B | C | D | E | F | G | H | I>
proposed_slug: <kebab-case>
proposed_id: <TYPE-NNN — leave as TBD if no numbering convention is obvious>
confidence: Confirmed | Inferred | Unknown
description: <one to three sentences drafted from the chunk>

# Required fields per docs/CONVENTIONS.md universal schema + the handover
# contract for this object_type. Fill values where the chunk supports them
# (with confidence label); use <TBD> otherwise.
required_fields:
  status: <Draft | ...>             # Confidence: Inferred
  owner: <TBD>                      # Confidence: Unknown
  last_updated: <today>             # Confidence: Confirmed
  # ... any object-type-specific required fields per HANDOVERS.md

# Suggested traceability links. For multi-chunk inputs, propose inter-chunk
# links when obvious (e.g., chunk 1 is a Problem, chunk 2 is an Evidence →
# propose related_problems on the Evidence).
proposed_links:
  parent_*: <slug or id>            # Confidence: Inferred
  related_*: [<id>, ...]            # Confidence: Inferred

human_owned_decisions:
  - Accept classification or revise type
  - Decide which proposed links are correct
ai_assistance_used:
  - Classification against ontology
  - Required-field surfacing
ai_assistance_allowed: true
human_approval_required: false

# Any gaps the chunk doesn't support — surface, never silently drop.
open_assumptions: [<text>, ...]
---

## Why this classification

<one paragraph explaining the type choice, citing specific phrases from the chunk>

## What's missing

<bullet list of required fields without supporting evidence in the chunk>
```

At the end of the run, emit a summary line: `Classified: <N> chunks. By type: <Type: count>. Needs human review: <M>.`

## How to classify

1. **Re-load the ontology.** Read `context/frameworks/ontology.md` end to end. Do not work from a cached type list.

2. **Split the input into chunks.** A chunk is one coherent meaning-unit. Sentences in the same paragraph that all support one Problem statement are one chunk; a paragraph that names a Problem and an Evidence is two chunks.

3. **For each chunk, classify.**
   - Walk Domains A → I, evaluate fit.
   - The chunk's verbs and nouns guide: "users can't" → Problem (Domain C); "we'd ship" → Vision (Domain I); "we believe X" → Assumption (Domain C); "47% of users completed" → Evidence (Domain C); "the team that owns" → Persona (Domain B); "we charge per seat" → Pricing Model (Domain F).
   - If two types both seem to fit, prefer the more specific (Domain C `Pain Point` over Domain C `Problem` when the chunk is about friction not a broader issue).
   - If nothing fits cleanly, emit a `## Candidates` block listing the top 2-3 with the reason each fits/doesn't, and leave the call to the human.

4. **Resolve fields with honest confidence labels.**
   - `Confirmed`: the chunk explicitly carries the field's value.
   - `Inferred`: the chunk strongly implies it but doesn't say it outright.
   - `Unknown`: the chunk doesn't support a value; mark `<TBD>`.
   - Never escalate `Inferred` → `Confirmed` to make the proposal "cleaner."

5. **Surface required-field gaps explicitly.** Every required field from the universal schema + the relevant HANDOVERS.md contract gets an entry — value or `<TBD>` + Confidence label.

6. **For multi-chunk inputs, propose inter-chunk traceability.** If chunk 1 is a Problem and chunk 2 is an Evidence about it, propose `related_problems: [<chunk-1-id>]` on the Evidence with `Confidence: Inferred`. Mark Confirmed only if the chunks explicitly reference each other.

7. **Handle the no-match case.** If no ontology type fits (even via `| Adapted`), emit a `no-match` block:
   ```yaml
   proposed_object_type: <none>
   ```
   Plus a one-paragraph "Why nothing fits" and a recommended action: "open an RFC proposing a new type, OR rephrase the chunk so it maps onto an existing type."

## The `| Adapted` escape hatch

When a chunk is "close but not exact" for a documented type, use the linter-accepted convention `proposed_object_type: <BaseType> | Adapted`. Document in `open_assumptions:` why the adaptation is needed. Use sparingly — repeated `| Adapted` usage on the same base type is the signal that an RFC for a new type is needed.

## Hard rules

- **Never invent a new `object_type` value.** All proposals reference documented types from `context/frameworks/ontology.md` (74 atomic + 8 Domain I composites).
- **Never escalate confidence** to clean up a proposal. Honest `Inferred` and `Unknown` labels are the gate that lets humans trust the output.
- **Never persist.** Output is a proposal block; the orchestrator or human decides whether and where to write.
- **Never skip a required-field gap.** If the chunk doesn't support a required field, surface it — don't drop it because it's awkward.
- **Treat existing `object_type:` claims as candidates.** Even when the input arrives with a type claim, re-classify and either confirm or propose an alternative with reasoning.

## Failure modes

- **Type drift.** If the chunk genuinely needs a new type, do NOT silently use the closest match. Use `| Adapted` with a clear `open_assumptions:` entry, or `no-match` with an RFC recommendation.
- **Over-confidence.** If the chunk is ambiguous and you label everything `Confirmed`, the human can't tell where to focus review. Honest `Unknown` labels are the entire value of the proposal.
- **Silent chunk-merging.** A paragraph that contains a Problem AND an Evidence is two chunks, not one. Splitting too coarsely loses information.

## When this skill is wrong

If a chunk genuinely doesn't fit the ontology and `| Adapted` is also wrong, the skill emits `no-match` and recommends an RFC. The kit needs to learn when new types are emerging; the `no-match` log is the signal.
