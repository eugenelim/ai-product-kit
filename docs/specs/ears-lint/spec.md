# Spec: ears-lint

- **Status:** Shipped (2026-05-23)
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** framework-ref + skill (one spec, two coupled artifacts — mirrors the F3 `template-authoring-convention` precedent of shipping multiple deliverables under one spec when they share contract surface)
- **Serves kit phase:** Delivery (specifically the requirements-quality surface — supports `/draft-spec` (P4.8, shipped without mechanical lint), `/handoff-packet` (P4.11) `acceptance-criteria.md` aggregation, and any future spec/handoff-packet authoring command).
- **Constrained by:** ROADMAP F4.12 (`framework-ears`) and P4.7 (`skill-ears-lint`); `docs/HANDOVERS.md` §"Handover 5: Initiative → Spec" and §"Handover 6: Spec → Engineering Handoff Packet" (the artifacts whose acceptance-criterion sentences EARS governs); `docs/CONVENTIONS.md` §"Specs and Plans" and §"Universal metadata schema" (kit-meta vs product-artifact frontmatter rule, and the `context/frameworks/` precedent of un-frontmatter-ed framework reference docs); `.claude/skills/work-loop/SKILL.md` (loop doctrine); `tools/lint-skill.sh` (the SKILL.md linter contract); Mavin, A., Wilkinson, P., Harwood, A., & Novak, M. (2009). "Easy Approach to Requirements Syntax (EARS)." 17th IEEE International Requirements Engineering Conference (the canonical academic source for the five EARS patterns).

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships one canonical EARS reference framework at `context/frameworks/ears.md` (rule library), one classification skill at `.claude/skills/ears-lint/SKILL.md` (rule consumer), and one fixture file under the skill's `references/` (manual-gesture verification). The framework is the source-of-truth for the five EARS patterns plus the Complex combination form; the skill cites the framework and does not restate it. Together they unblock `/draft-spec` (P4.8) to add mechanical EARS lint behind its current advisory EARS-pattern prompt without re-deriving rules.

## Objective

Author two coupled deliverables that, together, give the kit a single canonical source-of-truth for the EARS requirements-syntax patterns and an in-session sentence classifier that any spec-authoring or handoff-packet-authoring command can dispatch:

1. **`context/frameworks/ears.md`** — the EARS reference framework. Names the five canonical patterns (Ubiquitous, Event-driven, State-driven, Optional-feature, Unwanted-behavior) and the Complex combination form, with one canonical example per pattern. Cites Mavin et al. (2009) as the source. ≤ 150 body lines. Shape precedent: `context/frameworks/ontology.md` (existing framework-reference doc; no universal-metadata frontmatter — these docs sit outside `PHASE_DIRS` and are not linted by `lint-frontmatter.py` in default mode).
2. **`.claude/skills/ears-lint/SKILL.md`** — the classification skill. Given one or more candidate sentences, classifies each into one of {Ubiquitous, Event-driven, State-driven, Optional-feature, Unwanted-behavior, Complex, Non-conformant} and returns a structured per-sentence verdict with rationale and a suggested rewrite if non-conformant. The skill consumes `context/frameworks/ears.md` as its rule source and works standalone (no required orchestrator context beyond the candidate sentences themselves).
3. **`.claude/skills/ears-lint/references/fixture-sentences.md`** — ~10 candidate sentences with annotated expected classifications. Used for manual-gesture verification in-session and as a regression fixture for any future runnable script form of the skill.

## Why now

`/draft-spec` (P4.8) shipped 2026-05-23 with an *advisory* EARS-pattern prompt — it asks the human which pattern each Requirement follows, but does not lint the answer. Its ROADMAP row explicitly defers the lint to P4.7 ("EARS-lint skill planned; this command emits the EARS-pattern prompt without mechanical lint"). Without P4.7, every Requirement written by `/draft-spec` is ungoverned at the syntax level; downstream `/handoff-packet` (P4.11) aggregates these Requirements into `acceptance-criteria.md` without any syntax check. The longer this lasts, the more un-EARS sentences land in shipped Handoff Packets, and the more expensive a later cleanup pass becomes.

