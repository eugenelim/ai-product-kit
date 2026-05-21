# Human vs AI ownership

This kit operates on a single load-bearing principle, lifted from the product/business ontology:

> **AI may assist with analysis, synthesis, drafting, comparison, and consistency checking. Humans must own judgment, accountability, commitments, ethics, prioritization, and final decisions.**

This document specifies which activities sit where, and what every kit artifact must declare in its frontmatter.

## The three zones

Every activity in the PM workflow lives in one of three zones:

- **AI-assisted** — AI can produce a draft or analysis; humans review and approve
- **Human-led with AI support** — A human directs the work and owns interpretation; AI supports
- **Human-only** — A human must be the sole, accountable owner. AI can suggest inputs but cannot be the decision-maker

The default is *human-led with AI support*. Activities listed below as *AI-assisted* are explicitly cleared; activities listed as *human-only* are explicitly restricted.

## What AI can assist with (zone 1)

AI is useful for transforming messy information into structured artifacts:

- Drafting (PRDs, briefs, release notes, FAQs)
- Summarizing (interview notes, support tickets, papers, meetings)
- Pattern detection and feedback clustering
- Requirements cleanup and consistency checking
- Persona draft creation from raw signals
- Workflow extraction from transcripts
- Competitive summaries
- Assumption generation (surfacing what's *implied* but unstated)
- Risk identification
- Scenario exploration
- Test-case and acceptance-criteria suggestions
- Documentation drafts
- Engineering-handoff packet summaries
- Traceability matrix generation

Human review is required before treating any AI output as valid.

## Where humans must lead (zone 2)

Humans direct, AI supports. The human is the named decision owner in the artifact's frontmatter.

- Strategy and strategic-intent selection
- Customer interviews and field observation
- Customer-relationship and trust-sensitive conversations
- Interpretation of emotional, political, or organizational nuance
- Discovery strategy: what to learn next and from whom
- Problem prioritization and severity assessment
- Tradeoff decisions between customer value and business value
- Opportunity selection: what to build, what to leave alone
- Differentiation strategy
- Stakeholder alignment and cross-functional negotiation
- Launch readiness decisions
- Risk interpretation

## Where humans must completely own (zone 3)

These decisions cannot be delegated to AI. AI may produce input, but a human must be the accountable, named, signed-off owner.

### Strategic
- Whether to enter a market or serve a segment
- Whether to commit to a strategic intent
- Roadmap priority and resource allocation
- What we are willing *not* to build

### Customer-facing
- Customer commitments (in contracts, in conversations, in writing)
- Customer-facing claims (marketing copy, sales talking points, public statements)
- Customer trust and consent boundaries
- Ethical handling of sensitive information

### Commercial
- Pricing decisions
- Packaging and entitlement boundaries
- Revenue forecasts used externally
- Willingness-to-pay conversations and commitments

### Compliance and safety
- Legal interpretation and approval
- Compliance approval (GDPR, HIPAA, SOC 2, internal risk policy)
- Privacy decisions affecting user data
- Safety-critical decisions
- Ethical-risk decisions
- Permission and data-access policy

### Launch and operations
- Launch approval
- Incident and escalation policy
- External messaging approval
- Whether to override an AI-generated recommendation

## Frontmatter requirement

Every kit artifact carries this in frontmatter:

```yaml
human_owned_decisions:
  - <decision a human must make personally>
  - <another>
ai_assistance_used:
  - <what AI drafted, summarized, or checked>
ai_assistance_allowed: true | restricted | not-allowed
human_approval_required: true | false
approvals_obtained:
  - <role>: <YYYY-MM-DD>
```

### `ai_assistance_allowed` — value semantics

| Value | What it permits | What it forbids |
|---|---|---|
| `true` | Any Zone-1 activity (drafting, summarizing, pattern detection, etc.); AI may also surface options for human review in Zone 2. | Anything in Zone 3 (the human-only catalog below) cannot be AI-authored even with `true`. |
| `restricted` | Only the specific activities listed in the same artifact's `ai_assistance_used:` field. The `ai_assistance_used:` list must be non-empty. | All other AI involvement. Use this when the artifact is in a regulated context or a compliance-sensitive domain. |
| `not-allowed` | No AI-generated content of any kind in the artifact body. AI may still be used to *draft external content* that a human then re-writes from scratch before importing. | Inclusion of AI-generated content without explicit per-block human rewrite. |

The `/audit-completeness` command checks these fields. An artifact with `human_approval_required: true` cannot transition past `In Review` until `approvals_obtained` lists the required signatures. (Today the check is the `/audit-completeness` prose procedure; ROADMAP F1.5 plans the runnable script. The linter `tools/lint-frontmatter.py` currently only enforces "`human_approval_required: true` ⇒ `human_owned_decisions:` non-empty"; full `ai_assistance_allowed` enforcement is ROADMAP F0.12 — see `notes/deferred-findings.md` D8.)

### External publication of AI-generated content

External publication of AI-generated text without substantive human editing is treated as a **customer-facing claim** and falls under Zone 3 regardless of the source artifact's classification. That includes release notes, public FAQs, sales talking points, status-page copy, and any documentation that customers will read. The Zone-1 catalog covers internal drafts; publication is downstream of those drafts and is human-owned.

## Per-phase ownership map

A condensed view of the ontology's per-stage ownership tables, mapped onto the kit's five phases.

### Phase 1 — Strategy

| Activity | Zone | Notes |
|---|---|---|
| Market scan / Wardley map analysis | AI-assisted | Human selects what to investigate |
| Drafting strategic intent | AI-assisted | Human approves the one-sentence central challenge |
| Final strategic-intent decision | Human-only | Named decision owner; recorded as an ADR |
| Portfolio coherence audit | AI-assisted | Surfaces contradictions; human decides remediation |
| Roadmap commitments | Human-only | Even when AI suggests sequencing |

### Phase 2 — Discovery

| Activity | Zone | Notes |
|---|---|---|
| Customer interviews | Human-led | AI may draft guides, suggest questions |
| Interview transcription / clustering / theming | AI-assisted | Human validates patterns |
| Drafting problem statements | AI-assisted | Human approves which problems matter |
| OST generation / updating | AI-assisted | Repair-loop validation runs; human accepts the tree |
| Opportunity selection (`chosen: true`) | Human-only | Recorded in OST frontmatter |

### Phase 3 — Validation

| Activity | Zone | Notes |
|---|---|---|
| Identifying assumptions | AI-assisted | Including surfacing *implicit* assumptions humans haven't named |
| Designing experiments | AI-assisted | Human approves design and threshold |
| Setting falsification threshold | Human-only | Predeclared, locked by hook before results |
| Running experiments | Human-led | Where the experiment involves real customers |
| Interpreting ambiguous results | Human-only | AI may compare against threshold; human decides survived/killed |

### Phase 4 — Delivery

| Activity | Zone | Notes |
|---|---|---|
| Drafting vision | AI-assisted | Human owns customer-shaped narrative |
| Vision shape check (crosses teams?) | AI-assisted | Human approves the call |
| Drafting initiative / context map | AI-assisted | Human owns bounded-context ownership |
| Drafting specs | AI-assisted | Human owns scope, acceptance criteria |
| Final scope, requirement, acceptance-criteria approval | Human-only | Named owner per requirement |
| Compliance / legal sign-off | Human-only | Named legal/compliance owner |
| Pricing implications | Human-only | Even when AI surfaces them |

### Phase 5 — Landings

| Activity | Zone | Notes |
|---|---|---|
| Adoption-data fetching / cohort analysis | AI-assisted | Mechanical |
| Outcome vs prediction comparison | AI-assisted | Mechanical against predeclared thresholds |
| Landing-interview prep | AI-assisted | Human conducts the interviews |
| Verdict (`adopt | fix | kill`) | Human-only | Named decision owner; goes into ADR |

## The seven cross-phase human-only questions

Pulled directly from the ontology. AI never answers these on behalf of the business:

1. Should we enter this market?
2. Should we serve this customer segment?
3. Is this problem important enough to solve?
4. Should this be on the roadmap?
5. What are we willing not to build?
6. Can we make this claim publicly?
7. Should we override the AI-generated recommendation?

## What this is not

- **Not a permission system.** AI doesn't ask for permission per turn. The principle works through frontmatter declarations and the audit chain — an artifact with `human_approval_required: true` and no `approvals_obtained` will fail completeness audits.
- **Not a constraint on automation.** The scheduled team-of-agents runs many activities autonomously. The constraint is on *decisions of record*, not on the work that produces input to decisions.
- **Not infallible.** A human can sign off on a bad call. The ownership model ensures the call is *traceable* to a human, which is what accountability requires.

## When in doubt

If you're not sure which zone an activity sits in: it's zone 2 or 3. AI defaults to "human-led with AI support" rather than "AI-assisted." Promote to AI-assisted only when the activity has been explicitly cleared in this document.
