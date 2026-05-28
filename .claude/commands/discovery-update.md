---
description: Produces the weekly stakeholder digest of Discovery activity since `--since` (default 7 days ago). Six H2 sections (Headline / By the numbers / What changed in the OST / What we learned / What's blocking / Next week). Walks new snapshot files and change-set trail files within the window. When no activity is detected, surfaces continuous-discovery cadence drift in the headline rather than producing a "nothing happened" digest. Role-mode mechanical anchors (exec / eng-lead / design-lead / support / all-hands) tailor section content. Terminal — emits no NEXT (humans share with stakeholders). Stdout by default; --write persists to discovery/updates/<YYYY-MM-DD>-<scope>.md. Phase 2 (Discovery).
argument-hint: "[scope] [--since <YYYY-MM-DD>] [--for {exec,eng-lead,design-lead,support,all-hands}] [--write]"
---

# /discovery-update

> Phase-2 stakeholder-digest command. Reports Discovery activity over the `--since` window — snapshots added, opportunities surfaced, clusters proposed, OST changes (via the change-set trail files Batch B's `/update-ost` writes). Surfaces continuous-discovery cadence drift when the window covers a quiet period. Five role-mode mechanical anchors tailor section content. Terminal command (no NEXT chain — the digest is the artifact; humans share with stakeholders). Greenfield and enterprise modes both invoke this command unchanged.

## When to run

- Weekly, paired with `/audit-discovery-coherence`, as the kit's Discovery-phase cadence rhythm (per `context/frameworks/continuous-discovery.md`).
- After a Discovery sprint (one or more `/update-ost` runs or a batch of `/interview-snapshot` runs) and the team wants a stakeholder-facing recap.
- When `cadence-nudge` surfaces a stale-tree warning — the digest's "No Discovery activity" headline (per the cadence-drift rule below) is the human-readable artifact stakeholders see.
- Manually any time a stakeholder asks "what's Discovery up to?" — the command is idempotent and read-only by default (`--write` is opt-in).

## Inputs

1. Optional positional `[scope]` — one of `all` (default — every active strategic intent), `<intent-slug>`, or `<ost-slug>`. Validated against `^(all|[a-z0-9-]+)$`; non-matching scope exits code 2.
2. Optional `--since <YYYY-MM-DD>` — start of the digest window. Default: 7 days ago (ISO `today - 7d`).
3. Optional `--for <stakeholder-role>` — one of `{exec, eng-lead, design-lead, support, all-hands}`. Default: `all-hands`. See "Role-mode mechanical anchors" below.
4. Optional `--write` flag — persists the digest to `<repo-root>/discovery/updates/<YYYY-MM-DD>-<scope>.md` with frontmatter.
5. Reads `<repo-root>/discovery/snapshots/*.md`, `<repo-root>/discovery/opportunities/*.md` (and the `clusters/` subdirectory), `<repo-root>/discovery/trees/*.md`, and `<repo-root>/discovery/trees/*-change-set-*.json`.

## Activity definition

Activity is defined as **(a)** any new file under `<repo-root>/discovery/snapshots/` whose `created:` frontmatter date falls within the `--since` window, OR **(b)** any change-set trail file under `<repo-root>/discovery/trees/` whose filename timestamp segment (the `<YYYY-MM-DDTHH-MM-SS>` between `change-set-` and the `4-hex` suffix, per Batch B's `/update-ost` filename convention) falls within the window. File modifications without new IDs or new change-set trails do NOT count as activity — this prevents incidental touches (git-checkout retimes, formatting passes) from masking a quiet Discovery week.

When activity is zero across both (a) and (b), the digest's §"Headline" reads: `"No Discovery activity since <YYYY-MM-DD> — flagging continuous-discovery cadence drift. See cadence-nudge guidance and context/frameworks/continuous-discovery.md §'The weekly habit'."` The remaining sections are omitted (the "nothing happened, all good" digest is never produced).

## Role-mode mechanical anchors

The `--for` flag's tone hints are made mechanically grep-testable (until `voice-check` ships — P8.4):

- **`exec`** — only §"Headline" emitted (one sentence). Other sections suppressed. Business-outcome-oriented vocabulary in the headline (cite the parent intent's `coherent_actions:` language verbatim where possible).
- **`eng-lead`** — include OST change-set trail file IDs verbatim in §"What changed in the OST" (filename's timestamp + 4-hex suffix). Name each affected Opportunity by its `OPP-<NNN>` id.
- **`design-lead`** — include at least one Direct Quote per the interview-snapshot format (`"<verbatim>" — <Speaker>, <MM:SS>`) in §"What we learned"; cite the source snapshot's `IS-<NNN>` id.
- **`support`** — include the verbatim `workarounds:` field text from at least one snapshot in §"What's blocking" (the workarounds tell support what customers are coping with today).
- **`all-hands`** — full six sections, no per-section filtering; the default.

## Procedure

### Step 1 — resolve scope and the `--since` window

Resolve `<repo-root>` as the nearest ancestor of the current working directory containing `tools/lint-frontmatter.py`.

If `[scope]` is `all` (or omitted): walk all subdirectories listed in §"Inputs" item 5.
Otherwise: validate `[scope]` against `^(all|[a-z0-9-]+)$` — if non-matching, exit code 2 with: `"scope '<scope>' is not valid (must match ^(all|[a-z0-9-]+)$). Use 'all' or a kebab-case slug for an intent or OST."`

Resolve `<intent-slug>` or `<ost-slug>` to its subtree. If `<intent-slug>`: walk OSTs whose `parent_intent: <intent-slug>` matches. If `<ost-slug>`: walk only that one OST plus its change-set trails.

Resolve `--since` (default: 7 days ago ISO). Validate the date string against `^\d{4}-\d{2}-\d{2}$`; on mismatch, exit code 2.

### Step 2 — collect activity within the window

For (a) — new snapshots: walk `<repo-root>/discovery/snapshots/*.md`, parse each file's `created:` frontmatter date. Collect those whose `created:` is in the `[--since, today]` window.

For (b) — OST changes: walk `<repo-root>/discovery/trees/*-change-set-*.json`. Parse each filename's timestamp segment (the substring matching `(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})` between `change-set-` and the trailing `-<4-hex>.json`). Collect those in the window. **Sort chronologically by the filename timestamp, NOT by filesystem mtime** — this is the canonical ordering defined by Batch B's `/update-ost` spec; filesystem mtime is unreliable across git checkouts.

If activity is zero across both (a) and (b), proceed to Step 4 (emit the cadence-drift headline). Otherwise proceed to Step 3.

### Step 3 — walk the six H2 sections (or the role-mode subset)

For the default `all-hands` mode, emit all six sections. For other modes, emit only the sections named in the role-mode anchors above (with the relevant section receiving the role's required content).

**H2 1 — Headline.** One sentence stating the most consequential Discovery move in the window. Examples: "Chose Opportunity OPP-014 (analysts redo join logic) over four alternatives after the third sibling Opportunity emerged." OR "Three new snapshots; one ambiguity flag awaiting follow-up." Cite the parent intent's `coherent_actions:` vocabulary if `--for exec`.

**H2 2 — By the numbers.** Bullet list with counts:

- Snapshots added: N (list slugs)
- Opportunities surfaced via `/extract-opportunities`: N (list batch slugs)
- Clusters proposed via `/cluster-opportunities`: N (list proposal slugs)
- OST changes (count of change-set trail files in the window): N (list filenames if `--for eng-lead`)

**H2 3 — What changed in the OST.** Narrative description of OST mutations in chronological order (per the canonical sort defined in §"Activity definition"). Walk each change-set trail file; describe each in plain language. For `--for eng-lead`, include the verbatim filename (with timestamp + 4-hex suffix) and name each affected node by `OPP-<NNN>` / `SOL-<NNN>` / etc.

**H2 4 — What we learned.** Bullet list:

- `[ambiguous: ...]` flags resolved this week (snapshots that had ambiguity flags now have non-flagged content).
- New `[ambiguous: ...]` flags surfaced this week (awaiting follow-up).
- New evidence promoted into existing Opportunities (via `/update-ost --update-evidence-only` or via `add-source-opportunity` actions).
- New Solutions added (via `/update-ost --add-node solution:...` — though note that as of Batch B, AssumptionTests are a known vocabulary gap; surface that limitation if relevant).

For `--for design-lead`, include at least one Direct Quote in the framework's format from a sourcing snapshot.

**H2 5 — What's blocking.** Bullet list:

- Snapshots awaiting follow-up (those with unresolved `[ambiguous: ...]` flags).
- OSTs with unsourced Opportunities (forward to `/audit-discovery-coherence` for the formal verdict).
- Intents with no recent OST activity (forward to `/audit-discovery-coherence` Rule 2).

For `--for support`, include the verbatim `workarounds:` field text from at least one snapshot — these are the coping mechanisms support teams should know about today.

**H2 6 — Next week.** Bullet list (the team's stated plan):

- Interviews scheduled (count + interviewees, if known from `interviews/` subdirectory).
- Opportunities targeted for clustering (from the parking-lot file, if it exists).
- Assumption Tests being designed (Phase 3 prep — handover to `/assumption-test` planned P3.1).

This section is forward-looking and depends on the human's input — ask if the team's plan isn't surfaceable from artifacts alone.

### Step 4 — surface the cadence-drift headline (when activity is zero)

When Step 2 returned no activity, emit only §"Headline" with: `"No Discovery activity since <YYYY-MM-DD> — flagging continuous-discovery cadence drift. See cadence-nudge guidance and context/frameworks/continuous-discovery.md §'The weekly habit'."` Skip §§ 2-6. The point is to surface the cadence problem, not paper it over with a "nothing happened, all good" digest.

### Step 5 — render or persist

If `--write` is NOT set: stdout-only render of the digest. The human reads the markdown directly and shares with stakeholders.

If `--write` is set: persist to `<repo-root>/discovery/updates/<YYYY-MM-DD>-<scope>.md` with frontmatter:

```yaml
---
id: DUP-<NNN>
slug: <YYYY-MM-DD>-<scope>
object_type: Insight | Adapted
name: Discovery Update — <scope> — Week of <YYYY-MM-DD>
description: <headline content>
owner: <invoker name or role>
status: Filed
created: <today ISO>
last_updated: <today ISO>
scope: <scope>
since: <--since value>
for_role: <--for value>
human_owned_decisions:
  - Confirm the digest faithfully represents the artifacts walked
  - Decide which stakeholders receive the digest and through what channel
ai_assistance_used:
  - Activity walk over snapshots / opportunities / OSTs / change-set trails
  - Role-mode content tailoring
ai_assistance_allowed: restricted
human_approval_required: true
---
```

H1: `# Discovery Update: <scope> — Week of <YYYY-MM-DD>`. Body: the six H2 sections (or role-filtered subset).

Lint with `python3 <repo-root>/tools/lint-frontmatter.py <repo-root>/discovery/updates/<YYYY-MM-DD>-<scope>.md`. On lint failure, exit code 3 with the linter output; the digest file stays on disk for manual repair.

### Step 6 — no NEXT chain

The digest is terminal — emit no `NEXT:` line. Stakeholders read the digest; they decide what to do with it. The kit's NEXT chain pattern is for command-to-command flow; the digest's audience is humans, not commands.

Last line of output for a `--write` run: `Digest persisted to <relative-path>. Share via your team's stakeholder channel; no NEXT chain (digest is terminal).` For a no-`--write` run, the digest itself is the final output.

## What this command will not do

- Never produce a "nothing happened, all good" digest on quiet weeks. When activity is zero, the §"Headline" surfaces continuous-discovery cadence drift; the other sections are suppressed.
- Never auto-publish. `--write` persists to disk; humans share with stakeholders. The command does not Slack, email, or push anywhere.
- Never invent activity not surfaced from the artifacts. If §"Next week" can't be derived from `interviews/` or the parking-lot file, ask the human; do not fabricate.
- Never accept a `[scope]` value that does not match `^(all|[a-z0-9-]+)$`. Exit code 2 with a remediation message; do not silently sanitize.
- Never sort change-set trail files by filesystem mtime. Sort by the filename timestamp (per Batch B's canonical convention) — mtime is unreliable across git checkouts.
- Never emit a NEXT chain. The digest is terminal by design; chaining to another command would force a human action the digest is meant to inform, not script.
- Never assume the working directory is the repo root when invoking the linter.
- Never overwrite an existing digest at the same `<YYYY-MM-DD>-<scope>.md` path; exit code 2 with the existing digest's path and a suggestion to use a different scope or wait until tomorrow.
