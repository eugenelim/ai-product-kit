"""Kit-frontmatter parser (F1.2).

Stdlib-only YAML-subset parser for the constructs the kit's frontmatter uses.
Documented constructs (per docs/CONVENTIONS.md):
  - Scalars (str, int, bool, null) with native Python coercion for unquoted
    `true` / `false` / `null` / integer literals.
  - Block lists (`- item`) and inline lists (`[a, b, c]`).
  - Single-level nested maps; list-of-maps at depth 2 (e.g., evidence_basis).
  - Single- and double-quoted strings (no mangling on quote-containing values).
  - Multi-line scalars: `|` literal and `>` folded.
  - Comments (`# ...`).
  - Values containing spaces and `|` literals.
  - CRLF line endings.

Behavior deltas vs the old tools/lint-frontmatter.py:_parse_yaml_subset:
  - Unquoted `true` / `false` / `null` / integers are coerced to native Python
    types (old parser stored all as strings).
  - Inline-list values are parsed into Python lists (old parser stored the raw
    string).
  - Quoted values with both quote types are preserved correctly (old parser's
    `strip('"').strip("'")` mangled them).
  - Unclosed delimiters are tolerated: returns a Frontmatter with empty data and
    a parse_errors entry rather than returning None (old) or raising.
  - Duplicate top-level keys: last-write-wins on data; non-fatal parse_errors
    entry.

Public API:
  parse(source: str) -> Optional[Frontmatter]
  parse_file(path: Path) -> Optional[Frontmatter]
  Frontmatter (dataclass)
  FrontmatterError (reserved for I/O failures; never raised on parse anomalies)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


class FrontmatterError(Exception):
    """Reserved for I/O failures (file unreadable). Not raised on parse anomalies."""


@dataclass
class Frontmatter:
    data: dict[str, Any]
    raw_block: str
    byte_range: tuple[int, int]
    parse_errors: list[str] = field(default_factory=list)


_DELIM = "---"


def parse(source: str) -> Optional[Frontmatter]:
    """Parse a markdown string with leading frontmatter.

    Returns None if no leading frontmatter delimiter is present.
    Returns a Frontmatter with empty data + parse_errors entry if the
    frontmatter is unclosed.
    """
    if source is None:
        return None
    # Normalize CRLF to LF for delimiter detection; preserve original for byte_range.
    if not (source.startswith(_DELIM + "\n") or source.startswith(_DELIM + "\r\n")):
        return None

    # Find the closing delimiter line.
    # We accept "\n---\n" or "\r\n---\r\n" as the closing.
    # Search starting after the opening delimiter line.
    open_len = 4 if source.startswith(_DELIM + "\n") else 5  # "---\n" or "---\r\n"
    rest = source[open_len:]

    # Look for "\n---\n", "\n---\r\n", or end-of-string "\n---" as closing.
    pattern = re.compile(r"(?:\r?\n)---(?:\r?\n|$)")
    m = pattern.search(rest)
    if not m:
        # Unclosed — tolerate
        return Frontmatter(
            data={},
            raw_block="",
            byte_range=(0, 0),
            parse_errors=["unclosed frontmatter delimiter"],
        )

    block_start = open_len
    block_end = open_len + m.start()
    block_str = source[block_start:block_end]
    # byte_range covers the inner block (matches raw_block exactly); callers
    # who need the delimiter positions can derive them (block_start - open_len
    # for the opening, block_end + closing-len for the closing).
    fm_byte_range = (block_start, block_end)

    data, errors = _parse_block(block_str)
    return Frontmatter(
        data=data, raw_block=block_str, byte_range=fm_byte_range, parse_errors=errors
    )


def parse_file(path: Path) -> Optional[Frontmatter]:
    """Read a file and parse its frontmatter. Returns None if no frontmatter."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise FrontmatterError(f"cannot read {path}: {e}") from e
    return parse(text)


# --- Internals --------------------------------------------------------------


_BOOL_NULL = {"true": True, "false": False, "null": None, "~": None}
_INT_RE = re.compile(r"^-?\d+$")
_INLINE_LIST_RE = re.compile(r"^\[(.*)\]$")
_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$")


def _coerce_scalar(val: str) -> Any:
    """Coerce an unquoted scalar value to a native Python type."""
    if val == "":
        return ""
    # Quoted? Strip exactly one matching pair.
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
        return val[1:-1]
    low = val.lower()
    if low in _BOOL_NULL:
        return _BOOL_NULL[low]
    if _INT_RE.match(val):
        return int(val)
    return val


def _parse_inline_list(content: str) -> list[Any]:
    """Parse `[a, b, c]` body (content between brackets) into a Python list.

    Known limitation: items containing commas inside quotes (e.g.,
    `["a, b", "c"]`) are split incorrectly. The kit's frontmatter does not
    use comma-containing inline-list items today; if a future artifact needs
    them, switch this to a small CSV-aware splitter or use block-list syntax.
    """
    items: list[Any] = []
    if not content.strip():
        return items
    # Naive split on commas — good enough for the kit's flat-string usage.
    parts = [p.strip() for p in content.split(",")]
    # Drop trailing empty (handles trailing comma)
    if parts and parts[-1] == "":
        parts = parts[:-1]
    for p in parts:
        items.append(_coerce_scalar(p))
    return items


def _strip_comment(line: str) -> str:
    """Strip an end-of-line comment if present.

    Honors quoted contexts: `key: "# not a comment"` keeps the # inside the value.
    """
    in_single = False
    in_double = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            return line[:i].rstrip()
    return line