F4.12 (the framework doc) is upstream of P4.7 (the skill) because the skill must cite a single canonical rule source. Shipping the skill without the framework leaves the rules implicit and ungovernable; shipping the framework without the skill leaves it unused. Coupling them in one work-loop is the cheapest path to a closed feedback loop on Requirement syntax.

Wave-2 scope is precisely these two items. Wave-1 (the seven Phase-4 commands, shipped 17c198f) deliberately deferred mechanical EARS lint so Wave-2 could land it cleanly without forcing Wave-1 commands to evolve mid-flight.

## Inputs and outputs

**Inputs.**

- `docs/HANDOVERS.md` §"Handover 5" (PM Spec — `## Acceptance criteria` is the consuming section per F3.8 `templates/pm-spec.md`) and §"Handover 6" (Handoff Packet — `acceptance-criteria.md` aggregates per-Requirement). These name *where* EARS sentences live; the framework defines *what* they must look like.
- Mavin et al. (2009) "Easy Approach to Requirements Syntax (EARS)." Academic citation — quoted verbatim for each pattern's canonical form.
- `.claude/commands/draft-spec.md` (the consumer for the first integration milestone — referenced for context only; not modified in this spec). The "Which EARS pattern…?" prompt in Step 3 is the seam where the skill will eventually be dispatched.
- `.claude/skills/ost-validator/SKILL.md` and `.claude/skills/work-loop/SKILL.md` (precedent for SKILL.md shape — frontmatter, H1, "## When to use this skill", concrete invocation contract).
- `context/frameworks/ontology.md` (precedent for `context/frameworks/*.md` — no universal-metadata frontmatter; prose-only with H1 + intro blockquote + sections).
- `tools/lint-skill.sh` (the contract the new SKILL.md must pass).
- `tools/lint-frontmatter.py` (default mode walks `PHASE_DIRS = strategy/, discovery/, validation/, delivery/, market/` and does not walk `context/frameworks/`; the framework doc is therefore not subject to default-mode linting — same posture as `ontology.md`).

**Outputs.**

1. `context/frameworks/ears.md` — new file. Body outline (exact section order):
   - **H1** `# EARS — Easy Approach to Requirements Syntax`
   - **Intro blockquote** — one paragraph: what EARS is (Mavin et al., 2009; a constrained natural-language pattern for requirement sentences), why this kit uses it (downstream `/draft-spec` and `/handoff-packet` consume Requirement and Acceptance-Criterion sentences whose ambiguity has compounding cost), pointer to the consuming SKILL (`.claude/skills/ears-lint/SKILL.md`).
   - **H2** `## The five canonical patterns` — one H3 per pattern (Ubiquitous, Event-driven, State-driven, Optional-feature, Unwanted-behavior). Each H3 contains: the canonical sentence template (verbatim from Mavin et al.), one canonical example, a one-line "when to use" note, and a "common confusion" note (e.g., for Event-driven: "If the trigger is a sustained condition rather than a discrete event, the sentence is State-driven, not Event-driven").
   - **H2** `## The Complex combination form` — describes how multiple keywords combine (e.g., "When … while …" or "Where … if …"); one canonical example; classification rule (Complex = the sentence contains two or more EARS keywords from distinct pattern families).
   - **H2** `## Failure modes — how the pattern can be misused` — lists at minimum: (a) the sentence is a question, not a requirement; (b) the sentence states a goal or capability without naming the system actor and action ("The user should be able to log in" is not EARS); (c) the verb is "must" / "will" / "should" instead of "shall" — EARS requires "shall"; any other modal verb makes the sentence non-conformant (see Open Questions §2); (d) the sentence packs two requirements into one clause without the Complex form's explicit keywords; (e) the sentence is in the passive voice with "shall" but no named system actor ("An email shall be sent to the user…") — non-conformant because EARS requires the named system as the grammatical subject of the consequence clause.
   - **H2** `## How the kit uses this framework` — names the consumer skill (`.claude/skills/ears-lint/`) and the downstream commands (`/draft-spec`, `/handoff-packet`); names that the framework is the rule source and the skill is the rule consumer; explicitly states the framework does not restate the skill's classification procedure and the skill does not restate the framework's pattern definitions.
   - **H2** `## References` — Mavin et al. (2009) full citation; pointer to `docs/HANDOVERS.md` §"Handover 5" and §"Handover 6" as the kit's consuming surface.

   Total body ≤ 150 lines. No YAML frontmatter (matching the `ontology.md` precedent).

