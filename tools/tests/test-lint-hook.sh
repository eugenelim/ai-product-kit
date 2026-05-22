#!/usr/bin/env bash
# test-lint-hook.sh — contract tests for tools/lint-hook.sh
#
# Per spec §Contract tests. Does NOT use `set -e` — each test runs
# independently, failures accumulate in FAILED, and the harness exits
# with FAILED at the end so all failing tests are visible in one run.

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

LINT="tools/lint-hook.sh"
FIX="tools/tests/fixtures/lint-hook"
FAILED=0

# pass <name>: print a PASS line.
pass() {
    echo "✓ $1"
}

# fail <name> <reason>: print a FAIL line and bump FAILED.
fail() {
    echo "✗ $1: $2" >&2
    FAILED=$((FAILED + 1))
}

# expect_exit <name> <expected-code> <stderr-substring-or-empty> <command...>
# Runs the command, captures exit + stderr, compares.
expect_exit() {
    local name="$1" expected="$2" substr="$3"
    shift 3
    local stderr_file
    stderr_file=$(mktemp)
    "$@" 2>"$stderr_file"
    local actual=$?
    local stderr
    stderr=$(cat "$stderr_file")
    rm -f "$stderr_file"
    if [[ "$actual" -ne "$expected" ]]; then
        fail "$name" "expected exit $expected, got $actual; stderr: $stderr"
        return
    fi
    if [[ -n "$substr" && "$stderr" != *"$substr"* ]]; then
        fail "$name" "expected stderr to contain '$substr', got: $stderr"
        return
    fi
    pass "$name"
}

test_passes_on_assumption_threshold_lock_doc() {
    expect_exit "test_passes_on_assumption_threshold_lock_doc" 0 "" \
        bash "$LINT" .claude/hooks/assumption-threshold-lock.md
}

test_passes_on_good_fixture() {
    expect_exit "test_passes_on_good_fixture" 0 "" \
        bash "$LINT" "$FIX/good.md"
}

test_fails_on_missing_h1() {
    expect_exit "test_fails_on_missing_h1" 1 "H1" \
        bash "$LINT" "$FIX/missing-h1.md"
}

test_fails_on_missing_what_it_does() {
    expect_exit "test_fails_on_missing_what_it_does" 1 "What it does" \
        bash "$LINT" "$FIX/missing-what.md"
}

test_fails_on_missing_why_this_matters() {
    expect_exit "test_fails_on_missing_why_this_matters" 1 "Why this matters" \
        bash "$LINT" "$FIX/missing-why.md"
}

test_fails_on_missing_configuration() {
    expect_exit "test_fails_on_missing_configuration" 1 "Configuration" \
        bash "$LINT" "$FIX/missing-config.md"
}

test_fails_on_h1_not_matching_hook_pattern() {
    expect_exit "test_fails_on_h1_not_matching_hook_pattern" 1 "H1" \
        bash "$LINT" "$FIX/wrong-h1.md"
}

test_fails_on_empty_slug_h1() {
    expect_exit "test_fails_on_empty_slug_h1" 1 "H1" \
        bash "$LINT" "$FIX/empty-slug-h1.md"
}

test_usage_error_on_no_args() {
    expect_exit "test_usage_error_on_no_args" 2 "usage" \
        bash "$LINT"
}

test_error_on_missing_file() {
    expect_exit "test_error_on_missing_file" 1 "file not found" \
        bash "$LINT" "$FIX/does-not-exist.md"
}

test_soft_warns_on_long_body() {
    expect_exit "test_soft_warns_on_long_body" 0 "WARN" \
        bash "$LINT" "$FIX/long.md"
}

test_passes_on_assumption_threshold_lock_doc
test_passes_on_good_fixture
test_fails_on_missing_h1
test_fails_on_missing_what_it_does
test_fails_on_missing_why_this_matters
test_fails_on_missing_configuration
test_fails_on_h1_not_matching_hook_pattern
test_fails_on_empty_slug_h1
test_usage_error_on_no_args
test_error_on_missing_file
test_soft_warns_on_long_body

if [[ "$FAILED" -gt 0 ]]; then
    echo "" >&2
    echo "test-lint-hook: $FAILED test(s) failed" >&2
    exit 1
fi

echo "test-lint-hook: all tests passed"
exit 0