def _split_lines(block: str) -> list[str]:
    """Split a block on \\n or \\r\\n, dropping the trailing empty line if any."""
    # str.splitlines handles both LF and CRLF
    return block.splitlines()


def _parse_block(block: str) -> tuple[dict[str, Any], list[str]]:
    """Line-by-line state machine for the YAML-subset.

    Handles:
      - Top-level `key: value` scalars (with coercion).
      - Top-level `key:` followed by indented block (list, inline list at value
        position, or nested map at one level, or list-of-maps at depth 2).
      - Top-level `key: |` and `key: >` multi-line strings.
      - Comments and blank lines.
    """
    out: dict[str, Any] = {}
    errors: list[str] = []
    lines = _split_lines(block)

    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped_for_comment = _strip_comment(raw)
        # Blank or pure comment? skip
        if not stripped_for_comment.strip():
            i += 1
            continue

        # Top-level (no leading spaces) key?
        if raw.startswith(" ") or raw.startswith("\t"):
            # Unexpected indented content at top level — record and skip
            errors.append(f"unexpected indented line at top level: {raw!r}")
            i += 1
            continue

        m = _KEY_RE.match(stripped_for_comment)
        if not m:
            errors.append(f"could not parse top-level line: {raw!r}")
            i += 1
            continue

        key, val = m.group(1), m.group(2).rstrip()

        if key in out:
            errors.append(f"duplicate top-level key: {key!r} (last value wins)")

        # Case A: value is `|` or `>` (multi-line string)
        if val in ("|", ">"):
            mode = val
            multi_lines: list[str] = []
            i += 1
            while i < len(lines):
                ln = lines[i]
                if not ln.startswith(" ") and not ln.startswith("\t"):
                    break
                # Strip the leading indent (2 spaces, conventionally)
                content = ln[2:] if ln.startswith("  ") else ln.lstrip()
                multi_lines.append(content)
                i += 1
            if mode == "|":
                out[key] = "\n".join(multi_lines).rstrip()
            else:  # ">"
                out[key] = " ".join(s for s in multi_lines if s.strip()).strip()
            continue

        # Case B: value is empty → look ahead for block list, nested map, or list-of-maps
        if val == "":
            # Inspect next non-blank, non-comment indented line
            j = i + 1
            # Skip blank / comment lines
            while j < len(lines) and not _strip_comment(lines[j]).strip():
                j += 1
            if j >= len(lines) or not (
                lines[j].startswith(" ") or lines[j].startswith("\t")
            ):
                # Empty value, no indented continuation → empty list (conservative)
                out[key] = []
                i = j
                continue

            next_line = lines[j].rstrip()
            # Is it a list-of-maps? First child starts with `  - ` and there is a
            # following key under the same indent.
            if next_line.lstrip().startswith("- "):
                items, consumed = _parse_block_list(lines, j)
                out[key] = items
                i = consumed
                continue
            # Otherwise, it's a nested map (single level)
            nested, consumed = _parse_nested_map(lines, j)
            out[key] = nested
            i = consumed
            continue

        # Case C: value is `[ ... ]` inline list
        ilm = _INLINE_LIST_RE.match(val)
        if ilm:
            out[key] = _parse_inline_list(ilm.group(1))
            i += 1
            continue

        # Case D: scalar
        out[key] = _coerce_scalar(val)
        i += 1

    return out, errors


def _parse_block_list(lines: list[str], start: int) -> tuple[list[Any], int]:
    """Parse a `  - item` block list starting at index `start`. Returns (list, next_index).

    Each item may be a scalar (`  - foo`) or a map (`  - source: x\\n    strength: y`).
    """
    items: list[Any] = []
    i = start
    while i < len(lines):
        ln = lines[i]
        # Skip blank lines within a block list (per spec "tolerate extra whitespace").
        if not ln.strip():
            i += 1
            continue
        if not (ln.startswith("  - ") or ln == "  -"):
            # End of block list
            break
        # Strip the `  - ` prefix
        item_first = ln[4:] if ln.startswith("  - ") else ""
        # Is the first content a `key: value` pair? Then this list item is a map.
        if item_first and ":" in item_first and not item_first.startswith("["):
            # Map item — collect this line's key/val plus any continuation lines
            # at 4-space indent until the next `  - ` or dedent.
            item_map: dict[str, Any] = {}
            # Parse the first line's key/value
            m = _KEY_RE.match(item_first)
            if m:
                item_map[m.group(1)] = _coerce_scalar(m.group(2).rstrip())
            i += 1
            while i < len(lines):
                cont = lines[i]
                if cont.startswith("    "):  # 4-space continuation
                    cont_stripped = _strip_comment(cont[4:])
                    if cont_stripped.strip():
                        m2 = _KEY_RE.match(cont_stripped)
                        if m2:
                            item_map[m2.group(1)] = _coerce_scalar(
                                m2.group(2).rstrip()
                            )
                    i += 1
                else:
                    break
            items.append(item_map)
            continue
        # Scalar item
        items.append(_coerce_scalar(item_first))
        i += 1
    return items, i


def _parse_nested_map(lines: list[str], start: int) -> tuple[dict[str, Any], int]:
    """Parse a `  key: value` nested map starting at index `start`. Returns (dict, next_index)."""
    out: dict[str, Any] = {}
    i = start
    while i < len(lines):
        ln = lines[i]
        if not ln.startswith("  ") or ln.startswith("  - "):
            break
        stripped = _strip_comment(ln[2:])
        if not stripped.strip():
            i += 1
            continue
        m = _KEY_RE.match(stripped)
        if m:
            out[m.group(1)] = _coerce_scalar(m.group(2).rstrip())
        i += 1
    return out, i
