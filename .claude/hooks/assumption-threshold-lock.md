# assumption-threshold-lock hook

The single most important guard in the kit. Refuses to write experiment results unless a falsification threshold was filed *before* the experiment ran.

This is what separates real validation from validation theatre.

## What it does

Registered as a `PreToolUse` hook matching `Write` operations on `validation/experiments/**/results.md`.

Before any such write succeeds, the hook runs `scripts/check-assumption-threshold.py`, which:

1. Locates the experiment's `experiment.md` design file in the same folder
2. Reads its frontmatter — must contain `predeclared_threshold:` with both `success:` and `falsification:` criteria
3. Confirms `predeclared_at:` is on or before today (rejects future-dated thresholds — the assumption can't be predeclared after the fact)
4. Confirms the design file's modification time predates the results-write event
5. If all checks pass, the write proceeds
6. If any fails, the write is blocked and the hook returns an error explaining what's missing

## Why this matters

Operating-model failure mode #4: **Validation theatre.** Running experiments after the build decision has been made. Validation only counts if the team will *pull the work* when the assumption fails.

The mechanical version of "would we pull the work?" is "did we declare what failure would look like *before* we ran the test?" If yes: real validation, real possibility of being wrong. If no: theatre.

This hook removes the theatre option. You can still skip validation — but you can't skip it and call it validation.

## How to write a results file that won't be blocked

The experiment design file (`experiment.md`) must exist first, with frontmatter:

```yaml
---
object_type: Experiment
slug: <experiment-id>
created: <YYYY-MM-DD>
parent_assumption: <assumption from the map>
predeclared_threshold:
  success: <quantitative criterion, e.g. "≥40% of test cohort completes the action">
  falsification: <quantitative criterion, e.g. "<15% completion → assumption killed">
predeclared_at: <YYYY-MM-DD>     # MUST be before the results-write
sample_target: <n>
duration: <days>
human_owned_decisions:
  - Threshold selection
  - Survived/killed call on ambiguous results
human_approval_required: true
---
```

Then run the experiment. Then file `results.md`. The hook will check that the design file existed first.

## What's NOT enforced

The hook only checks that *a* threshold was predeclared and the design file predates results. It doesn't audit whether the threshold was a *reasonable* threshold — that's a judgment call.

That judgment is what the `assumption-skeptic` agent is for. Run it before `/design-experiment` is finalized: "Would you actually pull the work at this threshold?" If the answer is no, the threshold is too lenient — back to theatre.

## Override

To override (rare — sometimes you need to capture results from a test that wasn't predeclared, e.g. an organic A/B discovered after the fact), set in the experiment design file:

```yaml
override_threshold_lock: true
override_reason: <one-paragraph explanation>
override_authorized_by: <name>
override_authorized_at: <YYYY-MM-DD>
```

The hook will allow the write but log it to `validation/experiments/OVERRIDE-LOG.md` and flag it permanently in the audit chain. Overrides accumulate; if the log gets long, post-hoc validation is happening across the board — which is itself a signal.

## Configuration

Wired in `.claude/settings.json` as of F2.6 (2026-05-21):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {"type": "command", "command": "python3 scripts/check-assumption-threshold.py"}
        ]
      }
    ]
  }
}
```

The script path-filters internally (it only acts when `tool_input.file_path` matches `validation/experiments/**/results.md`); no `matchPaths` filter is needed at the settings layer.

## Related

- `/design-experiment` — produces a compliant `experiment.md`
- `/run-assumption-test` — captures results in the format the hook expects
- `/audit-vision-evidence` — surfaces visions citing untested assumptions
- `assumption-skeptic` agent — theatre detector at the design stage
- `context/frameworks/validation-theatre.md` — the failure modes
