#!/usr/bin/env bash
# test-settings-json.sh — contract tests for .claude/settings.json (F2.6).
#
# Validates that the hook-wiring file matches the canonical Claude Code
# hook-entry schema and that every shipped F2 hook script is registered.
#
# Does NOT use `set -e` — each test runs independently; failures accumulate
# in FAILED and are reported in one run.

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

SETTINGS=".claude/settings.json"
FAILED=0

pass() { echo "✓ $1"; }
fail() { echo "✗ $1: $2" >&2; FAILED=$((FAILED + 1)); }

# expect_jq <name> <jq-filter> — passes if `jq -e <filter>` succeeds on SETTINGS.
expect_jq() {
    local name="$1" filter="$2"
    if jq -e "$filter" "$SETTINGS" >/dev/null 2>&1; then
        pass "$name"
    else
        fail "$name" "jq -e '$filter' did not succeed"
    fi
}

test_settings_file_exists() {
    if [[ -f "$SETTINGS" ]]; then pass "test_settings_file_exists"
    else fail "test_settings_file_exists" "$SETTINGS not found"; fi
}

test_settings_is_valid_json() {
    if jq -e . "$SETTINGS" >/dev/null 2>&1; then pass "test_settings_is_valid_json"
    else fail "test_settings_is_valid_json" "$SETTINGS is not valid JSON"; fi
}

test_has_session_start_array() {
    expect_jq "test_has_session_start_array" '.hooks.SessionStart | type == "array"'
}

test_has_user_prompt_expansion_array() {
    expect_jq "test_has_user_prompt_expansion_array" '.hooks.UserPromptExpansion | type == "array"'
}

test_has_pre_tool_use_array() {
    expect_jq "test_has_pre_tool_use_array" '.hooks.PreToolUse | type == "array"'
}

test_every_entry_uses_canonical_hooks_shape() {
    # Every event entry must have a `hooks` array; each element must be
    # {type: "command", command: <string>}. No shorthand `{matcher, command}` siblings.
    expect_jq "test_every_entry_uses_canonical_hooks_shape" '
        .hooks | to_entries | all(.value | type == "array" and all(
            .hooks | type == "array" and all(
                .type == "command" and (.command | type == "string")
            )
        ))
    '
}

test_no_matchPaths_field() {
    # `matchPaths` is not in the documented schema. Assert no nested object has it.
    expect_jq "test_no_matchPaths_field" '[.. | objects | has("matchPaths")] | any | not'
}

test_every_command_script_exists() {
    # Extract every command string, derive scripts/<name>.py paths, assert each exists.
    local missing=0
    while IFS= read -r cmd; do
        # Pull the scripts/<name>.py token from the command.
        local script
        script=$(echo "$cmd" | grep -oE 'scripts/[a-z_-]+\.py' | head -1)
        if [[ -z "$script" ]]; then
            fail "test_every_command_script_exists" "command lacks scripts/<name>.py: $cmd"
            missing=$((missing + 1))
            continue
        fi
        if [[ ! -f "$script" ]]; then
            fail "test_every_command_script_exists" "referenced script not on disk: $script"
            missing=$((missing + 1))
        fi
    done < <(jq -r '[.. | .command? // empty] | .[]' "$SETTINGS")
    if [[ "$missing" -eq 0 ]]; then pass "test_every_command_script_exists"; fi
}

test_guard_credentials_matcher_covers_all_io_tools() {
    expect_jq "test_guard_credentials_matcher_covers_all_io_tools" '
        .hooks.PreToolUse[] | select(.hooks[].command | test("guard-credentials\\.py")) | .matcher == "Bash|Write|Edit|MultiEdit|Read"
    '
}

test_check_handover_link_wired_to_write_edit_multiedit() {
    expect_jq "test_check_handover_link_wired_to_write_edit_multiedit" '
        .hooks.PreToolUse[] | select(.hooks[].command | test("check-handover-link\\.py")) | .matcher == "Write|Edit|MultiEdit"
    '
}

test_check_ontology_type_wired_to_write_edit_multiedit() {
    expect_jq "test_check_ontology_type_wired_to_write_edit_multiedit" '
        .hooks.PreToolUse[] | select(.hooks[].command | test("check-ontology-type\\.py")) | .matcher == "Write|Edit|MultiEdit"
    '
}

test_assumption_threshold_wired_to_write_only() {
    expect_jq "test_assumption_threshold_wired_to_write_only" '
        .hooks.PreToolUse[] | select(.hooks[].command | test("check-assumption-threshold\\.py")) | .matcher == "Write"
    '
}

test_mode_guard_wired_to_three_events() {
    expect_jq "test_mode_guard_wired_to_three_events" '
        (.hooks.SessionStart[]?.hooks[]?.command | select(. | test("mode-guard\\.py"))) and
        (.hooks.UserPromptExpansion[]?.hooks[]?.command | select(. | test("mode-guard\\.py"))) and
        (.hooks.PreToolUse[]? | select(.matcher == "Skill") | .hooks[].command | test("mode-guard\\.py"))
    '
}

test_cadence_nudge_wired_to_session_start() {
    expect_jq "test_cadence_nudge_wired_to_session_start" '
        [.hooks.SessionStart[]?.hooks[]?.command | select(. | test("cadence-nudge\\.py"))] | length > 0
    '
}

test_settings_file_exists
test_settings_is_valid_json
test_has_session_start_array
test_has_user_prompt_expansion_array
test_has_pre_tool_use_array
test_every_entry_uses_canonical_hooks_shape
test_no_matchPaths_field
test_every_command_script_exists
test_guard_credentials_matcher_covers_all_io_tools
test_check_handover_link_wired_to_write_edit_multiedit
test_check_ontology_type_wired_to_write_edit_multiedit
test_assumption_threshold_wired_to_write_only
test_mode_guard_wired_to_three_events
test_cadence_nudge_wired_to_session_start

if [[ "$FAILED" -gt 0 ]]; then
    echo "" >&2
    echo "test-settings-json: $FAILED test(s) failed" >&2
    exit 1
fi

echo "test-settings-json: all 14 tests passed"
exit 0
