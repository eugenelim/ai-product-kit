---
description: Facilitate a five-question post-ship retrospective on a recently shipped initiative — asks the kit's five fixed retro questions one at a time in fixed order (never batched), captures answers verbatim into five corresponding H2 sections, and writes the assembled retro adjacent to the upstream Landing Report (delivery/landings/<slug>-retro.md) or Handoff Packet (delivery/handoff-packets/<slug>/retro.md) per --scope.
argument-hint: <slug> [--scope landing|handoff] [--force]
---

# /retro

> Phase-4 terminal **facilitator** (Wave-4, P4.15) — deviates from the template-fill convention in three named ways (positional names the upstream artifact being retro'd, not the new artifact being written; no multi-candidate parent-resolution picker — positional + `--scope` flag pin upstream deterministically; the template is optional / minimal — the load-bearing contract is the in-command five-question script). Asks five fixed questions in a fixed order, **one at a time, never batched**, and assembles the human's answers into a retro markdown file adjacent to the upstream Landing Report or Handoff Packet. Captures answers verbatim — no synthesis, no summary, no paraphrase. Gates the bridge from Handover 7 back into Phase 1 Strategy at the next cadence.

## When to run

- After a Landing Report has been signed off (`verdict_by:` populated; `measured_at:` ≥ 30d post-ship); the retro is the team-process complement to the report's exec-facing verdict.
- After a Handoff Packet has shipped but before its 30-day measurement window has elapsed — when the team wants immediate-post-ship reflection ahead of the landing report. Use `--scope handoff` to explicitly select this path.
- Before the next cadence-level `/strategy-refresh` — retros feed into the strategy-refresh as process signal, complementing the landings' verdict signal.

## Inputs

1. The positional arg — `<slug>`. **The upstream artifact's slug, not the new retro file's slug** (the retro file's path is derived from the input slug — see Step 1). Kebab-case, matches `^[a-z0-9-]+$`, ≤ 80 chars. This deviates from the F4 template-fill convention where the positional names the new artifact.
2. Optional flag `--scope landing|handoff` — selects which upstream artifact to retro against. Default behavior: if both `delivery/landings/<slug>.md` and `delivery/handoff-packets/<slug>/` exist, **demand `--scope`** — do not auto-pick (exit code 2). If only one exists, pick it automatically and confirm with the human. If neither exists, exit code 2.
3. Optional flag `--force` — permits overwriting an existing retro file at the resolved destination.
4. `templates/retro.md` — the F3 single-file template this command copies. Frontmatter block + five empty H2 sections in the fixed order + a `## Cross-references` stub.
5. Upstream artifact body — read-only. The command reads the landing report's `verdict:`, `parent_vision:`, `parent_handoff_packet:` (when scope=landing) or the handoff packet's `parent_initiative:` and `engineering_partner:` (when scope=handoff). These pre-fill the retro's mechanical frontmatter; they are NOT surfaced as facilitation prompts (the human is not asked to retype them).
6. `tools/lint-frontmatter.py` — default-mode linter run against the written retro file.

## Procedure

### Step 1 — resolve upstream artifact and destination path

If `--scope landing`: validate `delivery/landings/<slug>.md` exists. If not, exit code 2: `"no Landing Report found at delivery/landings/<slug>.md."`. Destination: `delivery/landings/<slug>-retro.md`.

If `--scope handoff`: validate `delivery/handoff-packets/<slug>/README.md` exists. If not, exit code 2: `"no Handoff Packet found at delivery/handoff-packets/<slug>/."`. Destination: `delivery/handoff-packets/<slug>/retro.md`.

If `--scope` is **absent**:
- Both `delivery/landings/<slug>.md` AND `delivery/handoff-packets/<slug>/` exist → exit code 2: `"both a Landing Report and a Handoff Packet exist for slug '<slug>' — demand --scope landing|handoff to pin the upstream deterministically (do not auto-pick)."`. The "do not auto-pick" rule is load-bearing — silently choosing landing over handoff (or vice versa) hides the team's actual choice.
- Only the landing exists → pick `--scope landing` and confirm with the human.
- Only the handoff exists → pick `--scope handoff` and confirm with the human.
- Neither exists → exit code 2: `"no Landing Report or Handoff Packet found for slug '<slug>' — nothing to retro against."`.

If the destination file already exists and `--force` is not set, exit code 2 with: `"<dest-path> already exists — re-run with --force or pick a different slug."`

### Step 2 — instantiate the template at the destination

Copy `templates/retro.md` to the resolved destination. Pre-fill mechanical frontmatter (the human is never asked for these):

- `id: RETRO-<NNN>` — scan `delivery/landings/*-retro.md` AND `delivery/handoff-packets/*/retro.md` for `id: RETRO-` lines, take max + 1, zero-pad to three digits (or `001` if none).
- `slug:` — the positional argument.
- `object_type: Decision` — re-assert (template pre-fills).
- `status: Draft` — re-assert.
- `created:`, `last_updated:` — today's date (ISO-8601, system clock at command start).
- `retro_scope:` — the resolved value (`landing` or `handoff`).
- `parent_landing:` (when scope=landing) **or** `parent_handoff_packet:` (when scope=handoff) — the resolved upstream slug. The other field is omitted from frontmatter.
- `parent_vision:` — transitive carry-through from the upstream artifact's frontmatter.
- `parent_initiative:` — transitive carry-through (when present in the upstream).

### Step 3 — walk the five questions, one at a time, never batched

The kit's "one clarifying question at a time. Never batch." rule is the load-bearing contract for this command. For each of the five questions, in this exact order:

1. Ask the question verbatim.
2. Wait for the human's answer.
3. Echo the captured answer back.
4. Ask the human to confirm or revise.
5. Only after confirmation, write the answer into the corresponding H2 section of the destination file and advance to the next question.

**The five questions, in fixed order:**

1. **What worked?** _Ask: "What worked? — name the moves, processes, decisions, or moments that earned their place this time."_ Capture verbatim into `## What worked?`.
2. **What didn't?** _Ask: "What didn't? — name what failed or fell short, without softening."_ Capture verbatim into `## What didn't?`.
3. **What surprised us?** _Ask: "What surprised us? — the things we didn't predict, good or bad."_ Capture verbatim into `## What surprised us?`.
4. **What would we repeat?** _Ask: "What would we repeat? — what's the explicit pattern from 'worked' worth re-using next time?"_ Capture verbatim into `## What would we repeat?`.
5. **What would we change?** _Ask: "What would we change? — the actionable changes the next initiative should adopt."_ Capture verbatim into `## What would we change?`.

The command **does not** synthesize, summarize, paraphrase, or bullet-ify the human's answers. It captures the human's voice verbatim. The questions are asked one per turn — never as a single "tell me how it went" mega-prompt.

### Step 4 — surface human-owned decisions

Read the written file's `human_owned_decisions:` list (template ships a placeholder for "Explicit decisions the retro surfaces — e.g., 'stop doing X' or 'double down on Y'"). Ask the human to enumerate the actionable decisions the retro surfaces. One decision per turn. Record under `approvals_obtained:` only if the team owner has been named.

### Step 5 — lint the written retro file

Resolve repo root as nearest ancestor of CWD containing `tools/lint-frontmatter.py`. Run `python3 <repo-root>/tools/lint-frontmatter.py <destination-path>` (default mode).

- Exit 0: proceed to Step 6.
- Non-zero: surface the linter output; offer to re-open the relevant frontmatter or sections. If the human accepts and re-lint exits 0, proceed normally. If the human declines (or re-lint still fails), exit code 3.

### Step 6 — emit the chaining hint

Last line of output, formatted exactly:

```
NEXT: /strategy-refresh (planned — ROADMAP P7.1; Phase-4 chain ends here, the kit re-enters Phase 1 Strategy on a cadence decision, not an auto-chain)
```

The retro is the terminal step of the Phase-4 chain. The kit re-enters Phase 1 Strategy on a quarterly cadence, but that transition is human-decided, not command-chained. The NEXT line names `/strategy-refresh` for discoverability and surfaces its planned status per the kit-drift policy.

No `REVIEW:` line is emitted (only `/sequence-initiative` emits a REVIEW interstitial).

## Exit codes

- `0` — retro file written, all five answers captured verbatim, linter passed, NEXT emitted.
- `1` — human aborted mid-walk before Step 5 completed. Partial retro file left on disk (answers captured up to the abort point are persisted). Resume by re-running with the same `<slug>`, `--scope`, and `--force`.
- `2` — pre-conditions failed: slug malformed; upstream artifact not found for the resolved scope; both landing and handoff exist and `--scope` is absent (demand the flag); destination exists without `--force`; `templates/retro.md` missing.
- `3` — file written but post-fill linter exited non-zero and human declined re-open. File persists on disk in known-imperfect state.

## What this command will not do

- **Never batch the five questions into one prompt.** The single most load-bearing rule for this command. A prompt like "Walk me through what worked, what didn't, what surprised you, what you'd repeat, and what you'd change" is a contract violation, even if it elicits the same five answers. The questions are asked one at a time, never batched, and the command body explicitly encodes this.
- **Never reorder the five questions.** The order is fixed: What worked? → What didn't? → What surprised us? → What would we repeat? → What would we change?. The order primes the team for honest reflection on what didn't, and ends with the actionable output the next strategy refresh consumes.
- **Never collapse two questions into a single H2.** Five questions → five H2 sections → five answer blocks. Not four, not six.
- **Never synthesize or summarize the human's answers.** `/retro` is a facilitator. It captures verbatim what the human types. It does not paraphrase, does not bullet-ify a prose answer, does not "improve" the wording. The retro is the human's voice.
- Not produce metric analysis (adoption curves, KPI-vs-threshold). That's the Landing Report's job (HANDOVERS-7).
- Not produce customer-facing copy. That's `/release-notes` (P4.12) and `/launch-comms` (P4.13).
- Not produce a verdict (`adopt | fix | kill`). That's the Landing Report's `verdict:` frontmatter.
- Not auto-resolve the upstream when both candidates exist. The positional `<slug>` plus `--scope` flag pins upstream deterministically; absent `--scope` with both candidates present is exit code 2.
- Not auto-invoke `/strategy-refresh` or any successor command. The NEXT line names `/strategy-refresh` for discoverability; the human runs it on a cadence decision.
- Not call `/audit-portfolio-coherence` or any other audit. The retro is local to one initiative; portfolio audits are quarterly-cadence concerns.
- Not bump any sibling artifact's `last_updated:`. Unlike `/draft-spec` (which bumps the parent Initiative's README), `/retro` writes a sibling file only. The upstream Landing Report is signed off and **must not** be touched.
- Not append to the landing report's body in place. The landing report is signed off; the retro is a sibling file (or, for scope=handoff, a child of the packet folder).
- Not overwrite an existing retro file without `--force`.
- Not write a retro file when the linter fails post-fill without explicit human confirmation (exit 3 — known-imperfect state).
- Not assume the working directory is the repo root when invoking the linter.

$ARGUMENTS