2. `.claude/skills/ears-lint/SKILL.md` — new file. Frontmatter (exact fields):
   ```yaml
   ---
   name: ears-lint
   description: <one-paragraph summary, ≤ 1024 chars — names the skill's input (one or more candidate requirement sentences), its output (a structured per-sentence verdict with pattern, rationale, suggested rewrite), the rule source (context/frameworks/ears.md), and the typical dispatch (per acceptance-criterion sentence in /draft-spec and per requirement in /handoff-packet). Includes the load trigger: invoked whenever the orchestrator needs to verify a candidate requirement sentence conforms to EARS.>
   license: MIT
   ---
   ```
   Body outline (exact section order):
   - **H1** `# ears-lint`
   - **Intro paragraph** — one paragraph: what the skill does, what it consumes (sentences), what it returns (verdicts).
   - **H2** `## When to use this skill` (required by `lint-skill.sh`):
     - Right after a Requirement or Acceptance Criterion sentence is drafted (typically by `/draft-spec` or `/handoff-packet`).
     - When auditing an existing PM Spec's `## Functional requirements` or `## Acceptance criteria` section for syntax conformance.
     - As a fan-out target when reviewing many sentences at once (each invocation handles one or more sentences; the orchestrator batches).
   - **H2** `## Invocation contract`:
     - **Input.** Either (a) one or more candidate sentences passed inline as text, OR (b) a path to a file the orchestrator names; the skill reads from the path and treats each non-empty line as one candidate sentence. The orchestrator is responsible for stripping bullet markup (`- `, `* `, leading numbers) before passing sentences. Multi-sentence acceptance criteria are split by the orchestrator before invocation (one EARS sentence per invocation slot) — see Open Questions §1 for the resolved rule. **Known failure modes of the orchestrator-side splitter** (the skill does not fix these; the orchestrator must handle them): sentence-final periods inside abbreviations (`Req.`, `Fig.`, `e.g.`), decimal numbers (`$1.00`), embedded URLs (`https://example.com`), and quoted strings that contain `;` or `.`. When the orchestrator cannot split unambiguously, it surfaces the bullet to the human rather than guessing.
     - **Output.** A structured verdict per sentence:
       ```
       sentence: "<the input sentence verbatim>"
       pattern: ubiquitous | event-driven | state-driven | optional-feature | unwanted-behavior | complex | non-conformant
       rationale: "<one short sentence — what keyword(s) or shape triggered the classification, or what's missing>"
       suggested_rewrite: "<EARS-conformant rewrite if pattern == non-conformant; null otherwise>"
       ```
     - **Exit conditions.** The skill always emits a verdict for each input sentence — there is no "skip" or "abort" state. If the orchestrator passed zero sentences, the skill returns an empty verdict list (no error).
   - **H2** `## Classification procedure` — names that `context/frameworks/ears.md` is the canonical rule source and the skill applies the patterns defined there in keyword-priority order: Unwanted-behavior (`If … then …`), Event-driven (`When … the … shall …`), State-driven (`While … the … shall …`), Optional-feature (`Where … the … shall …`), Ubiquitous (no leading keyword; `The … shall …`), Complex (two or more keywords from distinct families). A sentence with no `shall` (or that fails the Ubiquitous shape after keyword stripping) classifies as Non-conformant. Body cites the framework, does not restate pattern definitions.
   - **H2** `## Failure modes` — at minimum: sentence is a question (ends with `?`); sentence lacks `shall` (modal verb required); sentence uses "must" / "will" / "should" instead of "shall"; sentence packs two requirements without the Complex form's keywords; sentence is multi-clause prose, not a single requirement.
   - **H2** `## Examples` — at least one passing example per pattern (five canonical + one Complex), one failing example with the `suggested_rewrite` filled in, and an explicit non-EARS sentence (e.g., a question).
   - **H2** `## Files` — points to `references/fixture-sentences.md` as the manual-gesture verification fixture; names that the skill itself is prose-procedure (no bundled script today — runnable form is a deferred follow-up, tracked as an open question, not in scope for this spec).

   Body ≤ 200 lines. Passes `tools/lint-skill.sh`.

