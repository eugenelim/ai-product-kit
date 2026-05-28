---
description: Audits the kit's Discovery-phase coherence by walking five rules against the strategy/intents/, discovery/trees/, discovery/snapshots/, and discovery/opportunities/ subtrees. Reports OSTs missing their parent intent, intents with no recent downstream OST, OSTs whose chosen_opportunity.id doesn't resolve, Opportunities with empty or dangling evidence_basis, and OSTs whose outcome metric doesn't appear in the parent intent's coherent_actions. Verdicts (highest severity wins on multi-rule firings) clean/drift/broken/insufficient-data with exit codes 0/1/2/3. Markdown / JSON / human output formats; optional --write persists to docs/audits/. Emits NEXT chain per verdict.
argument-hint: "[scope] [--format {markdown,json,human}] [--write]"
---

# /audit-discovery-coherence

> Audits the Discovery phase's structural coherence — without it, OSTs can drift away from strategic intents, Opportunities can claim non-existent snapshots, and Validation pulls evidence from undersourced trees. Five rules; verdict-driven exit code; NEXT chain to the remediation command per verdict. Follows the F1.4 "script-when-available, prose-fallback when not" pattern: shells out to `scripts/audit-discovery-coherence.py` if present; the prose procedure below is the implementation when the script is absent (which is its state today; a future ROADMAP item may promote).

## When to run

- Weekly, as part of the continuous-discovery cadence review (paired with `/discovery-update`).
- Before any `/opportunity-narrative` run — if the audit returns `broken` or `drift` on the OST you intend to narrativize, fix the violations first.
- Before any Validation-phase command (`/assumption-test`, `/design-experiment`) — the chosen Opportunity must rest on coherent evidence.
- When `cadence-nudge` surfaces a stale-tree warning at session start.
- When the team has just completed a Discovery sprint (one or more `/update-ost` runs) and wants a coherence checkpoint.

## Inputs

1. Optional positional `[scope]` — one of `all` (default), `<intent-slug>`, or `<ost-slug>`. Resolves the audit's subtree.
2. Optional `--format {markdown,json,human}` — defaults to `markdown`. `json` for machine consumption. `human` for a one-paragraph summary.
3. Optional `--write` flag — persists the report to `<repo-root>/docs/audits/discovery-coherence-<YYYY-MM-DD>.md` AND appends a log entry to `<repo-root>/docs/audits/log.md`.
4. Reads `<repo-root>/strategy/intents/*.md`, `<repo-root>/discovery/trees/*.md`, `<repo-root>/discovery/snapshots/*.md`, `<repo-root>/discovery/opportunities/*.md`.

## The five Discovery-coherence rules

1. **OST → parent intent.** Every OST under `discovery/trees/` must declare a `parent_intent:` resolving to an existing strategic intent under `strategy/intents/` whose `status:` is not in `{killed, abandoned}`. **Severity: broken.**
2. **Intent → downstream OST.** Every active strategic intent should have ≥ 1 OST under `discovery/trees/` with `parent_intent: <intent-slug>` and `last_updated:` within 30 days. Intents with no recent downstream OST are flagged **stale**. **Severity: drift.**
3. **OST `chosen_opportunity:` resolution.** When `chosen_opportunity:` is set, its `id:` must match an Opportunity node in the OST's body (a verifiable node in `nodes[]`, not a free-floating reference). A `merge` or `delete` via `/update-ost` may have invalidated a previously-set chosen id; this rule catches it. **Severity: broken.**
4. **Opportunity → snapshot evidence.** Every Opportunity node in every OST must have `evidence_basis:` containing ≥ 1 `IS-<NNN>` reference, AND each `IS-<NNN>` must resolve to an existing file under `discovery/snapshots/<slug>.md` (the snapshot whose `id:` matches). Dangling references (`IS-<NNN>` cited with no snapshot file) are flagged. **Severity: broken.**
5. **Outcome alignment.** The OST's `outcome.metric:` should be cited verbatim or paraphrased in the parent intent's `coherent_actions:` body. A hard mechanical check is impossible (paraphrase tolerance), so this rule emits a **warning** when the OST's outcome name (or its metric) appears nowhere in the parent intent's H2 body. **Severity: drift (warning only).**

