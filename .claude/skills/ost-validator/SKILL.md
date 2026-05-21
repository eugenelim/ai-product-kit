---
name: ost-validator
description: Validates an Opportunity Solution Tree change set against an input tree to confirm the change set produces the claimed output tree, with no orphans, no double-deletes, no data loss. Use whenever an OST is being generated or updated, before writing to disk. Returns structured pass/fail with specific repair instructions on failure. Phase 2 (Discovery).
license: MIT
---

# ost-validator

When Claude generates or updates an OST, the model emits both the new tree AND a step-by-step change set explaining how it got there. This skill validates that the change set actually produces the claimed tree, and gives the model specific repair instructions if not.

This is the **repair loop** pattern from Teresa Torres's Vistaly AI-OST work: the model fixes its own mistakes in 1–2 turns rather than us silently accepting invalid structural output.

## When to use this skill

- Right after `/generate-ost` from interview snapshots
- Right after `/update-ost`
- Before writing anything under `discovery/trees/`

The `validate-ost` hook calls this skill automatically on PostToolUse(Write on `discovery/trees/**`).

## How to use

Call the bundled script with input tree, output tree, and change set:

```bash
python scripts/validate_ost.py \
  --input  discovery/trees/<tree-id>.json \
  --output /tmp/proposed-tree.json \
  --change-set /tmp/proposed-change-set.json
```

Exit 0 on success, 1 on failure. On failure, writes a JSON report to stderr with every error and a remediation hint.

## Validation rules

1. **Change set determinism** — applying the change set to the input must produce the output node-for-node
2. **No orphans** — every non-root node has a parent after the change set is applied
3. **No double-references** — each source opportunity appears under exactly one tree opportunity
4. **No data loss** — every source opportunity and child of the input is accounted for in the output
5. **Valid action vocabulary** — only `add-outcome`, `add-opportunity`, `add-solution`, `reframe`, `merge`, `split`, `delete`, `reparent`, `add-source-opportunity`
6. **Compound-operation visibility** — if sources moved between tree opportunities, the change set must contain the intermediate split/merge that explains the move

## Repair loop protocol

When validation fails, return errors to the model with this framing:

```
The change set you produced does not generate the output tree you proposed. Specifically:

<errors with line references>

Fix the change set so that it correctly produces the output tree. Don't change the output tree itself unless you've decided to revise your recommendation. Re-run validation when done.
```

Typically converges in 1–2 turns. If 5 turns without convergence, abort and surface to the human.

## Files

- `scripts/validate_ost.py` — the validator
- `references/ost-schema.json` — JSON Schema for tree and change-set shapes
- `references/action-vocabulary.md` — allowed actions and semantics
- `references/examples/` — input/output/change-set triples (valid + invalid)