3. `.claude/skills/ears-lint/references/fixture-sentences.md` — new file. Approximately 11 candidate sentences with annotated expected classifications. Required coverage (each row is one sentence + expected pattern + one-line rationale):
   - 1× Ubiquitous (e.g., "The system shall log every API request.")
   - 1× Event-driven (e.g., "When a user submits the checkout form, the system shall validate the card details.")
   - 1× State-driven (e.g., "While the user is authenticated, the system shall display the dashboard.")
   - 1× Optional-feature (e.g., "Where multi-factor authentication is enabled, the system shall require a second factor.")
   - 1× Unwanted-behavior with explicit "then" (e.g., "If the payment gateway returns an error, then the system shall display a retry prompt.")
   - 1× Unwanted-behavior without explicit "then" (e.g., "If the user's session expires, the system shall redirect to the login page.") — forces a decision on the `If … shall …` form per the §"Always do" rule below.
   - 1× Complex (e.g., "When a user submits the checkout form, while the cart total exceeds $1000, the system shall require manager approval.")
   - 1× Non-conformant — question (e.g., "Should the system support guest checkout?")
   - 1× Non-conformant — missing "shall" / wrong modal verb (e.g., "The system must validate the email field.")
   - 1× Non-conformant — goal-style without system actor (e.g., "The user should be able to log in via SSO.")
   - 1× Non-conformant — passive-voice with "shall" but no named system actor (e.g., "An email shall be sent to the user on checkout completion.") — covers the most common PM drafting error after the modal-verb swap.
   - 1× Non-conformant — multi-requirement without Complex keywords (e.g., "The system shall validate the email and the system shall send a confirmation message.")

   Each row in markdown table form: `| # | Sentence | Expected pattern | Rationale |`.

A reader of this section should be able to write the framework body, the skill body, and the fixture rows without reading anything else.

## Boundaries

### Always do

- Quote Mavin et al. (2009) verbatim for the canonical sentence templates of all five patterns. The framework is a re-projection of the academic source, not a parallel rule definition.
- Keep `context/frameworks/ears.md` ≤ 150 body lines. The framework is one page of reference, not a tutorial.
- Keep the skill's body ≤ 200 lines and ensure it passes `tools/lint-skill.sh` (required frontmatter fields, H1 matching the skill name, "## When to use this skill" section, description ≤ 1024 chars).
- Cite `context/frameworks/ears.md` from the skill body as the rule source for every pattern classification; do not restate the patterns inside the SKILL.md.
- Classification procedure: a Complex pre-filter runs first (count distinct leading-pattern keywords from distinct pattern families; if two or more, classify Complex). Only if the pre-filter does not match, apply the single-keyword cascade Unwanted-behavior → Event-driven → State-driven → Optional-feature → Ubiquitous → Non-conformant. The pre-filter is load-bearing because Mavin's Complex form is unreachable under a pure sequential cascade — a sentence starting with `When` that also contains `while` would classify as Event-driven on the first match and never reach a Complex check. _Note: pre-EXECUTE iter-1 specified the order with Complex at the tail; post-EXECUTE iter-2 corrected this — see Changelog._
- Treat Unwanted-behavior's keyword as `If` alone — the literal "then" in Mavin et al.'s canonical template `"If <precondition>, then the <system> shall <response>"` is the canonical form, but the kit accepts the equivalent comma-only form `"If <precondition>, the <system> shall <response>"` as Unwanted-behavior. Rationale: in PM-authored requirements the comma-only form is far more common than the explicit `then`, and rejecting it would force ungrammatical rewrites for no semantic gain. The skill's classification procedure encodes this; the framework's Unwanted-behavior H3 names both forms.
- Record manual-gesture verification in `docs/specs/ears-lint/notes/manual-verification-2026-05-23.md` — sentence-by-sentence expected vs actual classification, with any discrepancies surfaced and resolved before VERIFY exits.

### Ask first

- Extending the skill to do anything beyond per-sentence classification (e.g., auto-rewriting non-conformant sentences in bulk, or modifying the source file in-place). Ask before scope-creeping into spec/handoff-packet authoring; the skill is a classifier only.
- Adding any modal verb beyond "shall" to the accepted vocabulary (the Open Questions resolve to shall-only; revisit only on a separate spec).
- Introducing a runnable Python implementation of the skill (e.g., `scripts/ears_lint.py`). Surface as a follow-up spec; out of scope for this wave per the Wave-2 plan.

