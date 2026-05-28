# Spec: phase-2-discovery-audits-and-comms

- **Status:** Approved
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored — session scratch)
- **Component type:** Coupled batch of three slash commands — one audit (P2.11), one narrative-drafter (P2.12), one weekly digest (P2.14). Mirrors the `phase-4-template-fill-commands` and Batch A / Batch B precedents.
- **Serves kit phase:** Discovery (Phase 2)
- **Constrained by:** ROADMAP **P2.11** `cmd-audit-discovery-coherence`, **P2.12** `cmd-opportunity-narrative`, **P2.14** `cmd-discovery-update`; Batch A + Batch B outputs (snapshots, opportunity batches, clusters, OSTs, change-set trails the commands consume); `scripts/lib/graph.py` (F1.1) and `scripts/audit-traceability.py` (F1.4 — shape exemplar for kit audits, "script-when-available, prose-fallback when not" pattern); `docs/HANDOVERS.md` §"Handover 2" (Discovery → Validation handover); `context/frameworks/opportunity-solution-tree.md`, `context/frameworks/continuous-discovery.md`, `context/frameworks/interview-snapshot.md`; `.claude/commands/_meta/command-skeleton.md` (the F4 convention all new slash commands consume); `.claude/skills/work-loop/SKILL.md`.

_Specs are exempt from the universal metadata schema (see [`docs/CONVENTIONS.md`](../../CONVENTIONS.md) §"Specs and Plans"). The bullet block above IS the spec's metadata; no YAML frontmatter is required._

> **Spec contract.** Ships the three Phase-2 commands that close the Discovery phase's audit and communication surface: `/audit-discovery-coherence` (P2.11) flags OSTs missing parent intents and other Discovery-coherence violations; `/opportunity-narrative` (P2.12) writes the customer-shaped one-pager that crosses the Discovery → Validation handover boundary; `/discovery-update` (P2.14) produces the weekly stakeholder digest covering snapshots / opportunities / cluster decisions / OST changes since the last update. With these three, Phase 2 is complete — every ROADMAP P2.x item is shipped.

## Objective

Author three slash commands, each implementing one ROADMAP Phase-2 item:

| # | ROADMAP | Slug | Output path |
|---|---|---|---|
| 1 | P2.11 | `cmd-audit-discovery-coherence` | `.claude/commands/audit-discovery-coherence.md` |
| 2 | P2.12 | `cmd-opportunity-narrative` | `.claude/commands/opportunity-narrative.md` |
| 3 | P2.14 | `cmd-discovery-update` | `.claude/commands/discovery-update.md` |

The three components are authoring-time-independent (no cross-references between command files) and runtime-light-coupling (the audit may inform the narrative and digest; the narrative may be cited in the digest, but neither blocks the other).

## Why now

Phase 2 has 12 of 14 items shipped after Batches A and B. The three remaining items close the phase by adding the audit-surface (`/audit-discovery-coherence` — without it, no mechanical gate confirms OSTs trace to intents), the handover-narrative-surface (`/opportunity-narrative` — without it, no human-readable artifact crosses the Discovery → Validation boundary alongside the OST), and the cadence-surface (`/discovery-update` — without it, weekly Discovery cadence has no surface that surfaces drift to stakeholders). Shipping all three together completes Phase 2 and unblocks Phase 3's pre-conditions: `/assumption-test` (P3.1) and `/audit-assumption-coverage` (P3.11) both implicitly assume the Discovery-side audit has run.

## Inputs and outputs

### P2.11 — `/audit-discovery-coherence [scope]`

**Inputs.**

- Optional positional `[scope]` — one of `all` (default), `<intent-slug>`, or `<ost-slug>`. Resolves the subtree to audit.
- Optional `--format {markdown,json,human}` — defaults to `markdown` for human reading; `json` for machine consumption; `human` for a one-paragraph summary.
- Optional `--write` flag — when set, persists the report to `docs/audits/discovery-coherence-<YYYY-MM-DD>.md` AND appends a log entry to `docs/audits/log.md`.
- Reads `<repo-root>/strategy/intents/*.md`, `<repo-root>/discovery/trees/*.md`, `<repo-root>/discovery/snapshots/*.md`, `<repo-root>/discovery/opportunities/*.md` for the graph walk.

**Outputs.** A structured audit report (markdown or JSON) covering five Discovery-coherence rules:

