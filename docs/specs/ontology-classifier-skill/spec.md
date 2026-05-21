# Spec: ontology-classifier-skill

- **Status:** Draft
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored)
- **Component type:** skill
- **Serves kit phase:** Cross-cutting (every phase classifies inbound input)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md`; `context/frameworks/ontology.md` (Domains A-H + Domain I composites; the canonical type set); `docs/CONVENTIONS.md` (universal metadata schema)

> **Spec contract.** Defines the `ontology-classifier` skill — Claude's reference for extracting typed objects from unstructured input and surfacing missing required fields.

## Objective

Build `.claude/skills/ontology-classifier/SKILL.md` plus optional reference docs. The skill teaches Claude to: read unstructured input (an interview transcript snippet, a Slack thread, a customer email, a meeting note), classify each meaningful chunk into one of the kit's documented ontology types (74 atomic + 8 composite), and emit a structured output the orchestrator can either persist as an artifact or surface for human review.

This is the F1.3 deliverable. It unblocks AGENTS.md's repeated "run the ontology-classifier skill when uncertain" advice and discharges the `(planned — F1.3)` annotation across the kit's docs.

## Why now

Without this skill, kit users classify inbound material by hand against `context/frameworks/ontology.md`. That works but is slow and inconsistent. Promoting classification to a named skill: (a) makes the criteria explicit, (b) gives downstream audits a clean input format, (c) discharges the multiple planned-markers in AGENTS.md / .claude/CLAUDE.md / context/README.md.

## Inputs and outputs

**Inputs.**
- Unstructured text (the chunk to classify).
- Optional context: which phase the user is working in (Strategy / Discovery / Validation / Delivery / Landings), which intent / OST / vision the chunk is being added to.
- The ontology itself: `context/frameworks/ontology.md` (loaded on demand).

**Outputs.**
- A structured proposal block (markdown + frontmatter) the orchestrator can edit-and-persist:
  - For each chunk: proposed `object_type` (with Domain), proposed `slug`, draft `description`, required fields from `docs/CONVENTIONS.md` (with values where derivable, `<TBD>` where not), suggested traceability links (with confidence: Confirmed / Inferred / Unknown), and any `open_assumptions:` the skill couldn't resolve.
  - For chunks that don't classify cleanly: a "candidates" list with the top 2-3 types and why each fits/doesn't, leaving the call to the human.
- A summary line: counts by type + count of "needs human review" items.

## Boundaries

### Always do
- Classify against the ontology's 74 atomic + 8 composite types only. New types require an RFC, not skill output.
- Mark confidence honestly: `Confirmed` only when the chunk explicitly carries the field's value; `Inferred` when reasonable; `Unknown` when the chunk doesn't support a value.
- Surface every required-field gap rather than silently dropping them — the human owner decides what to fill.
- Use the `| Adapted` suffix when a chunk is "close but not exact" — never invent a new type.
- Follow the human-vs-AI ownership rule: classification is AI-assisted; the decision to persist is human-owned. Output declares `human_owned_decisions: ["Accept classification or revise type"]`.
- **Re-load `context/frameworks/ontology.md` on each invocation** (don't rely on context-window carry); this ensures new types added via RFC are picked up automatically.
- **When input already contains structured artifact content** (existing frontmatter, an `object_type:` claim): treat the existing claim as a candidate, not confirmed. Apply the same classification protocol and either confirm or propose an alternative with reasoning.
- **When a chunk cannot be classified at all** (no ontology type fits, even via `| Adapted`): emit a `no-match` block — `object_type: <none>`, a one-paragraph "Why nothing fits" explanation, and a recommended action: "open an RFC proposing a new type, OR rephrase the chunk so it maps onto an existing type."
- **For multi-chunk inputs:** in addition to classifying each chunk, propose inter-chunk traceability links when the relationship is obvious (e.g., chunk 1 is a Problem, chunk 2 is an Evidence → propose `related_problems:` on the Evidence). Mark these proposals with the same confidence labels (Confirmed/Inferred/Unknown).

### Ask first
- Persisting the classification to disk. The skill emits a proposal; the orchestrator (or human) decides where to file it.
- Modifying the ontology itself. Always RFC.

### Never do
- Invent new `object_type` values.
- Resolve traceability links with confidence higher than the evidence supports.
- Skip required-field surfacing because the chunk doesn't have the data.
- Treat a chunk as a single type when it spans multiple (split it).

## Verification mode

- **Manual gesture (golden-set).** A small set of fixture inputs under `.claude/skills/ontology-classifier/fixtures/` with documented expected classifications. A verifier loads the skill in a fresh session, feeds each fixture, and checks the output matches (object_type, key fields, confidence labels). Codify the golden set in `fixtures/golden.md`.
- **Goal-based check.** `tools/lint-skill.sh .claude/skills/ontology-classifier/SKILL.md` exits 0.

## Contract tests (manual-gesture form)

For each golden fixture (5 fixtures minimum, one per dominant domain):
- Skill produces a classification block.
- Proposed `object_type` matches the documented expected type.
- Required fields enumerated match `docs/CONVENTIONS.md` + the relevant HANDOVERS contract.
- Confidence labels are honest (not all `Confirmed`).
- For multi-chunk inputs: the chunks are split appropriately.

Golden fixtures: (1) Interview snippet revealing a Problem + Pain Point + Use Case; (2) Slack thread containing a candidate Assumption + Experiment idea; (3) Customer email with a Feature Request + Job to Be Done; (4) Meeting note containing a Decision + Risk; (5) Competitor announcement implying a Trend + Differentiator gap.

## Non-goals

- Doing the persistence write — that's the caller's responsibility.
- Running the audits — that's F1.4/F1.5/F1.6.
- Inventing new ontology types or domains.
- Becoming a generic "classify any text" tool — kit-ontology-only.

## Open questions

1. **Skill structure: single SKILL.md or sub-files?** Lean: single SKILL.md ≤ ~250 lines + a `fixtures/` directory. Sub-files only if the skill grows.
2. **Loading the ontology:** lean — instruct Claude to reference `context/frameworks/ontology.md` rather than embedding the type list. Single source of truth.

## Acceptance criteria

- [ ] `.claude/skills/ontology-classifier/SKILL.md` exists.
- [ ] `.claude/skills/ontology-classifier/fixtures/golden.md` exists with 5 inputs + expected classifications.
- [ ] `tools/lint-skill.sh .claude/skills/ontology-classifier/SKILL.md` exits 0.
- [ ] Manual-gesture verification: a fresh Claude Code session loads the skill and produces the documented classification for each golden fixture (recorded in a verification log in the spec's `notes/`).
- [ ] AGENTS.md, .claude/CLAUDE.md, context/README.md updated: the `(planned — F1.3)` annotation on `ontology-classifier` removed.
- [ ] `.claude/skills/README.md` updated: `ontology-classifier` moved from Planned to Shipped.
- [ ] INVENTORY.md updated: relevant rows mentioning `ontology-classifier` flipped from `planned (F1.3)` to `shipped`.
- [ ] ROADMAP.md: F1.3 checked off.
- [ ] PLAN/VERIFY/REVIEW gates exit 0.

## Cross-references

- **Consumed by:** every phase via the orchestrator; especially Discovery (extract opportunities) and Delivery (classify handoff-packet content).
- **Consumes:** `context/frameworks/ontology.md`, `docs/CONVENTIONS.md`, `docs/HANDOVERS.md`. Optionally `scripts.lib.frontmatter` for round-trip persistence in caller code.
- **Frontmatter fields owned:** none directly; surfaces all per the schema.
- **Ontology object types touched:** all.
