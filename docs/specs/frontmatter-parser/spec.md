# Spec: frontmatter-parser

- **Status:** Shipped
- **Plan:** [`plan.md`](./plan.md)
- **State:** [`state.json`](./state.json) (gitignored)
- **Component type:** script (shared library)
- **Serves kit phase:** Meta (kit infrastructure consumed by audits, hooks, classifiers)
- **Constrained by:** `.claude/skills/work-loop/SKILL.md`; `docs/CONVENTIONS.md` (universal metadata schema); `context/frameworks/ontology.md`; the existing inline parser in `tools/lint-frontmatter.py` (`_parse_yaml_subset`)

> **Spec contract.** Defines a robust YAML-subset parser for kit frontmatter, extracted from the rough inline version in `tools/lint-frontmatter.py`. Becomes the canonical parser every audit script and hook shells out to.

## Objective

Build `scripts/lib/frontmatter.py` — a stdlib-only Python module that parses the YAML-subset used by kit artifact frontmatter into typed Python objects. Today, `tools/lint-frontmatter.py:_parse_yaml_subset()` does this inline with known gaps (no inline lists, no `|` folding, brittle on quotes). Extracting it produces one tested implementation that the F1.4/F1.5/F1.6 audit scripts, F1.3 ontology-classifier skill, F2.x hooks, and any future component can import.

## Why now

Foundation 1's audits (F1.4-F1.6) all need to parse frontmatter to walk the typed-object graph. Without a shared parser, each script reinvents it (drift) or imports a heavy YAML library (deps bloat). The kit's existing `lint-frontmatter.py` has the rough version; promoting it is the cheapest unblock for everything downstream in F1.

## Inputs and outputs

**Inputs.**
- A string containing markdown frontmatter delimited by `---` lines, OR a `Path` to a `.md` file.
- The caller may pass the file path for error messages even when passing a string.

**Outputs.**
- Returns a `Frontmatter` dataclass exposing: `data: dict`, `raw_block: str`, `byte_range: tuple[int, int]`, `parse_errors: list[str]`.
- For `parse_file(path)`: returns the same `Frontmatter` object, or `None` if the file has NO frontmatter at all (no leading `---` line).
- **Tolerant on malformed:** an unclosed delimiter (leading `---` but no closing `---`) is NOT raised. Returns a `Frontmatter` with `data={}`, `raw_block=""`, and `parse_errors=["unclosed frontmatter delimiter"]`. Callers writing `if fm is None: skip` continue to behave correctly because they get a non-None object with empty data; callers wanting strict behavior check `fm.parse_errors`.
- `FrontmatterError` is reserved for I/O failures (e.g., file unreadable), not parse anomalies.

A caller should be able to: load a file, get `fm.data["object_type"]`, check `fm.parse_errors`, and round-trip-edit by substituting `fm.raw_block`.

**Coercion (explicit behavior change from `_parse_yaml_subset`):**
- Bare `true` / `false` → Python `bool`. Bare `null` → Python `None`. Bare integer literals → `int`. Quoted values always remain `str`. Everything else → `str`.
- This is a deliberate behavior delta from the old inline parser, which stored all scalars as strings (e.g., `human_approval_required: true` was stored as the string `"true"`). Task 3 must update `tools/lint-frontmatter.py` line ~144 to check `fm.get("human_approval_required") is True` (or `== True`) instead of `== "true"`. Document in the task's Tests section.

## Boundaries