1. **OST → parent intent.** Every OST under `discovery/trees/` must declare a `parent_intent:` resolving to an existing strategic intent under `strategy/intents/` whose `status:` is not `killed` / `abandoned`.
2. **Intent → downstream OST.** Every active strategic intent should have at least one OST under `discovery/trees/` with `parent_intent: <intent-slug>` and `last_updated:` within 30 days. Intents with no recent downstream OST are flagged as **stale**.
3. **OST `chosen_opportunity:` resolution.** When `chosen_opportunity:` is set, its `id:` must match an Opportunity node in the OST's body (a verifiable Opportunity, not a free-floating reference).
4. **Opportunity → snapshot evidence.** Every Opportunity node in every OST must have `evidence_basis:` containing ≥ 1 `IS-<NNN>` reference, AND each `IS-<NNN>` must resolve to an existing file under `discovery/snapshots/`. Dangling references (`IS-<NNN>` cited with no snapshot file) are flagged.
5. **Outcome alignment.** The OST's `outcome.metric:` should be cited (verbatim or paraphrased) in the parent intent's `coherent_actions:` — a hard check is impossible (paraphrase tolerance), so this rule emits a **warning** (not a failure) when the OST's outcome name appears nowhere in the parent intent's body.

Verdicts: `clean` (no violations — exit 0), `drift` (warnings only — exit 1), `broken` (any rule 1/3/4 violation — exit 2), `insufficient-data` (e.g., no OSTs to audit — exit 3). **When multiple rules fire**, the highest-severity verdict is reported (precedence: `broken` > `drift` > `insufficient-data` > `clean`). All violating rules are enumerated in the report regardless of which verdict wins — the verdict drives the exit code and the NEXT chain, but the report shows the full picture.

**NEXT chain per verdict:** `broken` → `NEXT: /update-ost <ost-slug>` for the first OST with an evidence-broken violation (Rule 4) OR `NEXT: /strategy-refresh <intent-slug>` for Rule 1 (missing parent intent). `drift` → `NEXT: /strategy-refresh <intent-slug>` for stale intents (Rule 2); for Rule-5-only `drift` (outcome-alignment warning, no remediation required), no NEXT is emitted. `clean` → if any OST has `chosen_opportunity:` set but no narrative under `discovery/opportunities/narratives/<...>.md`, `NEXT: /opportunity-narrative <slug> --from <ost-slug>`; otherwise no NEXT (nothing actionable). `insufficient-data` → `NEXT: /generate-ost <slug>` (or `/interview-snapshot <slug>` if no snapshots exist).

Per the F1.4 convention, the command attempts to shell out to `<repo-root>/scripts/audit-discovery-coherence.py` if that script exists; **the script does not exist as part of this batch** (the prose procedure in the command body IS the implementation, mirroring how `/audit-traceability` operated before F1.4 was authored). A future ROADMAP item may promote the prose procedure to a runnable script.

### P2.12 — `/opportunity-narrative <slug>`

**Inputs.**

- Positional `<slug>` — the new narrative's slug.
- `--from <ost-slug>` — required parent OST (resolution rule per the F4 convention). The OST MUST satisfy **both** anti-prematurity conditions: (a) `chosen_opportunity:` block is present and non-empty, AND (b) `chosen_opportunity.id` resolves to an actual Opportunity node in the OST body (a `merge` or `delete` action via `/update-ost` may have invalidated a previously-set `chosen_opportunity.id`; this is the case Rule 3 of `/audit-discovery-coherence` catches). If either condition fails, the command exits code 2 with a remediation message naming the failed condition and pointing at `/audit-discovery-coherence` (for diagnosis) or `/update-ost` (to re-set a valid chosen opportunity).
- Optional `--force` — overwrite existing narrative file. Does NOT bypass the anti-prematurity guard (the guard is a hard precondition for a meaningful narrative).