## Verdicts and precedence

When multiple rules fire, the **highest-severity verdict** is reported. Precedence: `broken` > `drift` > `insufficient-data` > `clean`. All violating rules are enumerated in the report regardless of which verdict wins.

| Verdict | Exit code | Triggers |
|---|---|---|
| `clean` | 0 | No rule violations |
| `drift` | 1 | Only Rule 2 (stale intent) or Rule 5 (outcome-alignment warning) |
| `broken` | 2 | Any Rule 1, Rule 3, or Rule 4 violation |
| `insufficient-data` | 3 | No OSTs exist under `discovery/trees/` (or no intents under `strategy/intents/` for `all` scope) |

## Procedure

### Step 1 — scope the audit

Resolve `<repo-root>` as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`.

If `[scope]` is `all` (or omitted): walk the whole `<repo-root>/strategy/intents/` and `<repo-root>/discovery/trees/` trees.
If `[scope]` matches `<intent-slug>`: walk only OSTs whose `parent_intent: <intent-slug>` matches.
If `[scope]` matches `<ost-slug>`: walk only that one OST plus its parent intent.

If the resolved scope contains zero OSTs, set verdict `insufficient-data` and proceed to Step 5 (skip the rule checks; emit a remediation report).

### Step 2 — attempt script shell-out (forward-compatibility)

If `<repo-root>/scripts/audit-discovery-coherence.py` exists, shell out:

```bash
python3 <repo-root>/scripts/audit-discovery-coherence.py --root <repo-root> --scope <scope> --format <format>
```

(With `--write` passed through when set.) Parse the script's output and use it as the report. The script is the authoritative implementation when present; the prose procedure below is the fallback.

If the script does NOT exist (its state as of this command's authoring): fall through to Step 3 and run the rules in prose.

### Step 3 — walk the five rules in order

For each rule, collect the list of violations (artifact path + violation-type + remediation hint). Use `<repo-root>/scripts/lib/graph.py` (F1.1) if available to build the typed-object graph from frontmatter; otherwise read frontmatter directly via `scripts/lib/frontmatter.py` (F1.2).

**Rule 1.** For each OST file, parse frontmatter, read `parent_intent:`. If empty: violation. If non-empty: resolve `<repo-root>/strategy/intents/<parent_intent>.md`; if missing OR the intent's `status:` is `killed`/`abandoned`: violation.

**Rule 2.** For each active strategic intent (status not `killed`/`abandoned`), find all OSTs with `parent_intent: <intent-slug>`. If none have `last_updated:` within the last 30 days, the intent is stale; emit a drift warning naming the intent slug and the days-since-update.

**Rule 3.** For each OST whose `chosen_opportunity:` block is non-empty, parse `chosen_opportunity.id`. Walk the OST body's H2 "Opportunity space" sub-tree (or the JSON projection at `<slug>.json` if present) for matching Opportunity node ids. If no match: violation.

**Rule 4.** For each Opportunity node in every OST (both H2 sub-sections and the JSON projection's `nodes[]`), read `evidence_basis:`. If empty list: violation (unsourced Opportunity). For each `IS-<NNN>` entry: resolve `<repo-root>/discovery/snapshots/<slug>.md` where the file's `id:` matches; if no match: violation (dangling reference).

**Rule 5.** For each OST, parse `outcome.metric:` and `outcome.name:`. Read the parent intent's full body. Grep for either string (case-insensitive, partial match acceptable). If neither appears in the parent intent: warning.

### Step 4 — compute verdict

Walk the collected violations per Rule 1, 3, 4 → if any: verdict `broken`. Else if Rule 2 or 5 fired: verdict `drift`. Else: verdict `clean`. (`insufficient-data` was set in Step 1 if applicable; skip the rule walk in that case.)

### Step 5 — emit the report

**Markdown format (default):** H1 `# Discovery Coherence Audit — <YYYY-MM-DD>` + H2 `## Verdict: <verdict>` + H2 per rule with its violations as a sub-list. Last line: stdout the NEXT chain per Step 6.

