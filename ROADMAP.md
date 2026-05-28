# ROADMAP

The ordered build queue for the kit. Every item below is — or will become — a spec under `docs/specs/<slug>/`. Build them in order. Each item's number is its priority; the slug is its directory name.

**How to use this file:**

1. Pick the lowest-numbered unchecked item.
2. Run `tools/new-spec.sh <slug>` to scaffold the spec.
3. Fill `spec.md` (the contract) and `plan.md` (the strategy).
4. Dispatch `adversarial-reviewer` against both — that's the pre-EXECUTE gate.
5. Set `state.json.plan_review_status = "approved"` once findings are addressed.
6. EXECUTE per the plan.
7. VERIFY (run the relevant linters via `tools/pre-pr.sh`).
8. REVIEW (adversarial-reviewer against the implementation).
9. CAPTURE (update AGENTS.md, INVENTORY.md, README.md as needed; mark this item checked).

The full mechanics are in [`.claude/skills/work-loop/SKILL.md`](.claude/skills/work-loop/SKILL.md).

**Order rationale.** Items are sequenced by dependency and leverage. Foundation items unblock multiple downstream items; phase commands are ordered by frequency of use in real PM practice; reviewer and convenience items come last. When you skip an item, name what you're trading away.

---

## Foundation 0 — Build harness (✓ complete; reference only)

These shipped before the roadmap formally existed, in the same session that produced this file. They are the bootstrap that makes every subsequent item buildable. Listed for traceability, not for execution.

- [x] **F0.1** Spec template, plan template, state.json template (`docs/_templates/`)
- [x] **F0.2** ADR template, RFC template (`docs/_templates/`)
- [x] **F0.3** `tools/check-done.py` — phase-gate enforcement
- [x] **F0.4** `tools/lint-skill.sh`, `lint-agent.sh`, `lint-command.sh` — shape linters
- [x] **F0.5** `tools/lint-frontmatter.py` — ontology / universal-metadata linter
- [x] **F0.6** `tools/pre-pr.sh` — aggregation hook
- [x] **F0.7** `tools/new-spec.sh` — scaffold a spec from templates
- [x] **F0.8** GitHub Actions CI (`.github/workflows/lint.yml`)
- [x] **F0.9** Reconcile-and-harden pass — drift fixes across AGENTS/README/INVENTORY/.claude/CLAUDE.md/context/README.md; CLAUDE.md → symlink; created `.claude/skills/README.md` + `.claude/agents/README.md`; ran adversarial-reviewer fan-out across 20 in-scope components + 2 ADRs; applied in-pass fixes; deferred substantive hardening to F0.10-F0.13 + F1.7 + D-series sub-tasks. **Spec:** `docs/specs/reconcile-existing-components/`. **Shipped:** 2026-05-21.

---

## Foundation 1 — Make the existing audits run

The v3 kit ships three audit commands (`/audit-completeness`, `/audit-traceability`, `/audit-portfolio-coherence`) that document procedures Claude can follow, but they want shared Python utilities to do the heavy walks repeatably and testably. These come first because every other audit and many slash commands will reuse them.

- [x] **F1.1** `audit-graph-walker` — Python library (`scripts/lib/graph.py`) that builds the typed-object graph from a kit's artifacts. Reads `parent_*`/`related_*` frontmatter, returns an in-memory graph the audits walk. **Slug:** `audit-graph-walker`. **Shipped:** 2026-05-21.

- [x] **F1.2** `frontmatter-parser` — Robust YAML-subset parser for kit frontmatter (`scripts/lib/frontmatter.py`). Extracted from the rough version inside `lint-frontmatter.py`. Handles lists, nested maps to one level, comments, multi-line strings. **Slug:** `frontmatter-parser`. **Shipped:** 2026-05-21.

- [x] **F1.3** `ontology-classifier` skill — Extracts typed objects from unstructured input (interview transcripts, Slack threads, customer emails) and surfaces missing required fields. Used by every audit and by humans when classifying inbound material. **Slug:** `ontology-classifier-skill`. **Depends on:** F1.2. **Shipped:** 2026-05-21.

- [x] **F1.4** `audit-traceability` script — Promotes the prose procedure in `.claude/commands/audit-traceability.md` to a runnable `scripts/audit-traceability.py` that the slash command shells out to. Walks the seven traceability rules across the typed graph. **Slug:** `audit-traceability-script`. **Depends on:** F1.1, F1.2. **Shipped:** 2026-05-21.

- [x] **F1.5** `audit-completeness` script — `scripts/audit-completeness.py` running the ontology's 25-item pre-engineering-handoff checklist against a named initiative or handoff packet. **Slug:** `audit-completeness-script`. **Depends on:** F1.1, F1.2. **Shipped:** 2026-05-21.

- [x] **F1.6** `audit-portfolio-coherence` script — `scripts/audit-portfolio-coherence.py` performing the pairwise Rumelt coherence check. **Slug:** `audit-portfolio-coherence-script`. **Depends on:** F1.1, F1.2. **Shipped:** 2026-05-21.

---

## Foundation 2 — Hook scripts

The hook documentation in `.claude/hooks/` and AGENTS.md describes phase guards that don't yet have enforcement scripts. Build these so the hooks aren't aspirational.

- [x] **F2.1** `check-handover-link.py` — PreToolUse hook that refuses to write a delivery artifact without its `parent_*` frontmatter link. **Slug:** `hook-check-handover-link`. **Depends on:** F1.2. **Shipped:** 2026-05-21.

