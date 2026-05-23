# Deferred findings — ears-lint

Items surfaced during this work-loop but explicitly deferred to a separate spec or wave.

## Open Question §3 — runnable Python implementation

**Status:** deferred to a future ROADMAP row. Placeholder slug: `script-ears-lint`.

**Context:** Open Question §3 in `spec.md` resolved "no runnable Python implementation in this wave" and named this notes entry as the persistent tracking location. The precedent is `ost-validator`, which shipped as a prose skill first and queued the runnable form as ROADMAP P2.8 under slug `script-ost-validator`. A future spec can adopt the `script-ears-lint` slug, copy the analogous P2.8 framing (`scripts/ears_lint.py` against a copy of the fixture file), and ship without re-deriving context from this spec.

**Why deferred:** the prose skill is sufficient for the current dispatch surface (model-executed classification inside `/draft-spec` and `/handoff-packet`). A runnable form is justified only when CI or a hook needs model-free lint, which is not yet a present requirement.

## Pre-EXECUTE adversarial-reviewer iter-1 finding E3 — no negative test for skill restating pattern definitions

**Status:** deferred to post-EXECUTE Task 6 (adversarial review) per the reviewer's recommendation.

**Context:** T18 verifies the skill cites `context/frameworks/ears.md` at least once, but no contract test verifies the skill does *not* also restate the Mavin pattern templates. The "Never do" boundary forbids restatement; the post-EXECUTE adversarial reviewer is the agreed enforcer.

**Why deferred:** adding a contract test for absence of duplication is a heuristic (e.g., `grep -c "shall"` in the skill body vs the framework body) and would be more brittle than the post-EXECUTE review pass that reads both files end-to-end.

## `/draft-spec` and `/handoff-packet` integration patches

**Status:** deferred. Each is its own follow-up spec.

**Context:** `/draft-spec` (P4.8, shipped 2026-05-23) has an advisory EARS prompt at Step 3 with no mechanical lint; `/handoff-packet` (P4.11, shipped 2026-05-23) aggregates per-Requirement acceptance criteria without lint. Both will dispatch `ears-lint` once a separate integration patch is authored. The skill's invocation contract is concrete enough that the patches can be written without re-deriving anything from this spec.

**Why deferred:** modifying shipped Phase-4 commands mid-wave was explicitly forbidden by the spec's "Never do" boundary to keep the wave coupled to its stated scope (framework + skill only).