**Outputs.** Writes `discovery/opportunities/narratives/<slug>.md` — a customer-shaped one-pager that crosses the Discovery → Validation handover boundary alongside the OST. Frontmatter: `object_type: Opportunity | Adapted` (the H1 names it "Opportunity Narrative"), `id: ONA-<NNN>`, `parent_ost: <ost-slug>`, `parent_opportunity: <OPP-NNN>` (the chosen opportunity's id), `parent_intent: <intent-slug>` (carried through from the OST), the universal metadata schema.

Body (H2 sections, walked one at a time):

1. **The customer** — one paragraph in narrative voice: who is the customer, what segment, what role, what they're trying to accomplish. Cite the customer-voice from the snapshots in the chosen opportunity's `evidence_basis:`.
2. **The pain** — one paragraph: what specifically is the customer hitting, in their words. Cite at least one Direct Quote from a sourcing snapshot (`"<verbatim>" — <Speaker Name>, <MM:SS>` per the interview-snapshot framework).
3. **Why this, why now** — one paragraph: what makes this Opportunity worth pursuing relative to the sibling Opportunities the OST surfaced. Cite the OST's `chosen_opportunity:` rationale and (briefly) the excluded siblings.
4. **What we're betting** — one paragraph: the riskiest assumption underneath this Opportunity (informally; the formal Assumption Map is downstream, in `/assumption-test` / `/design-experiment`). This is the bridge that primes Validation.
5. **Open questions for Validation** — bullet list: what does the team not yet know that the Validation phase will address? Pre-populates the Assumption Map's `assumptions:` list per Handover-2.5.

Emits `NEXT: /assumption-test <slug>` (planned — P3.1) on success.

### P2.14 — `/discovery-update [scope]`

**Inputs.**

- Optional positional `[scope]` — one of `all` (default — every active strategic intent), `<intent-slug>`, or `<ost-slug>`. Defaults to `all`.
- Optional `--since <YYYY-MM-DD>` — start of the digest window. Default: 7 days ago.
- Optional `--for <stakeholder-role>` — tailors the voice for one of `{exec, eng-lead, design-lead, support, all-hands}`. Default: `all-hands`.
- Optional `--write` flag — when set, persists the digest to `discovery/updates/<YYYY-MM-DD>-<scope>.md`.

**Outputs.** A weekly digest covering Discovery activity since `--since`. Structure (H2 sections):

1. **Headline** — one sentence stating the most consequential Discovery move this week.
2. **By the numbers** — bullet list: snapshots added (count + slugs), opportunities surfaced, clusters proposed, OST changes (counted via change-set trail files in `discovery/trees/*-change-set-*.json`).
3. **What changed in the OST** — narrative description of OST mutations: new Opportunities, merges, splits, renames, the chosen Opportunity if newly set. Walk the change-set trail files in chronological order; describe each in plain language.
4. **What we learned** — bullet list of `[ambiguous: ...]` flags resolved or surfaced; new evidence promoted into existing Opportunities; new Solutions or Assumption Tests added.
5. **What's blocking** — bullet list: snapshots awaiting follow-up; OSTs with unsourced Opportunities (forward to `/audit-discovery-coherence`); intents with no recent OST activity.
6. **Next week** — bullet list: interviews scheduled, Opportunities targeted for clustering, Assumption Tests being designed.

When `--write` not set: stdout-only render of the digest. When `--write` set: persist to `discovery/updates/<YYYY-MM-DD>-<scope>.md` with frontmatter (`object_type: Insight | Adapted` — confirmed: the kit's ontology has no canonical "Stakeholder Update" type as of 2026-05-28, so the digest uses the `| Adapted` escape hatch; H1 names it "Discovery Update: Week of YYYY-MM-DD"; `id: DUP-<NNN>`; `parent_intent` or `parent_ost`; universal schema). The scope value is validated against `^(all|[a-z0-9-]+)$` before being used in the filename; non-matching scope exits code 2 with a remediation message. Emits no NEXT chain (digest is terminal — stakeholders read it, no downstream command is forced).

**Activity definition** (for the "no activity → cadence-drift surface" rule below): activity is defined as **(a)** any new file under `<repo-root>/discovery/snapshots/` whose `created:` frontmatter date falls within the `--since` window, OR **(b)** any change-set trail file under `<repo-root>/discovery/trees/` whose filename timestamp segment (`<YYYY-MM-DDTHH-MM-SS>` between `change-set-` and the 4-hex suffix, per Batch B's `/update-ost` spec) falls within the window. File modifications without new IDs or new change-set trails do NOT count as activity — this prevents incidental touches (git-checkout retimes, formatting passes) from masking a quiet Discovery week.

**Chronological sort.** When walking change-set trail files, sort by the ISO-8601 timestamp embedded in the filename (NOT by filesystem mtime). This is the canonical ordering defined by Batch B's `/update-ost` spec; filesystem mtime is unreliable across git checkouts and copies.

**Role-mode mechanical anchors** (the `--for` flag's tone hints, made mechanically grep-testable until `voice-check` ships — P8.4):

- `exec` — only the §"Headline" section (one sentence) is emitted; other sections suppressed. Business-outcome-oriented vocabulary in the headline (cite the parent intent's `coherent_actions:` language).
- `eng-lead` — include OST change-set trail file IDs verbatim in §"What changed in the OST" (the filename's timestamp + 4-hex suffix); name each affected Opportunity by `OPP-<NNN>` id.
- `design-lead` — include at least one Direct Quote per the interview-snapshot format (`"<verbatim>" — <Speaker>, <MM:SS>`) in §"What we learned"; cite the source snapshot's `IS-<NNN>` id.
- `support` — include the verbatim `workarounds:` field text from at least one snapshot in §"What's blocking" (the workarounds tell support what customers are coping with today).
- `all-hands` — full six sections, no per-section filtering; the default.

## Boundaries

### Always do

- Follow the F4 command-skeleton convention (frontmatter, H1, `## When to run`, `## Inputs`, `## Procedure` with numbered Steps, `## What this command will not do`).
- Resolve `<repo-root>` as the nearest ancestor containing `tools/lint-frontmatter.py`.
- For `/audit-discovery-coherence`: emit a structured report with explicit verdict (`clean` / `drift` / `broken` / `insufficient-data`) and per-rule violation lists.
- For `/opportunity-narrative`: refuse to draft a narrative against an OST whose `chosen_opportunity:` is empty (the anti-prematurity guard at Handover 2).
- For `/discovery-update`: read change-set trail files in chronological order so the digest's OST-change narrative respects history.
- Lint every written artifact with `<repo-root>/tools/lint-frontmatter.py` before declaring done.

### Ask first

- Adding new ontology object_types for the digest (the spec uses `Stakeholder Update` — confirm this exists in the ontology before relying on it; if not, fall back to the `| Adapted` escape hatch).
- Promoting `/audit-discovery-coherence`'s prose procedure to a runnable script — that's a future ROADMAP item, not this batch.
- Extending the digest's stakeholder-role voice modes — pick the minimum useful set; a future batch can add more.

### Never do

- Never draft an `/opportunity-narrative` against an OST without `chosen_opportunity:` set. The OST framework's `## Common failure modes` warns against premature commitment.
- Never fabricate Direct Quotes in the narrative. If the chosen Opportunity's `evidence_basis:` snapshots have no Direct Quotes (e.g., no-recording fallback was used), surface that gap; do not invent a quote.
- Never silently skip an audit rule on missing inputs. If `discovery/trees/` is empty, the audit returns `insufficient-data` (exit 3), not `clean` (exit 0) — the absence of OSTs is a Discovery failure to surface.
- Never have `/discovery-update` write a digest covering a window with zero activity. If `--since` covers a quiet period, surface that explicitly in the headline ("No Discovery activity since <date> — flagging continuous-discovery cadence drift") and link to `cadence-nudge`'s guidance — do NOT produce a "nothing happened, all good" digest.
- Never auto-publish the digest. `--write` persists to disk; humans share with stakeholders. The command does not Slack, email, or push anywhere.
- Never accept a `[scope]` value that does not match `^(all|[a-z0-9-]+)$`. Exit code 2 with a remediation message naming the offending scope value; do not silently sanitize.

## Verification mode

**Goal-based check** for all three commands:

- `tools/lint-command.sh` exits 0 on each.
- `tools/pre-pr.sh` exits 0 across the repo.
- Each body contains a `NEXT:` line (or, for `/discovery-update`, an explicit "no NEXT — digest is terminal" note).

**Manual gesture** (deferred to post-EXECUTE — recorded under `notes/manual-verification.md`):

- `/audit-discovery-coherence` against a real kit state returns a parseable report.
- `/opportunity-narrative test-narrative --from <ost-with-chosen-set>` produces a five-section narrative with a non-fabricated Direct Quote.
- `/discovery-update --since <date>` over a real Discovery window produces a digest naming actual snapshots, opportunities, and OST changes.

## Contract tests

### Per-command mechanical tests

For each of the three commands:

- File exists at the declared path.
- `tools/lint-command.sh` exits 0.
- Frontmatter `description` ≤ 1024 chars.
- Body contains H1 matching the command name.
- Body contains `## When to run`, `## Inputs`, `## Procedure`, `## What this command will not do`.

### Cross-cutting tests

- `tools/pre-pr.sh` exits 0.
- `/audit-discovery-coherence.md` body names the five rules (mechanical grep — each rule's anchor phrase appears at least once).
- `/opportunity-narrative.md` body explicitly enforces the "no chosen_opportunity → no narrative" rule (mechanical grep).
- `/discovery-update.md` body explicitly enforces the "no activity → surface the gap" rule (mechanical grep) AND explicitly documents the "no NEXT — digest is terminal" posture.
- None of the three new commands' bodies cite `scripts/validate_ost.py` (none of them mutate the OST; the validator is Batch B's surface).

## Non-goals

- **Not promoting `/audit-discovery-coherence`'s prose procedure to a runnable Python script** (analogous to F1.4 promoting `/audit-traceability`). Future ROADMAP item.
- **Not building an F2-hook integration** for the audit (analogous to F2.7 wiring `validate_ost.py`). Future ROADMAP item.
- **Not modifying `templates/ost.md`, `templates/assumption-map.md`, or any framework reference.**
- **Not introducing `Opportunity Narrative` as a new Domain A-I ontology type** — uses the `Opportunity | Adapted` escape hatch.
- **Not implementing full voice-guide enforcement on `/discovery-update --for <role>`** — modes are tone hints only; `voice-check` (P8.4) is the future surface for stricter voice-guide enforcement.

## Open questions

- **Audit prose vs script.** The kit's audit pipeline (F1.4, F1.5, F1.6) consistently follows the "script-when-available, prose-fallback otherwise" pattern. This batch ships the prose only; a future item promotes to a script. The command body explicitly names this — it does not pretend the script exists. **When to address:** when `/audit-discovery-coherence` is invoked enough in real workflows that automation pays off.
- **Ontology types verified at Stage 1 of the plan (resolved 2026-05-28):** `Audit Report` is present in `context/frameworks/ontology.md` Domain I — `/audit-discovery-coherence`'s persisted reports (when `--write` is set) use `object_type: Audit Report` directly, no escape hatch needed. `Stakeholder Update` is NOT present in the ontology — `/discovery-update`'s digest uses `object_type: Insight | Adapted` via the kit's escape hatch. A future RFC may promote "Discovery Update" or "Stakeholder Update" to a first-class Domain F type if these digests prove load-bearing. **Both decisions are settled — no open question.**
- **Digest voice-guide integration.** `/discovery-update --for <role>` ships with role-specific tone hints (exec: terse + business-outcome-oriented; eng-lead: cite specific OST changes; design-lead: cite specific customer pain quotes; support: cite specific workarounds; all-hands: balanced). When `voice-check` (P8.4) ships, integrate. **When to address:** when P8.4 ships.

## Acceptance criteria

- [ ] `.claude/commands/audit-discovery-coherence.md` exists, lint-clean, body names the five Discovery-coherence rules with verdict semantics, emits `NEXT:` to a remediation command (e.g., `/update-ost` or `/opportunity-narrative`) based on findings.
- [ ] `.claude/commands/opportunity-narrative.md` exists, lint-clean, body enforces "no chosen_opportunity → no narrative", emits `NEXT: /assumption-test` (planned — P3.1).
- [ ] `.claude/commands/discovery-update.md` exists, lint-clean, body enforces "no activity → surface the gap", explicitly documents that the digest is terminal (no NEXT).
- [ ] `tools/pre-pr.sh` exits 0 across the whole repo.
- [ ] `ROADMAP.md` rows P2.11, P2.12, P2.14 are marked `[x]` with `**Shipped:** 2026-05-28`.
- [ ] `docs/INVENTORY.md` Phase-2 table updates the three rows from "planned" to "shipped".

## Cross-references

- **Consumed by (when shipped):** `/assumption-test` (P3.1) — reads `/opportunity-narrative` output to seed the Assumption Map's chosen-opportunity restatement; future `cadence-manager` scheduled agent (P7.6) — runs `/audit-discovery-coherence` weekly.
- **Consumes:** Batch A + Batch B outputs (snapshots, opportunity batches, clusters, OSTs, change-set trails); `scripts/lib/graph.py` (F1.1) for the audit's graph walk; the F4 command-skeleton convention.
- **Frontmatter fields owned:** `parent_ost:` and `parent_opportunity:` (for narratives) — both are kit-composite uses of existing universal-schema patterns.
- **Ontology object types touched:** *Opportunity* (Domain C, via `| Adapted` for narratives), *Insight* (Domain C, via `| Adapted` for digests — no canonical "Stakeholder Update" type exists today), *Audit Report* (Domain I — used directly; present in the ontology).
