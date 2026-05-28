# Plan: phase-2-discovery-audits-and-comms

- **Spec:** [`spec.md`](./spec.md)
- **Status:** Done
- **Plan review:** approved (set by `tools/check-done.py --phase plan`)

> **Plan contract.** Implementation strategy for shipping P2.11, P2.12, P2.14 in a single coupled work-loop. Each component is a markdown file under `.claude/commands/`. No code dependencies between authoring tasks.

## Approach

**Stage 1 — Verify ontology types.** Before authoring, confirm whether `Stakeholder Update` (for the digest) and `Audit Report` (for the audit) are present in `context/frameworks/ontology.md`. If present, use them as `object_type` directly; if absent, use the `| Adapted` escape hatch (`Insight | Adapted` for digest; `Opportunity | Adapted` for audit). This is a 30-second grep before authoring; it determines the frontmatter pre-fill in T1 and T3.

**Stage 2 — Parallel authoring of three commands.** Each consumes `.claude/commands/_meta/command-skeleton.md` as the shape exemplar. Authoring is fully parallel-safe (no cross-references between command files at runtime; the spec's cross-references are downstream, in Phase 3 / future ROADMAP items). Per Batch B's experience, author directly rather than dispatching subagents (sandboxing issues from Batch A).

**Stage 3 — Verify + Review + Capture.** `tools/pre-pr.sh` gates verify; adversarial-reviewer runs post-EXECUTE for drift / missed cases; ROADMAP / INVENTORY captures.

## Constraints

- **No new scripts.** Authoring-only batch.
- **No edits to existing kit components** beyond the ROADMAP, INVENTORY, and the spec-flip captures.
- **F4 convention compliance.** Each command follows `.claude/commands/_meta/command-skeleton.md`.
- **Body cap.** Target ≤ 300 lines per command file.
- **Date discipline.** `Shipped:` timestamps use 2026-05-28.
- **Branch hygiene.** Work continues on `eugenelim/phase-2-batch-c`.

## Construction tests

Cross-cutting checks (not specific to one task):

- `tools/pre-pr.sh` exits 0 across the whole repo at the end of EXECUTE.
- For each command body: a grep confirms (a) the NEXT chain line is present (or, for `/discovery-update`, an explicit "no NEXT" note), (b) `lint-frontmatter.py` is invoked in Step 5, (c) the F4 Step pattern is followed (numbered Steps 1–6 minimum), (d) the body uses `<repo-root>` path-resolution language for any script invocation.
- For `/audit-discovery-coherence`: a grep confirms each of the five rule anchor phrases ("OST → parent intent", "Intent → downstream OST", "OST `chosen_opportunity:` resolution", "Opportunity → snapshot evidence", "Outcome alignment") appears.
- For `/opportunity-narrative`: a grep confirms the body says "chosen_opportunity" and refuses to draft without it.
- For `/discovery-update`: a grep confirms the body documents "no activity" handling AND the "no NEXT — digest is terminal" posture.

## Tasks

T1, T2, T3 are fully parallelizable.

### Task T1: ship `.claude/commands/audit-discovery-coherence.md`

- **Depends on:** Stage 1 ontology verification.
- **Tests:**
  - `tools/lint-command.sh` exits 0.
  - Body contains the five rule headings (mechanical grep).
  - Body declares verdicts `clean | drift | broken | insufficient-data` with corresponding exit codes 0/1/2/3.
  - Body documents the "shell out to `scripts/audit-discovery-coherence.py` if it exists, prose-fallback otherwise" pattern per F1.4 precedent.
- **Approach:**
  - Use `.claude/commands/audit-traceability.md` as the shape exemplar (it's the kit's prior-art audit command).
  - Frontmatter `description` ≤ 1024 chars; `argument-hint: "[scope] [--format {markdown,json,human}] [--write]"`.
  - Procedure: (1) scope the audit (resolve `all` / `<intent-slug>` / `<ost-slug>`), (2) attempt script shell-out at `<repo-root>/scripts/audit-discovery-coherence.py`, fall through to prose if absent, (3) walk the five rules — for each, list violations with artifact path + rule-violation type, (4) compute verdict per the rule-severity table, (5) emit report in chosen format, (6) when `--write` is set, persist to `<repo-root>/docs/audits/discovery-coherence-<YYYY-MM-DD>.md` and append a log entry, (7) emit `NEXT:` based on findings — `/update-ost <slug>` for broken-evidence rule violations, `/opportunity-narrative <slug>` for clean OSTs with `chosen_opportunity:` set but no narrative, or no NEXT for `clean` with nothing actionable.
  - `## What this command will not do`: never silently skip a rule on missing inputs; never return `clean` on `insufficient-data`; never auto-mutate the artifacts it audits.
- **Done when:** file exists; lint exits 0; grep checks pass.

### Task T2: ship `.claude/commands/opportunity-narrative.md`

- **Depends on:** none.
- **Tests:**
  - `tools/lint-command.sh` exits 0.
  - Body explicitly enforces "no chosen_opportunity → no narrative" (mechanical grep).
  - Body emits `NEXT: /assumption-test` (planned — P3.1).
  - Body walks the five H2 sections (The customer / The pain / Why this, why now / What we're betting / Open questions for Validation) one at a time.
- **Approach:**
  - Use `.claude/commands/draft-vision.md` as the shape exemplar (it's the kit's prior-art handover-narrative command, also five H2 sections, also a Validation-adjacent artifact).
  - Frontmatter `description` ≤ 1024 chars; `argument-hint: <slug> --from <ost-slug> [--force]`.
  - Procedure: (1) resolve the parent OST via the F4 candidate-listing rule, refuse if `chosen_opportunity:` is empty (anti-prematurity guard), (2) instantiate the narrative file at `<repo-root>/discovery/opportunities/narratives/<slug>.md` with frontmatter pre-fill, (3) load the chosen opportunity's `evidence_basis:` snapshots and surface the customer-voice content for the human's review, (4) walk the five H2 sections one at a time; cite at least one Direct Quote in H2 "The pain"; refuse to fabricate quotes (surface the gap if no quote is available), (5) surface `human_owned_decisions:` (the narrative will be read by the Validation team — confirm it faithfully represents the snapshots), (6) lint, (7) emit `NEXT: /assumption-test <slug>` (planned — P3.1).
  - `## What this command will not do`: never draft against an OST without `chosen_opportunity:`; never fabricate Direct Quotes; never silently extrapolate beyond what the snapshots support.
- **Done when:** file exists; lint exits 0; grep checks pass.

### Task T3: ship `.claude/commands/discovery-update.md`

- **Depends on:** Stage 1 ontology verification.
- **Tests:**
  - `tools/lint-command.sh` exits 0.
  - Body explicitly handles the "no activity since `--since`" case with the cadence-drift surface (mechanical grep).
  - Body documents "no NEXT — digest is terminal" (mechanical grep).
  - Body covers the six H2 sections (Headline / By the numbers / What changed in the OST / What we learned / What's blocking / Next week).
- **Approach:**
  - Use `.claude/commands/audit-traceability.md` as the shape exemplar for the stdout-vs-`--write` distinction.
  - Frontmatter `description` ≤ 1024 chars; `argument-hint: "[scope] [--since <YYYY-MM-DD>] [--for {exec,eng-lead,design-lead,support,all-hands}] [--write]"`.
  - Procedure: (1) resolve scope + `--since` window (default 7 days ago), (2) walk `<repo-root>/discovery/snapshots/`, `<repo-root>/discovery/opportunities/`, `<repo-root>/discovery/trees/*-change-set-*.json` for activity in the window, (3) if no activity, emit the cadence-drift headline and link to `cadence-nudge` (do NOT produce a "nothing happened" digest), (4) otherwise compose the six H2 sections per the spec, with role-specific tone hints per `--for`, (5) when `--write` is set, persist to `<repo-root>/discovery/updates/<YYYY-MM-DD>-<scope>.md` with frontmatter pre-fill, (6) lint when persisted, (7) explicit note in the body: "no NEXT — digest is terminal; humans share with stakeholders."
  - `## What this command will not do`: never produce a "nothing happened, all good" digest on quiet weeks; never auto-publish; never invent activity not surfaced from the artifacts.
- **Done when:** file exists; lint exits 0; grep checks pass.

## Rollout

- `tools/pre-pr.sh` picks up the new commands automatically.
- `docs/INVENTORY.md` Phase-2 table: flip the 3 rows from `planned (P2.x)` to `shipped (P2.x, 2026-05-28)`.
- `ROADMAP.md`: mark P2.11, P2.12, P2.14 `[x]` with shipped dates. **This completes Phase 2.**
- `AGENTS.md` and `.claude/CLAUDE.md`: not edited (no policy change).
- New directories created on first command run (not at authoring time): `discovery/opportunities/narratives/`, `discovery/updates/`, `docs/audits/`. These follow the kit's "directories appear when artifacts land" convention.

## Risks

- **Ontology-type uncertainty.** If `Stakeholder Update` or `Audit Report` are absent from the ontology, the `| Adapted` escape hatch absorbs the gap — but the command body must name the chosen `object_type` precisely (no placeholder). Stage 1 mitigation: verify before authoring.
- **F4 convention drift.** Three new commands; risk of subtle drift. Mitigation: each task's Tests bullet enumerates the convention checks; the verify gate catches drift before review.
- **Audit prose vs script ambiguity.** Per Batch B's `/generate-ost` review iter-1, ambiguous "shell out to X" wording can confuse implementers. Mitigation: explicitly document the "script-when-available, prose-fallback when not" pattern, with the script path clearly marked as not-yet-shipped.

## Changelog

-