- [x] **F2.2** `check-assumption-threshold.py` — The kit's signature guard: refuses to write `validation/experiments/**/results.md` unless a falsification threshold was filed *before* the experiment ran. **Slug:** `hook-assumption-threshold-lock`. **Depends on:** F1.2. **Shipped:** 2026-05-21.

- [x] **F2.3** `ontology-type-check.py` — PreToolUse hook that warns when an artifact path implies an ontology object type but the frontmatter omits `object_type:`. **Slug:** `hook-ontology-type-check`. **Depends on:** F1.2. **Shipped:** 2026-05-21.

- [x] **F2.4** `mode-guard.py` — SessionStart hook that reads `mode:` from `.claude/CLAUDE.md` and blocks the wrong-mode slash commands. **Slug:** `hook-mode-guard`. **Shipped:** 2026-05-21.

- [x] **F2.5** `cadence-nudge.py` — SessionStart hook that surfaces strategy/OST/kill-drought drift. **Slug:** `hook-cadence-nudge`. **Depends on:** F1.1. **Shipped:** 2026-05-21.

- [x] **F2.6** `.claude/settings.json` — Wire all hooks together with the proper matchers and exit-code conventions. **Slug:** `claude-settings-hooks-wiring`. **Depends on:** F2.1–F2.5. **Shipped:** 2026-05-21.

- [ ] **F2.7** `validate-ost.py` — PostToolUse hook on `discovery/trees/**` writes that runs the OST validator and aborts on failure. **Slug:** `hook-validate-ost`. **Depends on:** P2.8 (script-ost-validator).

- [x] **F2.8** `guard-credentials.py` — PreToolUse(Bash) hook that blocks touches to `~/.ssh`, `.env*`, and credential paths. **Slug:** `hook-guard-credentials`. **Shipped:** 2026-05-21.

- [ ] **F2.9** `pin-date.sh` — SessionStart hook that runs the dates skill and pins today's date into the session context so Claude doesn't drift to its training-data year. **Slug:** `hook-pin-date`. **Depends on:** P9.1 (skill-dates).

---

## Foundation 0-X — Build-harness additions (surfaced by reconcile-and-harden pass, 2026-05-21)

Items appended after Foundation 0 was marked complete. Same Foundation-0 character (build harness / linters / templates / scripts), surfaced by adversarial-reviewer findings during the inaugural reconcile-and-harden pass (see `docs/specs/reconcile-existing-components/notes/deferred-findings.md`).

- [x] **F0.10** `tools/lint-hook.sh` — Shape linter for hook documentation files under `.claude/hooks/`. Referenced by the work-loop SKILL §3.2 as the per-component-type linter for hooks. **Slug:** `tool-lint-hook`. **Source:** D1 (work-loop reviewer finding). **Shipped:** 2026-05-21.

- [x] **F0.11** `docs/_templates/spec.md` frontmatter additions — Chose option (b): documented spec template as an explicit exemption from the universal-metadata schema. Narrowed "every artifact" → "every product artifact" across AGENTS.md, .claude/CLAUDE.md, README.md, CONTRIBUTING.md, docs/CHARTER.md, docs/CONVENTIONS.md (lines 7, 14, YAML-block comment); added `### Exempt from the universal metadata schema` sub-section to CONVENTIONS.md §"Specs and Plans"; added one-line exemption note to the spec template. **Slug:** `template-kit-spec-frontmatter`. **Source:** D2 (reconcile-existing-components OQ5). **Shipped:** 2026-05-21.

- [x] **F0.12** `lint-frontmatter.py` — extend `ai_assistance_allowed` enforcement. Added rule: `ai_assistance_allowed: restricted` ⇒ `ai_assistance_used:` non-empty list (with strengthened `not isinstance(aiu, list)` check that rejects scalar strings, dicts, ints). 5 fixtures + 7 unittest tests under `scripts/tests/test_lint_frontmatter.py`. Latent non-list bug in the existing `human_approval_required` rule recorded as F0.12-D1 in `docs/specs/lint-frontmatter-ai-assistance-allowed/notes/deferred-findings.md`. **Slug:** `lint-frontmatter-ai-assistance-allowed`. **Source:** D8 (HUMAN-AI-OWNERSHIP reviewer finding). **Shipped:** 2026-05-21.

- [x] **F0.13** `INVENTORY.md` "Produces (ontology)" column refactor — Chose option (c): renamed column to "Produces (output)" across all twelve tables; updated legend (`**Type:**` → `**Output:**`) and line-3 prose. Cell values unchanged. **Slug:** `inventory-produces-column-refactor`. **Source:** D10 (INVENTORY reviewer finding). **Shipped:** 2026-05-21.

- [x] **F1.7** `traceability-walker` agent — Fan-out worker dispatched by `/audit-traceability` per upstream subtree. **Slug:** `agent-traceability-walker`. **Source:** D3 (audit-traceability reviewer finding). **Shipped:** 2026-05-21.

