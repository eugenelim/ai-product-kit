# Deferred findings — foundation-4-frameworks-batch

Findings surfaced by the post-EXECUTE adversarial reviewer (REVIEW iter-1, 2026-05-28) that were deferred rather than fixed in-loop. Each row carries a one-line rationale and a "when to address" trigger.

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