**JSON format:**

```json
{
  "verdict": "broken|drift|clean|insufficient-data",
  "scope": "<resolved scope>",
  "rules": [
    {"rule": "ost-parent-intent", "severity": "broken", "violations": [{"ost": "<slug>", "issue": "..."}]},
    ...
  ],
  "next": "<NEXT command, or empty>"
}
```

**Human format:** one paragraph summarizing the verdict and the top-three most-actionable violations.

### Step 6 — emit the NEXT chain per verdict

Last line of stdout, formatted exactly:

| Verdict | NEXT chain |
|---|---|
| `broken` (Rule 1 violations) | `NEXT: /strategy-refresh <intent-slug>` (planned — P7.1) — fix the missing or terminal parent intent |
| `broken` (Rule 3 violations) | `NEXT: /update-ost <ost-slug>` — re-set a valid `chosen_opportunity:` |
| `broken` (Rule 4 violations) | `NEXT: /update-ost <ost-slug>` — add evidence or remove unsourced Opportunities; OR `NEXT: /interview-snapshot` if the broken reference is to a missing snapshot |
| `drift` (Rule 2 only) | `NEXT: /strategy-refresh <intent-slug>` (planned — P7.1) — the intent has aged out of recent Discovery activity |
| `drift` (Rule 5 only — warning) | No NEXT — the warning is informational; outcome alignment is paraphrase-tolerant. The human reviews and decides whether to revise the outcome name or the intent's coherent_actions. |
| `clean` (with an OST whose `chosen_opportunity:` is set but no narrative exists at `discovery/opportunities/narratives/<...>.md`) | `NEXT: /opportunity-narrative <slug> --from <ost-slug>` |
| `clean` (nothing actionable) | No NEXT |
| `insufficient-data` | `NEXT: /generate-ost <slug>` if intents exist; `NEXT: /interview-snapshot <slug>` if not (start the pipeline) |

### Step 7 — when `--write` is set, persist the report

Write the markdown report to `<repo-root>/docs/audits/discovery-coherence-<YYYY-MM-DD>.md` with frontmatter:

```yaml
---
id: AUD-<NNN>
slug: discovery-coherence-<YYYY-MM-DD>
object_type: Audit Report
name: Discovery Coherence Audit — <YYYY-MM-DD>
description: <verdict + one-line summary>
owner: <invoker name or role>
status: Filed
created: <today ISO>
last_updated: <today ISO>
scope: <scope>
verdict: <verdict>
human_owned_decisions:
  - Acknowledge violations and assign remediation
ai_assistance_used:
  - Five-rule graph walk
ai_assistance_allowed: true
human_approval_required: false
---
```

Append a one-line entry to `<repo-root>/docs/audits/log.md`: `- <YYYY-MM-DD>: discovery-coherence-<YYYY-MM-DD>.md — verdict <verdict> (<N violations>)`.

Lint the persisted report with `python3 <repo-root>/tools/lint-frontmatter.py`. On lint failure, exit code 3 with the linter output; the audit report stays on disk for manual repair.

## What this command will not do

- Not silently skip a rule on missing inputs. If `discovery/trees/` is empty, the audit returns `insufficient-data` (exit 3), not `clean` (exit 0).
- Not auto-mutate the artifacts it audits. The audit reads; the human (or downstream `/update-ost`) writes the remediation.
- Not return `clean` when the only OSTs are killed or abandoned (those are filtered out before the rule walk; if no active OSTs survive the filter, verdict is `insufficient-data`).
- Not paraphrase or interpret Rule 5 violations beyond emitting the warning. The human decides whether the OST's outcome aligns with the intent's coherent actions — the paraphrase tolerance is intentional.
- Not assume the working directory is the repo root when invoking the linter or shelling out to the (planned) script.
- Not silently overwrite a same-day audit report — `--write` on a date that already has a report exits code 2 with the existing report's path; the human re-runs with a date suffix if needed.
