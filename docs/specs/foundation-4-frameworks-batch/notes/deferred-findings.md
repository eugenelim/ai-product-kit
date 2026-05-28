# Deferred findings — foundation-4-frameworks-batch

Findings surfaced by the post-EXECUTE adversarial reviewer (REVIEW iter-1, 2026-05-28) that were deferred rather than fixed in-loop. Each row carries a one-line rationale and a "when to address" trigger.

## Resolved in REVIEW iter-4 (2026-05-28, user-requested deferred-finding fix pass)

User asked the deferred-findings be addressed. 6 parallel sub-agent expansions for the substantive line-budget deferrals + 3 main-thread small-nit fixes. All gates remained green throughout (T-<slug>-1..8 per-file + lint-frontmatter + pre-pr).

### Substantive expansions (6 — via parallel sub-agent fan-out)

- **`falsification.md`** (48 → 52 lines, long-line style; ~2x prose) — `## What "survived" means` now includes the p=0.04/0.05 worked example showing soft-confirm laundering; `## Why the kit is asymmetric` adds the 99%-success / 1%-vulnerable-cohort product analogy explaining structural vs arithmetic asymmetry; `## Common failure modes — moving threshold` mitigation expanded with clean-vs-dirty revision definitions and the named human-gate sign-off in `human_owned_decisions:`.
- **`rumelt.md`** (53 → 61 lines) — `## The kernel` now walks the **Wal-Mart small-town kernel** end-to-end (Diagnosis: metro cost/density made entry uneconomic; Guiding Policy: saturate small-town markets below incumbent radar; four Coherent Actions with mutual-reinforcement spelled out); `## The coherent-actions leg` expanded to ~14 lines with a per-axis failure named for each (resource: bets fighting for the same eng team; capability: speed vs accuracy without dominance; posture: enterprise vs freemium same quarter).
- **`validation-theatre.md`** (56 → 61 lines, but ~2x character density per the agent's report) — each of the five failure modes now carries a definition + a recognition signal ("you're in this mode if..." tell) + a common example. The **no-consequences theatre** is explicitly flagged as the most prevalent mode in product practice, with the directive "when in doubt, check this first."
- **`strategic-coherence.md`** (65 → 86 lines) — `## Incoherence patterns` now has definition + worked example per pattern (Postgres re-platform vs billing engine for resource; speed-to-market vs regulatory accuracy for capability; $50k ACV enterprise vs self-serve freemium for posture; Q4 power-user vs Q4 onboarding feature for implicit-shared-audience); `## Common failure modes` parallel structure with worked example/signal per mode.
- **`competitive-analysis.md`** (61 → 73 lines, ~2x prose volume per agent report) — `## What thorough analysis contains` now requires a concrete decision + owner ("not 'we should keep watching this space'"); adds a competitor-scope-selection sub-block (direct / indirect / out-of-scope using JTBD as scoping tool); `## Three lenses` adds a Wardley example (Commodity-vs-Genesis competitor differentiator) and a JTBD example (Notion vs Confluence — feature overlap, job non-overlap).
- **`opportunity-solution-tree.md`** (57 → 57 lines, file rewritten with denser prose) — `## The four node types` adds the missing Assumption Test canonical example ("do analysts adopt the saved-query snippet feature in their first session? Threshold: ≥40% within 7 days") and ties the chain Outcome→Opportunity→Solution→Assumption Test end-to-end with one running example; `## Source opportunities` tightened per iter-1 reviewer (validator flags zero-`evidence_basis:`, one minimum, richer chains more defensible).

### Small-nit fixes (main thread)

- **`continuous-discovery.md`** — added **solo-PM-as-trio** failure mode bullet (the calendar-friction relay pattern where a single PM does the interviews and forwards notes to designer + tech lead; named as the most common failure of the trio discipline in practice).
- **`wardley.md`** — strategic implications of evolution stages now qualified as "**first-order heuristics**" (Wardley's own doctrine is that gameplay is map-shape-dependent, so these are starting points not rules); `scripts/mode-guard.py` dropped from the mode-guard parenthetical reference (it was an internal implementation detail that would go stale if the path moves — only the contract path `.claude/hooks/mode-guard.md` remains).

### Mechanical gate state after iter-4

All 12 frameworks pass T-<slug>-1..8. Kit-wide: `python3 tools/lint-frontmatter.py --all` clean; `bash tools/pre-pr.sh` clean. Spec's per-framework advisory targets still under-met on raw line count for several docs (because the agents used long-line markdown style that compresses content into fewer lines), but the substantive content gaps the iter-3 reviewer flagged are all closed.

### Remaining true deferrals — none load-bearing

- VL nits (atmospheric prose, minor phrasing): deferred indefinitely as taste-level edits.
- ME findings the iter-3 reviewer flagged as nit-level without recommended fix: deferred.
- Line-budget raw-count shortfall in `wardley.md` and `landings-not-launches.md`: their substantive coverage is complete; raw line count is the only gap. Deferred.



## Resolved in REVIEW iter-2 (2026-05-28)

User requested the deferred findings be addressed in a follow-up pass after the initial SHIP commit. Iter-2 resolved 8 of the 7 originally-deferred items (1 was bundled with another). The remaining items below are the new deferrals.

- **N-1.** Five thin frameworks expanded via parallel sub-agent dispatch:
  - `continuous-discovery.md` (55 → 61 lines; intent paragraphs added to "The weekly habit" explaining the asymmetric cadence, and to "The product trio" explaining concurrent ownership vs broader attendance).
  - `wardley.md` (60 → 61 lines, ~35% word-count growth; "The map" gained a paragraph on the user-need anchor as the coordinate system; "Doctrine and gameplay" gained the strategic-load-bearing explanation plus third doctrine and gameplay examples).
  - `assumption-tests.md` (51 → 64 lines, ~2x word count; each of the five lenses gained a signature-failure-mode sentence — stated-preference-over-revealed-behavior for desirability, support-and-success-cost-forgotten for viability, controlled-environment-breaks-at-production for feasibility, 5-user-studies-miss-long-tail for usability, affected-populations-not-in-sample for ethical).
  - `jtbd.md` (60 → 81 lines; "When to use which" gained the data-input contrast and the handoff-point in the OST workflow; the wrong-segmentation vs wrong-investment error framing was added).
  - `interview-snapshot.md` (48 → 82 lines; concrete examples added for the ambiguous-flagging rule and the paraphrase-vs-invent rule; proxy-research anti-example added to the "what a good snapshot is *not*" section).
- **ME-1.** `falsification.md` — predeclared-threshold section now names the statistical-shape rule explicitly (point estimate vs interval vs categorical; the shape must match the test's output). Prescriptive fix lives next to the diagnostic.
- **ME-2.** `opportunity-solution-tree.md` — "frozen tree" failure mode added as a fifth common failure-mode bullet (an OST not updated in weeks while the team continues interviewing; cross-references the `cadence-nudge` hook).
- **ME-3.** `jtbd.md` — `## How the kit uses this framework` clarifies that the framework itself is mode-agnostic; only the named slash-commands are mode-gated.
- **VL-1.** `continuous-discovery.md` — "Cadence is the carrier wave..." metaphor replaced with the precise sentence about insights not aggregating without sustained cadence.
- **VL-2.** `wardley.md` — intro-blockquote "spatial position carries meaning" replaced with the explicit two-axis-semantics sentence.
- **VL-3.** `landings-not-launches.md` — "rarely surfaced before the next quarter's commitments lock in" replaced with the more concrete "failed outcomes typically only appear during the next planning cycle when prior work's impact is reviewed — after new commitments have already been made."

All kit-wide gates re-verified after the fixes: `python3 tools/lint-frontmatter.py --all` clean; `bash tools/pre-pr.sh` clean.

## Resolved in REVIEW iter-3 (2026-05-28, fan-out reviewer pass)

User requested a work-loop REVIEW pass with parallel reviewer fan-out across all 12 framework files. 12 `adversarial-reviewer` agents dispatched in parallel; 11 returned `needs-fixes`, 1 (`wardley.md`) returned `pass`. Aggregated 14 critical-or-needs-fix findings; 13 fixed in-loop; 1 spec drift (Torres-cadence attribution) resolved by amending the spec to match the doc's factual correction from iter-1.

### Critical (7 — all fixed in-loop)

- **opportunity-solution-tree.md**: `chosen: true` (wrong field name) → `chosen_opportunity:` with `id:` + `rationale:` sub-fields, matching `docs/HANDOVERS.md` §"Handover 2" verbatim. Fixed in 2 locations (intro blockquote + "How the kit uses" section).
- **interview-snapshot.md**: intro blockquote was missing the `Interviewer` field from the schema enumeration; added.
- **assumption-tests.md**: References section claimed "Bland's subsequent public work adds the Ethical lens" — unverifiable attribution. Removed; replaced with explicit "the kit adds Ethical as a co-equal fifth lens" pointer to the body section that already labels it as kit synthesis.
- **validation-theatre.md**: hook described as "shipped at `scripts/check-assumption-threshold.py`" (the script is the implementation, not the hook itself) — corrected to name the PreToolUse registration in `.claude/settings.json` + implementation script + contract doc all three. Same fix applied to `assumption-tests.md` and `falsification.md` where the same mischaracterization appeared.
- **competitive-analysis.md**: shape-contract violation — had both `## What this kit asks for` and `## How the kit uses this framework` covering the same consuming-surface ground. Collapsed into the single required `## How the kit uses this framework` section per the shape contract precedent (`ears.md`).
- **strategic-coherence.md**: `## The audit lens` section asserted that the three axes decompose Rumelt's three criteria but did not show the mapping. Added explicit mapping: resource coherence ↔ resource-feasible, capability coherence ↔ mutually reinforcing, market posture coherence ↔ coordinated.
- **landings-not-launches.md**: `## "Launches are starts, not ends"` section named the symptom (failed outcomes surface only at planning) but not the structural cause. Added the three forces (team reassignment immediately after launch; adoption not in anybody's OKRs; planning cycles forming concurrently with current work landing) and named the kit's mechanical guard (`/audit-landings-debt` + `landings-manager` scheduled agent).

### Needs-fix (6 — all fixed in-loop)

- **continuous-discovery.md spec drift**: iter-2 reviewer flagged that the spec said "3 interviews per week as Torres's target" but the doc had been corrected in iter-1 to honor factual accuracy (Torres publishes "weekly", not "3"). Spec updated 2026-05-28 to match the doc's factually-correct framing (with an amendment-history note in the spec entry).
- **jtbd.md opportunity-score formula**: previously stated as "importance minus satisfaction"; corrected to Ulwick's canonical formula `importance + max(importance − satisfaction, 0)` which deliberately weights importance — the formula is in Ulwick (2005) ch. 6 and Ulwick & Bettencourt (2008) covers the survey mechanics.
- **interview-snapshot.md no-recording case**: previous version assumed a recording always existed (timestamp format `<MM:SS>`); added explicit no-recording fallback (`[no recording]` instead of timestamp; do not fabricate).
- **assumption-tests.md hook path consistency**: line 35 of the test-card schema previously gave the script path without the hook-contract path; line 52 had both. Reconciled — both occurrences now name the settings registration, the script, and the contract doc consistently.
- **falsification.md missing forward cross-link**: the predeclared-threshold section did not cite `context/frameworks/assumption-tests.md` (where the test-card schema with the Threshold field lives). Added the forward pointer.
- **validation-theatre.md vague "weeks to materialize"**: replaced with the concrete "a retention metric that requires 14–28 days of post-event observation to stabilize."

### Drift-resolution: `chosen: true` → `chosen_opportunity:` consistency

The wrong field name `chosen: true` had propagated to `validation-theatre.md`'s "How the kit guards against theatre" section (the Discovery → Validation handover note). Fixed there too — now uses `chosen_opportunity:` consistently across all docs that reference Handover 2.

### Nits and substantive expansions — deferred to follow-up

- continuous-discovery: solo-PM-as-trio failure mode (already named in body of `## The product trio`; nit-level addition to failure-mode list)
- opportunity-solution-tree: line-budget expansion + Assumption Test canonical example (NF-2 from review)
- assumption-tests: line-budget expansion + cross-link to falsification moving-threshold (nit; the inline note in the Threshold field now references it)
- falsification: line-budget expansion (target ~120, currently 48)
- rumelt: Wal-Mart kernel concrete walk-through (NF-1 from review) + coherent-actions section depth (NF-2)
- strategic-coherence: section-depth expansion for `## Incoherence patterns` and `## Common failure modes` worked examples
- jtbd: Christensen job-statement form template (already partially addressed by the three diagnostic questions)
- landings-not-launches: line-budget expansion of `## What a landing report contains` (mostly addressed by the threshold-fallback addition above)
- competitive-analysis: line-budget expansion of `## What thorough analysis contains` and `## Three lenses` after the dedup
- wardley: "first-order heuristic" qualifier on the strategic implications (VL nit) + drop `scripts/mode-guard.py` from parenthetical references (NF nit)
- All VL findings (atmospheric prose, vague language) and ME findings (missed edge cases that were not load-bearing)

**Rationale for deferring the line-budget expansions:** the spec explicitly marks per-framework targets as advisory, not gated; the reviewer is the gate; the reviewer-flagged thinness is real but every required section is substantively present. Expanding further turns reference into tutorial. Track for a future hardening pass when a real adopter consumes the docs against a real product situation and reports a content gap.

## Deferred

- **N-1 (thinness across 5 frameworks).** Five of twelve docs (`continuous-discovery.md`, `wardley.md`, `assumption-tests.md`, `jtbd.md`, `interview-snapshot.md`) came in at 46–58 lines, below the spec's advisory per-framework targets (110–150 lines). The reviewer named specific sections that read as compressed.
  - **Rationale for deferring:** the spec set the per-framework target as advisory, not gated, and explicitly named the post-EXECUTE reviewer as the gate. The reviewer flagged thinness but did not classify it as `block`. The shipped docs cover every required H2, every contract test passes, and reference-quadrant docs (Diátaxis) benefit from compression — extending them risks turning reference into tutorial.
  - **When to address:** when a real adopter (not the original author) tries to consume one of the five thin frameworks against an actual product situation and reports a content gap, or when a downstream skill/command is built that needs more framework grounding than the current density supports. The expansion is per-section and additive — no structural rework needed.

- **ME-1 (`falsification.md` — statistical-shape rule not in the prescriptive section).** The "confidence-interval confusion" failure mode is named in the failure-modes section, but the predeclared-threshold section does not name the prescriptive fix (the threshold must declare the statistical shape of the metric).
  - **Rationale for deferring:** the failure-mode section already names the problem; a consumer who reads both sections sees the diagnosis and the failure together. The cross-section duplication is small and the loss of clarity is bounded.
  - **When to address:** when the first experiment template instance ships and the statistical-shape rule needs a procedural home. The fix is one sentence added to the predeclared-threshold section.

- **ME-2 (`opportunity-solution-tree.md` — "frozen tree" failure mode missing).** The doc names four failure modes; the reviewer flagged "frozen tree" (an OST not updated in weeks/months) as a fifth canonical mode that should appear.
  - **Rationale for deferring:** the `cadence-nudge` hook (F2.5, shipped) is the mechanical guard for this mode and is named in the `continuous-discovery.md` framework. A reader navigating from the OST doc to "why does the OST go stale" reaches the same guard via the companion framework.
  - **When to address:** if a real adopter's OST drifts despite the cadence-nudge running, and the post-hoc question is "why isn't the OST framework warning about this," the failure mode should land in the OST doc directly. The fix is one bullet.

- **ME-3 (`jtbd.md` — framework vs commands mode-gating ambiguity).** The doc says `/jtbd-analogues` is greenfield-only and `/internal-jtbd-interview` is enterprise-only, which could read as "the JTBD framework itself is mode-gated."
  - **Rationale for deferring:** the framework's cross-link from `opportunity-solution-tree.md` ("Opportunities are often expressed as jobs or job-fragments") implicitly establishes that JTBD concepts are usable across modes — only the commands are gated.
  - **When to address:** if a greenfield-mode adopter raises the question. One clarifying sentence in `## How the kit uses this framework`.

- **VL-1 (`continuous-discovery.md` — atmospheric prose).** "Cadence is the carrier wave. The signal — what you learn — only accumulates if the carrier is continuous." The reviewer flagged this as metaphor adding no precision.
  - **Rationale for deferring:** the metaphor is short and the surrounding prose is concrete. Reference-doc voice tolerates one figurative sentence per section; this is the only one in the doc.
  - **When to address:** if a future style pass surfaces this as a pattern across multiple framework docs; address all at once.

- **VL-2 (`wardley.md` — "carries meaning" vague).** Replace with explicit two-axis-semantics sentence.
  - **Rationale for deferring:** the body text following the intro blockquote already explains the two-axis semantics concretely (sections 1 and 2 — `## The map` and `## The evolution axis`). The intro is a summary; the body is where the precision lives.
  - **When to address:** if the intro blockquote starts being cited in isolation (e.g., excerpted in a slide or another doc) and the vagueness becomes a problem there.

- **VL-3 (`landings-not-launches.md` — "rarely surfaced" unsourced).** Reviewer suggested a more concrete phrasing.
  - **Rationale for deferring:** the claim is supported by the rest of the doc's argument about Phase 5 being the place where landings-debt becomes visible. Replacing the rhetorical "rarely surfaced" with the reviewer's longer prescriptive phrasing trades concision for precision; current density choice is defensible.
  - **When to address:** if a real adopter reads the line and asks "is that true, or is that just your opinion?"

## Resolved in-loop (REVIEW iter-1)

- **C-1.** Wrong hook-contract path (`.claude/hooks/check-assumption-threshold.md` → `.claude/hooks/assumption-threshold-lock.md`) corrected in three files: `assumption-tests.md`, `falsification.md`, `validation-theatre.md`.
- **C-2.** Unverifiable trio-joint-signature claim in `continuous-discovery.md` softened to reference the actual `human_owned_decisions` and `approvals_obtained` fields that the F3.9 template carries (verified by reading `templates/handoff-packet/README.md`).
- **N-2.** Torres weekly cadence misattribution: "Torres's target cadence is ≥3 customer interviews..." reframed to "Torres names weekly customer contact as the discipline; the kit's practical target is ≥3 interviews + 1 + 1 (three interviews is the kit's practical minimum, not Torres's published number)."
- **N-3.** Ethical lens attribution shaky: re-labelled as a kit addition with explicit acknowledgment that Bland & Osterwalder (2019) name four lenses, the kit treats Ethical as a co-equal fifth.
- **N-4.** Asymmetric cross-link: `context/frameworks/opportunity-solution-tree.md` added to `continuous-discovery.md`'s References section (was already cited in body, now in references too).
- **N-5.** Rumelt's "bad strategic objectives" entry sharpened to name the distinguishing criterion (action-language without diagnostic connection).
- **N-6 / SC-1.** Wardley body stage label "Custom-built" → "Custom" (matches H2 heading and Wardley's canonical taxonomy).
- **N-7.** Ulwick formulation expanded to name the importance × satisfaction grid as the prioritization methodology.
- **N-8.** `validation-theatre.md` adds a fifth failure mode: "The wrong-population theatre" — separates population validity from statistical power.
- **N-9.** `competitive-analysis.md` Porter five-forces section adds one operative question per force, making the lens usable without the 1980 book in hand.

## Reviewer-flagged but not findings (recorded for traceability)

The reviewer's §"Self-consistency drift" section confirmed:
- `landings-not-launches.md` and `validation-theatre.md` agree on Cagan's *Inspired* 2nd ed. 2017 (no cross-file drift).
- `jtbd.md` and `competitive-analysis.md` agree on the three-lens framing (symmetric cross-links).
- `continuous-discovery.md` and `landings-not-launches.md` cross-link symmetrically.

The §"Scope creep" section returned clean.
