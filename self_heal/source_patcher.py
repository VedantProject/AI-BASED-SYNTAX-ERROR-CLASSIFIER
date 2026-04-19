"""
self_heal/source_patcher.py
============================
Low-level, line-oriented text-patching utilities used by the self-healing
engine.  All functions are pure (no side-effects) and work on *lists of
lines* (str, NO trailing newline per element).
"""

from __future__ import annotations
from typing import List


# ── Primitive patch operations ────────────────────────────────────────────────

def source_to_lines(source: str) -> List[str]:
    """Split source into lines preserving empty trailing line."""
    return source.splitlines()


def lines_to_source(lines: List[str]) -> str:
    """Rejoin lines into a single source string."""
    return "\n".join(lines)


def insert_at_line_end(lines: List[str], line_no: int, text: str) -> List[str]:
    """
    Insert *text* immediately before any trailing whitespace on line_no
    (1-indexed).  Returns a new list; original is not mutated.
    """
    lines = list(lines)
    idx = line_no - 1
    if 0 <= idx < len(lines):
        original = lines[idx]
        # Insert before trailing whitespace / comments
        stripped = original.rstrip()
        trailing = original[len(stripped):]
        lines[idx] = stripped + text + trailing
    return lines


def replace_on_line(lines: List[str], line_no: int,
                    old: str, new: str, count: int = 1) -> List[str]:
    """
    Replace the first *count* occurrences of *old* with *new* on line_no.
    1-indexed.  Returns a new list.
    """
    lines = list(lines)
    idx = line_no - 1
    if 0 <= idx < len(lines):
        lines[idx] = lines[idx].replace(old, new, count)
    return lines


def replace_line(lines: List[str], line_no: int, new_line: str) -> List[str]:
    """Replace the entire contents of line_no (1-indexed)."""
    lines = list(lines)
    idx = line_no - 1
    if 0 <= idx < len(lines):
        lines[idx] = new_line
    return lines


def reindent_line(lines: List[str], line_no: int,
                  target_spaces: int) -> List[str]:
    """
    Re-indent line_no to *target_spaces* spaces.
    All existing leading whitespace is replaced.  1-indexed.
    """
    lines = list(lines)
    idx = line_no - 1
    if 0 <= idx < len(lines):
        content = lines[idx].lstrip()
        lines[idx] = " " * target_spaces + content
    return lines


def tabs_to_spaces(lines: List[str], line_no: int,
                   spaces_per_tab: int = 4) -> List[str]:
    """Convert leading tabs to spaces on line_no (1-indexed)."""
    lines = list(lines)
    idx = line_no - 1
    if 0 <= idx < len(lines):
        line = lines[idx]
        result = []
        for ch in line:
            if ch == "\t":
                result.append(" " * spaces_per_tab)
            elif ch == " ":
                result.append(ch)
            else:
                result.append(line[len("".join(result)):])
                break
        else:
            lines[idx] = "".join(result)
            return lines
        # Reconstruct: leading part converted + rest unchanged
        leading = ""
        for ch in line:
            if ch == "\t":
                leading += " " * spaces_per_tab
            elif ch == " ":
                leading += " "
            else:
                break
        lines[idx] = leading + line.lstrip()
    return lines


def infer_indent_level(lines: List[str], line_no: int) -> int:
    """
    Guess the correct indentation for line_no by looking at the previous
    non-blank line.  If that line ends with ':', we add one level (4 spaces).
    Otherwise we match the previous line's indentation.
    Returns the number of spaces.
    """
    idx = line_no - 1
    # Scan backwards for previous non-blank line
    for i in range(idx - 1, -1, -1):
        prev = lines[i]
        if prev.strip():
            prev_indent = len(prev) - len(prev.lstrip())
            if prev.rstrip().endswith(":"):
                return prev_indent + 4
            return prev_indent
    return 0


def append_line_after(lines: List[str], line_no: int,
                      new_line: str) -> List[str]:
    """Insert *new_line* immediately after line_no (1-indexed)."""
    lines = list(lines)
    lines.insert(line_no, new_line)
    return lines
