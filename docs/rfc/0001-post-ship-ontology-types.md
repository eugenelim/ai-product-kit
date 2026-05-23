# RFC 0001: Add `Launch Communication` (Domain G) and `Launch Checklist` (Domain H)

- **Status:** Accepted (2026-05-23)
- **Drivers:** P4.13 `/launch-comms`, P4.14 `/launch-checklist`
- **Decision owner:** kit author + first adopter (eugenelim)

## Summary

Add two new atomic ontology types to `context/frameworks/ontology.md` to support Phase-4 post-ship commands shipped in Wave 4 (2026-05-23):

- **`Launch Communication`** — Domain G (Operational Readiness). Per-launch, per-audience messaging draft (internal-team announcement, external blog post, customer email). Authored post-ship by `/launch-comms` (P4.13) from a Handoff Packet.
- **`Launch Checklist`** — Domain H (Governance, Decisions, and Handoff). Change-type-aware operational gate authored post-handoff by `/launch-checklist` (P4.14). Sibling-child of a Handoff Packet; per-item human confirmation records what was actually cleared before launch.

The total atomic-type count moves from 74 to 76; the Domain-I composite count remains 8. The kit-wide total moves from 82 documented types to 84.

## Why

P4.13 and P4.14 shipped four template files (`templates/launch-comms/{internal,blog,email}.md`; `templates/launch-checklist/{new-feature,breaking-change,pricing,regulated}.md`) whose frontmatter declares an `object_type:` field. The closest existing types were:

- For `Launch Communication`: `Customer Communication` (Domain G, "External messaging") — fits `blog.md` and `email.md` but mis-types `internal.md` (internal-team announcement is not customer-facing). `Communication Plan` (mentioned in HANDOVERS-6 §"Folder contents") is too generic.
- For `Launch Checklist`: `Decision` (Domain H) was a partial fit (the per-item confirmations are Decision-class artifacts), but the operational-gate semantics warrant a named type so downstream consumers (the planned `/landing-report`, the planned `/audit-launches`) can pivot on it.

Both types were flagged as RFC-pending in the originating specs' open questions (P4.13 OQ2; P4.14 OQ6). This RFC closes those.

## Decision

**Accept both additions.** Reasoning:

1. **Domain placement is principled.** `Launch Communication` lives alongside `Launch Plan` and `Rollout Strategy` in Domain G (Operational Readiness — "whether the business can support, sell, launch, govern"). `Launch Checklist` lives in Domain H alongside `Approval` and `Decision` (governance + sign-off semantics).
2. **The frontmatter linter enforces ontology membership.** Shipping the templates with `object_type: Launch Communication` and `object_type: Launch Checklist` required the types to be added to `ontology.md`; the alternative ("ship without `object_type:` declared") would silently violate the universal metadata schema.
3. **No conflict with existing types.** Both names are non-overlapping with existing entries in their domains. The naming convention (`Launch <Noun>`) is consistent with the existing `Launch Plan`.

## Consequences

- `tools/lint-frontmatter.py`'s default `OBJECT_TYPE_SET` is regenerated from `ontology.md` at runtime; no code change needed.
- `ontology-classifier` skill's prompt mentions "74 atomic + 8 composite"; updated to "76 atomic + 8 composite" in the same Wave-4 commit. Other counts across `AGENTS.md`, `README.md`, `context/README.md`, `.claude/CLAUDE.md`, `.claude/skills/README.md`, `docs/INVENTORY.md` also updated.
- ADR 0002 ("Adopt product/business ontology") is **not** modified — it is a frozen historical decision (the per-AGENTS.md "Architecture Decision Records — frozen" rule). The ADR's count of "74 atomic types" reflects the state at adoption time; this RFC moves the count forward without rewriting history.

## Alternatives considered

- **Re-type `internal.md` as `Customer Communication` (Domain G existing).** Rejected: internal-team announcements are not customer-facing; using a "Customer Communication" type for internal copy would silently violate the type's definition.
- **Re-type `Launch Checklist` artifacts as `Decision` (Domain H existing).** Rejected: a Launch Checklist is composite (one named artifact with multiple per-item Decision-like records); using the plain `Decision` type loses the change-type-keyed structure that downstream consumers will want to pivot on.
- **Defer until a real adopter requests it.** Rejected: the templates ship with `object_type:` declared (they have to — the universal metadata schema requires it); deferring the type definition would ship a known-broken artifact.

## Cross-references

- `docs/specs/cmd-launch-comms/spec.md` Open Question 2 (resolved by this RFC).
- `docs/specs/cmd-launch-checklist/spec.md` Open Question 6 (resolved by this RFC).
- `context/frameworks/ontology.md` — the two type entries (Domain G line and Domain H line).
- `templates/launch-comms/{internal,blog,email}.md` — consume `Launch Communication`.
- `templates/launch-checklist/{new-feature,breaking-change,pricing,regulated}.md` — consume `Launch Checklist`.