### Never do

- Invent a sixth EARS pattern. The canonical academic source defines exactly five plus the Complex combination form. New patterns require a separate spec citing new academic precedent — not improvisation here.
- Modify `docs/HANDOVERS.md` or `docs/CONVENTIONS.md`. The framework and skill cite them; they are not authored here.
- Modify `.claude/commands/draft-spec.md` or any other Phase-4 command in this spec. The integration is a separate follow-up (a small `/draft-spec` patch to dispatch the skill after the EARS-pattern question in Step 3); calling it out here keeps the wave coupled to its stated scope.
- Add a new ontology object_type for "Framework Reference." Domain I is phase-boundary handover composites; framework-reference docs are kit-meta scaffolding (same posture as `context/frameworks/ontology.md`, which is itself the ontology source-of-truth and carries no frontmatter).
- Restate the Mavin pattern templates inside the skill body. The skill cites the framework; duplication causes drift.

## Verification mode

- **Goal-based check** for the framework doc — greps confirm all five pattern names appear, the Complex form section exists, and the file body is ≤ 150 lines.
- **Audit-driven** for the skill — `tools/lint-skill.sh .claude/skills/ears-lint/SKILL.md` exits 0.
- **Manual gesture** for the skill — in-session invocation against `.claude/skills/ears-lint/references/fixture-sentences.md`, with sentence-by-sentence expected-vs-actual matching recorded under `docs/specs/ears-lint/notes/manual-verification-2026-05-23.md`. (The fresh-session verifier loop is a deferred F1-G1-style follow-up; in-session manual gesture is the agreed VERIFY mode for the initial ship per the Wave-2 plan.) **Self-consistency limitation acknowledged:** because the same model instance authors the fixture's expected labels, the framework body, the skill's classification procedure, AND executes the gesture, the in-session pass primarily verifies that the three artifacts agree with each other (self-consistency), not that the classification procedure is independently correct on unseen inputs. The independent test — fresh-session execution against a fixture the executing model did not author — is the deferred follow-up. The mitigation inside this wave is that at least three fixture rows are sourced from PM-authored failure-mode patterns common in the wild (passive-voice-no-actor, `If` without `then`, modal-verb swap), increasing the chance that a procedure flaw surfaces in-session even with self-marking.
- **Audit-driven** for kit-wide health — `python3 tools/lint-frontmatter.py --all` exits 0 (no product-artifact regression); `bash tools/pre-pr.sh` exits 0.

## Contract tests

Each test is one shell line or one verifiable predicate. They are the gate.