### Always do
- Use stdlib only (`re`, `pathlib`, `dataclasses`, `typing`). No `pyyaml`, no `ruamel`, no external deps.
- Handle the constructs kit frontmatter uses (per `docs/CONVENTIONS.md`): scalars, **list-of-maps (depth 2 — required by `evidence_basis:` and `approvals_obtained:`)**, single-level nested maps, block lists (`- item`), inline lists (`[a, b, c]`), single and double quoted strings, multi-line scalars with `|` and `>`, comments (`# ...`), values containing spaces (e.g., `status: In Review`), values containing `|` literally (e.g., `ai_assistance_allowed: true | restricted | not-allowed` — distinguish from the `|` block-scalar marker which is alone on the right of `key:`), file paths in values (e.g., `parent_intent: ../intents/north-star.md`).
- Tolerate (don't fail) on: missing fields, unknown fields, extra whitespace, trailing commas in inline lists, **duplicate top-level keys (last-write-wins on data; append a non-fatal entry to `parse_errors`)**, **CRLF line endings (`\r\n`)**.
- Preserve the raw block string verbatim so callers can do round-trip edits.

### Ask first
- Adding support for YAML features beyond what kit frontmatter actually uses (anchors, tags, deeply nested structures). Default: not supported; surface as RFC.
- Returning anything other than `dict[str, Any]` for parsed data.

### Never do
- Take an external YAML dependency.
- Mutate the input string.
- Silently coerce values (e.g., string `"true"` → bool unless it's the YAML-correct unquoted `true` literal). Coercion rules are explicit and tested.
- Be permissive about delimiters — `---` on its own line, no leading whitespace; otherwise no frontmatter.

## Verification mode

- **TDD.** Unit tests under `scripts/tests/test_frontmatter.py` drive implementation. Tests cover: parse / round-trip / error / every supported YAML construct.
- **Goal-based check.** `tools/lint-frontmatter.py` migrated to use the new library; before/after behavior on every existing `.md` file with frontmatter is identical. This is the regression gate.

## Contract tests

Per-construct, each named by what it asserts:
- `test_parses_string_scalar`
- `test_parses_quoted_scalar` (single + double)
- `test_parses_int_and_bool_scalars`
- `test_parses_block_list`
- `test_parses_inline_list`
- `test_parses_nested_map_one_level`
- `test_preserves_comments_in_raw_block`
- `test_handles_pipe_literal_string`
- `test_handles_gt_folded_string`
- `test_raises_on_unclosed_frontmatter`
- `test_returns_none_on_no_frontmatter`
- `test_round_trip_preserves_byte_range`
- `test_collects_non_fatal_parse_errors`
- `test_bool_coercion_native` — `human_approval_required: true` parses as `True` (bool), not `"true"` (str).
- `test_existing_kit_files_parse_compatibly` — load every repo `.md` with frontmatter, parse with both old `_parse_yaml_subset` and new lib, then for every top-level key the OLD parser populated with a non-empty value, assert the new lib's value is either (a) identical, or (b) a more-precisely-typed version (bool / None / int instead of the string form, OR a populated dict where the old parser stored `[]` for nested maps it couldn't parse). The test enumerates the explicit acceptable upgrades; any unexpected divergence fails.
- `test_handles_windows_line_endings_crlf` — a file with `\r\n` endings parses correctly (split handles both).
- `test_handles_duplicate_keys_as_parse_error` — duplicate top-level keys collect a non-fatal entry in `parse_errors`; last-write-wins on the data dict.

The compat test (now widened to allow documented upgrades) is the regression gate.

## Non-goals

- General-purpose YAML parsing. Kit frontmatter only.
- Writing/serializing frontmatter beyond preserving the raw block.
- Schema validation (that's `lint-frontmatter.py`'s job; this lib gives it the parsed dict).
- Parsing the markdown body.

## Open questions

1. **`Frontmatter` as `@dataclass` or `TypedDict`?** Lean: dataclass — may want methods later.
2. **Error class location:** `scripts.lib.frontmatter.FrontmatterError`. Lean: yes.

## Acceptance criteria

- [ ] `scripts/lib/frontmatter.py` exists, stdlib-only, ≤ ~250 LOC.
- [ ] `scripts/lib/__init__.py` exists (minimal docstring).
- [ ] `scripts/tests/__init__.py` exists.
- [ ] `scripts/tests/test_frontmatter.py` exists; all listed contract tests pass.
- [ ] `python3 -m unittest scripts.tests.test_frontmatter` exits 0.
- [ ] Regression test: every existing kit `.md` with frontmatter parses identically under both the old and new parsers.
- [ ] `tools/lint-frontmatter.py` migrated to import `scripts.lib.frontmatter`; old `_parse_yaml_subset()` removed. `python3 tools/lint-frontmatter.py --all` returns the same exit code as before migration.
- [ ] PLAN/VERIFY/REVIEW gates via `tools/check-done.py` all exit 0.

## Cross-references

- **Consumed by:** F1.3, F1.4, F1.5, F1.6, F1.7, every future F2.x hook script.
- **Consumes:** stdlib only.
- **Frontmatter fields owned:** none.
- **Ontology object types touched:** none.