- [ ] **F0.14** `lint-frontmatter` non-list retrofit — F0.12 introduced the strengthened emptiness check (`not isinstance(aiu, list)`) for `ai_assistance_allowed: restricted`. The existing `human_approval_required: true ⇒ human_owned_decisions:` rule still uses the original check, which silently passes a scalar-string value (e.g., `human_owned_decisions: "ship it"`). Retrofit the strengthened check to the existing rule + add `approval-scalar-string` fixture + `test_human_approval_required_with_scalar_string_fails`. **Slug:** `lint-frontmatter-non-list-retrofit`. **Source:** F0.12-D1 (this batch's post-execute defer).

---

## Component-hardening defers (surfaced by reconcile-and-harden pass, 2026-05-21)

Items appended for substantive hardening that exceeded the reconcile-and-harden pass's scope (the pass committed not to build new primitives or substantively rewrite existing ones beyond textual reconciliation). Each row is a sub-task on an existing ROADMAP item OR a new mini-spec.

- [x] **D4** `ost-validator` references — author `references/ost-schema.json`, `references/action-vocabulary.md`, and `references/examples/`. **Sub-task of:** P2.8 (script-ost-validator). **Shipped:** 2026-05-28 (bundled into the P2.8 work-loop).
- [ ] **D5** `adversarial-reviewer` contract expansion — cover specs/plans/core docs (not just product-phase artifacts); add mandatory `location:` field to output schema. **Sub-task of:** P6.3 (audit-all aggregator); or own mini-spec.
- [ ] **D6** `competitor-research` hardening additions beyond the in-pass fixes — feedback-loop integration, sub-agent failure recovery, paid-data-source contract. **Appends to:** Phase 7 strategy items.
- [x] **D7** `handover-2.5-assumption-map` — add a formal Assumption Map handover contract between Discovery (chosen opportunity) and Validation (experiment design). **Source:** HANDOVERS.md reviewer C1. **Shipped:** 2026-05-22 (via `docs/specs/template-authoring-convention/` — Handover 2.5 added to `docs/HANDOVERS.md`).
- [ ] **D9** `ontology-add-handover-composite-types` — the Domain I extension shipped in the reconcile pass; track future RFC if any composite types are added or removed. **Status:** Domain I shipped in this pass; this is the placeholder for future Domain I edits.
- [ ] **D11** `skill-strategy-coherence-hardening` — fix classification-rule overlap on `coherent` vs `drifting`; add `sequenced` classification; specify single-artifact-portfolio behavior. **Sub-task of:** F4.10 (framework-strategic-coherence) and the skill itself.
- [ ] **D12** `audit-completeness-count-reconciliation` — confirm whether the canonical checklist is 25 items (current command), 26 items (per ontology §41 reviewer reading), or another number. Reconcile command + HANDOVERS.md + the ontology source. **Sub-task of:** F1.5.
- [ ] **D13** `audit-portfolio-coherence-fanout-spec` — define the fan-out sub-agent contract for `>10 artifacts` case; define the no-portfolio empty-repo behavior beyond the in-pass stop condition. **Sub-task of:** F1.6.
- [ ] **D14** `hook-assumption-threshold-lock-hardening` — tamper-resistant timestamp proof (git-commit ordering, not mtime); machine-checkable threshold schema; override gate beyond honor-system; concurrent-write handling. **Sub-task of:** F2.2.
- [ ] **D15** `cmd-phase-guide-routing-expansion` — add Validation sub-phase routing rows; add multi-intent navigation; define "signed off" operationally. **Sub-task of:** existing `/phase-guide` command.
- [ ] **D16** `doc-phase-guide-row-expansion` — add killed-path row (partially done in this pass); add single-spec-path row; add multi-intent guidance. **Sub-task of:** PHASE-GUIDE.md.
- [ ] **D17** `personal-os-agents-runtime-dir` — populate `personal-os/agents/` runtime directory with the five identity files. **Sub-task of:** P9.6.
- [ ] **D18** `framework-additions-batch` — 6 frameworks catalogued in `context/README.md` but absent from ROADMAP F4: `perri-strategy-stack`, `bland-testing-business-ideas`, `roadmap-as-bets`, `cagan-dual-track`, `context-map` (framework, not the per-initiative artifact), `outcome-vs-prediction`. Either assign F4.x slots or remove from the catalog. **Sub-task of:** F4 batch.
- [ ] **D20** `adversarial-reviewer` block-vs-needs-fixes threshold definition — for kit components (vs product artifacts). **Bundled with D5.**

## Foundation-1-pass defers (surfaced by F1.1–F1.7 reviews, 2026-05-21)

Items the F1.x build identified but did not fix. Each row carries an explicit **when to address** trigger so the next loop knows what to wait for.

- [ ] **F1-G1** `ontology-classifier` live fresh-session verification — F1.3 shipped with structural verification only (the SKILL.md and golden fixtures are concrete enough for a fresh-session verifier to compare against). Recorded in `docs/specs/ontology-classifier-skill/notes/manual-verification-2026-05-21.md`. **When to address:** before the kit transitions to multi-contributor v1, OR the first time a real human (not the original author) uses the skill against unstructured input. Append the live-session results to the same notes folder.

- [ ] **F1-G2** `graph.cycles()` Python recursion limit — `scripts/lib/graph.py:strongconnect()` is recursive. Default `sys.setrecursionlimit` is 1000; a kit graph with a 1000-hop parent chain (rare but possible in a large portfolio scan) will raise `RecursionError`. **When to address:** before F1.6 or F1.7 is invoked against a real portfolio with >500 typed nodes. Convert `strongconnect` to an explicit stack. Sub-task of F1.1.

- [ ] **F1-G3** `walk_up` vs `walk_down` BFS-style symmetry — both yield in BFS order, but their implementations differ (`walk_up` uses a level-by-level loop; `walk_down` uses an explicit `deque`). For graphs with multiple parents at the same depth, ordering may diverge between the two methods. **When to address:** if F1.7 (or any future downstream consumer) starts depending on symmetric traversal order. Sub-task of F1.1.

- [ ] **F1-G4** Scope-filter + `related_*` edges interaction — `_apply_scope` traverses only `parent_*` edges. Nodes reachable only via `related_*` edges from an in-scope node are excluded from the scoped graph. F1.5's traceability sub-audit calls F1.4 with `--scope <target-slug>`; orphan and dangling-edge results on the scoped graph may differ from a full-graph audit for nodes whose parents are related-only. **When to address:** when F1.5 in production produces orphan reports that contradict a full-graph audit on the same target. Sub-task of F1.1.

- [ ] **F1-G5** F1.4 broken-verdict test precision — `test_broken_verdict_on_broken_fixtures` accepts exit 1 OR 2 because the current broken fixture only produces 2 broken links (drift threshold, not broken). **When to address:** before `/audit-all` (P6.3) ships, OR if the audit's verdict thresholds change. Either extend the broken fixture to produce >3 broken links, or rename the test to `test_drift_or_broken_on_known_breakage` (the more honest contract). Sub-task of F1.4.

- [ ] **F1-G6** F1.5 sparse-packet test sharpness — `test_produces_verdict_on_sample_kit_packet` accepts any of {pass, needs-fixes, block} because the sample-kit packet only populates ~3 of the 25 checklist fields (it was built for graph-walking tests, not completeness tests). **When to address:** when F1.5 needs to gate a real handoff. Author a fully-populated `fixtures/completeness-packet/` fixture and add `test_pass_verdict_on_complete_packet` + `test_needs_fixes_verdict_on_packet_with_2_weak_items` (specified in the spec's contract tests, currently relaxed). Sub-task of F1.5.

- [ ] **F1-G7** `CONVENTIONS.md` formal amendment for `related_capabilities` — F1.1 added `related_capabilities` to `RELATED_FIELDS` because handoff-packet `requirements.yaml` files use it to trace Requirements → Capabilities. The field is not in `docs/CONVENTIONS.md`'s universal schema example block. **When to address:** before the next CONVENTIONS.md edit, OR when adding any other new `related_*` field. Append `related_capabilities` to the example block with a one-line note. Sub-task of F1.1 (doc-only).

- [ ] **F1-G8** `audit-traceability` Rule 4–7 fixture coverage — F1.4's unit tests cover Rule 1 end-to-end and Rule 3 via the sample-kit `evidence_basis`. Rules 4 (KPI→Outcome), 5 (high-risk Requirement owner+mitigation), 6 (Decision→ADR), 7 (Handoff Packet fixed_vs_flexible) are exercised by the rule-implementation logic but not by named contract tests against a fixture that triggers each. **When to address:** before any production audit run, OR if a Rule 4–7 violation is missed in real usage. Add one fixture-per-rule under `scripts/tests/fixtures/traceability/`. Sub-task of F1.4.

- [ ] **F1-G9** F1.5 `CHECKS` dict introspection on Python 3.13 — `importlib.util.spec_from_file_location` on `audit-completeness.py` fails because Python 3.13's dataclass-introspection touches `sys.modules.get(cls.__module__).__dict__` and the loaded-from-file module is not registered there. The contract test routed around this via end-to-end subprocess invocation. **When to address:** when adding any test that needs to introspect the script's internals (e.g., counting check functions without running them, or unit-testing individual check functions). Either register the loaded module in `sys.modules` before exec, or refactor `audit-completeness.py` to import-friendly. Sub-task of F1.5.

- [ ] **F1-G10** F1.5 `_resolve_packet` multi-packet tie-break documented but untested — when a single slug has multiple packet README files (e.g., dated revisions), `_resolve_packet` picks the most-recently-modified. The spec says "use most-recently-modified; surface older in open_questions." The "surface older in open_questions" half is not implemented. **When to address:** when adopters start producing multiple dated packets per slug, or when a real audit silently picks a stale packet. Sub-task of F1.5.

## Governance defers — RFC candidates (surfaced by reconcile-and-harden pass)

Items that originated as ADR-review findings. ADRs were edited inline in this pass (user authorization for v0.x); these are kept for future RFC consideration once the kit ships v1 and the frozen-ADR discipline reactivates.

- [ ] **RFC1** ADR 0001 — full delivery audit of "what was promised vs what shipped" (addressed in this pass via Decision Outcome rewrites; track for v1 review).
- [ ] **RFC4** ADR 0001 — empirical verification of "cross-tool portability" claim across Cursor / Codex / Gemini CLI / Copilot.
- [ ] **RFC6** ADR 0002 — confirm `Shipped` / `Frozen` kit-build lifecycle states + Domain I composite types are stable enough to freeze.

---

## Foundation 3 — Templates per ontology type

Once the type system has enforcement, per-type frontmatter templates make correct artifact creation cheap. Each template is short — a frontmatter block plus a one-line note on required sections.

> F3.x items consume the authoring convention from `docs/specs/template-authoring-convention/`. Read that spec first; copy `templates/_meta/template-skeleton.md` to start each F3.x template.

- [x] **F3.1** Strategic Intent template (`templates/strategic-intent.md`). **Slug:** `template-strategic-intent`. **Shipped:** 2026-05-22.
- [x] **F3.2** OST template (`templates/ost.md`). **Slug:** `template-ost`. **Shipped:** 2026-05-22.
- [x] **F3.3** Assumption Map template (`templates/assumption-map.md`). **Slug:** `template-assumption-map`. **Shipped:** 2026-05-22.
- [x] **F3.4** Experiment design + results templates. **Slug:** `template-experiment`. **Shipped:** 2026-05-22.
- [x] **F3.5** Learning Memo template. **Slug:** `template-learning-memo`. **Shipped:** 2026-05-22.
- [x] **F3.6** Vision template. **Slug:** `template-vision`. **Shipped:** 2026-05-22.
- [x] **F3.7** Initiative README + context-map + flow + child-specs + sequence + capabilities templates. **Slug:** `template-initiative`. **Shipped:** 2026-05-22.
- [x] **F3.8** Spec template (PM-side — distinct from the kit's spec template). **Slug:** `template-pm-spec`. **Shipped:** 2026-05-22.
- [x] **F3.9** Handoff Packet template (`templates/handoff-packet/` with the 23 required sections from the ontology). **Slug:** `template-handoff-packet`. **Shipped:** 2026-05-22.
- [x] **F3.10** Landing Report template. **Slug:** `template-landing-report`. **Shipped:** 2026-05-22.

---

## Foundation 4 — Reference frameworks

The `context/frameworks/*.md` reference files are pulled on demand by skills and commands. Several are referenced but don't yet exist; build them so the on-demand context loading doesn't go to broken links.

- [x] **F4.1** `continuous-discovery.md` — Torres's weekly habit loop. **Slug:** `framework-continuous-discovery`. **Shipped:** 2026-05-28.
- [x] **F4.2** `opportunity-solution-tree.md` — OST node types, source opportunities, structure. **Slug:** `framework-ost`. **Shipped:** 2026-05-28.
- [x] **F4.3** `interview-snapshot.md` — Snapshot schema and transcript extraction rules. **Slug:** `framework-interview-snapshot`. **Shipped:** 2026-05-28.
- [x] **F4.4** `assumption-tests.md` — Five-lens taxonomy (desirability / viability / feasibility / usability / ethical). **Slug:** `framework-assumption-tests`. **Shipped:** 2026-05-28.
- [x] **F4.5** `falsification.md` — What "survived" means; predeclared threshold pattern. **Slug:** `framework-falsification`. **Shipped:** 2026-05-28.
- [x] **F4.6** `validation-theatre.md` — Failure modes; "would you pull the work?" test. **Slug:** `framework-validation-theatre`. **Shipped:** 2026-05-28.
- [x] **F4.7** `rumelt.md` — Diagnosis / guiding policy / coherent actions; failure modes. **Slug:** `framework-rumelt`. **Shipped:** 2026-05-28.
- [x] **F4.8** `wardley.md` — Value chain, evolution axis, climatic patterns. **Slug:** `framework-wardley`. **Shipped:** 2026-05-28.
- [x] **F4.9** `jtbd.md` — Christensen / Ulwick formulations. **Slug:** `framework-jtbd`. **Shipped:** 2026-05-28.
- [x] **F4.10** `strategic-coherence.md` — Three axes (resources / capabilities / market posture); incoherence patterns. **Slug:** `framework-strategic-coherence`. **Shipped:** 2026-05-28.
- [x] **F4.11** `landings-not-launches.md` — Adoption curve is part of the work. **Slug:** `framework-landings-not-launches`. **Shipped:** 2026-05-28.
- [x] **F4.12** `ears.md` — EARS pattern for spec sentences. **Slug:** `framework-ears`. **Shipped:** 2026-05-23.
- [x] **F4.13** `competitive-analysis.md` — What a thorough analysis contains. **Slug:** `framework-competitive-analysis`. **Shipped:** 2026-05-28.

---

## Phase 2 — Discovery commands

The highest-volume PM activity. Build these before Phase 1 strategy commands because Discovery work happens weekly while Strategy work happens quarterly.

- [x] **P2.1** `/interview-snapshot` — Raw transcript → structured snapshot. **Slug:** `cmd-interview-snapshot`. **Depends on:** F4.3. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-pipeline/`).
- [x] **P2.2** `interview-snapshot` skill — Speaker detection + time-aligned quotes (used by the command). **Slug:** `skill-interview-snapshot`. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-primitives/`).
- [x] **P2.3** `interview-coder` agent — Fan-out worker, one transcript at a time. **Slug:** `agent-interview-coder`. **Depends on:** P2.2. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-pipeline/`).
- [x] **P2.4** `/extract-opportunities` — Snapshots → opportunity candidates. **Slug:** `cmd-extract-opportunities`. **Depends on:** P2.1. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-pipeline/`).
- [x] **P2.5** `opportunity-clustering` skill — Theme raw opportunities into clusters. **Slug:** `skill-opportunity-clustering`. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-primitives/`).
- [x] **P2.6** `/cluster-opportunities` — Group raw opportunities. **Slug:** `cmd-cluster-opportunities`. **Depends on:** P2.5. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-pipeline/`).
- [x] **P2.7** `/generate-ost` — First-pass OST from snapshots + the strategic intent. **Slug:** `cmd-generate-ost`. **Depends on:** F4.2, P2.4. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-pipeline/`).
- [x] **P2.8** `ost-validator` script — Promote the existing skill's procedure to a runnable `scripts/validate_ost.py`. **Slug:** `script-ost-validator`. **Depends on:** F1.2. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-primitives/`; closes D4 in the same loop — `references/ost-schema.json`, `references/action-vocabulary.md`, `references/examples/`).
- [x] **P2.9** `/update-ost` — Integrate new interview content; emits change set + tree; calls the validator. **Slug:** `cmd-update-ost`. **Depends on:** P2.7, P2.8. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-pipeline/`).
- [x] **P2.10** `opportunity-merger` agent — Fan-out worker on `/update-ost` per OST node. **Slug:** `agent-opportunity-merger`. **Depends on:** P2.9. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-pipeline/`).
- [x] **P2.11** `/audit-discovery-coherence` — Flag OSTs without parent intent. **Slug:** `cmd-audit-discovery-coherence`. **Depends on:** F1.1. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-audits-and-comms/`).
- [x] **P2.12** `/opportunity-narrative` — Write up the chosen opportunity for the validation handover. **Slug:** `cmd-opportunity-narrative`. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-audits-and-comms/`).
- [x] **P2.13** `discovery-coach` agent — Auto-invoke when stuck on an opportunity. **Slug:** `agent-discovery-coach`. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-primitives/`; manual invocation today, auto-invoke wiring deferred to a future ROADMAP item).
- [x] **P2.14** `/discovery-update` — Weekly stakeholder digest. **Slug:** `cmd-discovery-update`. **Shipped:** 2026-05-28 (via `docs/specs/phase-2-discovery-audits-and-comms/`).

---

## Phase 3 — Validation commands

The kit's most important guard surface. The `assumption-threshold-lock` hook from Foundation 2 enforces predeclaration; these commands produce the artifacts the hook checks.

- [ ] **P3.1** `/assumption-test` — Design a test using the five-lens taxonomy. **Slug:** `cmd-assumption-test`. **Depends on:** F4.4.
- [ ] **P3.2** `assumption-skeptic` agent — "Would you actually pull the work?" theatre detector. **Slug:** `agent-assumption-skeptic`. **Depends on:** F4.6.
- [ ] **P3.3** `experiment-template` skill — Scaffold the experiment folder. **Slug:** `skill-experiment-template`. **Depends on:** F3.4.
- [ ] **P3.4** `/design-experiment` — Turn the test into a runnable experiment with predeclared threshold. **Slug:** `cmd-design-experiment`. **Depends on:** P3.3.
- [ ] **P3.5** `experiment-designer` agent — Proposes the cheapest valid test. **Slug:** `agent-experiment-designer`.
- [ ] **P3.6** `/test-cost-vs-evidence` — Prioritize backlog by cost vs evidence needed. **Slug:** `cmd-test-cost-vs-evidence`.
- [ ] **P3.7** `/run-assumption-test` — Capture results; compute pass/fail vs the predeclared threshold. **Slug:** `cmd-run-assumption-test`. **Depends on:** F2.2.
- [ ] **P3.8** `/falsify-or-confirm` — Write the learning memo; flip status; propagate. **Slug:** `cmd-falsify-or-confirm`. **Depends on:** P3.7.
- [ ] **P3.9** `/kill-or-survive` — Formal opportunity disposition. **Slug:** `cmd-kill-or-survive`.
- [ ] **P3.10** `/learning-memo` — Synthesize learning separately from the proceed decision. **Slug:** `cmd-learning-memo`.
- [ ] **P3.11** `/audit-assumption-coverage` — Flag chosen opportunities with no assumption map. **Slug:** `cmd-audit-assumption-coverage`. **Depends on:** F1.1.
- [ ] **P3.12** `/audit-vision-evidence` — Flag visions citing untested assumptions. **Slug:** `cmd-audit-vision-evidence`. **Depends on:** F1.1.
- [ ] **P3.13** `/validation-update` — Weekly stakeholder digest. **Slug:** `cmd-validation-update`.

---

## Phase 4 — Delivery and Engineering Handoff

> P4.1, P4.3, P4.4, P4.5, P4.6, P4.8, P4.11 items consume the command convention from `docs/specs/phase-4-command-convention/`. Read that spec first; copy `.claude/commands/_meta/command-skeleton.md` to start each command.

The culmination: producing the validated engineering-handoff packet.

- [x] **P4.1** `/draft-vision` — Vision from learning memo + persona + product. **Slug:** `cmd-draft-vision`. **Depends on:** F3.6. **Shipped:** 2026-05-23.
- [x] **P4.2** `/vision-shape-check` — Crosses teams? Initiative or single spec? **Slug:** `cmd-vision-shape-check`. **Shipped:** 2026-05-23.
- [x] **P4.3** `/draft-initiative` — Build the initiative folder structure. **Slug:** `cmd-draft-initiative`. **Depends on:** F3.7. **Shipped:** 2026-05-23.
- [x] **P4.4** `/context-map` — Interactive bounded-contexts + Wardley-lite evolution check. **Slug:** `cmd-context-map`. **Shipped:** 2026-05-23.
- [x] **P4.5** `/end-to-end-flow` — Mermaid cross-team flow. **Slug:** `cmd-end-to-end-flow`. **Shipped:** 2026-05-23.
- [x] **P4.6** `/sequence-initiative` — Dependency-aware delivery sequence. **Slug:** `cmd-sequence-initiative`. **Shipped:** 2026-05-23.
- [x] **P4.7** `ears-lint` skill — EARS pattern checker for spec sentences. **Slug:** `skill-ears-lint`. **Depends on:** F4.12. **Shipped:** 2026-05-23.
- [x] **P4.8** `/draft-spec` — Spec from initiative + context-map row + EARS guidance. **Slug:** `cmd-draft-spec`. **Depends on:** P4.7 (EARS-lint skill planned; this command emits the EARS-pattern prompt without mechanical lint). **Shipped:** 2026-05-23.
- [x] **P4.9** `/spec-impact-analysis` — What changes if this spec changes? **Slug:** `cmd-spec-impact-analysis`. **Shipped:** 2026-05-23.
- [x] **P4.10** `/audit-spec-linkage` — Every spec needs `parent_initiative:`. **Slug:** `cmd-audit-spec-linkage`. **Depends on:** F1.1. **Shipped:** 2026-05-23.
- [x] **P4.11** `/handoff-packet` — Assemble the 23-section engineering deliverable. **Slug:** `cmd-handoff-packet`. **Depends on:** F3.9, F1.5. **Shipped:** 2026-05-23.
- [x] **P4.12** `/release-notes` — Customer-facing notes. **Slug:** `cmd-release-notes`. **Shipped:** 2026-05-23.
- [x] **P4.13** `/launch-comms` — Internal + external launch messaging. **Slug:** `cmd-launch-comms`. **Shipped:** 2026-05-23.
- [x] **P4.14** `/launch-checklist` — Change-type-aware checklist. **Slug:** `cmd-launch-checklist`. **Shipped:** 2026-05-23.
- [x] **P4.15** `/retro` — Facilitated retro. **Slug:** `cmd-retro`. **Shipped:** 2026-05-23.
- [x] **P4.16** `roadmap-skeptic` agent — Bets vs commitments lens. **Slug:** `agent-roadmap-skeptic`. **Shipped:** 2026-05-23.

---

## Phase 5 — Landings

Closes the loop. Runs after delivery, feeds into the next strategy cycle.

- [ ] **P5.1** `/landing-report` — Adoption / outcome / counter-metric vs vision predictions. **Slug:** `cmd-landing-report`. **Depends on:** F3.10.
- [ ] **P5.2** `/adoption-readout` — Adoption curve only. **Slug:** `cmd-adoption-readout`.
- [ ] **P5.3** `/outcome-vs-prediction` — Mechanical diff against predeclared thresholds. **Slug:** `cmd-outcome-vs-prediction`.
- [ ] **P5.4** `/cohort-analysis` — Slice by segment / surface / cohort. **Slug:** `cmd-cohort-analysis`.
- [ ] **P5.5** `cohort-analyst` agent — Fan-out, one cohort at a time. **Slug:** `agent-cohort-analyst`.
- [ ] **P5.6** `/landing-interview` — Qualitative follow-up with adopters AND non-adopters. **Slug:** `cmd-landing-interview`.
- [ ] **P5.7** `landing-skeptic` agent — "What would have to be true for us to revert?" **Slug:** `agent-landing-skeptic`.
- [ ] **P5.8** `/landings-update` — Stakeholder digest. **Slug:** `cmd-landings-update`.
- [ ] **P5.9** `/audit-landings-debt` — Flag shipped initiatives without a landing report after 30 days. **Slug:** `cmd-audit-landings-debt`. **Depends on:** F1.1.
- [ ] **P5.10** `landings-manager` scheduled agent — Mid-week landings-debt scan (CRON Wed 7am). **Slug:** `sched-landings-manager`.

---

## Phase 6 — Reviewer agents and the work-loop closure

The work-loop SKILL names three reviewer subagents but only `adversarial-reviewer` ships in v3. Add the other two and a thin coordinator.

- [ ] **P6.1** `compliance-reviewer` agent — Regulatory, legal, privacy, ethics lens. Used by the work-loop when an artifact touches user data, claims, pricing, safety, or regulated workflows. **Slug:** `agent-compliance-reviewer`.
- [x] **P6.2** `quality-engineer` agent — Testability, observability, reliability, maintainability lens. Used for specs and handoff packets. **Slug:** `agent-quality-engineer`. **Shipped:** 2026-05-21.
- [ ] **P6.3** `/audit-all` — Aggregator that runs every handover audit in sequence and produces the one-page portfolio report. **Slug:** `cmd-audit-all`. **Depends on:** F1.4, F1.5, F1.6, P2.11, P3.11, P3.12, P4.10, P5.9.

---

## Phase 7 — Phase 1 strategy commands (the missing ones)

Lower-frequency than discovery/validation but completes the cycle. The `/competitive-research` command and `competitor-research` agent already ship in v3.

- [ ] **P7.1** `/strategy-refresh` — Draft a Rumelt-style diagnosis from current state. **Slug:** `cmd-strategy-refresh`. **Depends on:** F4.7.
- [ ] **P7.2** `/strategic-intent` — Synthesize the one-pager. **Slug:** `cmd-strategic-intent`. **Depends on:** F3.1.
- [ ] **P7.3** `strategy-skeptic` agent — Challenges drafts with Rumelt's failure modes. **Slug:** `agent-strategy-skeptic`. **Depends on:** F4.7.
- [ ] **P7.4** `/exec-strategy-narrative` — Turn the intent into a 6-pager. **Slug:** `cmd-exec-strategy-narrative`.
- [ ] **P7.5** `/cadence-check` — Detect drift across quarterly/monthly/weekly rhythms. **Slug:** `cmd-cadence-check`. **Depends on:** F1.1.
- [ ] **P7.6** `cadence-manager` scheduled agent — First-Monday-of-month cadence-drift report. **Slug:** `sched-cadence-manager`. **Depends on:** P7.5.

### Enterprise-mode strategy

- [ ] **P7.7** `/wardley-map` — Interactive value-chain mapping with evolution axis. **Slug:** `cmd-wardley-map`. **Depends on:** F4.8.
- [ ] **P7.8** `wardley-evolution` skill — Place components on the evolution axis. **Slug:** `skill-wardley-evolution`. **Depends on:** F4.8.
- [ ] **P7.9** `/internal-jtbd-interview` — Interview prep + analysis for the captive user base. **Slug:** `cmd-internal-jtbd-interview`. **Depends on:** F4.9.
- [ ] **P7.10** `/value-chain-evolution` — Diff the value chain across quarters. **Slug:** `cmd-value-chain-evolution`.

### Greenfield-mode strategy

- [ ] **P7.11** `/market-scan` — Analogical scan across the wider industry. **Slug:** `cmd-market-scan`.
- [ ] **P7.12** `/jtbd-analogues` — Surface jobs being hired-for in adjacent markets. **Slug:** `cmd-jtbd-analogues`. **Depends on:** F4.9.

---

## Phase 8 — Communication and Research

Cross-cutting commands that support every phase.

- [ ] **P8.1** `/stakeholder-update` — Auto-compose from current state across all phases. **Slug:** `cmd-stakeholder-update`.
- [ ] **P8.2** `/exec-narrative` — 6-pager on a strategic question. **Slug:** `cmd-exec-narrative`.
- [ ] **P8.3** `/battlecard` — One-competitor sales battlecard. **Slug:** `cmd-battlecard`.
- [ ] **P8.4** `voice-check` skill — Voice-guide rubric for customer-facing drafts. **Slug:** `skill-voice-check`.
- [ ] **P8.5** `/headlines` — 3-5 headlines × 7 categories. **Slug:** `cmd-headlines`.
- [ ] **P8.6** `/seo` — Content + keyword + volume analysis. **Slug:** `cmd-seo`.
- [ ] **P8.7** `/critique` — Direct feedback on a draft. **Slug:** `cmd-critique`. **Depends on:** P8.4.
- [ ] **P8.8** `writing-critic` agent — Voice-aware review (dispatched by `/critique`). **Slug:** `agent-writing-critic`.
- [ ] **P8.9** `section-fact-checker` agent — Fan-out, one section at a time. **Slug:** `agent-section-fact-checker`.
- [ ] **P8.10** `/research-digest` — Academic + industry digest. **Slug:** `cmd-research-digest`.
- [ ] **P8.11** `/summarize-paper` — Structured summary of one PDF. **Slug:** `cmd-summarize-paper`.
- [ ] **P8.12** `paper-summarizer` agent — Fan-out, one paper at a time. **Slug:** `agent-paper-summarizer`.

---

## Phase 9 — Personal OS

Daily-rhythm convenience. Independent of the other phases.

- [ ] **P9.1** `dates` skill — today/tomorrow/this-week/next-week. Eliminates the "Claude thinks it's 2024" failure. **Slug:** `skill-dates`.
- [ ] **P9.2** `/today` — Pull tasks, build today.md, run dates, surface AI-helpable items. **Slug:** `cmd-today`. **Depends on:** P9.1.
- [ ] **P9.3** `/inbox` — Triage and file inbox. **Slug:** `cmd-inbox`.
- [ ] **P9.4** `/meeting-prep` — Prep brief for next calendar event. **Slug:** `cmd-meeting-prep`.
- [ ] **P9.5** `/weekly-retro` — Surface session patterns. **Slug:** `cmd-weekly-retro`.
- [ ] **P9.6** Scheduled agents — `podcast-manager`, `sales-admin`, `coding-manager`, `discovery-manager`, `validation-manager`. **Slug:** `sched-personal-os-agents`. **Depends on:** P9.1.

---

## When to deviate from the order

Skipping ahead is allowed but each skip should be deliberate. The pattern:

- **Skipping a foundation item** trades long-term leverage for short-term progress. Note it in the spec's `## Why now` section.
- **Skipping a phase** (jumping from Phase 2 to Phase 4 because Phase 3 isn't urgent) is fine — but the items inside each phase still have local dependencies.
- **Never skip the work-loop** for an item just because it's "small." The loop catches the same failures regardless of size.

---

## Done definition for the whole roadmap

The kit is "complete" when:

1. Every item above is checked.
2. `tools/pre-pr.sh` returns clean against the whole kit.
3. The twelve failure modes from `docs/PHASE-GUIDE.md` (the seven core + five v3 additions) each have a mechanical detector that fires on a known-bad fixture and stays silent on a known-good one.
4. A new adopter can clone the repo, run `tools/new-spec.sh`, follow the work-loop, and ship a new kit component without reading source code.

"Complete" is a horizon, not an endpoint. New ontology types, new audits, and new phases will surface over time. When they do, they get RFCs and ADRs — not bolted-on additions.