- `T1` — `test -f context/frameworks/ears.md` (the framework doc exists).
- `T2` — `[[ $(wc -l < context/frameworks/ears.md) -le 200 ]]` (size cap with a 50-line cushion above the 150-line target — the cap exists to catch a runaway draft).
- `T3` — `[[ $(grep -c -E "^### (Ubiquitous|Event-driven|State-driven|Optional-feature|Unwanted-behavior)$" context/frameworks/ears.md) -eq 5 ]]` (all five canonical patterns named as H3 sub-sections, each appearing exactly once).
- `T4` — `[[ $(grep -c "^## The Complex combination form$" context/frameworks/ears.md) -eq 1 ]]` (Complex form section present).
- `T5` — `[[ $(grep -c "Mavin" context/frameworks/ears.md) -ge 1 ]]` (Mavin cited).
- `T6` — `test -f .claude/skills/ears-lint/SKILL.md` (the skill exists).
- `T7` — `bash tools/lint-skill.sh .claude/skills/ears-lint/SKILL.md` exits 0.
- `T8` — `test -f .claude/skills/ears-lint/references/fixture-sentences.md` (fixture exists).
- `T9` — `[[ $(grep -c "^| " .claude/skills/ears-lint/references/fixture-sentences.md) -ge 13 ]]` (header row + separator + ≥ 11 sentence rows after adversarial-review iter-1 added two coverage rows for passive-voice-no-actor and If-without-then).
- `T10` — Fixture coverage: the file contains at least one row whose Expected-pattern column matches each of {Ubiquitous, Event-driven, State-driven, Optional-feature, Unwanted-behavior, Complex, Non-conformant}. Verified by seven separate `grep -c` predicates inside the manual-verification note.
- `T11` — Manual-gesture pass: every fixture row's expected classification matches the in-session classification recorded in `docs/specs/ears-lint/notes/manual-verification-2026-05-23.md`. Discrepancies must be either (a) resolved by re-authoring the fixture row, (b) resolved by re-authoring the framework body to remove ambiguity, OR (c) explicitly documented in `notes/deferred-findings.md` with a stated reason — never silently dropped.
- `T12` — `python3 tools/lint-frontmatter.py --all` exits 0 (no regression in default-mode linting across the existing kit; the framework doc and SKILL.md sit outside `PHASE_DIRS` so they are not subject to default-mode lint).
- `T13` — `bash tools/pre-pr.sh` exits 0.
- `T14` — Spec/plan/state cleanup: spec.md status reads `Shipped (2026-05-23)` and plan.md status reads `Done (2026-05-23)` after CAPTURE; state.json is gitignored and not staged.
- `T15` — ROADMAP F4.12 and P4.7 both flipped to `[x]` with `**Shipped:** 2026-05-23` appended (mirrors the F4 row format used by P4.1 through P4.11).
- `T16` — INVENTORY has one row for `context/frameworks/ears.md` (REF, Phase 4 / Spec sub-section) and one updated row for the `ears-lint` skill (status flipped from `planned (P4.7)` to `shipped (2026-05-23)`).
- `T17` — AGENTS.md `## Skills available to you` section lists `ears-lint` without the `(planned — ROADMAP P4.7)` annotation; `.claude/skills/README.md` moves the `ears-lint` line from "Planned" to "Shipped".
- `T18` — `[[ $(grep -c "context/frameworks/ears.md" .claude/skills/ears-lint/SKILL.md) -ge 1 ]]` (the rule-source citation is present, satisfying the no-duplication rule between framework and skill).

## Non-goals

- Authoring a runnable Python implementation of the skill (`scripts/ears_lint.py`). Out of scope; tracked as Open Question §3.
- Modifying `/draft-spec` (P4.8) to dispatch the skill at the seam where the advisory EARS prompt currently lives. The integration is a separate follow-up spec; this wave ships only the framework and the skill.
- Adding mechanical EARS lint to `/handoff-packet` (P4.11) for the `acceptance-criteria.md` aggregation. Same posture as `/draft-spec` — separate follow-up.
- Adding a `pretooluse` or `posttooluse` hook that auto-invokes `ears-lint` on writes to `delivery/initiatives/*/specs/*.md` or `delivery/handoff-packets/*/acceptance-criteria.md`. Out of scope — hooks are F2 territory and require their own spec.
- Reconciling the other twelve F4 framework docs (F4.1–F4.11, F4.13). Each is its own spec; this wave ships F4.12 only.
- Authoring `templates/<slug>.md` for "EARS sentence" or anything similar. EARS is a *sentence-shape constraint*, not an artifact type; no template is needed.

## Open questions

