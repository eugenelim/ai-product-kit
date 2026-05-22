# hook

## What it does

Tests the H1 rule: a literal `# hook` line with no slug between `#` and `hook` is rejected (the regex `^# .+ hook$` requires non-empty slug).

## Why this matters

Without a slug, the H1 doesn't identify which hook is documented.

## Configuration

(none)