1. **How should the skill handle multi-sentence acceptance criteria?** A `## Acceptance criteria` bullet can contain a compound sentence ("REQ-001: When the user clicks submit, the system shall validate the form; if validation fails, the system shall display an inline error."). _Resolved here: the orchestrator splits on `;` and `.` boundaries before invocation and passes each resulting sentence as a separate input; the skill operates on the one-EARS-sentence-per-slot rule. If a splitter is non-trivial in practice (e.g., the bullet contains a list), the orchestrator surfaces ambiguity to the human rather than guessing. Encoded in the skill's "Invocation contract" section under the orchestrator-responsibility note. This resolution intentionally keeps the splitter responsibility outside the skill so the skill stays a pure classifier._
2. **Should "shall" be required verbatim, or are "must"/"should"/"will" also accepted?** The canonical Mavin form uses "shall." _Resolved (enforcement deferred to `/draft-spec` integration patch): shall-only. Other modal verbs classify as Non-conformant with a suggested_rewrite that swaps the modal for "shall". Note in the framework's "Common confusion" entry for each pattern and in the skill's "Failure modes" section. Rationale: shall is the unambiguous deontic marker EARS adopted from formal-requirements practice precisely to avoid the modal ambiguity that "should" and "will" introduce in natural English. Loosening the rule would silently weaken the lint. **Enforcement gap:** today `/draft-spec` (P4.8) does not lint the modal verb used in the written Requirement; the shall-only rule is enforceable only when a future integration patch dispatches `ears-lint` against each Requirement after Step 3. Until that patch ships, the rule is documentary, not enforced. Surfaced in §"Non-goals" so this is not silently shipped as "lint complete."_
3. **Should a runnable Python implementation ship in this wave?** A `scripts/ears_lint.py` would let CI run lint without a model. _Resolved here: no. The skill ships as prose procedure first; a runnable form is a deferred follow-up. Tracking location: this wave records the follow-up in `docs/specs/ears-lint/notes/deferred-findings.md` with placeholder slug `script-ears-lint` (a future ROADMAP row can adopt this slug, mirroring the `ost-validator` precedent where the runnable `scripts/validate_ost.py` was queued as P2.8 under slug `script-ost-validator`). The skill's "Files" section names this explicitly so a future spec can pick it up without re-deriving context._
4. **How is the skill dispatched by `/draft-spec` (P4.8)?** _Resolved here as scope-boundary only: not dispatched in this wave; tracked as a follow-up. The skill's "When to use this skill" section names `/draft-spec` and `/handoff-packet` as the eventual consumers; the consumers themselves are not modified here. This explicitly avoids the Wave-2 trap of partially specifying P4.8 to ground the contract — the contract grounds itself by being concrete enough that any consumer can call it without re-deriving anything._

## Acceptance criteria

- [ ] `context/frameworks/ears.md` exists, matches the §"Inputs and outputs" output-1 outline, names all five canonical patterns (Ubiquitous, Event-driven, State-driven, Optional-feature, Unwanted-behavior) and the Complex combination form, cites Mavin et al. (2009), and is ≤ 150 body lines.
- [ ] `.claude/skills/ears-lint/SKILL.md` exists, matches the §"Inputs and outputs" output-2 outline, declares `name: ears-lint`, `description:` (≤ 1024 chars), and `license:` in YAML frontmatter, passes `tools/lint-skill.sh`, and cites `context/frameworks/ears.md` by path at least once.
- [ ] `.claude/skills/ears-lint/references/fixture-sentences.md` exists with ≥ 10 rows covering all seven verdict labels at least once.
- [ ] Manual-gesture verification recorded at `docs/specs/ears-lint/notes/manual-verification-2026-05-23.md`, with every fixture row's expected classification matching the in-session classification (or discrepancies explicitly resolved per T11).
- [ ] All contract tests pass: T1–T18.
- [ ] ROADMAP F4.12 and P4.7 flipped to `[x]` with `**Shipped:** 2026-05-23`.
- [ ] INVENTORY rows added for the framework and the skill (skill row updated, framework row inserted).
- [ ] AGENTS.md skill list flipped to shipped (no `(planned — ROADMAP P4.7)` annotation).
- [ ] `.claude/skills/README.md` moves `ears-lint` from "Planned" to "Shipped".
- [ ] No new ontology object_type introduced; no Phase-4 command modified; no hook added.

## Cross-references

- **Consumed by:** `/draft-spec` (P4.8, shipped — advisory EARS prompt today; mechanical lint will be wired by a separate follow-up spec); `/handoff-packet` (P4.11, shipped — `acceptance-criteria.md` aggregation will benefit similarly); any future spec/handoff-packet authoring command.
- **Consumes:** `docs/HANDOVERS.md`, Mavin et al. (2009) academic source, `.claude/skills/work-loop/SKILL.md` (loop doctrine), `tools/lint-skill.sh` (linter contract).
- **Frontmatter fields owned:** none. The framework doc is un-frontmatter-ed (matches `context/frameworks/ontology.md`); the SKILL.md uses the existing skill frontmatter schema (`name`, `description`, `license`).
- **Ontology object types touched:** none directly. EARS is a syntax constraint on Requirement and Acceptance Criterion sentences (both Domain E); the framework reference does not instantiate a new type, and the skill does not create or modify Domain-E objects — it classifies their *text*.
